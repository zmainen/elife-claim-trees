---
uuid: 3161ff4b-59d3-4fae-a466-17299dd3ba78
slug: likelihood-ratio-test-showed-responsibility
doi: null
claim: 'A likelihood ratio test showed the Responsibility model fitted the happiness data better than
  all other models, including the Responsibility Redux model (Study 1: all LR ≥ 47.36, p < 0.0001; Study
  2: all LR ≥ 77.83, p < 0.0001).'
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-13'
epistemic: tentative
tests:
- responsibility-partner-outcomes-influences-participant
confirms:
- responsibility-partner-outcomes-influences-participant
belongings:
- relation: requires
  target: momentary-happiness-modelled-five-computational
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: table1
  confidence: tentative
reproductions:
- carried_from: responsibility-modulates-guilt-computational
  agent: mainen-z
  date: 2026-03-30
  status: unattempted
  notes: Computational model code in GitHub repo. Behavioral data in BehaviouralData/ directory (.mat
    files). MATLAB required. Not yet executed.
---

**Notes from extraction:** Kept separate from the R² comparison to preserve the results reader's distinct verbatim quote for each statistic.

**Relations.** Why each outgoing edge was inferred:

- `tests` → `responsibility-partner-outcomes-influences-participant`: The likelihood-ratio result that the Responsibility model fits best tests the prediction that social_pRPE improves the fit.
- `requires` → `momentary-happiness-modelled-five-computational`: The likelihood-ratio comparison depends on the set of five happiness models.
- `confirms` → `responsibility-partner-outcomes-influences-participant`: The Responsibility model fitting the happiness data better than all others confirms the prediction that a model carrying social_pRPE explains happiness best.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> a likelihood ratio test (Equation 9) revealed that the Responsibility model fitted better than all the other models, including the Responsibility Redux model (Study 1: all LR ≥47.36, p < 0.0001; Study 2: all LR ≥77.83, p < 0.0001).
