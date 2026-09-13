---
uuid: 06c675dd-5a37-4e64-8af8-f02b15870215
slug: d2r-insensitive-to-brief-pauses
doi: ~
claim: >
  A complete 1 s pause in firing reduces D2R occupancy from approximately 0.55 to 0.45 only;
  this finding is robust across an order of magnitude of D2R affinity (2–20 nM).
claim-type: empirical
role: empirical
concepts:
  - D2 receptor
  - pause in firing
  - receptor occupancy
  - autoreceptor dynamics
priority: 2026-03-29
epistemic: weak
check_verification: partial
check_verification_from:
- record:verified

tests:
  - hypothesis-d1-d2-temporal-distinction

supports:
  - hypothesis-d1-d2-temporal-distinction

belongings:
  - relation: requires
    target: d2r-integrates-over-seconds
  - relation: requires
    target: d2r-initialization-unjustified
  - relation: supports
    target: hypothesis-d1-d2-temporal-distinction

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig1J
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: Figure 1-Fig 1j-Source code.py
    dataset: https://zenodo.org/record/17664800
    dataset-doi: 10.5281/zenodo.17664800
    method: mathematical modelling
    confidence: weak

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: verified
    notes: >
      Figure 1-Fig 1j-Source code.py ran to completion with EXIT:0, no errors (6 tqdm
      100% completions for 50^3, 17s simulation including a 1s firing pause). Script
      implements the D2R affinity sweep (Km range from 2 to 20 nM equivalent) and
      computes occupancy drop during the pause. The insensitivity claim (0.55→0.45
      drop) follows structurally from the D2R off-rate implementation — confirmed in
      code as k_off = 0.2 s⁻¹ decay. The D2R initialization at 0.4 (start_occ_D2=0.4)
      is confirmed again in this script. The directional finding is structurally robust;
      absolute occupancy values remain sensitive to initialization.
---

The insensitivity of D2R occupancy to 1 s pauses is a direct consequence of the slow off-kinetics established in `d2r-integrates-over-seconds`. The affinity sweep (2–20 nM EC50) is a genuine sensitivity analysis and supports the directional claim across a physiologically plausible range of D2R affinities — this is the strongest element of this claim. However, the absolute occupancy values (~0.55 at baseline, ~0.45 at pause nadir) are again sensitive to initialization, and the claim as stated quotes the absolute values explicitly. Epistemic is held at weak pending a sensitivity analysis on initialization. The directional conclusion — pauses are a weak D2R signal — is `moderate` on its own.
