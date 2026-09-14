---
uuid: 16d67552-5456-47aa-a8e7-b2f8a6dba280
slug: parameter-recovery-procedure-synthetic-data-generated
doi: null
claim: A parameter-recovery procedure on synthetic data generated from each participant's estimated parameters
  showed the happiness-model parameters could be reliably recovered, verifying their stability.
claim-type: assessment
role: methodological
concepts: []
priority: '2026-09-13'
enables-method:
- responsibility-redux-model-incorporating-expected
validates:
- responsibility-redux-model-incorporating-expected
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig3s1
  readers: contested
reproductions: []
warrant: weak
warrant_why: the tree records nothing bearing on this methodological check
check_verification: unrecorded
---

**Notes from extraction:** All three readers surfaced this and agree on the substance and panel (fig3s1), but disagree on role/type: the results and caption readers classified it as a methodological assessment (a capability warranting the model-based analysis), while the structure reader classified it as an empirical control (claim_type empirical) validating parameter stability. Resolved to methodological by majority; recorded as contested because they disagree on whether it is an assessment or a result.

**Relations.** Why each outgoing edge was inferred:

- `enables-method` → `responsibility-redux-model-incorporating-expected`: parameter recovery establishes the model estimates are stable enough to trust the fit
- `validates` → `responsibility-redux-model-incorporating-expected`: the parameter-recovery procedure (fig3s1) verifies the Responsibility Redux estimates are stable, strengthening the fit

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The stability of these estimated parameters was verified using a parameter recovery procedure (see Methods and Figure 3—figure supplement 1).

**caption-reader evidence:**
> Stability of the estimated parameters of the temporal difference models was evaluated by attempting to recover parameters from synthetic data created using each participant’s real estimated parameters.

**structure-reader evidence:**
> The results show that the estimated parameters could be reliably recovered from noisy synthetic data.
