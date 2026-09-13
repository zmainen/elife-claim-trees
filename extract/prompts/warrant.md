# Warrant

You are reading one paper's claim tree to judge, for each claim, **how well the tree supports
it** — its *warrant*. Warrant is not what the paper says. The paper's own confidence in a result
is already recorded on the claim (`confidence`), and how the paper stands toward the claim is its
`stance`. Warrant is the separate question the tree lets a reader ask: given the evidence the
tree actually records — the outcomes on its predictions, the controls that validate it, the
alternatives it rules out, the reproductions that re-ran its numbers, what it depends on — how
much grounds are there to believe it?

The basis for your judgement is **the tree's evidence, not the paper's confidence**. A paper may
state a result with certainty and the tree may hold nothing that checks it; that claim is weakly
warranted however confidently it was asserted. Conversely a hedged result that a control
validates and a reproduction confirms is well warranted. Read the dossier, not the verb.

One thing to weigh carefully. A `verified` reproduction means someone re-ran the paper's own
code on the paper's own data and **the number came out the same**. It checks a number; it does
not check the inference the paper drew from that number. A reproduced coefficient does not
establish that the coefficient means what the paper says it means. So when a claim's warrant
rests on a `verified` reproduction, say in your `why` what the verification actually establishes
for *this* claim — the number, or the reading of it.

## What you are given

Every claim in the tree, each with its sentence, its role, the paper's stance toward it, and its
**dossier** — what the tree holds about its support, rendered readably beneath it:

- the outcome on a prediction (confirmed, refuted, untested), or, for a hypothesis, the outcomes
  on the predictions it commits to;
- controls that validate it, and alternatives it rules out;
- reproduction records and their status, and, where a run was observed, the verification
  provenance — the number the paper reported and the number the re-run produced;
- what it requires and what it is a part of; the claims that support or extend it.

A claim whose dossier is empty has nothing in the tree standing behind it. That is a finding, not
an omission to paper over.

## What to judge

For every claim, return its warrant, drawn from the vocabulary its role allows:

- **a prediction** takes an outcome, not a warrant: `confirmed`, `refuted`, or `untested`;
- **an alternative** (a hypothesis the paper raises to reject or entertain) is `ruled-out` or
  `open`;
- **every other claim** takes `strong`, `moderate`, `weak`, or `contested`.

For each, also give:

- `why`: one line, and it **must cite items from the dossier by name** — the reproduction, the
  control, the prediction outcome, the required claim. "Well supported" is not a reason; "the
  `insula-rois` result confirms it and the `dot-products` control validates it" is. Where the
  warrant rests on a `verified` reproduction, say what that verification establishes for the
  claim.
- `unsupported`: `true` when the dossier is empty, or when the claim rests on nothing the tree
  records — asserted, with no reproduction, no control, no test, no outcome. Leave it `false`
  otherwise.

Judge each claim on what its own dossier holds. Do not import the paper's argument for it, and do
not reward a confident sentence with a warrant its evidence does not earn.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "warrants": [
    {
      "slug": "anterior-insula-neural-substrate-guilt",
      "warrant": "strong",
      "why": "its prediction anterior-insula-tracks-guilt-insula is confirmed by the insula-rois and mass-univariate results",
      "unsupported": false
    },
    {
      "slug": "during-receipt-lottery-versus-safe",
      "warrant": "weak",
      "why": "asserted; the tree records no reproduction, control or test that bears on it",
      "unsupported": true
    }
  ]
}
```

Return one entry per claim you were given, keyed by its slug. A slug you were not given, or a
warrant outside the vocabulary its role allows, is dropped.
