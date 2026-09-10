---
uuid: af8bc967-3346-4e25-ac9e-8ad3536313fd
slug: artery-dilates-venule-unchanged-at-low-power
doi: ~
claim: >
  At 1.1 mW/mm² 458 nm stimulation, a sample artery dilated 1.33±0.86 µm (p<1e-4) and a
  sample capillary dilated 0.42±0.39 µm (p<1e-4), while a sample venule showed no significant
  radius change (p=0.22), demonstrating vessel-type heterogeneity in optogenetic neurovascular
  responses.
claim-type: empirical
role: empirical
concepts:
  - artery
  - venule
  - capillary
  - vessel-type heterogeneity
  - optogenetic neurovascular response
priority: 2026-03-30
epistemic: weak

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination
dissociates-with:
  - vessel-radius-heterogeneity-stimulation

belongings:
  - relation: supports
    target: vessel-radius-heterogeneity-stimulation

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig7A
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig7-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: vertex-wise radius tracking; Mann-Whitney U test; single image stack example
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      This is a single-example illustration (one artery, one capillary, one venule from
      one mouse) shown to demonstrate the vertex-wise tracking capability. The p-values
      are from Mann-Whitney U tests on vertex-wise radius distributions before vs. after
      stimulation — not from a population comparison. The statistical significance here
      reflects the number of measurement points along the vessel, not biological replication.
      The venule null result (p=0.22) is consistent with known physiology but cannot be
      generalized from n=1.
---

Marked weak because Figure 7 is an illustrative example, not a systematic population analysis
of vessel-type responses. The population-level analysis of capillary vs. large vessel responses
is in Figure 8 and the appendix figures; Figure 7 demonstrates the vertex-wise tracking
methodology using one example of each vessel type. The artery and venule classifications
appear to be based on visual identification in the MIP, not automated morphological criteria.
