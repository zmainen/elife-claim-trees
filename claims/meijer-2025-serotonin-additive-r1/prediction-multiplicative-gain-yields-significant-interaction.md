---
uuid: 1fe51410-07cb-4c4b-b42d-0b87648b06bb
slug: prediction-multiplicative-gain-yields-significant-interaction
doi: ~
claim: >
  If serotonergic modulation acted via multiplicative gain modulation — that is, scaling the
  choice-related component of neural activity rather than shifting it additively — then a
  per-neuron GLM with choice, stimulation, and choice × stimulation predictors should yield
  a significantly non-zero interaction coefficient, because under multiplicative scaling the
  size of the stimulation effect on a neuron depends on the magnitude of its choice-related
  drive.
displayClaim: >
  Multiplicative gain modulation predicts a significantly non-zero choice-by-stimulation
  interaction coefficient — the contrastive prediction to additivity.
claim-type: prediction
role: prediction
concepts:
  - multiplicative gain
  - generalized linear model
  - interaction term
  - contrastive prediction
priority: 2026-04-19
epistemic: prediction
status: refuted
panel: prediction

derived-from:
  - interprets-gain-control-default-framework

belongings: []

contradicts:
  - prediction-near-zero-choice-stim-interaction

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: contrastive prediction derived from the dominant gain-control framework, stated alongside the additive prediction in the R1 results paragraph
    confidence: strong

reproductions: []
---

This is the contrastive-prediction node that gives the R1 GLM analysis its eliminative force. Without an explicit prediction from the gain-control framework against which to test the data, the additivity finding would be merely a description ("the interaction is near zero"); with the contrastive prediction in place, the same data become an elimination ("the brain-wide signature of multiplicative gain control is absent"). The R1 results paragraph (per the revision notes, R2) makes both predictions explicit before reporting the t-test result. The prediction is refuted by `near-zero-choice-by-stim-interaction`. The empirical refutation propagates upward to license `rules-out-multiplicative-gain-control`.

The prediction is a strong-form one — it would be refuted both by a near-zero interaction (the actual result) and, more weakly, by failure of the interaction to scale with stimulation strength or with the choice coefficient magnitude. The paper does not test the latter forms, so the eliminative claim it licenses is correspondingly bounded: gain control is ruled out as the *dominant brain-wide mode* during this task, not as a mechanism that operates in any region or under any condition.
