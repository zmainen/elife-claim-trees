---
uuid: 01384854-d4e5-4e8c-bf0b-239409c22675
slug: globuli-cells-cholinergic-gabaergic
doi: ~
claim: >
  The globuli cell cluster at the mushroom body heads of Uloborus diversus is revealed by
  ChAT immunoreactivity and to a lesser extent by GAD immunoreactivity, indicating that the
  globuli cells represent cholinergic and GABAergic populations; this is consistent with prior
  demonstration of ChAT-positive globuli cells in C. salei.
claim-type: empirical
role: empirical
concepts:
  - globuli cells
  - mushroom body
  - cholinergic
  - GABAergic
  - ChAT
  - GAD
  - spider brain
priority: 2026-03-30
epistemic: moderate

confirms:
  - mushroom-bodies-present-asta-exclusive

belongings:
  - relation: supports
    target: mushroom-bodies-present-asta-exclusive

assertions:
  - paper-slug: artiushin-2026-spider-atlas
    doi: 10.7554/eLife.107732
    panel: fig7H, fig7I
    figureUri: https://iiif.elifesciences.org/lax/107732%2Felife-107732-fig7-v1.tif/full/1500,/0/default.jpg
    analysis: atlas visualization
    dataset: https://doi.org/10.35077/ace-owl-gum
    dataset-doi: 10.35077/ace-owl-gum
    method: immunofluorescence, anti-ChAT / anti-GAD, confocal atlas
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: >
      Results: "We find the cluster of cells closely associated with the MB heads is revealed by
      ChAT immunoreactivity, and to a lesser extent by GAD immunoreactivity, suggesting they
      represent cholinergic and GABAergic populations." Fig7H shows ChAT putative globuli cells
      with DAPI; Fig7I shows GAD potential innervation. BIL atlas required.
---

Epistemic status is moderate rather than strong because: (1) globuli cells are not distinguishable from surrounding nuclei by DAPI signal alone, so the identification is inferred from juxtaposition with the MB head; (2) anti-GAD signal penetration is limited to the tissue periphery (see gad-antibody-peripheral-penetration-only), which may affect the reliability of the GABAergic claim. The ChAT claim is better grounded, consistent with C. salei data (Fabian-Fine et al., 2017), and elevated relative to the GABAergic attribution.
