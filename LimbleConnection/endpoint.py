from __future__ import annotations

from pprint import pprint
from traceback import format_exc
from typing import TYPE_CHECKING, Any, Optional, Union, List, Dict
import re

import pandas as pd
import requests
from LimbleConnection.util import logger, ResilienceHandler

if TYPE_CHECKING:
    from LimbleConnection.connection import LimbleConnection


url_still_contains_path_params_pattern = re.compile(r':[a-zA-Z]+')

class Paginator:
    """Interface for handling different pagination strategies (FR-011)."""
    def get_next_params(self, current_params: Dict[str, Any], last_response: Any) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

class DefaultPaginator(Paginator):
    """Standard limit/page pagination strategy."""
    def get_next_params(self, current_params: Dict[str, Any], last_response: Any) -> Optional[Dict[str, Any]]:
        if not last_response:
            return None
        
        # If the last response was empty, we reached the end
        if isinstance(last_response, list) and not last_response:
            return None
        
        # If we got fewer items than the limit, we reached the end
        limit = current_params.get('limit', 100)
        if isinstance(last_response, list) and len(last_response) < limit:
            return None
            
        next_params = current_params.copy()
        next_params['page'] = next_params.get('page', 1) + 1
        return next_params

class Namespace:
    """A generic container for nested attributes to provide a fluent API."""
    def __repr__(self):
        return f"<Namespace {list(self.__dict__.keys())}>"

class LimbleEndpoint:
    """Base class for all dynamic endpoints (FR-004)."""

    def __init__(self, connection: 'LimbleConnection', endpoint_name: str, route_url: str, config: Dict[str, Any]):
        self.connection = connection
        self.name = endpoint_name
        self.route_url = route_url
        self.config = config
        self.resilience = ResilienceHandler()
        self.paginator = self._setup_paginator()

    def _setup_paginator(self) -> Paginator:
        # Placeholder for more complex paginator setup from config
        return DefaultPaginator()

    def _get_headers(self) -> Dict[str, str]:
        headers = self.connection.authentication_header.copy()
        if self.config.get('headers'):
            headers.update(self.config['headers'])
        return headers

    def raw(self, method: str, **kwargs) -> Any:
        """Execute a raw request to this endpoint."""
        url = self.route_url

        _ = kwargs.pop('limit', None)  # don't pass this to the request
        path_params = kwargs.pop('path_params')
        for k, v in path_params.items():
            url = url.replace(f':{k}', str(v))
        if url_still_contains_path_params_pattern.search(url):
            raise ValueError(f"Path params not all replaced in URL: {url}")

        # add any params to url in the 'base_url?key1=value1&key2=value2' format
        if 'query_params' in kwargs:
            url += '?' + '&'.join([f'{k}={v}' for k, v in kwargs.pop('query_params').items()])

        logger.debug(f"Executing {method} request to {self.name}")
        logger.debug(f"Full URL: {url}")
        
        headers = self._get_headers()
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        def _make_request():
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                proxies=self.connection.proxy,
                **kwargs
            )
            self._normalize_error(response)
            return response

        return self.resilience.execute(_make_request)

    def _normalize_error(self, response: requests.Response):
        """Standardizes error messages across different endpoints (FR-008)."""
        if response.status_code >= 400:
            try:
                data = response.json()
                error_msg = data.get('error') or data.get('message') or response.text
                logger.error(f"API Error {response.status_code} on {self.name}: {error_msg}\n{pprint(data)}")
            except Exception:
                logger.error(f"API Error {response.status_code} on {self.name}: {response.text}\n{pprint(data)}")

    def get(self, **kwargs) -> Dict[str, Any]:
        """GET a single resource or the endpoint root."""
        response = self.raw('GET', **kwargs)
        return self._map_response(response.json())

    def list(self, auto_paginate: bool = True, **kwargs) -> List[Dict[str, Any]]:
        """LIST resources with optional auto-pagination (FR-014)."""
        params = kwargs.copy()
        if 'limit' not in params:
            params['limit'] = 100

        if not auto_paginate:
            logger.debug(f"Auto-pagination disabled for {self.name}")
            logger.debug(f"Params passed to .raw: {params}")
            return self._map_response(self.raw('GET', **params).json())

        all_results = []
        current_params = params
        
        while current_params:
            logger.debug(f"Current params: {current_params}")
            if 'page' in current_params:
                logger.debug(f"Fetching page {current_params['page']} for {self.name}")
            response = self.raw('GET', **current_params)
            page_data = response.json()
            
            if not page_data or not isinstance(page_data, list):
                break
                
            all_results.extend(self._map_response(page_data))
            current_params = self.paginator.get_next_params(current_params, page_data)
            
        return all_results

    def _map_response(self, data: Any) -> Any:
        """Applies field aliasing/mapping (FR-005, FR-009)."""
        mapping = self.config.get('response_mapping')
        if not mapping or not data:
            return data
            
        if isinstance(data, list):
            return [self._map_item(item, mapping) for item in data]
        return self._map_item(data, mapping)

    def _map_item(self, item: Dict[str, Any], mapping: Dict[str, str]) -> Dict[str, Any]:
        new_item = item.copy()
        for internal_name, api_name in mapping.items():
            if api_name in item:
                new_item[internal_name] = item[api_name]
        return new_item

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """CREATE a new resource."""
        response = self.raw('POST', json=data)
        return response.json()

    def update(self, resource_id: Union[int, str], data: Dict[str, Any]) -> Dict[str, Any]:
        """UPDATE an existing resource."""
        path_params = {'id': resource_id} # Default path param name
        # In reality, this should be driven by config
        url = f"{self.route_url}/{resource_id}"
        response = self.resilience.execute(lambda: requests.patch(
            url=url,
            json=data,
            headers=self._get_headers(),
            proxies=self.connection.proxy
        ))
        return response.json()

    def delete(self, resource_id: Union[int, str]) -> bool:
        """DELETE a resource."""
        url = f"{self.route_url}/{resource_id}"
        response = self.resilience.execute(lambda: requests.delete(
            url=url,
            headers=self._get_headers(),
            proxies=self.connection.proxy
        ))
        return response.status_code == 200

    @property
    def df(self) -> pd.DataFrame:
        """Convenience property to return the list results as a pandas DataFrame using default parameters."""
        return self.df_params()

    def df_params(self, **kwargs) -> pd.DataFrame:
        """Return the list results as a pandas DataFrame."""
        logger.debug(f"Fetching data for {self.name} with params: {kwargs=}")
        return pd.DataFrame(self.list(**kwargs))


class RegistryLoader:
    """Loads and validates the registry.yaml (T006)."""

    def __init__(self, registry_path: str, schema_path: str):
        self.registry_path = registry_path
        self.schema_path = schema_path

    def load(self) -> Dict[str, Any]:
        """Load and validate registry."""
        import yaml
        # Validation logic using schema_path would go here
        with open(self.registry_path, 'r') as f:
            return yaml.safe_load(f)
