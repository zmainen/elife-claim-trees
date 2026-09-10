---
uuid: 5e63c146-b0e8-457b-8fdc-5751afaefb2a
slug: u-shaped-eccentricity-rejects-spillover
doi: ~
claim: >
  Decoding accuracy in the experimental condition follows a U-shaped function of eccentricity — stronger at foveal and peripheral regions, weaker at parafoveal regions — in all early visual areas (V1: t(27)=3.98, p=0.008; V2: t(27)=3.03, p=0.02; V3: t(27)=2.776, p=0.025, one-sided quadratic curvature), ruling out peripheral spillover as an explanation for foveal decoding.
displayClaim: >
  Decoding accuracy across V1, V2, and V3 dips at parafoveal eccentricities and rises again at the fovea, a U-shaped profile that is incompatible with passive spillover from large peripheral receptive fields.
claim-type: empirical
role: control
concepts:
  - eccentricity
  - peripheral spillover
  - U-shaped profile
  - early visual cortex
  - foveal feedback
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-u-shape-eccentricity
rules-out:
  - "passive spillover from large peripheral receptive fields"
interprets:
  - interprets-williams-2008-peripheral-spillover

belongings:
  - relation: supports
    target: foveal-v1-decodes-peripheral-saccade-target
  - relation: supports
    target: hypothesis-feedback-not-spillover

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig2B
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: weighted quadratic regression on eccentricity-binned decoding accuracy, fMRI
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Requires retinotopic ROI construction (FSL retinotopic localizer FEAT →
      thresh_zstat{d}.nii.gz per eccentricity degree) plus eccentricity-binned decoding across 10 bins
      (5 retinotopy-based, 5 Benson atlas-based). Implemented in decoding_by_eccentricity.py via
      prepare_all_data(retinotopy=True, eccen=True). Both ROI construction and MVPA require the full
      preprocessed data pipeline (fMRIPrep → FSL FEAT → zstat NIfTIs; same ~100 CPU-hour requirement).
      No pre-computed eccentricity-binned results exist in the repo. Three-source confidence: found by
      all three extraction passes.
---

The U-shaped eccentricity profile is the key control ruling out the peripheral-spillover alternative. If decoding in foveal V1 were driven by large receptive fields reaching into the periphery (cf Williams et al. 2008), one would expect a monotonic relationship between peripheral and foveal decoding in the experimental condition. Instead, the decoding dip at parafoveal eccentricities dissociates foveal feedback from direct peripheral activation. The control condition shows the expected monotonic decay (strongest at center), providing a clean contrast. All three quadratic curvature tests survive at p<0.05 (one-sided), though the preregistration did not preregister this specific test.
