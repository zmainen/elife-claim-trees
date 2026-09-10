---
uuid: e5023cc6-f631-4d2b-b768-ed36dbef9edb
slug: no-bold-differences-test-phases
doi: ~
claim: >
  During both test phases (test_new and test_old), no significant BOLD activation differences
  between any CS type contrasts are found, despite significant US expectancy differences at
  the behavioral level, motivating RSA over univariate analysis.
claim-type: empirical
role: control
concepts:
  - null result
  - BOLD activation
  - test phase
  - univariate analysis
  - RSA motivation
priority: 2026-03-30
epistemic: moderate

enables-method:
  - ifg-reinstates-reversal-traces-item-specific
  - dmpfc-reinstates-acquisition-traces-generalized

belongings:
  - relation: supports
    target: cue-generalization-increases-acquisition

assertions:
  - paper-slug: bouyeure-2026-fear-rsa
    doi: 10.7554/eLife.105126
    panel: fig2B (test phases)
    figureUri: https://iiif.elifesciences.org/lax/105126%2Felife-105126-fig2-v1.tif/full/1500,/0/default.jpg
    analysis: run_nina_analysis.py
    dataset: https://doi.org/10.17605/OSF.IO/NGWKA
    dataset-doi: 10.17605/OSF.IO/NGWKA
    method: second-level mass-univariate GLM, cluster FWE with 10k permutations (p_uncorr<0.001)
    confidence: moderate

reproductions:
  - agent: mainen-z
    date: 2026-03-30
    status: unattempted
    notes: ~
---

This is a critical rhetorical claim: the paper uses the failure of univariate BOLD analysis in test phases to argue that representational pattern analysis (RSA) is necessary to detect memory traces. The claim is a null result — absence of significant clusters across all contrasts (CS++ > CS--, CS-+ > CS--, CS+- > CS--) in both test phases. Null results are sensitive to the multiple comparison correction applied. The paper applies Bonferroni-corrected cluster FWE at p<0.025 (two comparisons per phase); this threshold may be conservative enough to suppress true effects as well as noise.
