---
paper-slug: meijer-2025-serotonin-additive-r1
title: "Serotonin drives choice-independent reconfiguration of distributed neural activity"
authors:
  - Guido T. Meijer
  - Joana A. Catarino
  - Laura Freitas-Silva
  - Inês Laranjeira
  - International Brain Laboratory
  - Zachary F. Mainen
journal: Nature Neuroscience
stage: revision
doi: ~
url: ~
github: https://github.com/guidomeijer/SerotoninStimulation
data: https://int-brain-lab.github.io/ONE/
added: 2026-04-19
badge: bronze
claim-count: 41
prior-version: meijer-2025-serotonin-orthogonal
---

## Abstract

Serotonin (5-HT) is a central neuromodulator which is implicated in, amongst other functions, cognitive flexibility. 5-HT is released from the dorsal raphe nucleus (DRN) throughout nearly the entire forebrain. Little is known, however, about how serotonin affects downstream populations of neurons and how this modulation might support its cognitive functions. Here, we optogenetically stimulated serotonergic neurons in the DRN while recording large parts of the brain with Neuropixels during quiet wakefulness and performance of a perceptual decision-making task. During quiet wakefulness, 5-HT stimulation induced a rapid switch in internal state, as indicated by dilation of the pupil, suppression of hippocampal sharp wave ripples, and increased exploratory behaviors, such as whisking. To elucidate the brain-wide effect of optogenetic activation of serotonergic neurons on single neuron spiking activity, we performed acute Neuropixels recordings across seven target trajectories, recording 7,478 neurons across 17 mice. We found that 5-HT stimulation significantly modulated neural activity in all recorded brain regions, both during quiet wakefulness and task performance. During task performance, however, activation of serotonergic neurons had no effect on behavior. Using a generalized linear model, we show that serotonergic modulation combines additively with choice-related activity, as opposed to a multiplicative gain modulation; the choice-by-stimulation interaction was near zero across regions and animals. As a geometric consequence of this additivity, 5-HT modulation was confined to a subspace orthogonal to the choice axis. These findings suggest that serotonin can reconfigure distributed neural dynamics without interfering with ongoing task computations.

## Revision history

This is the R1 (revised) version of `meijer-2025-serotonin-orthogonal` (bioRxiv preprint 10.1101/2025.08.01.668048, August 2025) submitted to Nature Neuroscience. This claim graph is built from the **authoritative R1 manuscript dated 2026-04-16** (`meijer-r1-actual-2026-04-16.docx` in the haak archive at `home/orgs/mainen-lab/projects/serotonin/5HT-neuropix-guido/revisions/`), not from earlier revision-plan documents.

The R1 carries the same dataset and the same primary geometric analyses as v1 but reframes the central organizing claim and adds substantial new analyses. In v1, *orthogonality* of the 5-HT and choice subspaces was the main finding, introduced post-hoc to reconcile widespread neural modulation with intact behavior. In R1, *additivity* — operationalized as a near-zero choice-by-stimulation interaction in a per-neuron GLM — is the central finding, and orthogonality is presented as its geometric consequence. The reframing carries three substantive structural shifts:

1. **Additivity is now a directly tested empirical claim** (`near-zero-choice-by-stim-interaction`, Fig. 6c) rather than an implicit consequence of the manifold geometry. The GLM with separate choice, stimulation, and choice×stimulation predictors and the t-test of the interaction term against zero is the new analysis.
2. **The result rules out multiplicative gain control** (`rules-out-multiplicative-gain-control`) — the default computational framework for neuromodulators since Servan-Schreiber et al. (1990). This is a positive elimination, not a null result; the GLM predictions of additive vs. multiplicative modulation diverge concretely on the interaction term.
3. **Orthogonality is demoted to a derivation** (`orthogonality-derived-from-additivity`). The graph encodes this with `derived-from: [hypothesis-additive-modulation]` on the orthogonality hypothesis. The orthogonality measurements (Fig. 6d–f) are still load-bearing empirical confirmations, but they no longer carry the conceptual weight on their own.

