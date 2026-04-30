# Feature Specification: LimbleConnector Spec-Driven Wrapper (Hybrid Option C)

**Feature Branch**: `001-spec-driven-wrapper`
**Created**: 2026-02-27
**Status**: Refined
**Refined**: 2026-04-29 — Added FR-021 for registry access utilities
**Refined**: 2026-04-30 — Enhanced FR-018 to use OpenAPI spec as supplemental source for origin_type
**Input**: Refined prompt for Hybrid SDK implementation (Option C)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Postman-Driven Endpoint Addition (Priority: P1)

As an SDK developer, I want to add a new upstream endpoint by importing its definition from the Limble Postman collection into the internal spec, so that it becomes part of the SDK's generic layer with zero manual coding.

**Why this priority**: High priority as it enables the core "Spec-Driven" value proposition and ensures the SDK can quickly catch up with upstream API expansion.

**Independent Test**: Can be tested by adding a new endpoint to the Postman collection, running the generator, and verifying that the endpoint is available via the fluent API with full IDE typing support.

**Acceptance Scenarios**:

1. **Given** a new endpoint is added to the Postman collection JSON, **When** I update the internal spec and run the generation tool, **Then** the endpoint MUST be accessible via `lc.<resource>.<method>()` in my IDE.
2. **Given** the generator has run, **When** I inspect the typing artifacts, **Then** they MUST contain the correct parameter and return type stubs for the new endpoint.

---

### User Story 2 - Curated Operation Implementation (Priority: P2)

As an SDK user, I want stable, high-level methods for common workflows (like "Get a user and add them to a team") that remain consistent even if the underlying generic endpoints change.

**Why this priority**: Provides the "premium" developer experience for high-value tasks while keeping the base generic layer clean and unpolluted.

**Independent Test**: Can be tested by implementing a curated method in a separate layer, calling multiple generic endpoints internally, and verifying the stable result.

**Acceptance Scenarios**:

1. **Given** a curated operation `search_assets()` is defined, **When** I call it, **Then** it MUST orchestrate the necessary calls to the generic `assets` endpoints internally and return a normalized, stable result.
2. **Given** an internal implementation of a curated operation, **When** I add a contract test, **Then** it MUST validate the output against a stable schema independently of the upstream payload.

---

### User Story 3 - Stability Shielding (Priority: P3)

As an SDK user, I want my code to continue working without modification even when Limble releases a breaking change to their API.

**Why this priority**: One of the core principles of the SDK is "Stability-First". It prevents user-side breakages.

**Independent Test**: Can be tested by modifying a mock response to simulate an upstream change, updating the SDK's internal adapter logic, and verifying that the public API continues to return the expected data.

**Acceptance Scenarios**:

1. **Given** Limble renames a field in an upstream response, **When** I update the mapping/adapter logic in the internal spec, **Then** the SDK's public return types MUST remain unchanged.

### Edge Cases

- **Handling Unknown Response Shapes**: For endpoints without a defined response schema in Postman, the generator will default to a generic `dict[str, Any]` to ensure all endpoints are accessible (SC-001) while emitting a warning for further documentation.
- **Auth Inheritance Complexity**: The SDK will default to the collection-level auth, with per-endpoint overrides defined in the internal spec for requests requiring custom authentication methods.
- **Pagination Misalignment**: The SDK will use a unified `Paginator` interface defined in the internal spec to map varied upstream pagination strategies to a consistent `list().next()` behavior.

## Clarifications

