---
uuid: 2d6bb516-6c05-4a2f-bb64-9e9142bbf326
slug: in-vivo-hypersynchronous-discharges-mutant-only
doi: ~
claim: >
  Paroxysmal hypersynchronous discharges in the neuropil calcium signal are observed in
  7 of 7 Kcnc1-A421V/+ mice examined in vivo (>P50) by two-photon GCaMP imaging, but
  never in WT mice (N=5), each discharge coinciding with a brief diffuse twitch of the
  facial musculature and bilateral limbs consistent with myoclonic seizures.
claim-type: empirical
role: empirical
concepts:
  - hypersynchronous discharge
  - two-photon calcium imaging
  - in vivo
  - neuropil
  - myoclonic seizures
  - KCNC1
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-network-hyperexcitability-in-vivo
confirms:
  - prediction-network-hyperexcitability-in-vivo
  - hypothesis-pv-dysfunction-drives-encephalopathy

belongings:
  - relation: supports
    target: a421v-mice-die-before-122d

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig8B, fig8C, fig8D
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig8-v1.tif/full/1500,/0/default.jpg
    scope: in-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: two-photon calcium imaging, AAV9-syn-jGCaMP8m, head-fixed somatosensory cortex
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      7/7 penetrance is a very strong effect. The paper distinguishes this neuropil-dominated
      signal from somatic signals using a separate cohort with soma-tagged GCaMP8m. That cohort
      did not show discharges, suggesting events are primarily axonal/dendritic (neuropil).
      Imaging performed at >P50 — important: this is after both behavioral testing and slice
      physiology age ranges, placing it closer to end-stage phenotype.
---
