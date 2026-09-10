---
uuid: 0219a626-2c4e-48d5-b2e2-2fbd53cbbb38
slug: v2-v3-generalize-shape-not-category
doi: ~
claim: >
  The shape-sensitive, category-insensitive pattern of foveal feedback decoding found in V1 generalizes to foveal regions of V2 and V3, as shown in supplementary figure analyses, suggesting that low-level feature specificity is a property of early visual cortex as a whole rather than V1 specifically.
displayClaim: >
  The shape-sensitive, category-insensitive feedback profile extends to foveal V2 and V3, locating the effect in early visual cortex broadly rather than in V1 alone.
claim-type: empirical
role: empirical
concepts:
  - V2
  - V3
  - early visual cortex
  - generalization
  - shape decoding
  - foveal feedback
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-v1-category-drops-shape-preserved

belongings:
  - relation: supports
    target: hypothesis-feedback-carries-shape-not-category
  - relation: extends
    target: decoding-shape-sensitive-not-semantic
  - relation: extends
    target: v1-category-decoding-drops-in-feedback

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig3-figure-supplement-1
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig3-figsupp1-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: pairwise MVPA decoding in foveal V2/V3 ROIs
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Same pipeline as V1 decoding but with vareas=[2] and vareas=[3] passed
      to prepare_all_data(). Supplementary figure only; no per-area statistics in main text.
      Requires full fMRIPrep → FSL FEAT → MVPA pipeline (~100 CPU-hours). No pre-computed V2/V3
      pairwise results in repo. Two-source confidence (caption, structure); no per-area statistics
      available from text extraction — moderate epistemic status maintained.
---

The caption states the results "generalize" but provides no statistics for V2 and V3 directly. The supplement is described as showing the same pattern. Without per-area statistics, this claim is moderate rather than strong — it relies on the caption assertion of generalization without quantitative confirmation extractable from the full text.
