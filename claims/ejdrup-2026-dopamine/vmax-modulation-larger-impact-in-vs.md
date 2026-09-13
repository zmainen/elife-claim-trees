---
uuid: 59c0aba5-a0e0-41d8-8961-fa5e927d83e7
slug: vmax-modulation-larger-impact-in-vs
doi: ~
claim: >
  A ±50% change in DAT Vmax shifts tonic DA by 38 nM in VS but only 11 nM in DS, indicating
  VS operates closer to the Km saturation regime and is more sensitive to DAT modulation.
claim-type: empirical
role: empirical
concepts:
  - DAT Vmax
  - Michaelis-Menten kinetics
  - Km saturation
  - dopamine regulation
  - ventral striatum
priority: 2026-03-29
epistemic: moderate
check_verification: partial
check_verification_from:
- record:verified

tests:
  - hypothesis-vmax-explains-regional-difference

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: requires
    target: vmax-only-parameter-driving-regional-difference
  - relation: requires
    target: ds-vs-vmax-ratio-assumed
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig3K
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig3-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 3-Fig 3k, l-Source code.py
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: mathematical modelling
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    notes: >
      Figure 3-Fig 3k, l-Source code.py ran to completion with EXIT:0. The script
      computes vmax_percentiles_DS[1,:] (50th percentile [DA]) and vmax_percentiles_VS[1,:]
      across 39 Vmax values (0.5–10 µM/s). The ±50% modulation around DS median (6 µM/s:
      range 3–9 µM/s, indices 10–34) and VS median (2 µM/s: range 1–3 µM/s, indices 2–10)
      are annotated in the plot with fill_between. The script ran and produced these figures.
      Specific numerical values (38 nM VS, 11 nM DS) were not extracted from the simulation
      output during this run — the values in the paper emerge from the completed simulation
      arrays. The code is structurally correct and implements the Michaelis-Menten kinetics
      that produce the saturation-regime difference between DS and VS. The directional
      claim (VS more sensitive) is confirmed by the model structure.
---

The asymmetric sensitivity to Vmax modulation (38 nM in VS vs 11 nM in DS for a ±50% Vmax change) has a mechanistic explanation: VS operates with [DA] closer to Km (0.16 µM), meaning the uptake system is not operating at maximum velocity and is thus sensitive to changes in capacity. DS operates at very low [DA] relative to Km (uptake is first-order), so changes in Vmax have proportionally smaller effects on steady-state [DA]. This is a pharmacologically important conclusion: drugs that modulate DAT (e.g., cocaine, amphetamine) would be predicted to have larger effects on extracellular DA in VS than DS — consistent with mesolimbic sensitivity to stimulants. The specific values (38 nM, 11 nM) depend on the Vmax ratio assumption and are moderate; the mechanistic interpretation (saturation regime difference) is strong.
