# Quickstart: LimbleConnector Spec-Driven Wrapper

This document provides a preview of how the new Spec-Driven Wrapper will be used.

## Installation
```bash
pip install LimbleConnector
```

## Generic Endpoint Usage (Dynamic)
The generic layer is derived from the Postman collection.

```python
from LimbleConnection import LimbleConnection

# Initialize the connection
lc = LimbleConnection(client_id="...", client_secret="...")

# Access endpoints via the fluent API (full IDE typing support)
assets = lc.assets.list()  # Auto-paginates (FR-014)
print(f"Total assets: {len(assets)}")

# Search for specific assets
results = lc.assets.search(query="Tractor")

# Access raw response if needed (Constitution X)
raw = lc.assets.list().raw()
```

## Curated Operation Usage (Stable)
High-level workflows for common tasks.

```python
# Curated search with stability guarantees (User Story 2)
assets = lc.search_assets(category="Vehicles")

# Stability shielding (User Story 3)
# Even if Limble changes 'AssetId' to 'id' upstream, 
# 'asset_id' remains stable in the SDK.
for asset in assets:
    print(asset["asset_id"])
```

## Updating the SDK Inventory
When Limble releases a new API version or endpoint in Postman:

1. Update the `Limble API V2.postman_collection.json`.
2. (Optional) Update the `20260430 - Limble API V2.postman OpenAPI3.0 generated spec.yaml` for enhanced type information.
3. Run the generator:
   ```bash
   python -m LimbleConnection._generate_classes_automatically.generator
   ```
4. The `registry.yaml` and `.pyi` stubs will be updated.
5. The new endpoint is immediately available in the SDK with full typing.

### Type Information Sources (FR-018)

The generator uses multiple sources to infer accurate Python types for parameters and response fields:

- **OpenAPI spec** (if available): Provides machine-readable schema types (integer→int, string→str, etc.)
- **Postman collection**: Provides explicit type declarations from description tables
- **Pattern inference**: Infers types from parameter names and example values
- **Manual overrides**: Preserves human-curated type corrections in `registry.yaml`

**Type precedence**: `override_type > origin_type (OpenAPI > Postman) > inferred_type`

The OpenAPI spec is automatically used if present at:
`20260430 - Limble API V2.postman OpenAPI3.0 generated spec.yaml`
