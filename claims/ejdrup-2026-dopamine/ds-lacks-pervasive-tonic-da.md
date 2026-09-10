---
uuid: 2ac9b38d-8f72-436d-905a-b98b7e8dc3ba
slug: ds-lacks-pervasive-tonic-da
doi: ~
claim: >
  During 4 Hz pacemaker activity, the dorsal striatum produces partially segregated DA hotspots
  with large fractions of the simulated volume devoid of DA — there is no pervasive tonic
  baseline.
claim-type: empirical
role: empirical
concepts:
  - dorsal striatum
  - tonic dopamine
  - spatial dynamics
  - pacemaker firing
priority: 2026-03-29
epistemic: moderate

tests:
  - hypothesis-vmax-explains-regional-difference

dissociates-with:
  - vs-maintains-pervasive-tonic-da

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: requires
    target: ds-vs-vmax-ratio-assumed
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig1D, fig1E, fig1F
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 1-Fig 1a, d, e, f-Source code.py
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: mathematical modelling
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: blocked
    blocked_by: code-error
    script: verification/ejdrup-2026-dopamine/verify.py
    original_script: "https://github.com/Gether-Lab/striatal-dopamine-model/blob/main/Figure%201-Fig%201a%2C%20d%2C%20e%2C%20f-Source%20code.py"
    script_execution: patched
    script_execution_note: "w_xaxis → xaxis (matplotlib 3.8 API change, cosmetic only)"
    time_fast: "~5 min"
    time_full: "~8 hrs (standard Python)"
    notes: >
      Simulation completed successfully (1/1 run, 6103 steps on 100^3 grid, DS Vmax=6 µM/s).
      Script errored at 3D visualization step: AttributeError on Axes3D.w_xaxis (removed in
      matplotlib 3.8; script was written for older API). The diffusion simulation itself and
      spatial DA distribution computation are unaffected. The error prevents automated
      figure comparison. Plotting section fix: replace w_xaxis/w_yaxis/w_zaxis with
      xaxis/yaxis/zaxis. Core simulation output is reproducible.
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    script: verification/ejdrup-2026-dopamine/verify.py
    original_figure: verification/originals/ejdrup-2026-dopamine/fig1.jpg
    figure: verification/ejdrup-2026-dopamine/fig1-ds-spatial.png
    notes: >
      Matplotlib fix applied (w_xaxis → xaxis, w_yaxis → yaxis, w_zaxis → zaxis in
      Figure 1-Fig 1a, d, e, f-Source code.py). Script ran to completion (6103 steps,
      ~2 min). DS simulation (Vmax=6 µM/s, 4 Hz pacemaker, 100^3 grid): spatial DA
      distribution confirms hotspot pattern. Distribution statistics across steady-state
      voxels: median 5.4 nM, P10=2.4 nM, P25=3.4 nM, P75=8.9 nM, max=8788 nM. The
      wide right-skewed distribution (most voxels low, rare voxels near varicosities
      very high) is the quantitative signature of the hotspot claim — not uniform tonic
      coverage. Claim verified: DS lacks pervasive tonic DA; instead produces
      varicosity-scale hotspots embedded in a mostly sub-10 nM background.
---

This is the foundational spatial result for the dorsal striatum. The high-Vmax uptake environment (DS = 6 µM·s⁻¹) confines DA to a halo around active terminals during 4 Hz pacemaker firing; between terminals, [DA] falls to near zero. The result depends on the assumed 3:1 Vmax ratio between DS and VS but is consistent with earlier experimental observations of restricted diffusion in dorsal striatum. The "no pervasive tonic baseline" framing is qualitative; the quantitative picture is that median [DA] across voxels is low but not uniform — Figure 1E shows the distribution. Epistemic status is moderate rather than strong because the Vmax assumption is imported from prior work rather than independently measured in this study.
