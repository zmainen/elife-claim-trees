---
uuid: a4af1338-dbef-4dad-ba5d-699735dc08df
slug: foveal-v1-decodes-peripheral-saccade-target
doi: ~
claim: >
  Saccade target identity (4 stimuli varying in shape and semantic category) can be decoded from foveal V1 BOLD signal above chance in the experimental condition where targets disappear before fixation: 57.43% accuracy (t(27)=8.81, p<0.001), significantly above 50% chance.
displayClaim: >
  Foveal V1 carries decodable information about peripheral saccade targets even when those targets are extinguished before the eye lands, demonstrating retinotopically anticipatory feedback into early visual cortex.
claim-type: empirical
role: empirical
concepts:
  - foveal V1
  - decoding accuracy
  - saccade target
  - peripheral target
  - MVPA
priority: 2026-03-30
epistemic: strong

belongings: []

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig2A
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: multivariate decoding (cross-validated classification), fMRI
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): No pre-computed results anywhere in repo or OpenNeuro.
      OpenNeuro ds005933 (61 GB raw BIDS) contains only raw BOLD NIfTI files — no derivatives folder,
      no pre-computed betas or zstats. Code path: (1) fMRIPrep v20.2.0 (Docker) on raw BOLD → MNI-space
      preprocessed data at /BULK/lkaemmer/…/data_out/{sub}/foveal_decoding/run_N/stats/zstat*.nii.gz;
      (2) FSL FEAT on each run (feat_foveal_decoding_template.fsf) to generate per-block z-stats;
      (3) decoding_shape_category.ipynb / decoding_by_eccentricity.py (sklearn SVC, nilearn masking)
      reads those z-stats and runs leave-one-run-out cross-validation across 28 subjects.
      Minimum steps to verify 57.43%: download ds005933 (~61 GB), run fMRIPrep per subject (~4h GPU
      each × 28 subjects), run FSL FEAT GLM per run (~1h × 10 runs × 28 subjects), then run
      decoding notebook (~30 min). Total: ~100 CPU-hours minimum, GPU required for fMRIPrep.
      No shortcut: eye-tracking data (needed for trial exclusion, constitute=99.27% saccade check)
      are explicitly not on OpenNeuro ("available upon request" per README).
---
