---
uuid: e3041ac0-b702-47fc-a127-dbe692110449
slug: 5ht-stim-suppresses-sharp-wave-ripples
doi: ~
claim: >
  Optogenetic activation of dorsal-raphe serotonergic neurons during quiet wakefulness
  significantly reduces the frequency of hippocampal sharp-wave ripples detected in CA1
  local-field potential, consistent with a transition out of the offline / quiescent state
  in which ripples preferentially occur.
displayClaim: >
  DRN 5-HT activation suppresses CA1 sharp-wave ripples — a hallmark of moving the
  hippocampus out of its offline / quiescent regime.
claim-type: empirical
role: empirical
concepts:
  - sharp-wave ripples
  - hippocampus
  - CA1
  - local-field potential
  - offline state
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
    panel: fig1k, fig1l
    analysis: figure-generation scripts in https://github.com/guidomeijer/SerotoninStimulation
    dataset: IBL ONE protocol
    dataset-doi: ~
    method: CA1 LFP ripple detection, event-aligned to passive 5-HT stimulation
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-04-19
    status: unverified
    notes: ~

discrepancy:
  type: methodological-gap
  explanation: >
    Repo CSV (ripple_freq.csv) contains raw frequency values without baseline subtraction or SERT-vs-WT contrast. Paper figure plots delta ripple frequency after subtracting baseline and comparing SERT to WT, showing net suppression. The preprocessing pipeline is not reproduced from the deposited CSV alone.
---

The ripple-suppression result is the cleanest single-modality evidence for the state-switch hypothesis because ripples have a tight, well-characterized state association: they occur during quiet wakefulness and slow-wave sleep, and are suppressed by arousing inputs. Demonstrating that 5-HT stimulation alone is sufficient to suppress them positions DRN serotonin as a candidate driver of the SWR-suppression circuit, consistent with the broader literature on neuromodulator gating of hippocampal offline replay. Note that the hippocampus has weak direct serotonergic input from DRN; the discussion attributes the rapid hippocampal effect to indirect routing through median raphe.
