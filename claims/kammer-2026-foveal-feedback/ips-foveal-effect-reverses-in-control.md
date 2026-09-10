---
uuid: 3af0625b-efea-46a1-93d6-60b55f7506e9
slug: ips-foveal-effect-reverses-in-control
doi: ~
claim: >
  In the control condition (direct foveal stimulation), IPS activation is significantly negatively associated with foveal decoding (t(27)=−3.61, p=0.004, difference=11.6), the opposite direction to the experimental condition, confirming that the IPS–foveal decoding relationship is specific to the feedback context.
displayClaim: >
  Under direct foveal stimulation the IPS–foveal-decoding correlation reverses sign, confirming that the positive coupling seen during feedback is context-specific and not a generic effect of attention or arousal.
claim-type: empirical
role: control
concepts:
  - IPS
  - control condition
  - parametric modulation
  - specificity
  - direct stimulation
priority: 2026-03-30
epistemic: strong

validates:
  - ips-candidate-driver-foveal-feedback
rules-out:
  - "generic brain-state or arousal explanation of IPS-foveal-decoding coupling"

belongings:
  - relation: supports
    target: ips-candidate-driver-foveal-feedback
  - relation: extends
    target: fef-lo-nonsignificant-after-correction

assertions:
  - paper-slug: kammer-2026-foveal-feedback
    doi: ~
    panel: fig4-figure-supplement-1
    figureUri: https://iiif.elifesciences.org/lax/107053%2Felife-107053-fig4-figsupp1-v1.tif/full/1500,/0/default.jpg
    analysis: Lucakaemmer/FovealFeedback (GitHub)
    dataset: https://doi.org/10.18112/openneuro.ds005933.v1.0.0
    dataset-doi: 10.18112/openneuro.ds005933.v1.0.0
    method: parametric modulation analysis (FSL FEAT), control condition
    confidence: strong

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: blocked
    blocked_by: compute-infeasible
    notes: >
      Blocker (2026-03-30): Control condition parametric modulation, supplementary figure. Requires
      same FSL FEAT parametric modulation GLM as the experimental condition IPS analysis, run on
      control-condition runs (run separately from experimental). IPS control: t(27)=−3.61, p=0.004,
      difference=11.6 (sign reversal from +4.22 experimental). Same hard-coded path blocker
      (/home/lkaemmer/…/control_regressors.pkl) applies. Two-source confidence (B caption, A results
      text). The sign reversal mechanistically supports IPS-as-feedback-driver but requires same
      ~100 CPU-hours minimum pipeline to verify.
---

The reversal in the control condition is an important specificity check. If IPS activity were simply a proxy for brain-state variance or signal-to-noise, it would correlate with foveal decoding in both conditions. The fact that IPS correlates positively with foveal decoding in the experimental condition (eye movements → feedback → IPS active → better foveal decoding) but negatively in the control condition (eye movements → gaze away from foveal stimulus → IPS active → worse foveal decoding) is mechanistically coherent and supports the IPS-as-feedback-driver interpretation.
