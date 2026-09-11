# Abstract ↔ claims

You are aligning a paper's **abstract** with its **claim graph**, in both directions. Of each
abstract sentence you ask which claims carry it; of the claim list you ask which claims no
sentence of the abstract accounts for. The interesting column is the empty one: an abstract is
the paper's own summary of itself, so the difference between the two lists is the difference
between what the paper found and what it advertises.

## What you are given

- **The abstract, cut into numbered sentences.** The numbering is fixed — return each sentence
  under the number it was given.
- **The paper's claims**, each as a slug, its role and its sentence. These are the only slugs you
  may name.

## What to find

For each numbered sentence, its `type`, the claims it carries, and — for a sentence that carries
claims — the `kind` of mapping and a short note on what is preserved or lost.

- **`type`** is one of:
  - `claim` — the sentence states a finding, a hypothesis or a conclusion that maps to one or
    more claims in the graph. Its `claims` list names them.
  - `background` — framing, motivation, prior context, or a bare description of the method that
    states no paper-specific finding. Its `claims` list is empty.
  - `unmappable` — abstract content that ought to map to a claim but finds none in the graph.
    Every `unmappable` sentence is listed in `orphanSentences`, and no other type is.
- **`kind`**, for a `claim` sentence only, is one of:
  - `direct` — the sentence maps cleanly onto one claim.
  - `combined` — the sentence compresses several claims into one statement. Name all of them.
  - `synthesis` — the sentence states a conclusion drawn across claims rather than any single one.
  Leave `kind` off a `background` or `unmappable` sentence.
- **`note`** — one sentence on what the mapping preserves or loses. The revealing case is the
  eliminative move an abstract flattens: a `refutes` stated as "is consistent with", a `rules-out`
  or a `validates` control dropped entirely. Say so when you see it.

Then, across the whole:

- **`orphanClaims`** — the slugs of claims the graph holds that no abstract sentence carries.
  This is usually the long list: the controls, the scope conditions, the eliminated alternatives
  and the fine-grained measures an abstract has no room for.
- **`orphanSentences`** — the numbers of the `unmappable` sentences, and only those.

Assigning a claim to a sentence and leaving it out of `orphanClaims` are the same decision made
from the two ends; a claim named by any sentence is not an orphan.

## What to return

A single JSON object and nothing else — no prose before or after, no code fence:

```json
{
  "sentences": [
    {"n": 1, "type": "claim", "claims": ["hypothesis-insula-tracks-interpersonal-guilt"], "kind": "synthesis", "note": "Framing sentence naming the paper's central bet."},
    {"n": 2, "type": "background", "claims": [], "note": "Describes the two-study design; states no finding."},
    {"n": 3, "type": "unmappable", "claims": [], "note": "Asserts a follow-up no claim in the graph represents."}
  ],
  "orphanClaims": ["risk-premiums-null-social-solo", "guilt-effect-independent-of-own-outcome"],
  "orphanSentences": [3]
}
```

Every numbered sentence appears once in `sentences`, under its given number. `claims` and
`orphanClaims` name only slugs you were given. You need not echo each sentence's text — it is
re-attached by its number.
