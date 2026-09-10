---
uuid: 0b8f6f71-6251-48b6-9cca-738ba83a4942
slug: alt-signal-from-cross-reactivity
doi: ~
claim: >
  The fluorescence response attributed to iGABASnFR2 reflects binding of, or interference by,
  compounds structurally related to GABA rather than GABA itself, so the reported sensitivity
  is not a measure of GABA detection.
claim-type: interpretive
role: hypothesis
concepts:
  - selectivity
  - cross-reactivity
  - alternative explanation
priority: 2026-09-10
epistemic: weak

assertions:
  - paper-slug: kolb-2026-igabasnfr2
    doi: 10.7554/eLife.108319
    stance: rejects
    method: agent extraction of the alternative addressed by the paper's selectivity panel
    confidence: weak

reproductions: []
---

An alternative the paper argues against, not a proposition it asserts. It is the threat any
biosensor paper must close: that the signal reports something other than the analyte.

`igabasnfr2-gaba-selective-specificity` closes it — structurally related compounds neither
produce a response nor interfere with GABA binding as competitive or non-competitive
antagonists at 1 mM.

That control previously carried `rules-out: igabasnfr2-fourfold-sensitivity-gain`, aimed at the
paper's own headline sensitivity result. A selectivity control does not rule out a sensitivity
gain; it rules out the possibility that the gain measures the wrong thing.
