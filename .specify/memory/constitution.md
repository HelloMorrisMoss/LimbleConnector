<!--
Sync Impact Report
- Version change: 0.0.0 → 0.1.0
- Modified principles: 
    - XIV. Mapping Verification (Clarified with fixture requirements)
    - XXI. Release Quality Gates (Expanded with explicit tool chain)
- Added sections: 
    - Development Workflow (New Section)
- Removed sections: None
- Templates requiring updates: 
    - ✅ .specify/templates/plan-template.md (Synced Quality Gates)
    - ✅ .specify/templates/tasks-template.md (Synced Task Categories)
- Follow-up TODOs: 
    - TODO(RATIFICATION_DATE): Confirm original adoption date for v0.1.0.
-->
# LimbleConnection Constitution

Interpretation of Requirement Language

The keywords **MUST**, **MUST NOT**, **SHALL**, **SHOULD**, **SHOULD NOT**, and **MAY** are to be interpreted as described in RFC 2119.

---

## Core Principles

### Code Quality & Architecture

#### I. Intuitive Fluent API
All endpoints MUST maintain a predictable fluent interface with consistent naming and behavior.

#### II. Compositional Integrity
`LimbleConnection` MUST orchestrate. Endpoint implementations MUST encapsulate resource logic.

#### III. Synchronized Scaffolding
Dynamic endpoints MUST provide IDE-visible typing via generated or static typing artifacts.

#### IV. Stable Data Structures
Returned data SHOULD use standard Python types or documented abstractions and MUST be normalized into stable, documented schemas independent of upstream payload structure.

#### V. Hybrid Surface: Generic Endpoints + Curated Operations
The SDK MUST expose two tiers of functionality:

1. **Generic endpoints** (broad coverage)
   - MUST be discoverable via the fluent endpoint namespace.
   - MUST provide consistent baseline behaviors (timeouts, retries, raw access, error mapping, typing support).
   - SHOULD closely track the upstream endpoint inventory while remaining governed by this SDK’s stability guarantees.

2. **Curated operations** (high-value workflows)
   - MUST provide stable, documented higher-level behaviors for common tasks.
   - MUST remain backward compatible within SemVer guarantees, even when upstream changes require adapter logic.
   - MUST NOT force all endpoint-specific semantics into the generic endpoint base implementation.

---

### Security Standards

#### VI. Credential Neutrality
The library MUST NOT store or leak credentials, secrets, or PII.

#### VII. Configuration Isolation
Sensitive configuration MUST exist outside version control.

#### VIII. Secure Transport & Logging
Connections MUST use HTTPS and MUST redact secrets in logs. Logging MUST NOT expose credentials or sensitive payloads even in debug mode. The connection layer SHOULD allow custom transport injection.

---

### User Experience

#### IX. Complexity Abstraction
Pagination and retryable failures SHOULD be handled internally. Retries MUST be bounded and limited to idempotent operations. Network calls MUST specify timeouts. Authentication MUST be pluggable.

#### X. Opt‑Out Controls
Users MUST be able to disable automated transformations and access raw responses.

#### XI. Error Mapping
Errors MUST surface as typed exceptions with actionable context.

---

### Testing & Reliability

#### XII. Offline Testability
Tests MUST run without live API access.

#### XIII. Contract Validation
Automated validation MUST detect schema or mapping drift.

#### XIV. Mapping Verification
Generated or automated mappings SHOULD be validated against expected structures.

---

### Versioning & Compatibility

#### XV. Semantic Versioning
The SDK SHALL follow SemVer.

#### XVI. Public API Surface
The public API includes documented constructors, endpoints, return types, exceptions, curated operations, and configuration behavior. Undocumented or internal components are excluded.

#### XVII. Stability‑First Policy
The SDK SHOULD shield users from upstream changes whenever possible. Adapter logic SHOULD preserve SDK behavior when upstream contracts change.

#### XVIII. Deprecation Policy
Breaking changes MUST follow a documented deprecation cycle before removal.

