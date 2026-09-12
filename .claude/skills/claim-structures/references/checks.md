# Checks

Run these before handing over any claim structure, whether you built it or are auditing someone
else's. They are ordered by how often they catch something real.

## Structural errors

These are errors, not style. Each one makes the graph assert something false.

1. **An opposing edge aimed at an asserted claim.** `rules-out`, `contradicts` and `opposes` may
   not target a claim the same paper asserts. The cause is almost always a missing alternative
   node, and the fix is to author it — never to redirect the edge. (`refutes` at the paper's own
   prediction is legal and correct.)
2. **A dangling target.** An edge naming a slug no claim has. Either the target was never
   written or the slug was renamed and the edge not followed. `scopes: ["*"]` is the one legal
   non-slug target.
3. **Both supporting and opposing the same target.** A pair carrying, say, `supports` and
   `rules-out` cannot both be meant. (`dissociates-with` alongside `supports` is the known
   ambiguous case — flag it for review rather than failing it.)
4. **`stance: attributes` with no source.** An attributed claim must say who asserts it.
5. **An unknown stance, role, claim-type, relation or status.** The vocabularies are closed.
   Inventing a value hides the claim from every query written against the schema.
6. **A number in a claim sentence that is not in the source.** The one defect a reader cannot
   detect. Re-check every value against the text it came from.
7. **A fabricated identifier.** A guessed DOI, a hand-written UUID, a panel id that is not the
   publisher's. Generate UUIDs properly; leave `doi: ~`.

In a corpus with the tooling:

```bash
python3 scripts/check_relations.py          # stance and edge legality, all papers
python3 scripts/check_relations.py --warnings <paper>
make check
```

## Structural smells

Not errors — read each one and decide.

| Smell | Usually means |
|:------|:--------------|
| a control with no `rules-out` | the alternative it eliminates has no node |
| an alternative (`entertains`) with no incoming `rules-out` | an open rival — legitimate, but say so deliberately |
| a prediction with no incoming `tests` | an untested commitment |
| an empirical claim with no outgoing edges | an orphan result, or a missing hypothesis |
| a hypothesis with one `entails` | a single point of contact with the world |
| no `scope` claims anywhere | boundaries unexamined, not absent |
| no `requires` edges | the dependencies are real and unwritten |
| every edge is `supports` | no deductive spine; nothing entails and nothing tests |
| a synthesis with one `supports` | an integration of one thing |
| two claims with near-identical sentences | one claim, or a whole plus a `part-of` component |
| a claim needing two sentences | two claims |
| an `interprets` edge doing a derivation's work | the reconstruction overstates what was shown |

## Direction check

Walk every edge and read it aloud as a sentence. The direction is wrong more often than the
type:

- `A entails B` — "if A holds, B follows." A is the hypothesis, B the prediction.
- `A tests B` — "measuring A settles B." A is the result, B the prediction.
- `A rules-out B` — "A's evidence eliminates B." B is a rival the paper does not assert.
- `A requires B` — "A would be invalid if B were false." A is the dependent claim.
- `A scopes B` — "A bounds what B can mean." A is the boundary condition.
- `A supports B` — "A is evidence for B." A survives B being false.
- `A part-of B` — "A is one component of what B states whole."

## The reconstruction test

The one check that catches what the others miss: read the claim sentences and the edges, with
the paper closed, and write the argument out in a paragraph. Then compare it to the abstract.

- If your paragraph reconstructs the argument, the graph is sound.
- If it reconstructs something *more* than the abstract — the eliminated alternatives, the
  controls, the scope — that is expected and is the point.
- If it reconstructs something *less*, or something different, the edges are wrong. Find the
  step your paragraph could not make and look at the claims on either side of it.

## Reporting

State in the handoff what you could not settle: reconstructed hypotheses and predictions,
single-source readings, numbers not found verbatim, alternatives you paraphrased, coverage gaps,
and every place you guessed. A structure whose uncertainties are unreported is not a finished
structure — it is an unreviewed one, and it reads as finished, which is worse.
