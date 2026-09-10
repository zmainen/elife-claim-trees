---
uuid: af22eed8-ee48-4772-9294-94abc7fb74cc
slug: guilt-effect-independent-of-own-outcome
doi: ~
claim: >
  The guilt effect (happiness decrease after low partner outcomes under participant
  vs partner choice) is present regardless of whether the participant received the high
  or low lottery outcome: high own outcome: Study 1 t(39)=−3.58, p<0.001, d=0.56,
  BF10=32; Study 2 t(43)=−2.68, p=0.01, d=0.40, BF10=3.8; low own outcome: Study 1
  t(39)=−3.39, p=0.002, d=0.54, BF10=19; Study 2 t(43)=−3.58, p<0.001, d=0.54, BF10=33.5.
claim-type: empirical
role: control
concepts:
  - guilt
  - interpersonal emotion
  - own outcome
  - other outcome
  - responsibility
priority: 2026-03-30
epistemic: strong

rules-out:
  - alt-guilt-effect-driven-by-own-outcome
validates:
  - guilt-reduces-happiness-after-partner-loss
  - hypothesis-insula-tracks-interpersonal-guilt
dissociates-with:
  - happiness-correlates-partner-reward

belongings:
  - relation: extends
    target: guilt-reduces-happiness-after-partner-loss

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig3d, fig3h
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: master_behavAnalysis.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: paired t-test within participants (binned by own outcome × decision-maker)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

This specificity claim is important for interpreting the guilt operationalization. Guilt is sometimes confounded with regret (about one's own bad outcome) or empathy (about the partner's bad outcome regardless of responsibility). The finding that guilt effect persists when the participant won (high own outcome) rules out that the effect is driven by shared loss or personal regret. The Bayes factors are notably strong for both own-outcome conditions in both studies, making this one of the more robust behavioral claims in the paper.
