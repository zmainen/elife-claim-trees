---
uuid: c1fca5f1-0911-43e7-ab37-08816a073dfc
slug: decisions-social-compared-solo-condition
doi: null
claim: Decisions in the Social compared with the Solo condition engaged three clusters — the precuneus
  (d = 0.79), left temporo-parietal junction (d = 0.59), and medial prefrontal cortex (d = 0.54).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-11'
epistemic: tentative
belongings:
- relation: requires
  target: all-reported-clusters-survive-whole-brain
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4b
  confidence: tentative
reproductions:
- carried_from: precuneus-tpj-mpfc-social-decisions
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: fMRIresults/decision/social>solo_0p05FWE_clust.nii
  paper_value: '3 clusters: precuneus, left TPJ, mPFC'
  reproduced_value: 758vox [0, -62, 38] T=5.72 · 216vox [-34, -58, 26] T=4.5 · 135vox [4, 52, 22] T=3.97
  notes: 'Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py.
    Paper: 3 clusters: precuneus, left TPJ, mPFC. Reproduced: 758vox [0, -62, 38] T=5.72 · 216vox [-34,
    -58, 26] T=4.5 · 135vox [4, 52, 22] T=3.97. Recorded `blocked` until this run, which was inaccurate:
    `blocked` asserts a re-run was attempted and could not settle the claim, and no re-run had been attempted.
    The deposited map makes this checkable without re-running the GLM.

    '
- carried_from: precuneus-tpj-mpfc-social-decisions
  agent: mainen-z
  date: 2026-03-30
  status: blocked
  blocked_by: compute-infeasible
  notes: Pre-computed NIfTI results in fMRIresults/ enable figure reproduction without re-running GLM.
---

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Three significant clusters of voxels were identified (Figure 4B and Appendix 1—table 3), in the precuneus (d = 0.79), the left temporo-parietal junction (TPJ; d = 0.59) and the medial prefrontal cortex (mPFC; d = 0.54).

**caption-reader evidence:**
> ( B ) Regions showing a greater response when participants chose for both themselves and their partner rather than just for themselves (Social > Solo).
