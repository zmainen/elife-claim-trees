---
uuid: cc992651-67bd-4d1b-9237-fa13d9f9ec94
slug: fscv-matches-may-wightman-1989
doi: ~
claim: >
  Simulated FSCV responses to 10, 30, and 60 Hz stimulation closely replicate May & Wightman
  (1989): VS reaches considerably higher peak DA than DS at all three stimulation frequencies.
claim-type: empirical
role: empirical
concepts:
  - FSCV
  - dopamine release
  - dorsal striatum
  - ventral striatum
  - stimulation frequency
priority: 2026-03-29
epistemic: moderate

tests:
  - hypothesis-vmax-explains-regional-difference

validates:
  - vs-maintains-pervasive-tonic-da
  - ds-lacks-pervasive-tonic-da
  - ds-vs-vmax-ratio-assumed

supports:
  - hypothesis-vmax-explains-regional-difference

interprets:
  - interprets-may-wightman-1989-fscv

belongings:
  - relation: requires
    target: vs-maintains-pervasive-tonic-da
  - relation: requires
    target: ds-vs-vmax-ratio-assumed
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig2E
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 2-Fig 2g, h-Source code.py
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: mathematical modelling
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      The FSCV simulation (Figure 2-Fig 2g, h-Source code.py) requires running the full
      tissue-scale model for 10, 30, and 60 Hz stimulation conditions in both DS and VS.
      Script execution timed out during the simulation runs. The Fig2g/h script uses the same
      matplotlib w_xaxis API (not confirmed broken here, but VS simulation runs upstream).
      Pre-computed output arrays for Fig 2g/h were not found in the Zenodo deposit for this
      specific panel. Workaround: download zenodo.17664800 and check for fig2_fscv_* .npy
      arrays; if present, plotting section can run immediately.
---

Matching the May & Wightman (1989) FSCV dataset provides an important empirical anchor: this is a direct comparison to real experimental data rather than an internal model consistency check. The match supports the model's parameterization (Vmax ratio, release probability, quantal size) as reproducing observed regional differences. The epistemic caveat is that May & Wightman used rat striatal slices while this model is parameterized for in vivo mouse — slice preparation removes tonic activity, alters extracellular volume fraction, and may affect Km estimates. The qualitative pattern (VS > DS across frequencies) is robust; the quantitative match should be interpreted with these species and preparation differences in mind.
