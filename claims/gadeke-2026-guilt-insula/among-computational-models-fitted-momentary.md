---
uuid: 2b7d839d-9617-46ad-8d4e-dc19f19a6841
slug: among-computational-models-fitted-momentary
doi: null
claim: Among the computational models fitted to momentary happiness data, the Responsibility Redux model
  achieved the best (lowest) AIC in both studies (Study 1 AIC –1499; Study 2 AIC –1195).
claim-type: assessment
role: methodological
concepts: []
priority: '2026-09-13'
belongings:
- relation: requires
  target: momentary-happiness-modelled-five-computational
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: table1
  readers: single-source
reproductions: []
warrant: weak
warrant_why: an AIC ranking that requires momentary-happiness-modelled-five-computational; nothing in the tree validates or supports it
warrant_from:
- requires
check_verification: unrecorded
---

**Notes from extraction:** Best-fitting model inferred from the lowest AIC values (Study 2 Responsibility Redux AIC –1195). Note the apparent tension: the results reader instead reported the (non-Redux) Responsibility model as the best fit by likelihood-ratio test and R²; which model is 'best' depends on the metric, and the two readers anchored different models to Table 1, so they are not merged.

**Relations.** Why each outgoing edge was inferred:

- `requires` → `momentary-happiness-modelled-five-computational`: the Responsibility Redux AIC ranking (table1) requires the five happiness models to have been fitted

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> Responsibility Redux 4 0.361 0.331 –999 –1499
