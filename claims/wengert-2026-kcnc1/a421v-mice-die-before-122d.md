---
uuid: e2edfcd1-ec01-4ec7-ba36-01ab26290d69
slug: a421v-mice-die-before-122d
doi: ~
claim: >
  All Kcnc1-A421V/+ knock-in mice die before 122 days of age, while wild-type littermates survive significantly longer (Mantel-Cox p<0.001; n=33 mutant, n=46 wild-type).
claim-type: empirical
role: empirical
concepts:
  - KCNC1
  - A421V
  - survival
  - mortality
  - knock-in mouse
priority: 2026-03-30
epistemic: strong

confirms:
  - prediction-seizures-and-sudep
  - hypothesis-pv-dysfunction-drives-encephalopathy

belongings: []

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: ~
    panel: fig1
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: survival analysis (Kaplan-Meier, Mantel-Cox)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    script: verification/wengert-2026-kcnc1/verify.py
    original_figure: verification/originals/wengert-2026-kcnc1/fig1.jpg
    figure: verification/wengert-2026-kcnc1/fig-survival.png
    original_script: https://doi.gin.g-node.org/10.12751/g-node.bqni9h
    script_execution: pre-computed
    script_execution_note: "Primary analysis in Clampfit (proprietary). Statistics verified from deposited Excel summary file."
    time_fast: "~2 min"
    time_full: "~48 hrs (68 GB download + gin)"
    notes: >
      Data extracted from Wengert et al_eLife_Electrophysiology Analysis.xlsx (G-Node,
      Survival sheet, fig1E). n=33 KI, n=46 WT confirmed exactly. 30/33 KI mice died
      (event=1), 3 censored. Max KI day = 122.0 — one mouse died at exactly day 122,
      so the claim "before 122 days" is marginally imprecise; the data shows at or before
      122 days. All WT mice censored (no deaths). Significance not recomputed (Mantel-Cox
      requires lifelines/R); direction and n counts fully confirmed.
---
