---
uuid: 25ad6b4e-1066-424b-b337-98b5188b5553
slug: decisional-dimension-tradeoff
doi: ~
claim: >
  Across individuals, processing rate changes in the social decision dimension and the
  perceptual decision dimension are negatively correlated (r = -0.243, BF10 = 6.58),
  driven by differential allocation of relative attentional weights (r = -0.268,
  BF10 = 16.93): individuals who show stronger automatic self-prioritization at the
  perceptual level show less facilitation of self-associated information at the social level.
claim-type: empirical
role: empirical
concepts:
  - individual differences
  - decisional dimension
  - attentional trade-off
  - negative correlation
  - self-prioritization
priority: 2026-03-30
epistemic: moderate

confirms:
  - hypothesis-self-association-alters-attentional-selection
dissociates-with:
  - spe-matching-correlates-social-decision

belongings:
  - relation: requires
    target: self-prioritization-perceptual-decision-automatic
  - relation: requires
    target: self-prioritization-absent-social-decision

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig9
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig9-v1.tif/full/1500,/0/default.jpg
    analysis: OSF analysis notebooks (https://osf.io/a62df)
    dataset: https://osf.io/a62df
    dataset-doi: ~
    method: Bayesian correlation analysis across N=140
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    notes: >
      Partially verified from Correlation_Results.xlsx (OSF cross-exp folder). Pearson r
      computed from ΔΔv_Per vs ΔΔv_Soc for Exp1 (N=63): r = -0.211, p = 0.096
      (claim: r=-0.243, BF10=6.58). Sign confirmed. Magnitude close but not identical —
      the paper likely uses different exclusion criteria or computes the correlation across
      N=140 (both experiments combined). The separate weight correlation (r=-0.268 for Δwp)
      was not re-computed here. Direction of trade-off is confirmed.
---

The negative correlation is the individual-differences signature of the trade-off: participants who automatically prioritize self-associated shapes at the perceptual level are the same individuals who show the least facilitation when decoding the social identity. The paper interprets this as evidence that the perceptual and social processing stages compete for the same attentional resource, so strong automatic engagement at the perceptual level leaves fewer resources for the deliberate social decoding stage.
