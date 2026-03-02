import unittest
import os
import json
import yaml
from LimbleConnection._generate_classes_automatically.generator import Generator

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
                                "url": {"raw": "{{baseUrl}}/assets"},
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
        
        # Verify .pyi stubs
        self.assertTrue(os.path.exists(self.stubs_pyi))
        with open(self.stubs_pyi, 'r') as f:
            content = f.read()
        self.assertIn('@property', content)
        self.assertIn('def assets_list_assets(self) -> LimbleEndpoint: ...', content)

if __name__ == '__main__':
    unittest.main()
