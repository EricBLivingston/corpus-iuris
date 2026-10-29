# Rust Development Principles

Rust 2021 edition+.

---

## Language extensions

| § | Principle | Summary |
| --- | --- | --- |
| §rs1 | **Workspace Boundaries** | Shared types and config in a common crate |
| §rs2 | **Memory Efficiency** | Right string type, shared alias module, fixed-size collections |
| §rs3 | **Safety and Linting** | Unsafe justification and the Cargo lint table |
| §rs4 | **Code Quality** | Conventions checklist for idiomatic Rust |
| §rs5 | **Async Hazards** | Runtime hazards of async code |

---

## §1. No Backward Compatibility

Use `#[non_exhaustive]` on public structs/enums in library crates to reserve the right to add fields or variants without a major bump.

## §2. YAGNI

A `cfg` gate does not exempt dead code; `#[allow(dead_code)]` stands only beside a worthy `// TODO`.

## §3. Explicit Configuration

Configuration deserializes under these rules:

- Documented defaults are named `Default` implementations
- Two-phase pipeline where applicable: raw deserialized types (`RuleConfig`) compile into validated runtime types (`Rule` with `Regex`)
- `#[serde(default)]` is forbidden on application Settings structs and fields
- `#[serde(default)]` is acceptable on types deserialized from external sources (socket protocols, session files, plugin manifests) where forward compatibility matters
- Settings structs have `#[serde(deny_unknown_fields)]` (incompatible with `#[serde(flatten)]`); without it a mistyped key is ignored and the `Option` field it meant to set stays `None`

## §4. Strict Typing

Eliminate magic strings: use enums or consts.

## §5. Required means Required

The forbidden Rust shape is `Option<T>` on a logically required parameter, struct field, config value, or builder slot.

## §6. Fail Fast

Prefer compile-time guarantees (type system, const generics) over runtime checks.

## §7. Composition Over Implicit Context (covers universal §14)

Heap-allocate `AppContext` via `Arc<AppContext>` (or `Box<AppContext>` for single-owner cases) so it can be cheaply cloned and passed as a pointer across threads, tasks, and modules.

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

The redundant Rust shape is `if let Some(x)` on a value the type or config loader already guarantees.

## §9. Batch-First APIs

Design APIs to accept `&[T]` by default; obvious singletons (`get_by_id`, `authenticate`) stay singular.

## §10. Logging

Use `tracing` with structured, leveled output and named targets for cross-cutting concerns (*e.g.*, `target: "audit"`).

| Level | Use For |
| --- | --- |
| `error` | Failures requiring attention |
| `warn` | Recoverable issues |
| `info` | Significant events (startup, config loaded, decisions) |
| `debug` | Development details |
| `trace` | Fine-grained execution flow |

`tracing` has these pitfalls:

- `fmt::init()` with no `RUST_LOG` set logs only `error`: `EnvFilter::from_default_env()` falls back to `LevelFilter::ERROR`. Override with `.with_default_directive(LevelFilter::INFO.into())` (§3)
- `Level` orders by verbosity, not severity: `trace > debug > info > warn > error`. `LevelFilter::WARN` is a *maximum*: it permits `warn` and `error`
- `#[instrument]` records every argument: a secret argument takes `skip` or `skip_all`, or is a redacting newtype

## §12. Testing

- Tests in dedicated `tests.rs` files, not inline `#[cfg(test)] mod tests`
- A module with its own `tests.rs` or with submodules resides in `module/mod.rs`, beside `module/tests.rs`; `module.rs` beside a `module/` directory is forbidden (enforced by `clippy::self_named_module_files`, §rs3)
- Integration tests in top-level `tests/` directory
- An integration-test crate with submodules is rooted at `tests/<name>/main.rs`

## §rs1. Workspace Boundaries

In a multi-crate workspace, shared domain types and config logic live in a common crate.

## §rs2. Memory Efficiency

Use the right type for the data's lifecycle:

| Type | Use Case | Example |
| --- | --- | --- |
| `CompactString` | Short immutable strings <=24 bytes, stack-allocated | IDs, names, keys, labels |
| `Text` (`Arc<str>`) | Long read-only strings, cheap atomic clone | Descriptions, messages, error text |
| `String` | Only when mutation is required | Dynamic content, input buffers |

One shared types module per workspace exports all three under these names; no other crate imports `compact_str` directly.

Fixed-size collections use `Box<[T]>` (16 bytes) over `Vec<T>` (24 bytes) via `.into_boxed_slice()`.

## §rs3. Safety and Linting

Lint levels are set in the Cargo `[lints]` table (`[workspace.lints]` with `lints.workspace = true` in each member of a workspace); crate-level lint attributes are not used.

```toml
[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
all = { level = "warn", priority = -1 }
unwrap_used = "deny"
undocumented_unsafe_blocks = "deny"
self_named_module_files = "deny"
```

- Tests are exempt from `unwrap_used` through `allow-unwrap-in-tests = true` in `clippy.toml`, which covers `#[test]` functions and `#[cfg(test)]` items; an integration-test crate declares its helper modules `#[cfg(test)]`
- Each admitted `unsafe` block has a `// SAFETY:` comment, each `unsafe fn` a `# Safety` doc section, and each `unsafe impl Send`/`Sync` the same justification; CI runs Miri over whatever of it Miri can execute
- CI runs `RUSTFLAGS="-D warnings" cargo clippy --all-targets`

## §rs4. Code Quality

- `Result` and `?` consistently; `.unwrap()` only in tests (enforced by `clippy::unwrap_used`, §rs3); `.expect()` only where failure means a broken invariant
- A non-`Copy` parameter borrows (`&T`, `&str`, `&[T]`) unless the function keeps it; kept and returned values are owned
- `TryFrom` over `as` for narrowing; checked or saturating arithmetic on integers from external input
- No pattern stands in place of a variant of an enum this workspace defines, at any depth of a `match` arm where a sibling arm names a variant in that position, so a new variant fails to compile there
- `thiserror` for library errors, `anyhow` for application entry points
- `Display` for every custom error and user-facing type
- Derive `Debug`, `Clone`, `PartialEq` where appropriate; `Copy` only for small value types
- `cargo fmt` with default settings; commit `rustfmt.toml` if overrides needed
- `From`/`Into` over explicit conversion functions in public APIs

## §rs5. Async Hazards

- No `std` lock guard (`Mutex`, `RwLock`) is held across `.await`; a `tokio` guard may be, where serializing access to the awaited resource is the point
- No blocking call on a runtime thread: blocking I/O goes through `spawn_blocking`; sustained CPU work goes to a dedicated thread or pool. Startup work that completes before the program serves its first request is exempt
- `select!` branches are cancellation-safe
- Channels are bounded