Beyond the additivity reframe, R1 adds a substantial new analysis (entirely new in R1, no v1 equivalent): **Figure 3** presents a receptor-expression and DRN-projection-density GLM that predicts regional modulation strength, directionality, and latency from public Allen Brain Atlas data on serotonergic receptor expression and DRN projections. This was added in direct response to Reviewer 2 (comment 1.2.a, b). The four claims it generates — `receptor-expression-predicts-modulation-strength`, `receptor-expression-predicts-modulation-direction`, `5ht1a-predicts-fast-modulation-latency`, and `drn-projection-density-not-significant-predictor` — give the brain-wide bidirectional-modulation finding a partial mechanistic substrate. Inserting this new figure shifts subsequent figure numbers: v1's Fig. 3 (behavior) becomes R1's Fig. 4; v1's Fig. 4 (task neural) becomes R1's Fig. 5; v1's Fig. 5 (orthogonality manifold) becomes R1's Fig. 6 (now combined with the new GLM additivity panels in subpanels 6a–c).

R1 also adds a quantitative comparison with the Hamada et al. (2024) opto-fMRI dataset as Supplementary Figure 3, in response to Reviewer 2 comment 1.1. This becomes the claim `fmri-bold-correlates-but-misses-suppressed-regions`: BOLD beta values correlate with single-unit modulation strength at the region level, but fMRI sees only activation while ephys reveals widespread bidirectional modulation. The interpretation is that serotonin's vasoactive effects on neurovascular coupling (Padawer-Curry et al., 2025) confound BOLD-based readout of neural activity.

The R1 also adds richer literature interpretation in the introduction and discussion: the gain-control framework as the dominant computational hypothesis (Servan-Schreiber 1990, Salinas & Thier 2000), its serotonin-specific demonstration in visual cortex via 5-HT2A (Azimi 2020, Barzan 2024), and the single-region precedent of additive modulation in piriform cortex (Lottem 2016). These appear as `interprets:` claims in the graph. The optogenetic-scope discussion is extensively rewritten with corrected citations (Cohen 2015, Li 2016, Matias 2017, Paquelet 2022, Dugué 2014, Kauvar 2025); the corrected scope claim replaces v1's "synchronized burst-like firing of 50–60% of neurons" with "correlated ensembles comprising up to 59% (sucrose) and 45% (footshock) of serotonergic neurons" and acknowledges that optogenetic drive itself is not spatially uniform (light fall-off, ChR2 adaptation).

The latency analysis (Fig. 2k–m) was rerun under the new latenZy method (Haak & Heimel 2025, ref. 27), in response to Reviewer 3 comment 3. Critically, the v1 finding of "fast inhibition / slow excitation" could not be replicated — that figure panel was removed. What R1 reports instead is that the absolute modulation index correlates negatively with latency: stronger modulation (in either direction) is associated with shorter latency. This is captured as `latency-correlates-with-absolute-modulation`, which replaces the v1 claim `inhibition-fast-excitation-slow`. R1 also reports a new finding from the latenZy analysis: putative fast-spiking interneurons are modulated at *longer* latencies than regular-spiking neurons (Supp. Fig. 4e), strengthening the argument that they do not drive the fast inhibition.

The surprise hypothesis (`hypothesis-5ht-codes-surprise`) and its behavioral refutation (`5ht-stim-leaves-decision-behavior-intact`) carry over from v1 unchanged. All Fig. 1 (state switch) and Fig. 2 (brain-wide modulation) empirical claims and the control claims carry over with text identical to v1 modulo the figure-renumbering and the latency revision. The R1 manuscript also presents an additional reconciliation hypothesis, `reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control`, that proposes a receptor-dependent picture in which 5-HT2A-mediated gain control of evoked responses coexists with a 5-HT1A-mediated stimulus-independent baseline suppression, and the brain-wide additive mode reflects dominance of the latter.

## Claims

