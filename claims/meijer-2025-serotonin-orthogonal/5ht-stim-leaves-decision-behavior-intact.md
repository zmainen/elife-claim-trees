---
uuid: e59d7d03-4f0f-4939-b88a-c604804a7bb2
slug: 5ht-stim-leaves-decision-behavior-intact
doi: ~
claim: >
  In the IBL steering-wheel perceptual decision-making task, optogenetic activation of
  dorsal-raphe serotonergic neurons starting at visual stimulus onset and lasting until
  choice (or 1 s, whichever is shorter) produces no detectable change in any of: psychometric
  slope (visual acuity), bias (prior influence), lapse rate (motivation), percent-correct,
  median reaction time, the speed of choice-bias updating after a prior-probability block
  switch, or the per-predictor weights of a probabilistic choice model fitting visual
  evidence, prior, and past choice with separate stimulated / unstimulated coefficients.
displayClaim: >
  In the IBL steering-wheel task, 5-HT stimulation has no detectable effect on psychometric
  slope, bias, lapse, percent-correct, RT, prior-update speed, or any choice-model weight.
claim-type: empirical
role: empirical
concepts:
  - psychometric function
  - probabilistic choice model
  - prior updating
  - reaction time
  - null result
priority: 2026-04-20
epistemic: strong

refutes:
  - prediction-5ht-shifts-psychometric
  - prediction-5ht-accelerates-prior-update
  - hypothesis-5ht-codes-surprise

belongings:
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig3c, fig3d, fig3e, fig3g
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: psychometric error-function fit, paired t-test on RT, regularized maximum-likelihood logistic choice model, paired t-tests against zero and per-predictor
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

This is the load-bearing null result of the paper. Its strength is that the test is repeated under multiple operationalizations: a model-free psychometric fit, a model-free RT comparison, a model-free prior-block-switch analysis, and a model-based probabilistic-choice analysis. None show a significant effect; the four-way convergence makes a single-test multiple-comparisons explanation unlikely. The null is what creates the central explanatory puzzle ("strong neural modulation, no behavior") and motivates the orthogonal-subspace hypothesis.

Note the scope conditions: this null applies *to this task* (a perceptual decision with stimulus prior), *with this stimulation protocol* (1 s during the trial, blocked across trials), and at the population behavioral level. The discussion explicitly acknowledges that other paradigms with stronger surprise / punishment / uncertainty content might show different results.
