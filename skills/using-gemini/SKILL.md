---
name: using-gemini
description: Documents agy invocation, the CLI for Gemini models — the canonical shapes, the mandatory prompt clauses and the model roster live here (⊢2). Use Gemini for analysis of very large files, surveys across many documents, instance-finding over a tree, mechanical bulk edits, second-opinion review. Use when the user asks for Gemini, or when the reading spans more files than this context should take on — the window buys breadth of reading and judgement over it, not counting. A task whose product is a tally, a per-file column, or any other count stays local, where grep answers it in a fraction of the wall clock.
---

# Using Gemini Skill

The canonical invocation shapes, workflow, triage, edge cases, and model selection for the headless Gemini CLI tool `agy -p`. Nothing here describes the interactive TUI.

## Workflow

1. Choose the model (below); then, if the call is not a plain single-root one, the shape (below). Copy the shape from § Invocation Floor below — never compose one from memory (⊢2).
2. Everything downstream of the call — foreground execution, splitting, verification, relaying, advisory second opinions, chaining — is shared with every peritus and lives in {reference-root}/periti-workflow.md.

## Model Selection

`--model {gemini-pro}` for complex reasoning, large-file analysis, architecture review, and code review. `--model {gemini-flash}` for fast summaries, simple extraction, and mechanical bulk edits. See **[models.md](models.md)** for the selection table, effort tiers, and the failure behaviour of a bad identifier.

## Invocation Floor

These shapes cover every engagement. Both need `@`+**absolute** file references, an explicit roster model, `--print-timeout 8m` (agy's own default is `5m0s`, which silently cuts a large-tree run off), and — as the prompt's closing lines, verbatim — the no-shell clause, the mandate clause, and a scope line naming exactly the paths granted on the command line. Every path the prompt `@`-references must itself be granted: headless mode cannot prompt for approval, so an ungranted read is auto-denied, and neither cwd nor a trusted workspace substitutes. `--add-dir` is the only grant channel and it takes **directories** — the scope line renders the grant and never creates one, so an `@`-referenced file is reached by granting a directory above it, not by naming the file anywhere. An exit 0 is not success.

| Placeholder | Model identifier |
| ---- | ---- |
| `{gemini-pro}` | `gemini-3.1-pro-high` |
| `{gemini-flash}` | `gemini-3.7-flash-high` |

Live guidance carries the placeholder, never the literal: model identifiers resolve in the table above, and every `{…-root}` placeholder in the instance ambit.

### Case 1 — answer to stdout

```bash
# Foreground only; sustain an 8m wait by whatever mechanism this harness provides — agy's --print-timeout binds first
ROOT=/absolute/path/to/tree

out=$(agy --add-dir "$ROOT" --model {gemini-flash} --print-timeout 8m -p "Summarize what @$ROOT/src/auth.py does, function by function; do not modify any file.

Do NOT use shell commands or the Bash tool; use only your built-in file listing and file reading tools.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): @$ROOT" 2>&1); rc=$?
[ -z "$out" ] && echo "agy FAILED (rc=$rc)" >&2
printf '%s\n' "$out" | grep -q '^Error: permission check failed' && echo "agy FAILED: denial in output (rc=$rc)" >&2
printf '%s\n' "$out"
```

Say "do not modify any file" whenever read-only behaviour matters; nothing else enforces it.

A denied run exits 0 and writes its error to *stdout*, which `2>&1` then folds into `$out` — so the blank check passes a run that produced nothing but a denial. Case 1 has no product to stat, which leaves the grep as its only assay.

### Case 2 — agy writes one document and summarizes it to stdout

```bash
ROOT=/absolute/path/to/tree
OUT=$ROOT/{analysis-root}/Findings.md

out=$(agy --add-dir "$ROOT" --model {gemini-flash} --print-timeout 8m -p "List every file under @$ROOT/rules that mentions 'no-shell clause', with the matching line. Write the full list to @$OUT, then summarise briefly what you wrote.

Do NOT use shell commands or the Bash tool; use only your built-in file listing and file reading tools.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): @$ROOT" 2>&1); rc=$?
[ -z "$out" ] && echo "agy FAILED (rc=$rc)" >&2
printf '%s\n' "$out" | grep -q '^Error: permission check failed' && echo "agy FAILED: denial in output (rc=$rc)" >&2
[ -s "$OUT" ] || echo "agy FAILED: $OUT missing or empty" >&2
printf '%s\n' "$out"
```

The checks are independent — no one result implies another. Always ask for the stdout summary. A Case 2 run writes nothing unless the `agentMode` write gate is set — [capabilities.md](capabilities.md) § Write Gate. Name the exact output path in the prompt.

### Forbidden

`--dangerously-skip-permissions`, in any shape (`periti.md § The engagement`) — agy's stderr recommends it on *every* denial, not occasionally.

## Shapes Beyond The Single-Root Call

Each of these is a delta on the shape already in hand; the mandatory prompt clauses ride along unchanged.

### Multi-root

Repeat the flag — one `--add-dir` per path, never `--add-dir=A,B` — and name every one of those paths on the prompt's scope line, so the two renderings of the path list stay identical:

```bash
--add-dir "$SRC" --add-dir "$DOCS" --add-dir "$OUTDIR"
```

### Feeding in what agy cannot be handed

Capture to a file inside a granted directory, then `@`-reference that file in the prompt body (why, in [capabilities.md](capabilities.md) under *Shape Semantics*):

```bash
git diff HEAD~3 > "$OUTDIR/diff.patch"
uv run pytest tests/unit/ > "$OUTDIR/pytest.out" 2>&1
# prompt body: Review the changes in @$OUTDIR/diff.patch for bugs.
```

Never pipe a producer into agy. Beyond losing the input, a slow producer holds the shell open long after agy exits and looks exactly like an agy hang: `bash` waits for every pipeline member, so the harness timeout can fire although agy already answered and exited.

### Capturing large output

When the answer is long, keep it out of the context window — redirect the captured stdout to a scratch file and read or grep that instead of printing it:

```bash
printf '%s\n' "$out" > "$SCRATCH/agy-out.md"
```

For anything report-sized, prefer having agy write the document itself and summarise it to stdout; that gives a file to verify as well as a short answer to relay.

## Triage

- **A zero-byte result is a refusal**, not an empty finding — so it has a cause worth naming. First suspect: agy elected a `command` / `run_command` call, which headless mode refuses.
- **To see the refusal**, re-run with `--log-file` at a throwaway scratch path (never inside a project), then `grep -i 'soft-deny'` the log for the tool that was refused. `--log-file` stays out of ordinary calls.
- **Dozens of tool-call steps, then failure** is the path-resolution spiral, not a model fault: a reference agy cannot resolve sends it looking. Prevent it rather than diagnose it — before invoking, check that every path the prompt `@`-references is absolute and sits under a granted directory, per the operation table in [capabilities.md](capabilities.md).
- **Never search from a relative reference to a tree outside cwd** — resolve it to an absolute path under a grant before invoking.
- **A run that appears to hang** is never a bad model identifier: that fails loudly with exit 1. Suspect a pipeline producer, or work too large for one call, instead.
- **A run cut off at the timeout** was too large for one call. The shape's own print timeout binds before the harness maximum, so there is no bound to raise — split the work.
- Exit-code meanings are in [capabilities.md](capabilities.md).

## References

- **[capabilities.md](capabilities.md)** — the agy mechanics the floor leaves to a sidecar: shape semantics, native tools, the write gate, the bulk-edit shape, exit codes
- **[models.md](models.md)** — model details and selection guidance
- **{reference-root}/periti-workflow.md** — the protocol shared by every peritus
