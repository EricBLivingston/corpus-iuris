# Adopting This Corpus

The corpus binds once you adopt it. This file is different: it is guidance on a process we do not run and cannot see, so everything below is a recommendation with its reasoning attached, and the decision is yours.

## If you are on Claude Code

Take it as it stands. The content here was written for the Claude Code harness, and most should work out of the box, with tweaks made in the local `instance.md` file. `installing.md` carries the mechanics: the three surfaces a copy moves between, the staging loop, and where each published piece lands under `~/.claude`.

## If you are on another harness

Look for a `transforms/<harness>/` package that matches your harness. One means there is no translating left to do: the base is already generic wherever a harness particular would go, and the package carries that harness's own artifacts and the sequence for installing them, so what remains is § Write your instance file first and the decisions below. With no matching package you can still adopt the corpus, but the harness-specific provisions are yours to translate. `installing.md` carries the install model every harness shares, so a package holds only its own delta.

## Write your instance file first

The base is generic wherever no concrete name would be true of every installation. Wherever a provision turns on a name only your installation can supply, it names the *kind* of referent and stops there. Those are the slots the instance ambit exists to fill, and until you fill them the provisions that turn on them have no referent on your installation.

`instance-example.md` is a platform-specific base example: copy it and refactor as necessary. Its content is the first thing to decide; where in the sequence the file is written is the harness's own call, and on Claude Code `installing.md` § What you supply places it in the installed tree after the corpus is copied rather than before it.

The decisions below come one provision at a time, and that file is the mechanism nearly all of them use.

## Taking a provision you do not want as written

These routes differ in cost and in what they leave behind rather than in legitimacy. What separates them is the fate of the token: whether it still resolves to the same provision on both sides, and what a reader finds where it does not. A removal is complete when the citations to it are gone from your live corpus. One provision is a text search and a few edits; an instrument costs what cites it, caselaw included. Stubbing and keying over leave every citation in place and resolving.

| Strategy | Root corpus | Instance ambit | Best for |
| ---- | ---- | ---- | ---- |
| **Key over** | provision stays as published | one keyed entry replacing what conflicts | anything from a narrowing to a wholesale rewrite, as long as it still answers the question the original asked |
| **Key over to disable** | provision stays as published | one keyed entry disabling it | a provision your environment contradicts outright, where the number should stay resolvable |
| **Omit** | provision removed, every citation to it swept | nothing | a provision with no subject here at all, and no replacement |
| **Omit and replace** | provision removed | the replacement, minted whole | a replacement with nothing left of the original to reconcile |
| **Transpose at staging** | provision stubbed, or stripped with its citations, on its way to production | nothing | more provisions than you want resident rows for |

Key over is the mechanism the ius is built around: a keyed entry *overlays* its base rather than displacing it, so it scales from the smallest tweak to a wholesale rewrite without changing form, and with no root omission. Whatever you do not restate stays live and keeps merging with our revisions, and the token resolves to the same provision on both sides, which is what the citation-resolution argument below asks for. It costs one row of resident context.

Key over to disable is that same entry saying the base does not bind here. The number stays resolvable, and resolving it tells a reader the absence was decided rather than overlooked, which is the record § Keeping a record otherwise asks you to keep by hand.

Omit is for a provision with no subject on your installation at all, rather than merely a different subject, which is what keying over is for.

Omit and replace gives you a full replacement at zero residual cost in root, but the number then denotes your provision in your corpus and ours in ours. If we later revise ours in a way you would have wanted, taking that revision is manual work and nothing will tell you it happened. How much that matters depends on how closely you expect to track us. Prefer keying over wherever your replacement still answers the question the original was asking.

Transpose at staging is the bulk instrument, and it is the strongest reason for the staging surface `installing.md` puts between the clone and production. Reconciliation is what staging is described there for; mutability is what it gives you. Everything in staging is yours to rewrite before any of it becomes resident, so a script in the clone-to-staging path can rewrite the canon files themselves and hand production a corpus already shaped to your installation. A run of provisions is stubbed in one pass, where keying each one over would cost a resident row apiece. Keep the rewrite in the script rather than editing staging by hand: every pull re-mirrors the clone into staging, so a hand edit is recovered by hand every cycle, where a script reapplies itself.

The script strips a provision or stubs it, and the citation-resolution argument decides which. Stripping vacates the number, so the script's second job is every citation to it in the files you kept, a sweep growing with each provision taken. Stubbing (its token, its heading, and a body stating that it does not apply on this installation) leaves those citations resolving to the decision, with no sweep behind it.

## What we recommend, and why

Key over in your instance file wherever the provision still has a subject here. Where it has none, go sparse in root (skip it, leave the gap, do not renumber) and mint fresh from `I1`.

The reason is citation resolution. A global token is worth having only if it means the same provision in your corpus and in ours; that is what lets a provision be cited in a document that travels between them. Renumber root to close a gap and your `※5` stops being our `※5`. The failure is silent: a citation to a removed provision fails loudly and gets noticed, while a citation that resolves to a *different* provision because the numbers shifted underneath it does not.

Root moving underneath you is the one case where that failure is not silent. Our numbers are not frozen, but a release that disturbs one is tagged accordingly: `README.md` § Versioning states what each version tag means and what a MAJOR one obliges you to go re-read.

Distance from the published corpus correlates to greater caselaw disruption. A ruling whose `Governs:` line names a provision you stripped comes out with it, and its holding over the provisions you kept goes too. A stubbed provision leaves its rulings resolvable and inert, and one that composed the stub with provisions you kept still recounts the collision it settled, carrying the removed force back by paraphrase. Read whatever names what you stubbed. The corpus is tuned as a whole; a heavy rewrite reaches further than we can predict or support.

