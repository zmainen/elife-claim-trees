---
uuid: b7b55f60-7438-47fd-a42a-431bcbaf696b
slug: gamma-perisomatic-no-dendritic-spike-change
doi: ~
claim: >
  Gamma-frequency perisomatic rhythms phase-modulate action potential threshold without
  substantially altering overall dendritic spike rates, demonstrating functional orthogonality
  between the perisomatic-gamma and distal-beta inhibitory streams.
claim-type: empirical
role: empirical
concepts:
  - gamma rhythm
  - perisomatic inhibition
  - dendritic spike rates
  - functional orthogonality
  - AP threshold
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-perisomatic-threshold-mechanism

belongings:
  - relation: requires
    target: perisomatic-inhib-drops-firing-07hz
  - relation: requires
    target: gamma-optimal-perisomatic-ap-modulation
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: pv-gamma-sst-beta-correspondence
  - relation: supports
    target: hypothesis-distinct-compartmental-roles

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig5.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — dendritic event rate comparison
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig5.ipynb
    script_execution: pre-computed
    script_execution_note: "Static case verified from pre-computed CSV; rhythmic gamma panels require 1.88 GB Dryad data"
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Partially verified from Figure4d-f.csv pre-computed data. Somatic (perisomatic
      inhibition) vs control dendritic spike rates: Ca spike freq = 4.84 vs 4.86 Hz
      (0.4% change); NMDA freq = 4.19 vs 4.28 Hz (2.1% change); Na freq = 2.27 vs 2.12 Hz
      (unchanged). Under static doubling of perisomatic inhibition, dendritic spike rates
      are preserved while somatic firing drops from 5.5 → 0.7 Hz. This is the key
      non-interference result. The rhythmic gamma modulation (Fig5.ipynb) requires Dryad
      simulation files from DendCompOscPublic/ for full frequency-sweep verification, but
      the static case (which the claim is grounded in) is confirmed. Claim verified for
      the static case; rhythmic modulation at 40-80 Hz needs Dryad data.
---

The orthogonality claim — that gamma perisomatic and beta distal streams operate independently — is one of the paper's central theoretical contributions. If true, it implies that cortical circuits can simultaneously modulate somatic output (via PV+/gamma) and distal dendritic integration (via SST+/beta) without interference. The moderate epistemic status reflects that "not substantially altering" is a qualitative claim; the quantitative threshold for "substantial" was not defined, and small effects on dendritic spike rates under gamma perisomatic inhibition are possible but not ruled out.
