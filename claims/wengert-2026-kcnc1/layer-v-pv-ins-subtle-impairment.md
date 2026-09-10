---
uuid: d6e81203-d9f1-4344-97d0-48ec7b6afe39
slug: layer-v-pv-ins-subtle-impairment
doi: ~
claim: >
  Layer V neocortical PV-INs from juvenile (P16–21) Kcnc1-A421V/+ mice show more subtle
  abnormalities than layer II-IV PV-INs: AP frequency reduction is confined to the largest
  current injection magnitudes (***p<0.001 for genotype × current injection interaction),
  consistent with the higher relative expression of Kv3.2 vs Kv3.1 in deeper cortical layers.
claim-type: empirical
role: empirical
concepts:
  - layer V
  - PV interneurons
  - cell-type specificity
  - Kv3.1 vs Kv3.2
  - laminar differences
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-impairment-grades-with-kv31-dependence
confirms:
  - prediction-impairment-grades-with-kv31-dependence
  - hypothesis-pv-in-selective-vulnerability
dissociates-with:
  - pv-ins-impaired-maximal-firing

belongings:
  - relation: extends
    target: pv-ins-impaired-maximal-firing
  - relation: supports
    target: inhibitory-dysfunction-progresses-to-adulthood

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig4—figure supplement 2
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig4-figsupp2-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: whole-cell current-clamp
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Note: Figure supplement label in the paper uses fig4—figure supplement 2 for layer V
      PV-INs and fig4—figure supplement 3 for RTN. The RTN data appears in what the paper
      calls fig4—figure supplement 2 in the caption text but the label reads as the second
      supplement. Check actual figure numbering against G-Node deposit when verifying.
---

The layer-specificity finding rests on the prior literature: Chow et al. (1999) showed that
Kv3.1 comprises a lower proportion of Kv3 channels in layer V compared to layer II-IV
cortical cells. This claim operationalizes that background expectation as an observed
phenotypic gradient — a stronger test of the Kv3.1-loss-of-function mechanism than the
superficial layer result alone.
