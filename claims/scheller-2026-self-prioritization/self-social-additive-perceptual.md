---
uuid: b32daec4-44c8-409c-8c3c-e7a1d13eb526
slug: self-social-additive-perceptual
doi: ~
claim: >
  The combination of social association and perceptual salience for other-associated stimuli
  produces effects consistent with additivity: the interaction term for other-associated
  salient stimuli is -0.54 Hz [HDI95: -2.4 to 1.4 Hz], indistinguishable from zero,
  indicating that social and perceptual salience operate via independent mechanisms for
  other-associated stimuli.
claim-type: empirical
role: empirical
concepts:
  - additivity
  - social salience
  - perceptual salience
  - independent mechanisms
  - interaction
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-additive-effects-other-associated
confirms:
  - hypothesis-social-perceptual-independent-mechanisms
dissociates-with:
  - self-salience-reduces-perceptual-benefit

belongings:
  - relation: supports
    target: social-perceptual-salience-independent-streams

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig7
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig7-v1.tif/full/1500,/0/default.jpg
    analysis: OSF analysis notebooks (https://osf.io/a62df)
    dataset: https://osf.io/a62df
    dataset-doi: ~
    method: hierarchical Bayesian TVA, interaction computation, Experiment 2 (N=71)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    notes: >
      Partially verified from estimates_indiv_C.csv (Exp2, OSF https://osf.io/a62df).
      The additivity test can be computed from v_p/v_r per condition: other-associated
      social (cond 3) diff = -1.36 Hz; perceptual (cond 2) diff = 6.05 Hz; other-salient
      combined (cond 5) diff = 5.32 Hz. Expected additive = 6.05 + (-1.36) = 4.69 Hz;
      observed = 5.32 Hz; interaction ≈ +0.63 Hz (near-zero, consistent with additivity).
      Sign and magnitude support the additivity claim; precise HDI bounds require posterior
      samples from .nc trace to fully verify.
---

The null interaction for other-associated stimuli supports the independence claim: when the stimulus is associated with another social identity, physical salience and social salience capture attention through separate mechanisms that do not interfere. The key contrast is with self-associated stimuli, where the interaction is sub-additive — suggesting that self-relevance and physical salience do share some mechanism or resource.
