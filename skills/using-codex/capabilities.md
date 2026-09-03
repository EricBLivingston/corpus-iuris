# Codex CLI Capabilities Reference

What the canonical shapes' elements mean, opt-in flags, the `review` subcommand, sandbox and approval mechanics, gotchas, and the agy↔codex divergences for the using-codex skill. Everything here was measured against `codex-cli 0.145.0`; a later CLI may have moved, so check the installed version before treating a surprise as a defect in the shape.

## Shape Semantics

The canonical shapes are **Case 1** and **Case 2**, in [SKILL.md](SKILL.md) § Invocation Floor; nothing below reproduces them — a shape is copied from there, never assembled from this file (⊢2). This section carries only what the shapes leave unexplained — what their elements mean, and what breaks when one is varied.

**`--sandbox read-only` confines writes, not reads or traversal.** `-C, --cd` is a working root, not a read boundary, and no flag bounds where Codex looks. The prompt's scope line is therefore the only thing that does, which is why it is a required element of the shape rather than a courtesy.

**stdin is read.** `</dev/null` is in both shapes because a non-interactive run must never block on an inherited stdin — it is a default, not a prohibition, and a deliberate pipe displaces it. Piped content arrives as a `<stdin>` block *appended* to the prompt argument rather than replacing it, so the instructions stay in the positional argument and both are read.

**`--add-dir` is the write grant here; on agy it is the read grant and the resolution anchor.** An output directory under `-C` is already writable under `workspace-write`, so `--add-dir` is reached for only when the output directory sits outside `-C`, and it must then be named on the scope line too. Never carry agy's `--add-dir` reasoning across.

**The final message is printed exactly once.** The run's interleaved stdout and stderr go to a scratch log, read only when triaging; the answer is `cat`-ed from the `-o` capture. Printing the transcript *and* the capture duplicates the whole answer into the context window.

**Scratch files live in a session-scoped scratch area**, never under `/tmp` and never in the project tree. The `-o` capture is removed once printed; the run log is **not** — it is the only place a headless auto-deny announces itself, so deleting it unconditionally destroys the diagnostic on exactly the runs that need it. That area is reclaimed anyway. Documents Codex is asked to *write* follow the `{analysis-root}` placement norm instead.

**A Case 2 `$OUT` parent directory is not guaranteed.** `mkdir -p` the `{analysis-root}` directory before a Case 2 run rather than relying on Codex to create it.

---

## Opt-In Flags

Absent from an ordinary engagement; each is reached for deliberately.

| Flag | Purpose |
| ---- | ---- |
| `-c key=value` | Ad-hoc TOML config override. The one in routine use is `-c model_reasoning_effort="medium"` for a latency-sensitive call. |
| `--output-schema <FILE>` | A JSON Schema file describing the final response's shape — the clean way to get a machine-readable verdict, versus asking for JSON in-prompt and parsing whatever comes back. |
| `--json` | Print events to stdout as JSONL. Reach for it to see *what the run did* when a run misbehaves; `-o` remains the way to capture the answer. |
| `-i, --image <FILE>` | Attach image(s) to the initial prompt — a failure screenshot, a diagram, a rendered output under review. Beats describing the image in prose. Repeatable. |
| `-p, --profile <NAME>` | Layers `$CODEX_HOME/<name>.config.toml` over the base user config. **Footgun: agy's `-p` is its prompt flag.** On Codex the prompt is a positional argument, so a ported `-p "…"` is consumed as a profile name and never reaches the model as instructions. Live for anyone who *varies* a shape — a floor copied verbatim is already correct at its own site. |
| `--full-auto` | Alias for `--sandbox workspace-write` on `codex exec`. Prefer the explicit `--sandbox` spelling; recognise the alias in others' commands. |

---

## The `review` Subcommand

`codex exec review [PROMPT]` runs a code review against the current repository and selects the diff itself — `--uncommitted`, `--base <BRANCH>`, or `--commit <SHA>` — so no staging or piping step is needed. Prefer it over a hand-rolled review prompt whenever the unit under review is exactly one of those three; the optional prompt argument carries custom review instructions on top, and `--title <TITLE>` labels the summary.

Its flag set is not the `exec` flag set: no `-C/--cd`, no `-s/--sandbox`, no `--add-dir`, no `-i`. The repository is the one containing the working directory, so the canonical single-root shape does not transfer wholesale. Shared with `exec`: `-m`, `-o`, `-c`, `--json`, `--output-schema`, `--skip-git-repo-check`.

### The `review` shape

A third shape, not one of the floor's two — every mechanism the floor calls the privilege axis is absent, so confinement becomes **post-hoc detection**: treat the run as unconditionally write-capable and compare `git status --porcelain` before and after. `--base`, `--commit` and `--uncommitted` bound the unit under review, not the filesystem; traversal rests on the prompt scope line alone. agy's no-shell clause is **not** ported — the shell is Codex's only file access.

