import json
import yaml
import os
import re
from typing import Dict, Any, List, Tuple, Optional
from bs4 import BeautifulSoup

try:
    from LimbleConnection.util import collapse_redundant_path_parts, logger
except ImportError:
    import sys
    import os
    # Add project root to sys.path to allow importing LimbleConnection.util
    _root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if _root not in sys.path:
        sys.path.append(_root)
    from LimbleConnection.util import collapse_redundant_path_parts, logger

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

def infer_type_from_value(value: str) -> str:
    """Infer Python type from a string value (FR-018)."""
    if not value:
        return "str"

    # Try to infer from the value
    value_clean = value.strip()

    # Boolean
    if value_clean.lower() in ('true', 'false'):
        return "bool"

    # Integer
    if re.match(r'^-?\d+$', value_clean):
        return "int"

    # Float
    if re.match(r'^-?\d+\.\d+$', value_clean):
        return "float"

    # List/Array (comma-separated or JSON array)
    if ',' in value_clean or (value_clean.startswith('[') and value_clean.endswith(']')):
        return "list[str]"

    # Default to string
    return "str"

def infer_type_from_name(name: str) -> str:
    """Infer type from parameter/field name patterns (FR-018)."""
    name_lower = name.lower()

    # ID patterns
    if name_lower.endswith('id') or name_lower.endswith('_id'):
        return "int"

    # Boolean patterns
    if name_lower.startswith('is_') or name_lower.startswith('has_') or name_lower.startswith('can_'):
        return "bool"

    # Date/timestamp patterns
    if 'date' in name_lower or 'time' in name_lower or 'timestamp' in name_lower:
        return "int"  # Epoch timestamps

    # Count/limit patterns
    if name_lower in ('limit', 'count', 'page', 'offset', 'size'):
        return "int"

    # List patterns
    if name_lower.endswith('s') or name_lower.endswith('_list') or 'ids' in name_lower:
        return "list[str]"

    return "str"

