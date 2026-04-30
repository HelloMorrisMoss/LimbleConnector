"""
Unit tests for OpenAPI extraction utilities.

Tests schema parsing, type conversion, and parameter extraction functions
from the openapi_extract module (FR-018).
"""

import unittest
from pathlib import Path
from LimbleConnection._generate_classes_automatically.openapi_extract import (
    extract_params,
    extract_request_body_fields,
    extract_response_fields,
    iter_operations,
    load_openapi,
    normalize_path,
    schema_to_python_type,
)


class TestNormalizePath(unittest.TestCase):
    """Test path normalization for registry comparison."""

    def test_strips_v2_prefix(self):
        self.assertEqual(normalize_path("/v2/assets"), "/assets")
        self.assertEqual(normalize_path("/v2/assets/{id}"), "/assets/{id}")

    def test_preserves_path_without_v2(self):
        self.assertEqual(normalize_path("/assets"), "/assets")
        self.assertEqual(normalize_path("/tasks/{id}"), "/tasks/{id}")

    def test_removes_trailing_slash(self):
        self.assertEqual(normalize_path("/assets/"), "/assets")
        self.assertEqual(normalize_path("/v2/users/"), "/users")

    def test_lowercases_path_params(self):
        self.assertEqual(normalize_path("/assets/{AssetID}"), "/assets/{assetid}")
        self.assertEqual(normalize_path("/tasks/{TaskID}/users/{UserID}"), "/tasks/{taskid}/users/{userid}")

    def test_handles_root_path(self):
        self.assertEqual(normalize_path("/"), "/")
        self.assertEqual(normalize_path("/v2/"), "/")


class TestSchemaToPythonType(unittest.TestCase):
    """Test OpenAPI schema to Python type conversion."""

    def test_integer_type(self):
        self.assertEqual(schema_to_python_type({"type": "integer"}), "int")

    def test_number_type(self):
        self.assertEqual(schema_to_python_type({"type": "number"}), "float")

    def test_string_type(self):
        self.assertEqual(schema_to_python_type({"type": "string"}), "str")

    def test_binary_string_type(self):
        self.assertEqual(schema_to_python_type({"type": "string", "format": "binary"}), "bytes")

    def test_boolean_type(self):
        self.assertEqual(schema_to_python_type({"type": "boolean"}), "bool")

    def test_array_type(self):
        self.assertEqual(schema_to_python_type({"type": "array", "items": {"type": "string"}}), "list[str]")
        self.assertEqual(schema_to_python_type({"type": "array", "items": {"type": "integer"}}), "list[int]")

    def test_nested_array_type(self):
        schema = {
            "type": "array",
            "items": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
        self.assertEqual(schema_to_python_type(schema), "list[list[str]]")

    def test_object_with_properties(self):
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"}
            }
        }
        self.assertEqual(schema_to_python_type(schema), "dict[str, Any]")

    def test_object_without_properties(self):
        self.assertEqual(schema_to_python_type({"type": "object"}), "dict[str, Any]")

    def test_none_schema(self):
        self.assertEqual(schema_to_python_type(None), "Any")

    def test_empty_schema(self):
        self.assertEqual(schema_to_python_type({}), "Any")

    def test_unknown_type(self):
        self.assertEqual(schema_to_python_type({"type": "unknown"}), "Any")

    def test_ref_schema(self):
        self.assertEqual(schema_to_python_type({"$ref": "#/components/schemas/Asset"}), "Asset")
        self.assertEqual(schema_to_python_type({"$ref": "#/components/schemas/Task"}), "Task")


class TestExtractParams(unittest.TestCase):
    """Test parameter extraction from operations."""

    def test_extracts_query_param(self):
        operation = {
            "parameters": [
                {
                    "name": "limit",
                    "in": "query",
                    "required": False,
                    "description": "Maximum number of results",
                    "schema": {"type": "integer"},
                    "example": 50
                }
            ]
        }
        params = extract_params(operation)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["name"], "limit")
        self.assertEqual(params[0]["in"], "query")
        self.assertFalse(params[0]["required"])
        self.assertEqual(params[0]["origin_type"], "int")
        self.assertEqual(params[0]["description"], "Maximum number of results")
        self.assertEqual(params[0]["example"], 50)

    def test_extracts_path_param(self):
        operation = {
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"}
                }
            ]
        }
        params = extract_params(operation)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["name"], "id")
        self.assertEqual(params[0]["in"], "path")
        self.assertTrue(params[0]["required"])
        self.assertEqual(params[0]["origin_type"], "int")

    def test_handles_missing_schema(self):
        operation = {
            "parameters": [
                {
                    "name": "test",
                    "in": "query"
                }
            ]
        }
        params = extract_params(operation)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["origin_type"], "Any")

    def test_handles_empty_parameters(self):
        operation = {"parameters": []}
        self.assertEqual(extract_params(operation), [])


