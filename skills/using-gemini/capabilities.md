# Agy CLI Capabilities Reference

What the canonical shapes' elements mean, the native tool inventory, the write gate, the bulk-edit shape, and exit codes for the using-gemini skill. Everything here describes headless `agy -p`.

## Shape Semantics

The canonical shapes are **Case 1** and **Case 2**, in [SKILL.md](SKILL.md) § Invocation Floor; nothing below reproduces them — a shape is copied from there, never assembled from this file (⊢2). This section carries only what the shapes leave unexplained: what their elements mean, and what breaks when one is varied.

### `--add-dir` is a permission grant, not only an anchor

A read is gated by the **headless approval gate**, not by path resolution: `-p` mode cannot prompt, so a `read_file` whose target sits under no grant is auto-denied — `toolPermission` defaults to `request-review`, and headless has no reviewer — and the denial text recommends the forbidden bypass flag. Grant membership is the only thing that decides it. Path shape does not enter into it, and neither does cwd nor a `trustedWorkspaces` root: the settings key that pre-trusts workspace paths was measured against this gate and did not lift it. `allowNonWorkspaceAccess`, whose name claims exactly the power denied here, is **untested headlessly** — nothing establishes that it does or does not lift the gate, so never reach for it in place of a grant.

The anchor role is separate and still holds: a bare relative reference to a tree outside cwd resolves only through the grant.

| Operation | `--add-dir` required? |
| ---- | ---- |
| Read, any path shape | **Yes** — the approval gate |
| Write to an absolute path | No — `agentMode` pre-approves edits ambiently, with no read counterpart |
| Search outside cwd | **Yes** — omitted, the run spirals and times out |
| Search a relative path outside cwd | **Yes** — and resolve the reference to an absolute path first |

Grant a **directory containing** every path the prompt names, whatever the operation — a grant is never a file, however precisely the prompt names one. Vendor reference: <https://antigravity.google/docs/agent-permissions>.

### The no-shell clause is functional, not courteous

Omit it and search *fails*. agy elects a `command` / `run_command` call, headless mode refuses it, and the run ends empty at exit 0. That is the whole reason the clause is a required element of the shape and not a preference.

### stdin is not read

In prompt mode agy reads no stdin, so a pipe into it is silently discarded — hence the capture-and-`@`-reference route the skill's shape section gives. Codex is the opposite: it reads stdin and appends it as a `<stdin>` block.

## Available Tools

agy's **native** tools, all available in headless mode:

| Tool | Description |
| ---- | ---- |
| `read_file` | Read file content (text, images, audio, PDF). Supports `start_line`/`end_line`. |
| `read_many_files` | Multi-file read by glob pattern. Triggered by `@` on a directory. |
| `list_directory` | List directory contents. |
| `glob` | Find files by glob pattern. |
| `grep_search` | Regex search across file contents (ripgrep-powered). |
| `google_web_search` | Grounded Google Search with citations. |
| `web_fetch` | Read and analyze URLs, up to 20. |
| `write_file` | Create or overwrite files. Auto-creates parent directories. Gated — see below. |
| `replace` | Precise text replacement (old_string → new_string) within files. Gated — see below. |

`@`-referenced content is read **before** the prompt is sent and consumes the context window, so reference the narrowest path that answers the question rather than a whole tree. Searching and listing cost nothing up front — `grep_search` / `glob` / `list_directory` reach across a tree without paying for it.

Shell execution is not *unavailable* headlessly, it is **unapprovable**: agy can still elect a `command` / `run_command` call, and headless mode then refuses it, yielding empty stdout and exit 0. This is why the caller handles all shell work itself.

Output is plain text and there is no structured-output mode. Where structured data is wanted, ask for raw JSON in-prompt and parse stdout directly — there is no `.response` envelope to unwrap.

## Write Gate

agy (the Antigravity CLI) does not use gemini's `~/.gemini/policies/*.toml` policy engine. Its config file is **`~/.gemini/antigravity-cli/settings.json`**, and writes are gated by one key in that file and by nothing else. Three similarly-named mechanisms exist; only one works.

- **`agentMode` must be present with the value `accept-edits`.** With it set, agy logs `Accept-edits mode: auto-approving file write` and the write lands. The operator sets it by hand.
- **`--mode` on the command line does nothing.** It is not a substitute for the key; passed with the key absent, the write still fails.
- **`accept-edits` is the only value to use**, and `toolPermission: always-proceed` — the settings key governing confirmation mode — is not a substitute for it.
- **Privileges are ambient.** Nothing on the command line grants or confines them, so *every* run is write-capable whenever the key is set — Case 1 included, which is why "do not modify any file" is worth saying in a read-only prompt. Nothing confines *where* a write lands either, which is why the shape names an exact output path: a run has been seen writing a helper script into agy's own `~/.gemini/antigravity-cli/brain/<uuid>/scratch/`, under no grant covering it. A Case 2 run silently writes nothing without `accept-edits` set.

## The In-Place Bulk-Edit Shape

A third shape, not one of the floor's two: it writes back to the files it read, so there is no output document to check. **The file set is enumerated in the prompt and never discovered** — a discovered set is how a mechanical edit becomes an unbounded one. Verification shifts to a `git diff --stat` over exactly that set, taken before and after; an empty diff is a failure exactly as blank stdout is. The `agentMode` key is a precondition — § Write Gate.

```bash
ROOT=/absolute/path/to/tree
FILES="$ROOT/src/loader.py $ROOT/src/runner.py $ROOT/src/cli.py"   # enumerated, never discovered
DIFF=$ROOT/{analysis-root}/bulk-edit

git -C "$ROOT" diff --stat -- $FILES > "$DIFF.before"
out=$(agy --add-dir "$ROOT" --model {gemini-flash} --print-timeout 8m -p "In these files and no others, rename the function \`load_cfg\` to \`load_config\` at every definition and call site, then summarise briefly what you changed: $FILES

Do NOT use shell commands or the Bash tool; use only your built-in file listing and file reading tools.
Never manipulate a database or a role, and never escalate to a superuser.
Only search and operate within the following path(s): @$ROOT" 2>&1); rc=$?
git -C "$ROOT" diff --stat -- $FILES > "$DIFF.after"

[ -z "$out" ] && echo "agy FAILED (rc=$rc)" >&2
printf '%s\n' "$out" | grep -q '^Error: permission check failed' && echo "agy FAILED: denial in output (rc=$rc)" >&2
cmp -s "$DIFF.before" "$DIFF.after" && echo "agy FAILED: no file changed" >&2
printf '%s\n' "$out"
```

## Exit Codes

The canonical shapes capture `rc=$?` immediately after the call and print it in their failure echo; this table is what that number indexes. The echo itself **does not change the exit status**, so the caller reads the string, not `$?`.

| Code | Meaning |
| ---- | ---- |
| 0 | Success — **or** a headless refusal |
| 1 | General error or API failure, including an invalid `--model` identifier (fails loudly, with a model list on stderr) |
| 42 | Input error (invalid prompt/arguments) |
| 53 | Turn limit exceeded |
| 124 | `timeout` fired — check whether a slow pipeline producer, not agy, held the shell open |