def compute_final_type(inferred: str, origin: Optional[str], override: Optional[str]) -> str:
    """Compute final type using preference order: override > origin > inferred (FR-018)."""
    if override:
        return override
    if origin:
        return origin
    return inferred

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
            
            collapsed_path = collapse_redundant_path_parts(current_path)
            endpoint_key = '.'.join(collapsed_path)
            
            description_obj = item.get('description', "")
            if isinstance(description_obj, dict):
                description_text = description_obj.get('content', '')
            else:
                description_text = description_obj
            description_data = get_text_and_table(description_text)
            
            if 'item' in item: # It's a Folder
                # Store folder description even if it's not a direct endpoint
                endpoints[endpoint_key] = {
                    'is_folder': True,
                    'description_data': description_data
                }
                self._process_items(item['item'], current_path, endpoints)
            elif 'request' in item: # It's a Request
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
                    query_params_raw = []
                else:
                    url = url_obj.get('raw', '')
                    query_params_raw = url_obj.get('query', [])

                # Normalize URL: replace {{baseUrl}} with a placeholder
                url = url.replace('{{baseUrl}}', '{api_base_url}')
                url = url.replace('{{protocol}}://{{server}}:{{port}}/v2', '{api_base_url}')

                # Strip query parameters from the URL as they should not be part of the endpoint definition (FR-001)
                url = url.split('?')[0]

                # Typo in the Postman collection for the DELETE assets endpoint (FR-001 typo)
                # It currently is assets/1?assetID={{assetID}} but it should be assets/:assetID and no query param.
                if endpoint_key == 'routes.assets.delete_asset' and request.get('method') == 'DELETE':
                    url = url.replace('/assets/1', '/assets/:assetID')
                    query_params_raw = []

                # T009a: Process query parameters - omit 'disabled' property (FR-016)
                query_params = self._process_query_params(query_params_raw)

                # T009b: Extract response fields from description tables (FR-017)
                response_fields = self._extract_response_fields(request_description_data)

                # Build endpoint entry
                endpoint_data = {
                    'url': url,
                    'method': request.get('method', 'GET'),
                    'description_data': request_description_data,
                    'is_folder': False,
                    'query_params': query_params
                }

                # Add response mapping if fields were found
                if response_fields:
                    endpoint_data['response'] = {
                        'fields': response_fields,
                        'container_type': 'list'  # Default assumption for Limble endpoints
                    }

                endpoints[endpoint_key] = endpoint_data

    def _process_query_params(self, raw_params: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process query parameters, omitting 'disabled' property but keeping the param (FR-016, FR-018).

        Note: 'disabled' in Postman means the parameter isn't sent in the example request by default,
        but it's still a valid, documented API parameter that should be in our registry.
        We omit the 'disabled' property itself (as it's Postman-specific), not the parameter.
        """
        processed = []

        for param in raw_params:
            key = param.get('key', '')
            value = param.get('value', '')
            description = param.get('description', '')

            # T009c: Infer types (FR-018)
            inferred_type = infer_type_from_value(value) if value else infer_type_from_name(key)
            origin_type = param.get('type')  # Explicit type from Postman (rare)

            processed_param = {
                'key': key,
                'value': value,
                'description': description,
                'inferred_type': inferred_type,
                'type': compute_final_type(inferred_type, origin_type, None)
            }

            # Include origin_type if it exists
            if origin_type:
                processed_param['origin_type'] = origin_type

            # NOTE: We intentionally do NOT include 'disabled' property (FR-016)
            # as it's Postman-specific UI state, not API metadata

            processed.append(processed_param)

        return processed

    def _extract_response_fields(self, description_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Extract response fields from description tables (FR-017, FR-018)."""
        if not description_data:
            return {}

        headers = description_data.get('headers', [])
        rows = description_data.get('data_rows', [])

        # Look for tables with "Property" or "Field" and "Description" headers
        # Common patterns in Limble Postman collection:
        # - "Property" | "Description"
        # - "Property" | "Type" | "Description"
        # - "Field" | "Description"

        if not headers or not rows:
            return {}

        # Normalize headers
        headers_lower = [h.lower().strip() for h in headers]

        # Find relevant column indices
        prop_idx = next((i for i, h in enumerate(headers_lower) if 'property' in h or 'field' in h), None)
        desc_idx = next((i for i, h in enumerate(headers_lower) if 'description' in h), None)
        type_idx = next((i for i, h in enumerate(headers_lower) if h == 'type'), None)

        if prop_idx is None or desc_idx is None:
            return {}

        fields = {}
        for row in rows:
            if len(row) <= max(prop_idx, desc_idx):
                continue

            field_name = row[prop_idx].strip()
            field_desc = row[desc_idx].strip()

            if not field_name:
                continue

            # Get origin type if available
            origin_type = row[type_idx].strip() if type_idx is not None and len(row) > type_idx else None

            # Infer type
            inferred_type = infer_type_from_name(field_name)

            fields[field_name] = {
                'description': field_desc,
                'inferred_type': inferred_type,
                'type': compute_final_type(inferred_type, origin_type, None)
            }

            if origin_type:
                fields[field_name]['origin_type'] = origin_type

        return fields

class Generator:
    """Generates registry.yaml and .pyi stubs (FR-007, FR-013, FR-019, FR-020)."""

    def __init__(self, postman_json_path: str, output_registry_path: str, output_stubs_path: str):
        self.engine = TranslationEngine(postman_json_path)
        self.output_registry_path = output_registry_path
        self.output_stubs_path = output_stubs_path

    def run(self):
        # Load existing registry if it exists (T009d: FR-019, FR-020)
        existing_registry = self._load_existing_registry()

        # Generate new registry from Postman
        new_registry = self.engine.translate()

        # Merge with existing, preserving overrides
        merged_registry = self._merge_registries(existing_registry, new_registry)

        # Write updated registry
        with open(self.output_registry_path, 'w', encoding='utf-8') as f:
            yaml.dump(merged_registry, f, sort_keys=False, allow_unicode=True)

        # Generate stubs
        self.generate_stubs(merged_registry)

    def _load_existing_registry(self) -> Dict[str, Any]:
        """Load existing registry.yaml if it exists."""
        if not os.path.exists(self.output_registry_path):
            return {}

        try:
            with open(self.output_registry_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.warning(f"Could not load existing registry: {e}")
            return {}

    def _merge_registries(self, existing: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Any]:
        """Merge registries, preserving override_type values and emitting warnings (FR-019, FR-020)."""
        if not existing or 'endpoints' not in existing:
            return new

        merged = new.copy()
        existing_endpoints = existing.get('endpoints', {})
        new_endpoints = new.get('endpoints', {})

        for endpoint_key, new_data in new_endpoints.items():
            if endpoint_key not in existing_endpoints:
                continue  # New endpoint, no merging needed

            existing_data = existing_endpoints[endpoint_key]

            # Merge query_params
            if 'query_params' in new_data and 'query_params' in existing_data:
                merged_params = self._merge_params(
                    existing_data['query_params'],
                    new_data['query_params'],
                    endpoint_key,
                    'query_param'
                )
                merged['endpoints'][endpoint_key]['query_params'] = merged_params

            # Merge response fields
            if 'response' in new_data and 'response' in existing_data:
                new_fields = new_data.get('response', {}).get('fields', {})
                existing_fields = existing_data.get('response', {}).get('fields', {})

                merged_fields = self._merge_fields(
                    existing_fields,
                    new_fields,
                    endpoint_key
                )

                if 'response' not in merged['endpoints'][endpoint_key]:
                    merged['endpoints'][endpoint_key]['response'] = {}
                merged['endpoints'][endpoint_key]['response']['fields'] = merged_fields

        return merged

    def _merge_params(self, existing_params: List[Dict[str, Any]], new_params: List[Dict[str, Any]],
                      endpoint_key: str, param_type: str) -> List[Dict[str, Any]]:
        """Merge query parameters, preserving override_type (FR-019, FR-020)."""
        # Build lookup by key
        existing_by_key = {p['key']: p for p in existing_params if 'key' in p}

        merged = []
        for new_param in new_params:
            key = new_param.get('key')
            if not key:
                merged.append(new_param)
                continue

            if key not in existing_by_key:
                # New parameter
                merged.append(new_param)
                continue

            existing_param = existing_by_key[key]

            # Start with new param
            merged_param = new_param.copy()

            # Preserve override_type if it exists (FR-019)
            if 'override_type' in existing_param and existing_param['override_type']:
                merged_param['override_type'] = existing_param['override_type']
                # Recalculate final type with override
                merged_param['type'] = compute_final_type(
                    merged_param.get('inferred_type', 'str'),
                    merged_param.get('origin_type'),
                    merged_param['override_type']
                )

            # Emit warning if generated values differ (FR-020)
            if 'override_type' in existing_param and existing_param['override_type']:
                new_inferred = new_param.get('inferred_type', 'str')
                old_inferred = existing_param.get('inferred_type', 'str')

                if new_inferred != old_inferred:
                    logger.warning(
                        f"Type inference changed for {endpoint_key}.{param_type}[{key}]: "
                        f"{old_inferred} -> {new_inferred}. Override is set to {existing_param['override_type']}"
                    )

            merged.append(merged_param)

        return merged

    def _merge_fields(self, existing_fields: Dict[str, Dict[str, Any]], new_fields: Dict[str, Dict[str, Any]],
                      endpoint_key: str) -> Dict[str, Dict[str, Any]]:
        """Merge response fields, preserving override_type (FR-019, FR-020)."""
        merged = {}

        for field_name, new_field in new_fields.items():
            if field_name not in existing_fields:
                # New field
                merged[field_name] = new_field
                continue

            existing_field = existing_fields[field_name]
            merged_field = new_field.copy()

            # Preserve override_type if it exists (FR-019)
            if 'override_type' in existing_field and existing_field['override_type']:
                merged_field['override_type'] = existing_field['override_type']
                # Recalculate final type with override
                merged_field['type'] = compute_final_type(
                    merged_field.get('inferred_type', 'str'),
                    merged_field.get('origin_type'),
                    merged_field['override_type']
                )

            # Emit warning if generated values differ (FR-020)
            if 'override_type' in existing_field and existing_field['override_type']:
                new_inferred = new_field.get('inferred_type', 'str')
                old_inferred = existing_field.get('inferred_type', 'str')

                if new_inferred != old_inferred:
                    logger.warning(
                        f"Type inference changed for {endpoint_key}.response.{field_name}: "
                        f"{old_inferred} -> {new_inferred}. Override is set to {existing_field['override_type']}"
                    )

            merged[field_name] = merged_field

        return merged

    def generate_stubs(self, registry: Dict[str, Any]):
        """Build a tree and generate nested stubs for the fluent API."""
        tree = {}
        # Pre-process endpoints to build the tree and attach data
        for name, data in registry['endpoints'].items():
            parts = name.split('.')
            if parts[0] == 'routes':
                parts = parts[1:]
                
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

        def format_docstring(description_data: Dict[str, Any], indent_level: int, query_params: List[Dict[str, Any]] = None) -> List[str]:
            if not description_data and not query_params:
                return []
            
            doc_lines = []
            indent = "    " * indent_level
            
            if description_data:
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
            
            if query_params:
                doc_lines.append("")
                doc_lines.append(f"{indent}Query Parameters:")
                for param in query_params:
                    key = param.get('key', '')
                    desc = param.get('description', '')
                    disabled = " (disabled)" if param.get('disabled') else ""
                    doc_lines.append(f"{indent}- {key}{disabled}: {desc}")
            
            if not doc_lines:
                return []
            
            return [f'{indent}"""'] + doc_lines + [f'{indent}"""']

        def process_node(node_name: str, node: Dict[str, Any], path: List[str]):
            class_name = get_class_name(path)
            base = "LimbleEndpoint" if node["_is_endpoint"] else "object"
            
            class_lines = [f"class {class_name}({base}):"]
            
            # Add docstring for the class if available
            if node.get("_data"):
                desc_data = node["_data"].get("description_data")
                q_params = node["_data"].get("query_params")
                if desc_data or q_params:
                    class_lines.extend(format_docstring(desc_data, 1, q_params))
            
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
                    if child_node.get("_data"):
                        c_desc_data = child_node["_data"].get("description_data")
                        c_q_params = child_node["_data"].get("query_params")
                        if c_desc_data or c_q_params:
                            prop_doc = format_docstring(c_desc_data, 2, c_q_params)
                    
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
