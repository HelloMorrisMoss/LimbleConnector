import json
import yaml
from typing import Dict, Any, List

class TranslationEngine:
    """Translates Postman JSON to registry.yaml (FR-001, FR-002)."""

    def __init__(self, postman_json_path: str):
        self.postman_json_path = postman_json_path

    def translate(self) -> Dict[str, Any]:
        """Convert Postman collection to an internal registry format."""
        with open(self.postman_json_path, 'r', encoding='utf-8') as f:
            collection = json.load(f)
        
        registry = {
            'version': '1.0',
            'endpoints': {}
        }

        self._process_items(collection.get('item', []), [], registry['endpoints'])
        return registry

    def _process_items(self, items: List[Dict[str, Any]], path: List[str], endpoints: Dict[str, Any]):
        for item in items:
            name = item.get('name', '').lower().replace(' ', '_')
            current_path = path + [name]
            
            if 'item' in item: # It's a Folder
                self._process_items(item['item'], current_path, endpoints)
            elif 'request' in item: # It's a Request
                endpoint_key = '.'.join(current_path)
                request = item['request']
                url_obj = request.get('url', {})
                
                if isinstance(url_obj, str):
                    url = url_obj
                else:
                    url = url_obj.get('raw', '')
                
                # Normalize URL: replace {{baseUrl}} with a placeholder
                url = url.replace('{{baseUrl}}', '{api_base_url}')
                url = url.replace('{{protocol}}://{{server}}:{{port}}/v2', '{api_base_url}')
                
                endpoints[endpoint_key] = {
                    'url': url,
                    'method': request.get('method', 'GET'),
                    'description': request.get('description', ""),
                }

class Generator:
    """Generates registry.yaml and .pyi stubs (FR-007, FR-013)."""
    
    def __init__(self, postman_json_path: str, output_registry_path: str, output_stubs_path: str):
        self.engine = TranslationEngine(postman_json_path)
        self.output_registry_path = output_registry_path
        self.output_stubs_path = output_stubs_path

    def run(self):
        registry = self.engine.translate()
        with open(self.output_registry_path, 'w') as f:
            yaml.dump(registry, f, sort_keys=False)
        
        self.generate_stubs(registry)

    def generate_stubs(self, registry: Dict[str, Any]):
        """Build a tree and generate nested stubs for the fluent API."""
        tree = {}
        for name in registry['endpoints']:
            parts = name.split('.')
            if parts[0] == 'routes':
                parts = parts[1:]
            
            if len(parts) > 1 and parts[-1] == parts[-2]:
                parts = parts[:-1]
                
            current = tree
            for part in parts:
                if part not in current:
                    current[part] = {"_is_endpoint": False, "_children": {}}
                current_node = current[part]
                current = current_node["_children"]
            
            current_node["_is_endpoint"] = True

        lines = [
            "from typing import List, Dict, Any, Optional, Union",
            "import pandas as pd",
            "from LimbleConnection.endpoint import LimbleEndpoint",
            ""
        ]

        def get_class_name(path: List[str]) -> str:
            if not path: return "LimbleConnection"
            return "".join(p.capitalize() for p in path) + "Namespace"

        def process_node(node_name: str, node: Dict[str, Any], path: List[str]):
            class_name = get_class_name(path)
            base = "LimbleEndpoint" if node["_is_endpoint"] else "object"
            
            class_lines = [f"class {class_name}({base}):"]
            if not node["_children"]:
                class_lines.append("    pass")
            else:
                for child_name, child_node in node["_children"].items():
                    child_path = path + [child_name]
                    child_class = get_class_name(child_path)
                    class_lines.append(f"    @property")
                    class_lines.append(f"    def {child_name}(self) -> {child_class}: ...")
            
            # Recursively process children
            for child_name, child_node in node["_children"].items():
                process_node(child_name, child_node, path + [child_name])
            
            lines.insert(4, "\n".join(class_lines) + "\n")

        # Start from root
        root_node = {"_is_endpoint": False, "_children": tree}
        process_node("root", root_node, [])

        with open(self.output_stubs_path, 'w') as f:
            f.write("\n".join(lines))

if __name__ == "__main__":
    import os
    # Default execution for the project
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    postman_path = os.path.join(os.path.dirname(base_dir), 'Limble API V2.postman_collection.json')
    registry_path = os.path.join(base_dir, 'registry.yaml')
    stubs_path = os.path.join(base_dir, 'connection.pyi')
    
    if os.path.exists(postman_path):
        gen = Generator(postman_path, registry_path, stubs_path)
        gen.run()
        print(f"Generated {registry_path} and {stubs_path}")
    else:
        print(f"Postman collection not found at {postman_path}")
