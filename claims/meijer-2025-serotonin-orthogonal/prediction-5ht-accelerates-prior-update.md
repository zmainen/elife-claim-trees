---
uuid: 1a5cd255-9f81-4e90-9fbc-e49873ac4e36
slug: prediction-5ht-accelerates-prior-update
doi: ~
claim: >
  If 5-HT signals surprise and supports cognitive flexibility, then optogenetic 5-HT
  stimulation across blocks of trials should accelerate the rate at which the animal
  updates its choice bias after a prior-probability block switch — for example, after the
  prior switches from 80% left to 80% right, 5-HT-stimulated mice should reach the new
  rightward bias in fewer trials than unstimulated mice.
displayClaim: >
  If 5-HT codes surprise, mice should update their choice bias faster after a prior block
  switch under 5-HT stimulation.
claim-type: prediction
role: prediction
concepts:
  - prior updating
  - block switch
  - cognitive flexibility
  - learning rate
priority: 2026-04-19
epistemic: prediction
status: refuted
panel: prediction

derived-from:
  - hypothesis-5ht-codes-surprise

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: prediction
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: derived prediction
    confidence: strong

reproductions: []
---

This prediction is operationally distinct from the psychometric-shift prediction: it concerns the *dynamics* of belief updating across blocks, not the steady-state choice function within a block. It is the test that most directly maps to the surprise / unexpected-uncertainty framework, since prior-block switches are the events at which a surprise signal would be most useful. The paper's design deliberately decouples 5-HT-stimulation blocks from prior-probability blocks, so that block-switch trials can include both stimulated and unstimulated cases. The empirical result (Fig. 3e) shows no acceleration of prior updating — refuting this prediction independently of the steady-state psychometric refutation.