### Hypotheses

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [hypothesis-additive-modulation](hypothesis-additive-modulation.md) | hypothesis | hypothesis | 5-HT modulates spiking activity additively rather than multiplicatively, shifting baseline firing without scaling stimulus-driven gain |
| [hypothesis-orthogonal-neuromodulatory-subspace](hypothesis-orthogonal-neuromodulatory-subspace.md) | hypothesis | hypothesis | Geometric reframing of additivity in subspace terms — derived from the additivity hypothesis under a 2×2 factorial choice×stim design |
| [hypothesis-5ht-codes-surprise](hypothesis-5ht-codes-surprise.md) | hypothesis | hypothesis | Carried over from v1; predicts behavioral effects, refuted in the task |
| [hypothesis-state-switch-by-5ht](hypothesis-state-switch-by-5ht.md) | hypothesis | hypothesis | Phasic 5-HT release drives a rapid offline→online internal-state switch in the awake quiescent animal |
| [reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control](reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control.md) | discussion | hypothesis | The brain-wide additive mode reflects 5-HT1A-mediated stimulus-independent baseline suppression dominating over the 5-HT2A-mediated evoked-response gain modulation reported in visual cortex |

### Predictions

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [prediction-near-zero-choice-stim-interaction](prediction-near-zero-choice-stim-interaction.md) | prediction | prediction | If 5-HT modulation is additive, a per-neuron GLM with choice, stimulation, and choice×stim predictors should yield a near-zero interaction term |
| [prediction-multiplicative-gain-yields-significant-interaction](prediction-multiplicative-gain-yields-significant-interaction.md) | prediction | prediction | If 5-HT acted via multiplicative gain modulation, the choice×stimulation interaction term should be significantly different from zero |
| [prediction-5ht-axis-orthogonal-to-choice](prediction-5ht-axis-orthogonal-to-choice.md) | prediction | prediction | Derived consequence of additivity in 2×2 factorial design — the 5-HT effect axis in PCA should be near-orthogonal to the choice axis |
| [prediction-orthogonality-grows-toward-choice](prediction-orthogonality-grows-toward-choice.md) | prediction | prediction | Orthogonality between 5-HT and choice axes should grow as the choice moment approaches and exceed shuffle controls |
| [prediction-5ht-shifts-psychometric](prediction-5ht-shifts-psychometric.md) | prediction | prediction | If 5-HT codes surprise, stimulation should change psychometric slope, bias, lapse, RT, or choice-model weights |
| [prediction-5ht-accelerates-prior-update](prediction-5ht-accelerates-prior-update.md) | prediction | prediction | If 5-HT codes surprise, stimulation should speed updating of choice bias after a prior block switch |

