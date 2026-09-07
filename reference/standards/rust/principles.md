# Rust Development Principles

Directives for all Rust development. Rust 2021 edition+.

> **Bare-integer `§N` sections here restate, in Rust-specific form, the canonically defined universal principles** — the sections below elaborate each with Rust-specific mechanisms (type system, lifetimes, tracing, etc.). Genuine lingua extensions **owned by this file** use the `§rs` prefix. This file acts as the lingua proxy for the `rs` namespace — a finding citing "§rs2" means "Memory Efficiency" everywhere this file is in scope. §14's `AppConfig` + `AppContext` mechanics are elaborated jointly under §7.

---

## Language Extensions

| § | Principle | Summary |
| --- | --- | --- |
| **§rs1** | **Workspace Boundaries** | Clear crate separation; shared types in common crates |
| **§rs2** | **Memory Efficiency** | Right string type, shared alias module, fixed-size collections |
| **§rs3** | **Safety and Linting** | `forbid(unsafe_code)`, `warn(clippy::all)` in every crate |
| **§rs4** | **Code Quality** | Conventions checklist for idiomatic Rust |

---

## §1. No Backward Compatibility

Refactor freely in self-contained codebases. Git is the only archive. Zero technical debt.

- No deprecated code accommodations
- Any `#[allow(dead_code)]` must have a worthy `// TODO` or be removed
- Remove unused code, imports, and dependencies immediately

*For published library crates: apply semantic versioning.*

| Code type | Rule |
| --- | --- |
| Internal modules / binary crates | Refactor freely -- no compatibility layers |
| Published library crates | SemVer -- breaking changes require major version bump |

Use `#[non_exhaustive]` on public structs/enums in library crates to reserve the right to add fields without a major bump.

## §2. YAGNI

Do not build for hypothetical futures.

- No speculative abstractions, wrapper types, or trait implementations for one-time operations
- No premature generalization -- concrete types until a second use case exists
- No extra configurability beyond what the task requires
- Delete dead code; do not gate behind `cfg` flags or comment out
- Apply judgment: if a function obviously takes a single value (`authenticate_user(user_id)`), don't force batch signatures

## §3. Explicit Configuration

All config values in files (TOML, YAML, etc.) or named `Default` implementations. No hidden defaults buried in code.

- Missing required config: explicit error at startup, not silent fallback
- Use `Default` trait for documented defaults
- Keep defaults discoverable -- never scatter through business logic
- Two-phase pipeline where applicable: raw deserialized types (`RuleConfig`) compile into validated runtime types (`Rule` with `Regex`)
- `#[serde(default)]` is forbidden on application Settings structs and fields -- missing config must cause an explicit error at startup
- `#[serde(default)]` is acceptable on types deserialized from external sources (socket protocols, session files, plugin manifests) where forward compatibility matters

## §4. Strict Typing

Deserialize into concrete structs at boundaries. Domain logic operates on typed data only.

- No `serde_json::Value` or raw `HashMap` in domain logic
- Eliminate magic strings: use enums or consts

## §5. Required means Required

Universal §5 governs unchanged; the forbidden Rust shape is `Option<T>` on a logically required parameter, struct field, config value, or builder slot.

## §6. Fail Fast

Fail explicitly at startup. Do not mask errors with defensive fallbacks.

- Invalid regex, unresolvable path, missing config field: error at startup, not at first use
- Compile/validate all patterns during initialization
- Use `Result` and `?` consistently; `.unwrap()` only in tests
- Prefer compile-time guarantees (type system, const generics) over runtime checks

## §7. Composition Over Implicit Context (covers universal §14)

Universal §7 (no globals, thread-locals, or ambient state) and universal §14 (the `AppConfig` + `AppContext` shape, single source of truth, leaf-node extraction) govern unchanged. They are elaborated together because in Rust one set of mechanisms serves both.

