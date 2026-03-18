import unittest
from unittest.mock import MagicMock, patch
from LimbleConnection.endpoint import LimbleEndpoint

class TestEndpointParams(unittest.TestCase):
    def setUp(self):
        self.mock_connection = MagicMock()
        self.mock_connection.authentication_header = {"Authorization": "Basic xxx"}
        self.mock_connection.proxy = None
        self.mock_connection.apiv_addrs = "https://api.limblecmms.com/v2"
        self.mock_connection.page_limit = 100

    def test_supports_query_param(self):
        config = {
            "query_params": [
                {"key": "limit", "description": "some limit"},
                {"key": "page", "description": "some page"}
            ]
        }
        endpoint = LimbleEndpoint(self.mock_connection, "test.endpoint", "https://api.limblecmms.com/v2/test", config)
        
        self.assertTrue(endpoint.supports_query_param("limit"))
        self.assertTrue(endpoint.supports_query_param("page"))
        self.assertFalse(endpoint.supports_query_param("other"))

    def test_supports_query_param_missing_config(self):
        config = {}
        endpoint = LimbleEndpoint(self.mock_connection, "test.endpoint", "https://api.limblecmms.com/v2/test", config)
        
        # If missing, we should probably assume True for backward compatibility or if registry is incomplete?
        # Actually, the user wants us to NOT pass it if not supported.
        # If we don't have query_params in config, it might be an old registry.
        self.assertTrue(endpoint.supports_query_param("limit"))

    def test_list_adds_limit_only_if_supported(self):
        # Endpoint that supports limit
        config_with_limit = {
            "query_params": [{"key": "limit"}]
        }
        endpoint_with_limit = LimbleEndpoint(self.mock_connection, "test.limit", "https://api.limblecmms.com/v2/limit", config_with_limit)
        
        with patch.object(endpoint_with_limit, 'raw') as mock_raw:
            mock_raw.return_value.json.return_value = []
            endpoint_with_limit.list(auto_paginate=False)
            args, kwargs = mock_raw.call_args
            self.assertIn('limit', kwargs)
            self.assertEqual(kwargs['limit'], 100)

        # Endpoint that DOES NOT support limit
        config_no_limit = {
            "query_params": [{"key": "something_else"}]
        }
        endpoint_no_limit = LimbleEndpoint(self.mock_connection, "test.no_limit", "https://api.limblecmms.com/v2/no_limit", config_no_limit)
        
        with patch.object(endpoint_no_limit, 'raw') as mock_raw:
            mock_raw.return_value.json.return_value = []
            endpoint_no_limit.list(auto_paginate=False)
            args, kwargs = mock_raw.call_args
            self.assertNotIn('limit', kwargs)

if __name__ == '__main__':
    unittest.main()
