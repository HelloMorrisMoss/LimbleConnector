"""Integration tests for dynamic endpoint loading from registry.yaml (T008, FR-003)."""
import os
import tempfile
import yaml
from unittest.mock import patch, MagicMock

import pytest

from LimbleConnection.connection import LimbleConnection
from LimbleConnection.endpoint import LimbleEndpoint, Namespace


class TestDynamicEndpointLoading:
    """Test suite for dynamic endpoint attachment from registry.yaml (FR-003)."""

    @pytest.fixture
    def minimal_registry(self):
        """Create a minimal registry for testing."""
        return {
            'version': '1.0',
            'endpoints': {
                'routes.test_endpoint': {
                    'url': '{api_base_url}/test',
                    'method': 'GET',
                    'is_folder': False,
                    'query_params': [],
                    'response': {
                        'fields': {},
                        'container_type': 'list'
                    }
                },
                'routes.users.list': {
                    'url': '{api_base_url}/users',
                    'method': 'GET',
                    'is_folder': False,
                    'query_params': [],
                    'response': {
                        'fields': {},
                        'container_type': 'list'
                    }
                },
                'routes.assets.search': {
                    'url': '{api_base_url}/assets/search',
                    'method': 'POST',
                    'is_folder': False,
                    'query_params': [],
                    'response': {
                        'fields': {},
                        'container_type': 'list'
                    }
                },
                'routes.folders_only': {
                    'is_folder': True,
                    'description_data': {}
                }
            }
        }

    @pytest.fixture
    def temp_registry_file(self, minimal_registry, tmp_path):
        """Create a temporary registry file for testing."""
        temp_file = tmp_path / "registry.yaml"
        with open(temp_file, 'w') as f:
            yaml.dump(minimal_registry, f)
        return str(temp_file)

    def _patch_registry_path(self, temp_file):
        """Helper to patch the registry path lookup without affecting pytz."""
        # Patch __file__ to point to a directory containing our temp registry
        fake_module_dir = os.path.dirname(temp_file)
        original_dirname = os.path.dirname  # Save original before patching

        def mock_dirname(path):
            # Only intercept calls for connection.py's __file__
            if 'connection' in str(path):
                return fake_module_dir
            return original_dirname(path)  # Use saved original

        return patch('LimbleConnection.connection.os.path.dirname', side_effect=mock_dirname)

    def test_endpoints_loaded_from_registry(self, temp_registry_file):
        """Test that endpoints are loaded from registry.yaml into __endpoints__ dict."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            # Verify endpoints were loaded
            assert len(lc.__endpoints__) > 0

            # Verify specific endpoints exist
            assert 'routes.test_endpoint' in lc.__endpoints__
            assert 'routes.users.list' in lc.__endpoints__
            assert 'routes.assets.search' in lc.__endpoints__

            # Verify folders are not loaded as endpoints
            assert 'routes.folders_only' not in lc.__endpoints__

    def test_fluent_api_attachment(self, temp_registry_file):
        """Test that endpoints are attached as fluent API attributes."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            # Test simple endpoint access
            assert hasattr(lc, 'test_endpoint')
            assert isinstance(lc.test_endpoint, LimbleEndpoint)

            # Test nested namespace access
            assert hasattr(lc, 'users')
            assert isinstance(lc.users, Namespace) or isinstance(lc.users, LimbleEndpoint)

            # Test deeply nested endpoint access
            assert hasattr(lc, 'assets')
            assert hasattr(lc.assets, 'search')
            assert isinstance(lc.assets.search, LimbleEndpoint)

    def test_endpoint_url_replacement(self, temp_registry_file):
        """Test that {api_base_url} placeholder is replaced with actual API URL."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            endpoint = lc.__endpoints__['routes.test_endpoint']
            assert '{api_base_url}' not in endpoint.route_url
            assert 'https://api.limblecmms.com:443/v2/test' == endpoint.route_url

    def test_endpoint_preserves_config(self, temp_registry_file):
        """Test that endpoint config is preserved from registry."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            endpoint = lc.__endpoints__['routes.test_endpoint']
            assert endpoint.config['method'] == 'GET'
            assert 'query_params' in endpoint.config
            assert 'response' in endpoint.config

    def test_no_registry_file_graceful_handling(self, tmp_path):
        """Test that missing registry.yaml doesn't crash initialization."""
        # Point to a directory without registry.yaml
        fake_dir = str(tmp_path / "nonexistent")
        original_dirname = os.path.dirname  # Save original before patching

        def mock_dirname(path):
            if 'connection' in str(path):
                return fake_dir
            return original_dirname(path)  # Use saved original

        with patch('LimbleConnection.connection.os.path.dirname', side_effect=mock_dirname):
            lc = LimbleConnection(b64_credentials='test123')

            # Should initialize without errors
            assert lc is not None
            assert len(lc.__endpoints__) == 0

    def test_namespace_to_endpoint_replacement(self, tmp_path):
        """Test that Namespace is properly replaced with LimbleEndpoint while preserving children."""
        registry = {
            'version': '1.0',
            'endpoints': {
                'routes.parent': {
                    'url': '{api_base_url}/parent',
                    'method': 'GET',
                    'is_folder': False,
                    'query_params': [],
                    'response': {'fields': {}, 'container_type': 'dict'}
                },
                'routes.parent.child': {
                    'url': '{api_base_url}/parent/child',
                    'method': 'GET',
                    'is_folder': False,
                    'query_params': [],
                    'response': {'fields': {}, 'container_type': 'list'}
                }
            }
        }

        temp_file = tmp_path / "registry.yaml"
        with open(temp_file, 'w') as f:
            yaml.dump(registry, f)

        with self._patch_registry_path(str(temp_file)):
            lc = LimbleConnection(b64_credentials='test123')

            # Parent should be an endpoint
            assert isinstance(lc.parent, LimbleEndpoint)

            # Child should still be accessible
            assert hasattr(lc.parent, 'child')
            assert isinstance(lc.parent.child, LimbleEndpoint)

    def test_endpoint_name_normalization(self, temp_registry_file):
        """Test that 'routes.' prefix is stripped for attribute attachment."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            # 'routes.test_endpoint' should be accessible as 'test_endpoint'
            assert hasattr(lc, 'test_endpoint')
            # Should NOT be accessible as 'routes.test_endpoint'
            assert not hasattr(lc, 'routes')

    def test_multiple_endpoints_loaded(self, temp_registry_file):
        """Test that multiple endpoints can be loaded simultaneously."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            # Verify all non-folder endpoints are loaded
            # From minimal_registry: test_endpoint, users.list, assets.search
            assert len(lc.__endpoints__) == 3

    def test_endpoint_connection_reference(self, temp_registry_file):
        """Test that each endpoint has a reference to the parent LimbleConnection."""
        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            endpoint = lc.__endpoints__['routes.test_endpoint']
            assert endpoint.connection is lc

    def test_logging_on_load(self, temp_registry_file, caplog):
        """Test that endpoint loading is logged for observability."""
        import logging
        caplog.set_level(logging.INFO, logger='LimbleConnector')

        with self._patch_registry_path(temp_registry_file):
            lc = LimbleConnection(b64_credentials='test123')

            # Check that loading was logged
            assert any('Loading endpoints from' in record.message for record in caplog.records)
            assert any('Loaded 3 endpoints from registry' in record.message for record in caplog.records)
