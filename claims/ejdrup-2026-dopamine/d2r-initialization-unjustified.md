---
uuid: 006a2982-b056-4c8c-b1f5-6c9819c1eaff
slug: d2r-initialization-unjustified
doi: ~
claim: >
  D2 receptor occupancy is initialized at 0.4 in all receptor dynamics simulations without
  derivation from steady state; at the modeled EC50 of 7 nM and simulated tonic [DA] of ~10 nM
  in DS, equilibrium occupancy would be approximately 0.59. No sensitivity analysis over this
  initialization is reported.
claim-type: assessment
role: methodological
concepts:
  - D2 receptor
  - receptor occupancy
  - model initialization
  - dopamine kinetics
priority: 2026-03-29
epistemic: weak
check_verification: partial
check_verification_from:
- record:verified

scopes:
  - d2r-integrates-over-seconds
  - d2r-insensitive-to-brief-pauses
  - d2r-occupancy-higher-in-vs

belongings: []

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig1H
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 1-Fig 1h-Source code.py
    dataset: ~
    dataset-doi: ~
    method: code inspection
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    notes: >
      Code inspection confirmed: Figure 1-Fig 1h-Source code.py initializes D2R occupancy at
      occ_D2 = 0.4. No sensitivity sweep over this parameter appears in any notebook or
      supplementary script. Calculation from paper's own EC50 (7 nM) and DS tonic [DA] (~10 nM)
      gives equilibrium occupancy ≈ 0.59 via Hill equation with n=1. Assessment claim confirmed
      by direct code reading.
---

The initialization value of 0.4 is inconsistent with the equilibrium prediction from the model's own parameters. Using the Hill equation with EC50 = 7 nM and [DA]_tonic ≈ 10 nM in DS gives occupancy ≈ 0.59. The directional claims about D2R dynamics (slow return to baseline, insensitivity to brief pauses) are unlikely to be qualitatively wrong, but quantitative occupancy values reported in Figures 1H, 1J, 2G, and 2H are sensitive to this choice. The absence of a sensitivity analysis is the methodological gap: readers cannot assess how much the absolute occupancy values would shift under correct initialization. Claims requiring this assessment node are flagged as `weak` in their absolute values even when the directional logic is `moderate` or `strong`.
