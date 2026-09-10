---
uuid: 9a141a31-1a8a-4f94-8a33-c8c2386f023f
slug: latency-correlates-with-absolute-modulation
doi: ~
claim: >
  Across single neurons (latencies estimated by latenZy; ref. 27 — Haak & Heimel 2025),
  modulation onset latency is significantly negatively correlated with the absolute
  modulation index: neurons modulated more strongly by 5-HT stimulation, in either direction
  (excitation or suppression), have shorter onset latencies. The latency is longest for
  weakly-modulated neurons (absolute modulation index near zero). Some neurons reach
  extremely short latencies — the example amygdala neuron in Fig. 2l reaches 16 ms — and a
  small fraction show offset responses with extremely long latencies.
displayClaim: >
  Stronger 5-HT modulation = shorter onset latency, regardless of sign (Fig. 2m). Latencies
  range from ~16 ms (amygdala) to long offset responses.
claim-type: empirical
role: empirical
concepts:
  - modulation latency
  - latenZy estimator
  - absolute modulation index
  - onset response
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig2k, fig2l, fig2m
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-neuron latency estimation via latenZy (ref. 27 — Haak & Heimel 2025), Pearson correlation between absolute modulation index and onset latency, manual inspection of shortest-latency neurons
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

This is a substantively new R1 finding that replaces the v1 claim of "fast inhibition / slow excitation" with a more rigorous and qualitatively different result. The v1 paper had reported a correlation between modulation sign and latency — inhibited neurons fast, excited neurons slow. R1's revision (in response to Reviewer 3 comment 3 and using the new latenZy method developed by Haak & Heimel 2025) could not replicate that sign-by-latency correlation. The original Figure 2l showing the sign-latency correlation was removed.

What R1 reports instead is a different and more interpretable correlation: latency is correlated with the *absolute* modulation index — stronger modulation in either direction is associated with shorter latency, weaker modulation with longer latency. This correlation appears as the new Fig. 2m. The interpretation is straightforward: neurons that are strongly affected by serotonergic input respond quickly; neurons that are weakly affected respond slowly. The relationship is symmetric across the sign of modulation.

Two methodological refinements are bundled in: (1) the latenZy method (Haak & Heimel 2025) is non-parametric and binning-free, and includes an explicit significance test that excludes neurons with no reliable activity peak. This produces fewer but more trustworthy latency estimates than the earlier method. (2) The shortest latencies are no longer artifacts of estimation noise — they were manually inspected and confirmed (Fig. 2l shows an example amygdala neuron at 16 ms).

Under R1's broader framing, this finding contributes to the receptor-pharmacology picture (Fig. 3): the receptor-density GLM (`5ht1a-predicts-fast-modulation-latency`) finds that 5-HT1a expression specifically predicts short latencies. The absolute-modulation-index correlation is consistent with strong receptor coupling (likely 5-HT1a in the inhibitory direction, 5-HT2 in the excitatory direction) producing both larger and faster effects.

This claim replaces the v1 claim `inhibition-fast-excitation-slow` (which was carried over into the previous draft of this R1 paper); since R1 explicitly removed the sign-latency finding, that earlier slug should not appear in this paper's claim graph. The retained slug here uses the new content of Fig. 2k–m.
