# Grok Transform

This package is a thin install delta: it sits the shared Corpus Iuris sources next to an existing Grok installation. It ships no replacement for a user's live Grok configuration. `AGENTS.md` beside this file governs work performed inside the transform and is not installed.

Grok already ingests the Claude filesystem dialect when `compat.claude.*` is on (the default): named `CLAUDE.md` files, `~/.claude/rules/`, skills, commands, agents, hooks, MCP. This is not a Codex-style port. There is no `canon.md` and no loader; the root `installing.md` § On Grok states what makes a file resident here.

The corpus sits next to existing content. Do not require edits to files that already exist and have prior content. The adopter's `AGENTS.md` — user or project — is not an install target, not a merge target, and not a prerequisite. The default path does not require an edit to `config.toml`. Setting a `compat.claude.*` cell to `false` is an authorized overlay when a Grok-only copy of that surface is wanted; it is not an install prerequisite. Inspect the cells with `grok inspect` before proposing any such edit, and still obtain authorization.

The only prerequisite is Grok Build. Unlike the Codex transform, this package ships no loader and no Python the adopter runs.

## For an adopting Grok

The root `installing.md` § Three surfaces governs the separation between the working clone, the installed corpus, and the user's live Grok configuration, and the copy steps below run the model it carries.

This repository is designed to guide its own adoption. When a user points Grok at the repository URL, the expected journey is:

1. Obtain a local working copy and read the root `README.md`, `adopting.md`, this file, and `AGENTS.md`.
2. Inspect the live Grok home read-only (`grok inspect`). Identify active configuration layers, `compat.claude.*` cells, existing skills, agents, commands, collisions, and required destinations.
3. Report the proposed bootstrap and ask the user explicitly before writing outside the clone.
4. With approval, the first corpus-owned write is the instance file into `~/.grok/rules/instance.md` (create the directory if needed). Do not create or edit `AGENTS.md` to make the install look complete. Scenario 2 copies nothing corpus-owned into `~/.grok`.
5. Identify which of the three scenarios applies: inspect the `compat.claude.*` cells and what already lives under the Grok home.
6. Install per that scenario, below.
7. Review each selected artifact before copying it.

## Three scenarios

The unit of decision is each `compat.claude.*` cell, not the home.

### 1. No Claude

Copy rules, skills, commands, agents, and reference into the Grok home. `src/instance-example.md` is this shape. Compat cells do not matter.

### 2. Claude, no Grok overlay

Leave `compat.claude.*` at defaults. Load doctrine, skills, instance file, agents, and commands from `~/.claude`. Copy nothing corpus-owned into `~/.grok`. This path is spawn-unsafe for the production chain until transposed agents (and, same posture, commands) are added; at that point it is the thin edge of scenario 3.

### 3. Claude plus Grok overlays

Per cell, not per home. Copy a surface into `~/.grok` only when that cell is off, or when a same-named Grok file must shadow. Leave Claude-only names to fall through.

Worked pattern:

- Rules cell off: full copy in `~/.grok/rules/`, so Grok's `instance.md` is the only instance file and caselaw is not loaded twice.
- Agents and commands cells on: Grok files for names that must differ (the transposed corpus set), Claude files for names that can stand.
- Skills cell on: no Grok skill tree; `{skill-root}` points at `~/.claude/skills/`.
- `{reference-root}` and `{core-rubric}` pointed at the Claude home; `{rules-root}`, `{agent-root}`, `{command-root}`, `{analysis-root}` at the Grok home.

A fourth hybrid exists and is not a default: only `instance.md` in `~/.grok/rules/` with the rules cell still on yields Grok instance plus Claude doctrine, no double caselaw (different filenames), and also loads Claude's `instance.md` beside it (two placeholder tables). The worked pattern turns the rules cell off so that does not happen.

### Discovery

