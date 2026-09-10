---
uuid: 677d38e8-8b0f-42cb-a194-293cf4899020
slug: hypothesis-orthogonal-neuromodulatory-subspace
doi: ~
claim: >
  A neuromodulatory signal can produce strong, brain-wide single-neuron modulation while
  leaving ongoing task-driven behavior unaffected if the modulation is geometrically
  confined to a population subspace orthogonal to the readout dimensions used by downstream
  circuits to extract task variables (here, the upcoming choice). Orthogonality permits a
  linear-readout downstream region to project onto either the choice subspace or the
  neuromodulatory subspace independently.
displayClaim: >
  Strong neural modulation can leave behavior intact if the modulation lives in a subspace
  orthogonal to the population dimensions a downstream linear readout uses to extract the
  task variable.
shortClaim: "Modulation orthogonal to the task-readout subspace leaves behavior intact."
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

belongings: []

entails:
  - prediction-5ht-axis-orthogonal-to-choice
  - prediction-orthogonality-grows-toward-choice

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: post-hoc hypothesis introduced to reconcile widespread neural modulation with intact behavior
    confidence: N/A

reproductions: []
---

This is the paper's central conceptual contribution. It is introduced post-hoc — only after the data establish that 5-HT stimulation produces both strong neural modulation (Fig. 2, Fig. 4) and no behavioral effect (Fig. 3) is the orthogonal-subspace hypothesis stated as the candidate reconciliation. The hypothesis is geometrically precise: it predicts a specific structural property of the population response (the 5-HT-driven displacement vector in PCA space lies near the orthogonal complement of the L-vs-R choice vector). It is not a statement about which neurons are affected or how strongly — those questions are addressed by the bidirectional-modulation claim. It is a statement about how the modulation is *organized* across the population.

The hypothesis is best read as a structural reframing of the neuromodulator-vs-behavior puzzle: rather than treating "no behavior effect" as evidence of a weak or restricted neural effect, the paper proposes that downstream readout geometry can selectively ignore the modulation. The proposed manuscript revisions strengthen this framing by introducing an additivity-vs-multiplicativity dichotomy (the GLM analysis), positioning orthogonality as the geometric consequence of additive modulation; the v1 preprint stops at the geometric claim itself.
