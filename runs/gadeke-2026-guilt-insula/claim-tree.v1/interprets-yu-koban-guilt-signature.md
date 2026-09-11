---
uuid: 1f9bf241-1d6a-4288-80a3-cf0f5d9460a0
slug: interprets-yu-koban-guilt-signature
doi: 10.1101/835520
claim: >
  Yu and Koban (with colleagues) trained a whole-brain multivariate SVM to decode
  interpersonal guilt from fMRI activity patterns and derived a voxel-weight map — the
  "guilt signature" — that generalizes across guilt-inducing paradigms. The signature
  loads most strongly on anterior insula, medial prefrontal, and surrounding regions and
  has been validated as a pattern-level neural marker of guilt states across independent
  samples.
displayClaim: >
  Yu, Koban and colleagues trained a whole-brain multivariate guilt signature from fMRI
  activity patterns; the signature loads on anterior insula and has been validated as a
  generalizable pattern-level marker of interpersonal guilt.
shortClaim: "The Yu & Koban multivariate guilt signature is a validated neural marker of guilt."
claim-type: interpretive
role: literature-context
concepts:
  - neural guilt signature
  - multivariate pattern
  - anterior insula
  - convergent validity
priority: 2026-04-20
epistemic: moderate

belongings: []

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: ~
    panel: fig4 supplement (convergent-validity analysis)
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: ~
    dataset: ~
    dataset-doi: ~
    method: literature interpretation; cited as the prior pattern map against which this paper's guilt contrast is tested for convergent validity
    confidence: moderate

reproductions: []
---

This claim registers the Yu/Koban guilt signature as a discrete literature node so the dot-product convergent-validity test (`insula-guilt-replicates-yu-koban-signature`) and the individual-differences null (`guilt-signature-no-individual-difference`) both have an explicit reference to point at. The present paper uses the signature in its standard pattern-expression role: compute the voxelwise dot product between each participant's guilt-effect map and the Yu/Koban weight map, and test whether the resulting scores are significantly greater than zero.

The signature is load-bearing for this paper's argument in a specific way. The univariate anterior-insula result (`insula-tracks-guilt-effect`) establishes a local effect; the Yu/Koban comparison argues that this local effect sits on the same pattern as prior work's multivariate guilt marker, upgrading the univariate finding from "insula happens to be active here" to "insula is active in the specific pattern-level way that prior work characterized as a guilt state." The individual-differences null (`guilt-signature-no-individual-difference`) then qualifies the strength of this convergent-validity claim: group-level pattern expression is significant, but the dot products do not correlate with each participant's behavioral guilt effect, so the signature is a population-level marker here rather than a subject-level trait readout.
