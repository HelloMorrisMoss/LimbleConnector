# Feature Specification: LimbleConnector Spec-Driven Wrapper (Hybrid Option C)

**Feature Branch**: `001-spec-driven-wrapper`  
**Created**: 2026-02-27  
**Status**: Draft  
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

As an SDK user, I want stable, high-level methods for common workflows (like "Search and update work orders") that remain consistent even if the underlying generic endpoints change.

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

- **Handling Unknown Response Shapes**: How does the system handle an endpoint with no defined response schema in Postman? [NEEDS CLARIFICATION: Should we default to a generic dict or require a manual fixture?]
- **Auth Inheritance Complexity**: What happens if an endpoint has complex auth overrides that differ from the collection default?
- **Pagination Misalignment**: How to handle upstream endpoints that use inconsistent pagination tokens?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001: Postman Translation Engine**: System MUST derive the generic endpoint layer from the `Limble API V2.postman_collection.json`.
- **FR-002: Naming Normalization**: System MUST translate Postman's folder-based hierarchy and endpoint names into a predictable, snake_case fluent namespace (e.g., `Routes > Assets > Search` -> `lc.assets.search`).
- **FR-003: Dynamic Attachment**: Generic endpoints MUST be attached to the `LimbleConnection` instance at runtime using a deterministic registry derived from the internal spec.
- **FR-004: Standard Method Contract**: Every generic endpoint MUST support baseline methods: `get()`, `list()`, `create()`, `update()`, `delete()`, and `raw()` where applicable.
- **FR-005: Internal Spec Source-of-Truth**: The SDK's public contract MUST be defined in an internal spec file that stabilizes the Postman definitions.
- **FR-006: Curated Layer Separation**: Curated operations MUST live in a separate layer from generic endpoints to avoid polluting the dynamic base implementation.
- **FR-007: Scaffolding and Typing**: System MUST generate IDE-visible typing artifacts (stubs or modules) that synchronize with the dynamic endpoint registry.
- **FR-008: Error Normalization**: Errors MUST be mapped to a typed exception hierarchy with metadata including endpoint name, status code, and redacted response context.
- **FR-009: Contract Validation**: Every endpoint MUST have associated JSON fixtures and validation tests to detect upstream drift.

### Key Entities

- **Endpoint Registry**: A centralized definition of all generic endpoints and their mapping rules.
- **Curated Operation**: A stable, high-level method that encapsulates one or more generic endpoint calls.
- **Normalized Schema**: A stable data structure returned by curated operations and some generic helpers (e.g., `.df()`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of upstream endpoints in the Postman collection are accessible via the SDK's generic layer.
- **SC-002**: 100% of the public API surface provides IDE-visible typing with zero "missing member" errors.
- **SC-003**: 0% breaking changes to "Curated Operations" for at least 12 months, regardless of upstream changes.
- **SC-004**: CI pipeline catches 100% of schema drift regressions via contract tests.
- **SC-005**: Adding a new endpoint definition to the internal spec and generating its stubs takes less than 5 minutes of developer effort.
