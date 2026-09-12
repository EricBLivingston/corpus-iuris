# Installing This Corpus

`adopting.md` addresses which provisions to take and how to key over what doesn't fit your environment. This file addresses where the files go, and how they get there.

## The installation sequence

The installation (or update) involves three file trees:

- **repository clone**, read and pulled and never modified;
- **staging**, the working area where local modifications live and where reconciliation happens;
- **production**, the harness's own configuration root.

These locations are used in the following sequence:

1. Pull the clone.
2. Mirror the clone to staging.
3. Diff staging against production.
4. Fold into staging what that diff turned up on the production side: the drift worth keeping, and your own local modifications.
5. Once staging is correct, copy it into production in one pass.

The clone isn't modified locally so the next pull is non-destructive. Staging is the area where changes are made that affect neither the repo, nor production, and thus is the safe place to reconcile differences before they reach the live environment. Production comprises the folders and files the harness auto-loads with each session; thus, changes there are immediate and persistent.

## Why not a symlink

A symlinked corpus file makes the pull the installation step: an upstream change is in production the moment it lands, resident at the next session start, with nothing between it and the context it enters.

## On Claude Code

`~/.claude` is Claude Code's own state directory: a merge target, never a checkout. There is no `transforms/claude/` package, this being the harness the base is written for.

| Piece | Destination |
| ---- | ---- |
| each `*.md` in `rules/` | `~/.claude/rules/` |
| each `*.md` in `agents/` | `~/.claude/agents/` |
| each `*.md` in `commands/` | `~/.claude/commands/` |
| each skill directory in `skills/` | `~/.claude/skills/<name>/`, `SKILL.md` and its peer files kept together |
| `reference/`, whole | wherever your instance file's `{reference-root}` names |
| the instance file, refactored from `instance-example.md` | `~/.claude/rules/instance.md` |
| `docs/` | read in the clone; installed nowhere |
| `transforms/` | not an install target on this harness; the packages carry other harnesses |
| the root documents | read in the clone; installed nowhere |
| an admission | placing the file in the directory above; the copy is itself the activation |

`reference/` is not a discovery surface and never goes inside `rules/`, where it would load resident. It is meant as an area for on-demand, progressive-disclosure supporting material.

### What you supply

The main editing role during installation or update is that of curating `~/.claude/rules/instance.md`, refactored from `instance-example.md`. Decide its content first, per `adopting.md`. Once written, place it into `~/.claude/rules/` where it resolves the placeholders the published tree consumes, as well as providing instance-specific overrides for provisions that require customization.

## On Codex

Codex auto-loads no rules directory. An artifact becomes resident when `canon.md` authorizes its import, and the SessionStart loader the package ships reads that file to learn what to pull into a session.

See `transforms/codex/README.md` for the rest: installing and registering the loader, the roots it resolves, the order admission runs in, and the Codex destination for each published piece.

## On Grok

Grok scans its own folders and those of Claude, depending on how the various `compat.claude.*` settings are configured. Curate those settings and the file placement together, so that the intended files are resident and each is loaded once.

See `transforms/grok/README.md` for the rest: the cells and the scenarios they select, the shadowing rules where a name exists on both harnesses, the discovery paths, and the Grok destination for each published piece.
