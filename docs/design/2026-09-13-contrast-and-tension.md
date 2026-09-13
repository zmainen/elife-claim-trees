# Contrast and tension: two relations where the corpus had one

**Status:** proposed
**Issue:** [#125](https://github.com/zmainen/elife-claim-trees/issues/125)
**Frames:** [#19](https://github.com/zmainen/elife-claim-trees/issues/19) · [#31](https://github.com/zmainen/elife-claim-trees/issues/31)
**Depends on:** `scripts/relations.py`, `scripts/export_mira.py`, `extract/elife_extract/oxa.py`, `scripts/check_relations.py`, the archived trees under `runs/*/claim-tree.v1/`

The ruling on #19 was that `dissociates-with` has been used for two different things, a neutral
contrast between results and a tension between them, and that the corpus should be able to say
both. This note proposes the two definitions, re-reads the twelve pairs that made the issue
visible to say which is which, and fixes what the exporters and the linter do with each.

## How one relation came to carry two meanings

The relation was defined as "the source result separates two things the destination claim
joins", which is a mild opposition, and the MIRA export declared it under `mira:opposes` on that
reading. The trees then used it 65 times, and the twelve cases where it sat beside `supports` or
`extends` on the same pair were the symptom: a claim cannot both support a target and oppose it
unless the word is doing something other than opposing. The contract work of #56 redefined it as
symmetric and non-opposing, "the source and target jointly establish a dissociation", which
matched most of the uses and none of the exports.

Today the corpus has 59 edges of this relation and none of them sits beside a positive edge. The
twelve pairs are gone because the trees that carried them were re-induced under the new
definition. That is not a resolution. The induction chain now writes the relation rarely
(Gädeke v3 has one edge where v1 had many), and a reading of the archived pairs shows that some
of what was lost was a real thing the new definition no longer names.

## The twelve pairs, re-read

Eight are contrasts, where two results differ on a condition, region, population or measure and
the difference is the finding. Neither bears on the other's truth:

- artiushin: the hagstone neuropil is serotonergic; the tonsillar neuropil is a novel structure.
- bouyeure: item stability does not differ between CS+ and CS−; generalisation across items
  increases for CS+. The null sharpens the positive result rather than pulling against it.
- gadeke: being the decision-maker reduces happiness regardless of outcome; guilt reduces it
  after the partner's loss. Two effects, both present, the second over and above the first.
- kammer: LO shows the reverse of V1's pattern. The reversal is the finding.
- rozak, three pairs: an artery dilates while a venule does not; constrictions lie deeper than
  dilations; dilations lie nearer neurons than constrictions. Spatial regularities side by side.
- kolb: on-cell affinity is sevenfold higher; sensitivity gain is fourfold. Two measurements of
  the same improvement.

Four are tensions, where both results stand and pull a shared implication in opposite
directions, or cannot be jointly explained without a further claim:

- gadeke: the insula guilt effect matches the published guilt signature at the group level, and
  individual signature scores do not correlate with individual guilt effects. The replication is
  real and the null bounds what it can mean.
- kolb: iGABASnFR2 rises faster than its predecessor and decays slower. A trade-off: the
  sensitivity gain is bought partly with temporal resolution.
- rozak: the ensemble beats ilastik on surface distance, and ilastik has higher recall. Two
  metrics disagree about which segmentation is better.
- wengert: PV interneurons show impaired maximal firing, and in layer V the impairment is confined
  to the largest current injections. A general claim and a layer that mostly escapes it.

The two kinds want different verbs. "Whereas", "in contrast", "selectively" mark a contrast.
"Although", "however", "despite", "no correlation with", "at the cost of" mark a tension.

## The proposal: two symmetric relations

**`dissociates-with`** keeps its current definition. Symmetric, between two empirical claims the
paper asserts, whose difference across a condition, region, population or measure is itself a
finding. Neither claim bears on the truth of the other. It is not an opposition and does not
belong under `mira:opposes`.

**`in-tension-with`** is new. Symmetric, between two claims the paper asserts, both of which
stand, that pull a shared implication in opposite directions or cannot be jointly explained
without a further claim. It is distinct from three neighbours, and the contract carries the
distinctions as confusable pairs:

- `contradicts` says two claims cannot both hold. A tension says both do.
- `qualifies` is directional: one result narrows the applicability of another. A tension has no
  narrower side; the wengert case is arguably a qualification and the note leaves it to the
  reader, which is what the confusable text should say.
- `rules-out` eliminates an alternative the paper raised in order to reject. A tension is between
  two claims the paper asserts.

The paper usually resolves a tension in its discussion with a synthesis or interpretation claim,
and that claim `interprets` both. A tension with no such claim is a gap the coverage layer can
report, which is a small later addition and not part of this ruling.

## Exports and the linter

`dissociates-with` leaves `mira:opposes`. MIRA has no predicate for a contrast, so it goes where
`part-of` and `entails` go, the `haak:` namespace of the extended export, and the gap report says
so. OXA's `cito:disagreesWith` is wrong for the same reason and is replaced by the nearest neutral
predicate the OXA mapping offers, or dropped with a line in the formats report.

`in-tension-with` is the harder call and the note does not make it. `mira:opposes` would let a
MIRA reader see friction in the graph, at the cost of saying more than the relation means. The
extended export can carry it exactly. The recommendation is the extended export only, and the
issue is where to argue for `mira:opposes` instead.

With both definitions written, the rule #19 asked for becomes sound: a source may not both
support a target and `contradicts`, `rules-out` or `refutes` it. Neither of the two relations
here is in that set. `in-tension-with` beside `supports` is allowed, because a result can support a
hypothesis and be in tension with another result. The 72 cases the linter holds in review close
as fine.

## What changes, and what is re-run

`relations.py` gains the definition, direction rule, example and the three confusable pairs;
`docs/method.md` the row; the contract regenerates. The edge-inference task asks for both. The
exporters change as above. None of the 59 current edges is re-typed by this note; on my reading
all are contrasts. The four tensions live in archived trees, and writing them back is part of
each paper's next reading: the Gädeke case is one verdict in the v3 adjudication, `missing`
with the relation named.

Every tree's edge-inference goes stale when the vocabulary changes, and the re-runs are runs.

## Cost

Definitions, contract and exports: half a day. The linter rule and closing the review list: an
hour. Nothing is re-induced for this note alone; the next induction picks it up.

## What this does not decide

The MIRA parent for `in-tension-with`, above. Whether the wengert case is a tension or a
qualification, which is a reading rather than a rule. Whether an unresolved tension should be
reported as a gap.
