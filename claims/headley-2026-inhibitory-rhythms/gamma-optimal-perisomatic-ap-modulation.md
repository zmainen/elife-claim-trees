---
uuid: 568bd16c-91dc-4bf0-8841-1836968cf68e
slug: gamma-optimal-perisomatic-ap-modulation
doi: ~
claim: >
  In a sweep across 11 frequencies from 0.5 to 80 Hz, gamma frequencies (40–80 Hz) produce
  the strongest phase-dependent modulation of somatic action potential voltage threshold by
  perisomatic rhythmic inhibition.
displayClaim: >
  Across an 11-frequency sweep from 0.5 to 80 Hz, perisomatic inhibition at gamma (40–80 Hz)
  most strongly phase-modulates the somatic AP voltage threshold.
claim-type: empirical
role: empirical
concepts:
  - gamma rhythm
  - AP voltage threshold
  - perisomatic inhibition
  - frequency sweep
  - phase modulation
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-gamma-optimal-perisomatic

belongings:
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: gamma-perisomatic-no-dendritic-spike-change
  - relation: supports
    target: gamma-gates-proximal-basal-inputs
  - relation: supports
    target: pv-gamma-sst-beta-correspondence
  - relation: supports
    target: hypothesis-frequency-compartment-matching

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig8
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig8-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig8.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — perisomatic frequency sweep
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig8.ipynb
    script_execution: pre-computed
    script_execution_note: "11-frequency perisomatic sweep requires 1.88 GB Dryad DendCompOscPublic/"
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Script: Fig8.ipynb requires Dryad simulation files from DendCompOscPublic/
      (11-frequency perisomatic sweep, 0.5–80 Hz). Not in GitHub repo.
      Dryad API confirmed (2026-03-30): monolithic zip only (1.88 GB); no individual file access.
      Download Headley_etal_eLifeDRYAD.zip, extract DendCompOscPublic/, install environment.yml
      (Python 3.9 + holoviews), run Fig8.ipynb.
---

The gamma optimum for perisomatic AP threshold modulation has a different mechanistic basis than the beta/distal optimum. At gamma frequencies (~40–80 Hz), the inhibitory cycle is brief (~12–25 ms), which efficiently gates the fast Na+ spike process that underlies axonal AP initiation. The perisomatic location means the inhibitory conductance directly modulates the axon initial segment depolarization window. Slower frequencies allow recovery between cycles; faster frequencies would produce sustained suppression rather than phase-specific modulation.
