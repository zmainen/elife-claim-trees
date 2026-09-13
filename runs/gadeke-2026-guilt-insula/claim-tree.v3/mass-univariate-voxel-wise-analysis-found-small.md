---
uuid: 071373be-51ef-4d9f-8101-1379e5fae233
slug: mass-univariate-voxel-wise-analysis-found-small
doi: null
claim: A mass-univariate voxel-wise analysis found a small left anterior insula cluster (peak T = 3.95,
  d = 0.59, 22 voxels) responding more to low partner outcomes following participant than partner choices,
  which survived small-volume family-wise-error correction (p = 0.024).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-12'
epistemic: tentative
tests:
- anterior-insula-tracks-guilt-insula
belongings:
- relation: supports
  target: anterior-insula-neural-substrate-guilt
- relation: requires
  target: prior-literature-documents-association-between
- relation: requires
  target: during-receipt-lottery-versus-safe
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4f
  confidence: tentative
reproductions:
- carried_from: insula-tracks-guilt-effect
  agent: mainen-z
  date: 2026-03-30
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  original_figure: verification/originals/gadeke-2026-guilt-insula/fig4.jpg
  figure: verification/gadeke-2026-guilt-insula/fig-insula-peak.png
  original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
  script_execution: not-executed
  script_execution_note: Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI
    and CSV outputs.
  time_fast: ~3 min
  time_full: ~3 hrs (MATLAB + SPM12)
  notes: "NIfTI peak extraction from deposited fMRIresults/outcome/guiltEffect_0p05FWE_SVC_aIns.nii (FWE-corrected\
    \ SVC result, 2mm isotropic). After NaN-masking (592873 NaN voxels, 22 surviving FWE voxels), the\
    \ peak absolute value is 3.955 at voxel index (53, 68, 33). Applying the affine ([-2,0,0,78],[0,2,0,-112],[0,0,2,-70])\
    \ gives:\n  Peak MNI = [-28, 24, -4]\nThe deposited .mat file is named \"Group response at -28 24\
    \ -4 LeftInsulaGuiltEffect.mat\", confirming perfect match. The paper reports anterior insula peak\
    \ coordinates at [-28 24 -4] (left hemisphere). Claim verified: peak coordinates match and cluster\
    \ is restricted to anterior insula as described.\n"
- carried_from: insula-tracks-guilt-effect
  agent: mainen-z
  date: 2026-09-06
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  function: verify_insula_peak() (verify.py line 235)
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_commit: 11854fe
  data_file: fMRIresults/outcome/guiltEffect_0p05FWE_SVC_aIns.nii
  script_execution: executed
  script_execution_note: Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited
    analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run;
    that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12.
  paper_value: peak MNI [-28, 24, -4]
  reproduced_value: peak MNI [-28, 24, -4]
  notes: Loads the authors' deposited thresholded contrast map, finds the peak voxel, and applies the
    image affine to convert voxel indices to MNI millimetres. Exact match to the published coordinates.
---

**Notes from extraction:** The caption reader treated this as a control — convergent voxel-wise confirmation of the ROI-based insula guilt effect in panel E; the results reader treated it as the empirical voxel-wise guilt result. The small-volume FWE correction (p = 0.024) is reported in a following sentence by the results reader. Both are empirical measurements agreeing on panel and direction; resolved to empirical.

**Relations.** Why each outgoing edge was inferred:

- `tests` → `anterior-insula-tracks-guilt-insula`: The voxel-wise left-insula cluster surviving small-volume correction tests the insula prediction at the voxel level (evidence at span results-129).
- `supports` → `anterior-insula-neural-substrate-guilt`: The voxel-wise left-insula cluster independently supports the insula-substrate claim (evidence at span results-129).
- `requires` → `prior-literature-documents-association-between`: The small-volume correction on the left insula rests on the prior insula-guilt association (evidence at span results-129).
- `requires` → `during-receipt-lottery-versus-safe`: The voxel-wise insula cluster lies within the outcome-phase insula region (evidence at span results-129).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found a weak response in a small cluster within the left anterior insula (peak T = 3.95, d = 0.59, 22 voxels, peak intensity at [–28 24 –4]; Figure 4F).

**caption-reader evidence:**
> A cluster of voxels within the left insula ROI showed higher responses to low lottery outcomes for the partner if these resulted from participant rather than partner choices.
