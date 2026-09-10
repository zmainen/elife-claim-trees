---
uuid: 83d656ca-94ec-4a0f-bfb1-1138605cc136
slug: interprets-paquelet-correlated-ensembles
doi: 10.1016/j.neuron.2022.05.015
claim: >
  Paquelet et al. (2022, Neuron) used calcium imaging in awake behaving mice to
  characterize population activity of DRN serotonergic neurons. Sucrose consumption
  activated correlated ensembles comprising up to ~59% of recorded serotonergic neurons;
  footshock activated correlated ensembles comprising up to ~45%. Across exploratory and
  social behaviors, serotonergic neurons were recruited as structured, correlated
  subpopulations with mixed selectivity — not as a uniform population-wide burst.
displayClaim: >
  Paquelet et al. (2022) found that DRN serotonergic neurons are activated in correlated
  ensembles (~59% for sucrose, ~45% for footshock) with mixed selectivity — not uniform
  synchronous firing.
shortClaim: "DRN 5-HT neurons activate as correlated ensembles, not uniform bursts (Paquelet 2022)."
claim-type: interpretive
role: literature-context
concepts:
  - DRN ensemble structure
  - calcium imaging
  - correlated activation
  - mixed selectivity
  - endogenous vs evoked
priority: 2026-04-20
epistemic: moderate

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: ~
    panel: discussion (optogenetics-vs-endogenous scope paragraph)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited in the v1 scope paragraph to characterize endogenous DRN activation patterns against which optogenetic SERT-Cre stimulation is compared
    confidence: moderate

reproductions: []
---

This claim registers the Paquelet et al. (2022) finding as a discrete literature node so the scope claim `optogenetic-activation-not-physiological-pattern` has an explicit reference for its characterization of endogenous DRN activation patterns. The v1 manuscript cites Paquelet with the phrasing "synchronized burst-like firing of 50–60% of serotonergic neurons" in response to sucrose and footshock, which the R1 revision later sharpens (the source modality — calcium imaging — cannot resolve bursts, the sucrose and footshock numbers are separate rather than a single range, and the population structure is correlated-ensemble rather than uniformly synchronous).

For the v1 graph specifically, the Paquelet reference is the piece of literature that carries the weight of the scope-bounding claim: optogenetic SERT-Cre + ChR2 activation is characterized as broader and less structured than endogenous release, and the endogenous characterization comes from Paquelet. Without this node, the scope claim's reference would be implicit. The R1 paper registers the same Paquelet finding at its own slug (see `meijer-2025-serotonin-additive-r1/interprets-paquelet-correlated-ensembles`) with the corrected framing; registering a parallel node here maintains the continuity of the literature reference across the two versions of the paper.

Epistemic qualification is moderate — the underlying Paquelet result is well-supported within its own paper (calcium imaging with appropriate controls), but the ensemble-structure vs synchronous-burst distinction is a characterization that the imaging modality cannot fully resolve; direct electrophysiology in the same conditions would be required to adjudicate the firing-pattern question decisively.
