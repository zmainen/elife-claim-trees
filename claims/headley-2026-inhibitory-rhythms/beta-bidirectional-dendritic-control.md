---
uuid: bf7efeee-2819-485d-a06d-1fc3782ce66f
slug: beta-bidirectional-dendritic-control
doi: ~
claim: >
  Beta-frequency rhythms at distal dendritic locations produce bidirectional control of
  dendritic spike probability: enhanced dendritic spike occurrence during inhibitory troughs
  and suppressed occurrence during inhibitory peaks within the same oscillatory cycle.
displayClaim: >
  Beta-frequency distal inhibition controls dendritic spikes bidirectionally within each
  cycle — enhancing them during inhibitory troughs and suppressing them during peaks.
claim-type: empirical
role: empirical
concepts:
  - beta rhythm
  - bidirectional control
  - dendritic spike probability
  - phase-dependent modulation
  - inhibitory trough
priority: 2026-03-30
epistemic: moderate

belongings:
  - relation: requires
    target: beta-optimal-distal-dendritic-entrainment
  - relation: requires
    target: ca-spikes-couple-20ms-before-ap
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: beta-gates-distal-apical-inputs

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig5, fig7
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig5.ipynb, scripts/Fig7.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — phase-binned dendritic spike analysis
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig5.ipynb
    script_execution: pre-computed
    script_execution_note: "Requires 1.88 GB Dryad download (DendCompOscPublic/); no individual file access available"
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Scripts: Fig5.ipynb and Fig7.ipynb both require Dryad simulation files from
      DendCompOscPublic/ (rhythmic inhibition simulations at 16 Hz and 64 Hz).
      Phase-binned analysis code is in src/phase_analysis. Not in GitHub repo.
      Dryad API confirmed (2026-03-30): monolithic zip only (1.88 GB); no individual file access.
      Download Headley_etal_eLifeDRYAD.zip, extract DendCompOscPublic/, install environment.yml
      (Python 3.9 + holoviews), run Fig5.ipynb and Fig7.ipynb.
---

Bidirectional control within a single beta cycle is a stronger claim than mere phase-dependent modulation — it asserts that the same inhibitory rhythm actively promotes spiking in one phase while suppressing it in another, rather than simply gating a uniform suppression. This bidirectional property emerges because the inhibitory trough provides a window of reduced conductance into which the slow Ca²⁺/NMDA spike dynamics can unfold. The epistemic status is moderate rather than strong because the quantitative asymmetry between trough-enhancement and peak-suppression is not extracted here; the claim is directionally clear but the relative magnitudes were not verified.
