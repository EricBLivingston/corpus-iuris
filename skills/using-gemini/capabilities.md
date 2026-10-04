# Agy CLI Capabilities Reference

Headless `agy -p` mechanics for the using-gemini skill.

## Shape Semantics

### `--add-dir` is a permission grant

The read gate is `toolPermission`, which defaults to `request-review`; headless mode has no reviewer, so grant membership alone decides a read. `trustedWorkspaces` was measured against this gate and does not lift it. `allowNonWorkspaceAccess` is untested headlessly; never substitute it for a grant.

| Operation | `--add-dir` required? |
| ---- | ---- |
| Read, any path shape | **Yes** — the approval gate |
| Write to an absolute path | No — `agentMode` pre-approves edits ambiently, with no read counterpart |
| Search outside cwd, on an absolute path | **Yes** — omitted, the run spirals and times out |

Vendor reference: <https://antigravity.google/docs/agent-permissions>.

### The no-shell clause is functional

Shell execution is unapprovable headlessly. Without the clause, agy elects a `command` / `run_command` call to search, headless mode refuses it, and the run ends at exit 0 with no answer; the caller does all shell work itself.

## Available Tools

Search and listing are native tools, which run headlessly. `@`-referenced content, a directory's whole tree included, is read before the prompt is sent and consumes the context window: reference the narrowest path that answers, and let agy search the rest.

Output is plain text, with no structured mode and no envelope: for data, ask for raw JSON in-prompt and parse stdout.

## Write Gate

agy (the Antigravity CLI) ignores the retired `gemini` CLI's `~/.gemini/policies/*.toml`. Its config file is **`~/.gemini/antigravity-cli/settings.json`**, and one key there gates writes.

- **`agentMode` must be present with the value `accept-edits`.** agy then logs `Accept-edits mode: auto-approving file write` and the write lands; `write_file` creates parent directories. The operator sets the key by hand.
- **`--mode` on the command line does nothing**: with the key absent, the write still fails.
- **`toolPermission: always-proceed` does not substitute** for `accept-edits`.
- **Privileges are ambient.** With the key set, every run is write-capable, Case 1 included, and nothing confines where a write lands, a directory outside every grant included.

## Exit Codes

agy exits 0 on a refusal, so a shape's failure echo, not `$?`, is the signal.

| Code | Meaning |
| ---- | ---- |
| 0 | Success — **or** a headless refusal |
| 1 | General error or API failure, an invalid `--model` identifier included (stderr lists the models) |
| 42 | Input error (invalid prompt/arguments) |
| 53 | Turn limit exceeded |
| 124 | `timeout` fired |
