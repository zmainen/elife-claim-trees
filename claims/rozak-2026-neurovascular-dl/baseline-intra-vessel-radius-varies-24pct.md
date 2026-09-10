---
uuid: 083ef4c3-9e93-4927-9867-3c785b2c03c0
slug: baseline-intra-vessel-radius-varies-24pct
doi: ~
claim: >
  Capillary radius varies along vessel length by 24±28% of the mean resting radius across
  baseline frames, such that point measurements of vessel caliber cannot accurately estimate
  microvessel volume changes.
claim-type: empirical
role: empirical
concepts:
  - intra-vessel radius heterogeneity
  - capillary morphology
  - point measurement limitation
  - vessel volume
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-pipeline-reveals-network-coordination
confirms:
  - hypothesis-network-level-nvc-coordination
  - synthesis-individual-vessel-measurements-insufficient
rules-out:
  - alt-point-measurement-estimates-vessel-volume

belongings:
  - relation: supports
    target: vessel-radius-heterogeneity-stimulation

assertions:
  - paper-slug: rozak-2026-neurovascular-dl
    doi: 10.7554/eLife.95525
    panel: fig7
    figureUri: https://iiif.elifesciences.org/lax/95525%2Felife-95525-fig7-v1.tif/full/1500,/0/default.jpg
    analysis: Tutorial.ipynb
    dataset: https://doi.org/10.20383/103.01588
    dataset-doi: 10.20383/103.01588
    method: vertex-wise radius tracking along centerline, 2PFM, n=17 mice
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      This is a baseline measurement (not a stimulation result). The 24±28% figure is reported
      in the Results prose ("Vascular morphology and heterogeneity within and among vessels")
      and instantiated in Figure 7 which shows vertex-wise profiles along an artery, capillary,
      and venule. The large SD (28%) relative to the mean (24%) indicates highly skewed
      distribution across vessels.
---

This claim carries methodological implications for the entire 2PFM literature: it argues that
single-point caliber measurements (the historical standard) systematically misrepresent vessel
volume. The 24±28% within-vessel variation is a property of the imaging technique capturing
true biological heterogeneity — but the large SD also raises the question of whether the
variation is partly measurement noise. The paper does not disentangle biological heterogeneity
from estimation variance at the vertex level.
