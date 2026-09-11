---
uuid: ce86ffb9-f29e-4374-b2d3-9c2c78927ba7
slug: ventral-striatum-tracks-computational-reward
doi: ~
claim: >
  Bilateral ventral striatum activation increases with the computational model's
  expected certain rewards and expected values of chosen lotteries (left: pFWE=0.002,
  T=5.63, d=0.75, Z=5.41, 110 voxels, MNI [−14 8 −8]; right: pFWE=0.005, T=5.46,
  d=0.70, Z=5.26, 80 voxels, MNI [10 10 −4]), validating the model-based fMRI approach
  as a manipulation check before the STS analysis.
claim-type: empirical
role: control
concepts:
  - ventral striatum
  - computational model
  - expected value
  - model-based fMRI
  - reward prediction error
priority: 2026-03-30
epistemic: strong

rules-out:
  - alt-model-based-glm-invalid
validates:
  - sts-tracks-partner-reward-prediction-errors

belongings:
  - relation: supports
    target: sts-tracks-partner-reward-prediction-errors

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig4g
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: master_fMRI_showResults.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: fMRI model-based GLM (GLM2, SPM12), whole-brain FWE-corrected
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-09-11
    status: verified
    script: verification/gadeke-2026-guilt-insula/verify.py
    script_execution: executed
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_file: fMRIresults/model-based/CR+EV_0p001u_k70_0p05FWE.nii
    paper_value: "L 110vox [-14 8 -8] T=5.63 · R 80vox [10 10 -4] T=5.46"
    reproduced_value: "110vox [-14, 8, -8] T=5.63 · 80vox [10, 10, -4] T=5.46"
    notes: >
      Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py. Paper: L 110vox [-14 8 -8] T=5.63 · R 80vox [10 10 -4] T=5.46. Reproduced: 110vox [-14, 8, -8] T=5.63 · 80vox [10, 10, -4] T=5.46. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts a re-run was attempted and could not settle the claim, and no re-run had been attempted. The deposited map makes this checkable without re-running the GLM.
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: Pre-computed NIfTI results in fMRIresults/ enable figure reproduction without re-running GLM.
---

The ventral striatum model-based result (fig4G) serves as a manipulation check for the GLM2 model-based approach before reporting the STS finding (fig4H). If GLM2 failed to replicate the canonical ventral striatum reward signal, the STS result would be suspect. The effect sizes here (d=0.70–0.75) are comparable to those from the conventional analysis (fig4A, d=0.72–0.85), providing mutual validation. This claim requires GLM2, not GLM1, and so is structurally dependent on the Responsibility computational model being fitted first to each participant's happiness data.
