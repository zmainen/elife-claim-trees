# Argument from the graph

You are reconstructing a paper's argument from its **claim graph alone** — no abstract, no
prose, no title, no author framing. You see only the claim sentences, their roles, their panels,
their epistemic markers and the typed edges between them. If the graph carries the argument, a
restatement built from it should be recognisable as the same paper; what you cannot recover is
what the abstract adds beyond the graph. That comparison is the whole point, so recovering the
framing from anything but the graph would defeat it. The vocabulary that follows this task
defines the roles and the relations.

## What you are given

The paper's claims, each as a slug, its role, the panel it rests on, its epistemic marker and
its sentence, followed by the typed edges of the graph, each written `source --relation--> target`.

## The relations carry the argument

Each edge type is a different argumentative move; use the move the edge names:

- `requires` — the source depends on the target being true. A mechanistic or hierarchical chain.
- `entails` / `derived-from` — hypothesis → prediction, or one hypothesis as the logical
  consequence of another. Deductive. State a `derived-from` hypothesis as a consequence, not an
  independent finding.
- `tests` — an empirical claim tests the prediction it points at.
- `supports` / `refutes` — an empirical result bears on the hypothesis it points at, abductively.
  When `refutes` is present, articulate the refutation explicitly; do not soften it to "is
  consistent with".
- `rules-out` — the source's evidence eliminates an alternative. Argument by elimination; name
  the alternative that was eliminated.
- `dissociates-with` — two claims jointly establish a dissociation. Argument by contrast.
- `validates` — a control or sign-flip strengthens the claim it points at. Argument by
  disconfirmation; surface the control rather than absorbing it.
- `predicts` / `confirms` — predictive validation across a model and an experiment.
- `scopes` — the source is a boundary condition on the target. Qualify, do not overclaim.
- `interprets` — a theoretical or literature claim reframes an empirical one.
- `enables-method` — the source is the methodological capability that warrants the target's
  interpretability.
- `part-of` — the source is a component of the target; the target is the claim to restate, the
  source the comparison, condition or measure beneath it.

Scientific argument combines deduction (`entails`, `derived-from`), induction (`requires`,
`supports`) and abduction (`supports`, `refutes` from observation back to hypothesis). Surface
the hypothetico-deductive structure: hypotheses, the predictions they entail, the tests, and the
support or refutation that closes the loop — not a flat list of findings.

## What to write

- **`synthesis`** — the paper's argument, restated from the graph, 200–400 words, in as many
  paragraphs as the argument needs. Lead with the hypotheses, move through the predictions and
  the evidence that tests them, and end on what is concluded and the scope it is held within.
- **`traceback`** — one entry per sentence of your synthesis, in order, each naming the claims
  and edges that sentence was built from. This is the audit trail: any sentence must be
  followable back to the nodes that produced it. A framing sentence may draw on several claims
  and no edge; an argumentative sentence usually rests on an edge. Use only slugs you were given
  and only edges present in the graph, written exactly `source --relation--> target`.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "synthesis": "The authors argue that … . First, … . Second, … .\n\nEach hypothesis generates …",
  "traceback": [
    {
      "sentence": "The authors argue that interpersonal guilt has a neural substrate in the anterior insula.",
      "claims": ["hypothesis-insula-tracks-interpersonal-guilt"],
      "edges": []
    },
    {
      "sentence": "The insula hypothesis predicts a behavioural guilt effect.",
      "claims": ["prediction-behavioral-guilt-effect"],
      "edges": ["hypothesis-insula-tracks-interpersonal-guilt --entails--> prediction-behavioral-guilt-effect"]
    }
  ]
}
```

`synthesis` is one string (paragraphs separated by `\n\n`). `traceback` is a list; each entry has
`sentence` (a string that appears verbatim in `synthesis`), `claims` (a list of slugs) and
`edges` (a list of `source --relation--> target` strings, possibly empty).
