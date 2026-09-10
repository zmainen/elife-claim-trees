---
paper-slug: meijer-2025-serotonin-orthogonal
title: "Serotonin modulates neural dynamics in a subspace orthogonal to the choice space"
authors:
  - Guido T. Meijer
  - Joana A. Catarino
  - Laura Freitas-Silva
  - Inês Laranjeira
  - International Brain Laboratory
  - Zachary F. Mainen
journal: bioRxiv
stage: preprint
doi: 10.1101/2025.08.01.668048
url: https://www.biorxiv.org/content/10.1101/2025.08.01.668048v1
github: https://github.com/guidomeijer/SerotoninStimulation
data: https://int-brain-lab.github.io/ONE/
added: 2026-04-19
badge: bronze
claim-count: 23
---

## Abstract

Serotonin (5-HT) is a central neuromodulator which is implicated in, amongst other functions, cognitive flexibility. 5-HT is released from the dorsal raphe nucleus (DRN) throughout nearly the entire forebrain. Little is known, however, about how serotonin affects downstream populations of neurons and how this modulation might support its cognitive functions. Here, we optogenetically stimulated serotonergic neurons in the DRN while recording large parts of the brain with Neuropixels during quiet wakefulness and performance of a perceptual decision-making task. During quiet wakefulness, 5-HT stimulation induced a rapid switch in internal state, as indicated by dilation of the pupil, suppression of hippocampal sharp wave ripples, and increased exploratory behaviors, such as whisking. To elucidate the brain-wide effect of serotonin release we performed acute Neuropixel recordings in seven target locations, a total of 7,478 neurons were recorded across 17 mice. We found that 5-HT stimulation significantly modulated neural activity in all the recorded brain regions, both during quiet wakefulness and task performance. During task performance, however, we observed no change in behavior when stimulating 5-HT. We found that the 5-HT modulation of high-dimensional neural dynamics is confined to a subspace which is orthogonal relative to the choice axis. These observations describe a possible mechanism for the induction of state-dependent stimulus representations, suggesting a neural basis for neuromodulatory effects on brain-wide circuits to flexible decision-making.

## Claims

### Hypotheses

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [hypothesis-state-switch-by-5ht](hypothesis-state-switch-by-5ht.md) | hypothesis | hypothesis | Phasic 5-HT release drives a rapid offline→online internal-state switch in the awake quiescent animal |
| [hypothesis-5ht-codes-surprise](hypothesis-5ht-codes-surprise.md) | hypothesis | hypothesis | 5-HT codes surprise — therefore stimulation should accelerate prior updating and alter choice behavior in the steering-wheel task |
| [hypothesis-orthogonal-neuromodulatory-subspace](hypothesis-orthogonal-neuromodulatory-subspace.md) | hypothesis | hypothesis | Strong neuronal modulation can leave behavior unaffected if neuromodulation is confined to a subspace orthogonal to the readout dimensions for ongoing computation |

### Predictions

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [prediction-5ht-shifts-psychometric](prediction-5ht-shifts-psychometric.md) | prediction | prediction | If 5-HT codes surprise / changes flexibility, stimulation should change psychometric slope, bias, lapse, RT, or choice-model weights |
| [prediction-5ht-accelerates-prior-update](prediction-5ht-accelerates-prior-update.md) | prediction | prediction | If 5-HT codes surprise, stimulation should speed updating of the choice bias after a prior block switch |
| [prediction-5ht-axis-orthogonal-to-choice](prediction-5ht-axis-orthogonal-to-choice.md) | prediction | prediction | If neuromodulation occupies an orthogonal subspace, the 5-HT effect axis in PCA should be near-orthogonal to the choice axis |
| [prediction-orthogonality-grows-toward-choice](prediction-orthogonality-grows-toward-choice.md) | prediction | prediction | If the orthogonal-subspace hypothesis is correct, orthogonality between 5-HT and choice axes should grow as the choice moment approaches and exceed shuffle controls |

