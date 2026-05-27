# Feature Specification: LimbleConnector Spec-Driven Wrapper (Hybrid Option C)

**Feature Branch**: `001-spec-driven-wrapper`
**Created**: 2026-02-27
**Status**: Refined
**Refined**: 2026-04-29 — Added FR-021 for registry access utilities
**Refined**: 2026-04-30 — Enhanced FR-018 to use OpenAPI spec as supplemental source for origin_type
**Refined**: 2026-05-27 — Added US4 and FR-022 for live registry type reconciliation via `attended_preliminary_testing.py`; extended FR-018 type system with `observed_type` field (with `Optional[X]` nullability convention) and revised precedence `override_type > origin_type > observed_type > inferred_type`; added `flag-and-prompt` / `flag-and-skip` reconciliation modes and split per-field nullability from whole-response non-representative samples; added FR-023 for opportunistic empty-response-shape capture at the endpoint level
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

---

### User Story 4 - Registry Type Reconciliation from Live Testing (Priority: P4)

As an SDK maintainer, I want the attended preliminary testing utility to optionally compare registry endpoint types against the types observed in live API responses and update the registry when they disagree, so that the registry's type information stays aligned with actual upstream behavior without manual reconciliation.

**Why this priority**: Keeps the registry's `inferred_type` and `origin_type` values accurate over time, directly supporting SC-004 (schema drift detection) and reducing the manual effort of reviewing FR-020 type conflict warnings. Lower priority than the core generic/curated layers because it is a maintainer workflow, not an end-user-visible feature.

**Independent Test**: Can be tested by deliberately seeding a registry entry with a wrong `inferred_type` or `origin_type`, running the testing utility with the type-update option enabled against a live endpoint, and verifying that the discrepancy is reported and the registry entry is updated (while any `override_type` is preserved).

**Acceptance Scenarios**:

1. **Given** a registry entry whose response field or query parameter type disagrees with the type observed in a live API response, **When** I run `attended_preliminary_testing.py` with the type-update option enabled in **`flag-and-prompt`** mode, **Then** the utility MUST classify the discrepancy (documentation drift / nullability / non-representative sample / prior-observation conflict / other), report it in a scannable form, and prompt for confirmation before writing `observed_type` to the registry.
2. **Given** the same conditions but **`flag-and-skip`** mode is selected, **When** the run completes, **Then** the utility MUST log each classified discrepancy without prompting and without writing to the registry, so the maintainer can review the log afterward.
3. **Given** a registry entry with a non-empty `override_type`, **When** a type discrepancy is detected for that field in either mode, **Then** the utility MUST NOT overwrite `override_type`; only `observed_type` may be updated by this path (preserving FR-019).
4. **Given** a live response where a record is fully populated but one of its fields is `null` (e.g., `address: None` in a `locations` record), **When** the utility records the observation, **Then** the observed_type MUST be `Optional[<type>]` and the discrepancy (if any) MUST be classified as **nullability**, NOT as non-representative sample.
5. **Given** the live response's whole envelope is empty (e.g., `[]`, `{}`, top-level `null`), **When** the utility records the observation, **Then** the discrepancy MUST be flagged as a **non-representative sample** with an explanation of why the observed_type may not be trustworthy, and (if FR-023 capture applies) the empty-response shape MUST be recorded against the endpoint.
6. **Given** a previously stored `observed_type` exists for a field, **When** a new run produces a different observed_type, **Then** the utility MUST flag this as a **prior-observation conflict** so the maintainer can decide whether to accept the new value, keep the old, or escalate to an `override_type`.
7. **Given** the type-update option is not enabled, **When** I run the testing utility, **Then** its behavior MUST be unchanged from before this refinement (live testing only, no registry writes).

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
  - `type`: Final computed type derived from the preference order: **override_type > origin_type > observed_type > inferred_type**
  - `inferred_type`: Type inferred from examples, patterns, and naming conventions
  - `origin_type`: Explicit type declarations from upstream sources, with precedence: OpenAPI schema type > Postman explicit table type (when available)
  - `observed_type`: Type recorded from live API responses by tooling such as `attended_preliminary_testing.py` (see FR-022). Empirical, may be absent until the field has been exercised against the live API. Initially empty; preserved on registry regeneration unless explicitly updated by reconciliation tooling. When a sampled field value is `null`/`None`, the observed_type MUST be recorded using `Optional[X]` notation (e.g., `Optional[str]`) where `X` is the non-null type derived from prior samples or, if no non-null sample exists yet, the inferred_type. The downstream consumers treat the type field as an opaque string, so `Optional[...]` is preserved without further parsing.
  - `override_type`: Manual configuration value (initially empty, preserved on updates)
  - Documentation is treated as canonical in the precedence (origin above observed) so that one-off live samples (nulls, empty containers, edge cases) do not silently displace declared types. Disagreement between `observed_type` and `origin_type` MUST surface via FR-020-style warnings rather than being silently buried by the precedence rule.
  - The generator MUST use the Postman-generated OpenAPI spec (`20260430 - Limble API V2.postman OpenAPI3.0 generated spec.yaml`) as a supplemental source for `origin_type` by extracting parameter/request/response schema types, following conservative type mapping (integer→int, string→str, array→list[T], object→dict[str, Any]/TypedDict candidate)
