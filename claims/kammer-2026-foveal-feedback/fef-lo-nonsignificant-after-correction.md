---
uuid: 3190bd67-2477-4174-b65f-7e70b8128535
slug: fef-lo-nonsignificant-after-correction
doi: ~
claim: >
  Frontal eye fields (FEF) and lateral occipital area (LO) show trends in the expected direction but do not survive Bonferroni correction for multiple comparisons in the parametric modulation analysis (LO: t(27)=0.67, p=0.767; FEF: t(27)=2.07, p=0.072), making IPS the only ROI significantly associated with foveal decoding after correction.
displayClaim: >
  Neither FEF nor LO survives Bonferroni correction in the parametric modulation analysis, leaving IPS as the only ROI specifically coupled to foveal decoding rather than a global brain-state effect.
claim-type: empirical
role: control
concepts:
  - frontal eye fields
  - FEF
  - lateral occipital area
  - parametric modulation
  - multiple comparisons
  - negative result
priority: 2026-03-30
epistemic: moderate

rules-out:
  - "FEF as candidate driver of foveal feedback"
  - "LO as candidate driver of foveal feedback"

belongings:
  - relation: supports
    target: ips-candidate-driver-foveal-feedback

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig4B
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: parametric modulation analysis (FSL FEAT), Bonferroni correction
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Same parametric modulation pipeline as ips-candidate-driver-foveal-feedback
      (FSL FEAT → ROI averaging, Bonferroni correction across IPS/FEF/LO). FEF: t(27)=2.07, p=0.072
      uncorrected (threshold p<0.0167 with Bonferroni for 3 ROIs); LO: t(27)=0.67, p=0.767. Both fail
      correction. Code path: same as IPS claim including the hard-coded pickle path blocker.
      Two-source confidence (A results text, B caption); exploratory analysis.
---

Note that FEF (p=0.072 uncorrected) is borderline: with three ROIs and Bonferroni correction, the threshold would be p<0.0167. FEF passes only if you ignore the correction. The paper appropriately reports this as non-significant after correction. This negative result matters because it makes the IPS finding more specific rather than a global brain-state effect.
