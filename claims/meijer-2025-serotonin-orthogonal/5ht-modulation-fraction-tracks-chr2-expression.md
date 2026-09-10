---
uuid: 275ffb65-3c47-4736-9649-2fb33c1934ad
slug: 5ht-modulation-fraction-tracks-chr2-expression
doi: ~
claim: >
  The fraction of significantly 5-HT-modulated neurons recorded per animal is positively
  correlated with the histologically measured channelrhodopsin expression level in that
  animal's DRN (Pearson r = 0.77, p = 0.005), establishing that the magnitude of the neural
  effect scales with the optogenetic drive — and ruling out a stimulation-condition-related
  artifact common across animals.
displayClaim: >
  The percent of 5-HT-modulated neurons per mouse correlates with that mouse's DRN ChR2
  expression (r=0.77, p=0.005) — the effect tracks the drive.
claim-type: empirical
role: control
concepts:
  - channelrhodopsin expression
  - dose-response
  - histology
  - methodological control
priority: 2026-04-20
epistemic: strong

validates:
  - 5ht-modulates-all-recorded-regions-bidirectionally

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig2g
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: Pearson correlation between per-mouse modulated-neuron fraction and per-mouse DRN/control fluorescence ratio
    confidence: strong
    scope: per-animal correlation, n = 11 SERT-Cre mice

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~
---

This is a critical internal control rather than a primary result. It serves three functions: (1) it establishes a dose-response — animals with more ChR2 show larger neural effects, which is what one expects of a real optogenetic effect and what one does not expect of a non-specific artifact; (2) it provides a calibration that anchors interpretations of cross-animal variability; (3) it indirectly supports the WT-control claim by showing that within SERT-Cre animals the effect varies in the predicted direction, not just at the SERT-vs-WT contrast.