### Empirical results

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [near-zero-choice-by-stim-interaction](near-zero-choice-by-stim-interaction.md) | fig6c | strong | Per-neuron GLM choice×5-HT-stimulation interaction coefficient is near zero (mean ± SEM across animals: -0.05 ± 0.06; t(9) = -0.92, p = 0.38) |
| [glm-significant-choice-and-5ht-coefficients](glm-significant-choice-and-5ht-coefficients.md) | fig6c | strong | Both choice and 5-HT main-effect predictors have significant non-zero coefficients in the per-neuron GLM, establishing that each independently modulates spiking |
| [5ht-stim-dilates-pupil](5ht-stim-dilates-pupil.md) | fig1h | strong | 5-HT stimulation dilates the pupil ~2 s after stimulation offset in SERT-cre but not WT mice |
| [5ht-stim-suppresses-sharp-wave-ripples](5ht-stim-suppresses-sharp-wave-ripples.md) | fig1l | strong | 5-HT stimulation reduces hippocampal sharp wave ripple frequency |
| [5ht-stim-increases-exploratory-behaviors](5ht-stim-increases-exploratory-behaviors.md) | fig1i, fig1j | strong | 5-HT stimulation increases whisking and sniffing at short latency in SERT-cre mice |
| [5ht-modulates-all-recorded-regions-bidirectionally](5ht-modulates-all-recorded-regions-bidirectionally.md) | fig2f, fig2h, fig2i, fig2j | strong | 5-HT stimulation significantly modulates 10–60% of neurons in every recorded region, with bidirectional sign |
| [5ht-modulation-fraction-tracks-chr2-expression](5ht-modulation-fraction-tracks-chr2-expression.md) | fig2g | strong | Fraction of 5-HT-modulated neurons per animal correlates with histologically measured ChR2 expression (r=0.77, p=0.005) |
| [latency-correlates-with-absolute-modulation](latency-correlates-with-absolute-modulation.md) | fig2k, fig2l, fig2m | moderate | Stronger 5-HT modulation (in either direction) is associated with shorter onset latency; latencies range from ~16 ms (amygdala) to long offset responses |
| [fmri-bold-correlates-but-misses-suppressed-regions](fmri-bold-correlates-but-misses-suppressed-regions.md) | Supp fig3 | moderate | NEW IN R1. Region-level Hamada (2024) BOLD beta correlates with our single-unit modulation strength, but fMRI sees only activation while ephys reveals widespread bidirectional modulation |
| [receptor-expression-predicts-modulation-strength](receptor-expression-predicts-modulation-strength.md) | fig3a, fig3b | strong | NEW IN R1 (Fig. 3 added in response to reviewer). Per-region GLM (receptor expression + DRN projection density) explains 50% of variance in modulation strength; 5-HT1 expression is the leading positive predictor |
| [receptor-expression-predicts-modulation-direction](receptor-expression-predicts-modulation-direction.md) | fig3c | strong | NEW IN R1. GLM on signed modulation index: 5-HT2 receptors positively predict (excitatory Gq), 5-HT1a receptors negatively predict (inhibitory Gi/o); pseudo R²=0.62 |
| [5ht1a-predicts-fast-modulation-latency](5ht1a-predicts-fast-modulation-latency.md) | fig3d | moderate | NEW IN R1. 5-HT1a receptor expression is the only significant negative predictor of modulation latency; ionotropic 5-HT3 and DRN projection density are not significant |
| [drn-projection-density-not-significant-predictor](drn-projection-density-not-significant-predictor.md) | fig3b | moderate | NEW IN R1, negative finding. DRN projection density does not significantly predict modulation strength as a positive coefficient — most modulation is likely indirect/polysynaptic |
| [5ht-stim-leaves-decision-behavior-intact](5ht-stim-leaves-decision-behavior-intact.md) | fig4c, fig4d, fig4e, fig4g | strong | 5-HT stimulation produces no detectable change in psychometric, RT, prior-update, or choice-model behavior |
| [5ht-modulation-weaker-during-task](5ht-modulation-weaker-during-task.md) | fig5d | moderate | Significantly fewer neurons are 5-HT-modulated during task than during quiet wakefulness (p=0.012, paired t-test) |
| [5ht-axis-orthogonal-to-choice-axis](5ht-axis-orthogonal-to-choice-axis.md) | fig6d, fig6e | strong | The 5-HT effect axis in PCA is significantly more orthogonal to the choice axis than shuffle null, with orthogonality growing toward choice |
| [orthogonality-significant-in-mpfc-vis-m2](orthogonality-significant-in-mpfc-vis-m2.md) | fig6f | moderate | Per-region orthogonality is significant in mPFC, visual cortex, and supplementary motor area at the last pre-choice time bin |

### Synthesis / interpretation

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [rules-out-multiplicative-gain-control](rules-out-multiplicative-gain-control.md) | results+discussion | strong | The near-zero choice×stim interaction is inconsistent with multiplicative gain modulation as the brain-wide mode of 5-HT action; the dominant default framework is eliminated |
| [orthogonality-derived-from-additivity](orthogonality-derived-from-additivity.md) | results+discussion | strong | In a 2×2 factorial design (choice × stimulation), additive modulation mathematically entails that the stimulation-effect direction be orthogonal to the choice direction in PCA space; orthogonality is therefore a geometric consequence, not an independent finding |

### Literature interpretation

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [interprets-gain-control-default-framework](interprets-gain-control-default-framework.md) | introduction+discussion | moderate | The dominant computational framework treats neuromodulators as multiplicative gain controllers (Servan-Schreiber 1990, Salinas & Thier 2000) |
| [interprets-5ht2a-gain-control-visual-cortex](interprets-5ht2a-gain-control-visual-cortex.md) | introduction+discussion | moderate | 5-HT2A-mediated multiplicative gain control of sensory responses has been demonstrated in visual cortex (Azimi 2020, Barzan 2024) |
| [interprets-lottem-2016-additive-piriform](interprets-lottem-2016-additive-piriform.md) | introduction+discussion | moderate | DRN serotonin stimulation in piriform cortex suppressed spontaneous firing while leaving odor-evoked responses intact, with no stimulation-by-stimulus interaction (Lottem 2016) — the single-region precedent for additive modulation |
| [interprets-paquelet-correlated-ensembles](interprets-paquelet-correlated-ensembles.md) | discussion | moderate | Sucrose consumption and footshock activate correlated DRN serotonergic ensembles comprising up to 59% and 45% of neurons respectively, with mixed selectivity (Paquelet 2022) — replaces the v1 mischaracterization as uniform "synchronous burst-like firing" |
| [interprets-cohen-li-matias-phasic-5ht-responses](interprets-cohen-li-matias-phasic-5ht-responses.md) | discussion | moderate | Phasic 5-HT responses to appetitive and aversive stimuli are documented electrophysiologically (Cohen 2015) and via fiber photometry (Li 2016, Matias 2017) |

