---
uuid: b5f7aa26-4228-4741-8680-93ebd04474fa
slug: cross-decoding-experimental-to-control
doi: ~
claim: >
  Cross-decoding from experimental (feedback) to control (direct stimulation) condition yields 57.2% accuracy (t(27)=5.22, p<0.001), indicating that the representational format of foveal feedback is similar to that of direct foveal stimulation.
displayClaim: >
  Classifiers trained on foveal feedback responses generalize to direct foveal stimulation, indicating that feedback uses a representational format shared with bottom-up sensory drive.
claim-type: empirical
role: empirical
concepts:
  - cross-decoding
  - representational format
  - feedback
  - direct stimulation
  - MVPA
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-cross-decoding-generalizes

belongings:
  - relation: supports
    target: hypothesis-shared-representational-format

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig2B
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: cross-condition multivariate decoding, fMRI
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Requires same full pipeline as foveal-v1-decodes-peripheral-saccade-target.
      Cross-decoding (train on experimental, test on control) is implemented in run_cross_condition_classifier()
      in foveal_decoding.py using sklearn cross_val_predict. Both conditions' zstat files must be present.
      No pre-computed cross-decoding matrices exist in the repo or OpenNeuro. Same ~100 CPU-hour
      minimum requirement as the within-condition decoding claim.
---
