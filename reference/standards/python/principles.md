# Python Development Principles

Python 3.12+.

---

## Language extensions

| § | Principle | Summary |
| --- | --- | --- |
| §py1 | **Code Standards** | File layout, imports, docstrings, PEP 8 |
| §py2 | **Method Signatures** | Keyword-only optional args |
| §py3 | **Pydantic Patterns** | No single-field subclasses, no structural duplicates, no field duplication |
| §py4 | **Immutable Value Objects** | Dataclasses: frozen, slots, kw\_only; named fields over tuple unpacking |
| §py5 | **Modern Type Syntax** | PEP 695 type params, `Self`, `@override`, `StrEnum`, `Protocol` |
| §py6 | **Attribute Provenance** | Bare names for borrowed refs; underscore prefix for owned state |
| §py7 | **Top-Level Imports** | All imports at module top; scoped imports require documented precondition |

---

## §3. Explicit Configuration

Config stores values via Pydantic models only, and all defaults belong in Pydantic model `Field()` definitions. A configurable value is never a function default.

## §4. Strict Typing

Every function is fully annotated, return type included; untyped code gains annotations when a change touches it. Circular imports go behind an `if TYPE_CHECKING:` block.

`model_dump()` runs only at serialization boundaries: JSON files, LLM prompts, spreadsheets, external APIs, logging.

## §7. Composition Over Implicit Context (covers universal §14)

`AppConfig` sets `model_config = ConfigDict(frozen=True)`.

## §8. EAFP Over LBYL

On Pydantic models, no `hasattr()` or `getattr()` with a default.

```python
# Do
model_config = config.models.extraction
temperature = model_config.temperature

# Don't
if hasattr(config, 'models') and hasattr(config.models, 'extraction'):
    model_config = config.models.extraction
```

## §10. Logging

Each class derives its logger from `config.log` by `getChild()`, named for the class.

```python
class DataExtractor:
    def __init__(self, config: AppConfig):
        self.log = config.log.getChild("DataExtractor")
```

## §12. Testing

Tests run under pytest, categorized by markers, at an 80% coverage threshold; `make test`, `make lint`, `make format` and `make typecheck` are the entry points.

## §py1. Code Standards

### File Layout

A module opens with its docstring, `from __future__ import annotations`, module-level dunders (`__all__`, `__version__`), and imports (stdlib > third-party > local > the `if TYPE_CHECKING:` block), followed by module code and a trailing newline. Lines follow PEP 8 at 120 characters.

### Docstrings

Class docstrings give role, key methods, and attributes; method docstrings use Google style with `Args`, `Returns`, `Raises`. `BaseModel` fields declare a `description` in `Field()`.

## §py2. Method Signatures

Optional parameters are keyword-only, after `*`.

```python
def process(
    self, text: str, page_number: int, *, max_retries: int = 1
) -> tuple[Result, dict[str, Any]]:
```

## §py3. Pydantic Patterns

Pydantic models avoid redundant structure:

- No single-field subclasses: add the field to the base
- No structural duplicates: reuse existing models
- No field duplication across inheritance: define once in the base

## §py4. Immutable Value Objects

Dataclasses use `@dataclass(frozen=True, slots=True, kw_only=True)` by default, with mutability only when explicitly required and justified. Structured dataclasses or Pydantic models replace tuple unpacking, since named fields prevent positional ambiguity and are self-documenting; a tuple of more than two elements wants a dataclass.

## §py5. Modern Type Syntax

Prefer these features over what they replace:

| Feature | Replaces | Example |
| --- | --- | --- |
| PEP 695 type params | `TypeVar` boilerplate | `class Repo[T]:`, `def first[T](items: list[T]) -> T:` |
| `type` aliases | `TypeAlias` | `type JsonDict = dict[str, object]` |
| `Self` | manually repeating class name | `def set_name(self, name: str) -> Self:` |
| `@override` (PEP 698) | an unmarked override (silent breakage on rename) | `@override def extract(self, text: str) -> Result:` |
| `StrEnum` | raw string constants | `class Status(StrEnum): PENDING = "pending"` |
| `Protocol` | inheritance for contracts | Prefer over ABC when no shared implementation needed |

## §py6. Attribute Provenance

Instance attributes that store externally-provided objects ("borrowed" references like `proxy`, `config`) use bare names (`self.proxy`, `self.config`), and the class does not mutate them. Attributes that are internally created and fully scoped to the class use underscore-prefixed names: `self._thread`, `self._stop_event`. `self.log` (from `config.log.getChild()`) uses bare naming for readability despite being technically owned.

## §py7. Top-Level Imports

All imports go at the top of the module, grouped per the File Layout in §py1, so an unresolvable import raises at load time, before any code path executes. Scoped imports (inside functions or conditionals) are prohibited unless a documented precondition requires deferred loading.

A scoped import is acceptable where the imported module executes side effects that depend on prior initialization; "convenience", "only used here", and "avoids importing something heavy" do not qualify. A necessary scoped import is commented with its precondition.
