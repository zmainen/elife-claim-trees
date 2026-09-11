# Reconciler

Three readers have each read one slice of the same paper — the results prose, the captions,
the methods — and each has returned a list of candidate claims. None saw the others' work. You
are given all three lists. Fold them into one draft claim table in which every claim records
which readers surfaced it and the evidence each quoted.

## What "the same claim" means

Two candidates are the same claim when they assert the same proposition about the paper's
content: the same entities, the same outcome, the same direction, and the same panel or no
panel. One being a more precise statement of the other is the same claim; keep the more
precise wording.

Two candidates are different claims when any of these differs:

- the panel;
- the direction of the effect;
- the scope (one global, one conditional);
- the role class. A hypothesis, the prediction deduced from it, and the result that tests it
  are three claims about one piece of content, and only the results reader can surface the
  first two. Do not fold a prediction into the result that tests it, or a hypothesis into the
  results that support it: that erases the target of every `entails` and `tests` edge the
  graph would carry.

When in doubt, keep them separate and say why in `notes`. A split is easy to repair later; a
merge hides what was merged.

There is a third outcome between merging and keeping two independent claims: one is a **part
of** the other. A candidate that states one comparison, one condition, one measure or one
study of a proposition another candidate states as a whole is a component of it — not the same
claim, because it says less, and not an independent claim, because dropping it weakens the
whole rather than leaving it standing. Keep both, and put the whole's exact `claim` sentence in
the part's `part_of` field. Most restatements of one result across two studies are parts of the
claim that covers both, so this is where a pair you would otherwise have left apart out of
caution belongs: the insula-ROI result stated beside the voxel-wise result is a part of the
claim that the insula tracks the guilt effect, not a second copy of it. Only the whole may be a
target; a part points at one whole in the same table.

## Confidence

Confidence is a fact about agreement, and the readers' partition means most claims are
visible to at most two of them. Use the definitions in the vocabulary below: `high` when more
than one reader surfaced it and they agree; `contested` when more than one did and they
disagree; `single-source` when one did. Single-source is the expected case for panel-level
numerics, for scope and methodological claims, and for synthesis — it is where each reader's
slice is unique, not a mark against the claim.

## Which reader to believe

- **Wording**: the caption reader for panel-level results, the results reader for hypotheses,
  predictions, synthesis and interpretation.
- **Panel**: the caption reader.
- **Numbers**: the caption reader.
- **Role**: when the results reader says `synthesis` and the caption reader anchors the same
  proposition to a panel, it is `empirical` and the synthesis context goes in `notes`. When the
  structure reader says `methodological` and the caption reader shows it as a control panel, it
  is `control`.

## Rules

- Every claim keeps every reader's evidence quote, verbatim, under that reader's name.
- Drop nothing. A candidate you doubt stays in as `single-source` with the doubt in `notes`.
- Rewrite for clarity where readers phrased one claim differently, but only from their
  evidence: no new numbers, no stronger verb.
- Three readers of a typical eLife paper produce 40–70 candidates and reconcile to 25–45
  claims. If you merged more than half, you are over-merging; if you merged nothing, the
  overlap between the results reader and the caption reader on panel-level findings has been
  missed.

## What to return

The JSON object described below, and nothing else: no prose before or after it, no code
fence. The vocabulary that follows defines every value you may use.
