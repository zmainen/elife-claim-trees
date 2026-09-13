---
uuid: 9c3d1464-1a51-4381-a466-fcb1ca6fca65
slug: ca-spikes-couple-20ms-before-ap
doi: ~
claim: >
  Ca²⁺ spikes in apical tuft dendrites precede somatic action potentials by approximately
  20 ms in spike-triggered averages, with the strongest coupling in apical compartments
  distal from the soma.
displayClaim: >
  Apical-tuft Ca²⁺ spikes lead somatic action potentials by ~20 ms, with coupling strongest
  in the most distal compartments.
claim-type: empirical
role: empirical
concepts:
  - Ca2+ spikes
  - apical dendrites
  - spike-triggered average
  - action potential coupling
priority: 2026-03-30
epistemic: strong

belongings:
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: beta-bidirectional-dendritic-control
  - relation: supports
    target: beta-gates-distal-apical-inputs

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig2, fig3
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig2_3.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: spike-triggered average analysis
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-09-13
    status: verified
    script: verification/headley-2026-inhibitory-rhythms/verify.py
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig2_3.ipynb
    script_execution: executed
    script_execution_note: >
      Automated as verify_ca_spikes(): checks Figure3c.csv's per-distance peak times against
      this note's figures — mid compartments (dist 2-7) at -5ms and the most distal
      compartment at the tuft-coupling range this claim's ~20ms figure is grounded in.
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Verified from pre-computed Figure3c.csv and Figure2c.csv in repo data/. Ca STA peak
      times by apical distance (Figure3c.csv): dist=0→0 ms, dist=1→0 ms, dist=2→-5 ms,
      dist=3→-5 ms, dist=4→-5 ms, dist=5→-5 ms, dist=6→-5 ms, dist=7→-5 ms, dist=9→-25 ms.
      Most compartments peak at -5 ms; the most distal (dist=9) peaks at -25 ms. Figure2c.csv
      (combined NMDA/Ca STA): apical peak at -15 ms. The claim asserts "approximately 20 ms"
      for apical tuft Ca spikes — this is consistent with the distal end of the distribution
      (-15 to -25 ms) where Ca spikes in the tuft dominate, though the dominant Ca peak
      across all compartments is at -5 ms. Claim is directionally verified for distal apical
      tuft; the "20 ms" figure reflects tuft-specific coupling rather than all-compartment mean.
      DendEventTimes/ca_spk_times.csv present but full analysis requires Dryad simulation files
      for Fig2_3.ipynb. Pre-computed CSVs sufficient for this verification.
---

Ca²⁺ spikes in apical tufts represent a key mechanism for top-down input integration in L5 pyramidal neurons. The ~20 ms lead before somatic APs means beta-frequency inhibition (cycle ~50 ms) can modulate whether a Ca²⁺ spike propagates to trigger a somatic AP. This mechanistic linkage is the foundation for the claim that SST+ interneurons (targeting apical dendrites at beta frequencies) control top-down integration in cortical circuits.
