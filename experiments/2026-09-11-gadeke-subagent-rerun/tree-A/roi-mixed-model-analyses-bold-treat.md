---
uuid: 8a272fa0-ec29-4d44-bda0-5d28a580e862
slug: roi-mixed-model-analyses-bold-treat
doi: null
claim: The ROI mixed-model analyses of BOLD treat individual voxels as observations with subject as the
  only random factor, giving observation counts in the tens to hundreds of thousands.
claim-type: assessment
role: methodological
concepts: []
priority: '2026-09-11'
epistemic: tentative
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  confidence: tentative
reproductions: []
---

**Notes from extraction:** The single most consequential auditor flag in the Structure-reader's slice: voxels within an ROI are spatially smoothed (8 mm FWHM) and therefore strongly dependent, so the N values in Appendix 1—tables 4–10 (e.g. N = 947,840 for dmPFC) are not independent observations. The resulting p-values and standard errors are anticonservative; effect directions remain interpretable but significance from these models should not be read as participant-level inference. Applies to the fig4c and fig4e LMM claims, where both the caption and the prose assert that all coefficients differ significantly from 0. Corrected whole-brain SPM results are unaffected.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> Similar to the behavioural data, we analysed GLM1 parameter estimates from voxels of specific regions of interest (see Results) using mixed-effects linear regressions with residual ε ij  ∼  N (0,  σε 2 ) and subject-specific random effects  uj  ∼  N (0,  σu 2 ). ... In all models,  Subject  was the only random factor (random intercept).
