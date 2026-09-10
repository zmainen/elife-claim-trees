---
uuid: 69cad10c-46f3-4f7e-8cec-3c9de1c629de
slug: responsibility-modulates-guilt-computational
doi: ~
claim: >
  A computational model incorporating responsibility-modulated happiness better accounts for the behavioral guilt effect than models without responsibility weighting, providing formal parameterization of the social decision-making component.
claim-type: empirical
role: empirical
concepts:
  - computational model
  - responsibility
  - happiness
  - model comparison
  - guilt
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-responsibility-model-wins-comparison
confirms:
  - hypothesis-responsibility-weights-partner-rpes
interprets:
  - social-prpe-weight-positive
enables-method:
  - sts-tracks-partner-reward-prediction-errors
  - ventral-striatum-tracks-computational-reward

belongings:
[]

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig3, table1
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Code/behavioural analysis scripts
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: computational model fitting (expected utility + responsibility parameter)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Computational model code in GitHub repo. Behavioral data in BehaviouralData/ directory (.mat files). MATLAB required. Not yet executed.
---


