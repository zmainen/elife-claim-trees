---
uuid: 3ec20b3f-8573-4f5f-8907-4cfd0319a5c7
slug: near-zero-choice-by-stim-interaction
doi: ~
claim: >
  In a per-neuron generalized linear model fitted to trial-by-trial spike counts with
  predictors for choice (left/right), 5-HT stimulation (on/off), and their interaction
  (choice × stimulation), the absolute interaction coefficient — averaged across the 13
  recorded brain regions and across animals — was statistically indistinguishable from
  zero (mean ± SEM across animals: -0.05 ± 0.06; t(9) = -0.92, p = 0.38, one-sample
  t-test against zero). The choice and 5-HT main-effect predictors had significant
  non-zero coefficients in the same model.
displayClaim: >
  Per-neuron GLM choice × 5-HT-stimulation interaction is near zero across animals
  (-0.05 ± 0.06; t(9) = -0.92, p = 0.38), while both main effects are significant.
claim-type: empirical
role: empirical
concepts:
  - generalized linear model
  - interaction term
  - additive modulation
  - one-sample t-test
priority: 2026-04-20
epistemic: strong

confirms:
  - prediction-near-zero-choice-stim-interaction
refutes:
  - prediction-multiplicative-gain-yields-significant-interaction
supports:
  - hypothesis-additive-modulation
  - rules-out-multiplicative-gain-control

belongings:
  - relation: requires
    target: glm-significant-choice-and-5ht-coefficients
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons
  - relation: supports
    target: hypothesis-additive-modulation

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig6c
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-neuron GLM with choice, stimulation, and choice × stimulation predictors fit to trial-by-trial spike counts; absolute coefficients averaged per animal; one-sample t-test against zero across animals
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

This is the new empirical centerpiece of R1 and the claim that licenses the entire reframing relative to v1. The structural moves that give it its bite are three: (1) the GLM is per-neuron and the coefficients are absolute-valued, capturing the magnitude of modulation rather than its sign — this matters because the paper's bidirectional-modulation finding (`5ht-modulates-all-recorded-regions-bidirectionally`) means signed coefficients would average toward zero for trivial reasons; (2) the interaction term is tested with a one-sample t-test against zero, not against shuffle null, so the test is for absence of interaction rather than for departure from a particular generative model; (3) the test is across animals (n = 10 in the t-test, t(9) = -0.92), not across neurons or regions, so the unit of analysis matches the unit of biological replication.

Two epistemic considerations bound the claim. First, t(9) = -0.92 with p = 0.38 is an absence-of-evidence result, not strong evidence of absence — with n = 10 the test is not powered to detect small interactions. The 95% CI on the mean interaction coefficient is approximately (-0.18, +0.08), which excludes large interactions but is consistent with small ones. The paper appropriately frames this as "consistent with additive modulation" rather than as proof of additivity. Second, the GLM treats stimulation as a binary on/off predictor, which discards information about within-stimulation temporal structure — multiplicative gain modulation might operate on a faster timescale than the GLM resolves and average toward additive in the trial-aggregated coefficients. The orthogonality result in PCA space (`5ht-axis-orthogonal-to-choice-axis`) is geometrically a consequence of additive modulation under linear projection (`orthogonality-derived-from-additivity`), so its independent confirmation provides convergent support that does not rely on the same statistical test.

The claim is new in R1; the v1 preprint does not carry the GLM analysis or the interaction-term result.
