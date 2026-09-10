---
uuid: 84677204-94c6-4bc3-928e-93449079091c
slug: inhibition-fast-excitation-slow
doi: ~
claim: >
  Across the 13 recorded brain regions, the mean onset latency of 5-HT modulation is
  positively correlated with mean modulation index — regions in which 5-HT suppresses
  activity respond at short latencies (e.g. hippocampus, ~25 ms after stimulation onset),
  while regions in which 5-HT excites activity respond at longer latencies (e.g. medial
  prefrontal cortex). The cross-region Pearson correlation between mean latency and
  mean modulation index is r = 0.61, p = 0.028.
displayClaim: >
  Across regions, inhibition is fast (e.g. hippocampus ~25 ms) and excitation is slow
  (mPFC); mean latency correlates with mean sign across regions (r=0.61, p=0.028).
claim-type: empirical
role: empirical
concepts:
  - onset latency
  - modulation index
  - brain region heterogeneity
  - direct vs indirect pathways
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons

rules-out:
  - narrow-spike-interneurons-not-driver-of-rapid-inhibition

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig2k, fig2l
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-neuron ZETA-test latency, region-mean correlation against region-mean modulation index
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~

discrepancy:
  type: methodological-gap
  explanation: >
    Paper reports r=0.61, p=0.028 across 13 regions. Script finds r=0.09, p=0.70 across 19 regions. The discrepancy is likely different region grouping (fine vs paper-level targets) and possibly different neuron inclusion criteria for reliable latency estimates.
---

The latency-sign correlation is structurally interesting because it suggests that the rapid inhibitory effect cannot be a simple monosynaptic 5-HT₁A-mediated hyperpolarization in regions like cortex (which are ~10–20 ms from DRN by direct projection but show slow excitation), but is more consistent with rapid inhibition being routed through indirect circuits — possibly via cortical interneurons or via fast subcortical loops. The paper uses this observation as motivation for the narrow-spiking-interneuron analysis (Supp Fig 3), which then rules out the obvious candidate (rapid recruitment of fast-spiking interneurons). The remaining candidates — multi-synaptic loops, rapid 5-HT₃-receptor-mediated effects on subsets of neurons, indirect routing through median raphe for hippocampus — are discussed but not directly tested.
