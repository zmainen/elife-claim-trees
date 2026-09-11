# Roles and relations

What may be said about a claim, and what may be said between two of them. This is the reference
behind two corpus-scope layers — [claim-format](/elife-claim-trees/pipeline/claim-format/),
which asks what a claim is, and
[relation-vocab](/elife-claim-trees/pipeline/relation-vocab/), which asks what each relation
asserts and which of them are oppositions. That second question is open, so everything
downstream of it is provisional.

Counts are generated from the claim files by `scripts/corpus_facts.py`. The denominator is the
{{papers}} published papers; the two method-example papers are counted separately, which is why
a relation the examples use can still show zero here.

## The roles

A role is the **rhetorical function** a claim serves in the paper's argument — what work it is
doing. It is distinct from claim-type, which is the epistemic character of the proposition
itself. The role governs what edges a claim can carry and how a reconstruction reads the
argument from the graph alone.

Nine roles, and {{roles_used}} of them appear in the corpus. The commonest is
`{{largest_role}}`, at {{largest_role_n}} of {{claims}} claims.

### `hypothesis` — {{role_counts.hypothesis}} claims

The paper's organising bet: the proposition the rest of the paper defends or tests.

*Signals*: "we hypothesize", "we propose that", "we asked whether", "we sought to test", "the
central question is whether".

Carries `entails:` to its predictions. It holds no empirical content itself and does not
`requires:` empirical claims — predictions do that. Panel is normally null; a hypothesis is
paper-level.

> **Headley.** `hypothesis-distinct-compartmental-roles` — "Perisomatic and distal dendritic
> inhibition serve distinct computational roles in regulating neuronal output." Entails four
> predictions.

### `prediction` — {{role_counts.prediction}} claims

The deductive consequence of a hypothesis under stated conditions: what we should observe if
the hypothesis holds.

*Signals*: "if X, then we should observe Y", "this predicts that", "the model predicts", "is
predicted to".

`derived-from:` its hypothesis, and is the target of `tests:` from the empirical claim that
closes the loop.

### `empirical` — {{role_counts.empirical}} claims

A measured or computed result, panel-grounded. The largest bucket by a wide margin.

*Signals*: "we found that", "we observed", "we measured", "Figure N shows", "doubling X reduced
Y from A to B".

Carries the most edges of any role: `tests:` predictions, `dissociates-with:` complementary
results, `requires:` methodological and scope claims, `supports:` synthesis, `rules-out:`
alternatives. Panel is required — an empirical claim is panel-grounded by definition.

### `control` — {{role_counts.control}} claims

An empirical result whose primary work is to **eliminate a rival explanation**. Functional
rather than contentful: the same proposition could be `empirical` in another paper.

*Signals*: "rules out", "excludes", "shows the effect is not due to", "no significant effect of
[confound]", "control condition".

**The alternative needs a node.** A control exists to kill a rival, so the rival must exist for
the `rules-out:` edge to reach it — authored as an ordinary claim, usually `hypothesis`, marked
as one the paper does not hold by the stance on its assertion rather than by its role or its
slug. A control whose edges name only the claim it defends, and never the alternative it
eliminates, has not recorded the point of the control. The
[stance layer](/elife-claim-trees/pipeline/stance/) found five eliminative relations aiming at
claims their own paper asserts, and {{dangling_rules_out}} still name prose that resolves to no
claim at all.

### `scope` — {{role_counts.scope}} claims

A boundary condition on the empirical claims, often global: `scopes: ["*"]` qualifies every
empirical claim in the paper.

*Signals*: "all results come from", "results are restricted to", "the model assumes", "is not a
physiological pattern".

> **Headley.** `l5-model-single-cell-scope` — "All results come from a single-cell compartmental
> model — no network dynamics, no recurrent excitation, no population effects."

### `methodological` — {{role_counts.methodological}} claims

A procedural or analytical capability that warrants a downstream interpretation. Not a claim
about the world; a claim about the apparatus.

*Signals*: "spike-sorting uses Kilosort 2.5", "rhythmic inhibition is modeled as sinusoidal rate
modulation", "the analysis uses [method]".

Carries `enables-method:` and `scopes:` to the empirical claims that depend on it.

### `synthesis` — {{role_counts.synthesis}} claims

A higher-order proposition integrating several empirical claims into one statement, staying
inside the paper's own evidence.

*Signals*: "taken together", "in summary", "these results show", "this dissociation
establishes" — typically at section breaks.

`derived-from:` where the synthesis is a deductive consequence, `supports:` where it integrates
results. The distinction is load-bearing:

> **Meijer R1.** `orthogonality-derived-from-additivity` — "Under a linear readout, additive
> modulation entails orthogonality of the stim and choice axes." Carries
> `derived-from: hypothesis-additive-modulation`, which demotes the empirical orthogonality
> finding from independent evidence to geometric corollary. An edge choice that changes what
> the paper has shown.

### `interpretation` — {{role_counts.interpretation}} claims

A reframing of empirical results through a theoretical lens — an act of mapping to broader
theory, as against `synthesis`, which stays inside the paper.

*Signals*: "may provide a functional interpretation", "suggests a role for", "points to a
mechanism whereby", "may explain".

Carries `interprets:` to the empirical claims being reframed.

### `literature-context` — {{role_counts.literature-context}} claims

A cited prior result treated as a first-class node: the paper depends on it, but did not produce
it.

*Signals*: "as shown by Author (Year)", "previous work has established", and the slug pattern
`interprets-<author>-<year>-<topic>`.

