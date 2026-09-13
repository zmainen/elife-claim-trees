---
uuid: 744191f0-c636-4388-887c-cb552e458d9f
slug: parameter-recovery-procedure-synthetic-data-generated
doi: null
claim: A parameter-recovery procedure on synthetic data generated from each participant's estimated parameters
  showed the happiness-model parameters could be reliably recovered, verifying their stability.
claim-type: assessment
role: methodological
concepts: []
priority: '2026-09-12'
epistemic: tentative
enables-method:
- partner-reward-prediction-errors-resulting
belongings: []
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig3s1
  confidence: tentative
reproductions: []
---

**Notes from extraction:** All three readers surfaced this and agree on the substance and panel (fig3s1), but disagree on role/type: the results and caption readers classified it as a methodological assessment (a capability warranting the model-based analysis), while the structure reader classified it as an empirical control (claim_type empirical) validating parameter stability. Resolved to methodological by majority; recorded as contested because they disagree on whether it is an assessment or a result.

**Relations.** Why each outgoing edge was inferred:

- `enables-method` → `partner-reward-prediction-errors-resulting`: Parameter recovery warrants trusting the estimated social_pRPE weights (evidence at span results-068).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The stability of these estimated parameters was verified using a parameter recovery procedure (see Methods and Figure 3—figure supplement 1).

**caption-reader evidence:**
> Stability of the estimated parameters of the temporal difference models was evaluated by attempting to recover parameters from synthetic data created using each participant’s real estimated parameters.

**structure-reader evidence:**
> The results show that the estimated parameters could be reliably recovered from noisy synthetic data.
