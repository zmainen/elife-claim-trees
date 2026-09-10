---
uuid: 4ee66306-a11b-4333-86cf-47ea92155e76
slug: beta-optimal-distal-dendritic-entrainment
doi: ~
claim: >
  In a frequency sweep from 0.5 to 80 Hz, beta frequencies near 20 Hz produce the strongest
  phase-dependent entrainment of dendritic Ca²⁺ and NMDA spike onsets by distal rhythmic
  inhibition, as measured by Pairwise Phase Consistency.
displayClaim: >
  Across a 0.5–80 Hz frequency sweep, distal inhibition near 20 Hz (beta) most strongly
  entrains the timing of dendritic Ca²⁺ and NMDA spike onsets.
claim-type: empirical
role: empirical
concepts:
  - beta rhythm
  - dendritic spike entrainment
  - distal inhibition
  - frequency sweep
  - Pairwise Phase Consistency
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-beta-optimal-distal

belongings:
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: beta-bidirectional-dendritic-control
  - relation: supports
    target: beta-gates-distal-apical-inputs
  - relation: supports
    target: pv-gamma-sst-beta-correspondence
  - relation: supports
    target: hypothesis-frequency-compartment-matching

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig7
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig7-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig7.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — frequency sweep, Pairwise Phase Consistency (PPC)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig7.ipynb
    script_execution: pre-computed
    script_execution_note: "Frequency sweep simulations require 1.88 GB Dryad DendCompOscPublic/"
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Script: Fig7.ipynb requires Dryad simulation files from DendCompOscPublic/
      (frequency sweep simulations across 0.5–80 Hz distal inhibition conditions).
      These are not in the GitHub repo. PPC analysis code is implemented in src/ modules.
      Dryad API confirmed (2026-03-30): monolithic zip only (1.88 GB); no individual file access.
      Download Headley_etal_eLifeDRYAD.zip, extract DendCompOscPublic/, install environment.yml
      (Python 3.9 + holoviews), run Fig7.ipynb.
---

The beta optimum at ~20 Hz is mechanistically interpretable: the beta cycle period (~50 ms) matches the temporal window over which Ca²⁺ and NMDA spikes build to threshold (Ca²⁺ ~20 ms, NMDA ~25 ms lead before APs, from Figures 2–3). Slower rhythms allow multiple spikes per cycle; faster rhythms truncate the integration window. The beta optimum emerges from this temporal matching between the rhythm period and the intrinsic spike dynamics, not from an arbitrary parametric choice. Epistemic status is strong because the frequency sweep result is a systematic parametric scan with an unambiguous peak.
