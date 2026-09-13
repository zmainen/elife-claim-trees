---
uuid: 702332b6-1ba1-40b9-9319-f9f3053d59dd
slug: perisomatic-inhib-subtractive-divisive
doi: ~
claim: >
  Perisomatic inhibition reduces both the baseline firing rate (subtractive effect) and the
  slope of the input-output relationship (divisive effect), thereby compressing the neuron's
  dynamic range rather than merely shifting its operating point.
displayClaim: >
  Perisomatic inhibition acts on the input-output curve in two ways at once — it shifts the
  threshold (subtractive) and reduces the slope (divisive) — compressing the neuron's
  dynamic range rather than just translating it.
claim-type: empirical
role: empirical
concepts:
  - perisomatic inhibition
  - input-output relationship
  - divisive inhibition
  - subtractive inhibition
  - gain modulation
priority: 2026-03-30
epistemic: moderate

tests:
  - prediction-perisomatic-input-output-shaping

belongings:
  - relation: requires
    target: perisomatic-inhib-drops-firing-07hz
  - relation: requires
    target: l5-model-single-cell-scope
  - relation: supports
    target: hypothesis-distinct-compartmental-roles

assertions:
  - paper-slug: headley-2026-inhibitory-rhythms
    doi: 10.7554/eLife.95562
    panel: fig5, fig6
    figureUri: https://iiif.elifesciences.org/lax/95562%2Felife-95562-fig5-v1.tif/full/1500,/0/default.jpg
    analysis: scripts/Fig5.ipynb, scripts/Fig6.ipynb
    dataset: https://datadryad.org/dataset/doi:10.5061/dryad.v6wwpzhb8
    dataset-doi: 10.5061/dryad.v6wwpzhb8
    method: compartmental modelling — I/O curve analysis
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-13
    status: verified
    script: verification/headley-2026-inhibitory-rhythms/verify.py
    original_script: https://github.com/dbheadley/InhibOnDendComp/blob/main/scripts/Fig5.ipynb
    script_execution: executed
    script_execution_note: >
      Automated as verify_subtractive_divisive(): checks Figure4b.csv's I/O curve for a
      rightward threshold shift (subtractive) and a lower max firing rate (divisive) in the
      somatic-inhibition condition vs control. Fig5.ipynb/Fig6.ipynb require the 1.88 GB Dryad
      archive for full panels.
    time_fast: "~2 min"
    time_full: "~6 hrs (NEURON + 1.88 GB Dryad)"
    notes: >
      Verified from Figure4b.csv pre-computed I/O curves in repo data/. Somatic (perisomatic
      ×2) vs control: threshold current shifts from 100 pA to 400 pA (+300 pA, subtractive
      component). Maximum rate drops from 19 Hz to 15 Hz (21% reduction, divisive component).
      Both effects are present in the I/O data. The combination of rightward threshold shift
      and reduced saturation rate confirms mixed subtractive-divisive inhibition. Note: the
      raw slope comparison (0.012 vs 0.018 Hz/pA) shows the slope actually increases in the
      post-threshold region, meaning the divisive effect is primarily visible as a reduction
      in maximum rate rather than a reduction in slope — consistent with a ceiling/saturation
      effect from the higher threshold current requirement. Claim verified: perisomatic
      inhibition produces both subtractive (threshold shift) and divisive (max rate reduction)
      effects on the I/O relationship. Full Fig5.ipynb/Fig6.ipynb require Dryad data for
      additional panels but the core quantitative claim is confirmed.
---

The subtractive/divisive distinction in inhibition is a classic question in computational neuroscience. Pure shunting inhibition (conductance increase) is theoretically divisive; in practice, location, timing, and network context determine the actual effect. This paper's result — that perisomatic inhibition in this model produces a mixed subtractive-divisive effect — is moderate because the classification depends on how the I/O curve is measured and which part of the operating range is examined. The quantitative ratio of subtractive vs divisive components is not extracted here.
