# Research: LimbleConnector Spec-Driven Wrapper

## Unknowns & Needs Clarification

### 1. Dynamic Attachment vs. Static Typing
- **Question**: How can we achieve FR-003 (Dynamic Attachment) while maintaining SC-002 (100% IDE-visible typing)?
- **Research**: If we attach endpoints at runtime (e.g., via `__getattr__` or `setattr`), IDEs like PyCharm/VSCode won't see them unless we provide `.pyi` stubs or a generated module.
- **Decision**: FR-013 specifies committing typing stubs (`.pyi`). The generator will create these stubs based on the `registry.yaml`.

### 2. Postman Folder Hierarchy Translation
- **Question**: How to translate nested Postman folders into a fluent API (e.g., `Routes > Assets > Search` -> `lc.assets.search`)?
- **Research**: `postmanparser` can traverse the collection. We need a recursive function to flatten or map these folders to snake_case attributes.
- **Decision**: Implement a `TranslationEngine` that flattens the folder structure into a nested dictionary in `registry.yaml`, which then informs both the dynamic attachment and the stub generation.

### 3. Stability Mapping in YAML
- **Question**: How should the `registry.yaml` define the mapping between upstream fields and stable SDK fields?
- **Research**: Look at how other SDKs (like Stripe or AWS) handle field mapping. A simple `field_map` key in the YAML per endpoint should suffice.
- **Decision**: `registry.yaml` will have a `responses` section for each endpoint with a `mappings` dictionary.

### 4. RateLimitHandler Adaptation
- **Question**: How to adapt the existing `RateLimitHandler` in `util.py` to meet NFR-002?
- **Research**: Inspect `LimbleConnection/util.py`.
- **Decision**: Refactor `RateLimitHandler` into a more generic `ResilienceHandler` that supports exponential backoff for 429, 502, and 503.

## Technology Choices

| Tech | Rationale | Alternatives Considered |
|------|-----------|-------------------------|
| `postmanparser` | Specifically designed for Postman collections. | Manual JSON parsing (too brittle). |
| `pyyaml` | Standard for YAML in Python. | JSON (less readable for manual overrides). |
| `.pyi` stubs | Best way to provide typing for dynamic attributes without runtime overhead. | Generated `.py` modules (harder to manage). |
| `responses` | Recommended in Constitution XII for offline testing. | `unittest.mock` (less convenient for HTTP). |

## Dependencies Best Practices

- **requests**: Use `Session` objects for connection pooling.
- **pandas**: Use for the `.df()` helper as it's already in requirements and excellent for tabular data.
