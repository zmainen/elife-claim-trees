---
uuid: 1f154108-1ed9-4084-935a-6ef65adc2418
slug: social-prpe-weight-positive
doi: ~
claim: >
  The weight on partner reward prediction errors resulting from participant choices
  (social_pRPE) is significantly greater than zero in both the Responsibility model
  (Study 1: Z=2.85, p=0.004; Study 2: Z=3.26, p=0.001) and the Responsibility Redux
  model (Study 1: Z=2.93, p=0.003; Study 2: Z=3.30, p=0.001), demonstrating that
  participant-caused partner RPEs independently influence participant happiness.
claim-type: empirical
role: empirical
concepts:
  - reward prediction error
  - responsibility
  - computational model
  - partner RPE
  - happiness
priority: 2026-03-30
epistemic: strong

tests:
  - hypothesis-responsibility-weights-partner-rpes
confirms:
  - hypothesis-responsibility-weights-partner-rpes

belongings:
  - relation: supports
    target: responsibility-modulates-guilt-computational
  - relation: supports
    target: guilt-reduces-happiness-after-partner-loss

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig3c, fig3g, table1
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: master_behavAnalysis.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: Wilcoxon sign-rank test on model weights (non-normal distribution)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

This is the parameter-level claim supporting the model-comparison claim. It is distinct from the model comparison claim (Responsibility model beats others) because it directly establishes that the social_pRPE regressor carries positive weight — i.e., that unexpected bad partner outcomes from one's own choices reduce happiness, not just that the model with this term fits better. The paper also reports a trend for social_pRPE weights being higher than partner_pRPE weights (Study 1: Z=2.14, p=0.033; Study 2: Z=1.41, p=0.16), though this is not consistently significant across studies.
