import json
import yaml
from typing import Dict, Any, List, Tuple
from bs4 import BeautifulSoup

def clean_bs4_text(soup_fragment):
    """Clean <p> and <b> tags and return text with preserved line breaks."""
    for tag in soup_fragment.find_all(['b', 'strong']):
        tag.unwrap()
    for p in soup_fragment.find_all('p'):
        p.insert_after('\n')
        p.unwrap()
    return soup_fragment.get_text()

def get_text_and_table(text: str):
    """Extract a markdown or HTML table from the text, returning uniform dictionary format."""
    if not text:
        return {
            'headers': [],
            'data_rows': [],
            'non_table_before': "",
            'non_table_after': ""
        }
    
    # First, let BeautifulSoup try to parse HTML content and extract any <table>
    bs = BeautifulSoup(text, 'html.parser')
    table = bs.find('table')
    if table:
        headers = []
        data_rows = []
        for i, tr in enumerate(table.find_all('tr')):
            cells = tr.find_all(['th', 'td'])
            cell_text = [clean_bs4_text(c).strip() for c in cells]
            if i == 0:
                headers = cell_text
            else:
                data_rows.append(cell_text)
        table.decompose()
        cleaned_text = clean_bs4_text(bs)
        return {
            'headers': headers,
            'data_rows': data_rows,
            'non_table_before': cleaned_text.strip(),
            'non_table_after': ''
        }

    # If no HTML table, attempt markdown table extraction
    table_start = text.find('|')
    table_end = len(text) - text[::-1].find('|')
    if table_start == -1 or table_end == -1:
        return {
            'headers': [],
            'data_rows': [],
            'non_table_before': text,
            'non_table_after': ''
        }

    non_table_before = text[:table_start]
    non_table_after = text[table_end:]
    table_txt = text[table_start:table_end]
    headers = []
    data_rows = []

    for ln, line in enumerate(table_txt.splitlines()):
        line = line.strip()
        if not line or not line.startswith('|'):
            continue
        cells = [x.strip() for x in line[1:-1].split('|')]
        if ln == 0:
            headers = cells
        elif ln == 1:
            continue  # skip the separator line
        else:
            data_rows.append(cells)

    return {
        'non_table_before': non_table_before.strip(),
        'headers': headers,
        'data_rows': data_rows,
        'non_table_after': non_table_after.strip()
    }

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
            
            description_obj = item.get('description', "")
            if isinstance(description_obj, dict):
                description_text = description_obj.get('content', '')
            else:
                description_text = description_obj
            description_data = get_text_and_table(description_text)
            
            if 'item' in item: # It's a Folder
                endpoint_key = '.'.join(current_path)
                # Store folder description even if it's not a direct endpoint
                endpoints[endpoint_key] = {
                    'is_folder': True,
                    'description_data': description_data
                }
                self._process_items(item['item'], current_path, endpoints)
            elif 'request' in item: # It's a Request
                endpoint_key = '.'.join(current_path)
                request = item['request']
                
                # Get description from the request itself
                request_description_obj = request.get('description', "")
                if isinstance(request_description_obj, dict):
                    request_description_text = request_description_obj.get('content', '')
                else:
                    request_description_text = request_description_obj
                
                # Fallback to item description if request description is empty
                if not request_description_text:
                    request_description_text = description_text
                
                request_description_data = get_text_and_table(request_description_text)
                
                url_obj = request.get('url', {})
                
                if isinstance(url_obj, str):
                    url = url_obj
                else:
                    url = url_obj.get('raw', '')
                
                # Normalize URL: replace {{baseUrl}} with a placeholder
                url = url.replace('{{baseUrl}}', '{api_base_url}')
                url = url.replace('{{protocol}}://{{server}}:{{port}}/v2', '{api_base_url}')
                
                # Update folder entry if it exists (some items are both folder and request? unlikely in this structure but possible)
                endpoints[endpoint_key] = {
                    'url': url,
                    'method': request.get('method', 'GET'),
                    'description_data': request_description_data,
                    'is_folder': False
                }

