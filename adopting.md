# Adopting This Corpus

**Register.** The corpus binds: once a provision is in your corpus it is a provision there. This
file is different — it is guidance on a process we do not run and cannot see, so everything below
is a recommendation with its reasoning attached, and the decision is yours.

## If you are on Claude Code

Take it as it stands. The content here was written for the Claude Code harness, and most should work out of the box, with tweaks made in the local instance.md file.

## If you are on another harness

Look for a `transforms/<harness>/` package that matches your harness. One means there is no translating left to do: the base is already generic wherever a harness particular would go, and the package carries that harness's own artifacts and the sequence for installing them, so what remains is § Write your instance file first and the decisions below. With no matching package you can still adopt the corpus, but the harness-specific provisions are yours to translate.

## Write your instance file first

The base is generic wherever no concrete name would be true of every installation. Wherever a provision turns on a name only your installation can supply, it names the *kind* of referent and stops there. Those are not gaps in the publication; they are the slots the instance ambit exists to fill, and until you fill them the provisions that turn on them have no referent on your installation.

`instance-example.md` is a platform-specific base example. Copy it, and refactor as necessary:

```md
| ⊨1 | The symbolic toolserver here is <name>; prefer its symbolic tools over their built-in and shell equivalents. |
| ※md1 | The Markdown linter is <name> — `<check invocation>`, `<fix invocation>`. |
```

Everything below is about deciding one provision at a time. That file is the mechanism nearly all of those decisions use.

## Taking a provision you do not want as written

Each way below is valid, and they differ in cost and in what they leave behind rather than in legitimacy. The keyed routes keep it resolving to the same provision on both sides, omitting vacates it, and replacing what you omitted forks it.

| Strategy | Root corpus | Instance ambit | Best for |
| ---- | ---- | ---- | ---- |
| **Key over** | provision stays as published | one keyed entry replacing what conflicts | anything from a narrowing to a wholesale rewrite, as long as it still answers the question the original asked |
| **Key over to disable** | provision stays as published | one keyed entry disabling it | a provision your environment contradicts outright, where the number should stay resolvable |
| **Omit** | provision removed, number left vacant | nothing | a provision with no subject here at all, and no replacement |
| **Omit and replace** | provision removed | the replacement, minted whole | a replacement with nothing left of the original to reconcile |

**Key over** is the mechanism the ius is built around: a keyed entry *overlays* its base rather than displacing it, so it scales from the smallest tweak to a wholesale rewrite without changing form, with no root omission and no forked number. Whatever you do not restate stays live and keeps merging with our revisions, and the token resolves to the same provision on both sides — which is what the citation-resolution argument below asks for. It costs one row of resident context.

**Key over to disable** is that same entry saying the base does not bind here. The number stays resolvable, and resolving it tells a reader the absence was decided rather than overlooked — which is the record § Keeping a record otherwise asks you to keep by hand.

**Omit** is for a provision with no subject on your installation at all — not merely a different subject, which is what keying over is for.

**Omit and replace** gives you a full replacement at zero residual cost in root — but it **forks that provision**. If we later revise it in a way you would have wanted, taking that revision is manual work and nothing will tell you it happened. How much that matters depends on how closely you expect to track us. Prefer keying over wherever your replacement still answers the question the original was asking.

## What we recommend, and why

**Key over in your instance file wherever the provision still has a subject here. Where it has none, go sparse in root — skip it, leave the gap, do not renumber — and mint fresh from `I1`.**

The reason is citation resolution, not tidiness. A global token is worth having only if it means the
same provision in your corpus and in ours; that is what lets a provision be cited in a document that
travels between them. Renumber root to close a gap and your `※5` stops being our `※5`. The failure
is silent: a citation to a removed provision fails loudly and gets noticed, while a citation that
resolves to a *different* provision because the numbers shifted underneath it does not. A dead link
announces itself; a live link to the wrong target does not.

Root moving underneath you is the one case where that failure is not silent. Our numbers are not frozen — a provision here may still be renumbered, retired, or re-held — but a release that does any of those is tagged as one: `README.md` § Versioning states what a version tag means and what a MAJOR one obliges you to go re-read.

A gap also keeps the decision reversible. Skipping a provision reads your environment as it stands, and environments gain mechanisms; the vacant number is the home it returns to if yours does. A keyed entry is more reversible still — deleting the row restores the base — which is another reason to prefer it wherever the provision has a subject to key over at all.

The same reasoning applies to minting a provision logically prior to the others: give it a new
number, including one below the existing sequence, rather than renumbering the rest.

## Where to mint

The global ambit is shared — we append to it, and a number there has to mean the same thing on both
sides. The `I`, `P` and `A` ambits are yours alone. Mint there and no collision can arise, including
for a lingua: `§Ipy4` is yours, `§py4` is ours, and neither has to know about the other.

## Keeping a record

Optional, and worth it for one reason: a keyed entry is visible in your corpus, and so is a minted replacement, but an **omission leaves no trace anywhere**. Six months on you cannot tell a deliberate skip from an oversight, and neither can anyone reviewing your corpus. If that distinction is worth preserving, note the omitted provisions somewhere with a line on why — that is the whole record, and nothing else about adoption needs one. Keying over to disable buys the same record for free, which is the case for preferring it wherever the number is worth keeping resolvable.

The one check worth running afterwards, and again on every MAJOR revision you take: every citation in your live corpus resolves to a provision you kept.
