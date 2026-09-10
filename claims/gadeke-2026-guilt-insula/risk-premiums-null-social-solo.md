---
uuid: 5650c9b0-92e0-42da-8772-aa8523bfbd6b
slug: risk-premiums-null-social-solo
doi: ~
claim: >
  Risk premiums do not differ between Solo and Social conditions in either study
  (Study 1: t(39)=1.53, p=0.134, Cohen's d=0.24, BF10=0.49; Study 2: t(43)=−0.21,
  p=0.84, d=−0.03, BF10=0.17), providing evidence against social-context-driven
  changes in risk aversion in this paradigm.
claim-type: empirical
role: control
concepts:
  - risk premium
  - risk aversion
  - social context
  - lottery choice
  - null result
priority: 2026-03-30
epistemic: strong

rules-out:
  - solo-vs-social-choice-difference
validates:
  - insula-tracks-guilt-effect
  - sts-tracks-partner-reward-prediction-errors

belongings:
  - relation: contradicts
    target: solo-vs-social-choice-difference

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig2b, fig2e
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: master_behavAnalysis.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: paired t-tests on risk premium (certainty equivalent approach)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

The risk premium is the simpler and more robust of the two risk preference measures (the other being the EUT/CARA ρ parameter). The null result here qualifies the Study 1 finding that lottery choice was more frequent in the Solo condition: that difference in raw choice rate did not survive when measured against a calibrated risk preference metric. The authors argue this null, together with matched risk premiums across conditions, means the neural signals evoked in Solo vs Social conditions are comparable — an important assumption for interpreting the fMRI contrasts.
