---
uuid: fe6f5cc9-f01d-4c96-89fa-9932ae396b77
slug: target-excluded-fovea-in-99pct-saccades
doi: ~
claim: >
  The gaze-contingent paradigm successfully excluded the peripheral target from the central fovea (within 2° of visual angle) in 99.27% of saccades, validating that the decoded information was not due to direct foveal viewing of the target.
displayClaim: >
  The gaze-contingent display extinguished the peripheral target before it crossed into the central 2 degrees of visual angle on 99.27 percent of saccades, ruling out direct foveal stimulation as the source of the decoded signal.
claim-type: empirical
role: methodological
concepts:
  - gaze-contingent
  - stimulus exclusion
  - saccade
  - validity check
  - foveal eccentricity
priority: 2026-03-30
epistemic: strong

enables-method:
  - foveal-v1-decodes-peripheral-saccade-target
  - decoding-shape-sensitive-not-semantic
  - v1-category-decoding-drops-in-feedback
  - v2-v3-generalize-shape-not-category
  - cross-decoding-experimental-to-control
  - foveal-feedback-below-direct-stimulation
  - u-shaped-eccentricity-rejects-spillover
  - ips-foveal-effect-reverses-in-control
  - ips-candidate-driver-foveal-feedback

belongings: []

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig1C
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig1-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: eye tracking quality control, gaze-contingent fMRI
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Eye-tracking data are NOT on OpenNeuro. The README states "Eye Tracking
      data can be obtained upon request." The gaze analysis pipeline reads raw eye-tracker CSV files
      from /BULK/lkaemmer/data/foveal_decoding/data_eye/{sub}/*data*C1*.csv and computes per-saccade
      post-flip gaze distance (gaze_analysis.py). The 99.27% figure comes from the package_data()
      exclusion step using threshold 2.5° from foveal center. Without the eye-tracking CSV files
      (not publicly available), this specific validity statistic cannot be reproduced. Status
      unverified:compute-infeasible correctly reflects accessible code; however this particular
      claim also requires non-public eye data — contact dbheadley@newark.rutgers.edu or repo author.
---
