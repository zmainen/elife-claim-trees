---
uuid: bafb4184-4ce0-472e-a84f-9eba891bd417
slug: hypothesis-5ht-codes-surprise
doi: ~
claim: >
  Phasic dorsal-raphe serotonin release functions as a surprise / belief-updating signal —
  therefore, optogenetically driven 5-HT release during a perceptual decision-making task
  should accelerate the rate at which the animal updates its prior, increase behavioral
  flexibility, and/or measurably alter the trade-off between sensory evidence and prior
  expectation in the choice computation.
displayClaim: >
  If 5-HT codes surprise, then stimulating it during a task with a shifting prior should
  speed up belief updating and shift psychometric or choice-model parameters.
shortClaim: "If 5-HT codes surprise, stimulating it should speed belief updating under shifting priors."
claim-type: hypothesis
role: hypothesis
concepts:
  - serotonin
  - surprise
  - belief updating
  - prior probability
  - cognitive flexibility
priority: 2026-04-19
epistemic: hypothesis

belongings: []

entails:
  - prediction-5ht-shifts-psychometric
  - prediction-5ht-accelerates-prior-update

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: hypothesis stated in introduction and as motivation for the task-engagement experiments
    confidence: N/A

reproductions: []
---

The introduction frames this hypothesis explicitly: "Given serotonin's supposed role as a surprise signal we hypothesized that it would modulate how animals incorporate prior knowledge into current sensory evidence, and how fast their prior would update given changes in the environment." The hypothesis inherits from Matias et al. (2017) and the broader surprise / unexpected-uncertainty literature. The paper then reports that *every* behavioral test of this hypothesis came out null — psychometric parameters, reaction times, prior-block-switch updating speed, and the probabilistic choice-model weights all show no detectable effect of 5-HT stimulation. The hypothesis is therefore empirically refuted by this paper for this task and stimulation protocol; the orthogonal-subspace hypothesis is the post-hoc explanation introduced to reconcile this null behavioral result with the strong observed neural modulation.
