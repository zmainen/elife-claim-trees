---
uuid: 3709a410-d465-4bb2-9386-e08e680a19a1
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
  bidirectional within every region.
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
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: fig2f, fig2h, fig2i, fig2j
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: per-neuron ZETA test for significant modulation; modulation index = 2 × (auROC - 0.5) for [0.3, 0.8] s post-stim vs baseline window
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~
---

Carries over from v1 unchanged. The empirical anchor for the brain-wide framing of the paper. Two distinct claims bundled: every region significantly modulated (ruling out localized projection-target hotspots as the only mechanism), and within most regions the sign of modulation is heterogeneous (ruling out a global signed brain-wide bias of the form fMRI studies have reported). The R1 reframing does not change this claim — additivity vs. multiplicativity is a property of how 5-HT modulates each neuron, not of which neurons are modulated.
