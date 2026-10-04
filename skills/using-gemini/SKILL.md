---
name: using-gemini
description: "Documents agy invocation, the CLI for Gemini models: the canonical shapes, the mandatory prompt clauses and the model roster live here (⊢2). Use Gemini for analysis of very large files, surveys across many documents, instance-finding over a tree, second-opinion review, and mechanical in-place bulk edits, for which it is the default peritus, being the stronger model. Use when the user asks for Gemini, or when the reading spans more files than this context should take on: the window buys breadth of reading and judgement over it. A task whose product is a tally, a per-file column, or any other count stays local, where grep answers it in a fraction of the wall clock."
---

# Using Gemini Skill

Headless `agy -p` only; nothing here describes the interactive TUI.

## Workflow

1. Choose the model, then the Case; copy its shape from § Invocation Floor (⊢2), applying a § Shapes Beyond The Single-Root Call delta where the call needs one.
2. Everything downstream of the call is shared with every peritus: {reference-root}/periti-workflow.md.

## Model Selection

`{gemini-flash}` serves every task. Only a full roster identifier resolves (`agy models` lists them): agy has no `auto` alias and no shorthand. Effort rides the identifier's suffix (`…-flash-medium`), so the shapes pass no `--effort`.

## Invocation Floor

Vary only the task text, the model and the paths. The prompt's closing clauses are verbatim, and its scope line names exactly the directories `--add-dir` grants. `--print-timeout 8m` overrides agy's `5m0s` default, which silently cuts a large-tree run off. Run it as one blocking foreground call at the harness's maximum wait. Never pass `--dangerously-skip-permissions`, which agy's stderr recommends on every denial (`periti.md § The engagement`).

Every `@`-referenced path is absolute and sits under a directory granted by `--add-dir`, the only grant channel: headless mode cannot prompt, so an ungranted read is auto-denied, and neither cwd nor a trusted workspace substitutes. The scope line renders the grant; it never creates one.

Cases 2 and 3 write nothing, silently, unless the `agentMode` write gate is set ([capabilities.md](capabilities.md) § Write Gate).

| Placeholder | Model identifier |
| ---- | ---- |
| `{gemini-flash}` | `gemini-3.8-flash-medium` |

Live guidance uses the placeholder, never the literal; `{…-root}` placeholders resolve in the instance ambit.

Every Case runs in one Bash call that opens with this preamble, copied whole:

```bash
# Foreground only; sustain an 8m wait by whatever mechanism this harness provides — agy's --print-timeout binds first
ROOT=/absolute/path/to/tree
agy_run() {   # $1 model, $2 task text; the closing clauses follow it verbatim
  out=$(agy --add-dir "$ROOT" --model "$1" --print-timeout 8m -p "$2

Do NOT use shell commands or the Bash tool; use only your built-in file listing and file reading tools.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): @$ROOT" 2>&1); rc=$?
  [ -z "$out" ] && echo "agy FAILED (rc=$rc)" >&2
  printf '%s\n' "$out" | grep -q 'auto-denied' && echo "agy FAILED: denial in output (rc=$rc)" >&2
}
```

### Case 1 — answer to stdout

```bash
agy_run {gemini-flash} "Summarize what @$ROOT/src/auth.py does, function by function; do not modify any file."
printf '%s\n' "$out"
```

Say "do not modify any file" whenever read-only behaviour matters; nothing else enforces it.

### Case 2 — agy writes one document and summarizes it to stdout

```bash
FILES="$ROOT/rules/a.md $ROOT/rules/b.md $ROOT/rules/c.md"   # enumerated, never discovered
OUT=$ROOT/{analysis-root}/Findings.md
agy_run {gemini-flash} "For each of these files, list every line that mentions 'no-shell clause'. Write the full list to @$OUT, then summarise briefly what you wrote: $(printf '@%s ' $FILES)"
[ -s "$OUT" ] || echo "agy FAILED: $OUT missing or empty" >&2
printf '%s\n' "$out"
```

Keep the prompt's exact output path and its request for a stdout summary. agy hands discovery under a directory to a subagent, which in trials stalled or drew a refused `read_url` call and wrote nothing, so enumerate a written report's inputs.

### Case 3 — agy edits the enumerated files in place

```bash
FILES="$ROOT/src/loader.py $ROOT/src/runner.py $ROOT/src/cli.py"   # enumerated, never discovered
DIFF=$ROOT/{analysis-root}/bulk-edit
git -C "$ROOT" diff --stat -- $FILES > "$DIFF.before"
agy_run {gemini-flash} "In these files and no others, rename the function \`load_cfg\` to \`load_config\` at every definition and call site, then summarise briefly what you changed: $FILES"
git -C "$ROOT" diff --stat -- $FILES > "$DIFF.after"
cmp -s "$DIFF.before" "$DIFF.after" && echo "agy FAILED: no file changed" >&2
printf '%s\n' "$out"
```

The file set is enumerated, never discovered: a discovered set is how a mechanical edit becomes an unbounded one.

## Shapes Beyond The Single-Root Call

Deltas on a Case; its closing clauses stay verbatim.

### Multi-root

One `--add-dir` per directory, never `--add-dir=A,B`, and the scope line names every one:

```bash
--add-dir "$SRC" --add-dir "$DOCS" --add-dir "$OUTDIR"
```

### Feeding in what agy cannot be handed

agy reads no stdin in prompt mode, so capture to a file inside a granted directory and `@`-reference it:

```bash
git diff HEAD~3 > "$OUTDIR/diff.patch"
uv run pytest tests/unit/ > "$OUTDIR/pytest.out" 2>&1
# prompt body: Review the changes in @$OUTDIR/diff.patch for bugs.
```

Never pipe a producer into agy: `bash` waits for every pipeline member, so a slow producer outlives agy and presents as an agy hang.

### Capturing large output

Redirect a long `$out` to a scratch file and read or grep it there. Anything report-sized is a Case 2: a file to verify, and a short answer to relay.

## Triage

- **A zero-byte result, or an `auto-denied` line at exit 0, is a refusal.** First suspect an elected `command` / `run_command` call, which headless mode refuses.
- **To see the refusal**, re-run with `--log-file` at a throwaway scratch path (never inside a project), then `grep -i 'soft-deny'` the log for the refused tool.
- **Dozens of tool-call steps, then failure** is the path-resolution spiral: some `@`-reference is relative or under no grant ([capabilities.md](capabilities.md) § Shape Semantics).
- **A run that appears to hang, or is cut off at the timeout,** has a pipeline producer or work too large for one call (split it); a bad model identifier fails at once with exit 1.
- **A read under `/tmp` outside every `--add-dir` grant succeeded once**, while ungranted reads of `/etc` and `~/.claude` were denied; the cause is unexplained, so test a denial with a path outside `/tmp`.
- Exit codes: [capabilities.md](capabilities.md) § Exit Codes.
