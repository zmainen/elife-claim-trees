---
uuid: 12a7d6d9-5768-4559-8dfe-60e9163a461b
slug: hypothesis-additive-modulation
doi: ~
claim: >
  Optogenetic activation of dorsal-raphe serotonergic neurons modulates downstream single-neuron
  spiking activity additively rather than multiplicatively — that is, the 5-HT effect on a
  neuron's firing rate is well approximated by a constant additive offset that is independent
  of the choice-related component of activity, rather than by a gain factor that scales the
  choice-related component. As a per-neuron statistical statement this predicts a near-zero
  choice-by-stimulation interaction term in a generalized linear model with separate choice,
  stimulation, and choice×stimulation predictors.
displayClaim: >
  5-HT modulates spiking activity additively (constant offset, independent of choice) rather
  than multiplicatively (gain), brain-wide.
shortClaim: "5-HT modulates spiking additively, not multiplicatively, brain-wide."
claim-type: hypothesis
role: hypothesis
concepts:
  - additive modulation
  - multiplicative gain
  - generalized linear model
  - neuromodulator computation
  - choice coding
priority: 2026-04-19
epistemic: hypothesis

belongings: []

entails:
  - prediction-near-zero-choice-stim-interaction
  - prediction-multiplicative-gain-yields-significant-interaction
  - orthogonality-derived-from-additivity

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: hypothesis
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: stated as the central organizing hypothesis in the R1 abstract, introduction (orthogonality paragraph), results (GLM coefficients paragraph), and discussion
    confidence: N/A

reproductions: []
---

This is the central organizing hypothesis of the R1 manuscript and the conceptual reframing relative to v1. Where v1 led with the geometric finding (orthogonality of the 5-HT and choice subspaces) and treated additivity as an implicit consequence, R1 leads with additivity as a directly-tested computational claim and treats orthogonality as its geometric corollary. The two claims are mathematically equivalent in a 2×2 factorial choice × stimulation design under linear (PCA) projection — additive modulation displaces every choice trajectory by the same vector, which by definition is orthogonal to the displacement that distinguishes the choice trajectories from each other. The reframing is therefore not a new measurement but a new hierarchy of explanation: the additivity hypothesis names the underlying computational property, and the orthogonality result is what a manifold-geometry view of that property looks like.

The hypothesis is consequential because it directly contradicts the dominant computational framework for neuromodulators, which since Servan-Schreiber et al. (1990) has treated them as multiplicative gain controllers that scale neural input-output functions (`interprets-gain-control-default-framework`). For serotonin specifically, this gain-control framework has been instantiated through 5-HT2A receptors in visual cortex (`interprets-5ht2a-gain-control-visual-cortex`). The additivity finding does not rule out gain-control mechanisms locally — it rules them out as the *brain-wide dominant mode*. The receptor-dependent reconciliation that R1 proposes (`reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control`) is that the 5-HT2A gain component coexists with a 5-HT1A-mediated stimulus-independent baseline suppression, and the brain-wide additive signature reflects dominance of the latter across most regions.

The single-region precedent for additive 5-HT modulation in a behaving animal is Lottem et al. (2016, from the Mainen lab), which found that DRN serotonin stimulation in piriform cortex suppressed spontaneous firing while leaving odor-evoked responses intact (`interprets-lottem-2016-additive-piriform`). This paper's brain-wide GLM result generalizes that single-region finding to 13 regions and a perceptual decision task.
