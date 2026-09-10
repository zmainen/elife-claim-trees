---
uuid: c79c1fff-fe7a-4580-8474-a2295d879da1
slug: 5ht-stim-suppresses-sharp-wave-ripples
doi: ~
claim: >
  Optogenetic 5-HT stimulation during quiet wakefulness produces a significant reduction
  in hippocampal sharp wave ripple frequency. Ripples are detected on the CA1 pyramidal-layer
  channel (selected by maximum AP-band RMS) of dorsal-hippocampus Neuropixel insertions,
  using a 150–250 Hz Butterworth bandpass and a 6-SD threshold with 100-ms minimum
  inter-event interval.
displayClaim: >
  5-HT stimulation reduces hippocampal sharp wave ripple frequency, consistent with an
  offline-to-online state shift.
claim-type: empirical
role: empirical
concepts:
  - sharp wave ripples
  - CA1
  - quiet wakefulness
  - state transition
priority: 2026-04-20
epistemic: strong

supports:
  - hypothesis-state-switch-by-5ht

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig1l
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: CA1 LFP filtered 150–250 Hz; threshold-crossing detection at 6 SD with 100 ms minimum interval; ripple frequency conditioned on stimulation onset
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. The interpretive force comes from the well-established association of sharp wave ripples with offline/quiescent states (refs. 21–23 in the paper) — their suppression is one of the converging readouts of the proposed offline-to-online state switch.
