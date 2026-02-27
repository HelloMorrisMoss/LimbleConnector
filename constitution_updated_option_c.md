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
Releases MUST pass linting, typing, tests, and changelog verification.

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

## Technical Constraints
Python 3.11+ runtime.
Dependencies SHOULD remain minimal.
Target API: Limble v2.

---

## Governance
This constitution supersedes individual coding preferences.
All PRs and updates to the core connection logic MUST verify compliance with these principles.
Complexity added to the library MUST be justified by a significant improvement in developer ergonomics.
