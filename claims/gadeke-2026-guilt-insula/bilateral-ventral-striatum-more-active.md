---
uuid: 8eccf358-8cda-4fec-b608-34581e8afbe7
slug: bilateral-ventral-striatum-more-active
doi: null
claim: The bilateral ventral striatum was more active when participants chose the risky rather than the
  safe option (Cohen's d = 0.72 left, 0.85 right), irrespective of Social or Solo condition, replicating
  previous findings.
claim-type: empirical
role: control
concepts: []
priority: '2026-09-12'
epistemic: tentative
rules-out:
- alt-imaging-contrast-invalid
belongings:
- relation: supports
  target: manipulation-check-bilateral-ventral-striatum
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4a
  confidence: tentative
reproductions:
- carried_from: ventral-striatum-tracks-risky-choices
  agent: mainen-z
  date: 2026-09-11
  status: verified
  script: verification/gadeke-2026-guilt-insula/verify.py
  script_execution: executed
  data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
  data_file: fMRIresults/decision/risky>safe_0p05FWE_clust.nii
  paper_value: bilateral VS, risky>safe (d=0.72 / 0.85)
  reproduced_value: 401vox [10, 12, -4] T=7.18 · 390vox [-10, 8, -6] T=6.12
  notes: 'Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py.
    Paper: bilateral VS, risky>safe (d=0.72 / 0.85). Reproduced: 401vox [10, 12, -4] T=7.18 · 390vox [-10,
    8, -6] T=6.12. Recorded `blocked` until this run, which was inaccurate: `blocked` asserts a re-run
    was attempted and could not settle the claim, and no re-run had been attempted. The deposited map
    makes this checkable without re-running the GLM.

    '
- carried_from: ventral-striatum-tracks-risky-choices
  agent: mainen-z
  date: 2026-03-30
  status: blocked
  blocked_by: compute-infeasible
  notes: Pre-computed NIfTI results in fMRIresults/ enable figure reproduction without re-running GLM.
    Raw BOLD data available on OpenNeuro but full re-analysis requires SPM12/MATLAB.
---

**Notes from extraction:** The results reader treated this as a control replicating a known risk-related effect and validating the imaging analysis; the caption reader described it as a plain empirical result. Both are empirical measurements agreeing on panel and direction; resolved to control.

**Relations.** Why each outgoing edge was inferred:

- `supports` → `manipulation-check-bilateral-ventral-striatum`: Ventral-striatum activation to risky choices supports the model-based finding that the striatum tracks reward (evidence at span results-088).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We searched for brain regions engaged more when participants chose the risky instead of the safe option and found such responses in the bilateral ventral striatum (Cohen’s d = 0.72 and 0.85 in the left and right clusters, respectively; Figure 4A and Appendix 1—table 3), which replicates previous findings (Cui et al., 2022; Preuschoff et al., 2006).

**caption-reader evidence:**
> ( A ) Regions showing a greater response when participants chose the risky (lottery) rather than the safe option, irrespective of Social or Solo condition.
