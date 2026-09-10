---
uuid: e3b1dbf0-1b42-4d06-ae59-6458e88e7485
slug: glm-significant-choice-and-5ht-coefficients
doi: ~
claim: >
  In the same per-neuron generalized linear model that tests the choice × stimulation
  interaction, both the choice main-effect predictor and the 5-HT-stimulation main-effect
  predictor had absolute coefficients significantly different from zero, indicating that
  each variable independently modulates spiking activity. The two effects are present and
  measurable; the question of whether they interact is therefore a meaningful one.
displayClaim: >
  Both choice and 5-HT main-effect coefficients in the per-neuron GLM are significantly
  non-zero — each independently modulates spiking.
claim-type: empirical
role: empirical
concepts:
  - generalized linear model
  - main effects
  - choice coefficient
  - stimulation coefficient
priority: 2026-04-20
epistemic: strong

belongings:
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig6c
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-neuron GLM with choice, stimulation, and choice × stimulation predictors; absolute-valued coefficients averaged per animal
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

This claim is the necessary precondition for the additivity test in `near-zero-choice-by-stim-interaction` to be meaningful. If either the choice main effect or the 5-HT main effect were itself near zero, then the near-zero interaction would have a trivial explanation (you cannot have a choice × stim interaction if there is no choice effect). The R1 results paragraph reports both main effects as significant before testing the interaction — this is the right epistemic order. The claim is new in R1 (the GLM analysis itself is new), but it is structural rather than novel: that 5-HT modulates spiking is established by `5ht-modulates-all-recorded-regions-bidirectionally` from quiet-wakefulness data, and that choice modulates spiking is the entire premise of the manifold/choice-axis analysis.
