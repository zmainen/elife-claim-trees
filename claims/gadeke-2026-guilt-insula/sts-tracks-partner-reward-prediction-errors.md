---
uuid: e0633fdd-645b-4fa1-ae43-8d6b6b170000
slug: sts-tracks-partner-reward-prediction-errors
doi: ~
claim: >
  Superior temporal sulcus (STS) BOLD activity tracks partner reward prediction errors specifically when the participant was responsible for the choice, consistent with mentalizing about the partner's experiential state.
claim-type: empirical
role: empirical
concepts:
  - superior temporal sulcus
  - prediction error
  - mentalizing
  - partner reward
  - fMRI
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-sts-tracks-partner-rpe-under-responsibility
confirms:
  - hypothesis-sts-mentalizes-partner-state-under-responsibility

belongings:
[]

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig4h
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: master_fMRI_showResults.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: fMRI model-based analysis (computational happiness/responsibility model)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-11
    status: verified
    script: verification/gadeke-2026-guilt-insula/verify.py
    script_execution: executed
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_file: fMRIresults/model-based/pRPEsocial>pRPEpartner_0p001u_k70.nii
    paper_value: "left STS, pRPEsocial > pRPEpartner"
    reproduced_value: "99vox [-52, -32, 0] T=4.7"
    notes: >
      Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py. Paper: left STS, pRPEsocial > pRPEpartner. Reproduced: 99vox [-52, -32, 0] T=4.7. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts a re-run was attempted and could not settle the claim, and no re-run had been attempted. The deposited map makes this checkable without re-running the GLM.
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Model-based fMRI analysis requires computational model fitted to behavioral data. Model code in GitHub repo. Pre-computed group NIfTI results may be in fMRIresults/. Not yet executed.
---


