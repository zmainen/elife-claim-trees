---
uuid: 55e1f8d1-c9b3-4bc0-8864-98fdba79b3c7
slug: fmri-bold-correlates-but-misses-suppressed-regions
doi: ~
claim: >
  Direct comparison of the present brain-wide single-unit modulation results with the
  opto-fMRI data of Hamada et al. (2024) — beta values per region from the fMRI study
  versus mean modulation index per region from the present study — shows a significant
  region-level correlation between fMRI BOLD beta and electrophysiological modulation
  strength. However, while the fMRI data showed only activation (or no effect) across
  regions, the single-unit recording reveals that some regions are suppressed by 5-HT
  stimulation, others are activated, and most show a balance of neurons increasing and
  decreasing their firing rates. The fMRI signal therefore correlates with neural
  modulation magnitude at the region level but cannot resolve the bidirectional sign of
  modulation, which is the qualitatively distinct finding of single-unit recording.
displayClaim: >
  Region-level BOLD (Hamada 2024 fMRI) correlates with our single-unit modulation strength,
  but fMRI sees only activation while ephys reveals widespread bidirectional modulation.
claim-type: empirical
role: empirical
concepts:
  - opto-fMRI
  - BOLD signal
  - bidirectional modulation
  - cross-modality comparison
  - neurovascular coupling
priority: 2026-04-20
epistemic: moderate

belongings:
  - relation: requires
    target: 5ht-modulates-all-recorded-regions-bidirectionally

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: Supp fig3
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol; Hamada et al. (2024) public opto-fMRI data
    dataset-doi: ~
    method: per-region correlation between Hamada et al. (2024) BOLD beta values and present-study mean modulation index, with per-region comparison of activation vs bidirectional sign
    confidence: moderate

reproductions: []
---

This is a new R1 empirical claim added directly in response to Reviewer 2's comment 1.1 requesting a quantitative comparison with the Hamada et al. (2024) opto-fMRI dataset. Supplementary Figure 3 presents the result. Two findings are bundled in one claim:

1. **Convergent validation**: BOLD beta values from Hamada et al. correlate with single-unit modulation strength at the region level. This rules out the alternative that the two studies are measuring fundamentally unrelated phenomena and provides convergent support that 5-HT optogenetic stimulation produces a real region-level neural modulation pattern detectable by both modalities.

2. **Resolution-dependent qualitative discrepancy**: The fMRI study reported only activation (uniform brain-wide BOLD increase). The present single-unit study reveals widespread bidirectional modulation: some regions suppressed (e.g., hippocampus, thalamus), some activated (e.g., medial prefrontal cortex, periaqueductal gray), and most showing within-region balance of excitation and inhibition. The fMRI signal therefore averages over the bidirectional sign and reports a positive net effect, missing the qualitative finding that single-unit recording reveals.

The interpretation given by R1 (paragraph after the Hamada comparison): the discrepancy is likely due to the vasoactive effects of serotonin on the cerebrovasculature, which directly impact the hemodynamic signal that fMRI relies on (Padawer-Curry et al., 2025, ref. 25). Direct neural recording circumvents this confound and reveals neural dynamics at single-cell resolution.

The claim is consequential for how the field interprets prior opto-fMRI work on serotonin: brain-wide BOLD activation in opto-fMRI does not imply uniform neural activation. The result strengthens the methodological argument for direct electrophysiology in studying serotonergic modulation.
