---
uuid: 87e4d6e1-5f61-419f-a05a-782fb5950745
slug: 5ht-modulation-fraction-tracks-chr2-expression
doi: ~
claim: >
  Across the 11 SERT-Cre mice, the per-animal fraction of significantly 5-HT-modulated
  neurons (ZETA test, p < 0.05) correlates significantly with the per-animal histological
  measurement of channelrhodopsin expression density in the DRN (Pearson r = 0.77,
  p = 0.005).
displayClaim: >
  Across SERT-Cre mice, the fraction of 5-HT-modulated neurons correlates with histologically
  measured ChR2 expression (r = 0.77, p = 0.005).
claim-type: empirical
role: empirical
concepts:
  - dose-response
  - ChR2 expression
  - histology
  - construct validity
priority: 2026-04-20
epistemic: strong

belongings: []

supports:
  - 5ht-modulates-all-recorded-regions-bidirectionally

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig2g
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-animal modulated-fraction (ZETA-test, p<0.05) vs. per-animal relative DRN/control fluorescence; Pearson correlation
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. Important construct-validity claim: the dose-response relationship between expression and effect rules out the alternative that the modulated fraction is a generic experimental artifact unrelated to the optogenetic intervention. Required by the brain-wide modulation claim.
