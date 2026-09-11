---
uuid: 88edff87-3bea-4030-bdf5-fb172865c445
slug: hypothesis-responsibility-weights-partner-rpes
doi: ~
claim: >
  Momentary happiness in social decision contexts is governed by a computational rule
  in which partner reward prediction errors that arise from the participant's own
  choices (social_pRPEs) carry an independent, non-zero weight, distinct from the
  weight on partner RPEs that arise without participant agency. Responsibility
  modulates how partner outcomes enter the happiness computation: participants
  internalize partner losses as affective costs specifically when those losses can
  be attributed to their own decision.
displayClaim: >
  Happiness incorporates partner reward prediction errors with a responsibility-weighted
  rule — partner RPEs caused by the participant's own choices receive an independent,
  non-zero weight in the happiness computation.
shortClaim: "Happiness weights partner reward prediction errors by the subject's responsibility."
claim-type: hypothesis
role: hypothesis
addresses: q2
concepts:
  - computational happiness model
  - reward prediction error
  - responsibility weighting
  - guilt
  - social decision
priority: 2026-04-20
epistemic: hypothesis
status: N/A
panel: hypothesis

entails:
  - prediction-responsibility-model-wins-comparison
  - prediction-behavioral-guilt-effect

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: hypothesis stated in introduction and modelling section
    confidence: N/A

reproductions: []
---

This is the computational formulation of the guilt hypothesis. Where `hypothesis-insula-tracks-interpersonal-guilt` is anatomical, this hypothesis is algebraic: it commits to a particular structural form for the happiness equation in which a `social_pRPE` regressor (partner RPE × subject-decided indicator) carries non-zero weight separable from the regressor for partner RPEs without responsibility. The Responsibility model and Responsibility Redux model in the paper instantiate this hypothesis. It is dissociable from a simpler social-utility hypothesis in which partner outcome enters happiness with a single weight regardless of who chose; the responsibility hypothesis predicts that the model with the social_pRPE × responsibility interaction outperforms the model without it. This hypothesis also enables the model-based fMRI analysis in fig4G/H — it provides the regressors against which BOLD is correlated.
