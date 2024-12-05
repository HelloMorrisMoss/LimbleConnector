import pandas as pd
import requests

from untracked_config.api_auth import b64_credentials
from untracked_config.proxy import internal_proxies
from untracked_config.timezones import local_tz


class LimbleEndpoint:  # rename something like endpoint?
    def __init__(self, parent, rt_add):
        # print(f'init with {parent=}, {rt_add=}')
        self.parent = parent
        self.rt_add = rt_add

        self.epoch_columns = ['createdDate', 'startDate', 'due', 'dateCompleted ', 'lastEdited', 'startedOn',
                              'lastEdited', 'dateAdded']

    def request_params(self, *args, **kwargs):
        print(f'response partial: {args=} - {kwargs=}')
        params = kwargs.pop('rq_params', None)
        response = requests.get(*args, **kwargs, url=self.rt_add, proxies=internal_proxies,
                                headers=self.parent.authentication_header, params=params)
        return response

    def df_params(self, *args, **kwargs):
        print(f'df partial: {args=} - {kwargs=}')

        if (convert_datetimes:=kwargs.get('convert_datetimes')) is None:
            convert_datetimes = self.parent.convert_datetimes
        else:
            del kwargs['convert_datetimes']


        if self.convert_datetimes:
        if convert_datetimes:
            self.convert_datetime_columns(result_df)

        return result_df

    def convert_datetime_columns(self, df: pd.DataFrame):
        cols_to_convert = [col for col in df.columns if col in self.epoch_columns]
        # todo: pandas does not like replacing a column in this way
        #  "FutureWarning: Setting an item of incompatible dtype is deprecated and will raise in a future error of
        #  pandas. Value '<DatetimeArray>"
        for col in cols_to_convert:
            df.loc[:, col] = pd.to_datetime(df.loc[:, col], unit='s', origin='unix', utc=True).dt.tz_convert(local_tz)

    @property
    def df(self):
        return self.df_params()

    @property
    def response(self):
        return self.request_params()


class LimbleConnection():

    def __init__(self, convert_datetimes=False):
        self.authentication_header = {'Authorization': f'Basic {b64_credentials}'}
        self.api_base_address = 'https://api.limblecmms.com:443'
        self.api_version = 'v2'  # todo: handle other versions?
        self.apiv_addrs = f'{self.api_base_address}/{self.api_version}'

        self.convert_datetimes = convert_datetimes

        # design decision, add the slash when it is needed not before
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
        to_add_properties_list = [(epn, epaddr) for (epn, epaddr) in self.__endpoints__.items()]
        while to_add_properties_list:
            epn, epaddr = to_add_properties_list.pop(0)
            if '.' in epn:
                pass
                self.set_sub_property(epaddr, epn, to_add_properties_list)
            else:
                propertish = self.__create_endpoint(epn, epaddr)
                setattr(self.__class__, epn, propertish)

    def set_sub_property(self, epaddr, epn, incomplete_list):
        try:  # ensure that the parent exists
            epn_path = epn.split('.')
            parent_path_list = epn_path[:-1]
            parent = getattr(self, parent_path_list.pop(0))
            while parent_path_list:
                parent_name = parent_path_list.pop(0)
                parent = getattr(parent, parent_name)
            propertish = self.__create_endpoint(epn_path[-1], epaddr)
            setattr(parent, epn_path[-1], propertish)
        except AttributeError as aerr:
            print(f'No parent for {epn}')
            incomplete_list.append((epn, epaddr))

    def __create_endpoint(self, epn, epaddr):

        rt_add = self.get_route_address(epaddr)
        propertish = LimbleEndpoint(self, rt_add)

        return propertish

    def get_route_address(self, endpoint: str):
        return f'{self.apiv_addrs}/{endpoint}'


if __name__ == '__main__':
    # for development:

    # print DataFrames wider/longer than visible - for development
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)

    lc = LimbleConnection(convert_datetimes=True)
    pass  # for debug breakpoint in IDE
