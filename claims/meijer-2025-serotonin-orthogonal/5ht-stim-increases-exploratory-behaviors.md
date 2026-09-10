---
uuid: 2ce5650a-94bd-4d14-91cd-4fba82bcc7b0
slug: 5ht-stim-increases-exploratory-behaviors
doi: ~
claim: >
  Optogenetic activation of dorsal-raphe serotonergic neurons during quiet wakefulness
  increases exploratory motor behaviors at short latency in SERT-Cre mice — specifically,
  whisking (movement energy in a region of interest around the whisker pad) and sniffing
  (frame-to-frame movement of a tracked DLC point on the nose tip) both rise relative to
  WT controls within the seconds following stimulation onset.
displayClaim: >
  DRN 5-HT activation rapidly increases whisking and sniffing — exploratory motor behaviors
  characteristic of an alert / online state.
claim-type: empirical
role: empirical
concepts:
  - whisking
  - sniffing
  - exploratory behavior
  - DLC tracking
priority: 2026-04-19
epistemic: strong

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
    panel: fig1i, fig1j
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: video-derived motion energy and DLC point tracking, head-fixed
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Whisking and sniffing are two of the most robust mouse behavioral correlates of the alert / exploratory state. Their concurrent increase (alongside pupil dilation and ripple suppression) is what licenses the "rapid offline→online switch" interpretation rather than a more circumscribed reading of 5-HT as an arousal-only or autonomic-only modulator. The short latency relative to pupil dilation (which takes ~2 s) suggests these behaviors are downstream of a faster motor-circuit effect, while pupil reflects a slower autonomic readout.
