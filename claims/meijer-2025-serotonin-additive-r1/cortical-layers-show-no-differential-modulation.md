---
uuid: 55eae44b-bbdc-4ad0-949b-e75aa1d3babe
slug: cortical-layers-show-no-differential-modulation
doi: ~
claim: >
  When all cortical recordings are split by layer (using the layer assignment from
  histology-aligned probe positions), the percentage of 5-HT-modulated neurons per layer,
  the sign of modulation, and the onset latency do not differ across layers. This rules
  out a layer-specific cortical mechanism (e.g., 5-HT receptor density gradients across
  layers) as the source of the regional sign and timing heterogeneity.
displayClaim: >
  Splitting cortical recordings by layer reveals no differences in modulation fraction,
  sign, or latency.
claim-type: empirical
role: control
concepts:
  - cortical layers
  - laminar organization
  - 5-HT receptor distribution
  - control experiment
priority: 2026-04-20
epistemic: moderate

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: Supp fig5
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: layer-stratified analysis of modulated fraction, modulation index sign, and onset latency
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 substantively unchanged; supplementary figure renumbered from v1's Supp. Fig. 4 to R1's Supp. Fig. 5 because R1 inserts a new Supp. Fig. 3 (Hamada fMRI comparison) and a renumbered Supp. Fig. 4 (the spike-width and interneuron analyses).
