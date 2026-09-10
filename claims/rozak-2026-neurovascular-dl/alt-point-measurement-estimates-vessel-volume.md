---
uuid: d58f5ce7-bd4f-461e-9b01-4550aa813eff
slug: alt-point-measurement-estimates-vessel-volume
doi: ~
claim: >
  Vessel caliber measured at a single point along a capillary is an adequate estimate of
  microvessel volume change, so point measurements suffice for quantifying neurovascular
  coupling without volumetric segmentation.
claim-type: interpretive
role: hypothesis
concepts:
  - point measurement
  - vessel caliber
  - alternative explanation
priority: 2026-09-10
epistemic: weak

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    stance: rejects
    method: agent extraction of the alternative named in the paper's baseline variability result
    confidence: weak

reproductions: []
---

An alternative the paper argues against, not a proposition it asserts. It is the standing
practice this work displaces: measuring a vessel's diameter at one location and treating the
result as a proxy for its volume.

`baseline-intra-vessel-radius-varies-24pct` closes it directly — capillary radius varies along
vessel length by 24±28% of the mean resting radius across baseline frames alone, so a point
measurement carries a variability comparable to the effect it is being used to detect.

Before this claim existed that result's `rules-out` and `contradicts` relations both pointed at
`novas3d-outperforms-ilastik`, a segmentation-benchmark claim about an entirely different
matter, because the standing practice had no node to point at.
