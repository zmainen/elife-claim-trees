---
uuid: 890a5223-4eb7-4dd0-a112-42e195398da1
slug: in-vivo-pv-minus-transient-frequency-increased
doi: ~
claim: >
  During quiet rest, PV– (excitatory) cells in Kcnc1-A421V/+ mice show significantly
  increased calcium transient frequency (mean 1.63 vs 1.17 transients/min in WT; n=1041
  vs 885 cells), while PV+ cell transient frequency is not significantly changed but PV+
  transient amplitude is reduced (mean 0.40 vs 0.48 dF/F0), consistent with decreased
  perisomatic inhibition in vivo.
claim-type: empirical
role: empirical
concepts:
  - in vivo calcium imaging
  - PV interneurons
  - excitatory neurons
  - calcium transients
  - network excitability
  - perisomatic inhibition
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-network-hyperexcitability-in-vivo
confirms:
  - prediction-network-hyperexcitability-in-vivo
  - hypothesis-pv-dysfunction-drives-encephalopathy

belongings:
  - relation: supports
    target: pv-ins-impaired-maximal-firing
  - relation: extends
    target: in-vivo-hypersynchronous-discharges-mutant-only

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig8G, fig8H, fig8I, fig8J
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig8-v1.tif/full/1500,/0/default.jpg
    scope: in-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: two-photon calcium imaging, soma-tagged GCaMP8m, S5E2-driven tdTomato for PV-ID
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Statistics by mixed-effects modeling. Confidence rated moderate because: (1) this
      cohort did not show hypersynchronous discharges (different from fig8B-D cohort),
      (2) the differences are modest in magnitude, and (3) running epochs show no differences
      (fig8—figure supplement 1C-F), indicating state-dependence. Effect is specific to
      quiet-rest epochs.
---

The state-dependence (effect during quiet rest, not during running) is an important boundary
condition. Running engages somatosensory and motor circuits in ways that may mask or compensate
for the interneuron deficit. The quiet-rest specificity is consistent with a tonic inhibition
impairment rather than a phasic or stimulus-locked one.
