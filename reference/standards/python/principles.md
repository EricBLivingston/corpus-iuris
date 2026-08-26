# Python Development Principles

Directives for all Python development. Python 3.12+.

> **Bare-integer `§N` sections here restate, in Python-specific form, the canonically defined universal principles** — the sections below elaborate each with Python-specific mechanisms (Pydantic, typing, imports, etc.). Genuine lingua extensions **owned by this file** use the `§py` prefix. This file acts as the lingua proxy for the `py` namespace — a finding citing "§py3" means "Pydantic Patterns" everywhere this file is in scope. §14's `AppConfig` + `AppContext` mechanics are elaborated jointly under §7.

---

## Language Extensions

| § | Principle | Summary |
| --- | --- | --- |
| **§py1** | **Code Standards** | File layout, imports, docstrings, PEP 8 |
| **§py2** | **Method Signatures** | Keyword-only optional args, explicit return types |
| **§py3** | **Pydantic Patterns** | No single-field subclasses, no structural duplicates, no field duplication |
| **§py4** | **Immutable Value Objects** | Dataclasses: frozen, slots, kw\_only; named fields over tuple unpacking |
| **§py5** | **Modern Type Syntax** | PEP 695 type params, `Self`, `@override`, `StrEnum`, `Protocol` |
| **§py6** | **Attribute Provenance** | Bare names for borrowed refs; underscore prefix for owned state |
| **§py7** | **Top-Level Imports** | All imports at module top; scoped imports require documented precondition |

---

## §1. No Backward Compatibility

Refactor freely in self-contained codebases. Git is the only archive. Zero technical debt.

- Remove deprecated parameters and patterns immediately
- Update all callers in the same change
- No compatibility shims, re-exports, or `_old` suffixes

*For published libraries with external consumers: apply semantic versioning and deprecation cycles.*

## §2. YAGNI

Do not build for hypothetical futures.

- No speculative abstractions, helper utilities, or wrapper functions for one-time operations
- No premature generalization -- three similar lines are better than an unnecessary abstraction
- No extra configurability beyond what the task requires
- Delete dead code; do not comment it out or gate it behind flags
- Apply judgment: if a function obviously takes a single value (`authenticate_user(user_id)`), don't force batch signatures

## §3. Explicit Configuration

Config stores values via Pydantic models only. Create once at entry point, pass as objects.

- Context = config + derived values/validations
- Pass complete config/context objects; extract values at the lowest level
- All defaults belong in Pydantic model `Field()` definitions, not scattered through code
- Values subject to change (model names, thresholds, paths) come from config, never hardcoded
- Use `None` default + assign from config in body -- never use function defaults for configurable values
- **Never** instantiate global config for import elsewhere

## §4. Strict Typing

All code typed. Use `from __future__ import annotations`.

- Prefer precise types over `Any`; use modern built-ins (`list`, `dict`, `tuple`)
- Use `TYPE_CHECKING` guard for circular imports
- Keep Pydantic models intact through domain logic; only `model_dump()` at serialization boundaries (JSON output, prompt construction, API responses, CSV export)
- Gradual migration: new code fully typed, modified code adds types opportunistically

**Serialization boundaries** (where `model_dump()` is appropriate): JSON files, LLM prompts, spreadsheets, external APIs, logging.

**Never `model_dump()` for**: passing between internal functions, temporary variables, method parameters within the codebase.

## §5. Required means Required

Never use `Optional[T]` or `None` defaults for parameters that are logically required. If every production caller must provide a value, make it required.

- Applies to function parameters, Pydantic fields, dataclass fields, and constructor arguments
- Do not introduce optionality to simplify testing; tests bear the cost of satisfying production interfaces
- A required parameter with a `None` default is a lie the type system cannot catch
- When refactoring surfaces a new dependency, add it as a required parameter -- do not paper over it with `Optional`

## §6. Fail Fast

Let exceptions bubble. Use specific exception types with actionable context.

- Don't catch exceptions just to re-raise without added context
- Missing config, invalid patterns, unresolvable paths: fail at startup, not at first use
- Validate once at boundaries (user input, API responses, files), trust types internally

## §7. Composition Over Implicit Context (covers universal §14)

This section elaborates two universal clusters: **§7** (no globals, thread-locals, or ambient state) and **§14** (the `AppConfig` + `AppContext` construction shape, single source of truth, leaf-node extraction). They are presented together because in Python the mechanisms for both — Pydantic-frozen `AppConfig`, constructor injection, no module-level singletons — are the same set of techniques.

Use the `AppConfig` + `AppContext` construction pattern.

- **`AppConfig`** holds all static external values: config files (TOML/YAML/JSON), environment variables, CLI parameters. Deserialized once at startup, validated, never mutated. Holds values, not resources.
- **`AppContext`** holds `AppConfig` plus the app-wide resources constructed from it: database connection pools, API clients, HTTP clients, message queues, file handles, singleton services. Expensive to construct, app-lifetime, shared across the codebase.
- **Constructed once** at the entry point (app factory or `main()`) from a validated `AppConfig`.
- **Passed as the single source of truth** for both configuration and derived resources throughout the application's lifetime.
- Components receive `AppContext` via **constructor injection**, then extract specific values/resources at leaf nodes (`ctx.config.database.url`, `ctx.db_pool`).
- **Never reconstruct** a resource that already exists in `AppContext` — use the instance from the context object.
- **No global state**: never `from mypackage.config import config`, no module-level singletons, no "get X" free functions that reach for hidden state.

