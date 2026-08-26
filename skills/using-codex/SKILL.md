---
name: using-codex
description: Load this skill before every Codex invocation — the canonical shapes, the sandbox privilege choice and the mandatory prompt clauses live here, and a command composed from memory gets them wrong. Delegates one hard, self-contained problem to the Codex CLI: a root cause that resists inspection, an architecture trade-off worth a second opinion, a security read on a targeted change. Use when the user asks for Codex, or when one focused question needs a rigorous answer rather than a survey.
---

# Using Codex Skill

The canonical invocation shapes, workflow, triage, and edge cases for non-interactive `codex exec`. Nothing here describes the root `codex` TUI.

## Workflow

1. Pick the least privilege the task needs, then the effort. Copy the shape from § Invocation Floor below — never compose one from memory (⊢2); the effort default and the one lever are gotcha 1 in [capabilities.md](capabilities.md).
2. Everything downstream of the call — foreground execution, splitting, verification, relaying, advisory second opinions, chaining — is shared with every other delegate and lives in {reference-root}/delegation-workflow.md.

## Invocation Floor

These shapes cover every delegation. Both need absolute paths in the prompt text, `-m {codex}`, `-c model_reasoning_effort="high"`, `--skip-git-repo-check`, `--color never`, `</dev/null`, and — as the prompt's closing lines, verbatim — the scoped-shell-read clause, the mandate clause, and a scope line naming exactly the paths granted on the command line. An exit 0 is not success. `-s, --sandbox` is the privilege axis and real enforcement.

| Placeholder | Model identifier |
| ---- | ---- |
| `{codex}` | `gpt-5.6-sol` |

Live guidance carries the placeholder, never the literal: the model identifier resolves in the table above, and every `{…-root}` placeholder in the instance ambit.

### Case 1 — answer to stdout

```bash
# Foreground only; sustain the wait by whatever mechanism this harness provides — Codex has no internal timeout, so that ceiling is the only bound
DIR=/absolute/path/to/repo; S=/absolute/path/to/session/scratchpad

codex exec --skip-git-repo-check --sandbox read-only \
  -C "$DIR" -m {codex} -c model_reasoning_effort="high" -o "$S/last.txt" --color never \
  "Analyze $DIR/src/auth.py for auth bypasses. Report findings only.

Use shell commands only to read files within the paths listed below. Do not search, list, or traverse outside them.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): $DIR" </dev/null > "$S/run.log" 2>&1; rc=$?

[ -s "$S/last.txt" ] || echo "codex FAILED: no final message (rc=$rc)" >&2
cat "$S/last.txt"; rm -f "$S/last.txt"
```

### Case 2 — Codex writes one document and summarizes it to stdout

```bash
DIR=/absolute/path/to/repo; S=/absolute/path/to/session/scratchpad
OUT=$DIR/{analysis-root}/Review.md

codex exec --skip-git-repo-check --sandbox workspace-write \
  -C "$DIR" -m {codex} -c model_reasoning_effort="high" -o "$S/last.txt" --color never \
  "Review $DIR/src/auth.py. Write the full review to $OUT, then summarise briefly what you wrote.

Use shell commands only to read files within the paths listed below. Do not search, list, or traverse outside them.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): $DIR" </dev/null > "$S/run.log" 2>&1; rc=$?

[ -s "$S/last.txt" ] || echo "codex FAILED: no final message (rc=$rc)" >&2
[ -s "$OUT" ] || echo "codex FAILED: $OUT missing or empty" >&2
cat "$S/last.txt"; rm -f "$S/last.txt"
```

The two checks are independent — neither result implies the other. Always ask for the stdout summary.

### Forbidden

`--dangerously-bypass-approvals-and-sandbox`, and `--ephemeral` unconditionally — session files are required for forensics.

## Shapes Beyond The Single-Root Call

Deltas on the shape already in hand; the mandatory prompt clauses ride along unchanged. Opt-in flags reached for by these shapes are inventoried in [capabilities.md](capabilities.md).

### Feeding in content Codex cannot reach by path

Codex has no `@` reference syntax, so command output arrives one of two ways.

**Piped.** Keep the instructions as the prompt argument and let the bytes arrive alongside them (see *Shape Semantics* in [capabilities.md](capabilities.md)).

```bash
git diff HEAD~3 | codex exec … "Review the diff in the <stdin> block for bugs and security issues."
```

**Staged.** Capture to a file, then name that file by absolute path in the prompt body — the route whenever a later run must reread the content or the answer should cite it by path.

```bash
git diff HEAD~3 > "$PROJECT_DIR/{analysis-root}/diff.patch"
# prompt body: Review the diff at $PROJECT_DIR/{analysis-root}/diff.patch for bugs and security issues.
```

Keep the capture file under `-C` so it needs no extra grant, and name it on the scope line if it lives anywhere else.

## Triage

- **An empty final message is a refusal or an abort**, not an empty finding, and its diagnostic is already on disk: read the run log the shape redirects the interleaved transcript into before re-running, because a headless auto-deny announces itself nowhere else.
- **Suspect the prompt's paths first.** Codex must locate every path the prompt names; a path that is wrong, relative, or ungranted turns into a search, which the home-scan mandate forbids.
- **A refused write** under `read-only` is the sandbox working as intended, not a failure to diagnose — the fix is choosing the right privilege for the case, never widening it after the fact.
- That log's banner and token-usage footer also carry the model version, effort level, and token cost — worth reading on any run whose answer looks off-model.

## References

- **[capabilities.md](capabilities.md)** — the codex mechanics the floor leaves to a sidecar: shape semantics, opt-in flags, the `review` subcommand, sandbox mechanics, divergences from agy
- **{reference-root}/delegation-workflow.md** — the protocol shared by every delegate
