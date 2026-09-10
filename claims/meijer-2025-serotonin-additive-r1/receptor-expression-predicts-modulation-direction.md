---
uuid: d7fc27da-fdcb-4182-8bae-5d2ee8830a72
slug: receptor-expression-predicts-modulation-direction
doi: ~
claim: >
  A generalized linear model predicting per-region signed 5-HT modulation index (the mean
  modulation index spanning negative for inhibition to positive for excitation) from z-scored
  expression density of six serotonergic receptors and DRN projection density yields a high
  explained-variance fit (pseudo R² = 0.62, Gaussian family with identity link). 5-HT2
  receptors are significant positive predictors of the modulation index — regions expressing
  more 5-HT2 receptors are more likely to be excited by serotonin stimulation, consistent
  with their excitatory (Gq-coupled) downstream effects. Conversely, 5-HT1a receptors are
  significant negative predictors — regions with more 5-HT1a receptors are suppressed by
  serotonin, consistent with their inhibitory (Gi/o-coupled) mechanism. The receptor
  contributions to direction are oppositely signed from their contributions to strength
  (`receptor-expression-predicts-modulation-strength`).
displayClaim: >
  Regional modulation direction is predicted oppositely by receptor type: 5-HT2 (excitatory
  Gq) positive, 5-HT1a (inhibitory Gi/o) negative — pseudo R² = 0.62.
claim-type: empirical
role: empirical
concepts:
  - 5-HT1a inhibitory
  - 5-HT2 excitatory
  - Gi/o coupling
  - Gq coupling
  - modulation directionality
priority: 2026-04-20
epistemic: strong

belongings:
  - relation: requires
    target: receptor-expression-predicts-modulation-strength

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig3c
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation; statsmodels GLM
    dataset: Allen Brain Atlas ISH; Allen Mouse Connectivity Atlas; IBL ONE protocol
    dataset-doi: ~
    method: per-Beryl-region GLM (Gaussian family, identity link) on signed mean modulation index
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

The directionality result is the cleanest single piece of receptor-pharmacology validation in the paper: the GLM coefficients align with the textbook G-protein coupling and the textbook excitatory/inhibitory polarity of the receptor families. Regions with more 5-HT1a (Gi/o-coupled, inhibitory) are inhibited; regions with more 5-HT2 (Gq-coupled, excitatory) are excited. The pseudo R² of 0.62 is the highest of the three Fig. 3 GLMs (strength, direction, latency), consistent with directionality being more receptor-pharmacology-determined than the other two quantities.

This claim is consequential for the receptor-dependent reconciliation hypothesis (`reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control`): the directionality result confirms that 5-HT1a and 5-HT2 receptors contribute to brain-wide effects of opposite sign, which is the necessary precondition for the reconciliation hypothesis to be coherent. The R1 discussion makes this connection explicit.

Note that the strength and direction models use different families (Binomial vs. Gaussian) because the targets have different distributions: modulated-fraction is bounded in [0, 1] (Binomial) while signed mean modulation index is unbounded and approximately Gaussian. The two models are therefore not strictly comparable in their pseudo R² values, but both describe well-explained variance.
