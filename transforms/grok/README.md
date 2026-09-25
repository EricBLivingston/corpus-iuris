# Grok Transform

This package installs the shared Corpus Iuris sources beside an existing Grok configuration and does not replace that configuration. The only prerequisite is Grok Build. There is no `canon.md`, no loader, and no Python the adopter runs. The root `installing.md` § On Grok states what makes a file resident. `AGENTS.md` beside this file is the discipline for work inside the transform and is not installed.

When `compat.claude.*` is on (the default), Grok ingests named `CLAUDE.md` files, `~/.claude/rules/`, skills, commands, agents, hooks, and MCP. § Discovery states the cells and the copy rules.

Do not require edits to files that already exist and have prior content. Do not treat the adopter's `AGENTS.md` (user or project) as an install target, a merge target, or a prerequisite. Do not create or edit one to make the install look complete. The default path requires no edit to `config.toml`. Setting a `compat.claude.*` cell to `false` is an authorized overlay when a Grok-only copy of that surface is wanted. That overlay is not required to install. Inspect the cells with `grok inspect` before proposing that edit. Obtain authorization.

## For an adopting Grok

The root `installing.md` § The installation sequence states the separation between the working clone, the installed corpus, and the user's live Grok configuration. The copy steps below run the model in that section. When a user points Grok at the repository URL:

1. Obtain a local working copy and read the root `README.md`, `adopting.md`, this file, and `AGENTS.md`.
2. Inspect the live Grok home read-only (`grok inspect`). Identify active configuration layers, `compat.claude.*` cells, existing skills, agents, commands, collisions, and required destinations.
3. Report the proposed bootstrap and ask the user explicitly before writing outside the clone.
4. With approval, the first corpus-owned write is the instance file into `~/.grok/rules/instance.md` (create the directory if needed). Do not create or edit `AGENTS.md` to make the install look complete. Scenario 2 copies nothing corpus-owned into `~/.grok`.
5. Identify which of the three scenarios applies from the `compat.claude.*` cells and what already lives under the Grok home.
6. Install per that scenario.
7. Review each selected artifact before copying it.

After the first write, with only that instance file present, nouns and keyed notes load, and doctrine is not yet admitted. An artifact copied into a scanned directory later becomes resident at the next matching session start.

## Three scenarios

The unit of decision is each `compat.claude.*` cell.

### 1. No Claude

Copy rules, skills, commands, agents, and reference into the Grok home. `src/instance-example.md` is this shape. Compat cells do not matter.

### 2. Claude, no Grok overlay

Leave `compat.claude.*` at the defaults. Load doctrine, skills, the instance file, agents, and commands from `~/.claude`. Copy nothing corpus-owned into `~/.grok`. This path is spawn-unsafe for the production chain until transposed agents (and, same posture, commands) are added; it is then the thin edge of scenario 3.

### 3. Claude plus Grok overlays

Copy a surface into `~/.grok` only when that cell is off, or when a same-named Grok file must shadow. Leave Claude-only names to fall through.

- Rules cell off: full copy in `~/.grok/rules/`, so Grok's `instance.md` is the only instance file and caselaw is not loaded twice.
- Agents and commands cells on: Grok files for names that must differ (the transposed corpus set); Claude files for names that can stand.
- Skills cell on: no Grok skill tree; `{skill-root}` is `~/.claude/skills/`.
- `{reference-root}` and `{core-rubric}` point at the Claude home; `{rules-root}`, `{agent-root}`, `{command-root}`, and `{analysis-root}` point at the Grok home.

A fourth hybrid is not a default. Only `instance.md` in `~/.grok/rules/`, with the rules cell still on, loads the Grok instance file plus Claude doctrine. Caselaw is not doubled (different filenames). Claude's `instance.md` loads beside it (two placeholder tables). The worked pattern turns the rules cell off so that hybrid does not occur.

### Discovery

Home `~/.grok/rules/` is always scanned. Subagent spawn depth is one: a child cannot spawn.

