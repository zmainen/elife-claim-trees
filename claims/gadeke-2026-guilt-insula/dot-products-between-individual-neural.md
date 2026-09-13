---
uuid: 079ebf00-e69a-40ab-863a-03d6a7d34129
slug: dot-products-between-individual-neural
doi: null
claim: Dot products between individual neural guilt responses and the Yu et al. (2020) guilt-related brain
  signature (GRBS) were overall positive (mean = 5.22, median = 6.97, sign test p = 0.017, Cliff's Delta
  = 0.4), providing convergent validity with a previously published neural guilt signature.
claim-type: empirical
role: control
concepts: []
priority: '2026-09-12'
epistemic: tentative
validates:
- insula-rois-responded-more-low
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  confidence: tentative
reproductions:
- carried_from: insula-guilt-replicates-yu-koban-signature
  agent: mainen-z
  date: 2026-03-30
  status: partial
  script: verification/gadeke-2026-guilt-insula/verify.py
  original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
  script_execution: not-executed
  script_execution_note: Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI
    and CSV outputs.
  time_fast: ~3 min
  time_full: ~3 hrs (MATLAB + SPM12)
  notes: "Implemented the dot-product pattern expression approach from f_apply_YuKoban_guilt_signature_map.m\
    \ in Python (nibabel). Loaded guiltEffectEachPartic.nii (4D, 40 participants) and Yu_guilt_SVM_sxpo_sxpx_EmotionForwardmask.nii,\
    \ resampled Yu map to guilt map space, then computed per-participant dot products within the Yu mask\
    \ (589,149 non-zero voxels). Results:\n  Mean dot product = 5.29 (SD=17.82), range [-41.5, 36.9]\n\
    \  N positive = 28/40\n  One-sample t-test vs 0: t=1.855, p=0.071 (marginal)\n  Wilcoxon signed-rank:\
    \ p=0.042\n  Sign test (binomial): p=0.017\nThe paper claims the guilt response is significantly above\
    \ 0. Our Python implementation gives marginal t-test but significant nonparametric tests, consistent\
    \ with the paper's use of signtest_nice (which tests median). The claim of consistency with Yu/Koban\
    \ signature is supported at p<0.05 by nonparametric test; t-test marginal. Claim status: verified\
    \ for the nonparametric result; the t-test is borderline, suggesting the pattern expression approach\
    \ (canlab apply_mask) may differ slightly from our resampling implementation.\n"
- carried_from: insula-guilt-replicates-yu-koban-signature
  agent: mainen-z
  date: 2026-09-10
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  function: verify_yu_koban() (verify.py line 278)
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_commit: 11854fe
  data_file:
  - fMRIresults/outcome/guiltEffectEachPartic.nii.zip
  - Code/bin/Yu_guilt_SVM_sxpo_sxpx_EmotionForwardmask.nii
  data_note: 'The first is 4D over 40 participants and ships in the deposit as .nii.zip; the second is
    the Yu & Koban signature mask, 50,860 voxels. The comparison is a dot product of the two.

    '
  script_execution: executed
  script_execution_note: Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited
    analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run;
    that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12.
  paper_value: sign test p < 0.05
  reproduced_value: sign p=0.008, wilcoxon p=0.021 (n_pos=28/40)
  notes: 'Read this entry together with its caveats; the numbers above did NOT come from the committed
    script as it currently stands. (a) Until this run the check had been failing in the committed verify.py
    for two separate reasons. First, the 4D per-participant guilt-effect map ships in the deposit zipped,
    as guiltEffectEachPartic.nii.zip, while the script''s file-search pattern only matched a plain .nii,
    so the input was never found. Second, the Yu/Koban signature mask was being resampled onto the 4-dimensional
    image rather than onto its 3-dimensional spatial grid, which produced a malformed transform. (b) Both
    are one-line fixes: match the zipped filename, and resample to guilt_img.shape[:3] using guilt_img.affine.
    (c) These fixes are NOT yet applied to the committed verify.py. The 2026-09-06 numbers were produced
    in a scratch copy of the script, so re-running the repository copy today will not reproduce them until
    the two fixes land. (d) The 2026-03-30 entry above records sign test p = 0.017 and Wilcoxon p = 0.042
    — the same direction and the same conclusion, but different figures, presumably from a different resampling
    choice. That discrepancy is unresolved, and both sets of numbers are recorded here deliberately rather
    than one replacing the other.

    '
---

**Notes from extraction:** [reviewer] role: empirical → control. The comparison against an independent, previously published neural guilt signature (Yu et al., 2020) is a convergent-validity check: its specific outcome - positive dot products - strengthens the warrant for the anterior insula as a guilt-tracking substrate rather than establishing a new primary finding, so its work in the argument is to validate the insula/guilt result. Provides convergent validity with a previously published neural guilt signature.

**Relations.** Why each outgoing edge was inferred:

- `validates` → `insula-rois-responded-more-low`: Positive GRBS dot products give convergent validity to the insula guilt response (evidence at span results-152).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The dot products between individual responses and the GRBS varied between –40.1 and 36.7, but overall these values were positive (mean = 5.22; median = 6.97; sign test: p = 0.017; Cliff’s Delta = 0.4 = medium effect size; data are not normally distributed).
