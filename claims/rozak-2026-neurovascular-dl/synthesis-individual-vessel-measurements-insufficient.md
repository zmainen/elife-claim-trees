---
uuid: 8b9c0d1e-2f3a-4b5c-6d7e-8f9a0b1c2d3e
slug: synthesis-individual-vessel-measurements-insufficient
doi: ~
claim: >
  Interrogating individual vessels in isolation is insufficient to predict how blood flow is
  modulated across the cerebral microvascular network. The paper's combined evidence — within-vessel
  radius heterogeneity (24 ± 28% along vessel length at baseline), the spatial segregation of
  dilations and constrictions relative to active neurons, the network-wide rise in assortativity
  during optogenetic stimulation, and the modulation of capillary network efficiency — together
  argue that point-caliber and single-vessel approaches systematically miss the coordinated,
  graph-level structure of functional hyperemia.
displayClaim: >
  Single-vessel measurements cannot predict network-level blood flow modulation: within-vessel
  heterogeneity, neuron-relative spatial gradients, assortativity rise, and efficiency changes
  together require a network-level treatment.
shortClaim: "Single-vessel measurements cannot predict network-level blood flow modulation."
claim-type: synthesis
role: synthesis
concepts:
  - synthesis
  - network-level neurovascular coupling
  - methodological argument
  - point-measurement insufficiency
priority: 2026-04-20
epistemic: moderate

derived-from:
  - hypothesis-network-level-nvc-coordination

belongings: []

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: synthesis (Discussion)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: synthesis across pipeline outputs and biological findings
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unattempted
    blocked_by: not-applicable
    notes: >
      Synthesis claim — not directly reproducible. Stands on the constituent empirical claims
      (`baseline-intra-vessel-radius-varies-24pct`, `dilations-nearer-neurons-than-constrictions`,
      `network-assortativity-increases-stimulation`, `capillary-efficiency-increases-4pct`)
      which carry their own reproduction status.
---

This is the abstract's load-bearing closing assertion: "interrogating individual vessels is thus
not sufficient to predict how blood flow is modulated in the network." It is a synthesis claim
because no single figure establishes it; it emerges from the convergence of the within-vessel
heterogeneity result (Fig 7), the spatial-gradient result (Fig 8), and the network-metric results
(Fig 9). Its epistemic status is moderate because each constituent is moderate, the inference is
the paper's argument rather than a single test, and the within-vessel heterogeneity component (the
most direct argument against point measurement) has unresolved noise-vs-biology decomposition.
