---
uuid: dba3c7b4-0a96-48cb-97d4-9aca0edbe90f
slug: dat-nanoclustering-slows-clearance
doi: ~
claim: >
  Dense DAT nanoclusters (20 nm diameter) take approximately 400 ms to clear a 100 nM DA bolus
  compared to approximately 200 ms for unclustered DAT, because local [DA] at the cluster
  surface drops near zero creating a diffusion-limited bottleneck.
claim-type: empirical
role: empirical
concepts:
  - DAT nanoclustering
  - dopamine clearance
  - diffusion limitation
  - varicosity-scale dynamics
priority: 2026-03-29
epistemic: moderate

tests:
  - hypothesis-nanoclustering-regulates-vmax

supports:
  - hypothesis-nanoclustering-regulates-vmax

belongings:
  - relation: requires
    target: nanoclustering-model-varicosity-scale
  - relation: requires
    target: nanoclustering-constant-vmax-constraint
  - relation: supports
    target: hypothesis-nanoclustering-regulates-vmax

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig4C, fig4D, fig4E, fig4F, fig4G
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 4-Fig 4 simulations-Source code.py
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
      Figure 4-Fig 4 simulations-Source code.py: computationally infeasible as written.
      The nanoclustering simulation uses dx=0.02 µm (varicosity scale), producing a
      90×90×352 grid (2.85M voxels) with dt=1.31×10⁻⁷ s and 3,052,000 steps for a
      0.4s simulation — estimated runtime ~43 hours at observed throughput (~19 it/s).
      The script timed out at 240s, completing <0.01% of steps. This is why the paper
      deposits pre-computed Zenodo data (https://doi.org/10.5281/zenodo.17664800):
      the simulation itself is not designed to be re-run from scratch. The plotting
      script (Figure 4-Fig 4a-e and g-i-Source code.py) requires sim_result_*.npy and
      steady_state_DAT_*.csv from Zenodo. Verification would require either downloading
      Zenodo data or running on a compute cluster. Code was not assessed for correctness.
  - agent: mainen-z
    date: 2026-03-26
    status: partial
    notes: >
      Zenodo deposit (DOI 10.5281/zenodo.17664800, latest record 18046987) downloaded
      2026-03-26. The deposit contains: 5 × sim_result_*.npy (9.1 GB each — 45 GB
      total, not feasible to download); 5 × steady_state_DAT_*.csv (12.5 kB each,
      downloaded); DAT_sim_gradient.csv, DAT_sim_conc_surface.csv (downloaded);
      DAT_clustering.csv (194 bytes, downloaded); dSTORM zip archives (1.3 GB + 966 MB).
      The burst clearance claim (400 ms vs 200 ms from 100 nM) is in Fig 4h and requires
      sim_result_*.npy — these were not downloaded. The 400 vs 200 ms numbers therefore
      remain unverified. The steady_state_DAT_*.csv files (Fig 4g, equilibrium [DA]) were
      successfully plotted: 20nm clusters reach 29.5 nM tonic equilibrium vs 15.4 nM for
      unclustered DAT — a 1.9× elevation consistent with the directional claim of slower
      effective clearance. The plotting script requires additional CSVs
      (DAT_sim_conc.csv, DAT_sim_rel_time.csv, DAT_sim_dist.csv, DAT_sim_DA_diff*.csv)
      not present in the Zenodo deposit — these correspond to an older simulation format
      and their absence prevents running the full script. Output: /tmp/ejdrup-2026/outputs/fig4/

discrepancy:
  type: methodological-gap
  explanation: >
    Nanoclustering simulation uses dx=0.02 um grid (2.85M voxels per timestep) making it computationally infeasible on a standard workstation. Zenodo data downloaded but simulation not re-run.
---

The mechanism is physically intuitive: when DAT molecules are concentrated into nanoclusters rather than distributed uniformly across the membrane, DA arriving at the membrane surface rapidly depletes local [DA] at the cluster to near zero, reducing the concentration gradient that drives further uptake. This is analogous to enzyme saturation at a local level — even though total Vmax is held constant, the effective clearance rate is lower because substrates must diffuse to the cluster location. The ~2× slower clearance (400 vs 200 ms) is the quantitative result. This claim is scoped to the varicosity-scale model and cannot be directly translated to tissue-scale predictions without the formal coupling that the assessment node (`nanoclustering-model-varicosity-scale`) identifies as absent.
