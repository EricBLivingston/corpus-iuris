---
name: performing-audits
description: "Use this skill to audit work already done: a run of delegates against their session logs, or a file or folder against canon."
---

# Performing audits

The judgement is the auditor agent's own; a dispatch supplies the inputs.

## The package

Work already done is documented in the harness's session logs of the delegates' executions. The dispatcher passes the run's selector (the dispatch label), and the auditor selects the logs that carry it and their descendants. A log of requests (e.g. a permission hook's) is no record of execution.

| Role | Run audit | Tree audit |
| ---- | ---- | ---- |
| Work | The plan files that defined the work | The target's files |
| Record | The logs the selector selects, and each record a report cites (a peritus responsum, a log under `tests/`) | The repository as it stands |
| Reports | The delegates' report files | Every descriptive claim whose site or subject lies in the target: the target's own, and canon's |
| Q2 reach | Conduct | Product |

## Invoking the auditor

Filled with absolute paths.

Run shape:

```text
Audit the reports below. Q1 over the reports against the record; Q2 over conduct. Write the report to {report path}, stage scratch under {staging directory}, and return the summary line alone.

Work: {plan files that defined the work}
Record: {the run's selector, or one delegate's log; each with its descendants and cited records}
Reports: {the delegates' report files}
Reach: conduct
```

Tree shape:

```text
Audit the target below. Q1 over the descriptive claims sited in or about it (a frontmatter `description` is a claim about its body), against the tree; Q2 over the target against every precept. Write the report to {report path}, stage scratch under {staging directory}, and return the summary line alone.

Work: {the target's members}
Record: {project root}
Reach: product
```

## Handling the summary line

No line halts anything. The dispatcher relays each line verbatim and marks a malformed one.

- A run dispatcher collects every line before its final summary or failure report, reads no audit file, and confirms each audit file on disk by directory listing (※3).
- Where an audit file is on disk but no line arrived, ask its auditor for the line once; a second silence is relayed as `no line returned`. No file on disk means the audit is still running.
- A tree dispatcher replies with the line and the report path.
- Every finding reaches triage under its ID.