| Surface | Cell | Same-name behavior | When to copy |
| ---- | ---- | ---- | ---- |
| rules | `compat.claude.rules` | every `*.md` in each enabled directory loads, `$GROK_HOME/rules/` then `~/.claude/rules/` if the cell is on; no filename fallback; same name double-injects | cell off, or no Claude |
| agents | `compat.claude.agents` | first-seen: project `.grok/agents`, `~/.grok/agents`, then `~/.claude/agents`; Grok shadows; Claude-only names fall through | cell off, or a same-named Grok file must shadow; transposed agents on any Claude-present install |
| commands | `compat.claude.commands` | discovered as skills (flat `*.md` under `commands/`); inspect lists them as Skills; User scope, `~/.grok` before `~/.claude`; Grok shadows; Claude-only names fall through | same as agents; do not convert commands into skill folders |
| skills | `compat.claude.skills` | name fallback, `~/.grok` first; a skill is `skills/<name>/SKILL.md` | cell off, or a skill that needs a Grok body; scenario 3 may have no `~/.grok/skills/` |
| `CLAUDE.md` | agents cell. The rules cell does not gate it | gated on the agents cell | do not copy |
| reference | none | not a discovery surface; whatever `{reference-root}` names | when `{reference-root}` is `~/.grok/corpus/reference/` (scenario 1); never into `rules/` |

Claude agent `model: opus|sonnet|fable` is a Grok model id and fails spawn, which is why transposed agents are installed on any Claude-present install. Claude command `model:` slugs are a Grok skill-model field. Transpose commands on the same posture as agents (slash invocation currently ignores `SkillInfo.model`; disclosed non-use).

## Where the pieces go

| Piece | Destination |
| ---- | ---- |
| the instance file, refactored from `src/instance-example.md` | `~/.grok/rules/instance.md` |
| each definition in `src/agents/` | `~/.grok/agents/` on any Claude-present install and on scenario 1 |
| each skill directory in `skills/` | `~/.grok/skills/<name>/`, unchanged, only for scenario 1 or a skill that needs a Grok body. Scenario 3 may have no `~/.grok/skills/` |
| each definition in `src/commands/` | `~/.grok/commands/` on any Claude-present install and on scenario 1 |
| a selected rule | `~/.grok/rules/` when the rules cell is off or there is no Claude (scenario 1) |
| reference material | `~/.grok/corpus/reference/` when `{reference-root}` is that path (scenario 1); do not copy it there if `{reference-root}` already names the Claude reference tree. Grok does not auto-scan it |

A same-named Grok agent, command, or skill is the intended shadow. Do not skip it as a discovery conflict. A same-named rule file double-loads unless the Claude rules cell is off.

`src/instance-example.md` is scenario 1. For scenario 3, retarget `{skill-root}`, `{reference-root}`, and `{core-rubric}` at the Claude home when those surfaces still load from Claude; keep `{analysis-root}` and the Grok-owned roots on the Grok home.

## Initial scope

The first cut is the corpus files this repository publishes: the tree as it stands beside this transform. This file does not list that set again.

The doctrinal core is copied as it stands. Do not correct it provision by provision. The upstream refactor moved the harness particulars out of those files and into the instance ambit, so the instance file names this installation's referents. `src/instance-example.md` is an unfilled example of that file. Custom-agent definitions are already transposed, per AGENTS.md § What `src/` holds. Do not defer them and do not author them here. Commands stay commands: they are already transposed, per the same section. Skills are native Grok discovery artifacts, copied unchanged only for scenario 1 or for a skill that needs a Grok body. Every other artifact an admitted source merely names is a deferred dependency.

## The baseline stands alone

The baseline must work without optional MCP servers, private skills, custom agents, or extra hooks. Serena, the knowledge MCP, and any additional hooks are optional capabilities, each allowed only where its absence has an explicit fallback.

## Source provenance

The public transform is authored in a private publish staging tree and promoted into this repository after review. Adopters do not run that pipeline. They work from their clone and promote vetted artifacts into their own installed corpus.
