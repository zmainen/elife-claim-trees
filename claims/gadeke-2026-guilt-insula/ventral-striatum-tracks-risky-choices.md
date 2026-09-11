---
uuid: 4585605a-6c71-4fd1-ab45-3ef5d2f449c8
slug: ventral-striatum-tracks-risky-choices
doi: ~
claim: >
  Bilateral ventral striatum shows greater BOLD response when participants choose the
  risky (lottery) rather than safe option, irrespective of Social or Solo condition
  (left cluster: Cohen's d=0.72; right cluster: d=0.85), replicating established striatal
  responses to risky decision-making.
claim-type: empirical
role: control
concepts:
  - ventral striatum
  - risky choice
  - fMRI
  - replication
  - reward
priority: 2026-03-30
epistemic: strong

rules-out:
  - alt-imaging-contrast-invalid
validates:
  - insula-tracks-guilt-effect
  - precuneus-tpj-mpfc-social-decisions

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig4a
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: master_fMRI_showResults.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: fMRI mass-univariate GLM (SPM12), whole-brain cluster-corrected (p<0.05 FWE)
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-09-11
    status: verified
    script: verification/gadeke-2026-guilt-insula/verify.py
    script_execution: executed
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_file: fMRIresults/decision/risky>safe_0p05FWE_clust.nii
    paper_value: "bilateral VS, risky>safe (d=0.72 / 0.85)"
    reproduced_value: "401vox [10, 12, -4] T=7.18 · 390vox [-10, 8, -6] T=6.12"
    notes: >
      Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py. Paper: bilateral VS, risky>safe (d=0.72 / 0.85). Reproduced: 401vox [10, 12, -4] T=7.18 · 390vox [-10, 8, -6] T=6.12. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts a re-run was attempted and could not settle the claim, and no re-run had been attempted. The deposited map makes this checkable without re-running the GLM.
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: Pre-computed NIfTI results in fMRIresults/ enable figure reproduction without re-running GLM. Raw BOLD data available on OpenNeuro but full re-analysis requires SPM12/MATLAB.
---

This is a manipulation check and replication claim. The authors include it to validate their fMRI pipeline and confirm their task evokes expected neural responses before proceeding to the novel social contrasts. The ventral striatum finding replicates Preuschoff et al. 2006 and Cui et al. 2022. This claim does not depend on the social manipulation and requires only GLM1 with the risky vs safe contrast.
