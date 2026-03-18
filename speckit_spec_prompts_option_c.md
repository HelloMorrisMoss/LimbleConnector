# Speckit Prompts — Generate spec.md (Option C: Hybrid SDK)

These prompts are designed to be run **one at a time**, producing one section of `spec.md` per prompt.
The coding assistant MUST read `constitution.md` in the repo before generating any section.

IMPORTANT ASSEMBLY RULE:
- Each prompt output should be pasted into a single `spec.md` file following `spec-template.md` ordering.
- Do NOT include plan/task execution steps in `spec.md` (commands, CI YAML, exact file paths unless they are stable interface contracts).
- Put step-by-step execution into Speckit `plan` or `tasks` outputs.

---

## Prompt 0 — Create the spec skeleton (header + empty sections)

You are a senior software architect and spec author.

Create `spec.md` using the repository’s `spec-template.md` as the required structure.

Rules:
- You MUST read and comply with `constitution.md`.
- You MUST also read:
  - the Limble Postman Collection export JSON in the repo (upstream inventory authority)
  - any existing `.specify` files and generator outputs (derived artifacts)
  - old-constitution-spec.md (contains implementation-level rules to be moved into this spec)
- Output MUST include the template headings in the same order.
- Fill out metadata fields (Feature Branch/Created/Status/Input) with:
  - Feature Name: “LimbleConnector Spec-Driven Wrapper (Hybrid Option C)”
  - Branch: `[EXAMPLE—replace with your branch name]`
  - Created: today’s date
  - Status: Draft
  - Input: “Generate spec.md from constitution, old constitution details, and Postman collection.”

For any unknowns, write:
`[NEEDS CLARIFICATION: <reason>]`

Output ONLY the skeleton contents of `spec.md`.

---

## Prompt 1 — Fill “User Scenarios & Testing” (mandatory)

You are a senior software architect.

Update ONLY the “User Scenarios & Testing” section of `spec.md`.

You MUST base scenarios on real workflows for this repository, including:

P1:
- Add/update an endpoint starting from the Postman collection (inventory) and internal spec (stability contract).
- Regenerate typing/docs artifacts and ensure fluent access remains stable.

P2:
- Add a curated operation (semantic wrapper) that uses generic endpoints without polluting the base endpoint class.
- Add contract tests/fixtures for drift detection.

P3:
- Handle an upstream breaking change while preserving SDK surface (stability-first).

Each story MUST be independently testable and include acceptance scenarios.

Do NOT write any implementation steps or commands.
Do NOT include file paths unless they are stable contracts.

Output ONLY the completed “User Scenarios & Testing” section.

---

## Prompt 2 — Fill “Requirements” (mandatory)

You are a senior software architect.

Update ONLY the “Requirements” section of `spec.md`.

You MUST derive requirements from:
- constitution.md (non-negotiables)
- old-constitution-spec.md (implementation details previously removed from the constitution)
- the Postman collection JSON (upstream endpoint inventory)
- current repository approach (dynamic endpoints + generated typing placeholders)

The requirements MUST be consistent with Option C (Hybrid):
- Generic endpoints (inventory coverage, fluent, consistent base methods)
- Curated operations (semantic workflows, stable guarantees)

Your Requirements section MUST include these subsections under “Functional Requirements” as numbered FR items:

A) Postman → Internal Spec Translation Rules
- how endpoints are identified/named
- how methods/paths/params are derived
- how auth inheritance is interpreted
- how variables/path params are represented
- how missing response schemas are handled (fixtures + NEEDS CLARIFICATION)

B) Endpoint Registry & Dynamic Attachment
- endpoint naming rules (including nested dot-notation)
- deterministic attachment order (no order-dependent hacks)
- requirements for registry structure (conceptually—avoid hard-coded file paths)

C) Generic Endpoint Interface Contract
- baseline methods that MUST exist (e.g., get/list/create/update/delete/raw or equivalent)
- idempotency + retry bounding + timeouts requirements
- pagination toggles and endpoint-specific flags as spec metadata (not scattered if/else)

D) Curated Operations Contract
- where they live conceptually (operations layer/facade)
- how they call generic endpoints
- stability guarantees and testing requirements

E) Typing/Docs Generation Contract
- what must be generated for IDE support (stubs or modules)
- what must be documented (docstrings, parameter docs)
- how generated artifacts are marked as generated (header notice + validation hash)
- CI verification requirement (conceptual; no pipeline steps)

F) Error Model Contract
- exception hierarchy expectations
- required metadata fields (endpoint name, method, status code, request id if present, redacted response excerpt)

G) Contract Tests & Fixtures
- fixtures MUST exist for each endpoint and curated op (where feasible)
- snapshot/schema validation requirements for `.df()` outputs where applicable
- offline-only requirement

If anything cannot be determined from repo + inputs, use:
`[NEEDS CLARIFICATION: ...]`

Do NOT include step-by-step execution instructions or shell commands.
Those belong in Speckit `plan`/`tasks`.

Output ONLY the completed “Requirements” section.

---

## Prompt 3 — Fill “Success Criteria” (mandatory)

You are a senior software architect.

Update ONLY the “Success Criteria” section of `spec.md`.

Success criteria MUST be measurable and should reflect:

- drift detection effectiveness (schema/mapping regressions caught)
- stable SDK surface across Postman changes (compatibility)
- contributor workflow quality (time to add endpoint + tests)
- offline test coverage reliability
- typing/IDE experience success

No implementation steps.

Output ONLY the completed “Success Criteria” section.
