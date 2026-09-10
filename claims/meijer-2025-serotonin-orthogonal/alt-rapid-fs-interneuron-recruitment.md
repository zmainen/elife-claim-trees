---
uuid: 1e7ad84e-d186-4d10-802b-68f9a32c266e
slug: alt-rapid-fs-interneuron-recruitment
doi: ~
claim: >
  The rapid inhibition observed after dorsal-raphe stimulation is produced by preferential,
  fast recruitment of fast-spiking inhibitory interneurons, which are engaged by 5-HT more
  readily than other cell types and impose inhibition at short latency.
claim-type: interpretive
role: hypothesis
concepts:
  - fast-spiking interneurons
  - rapid inhibition
  - alternative explanation
priority: 2026-09-10
epistemic: weak

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    stance: rejects
    method: agent extraction of the mechanism named and excluded by the paper's spike-width control
    confidence: weak

reproductions: []
---

An alternative the paper argues against, not a proposition it asserts. It is the obvious
circuit explanation for inhibition arriving within ~25 ms: that 5-HT drives fast-spiking
interneurons first.

`narrow-spike-interneurons-not-driver-of-rapid-inhibition` closes it — narrow-spiking putative
fast-spiking neurons are only marginally more likely to be 5-HT modulated than wide-spiking
neurons and show no significant difference in modulation index.

That control already carried the right relation, `rules-out`, pointing at a slug named
`rapid-fs-interneuron-recruitment-as-mechanism` — a claim that had never been written. The edge
therefore resolved to nothing and was dropped by every export. This file is that claim, under
the corpus's `alt-` naming.
