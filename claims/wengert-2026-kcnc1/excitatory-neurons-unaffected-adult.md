---
uuid: 3df55d45-b8a0-42c6-9807-0323c08e8815
slug: excitatory-neurons-unaffected-adult
doi: ~
claim: >
  Excitatory neurons from adult (P32–42) Kcnc1-A421V/+ mice show no significant differences
  from WT in AP firing frequency across current injection magnitudes, and show no significant
  alterations in passive membrane properties or single AP properties (Table 2), with the
  sole exception of reduced rheobase (*p=0.023) whose functional significance is uncertain.
claim-type: empirical
role: control
concepts:
  - excitatory neurons
  - cell-type selectivity
  - adult
  - intrinsic excitability
  - null result
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-excitatory-neurons-spared
confirms:
  - prediction-excitatory-neurons-spared
validates:
  - pv-in-inhibitory-synapse-altered-adult

belongings:
  - relation: extends
    target: excitatory-neurons-unaffected-juvenile

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig5—figure supplement 1D, Table 2 (layer IV exc. cells)
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig5-figsupp1-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: whole-cell current-clamp, adult slice preparation
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      n=12 WT (N=4 mice), n=12 Kcnc1-A421V/+ (N=4 mice). One significant result: rheobase
      reduced in Kcnc1-A421V/+ (*p=0.023 by unpaired t-test, Table 2). The paper does not
      comment on this isolated finding. All other comparisons non-significant by repeated-
      measures two-way ANOVA. Confidence rated moderate because of the isolated rheobase
      finding that goes unexplained — could be a true secondary network effect or Type I error.
---

The adult excitatory neuron null result is an important complement to the juvenile null
in fig5. Both together support the conclusion that excitatory neuron impairment is not a
direct effect of the A421V variant (consistent with excitatory cells lacking Kv3.1 expression).
The unexplained rheobase reduction at adult stage warrants flag as a potential secondary
effect that could become significant in a larger-N study.
