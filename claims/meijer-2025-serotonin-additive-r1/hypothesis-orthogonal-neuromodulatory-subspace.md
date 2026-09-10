---
uuid: 2e0f1cb9-4f6a-4009-b3b2-dea39d6c6749
slug: hypothesis-orthogonal-neuromodulatory-subspace
doi: ~
claim: >
  A neuromodulatory signal can produce strong, brain-wide single-neuron modulation while
  leaving ongoing task-driven behavior unaffected if the modulation is geometrically
  confined to a population subspace orthogonal to the readout dimensions used by downstream
  circuits to extract task variables. In the R1 framing, this is not an independent
  hypothesis but a geometric consequence of additive (rather than multiplicative)
  modulation, derivable from the additivity hypothesis under a 2×2 factorial choice ×
  stimulation design.
displayClaim: >
  Strong neural modulation can leave behavior intact if the modulation lives in a subspace
  orthogonal to the population dimensions a downstream linear readout uses for the task —
  a geometric reformulation of additive modulation.
shortClaim: "Modulation orthogonal to the readout dimensions leaves behavior intact."
claim-type: hypothesis
role: hypothesis
concepts:
  - neural manifold
  - orthogonal subspaces
  - linear readout
  - choice coding
  - neuromodulation
priority: 2026-04-19
epistemic: hypothesis

derived-from:
  - hypothesis-additive-modulation

belongings: []

entails:
  - prediction-5ht-axis-orthogonal-to-choice
  - prediction-orthogonality-grows-toward-choice

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: stated as the geometric corollary of additive modulation in the R1 introduction and discussion
    confidence: N/A

reproductions: []
---

This claim carries over from v1 (`meijer-2025-serotonin-orthogonal/hypothesis-orthogonal-neuromodulatory-subspace`) but its position in the explanatory hierarchy has changed. In v1 it was the central post-hoc reconciliation of the strong-modulation/no-behavior puzzle. In R1 it is presented as a geometric reformulation of the additivity hypothesis: under a 2×2 factorial choice × stimulation design with linear (PCA) projection, additive modulation entails that the stimulation-effect direction (the displacement between mean-stim and mean-no-stim trajectories, averaged across choice) is orthogonal to the choice direction (the displacement between mean-left and mean-right, averaged across stimulation). The two claims describe the same computational property in different mathematical languages — one in terms of GLM regression coefficients, the other in terms of population subspace geometry.

The graph encodes the demotion via `derived-from: [hypothesis-additive-modulation]`. The orthogonality hypothesis is not eliminated — it remains the lens through which the manifold geometry results (Fig. 5g–i) are read, and its forward-looking implication for downstream readout circuits is still the paper's mechanistic suggestion. But the conceptual primacy that v1 gave it is reassigned to additivity. This is consequential for how the paper situates itself in the literature: the v1 framing put it in dialogue with prior work on neural-population subspace geometry; the R1 framing puts it in dialogue with prior work on neuromodulator computation, where the additive-vs-multiplicative dichotomy has a long history but had not been brain-wide tested in a behaving animal.
