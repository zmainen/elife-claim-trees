---
uuid: c47aae16-e029-4c77-8164-f7c3c92df662
slug: one-cluster-left-sts-responded
doi: null
claim: One cluster in the left STS responded more to partner reward prediction errors resulting from participant
  rather than partner choices (pFWE = 0.022, T = 4.70, d = 0.53, 100 voxels, peak MNI [−52 –32 0]).
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-11'
epistemic: tentative
tests:
- neural-substrate-tracks-participant-responsibility-2
belongings:
- relation: requires
  target: model-based-glm-entered-best-fitting-computational
- relation: requires
  target: all-reported-clusters-survive-whole-brain
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4h
  confidence: tentative
reproductions:
- carried_from: sts-tracks-partner-reward-prediction-errors
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: fMRIresults/model-based/pRPEsocial>pRPEpartner_0p001u_k70.nii
  paper_value: left STS, pRPEsocial > pRPEpartner
  reproduced_value: 99vox [-52, -32, 0] T=4.7
  notes: 'Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py.
    Paper: left STS, pRPEsocial > pRPEpartner. Reproduced: 99vox [-52, -32, 0] T=4.7. Recorded `blocked`
    until this run, which was inaccurate: `blocked` asserts a re-run was attempted and could not settle
    the claim, and no re-run had been attempted. The deposited map makes this checkable without re-running
    the GLM.

    '
- carried_from: sts-tracks-partner-reward-prediction-errors
  agent: mainen-z
  date: 2026-03-30
  status: blocked
  blocked_by: compute-infeasible
  notes: Model-based fMRI analysis requires computational model fitted to behavioral data. Model code
    in GitHub repo. Pre-computed group NIfTI results may be in fMRIresults/. Not yet executed.
---

**Notes from extraction:** Caption notes this is restricted to brain regions sensitive to outcomes of risky choices.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found this effect in one cluster within the left STS (pFWE = 0.022, T = 4.70, d = 0.53, Z = 4.57, 100 voxels, peak at MNI [−52 –32 0]; Figure 4H).

**caption-reader evidence:**
> one cluster in the left superior temporal sulcus region showed a higher response to partner reward prediction errors resulting from participant rather than partner choices.
