from __future__ import annotations
from typing import Optional, Union, Any

import requests
import tzlocal
import pandas as pd
import pytz

from LimbleConnection.LimbleEndpoint import LimbleEndpoint
from LimbleConnection._documentation_placeholders import Users

api_cache_lifetime_seconds = 5


class LimbleConnection:
    """Handles connection and interactions with the Limble CMMS API.

    This class manages API authentication, endpoint generation, and configuration
    settings for communicating with the Limble CMMS API.

    Attributes:
        authentication_header (dict): The authorization header for API requests.
        api_base_address (str): The base address for the API.
        api_version (str): The version of the API to use. Currently only 'v2' is implemented.
        apiv_addrs (str): The full base URL with the API version included.
        auto_page_all (bool): Whether to automatically paginate API responses (collecting all available).
        convert_datetimes (bool): Whether to convert epoch seconds columns to a pandas Timestamp in dataframes.
        __endpoints__ (dict): Dictionary of API endpoints and their paths.
    """
    # todo: __slots__
    def __init__(self, convert_datetimes=False, auto_page_all=True, location:str=None, location_id:int=None,
                 *args, **kwargs):
        """Initializes a LimbleConnection instance.

        Args:
            convert_datetimes (bool, optional): If True, converts datetime fields in API responses to Python
                datetime objects. Defaults to False.
            auto_page_all (bool, optional): If True, automatically paginates all API responses. Defaults to True.
            location (str, optional): The default location for API requests. Defaults to None.
            location_id (int, optional): The locationID for the default location. Defaults to None.
            page_limit (int, optional): The maximum number of results to return per page. Defaults to 100.
        """
        self.authentication_header = {'Authorization': f'Basic {b64_credentials}'} if (b64_credentials:=kwargs.get('b64_credentials')) else None
        self.proxy = kwargs.get('proxy', None)
        self.timezone = pytz.timezone(tz) if (tz := kwargs.get('tz')) else pytz.timezone(tzlocal.get_localzone_name())

        self.api_base_address = 'https://api.limblecmms.com:443'
        self.api_version = 'v2'  # todo: handle other versions?
        self.apiv_addrs = f'{self.api_base_address}/{self.api_version}'

        self.auto_page_all = auto_page_all
        self.page_limit = 100 if kwargs.get('page_limit') is None else kwargs.get('page_limit')
        self.convert_datetimes = convert_datetimes
        self._location = location
        self._location_id = location_id  # todo: handle default location being multiple locations

        # placeholders
        self.assets: Optional[LimbleEndpoint] = None
        self.locations: Optional[LimbleEndpoint] = None
        self.parts: Optional[LimbleEndpoint] = None
        self.tasks: Optional[LimbleEndpoint] = None
        # self.users: Optional[LimbleEndpoint] = None
        # self.users = property(self.users, self)
        self.users = Users
        self.statuses: Optional[LimbleEndpoint] = None

        # design decision: add the slash when it is needed not before (so no trailing or leading slashes here)
        # design decision: keep the name and path seperate to allow flexibility; ex: synonyms
        self.__endpoints__ = {'assets': 'assets',
                              'assets.fields': 'assets/fields',
                              'assets.fields.suggested': 'assets/fields/suggested',
                              'assets.fields.history': 'assets/fields/history',

                              'locations': 'locations',

                              'parts': 'parts',
                              'parts.categories': 'parts/categories',
                              'parts.fields': 'parts/fields',
                              'parts.logs': 'parts/logs',

                              'tasks': 'tasks',
                              'tasks.labor': 'tasks/labor',
                              'tasks.labor.categories': 'tasks/labor/categories',

                              'teams': 'teams',

                              'users': 'users',
                              'users.teams': 'users/{path_param}/teams',
                              'priorities': 'priorities',
                              'statuses': 'statuses',

                              # todo: create
                              #  assets/:assetID/logs
                              #  tasks/:taskID/instructions
                              #  tasks/:taskID/instructions/:instructionID/options
                              #  tasks/labor
                              #  tasks/labor/categories
                              }

        to_add_properties_list = list(self.__endpoints__.items())
        while to_add_properties_list:
            epn, epaddr = to_add_properties_list.pop(0)
            print(epn)
            if '.' in epn:
                # propertish, epn = self.__set_sub_property(epaddr, epn, to_add_properties_list)
                self.__set_sub_property(epaddr, epn, to_add_properties_list)
            else:
                propertish, epn = self.__create_endpoint(epn, epaddr)
                setattr(self, epn, propertish)

    def get_from_path(self, path_route:str, **kwargs) -> Any:
        """Send a GET request to a route provided as a string. Intended for development purposes.

        ex:
            lc.get_from_path('tasks/{path_param}/instructions', path_param=1234, limit=2)
            Would return the requests.Response object for the GET request to:
            https://api.limblecmms.com:443/v2/tasks/1234/instructions?limit=2

            Convenience features such as path parameter formatting, auto paging if enabled and the route supports
            paging, etc. will be applied.

        ex using raw=True:
            lc.get_from_path(
            path_route='https://api.limblecmms.com:443/v2/users/8675309/teams',
             raw=True, teams=(436,437), locations=(163,74), limit=100)
            Would return the requests.Response object for the GET request to:
            https://api.limblecmms.com:443/v2/users/8675309/teams?teams=436,437&locations=163,74&limit=100

        Args:
            path_route: str, the route to send the ge request to. ex: /statuses or tasks/1234/
            **kwargs: Keyword arguments, including:
                - auto_page_all (bool, optional): Overrides the parent's setting for automatic pagination.
                - path_param (str, optional): for accessing endpoints that have a path parameter
                - raw (bool, optional): If True, neither the route string and results will not be processed by
                    convenience features. Only authentication and proxy will be applied. All other kwargs will be passed
                    to the request as query parameters.
                - as_df (bool, optional): If True, returns the results as a pandas DataFrame, just as df_from_path.
                - rq_params (dict, optional): Additional query parameters for the request, see Limble API docs.
                - any other keyword arguments will be passed to the GET request as query parameters.

        return: Any, depends on the endpoint.
            """
        raw = kwargs.pop('raw', False)

        if raw:
            print(f'Processing path as-is, convenience features will not be available,'
                  f' except for authentication and proxy. {path_route=}')
            value = LimbleEndpoint(self, '_', rt_addr='_')._get_request(kwargs, path_route)
        else:
            ep_keys = {key: kwargs.pop(key, None) for key in ('auto_page_all', 'path_param', 'rq_params')}
            as_df = kwargs.pop('as_df', False)
            ep_keys['rq_params'] = ep_keys['rq_params'] | kwargs if isinstance(ep_keys['rq_params'], dict) else kwargs

            this_address = self.apiv_addrs + f'{"/" if path_route[0] != "/" else ""}{path_route}'
            route_name = path_route.replace('/', '.')

            if not route_name in self.__endpoints__.keys():
                print(f'Custom route {route_name} is not implemented in LimbleConnector yet, some convenience features may'
                      f' not be available.')

            if as_df:
                value = LimbleEndpoint(self, route_name, rt_addr=this_address).df_params(
                    **ep_keys)
            else:
                value = LimbleEndpoint(self, route_name, rt_addr=this_address).get_request_params(
                **ep_keys)
        return value

    def df_from_path(self, path_route:str, **kwargs) -> pd.DataFrame:
        """Get the data as a pandas DataFrame from an endpoint provided as a path string.

        Intended for development purposes.

        Args:
            path_route: str, the route to send the ge request to. ex: /statuses or tasks/invoices
            kwargs (optional, any):
                - auto_page_all (bool, optional): Overrides the connection's setting for automatic pagination.
                - path_param (str, optional): for accessing endpoints that have a path parameter. The route string must
                    have a '{path_param}' placeholder. ex: 'users/{path_param}' where the path parameter would be the
                    userID.
        :return: pandas.DataFrame
        """
        return self.get_from_path(path_route, as_df=True, **kwargs)

    @property
    def location(self):
        """The default location for this connection instance.

        :return: str
        """
        if self._location is None:
            if self._location_id is not None:
                all_locations = self.locations.df
                # using the setter, not ._location
                self.location = all_locations.set_index('locationID').loc[self._location_id, 'name']
            else:
                self._default_when_single_location()
        return self._location

    @location.setter
    def location(self, location):
        self._location = location

    def _default_when_single_location(self):
        """If there is only a single location, set that as the default location.

        Otherwise, error requiring setting it."""
        # todo: this has a hazard that someone using the connection could have code that works until a second location
        #  is added...
        all_locations = self.locations.df
        if len(all_locations) == 1:
            self._location = all_locations.loc[0, 'name']
            self._location_id = all_locations.loc[0, 'locationID']
        else:
            raise AttributeError('Multiple locations are available. Please set the .location property of the '
                                 'connection or specify in the endpoint method call.')

    @property
    def location_id(self) -> int:
        """The locationID for the default location for this connection instance.

        :return: int
        """
        if self._location_id is None:
            if self._location is not None:
                all_locations = self.locations.df
                self._location_id = all_locations.set_index('name').loc[self._location, 'locationID']
            else:
                self._default_when_single_location()
        return self._location_id

    @location_id.setter
    def location_id(self, location_id):
        self._location_id = location_id


    def __set_sub_property(self, epaddr, epn, incomplete_list):
        """Adds sub-properties for nested API endpoints.

        Args:
            epaddr (str): The API endpoint path.
            epn (str): The endpoint name.
            incomplete_list (list): List of endpoint definitions that remain to be created.
        """
        try:
            epn_path = epn.split('.')
            parent_path_list = epn_path[:-1]
            parent = getattr(self, parent_path_list.pop(0))
            while parent_path_list:
                parent_name = parent_path_list.pop(0)
                parent = getattr(parent, parent_name)
            propertish, repn = self.__create_endpoint(epn, epaddr)
            setattr(parent, epn_path[-1], propertish)
            return propertish, repn
        except AttributeError as aerr:
            incomplete_list.append((epn, epaddr))

    def __create_endpoint(self, epn, epaddr):
        """Creates an endpoint object.

        Args:
            epn (str): The endpoint name.
            epaddr (str): The endpoint path.

        Returns:
            LimbleEndpoint: An object representing the API endpoint.
        """
        rt_add = self.get_route_address(epaddr)
        propertish = LimbleEndpoint(self, epn, rt_add)
        return propertish, epn

    def get_route_address(self, endpoint):
        """Constructs the full route address for an API endpoint.

        Args:
            endpoint (str): The endpoint path.

        Returns:
            str: The full API route address.
        """
        return f'{self.apiv_addrs}/{endpoint}'


if __name__ == '__main__':
    # for development:

    try:
        from .untracked_config.api_auth import b64_credentials
        from .untracked_config.proxy import internal_proxies
        from .untracked_config.timezones import local_tz
    except ImportError:
        from untracked_config.api_auth import b64_credentials
        from untracked_config.proxy import internal_proxies
        from untracked_config.timezones import local_tz

    # print DataFrames wider/longer than visible - for development
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    lc = LimbleConnection(convert_datetimes=True, auto_page_all=True)
    assets = lc.assets.df
    pass  # for debug breakpoint in IDE
