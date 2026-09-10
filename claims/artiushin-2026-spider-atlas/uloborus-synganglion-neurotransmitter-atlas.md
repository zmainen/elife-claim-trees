---
uuid: ea4408d1-ec9e-491f-83d8-47edc01122d5
slug: uloborus-synganglion-neurotransmitter-atlas
doi: ~
claim: >
  A three-dimensional immunofluorescence atlas of the Uloborus diversus synganglion is established, mapping the distributions of GABA, acetylcholine, serotonin, octopamine/tyramine, and a subset of neuropeptides across all identified neuropils using elastix-registered confocal volumes.
claim-type: existence
role: methodological
concepts:
  - Uloborus diversus
  - synganglion
  - neurotransmitter atlas
  - immunofluorescence
  - 3D registration
priority: 2026-03-30
epistemic: strong

enables-method:
  - leg-neuropils-consistent-innervation
  - leg-neuropil-serotonin-bilateral-innervation
  - opisthosomal-neuropil-tdc2-perimeter-ladder
  - pedipalpal-neuropil-chat-tdc2-dominant
  - cheliceral-neuropil-serotonin-tdc2-dominant
  - hagstone-neuropil-serotonin-defined
  - mushroom-bodies-present-asta-exclusive
  - globuli-cells-cholinergic-gabaergic
  - tonsillar-neuropil-novel-structure
  - tonsillar-neuropil-serotonin-core-tdc2-shell
  - protocerebral-bridge-candidate-central-complex
  - protocerebral-bridge-layered-transmitter-architecture
  - arcuate-body-layers-neurotransmitter-distinguished
  - arcuate-body-four-sublayer-differential

belongings: []

assertions:
  - paper-slug: artiushin-2026-spider-atlas
    doi: ~
    panel: figs 1-13
    analysis: GordusLab/Artiushin-elastix-eLife (GitHub)
    dataset: https://doi.org/10.35077/ace-owl-gum
    dataset-doi: 10.35077/ace-owl-gum
    method: confocal microscopy, elastix image registration
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      BIL TIFF stacks are large (likely tens of GB). elastix registration pipeline on GitHub. Computationally intensive. Not yet executed.
---
