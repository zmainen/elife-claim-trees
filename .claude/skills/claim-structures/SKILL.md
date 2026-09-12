---
name: claim-structures
description: "Work with claim structures — typed propositions joined by typed logical relations (hypothesis entails prediction, empirical result tests it, control rules out an alternative, scope bounds it). Use when analyzing a paper into claims, speccing or outlining a paper around its argument, designing an experiment around what it has to rule out, auditing an argument for gaps, or authoring and editing claim files in a claim-tree corpus."
---

A claim structure is a scientific argument written as data: one declarative proposition per
node, one typed logical relation per edge. It is the same object whether you are reading a
finished paper, planning one, or designing the experiment that will fill it — what changes is
which end you start from.

## What a claim is

A claim is an **entity**, not a result and not a figure. `dat-reuptake-dominates` is a
proposition about the world that several papers might assert, that a reproduction might test,
and that other claims might depend on. A *paper* asserts a claim, in a particular panel, with a
particular analysis, on particular data — that pairing is an **assertion**, and it is a property
of the paper, not of the claim. The same proposition can be asserted by one paper and rejected
by another; both assertions hang off the one claim, and the disagreement becomes visible.

Relations between claims are **not citations**. `A requires B` says A would be invalid if B were
false. That is why the structure is worth building: invalidity propagates along the edges, so a
claim that fails is not an isolated correction but a traceable one.

## The minimal claim

```yaml
---
uuid: 26819b09-5b20-4c90-b9f3-8bdd29a2a57c   # uuid4, generated once, never changes
slug: distal-inhib-drops-firing-02hz          # 3-6 words, lowercase, verb phrase
claim: >
  Doubling the strength of distal dendritic inhibition reduces somatic firing rate from
  approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing dendritic Ca²⁺ and
  NMDA spikes rather than by directly raising AP threshold.
claim-type: empirical        # what kind of proposition it is
role: empirical              # what work it does in the argument
epistemic: strong            # strong | moderate | weak | contested
concepts: [distal dendritic inhibition, somatic firing rate, dendritic spike suppression]

tests: [prediction-distal-dendritic-spike-mechanism]
requires: [l5-model-single-cell-scope]
dissociates-with: [perisomatic-inhib-drops-firing-07hz]

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig4, fig5
    analysis: scripts/Fig4.ipynb
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — inhibition magnitude sweep
    confidence: strong
    stance: asserts          # asserts | entertains | rejects | attributes
---

Prose body: caveats, boundary conditions, why this edge and not that one.
```

Full field reference: [references/schema.md](references/schema.md).
Relation vocabulary, directions and the pairs people confuse: [references/relations.md](references/relations.md).

## The two axes

`claim-type` is the **epistemic character** of the proposition — empirical, interpretive,
existence, synthesis, assessment, hypothesis, prediction. `role` is the **rhetorical function**
it serves in this argument — hypothesis, prediction, empirical, control, scope, methodological,
synthesis, interpretation, literature-context.

They are orthogonal, and the distinction is load-bearing. A `claim-type: empirical` proposition
is `role: empirical` when it is a finding, `role: control` when its job is to kill a rival, and
`role: scope` when its job is to bound what the others mean. The same measurement does
different work in different arguments.

## The spine

```
question
  ├── hypothesis  (the answer the work commits to)
  │     └─ entails → prediction ←─ tests ── empirical result
  │                                              ├─ requires → scope, methodological
  │                                              └─ supports → synthesis → interpretation
  └── alternative (a rival answer, stance: entertains)
        ←─ rules-out ── control
```

Every workflow below walks this spine. Analysis walks it upward from the panels; a paper spec
walks it downward from the question; an experimental design walks it sideways, from the rivals
that have to be eliminated to the measurements that eliminate them.

## Pick the workflow

| You are… | Read |
|:---------|:-----|
| turning a published or drafted paper into claims | [workflows/analyze-paper.md](workflows/analyze-paper.md) |
| speccing or restructuring a paper you are writing | [workflows/spec-paper.md](workflows/spec-paper.md) |
| designing an experiment or study before data exists | [workflows/design-experiment.md](workflows/design-experiment.md) |
| checking a structure someone else built | [references/checks.md](references/checks.md) |

## Invariants

These hold in all three workflows. Most defects found in real claim trees are violations of one
of them.

1. **One sentence, one claim.** A proposition needing two sentences is two claims. Two results
   joined by "and" are two claims — or one whole with two `part-of` components, if neither
   states the proposition on its own.
2. **Quantitative where the result is.** Put the numbers in the claim sentence, taken verbatim
   from the source. Never compute, round, or infer a value that the source does not state —
   a plausible fabricated number is the failure mode a reader cannot catch.
3. **The alternative needs a node.** A control exists to eliminate a rival, so the rival must
   exist as a claim for `rules-out` to reach. A control whose edges name only the claim it
   defends has not recorded the point of the control.
4. **Never oppose what you assert.** `rules-out`, `contradicts` and `opposes` may not point at a
   claim the same paper asserts. When the real target has no node, the edge drifts to the
   nearest claim that does — structurally valid, factually false. (`refutes` at one's own
   prediction is different, and correct: that is the hypothetico-deductive loop closing.)
5. **Direction is part of the relation.** `entails` runs down from hypothesis to prediction;
   `tests` runs up from result to prediction. They are neither interchangeable nor reciprocal.
6. **Scope before results.** Write what the work does *not* establish — the model's boundary,
   the population, the stimulation regime — as scope claims, and point them at what they bound.
   Written afterwards, they become a discussion paragraph nobody traverses.
7. **The graph is the argument.** Read the edges alone, with the claim sentences, and see
   whether the argument reconstructs. If it does not, the edges are wrong — not the reader.
8. **Do not fabricate identifiers.** Generate UUIDs (`python3 -c "import uuid; print(uuid.uuid4())"`).
   Take panel ids from the source's own figure elements. Leave `doi: ~` unless the DOI is real.

## Stance, and why it is on the assertion

A paper does not only assert. It raises candidates it does not commit to (`entertains`), argues
that some are false (`rejects`), and reports what others claimed (`attributes`, which requires a
source). Stance says what the paper concluded; the edges say why. Keep both — a paper can
dismiss a rival with no evidence at all, and conversely the `rules-out` edge names which control
did the work, which stance cannot.

## In this repository

The corpus, the schema and the tooling live here:

```bash
python3 scripts/pipeline.py run <paper> claim-tree --dry-run   # what producing a tree would do
python3 scripts/check_relations.py                             # stance and edge legality
make check                                                     # the gate CI enforces
```

`docs/claim-format.md` is the normative format, `docs/vocabulary.md` the role and relation
reference, `docs/method.md` the full method including verification. `claims/<paper>/` holds
worked examples — `headley-2026-inhibitory-rhythms` is the cleanest complete spine.

Note that no human has verified any claim in this corpus (`docs/method.md` § 3). Treat existing
files as a draft annotation layer to imitate structurally, not as adjudicated content.
