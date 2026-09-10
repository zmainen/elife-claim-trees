---
uuid: 4bad74a6-ab11-4870-947d-a0b8b0d68ddc
slug: 5ht-stim-leaves-decision-behavior-intact
doi: ~
claim: >
  In the IBL steering-wheel perceptual decision-making task, optogenetic activation of
  dorsal-raphe serotonergic neurons starting at visual stimulus onset and lasting until
  choice (or 1 s, whichever is shorter) produces no detectable change in any of:
  psychometric slope (visual acuity), bias (prior influence), lapse rate (motivation),
  percent-correct, median reaction time, the speed of choice-bias updating after a
  prior-probability block switch, or the per-predictor weights of a probabilistic choice
  model fitting visual evidence, prior, and past choice with separate stimulated /
  unstimulated coefficients.
displayClaim: >
  In the IBL steering-wheel task, 5-HT stimulation has no detectable effect on
  psychometric, RT, prior-update, or choice-model behavior.
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
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig4c, fig4d, fig4e, fig4g
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: psychometric error-function fit (psychofit), paired t-test on RT, regularized maximum-likelihood logistic choice model, paired t-tests against zero and per-predictor
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. The load-bearing null result of the paper. Tested under multiple operationalizations (psychometric fit, RT, prior-block-switch, probabilistic choice model) — the four-way convergence makes a multiple-comparisons explanation unlikely. The null is what creates the central explanatory puzzle, which v1 reconciled with orthogonality and R1 reconciles with additivity. The two reconciliations are mathematically the same fact (under linear projection in a 2×2 design) but conceptually different — the additivity framing makes a positive computational claim about how neuromodulation acts, where the orthogonality framing made a structural claim about how it sits in population geometry.
