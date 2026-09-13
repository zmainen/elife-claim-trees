---
uuid: eff3fbf5-c0c4-46e8-b43e-7b5e6208a969
slug: manipulation-check-bilateral-ventral-striatum
doi: null
claim: 'As a manipulation check, bilateral ventral striatum activation increased with expected certain
  rewards and the expected values of chosen lotteries, explained by a model-based regressor coding participant
  rewards (left: pFWE = 0.002, T = 5.63, d = 0.75; right: pFWE = 0.005, T = 5.46, d = 0.70).'
claim-type: empirical
role: control
concepts: []
priority: '2026-09-12'
epistemic: tentative
rules-out:
- alt-model-based-glm-invalid
validates:
- model-based-glm-entered-best-fitting-computational
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4g
  confidence: tentative
reproductions:
- carried_from: ventral-striatum-tracks-computational-reward
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: fMRIresults/model-based/CR+EV_0p001u_k70_0p05FWE.nii
  paper_value: L 110vox [-14 8 -8] T=5.63 · R 80vox [10 10 -4] T=5.46
  reproduced_value: 110vox [-14, 8, -8] T=5.63 · 80vox [10, 10, -4] T=5.46
  notes: 'Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py.
    Paper: L 110vox [-14 8 -8] T=5.63 · R 80vox [10 10 -4] T=5.46. Reproduced: 110vox [-14, 8, -8] T=5.63
    · 80vox [10, 10, -4] T=5.46. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts
    a re-run was attempted and could not settle the claim, and no re-run had been attempted. The deposited
    map makes this checkable without re-running the GLM.

    '
- carried_from: ventral-striatum-tracks-computational-reward
  agent: mainen-z
  date: 2026-03-30
  status: blocked
  blocked_by: compute-infeasible
  notes: Pre-computed NIfTI results in fMRIresults/ enable figure reproduction without re-running GLM.
---

**Notes from extraction:** The results reader treated this as a manipulation check validating the model-based BOLD analysis; the caption reader described it as a plain empirical result. Both agree on panel and direction; resolved to control.

**Relations.** Why each outgoing edge was inferred:

- `validates` → `model-based-glm-entered-best-fitting-computational`: The ventral-striatum manipulation check validates the model-based GLM (evidence at span results-134).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found that activation in bilateral ventral striatum indeed increased with the amount of expected certain rewards and the expected values of chosen lotteries (left: pFWE = 0.002, T = 5.63, d = 0.75, Z = 5.41, 110 voxels, peak at MNI [–14 8 –8], right: pFWE = 0.005, T = 5.46, d = 0.70, Z = 5.26, 80 voxels, peak at MNI [10 10 −4]).

**caption-reader evidence:**
> ( G ) Activation in bilateral ventral striatum explained by a computational model-based regressor coding participant rewards.
