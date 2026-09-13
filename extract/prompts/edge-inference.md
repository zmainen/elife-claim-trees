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
`tests`, `part-of` is not `supports`, `rules-out` is not `refutes`, `confirms` is not
`supports`.

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
- `relation` is one of the corpus relation names. Never emit `derived-from`: it is written
  mechanically as the reciprocal of `entails`, so emitting it by hand double-counts the same
  deduction.
- `why` is one sentence saying why the edge holds, defensible from the digest, and citing the
  span id (for example `results-026`) wherever the claim it rests on shows one.

## Every tested prediction carries its outcome

A `tests` edge is neutral: it records that a result bears on a prediction, not which way the
test came out. That verdict is the point of the test, so it must be written down. For **every**
`tests` edge you emit, from a result to a prediction, emit an outcome edge beside it, from the
same result to the same prediction:

- `confirms` — the result came out the way the prediction said it would.
- `refutes` — the result came out against the prediction.

Read the evidence quotes to decide which; a `tests` edge with no `confirms` or `refutes` beside
it leaves the prediction a waypoint with no verdict on it, and the linter flags it.

Outcomes aim at **predictions only**. A result that bears on a hypothesis does not `confirms`
or `refutes` it — it `supports` the hypothesis (or `rules-out` an alternative). If a result
came out against a hypothesis, write the prediction the hypothesis entails and refute that
prediction; do not aim `refutes` at the hypothesis.

## Look for tensions between results the paper asserts

After the outcome edges, go back through the results the paper asserts and look deliberately for
**tensions**: two claims, both of which stand, that pull a shared implication in opposite
directions, or that cannot be jointly explained without a further claim. This is not a contrast,
where two results simply differ across a condition, region, population or measure and the
difference is the finding (that is `dissociates-with`). A tension is marked by “although”,
“however”, “despite”, “no correlation with”, “at the cost of” — a replication that holds at the
group level while the individual-level null bounds what it can mean; a gain bought at the cost of
a resolution; two metrics that disagree about which method is better. Where you find one, write:

```
{"source": 12, "target": 7, "relation": "in-tension-with", "why": "one sentence"}
```

`in-tension-with` is symmetric — write it once per pair. It holds only between two claims the
paper **asserts**; it is not `contradicts` (both claims hold), not `qualifies` (neither narrows
the other), and not `rules-out` (nothing is eliminated). Do not fail to surface a real tension:
a paper usually resolves one in its discussion, and an unresolved one is a gap worth seeing.

## Look for unsupported parts of the argument

Then look for parts of the argument that rest on nothing: a hypothesis with no prediction tested,
a prediction with no result testing it, an empirical claim with no evidence behind it. These are
not edges — they are the *absence* of one — so mark each on its own line, one object per claim,
alongside the edge lines:

```
{"unsupported": 4, "reason": "hypothesis with no tested prediction"}
```

`unsupported` is the claim's number (or slug); keep each reason to one clause. This is the other
half of the reading the ruling asks for: we do not want to fail to surface these.

## Complete the tree: every claim rests on something, or stands alone

Now go back over the whole tree one more time. This is a completion pass, not a fresh reading:
the spine is written, the outcomes are on it, the tensions are marked — what is left is to
account for every claim that the reading so far has not connected to any other.

For **every** claim that has no `supports`, `extends`, `validates`, `confirms`, `refutes`,
`tests`, `rules-out`, `part-of` or `interprets` edge in *either* direction — nothing pointing at
it and nothing it points at, across all of those relations — do one of two things:

- **Write the edge.** Say what the claim rests on, or what rests on it: the result that a
  methodological choice makes interpretable, the finding a claim supports, the whole a
  measurement is a part of, the prediction a result tests. Name the relation from the vocabulary,
  point it the way the vocabulary's direction rule states, and cite the span that shows it — a
  completion edge is held to the same standard as any other. Most unconnected claims have a real
  place in the argument that the spine reading simply did not reach: a control validating a
  result, a scope bounding one, an empirical finding supporting the hypothesis it was run under.
- **List it as unsupported.** If, having looked, the claim genuinely rests on nothing the paper
  says and nothing rests on it, mark it on its own line, exactly as in the section above, with a
  reason of one line saying it stands alone in the paper's argument:

```
{"unsupported": 9, "reason": "stands alone — no claim in the paper bears on it or rests on it"}
```

This is a pass to *find the edges the tree already has and did not write down*, not a licence to
invent connections. An edge you cannot cite a span for is an edge you should not write; when the
honest answer is that a claim stands alone, that absence is itself a finding, and listing it
under `unsupported` is the right move. It is better to mark a claim unsupported than to wire it
to a neighbour it has no real relation to.

## The rules the direction checks enforce

These are checked mechanically after you answer; an edge that breaks one is dropped rather than
written, so do not spend an edge on it.

- **`tests`** runs from an empirical result or a control to the **prediction** it checks. Never
  from the prediction, and never aimed at a hypothesis.
- **`confirms`, `refutes`** run from the empirical result or control to the **prediction** whose
  test they settle — `confirms` when it came out as predicted, `refutes` when it came out
  against. Both are aimed at a prediction only; aimed at a hypothesis they are dropped.
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
