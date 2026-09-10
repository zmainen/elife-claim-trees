---
uuid: e1ce7be2-5fe7-4cda-80cb-775473b52e21
slug: gamma-gates-proximal-basal-inputs
doi: ~
claim: >
  Gamma-frequency rhythmic inhibition at perisomatic locations gates the transmission of
  clustered synaptic inputs from proximal and basal dendrites to somatic output in a
  phase-dependent manner, while leaving distal apical inputs relatively unaffected.
displayClaim: >
  Gamma-frequency perisomatic inhibition gates clustered proximal/basal inputs
  phase-dependently while leaving distal apical inputs largely unaffected.
claim-type: empirical
role: empirical
concepts:
  - gamma rhythm
  - perisomatic inhibition
  - synaptic input gating
  - basal dendrites
  - proximal inputs
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-orthogonal-input-gating

dissociates-with:
  - beta-gates-distal-apical-inputs

belongings:
  - relation: requires
    target: gamma-optimal-perisomatic-ap-modulation
  - relation: requires
    target: gamma-perisomatic-no-dendritic-spike-change
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
      Script: Fig10.ipynb requires Dryad files (exc_stim_aux_spikes2.h5). Same blocker as
      beta-gates-distal-apical-inputs. Dryad API confirmed (2026-03-30): monolithic zip only
      (1.88 GB). Download Headley_etal_eLifeDRYAD.zip, extract DendCompOscPublic/, install
      environment.yml (Python 3.9 + holoviews), run Fig10.ipynb.
---

The gamma/proximal gating result is the counterpart to the beta/distal gating: together they establish that the two inhibitory streams independently gate two different input pathways. Gamma perisomatic inhibition modulates AP threshold timing without suppressing dendritic spikes, so it controls which proximal/basal depolarizations cross threshold at the axon initial segment. The distal dendritic inputs (top-down) are relatively spared by perisomatic gamma because the Ca²⁺/NMDA spikes initiated in distal compartments are not directly controlled by perisomatic conductances.
