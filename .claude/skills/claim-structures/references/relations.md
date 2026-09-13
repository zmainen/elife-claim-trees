# Relations

A relation is a proposition about logical structure between two claims — never a citation.
Each is a top-level YAML key whose value is a list of target slugs:

```yaml
tests: [prediction-distal-dendritic-spike-mechanism]
requires: [l5-model-single-cell-scope, naturalistic-drive-parameterization]
rules-out: [alt-distal-inhibition-raises-somatic-threshold]
```

An older list form, `belongings: [{relation: requires, target: …}]`, is equivalent and appears in
existing corpora. Both are the schema; a tool that reads only one undercounts.

## The vocabulary

| Relation | Reasoning form | What it asserts | Direction |
|:---------|:---------------|:----------------|:----------|
| `requires` | dependency | A would be invalid if B were false | from the dependent claim to its prerequisite |
| `supports` | abduction | A is evidence for B | from the evidence to what it is evidence for |
| `entails` | deduction | A (a hypothesis) deductively implies B | from the hypothesis down to the prediction |
| `derived-from` | deduction | reciprocal of `entails` | from the prediction back up to its hypothesis |
| `tests` | deduction → empirical | empirical A tests prediction B, closing the loop | from the result up to the prediction |
| `refutes` | negative abduction | A's evidence is incompatible with B | from the evidence to the prediction/hypothesis/alternative |
| `rules-out` | elimination | A's evidence eliminates alternative B | from the control to the alternative — never to an asserted claim |
| `dissociates-with` | dissociation | A and B jointly establish a dissociation | symmetric; direction carries no meaning |
| `validates` | disconfirmation control | A's specific result strengthens B's warrant | from the control to the claim it warrants |
| `predicts` | predictive validation | A predicts B, typically model to experiment | from the model to the observation |
| `confirms` | predictive validation | reciprocal of `predicts` | from the result to what it confirms |
| `interprets` | reframing | A reframes empirical B through a theoretical lens | from the interpretation to the result |
| `enables-method` | methodological warrant | A is the capability that warrants B's interpretability | from the capability to the result |
| `scopes` | scope qualification | A bounds B, or every empirical claim if `["*"]` | from the scope claim to what it bounds |
| `extends` | extension | A extends B beyond its original conditions | from the later or broader result |
| `qualifies` | qualification | A narrows B without contradicting it | from the qualifying result |
| `contradicts` | opposition | A and B cannot both hold | either direction |
| `opposes` | opposition | A stands against B | from the claim that stands against |
| `replicates` | replication | A is an independent finding of the same result | from the independent finding |
| `part-of` | composition | A is one comparison, condition, measure or study of the whole B states | from the component to the whole |

## The six moves

**Deduction.** `entails` and `derived-from` carry the hypothesis-to-prediction arc. One
hypothesis normally entails several predictions; each is derived-from it.

**Induction and support.** `requires` and `supports` carry dependency and evidence. A standalone
empirical claim outside any hypothesis loop still supports the higher-order claims it grounds.

**Abduction.** `supports` and `refutes` running from results back to hypotheses close the
abductive loop: a result that supports one hypothesis while refuting the prediction of its rival
is abduction by elimination.

**Elimination.** `rules-out` is the move a control makes. It needs a target the paper does not
assert, which is why alternatives are authored as claims.

**Dissociation.** `dissociates-with` joins two results that are both true and *differ*; the
contrast is the finding. It is the one relation where direction carries no meaning.

**Scope and warrant.** `scopes` and `enables-method` say where a result stops and what makes it
interpretable. They run *from* the bounding or enabling claim *to* the results affected —
opposite to `requires`, which runs from the result to what it depends on.

## Pairs that get confused

**`requires` vs `supports`.** `requires` is dependency: if the target were false the source
would be invalid. `supports` is evidence: the source makes the target more credible and survives
its falsity. One empirical claim commonly carries both — it *requires* the scope claim bounding
the model it was computed in, and *supports* the hypothesis it was run to test.

**`entails` vs `tests`.** Both connect a hypothesis's arc, in opposite directions and from
different roles. `entails` runs down and is deductive: the prediction follows if the hypothesis
holds. `tests` runs up from a measured result to the prediction it settles. A result never
entails; a hypothesis never tests.

**`rules-out` vs `refutes`.** `rules-out` eliminates an *alternative* — a claim raised in order
to reject, with a node of its own and stance `entertains` or `rejects`. `refutes` aims at one of
the paper's *own* predictions or hypotheses that the evidence came out against; a paper refuting
its own prediction is the hypothetico-deductive loop closing correctly, not an error.

**`dissociates-with` vs `contradicts`.** A dissociation joins two results that are both true and
differ. A contradiction says two claims cannot both hold. Two conditions producing different
effects is a dissociation, and calling it a contradiction destroys the finding.

**`scopes` vs `requires`.** The same pair of claims can carry both, in opposite directions: the
result requires the scope; the scope scopes the result. Pick the direction by asking which claim
is doing the bounding.

**`validates` vs `supports`.** `validates` is a control's edge — a check whose *specific*
outcome (a null where a confound would have produced an effect, a sign flip, a manipulation
check) strengthens a warrant. `supports` is ordinary evidence. A control validates; a main
result supports.

**`part-of` vs `supports`.** `part-of` is composition: the source is one comparison, condition,
measure or study *of* the proposition the target states whole, and removing it weakens the
target without falsifying it. `supports` is an independent finding that would survive removal. A
filter on `supports` cannot tell a component from an independent finding, which is why
composition needs its own relation.

## Worked spine

From `headley-2026-inhibitory-rhythms`, the shape to imitate:

```
hypothesis-distinct-compartmental-roles            (role: hypothesis)
  entails → prediction-distal-dendritic-spike-mechanism
  entails → prediction-perisomatic-threshold-mechanism
  entails → prediction-perisomatic-input-output-shaping
  entails → prediction-orthogonal-input-gating

distal-inhib-drops-firing-02hz                     (role: empirical, fig4/fig5)
  tests            → prediction-distal-dendritic-spike-mechanism
  rules-out        → alt-distal-inhibition-raises-somatic-threshold
  dissociates-with → perisomatic-inhib-drops-firing-07hz
  requires         → l5-model-single-cell-scope
  requires         → naturalistic-drive-parameterization
  supports         → hypothesis-distinct-compartmental-roles

l5-model-single-cell-scope                         (role: scope)
  scopes → ["*"]

pv-gamma-sst-beta-correspondence                   (role: interpretation)
  interprets → the four empirical claims it reframes
  requires   → interprets-pv-gamma-sst-beta-associations   (role: literature-context)
```

Read that alone and the argument reconstructs: a dissociation hypothesis, four predictions, a
pair of contrasting measurements that test two of them and jointly establish the dissociation, a
model boundary on everything, and an interpretation that reaches outside to prior literature
through an explicit node rather than an unnamed referent.

## Open question

Whether `supports` and a hypothetical `consistent-with` assert different things, and whether
opposition is one relation or three (`contradicts` / `opposes` / `rules-out`), is unsettled.
`dissociates-with` in particular is declared as an opposition but used alongside supporting
relations on the same pair — coherent only if it means "these come apart" rather than "the
target is wrong". Everything downstream of that question is provisional in the exact sense that
it would change if the answer did. Do not resolve it silently in a new tree: use `rules-out` for
elimination, `dissociates-with` for contrast, and leave `contradicts` and `opposes` for cases
where two claims genuinely cannot both hold.
