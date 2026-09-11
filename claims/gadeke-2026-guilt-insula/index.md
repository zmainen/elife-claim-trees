---
paper-slug: gadeke-2026-guilt-insula
title: "Contributions of insula and superior temporal sulcus to interpersonal guilt and responsibility in social decisions"
authors:
  - Maria Gädeke
  - Tom Willems
  - Omar Salah Ahmed
  - Bernd Weber
  - René Hurlemann
  - Johannes Schultz
journal: eLife
stage: published
doi: 10.7554/eLife.105391
url: https://elifesciences.org/articles/105391
github: https://github.com/BonnSocialNeuroscienceUnit/ResponsibilityExperiment
openneuro: https://openneuro.org/datasets/ds005588
added: 2026-03-30
badge: gold
claim-count: 26
questions:
- id: q1
  text: Does the anterior insula encode interpersonal guilt — the responsibility-contingent affect that
    arises specifically when a participant's own choice causes a negative outcome for their partner, as
    distinct from empathy for partner loss or regret over one's own loss?
- id: q2
  text: Is momentary happiness during social decisions under risk governed by a responsibility-weighted
    rule in which partner reward prediction errors caused by the participant's own choice carry an independent,
    non-zero weight — so that the larger happiness drop after low partner outcomes when the participant
    chose reflects interpersonal guilt rather than another cause?
- id: q3
  text: Does the superior temporal sulcus represent the partner's affective state — tracking partner reward
    prediction errors — specifically when the participant is responsible for the partner's outcome?
---

## Abstract

This study investigated the neural mechanisms involved in feelings of interpersonal guilt and responsibility evoked by social decisions in humans. In two studies (one during fMRI), participants repeatedly chose between safe and risky monetary outcomes in social contexts. Across conditions, each participant chose for both themselves and a partner (Social condition), or the partner chose for both themselves and the participant (Partner condition), or the participant chose just for themselves (Solo condition, control). If the risky option was chosen in the Social or Partner condition, participant and partner could each receive either the high or the low outcome of a lottery with 50% probability, independently of each other. Participants were shown the outcomes for themselves and for their partner on each trial and reported their momentary happiness every few trials. As expected, participant happiness decreased following both low lottery outcomes for themselves and for the partner. Crucially, happiness decreases following low outcomes for the partner were larger when the participant rather than their partner had made the choice, which fits an operational definition of guilt. This guilt effect was associated with BOLD signal increase in the left anterior insula. Connectivity between this region and the right inferior frontal gyrus varied depending on choice and experimental condition, suggesting that this part of prefrontal cortex is sensitive to guilt-related information during social choices. Variations in happiness were well explained by computational models based on participants' and partners' rewards and reward prediction errors. A model-based analysis revealed a left superior temporal sulcus cluster that tracked partner reward prediction errors that followed participant choices. Our findings identify neural mechanisms of guilt and social responsibility during social decisions under risk.

**Key methodological note:** The "partner" was in fact an expected-value-maximizing algorithm; participants were not informed (see `partner-algorithm-deception-assumption.md`).

## Hypotheses (top-level theoretical bets)

| Slug | Role | Epistemic | Summary |
|:-----|:-----|:----------|:--------|
| [hypothesis-insula-tracks-interpersonal-guilt](hypothesis-insula-tracks-interpersonal-guilt.md) | hypothesis | hypothesis | Anterior insula encodes interpersonal guilt — responsibility-contingent affect after self-caused partner harm |
| [hypothesis-responsibility-weights-partner-rpes](hypothesis-responsibility-weights-partner-rpes.md) | hypothesis | hypothesis | Happiness incorporates partner RPEs with a responsibility-weighted rule; partner RPEs caused by participant choice carry independent non-zero weight |
| [hypothesis-sts-mentalizes-partner-state-under-responsibility](hypothesis-sts-mentalizes-partner-state-under-responsibility.md) | hypothesis | hypothesis | STS represents partner experiential state via partner RPEs, conditional on participant responsibility |

## Predictions (derived from hypotheses)

| Slug | Derived from | Epistemic | Summary |
|:-----|:-------------|:----------|:--------|
| [prediction-behavioral-guilt-effect](prediction-behavioral-guilt-effect.md) | insula-guilt; responsibility-rpe | prediction | Happiness drops more after low partner outcomes when participant chose (Social > Partner condition × outcome interaction) |
| [prediction-insula-tracks-guilt](prediction-insula-tracks-guilt.md) | insula-guilt | prediction | Anterior insula BOLD elevated for Social > Partner specifically after negative partner outcomes (SVC over a priori ROI) |
| [prediction-responsibility-model-wins-comparison](prediction-responsibility-model-wins-comparison.md) | responsibility-rpe | prediction | Responsibility model with social_pRPE term outperforms nested alternatives; social_pRPE weight > 0 in both studies |
| [prediction-sts-tracks-partner-rpe-under-responsibility](prediction-sts-tracks-partner-rpe-under-responsibility.md) | sts-mentalizing | prediction | Left STS tracks partner RPEs in Social trials but not in Partner trials (conditional engagement) |

