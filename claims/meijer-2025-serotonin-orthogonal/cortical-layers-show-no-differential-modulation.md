---
uuid: 43dc14e4-5475-40a6-b981-fcbd00914ad4
slug: cortical-layers-show-no-differential-modulation
doi: ~
claim: >
  When cortical Neuropixel recordings are split by cortical layer, neither the percentage of
  significantly 5-HT-modulated neurons, the sign of the modulation, nor the onset latency
  shows a layer-dependent pattern — implying that any layer-specific receptor expression or
  axonal-targeting biases of dorsal-raphe serotonergic projections do not translate into a
  layer-specific population effect at this measurement scale.
displayClaim: >
  Across cortical layers, 5-HT modulation fraction, sign, and onset latency are
  indistinguishable — no layer dependence in the cortical 5-HT response.
claim-type: empirical
role: control
concepts:
  - cortical layers
  - laminar organization
  - serotonergic receptor expression
  - layer-specific modulation
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: supp-fig4a, supp-fig4b, supp-fig4c, supp-fig4d
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: layer assignment from histology-aligned probe coordinates; per-layer comparison of fraction, sign, and latency
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

This is a negative result that bears on biological interpretation. The literature suggests that 5-HT₂A receptors are enriched in cortical layer 5 pyramidal neurons, while 5-HT₁A is more broadly expressed; one might therefore predict a layer-5-biased excitatory effect or a layer-2/3-biased inhibitory effect. The absence of such a pattern at the population scale is informative but bounded: it could mean (1) the receptor distribution does not translate into firing-rate differences large enough to detect with this sample size; (2) per-neuron modulation patterns within layers are heterogeneous in ways that wash out in laminar means; (3) the effects ARE layer-specific but are masked by indirect inputs that arrive via similar-density axons across layers. The paper does not adjudicate among these.