A gap also keeps the decision reversible. Skipping a provision reads your environment as it stands, and environments gain mechanisms; the vacant number is the home it returns to if yours does. A keyed entry is more reversible still (deleting the row restores the base), which is another reason to prefer it wherever the provision has a subject to key over at all.

The same reasoning applies to minting a provision logically prior to the others: give it a new number, including one below the existing sequence, rather than renumbering the rest.

## Where to mint

The global ambit is shared: we append to it, and a number there has to mean the same thing on both sides. The `I`, `P` and `A` ambits are yours alone. Mint there and no collision can arise, including for a lingua: `§Ipy4` is yours, `§py4` is ours, and neither has to know about the other.

## Worked examples

Each is an entry as it would stand in your corpus: in your instance file, refactored from `instance-example.md`, in your project's own caselaw file, or in the canon file your staging script rewrites.

### A local authority stricter on one point

House style bans the em dash outright; `§en1` licenses one where interruption itself is the relation. Everything else the provision holds is untouched, so one keyed row carries it:

| Token | Intent on this installation |
| ---- | ---- |
| §en1 | House style bars the em dash outright, so interruption has no licensed dash realization here. Every other connective resolution stands. |

A narrowing and a disagreement take the same form, and the entry records the text in force here either way.

### A local authority governing the whole provision

An installed writing skill covers the whole of what `§en1` covers, and is stricter across it. There is nothing to disagree with and no local rule to restate, so the row defers wholesale:

| Token | Intent on this installation |
| ---- | ---- |
| §en1 | Skill `my-skill` supersedes entirely |

A keyed entry overlays its base (`rules/ius.md` § Precedence: *lex specialis*), so a body deferring entirely puts the named authority in front of the base on this installation, with nothing minted. A skill is the common case, loading when the work matches its description; an employer style guide or a journal's house rules take the same row.

### A provision your environment contradicts

Your harness carries a standing instruction not to dispatch subagents, written by you rather than supplied as a harness default. `※4` mandates delegating work that touches two or more files. `⊢3` resolves adventitia against the precept it collides with and reaches nothing that originated with you, so the precedence order settles this instead: written down at your installation, your instruction is a precept of the instance ambit, which outranks the universal ambit `※4` sits in.

Erasing the provision takes either of two forms. The negation carries it in your instance file, which is itself a site, so the marker reaches the whole installation:

| Token | Intent on this installation |
| ---- | ---- |
| ※4 | ⊬※4 in all cases: disabled |

In staging, a transposition script erases it where it is defined, so the canon file itself reads as what is in force. A stub takes the shape of the file it lands in. `rules/rules.md` carries its provisions as prose entries:

> **※4. 2-File Rule** — Not applicable on this installation.

`rules/directives.md` carries its own as a table, so a stub there is a row:

| § | Principle | Summary |
| ---- | ---- | ---- |
| §9 | **Batch-First APIs** | Not applicable on this installation. |

The negation leaves canon byte-identical to ours, so every pull is a clean re-mirror and the decision survives the update untouched; the cost is that a reader holds two files to know what is in force. The stub makes the canon file read as what is in force with no indirection; the cost is a rewrite living in the clone-to-staging script and re-running on every pull. Volume decides: a one-off goes in the instance file, an instrument's worth of provisions through staging.

### A collision with what the harness injects

Your harness's system prompt instructs the agent to change only what was asked; `※10` sweeps small adjacent fixes into scope. Adventitia colliding with an authored precept is the subject of the ⊢3 register in your instance file, so it takes a row there, naming the precept that governs and the delta:

| Governs | Displaced shape | Holding |
| ---- | ---- | ---- |
| ※10 | Scope held to the literal ask (`do not rewrite unrelated code`; `do not touch files that are not relevant`) | ※10. A fix inside a file the work already opens is swept in, unless a governance bound's file set excludes it; a file the work does not otherwise touch stays closed. |

### A collision with canon you already carry

The register handles what the harness injects. A collision with your own standing canon is caselaw, minted in the `P` ambit in your project's caselaw file:

> **⊢P1. A library another team consumes is published.** §1 reserves compatibility accommodation for published libraries with external consumers. House canon requires a deprecation cycle on every shared package in this monorepo, and a sibling team is not an external consumer on §1's reading. What makes the accommodation necessary is a consumer outside this team's release cadence, which a sibling team is. Every package under `libs/` is published for §1's purposes; everything outside it takes §1 as written.
>
> **Governs:** §1.

The `Governs:` line names every provision the entry composes, which is what makes the ruling reachable from the provision it settles. Mint `⊨P` where the collision surfaced in application and `⊢P` where the texts alone show it.

## Keeping a record

Optional, and worth it for one reason: a keyed entry is visible in your corpus, and so is a minted replacement, but an omission leaves no trace anywhere, unless a transposition script performed it and stands as its own record, reapplying on every pull. Six months on you cannot tell a deliberate skip from an oversight, and neither can anyone reviewing your corpus. If that distinction is worth preserving, note the omitted provisions somewhere with a line on why. That is the whole record, and nothing else about adoption needs one. Keying over to disable buys the same record for free, which is the case for preferring it wherever the number is worth keeping resolvable.

The one check worth running afterward, and again on every MAJOR revision you take: every citation in your live corpus resolves to a provision you kept.
