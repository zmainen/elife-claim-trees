---
uuid: 63ea3299-4288-46d1-b563-784d69f364cf
slug: social-perceptual-salience-independent-streams
doi: ~
claim: >
  Social salience and perceptual salience operate via largely independent mechanisms in
  attentional selection: their effects are additive for other-associated stimuli (interaction
  term -0.54 Hz, HDI includes zero), confirming that arbitrary social association and
  physical salience capture attention through separate processing streams rather than a
  single shared resource.
shortClaim: "Social and perceptual salience add independently in attentional selection."
claim-type: interpretive
role: interpretation
concepts:
  - social salience
  - perceptual salience
  - independent mechanisms
  - attentional processing streams
  - additivity
priority: 2026-03-30
epistemic: moderate

interprets:
  - self-social-additive-perceptual
  - self-salience-reduces-perceptual-benefit
  - perceptual-salience-6hz-advantage
confirms:
  - hypothesis-social-perceptual-independent-mechanisms

belongings:
  - relation: requires
    target: self-social-additive-perceptual
  - relation: requires
    target: perceptual-salience-6hz-advantage

assertions:
  - paper-slug: scheller-2026-self-prioritization
    doi: 10.7554/eLife.100932
    panel: fig7 (synthesis)
    figureUri: https://iiif.elifesciences.org/lax/100932%2Felife-100932-fig7-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: interpretive synthesis from interaction analysis
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: partial
    notes: >
      Interpretive synthesis — component empirical claims verified from OSF data.
      Additivity for other-associated stimuli confirmed: interaction ≈ +0.63 Hz (near-zero,
      consistent with additivity claim of -0.54 Hz). Sub-additivity for self-associated
      confirmed: self-salient benefit (2.58 Hz) << sum of social (-1.36) + perceptual (6.05)
      effects. The interpretation of "independent streams" follows from confirmed additivity
      pattern for non-self stimuli.
---

The independence claim is supported for other-associated stimuli but violated for self-associated stimuli (sub-additive interaction). This asymmetry is theoretically meaningful: the "separate streams" interpretation holds specifically for information that lacks personal relevance. When the object is self-associated, the self-relevance stream overrides and partially suppresses the salience stream — which is why the perceptual salience benefit is smaller for self-associated than for other-associated stimuli.