class TestExtractRequestBodyFields(unittest.TestCase):
    """Test request body field extraction from operations."""

    def test_extracts_json_body_fields(self):
        operation = {
            "request_body": {
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Asset name"},
                                "locationId": {"type": "integer"}
                            },
                            "required": ["name"]
                        }
                    }
                }
            }
        }
        fields = extract_request_body_fields(operation)
        self.assertEqual(len(fields), 2)

        name_field = next(f for f in fields if f["name"] == "name")
        self.assertEqual(name_field["in"], "body")
        self.assertEqual(name_field["media_type"], "application/json")
        self.assertTrue(name_field["required"])
        self.assertEqual(name_field["origin_type"], "str")
        self.assertEqual(name_field["description"], "Asset name")

        location_field = next(f for f in fields if f["name"] == "locationId")
        self.assertFalse(location_field["required"])
        self.assertEqual(location_field["origin_type"], "int")

    def test_handles_missing_request_body(self):
        operation = {}
        self.assertEqual(extract_request_body_fields(operation), [])

    def test_handles_empty_request_body(self):
        operation = {"request_body": {}}
        self.assertEqual(extract_request_body_fields(operation), [])


class TestExtractResponseFields(unittest.TestCase):
    """Test response field extraction from operations."""

    def test_extracts_object_response_fields(self):
        operation = {
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "integer"},
                                    "name": {"type": "string", "description": "Asset name"}
                                }
                            }
                        }
                    }
                }
            }
        }
        fields = extract_response_fields(operation)
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields["id"]["status"], "200")
        self.assertEqual(fields["id"]["media_type"], "application/json")
        self.assertEqual(fields["id"]["origin_type"], "int")
        self.assertEqual(fields["name"]["origin_type"], "str")
        self.assertEqual(fields["name"]["description"], "Asset name")

    def test_extracts_array_response_fields(self):
        operation = {
            "responses": {
                "200": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "userId": {"type": "integer"},
                                        "email": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        fields = extract_response_fields(operation)
        self.assertEqual(len(fields), 2)
        self.assertEqual(fields["userId"]["origin_type"], "int")
        self.assertEqual(fields["email"]["origin_type"], "str")

    def test_handles_missing_responses(self):
        operation = {}
        self.assertEqual(extract_response_fields(operation), {})

    def test_handles_empty_response_content(self):
        operation = {
            "responses": {
                "204": {"description": "No content"}
            }
        }
        self.assertEqual(extract_response_fields(operation), {})


class TestIterOperations(unittest.TestCase):
    """Test operation iteration over OpenAPI document."""

    def test_iterates_operations(self):
        openapi = {
            "paths": {
                "/v2/assets": {
                    "get": {
                        "summary": "List assets",
                        "description": "Get all assets",
                        "tags": ["Assets"],
                        "parameters": [
                            {"name": "limit", "in": "query", "schema": {"type": "integer"}}
                        ],
                        "responses": {"200": {}}
                    },
                    "post": {
                        "summary": "Create asset",
                        "tags": ["Assets"],
                        "parameters": [],
                        "requestBody": {"content": {}},
                        "responses": {"201": {}}
                    }
                }
            }
        }

        operations = list(iter_operations(openapi))
        self.assertEqual(len(operations), 2)

        get_op = next(op for op in operations if op["method"] == "GET")
        self.assertEqual(get_op["raw_path"], "/v2/assets")
        self.assertEqual(get_op["normalized_path"], "/assets")
        self.assertEqual(get_op["summary"], "List assets")
        self.assertEqual(get_op["description"], "Get all assets")
        self.assertEqual(get_op["tags"], ["Assets"])
        self.assertEqual(len(get_op["parameters"]), 1)

        post_op = next(op for op in operations if op["method"] == "POST")
        self.assertEqual(post_op["method"], "POST")
        self.assertEqual(post_op["summary"], "Create asset")

    def test_combines_path_and_operation_parameters(self):
        openapi = {
            "paths": {
                "/assets/{id}": {
                    "parameters": [
                        {"name": "id", "in": "path", "schema": {"type": "integer"}}
                    ],
                    "get": {
                        "parameters": [
                            {"name": "include", "in": "query", "schema": {"type": "string"}}
                        ],
                        "responses": {}
                    }
                }
            }
        }

        operations = list(iter_operations(openapi))
        self.assertEqual(len(operations), 1)
        self.assertEqual(len(operations[0]["parameters"]), 2)
        param_names = [p["name"] for p in operations[0]["parameters"]]
        self.assertIn("id", param_names)
        self.assertIn("include", param_names)

    def test_ignores_non_http_methods(self):
        openapi = {
            "paths": {
                "/assets": {
                    "get": {"responses": {}},
                    "parameters": [],
                    "servers": []
                }
            }
        }

        operations = list(iter_operations(openapi))
        self.assertEqual(len(operations), 1)
        self.assertEqual(operations[0]["method"], "GET")


class TestLoadOpenAPI(unittest.TestCase):
    """Test OpenAPI document loading."""

    def test_loads_valid_yaml(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            yaml_file = Path(tmp_dir) / "test.yaml"
            yaml_file.write_text("""
openapi: 3.0.0
info:
  title: Test API
  version: 1.0.0
paths:
  /test:
    get:
      responses:
        '200':
          description: OK
""")

            openapi = load_openapi(yaml_file)
            self.assertEqual(openapi["openapi"], "3.0.0")
            self.assertEqual(openapi["info"]["title"], "Test API")
            self.assertIn("/test", openapi["paths"])


if __name__ == '__main__':
    unittest.main()
