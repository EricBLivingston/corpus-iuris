# Installing This Corpus

`adopting.md` answers which provisions to take and how to key over what does not fit. This file answers the other half: where the files go, and how they get there.

## Three surfaces

The working clone, the installed corpus, and the user's live harness configuration are separate surfaces. An agent must not treat repository presence as installation or admission, and pulling the clone must not change resident context.

The sequence is the same on every harness:

1. **Clone** the repository. Nothing is installed and nothing is admitted; a clone is read.
2. Optionally create a **staging** copy: a fourth surface, disposable, neither the clone nor production, and the one on which local modifications are applied.
3. **Copy** into production, from the clone or from staging.

Production is a live directory its harness writes to continuously (sessions, history, credentials, caches), so it is never a tree that can be replaced wholesale: every install is a merge into something already running. Keep the clone update-managed and free of local artifacts, which are in the way of the next pull.

## When staging earns its keep

Copying straight from the clone is right whenever everything is taken off the shelf unmodified. Modify anything and the clone stops being a shelf: each update either clobbers your modifications, leaving you to redo them before the next copy, or forces a transpose-while-copy through a temporary location to keep the clone clean, which is staging contrived rather than declared.

Declare it instead, and the loop is:

1. Pull the clone.
2. Copy the clone over staging.
3. Diff staging against production.
4. Fold into staging what that diff turned up on the production side: the drift worth keeping, and your own local modifications, which live in production and nowhere else. The instance file is always on that list, since every harness installs it as `rules/instance.md` under its own root and it exists in no upstream tree; nothing carries it across an update but you.
5. Once staging is right, copy it into production in one pass.

The two copies are not the same operation. Staging is rebuilt from the clone every cycle, so step 2 mirrors: a file that left upstream leaves staging with it. Step 5 overlays, because production holds the harness's running state and your own files beside the corpus, and a mirror there would delete both. An upstream removal therefore reaches production through the step 3 diff and because you decided to apply it, never by the copy; and if you skip that decision, a rules file the corpus no longer asserts stays resident indefinitely.

A collision arrives the same way. Where a published file lands on a name you already have, your own `agents/coder.md` or a rules file of your own, step 3 is where it surfaces and staging is where it is settled: fold your version into staging, or rename one of the two, before the copy makes the choice for you.

Staging is the reconciliation surface; production changes in one pass, and only from a tree already read.

## Why not a symlink

Symlinking the clone's directories into production works. On a harness that resolves a symlink while scanning its rules directory, the target loads exactly as a regular file would, and a reader who tries it will find nothing wrong with it.

It is still the wrong shape. A symlinked corpus makes the pull the installation step: an upstream change is in production the moment it lands, resident at the next session start, with nothing between it and the context it enters. Pulling the clone must not change resident context, and under a symlink there is nothing left to hold it back. A copy puts that gate where the staging loop wants it, at a step you run against a diff you have read.

The rejection is about where the gate sits, not about what the filesystem will do.

## On Claude Code

`~/.claude` is Claude Code's own state directory: a merge target, never a checkout. There is no `transforms/claude/` package and none is missing, this being the harness the base is written for, so the destinations are stated here rather than translated.

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

`reference/` is not a discovery surface and never goes inside `rules/`, where it would load resident. Two published rules files reach into it by placeholder, `rules/python.md` and `rules/rust.md` each naming `{reference-root}` as where their lingua's principles live, so a `reference/` tree landing anywhere the instance file does not name leaves those citations resolving to nothing.

Presence in `~/.claude/rules/` is the whole mechanism: a `.md` file placed there is resident at the next session start whether or not anyone has read it, and nothing intervenes. `paths` frontmatter is the one thing that changes that, making a file conditional rather than resident: it loads only against a file the globs it names match, yours no less than ours. The lingua triggers are the published rules files that carry it, which is why the Python and Rust principles pointers stay silent until a file of that language is open; everything else the corpus publishes into that directory is resident on arrival.

Staging bites hardest where the copy is the activation. Nothing downstream of it will stop a change, so staging is the only surface on which one can be seen before it is resident.

### What you supply

Two files are yours to write, and neither is published:

- `~/.claude/rules/instance.md`, refactored from `instance-example.md`. Decide its content first, per `adopting.md` § Write your instance file first, and write it into `~/.claude/rules/` after the corpus is copied rather than before it: written after, it is independent of whether the copy landing on that directory overlays or mirrors. It resolves the placeholders the published tree consumes, and until it is in place they name nothing.
- `~/.claude/CLAUDE.md`. What sits there is the resident guidance layer of one installation, pinned to its own shims, paths and scripts, so the corpus publishes none. Every rules file installs and loads without it; `{core-rubric}` then names a file that does not exist.

## On Codex

Codex auto-loads no rules directory, so copying into the production corpus root makes nothing resident. An artifact becomes resident when `canon.md` imports it, and the SessionStart loader the package ships reads that file to learn what to pull into a session; a file the list does not name is not injected. That follows from how the loader finds its inputs rather than from a gate designed as one, so nothing on another harness should be modelled on it.

The gate therefore sits one step past the copy, at an edit made deliberately against a file you can read. Staging still earns its keep wherever the loop above describes your situation, but it is no longer the only thing standing between an upstream change and resident context.

`transforms/codex/README.md` carries the rest: installing and registering the loader, the roots it resolves, the order admission runs in, and the Codex destination for each published piece.

## On Grok

Grok scans its rules directories itself, so residency is directory membership: a file in a directory the scanner reaches is resident at the next session start, and the copy is the activation exactly as on Claude Code. Which directories those are is what the `compat.claude.*` cells decide, so on a machine running both harnesses one copy can be resident on each.

Staging carries the same weight here as it does on Claude Code, and for the same reason: nothing downstream of the copy will hold a change back.

`transforms/grok/README.md` carries the rest: the cells and the scenarios they select, the shadowing rules where a name exists on both harnesses, the discovery paths, and the Grok destination for each published piece.