- **FR-019: Override Preservation**: When the generator updates or creates registry entries, it MUST preserve existing override_type values.
- **FR-020: Type Conflict Warnings**: The generator MUST emit warnings when updating registry entries if the newly generated inferred_type or origin_type differs from the existing values, allowing developers to review and confirm the changes or set override_type.
- **FR-021: Registry Access Utilities**: The system MUST provide utilities for runtime access to the registry.yaml file, including `get_registry()` to return the parsed registry content and `get_registry_path()` to return the file path, enabling programs using the package to inspect available LimbleEndpoint properties at runtime.
- **FR-022: Live Registry Type Reconciliation**: The semi-automated testing utility `tests/semiautomated/attended_preliminary_testing.py` MUST support an opt-in mode (off by default) that records the types observed in live API responses (for both response fields and query parameters exercised during testing) into the registry's `observed_type` field (FR-018), and reconciles them against the other registry type fields. When a discrepancy is detected, the utility MUST:
  - Classify the discrepancy by *kind* (see below) and report the endpoint, field name, conflicting type values, and kind to the maintainer.
  - Honor the configured reconciliation mode (see below) when deciding whether to write to the registry.
  - When a write occurs, update only `observed_type`; `override_type` MUST be preserved per FR-019. Updates to `inferred_type` or `origin_type` MUST NOT occur through this path (those have their own upstream sources).
  - Emit warnings consistent with FR-020 for each detected conflict.

  **Reconciliation modes** (selected per run; default is `flag-and-prompt`):
  - **`flag-and-prompt`** — full attended review. For every discrepancy the maintainer is prompted before any registry write. Optimizes for correctness.
  - **`flag-and-skip`** — autonomy/throughput. Discrepancies are logged with their kind but no registry write occurs and no prompt is shown; the maintainer reviews the run log afterward. Useful for sweeping many endpoints quickly to surface where attention is needed.

  **Discrepancy kinds** — discrepancies MUST be classified into at least the following so the maintainer can quickly judge whether action is needed:
  - **documentation drift** — `observed_type` disagrees with the upstream-declared `origin_type`.
  - **nullability** — a sampled field value was `null`/`None`, producing an `Optional[X]` observed_type that disagrees with a non-Optional `origin_type` or `inferred_type`. Distinct from "non-representative sample": the record itself is fully populated, the field is simply nullable.
  - **non-representative sample** — the **whole response envelope** is empty or a sentinel (e.g., `[]`, `{}`, top-level `null`), so the underlying field types cannot be reliably inferred from this observation; the warning MUST indicate *why* the sample is suspect. Per-field `None` values inside an otherwise populated record do NOT qualify (those are `nullability`).
  - **prior-observation conflict** — the newly observed_type differs from a previously stored `observed_type` for the same field.
  - **other** — any other detected mismatch or gotcha not covered above.

  Suspicion flagging is a maintainer concern; the registry's stored values and the end-user-facing computed `type` (FR-018) MUST NOT expose discrepancy-kind metadata. End users see only the resolved type; they should not have to inspect the registry to detect suspicious entries.

  Output MUST be optimized for scannability so that signals are not lost during an already tedious attended-testing workflow; concrete display format (grouping, ordering, color, batching) is deferred to the plan/research phase but MUST avoid wall-of-text presentation.

  The default (option-disabled) behavior MUST remain identical to the existing live-testing flow with no registry writes.
- **FR-023: Empty-Response Shape Documentation**: The registry MUST be able to record, per endpoint, the **shape of the response envelope when it carries no data** — e.g., whether an empty result arrives as `null`, `[]`, `{}`, or as a populated envelope like `{"data": [], "meta": {...}}`. This information lives at the `ResponseMapping` (endpoint) level, not per-field, and exists to help end users write correct guard conditions (`if response:` vs `if response.get("data"):` etc.) without trial-and-error.
  - The field MAY be absent for endpoints where an empty response is impossible (e.g., single-record `GET by ID`, which returns 404 instead).
  - Capture is opportunistic: the live-testing utility (FR-022) MUST record the empty-response shape **when it naturally observes one** during testing, but MUST NOT block, retry, or attempt to synthesize empty responses to populate the field. Endpoints whose tests never produce an empty result leave the field empty.
  - Once recorded, the value is preserved across registry regeneration in the same manner as `override_type` (FR-019); a maintainer-prompt path analogous to FR-022 MAY apply when a new observation conflicts with a stored one.
  - The recorded shape is for end-user-facing documentation/typing decisions; format (literal value, schema fragment, or summary string) is deferred to the plan/research phase.

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
