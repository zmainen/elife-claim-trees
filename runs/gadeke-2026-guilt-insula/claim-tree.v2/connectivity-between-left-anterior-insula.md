---
uuid: 942639c4-2e6a-49b6-b8aa-b0089d609e51
slug: connectivity-between-left-anterior-insula
doi: null
claim: Connectivity between the left anterior insula and the right inferior frontal gyrus varied with
  choice and condition, suggesting this prefrontal region is sensitive to guilt-related information during
  social choices.
claim-type: interpretive
role: interpretation
concepts: []
priority: '2026-09-11'
epistemic: tentative
interprets:
- functional-connectivity-between-left-anterior
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: null
  confidence: tentative
reproductions:
- carried_from: insula-ifg-connectivity-guilt
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: fMRIresults/PPI/aIns_seed/Risky>SafeXSolo>Social_0p001u_k30_2IFGs.nii
  paper_value: aIns seed, condition-dependent IFG coupling
  reproduced_value: 113vox [46, 16, 22] T=4.34 · 38vox [-38, -2, 26] T=4.08
  notes: 'Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py.
    Paper: aIns seed, condition-dependent IFG coupling. Reproduced: 113vox [46, 16, 22] T=4.34 · 38vox
    [-38, -2, 26] T=4.08. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts a
    re-run was attempted and could not settle the claim, and no re-run had been attempted. The deposited
    map makes this checkable without re-running the GLM.

    '
- carried_from: insula-ifg-connectivity-guilt
  agent: mainen-z
  date: 2026-03-30
  status: blocked
  blocked_by: compute-infeasible
  notes: gPPI analysis requires individual-level GLM outputs from OpenNeuro raw data. gPPI toolbox dependency.
    Group-level results may be in fMRIresults/ NIfTI files. Not yet executed.
---

**Notes from extraction:** Interpretation stated in the abstract.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Connectivity between this region and the right inferior frontal gyrus varied depending on choice and experimental condition, suggesting that this part of prefrontal cortex is sensitive to guilt-related information during social choices.
