# Refined Speckit Prompt for LimbleConnector Hybrid SDK (Option C)

You are a senior software architect. Your goal is to create a comprehensive `spec.md` for the LimbleConnector project that implements "Option C: Hybrid SDK".

## Context
- **Constitution**: Read `.specify/memory/constitution.md` (v0.1.0) and `.specify/memory/old-constitution-spec.md` (v0.0.0).
- **Upstream Source**: `Limble API V2.postman_collection.json`.
- **Current Architecture**: Dynamic endpoints in `LimbleConnection`, generated typing stubs, and a fluent API.

## Goal: Option C (Hybrid)
- **Generic Endpoints**: Broad coverage of the Postman collection. Predictable, fluent, consistent naming.
- **Curated Operations**: High-value semantic workflows that use generic endpoints. Stable, backward-compatible.

## Sections to Complete in `spec.md`

### 1. Header Metadata
- Feature Name: "LimbleConnector Spec-Driven Wrapper (Hybrid Option C)"
- Status: Draft
- Input: "Refined prompt for Hybrid SDK implementation"

### 2. User Scenarios & Testing
- **P1: Postman-Driven Endpoint Addition**: Adding a new endpoint from Postman to the internal spec, regenerating artifacts, and verifying fluent access.
- **P2: Curated Operation Implementation**: Adding a semantic wrapper (e.g., `assets.get_with_custom_fields`) that utilizes generic endpoints without bloating the base class.
- **P3: Stability Shielding**: Handling an upstream breaking change by updating the internal spec and adapter layer to preserve the SDK's public contract.
- **Acceptance Scenarios**: Use Gherkin (Given/When/Then).

### 3. Requirements
- **Postman → Internal Spec Translation**: Naming conventions (camelCase to snake_case), auth inheritance, variable mapping.
- **Endpoint Registry**: Deterministic attachment to `LimbleConnection`.
- **Generic Interface**: Standard methods (`get`, `list`, `create`, `update`, `delete`, `raw`). Consistent handling of pagination, retries, and timeouts.
- **Curated Operations layer**: Conceptual separation from generic endpoints.
- **Typing/Docs Generation**: Requirement for IDE support (stubs/modules) and docstrings.
- **Error Model**: Typed exception hierarchy with rich metadata.
- **Contract Tests**: Mandatory fixtures and snapshot validation for `.df()` output.

### 4. Success Criteria
- **Measurable Outcomes**:
  - Drift detection caught 100% of schema regressions in CI.
  - 0% breaking changes to curated operations despite upstream modifications.
  - End-to-end time to add an endpoint < 15 minutes.
  - 100% of public API has IDE-visible typing.

## Guidelines
- Avoid "HOW" (implementation details) where possible, focus on "WHAT" and "WHY".
- Maintain consistency with the Constitution.
- Use `[NEEDS CLARIFICATION]` for gaps.