### Control / null claims

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [wt-controls-rule-out-light-artifact](wt-controls-rule-out-light-artifact.md) | fig1c, fig2f | strong | Wild-type controls show baseline DRN/control fluorescence and chance-level (~5%) modulation |
| [narrow-spike-interneurons-not-driver-of-rapid-inhibition](narrow-spike-interneurons-not-driver-of-rapid-inhibition.md) | Supp fig4 | moderate | Putative fast-spiking interneurons not preferentially recruited by 5-HT, similar modulation magnitude to wide-spiking neurons, and modulated at *longer* latencies (new in R1) |
| [cortical-layers-show-no-differential-modulation](cortical-layers-show-no-differential-modulation.md) | Supp fig5 | moderate | No layer-dependent differences in 5-HT modulation of cortex (renumbered from Supp Fig 4 in v1) |

### Scope / methodological claims

| Slug | Panel | Epistemic | Summary |
|:-----|:------|:----------|:--------|
| [optogenetic-activation-not-physiological-pattern](optogenetic-activation-not-physiological-pattern.md) | scope | moderate | SERT-Cre + ChR2 stimulation is broader and less structured than endogenous release; light fall-off from the fiber tip and ChR2 frequency-adaptation also mean optogenetic drive itself is not spatially uniform (Dugué 2014) |
| [seven-target-trajectories-13-regions-7478-neurons](seven-target-trajectories-13-regions-7478-neurons.md) | fig2c, fig2d | strong | 7,478 neurons recorded across 13 brain regions in 86 dual-Neuropixel insertions, 57 sessions, 17 mice (11 SERT-Cre, 6 WT) |
| [manifold-from-pooled-super-session](manifold-from-pooled-super-session.md) | methods | moderate | Manifold and orthogonality analyses computed on a pooled super-session of trial-averaged PETHs; nulls are block-aware shuffles |

## Dependency graph

