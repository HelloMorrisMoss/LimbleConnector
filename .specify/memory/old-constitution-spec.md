# LimbleConnection Constitution

*Interpretation of Requirement Language

The keywords MUST, MUST NOT, SHALL, SHOULD, SHOULD NOT, and MAY
are to be interpreted as described in RFC 2119.*


## Core Principles

### Code Quality & Architecture
#### I. Intuitive Fluent API
The primary value of this library is the transition from manual `requests` calls to an object-oriented interface. Maintain a "Fluent Interface API" feel across all endpoints, ensuring dot-notation access (e.g., `lc.assets.df`) is consistent and predictable.

#### II. Compositional Integrity
Use `LimbleEndpoint` as a reusable component for various API resources. Keep the `LimbleConnection` entry point clean and focused on orchestration, delegating resource-specific logic to dedicated endpoint implementations.

#### III. Synchronized Scaffolding
Dynamic endpoints MUST ship IDE-visible typing via generated .pyi stubs or generated static endpoint modules. Placeholders alone are not sufficient.

#### IV. Analysis-Ready Data Structures
Prefer returning standard Python types (lists/dicts) or high-level abstractions like `pandas.DataFrame`. Data returned by the library SHOULD be normalized into stable, documented structures suitable for analysis without requiring additional structural transformation.

### Security Standards
#### V. Credential Neutrality
The library MUST never store or "leak" credentials. It MUST accept `b64_credentials` or raw secrets at runtime and pass them directly to the headers. No hardcoded secrets are permitted in the codebase.

#### VI. Configuration Isolation
Sensitive data like proxies or internal IDs MUST remain in `untracked_config/` or environment variables. The `.gitignore` MUST be strictly enforced to prevent local configuration from reaching version control.

#### VII. Secure Transport & Sanitized Logging
All connections MUST default to HTTPS and respect system-level SSL certificates.
LimbleConnection SHOULD allow injection of a custom HTTP session or transport adapter.
Logging must avoid full API response bodies or authorization headers to prevent accidental exposure of PII or secrets in production logs. Logging MUST NOT expose secrets even in debug mode.


Sensitive fields MUST be redacted in logs, including:
* Authorization headers
* tokens
* password fields
* cookies

### User Experience (UX)
#### VIII. Abstraction of Complexity
Handle pagination and retryable failures (429/5xx/timeouts) internally with configurable backoff.
Retry logic MUST only retry idempotent operations unless explicitly documented otherwise.
Network requests MUST specify a timeout and MUST NOT rely on library defaults.
Authentication strategies MUST be pluggable; only implement refresh flows if supported by the auth scheme.

#### IX. Opt-Out Granularity
Quality-of-life features that "change" data (like timestamp conversion) or automate flow (like pagination) MUST be toggleable. Users MUST be able to opt out of these abstractions at the `LimbleConnection` instance level or via specific method parameters to access "raw" API behavior when needed.

#### X. Meaningful Error Mapping
Map errors to typed exceptions with actionable context. Automatic recovery is allowed only for transient failures and MUST be bounded (max retries/time).

### Testing & Reliability
#### XI. Mock-Based Isolation
The test suite MUST be runnable without an active internet connection. Use `responses` or `pytest-mock` to simulate Limble API v2 responses, ensuring the library\'s logic is tested independently of the live service.

#### XII. Contract Tests for Upstream Drift Detection

The SDK SHALL include contract tests to detect upstream schema drift and mapping regressions.

For each endpoint:

1. Representative JSON fixtures SHALL be stored as test artifacts.
2. Mapping logic SHALL be validated against these fixtures.
3. .df() output structure SHALL be validated via snapshot or schema tests.
4. Spec updates MUST trigger:
   * Generator execution
   * Mapping validation tests
   * Regression test updates if necessary 

If a spec change modifies an expected structure, the change MUST be reflected in both:
* Test fixtures
* Documentation placeholders

The test suite MUST run fully offline.

#### XIII. Schema & Mapping Verification
The automated class generation logic SHOULD be used to validate that incoming API data matches the expected structure. Every endpoint added to `__endpoints__` requires a corresponding test case to ensure dynamic mapping functions correctly.

### Versioning & Compatibility
#### XIV. Standard Semantic Versioning (SemVer)

The SDK SHALL follow Semantic Versioning (SemVer):
`MAJOR.MINOR.PATCH`

* MAJOR — Breaking changes to the public API surface.
* MINOR — Backward-compatible feature additions.
* PATCH — Backward-compatible bug fixes, internal refactors, documentation updates.

Breaking changes include (but are not limited to):
* Renaming or removing public methods or attributes.
* Changing return types of public methods.
* Changing default behavior in a way that alters user-visible results.
* Modifying exception types raised for known error states.
* Removing deprecated functionality.

Additive changes (new endpoints, new optional parameters, new fields in return payloads) MUST be released as MINOR versions.

Internal-only refactors SHOULD NOT require a MAJOR bump. If behavior changes, SemVer rules apply.

#### XV. Explicit Public API Surface Definition