### Empirical results

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [5ht-stim-dilates-pupil](5ht-stim-dilates-pupil.md) | fig1h | strong | Optogenetic 5-HT stimulation dilates the pupil ~2 s after stimulation offset in SERT-cre but not WT mice |
| [5ht-stim-suppresses-sharp-wave-ripples](5ht-stim-suppresses-sharp-wave-ripples.md) | fig1l | strong | 5-HT stimulation significantly reduces hippocampal sharp wave ripple frequency, consistent with an offline→online shift |
| [5ht-stim-increases-exploratory-behaviors](5ht-stim-increases-exploratory-behaviors.md) | fig1i, fig1j | strong | 5-HT stimulation increases whisking and sniffing at short latency in SERT-cre mice |
| [5ht-modulates-all-recorded-regions-bidirectionally](5ht-modulates-all-recorded-regions-bidirectionally.md) | fig2f, fig2h, fig2i, fig2j | strong | 5-HT stimulation significantly modulates 10–60% of neurons in every recorded brain region, with bidirectional sign — suppression and excitation coexist within most regions |
| [5ht-modulation-fraction-tracks-chr2-expression](5ht-modulation-fraction-tracks-chr2-expression.md) | fig2g | strong | The fraction of significantly 5-HT-modulated neurons per animal correlates with histologically measured ChR2 expression (r=0.77, p=0.005) |
| [inhibition-fast-excitation-slow](inhibition-fast-excitation-slow.md) | fig2k, fig2l | moderate | Across regions, mean modulation onset latency correlates with modulation sign — inhibited regions respond at short latencies, excited regions at longer latencies (r=0.61, p=0.028) |
| [5ht-stim-leaves-decision-behavior-intact](5ht-stim-leaves-decision-behavior-intact.md) | fig3c, fig3d, fig3e, fig3g | strong | 5-HT stimulation produces no detectable change in psychometric slope, bias, lapse, percent-correct, reaction time, prior updating speed, or probabilistic choice-model weights in the steering-wheel task |
| [5ht-modulation-weaker-during-task](5ht-modulation-weaker-during-task.md) | fig4d | moderate | Significantly fewer neurons are 5-HT-modulated during task performance than during quiet wakefulness (p=0.012, paired t-test across regions) |
| [5ht-axis-orthogonal-to-choice-axis](5ht-axis-orthogonal-to-choice-axis.md) | fig5g, fig5h | strong | The 5-HT effect axis in PCA space is significantly more orthogonal to the choice axis than expected from a shuffled null distribution, with orthogonality growing toward the choice moment |
| [orthogonality-significant-in-mpfc-vis-m2](orthogonality-significant-in-mpfc-vis-m2.md) | fig5i | moderate | When computed per region at the last time point before the choice, orthogonality is significant in medial prefrontal cortex, visual cortex, and supplementary motor area |

### Control / null claims

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [wt-controls-rule-out-light-artifact](wt-controls-rule-out-light-artifact.md) | fig1c, fig2f | strong | Wild-type controls (n=6) show baseline DRN/control fluorescence and chance-level (~5%) modulation — ruling out light, heat, or non-specific viral effects |
| [narrow-spike-interneurons-not-driver-of-rapid-inhibition](narrow-spike-interneurons-not-driver-of-rapid-inhibition.md) | Supp fig3 | moderate | Narrow-spiking putative fast-spiking interneurons are not preferentially recruited by 5-HT and have modulation indices indistinguishable from wide-spiking neurons — ruling out a fast-spiking-interneuron-mediated mechanism for the rapid inhibition |
| [cortical-layers-show-no-differential-modulation](cortical-layers-show-no-differential-modulation.md) | Supp fig4 | moderate | When cortical recordings are split by layer, neither the fraction modulated, the modulation sign, nor the onset latency differs across layers |

