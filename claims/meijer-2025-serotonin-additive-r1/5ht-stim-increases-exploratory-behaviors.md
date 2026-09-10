---
uuid: 5df1fd28-8409-47d8-a2a4-b10874716f7d
slug: 5ht-stim-increases-exploratory-behaviors
doi: ~
claim: >
  Optogenetic 5-HT stimulation during quiet wakefulness produces significant short-latency
  increases in two video-extracted exploratory behaviors: whisking (movement energy in an
  ROI around the whisker pad) and sniffing (frame-to-frame displacement of a tracked
  nose-tip DLC point). The increases are present in SERT-Cre mice and not in WT controls.
displayClaim: >
  5-HT stimulation increases whisking and sniffing at short latency in SERT-Cre but not
  WT mice.
claim-type: empirical
role: empirical
concepts:
  - whisking
  - sniffing
  - exploratory behavior
  - DeepLabCut
priority: 2026-04-20
epistemic: strong

supports:
  - hypothesis-state-switch-by-5ht

belongings:
  - relation: requires
    target: wt-controls-rule-out-light-artifact

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig1i, fig1j
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: ROI movement-energy quantification for whisking; DLC tracking + frame-to-frame displacement for sniffing; conditioning on stimulation onset; independent-samples t-test SERT vs WT
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. Together with pupil dilation and SWR suppression, the third converging readout of the offline-to-online state-switch interpretation. The latency is short (within hundreds of ms of stimulation onset), suggesting the state switch is fast — relevant for the trial-timescale arguments in the task-engagement section.
