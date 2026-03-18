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
2. Run the generator:
   ```bash
   python -m LimbleConnection._generate_classes_automatically.generator
   ```
3. The `registry.yaml` and `.pyi` stubs will be updated.
4. The new endpoint is immediately available in the SDK with full typing.
