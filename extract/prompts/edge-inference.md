# Edge inference

You are mapping the logical structure of one paper's claim table: the typed relations that hold
between its claims. This is the deductive spine — a hypothesis entailing its predictions, an
empirical result testing one back — together with the scope constraints, the dependency chains,
and the compositions that hold the argument together. The claims are given; the edges between
them are what you return.

Relations are named in the corpus's own vocabulary, defined in full in the vocabulary that
follows this task — not CiTO, not claimrel, just the bare relation names. Each relation is
directed, and the direction rule stated beside its definition is binding: an edge that points
the wrong way is wrong even when the two claims are genuinely related. Read the definitions and
the confusable-pair notes before you begin — `requires` is not `supports`, `entails` is not
`tests`, `part-of` is not `supports`, `rules-out` is not `refutes`.

## What you are given

The paper's claims, numbered. Refer to a claim only by its number — never by a slug and never by
a paraphrase. Each claim is shown with its role, the panel it rests on, the paper's stance toward
it, its full sentence, the span id its evidence was drawn from where the draft records one, and
the verbatim evidence quotes the readers gave. Reason only from what is there. A relation you
cannot defend from this digest is one you should not write.

## What to return

One edge per line, each a single JSON object and nothing else — no prose before or after, no code
fence:

```
{"source": 12, "target": 3, "relation": "tests", "why": "one sentence, citing a span id where the digest shows one"}
```

- `source` and `target` are claim numbers. The edge runs from source to target in the direction
  the vocabulary states for that relation.
- `relation` is one of the corpus relation names. Never emit `derived-from` or `confirms`: they
  are written mechanically as the reciprocals of `entails` and `predicts`, so emitting them by
  hand double-counts the same deduction.
- `why` is one sentence saying why the edge holds, defensible from the digest, and citing the
  span id (for example `results-026`) wherever the claim it rests on shows one.

## The rules the direction checks enforce

These are checked mechanically after you answer; an edge that breaks one is dropped rather than
written, so do not spend an edge on it.

- **`tests`** runs from an empirical result or a control to the **prediction** it checks. Never
  from the prediction, and never aimed at a hypothesis.
- **`entails`** runs from a **hypothesis** to a prediction it deductively implies. An empirical
  result never entails anything.
- **`scopes`** runs from a **scope** claim to the claims it bounds, or to `*` for every empirical
  claim in the paper.
- **`rules-out`, `contradicts`, `opposes`** may target only a claim the paper does **not** assert
  — one whose stance is `entertains` or `rejects`. A paper does not rule out what it claims; if
  every stance in the digest reads `asserts`, emit none of these, and let the alternative it
  eliminates get its own node later.
- **`part-of`** is composition, not evidence: the source states one comparison, condition, measure
  or study of a proposition the target states as a whole. An independent finding that supports a
  claim is not a part of it. A part points at exactly one whole, and the chain of wholes may not
  close a cycle.

It is better to miss an edge than to invent one. Return only the edges you can defend from the
digest.
