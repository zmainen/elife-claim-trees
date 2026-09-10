---
uuid: 6271606c-1989-4bb6-a6da-a14145a46145
slug: foveal-feedback-below-direct-stimulation
doi: ~
claim: >
  Foveal feedback decoding (57.43%) is significantly below direct foveal stimulation decoding (84.06%, t(27)=19.92, p<0.001), indicating that feedback information is weaker than direct sensory input in foveal V1.
displayClaim: >
  The feedback signal in foveal V1 is reliably weaker than the response to direct foveal stimulation, consistent with a low-bandwidth top-down channel rather than a fully reinstated sensory representation.
claim-type: empirical
role: empirical
concepts:
  - foveal feedback
  - direct stimulation
  - decoding accuracy comparison
  - foveal V1
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
    method: multivariate decoding, condition comparison
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Same pipeline as foveal-v1-decodes-peripheral-saccade-target —
      requires full fMRIPrep + FSL FEAT + MVPA pipeline on ds005933 (61 GB). The control condition
      (direct foveal stimulation, 84.06%) is analyzed in the same notebook (decoding_shape_category.ipynb,
      condition="control" branch). Both conditions require the same preprocessed zstat NIfTI files.
      No control-condition-specific shortcut exists.
---
