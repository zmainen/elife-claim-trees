# Handing a claim structure to a human

The structure is infrastructure. It is not the artifact a person reads, and pasting it into one
produces a document nobody wants: thirty YAML blocks where a paper used to be.

**The default is an overlay.** The human keeps their own document — the paper, the draft, the
protocol — and the claims arrive anchored to the spans that carry them. The structure annotates
the text; it does not replace it, summarise it away, or stand in front of it.

The exception is narrow and worth naming: when the deliverable *is* the structure — a corpus
contribution, an export, a file another tool will parse, a review another analyst will edit —
verbatim claim files are exactly right. Everything below is about the other case.

## What the reader wants, in order

A reader arriving at an annotated paper wants four things, in this order:

1. What does this paper claim?
2. How do those claims hold each other up?
3. What can I take away and use?
4. And only then — how was this made, and how far has it got?

The order is not arbitrary. The first is the paper; the last is us. A reader who cannot get the
first is not helped by the fourth, and an artifact that leads with provenance is an artifact
about its own machinery. Put the verification banner, the model names, the run ledger and the
layer map *after* the science, or in a view of their own. A green box at the top of someone
else's paper is one step's result wearing the paper's headline.

## Anchor to spans, and name the misses

The working form in this repository is `marked/<paper>.marked.md`: the paper's own prose, in its
own order, with one anchored note per span that carries a result.

```
Choices: manipulation check As expected, participants' probability of choosing the risky
option increased with the difference between the expected value …⟦>zach claim=86ccf2d0-…:
@{…quoted span…} participants-probability-choosing-risky-option⟧
```

Three properties make it useful, and all three are worth reproducing in any overlay you build:

- **The note quotes the span it is attached to**, so the anchor survives reformatting and is
  checkable by eye.
- **The key is the claim's UUID**, not its slug or its sentence — the identity that does not
  move when wording does.
- **Misses are first-class.** `claim=gap` marks a result no claim accounts for; `claim=no-assertion`
  marks a span that states no result (a paradigm narration, a figure title, a forward
  reference). An unmarked sentence carried no result and was never an obligation. An overlay
  that shows only its hits cannot be audited — it looks complete whatever it missed.

Gädeke's marked document carries 5 gaps and 16 no-assertions beside its claim anchors. That
ratio is the honest part of the artifact.

## Plain wording is what the reader meets first

Claims are recorded in the authors' words, and that is right: the corpus must be able to show
what the paper said, and a paraphrase is not evidence of anything. But the authors' words open
with the statistics —

> Being the decision-maker (Social + Solo vs Partner condition) reduces participant happiness
> independently of outcome (Study 1: t(3600)=−3.92, p<0.0001, …)

— and a page listing thirty of those has told a non-specialist nothing they can act on.

So: **the formal `claim` sentence stays canonical and unedited; a plain restatement is what the
reader meets.** One plain sentence per claim, the statistics behind a disclosure rather than in
front of the proposition. `shortClaim` was meant to serve this and is filled for hypotheses and
predictions only; `scripts/plain_claims.py` fills it for the rest as a layer.

Two rules that follow, and both are easy to get wrong:

- **Never rewrite the formal claim to make it readable.** The readable form is an additional
  field, produced and versioned separately, and it goes stale when the claim it restates
  changes.
- **Mark model-written prose as model-written.** A reader will take a fluent restatement for the
  paper's own words unless told otherwise. This is the whole reason the plain layer is a layer
  with a version, a recorded run, and a place for a person to approve it, rather than a field
  somebody edits.

## What stays behind the surface

Machine surfaces that do not belong in a human artifact's body text: UUIDs, `priority`, raw
relation lists, `claim-type` alongside `role`, run ids, model names, input hashes. They belong
in the detail view a reader opens for one claim — the drawer — or in a provenance view, not
inline where they crowd out the proposition.

The edges are the exception worth surfacing, because they answer question 2 — but surface them
as the argument, not as a list of typed tuples. "This is ruled out by the control in Figure 4"
is the edge; `rules-out: [alt-…]` is its storage.

## Two surfaces, one state

A tree gets read on screen and on paper, and the two must show the same state. The repository
does this with the Reader — claims in the margin of the paper — and
`scripts/review_document.py`, which regenerates the printable document from the current claim
files and carries any verdict already recorded, so a reading begun in one surface is visible in
the other. If you build an overlay that a person will mark up, decide where their marks land
before they make any, and regenerate the other surface from the same source rather than letting
the two drift.

## Checklist

Before handing over a human-facing artifact built from a claim structure:

- [ ] the person's own document is intact, in its own order, and readable with the overlay off
- [ ] every claim is anchored to the span it came from, quoting it
- [ ] gaps and no-assertion spans are shown, not only hits
- [ ] the wording a reader meets first is plain; the formal sentence is available, unedited
- [ ] model-written prose is labelled as model-written
- [ ] no UUIDs, hashes or run ids in body text
- [ ] edges appear as argument, not as tuples
- [ ] provenance and verification come after the science, not above it
- [ ] what the structure does *not* cover is stated where a reader will see it
