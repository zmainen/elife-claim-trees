# Analyze a paper into claims

Reverse construction: a finished argument in prose goes in, a claim graph comes out. You are
recovering a structure the authors had and did not write down.

Expect 15–40 claims for a full-length primary research paper, plus components. A tree with six
claims has collapsed the argument; one with a hundred has decomposed results into statistics.

## 1. Get structured source text

The format the text arrives in bounds everything downstream. Prefer the publisher's XML (JATS
for eLife and most journals) over the PDF:

| | JATS XML | PDF |
|:--|:--|:--|
| Section boundaries | tagged | inferred from heading text |
| Figure captions | one element each, with its own id | recovered by position |
| Figure identity | the publisher's own `fig2`, `fig3s1` | guessed from "Figure 2" |
| Reading order | explicit | a column-order guess |

eLife: `https://cdn.elifesciences.org/articles/<id>/elife-<id>-v1.xml`. Panel grounding is only
as good as figure structure at intake — from JATS a `panel` field is the publisher's element id,
from a PDF it is an inference about a label in running text.

Slice the source into abstract, results, figure captions, methods, and keep the verbatim text
you read. **Check the slice sizes before reading further.** A short results slice means section
detection failed and everything downstream read the wrong text — a fault in intake that presents
as a fault in reading.

## 2. Read the abstract for the top and the questions

Identify the two to four top-level claims — the paper's main bets — and write candidate slugs.
These become the synthesis and interpretation nodes; they usually have no panel of their own.

Write the paper's `questions` at the same time, from the introduction's closing paragraph and
the abstract's setup. A question the paper answers but never states is still a question; record
it and note that it is reconstructed.

## 3. Walk the results, panel by panel

For each panel, table or analysis block, ask: **what single proposition does this establish?**
That is one empirical claim. Write it as one declarative sentence carrying the paper's own
numbers, verbatim. If a panel establishes two propositions, it is two claims; if a proposition
needs three panels, it is one claim with three panels in `assertions[].panel`.

Where a claim states a whole that several comparisons each partly establish, write the whole and
attach the components with `part-of` rather than inflating the count with near-duplicates.

Capture provenance now, while the structured source is in front of you: panel id, figure URI,
the analysis script or notebook, the dataset and its DOI. Guessing figure filenames from panel
labels at a later build step loses information you have at this moment.

## 4. Recover the spine

Results give you the empirical layer. The spine is elsewhere:

- **Hypotheses** — the introduction's closing paragraph and the abstract's "we sought to
  test". Often unstated as such; a paper with results and no recoverable hypothesis is worth
  noting rather than inventing one.
- **Predictions** — sometimes explicit ("this predicts that"), more often implicit in how a
  result is framed as confirming or disconfirming. Where implicit, write the prediction that
  makes the test intelligible and say in the body that it is reconstructed.
- **Controls** — "to rule out", "no effect of", "we verified that". For each, name the
  alternative it eliminates and **give that alternative its own claim** with stance
  `entertains` or `rejects`. This is the step most often skipped, and skipping it leaves the
  control's edge pointing at whatever asserted claim is nearest.
- **Scope** — "all results come from", "the model assumes", "restricted to". Also the limits
  paragraph of the discussion, which is where scope claims hide in finished papers.
- **Methodological** — the analytical capabilities the interpretations lean on: the sorting
  pipeline, the pooling strategy, the null model. Register the ones a result *depends* on, not
  every method mentioned.
- **Literature-context** — prior results the argument inherits as premises, especially any
  framework the paper positions itself against. If the paper rules out "gain control", gain
  control needs a node or the eliminative move has no referent.

## 5. Assign role and claim-type

Two axes, assigned separately (see [references/schema.md](../references/schema.md)). Role is
the more consequential: it governs numbering, grouping and how the argument reads back. A
measurement whose job is to kill a confound is `role: control` even though its type is
`empirical`.

## 6. Draw the edges

Work from the spine outward, checking direction on each
([references/relations.md](../references/relations.md)):

1. `entails` from each hypothesis down to its predictions.
2. `tests` from each empirical result up to the prediction it settles.
3. `rules-out` from each control to its alternative.
4. `dissociates-with` between the pairs whose *contrast* is the finding.
5. `requires` from results to the scope and methodological claims they depend on;
   `scopes` and `enables-method` back the other way where the bounding claim is the subject.
6. `supports` from results to the syntheses they ground; `interprets` from interpretations to
   the results they reframe.

If an edge is hard to type, the usual cause is that one endpoint is the wrong claim — most often
a missing alternative or a missing scope claim.

## 7. Coverage — what did you miss?

Sweep the results text for every span carrying a statistic or a stated result, and check each
against the tree. Three outcomes: **covered** by a claim, a real **gap**, or **asserting
nothing** (a method restatement, a forward reference). Record the verdicts rather than
recomputing them — a mechanical match on "does a claim restate this statistic" is wrong in both
directions, and the residue is a judgement worth storing once.

Gaps cluster in the discussion and in negative results the abstract does not carry. Those are
exactly the claims a structure is worth building for, so do not let coverage stop at the figures.

## 8. Validate and report

Run [references/checks.md](../references/checks.md). Then say plainly, in the handoff:

- which claims are single-source readings you are unsure of;
- which predictions and hypotheses you reconstructed rather than found stated;
- which numbers you could not locate verbatim in the source;
- which alternatives the paper eliminates without naming, so their nodes are your paraphrase;
- what the coverage sweep left as gaps.

An extraction that reports none of this has not been checked, it has been asserted.

If what you hand over is for a person to read rather than for a corpus to hold, build it as an
overlay on the paper's own text — see [references/presentation.md](../references/presentation.md).

## Failure modes

**Quantitative hallucination.** A number that is plausible, absent from the paper, and
uncatchable by a reader. Take every value verbatim; leave the field out if you cannot.

**Panel inflation.** One claim per statistic yields a tree that mirrors the figures and explains
nothing. The unit is a proposition, not a p-value.

**Reading the discussion as results.** A reframing through outside theory is
`role: interpretation`, not an empirical claim, however confidently the discussion states it.

**Single-reader bias.** One pass fixes a reading. Where it matters, read the paper more than
once along different axes — framing, literal numerics, computational structure — and treat a
claim that only one pass surfaced as single-source: it may be real and buried, or an artefact of
how you read.

**Silent edge repair.** When `rules-out` has no legal target, the fix is a new alternative node,
never a redirect to the nearest asserted claim.
