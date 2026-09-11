# Instance Precepts — Grok

## Refinements

| Governs | Intent on this installation |
| ---- | ---- |
| ※7 | The main session reads a skill file Grok has already listed when invoking that skill. Still do not open `agents/` to learn a role: spawn it. |
| ※13 | On this harness, `explore` and `plan` do not inherit the parent system-prompt template or the parent skill listing. They do receive the same discovered instruction files as the primary session, in full. They are the context-free pair: anything turning on §, ※, delegate, or MCP-tool routing that is not already in those files still goes in the spawn prompt. |
| ⊨1 | The language-server-backed symbolic toolserver is the serena MCP tool; prefer its symbolic tools over their built-in and shell equivalents. (Example; may be absent.) |
| ※md1 | The Markdown linter is `rumdl` — `rumdl check <path>` and `rumdl fmt <path>`. |
| ⊢2 | The installed periti are <name>, whose skill is `using-<name>`. |
| ※6 | This harness does not auto-inject MEMORY.md. Grok's own memory store may be enabled separately. Every memory write still goes through the knowledge agent. |

This harness's subagent nesting depth is one: only the top-level session spawns. ※4 already says a child holding the work does it; the ※8 chain is orchestrated from the main session. The main session is the only dispatcher.

## Nouns

Corpus, command, and skill text keep Claude's names. Resolve them here:

| Corpus says | This harness |
| ---- | ---- |
| the Agent tool | `spawn_subagent` |
| the Skill tool | no such tool — open the `SKILL.md` Grok has already listed |
| Read / Edit / Grep / Bash | `read_file` / `search_replace` / `grep` / `run_terminal_command` |
| `SendMessage` | resume a completed child with `spawn_subagent` `resume_from`; this harness has no mid-flight mailbox |
| `TaskStop` | `kill_command_or_subagent` |
| `mcp__<server>__<tool>` | `search_tool`, then `use_tool` with `tool_name` `<server>__<tool>` |
| `agentId` | `subagent_id` |

### Register of ⊢3 holdings on this instance

A row names the governing precept and the shape of adventitia it displaces. The quoted fragment is an example, not an anchor: same shape, any wording, same row (⊨6).

| Governs | Displaced shape | Holding |
| ---- | ---- | ---- |
| ※4, ※8 | Delegation restricted to explicit user requests (`When the user explicitly asks you to use subagents`) | ※4 and ※8 make delegation mandatory. |
| ※11 | `<communication>` restatement / standalone-final-message defaults | ※11. |

## Rubric

| Placeholder | Resolves to |
| ---- | ---- |
| `{core-rubric}` | `~/.grok/rules/`, the user-level rules directory Grok always loads (this instance file sits there once installed). Not the adopter's AGENTS.md. |
| `{rules-root}` | `~/.grok/rules/` |
| `{reference-root}` | `~/.grok/corpus/reference/`, reference artifacts not auto-loaded |
| `{skill-root}` | `~/.grok/skills/` |
| `{agent-root}` | `~/.grok/agents/` |
| `{command-root}` | `~/.grok/commands/` — Grok's slash-command surface; not merged with `{skill-root}` |
| `{analysis-root}` | `.grok/.analysis`, relative to the project root. |
