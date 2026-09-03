---
name: using-pi
description: "Documents pi invocation: the canonical shapes, the provider/model pair and the auth posture live here (⊢2). Use pi for large-scale, low-effort work — file sweeps, bulk content assays, per-file triage across hundreds of targets, where the work is reading, not reasoning. pi is model-agnostic; it drives any OpenRouter model, tuned here for high volume, low latency, and thus low cost."
---

# Using Pi Skill

The canonical invocation shapes, model selection, verification, and triage for the headless pi CLI `pi -p`. Nothing here describes the interactive TUI.

## Workflow

1. Pick the provider/model pair (below). Copy the shape from § Invocation Floor below — never compose one from memory (⊢2).
2. Everything downstream of the call — foreground execution, splitting, verification, relaying, advisory second opinions, chaining — is shared with every peritus and lives in {reference-root}/periti-workflow.md.

## Provenance

pi is <https://pi.dev/>. Every shape below was measured against the Rust reimplementation, <https://github.com/Dicklesworthstone/pi_agent_rust>, whose own root CLAUDE.md is its charter (⊢2).

## Model Selection

Every call names both halves: `--provider openrouter` and an explicit `--model`. `pi --list-models | awk '$1=="openrouter"'` enumerates the roster the provider currently serves (228 entries on 2026-08-28); unfiltered, the command truncates to 5 of 103 providers. Before a batch rides on a model not in the § Invocation Floor table, spend one probe call on it.

## Invocation Floor

These shapes cover every engagement. Both need `--provider openrouter`, an explicit roster `--model`, `-p`, and absolute paths in the prompt text. pi in print mode has no approval gate and no sandbox axis of its own — the call is single-shot text in, text out, and the invoking session's own permission mode governs the Bash call that launches it, so there is no privilege flag to choose and none to invent. An exit 0 is not success.

| Placeholder | Model identifier |
| ---- | ---- |
| `{pi-micro}` | `meta/muse-spark-1.2-contributor` |

Live guidance carries the placeholder, never the literal: the model identifier resolves in the table above, and every `{…-root}` placeholder in the instance ambit.

### Case 1 — answer to stdout

```bash
# Foreground only; sustain the wait by whatever mechanism this harness provides — pi print mode has no internal timeout
out=$(pi --provider openrouter --model {pi-micro} -p "Reply with exactly: OK" 2>&1); rc=$?
[ -z "$out" ] && echo "pi FAILED (rc=$rc)" >&2
printf '%s\n' "$out"
```

### Case 2 — one call per file, answers to a scratch file

Prompt text is the measured channel by which content reaches pi, so a sweep substitutes each file into the prompt and calls once per file. One call per file keeps each context small and isolates each failure to a single row rather than the batch.

```bash
ROOT=/absolute/path/to/tree
OUT=/absolute/path/to/scratchpad/assay.tsv
: > "$OUT"

for f in "$ROOT"/src/*.rs; do
  ans=$(pi --provider openrouter --model {pi-micro} -p "Answer in one word, yes or no — does this file open a network connection?

$(cat "$f")" 2>&1)
  [ -z "$ans" ] && { echo "pi FAILED on $f" >&2; continue; }
  printf '%s\t%s\n' "$f" "$ans" >> "$OUT"
done

[ -s "$OUT" ] || echo "pi sweep produced nothing" >&2
```

Sweep output goes to a file, never into the context window; read or grep the result afterwards.

### Forbidden

`pi self-update`, which would replace the patched local build with an upstream release that does not compile here, and the repo's `install.sh`, which does the same by another route.

## Unmeasured Surface

Documented by pi and unmeasured. Probe each once before a batch depends on it, and record the outcome here.

- `@file` references in the prompt body (UNMEASURED) — would replace the `$(cat …)` substitution in Case 2.
- `PI_PROVIDER` and `PI_MODEL` environment variables (UNMEASURED) — would allow the flags to be dropped; keep both explicit until that is proven.
- `--mode rpc` (UNMEASURED) — structured request/response over stdio, for driving pi programmatically instead of one prompt per process.
- `--smol provider/model` (UNMEASURED) — nominates a cheap model for pi's own internal fan-out, a separate axis from `--model`.

## Auth and Trusted Input

Credentials live in `~/.pi/agent/auth.json` — `{"openrouter": {"type": "api_key", "key": …}}`, mode 600; `OPENROUTER_API_KEY` is honoured as well. `pi doctor` diagnoses environment and auth health. Run it before suspecting the shape, and read its WARNs before chasing one — several are routine and unrelated to the call.

A stored key may be a literal, `$ENV:VAR`, or `$CMD:command` resolved at request time (pi's README § auth, `README.md:1860` in the repo, verified against source 2026-08-28). That shell-execution path makes `auth.json` and `models.json` trusted input: never write either from model-generated or delegate-supplied content, and never point pi at a configuration tree you did not author.

## Triage

- **Empty stdout is a refusal or an auth failure**, not an empty finding. Run `pi doctor` first, then check the model identifier.
- **A rejected model identifier** is checked against `pi --list-models | awk '$1=="openrouter"'`, not against memory — the roster is the provider's and it moves.
- **`pi: command not found`, or a binary that vanished**, is an installation fault rather than a shape fault.

## References

- **{reference-root}/periti-workflow.md** — the protocol shared by every peritus
