# LimbleConnection
## Goal
This project seeks to provide a streamlined Python interface for common interactions with the Limble CMMS API.
Currently targeting the API v2.

## What is here?
The most significant thing in the project is the LimbleConnection class. This provides convenient dot notation access to
many of the API's endpoints. So you can simplify this:

    import base64
    import requests
    import pandas as pd
    
    from company_data import internal_proxies, client_id, client_secret
    from LimbleConnection.untracked_config.proxy import internal_proxies
    from LimbleConnection.untracked_config.timezones import local_tz
    
    auth_header = base64.b64encode(f'{client_id}:{client_secret}'.encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}'}
    assets_address = 'https://api.limblecmms.com:443/v2/assets'
    
    result_data = []
    results_returned = True
    params = dict(page=0)
    
    while results_returned:
        params['page'] += 1
        page_data = requests.get(url=assets_address, proxies=internal_proxies, headers=headers,
                                   data={'meta': ['fields']}, params=params).json()
        if not page_data:
            results_returned = False
        else:
            result_data += page_data
    
    assets_df = pd.DataFrame.from_records(result_data)
    
    timestamp_epoch_seconds_cols = 'startedOn', 'lastEdited'
    tz_name = 'America/New_York'
    for tscol in timestamp_epoch_seconds_cols:
        assets_df[tscol] = pd.to_datetime(assets_df[tscol], unit='s').apply(lambda x: x.tz_localize(tz=tz_name))

down to this:

    import LimbleConnection
    from company_data import internal_proxies, client_id, client_secret
    
    auth_header = LimbleConection.utils.encode_credentials(client_id, client_secret)
    lc = LimbleConnection.LimbleConnection(convert_datetimes=True, proxy=internal_proxies, b64_credentials=auth_header)
    assets_df = lc.assets.df



## Legal
The names and documentation referenced that are associated with Limble are trademarked/copyright Limble CMMS.
This project is not created, supported, or endorsed by Limble CMMS.
