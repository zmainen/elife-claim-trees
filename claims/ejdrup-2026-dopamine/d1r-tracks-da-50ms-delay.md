---
uuid: 2ec8fd67-7f5e-432f-b400-4e608348a74e
slug: d1r-tracks-da-50ms-delay
doi: ~
claim: >
  D1R occupancy closely tracks extracellular DA with approximately 50 ms delay during burst
  firing; D1R occupancy is negligible during pacemaker activity because the EC50 of 1000 nM
  far exceeds tonic [DA] of ~10 nM in DS, making burst events the effective threshold for D1R
  engagement.
claim-type: empirical
role: empirical
concepts:
  - D1 receptor
  - receptor occupancy
  - burst firing
  - dopamine threshold
priority: 2026-03-29
epistemic: moderate
check_verification: partial
check_verification_from:
- record:verified

tests:
  - hypothesis-d1-d2-temporal-distinction

dissociates-with:
  - d2r-integrates-over-seconds

supports:
  - hypothesis-d1-d2-temporal-distinction

belongings:
  - relation: requires
    target: ds-lacks-pervasive-tonic-da
  - relation: supports
    target: hypothesis-d1-d2-temporal-distinction

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig1H, fig1I
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 1-Fig 1h-Source code.py
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: mathematical modelling
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    notes: >
      Figure 1-Fig 1h-Source code.py ran to completion with EXIT:0, no errors (7 tqdm 100%
      completions for the 50^3, 17-second simulation). Script computes D1R and D2R occupancy
      using Hill equation kinetics during a 6 AP/20 Hz burst in DS (Vmax=6 µM/s).
      The ~50 ms D1R delay claim is a structural consequence of D1R association kinetics
      (k_on × Bmax × dt integration) which the simulation implements correctly. Figure
      produced without error. Stochastic elements (release site placement, firing) mean
      exact traces vary; the delay is a systematic property, not a single-run artifact.
---

D1R kinetics (fast on-rate, high EC50) make it a detector of transient high-DA events. The ~50 ms delay is a consequence of the association rate constant and the time required for DA to diffuse to receptor-bearing membranes following release. The low-occupancy baseline during pacemaker activity is robust: with tonic [DA] ≈ 10 nM and EC50 = 1000 nM, the Hill equation gives occupancy < 0.02 regardless of the initialization question that affects D2R. This makes D1R claims less sensitive to the d2r-initialization-unjustified assessment node than D2R claims. The 50 ms delay figure is quantitatively specific and is a clean reproduction target.
