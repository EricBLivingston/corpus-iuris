# Grok Transform

This package is a thin install delta: it sits the shared Corpus Iuris sources next to an existing Grok installation. It ships no replacement for a user's live Grok configuration. `AGENTS.md` beside this file governs work performed inside the transform and is not installed.

Grok already ingests the Claude filesystem dialect when `compat.claude.*` is on (the default): named `CLAUDE.md` files, `~/.claude/rules/`, skills, commands, agents, hooks, MCP. This is not a Codex-style port. There is no `canon.md` and no loader. Admission is directory membership: a file Grok's rules scanner will load is admitted; a file left in the clone is not.

The corpus sits next to existing content. Do not require edits to files that already exist and have prior content. The adopter's `AGENTS.md` — user or project — is not an install target, not a merge target, and not a prerequisite. The same posture holds for `config.toml`: do not require an edit.

The only prerequisite is Grok Build. Unlike the Codex transform, this package ships no loader and no Python the adopter runs.

## For an adopting Grok

This repository is designed to guide its own adoption. When a user points Grok at the repository URL, the expected journey is:

1. Obtain a local working copy and read the root `README.md`, `adopting.md`, this file, and `AGENTS.md`.
2. Inspect the live Grok home read-only (`grok inspect`). Identify active configuration layers, existing skills, agents, commands, collisions, and required destinations.
3. Report the proposed bootstrap and ask the user explicitly before writing outside the clone.
4. With approval, the first corpus-owned write is the instance file into `~/.grok/rules/instance.md` (create the directory if needed). Do not create or edit `AGENTS.md` to make the install look complete.
5. Choose dual-home or Grok-only, below.
6. Admit rules by copying selected files into `~/.grok/rules/` (Grok-only). Dual-home does not recopy rules already loaded from `~/.claude/rules/`.
7. Install transposed agents, and on the Grok-only path skills and commands, reviewing each first.

The working clone, the installed corpus, and the user's live Grok configuration are separate surfaces. An agent must not treat repository presence as installation or admission, and pulling the clone must not change resident context.

## Dual-home

Claude Code is already installed and the corpus already lives in `~/.claude`. Grok compat will load those rules, skills, and commands. Install only:

- the refactored instance file into `~/.grok/rules/instance.md`, so Grok-particular rows do not land in the Claude instance file
- transposed agents into `~/.grok/agents/`, so they shadow `~/.claude/agents/` (Grok user-level `.grok/agents` outranks `.claude/agents`)

Claude agent `model: opus|sonnet|fable` is a Grok model override and will fail spawn; that is why the transposition exists even for dual-home.

## Grok-only

Copy selected `rules/` files into `~/.grok/rules/` (admission), skills into `~/.grok/skills/<name>/`, commands into `~/.grok/commands/` as flat markdown (Grok's native slash-command surface — do not convert commands into skill folders), transposed agents into `~/.grok/agents/`, and the instance file into `~/.grok/rules/instance.md`. Reference material goes to a path Grok does not auto-scan: `~/.grok/corpus/reference/`. Do not dump reference into `rules/` or it becomes always-loaded.

## Where the pieces go

| Piece | Destination |
| ---- | ---- |
| the instance file, refactored from `src/instance-example.md` | `~/.grok/rules/instance.md` |
| each definition in `src/agents/` | `~/.grok/agents/` |
| each skill directory in `skills/` | `~/.grok/skills/<name>/` on the Grok-only path; dual-home already loads `~/.claude/skills/` |
| each `<name>.md` in `commands/` | `~/.grok/commands/<name>.md` on the Grok-only path, Claude `model` slug dropped; dual-home already loads `~/.claude/commands/` |
| a selected rule | `~/.grok/rules/` on the Grok-only path; dual-home already loads `~/.claude/rules/` |
| reference material | `~/.grok/corpus/reference/`, which Grok does not auto-scan |
| an admission | membership in a directory Grok's rules scanner loads |

Skill, agent, and command name collisions are discovery conflicts: inspect, report, skip or add a new directory; do not patch the occupant.

## Initial scope

The first cut covers the corpus files this repository publishes — the tree as it stands beside this transform is the set, and this file does not restate its membership.

That set's doctrinal core carries rather than being corrected provision by provision. The upstream refactor moved the harness particulars out of those files and into the instance ambit, so what a Grok installation owes them is not a corrected copy but an instance file naming its own referents; this transform ships an example rather than a filled one. Custom-agent definitions are neither deferred nor authored here: they arrive already transposed, per AGENTS.md § What `src/` holds. Skills are native Grok discovery artifacts: an installation that selects one copies its directory unchanged to `~/.grok/skills/<name>/`. Commands stay commands: an installation that selects one copies the markdown file to `~/.grok/commands/`, dropping a Claude `model` slug if present. Every other artifact an admitted source merely names remains a deferred dependency.

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
