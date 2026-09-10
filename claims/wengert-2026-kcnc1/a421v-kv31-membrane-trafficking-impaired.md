---
uuid: ba388b6b-662d-4f09-b481-11f90f7057dc
slug: a421v-kv31-membrane-trafficking-impaired
doi: ~
claim: >
  The ratio of membrane to cytosolic Kv3.1 immunofluorescence intensity is significantly
  reduced in PV-INs from juvenile (P24–33) Kcnc1-A421V/+ mice compared to WT controls
  (n=48 vs n=49 cells, N=5 vs N=6 mice), indicating that impaired trafficking to the
  cell surface contributes to the loss of K+ current density.
claim-type: empirical
role: empirical
concepts:
  - Kv3.1
  - membrane trafficking
  - immunohistochemistry
  - PV interneurons
  - subcellular localization
priority: 2026-03-30
epistemic: strong

tests:
  - prediction-kv31-surface-expression-reduced
confirms:
  - prediction-kv31-surface-expression-reduced
  - hypothesis-a421v-causes-kv31-lof

belongings:
  - relation: supports
    target: pv-ins-reduced-k-current-density
  - relation: extends
    target: pv-ins-reduced-k-current-density

assertions:
  - paper-slug: wengert-2026-kcnc1
    doi: 10.7554/eLife.103784
    panel: fig3H, fig3I
    figureUri: https://iiif.elifesciences.org/lax/103784%2Felife-103784-fig3-v1.tif/full/1500,/0/default.jpg
    scope: ex-vivo
    analysis: G-Node analysis code
    dataset: https://doi.org/10.12751/g-node.bqni9h
    dataset-doi: 10.12751/g-node.bqni9h
    method: immunohistochemistry, fluorescence intensity ratio quantification
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: no-data
    notes: >
      Significance: ***p<0.001 by unpaired t-test. The analysis quantifies membrane-to-cytosol
      Kv3.1 ratio as an index of subcellular distribution. The authors note that more prominent
      cytosolic labeling in mutants likely corresponds to endoplasmic reticulum accumulation.
---

This trafficking claim is mechanistically important: it distinguishes between loss of
channel conductance (gating) and loss of surface expression. The paper reports no differences
in voltage dependence or activation kinetics (fig3F, fig3G), making trafficking the more
parsimonious explanation. This is an interpretive implication drawn from two complementary
results: absent gating differences plus reduced membrane/cytosol ratio.
