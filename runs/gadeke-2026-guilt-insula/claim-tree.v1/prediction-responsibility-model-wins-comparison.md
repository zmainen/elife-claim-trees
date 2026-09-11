---
uuid: 6eb8393f-a95e-4360-91d9-442d08200190
slug: prediction-responsibility-model-wins-comparison
doi: ~
claim: >
  If happiness incorporates partner reward prediction errors with a responsibility-weighted
  rule, then a computational model of happiness that includes a social_pRPE regressor
  (partner RPE × subject-decided indicator) should fit participant happiness ratings
  better than nested alternatives that omit the responsibility interaction. Formally:
  the Responsibility model (and Responsibility Redux model) should achieve lower
  cross-validated error than baseline (own-reward-only) and additive social-utility
  models in both Study 1 and Study 2; and the fitted social_pRPE weight should be
  significantly greater than zero.
displayClaim: >
  The responsibility-weighting hypothesis predicts that a happiness model with a
  social_pRPE × responsibility interaction term outperforms nested alternatives,
  with a positive social_pRPE weight in both studies.
claim-type: prediction
role: prediction
concepts:
  - computational model
  - model comparison
  - responsibility
  - social_pRPE weight
  - cross-validation
priority: 2026-04-20
epistemic: prediction
status: N/A
panel: prediction

derived-from:
  - hypothesis-responsibility-weights-partner-rpes

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction
    confidence: strong

reproductions: []
---

This prediction has two components that the empirical claims test separately: model comparison (`responsibility-modulates-guilt-computational`) and parameter sign (`social-prpe-weight-positive`). The two components are not redundant — a winning model could in principle have a near-zero or negative social_pRPE weight if other terms compensate, so the parameter-level test is a stronger commitment than the model-comparison test. The Wilcoxon sign-rank test on per-participant social_pRPE weights provides the second test independently in both studies. This prediction also enables the model-based fMRI analyses (fig4G/H) by guaranteeing that the trial-by-trial regressors used in GLM2 carry meaningful variance — without a non-zero social_pRPE weight, the STS prediction below would be untestable.
