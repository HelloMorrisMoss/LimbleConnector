# LimbleConnection

A Python SDK for the Limble CMMS API V2, now featuring a **Spec-Driven Architecture**.

## Goal
This project seeks to provide a streamlined Python interface for common interactions with the Limble CMMS API.
Currently targeting the API v2.

## Key Features

- **Spec-Driven**: Endpoints are dynamically generated from `registry.yaml`, which is automatically translated from the official Postman collection.
- **Fluent API**: Access endpoints using a clean, dotted notation (e.g., `lc.assets.list()`).
- **Auto-Pagination**: Large result sets are automatically fetched across multiple pages.
- **Resilient**: Built-in exponential backoff and retries for transient errors (429, 502, 503).
- **SSL Support**: Built-in support for custom SSL certificate bundles and automatic Windows trust store integration via `certifi-win32`.
- **Type-Safe**: IDE support with generated `.pyi` stubs.
- **Curated Operations**: High-level methods for common workflows (e.g., `lc.curated_assets.search_assets()`).
- **Stability Shielding**: Internal field mapping to prevent upstream API changes from breaking user code.

## Quickstart

```python
from LimbleConnection import LimbleConnection

# Initialize connection
lc = LimbleConnection(b64_credentials="YOUR_BASE64_CREDENTIALS")

# List assets (auto-paginated, fluent API)
assets = lc.assets.list()

# Access nested endpoints
fields = lc.assets.fields.asset_fields.list()
```

### SSL Configuration

By default, `LimbleConnection` enables SSL verification.

- **Windows**: The library automatically attempts to use the Windows system trust store if `python-certifi-win32` is installed.
- **Custom Bundle**: You can provide a path to a custom CA bundle:
  ```python
  lc = LimbleConnection(b64_credentials="...", verify="/path/to/cert.pem")
  ```
- **Disable Verification**: (Not recommended)
  ```python
  lc = LimbleConnection(b64_credentials="...", verify=False)
  ```

## Developer Guide: Adding Endpoints

Instead of manual coding, simply update the Postman collection and run the generator:

```bash
python LimbleConnection/_generate_classes_automatically/generator.py
```

This will update `registry.yaml` and `connection.pyi` automatically.

## Old Documentation (to be reviewed)

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
