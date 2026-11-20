# Codex CLI Capabilities Reference

What the canonical shapes' elements mean, opt-in flags, the `review` subcommand, sandbox and approval mechanics, gotchas, and the agy↔codex divergences for the using-codex skill. Everything here was measured against `codex-cli 0.171.0`; a later CLI may have moved, so check the installed version before treating a surprise as a defect in the shape.

## Shape Semantics

The canonical shapes are **Case 1** and **Case 2**, in [SKILL.md](SKILL.md) § Invocation Floor; nothing below reproduces them — a shape is copied from there, never assembled from this file (⊢2). This section states only what the shapes leave unexplained — what their elements mean, and what breaks when one is varied.

**`--sandbox read-only` confines writes, not reads or traversal** (a `head` of a file outside `-C` succeeds). `-C, --cd` is a working root, not a read boundary, and no flag bounds where Codex looks. The prompt's scope line is therefore the only thing that does, which is why it is a required element of the shape rather than a courtesy.

**stdin is read.** `</dev/null` is in both shapes because a non-interactive run must never block on an inherited stdin — it is a default, not a prohibition, and a deliberate pipe displaces it. Piped content arrives as a `<stdin>` block *appended* to the prompt argument rather than replacing it, so the instructions stay in the positional argument and both are read.

**`--add-dir` is the write grant here; on agy it is the read grant and the resolution anchor.** An output directory under `-C` is already writable under `workspace-write`, so `--add-dir` is resorted to only when the output directory sits outside `-C`, and it must then be named on the scope line too. Never carry agy's `--add-dir` reasoning across.

**The final message is printed exactly once.** The run's interleaved stdout and stderr go to a scratch log, read only when triaging; the answer is `cat`-ed from the `-o` capture. Printing the transcript *and* the capture duplicates the whole answer into the context window.

**Scratch files live in a session-scoped scratch area**, never under `/tmp` and never in the project tree. The `-o` capture is removed once printed; the run log is **not** — it is the only place a headless auto-deny announces itself, so deleting it unconditionally destroys the diagnostic on exactly the runs that need it. That area is reclaimed anyway. Documents Codex is asked to *write* follow the `{analysis-root}` placement norm instead.

**A Case 2 `$OUT` parent directory is not guaranteed.** `mkdir -p` the `{analysis-root}` directory before a Case 2 run rather than relying on Codex to create it.

---

## Opt-In Flags

Absent from an ordinary engagement; each is resorted to deliberately.

| Flag | Purpose |
| ---- | ---- |
| `-c key=value` | Ad-hoc TOML config override. The one in routine use is `-c model_reasoning_effort="medium"` for a latency-sensitive call. |
| `--output-schema <FILE>` | A JSON Schema file describing the final response's shape — the clean way to get a machine-readable verdict, versus asking for JSON in-prompt and parsing whatever comes back. |
| `--json` | Print events to stdout as JSONL. Resort to it to see *what the run did* when a run misbehaves; `-o` remains the way to capture the answer. |
| `-i, --image <FILE>` | Attach image(s) to the initial prompt — a failure screenshot, a diagram, a rendered output under review. Beats describing the image in prose. Repeatable. |
| `-p, --profile <NAME>` | Layers `$CODEX_HOME/<name>.config.toml` over the base user config. **Footgun: agy's `-p` is its prompt flag.** On Codex the prompt is a positional argument, so a ported `-p "…"` is consumed as a profile name and never reaches the model as instructions. Live for anyone who *varies* a shape — a floor copied verbatim is already correct at its own site. |

---

## The `review` Subcommand

`codex exec review` reviews the repository containing the working directory and selects the diff itself: `--uncommitted`, `--base <BRANCH>`, or `--commit <SHA>`. It has no `-C` and no `--sandbox`.

**A selector and a prompt argument are mutually exclusive** (exit 2), so a selected review cannot carry the mandatory closing clauses. A review therefore runs as Case 1 with the diff piped ([SKILL.md](SKILL.md) § Feeding in content Codex cannot read by path).

---

## Sandbox and Approval Mechanics

The three sandbox levels are named `read-only`, `workspace-write`, and `danger-full-access`, all values of `--sandbox`. `workspace-write` makes `/tmp` and `$TMPDIR` writable besides `-C` and `--add-dir`.

Approval is implicit `never` on `codex exec` — there is no interactive prompt to answer and no way to escalate mid-run, which is why the privilege decision is made when the command is composed. `-a, --ask-for-approval` is a root-`codex` flag and is not valid on `exec`.

---

## Gotchas

1. **Runtime defaults** — the model catalog (`codex debug models`) lists each model's efforts and its default, `medium` for the `{codex}`-bound model; `~/.codex/config.toml` overrides the catalog, and `-m` and `-c` override both. The floor's `-c model_reasoning_effort="high"` is therefore what sets `high`, and the explicit `-m {codex}` is required because the user config's `model` may differ. A model bump may need a CLI upgrade: check the installed version before bumping the `{codex}` identifier in [SKILL.md](SKILL.md) § Invocation Floor. The forbidden-flag list itself is in [SKILL.md](SKILL.md) § Invocation Floor › Forbidden, copied with the shape (⊢2); only this version-conditional part is here.

2. **`-c key=value` is TOML with a literal-string fallback** — a value that fails to parse as TOML is taken as a literal string, which is how the floor's shell-unquoted `high` arrives. An invalid value is not caught by the CLI: `-c model_reasoning_effort=bogus` reaches the API and exits 1 with `invalid_request_error`.

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
| `-c` | `--continue`, which resumes the most recent conversation | A config override |
| `-i` | `--prompt-interactive` | `--image` |
| Workspace root | Implicit — derived from cwd and the granted directories; no root flag exists | `-C, --cd <DIR>`, explicit and mandatory |
| Privilege source | Ambient, from `~/.gemini/antigravity-cli/settings.json`; `--mode plan` confines a run | On the command line, per run, via `--sandbox` |
| Reasoning lever | Effort rides the identifier suffix; a conflicting `--effort` exits 1 | One model; effort set per run by `-c model_reasoning_effort`, which the floor pins to `high` |
| Internal timeout | `--print-timeout`, which the shapes set below the harness ceiling; unset, agy waits for the turn to complete | None — the harness ceiling is the only bound |
| Final-answer capture | Parse stdout | `-o <FILE>` writes the final message as plain text, no JSONL parsing |
| Structured output | `--output-format json` with `--json-schema`; the shapes ask for raw JSON in-prompt | `--output-schema <FILE>` |
| Attachments | Reference any file, including images and PDFs, by `@` path | `-i <FILE>` for images; other files are named in the prompt text |
