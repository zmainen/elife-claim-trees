---
uuid: 2b3e78d5-e3a7-4e42-9281-8594e67b4e30
slug: likelihood-ratio-test-showed-responsibility
doi: null
claim: 'A likelihood ratio test showed the Responsibility model fitted the happiness data better than
  all other models, including the Responsibility Redux model (Study 1: all LR ≥ 47.36, p < 0.0001; Study
  2: all LR ≥ 77.83, p < 0.0001).'
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-13'
tests:
- responsibility-partner-outcomes-influences-participant
confirms:
- responsibility-partner-outcomes-influences-participant
belongings:
- relation: supports
  target: responsibility-social-choice-yields-low
- relation: requires
  target: model-selection-among-happiness-models
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: table1
  readers: single-source
reproductions:
- carried_from: responsibility-modulates-guilt-computational
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: Computational model code in GitHub repo. Behavioral data in BehaviouralData/ directory (.mat
    files). MATLAB required. Not yet executed.
warrant: moderate
warrant_why: confirms the prediction responsibility-partner-outcomes-influences-participant and is supported by several happiness results
warrant_from:
- confirms
- supported_by
- requires
check_verification: unattempted
check_verification_from:
- record:unattempted
---

**Notes from extraction:** Kept separate from the R² comparison to preserve the results reader's distinct verbatim quote for each statistic.

**Relations.** Why each outgoing edge was inferred:

- `tests` → `responsibility-partner-outcomes-influences-participant`: the likelihood-ratio comparison tests whether the Responsibility model (with social_pRPE) fits best
- `confirms` → `responsibility-partner-outcomes-influences-participant`: the Responsibility model fitted better than all other models in both studies
- `supports` → `responsibility-social-choice-yields-low`: the Responsibility model's superior fit supports the responsibility/guilt account
- `requires` → `model-selection-among-happiness-models`: the model-comparison result depends on the likelihood-ratio selection procedure

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> a likelihood ratio test (Equation 9) revealed that the Responsibility model fitted better than all the other models, including the Responsibility Redux model (Study 1: all LR ≥47.36, p < 0.0001; Study 2: all LR ≥77.83, p < 0.0001).
