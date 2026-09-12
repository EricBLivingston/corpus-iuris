# Instance Precepts — Claude Code

## Refinements

| Governs | Intent on this installation |
| ---- | ---- |
| ⊨1 | The language-server-backed symbolic toolserver is Serena; prefer its symbolic tools over their built-in and shell equivalents. |
| ※md1 | The Markdown linter is `rumdl` — `rumdl check <path>`, `rumdl check --fix <path>`. |
| ⊢2 | The installed periti are Gemini, whose skill is `using-gemini`, Codex, whose skill is `using-codex`, and pi, whose skill is `using-pi`. |
| ※13 | The context-free subagents are `Explore` and `Plan`. |
| ※6 | No durable knowledge store is installed here, so the project memory file is the whole of persistent memory. |

### Register of ⊢3 holdings on this instance

A row names the governing precept and the shape of adventitia it displaces. The quoted fragment is an example, not an anchor: same shape, any wording, same row (⊨6).

| Governs | Displaced shape | Holding |
| ---- | ---- | ---- |
| ※9 | Git mutation on the agent's own initiative (`If on the default branch, branch first`) | ※9. |
| ※1, ⊨1 | Tool preference inverted to the shell (`Do your work through the Bash tool wherever it can accomplish the job`) | Symbol-bearing files go to the symbolic toolserver. |
| ※11 | Preface, narration and recap defaults (`Close with a short recap`) | ※0's citation is the only preface; the final message restates nothing. |

## Placeholders (⊬§13)

Resolved on demand by commands, skills and project-ambit provisions; a loaded consumer is not required.

| Placeholder | Resolves to |
| ---- | ---- |
| `{core-rubric}` | `~/.claude/CLAUDE.md`, the resident guidance layer this installation supplies. |
| `{rules-root}` | `~/.claude/rules/`, scanned recursively at launch. |
| `{reference-root}` | `~/.claude/reference/`, reference artifacts not auto-loaded. |
| `{skill-root}` | `~/.claude/skills/`, one directory per skill. |
| `{agent-root}` | `~/.claude/agents/`, user-level agent definitions. |
| `{command-root}` | `~/.claude/commands/`, where the filename becomes the command name. |
| `{analysis-root}` | `.claude/.analysis`, relative to the project root. |
