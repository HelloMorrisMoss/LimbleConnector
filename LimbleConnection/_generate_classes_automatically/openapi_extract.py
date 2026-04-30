"""
OpenAPI extraction utilities for type inference.

Provides functions to extract parameter and response type information from
the Postman-generated OpenAPI 3.0 spec to supplement Postman collection data.

Based on utilities documented in limble_openapi_utilization_notes.md.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterator

import yaml


HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def load_openapi(path: str | Path) -> dict[str, Any]:
    """
    Load and parse an OpenAPI YAML file.

    Args:
        path: Path to the OpenAPI YAML file

    Returns:
        Parsed OpenAPI document as a dictionary
    """
    with Path(path).open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def normalize_path(path: str) -> str:
    """
    Normalize OpenAPI paths to the registry's API-relative shape.

    - Strips /v2 prefix if present
    - Removes trailing slashes
    - Lowercases path parameter names

    Args:
        path: Raw OpenAPI path (e.g., "/v2/assets/{AssetID}")

    Returns:
        Normalized path (e.g., "/assets/{assetid}")
    """
    if path.startswith("/v2"):
        path = path[3:]
    path = path.rstrip("/") or "/"
    return re.sub(r"\{([^}]+)\}", lambda m: "{" + m.group(1).lower() + "}", path)


def iter_operations(openapi: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """
    Iterate over all HTTP operations in the OpenAPI document.

    Yields dictionaries containing:
    - method: HTTP method (uppercase)
    - raw_path: Original path from OpenAPI
    - normalized_path: Path normalized for registry comparison
    - summary: Operation summary
    - description: Operation description
    - tags: List of tags
    - parameters: Combined path-level and operation-level parameters
    - request_body: Request body definition (if present)
    - responses: Response definitions

    Args:
        openapi: Parsed OpenAPI document

    Yields:
        Operation dictionaries
    """
    for raw_path, path_item in openapi.get("paths", {}).items():
        path_level_params = path_item.get("parameters", [])

        for method, operation in path_item.items():
            if method not in HTTP_METHODS:
                continue

            parameters = list(path_level_params) + list(operation.get("parameters", []))

            yield {
                "method": method.upper(),
                "raw_path": raw_path,
                "normalized_path": normalize_path(raw_path),
                "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "tags": operation.get("tags", []),
                "parameters": parameters,
                "request_body": operation.get("requestBody"),
                "responses": operation.get("responses", {}),
            }


def schema_to_python_type(schema: dict[str, Any] | None) -> str:
    """
    Convert an OpenAPI schema object to a Python type string.

    Uses conservative type mapping:
    - integer → int
    - number → float
    - string → str (or bytes for binary format)
    - boolean → bool
    - array → list[T]
    - object → dict[str, Any]
    - unknown → Any

    Args:
        schema: OpenAPI schema object

    Returns:
        Python type string
    """
    if not schema:
        return "Any"

    if "$ref" in schema:
        return schema["$ref"].rsplit("/", 1)[-1]

    openapi_type = schema.get("type")
    fmt = schema.get("format")

    if openapi_type == "integer":
        return "int"
    if openapi_type == "number":
        return "float"
    if openapi_type == "boolean":
        return "bool"
    if openapi_type == "string":
        if fmt == "binary":
            return "bytes"
        return "str"
    if openapi_type == "array":
        return f"list[{schema_to_python_type(schema.get('items'))}]"
    if openapi_type == "object":
        props = schema.get("properties")
        if props:
            return "dict[str, Any]"
        return "dict[str, Any]"

    return "Any"


def extract_params(operation: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Extract parameter information from an operation.

    Returns a list of dictionaries containing:
    - name: Parameter name
    - in: Parameter location (path, query, header, etc.)
    - required: Whether parameter is required
    - description: Parameter description
    - origin_type: Python type string derived from schema
    - example: Example value (if present)

    Args:
        operation: Operation dictionary from iter_operations()

    Returns:
        List of parameter dictionaries
    """
    out = []
    for param in operation["parameters"]:
        schema = param.get("schema") or {}
        out.append(
            {
                "name": param["name"],
                "in": param.get("in"),
                "required": param.get("required"),
                "description": param.get("description", ""),
                "origin_type": schema_to_python_type(schema),
                "example": param.get("example"),
            }
        )
    return out


def extract_request_body_fields(operation: dict[str, Any]) -> list[dict[str, Any]]:
    """
    Extract request body field information from an operation.

    Returns a list of dictionaries containing:
    - name: Field name
    - in: Always "body"
    - media_type: Content type (e.g., "application/json")
    - required: Whether field is required
    - origin_type: Python type string derived from schema
    - description: Field description

    Args:
        operation: Operation dictionary from iter_operations()

    Returns:
        List of request body field dictionaries
    """
    request_body = operation.get("request_body")
    if not request_body:
        return []

    fields = []
    for media_type, media in (request_body.get("content") or {}).items():
        schema = media.get("schema") or {}
        for name, prop_schema in (schema.get("properties") or {}).items():
            fields.append(
                {
                    "name": name,
                    "in": "body",
                    "media_type": media_type,
                    "required": name in schema.get("required", []),
                    "origin_type": schema_to_python_type(prop_schema),
                    "description": prop_schema.get("description", ""),
                }
            )
    return fields


def extract_response_fields(operation: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """
    Extract response field information from an operation.

    Returns a dictionary mapping field names to metadata containing:
    - status: HTTP status code
    - media_type: Content type
    - origin_type: Python type string derived from schema
    - description: Field description

    Handles both object and array response schemas.

    Args:
        operation: Operation dictionary from iter_operations()

    Returns:
        Dictionary mapping field names to field metadata
    """
    fields: dict[str, dict[str, Any]] = {}

    for status, response in operation.get("responses", {}).items():
        for media_type, media in ((response or {}).get("content") or {}).items():
            schema = media.get("schema") or {}

            # Common OpenAPI response shapes:
            # object with properties, or array of object with properties.
            candidate = schema.get("items") if schema.get("type") == "array" else schema
            for name, prop_schema in (candidate.get("properties") or {}).items():
                fields[name] = {
                    "status": status,
                    "media_type": media_type,
                    "origin_type": schema_to_python_type(prop_schema),
                    "description": prop_schema.get("description", ""),
                }

    return fields
