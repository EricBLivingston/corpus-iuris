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

These shapes cover every engagement. Both need `--provider openrouter`, an explicit roster `--model`, `-p`, and absolute paths in the prompt text. pi in print mode has no sandbox axis of its own: the call is single-shot text in, text out, and the invoking session's own permission mode governs the Bash call that launches it, so there is no privilege flag to choose and none to invent. Its approval mode is `always-ask`, which print mode cannot satisfy, so a tool call pi elects is denied. Inline everything the answer needs and name no path, since a named path invites the read that is about to be refused. An exit 0 is not success. One blocking foreground call, with the harness's own wait set to its maximum — a default wait cuts a long engagement off mid-run.

**The prompt is the only control.** pi holds no canon of its caller's (`periti.md § The engagement`), and its default tools include `bash`, `find`, `grep` and `ls`, so a prompt that does not preclude a sweep permits one. Every call that could touch the filesystem closes, verbatim and last, with the no-shell clause, the mandate clause, and a scope line naming the paths the work is confined to. Whether pi honours them is unmeasured; the roots below are the backstop if it does not.

**cwd is the workspace root**, extended by `--add-dir`; paths outside every root are fail-closed. Independently, pi discovers `AGENTS.md` / `CLAUDE.md` in the cwd and every ancestor directory, which only `--no-context-files` disables. Launch from the directory the work is in, and grant no root wider than the work: a root the scope line does not name is one the scope line cannot confine.

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
  ans=$(pi --provider openrouter --model {pi-micro} -p "Answer in one word, yes or no — does the file content below open a network connection?

$(cat "$f")

Do NOT use shell commands, or your bash, find, grep or ls tools; everything you need is in this prompt.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): $ROOT" 2>&1)
  [ -z "$ans" ] && { echo "pi FAILED on $f" >&2; continue; }
  printf '%s\t%s\n' "$f" "$ans" >> "$OUT"
done

[ -s "$OUT" ] || echo "pi sweep produced nothing" >&2
```

The same sweep with a header naming the file, which is what the floor's no-path rule forbids:

```bash
  # NOT this — the header names a path, and pi opens what it already has
  ans=$(pi --provider openrouter --model {pi-micro} -p "Answer in one word, yes or no — does this file open a network connection?

--- FILE: $f ---
$(cat "$f")" 2>&1)
```

Sweep output goes to a file, never into the context window; read or grep the result afterwards.

### Forbidden

`pi self-update`, which would replace the patched local build with an upstream release that does not compile here, and the repo's `install.sh`, which does the same by another route.

## Unexercised Surface

Documented by pi. Probe each once before a batch depends on it, and record the outcome here.

- `@file` references in the prompt body — would replace the `$(cat …)` substitution in Case 2.
- `PI_PROVIDER` and `PI_MODEL` environment variables — would allow the flags to be dropped.
- `--mode rpc` — structured request/response over stdio, for driving pi programmatically instead of one prompt per process.
- `--smol provider/model` — nominates a cheap model for pi's own internal fan-out, a separate axis from `--model`.

## Auth and Trusted Input

Credentials live in `~/.pi/agent/auth.json` — `{"openrouter": {"type": "api_key", "key": …}}`, mode 600; `OPENROUTER_API_KEY` is honoured as well. `pi doctor` diagnoses environment and auth health. Run it before suspecting the shape, and read its WARNs before chasing one — several are routine and unrelated to the call.

A stored key may be a literal, `$ENV:VAR`, or `$CMD:command` resolved at request time (pi's README § auth, `README.md:1860` in the repo, verified against source 2026-08-28). That shell-execution path makes `auth.json` and `models.json` trusted input: never write either from model-generated or delegate-supplied content, and never point pi at a configuration tree you did not author.

## Triage

- **Empty stdout is a refusal or an auth failure**, not an empty finding. Run `pi doctor` first, then check the model identifier.
- **A rejected model identifier** is checked against `pi --list-models | awk '$1=="openrouter"'`, not against memory — the roster is the provider's and it moves.
- **`pi: command not found`, or a binary that vanished**, is an installation fault rather than a shape fault.
- **A slow run whose answers carry the CLI's denial text**, others returning a bare `NONE`, is a prompt that invited a tool call. Measured against the same content: minutes per call with a path named above it, 1.4s with it inlined and no path. That pi retries the denial rather than surfacing it is inferred from the elapsed time, not observed.

## References

- **{reference-root}/periti-workflow.md** — the protocol shared by every peritus
