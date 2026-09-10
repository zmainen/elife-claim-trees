---
uuid: c714f46f-4715-4d61-90d8-fdac5fffa159
slug: dat-immunostaining-dorsoventral-gradient
doi: ~
claim: >
  DAT expression is significantly higher in dorsal than ventral striatum (p=0.0021, one-sided
  t-test, n=4 mice), corroborating the 3:1 Vmax ratio assumed in the model.
claim-type: empirical
role: empirical
concepts:
  - DAT
  - dopamine transporter
  - dorsoventral gradient
  - immunostaining
  - protein expression
priority: 2026-03-29
epistemic: moderate

validates:
  - ds-vs-vmax-ratio-assumed
  - hypothesis-vmax-explains-regional-difference

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: supports
    target: ds-vs-vmax-ratio-assumed
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig2—supplement 1B, fig2—supplement 1C
    figureUri: https://iiif.elifesciences.org/lax/105214%2Felife-105214-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: immunostaining
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-29
    status: blocked
    blocked_by: no-data
    notes: Raw immunostaining data not in Zenodo deposit; reproduction would require original tissue samples.
---

The significant DAT immunostaining gradient (p=0.0021, DS > VS) provides the primary empirical support for the 3:1 Vmax ratio that underpins the model's regional differentiation. The p-value is strong for n=4, suggesting the effect size is large. The caveat — protein level does not directly establish functional Vmax — is real: surface trafficking, phosphorylation state, and endogenous substrate availability all affect transport rate independently of total protein. The claim correctly limits itself to "corroborating" the ratio rather than establishing it. The `supports` belonging to `ds-vs-vmax-ratio-assumed` expresses this: the immunostaining provides convergent evidence for an assumption the model inherits from prior functional studies.
