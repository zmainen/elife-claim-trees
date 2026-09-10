---
uuid: 2b60c032-f0f3-4a4c-8f39-b09a97005d9b
slug: prediction-near-zero-choice-stim-interaction
doi: ~
claim: >
  If serotonergic modulation combines additively with choice-related activity, then a
  generalized linear model fitted to per-neuron trial-by-trial spike counts with separate
  predictors for choice (left/right), 5-HT stimulation (on/off), and their interaction
  (choice × stimulation) should yield a near-zero interaction coefficient when averaged
  across animals and tested against zero with a one-sample t-test.
displayClaim: >
  Additive modulation predicts that the choice-by-stimulation GLM interaction coefficient
  should be near zero across animals.
claim-type: prediction
role: prediction
concepts:
  - generalized linear model
  - interaction term
  - additive modulation
  - one-sample t-test
priority: 2026-04-19
epistemic: prediction
status: confirmed
panel: prediction

derived-from:
  - hypothesis-additive-modulation

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction stated in R1 results (GLM coefficients paragraph)
    confidence: strong

reproductions: []
---

This is the load-bearing R1 prediction that is new relative to v1. The GLM specification (per-neuron, with absolute-valued coefficients for choice and 5-HT to capture magnitude regardless of direction, and an interaction term that captures whether the stimulation effect varies as a function of choice) makes the additive-vs-multiplicative dichotomy operational. Under additive modulation, the interaction coefficient should be statistically indistinguishable from zero. Under multiplicative gain modulation, the interaction coefficient should be significantly different from zero — see `prediction-multiplicative-gain-yields-significant-interaction`. The R1 abstract and results paragraph explicitly state both predictions before reporting the outcome. The prediction is confirmed by `near-zero-choice-by-stim-interaction` (Fig. 6c, mean ± SEM = -0.05 ± 0.06; t(9) = -0.92, p = 0.38).