The following components constitute the Public API Surface covered by SemVer guarantees:
* LimbleConnection constructor signature and configuration parameters.
* Public endpoint attributes (e.g., lc.assets, lc.work_orders, etc.).
* Public endpoint methods (e.g., .list(), .get(), .df(), .raw()).
* Return types and structural guarantees of high-level helper methods.
* Exception class names and hierarchy (e.g., LimbleConnectionError, RateLimitExceeded).
* Documented configuration behaviors (pagination defaults, retry logic, timestamp conversion rules).

The following items are NOT part of the public API:
* Private modules or names prefixed with _.
* Internal scaffolding or generator implementation.
* Undocumented helper functions.
* Exact upstream Limble payload content (fields may change upstream), except where the SDK explicitly normalizes into stable return shapes.

If a change affects the Public API Surface, a MAJOR version bump is required.

#### XVI. SDK Stability First Policy (Upstream Change Handling)

When upstream Limble API behavior changes:
1. The SDK SHALL attempt to preserve existing SDK behavior whenever possible.
2. Mapping or adapter logic SHOULD shield users from upstream breaking changes.
3. A MAJOR version bump SHALL occur only if preserving behavior is impossible without breaking the SDK’s public API contract.

The SDK SHALL NOT mirror upstream breaking changes blindly.

#### XVII. Deprecation Policy

Breaking changes MUST follow a structured deprecation cycle:

1. A feature MUST be marked deprecated in a MINOR release.
2. A FutureWarning (or DeprecationWarning if explicitly documented) SHALL be emitted at runtime when the deprecated feature is used.
3. The deprecation MUST include:
   * Clear explanation of what is changing.
   * Explicit migration guidance.
4. Deprecated functionality SHALL remain available for:
   * At least one MINOR release, AND
   * At least 60 days (recommended minimum) before removal.
5. Removal SHALL occur only in a MAJOR release.

Warnings MUST be emitted at call-time, not import-time.

#### XVIII. Versioned Namespaces (Forward Compatibility)

The SDK SHALL support versioned namespace isolation to prepare for future API versions.

    LimbleConnector/
        v2/
            connection.py


Public import paths SHOULD remain stable:

    from LimbleConnector.v2 import LimbleConnection


If a future Limble API v3 is introduced, it SHALL be implemented under:

    LimbleConnector.v3


WITHOUT breaking v2 behavior within the same MAJOR version of the SDK.

New upstream API versions SHOULD be implemented as additional namespaces within the same SDK unless architectural incompatibility makes coexistence impractical.

#### XIX. Changelog Discipline

The repository SHALL maintain a `CHANGELOG.md` using the “Keep a Changelog” format.

Each release MUST include sections for:
* Added
* Changed
* Deprecated
* Removed
* Fixed
* Security

All Pull Requests that modify the Public API Surface MUST include a changelog entry.

Changelog entries MUST describe user-visible behavior changes, not internal refactors.

Release & Enforcement Workflow
#### XX. Release Gating Requirements
Before any release:
* ruff (or equivalent linter) MUST pass.
* mypy or pyright MUST pass on public modules.
* Full test suite MUST pass.
* Public API diff MUST be reviewed if endpoints are changed.
* Changelog MUST be updated.
EXAMPLE — replace with actual commands:

    uv run ruff check .
    uv run mypy limble_sdk
    uv run pytest

#### XXI. Spec-Driven Enforcement (Post-Migration Policy)
Since spec-driven development is being introduced mid-project:
1. All new endpoints MUST be introduced through .specify.
2. Existing endpoints SHALL be gradually migrated to spec-driven generation.
3. Manual endpoint definitions SHOULD NOT be added once spec scaffolding exists.
Exceptions MAY be allowed for hotfixes or upstream emergency changes, but MUST be replaced with spec-generated implementations in the next MINOR release.
4. Spec diffs MUST be reviewed as part of the PR review.
5. Generated files MUST include a header comment indicating they are auto-generated and a validation hash. CI SHOULD verify generated files' content match generator output.

EXAMPLE — replace with actual file paths:
* .specify/limble_v2.yaml
* _documentation_placeholders.py
* limble_sdk/v2/_generated_endpoints.py

## Development Workflow
1.  **Specify:** Document the V2 endpoint contract in `.specify`.
2.  **Generate:** Execute scaffolding scripts to update `_documentation_placeholders.py`.
3.  **Implement:** Map the endpoint in `LimbleConnection` and verify the `LimbleEndpoint` integration.
4.  **Test:** Create a mock-based regression test for the new mapping.


## Technical Constraints
*   **Target Environment:** Python 3.11+ managed via `uv`.
*   **Dependencies:** Keep core dependencies lightweight where possible.
*   **Protocol:** Strictly target Limble API v2.


## Governance
This constitution supersedes individual coding preferences.
All PRs and updates to the core connection logic MUST verify compliance with these principles.
Complexity added to the library MUST be justified by a significant improvement in developer ergonomics.

**Version**: 0.0.0 | **Ratified**: 2026-02-18 | **Last Amended**: 2026-02-18
