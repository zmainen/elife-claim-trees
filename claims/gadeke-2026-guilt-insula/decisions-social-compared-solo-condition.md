---
uuid: 077e31a7-4fa3-471e-b1a7-aeba86331dca
slug: decisions-social-compared-solo-condition
doi: null
claim: Decisions in the Social compared with the Solo condition engaged three clusters — the precuneus
  (d = 0.79), left temporo-parietal junction (d = 0.59), and medial prefrontal cortex (d = 0.54).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-13'
belongings:
- relation: requires
  target: each-trial-participants-chose-between
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4b
  readers: high
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
warrant: weak
warrant_why: an fMRI contrast that requires the paradigm each-trial-participants-chose-between; no control or support bears on it
warrant_from:
- requires
---

**Relations.** Why each outgoing edge was inferred:

- `requires` → `each-trial-participants-chose-between`: the Social>Solo contrast requires the three-condition (Solo/Social/Partner) choice paradigm to have been run

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Three significant clusters of voxels were identified (Figure 4B and Appendix 1—table 3), in the precuneus (d = 0.79), the left temporo-parietal junction (TPJ; d = 0.59) and the medial prefrontal cortex (mPFC; d = 0.54).

**caption-reader evidence:**
> ( B ) Regions showing a greater response when participants chose for both themselves and their partner rather than just for themselves (Social > Solo).
