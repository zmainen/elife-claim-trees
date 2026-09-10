---
uuid: e3b92961-38ad-41b2-a66f-65e328d33a2e
slug: vs-low-active-fraction-resembles-ds-distribution
doi: ~
claim: >
  VS at 5% active terminals produces a spatial DA distribution resembling DS at 100% active
  terminals, demonstrating VS operates in a low-focality high-coverage regime while DS requires
  dense terminal participation for equivalent spatial reach.
claim-type: empirical
role: empirical
concepts:
  - active terminal fraction
  - spatial DA distribution
  - focality
  - dopamine coverage
priority: 2026-03-29
epistemic: moderate

tests:
  - hypothesis-vmax-explains-regional-difference

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: requires
    target: vs-maintains-pervasive-tonic-da
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig3B
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 3-Fig 3b, c, e-g-Source code.py
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
      Figure 3-Fig 3b, c, e-g-Source code.py sweeps active terminal fraction across many
      values in both DS and VS. The 5% vs 100% comparison (fig3B) requires multiple simulation
      runs. Script execution timed out before completing the sweep. Fig3B is a 2D spatial heatmap
      comparison — reproduction requires either re-running the simulations (hours of compute)
      or pre-computed spatial arrays from Zenodo. Check zenodo.17664800 for fig3b_*.npy arrays.
---

The visual comparison of VS (5% active terminals) versus DS (100% active terminals) maps makes the qualitative point about regime difference concrete: despite sparse release in VS, the lower uptake capacity allows DA to diffuse broadly, producing spatial coverage comparable to dense release in the high-uptake DS environment. This regime interpretation is mechanistically coherent and is a clean conceptual result from Figure 3B. The "resembling" language in the claim is appropriately qualitative — the paper makes a visual comparison rather than a formal statistical similarity test. Epistemic is moderate because the comparison is descriptive and depends on the Vmax assumption setting the scale of the uptake regimes.
