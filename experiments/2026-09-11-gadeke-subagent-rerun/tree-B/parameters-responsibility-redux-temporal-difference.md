---
uuid: 49662fe8-d9cd-40c4-806d-d5176a07880e
slug: parameters-responsibility-redux-temporal-difference
doi: null
claim: Parameters of the Responsibility Redux temporal difference model could be reliably recovered from
  synthetic happiness data generated from each participant's estimated parameters with 1SD of added noise.
claim-type: assessment
role: control
concepts: []
priority: '2026-09-11'
epistemic: tentative
belongings:
- relation: supports
  target: study-computational-model-taking-into
- relation: supports
  target: study-responsibility-redux-computational-model
- relation: supports
  target: among-five-computational-models-fitted
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig3s1
  confidence: tentative
reproductions: []
---

**Notes from extraction:** Asymmetry between readers, and the reason this is worth flagging: the Caption-reader can see only the recovery procedure and marked the claim tentative because the caption states no recovery outcome (no slope or correlation values); the Structure-reader has the methods sentence asserting that recovery succeeded. The assertion therefore rests on the authors' summary, not on a quantitative value either reader can see — check Figure 3—figure supplement 1 at review. Structure-reader's further caveat: recovery is demonstrated only for the generating model and does not address model identifiability (whether Responsibility and Guilt-envy can be told apart from data). Role revised to control per the caption-preference rule.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> Stability of the estimated parameters of the temporal difference models was evaluated by attempting to recover parameters from synthetic data created using each participant's real estimated parameters. After fitting each participant's momentary happiness data (see above), we synthesized new momentary happiness data based on each participant's estimated parameters, added 1SD of noise to the happiness data, fitted the model to these synthetic data, and repeated this procedure 10 times, for both studies.

**structure-reader evidence:**
> After fitting each participant's momentary happiness data (see above), we synthesized new momentary happiness data based on each participant's estimated parameters, added 1SD of noise to the happiness data, fitted the model to these synthetic data, and repeated this procedure 10 times, for both studies. ... The results show that the estimated parameters could be reliably recovered from noisy synthetic data.
