---
uuid: 37d23efe-7e34-48aa-82ff-b7f3ef45751c
slug: rtn-neurons-impaired-excitability
doi: ~
claim: >
  Parvalbumin-positive reticular thalamic nucleus (RTN) neurons from juvenile (P16–21)
  Kcnc1-A421V/+ mice generate fewer rebound APs in response to hyperpolarizing current
  and show attenuated frequency-current relationship (*p=0.0109), with significantly
  reduced AP downstroke velocity (*p=0.034) but preservation of other membrane properties.
claim-type: empirical
role: empirical
concepts:
  - reticular thalamic nucleus
  - RTN
  - PV neurons
  - Kv3.1
  - rebound firing
  - excitability
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-impairment-grades-with-kv31-dependence
confirms:
  - prediction-impairment-grades-with-kv31-dependence
  - hypothesis-pv-in-selective-vulnerability

belongings:
  - relation: extends
    target: pv-ins-impaired-maximal-firing

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig4—figure supplement 3
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig4-figsupp3-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: whole-cell current-clamp, acute thalamic slices
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      n=19 Kcnc1-A421V/+ cells (N=5 mice), n=16 WT cells (N=4 mice). Significance by
      repeated-measures two-way ANOVA. RTN predominantly expresses Kv3.1 and Kv3.3
      (Porcello et al., 2002; Espinosa et al., 2008) — no Kv3.2 compensation as in layer V.
---

The RTN finding extends the impairment beyond neocortex and supports a cell-autonomous
mechanism: cells expressing Kv3.1 with minimal Kv3.2 compensation (RTN) show stronger
effects than those with partial Kv3.2 compensation (layer V cortex). This gradient of
impairment is strong evidence for a direct Kv3.1 loss-of-function mechanism.