Use Pydantic for `AppConfig` with `model_config = ConfigDict(frozen=True)` to enforce immutable semantics. Construct `AppContext` at the entry point and pass via constructor injection everywhere.

```python
# Do
class AppContext:
    def __init__(self, config: AppConfig, db_pool: DBPool, api_client: ApiClient):
        self.config = config
        self.db_pool = db_pool
        self.api_client = api_client

class Handler:
    def __init__(self, context: AppContext):
        self.context = context

    def process(self, request: Request) -> Response:
        db = self.context.db_pool  # extract at leaf
        ...

# Don't
class Handler:
    def process(self, data_dir: Path, db_pool: DBPool, config: Config): ...
    # ^ threading values + resources through every call site
```

This is the canonical application-wide shared-state pattern across all languages (Rust, Python, TypeScript, etc.), not a Python-specific idiom.

## §8. EAFP Over LBYL

Trust validated data. Do not re-check what Pydantic/type system already guarantees.

- No `hasattr()` on Pydantic models -- use `getattr(obj, "attr", default)` if needed
- No `if key in dict` before access on validated structures
- Defensive checks only at system boundaries (external data, user input)

```python
# Do
model_config = config.models.extraction
temperature = model_config.temperature

# Don't
if hasattr(config, 'models') and hasattr(config.models, 'extraction'):
    model_config = config.models.extraction
```

## §9. Batch-First APIs

Design functions to accept iterables/lists by default. Add single-item wrappers only when needed.

- Applies to processing pipelines, query interfaces, bulk operations
- Use judgment: obvious singletons (`authenticate_user`, `get_by_id`) stay singular
- Reduces per-call overhead and enables internal optimizations

## §10. Logging

Class-level loggers with hierarchical naming.

```python
class DataExtractor:
    def __init__(self, config: AppConfig):
        self.log = config.log.getChild("DataExtractor")
```

## §11. Production Code Primacy

Production code has right-of-way. Tests adapt to production, never the reverse.

- Never weaken production types, structure, or interfaces to satisfy tests
- Exception: tests reveal genuine bugs -- fix the bug, not the architecture
- Tests must conform to production interfaces; tests bear the cost

## §12. Testing

- Pytest with markers for categorization
- 80% coverage threshold
- Separate unit (fast, isolated) from integration (multi-component)
- `make test`, `make lint`, `make format`, `make typecheck`

## §py1. Code Standards

### File Layout

1. Module docstring
2. `from __future__ import annotations`
3. Module-level dunders (`__all__`, `__version__`)
4. Imports (stdlib > third-party > local > `TYPE_CHECKING`)
5. Module code
6. Trailing newline

### Import Organization

```python
"""Module docstring."""

from __future__ import annotations

__all__ = ["exported_function"]

import sys
from abc import ABC, abstractmethod

from pydantic import BaseModel

from ..base import invoke_agent

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from mypackage.config import AppContext
```

### Docstrings

- Class: role, key methods, attributes
- Method: Google style with `Args`, `Returns`, `Raises`
- PEP 8, 120-char line limit
- `BaseModel` fields use `Field()` with defaults and descriptions

## §py2. Method Signatures

- Keyword-only args with `*` for optional parameters
- Order: required positional, `*`, keyword-only
- Always specify return types

```python
def process(
    self, text: str, page_number: int, *, max_retries: int = 1
) -> tuple[Result, dict[str, Any]]:
```

## §py3. Pydantic Patterns

- No single-field subclasses -- add the field to the base
- No structural duplicates -- reuse existing models
- No field duplication across inheritance -- define once in the base

## §py4. Immutable Value Objects

Dataclasses use `@dataclass(frozen=True, slots=True, kw_only=True)` by default.

- Structured dataclasses or Pydantic models over tuple unpacking -- named fields prevent positional ambiguity and are self-documenting
- If you're reaching for a tuple of more than two elements, you want a dataclass
- Mutability only when explicitly required and justified

## §py5. Modern Type Syntax

Use Python 3.12+ features actively, not just permissively:

| Feature | Replaces | Example |
| --- | --- | --- |
| PEP 695 type params | `TypeVar` boilerplate | `class Repo[T]:`, `def first[T](items: list[T]) -> T:` |
| `type` aliases | `TypeAlias` | `type JsonDict = dict[str, object]` |
| `Self` | manually repeating class name | `def set_name(self, name: str) -> Self:` |
| `@override` (PEP 698) | silent breakage on rename | `@override def extract(self, text: str) -> Result:` |
| `StrEnum` | raw string constants | `class Status(StrEnum): PENDING = "pending"` |
| `Protocol` | inheritance for contracts | Prefer over ABC when no shared implementation needed |

## §py6. Attribute Provenance

Instance attributes that store externally-provided objects ("borrowed" references like `proxy`, `config`) use bare names: `self.proxy`, `self.config`. Attributes that are internally created and fully scoped to the class use underscore-prefixed names: `self._thread`, `self._stop_event`.

- Bare names = pass-throughs, not subject to internal mutation
- Underscored names = owned state, created and managed by the class
- Convention: `self.log` (from `config.log.getChild()`) uses bare naming for readability despite being technically owned

## §py7. Top-Level Imports

All imports go at the top of the module, grouped per the File Layout in §py1. Scoped imports (inside functions or conditionals) are prohibited unless a documented precondition requires deferred loading.

- Acceptable: the imported module executes side effects that depend on prior initialization
- Not acceptable: "convenience", "only used here", or "avoids importing something heavy"
- When a scoped import is genuinely necessary, accompany it with a comment explaining the precondition
- Import failures should surface at load time, not hide until a code path executes
