---
uuid: 5476d15d-5249-43b3-a1db-ec0fa4ede39b
slug: decoding-shape-sensitive-not-semantic
doi: ~
claim: >
  Foveal V1 feedback contains low-to-mid-level visual information (shape-sensitive) but not higher-level semantic category information (animal vs instrument not decodable), indicating that feedback signals represent low-level feature properties of the saccade target.
displayClaim: >
  Foveal feedback carries low-to-mid-level shape information but not semantic category, identifying the feedback content as visual features of the saccade target rather than its identity.
shortClaim: "Foveal feedback carries low-to-mid-level shape, not semantic category."
claim-type: empirical
role: synthesis
concepts:
  - shape decoding
  - semantic category
  - low-level features
  - foveal V1
  - feedback content
priority: 2026-03-30
epistemic: moderate

derived-from:
  - v1-category-decoding-drops-in-feedback
  - lo-shows-reversed-specificity
  - v2-v3-generalize-shape-not-category
interprets:
  - hypothesis-feedback-carries-shape-not-category

belongings: []

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig3
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: category-specific decoding, MVPA
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Interpretive claim synthesized from fig3 (V1) and fig3B (LO) pairwise
      decoding results. Requires the full fMRIPrep + FSL FEAT + MVPA pipeline on ds005933 (61 GB).
      Pairwise decoding (shape pairs: horn vs guitar, tiger vs kangaroo; category pairs: horn vs tiger,
      guitar vs kangaroo) uses decoding_shape_category.ipynb with comparison='shape' and comparison='category'
      branches. No pre-computed pairwise decoding matrices in repo. Same pipeline as within-condition
      decoding; ~100 CPU-hours minimum.
---
