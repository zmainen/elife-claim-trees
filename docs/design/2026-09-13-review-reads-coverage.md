# The reviewer reads the coverage residue

**Status:** proposed
**Issue:** [#146](https://github.com/zmainen/elife-claim-trees/issues/146)
**Frames:** [#56](https://github.com/zmainen/elife-claim-trees/issues/56) · [#31](https://github.com/zmainen/elife-claim-trees/issues/31)
**Depends on:** the `prepare`, `reconcile`, `external-review`, `coverage`, `adjudication` and `gap-claim` layers; `extract/elife_extract/coverage.py`; `extract/prompts/external-reviewer.md`

The corpus reads a paper top-down and then measures it bottom-up. Three readers and a
reconciler produce a draft; the reviewer patches it; the writer makes a tree; and only then does
`coverage` cut the paper into sentences and ask, of each one that carries a result, which claim
accounts for it. The sentences nothing accounts for go to a judgement layer, then into the
margin, then to `gap-claim`, which drafts a claim for each real gap. This note proposes to run
the bottom-up test once more, earlier, and hand its residue to the one model call that already
reads the whole paper: the external reviewer. The readers are deliberately not given it.

## What the bottom-up test is, and where it runs today

`prepare` numbers every sentence of the paper before any reader runs, and every reader cites
the span its evidence came from. So the accounting is exact from the start: a claim names the
sentence it rests on. What `coverage` adds after the tree is the other direction, a denominator
taken from the paper rather than from the claim set. It cuts the text into spans, keeps the
spans that carry a result (a statistic the segmenter recognises, or a panel name), and marks
each as accounted for when some claim states the same statistic or names the same panel, or as
a candidate orphan when none does. The match is deliberately narrow and mechanical, and the
note on the layer says why: a model that guessed would hide exactly the sentences worth looking
at. On Gädeke the first run left 36 spans unaccounted for, of which the judgement layer found
22 to be the matcher's failures and 14 to be real.

Everything downstream of that number is repair after the fact. The 14 real gaps become
drafted claims, decided one by one in the margin, then promoted into the tree as a later
version. That is the right shape for the residue a reading leaves. It is the wrong shape for
what the reviewer could have caught in one pass, had it known where to look.

## Why not the readers

The obvious move is to give the readers the checklist: here are the sentences that carry a
result, account for each or say why not. It should not be done, for two reasons that the
corpus has already paid for.

The obligation detector is a pattern over statistics and panel names. A checklist built from
it names the numeric sentences and none of the others. The results reader exists to find what
the numbers are for: the organising hypothesis, the predictions, the premises from the
literature, the interpretation. A reader handed a list of numeric sentences and told to account
for them will read toward the numbers, which is what the readers did before the Introduction
and Discussion were put back into their slice, and the losses then were exactly the hypotheses
and premises.

The second reason is grain. A sentence-level checklist anchors the reading at the grain the
prose states things, and that grain is what produced the 42 extra claims that the parts note
had to sort into parts, duplicates and procedure. The readers should read at the grain of the
argument and cite spans; they should not be asked to clear spans.

## The reviewer already reads the whole paper

The external reviewer is given the abstract, the Introduction, the Results, the Discussion and
the captions beside the reconciled draft, and its task is to recover what the readers
systematically miss. Today that task is described in kind: hypotheses, predictions, multi-panel
claims. It is not described in place. The reviewer has to find the misses by reading the paper
against the draft, which is the whole paper against sixty claims, and it patches what it
notices.

Running the obligation test against the reconciled draft, before the reviewer, produces the
list of result-bearing sentences no draft claim accounts for. Handing the reviewer that list,
with the span ids the readers already use, turns "find what was missed" into "here are the
sentences that carry a result and match no claim; for each, either name the draft claim that
covers it, add the claim it needs, or say it asserts nothing". Those are the three verdicts
the judgement layer returns today, made by the reviewer at the moment it can act on them, with
the paper in front of it.

The reviewer's grain problem is smaller than the readers' because it is revising a draft, not
producing one. A span it decides to cover becomes a claim in the draft's vocabulary, folded by
the same rules the reconciler uses, and the reviewer is told, as it is now, that a component of
an existing claim is a part and not a new claim.

## What changes

A `review-coverage` step, mechanical, between `reconcile` and `external-review`: it runs the
span match from `coverage.py` against the reconciled draft rather than the tree, and writes
`runs/<paper>/review-coverage.json`, the unaccounted spans with their ids and text. It needs
`reconcile` and `prepare`, reads `coverage.py`, and costs nothing. `external-review` gains it as
a need and its task file gains a section: the list, the three verdicts, and the rule that a
span it covers by adding a claim must cite that span. The review patch format already carries
added claims; it gains a per-span verdict so that the decision is recorded and not only its
effect.

`coverage`, `adjudication`, `marks` and `gap-claim` are unchanged and still run after the tree.
What they measure becomes the residue of a reading that was told where to look, which is the
number the corpus actually wants: not how much the readers missed, but how much survived the
reviewer. On Gädeke the prediction is that the 14 real gaps fall to a handful, and that the 22
matcher failures stay, since they are the matcher's and not the reading's.

## What this does not decide

Whether the reviewer's per-span verdicts should feed the later judgement layer, so that a span
the reviewer said asserts nothing is not asked again after the tree. It should, and it is a
small change to `adjudication`, but it is a second step.

Whether the same list should go to the reconciler instead, one step earlier. The reconciler
does not read the paper; giving it the list would make it a reader, which is the thing this
note argues against.

## Cost

The step and the task section: half a day. Re-running the reviewer on Gädeke, answered by a
subagent: an hour. The readers are not re-run, which is the point.
