# Implementation Plan: LimbleConnector Spec-Driven Wrapper (Hybrid Option C)

**Branch**: `001-spec-driven-wrapper` | **Date**: 2026-03-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-spec-driven-wrapper/spec.md`
**Propagated**: 2026-04-29 — Updated from spec.md refinement

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

The goal is to implement a hybrid SDK architecture (Option C) that uses a Postman collection as the inventory source and a YAML internal spec as the stabilizer. This enables a generic layer with 100% endpoint coverage and a curated layer for high-value workflows.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: `requests`, `postmanparser`, `httpx`, `pandas` (for `.df()`)
**Storage**: Local YAML internal spec (Registry)
**Testing**: `pytest`, `responses` or `pytest-mock` (as per Constitution XII)
**Target Platform**: Python environments
**Project Type**: single project (SDK library)
**Performance Goals**: < 5 minutes for new endpoint addition; 100% coverage
**Constraints**: Synchronous only; Stability-First (SemVer); No credential leakage; Type inference system for query params and response fields
**Scale/Scope**: 100% of Limble API v2 endpoints (Postman-driven) with comprehensive type metadata

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Plan Alignment |
|-----------|-------------|----------------|
| I. Intuitive Fluent API | predictable fluent interface | FR-002: snake_case fluent namespace |
| III. Synchronized Scaffolding | IDE-visible typing | FR-007, FR-013: typing stubs committed |
| IV. Stable Data Structures | normalized schemas | FR-005, FR-006: internal spec and curated layer |
| V. Hybrid Surface | Generic + Curated | FR-001, FR-006: separate layers |
| VI-VIII. Security | No secrets in logs/VC | NFR-001: standard logging with redaction |
| IX. Complexity Abstraction | Pagination & Retries | FR-011, FR-014, NFR-002 |
| XII-XIV. Testing | Offline, Contract, Mapping | FR-009: JSON fixtures and contract tests |
| XXII. Source of Truth | Postman + Internal Spec | FR-001, FR-005: Postman is inventory, YAML is stability |

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
LimbleConnection/
├── _generate_classes_automatically/  # Scaffolding & Generation Logic
│   ├── generator.py                  # Translation Engine (FR-001, FR-016, FR-017, FR-018, FR-019, FR-020)
│   │                                 # - Query param processing (omit 'disabled')
│   │                                 # - Response data extraction from Postman tables
│   │                                 # - Type inference system (inferred/origin/override)
│   │                                 # - Override preservation and conflict warnings
│   └── templates/                    # Typing stub templates (FR-007)
├── connection.py                     # LimbleConnection (FR-003)
├── endpoint.py                       # Generic endpoint implementation (FR-004)
├── registry.yaml                     # Internal Spec Source-of-Truth (FR-005)
│                                     # - Contains query_params with type metadata
│                                     # - Contains response.fields with ResponseField specs
├── curated/                          # Curated Operation Layer (FR-006)
└── util.py                           # Logging (NFR-001), Retries (NFR-002)

tests/
├── contract/                         # Contract validation (FR-009)
├── integration/
└── unit/
```

**Structure Decision**: Single project (SDK). The existing `LimbleConnection` folder will be expanded. Generic layer will be dynamically attached to `LimbleConnection` instances at runtime based on the `registry.yaml` generated from Postman.

**Registry Schema Extensions**: The `registry.yaml` schema has been enhanced to include:
- `query_params` array with QueryParameter objects (key, value, description, type, inferred_type, origin_type, override_type)
- Enhanced `response` mapping with ResponseField objects containing the same type inference system
- Omission of Postman-specific 'disabled' property from query parameters

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
