---
uuid: 73da2169-c0ce-4ae2-85b2-42fb821ec872
slug: vmat2-gradient-absent
doi: ~
claim: >
  VMAT2 immunostaining shows no significant dorsoventral gradient in striatum (p=0.0086,
  one-sided t-test, n=4 mice), ruling out differential release capacity as the primary
  explanation for regional DA differences.
claim-type: empirical
role: control
concepts:
  - VMAT2
  - vesicular monoamine transporter
  - dorsoventral gradient
  - release capacity
  - immunostaining
priority: 2026-03-29
epistemic: moderate

rules-out:
  - "differential VMAT2 expression / vesicular release capacity as the explanation for the DS/VS DA difference"

validates:
  - hypothesis-vmax-explains-regional-difference

supports:
  - hypothesis-vmax-explains-regional-difference

belongings:
  - relation: supports
    target: hypothesis-vmax-explains-regional-difference

assertions:
  - paper-slug: ejdrup-2026-dopamine
    doi: 10.7554/eLife.105214
    panel: fig2—supplement 1A, fig2—supplement 1B, fig2—supplement 1C
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

The VMAT2 result is important as a negative control: it eliminates one alternative explanation for the regional DA difference (higher quantal release in VS). With VMAT2 uniform across the dorsoventral axis, the model's attribution of the regional contrast to DAT Vmax differences is strengthened by exclusion. The p-value (0.0086) is notable: this is a significant result in the direction consistent with no gradient (below a no-difference threshold), interpreted by the authors as evidence against a gradient. The small n (4 mice) limits the power to detect subtle gradients — the claim rules out gross differences rather than any gradient whatsoever. This is correctly reflected in the epistemic note.
