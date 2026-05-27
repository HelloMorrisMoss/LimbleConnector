# Tasks: LimbleConnector Spec-Driven Wrapper (Hybrid Option C)

**Input**: Design documents from `/specs/001-spec-driven-wrapper/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/
**Propagated**: 2026-04-29 — Updated from spec.md refinement
**Propagated**: 2026-04-30 — Updated from spec.md refinement (FR-018 OpenAPI spec integration)
**Propagated**: 2026-05-27 — Updated from spec.md refinement (US4, FR-022 live registry type reconciliation, FR-018 `observed_type` extension, FR-023 empty-response-shape capture)

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
- [x] T002a [P] Add registry access utilities `get_registry()` and `get_registry_path()` to `LimbleConnection/util.py` (FR-021)
- [x] T002b [P] Update `pyproject.toml` to include `registry.yaml` as package data (FR-021)
- [x] T003 [P] Add `postmanparser` and `pyyaml` to `requirements311.txt` if missing (already present/planned)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Implement base `LimbleEndpoint` class in `LimbleConnection/endpoint.py` supporting `get()`, `list()`, `raw()` (FR-004)
- [x] T005 Implement `Paginator` interface and `AutoPagination` logic in `LimbleConnection/endpoint.py` (FR-011, FR-014)
- [x] T006 Implement `RegistryLoader` to load and validate `registry.yaml` against `specs/001-spec-driven-wrapper/contracts/registry_schema.yaml`
- [x] T006a [P] [US4] Update `contracts/registry_schema.yaml` to add `observed_type` to `QueryParameter` and `ResponseField`, and `empty_response_shape` to `ResponseMapping` (FR-018, FR-022, FR-023) — *completed during refinement propagation 2026-05-27*
- [ ] T006b [P] [US4] Verify `RegistryLoader` and existing registry validation pass with the new optional fields and continue to accept registry entries that omit them (FR-018, FR-022, FR-023) (depends on T006a)

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Postman-Driven Endpoint Addition (Priority: P1) 🎯 MVP

**Goal**: Enable adding new endpoints by importing from Postman with zero manual coding and full typing support.

**Independent Test**: Add a new endpoint to a mock Postman JSON, run generator, and verify it's available on `lc` with correct types.

### Tests for User Story 1
- [x] T007 [P] [US1] Create generator unit tests in `tests/unit/test_generator.py` - include tests for type inference system (FR-018)
- [x] T007a [P] [US1] Add test for query parameter processing - verify all params are included but 'disabled' property itself is omitted (FR-016)
- [x] T007b [P] [US1] Add test for response data extraction from Postman description tables (FR-017)
- [x] T007b-1 [P] [US1] Add tests for OpenAPI extraction utilities in `tests/unit/test_openapi_extract.py` - verify schema parsing, type conversion, parameter extraction (FR-018)
- [x] T007c [P] [US1] Add test for override preservation and conflict warnings (FR-019, FR-020)
- [x] T007c-1 [P] [US1] Add test for origin_type precedence (OpenAPI > Postman table) and type merging logic (FR-018)
- [x] T008 [P] [US1] Create dynamic attachment tests in `tests/integration/test_dynamic_loading.py`

### Implementation for User Story 1
- [x] T009 [US1] Implement `TranslationEngine` in `LimbleConnection/_generate_classes_automatically/generator.py` to convert Postman JSON to `registry.yaml` (FR-001, FR-002)
- [x] T009a [US1] Add query parameter extraction to `TranslationEngine` - include all params but omit their Postman-specific 'disabled' property (FR-016) (depends on T009)
- [x] T009b [US1] Add response data table parsing to `TranslationEngine` - extract tabular 'return data'/'response data' from Postman descriptions (FR-017) (depends on T009)
- [x] T009b-1 [P] [US1] Implement OpenAPI extraction utilities in `LimbleConnection/_generate_classes_automatically/openapi_extract.py` - provide functions: `load_openapi()`, `iter_operations()`, `schema_to_python_type()`, `extract_params()`, `extract_request_body_fields()`, `extract_response_fields()` as documented in `limble_openapi_utilization_notes.md` (FR-018)
- [x] T009c [US1] Implement type inference system in `TranslationEngine` for query_params and response fields (FR-018) (depends on T009a, T009b)
- [x] T009c-1 [US1] Integrate OpenAPI spec into type inference system - extract origin_type from `20260430 - Limble API V2.postman OpenAPI3.0 generated spec.yaml` using precedence: OpenAPI schema type > Postman table type, with conservative type mapping (integer→int, string→str, array→list[T], object→dict[str, Any]) (depends on T009c, T009b-1)
- [ ] T009c-2 [US1+US4] Extend type inference system to include `observed_type` in the precedence chain (`override_type > origin_type > observed_type > inferred_type`); update `compute_final_type` signature and update generator to read `observed_type` from existing registry entries when computing the final `type` (FR-018) (depends on T009c-1)
- [x] T009d [US1] Implement override preservation logic - preserve existing override_type values and emit warnings on conflicts (FR-019, FR-020) (depends on T009c)
- [ ] T009d-1 [US1+US4] Extend preservation logic to also preserve `observed_type` and `empty_response_shape` across registry regeneration; emit FR-020-style warning when an existing `observed_type` disagrees with the newly computed `origin_type` (origin↔observed disagreement surfaced rather than buried by precedence) (FR-018, FR-019, FR-020) (depends on T009d, T009c-2)
- [x] T010 [US1] Implement `.pyi` stub generator in `LimbleConnection/_generate_classes_automatically/generator.py` using Jinja2 templates (FR-007, FR-013)
- [x] T011 [US1] Implement dynamic attribute attachment in `LimbleConnection/connection.py` using the `RegistryLoader` (FR-003)
- [x] T011a [US1] Implement `supports_query_param()` in `LimbleConnection/endpoint.py` (FR-015)
- [x] T012 [US1] Implement `ErrorNormalization` middleware in `LimbleConnection/endpoint.py` (FR-008)

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

## Phase 6: User Story 4 - Registry Type Reconciliation from Live Testing (Priority: P4)

**Goal**: Allow maintainers to reconcile registry types against live API responses via `tests/semiautomated/attended_preliminary_testing.py`, writing `observed_type` (and opportunistically `empty_response_shape`) without touching `override_type`, with a choice of `flag-and-prompt` (attended) or `flag-and-skip` (autonomy) modes.

**Independent Test**: Seed a registry entry with a deliberately wrong `inferred_type` or `origin_type`, run the utility against a live endpoint, and verify (a) the discrepancy is classified and reported, (b) `observed_type` is updated on confirmation, (c) `override_type` is preserved, (d) end-user-facing computed `type` recomputes through the new precedence.

### Tests for User Story 4
- [ ] T023 [P] [US4] Unit tests in `tests/unit/test_attended_type_reconciliation.py` covering: live-response type observation (incl. `Optional[X]` for null samples), classification of all 5 discrepancy kinds (documentation drift / nullability / non-representative sample / prior-observation conflict / other), `override_type` preservation, mode-specific behavior (flag-and-prompt vs flag-and-skip), opportunistic empty-response-shape capture (FR-018, FR-019, FR-022, FR-023)
- [ ] T024 [P] [US4] Integration test in `tests/integration/test_live_type_reconciliation.py` seeding a registry with deliberately wrong types and verifying the reconciliation flow updates `observed_type` correctly across QueryParameter and ResponseField, while preserving `override_type` (US4, FR-019, FR-022)

### Implementation for User Story 4
- [ ] T025 [US4] Add CLI plumbing to `tests/semiautomated/attended_preliminary_testing.py`: `--update-types` opt-in flag (default off) and `--mode {flag-and-prompt,flag-and-skip}` option (default `flag-and-prompt`); confirm the off-default behavior remains byte-identical to the existing flow (FR-022, US4 scenario 7)
- [ ] T026 [US4] Implement live-response type observation logic: walk response data (and exercised query parameters), derive observed type per field/parameter, apply `Optional[X]` notation when a sampled value is `None` per FR-018 nullability convention (FR-018, FR-022) (depends on T009c-2)
- [ ] T027 [US4] Implement discrepancy classification module producing the 5 kinds — documentation drift, nullability, non-representative sample (whole-envelope empty only, NOT per-field null), prior-observation conflict, other — with the suspicion message that explains *why* a sample is suspect (FR-022) (depends on T026)
- [ ] T028 [US4] Implement `flag-and-prompt` reconciliation flow: per discrepancy, present classified report and prompt maintainer before writing `observed_type` to the registry; `override_type` MUST be preserved per FR-019 (FR-022) (depends on T027)
- [ ] T029 [US4] Implement `flag-and-skip` reconciliation flow: log each classified discrepancy without prompting and without writing; produce a per-run summary suitable for post-hoc review (FR-022) (depends on T027)
- [ ] T030 [US4] Implement scannable output formatting common to both modes (concise per-discrepancy lines, grouped by endpoint, kind-tagged); concrete format documented in `research.md` (FR-022) (depends on T028, T029)
- [ ] T031 [US4] Implement opportunistic empty-response-shape capture: when the live testing utility naturally observes an empty response envelope (e.g., `[]`, `{}`, top-level `null`, `{"data": [], "meta": {...}}`), record it on the endpoint's `ResponseMapping.empty_response_shape`; never synthesize or force-produce empty responses (FR-023) (depends on T026)
- [ ] T032 [US4] Ensure suspicion/discrepancy-kind metadata stays scoped to maintainer output and registry tooling; verify it does NOT leak into the end-user-facing `type` field or any runtime surface (FR-022) (depends on T028, T029)

**Checkpoint**: User Story 4 complete. Maintainers can reconcile registry types against live API observations end-to-end.

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
- US4 depends on US1 (registry must exist) and on T009c-2/T009d-1 (precedence chain and preservation logic must include `observed_type` before the reconciliation utility writes to it). T006a/T006b (schema additions) are prerequisites for any code that reads or writes `observed_type` / `empty_response_shape`.

### Parallel Opportunities
- T002 and T003 can run in parallel.
- Tests (T007, T008) can be developed in parallel with implementation (T009, T010).
- US2, US3, and US4 can be developed in parallel once US1 core (and T009c-2/T009d-1) is stable.
- Within US4, T023 and T024 (tests) can be developed in parallel with T025–T032 (implementation).
