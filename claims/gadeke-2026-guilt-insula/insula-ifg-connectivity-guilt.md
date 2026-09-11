---
uuid: 8f7f9f33-a142-4962-b4cd-f161de239f2e
slug: insula-ifg-connectivity-guilt
doi: ~
claim: >
  Functional connectivity (gPPI) between anterior insula and inferior frontal gyrus varies by experimental condition, with increased coupling in the Social condition associated with the guilt effect.
claim-type: empirical
role: empirical
concepts:
  - insula
  - inferior frontal gyrus
  - gPPI
  - functional connectivity
  - guilt
priority: 2026-03-30
epistemic: moderate

interprets:
  - insula-tracks-guilt-effect

belongings:
  - relation: requires
    target: insula-tracks-guilt-effect


assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig5
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: c_gPPI.m, master_fMRI_showResults.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: gPPI functional connectivity (SPM12 + gPPI toolbox)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-11
    status: verified
    script: verification/gadeke-2026-guilt-insula/verify.py
    script_execution: executed
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_file: fMRIresults/PPI/aIns_seed/Risky>SafeXSolo>Social_0p001u_k30_2IFGs.nii
    paper_value: "aIns seed, condition-dependent IFG coupling"
    reproduced_value: "113vox [46, 16, 22] T=4.34 · 38vox [-38, -2, 26] T=4.08"
    notes: >
      Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py. Paper: aIns seed, condition-dependent IFG coupling. Reproduced: 113vox [46, 16, 22] T=4.34 · 38vox [-38, -2, 26] T=4.08. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts a re-run was attempted and could not settle the claim, and no re-run had been attempted. The deposited map makes this checkable without re-running the GLM.
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      gPPI analysis requires individual-level GLM outputs from OpenNeuro raw data. gPPI toolbox dependency. Group-level results may be in fMRIresults/ NIfTI files. Not yet executed.
---