Heap-allocate `AppContext` via `Arc<AppContext>` (or `Box<AppContext>` for single-owner cases) so it can be cheaply cloned and passed as a pointer across threads, tasks, and modules. Components receive it by constructor injection; there are no module-level singletons and no "get X" free functions reaching for hidden state.

```rust
// Do
struct AppContext {
    config: AppConfig,
    db_pool: Arc<PgPool>,
    api_client: Arc<ApiClient>,
}

async fn main() -> Result<()> {
    let config = AppConfig::load()?;
    let ctx = Arc::new(AppContext::new(config).await?);
    run_server(ctx).await
}

// Don't
async fn handle_request(config: AppConfig, db_pool: &PgPool) { ... }
// ^ threading config values and resources individually through every call site
```

## §8. EAFP Over LBYL

Universal §8 governs unchanged; the redundant Rust shape is `if let Some(x)` on a value the type or config loader already guarantees.

## §9. Batch-First APIs

Design APIs to accept `&[T]` by default. Add singleton wrappers only when needed.

- Applies to query interfaces, matching operations, processing pipelines
- Use judgment: obvious singletons (`get_by_id`, `authenticate`) stay singular
- Reduces per-call overhead and enables internal batching

## §10. Logging

Use `tracing` with structured, leveled output.

| Level | Use For |
| --- | --- |
| `error` | Failures requiring attention |
| `warn` | Recoverable issues |
| `info` | Significant events (startup, config loaded, decisions) |
| `debug` | Development details |
| `trace` | Fine-grained execution flow |

- Named targets for cross-cutting concerns (e.g., `target: "audit"`)
- `fmt::init()` with no `RUST_LOG` set logs **only** `error` — `EnvFilter::from_default_env()` falls back to `LevelFilter::ERROR`. Override with `.with_default_directive(LevelFilter::INFO.into())` (§3)
- `Level` orders by verbosity, not severity: `trace > debug > info > warn > error`. `LevelFilter::WARN` is a *maximum* — it permits `warn` and `error`

## §11. Production Code Primacy

Universal §11 governs unchanged; the one carve-out is that a test exposing a genuine bug is fixed in the code, not absorbed by the architecture.

## §12. Testing

- Tests in dedicated `tests.rs` files, not inline `#[cfg(test)] mod tests`
- For `module/mod.rs`, tests go in `module/tests.rs`
- Integration tests in top-level `tests/` directory
- Production logic files stay focused on production code

## §rs1. Workspace Boundaries

In multi-crate workspaces, maintain clear separation.

- Shared domain types and config logic in a common crate
- Each crate has a well-defined responsibility boundary
- No cross-crate dependencies that violate the intended separation

## §rs2. Memory Efficiency

Use the right type for the data's lifecycle:

| Type | Use Case | Example |
| --- | --- | --- |
| `CompactString` | Short immutable strings <=24 bytes, stack-allocated | IDs, names, keys, labels |
| `Text` (`Arc<str>`) | Long read-only strings, cheap atomic clone | Descriptions, messages, error text |
| `String` | Only when mutation is required | Dynamic content, input buffers |

- One shared types module per workspace exports all three under these names; no other crate imports `compact_str` directly
- Fixed-size collections: `Box<[T]>` (16 bytes) over `Vec<T>` (24 bytes) via `.into_boxed_slice()`

## §rs3. Safety and Linting

Every source crate:

```rust
#![forbid(unsafe_code)]
#![warn(clippy::all)]
```

- No exceptions without explicit justification in a code comment
- CI: `RUSTFLAGS="-D warnings" cargo clippy`

## §rs4. Code Quality

- `Result` and `?` consistently; `.unwrap()` only in tests
- Owned types in public APIs, borrows (`&T`, `&str`) in internal/hot-path code
- `thiserror` for library errors, `anyhow` for application entry points
- `Display` for every custom error and user-facing type
- Derive `Debug`, `Clone`, `PartialEq` where appropriate; `Copy` only for small value types
- `cargo fmt` with default settings; commit `rustfmt.toml` if overrides needed
- `From`/`Into` over explicit conversion functions in public APIs
