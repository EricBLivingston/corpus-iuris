---
description: "Builds from one implementation plan by driving the analyze, code, review, test cycle until review passes and tests are green. Takes a single plan file, or a plan already in the conversation. Use for an unphased plan; a folder of Overview plus phase files goes to orchestrate."
argument-hint: "[plan-file]"
model: opus
---

# Implement Command

Execute an implementation plan through the `writing-code` skill.

## Workflow

1. **Establish Plan**
   - Read the plan file if provided, or use conversation context
   - Set `{Plan Folder}` = absolute path of the directory containing the plan file
   - A conversation-borne plan has no such directory: ask the user for the destination folder and confirm it before proceeding

2. **Execute the plan via the `writing-code` skill**

   Notes:

   - The coder must update the plan file's Deviations section before invoking the reviewer.
   - The reviewer also verifies Deviations was filled and that ACs have verifier hints.
   - The tester's verification includes the §16 cross-boundary end-to-end gate wherever the plan's work crosses a boundary.
   - `governing-work` documents when holding the produced work to the plan's remit earns a governor dispatch, and the routing of its verdict.

3. **Completion Report**

   Write the implementation report to `{Plan Folder}/Phase-N-Implementation-Report.md` when the plan file is `Phase-N.md`, else `{Plan Folder}/Implementation-Report.md`. Include:

   - Files modified/created with brief descriptions
   - Confirmation all plan items completed
   - Deviations from plan (with justification)
   - Test results and coverage metrics (if available)
   - Suggested next steps
   - Known issues or technical debt introduced
