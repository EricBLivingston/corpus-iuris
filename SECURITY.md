# Security

Most of this repository is prose, which carries no execution risk of its own. One thing here does.

## What executes

`transforms/codex/src/hooks/corpus_iuris_session_start.py` is installed as a Codex session-start hook, which means it runs inside your session, on your machine, at your privilege, every time a session begins. It reads your global and project entrypoints, walks their `@import` graph, and injects the result into the session's context. It is fail-closed by design: the loader injects nothing rather than injecting part of the canon.

## Supported versions

The tip of the default branch, and nothing else. §1 governs: there are no release branches, no back-ports, and no security patches to an earlier state of the corpus. If you are pinned to a commit, the remedy for a defect is to move to the tip.

## Reporting

Please do not open a public issue for anything that would give a working exploit to a reader before the fix lands. Anything else — a hook that refuses valid canon, a loader that is merely wrong — is an ordinary defect and belongs in an issue.

Expect a slow reply. This is maintained in the margins of other work, there is no team behind it, and there is no disclosure deadline I can honestly promise to meet.
