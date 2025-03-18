import pandas as pd
import requests

from untracked_config.api_auth import b64_credentials
from untracked_config.proxy import internal_proxies
from untracked_config.timezones import local_tz


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

    def __init__(self, parent, rt_addr):
        """Initializes a LimbleEndpoint instance.

        Args:
            parent (LimbleConnection): The parent connection instance.
            rt_addr (str): The full route address for this endpoint.
        """
        self.parent = parent
        self.rt_addr = rt_addr

        self.epoch_columns = [
            'createdDate', 'startDate', 'due', 'dateCompleted', 'lastEdited',
            'startedOn', 'lastEdited', 'dateAdded'
        ]

    def request_params(self, *args, **kwargs):
        """Makes a GET request to the API endpoint allowing the use of parameters and retrieves data.

        Args:
            *args: Positional arguments passed to the `requests.get` function.
            **kwargs: Keyword arguments, including:
                - rq_params (dict, optional): Additional query parameters for the request.
                - auto_page_all (bool, optional): Overrides the parent's setting for
                  automatic pagination.

        Examples:
            Example getting only page 2 of the assets list:

            >>>lc = LimbleClass()
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
        # if provided parameter use that, otherwise the parent setting
        if (auto_page_all := kwargs.get('auto_page_all')) is None:
            auto_page_all = self.parent.auto_page_all
        else:
            del kwargs['auto_page_all']

        if any(self.rt_addr.endswith(end) for end in ('users',)):
            auto_page_all = None  # these do not support the page parameter

        if auto_page_all:
            result_data = []
            results_returned = True
            page_number = 0

            if params is None:
                params = {}

            while results_returned:
                page_number += 1
                params['page'] = page_number
                page_data = requests.get(
                    *args, **kwargs, url=self.rt_addr, proxies=internal_proxies,
                    headers=self.parent.authentication_header, params=params
                ).json()
                if not page_data:
                    results_returned = False
                else:
                    result_data += page_data
        else:
            result_data = requests.get(
                *args, **kwargs, url=self.rt_addr, proxies=internal_proxies,
                headers=self.parent.authentication_header, params=params
            ).json()
        return result_data

    def df_params(self, *args, **kwargs) -> pd.DataFrame:
        """Fetches data from the API endpoint allowing the use of parameters and returns it as a pandas DataFrame.

        Args:
            *args: Positional arguments passed to `request_params` method.
            **kwargs: Keyword arguments, including:
                - convert_datetimes (bool, optional): If True, converts epoch timestamp
                  columns to datetime objects.
                - rq_params (dict, optional): Dictionary of parameters to pass the the API get requests for data.

        Returns:
            pd.DataFrame: A DataFrame containing the API response data as a pandas DataFrame.
        """
        if (convert_datetimes := kwargs.get('convert_datetimes')) is None:
            convert_datetimes = self.parent.convert_datetimes
        else:
            del kwargs['convert_datetimes']

        result_df = pd.DataFrame.from_records(self.request_params(*args, **kwargs))

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
                ).dt.tz_convert(local_tz)
            )

    @property
    def df(self):
        """pd.DataFrame: A property that fetches and returns the endpoint data as a DataFrame."""
        return self.df_params()

    @property
    def response(self):
        """list: A property that fetches and returns the endpoint data as a list."""
        return self.request_params()


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

    def __init__(self, convert_datetimes=False, auto_page_all=True):
        """Initializes a LimbleConnection instance.

        Args:
            convert_datetimes (bool, optional): If True, converts datetime fields in API responses to Python
                datetime objects. Defaults to False.
            auto_page_all (bool, optional): If True, automatically paginates all API responses. Defaults to True.
        """
        self.authentication_header = {'Authorization': f'Basic {b64_credentials}'}
        self.api_base_address = 'https://api.limblecmms.com:443'
        self.api_version = 'v2'  # todo: handle other versions?
        self.apiv_addrs = f'{self.api_base_address}/{self.api_version}'

        self.auto_page_all = auto_page_all
        self.convert_datetimes = convert_datetimes

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

                              'tasks': 'tasks',
                              'tasks.labor': 'tasks/labor',
                              'tasks.labor.categories': 'tasks/labor/categories',

                              'users': 'users',

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
            if '.' in epn:
                self.set_sub_property(epaddr, epn, to_add_properties_list)
            else:
                propertish = self.__create_endpoint(epn, epaddr)
                setattr(self.__class__, epn, propertish)

    def set_sub_property(self, epaddr, epn, incomplete_list):
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
            propertish = self.__create_endpoint(epn_path[-1], epaddr)
            setattr(parent, epn_path[-1], propertish)
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
        propertish = LimbleEndpoint(self, rt_add)
        return propertish

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

    # print DataFrames wider/longer than visible - for development
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    lc = LimbleConnection(convert_datetimes=True, auto_page_all=True)
    assets = lc.assets.df
    pass  # for debug breakpoint in IDE