**The top-level `doi:` is the cited paper's DOI** — the schema's exception to the `doi: ~`
placeholder every other role carries. All {{literature_context_doi_top_level}} of the
{{literature_context_claims}} literature-context claims in the corpus put it there, and
{{literature_context_doi_in_assertions}} put it in `assertions[0].doi`. The
[reference-check layer](/elife-claim-trees/pipeline/reference-check/) resolves them against
CrossRef, which is the anti-hallucination check: a cited DOI that resolves to a different paper
than the claim names is the failure a reader would never catch.

## The relations

A relation is a proposition about logical structure between two claims — not a citation. A claim
file declares each as a top-level YAML key whose value is a list of target slugs. Reciprocals
(`predicts` / `confirms`) are populated symmetrically at build.

{{relation_types_defined}} are defined and {{relation_types_used}} appear in the corpus,
carrying {{relations}} relations in total.

| Relation | Reasoning form | What it asserts | Count |
|:---------|:---------------|:----------------|------:|
| `requires` | dependency | A would be invalid if B were false | {{relation_counts.requires}} |
| `supports` | abduction | A is evidence for B; several supports drive the abductive loop | {{relation_counts.supports}} |
| `entails` | deduction | A, typically a hypothesis, deductively implies B | {{relation_counts.entails}} |
| `derived-from` | deduction | A is the deductive consequence of B; reciprocal of `entails` | {{relation_counts.derived-from}} |
| `tests` | deduction → empirical | Empirical A tests prediction B, closing the loop | {{relation_counts.tests}} |
| `refutes` | negative abduction | A's evidence is incompatible with B | {{relation_counts.refutes}} |
| `rules-out` | elimination | A's evidence eliminates alternative B | {{relation_counts.rules-out}} |
| `dissociates-with` | dissociation (symmetric) | A and B jointly establish a dissociation | {{relation_counts.dissociates-with}} |
| `validates` | disconfirmation control | A is a control whose specific result strengthens B's warrant | {{relation_counts.validates}} |
| `predicts` | predictive validation | A predicts B, typically model to experiment | {{relation_counts.predicts}} |
| `confirms` | predictive validation | Reciprocal of `predicts`, populated at build | {{relation_counts.confirms}} |
| `interprets` | reframing | A reframes empirical B through a theoretical lens | {{relation_counts.interprets}} |
| `enables-method` | methodological warrant | A is the capability that warrants B's interpretability | {{relation_counts.enables-method}} |
| `scopes` | scope qualification | A is a boundary condition on B, or on every empirical claim if `["*"]` | {{relation_counts.scopes}} |
| `extends` | extension | A extends B beyond its original conditions | {{relation_counts.extends}} |
| `qualifies` | qualification | A narrows or conditions B without contradicting it | {{relation_counts.qualifies}} |
| `contradicts` | opposition | A and B cannot both hold | {{relation_counts.contradicts}} |
| `opposes` | opposition | A stands against B | {{relation_counts.opposes}} |
| `replicates` | replication | A is an independent finding of the same result as B | {{relation_counts.replicates}} |

Four sit at zero, and the zeros do not all mean the same thing.

`replicates` is zero because **no claim in this corpus replicates another**. These are ten
unrelated papers; replication needs an independent study of the same result, which nothing here
has. The [replication layer](/elife-claim-trees/pipeline/replication/) is declared with no
runner precisely so that this reads as an empty column rather than as an omission.

`contradicts` and `opposes` are zero because the eliminative work in this corpus is done by
`rules-out` — and whether those three are distinct relations or one relation with three names is
[an open question](/elife-claim-trees/pipeline/relation-vocab/) rather than a settled
distinction.

`predicts` is zero while its reciprocal `confirms` is not, which is an artefact rather than a
finding: `confirms` is populated at build from the forward edge, and the corpus authors have
written the confirming direction directly.

`refutes` at {{relation_counts.refutes}} is worth its own note. Until recently it was zero on
every page, not because the corpus lacked one but because the vocabulary was written down in
four scripts and none of them included it — so the single `refutes:` edge in the published
corpus was uncounted by the figures and dropped by every export. The vocabulary now lives in
`scripts/relations.py` and the four import it.

That episode is also why `refutes` is not treated as an opposition for checking purposes. A
paper that refutes its own prediction is closing the hypothetico-deductive loop, which is what
predictions are for; a paper that `rules-out` a claim it asserts has aimed an edge at the wrong
node. Collapsing the two reported eight legitimate refutations as errors.

### The reasoning forms

**Deduction.** `entails` and `derived-from` carry the hypothesis-to-prediction direction.
Headley's `hypothesis-distinct-compartmental-roles` entails four predictions; each is
derived-from the same hypothesis.

**The empirical loop.** `tests` runs the other way — from a measured result back to the
prediction it settles. `entails` and `tests` are not interchangeable and not reciprocal: one is
what the hypothesis commits you to, the other is what the experiment found.

**Elimination.** `rules-out` is the move a control makes. It needs a target that the paper does
not assert, which is why alternatives are authored as claims.

**Dissociation.** `dissociates-with` is symmetric — two results that jointly establish that two
things come apart. Neither is prior to the other, which is why it is the one relation where
direction carries no meaning.

**Reframing.** `interprets` maps a result onto theory. It is an act of mapping, not a
derivation, and reading it as a derivation is the commonest way a reconstruction overstates what
a paper showed.

**Warrant.** `enables-method` and `scopes` say what a result depends on and where it stops.

The choice is consequential rather than cosmetic. The synthesis pipeline reads these edges as
cues for the rhetorical move it should articulate, so the edge type governs the reconstruction —
which is the substance of the open question on
[relation-vocab](/elife-claim-trees/pipeline/relation-vocab/).