### Scope / methodological claims

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [optogenetic-activation-not-physiological-pattern](optogenetic-activation-not-physiological-pattern.md) | scope | moderate | SERT-Cre + ChR2 optogenetic stimulation drives DRN serotonergic neurons more broadly and uniformly than endogenous release — light intensity falls off from the fiber tip and ChR2 shows frequency-dependent adaptation; physiological 5-HT release engages anatomically and functionally distinct subpopulations |
| [seven-target-trajectories-13-regions-7478-neurons](seven-target-trajectories-13-regions-7478-neurons.md) | fig2c, fig2d | strong | The brain-wide claims rest on 7,478 neurons recorded across 13 brain regions in 86 dual-Neuropixel insertions across 57 sessions in 17 mice (11 SERT-Cre, 6 WT), via the IBL spike-sorting pipeline |
| [manifold-from-pooled-super-session](manifold-from-pooled-super-session.md) | methods | moderate | The manifold and orthogonality analyses are computed on a pooled "super-session" of trial-averaged PETHs concatenated across all neurons, sessions, and mice — not on individual animals; null distributions are generated by within-prior-block shuffles and pseudo-stimulation-blocks to preserve temporal autocorrelation structure |

## Dependency graph

```
hypothesis-state-switch-by-5ht
  └─ supported by ← 5ht-stim-dilates-pupil
  └─ supported by ← 5ht-stim-suppresses-sharp-wave-ripples
  └─ supported by ← 5ht-stim-increases-exploratory-behaviors

hypothesis-5ht-codes-surprise
  └─ entails → prediction-5ht-shifts-psychometric
  └─ entails → prediction-5ht-accelerates-prior-update
  └─ refuted by ← 5ht-stim-leaves-decision-behavior-intact

hypothesis-orthogonal-neuromodulatory-subspace
  └─ entails → prediction-5ht-axis-orthogonal-to-choice
  └─ entails → prediction-orthogonality-grows-toward-choice
  └─ supported by ← 5ht-axis-orthogonal-to-choice-axis
  └─ supported by ← orthogonality-significant-in-mpfc-vis-m2
  └─ contextually requires ← 5ht-modulates-all-recorded-regions-bidirectionally
                          ← 5ht-stim-leaves-decision-behavior-intact
                          (orthogonality is the proposed reconciliation of these two)

5ht-modulates-all-recorded-regions-bidirectionally
  └─ requires → wt-controls-rule-out-light-artifact
  └─ requires → 5ht-modulation-fraction-tracks-chr2-expression
  └─ requires → seven-target-trajectories-13-regions-7478-neurons
  └─ requires → optogenetic-activation-not-physiological-pattern (scope)

inhibition-fast-excitation-slow
  └─ rules out (with) → narrow-spike-interneurons-not-driver-of-rapid-inhibition
  └─ rules out (with) → cortical-layers-show-no-differential-modulation

5ht-axis-orthogonal-to-choice-axis
  └─ requires → manifold-from-pooled-super-session
  └─ requires → 5ht-modulation-weaker-during-task (scope: applies during task)
  └─ supports → orthogonality-significant-in-mpfc-vis-m2
```

## Reproduction status

Verification status: not yet attempted (added 2026-04-19, agent: mainen-z, ingest-only). Code is at https://github.com/guidomeijer/SerotoninStimulation, data via IBL ONE protocol. Expected reproduction path is the standard IBL pipeline plus the manifold-analysis code that follows reference 28 (Lebedev et al. / IBL prior code).

| Status | Count | Claims |
|:-------|:------|:-------|
| unverified | 23 | all (no reproduction attempted at ingest) |

**Notable structural feature:** This paper is unusual in the corpus in containing an explicitly *rejected* hypothesis (`hypothesis-5ht-codes-surprise`). The dependency graph models the rejection: the surprise hypothesis entails behavioral predictions that the empirical observation `5ht-stim-leaves-decision-behavior-intact` refutes. The orthogonal-subspace hypothesis is then introduced as the post-hoc reconciliation of the two findings the paper has now placed in tension — strong neural modulation and intact behavior. This is the structural shape worth preserving.