### Session 2026-03-02
- Q: How should the system handle an endpoint with no defined response schema in Postman? → A: Default to a generic dictionary (`dict[str, Any]`) and emit a warning during generation.
- Q: How should the SDK handle varied pagination methods (e.g., limit/offset vs. cursor-based)? → A: Provide a standard `Paginator` interface where the internal spec file defines the mapping for each endpoint.
- Q: How should the generator and SDK handle complex auth overrides in Postman? → A: Default to the collection's primary auth; provide a manual override mechanism in the internal spec for specific endpoints.
- Q: How should the IDE typing artifacts (stubs/modules) for the generic layer be managed? → A: Generate generic layer stubs and commit them to the repository (synchronized via internal spec updates).
- Q: What format should the "internal spec file" (endpoint registry) use for stabilization? → A: YAML (for high readability and powerful mapping/override support).
- Q: Should the initial version of the spec-driven generic layer support asynchronous calls (`async/await`)? → A: No, synchronous only for the initial version; `async` is out of scope.
- Q: How should the SDK handle logging of request/response cycles? → A: Use standard Python `logging` with a dedicated logger name (e.g., `LimbleConnector`).
- Q: Should the SDK automatically handle 429 (Too Many Requests) errors? → A: Yes, implement automatic retries with exponential backoff for transient errors (429, 502, 503). Reference `RateLimitHandler` in `util.py` for inspiration but adapt it to best practices.
- Q: How should the SDK handle large result sets from `list()` operations? → A: Return a full list of all items by auto-paginating until the end by default.
- Q: Are specialized features like webhooks and file uploads in scope? → A: No, they are out of scope for the initial version of the generic layer.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001: Postman Translation Engine**: System MUST derive the generic endpoint layer from the `Limble API V2.postman_collection.json`.
- **FR-002: Naming Normalization**: System MUST translate Postman's folder-based hierarchy and endpoint names into a predictable, snake_case fluent namespace (e.g., `Routes > Assets > Search` -> `lc.assets.search`).
- **FR-003: Dynamic Attachment**: Generic endpoints MUST be attached to the `LimbleConnection` instance at runtime using a deterministic registry derived from the internal spec.
- **FR-004: Standard Method Contract**: Every generic endpoint MUST support baseline methods: `get()`, `list()`, `create()`, `update()`, `delete()`, and `raw()` where applicable.
- **FR-005: Internal Spec Source-of-Truth**: The SDK's public contract MUST be defined in an internal YAML spec file that stabilizes the Postman definitions and defines mapping/override logic.
- **FR-006: Curated Layer Separation**: Curated operations MUST live in a separate layer from generic endpoints to avoid polluting the dynamic base implementation.
- **FR-007: Scaffolding and Typing**: System MUST generate IDE-visible typing artifacts (stubs or modules) that synchronize with the dynamic endpoint registry.
- **FR-008: Error Normalization**: Errors MUST be mapped to a typed exception hierarchy with metadata including endpoint name, status code, and redacted response context.
- **FR-009: Contract Validation**: Every endpoint MUST have associated JSON fixtures and validation tests to detect upstream drift.
- **FR-010: Unknown Response Handling**: If an endpoint lacks a defined response schema in Postman, the system MUST default its return type to a generic dictionary (`dict[str, Any]`) and emit a warning during the generation phase to ensure SC-001 is met.
- **FR-011: Unified Pagination**: The system MUST provide a standard `Paginator` interface for generic endpoints, with specific field mapping (e.g., `next_token` vs `page`) defined in the internal spec file to ensure consistency.
- **FR-012: Auth Strategy Overrides**: The system MUST support an auth strategy registry in the internal spec, defaulting to the collection-level auth but allowing per-endpoint overrides.
- **FR-013: Committed Typing Stubs**: The system MUST generate and commit IDE-visible typing stubs (`.pyi` files) for all Postman-derived generic endpoints to the repository to ensure SC-002 is met across all developer environments.
- **FR-014: Auto-Pagination by Default**: The `list()` method on generic endpoints MUST auto-paginate until the end of the result set and return a full list of items, abstracting away individual page requests.
- **FR-015: Parameter Support Validation**: The system MUST provide a mechanism to check if a specific query parameter is supported by an endpoint (e.g., via `supports_query_param()`) based on the internal spec to prevent invalid requests.
- **FR-016: Query Parameter Processing**: The generator MUST include all documented API query parameters in the registry with relevant metadata (key, value, description, type information), omitting the 'disabled' property as it is Postman UI state-specific (indicating whether the parameter is sent in example requests).
- **FR-017: Response Data Extraction**: The generator MUST parse tabular 'return data' and 'response data' sections from Postman endpoint descriptions and populate the ResponseMapping fields in the registry with field names, descriptions, and type information.
- **FR-018: Type Inference System**: Both query_params and response fields MUST include a comprehensive type system with:
  - `type`: Final computed type derived from the preference order: override_type > origin_type > inferred_type
  - `inferred_type`: Type inferred from examples, patterns, and naming conventions
  - `origin_type`: Explicit type declarations from upstream sources, with precedence: OpenAPI schema type > Postman explicit table type (when available)
  - `override_type`: Manual configuration value (initially empty, preserved on updates)
  - The generator MUST use the Postman-generated OpenAPI spec (`20260430 - Limble API V2.postman OpenAPI3.0 generated spec.yaml`) as a supplemental source for `origin_type` by extracting parameter/request/response schema types, following conservative type mapping (integer→int, string→str, array→list[T], object→dict[str, Any]/TypedDict candidate)
- **FR-019: Override Preservation**: When the generator updates or creates registry entries, it MUST preserve existing override_type values.
- **FR-020: Type Conflict Warnings**: The generator MUST emit warnings when updating registry entries if the newly generated inferred_type or origin_type differs from the existing values, allowing developers to review and confirm the changes or set override_type.
- **FR-021: Registry Access Utilities**: The system MUST provide utilities for runtime access to the registry.yaml file, including `get_registry()` to return the parsed registry content and `get_registry_path()` to return the file path, enabling programs using the package to inspect available LimbleEndpoint properties at runtime.

### Key Entities

- **Endpoint Registry**: A centralized definition of all generic endpoints and their mapping rules.
- **Curated Operation**: A stable, high-level method that encapsulates one or more generic endpoint calls.
- **Normalized Schema**: A stable data structure returned by curated operations and some generic helpers (e.g., `.df()`).

### Non-Functional Requirements

- **NFR-001: Standard Logging**: The SDK MUST use the standard Python `logging` module with a dedicated logger named `LimbleConnector` to allow user-configurable observability of request/response cycles.
- **NFR-002: Automatic Resilience**: The SDK MUST implement a retry mechanism with exponential backoff for transient errors (HTTP 429, 502, 503) to ensure robustness without requiring user-side retry loops.

## Out of Scope

- **Asynchronous (async/await) support**: The initial implementation is limited to synchronous Python calls only.
- **Specialized Features (Webhooks/File Uploads)**: These features are excluded from the initial scope to prioritize stabilizing core CRUD/Search operations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of upstream endpoints in the Postman collection are accessible via the SDK's generic layer.
- **SC-002**: 100% of the public API surface provides IDE-visible typing with zero "missing member" errors.
- **SC-003**: 0% breaking changes to "Curated Operations" for at least 12 months, regardless of upstream changes.
- **SC-004**: CI pipeline catches 100% of schema drift regressions via contract tests.
- **SC-005**: Adding a new endpoint definition to the internal spec and generating its stubs takes less than 5 minutes of developer effort.
