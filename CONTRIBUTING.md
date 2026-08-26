# Contributing

This is one person's corpus, published as a worked example rather than as a project seeking contributors. Suggestions are welcome, but adoption is dependent on their fit into my own ecosystem.

## Issues are open

Open one for anything that is wrong on its own terms rather than wrong by preference:

- A citation that resolves to nothing — a `§`, `※`, `⊢` or `⊨` token with no defining site in the published set, or a cross-reference into a file that was never published.
- A broken link, a dead path, a filename that no longer exists.
- A defect in the Codex transform: the session-start hook, the agent transposition, or the adoption sequence in `transforms/codex/README.md`.
- A factual error in the README's References table — a work misattributed, a claim the cited paper does not support, an arXiv identifier pointing somewhere else.

## What earns a new provision

`doctrine` was chosen over every synonym for one reason, indicated in the README: it's built from experience rather than reasoned out in advance. Every provision here is the remediation of a failure that was actually observed in my own experience.

If you've experience a similar deficiency and have worked out a remediating provision, please send it. A case where a model reliably did the wrong thing, and a precept that reliably stopped it, is worth an issue, and it is the only kind of contribution likely to be adopted. Show what the model did, how often, and what changed once the precept was in place. If it reproduces locally it probably becomes a provision.

For such a defect, an issue is enough; the fix is small and belongs in one hand. If you would rather show than describe, a patch pasted into the issue is welcome.

Anything sent through a patch pasted into an issue, or a pull request, is offered under the repository's own licence, CC BY-SA 4.0; there is no separate contributor agreement to sign.
