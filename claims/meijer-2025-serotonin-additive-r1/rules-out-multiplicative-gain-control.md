---
uuid: 492e197a-6d02-41c1-95e8-b425f6af9678
slug: rules-out-multiplicative-gain-control
doi: ~
claim: >
  The near-zero choice-by-stimulation interaction in the per-neuron GLM is inconsistent with
  multiplicative gain modulation as the dominant brain-wide mode of serotonergic action
  during the perceptual decision task. The dominant computational framework for
  neuromodulators since Servan-Schreiber et al. (1990) — that they act as multiplicative
  gain controllers scaling neural input-output functions — is therefore eliminated as the
  primary explanation of brain-wide 5-HT effects, although the result does not rule out
  gain-control mechanisms operating in specific regions, on specific timescales, or via
  specific receptors.
displayClaim: >
  The near-zero interaction term rules out multiplicative gain modulation as the
  dominant brain-wide mode of 5-HT action.
shortClaim: "A near-zero interaction term rules out multiplicative gain as the dominant 5-HT mode."
claim-type: interpretive
role: synthesis
concepts:
  - eliminative inference
  - gain control framework
  - additive modulation
  - brain-wide
priority: 2026-04-19
epistemic: strong
status: confirmed
panel: results+discussion

belongings:
  - relation: requires
    target: near-zero-choice-by-stim-interaction
  - relation: requires
    target: prediction-multiplicative-gain-yields-significant-interaction
  - relation: requires
    target: interprets-gain-control-default-framework

interprets:
  - interprets-gain-control-default-framework
  - interprets-5ht2a-gain-control-visual-cortex

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: results (GLM coefficients paragraph), discussion (D1)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: eliminative inference from contrastive prediction; explicit in R1 abstract ("This is inconsistent with the multiplicative gain modulation widely assumed to be the default mode of neuromodulatory action") and discussion ("This does not support multiplicative gain control — the dominant computational framework for neuromodulators since Servan-Schreiber et al. (1990)")
    confidence: strong

reproductions: []
---

This is one of two new R1-only synthesis claims (the other being `orthogonality-derived-from-additivity`). Its function in the graph is to make the eliminative inferential structure explicit. Without this node, the GLM result `near-zero-choice-by-stim-interaction` would sit as a description; with this node, the description carries forward as a positive elimination of the gain-control framework. The eliminative move is licensed by the explicit contrastive prediction `prediction-multiplicative-gain-yields-significant-interaction` — gain control entailed a significant interaction; the data show none; therefore gain control is rejected.

The scope of the elimination is bounded by three conditions that the graph encodes through the requires relations:

1. *Brain-wide and dominant.* The result averages across the 13 recorded regions and across animals. Region-specific gain control might persist below the brain-wide signature; the visual-cortex 5-HT2A gain control of `interprets-5ht2a-gain-control-visual-cortex` is a known case the paper explicitly preserves. This is reconciled in `reconciles-5ht1a-baseline-suppression-with-5ht2a-gain-control` — the brain-wide additive mode reflects dominance of 5-HT1A baseline suppression, not absence of 5-HT2A gain.

2. *In this task, with this stimulation protocol.* The same stimulation in a different paradigm with stronger surprise/punishment/uncertainty content might recruit different receptor populations and a different brain-wide mode. The graph carries this through `optogenetic-activation-not-physiological-pattern` (scope) on the upstream empirical claim.

3. *Statistical bound.* The t-test against zero with n = 10 animals is an absence-of-evidence test; it excludes large interactions but is not powered to detect small ones. The elimination is therefore "the data are inconsistent with gain control as the dominant brain-wide mode" rather than "gain control does not exist at any scale."

Within those bounds, however, the claim is genuinely eliminative, not merely null. This is the structural difference between R1 and v1 that the abstract change captures: v1 reported intact behavior alongside strong neural modulation and proposed orthogonality as a reconciliation; R1 makes a positive computational claim about how neuromodulation acts.
