---
uuid: c4a03387-7441-4430-bffb-d7cfec4e0d75
slug: narrow-spike-interneurons-not-driver-of-rapid-inhibition
doi: ~
claim: >
  Narrow-spiking putative fast-spiking interneurons (separated from wide-spiking neurons by
  spike width, with their higher firing rates confirming the classification) are only
  marginally more likely to be 5-HT modulated than wide-spiking neurons, and show no
  significant difference in modulation index — ruling out preferential rapid recruitment
  of fast-spiking interneurons as the mechanism for the rapid inhibition observed in
  short-latency-suppressed regions.
displayClaim: >
  Narrow-spiking putative interneurons are not preferentially modulated by 5-HT and show
  the same modulation index as wide-spiking neurons — rapid inhibition is not via FS
  interneurons.
claim-type: empirical
role: control
concepts:
  - fast-spiking interneurons
  - spike-width classification
  - parvalbumin interneurons
  - mechanism of inhibition
priority: 2026-04-20
epistemic: moderate

rules-out:
  - rapid-fs-interneuron-recruitment-as-mechanism

belongings:
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: supp-fig3a, supp-fig3b, supp-fig3c, supp-fig3d
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: spike-width threshold classification of narrow vs wide; firing-rate validation; per-class fraction modulated and modulation-index comparison
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

Spike-width classification is a coarse and imperfect proxy for parvalbumin-positive fast-spiking interneurons; it captures the largest population of FS interneurons but misses non-FS GABAergic populations (somatostatin, VIP, neurogliaform) and includes some glutamatergic neurons with narrow spikes. The result rules out one specific mechanism — rapid synchronous PV+ recruitment driving rapid inhibition — but cannot speak to other inhibitory mechanisms. The remaining candidates the discussion entertains include direct 5-HT₁A-mediated hyperpolarization in subsets of pyramidal cells (which would not be visible in this contrast), and indirect routing through subcortical loops or median raphe. The negative result therefore narrows but does not specify the mechanism.
