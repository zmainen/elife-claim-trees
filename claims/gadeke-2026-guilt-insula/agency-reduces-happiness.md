---
uuid: 8edb5949-b433-496e-8d9f-1f10df952ddc
slug: agency-reduces-happiness
doi: ~
claim: >
  Being the decision-maker (Social + Solo vs Partner condition) reduces participant
  happiness independently of outcome (Study 1: t(3600)=−3.92, p<0.0001, β=−0.14,
  95%CI=[−0.20, −0.07]; Study 2: t(2870)=−6.07, p<0.0001, β=−0.24, 95%CI=[−0.31, −0.16]),
  consistent with a psychological cost of assuming responsibility for others.
claim-type: empirical
role: empirical
concepts:
  - agency
  - responsibility aversion
  - happiness
  - decision-making
  - social choice
priority: 2026-03-30
epistemic: strong

dissociates-with:
  - guilt-reduces-happiness-after-partner-loss

belongings:
  - relation: supports
    target: guilt-reduces-happiness-after-partner-loss

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig3 (text, no dedicated panel)
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: master_behavAnalysis.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: linear mixed model (LMM) on z-scored happiness ratings
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

This is a distinct empirical claim from the guilt effect. The guilt effect is specifically about low partner outcomes under participant choice; this agency effect is a main effect of being the decision-maker regardless of trial outcome. The authors interpret this as a form of responsibility aversion (cf. Edelson et al. 2018), where the weight of responsibility itself is aversive even before outcomes are revealed. This claim has no dedicated figure panel — it appears in the Results text — making it a single-source (A) claim from the Results reading, though the statistics are unambiguous.
