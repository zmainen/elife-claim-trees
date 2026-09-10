---
uuid: 1ef1d1ae-1c10-4951-bd72-5fe9e3df202d
slug: vs-maintains-pervasive-tonic-da
doi: ~
claim: >
  With DAT Vmax reduced to 33% of DS and terminal density at 90%, VS produces a diffuse
  tonic-like DA level throughout the simulated volume rather than segregated hotspots during
  4 Hz pacemaker activity.
claim-type: empirical
role: empirical
concepts:
  - ventral striatum
  - tonic dopamine
  - spatial dynamics
  - DAT Vmax
priority: 2026-03-29
epistemic: moderate

tests:
  - hypothesis-vmax-explains-regional-difference

dissociates-with:
  - ds-lacks-pervasive-tonic-da

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: requires
    target: ds-lacks-pervasive-tonic-da
  - relation: requires
    target: ds-vs-vmax-ratio-assumed
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig2A, fig2B, fig2C
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 2-Fig 2a-f-Source code.py
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
    original_script: "https://github.com/Gether-Lab/striatal-dopamine-model/blob/main/Figure%202-Fig%202a-f-Source%20code.py"
    script_execution: patched
    script_execution_note: "w_xaxis → xaxis (matplotlib 3.8 API change, cosmetic only)"
    time_fast: "~5 min"
    time_full: "~8 hrs (standard Python)"
    notes: >
      Figure 2-Fig 2a-f-Source code.py: all 3 simulations ran to completion (4 tqdm
      100% bars before error, for DS, VS, and VS-reduced terminal density conditions,
      each on a 100^3 grid for 2s). The simulation code is structurally correct — VS
      uses Vmax=2 µM/s vs DS Vmax=6 µM/s, implementing the 3:1 ratio. The script
      errored at the 3D visualization step: AttributeError on Axes3D.w_xaxis (same
      matplotlib 3.8 API incompatibility as Fig1a script). Simulation outputs were
      computed but figures were not generated for visual comparison. Error is in
      plotting only; the spatial DA distribution computation ran successfully.
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    script: verification/ejdrup-2026-dopamine/verify.py
    original_figure: verification/originals/ejdrup-2026-dopamine/fig2.jpg
    figure: verification/ejdrup-2026-dopamine/fig2-ds-vs-spatial.png
    notes: >
      Matplotlib fix applied (w_xaxis → xaxis etc. in Figure 2-Fig 2a-f-Source code.py).
      Script ran to completion (61039 steps total across 3 conditions, ~8 min). VS
      simulation (Vmax=2 µM/s, 4 Hz, 100^3 grid): DA is diffuse throughout volume.
      Post-equilibration (t>2s cutoff) percentile statistics: VS median=20.9 nM,
      VS mean=24.2 nM, VS P2.5=12.6 nM. VS minimum across all voxels/time: 8.1 nM.
      Compare DS: median=5.5 nM, mean=9.1 nM. The VS distribution is compressed into
      a narrow high-concentration band (all voxels 8–200+ nM) versus DS's broad
      right-skewed hotspot distribution. Claim verified: VS produces pervasive diffuse
      tonic-like DA; the 3:1 Vmax reduction causes the qualitative regime change.
---

The pervasive tonic DA in VS is the complement of the DS result and follows mechanistically from the same model with reduced uptake capacity. The two parameters changed between DS and VS are Vmax (6 → 2 µM·s⁻¹) and terminal density (100% → 90% active). The density change is small and the Vmax change dominates. Figure 2A shows volumetric DA maps analogous to Figure 1D, now displaying broad coverage rather than isolated hotspots. This is the founding VS result on which the regional receptor occupancy, FSCV, and parameter sweep claims all depend. Epistemic is moderate because both the Vmax ratio and the terminal density assumption are inherited from prior literature.
