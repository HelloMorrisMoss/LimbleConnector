# Data Model: LimbleConnector Registry Schema

The `registry.yaml` is the central "internal spec" and source of truth for the SDK's public contract.

## Entities

### 1. Endpoint Registry (Root)
| Field | Type | Description |
|-------|------|-------------|
| `version` | `str` | Spec version (SemVer) |
| `resources` | `dict[str, Resource]` | Resource-level grouping (e.g., `assets`, `users`) |

### 2. Resource
| Field | Type | Description |
|-------|------|-------------|
| `endpoints` | `dict[str, Endpoint]` | Operation-level mapping (e.g., `search`, `get_by_id`) |
| `sub_resources` | `dict[str, Resource]` | Nested resource groups |

### 3. Endpoint
| Field | Type | Description |
|-------|------|-------------|
| `postman_id` | `str` | Reference to the Postman collection item ID |
| `method` | `str` | HTTP verb (GET, POST, etc.) |
| `path` | `str` | URL path with placeholders (e.g., `/assets/{id}`) |
| `stability` | `str` | `Stable`, `Experimental`, or `Deprecated` |
| `pagination` | `PaginationMapping` | Mapping for the `Paginator` interface (FR-011) |
| `responses` | `ResponseMapping` | Stabilization rules for upstream fields (FR-005) |
| `auth_override` | `AuthMapping` | Optional per-endpoint auth rules (FR-012) |

### 4. PaginationMapping
| Field | Type | Description |
|-------|------|-------------|
| `strategy` | `str` | `offset`, `cursor`, or `page` |
| `next_field` | `str` | Upstream field for next page (e.g., `next_token`) |
| `limit_field` | `str` | Upstream field for page limit |

### 5. ResponseMapping
| Field | Type | Description |
|-------|------|-------------|
| `fields` | `dict[str, str]` | Upstream -> SDK field mapping (e.g., `AssetId: asset_id`) |
| `defaults` | `dict[str, any]` | Default values for missing fields |
| `type` | `str` | `dict`, `list[dict]`, or `dataframe` |

## Validation Rules
- All `snake_case` field names for the SDK.
- Mandatory `postman_id` to maintain link with the Postman source.
- `stability` must be `Stable` for all curated operations.