class Generator:
    """Generates registry.yaml and .pyi stubs (FR-007, FR-013)."""
    
    def __init__(self, postman_json_path: str, output_registry_path: str, output_stubs_path: str):
        self.engine = TranslationEngine(postman_json_path)
        self.output_registry_path = output_registry_path
        self.output_stubs_path = output_stubs_path

    def run(self):
        registry = self.engine.translate()
        with open(self.output_registry_path, 'w', encoding='utf-8') as f:
            yaml.dump(registry, f, sort_keys=False)
        
        self.generate_stubs(registry)

    def generate_stubs(self, registry: Dict[str, Any]):
        """Build a tree and generate nested stubs for the fluent API."""
        tree = {}
        # Pre-process endpoints to build the tree and attach data
        for name, data in registry['endpoints'].items():
            parts = name.split('.')
            if parts[0] == 'routes':
                parts = parts[1:]
            
            if len(parts) > 1 and parts[-1] == parts[-2]:
                parts = parts[:-1]
                
            current = tree
            for i, part in enumerate(parts):
                if part not in current:
                    current[part] = {"_is_endpoint": False, "_children": {}, "_data": None}
                current_node = current[part]
                if i == len(parts) - 1:
                    current_node["_data"] = data
                    if not data.get('is_folder', False):
                        current_node["_is_endpoint"] = True
                current = current_node["_children"]

        lines = [
            "from typing import List, Dict, Any, Optional, Union",
            "import pandas as pd",
            "from LimbleConnection.endpoint import LimbleEndpoint",
            ""
        ]

        def get_class_name(path: List[str]) -> str:
            if not path: return "LimbleConnection"
            return "".join(p.capitalize() for p in path) + "Namespace"

        def format_docstring(description_data: Dict[str, Any], indent_level: int) -> List[str]:
            if not description_data:
                return []
            
            doc_lines = []
            indent = "    " * indent_level
            
            text_before = description_data.get('non_table_before', "")
            if text_before:
                for line in text_before.splitlines():
                    doc_lines.append(f"{indent}{line}")
            
            headers = description_data.get('headers', [])
            rows = description_data.get('data_rows', [])
            
            if headers or rows:
                doc_lines.append("") # Spacer
                # Basic table formatting
                if headers:
                    header_line = " | ".join(headers)
                    doc_lines.append(f"{indent}{header_line}")
                    doc_lines.append(f"{indent}{'-' * len(header_line)}")
                
                for row in rows:
                    doc_lines.append(f"{indent}{' | '.join(row)}")

            text_after = description_data.get('non_table_after', "")
            if text_after:
                doc_lines.append("") # Spacer
                for line in text_after.splitlines():
                    doc_lines.append(f"{indent}{line}")
            
            if not doc_lines:
                return []
            
            return [f'{indent}"""'] + doc_lines + [f'{indent}"""']

        def process_node(node_name: str, node: Dict[str, Any], path: List[str]):
            class_name = get_class_name(path)
            base = "LimbleEndpoint" if node["_is_endpoint"] else "object"
            
            class_lines = [f"class {class_name}({base}):"]
            
            # Add docstring for the class if available
            if node.get("_data") and node["_data"].get("description_data"):
                class_lines.extend(format_docstring(node["_data"]["description_data"], 1))
            
            if not node["_children"]:
                if len(class_lines) == 1: # only class def
                    class_lines.append("    pass")
            else:
                for child_name, child_node in node["_children"].items():
                    child_path = path + [child_name]
                    child_class = get_class_name(child_path)
                    class_lines.append(f"    @property")
                    
                    # Add docstring for the property if available from child
                    prop_doc = []
                    if child_node.get("_data") and child_node["_data"].get("description_data"):
                        prop_doc = format_docstring(child_node["_data"]["description_data"], 2)
                    
                    if prop_doc:
                        class_lines.append(f"    def {child_name}(self) -> {child_class}:")
                        class_lines.extend(prop_doc)
                        class_lines.append(f"        ...")
                    else:
                        class_lines.append(f"    def {child_name}(self) -> {child_class}: ...")
            
            # Recursively process children
            for child_name, child_node in node["_children"].items():
                process_node(child_name, child_node, path + [child_name])
            
            lines.insert(4, "\n".join(class_lines) + "\n")

        # Start from root
        root_node = {"_is_endpoint": False, "_children": tree, "_data": None}
        process_node("root", root_node, [])

        with open(self.output_stubs_path, 'w', encoding='utf-8') as f:
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