#### XIX. API Version Namespacing
The SDK MUST support namespaced API versions so multiple upstream API versions may coexist.

#### XX. Changelog Discipline
User‑visible changes MUST be recorded in the changelog.

---

### Release Requirements

#### XXI. Release Quality Gates
To ensure stability, every release MUST satisfy the following automated and manual gates:

1.  **Static Analysis**: Linter MUST pass with zero errors.
2.  **Type Safety**: Type checker MUST pass on all public modules with no "missing member" errors.
3.  **Test Coverage**: Full suite execution via testing MUST achieve 100% pass rate.
4.  **Contract Integrity**: New or modified endpoints MUST include representative JSON fixtures and validated mapping tests.
5.  **Documentation**: All public methods MUST have docstrings, and the `CHANGELOG.md` MUST be updated for the current version.

---

### Spec Authority & Upstream Contract

#### XXII. Source of Truth Hierarchy
The upstream API inventory is defined by the official Limble Postman Collection export.

The SDK’s public contract (including curated operations and any normalized return schemas) MUST be defined and stabilized in an internal spec source-of-truth.

When upstream behavior changes, the spec and adapter/mapping layers MUST be updated to preserve SDK stability wherever feasible.

If discrepancies exist:
- the Postman collection is authoritative for **what exists upstream** (inventory, methods, paths).
- the internal spec is authoritative for **what the SDK guarantees** (public surface, normalized shapes, curated operations).

Generated artifacts MUST be reproducible and MUST NOT be manually edited.

---

## Development Workflow

To maintain the "Spec-Driven" nature of the project, the following workflow is MANDATORY:

1.  **Specify**: Document the endpoint contract in `.specify` (using `speckit.specify`).
2.  **Generate**: Execute scaffolding scripts to update typing stubs and documentation placeholders.
3.  **Implement**: Map the endpoint in `LimbleConnection` using the dynamic `LimbleEndpoint` logic.
4.  **Test**: 
    - Create a mock-based test using `responses` or `pytest-mock`.
    - Validate `.df()` output structure via snapshot tests.
5.  **Verify**: Run the `/speckit.analyze` command to ensure the implementation plan aligns with the Constitution.

---

## Technical Constraints
Python 3.11+ runtime.
Dependencies SHOULD remain minimal.
Target API: Limble v2.

---

## Governance

### I. Authority
This constitution is the supreme authority for the LimbleConnector project. It supersedes individual coding preferences. All Pull Requests MUST be audited for compliance with these principles. Complexity added to the library MUST be justified by a documented improvement in developer ergonomics.

### II. Amendment Procedure
1. **Proposal**: Amendments are proposed via Pull Request to `.specify/memory/constitution.md`.
2. **Review**: Amendments require a "Request for Comments" (RFC) period.
3. **Ratification**: Merging the PR constitutes ratification. The `LAST_AMENDED_DATE` MUST be updated to the merge date.

### III. Versioning Policy (SemVer)
The SDK follows Semantic Versioning (`MAJOR.MINOR.PATCH`):
- **MAJOR**: Breaking changes to the Public API Surface (renaming methods, changing return types, removing deprecated features).
- **MINOR**: Backward-compatible feature additions (new endpoints, optional parameters).
- **PATCH**: Backward-compatible bug fixes or documentation updates.

### IV. Deprecation Cycle
Breaking changes MUST follow a structured cycle:
1. Feature marked `Deprecated` in a MINOR release with a `FutureWarning`.
2. Migration guidance MUST be provided in the documentation and warning message.
3. Feature remains available for at least one MINOR release or 60 days.
4. Removal occurs ONLY in a MAJOR release.

### V. Compliance Review
Every release MUST include a "Public API Diff" review. All PRs modifying the Public API Surface MUST include a `CHANGELOG.md` entry following the "Keep a Changelog" format.


**Version**: 0.1.0 | **Ratified**: 2026-02-27 | **Last Amended**: 2026-02-27