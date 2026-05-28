import unittest
import os
import json
import yaml
from LimbleConnection._generate_classes_automatically.generator import Generator, compute_final_type

class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.postman_json = "test_collection.json"
        self.registry_yaml = "test_registry.yaml"
        self.stubs_pyi = "test_connection.pyi"
        
        # Create a mock Postman collection
        mock_data = {
            "info": {"name": "Test Collection", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
            "item": [
                {
                    "name": "Assets",
                    "item": [
                        {
                            "name": "List Assets",
                            "request": {
                                "method": "GET",
                                "url": {
                                    "raw": "{{baseUrl}}/assets?limit=10",
                                    "query": [
                                        {
                                            "key": "limit",
                                            "value": "10",
                                            "description": "Number of results to return"
                                        }
                                    ]
                                },
                                "description": "Get all assets"
                            }
                        }
                    ]
                }
            ]
        }
        with open(self.postman_json, 'w') as f:
            json.dump(mock_data, f)

    def tearDown(self):
        for f in [self.postman_json, self.registry_yaml, self.stubs_pyi]:
            if os.path.exists(f):
                os.remove(f)

    def test_generator_run(self):
        generator = Generator(self.postman_json, self.registry_yaml, self.stubs_pyi)
        generator.run()
        
        # Verify registry.yaml
        self.assertTrue(os.path.exists(self.registry_yaml))
        with open(self.registry_yaml, 'r') as f:
            registry = yaml.safe_load(f)
        
        self.assertIn('assets.list_assets', registry['endpoints'])
        self.assertEqual(registry['endpoints']['assets.list_assets']['url'], '{api_base_url}/assets')
        self.assertIn('query_params', registry['endpoints']['assets.list_assets'])
        self.assertEqual(registry['endpoints']['assets.list_assets']['query_params'][0]['key'], 'limit')
        
        # Verify .pyi stubs
        self.assertTrue(os.path.exists(self.stubs_pyi))
        with open(self.stubs_pyi, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('class LimbleConnection(object):', content)
        self.assertIn('def assets(self) -> AssetsNamespace: ...', content)
        self.assertIn('class AssetsNamespace(object):', content)
        # Check that docstring is present for the property
        self.assertIn('def list_assets(self) -> AssetsList_assetsNamespace:', content)
        self.assertIn('Get all assets', content)
        self.assertIn('Query Parameters:', content)
        self.assertIn('- limit: Number of results to return', content)

    def test_disabled_property_omitted_but_param_included(self):
        """T007a: Test that 'disabled' property is omitted but parameters are kept (FR-016).

        The 'disabled' flag in Postman is UI state (whether to send the param in example requests),
        not API metadata. We keep all documented parameters but omit the Postman-specific 'disabled' property.
        """
        # Create mock with disabled and enabled params
        mock_data = {
            "info": {"name": "Test Collection", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
            "item": [{
                "name": "TestEndpoint",
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": "{{baseUrl}}/test",
                        "query": [
                            {"key": "active_param", "value": "10", "description": "Active parameter", "disabled": False},
                            {"key": "optional_param", "value": "20", "description": "Optional parameter", "disabled": True}
                        ]
                    }
                }
            }]
        }
        with open(self.postman_json, 'w') as f:
            json.dump(mock_data, f)

        generator = Generator(self.postman_json, self.registry_yaml, self.stubs_pyi)
        generator.run()

        with open(self.registry_yaml, 'r') as f:
            registry = yaml.safe_load(f)

        params = registry['endpoints']['testendpoint']['query_params']
        param_keys = [p['key'] for p in params]

        # Both parameters should be included (disabled is just Postman UI state)
        self.assertIn('active_param', param_keys)
        self.assertIn('optional_param', param_keys)

        # Verify 'disabled' property itself is not in any param dict
        for param in params:
            self.assertNotIn('disabled', param,
                f"'disabled' property should not be in registry for param {param['key']}")

    def test_response_data_extraction(self):
        """T007b: Test response data extraction from Postman description tables (FR-017)."""
        mock_data = {
            "info": {"name": "Test Collection", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
            "item": [{
                "name": "TestEndpoint",
                "request": {
                    "method": "GET",
                    "url": {"raw": "{{baseUrl}}/test"},
                    "description": "Get data\n\n| Property | Description |\n|----------|-------------|\n| assetID | The asset identifier |\n| name | Asset name |"
                }
            }]
        }
        with open(self.postman_json, 'w') as f:
            json.dump(mock_data, f)

        generator = Generator(self.postman_json, self.registry_yaml, self.stubs_pyi)
        generator.run()

        with open(self.registry_yaml, 'r') as f:
            registry = yaml.safe_load(f)

        endpoint = registry['endpoints']['testendpoint']
        self.assertIn('response', endpoint)
        self.assertIn('fields', endpoint['response'])

        fields = endpoint['response']['fields']
        self.assertIn('assetID', fields)
        self.assertIn('name', fields)

        # Verify type inference
        self.assertEqual(fields['assetID']['type'], 'int')  # ID suffix
        self.assertEqual(fields['name']['type'], 'str')

    def test_type_inference_and_override_preservation(self):
        """T007c: Test override preservation and conflict warnings (FR-019, FR-020)."""
        # First, create initial registry with override
        initial_registry = {
            'version': '1.0',
            'endpoints': {
                'test': {
                    'url': '{api_base_url}/test',
                    'method': 'GET',
                    'query_params': [{
                        'key': 'limit',
                        'value': '10',
                        'description': 'Limit',
                        'inferred_type': 'int',
                        'origin_type': None,
                        'override_type': 'str',  # Manual override
                        'type': 'str'
                    }]
                }
            }
        }

        with open(self.registry_yaml, 'w') as f:
            yaml.dump(initial_registry, f)

        # Now generate with new Postman data
        mock_data = {
            "info": {"name": "Test", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
            "item": [{
                "name": "Test",
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": "{{baseUrl}}/test",
                        "query": [{"key": "limit", "value": "100", "description": "Limit"}]
                    }
                }
            }]
        }
        with open(self.postman_json, 'w') as f:
            json.dump(mock_data, f)

        generator = Generator(self.postman_json, self.registry_yaml, self.stubs_pyi)
        generator.run()

        with open(self.registry_yaml, 'r') as f:
            registry = yaml.safe_load(f)

        param = registry['endpoints']['test']['query_params'][0]

        # Verify override is preserved
        self.assertEqual(param['override_type'], 'str')
        self.assertEqual(param['type'], 'str')  # Should use override, not inferred 'int'


class TestTypePrecedence(unittest.TestCase):
    """T007c-1 / T009c-2: Test type precedence and merging logic (FR-018).

    Precedence: override_type > origin_type > observed_type > inferred_type
    """

    def test_compute_final_type_override_wins(self):
        """Override type has highest priority."""
        result = compute_final_type(
            inferred='int',
            origin='str',
            observed='float',
            override='bool'
        )
        self.assertEqual(result, 'bool')

    def test_compute_final_type_origin_over_observed(self):
        """Origin type takes precedence over observed when no override (FR-018)."""
        result = compute_final_type(
            inferred='int',
            origin='str',
            observed='Optional[str]',
            override=None
        )
        self.assertEqual(result, 'str')

    def test_compute_final_type_observed_over_inferred(self):
        """Observed type wins over inferred when origin/override absent (FR-018, FR-022)."""
        result = compute_final_type(
            inferred='int',
            origin=None,
            observed='Optional[str]',
            override=None
        )
        self.assertEqual(result, 'Optional[str]')

    def test_compute_final_type_inferred_fallback(self):
        """Inferred type is used when no origin, observed, or override."""
        result = compute_final_type(
            inferred='int',
            origin=None,
            observed=None,
            override=None
        )
        self.assertEqual(result, 'int')

    def test_compute_final_type_empty_string_not_truthy(self):
        """Empty strings should be treated as falsy (not set)."""
        result = compute_final_type(
            inferred='int',
            origin='',
            observed='',
            override=''
        )
        # Empty strings are falsy, should fall through to inferred
        self.assertEqual(result, 'int')

    def test_openapi_origin_type_precedence(self):
        """Test that OpenAPI-derived origin_type takes precedence over Postman table type.

        Simulates the scenario where:
        - Postman table says a field is "string"
        - OpenAPI schema says it's "integer"
        - OpenAPI should win as the origin_type
        """
        # This test validates the documented precedence from FR-018:
        # origin_type should use: OpenAPI schema type > Postman explicit table type

        # Scenario: OpenAPI provides integer, Postman example infers string
        openapi_origin = 'int'  # From OpenAPI schema
        postman_inferred = 'str'  # From Postman example

        final_type = compute_final_type(
            inferred=postman_inferred,
            origin=openapi_origin,
            observed=None,
            override=None
        )

        # OpenAPI origin_type should win
        self.assertEqual(final_type, 'int')

    def test_type_merging_with_all_sources(self):
        """Test complete type merging scenario with all four sources present."""
        # - Postman example suggests: "10" → inferred as int
        # - OpenAPI schema declares: string
        # - Live observation: Optional[str]
        # - User override: Sequence[int] (for comma-delimited IDs)

        result = compute_final_type(
            inferred='int',
            origin='str',  # From OpenAPI
            observed='Optional[str]',  # From live testing
            override='Sequence[int]'  # Manual configuration
        )

        # Override should win
        self.assertEqual(result, 'Sequence[int]')


if __name__ == '__main__':
    unittest.main()
