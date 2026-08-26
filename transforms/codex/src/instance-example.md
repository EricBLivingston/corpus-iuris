# Instance Precepts — Dev Box

## Refinements

| Token | Intent on this installation |
| ---- | ---- |
| ※7 | SKILL.md may be read by the main agent when invoking that skill. |
| ※13 | There are no context-free subagents. All subagents receive full context. |
| ⊨1 | The language-server-backed symbolic toolserver is the serena MCP tool; prefer its symbolic tools over their built-in and shell equivalents. |
| ※md1 | The Markdown linter is `rumdl` — `rumdl check <path>` and `rumdl fmt <path>`. |

**⊢3** — Instance-local Adventitia conflict resolution register:

- “Codex may use subagents only when the user explicitly asks for subagents, delegation, workers, parallel agent work, or a workflow whose documented semantics require delegated agents” — ※4 is a workflow that requires delegation as indicated.

**Governs:** adventitia, and ※4.

## Rubric

| Placeholder | Resolves to |
| ---- | ---- |
| `{core-rubric}` | `~/.codex/AGENTS.md`, the always-loaded global guidance file. |
| `{rules-root}` | `~/.codex/corpus/rules/` |
| `{reference-root}` | `~/.codex/corpus/reference/`, reference artifacts not auto-loaded. |
| `{skill-root}` | `~/.agents/skills/`, the user-level skill-discovery root. |
| `{agent-root}` | `~/.codex/agents/`, user-level custom agents. |
| `{command-root}` | `~/.agents/skills/`, shared with `{skill-root}`. Commands resolve to skills. |
