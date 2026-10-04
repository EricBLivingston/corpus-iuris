---
name: using-pi
description: "Documents pi invocation: the canonical shapes, the provider/model pair and the auth posture live here (⊢2). Use pi for large-scale, low-effort reading: file sweeps, bulk content assays, per-file triage across hundreds of targets. Use pi for an in-place bulk edit only when a recipe fully specifies the transformation and no site calls for judgement; every other bulk edit goes to Gemini, the stronger model. pi is model-agnostic; it drives any OpenRouter model, tuned here for high volume, low latency, and thus low cost."
---

# Using Pi Skill

Headless `pi -p` only; nothing here describes the interactive TUI.

## Workflow

1. Pick the provider/model pair, then the Case; copy its shape from § Invocation Floor (⊢2).
2. Everything downstream of the call is shared with every peritus: {reference-root}/periti-workflow.md.

## Provenance

pi is <https://pi.dev/>. Every shape below was measured against the Rust reimplementation, <https://github.com/Dicklesworthstone/pi_agent_rust>, whose own root CLAUDE.md is its charter (⊢2).

## Model Selection

`pi --list-models | awk '$1=="openrouter"'` lists pi's OpenRouter catalogue, which omits some served identifiers, `{pi-micro}` among them; unfiltered, it truncates to five providers. Before a batch rides on a model outside the § Invocation Floor table, spend one Case 1 call on it.

## Invocation Floor

Vary only the task text, the model and the shell-side paths. Run each shape as one blocking foreground call at the harness's maximum wait; pi print mode sets no wall-clock cap.

pi print mode has no sandbox: the invoking session's permission mode controls the Bash call that launches it. Its privilege axis is `--approval-mode`, which the shapes leave at `always-ask`; print mode cannot satisfy it, so any tool call pi elects is denied. Inline everything the answer needs and name no path. Every `pi … -p` call takes `</dev/null`: print mode reads a non-tty stdin to EOF, and the harness's stdin socket never reaches EOF, so without it calls intermittently hang indefinitely.

`--no-tools` blocks every tool call pi elects, so no shape has closing clauses. `--no-context-files` stops pi loading `AGENTS.md` / `CLAUDE.md` from cwd and every ancestor; without it, an ancestor instruction lands in the reply.

| Placeholder | Model identifier |
| ---- | ---- |
| `{pi-micro}` | `meta/muse-spark-1.2-contributor` |

Live guidance uses the placeholder, never the literal; `{…-root}` placeholders resolve in the instance ambit.

### Case 1 — answer to stdout

```bash
# Foreground only; sustain the wait by whatever mechanism this harness provides; pi print mode sets no wall-clock cap
out=$(pi --provider openrouter --model {pi-micro} --no-tools --no-context-files -p "Reply with exactly: OK" </dev/null 2>&1); rc=$?
[ -z "$out" ] && echo "pi FAILED (rc=$rc)" >&2
printf '%s\n' "$out"
```

### Case 2 — one call per file, answers to a scratch file

One call per file keeps each context small and isolates a failure to one row.

```bash
ROOT=/absolute/path/to/tree
OUT=/absolute/path/to/scratchpad/assay.tsv
: > "$OUT"

for f in "$ROOT"/src/*.rs; do
  ans=$(pi --provider openrouter --model {pi-micro} --no-tools --no-context-files -p "Answer in one word, yes or no — does the file content below open a network connection?

$(cat "$f")" </dev/null 2>&1)
  [ -z "$ans" ] && { echo "pi FAILED on $f" >&2; continue; }
  printf '%s\t%s\n' "$f" "$ans" >> "$OUT"
done

[ -s "$OUT" ] || echo "pi sweep produced nothing" >&2
```

Grep `$OUT` rather than printing it whole.

### Case 3 — in-place bulk edit, one call per file

```bash
ROOT=/absolute/path/to/tree
FILES="$ROOT/src/loader.py $ROOT/src/runner.py $ROOT/src/cli.py"   # enumerated, never discovered
STAGE=/absolute/path/to/scratchpad/pi-stage
DIFF=$STAGE/bulk-edit.diff
mkdir -p "$STAGE"; : > "$DIFF"

for f in $FILES; do
  new=$(pi --provider openrouter --model {pi-micro} --no-tools --no-context-files -p "Rewrite the source below, replacing every whole-word occurrence of the identifier load_cfg with load_config, in code, comments and strings alike. Leave every other character unchanged. Reply with the complete rewritten source and nothing else: no code fences, no commentary.

$(cat "$f")" </dev/null 2>&1)
  [ -z "$new" ] && { echo "pi FAILED on $f" >&2; continue; }
  case "$new" in '```'*) echo "pi FAILED: fenced reply on $f" >&2; continue ;; esac
  s=$STAGE$f; mkdir -p "${s%/*}"
  printf '%s\n' "$new" > "$s"
  diff -u "$f" "$s" >> "$DIFF"
done
[ -s "$DIFF" ] || echo "pi FAILED: no file changed" >&2
```

Read `$DIFF`; once every hunk is the edit asked for, write back in a separate call, re-declaring `FILES` and `STAGE`:

```bash
for f in $FILES; do [ -f "$STAGE$f" ] && mv "$STAGE$f" "$f"; done
```

A hunk at a file's end can be an artifact: `$(…)` strips trailing newlines and `printf` restores exactly one.

### Forbidden

`pi self-update` and the repo's `install.sh`: each replaces the patched local build with an upstream release that does not compile here.

## Unexercised Surface

Documented by pi. Probe each once before a batch depends on it, and record the outcome here.

- `@file` references in the prompt body, which would replace Case 2's `$(cat …)`.
- `PI_PROVIDER` and `PI_MODEL` environment variables, which would let the flags drop.
- `--mode rpc`: structured request/response over stdio, driving pi programmatically instead of one prompt per process.
- `--smol provider/model`: a cheap model for pi's own internal fan-out, an axis separate from `--model`.

## Auth and Trusted Input

Credentials live in `~/.pi/agent/auth.json` (mode 600); `OPENROUTER_API_KEY` is honoured as well. A stored key can be a `$CMD:` command pi executes at request time (pi's README § Authentication & Credential Management), which makes `auth.json` and `models.json` trusted input: never write either from model-generated or delegate-supplied content, and never point pi at a configuration tree you did not author.

## Triage

- **Empty stdout is a refusal or an auth failure.** Run `pi doctor` first (several of its WARNs are routine and unrelated to the call), then check the model identifier.
- **`pi: command not found`, or a binary that vanished,** is an installation fault.
- **Tool-denial text, rc=3, and a call taking tens of seconds or more** is a prompt that named a path; inline the content.
- **A rejected model identifier** is tested by a Case 1 call; the catalogue (§ Model Selection) is incomplete.