## Empirical claims

| Slug | Panel | Role | Epistemic | Summary |
|:-----|:------|:-----|:----------|:--------|
| [lottery-choice-increases-with-ev](lottery-choice-increases-with-ev.md) | fig2a,d | control | strong | EV drives lottery choice in both studies (manipulation check) |
| [solo-vs-social-choice-difference](solo-vs-social-choice-difference.md) | fig2a | empirical | moderate | Social context reduces lottery choice vs Solo in Study 1 only; null in Study 2 |
| [risk-premiums-null-social-solo](risk-premiums-null-social-solo.md) | fig2b,e | control | strong | Risk premiums do not differ between Solo and Social conditions in either study |
| [happiness-correlates-partner-reward](happiness-correlates-partner-reward.md) | fig3a,b,e,f | empirical | strong | Happiness correlates with both own reward (R²≈0.16–0.20) and partner reward (R²≈0.05–0.06) |
| [responsibility-modulates-guilt-computational](responsibility-modulates-guilt-computational.md) | fig3, table1 | empirical | moderate | Responsibility model with partner RPE regressors outperforms all other models |
| [social-prpe-weight-positive](social-prpe-weight-positive.md) | fig3c,g | empirical | strong | social_pRPE weight significantly > 0 in both models and both studies |
| [guilt-reduces-happiness-after-partner-loss](guilt-reduces-happiness-after-partner-loss.md) | fig3d,h | empirical | strong | Happiness decreases more after negative partner outcomes in Social vs Partner condition |
| [guilt-effect-independent-of-own-outcome](guilt-effect-independent-of-own-outcome.md) | fig3d,h | control | strong | Guilt effect present regardless of whether participant won or lost own outcome |
| [agency-reduces-happiness](agency-reduces-happiness.md) | fig3 (text) | empirical | strong | Being the decision-maker reduces happiness independently of outcome |
| [ventral-striatum-tracks-risky-choices](ventral-striatum-tracks-risky-choices.md) | fig4a | control | strong | Bilateral ventral striatum active for risky > safe choices (replication) |
| [precuneus-tpj-mpfc-social-decisions](precuneus-tpj-mpfc-social-decisions.md) | fig4b | empirical | strong | Precuneus, left TPJ, mPFC more active Social > Solo at decision time |
| [insula-tracks-guilt-effect](insula-tracks-guilt-effect.md) | fig4e,f | empirical | strong | Anterior insula elevated in Social vs Partner after negative partner outcomes |
| [ventral-striatum-tracks-computational-reward](ventral-striatum-tracks-computational-reward.md) | fig4g | control | strong | Ventral striatum tracks model-based reward regressors (manipulation check for GLM2) |
| [sts-tracks-partner-reward-prediction-errors](sts-tracks-partner-reward-prediction-errors.md) | fig4h | empirical | moderate | Left STS tracks partner RPE specifically when participant is responsible |
| [insula-ifg-connectivity-guilt](insula-ifg-connectivity-guilt.md) | fig5 | empirical | moderate | Right IFG–left insula gPPI connectivity varies by condition × choice |
| [insula-guilt-replicates-yu-koban-signature](insula-guilt-replicates-yu-koban-signature.md) | fig4 supp | interpretation | moderate | Insula guilt activation pattern consistent with published neural guilt signature (group level) |
| [guilt-signature-no-individual-difference](guilt-signature-no-individual-difference.md) | fig4 supp | empirical | moderate | Guilt signature dot products do not correlate with individual behavioral guilt effect |

## Assessment claims (structural/scope)

| Slug | Panel | Role | Epistemic | Summary |
|:-----|:------|:-----|:----------|:--------|
| [partner-algorithm-deception-assumption](partner-algorithm-deception-assumption.md) | ~ | scope | weak | Partner decisions made by EV-maximizing algorithm, not real person (structural assumption all social claims inherit) |
| [scope-two-study-design](scope-two-study-design.md) | ~ | scope | weak | Two-study design (fMRI N=40, behavioural N=44); neural claims Study 1 only; behavioural claims tested in both |

## Role distribution

