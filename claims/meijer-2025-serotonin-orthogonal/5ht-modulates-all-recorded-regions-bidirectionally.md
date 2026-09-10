---
uuid: 6979e5c6-acb6-4083-ba5a-5ad25845f8a0
slug: 5ht-modulates-all-recorded-regions-bidirectionally
doi: ~
claim: >
  Optogenetic activation of dorsal-raphe serotonergic neurons during quiet wakefulness
  significantly modulates 10–60% of single neurons in every one of the 13 recorded brain
  regions (all exceeding the 5% chance level), with bidirectional sign — every region
  contains both 5-HT-excited and 5-HT-suppressed neurons, and no region shows pure
  brain-wide excitation or pure brain-wide suppression.
displayClaim: >
  5-HT stimulation modulates 10–60% of neurons in every recorded region; modulation is
  bidirectional within every region (no pure brain-wide excitation or inhibition).
claim-type: empirical
role: empirical
concepts:
  - bidirectional modulation
  - brain-wide
  - single-neuron firing rate
  - ZETA test
priority: 2026-04-20
epistemic: strong

belongings:
  - relation: requires
    target: wt-controls-rule-out-light-artifact
  - relation: requires
    target: 5ht-modulation-fraction-tracks-chr2-expression
  - relation: requires
    target: seven-target-trajectories-13-regions-7478-neurons
  - relation: requires
    target: optogenetic-activation-not-physiological-pattern

assertions:
  - paper-slug: meijer-2025-serotonin-orthogonal
    doi: 10.1101/2025.08.01.668048
    panel: fig2f, fig2h, fig2i, fig2j
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-neuron ZETA test for significant modulation; modulation index = ratio of post-stimulus to baseline firing rate
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-20
    status: unverified
    notes: ~

discrepancy:
  type: methodological-gap
  explanation: >
    Repo CSV uses 41 fine-grained anatomical regions; paper reports ~13 broader target areas. At fine granularity, one region shows 3% modulation (below 5% chance). Aggregating to paper-level targets would merge low-count regions upward. Direction and bidirectionality confirmed.
---

This is the empirical anchor for the paper's brain-wide framing. Two distinct claims are bundled in this one entry: (1) every recorded region contains a meaningful fraction of 5-HT-modulated neurons, exceeding chance — meaning 5-HT effects are truly distributed, not localized to projection-target hotspots; (2) within most regions the sign of modulation is heterogeneous, with excited and suppressed neurons coexisting — meaning regional means can be misleading and the brain-wide picture is one of bidirectional modulation rather than a single signed brain-wide bias. The paper takes care to make the second point with the per-neuron modulation-index plot in Fig. 2j, which shows that even the regions with mean suppression contain substantial numbers of excited neurons, and vice versa. The paper explicitly contrasts this picture with prior fMRI work that reported brain-wide inhibition or brain-wide excitation as a global effect.
