# Warrant

You are reading one paper's claim tree to judge, for each claim, **how well the tree's argument
supports it** — its *warrant*. Warrant is not what the paper says. The paper's own confidence in
a result is already recorded on the claim (`confidence`), and how the paper stands toward the
claim is its `stance`. Warrant is the separate question the tree lets a reader ask: given the way
the paper's argument hangs together, as the tree records it — the outcomes on its predictions,
the controls that validate it, the rivals it rules out, what supports it and what it depends on —
how much grounds are there to believe it?

**Judge from the argument the tree records — not from the paper's confidence, and not from any
reproduction.** A paper may state a result with certainty while its argument, as the tree holds
it, rests on nothing; that claim is weakly warranted however confidently it was asserted.
Conversely a hedged result whose prediction came out as predicted and which a control validates
is well warranted. Read the argument, not the verb.

**Checking is a separate layer, and it is not yours.** Whether a number reproduced, whether the
methods were sound, whether the statistics hold, whether a citation says what it is cited for —
each of these is assessed by a *later* layer that writes its own modifier beside your warrant. Do
not reason from a reproduction here, even where the tree happens to mention one. You are judging
the argument the paper makes; the checking layers judge whether that argument survives scrutiny,
and they may modify what you said, explicitly. Keep to your half.

## What you are given

Every claim in the tree, each with its sentence, its role, the paper's stance toward it, and its
**dossier** — what the tree's argument holds about its support, rendered readably beneath it:

- the outcome on a prediction (confirmed, refuted, untested), or, for a hypothesis, the outcomes
  on the predictions it commits to;
- the controls that validate it, and the rivals it rules out (or that still stand);
- the claims that support, extend, confirm or refute it;
- what it requires and what it is a part of, with their roles; what it interprets.

A claim whose dossier is empty has nothing in the tree's argument standing behind it. That is a
finding, not an omission to paper over.

## What to judge

For every claim, return its warrant, drawn from the vocabulary its role allows. The levels mean:

- **a prediction** takes an outcome, not a warrant: `confirmed`, `refuted`, or `untested`;
- **an alternative** (a hypothesis the paper raises to reject or entertain) is `ruled-out` when
  the argument eliminates it, or `open` when it still stands;
- **a hypothesis** is `strong` when a prediction it commits to came out as predicted, none was
  refuted, and every rival is ruled out; `moderate` when a prediction was confirmed but a rival
  still stands; `contested` when a prediction it made was refuted; `weak` when no prediction has
  an outcome yet;
- **an empirical, control, methodological or scope claim** is `strong` when it both tests a
  prediction that came out as predicted and is validated by a control; `moderate` when one of
  those holds, or when two or more distinct claims support it; `weak` when the argument does
  little more than assert it; `contested` when another result in the tree refutes it. Argument
  alone — no reproduction enters this;
- **an interpretation** rests on what it interprets: at most `moderate` (an interpretation the
  paper advances is never itself `strong` on argument alone), and weaker as the claims beneath it
  are weaker; `weak` when it interprets nothing graded;
- **a synthesis** reads agreement among what it interprets: `moderate` when it draws two or more
  claims together and none of them is weak; `weak` otherwise;
- a claim's warrant is also **bounded by the weakest claim of its own kind that it requires** — a
  result resting on a weak result is no stronger than what it rests on.

For each, also give:

- `why`: one line, and it **must cite items from the dossier by name** — the prediction outcome,
  the control, the rival ruled out, the supporting or required claim. "Well supported" is not a
  reason; "its prediction `anterior-insula-tracks-guilt-insula` is confirmed and the
  `dot-products` control validates it" is.
- `unsupported`: `true` when the dossier is empty, or when the claim rests on nothing the tree's
  argument records — asserted, with no prediction outcome, no control, no supporting claim. Leave
  it `false` otherwise.

Judge each claim on what its own dossier holds. Do not import the paper's argument for it, do not
reward a confident sentence with a warrant its argument does not earn, and do not credit or
penalise it for a reproduction — that is the checking layer's to weigh.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "warrants": [
    {
      "slug": "anterior-insula-neural-substrate-guilt",
      "warrant": "strong",
      "why": "its prediction anterior-insula-tracks-guilt-insula is confirmed and no rival stands",
      "unsupported": false
    },
    {
      "slug": "during-receipt-lottery-versus-safe",
      "warrant": "weak",
      "why": "asserted; the tree's argument records no prediction outcome, control or support that bears on it",
      "unsupported": true
    }
  ]
}
```

Return one entry per claim you were given, keyed by its slug. A slug you were not given, or a
warrant outside the vocabulary its role allows, is dropped.