| Role | Count |
|:-----|------:|
| hypothesis | 3 |
| prediction | 4 |
| empirical | 11 |
| control | 5 |
| interpretation | 1 |
| scope | 2 |
| **total** | **26** |

## Edge inventory (enriched schema)

| Edge type | Count | Notes |
|:----------|------:|:------|
| entails (hypothesis → prediction) | 5 | Each hypothesis entails 1–2 predictions |
| derived-from (prediction → hypothesis) | 5 | Inverse of entails; behavioral-guilt-effect derives from two hypotheses |
| tests (empirical → prediction) | 5 | Direct empirical tests of predictions |
| confirms (empirical/interpretation → hypothesis) | 6 | Empirical confirmations of hypotheses |
| validates (control → empirical/hypothesis) | 13 | Manipulation checks and methodological prerequisites |
| dissociates-with | 4 | Independent or contrasting effects (own-outcome, agency, individual differences) |
| rules-out | 1 | Risk-premium null rules out the choice-rate alternative explanation |
| interprets (interpretation/synthesis → empirical) | 3 | Yu/Koban convergent validity, IFG–insula connectivity |
| enables-method | 2 | Responsibility model fitting enables STS and ventral-striatum model-based analyses |
| scopes (scope/methodological → empirical) | 29 | Two scope claims govern all empirical claims (16 from each scope claim, minus overlap) |

## Extraction notes

**Method:** Triplicate extraction — Pass A (Results prose), Pass B (figure captions panel-by-panel), Pass C (Methods + code structure). Reconciled by confidence: high = all three agree; contested = two agree; single-source = one source only.

**Migration to enriched schema (2026-04-20):** Added three top-level hypotheses (insula-tracks-guilt, responsibility-weights-partner-rpes, sts-mentalizes-under-responsibility) and four predictions derived from them; added scope claim covering the two-study design. Annotated all 18 prior claims with `role:` and at least one new-schema edge. The enrichment makes explicit the central feature of this paper's argument structure — the convergence of behavioral, computational, and neural evidence on a single anatomical claim about anterior insula — by representing the insula-guilt hypothesis as the sink of multiple converging chains: behavioral test (`prediction-behavioral-guilt-effect`), computational test (`prediction-responsibility-model-wins-comparison`), neural test (`prediction-insula-tracks-guilt`), and convergent-validity test (`insula-guilt-replicates-yu-koban-signature`).

## Reproduction status

2026-03-30, agent: mainen-z. Deposited CSVs, pre-computed LMM tables, and NIfTI files enable Python verification of all five priority claims without MATLAB.

| Status | Count | Claims |
|:-------|:------|:-------|
| verified | 5 | happiness-correlates-partner-reward, guilt-reduces-happiness-after-partner-loss, insula-tracks-guilt-effect, partner-algorithm-deception-assumption, scope-two-study-design |
| verified:partial | 2 | lottery-choice-increases-with-ev (direction/significance confirmed; coefficient scale differs from paper due to predictor definition), insula-guilt-replicates-yu-koban-signature (nonparametric p<0.05; t-test marginal p=0.07) |
| unverified (incl. hypotheses/predictions, N/A) | 19 | Remaining empirical/control claims plus all hypothesis/prediction nodes (the latter are not the kind of claim that admits direct reproduction) |

### Session 2026-03-30 verification summary (Python, deposited data)

| Claim | Our result | Paper reports | Match? |
|:------|:-----------|:--------------|:-------|
| lottery-choice-increases-with-ev | fMRI β=0.116 p<1e-137; Behav β=0.088 p<1e-143 | fMRI β=0.093; Behav β=0.074 (mixed-effects LMM) | Direction/sig ✓; β scale differs (predictor definition) |
| happiness-correlates-partner-reward | fMRI R²=0.185, β(partner)=0.16*; Behav R²=0.147, β(partner)=0.21*** | fMRI R²=0.185; Behav R²=0.147 | Exact match ✓ |
| guilt-reduces-happiness-after-partner-loss | partnerWon:subjDecided β=0.33** (fMRI), 0.39*** (Behav) | Significant guilt effect in both studies | Match ✓ |
| insula-tracks-guilt-effect | Peak MNI=[-28, 24, -4] | Peak MNI=[-28, 24, -4] | Exact match ✓ |
| insula-guilt-replicates-yu-koban-signature | Dot products: sign test p=0.017, Wilcoxon p=0.042, t-test p=0.071 | Significant (sign test/median) | Nonparametric ✓; t borderline |

**Key risk:** Remaining empirical claims require MATLAB + SPM12. Pre-computed NIfTI files are present for fMRI claims.
