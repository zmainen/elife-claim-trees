---
uuid: 2cc94e19-2dac-419d-aea0-d0672cc3ecf0
slug: interprets-gain-control-default-framework
doi: 10.1126/science.2392679
claim: >
  The dominant computational framework for neuromodulators, established by Servan-Schreiber,
  Printz & Cohen (Science, 1990) and elaborated by Salinas & Thier (Neuron, 2000), treats
  neuromodulators as multiplicative gain controllers that scale neural input-output
  functions. This framework has been the default theoretical lens for interpreting
  neuromodulator effects on cortical computation for over three decades.
displayClaim: >
  The dominant theoretical framework treats neuromodulators as multiplicative gain
  controllers scaling input-output functions (Servan-Schreiber 1990, Salinas & Thier 2000).
claim-type: interpretive
role: literature-context
concepts:
  - gain modulation
  - neuromodulator computation
  - input-output function
  - theoretical framework
priority: 2026-04-19
epistemic: moderate

belongings: []

assertions:
  - paper-slug: meijer-2025-serotonin-additive-r1
    doi: ~
    panel: introduction (I1), results (R2 GLM paragraph), discussion (D1)
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited at three points in R1 (introduction reframing, results contrastive prediction setup, discussion eliminative claim)
    confidence: moderate

reproductions: []
---

This is a literature-interpretation claim that registers the gain-control framework as a discrete theoretical entity in the graph. Its function is to give the eliminative claim `rules-out-multiplicative-gain-control` something explicit to point at — without this node, "this paper rules out gain control" would have an unnamed referent.

Two source references anchor the framework. Servan-Schreiber, Printz & Cohen (1990, *Science* 249:892) developed the original computational treatment of neuromodulators (specifically dopamine and norepinephrine in their analysis) as gain controllers in connectionist networks, formalizing the role with the temperature parameter of a sigmoid activation function. Salinas & Thier (2000, *Neuron* 27:15) generalized the framework to broader cortical computation and established multiplicative gain as a canonical mechanism for nonlinear interaction between neural signals.

The framework is widely adopted but not exclusive — competing accounts include divisive normalization (which is multiplicative-divisive), additive-shift models, and receptor-specific computational accounts. The R1 paper engages with the gain-control framework specifically because it is the *default* — the prior expectation against which the additivity finding registers as a departure. The introduction (I1 per revision notes) names the framework and its serotonin-specific instantiation in visual cortex as the prior; the results (R2 per revision notes) names it as the source of the contrastive prediction; the discussion (D1 per revision notes) names it as what the data fail to support.

The claim does not assert the framework is correct or incorrect — it asserts that the framework exists, has the indicated theoretical content, and has been the default. The status (correct/incorrect) is a question that this paper's data bear on (via `rules-out-multiplicative-gain-control`).
