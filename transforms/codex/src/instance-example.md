# Instance Precepts — Dev Box

## Refinements

| Token | Intent on this installation |
| ---- | ---- |
| ※7 | `SKILL.md` may be read by the main agent when invoking that skill. |
| ※13 | There are no context-free subagents. All subagents receive full context. |
| ⊢2 | The periti are Gemini, whose skill is `using-gemini`, and Pi, whose skill is `using-pi`. ('Pi' proxies the called model) |
| ⊨1 | The language-server-backed symbolic toolserver is Serena; prefer its symbolic tools over their built-in and shell equivalents. |
| ※md1 | The Markdown linter is `rumdl` — `rumdl check <path>` and `rumdl fmt <path>`. |

### Register of ⊢3 holdings on this instance

A row names the governing precept and the shape of adventitia it displaces. The quoted fragment is an example, not an anchor: same shape, any wording, same row (⊨6).

| Governs | Displaced shape | Holding |
| ---- | ---- | ---- |
| ※4, ※8 | Delegation restricted to explicit user requests or instructions requiring it (`Do not spawn sub-agents unless the user or applicable AGENTS.md/skill instructions explicitly ask for sub-agents, delegation, or parallel agent work`) | ※4 and ※8 require delegation, sized under ⊨5. |

## Placeholders (⊬§13)

Resolved on demand by commands, skills and project-ambit provisions; a loaded consumer is not required.

| Placeholder | Resolves to |
| ---- | ---- |
| `{core-rubric}` | `~/.codex/AGENTS.md`, the always-loaded global guidance file. |
| `{rules-root}` | `~/.codex/corpus/rules/` |
| `{reference-root}` | `~/.codex/corpus/reference/`, reference artifacts not auto-loaded. |
| `{skill-root}` | `~/.codex/skills/`, the user-level skill-discovery root. |
| `{agent-root}` | `~/.codex/agents/`, user-level custom agents. |
| `{command-root}` | `~/.codex/skills/`, shared with `{skill-root}`. Commands resolve to skills. |
| `{analysis-root}` | `.codex/.analysis`, relative to the project root. |
