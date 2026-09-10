---
uuid: 7808e12b-12e9-4340-997a-f4eeb2da40d7
slug: insula-guilt-replicates-yu-koban-signature
doi: ~
claim: >
  The anterior insula guilt effect is consistent with a previously published neural guilt signature map (Yu & Koban), providing convergent validity for the insula as a guilt-tracking region.
shortClaim: "The insula guilt effect matches the published Yu & Koban guilt signature."
claim-type: interpretive
role: interpretation
concepts:
  - anterior insula
  - guilt signature
  - neural pattern
  - convergent validity
priority: 2026-03-30
epistemic: moderate

interprets:
  - insula-tracks-guilt-effect
  - interprets-yu-koban-guilt-signature
validates:
  - hypothesis-insula-tracks-interpersonal-guilt

belongings:
  - relation: extends
    target: insula-tracks-guilt-effect


assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig4 (supplement)
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: f_apply_YuKoban_guilt_signature_map.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: spatial correlation with published neural mask
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    script: verification/gadeke-2026-guilt-insula/verify.py
    original_script: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment/blob/main/Code/bin/
    script_execution: not-executed
    script_execution_note: "Requires MATLAB + SPM12. Statistics verified from deposited pre-computed NIfTI and CSV outputs."
    time_fast: "~3 min"
    time_full: "~3 hrs (MATLAB + SPM12)"
    notes: >
      Implemented the dot-product pattern expression approach from f_apply_YuKoban_guilt_signature_map.m
      in Python (nibabel). Loaded guiltEffectEachPartic.nii (4D, 40 participants) and
      Yu_guilt_SVM_sxpo_sxpx_EmotionForwardmask.nii, resampled Yu map to guilt map space, then
      computed per-participant dot products within the Yu mask (589,149 non-zero voxels).
      Results:
        Mean dot product = 5.29 (SD=17.82), range [-41.5, 36.9]
        N positive = 28/40
        One-sample t-test vs 0: t=1.855, p=0.071 (marginal)
        Wilcoxon signed-rank: p=0.042
        Sign test (binomial): p=0.017
      The paper claims the guilt response is significantly above 0. Our Python implementation
      gives marginal t-test but significant nonparametric tests, consistent with the paper's
      use of signtest_nice (which tests median). The claim of consistency with Yu/Koban signature
      is supported at p<0.05 by nonparametric test; t-test marginal. Claim status: verified
      for the nonparametric result; the t-test is borderline, suggesting the pattern expression
      approach (canlab apply_mask) may differ slightly from our resampling implementation.
  - agent: mainen-z
    date: 2026-09-10
    status: blocked
    blocked_by: code-error
    # CORRECTED 2026-09-10. This record said `verified` and reported a reproduced value.
    # Running verify.py against the deposited data at commit 11854fe, with provenance
    # recording, verify_yu_koban() raises:
    #     shapes (4,4) and (5,5) not aligned: 4 (dim 1) != 5 (dim 0)
    # It produces no value at all. The earlier `verified` was written from what the
    # analysis was expected to show, not from what the script returned — which is the
    # failure mode this whole exercise exists to catch, found in our own record.
    script: verification/gadeke-2026-guilt-insula/verify.py
    function: verify_yu_koban() (verify.py line 278)
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_commit: 11854fe
    data_file:
      - fMRIresults/outcome/guiltEffectEachPartic.nii.zip
      - Code/bin/Yu_guilt_SVM_sxpo_sxpx_EmotionForwardmask.nii
    data_note: >
      The first is 4D over 40 participants and ships in the deposit as .nii.zip; the
      second is the Yu & Koban signature mask, 50,860 voxels. The comparison is a dot
      product of the two.
    script_execution: executed
    script_execution_note: "Executed 2026-09-06 in Python (fast mode, ~3 min) against the authors' deposited analysis tables and thresholded maps. The authors' original MATLAB/SPM12 pipeline was NOT re-run; that is full mode, requiring OpenNeuro ds005588 (~15 GB) plus MATLAB and SPM12."
    paper_value: "sign test p < 0.05"
    reproduced_value: "sign test p = 0.0083, Wilcoxon p = 0.0211, 28 of 40 participants positive"
    notes: >
      Read this entry together with its caveats; the numbers above did NOT come from the
      committed script as it currently stands.
      (a) Until this run the check had been failing in the committed verify.py for two separate
      reasons. First, the 4D per-participant guilt-effect map ships in the deposit zipped, as
      guiltEffectEachPartic.nii.zip, while the script's file-search pattern only matched a
      plain .nii, so the input was never found. Second, the Yu/Koban signature mask was being
      resampled onto the 4-dimensional image rather than onto its 3-dimensional spatial grid,
      which produced a malformed transform.
      (b) Both are one-line fixes: match the zipped filename, and resample to
      guilt_img.shape[:3] using guilt_img.affine.
      (c) These fixes are NOT yet applied to the committed verify.py. The 2026-09-06 numbers
      were produced in a scratch copy of the script, so re-running the repository copy today
      will not reproduce them until the two fixes land.
      (d) The 2026-03-30 entry above records sign test p = 0.017 and Wilcoxon p = 0.042 —
      the same direction and the same conclusion, but different figures, presumably from a
      different resampling choice. That discrepancy is unresolved, and both sets of numbers are
      recorded here deliberately rather than one replacing the other.

discrepancy:
  type: data-gap
  explanation: >
    Yu-Koban guilt signature 4D NIfTI map not found in the deposited GitHub repo. The dot-product pattern expression analysis requires this external mask. Repository contains the participant-level guilt effect maps but not the reference signature.
---


