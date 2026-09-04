---
description: Builds from one implementation plan by driving the analyze, code, review, test cycle until review passes and tests are green. Takes a single plan file, or a plan already in the conversation. Use for an unphased plan; a folder of Overview plus phase files goes to orchestrate.
argument-hint: "[plan-file]"
---

# Implement Command

Execute an implementation plan through the `writing-code` skill.

## Workflow

1. **Establish Plan**
   - Read the plan file if provided, or use conversation context
   - Set `{Plan Folder}` = absolute path of the directory containing the plan file
   - If the plan is conversation-borne, there is no such directory: ask the user for the destination folder and confirm it before proceeding past this step

2. **Execute the plan via the `writing-code` skill**

   Additional Notes:

   - The coder must update the plan file's Deviations section before invoking the reviewer.
   - The reviewer also verifies Deviations was filled and that ACs have verifier hints.
   - The tester's verification includes the §16 cross-boundary end-to-end gate wherever the plan's work crosses a boundary.
   - Where the plan carries a `## Governance Bounds` section, `governing-work` carries the gate over it and the routing of its return.

3. **Completion Report**

   Write the implementation report to `{Plan Folder}/Phase-N-Implementation.md`, where `N` is the phase number just completed — or to `{Plan Folder}/Implementation.md` when the plan is unphased. Include:

   - Files modified/created with brief descriptions
   - Confirmation all plan items completed
   - Deviations from plan (with justification)
   - Test results and coverage metrics (if available)
   - Suggested next steps
   - Known issues or technical debt introduced