| Surface | Cell | Same-name behavior | When to copy |
| ---- | ---- | ---- | ---- |
| rules | `compat.claude.rules` | every `*.md` in each enabled directory loads, `$GROK_HOME/rules/` then `~/.claude/rules/` if the cell is on; no filename fallback; same name double-injects | cell off, or no Claude |
| agents | `compat.claude.agents` | first-seen: project `.grok/agents`, `~/.grok/agents`, then `~/.claude/agents`; Grok shadows; Claude-only names fall through | cell off, or a same-named Grok file must shadow; transposed agents on any Claude-present install |
| commands | `compat.claude.commands` | discovered as skills (flat `*.md` under `commands/`); inspect lists them as Skills; User scope, `~/.grok` before `~/.claude`; Grok shadows; Claude-only names fall through | same as agents; do not convert commands into skill folders |
| skills | `compat.claude.skills` | name fallback, `~/.grok` first; a skill is `skills/<name>/SKILL.md` | cell off, or a skill that needs a Grok body; scenario 3 may have no `~/.grok/skills/` |
| `CLAUDE.md` | agents cell, not rules | gated on the agents cell | not a copy target |
| reference | none | not a discovery surface; whatever `{reference-root}` names | when `{reference-root}` is `~/.grok/corpus/reference/` (scenario 1); never into `rules/` |

Claude agent `model: opus|sonnet|fable` is a Grok model id and will fail spawn: that is why transposed agents exist on any Claude-present install. Claude command `model:` slugs are a Grok skill-model field; slash invocation currently ignores `SkillInfo.model` (disclosed non-use). Same posture as agents: still transpose.

## Where the pieces go

The copy that fills these runs the model in the root `installing.md`.

| Piece | Destination |
| ---- | ---- |
| the instance file, refactored from `src/instance-example.md` | `~/.grok/rules/instance.md` |
| each definition in `src/agents/` | `~/.grok/agents/` on any Claude-present install and on scenario 1 |
| each skill directory in `skills/` | `~/.grok/skills/<name>/` only for scenario 1, or a skill that needs a Grok body; scenario 3 may have no `~/.grok/skills/` |
| each definition in `src/commands/` | `~/.grok/commands/` on any Claude-present install and on scenario 1 |
| a selected rule | `~/.grok/rules/` when the rules cell is off or there is no Claude (scenario 1) |
| reference material | `~/.grok/corpus/reference/` when `{reference-root}` is that path (scenario 1); Grok does not auto-scan it |

A same-named Grok agent, command, or skill is the intended shadow, not a discovery conflict to skip. A same-named rule file double-loads unless the Claude rules cell is off.

`src/instance-example.md` is scenario 1. For scenario 3, retarget `{skill-root}`, `{reference-root}`, and `{core-rubric}` at the Claude home when those surfaces still load from Claude; keep `{analysis-root}` and the Grok-owned roots on the Grok home.

## Initial scope

The first cut covers the corpus files this repository publishes — the tree as it stands beside this transform is the set, and this file does not restate its membership.

That set's doctrinal core carries rather than being corrected provision by provision. The upstream refactor moved the harness particulars out of those files and into the instance ambit, so what a Grok installation owes them is not a corrected copy but an instance file naming its own referents; this transform ships an example rather than a filled one. Custom-agent definitions are neither deferred nor authored here: they arrive already transposed, per AGENTS.md § What `src/` holds. Skills are native Grok discovery artifacts: copy a directory unchanged to `~/.grok/skills/<name>/` only for scenario 1, or for a skill that actually needs a Grok body. Scenario 3 may have no `~/.grok/skills/` directory. Commands stay commands: they arrive already transposed, per AGENTS.md § What `src/` holds. Every other artifact an admitted source merely names remains a deferred dependency.

## Why the bootstrap is safe

The first authorized corpus-owned write is the instance file into `~/.grok/rules/instance.md`. With only that file present, nouns and keyed notes load; doctrine is not yet admitted. This is the safe initial state, and an artifact copied into a scanned directory later becomes resident at the next matching session start.

## The baseline stands alone

The baseline must work without optional MCP servers, private skills, custom agents, or extra hooks. Serena, the knowledge MCP, and any additional hooks are optional capabilities, each allowed only where its absence has an explicit fallback.

## Grok references

- Project Rules — home `~/.grok/rules/` is always scanned; a named `AGENTS.md` is not this package's target
- Skills
- Subagents — spawn depth is one; a child cannot spawn
- Harness compatibility (`compat.claude`)

## Source provenance

The public transform is authored in a private publish staging tree and promoted into this repository after review. That maintainer publication pipeline is not the adopter's workflow: adopters work from their clone and promote vetted artifacts into their own installed corpus as described above.
