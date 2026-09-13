---
uuid: 2a3eeb46-8619-4df2-8111-6e94460538aa
slug: insula-rois-responded-more-low
doi: null
claim: The insula ROIs responded more to low lottery outcomes for the partner in the Social than the Partner
  condition — even after subtracting responses to high outcomes — mirroring the behavioural guilt effect.
claim-type: empirical
role: empirical
concepts: []
priority: '2026-09-13'
tests:
- anterior-insula-tracks-guilt-insula
confirms:
- anterior-insula-tracks-guilt-insula
belongings:
- relation: supports
  target: anterior-insula-neural-substrate-guilt
- relation: requires
  target: during-receipt-lottery-versus-safe
assertions:
- paper-slug: gadeke-2026-guilt-insula
  doi: 10.7554/eLife.105391
  panel: fig4e
  readers: high
reproductions: []
warrant: moderate
warrant_why: confirms anterior-insula-tracks-guilt-insula and is validated by dot-products-between-individual-neural, but rests on the unsupported localizer during-receipt-lottery-versus-safe, so not strong
warrant_from:
- validated_by
- confirms
- requires
---

**Notes from extraction:** Caption states all coefficients and differences are significantly different from 0 (see Appendix 1—table 6).

**Relations.** Why each outgoing edge was inferred:

- `tests` → `anterior-insula-tracks-guilt-insula`: the insula ROI Social>Partner low-outcome response tests the insula BOLD prediction (results-127)
- `confirms` → `anterior-insula-tracks-guilt-insula`: insula ROIs responded more to low partner outcomes in Social, mirroring the guilt effect
- `supports` → `anterior-insula-neural-substrate-guilt`: the insula guilt-tracking response supports the insula-as-substrate hypothesis
- `requires` → `during-receipt-lottery-versus-safe`: the insula guilt ROI depends on the outcome-responsive localizer regions

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Thus, activation in our insula ROIs increased in situations during which participants experienced guilt for low outcomes impacting their partner, compared to similar outcomes resulting from the partner’s choices.

**caption-reader evidence:**
> voxels here responded more to low lottery outcomes (L) for the partner when these resulted from participant’s rather than the partner’s choices, even when responses to high outcomes were subtracted (L–H).
