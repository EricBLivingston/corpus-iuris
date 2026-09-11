# Contributing

This is one person's corpus, published as a worked example rather than as a project seeking contributors. Suggestions are welcome, but adoption depends on their fit into my own ecosystem.

## Issues are open

Open one for anything that is wrong on its own terms rather than wrong by preference:

- A citation that resolves to nothing: a provision token with no defining site in the published set, or a cross-reference into a file that was never published.
- A broken link, a dead path, a filename that no longer exists.
- A defect in a harness transform: its loader, its transposition, or the adoption sequence in its `README.md`.
- A factual error in the references table at [`docs/references.md`](docs/references.md): a work misattributed, a claim the cited paper does not support, an arXiv identifier pointing somewhere else.

## What earns a new provision

`doctrine` was chosen over every synonym for one reason, given in [the lexicon](docs/lexicon.md): it is built from experience rather than reasoned out in advance. Every provision here is the remediation of a failure I actually observed.

If you have experienced a similar deficiency and have worked out a remediating provision, please send it. A case where a model reliably did the wrong thing, and a precept that reliably stopped it, is worth an issue, and it is the only kind of contribution likely to be adopted. Show what the model did, how often, and what changed once the precept was in place. If it reproduces locally it probably becomes a provision.

For such a case, an issue is enough; the fix is small and belongs in one hand. If you would rather show than describe, a patch pasted into the issue is welcome.

Anything sent through a patch pasted into an issue, or a pull request, is offered under the repository's own license, CC BY-SA 4.0; there is no separate contributor agreement to sign.
