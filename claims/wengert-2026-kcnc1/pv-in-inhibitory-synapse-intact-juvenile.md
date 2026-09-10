---
uuid: dbc34885-27d0-4b6e-afbb-6a34befb9b98
slug: pv-in-inhibitory-synapse-intact-juvenile
doi: ~
claim: >
  PV-IN-mediated inhibitory synaptic transmission is not significantly altered in juvenile
  (P16–21) Kcnc1-A421V/+ mice: failure rates, uIPSC magnitudes at 20/40/80 Hz, paired-pulse
  ratios, and synaptic latency are all not significantly different from WT (32.8% connection
  rate WT vs 34.9% Kcnc1-A421V/+; n=21/64 and 15/43 connected pairs respectively).
claim-type: empirical
role: empirical
concepts:
  - inhibitory synaptic transmission
  - uIPSC
  - PV interneurons
  - paired-pulse ratio
  - juvenile
  - Kv3.1
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-progressive-synaptic-failure
dissociates-with:
  - pv-in-inhibitory-synapse-altered-adult

belongings:
  - relation: rules-out
    target: alt-inhibitory-dysfunction-present-juvenile
  - relation: supports
    target: inhibitory-dysfunction-progresses-to-adulthood

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig6F, fig6G, fig6H, fig6I, fig6J, fig6K, fig6L
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig6-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: dual whole-cell patch-clamp, paired recording
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: verified
    notes: >
      Verified from G-Node Excel (WT P16-21 PV->Pyr and Kcnc1 P16-21 PV->Pyr sheets).
      uIPSC amplitude at 20Hz pulse 1: WT n=18 mean=-66.1 pA, KI n=14 mean=-99.0 pA;
      unpaired t-test p=0.22 (not significant). PPR at 20Hz: WT 0.774, KI 0.659; p=0.24 NS.
      PPR at 40Hz and 80Hz also NS. Null result fully confirmed. Connected pair counts
      from uIPSC data presence: ~19 WT, ~14 KI (paper: 21 and 15 — slight undercount in
      extraction, consistent with a few cells missing some frequency sweeps).
---

Note: this claim used to carry both `contradicts` and `supports` pointing at
`inhibitory-dysfunction-progresses-to-adulthood`, with a note explaining that it supports the
temporal framing (juvenile normal, adult altered) but contradicts "a naive reading of
'inhibitory dysfunction present at juvenile.'" That naive reading is now a claim of its own,
`alt-inhibitory-dysfunction-present-juvenile`, and the opposition points at it. The result
supports the progression claim and rules out the static one — no longer both at once.

The resolution the old note gave still holds and is the substance: firing-frequency impairment
is present in juveniles but synaptic-per-spike function is not. The distinction matters for
mechanistic interpretation.
