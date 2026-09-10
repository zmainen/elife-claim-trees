---
uuid: f61028a7-74b3-416f-9df2-cdd8b91d0063
slug: 5ht-stim-dilates-pupil
doi: ~
claim: >
  A 1-second optogenetic activation of dorsal-raphe serotonergic neurons in SERT-Cre mice
  produces a significant increase in pupil size relative to baseline, with the divergence
  from wild-type controls becoming significant approximately 2 seconds after stimulation
  offset.
displayClaim: >
  1 s of DRN 5-HT optogenetic activation dilates the pupil in SERT-Cre mice, significantly
  diverging from WT controls ~2 s after stimulation offset.
claim-type: empirical
role: empirical
concepts:
  - pupil dilation
  - arousal
  - DLC video tracking
  - SERT-Cre
priority: 2026-04-19
epistemic: strong

tests: []
supports:
  - hypothesis-state-switch-by-5ht

belongings:
  - relation: requires
    target: wt-controls-rule-out-light-artifact
  - relation: supports
    target: hypothesis-state-switch-by-5ht

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig1h
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: head-fixed video pupillometry, DLC tracking, SERT-Cre vs WT comparison
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

The pupil dilation result replicates a previously reported finding (cited as ref. 20 in the paper). It is one of three converging readouts of the offline→online state switch (with ripple suppression and exploratory-behavior increase). The ~2 s post-offset latency is consistent with the slow effective timecourse of 5-HT signalling on autonomic arousal circuits, distinct from the rapid (tens of ms) onset of direct neural modulation reported elsewhere in the paper.
