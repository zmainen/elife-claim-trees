---
uuid: a26a42bf-23a3-4c8c-a8da-981b1b317381
slug: guilt-signature-no-individual-difference
doi: ~
claim: >
  Individual dot-product values between participants' guilt-related BOLD responses and
  the Yu & Koban neural guilt signature do not correlate with individual behavioral
  guilt effect scores (Spearman's Rho=−0.058, p=0.725), indicating the neural signature
  does not track individual differences in guilt sensitivity as measured behaviorally.
claim-type: empirical
role: empirical
concepts:
  - guilt signature
  - individual differences
  - neural-behavioral correlation
  - null result
  - insula
priority: 2026-03-30
epistemic: moderate

dissociates-with:
  - insula-guilt-replicates-yu-koban-signature

interprets:
  - interprets-yu-koban-guilt-signature

belongings:
  - relation: extends
    target: insula-guilt-replicates-yu-koban-signature

assertions:
  - paper-slug: gadeke-2026-guilt-insula
    doi: 10.7554/eLife.105391
    panel: fig4 (supplement, text)
    figureUri: https://iiif.elifesciences.org/lax/105391%2Felife-105391-fig4-v1.tif/full/1500,/0/default.jpg
    analysis: f_apply_YuKoban_guilt_signature_map.m
    dataset: https://openneuro.org/datasets/ds005588
    dataset-doi: 10.18112/openneuro.ds005588.v1.0.0
    method: Spearman correlation between dot products and behavioural guilt effect
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-09-11
    status: partial
    script: verification/gadeke-2026-guilt-insula/verify.py
    script_execution: executed
    data_source: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
    data_file: fMRIresults/outcome/guiltEffectEachPartic.nii
    paper_value: "Spearman rho=-0.058, p=0.725"
    reproduced_value: "rho=0.088, p=0.588, n=40 — null reproduces, coefficient differs from the reported -0.058. Volume i is assumed to be row i: the deposit ships no participant order for the 4D map, so"
    notes: >
      Re-checked 2026-09-11 against the deposited group statistical map, observed by verification/audit_run.py. Paper: Spearman rho=-0.058, p=0.725. Reproduced: rho=0.088, p=0.588, n=40 — null reproduces, coefficient differs from the reported -0.058. Volume i is assumed to be row i: the deposit ships no participant order for the 4D map, so the pairing cannot be confirmed from it.. The substantive claim — no correlation between the neural signature and individual behavioural guilt — reproduces; the coefficient does not match the reported value, and the deposit ships no participant order for the 4D map, so volume-to-row pairing is assumed rather than confirmed.
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

The null individual-difference correlation is a negative finding that qualifies the positive group-level signature match. The group-level result (mean dot product positive, p=0.017) suggests the pattern is present on average, but the absence of individual correlation (Rho=−0.058) means the signature's magnitude does not track who feels more behaviorally guilty. This could reflect limited power (N=40 fMRI participants) or a genuine dissociation between average neural pattern match and individual behavioral sensitivity. The authors report the null without extensive discussion.
