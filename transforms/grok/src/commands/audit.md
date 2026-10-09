---
description: "Audits a file or folder of the invoking project: descriptive claims against the tree, the target against every precept. Takes one path relative to the project root. Writes under `{analysis-root}/`."
argument-hint: "[path relative to the project root]"
---

# Audit Command

Dispatch the auditor agent over one target of the invoking project. This session's canon is the project's, which the auditor inherits (※13).

## Process

1. Set `{Project Root}` from `pwd`, absolute.
2. Resolve the target: the argument relative to `{Project Root}`, a trailing slash normalized away; abort with a clear message if missing. For a folder, the members are its files.
3. Resolve `{Report}` under `{Project Root}/{analysis-root}/` and create its directory: `<path, extension dropped>-Audit.md` for a file, `<path>/Audit.md` for a folder; no path segment is stripped.
4. Set `{Staging}` to `<session scratchpad>/audit/<path>/`.
5. Report `{Project Root}`, the target and `{Report}`.
6. Invoke `performing-audits` and dispatch the auditor agent with its tree shape.
7. Wait for the summary line (∋3) and route it per `performing-audits`.