```bash
PROJECT_DIR=/absolute/path/to/repo
SCRATCH=/absolute/path/to/session/scratchpad   # never /tmp, never the project tree
LAST_MSG=$SCRATCH/codex-review.txt

# `review` has no -C: the repo under review is the one containing the working
# directory, so the cd is the only thing aiming it. Without it the run reviews
# whatever repo the shell happens to sit in while the git gate below watches
# $PROJECT_DIR — a mismatch no check catches.
cd "$PROJECT_DIR" || exit 1

before=$(git -C "$PROJECT_DIR" status --porcelain)
codex exec review --base main --skip-git-repo-check \
  -m {codex} -o "$LAST_MSG" --color never \
  "Review the selected diff for auth bypasses and unhandled errors.

Use shell commands only to read files within the paths listed below. Do not search, list, or traverse outside them.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): $PROJECT_DIR" </dev/null > "$SCRATCH/codex-review.log" 2>&1; rc=$?

[ -s "$LAST_MSG" ] || echo "codex FAILED: no final message (rc=$rc)" >&2
[ "$before" = "$(git -C "$PROJECT_DIR" status --porcelain)" ] || \
  echo "codex FAILED: unrequested modification of the working tree" >&2
cat "$LAST_MSG"; rm -f "$LAST_MSG"
```

The working-tree comparison is the general answer to an unrequested edit by any peritus, not a `review`-only precaution; the shared workflow makes it part of verifying before relaying.

---

## Sandbox and Approval Mechanics

The three sandbox levels are named `read-only`, `workspace-write`, and `danger-full-access`; the first two are selected with `--sandbox`, and the third exists only behind the forbidden blanket-bypass flag.

Approval is implicit `never` on `codex exec` — there is no interactive prompt to answer and no way to escalate mid-run, which is why the privilege decision is made when the command is composed. `-a, --ask-for-approval` is a root-`codex` flag and is not valid on `exec`.

---

## Gotchas

1. **Runtime defaults** — on `codex-cli 0.145.0` the CLI defaults to the `{codex}`-bound model at `reasoning effort: high`, so **only lowering is a real move**; there is nothing to raise, and raising was never the fix for a shallow answer. The explicit `-m {codex}` is still required per §3/§4 discipline, and to survive a future default change. A model bump may need a CLI upgrade: check the installed version before bumping the `{codex}` identifier in [SKILL.md](SKILL.md) § Invocation Floor. The forbidden-flag list itself is in [SKILL.md](SKILL.md) § Invocation Floor › Forbidden, copied with the shape (⊢2); only this version-conditional part is here.

2. **`-c key=value` is TOML** — quote string values: `-c model_reasoning_effort="medium"`, not `medium`. An unquoted value is a parse error, not a silent fallback.

3. **The stdin notice is not a hang** — the `Reading additional input from stdin...` line still prints even with stdin closed; the run proceeds regardless.

4. **Auth is a CLI-level login, not a per-run flag** — `codex login` caches a ChatGPT OAuth token under `$CODEX_HOME` (default `~/.codex`), and `codex login --with-api-key` is the alternative where no browser is reachable. Neither is selectable per invocation, so an auth failure is fixed outside the shape rather than inside it.

---

## Divergences from agy

Nothing generalises from one CLI to another, prompt discipline least of all — the first row is a habit that carries across as a silent no-op rather than an error. Each row below is a place where borrowing produces a broken command.

| Concern | Gemini (`using-gemini`) | Codex (`using-codex`) |
| ---- | ---- | ---- |
| File reading | Built-in listing and reading tools, with the shell barred in-prompt | The shell **is** the file reader; there is no separate one, so the prompt licenses shell reads inside the scoped paths and bans only traversal beyond them |
| stdin | Not read in `-p` mode; capture command output to a file and `@`-reference it | Read — see *Shape Semantics* |
| `-p` | The prompt flag | `--profile`, a config layer — see the flag table |
| Workspace root | Implicit — derived from cwd and the granted directories; no root flag exists | `-C, --cd <DIR>`, explicit and mandatory |
| Privilege source | Ambient, from `~/.gemini/antigravity-cli/settings.json`; nothing on the command line grants or confines | On the command line, per run, via `--sandbox` |
| Reasoning lever | Choose between two roster models; no effort flag | One model, one effort flag, default already high |
| Internal timeout | `--print-timeout` binds before the harness ceiling | None — the harness ceiling is the only bound |
| Final-answer capture | Parse stdout | `-o <FILE>` writes the final message as plain text, no JSONL parsing |
| Structured output | None; ask for raw JSON in-prompt | `--output-schema <FILE>` |
| Attachments | Reference any file, including images and PDFs, by `@` path | `-i <FILE>` for images; other files are named in the prompt text |