```
hypothesis-additive-modulation  [CENTRAL — R1 reframing]
  ├─ entails → prediction-near-zero-choice-stim-interaction
  ├─ entails → orthogonality-derived-from-additivity → prediction-5ht-axis-orthogonal-to-choice
  │                                                  → prediction-orthogonality-grows-toward-choice
  ├─ supported by ← near-zero-choice-by-stim-interaction
  └─ rules out → multiplicative gain control framework
       └─ supported by ← rules-out-multiplicative-gain-control
            ├─ requires ← near-zero-choice-by-stim-interaction
            ├─ requires ← prediction-multiplicative-gain-yields-significant-interaction
            └─ interprets → interprets-gain-control-default-framework
                          → interprets-5ht2a-gain-control-visual-cortex

hypothesis-orthogonal-neuromodulatory-subspace  [REFRAMED — derived from additivity in v2]
  ├─ derived-from ← hypothesis-additive-modulation
  ├─ supported by ← 5ht-axis-orthogonal-to-choice-axis
  └─ supported by ← orthogonality-significant-in-mpfc-vis-m2

hypothesis-5ht-codes-surprise  [CARRIED OVER — still refuted]
  ├─ entails → prediction-5ht-shifts-psychometric
  ├─ entails → prediction-5ht-accelerates-prior-update
  └─ refuted by ← 5ht-stim-leaves-decision-behavior-intact

hypothesis-state-switch-by-5ht  [CARRIED OVER — quiet wakefulness]
  ├─ supported by ← 5ht-stim-dilates-pupil
  ├─ supported by ← 5ht-stim-suppresses-sharp-wave-ripples
  └─ supported by ← 5ht-stim-increases-exploratory-behaviors

reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control  [NEW R1 — discussion synthesis]
  ├─ interprets → interprets-5ht2a-gain-control-visual-cortex
  ├─ interprets → interprets-lottem-2016-additive-piriform
  ├─ requires ← receptor-expression-predicts-modulation-direction
  │              (5-HT1a/2 oppositely signed receptor coefficients are the empirical anchor)
  └─ explains → 5ht-modulates-all-recorded-regions-bidirectionally
                (regional heterogeneity follows from receptor mix)

receptor-expression-predicts-modulation-strength  [NEW R1 — Fig. 3]
  ├─ supports → 5ht-modulates-all-recorded-regions-bidirectionally
  ├─ companion → receptor-expression-predicts-modulation-direction
  ├─ companion → 5ht1a-predicts-fast-modulation-latency
  └─ companion → drn-projection-density-not-significant-predictor

near-zero-choice-by-stim-interaction
  ├─ requires → glm-significant-choice-and-5ht-coefficients
  └─ requires → seven-target-trajectories-13-regions-7478-neurons

5ht-modulates-all-recorded-regions-bidirectionally
  ├─ requires → wt-controls-rule-out-light-artifact
  ├─ requires → 5ht-modulation-fraction-tracks-chr2-expression
  ├─ requires → seven-target-trajectories-13-regions-7478-neurons
  ├─ requires → optogenetic-activation-not-physiological-pattern
  └─ contextualized by → fmri-bold-correlates-but-misses-suppressed-regions
                         (cross-modality validation + qualitative discrepancy)
```

## Reproduction status

Verification status: not yet attempted (added 2026-04-19, ingest-only). Code is at https://github.com/guidomeijer/SerotoninStimulation; the Fig. 6c GLM analysis and the Fig. 3 receptor-expression GLM analysis are new in R1 and the scripts for them should appear in the repo following submission. Expected reproduction path is the standard IBL pipeline plus the manifold analysis plus the new GLM analyses.

| Status | Count | Claims |
|:-------|:------|:-------|
| unverified | 41 | all (no reproduction attempted at ingest) |

## Notable structural features relative to v1

The v1 paper had two competing post-hoc explanations on offer for the strong-modulation/no-behavior puzzle: (a) the orthogonal-subspace hypothesis (presented as the answer), and (b) implicitly, that the modulation simply did not interact with task-relevant variables. The v1 graph encoded only (a). R1 promotes (b) — additivity — to the central organizing claim and demotes (a) to a derivation. The structural shift the graph captures: in v1, orthogonality was the primary node with several supporting empirical confirmations; in R1, additivity is the primary node, with both the GLM interaction-term result and the orthogonality manifold result feeding into it (the latter as a derived geometric consequence rather than an independent finding). The graph also adds a `rules-out` relation to the multiplicative-gain framework — making the elimination structure explicit rather than rhetorical.

R1 also adds a new branch of the graph entirely: the receptor-expression GLM analyses (Fig. 3, four claims) provide a partial mechanistic substrate for the regional heterogeneity in 5-HT modulation. This branch dovetails with the discussion-level reconciliation hypothesis (`reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control`) by establishing empirically that 5-HT1a and 5-HT2 receptors contribute oppositely-signed effects, which is the necessary precondition for the receptor-dominance explanation of the brain-wide additive mode.

The Hamada-fMRI comparison (Supp. Fig. 3, `fmri-bold-correlates-but-misses-suppressed-regions`) is methodologically consequential: it establishes that fMRI BOLD correlates with single-unit modulation magnitude but cannot resolve the bidirectional sign that single-unit recording reveals — an important methodological contrast for the field's interpretation of prior opto-fMRI serotonin work.

The latency analysis (Fig. 2k–m) was substantively revised under the new latenZy method (Haak & Heimel 2025): the v1 finding "fast inhibition / slow excitation" could not be replicated and was removed. The new finding (`latency-correlates-with-absolute-modulation`) is that stronger modulation in either direction is associated with shorter latency. The previous-draft slug `inhibition-fast-excitation-slow` is therefore retired in favor of the new slug.
