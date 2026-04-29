# Tasks: LimbleConnector Spec-Driven Wrapper (Hybrid Option C)

**Input**: Design documents from `/specs/001-spec-driven-wrapper/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Propagated**: 2026-04-29 — Updated from spec.md refinement

**Tests**: Tests are explicitly requested in `spec.md` (Independent Test sections).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `LimbleConnection/endpoint.py` and `LimbleConnection/curated/` directory
- [x] T002 [P] Update `LimbleConnection/util.py` with `LimbleConnector` logger and `ResilienceHandler` (NFR-001, NFR-002)
- [x] T003 [P] Add `postmanparser` and `pyyaml` to `requirements311.txt` if missing (already present/planned)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Implement base `LimbleEndpoint` class in `LimbleConnection/endpoint.py` supporting `get()`, `list()`, `raw()` (FR-004)
- [x] T005 Implement `Paginator` interface and `AutoPagination` logic in `LimbleConnection/endpoint.py` (FR-011, FR-014)
- [x] T006 Implement `RegistryLoader` to load and validate `registry.yaml` against `specs/001-spec-driven-wrapper/contracts/registry_schema.yaml`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Postman-Driven Endpoint Addition (Priority: P1) 🎯 MVP

**Goal**: Enable adding new endpoints by importing from Postman with zero manual coding and full typing support.

**Independent Test**: Add a new endpoint to a mock Postman JSON, run generator, and verify it's available on `lc` with correct types.

### Tests for User Story 1
- [x] T007 [P] [US1] Create generator unit tests in `tests/unit/test_generator.py` - include tests for type inference system (FR-018)
- [x] T007a [P] [US1] Add test for query parameter processing - verify all params are included but 'disabled' property itself is omitted (FR-016)
- [x] T007b [P] [US1] Add test for response data extraction from Postman description tables (FR-017)
- [x] T007c [P] [US1] Add test for override preservation and conflict warnings (FR-019, FR-020)
- [ ] T008 [P] [US1] Create dynamic attachment tests in `tests/integration/test_dynamic_loading.py`

### Implementation for User Story 1
- [x] T009 [US1] Implement `TranslationEngine` in `LimbleConnection/_generate_classes_automatically/generator.py` to convert Postman JSON to `registry.yaml` (FR-001, FR-002)
- [x] T009a [US1] Add query parameter extraction to `TranslationEngine` - include all params but omit their Postman-specific 'disabled' property (FR-016) (depends on T009)
- [x] T009b [US1] Add response data table parsing to `TranslationEngine` - extract tabular 'return data'/'response data' from Postman descriptions (FR-017) (depends on T009)
- [x] T009c [US1] Implement type inference system in `TranslationEngine` for query_params and response fields (FR-018) (depends on T009a, T009b)
- [x] T009d [US1] Implement override preservation logic - preserve existing override_type values and emit warnings on conflicts (FR-019, FR-020) (depends on T009c)
- [x] T010 [US1] Implement `.pyi` stub generator in `LimbleConnection/_generate_classes_automatically/generator.py` using Jinja2 templates (FR-007, FR-013)
- [x] T011 [US1] Implement dynamic attribute attachment in `LimbleConnection/connection.py` using the `RegistryLoader` (FR-003)
- [ ] T012 [US1] Implement `ErrorNormalization` middleware in `LimbleConnection/endpoint.py` (FR-008)

**Checkpoint**: User Story 1 complete. MVP achieved.

---

## Phase 4: User Story 2 - Curated Operation Implementation (Priority: P2)

**Goal**: Provide stable, high-level methods for common workflows.

**Independent Test**: Call `lc.search_assets()` and verify it orchestrates multiple generic calls correctly.

### Tests for User Story 2
- [ ] T013 [P] [US2] Create integration tests for curated operations in `tests/integration/test_curated.py`

### Implementation for User Story 2
- [ ] T014 [US2] Implement `search_assets()` in `LimbleConnection/curated/assets.py` using generic endpoints (US2, FR-006)
- [ ] T015 [US2] Implement stable result normalization in `LimbleConnection/curated/base.py` (FR-006)

**Checkpoint**: User Story 2 complete.

---

## Phase 5: User Story 3 - Stability Shielding (Priority: P3)

**Goal**: Shield users from upstream breaking changes via internal spec mapping.

**Independent Test**: Modify a mock response field, update `registry.yaml` mapping, and verify SDK output remains the same.

### Tests for User Story 3
- [ ] T016 [P] [US3] Create contract tests in `tests/contract/test_stability.py` simulating field renames (FR-009)

### Implementation for User Story 3
- [ ] T017 [US3] Implement field aliasing/mapping logic in `LimbleEndpoint.responses` processing (FR-005)
- [ ] T018 [US3] Add `Unknown Response Handling` (default to `dict` + warning) in `LimbleEndpoint` (FR-010)

---

## Phase N: Polish & Cross-Cutting Concerns

- [ ] T019 [P] Update `readme.md` with new Spec-Driven architecture details and type inference system
- [ ] T020 [P] Run `speckit.analyze` to verify Constitution compliance
- [ ] T021 Finalize `CHANGELOG.md` for version 0.1.0
- [ ] T022 [P] Update `specs/001-spec-driven-wrapper/contracts/registry_schema.yaml` documentation with examples of type system usage

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)** -> **Foundational (Phase 2)** -> **User Stories (Phase 3+)**
- US2 depends on US1 (generic layer must exist to be used by curated layer).
- US3 depends on US1 (mapping logic applies to generic endpoints).

### Parallel Opportunities
- T002 and T003 can run in parallel.
- Tests (T007, T008) can be developed in parallel with implementation (T009, T010).
- US2 and US3 can potentially be developed in parallel once US1 core is stable.
