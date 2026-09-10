---
uuid: 7b7dd3fd-3946-4947-9799-a4f8a8821aba
slug: beta-gates-distal-apical-inputs
doi: ~
claim: >
  Beta-frequency rhythmic inhibition at distal dendritic locations gates the transmission of
  clustered synaptic inputs from apical dendrites to somatic output: inputs arriving during
  inhibitory troughs are transmitted, while inputs arriving during peaks are blocked.
displayClaim: >
  Beta-frequency distal inhibition gates clustered apical-dendrite inputs phase-by-phase:
  inputs arriving in inhibitory troughs reach the soma, inputs arriving in peaks are blocked.
claim-type: empirical
role: empirical
concepts:
  - beta rhythm
  - distal inhibition
  - synaptic input gating
  - apical dendrites
  - phase-dependent transmission
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-orthogonal-input-gating

dissociates-with:
  - gamma-gates-proximal-basal-inputs

belongings:
  - relation: requires
    target: beta-bidirectional-dendritic-control
  - relation: requires
    target: beta-optimal-distal-dendritic-entrainment
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: pv-gamma-sst-beta-correspondence
  - relation: supports
    target: hypothesis-distinct-compartmental-roles

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig10
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig10-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig10.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — clustered input gating experiment
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig10.ipynb
    script_execution: pre-computed
    script_execution_note: "Requires Dryad exc_stim_aux_spikes2.h5 (1.88 GB); not in GitHub repo"
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Script: Fig10.ipynb requires Dryad files (exc_stim_aux_spikes2.h5 and associated
      simulation outputs from DendCompOscPublic/). exc_stim_aux_spikes2.h5 confirmed NOT in
      GitHub repo data/ (only spikes.h5 is present). Dryad API confirmed (2026-03-30): monolithic
      zip only (1.88 GB); no individual file access. Download Headley_etal_eLifeDRYAD.zip, extract
      DendCompOscPublic/, install environment.yml (Python 3.9 + holoviews), run Fig10.ipynb.
---

Figure 10 is the paper's functional payoff: it demonstrates that the phase-modulation results from Figures 5–9 translate directly into selective gating of specific input streams. Beta rhythms at distal locations gate apical (top-down) inputs in a phase-dependent way. This is the direct mechanistic link between the SST+/beta association and the functional role proposed for these interneurons in controlling top-down processing. The strong epistemic status reflects that this is a direct simulation of the gating function rather than an inference from firing rate changes.
