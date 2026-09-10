---
uuid: a8ac5541-3763-40ad-86d8-471af9f63df3
slug: narrow-spike-interneurons-not-driver-of-rapid-inhibition
doi: ~
claim: >
  Narrow-spiking putative fast-spiking interneurons (separated from wide-spiking neurons by
  waveform spike width) have higher baseline firing rates than wide-spiking neurons (Supp.
  Fig. 4b), confirming the spike-width-based identification. Serotonin stimulation modulates
  a slightly higher fraction of putative interneurons than other neurons (Supp. Fig. 4c),
  but there is no significant difference in modulation index between putative interneurons
  and wide-spiking neurons (Supp. Fig. 4d). This rules out a fast-spiking-interneuron-mediated
  GABAergic mechanism as the driver of the rapid inhibition observed in regions like the
  hippocampus. R1 also reports a new finding: putative fast-spiking interneurons are
  modulated at *longer* latencies than regular-spiking neurons (Supp. Fig. 4e), making it
  even less plausible that they account for the fast inhibition.
displayClaim: >
  Putative fast-spiking interneurons not preferentially recruited by 5-HT, have similar
  modulation magnitude to wide-spiking neurons, and are modulated at *longer* latencies —
  ruling out an FSI-driven mechanism for fast 5-HT inhibition.
claim-type: empirical
role: control
concepts:
  - interneurons
  - waveform spike width
  - fast-spiking GABAergic
  - rapid inhibition mechanism
  - latency
priority: 2026-04-20
epistemic: moderate

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: Supp fig4
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: spike-width-based separation of narrow- vs. wide-spiking neurons; ZETA-test modulated fraction comparison; modulation-index distribution comparison; per-class latency comparison via latenZy
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1, with one R1 addition. The new latenZy-based latency analysis revealed that putative fast-spiking interneurons are modulated at longer latencies than regular-spiking neurons (Supp. Fig. 4e in R1). This is the opposite of what would be expected if FSIs drove fast inhibition; combined with the original v1 findings (no preferential recruitment, similar modulation index distribution), the FSI-driven-inhibition hypothesis is now ruled out by three convergent measurements rather than two. The longer-latency finding is reported in the R1 results paragraph (line 247-249) and in the reply letter as part of the latenZy revision (Reviewer 3 comment 3).

The control supports `latency-correlates-with-absolute-modulation` (the new R1 latency claim that replaces v1's `inhibition-fast-excitation-slow`) by ruling out one of the natural mechanistic explanations for fast inhibition.
