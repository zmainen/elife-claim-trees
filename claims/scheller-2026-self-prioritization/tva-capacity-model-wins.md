---
uuid: 24c24fef-2404-41a6-a0ea-edfe81cd3707
slug: tva-capacity-model-wins
doi: ~
claim: >
  Model comparison via leave-one-out cross-validation shows that a model with condition-specific
  processing capacity parameters outperforms a single-capacity model (Δloo=14.2, Δse=6.41,
  weight=0.86 pooled across N=140 participants), indicating that social salience changes absolute
  processing rates rather than merely redistributing attentional weights.
claim-type: assessment
role: methodological
concepts:
  - TVA model comparison
  - processing capacity
  - model selection
  - leave-one-out cross-validation
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-capacity-model-outperforms-weights-only
confirms:
  - hypothesis-capacity-mechanism-not-weights
interprets:
  - interprets-bundesen-tva-framework
enables-method:
  - self-prioritization-perceptual-decision-automatic
  - self-prioritization-absent-social-decision
  - processing-capacity-rises-perceptual-self
  - other-association-advantage-social-condition
  - perceptual-salience-6hz-advantage
  - self-social-additive-perceptual
  - self-salience-reduces-perceptual-benefit

belongings: []

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig4
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: OSF analysis notebooks (https://osf.io/a62df)
    dataset: https://osf.io/a62df
    dataset-doi: ~
    method: hierarchical Bayesian model comparison (Stan/R), LOO-CV
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Data and pre-computed posteriors accessible on OSF (https://osf.io/a62df).
      The Δloo value (14.2) and weight (0.86) require loading the Stan posterior trace
      files (.nc, ~2-5 GB each) and running az.compare() or loo::loo_compare() on the
      two model objects. The estimates_single_C.csv and estimates_indiv_C.csv confirm
      both models ran and converged (r_hat < 1.01 throughout). The indiv_C model has
      more parameters and produces the quantitative results verified in other claims.
      LOO comparison itself not yet executed — requires Stan posterior samples.
---

This model comparison is methodologically central: it determines the mechanism underlying the behavioral effect. A relative-weight-only model would imply that the brain redistributes fixed attentional resources toward self-associated stimuli; the capacity model implies that self-association actually mobilizes additional processing resources. The Bayesian model comparison result (weight=0.86 for the capacity model) is strong but not definitive — 14% probability remains for the simpler model. The distinction matters for theory: enhanced capacity (rather than mere weighting) suggests a link to arousal or motivational systems.
