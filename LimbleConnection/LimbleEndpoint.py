from __future__ import annotations

import json
from typing import Optional

import pandas as pd
import requests

# from LimbleConnection import LimbleConnection
from LimbleConnection.util import div_pattern


class LimbleEndpoint:
    """Represents an API endpoint for the Limble CMMS system.

    This class handles communication with a specific API endpoint, providing
    methods for data retrieval and conversion.

    Attributes:
        parent (LimbleConnection): The parent connection object managing the API.
        rt_addr (str): The full route address of the API endpoint.
        epoch_columns (list): A list of column names containing epoch timestamps
            that can be converted to datetime objects.
    """

    def __init__(self, connection, endpoint_name, rt_addr):
        """Initializes a LimbleEndpoint instance.

        Args:
            connection: LimbleConnection, The parent connection instance.
            endpoint_name: str, the breadcrumbs like path representing the endpoint url.
            rt_addr: str, The full route address for this endpoint.
        """
        self.name = endpoint_name  # TODO: added for custom handling of specifics; ex: users.teams.add
        self.connection = connection
        self.rt_addr = rt_addr

        self.epoch_columns = [
            'createdDate', 'startDate', 'due', 'dateCompleted', 'lastEdited',
            'startedOn', 'lastEdited', 'dateAdded'
        ]

        # placeholders - these unfortunately show in every LimbleEndpoint in IDE type resolution/autocomplete
        self.categories: Optional[LimbleEndpoint] = None
        self.fields: Optional[LimbleEndpoint] = None
        self.history: Optional[LimbleEndpoint] = None
        self.labor: Optional[LimbleEndpoint] = None
        self.suggested: Optional[LimbleEndpoint] = None
        self.teams: Optional[LimbleEndpoint] = None

        if self.name == 'users':
            self.get_user_id_from_username = self._get_user_id_from_username
        else:
            del self.teams

        if self.name == 'users.teams':
            self.get_team_members = self._get_team_members
            self.add_team = self._add_team
            self.remove_team = self._remove_team_from_user

    def _add_team(self, username: str = None, team: str = None, location: str = None, user_id: int = None,
                  team_id: int = None, location_id: int = None):
        """Add a team (membership) to user.

        :param username: str, the username of the team member.
        :param team: str, the team name.
        :param location: str, the location of the team.
        :param team_id: int, the teamID of the team.
        :param user_id: int, the userID of the user.
        :param location_id: int, the locationID of the team.
        :return: requests.Response
        """
        location_id, team_id, user_id = self._ensure_parameters_for_user_add_or_remove_team(team, username, location, team_id,
                                                                                            user_id, location_id)
        # make the put request
        add_response = self._add_team_to_user_put_request(user_id, team_id, location_id)
        return add_response  # todo: for dev

    def _add_team_to_user_put_request(self, user_id: int, team_id: int, location_id: int) -> requests.Response:
        """Send the PUT request to the Limble API to add a team to user.

        :param team_id: int, the teamID of the team.
        :param user_id: int, the userID of the user.
        :param location_id: int, the locationID of the team.
        :return: requests.Response, The PUT response object.
        """
        user_teams_address = (f'{self.connection.api_base_address}/{self.connection.api_version}/'
                              f'users/{user_id}/teams')
        payload = json.dumps({'teamID': int(team_id), 'locationID': int(location_id)})
        headers_add = self.connection.authentication_header | {'Content-Type': 'application/json'}
        add_response = requests.put(url=user_teams_address, proxies=self.connection.proxy, headers=headers_add,
                                    data=payload)
        if add_response.status_code != 200:
            if add_response.status_code == 409:
                print('This should be a log statement that the user already is added to that team!')
            else:
                raise ConnectionError(add_response.status_code)
        return add_response

    def _ensure_parameters_for_user_add_or_remove_team(self, team=None, username=None, location=None, team_id=None, user_id=None,
                                                       location_id=None):
        """Make sure that the required parameters to add a user to a team are known.

        One each of a name or id is required for the user and the team. Without them there is no way to know what to do.
        For location an attempt will be made to discover the id if the team is uniquely identifiable. Any non-id number
        parameters will potentially require additional Limble API calls.

        :param team: str, the team name.
        :param username: str, the username of the team member.
        :param location: str, the location of the team.
        :param location_id: int, the locationID of the team.
        :param team_id: int, the teamID of the team.
        :param user_id: int, the userID of the user.
        :return: tuple[int, int, int], the id numbers for the location, team, and user.
        """
        # without these there's no way
        if username is None and user_id is None:
            raise ValueError("Either username or user_id must be provided.")
        if team is None and team_id is None:
            raise ValueError("Either team or team_id must be provided.")

        # look these up
        if user_id is None and username is not None:  # look up user_id
            user_id = self.connection.users._get_user_id_from_username(username)
        if location_id is None and location is not None:
            location_id = self.connection.locations.df.set_index('name').loc[location,'locationID']
        if team_id is None and team is not None:
            team_id, location_id = self._get_team_id(team, location_id)
        if location_id is None and team_id is not None:
            location_id = self.connection.teams.df.set_index('teamID').loc[team_id, 'locationID']
        return location_id, team_id, user_id

    def _get_user_id_from_username(self, username: str) -> int:
        """Get the userID from the username by looking up the users in the Limble API. Case insensitive.

        :param username: str, the username of the user.
        :return: int, the userID of the user.
        """
        udf = self.connection.users.df.copy()
        udf.loc[:, 'username_lower'] = udf['username'].str.lower()
        user_id = udf.set_index('username_lower').loc[username.lower(), 'userID']
        return user_id

    def _get_team_id(self, team:str, location_id:int=None) -> tuple[int, int]:
        """Get the team id from the team name and possibly location ID.

        If there are multiple teams across locations with the same name, then location is required.
        If the team has a unique name across all locations, then location will be determined from the team and returned.

        :param team: str, the name of the team.
        :param location_id: int, the locationID for the location of the team.
        :return: tuple[int, int], the team id and location ID.
        """
        team_df = self.connection.teams.df
        this_team_df = team_df[team_df['name_clean'] == team]
        if this_team_df.empty:
            raise ValueError('There are no teams by that name.')  # todo: suggest close match? "Did you mean...?"
        elif this_team_df.shape[0] > 1:  # there are multiple teams across locations by that name
            try:
                location_id = self.connection.location_id if location_id is None else location_id
                this_team_df = this_team_df[this_team_df['locationID'] == location_id]
            except AttributeError as atterr:
                if str(atterr).startswith('Multiple locations are available'):
                    raise ValueError(f'There are multiple teams by the name "{team}". Please provide a location.')
                else:
                    raise atterr
            if this_team_df.empty:  # todo: suggest close match or one by that name at another location?
                raise ValueError(f'There are no teams named "{team}" at this location: {self.connection.location}')
        this_team = this_team_df.set_index('name_clean').loc[team]  # can probably just .loc[0, team]
        team_id = this_team['teamID']
        location_id = this_team['locationID']
        return team_id, location_id

    def _remove_team_from_user_del_request(self, user_id: int, team_id: int, location_id: int) -> requests.Response:
        """Remove a team member from a team Limble team.

        :param user_id: int, the userID of the user.
        :param team_id: int, the teamID of the team to remove the user from.
        :param location_id: int, the locationID of the team to remove the user from.
        :return: requests.Response, the response object from the API call.
        """
        user_teams_address = (f'{self.connection.api_base_address}/{self.connection.api_version}/'
                              f'users/{user_id}/teams')
        payload = json.dumps({'teamID': int(team_id), 'locationID': int(location_id)})
        headers_add = self.connection.authentication_header | {'Content-Type': 'application/json'}
        add_response = requests.delete(url=user_teams_address, proxies=self.connection.proxy,
                                       headers=headers_add, data=payload)
        if add_response.status_code != 200:
            if add_response.status_code == 404:
                print('This should be a log statement that the user is not on that team!')
            elif add_response.status_code == 400:
                print('This should be a log statement that the user is already on that team!')
            else:
                raise ConnectionError(add_response.status_code)
        return add_response

    def _remove_team_from_user(self, username: str = None, team: str = None, location: str = None, user_id: int = None,
                               team_id: int = None, location_id: int = None) -> requests.Response:
        """Remove a team member from a team Limble team.

        :param username: str, the username of the team member.
        :param team: str, the team name.
        :param location: str, the location of the team.
        :param user_id: int, the userID of the user to remove the team from.
        :param team_id: int, the teamID of the team.
        :param location_id: int, the locationID of the team.
        :return: requests.Response
        """
        print(f'add_team connection: {id(self.connection)=}')
        location_id, team_id, user_id = self._ensure_parameters_for_user_add_or_remove_team(team, username, location, team_id,
                                                                                            user_id, location_id)
        # make the put request
        add_response = self._remove_team_from_user_del_request(user_id, team_id, location_id)
        return add_response  # for development

    def _get_team_members(self, team:str, location:str=None, team_id: int = None, location_id:int=None):
        """Get the members of a team.

        :param team: str, the team name.
        :param location: str, the location of the team.
        :param team_id: int, the teamID of the team.
        :param location_id: int, the locationID of the team.
        :return:
        """
        if location_id is None:
            if location is None:  # provided no parameters, try to use default
                location_id = self.connection.location_id
            else:
                locations_df = self.connection.locations.df
                location_id = locations_df.loc[
                    locations_df.loc[locations_df['name'] == location].index[0], 'locationID']

        else:
            locations_df = self.connection.locations.df
            location_id = locations_df.loc[locations_df.loc[locations_df['name'] == location].index[0], 'locationID']

        teams_df = self.connection.teams.df
        loc_teams = teams_df.loc[teams_df['locationID'] == location_id]

        this_team_dicts = loc_teams[loc_teams['name_clean'] == team].to_dict(orient='records')
        if this_team_dicts:
            this_team =  this_team_dicts[0]
        else:
            raise AttributeError(f'Team "{team}" not found.')

        team_id = this_team['teamID']
        users_df = self.connection.users.df
        return users_df.loc[users_df['teams'].apply(lambda x: any([tid['teamID'] == team_id for tid in x]))]

    # @cached(cache=TTLCache(maxsize=100, ttl=api_cache_lifetime_seconds))  # currently causing an issue with rq_params
    def request_params(self, *args, **kwargs):
        """Makes a GET request to the API endpoint allowing the use of parameters and retrieves data.

        Args:
            *args: Positional arguments passed to the `requests.get` function.
            **kwargs: Keyword arguments, including:
                - rq_params (dict, optional): Additional query parameters for the request, see Limble API docs.
                - auto_page_all (bool, optional): Overrides the parent's setting for automatic pagination.
                - path_param (str, optional): for accessing endpoints that have a path parameter
                    ex: users/123/teams where 123 is userID
                    !: optional in that not all end points need one, the ones that do _require_ it.

        Examples:
            Example getting only page 2 of the assets list:

            >>>lc = LimbleConnection()
            >>>lc.assets.request_params(rq_params={'page': 2})
            [{'assetID': 101, 'name': 'Coating Line', 'startedOn': 1727890475, 'lastEdited': 1732230980,
            'parentAssetID': 0, 'locationID': 8675309, 'geoLocation': None, 'hoursPerWeek': 0,
            'meta': {'fields': '/v2/assets/fields/?assets=98', 'tasks': '/v2/tasks/?assets=98'},
            'workRequestPortal': 'https://app.limblecmms.com/problem/..., 'image': []}, ...]

        Returns:
            list: A list of results returned by the API.
        """
        params = kwargs.pop('rq_params', None)

        # why: the Limble API will by default only send 100 results at a time (or the limit parameter)
        # if provided parameter use that, otherwise the setting for the connection
        if (auto_page_all := kwargs.get('auto_page_all')) is None:
            auto_page_all = self.connection.auto_page_all
        else:
            del kwargs['auto_page_all']

        if any(self.rt_addr.endswith(end) for end in ('users', 'teams')):
            auto_page_all = None  # these do not support the page parameter

        # for accessing endpoints that have a path parameter; ex: users/123/teams where 123 is userID
        if (path_param := kwargs.get('path_param')) is not None:
            this_address = self.rt_addr.format(path_param=path_param)
            del kwargs['path_param']
        else:
            this_address = self.rt_addr

        if auto_page_all:
            result_data = []
            results_returned = True
            page_number = 0

            if params is None:
                params = {}

            while results_returned:
                page_number += 1
                print(f'Requesting {self.name} page number {page_number} - results so far: {len(result_data)}')
                params['page'] = page_number
                page_data = self._get_request(params, this_address).json()
                if not page_data:
                    results_returned = False
                else:
                    result_data += page_data
        else:
            result_data = self._get_request(params, this_address).json()
        return result_data

    # @cached(cache=TTLCache(maxsize=100, ttl=api_cache_lifetime_seconds))
    def _get_request(self, params:dict, this_address:str):
        response = requests.get(url=this_address, proxies=self.connection.proxy,
                           headers=self.connection.authentication_header, params=params)
        if not response.ok:
            response.raise_for_status()
        return response

    # @cached(cache=TTLCache(maxsize=100, ttl=api_cache_lifetime_seconds))
    def df_params(self, *args, **kwargs) -> pd.DataFrame:
        """Fetches data from the API endpoint allowing the use of parameters and returns it as a pandas DataFrame.

        Args:
            *args: Positional arguments passed to `request_params` method.
            **kwargs: Keyword arguments, including:
                - convert_datetimes (bool, optional): If True, converts epoch timestamp
                  columns to datetime objects.
                - rq_params (dict, optional): Dictionary of parameters to pass therequesting API get requests for data.

        Returns:
            pd.DataFrame: A DataFrame containing the API response data as a pandas DataFrame.
        """
        if (convert_datetimes := kwargs.get('convert_datetimes')) is None:
            convert_datetimes = self.connection.convert_datetimes
        else:
            del kwargs['convert_datetimes']

        result_df = pd.DataFrame.from_records(self.request_params(*args, **kwargs))

        # todo: perhaps the name_clean column should be an option for __init__ to do this wherever <div> may show up
        #  ...or a way to clean those up
        if 'name' in result_df.columns:
            result_df.loc[:, 'name_clean'] = result_df.loc[:, 'name'].apply(lambda x: div_pattern.sub("", x))

        if convert_datetimes:
            self.convert_datetime_columns(result_df)

        return result_df

    def convert_datetime_columns(self, df: pd.DataFrame):
        """Converts specified epoch seconds timestamp columns in a DataFrame to pandas Timestamp (datetime64) columns.

        Args:
            df (pd.DataFrame): The DataFrame to process.
        """
        cols_to_convert = [col for col in df.columns if col in self.epoch_columns]
        for column_header in cols_to_convert:
            column_index = df.columns.get_loc(column_header)
            df.isetitem(
                column_index,
                pd.to_datetime(
                    df.loc[:, column_header], unit='s', origin='unix', utc=True
                ).dt.tz_convert(self.connection.timezone)
            )

    @property
    def df(self) -> pd.DataFrame:
        """pd.DataFrame: A property that fetches and returns the endpoint data as a DataFrame."""
        return self.df_params()

    @property
    def response(self) -> list[dict]:
        """list: A property that fetches and returns the endpoint data as a list."""
        return self.request_params()
