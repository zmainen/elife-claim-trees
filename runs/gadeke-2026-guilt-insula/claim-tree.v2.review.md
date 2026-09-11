# Gädeke 2026 — claim-tree v2 for adjudication

This is the document a person reads to approve **claim-tree v2** of `gadeke-2026-guilt-insula` — and, having read it, records that approval with:

    python3 scripts/pipeline.py approve gadeke-2026-guilt-insula claim-tree --by "<name>"

74 claims in `claims/gadeke-2026-guilt-insula/`. For each: is the claim true to the paper, is the role right, is the panel right, and is each relation right in type and direction? Mark each line ✓ / ✗ / ? and note why; the vocabulary is `extract/prompts/contract/vocabulary.md`.

| # | Slug | Role | Type | Panel | Stance |
|--:|:--|:--|:--|:--|:--|
| 1 | `alt-agency-aversion-not-guilt` | hypothesis | interpretive | — | rejects |
| 2 | `alt-guilt-effect-driven-by-own-outcome` | hypothesis | interpretive | — | rejects |
| 3 | `alt-imaging-contrast-invalid` | hypothesis | interpretive | — | rejects |
| 4 | `alt-model-based-glm-invalid` | hypothesis | interpretive | — | rejects |
| 5 | `alt-participants-insensitive-to-value` | hypothesis | interpretive | — | rejects |
| 6 | `alt-social-context-shifts-risk-attitude` | hypothesis | interpretive | — | rejects |
| 7 | `anterior-insula-neural-substrate-guilt` | hypothesis | hypothesis | — | asserts |
| 8 | `functional-connectivity-between-guilt-responsibility-related` | hypothesis | hypothesis | — | asserts |
| 9 | `neural-substrate-tracks-participant-responsibility` | hypothesis | hypothesis | — | asserts |
| 10 | `responsibility-social-choice-yields-low` | hypothesis | hypothesis | — | asserts |
| 11 | `anterior-insula-tracks-guilt-insula` | prediction | prediction | — | asserts |
| 12 | `connectivity-between-guilt-responsibility-related-outcome-ph` | prediction | prediction | — | asserts |
| 13 | `neural-substrate-tracks-participant-responsibility-2` | prediction | prediction | — | asserts |
| 14 | `responsibility-outcomes-generates-guilt-participant` | prediction | prediction | — | asserts |
| 15 | `responsibility-partner-outcomes-influences-participant` | prediction | prediction | — | asserts |
| 16 | `decisions-social-compared-solo-condition` | empirical | empirical | fig4b | asserts |
| 17 | `difference-response-between-low-high` | empirical | empirical | app1table10 | asserts |
| 18 | `during-outcome-phase-responses-low` | empirical | empirical | app1table9 | asserts |
| 19 | `during-receipt-lottery-versus-safe` | empirical | empirical | fig4d | asserts |
| 20 | `functional-connectivity-between-left-anterior` | empirical | empirical | fig5 | asserts |
| 21 | `insula-rois-responded-more-low` | empirical | empirical | fig4e | asserts |
| 22 | `left-ifg-cluster-showed-opposite` | empirical | empirical | fig5s1 | asserts |
| 23 | `left-superior-temporal-sulcus-cluster` | empirical | empirical | fig4i | asserts |
| 24 | `likelihood-ratio-test-showed-responsibility` | empirical | empirical | table1 | asserts |
| 25 | `mass-univariate-voxel-wise-analysis-found-small` | empirical | empirical | fig4f | asserts |
| 26 | `mixed-effects-regressions-choices-social-condition` | empirical | empirical | app1table1 | asserts |
| 27 | `one-cluster-left-sts-responded` | empirical | empirical | fig4h | asserts |
| 28 | `only-precuneus-tpj-showed-positive` | empirical | empirical | fig4c | asserts |
| 29 | `participant-happiness-lower-when-participant` | empirical | empirical | — | asserts |
| 30 | `participant-momentary-happiness-varied-rewards` | empirical | empirical | fig3a,fig3e | asserts |
| 31 | `participant-momentary-happiness-varied-rewards-2` | empirical | empirical | fig3b,fig3f | asserts |
| 32 | `participants-chose-risky-option-lottery` | empirical | empirical | fig2a,fig2d | asserts |
| 33 | `participants-own-reward-prediction-errors` | empirical | empirical | — | asserts |
| 34 | `participants-slightly-more-risk-averse` | empirical | empirical | fig2c,fig2f | asserts |
| 35 | `partner-reward-prediction-errors-resulting` | empirical | empirical | — | asserts |
| 36 | `responsibility-model-yielded-higher-values` | empirical | empirical | table1 | asserts |
| 37 | `responsibility-redux-model-incorporating-expected` | empirical | empirical | fig3c,fig3g | asserts |
| 38 | `when-partner-received-low-lottery` | empirical | empirical | fig3d,fig3h | asserts |
| 39 | `bilateral-ventral-striatum-more-active` | control | empirical | fig4a | asserts |
| 40 | `dot-products-between-individual-neural` | control | empirical | — | asserts |
| 41 | `guilt-effect-occurred-whether-participant` | control | empirical | — | asserts |
| 42 | `individual-grbs-dot-product-values-not` | control | empirical | — | asserts |
| 43 | `manipulation-check-bilateral-ventral-striatum` | control | empirical | fig4g | asserts |
| 44 | `no-significant-interaction-between-difference` | control | empirical | — | asserts |
| 45 | `participants-probability-choosing-risky-option` | control | empirical | fig2a,fig2d | asserts |
| 46 | `pre-task-icebreaker-succeeded-establishing-positive` | control | empirical | app1table11 | asserts |
| 47 | `responsibility-choices-not-influence-happiness` | control | empirical | — | asserts |
| 48 | `risk-aversion-parameter-not-differ-between` | control | empirical | — | asserts |
| 49 | `risk-premiums-not-differ-between` | control | empirical | fig2b,fig2e | asserts |
| 50 | `all-reported-clusters-survive-whole-brain` | methodological | assessment | — | asserts |
| 51 | `among-computational-models-fitted-momentary` | methodological | assessment | table1 | asserts |
| 52 | `happiness-ratings-z-scored-per-participant` | methodological | assessment | — | asserts |
| 53 | `hold-partner-behaviour-constant-across` | methodological | assessment | — | asserts |
| 54 | `linear-mixed-model-containing-all` | methodological | assessment | app1table2 | asserts |
| 55 | `model-based-glm-entered-best-fitting-computational` | methodological | assessment | — | asserts |
| 56 | `model-selection-among-happiness-models` | methodological | assessment | — | asserts |
| 57 | `momentary-happiness-modelled-five-computational` | methodological | assessment | — | asserts |
| 58 | `parameter-recovery-procedure-synthetic-data-generated` | methodological | assessment | fig3s1 | asserts |
| 59 | `risk-attitude-quantified-risk-premium` | methodological | assessment | — | asserts |
| 60 | `study-sample-size-fixed-priori` | methodological | assessment | — | asserts |
| 61 | `two-gppi-seed-to-voxel-connectivity-analyses` | methodological | assessment | — | asserts |
| 62 | `each-trial-participants-chose-between` | scope | assessment | — | asserts |
| 63 | `findings-rest-two-samples-healthy` | scope | assessment | — | asserts |
| 64 | `fmri-data-four-study-participants` | scope | assessment | — | asserts |
| 65 | `study-reproduced-study-design-inside` | scope | assessment | — | asserts |
| 66 | `both-studies-participants-felt-worse` | synthesis | synthesis | — | asserts |
| 67 | `participants-showed-very-similar-risk` | synthesis | synthesis | — | asserts |
| 68 | `authors-suggest-left-sts-region` | interpretation | interpretive | — | asserts |
| 69 | `behavioural-guilt-effect-larger-happiness` | interpretation | interpretive | — | asserts |
| 70 | `connectivity-between-left-anterior-insula` | interpretation | interpretive | — | asserts |
| 71 | `lower-happiness-when-participant-decision-maker` | interpretation | interpretive | — | asserts |
| 72 | `prior-functional-connectivity-work-shown` | literature-context | interpretive | — | asserts |
| 73 | `prior-literature-documents-association-between` | literature-context | interpretive | — | asserts |
| 74 | `rutledge-colleagues-established-changes-momentary` | literature-context | interpretive | — | asserts |

## 1. `alt-agency-aversion-not-guilt`

**hypothesis** · type `interpretive` · panel `—` · epistemic `weak` · stance `rejects`

> The happiness cost observed in the Social condition is general agency aversion — the unpleasantness of being the decision-maker as such — and is not contingent on responsibility for a negative outcome befalling the partner.

Relations: none

Method: agent extraction of the alternative addressed by the paper's outcome-independent agency analysis  

An alternative explanation the paper argues against, not a proposition it asserts, and the one
most easily confused with the paper's own hypothesis.

The paper does not deny that agency depresses happiness — `agency-reduces-happiness` asserts
exactly that, independently of outcome. What it denies is that agency is the *whole* story. The
guilt effect is an interaction: happiness falls further when the participant's choice produced a
bad outcome *for the partner*. A pure agency-aversion account predicts a main effect and no such
interaction.

This is why `agency-reduces-happiness` both supports the guilt claim and rules this rival out.
Establishing the main effect is what makes the residual interaction interpretable as something
else.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 2. `alt-guilt-effect-driven-by-own-outcome`

**hypothesis** · type `interpretive` · panel `—` · epistemic `weak` · stance `rejects`

> The happiness decrease following negative partner outcomes under participant choice is driven by the participant's own lottery outcome rather than by the partner's, and so reflects self-directed disappointment rather than interpersonal guilt.

Relations: none

Method: agent extraction of the alternative named in the paper's control analysis  

An alternative explanation the paper argues against, not a proposition it asserts.

It is the sharpest confound available to a within-subject lottery design in which both parties
receive outcomes: a participant who has just lost may report lower happiness for reasons that
have nothing to do with the partner. `guilt-effect-independent-of-own-outcome` closes it by
showing the effect holds at both levels of the participant's own outcome, with Bayes factors
between 3.8 and 33.5 across the four cells.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 3. `alt-imaging-contrast-invalid`

**hypothesis** · type `interpretive` · panel `—` · epistemic `weak` · stance `rejects`

> The imaging pipeline and condition contrasts do not recover established effects, so differences reported between Social and Partner conditions cannot be attributed to the experimental manipulation.

Relations: none

Method: agent extraction of the validity threat addressed by the paper's replication check  

A threat to validity rather than a rival explanation — see the design note for why these are
held apart from scientific alternatives.

`ventral-striatum-tracks-risky-choices` closes it by replicating an established striatal
response to risky choice (d = 0.72 and 0.85) irrespective of condition. A pipeline that
recovers a known effect is not thereby correct, but one that fails to would undercut every
contrast the paper reports.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 4. `alt-model-based-glm-invalid`

**hypothesis** · type `interpretive` · panel `—` · epistemic `weak` · stance `rejects`

> The model-based fMRI approach does not recover known neural signals, so parametric modulators derived from the computational model — including the partner reward prediction error regressors — cannot be trusted.

Relations: none

Method: agent extraction of the validity threat named in the paper's manipulation check  

A threat to validity rather than a rival explanation — see
`alt-participants-insensitive-to-value` and the design note for why these are held apart.

`ventral-striatum-tracks-computational-reward` closes it, and says so in its own text:
bilateral ventral striatum tracks the model's expected values, "validating the model-based fMRI
approach as a manipulation check before the STS analysis." That sentence is the paper naming
what it is ruling out; before this claim existed, the graph had nowhere to put it.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 5. `alt-participants-insensitive-to-value`

**hypothesis** · type `interpretive` · panel `—` · epistemic `weak` · stance `rejects`

> Participants did not engage with the lottery task in a value-sensitive way — choices were inattentive or random — so the behavioural measures carry no information about preference or affect.

Relations: none

Method: agent extraction of the validity threat addressed by the paper's manipulation check  

A threat to validity rather than a rival explanation of guilt, and it is recorded separately
for that reason. It is not a competing account of the phenomenon; it is the possibility that
there is no phenomenon to account for.

Whether such preconditions belong as alternatives with `rules-out`, or as assessment claims
with `requires` (`docs/claim-format.md` §5), is open — see the design note
`docs/design/2026-09-10-stance-and-alternative-claims.md`. Recorded here as an alternative so
that `lottery-choice-increases-with-ev` has a target, and flagged for review.

The paper closes it by showing lottery choice probability rises with expected-value advantage
in both studies (p < 3.1e-20 and p < 5.3e-26).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 6. `alt-social-context-shifts-risk-attitude`

**hypothesis** · type `interpretive` · panel `—` · epistemic `weak` · stance `rejects`

> The happiness and choice differences between Social and Partner conditions reflect a social-context-driven shift in risk attitude — participants become more or less risk averse when choosing on another person's behalf — rather than responsibility-contingent interpersonal guilt.

Relations: none

Method: agent extraction of the alternative named in the paper's control analysis  

An alternative explanation the paper argues against, not a proposition it asserts. It is
recorded here so that `risk-premiums-null-social-solo` has something to rule out; before this
claim existed, that control's `rules-out` relation pointed at `solo-vs-social-choice-difference`
— a finding the paper does assert — which made the graph report a contradiction the paper does
not make.

The rival matters because it is the obvious deflationary reading of the whole paradigm: if
social context simply moves risk preference, then the Social-versus-Partner contrast is not
about guilt at all, and every downstream fMRI contrast is confounded. The paper closes it with
matched risk premiums across conditions in both studies, with Bayes factors favouring the null
(BF10 = 0.49 and 0.17).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 7. `anterior-insula-neural-substrate-guilt`

**hypothesis** · type `hypothesis` · panel `—` · epistemic `hypothesis` · stance `asserts`

> The anterior insula is the neural substrate of the guilt effect, increasing its BOLD response when participants are responsible for low outcomes affecting their partner.

Relations: `entails` → `anterior-insula-tracks-guilt-insula`


**Notes from extraction:** The insula-as-guilt-substrate proposition the paper pursues given prior literature; stated as an aim and later as a result rather than as an explicit hypothesis.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Next, we sought to uncover the neural mechanisms associated with our guilt effect and those involved in tracking consequences of participants’ decisions on their partner.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 8. `functional-connectivity-between-guilt-responsibility-related`

**hypothesis** · type `hypothesis` · panel `—` · epistemic `hypothesis` · stance `asserts`

> Functional connectivity between guilt- and responsibility-related outcome-phase regions and prefrontal cortex changes depending on whether participants decide for themselves alone or also for their partner, and on the type of choice (Safe or Risky).

Relations: `entails` → `connectivity-between-guilt-responsibility-related-outcome-ph`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We hypothesized that connectivity with regions that showed guilt- and responsibility-related responses during the outcome phase (see previous paragraph) might change depending on whether participants made decisions for themselves only or for themselves and their partner, and depending on the type of choice (Safe or Risky).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 9. `neural-substrate-tracks-participant-responsibility`

**hypothesis** · type `hypothesis` · panel `—` · epistemic `hypothesis` · stance `asserts`

> A neural substrate tracks the participant's responsibility for the partner's outcomes: within regions sensitive to choice outcomes, the partner's reward prediction errors are represented more strongly when they arise from the participant's own choice than from the partner's choice.

Relations: `entails` → `neural-substrate-tracks-participant-responsibility-2`


**Notes from extraction:** [reviewer] added: the paper's second organizing proposition, parallel to the insula/guilt hypothesis and named alongside it in the title and abstract - a neural substrate tracking the participant's responsibility for the partner (partner reward prediction errors arising from the participant's own choices). The results reader surfaced only the empirical STS result, not the hypothesis it tests.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**reviewer-reader evidence:**
> Inferred from the paper's second stated aim ('Next, we sought to uncover the neural mechanisms associated with our guilt effect and those involved in tracking consequences of participants' decisions on their partner'), from the abstract's model-based STS finding, and from the title's pairing of the superior temporal sulcus with 'responsibility'. The draft carried the STS test (fig4h) and its interpretation but not the proposition they test.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 10. `responsibility-social-choice-yields-low`

**hypothesis** · type `hypothesis` · panel `—` · epistemic `hypothesis` · stance `asserts`

> Responsibility for a social choice that yields a low outcome for a partner produces interpersonal guilt, experienced by the decision-maker as a larger decrease in momentary happiness than when the partner made the same choice.

Relations: `entails` → `responsibility-outcomes-generates-guilt-participant`; `entails` → `responsibility-partner-outcomes-influences-participant`


**Notes from extraction:** The paper's guiding proposition, framed via the research aim and the operational definition of guilt rather than an explicit 'we hypothesize' statement. Only the results reader could surface a hypothesis; single-source is expected.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> This study investigated the neural mechanisms involved in feelings of interpersonal guilt and responsibility evoked by social decisions in humans.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 11. `anterior-insula-tracks-guilt-insula`

**prediction** · type `prediction` · panel `—` · epistemic `prediction` · stance `asserts`

> If the anterior insula tracks guilt, then insula BOLD should be higher in the Social than the Partner condition and show a significant Social-by-low-outcome interaction.

Relations: `derived-from` → `anterior-insula-neural-substrate-guilt`


**Notes from extraction:** Phrased as the prediction the insula hypothesis commits the paper to; the text states it as the region-selection criteria.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> To identify regions likely to be involved in the guilt effect, we selected those satisfying two conditions: higher activity in the Social compared to the Partner condition, and a significant Social:LowOutcome interaction.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 12. `connectivity-between-guilt-responsibility-related-outcome-ph`

**prediction** · type `prediction` · panel `—` · epistemic `prediction` · stance `asserts`

> If connectivity between the guilt- and responsibility-related outcome-phase regions (left insula, left STS) and prefrontal cortex depends on whether participants decide for themselves alone or also for their partner and on the type of choice, then a seed-to-voxel psychophysiological-interaction analysis seeded in these regions should reveal prefrontal clusters showing a significant Condition-by-Choice interaction.

Relations: `derived-from` → `functional-connectivity-between-guilt-responsibility-related`


**Notes from extraction:** [reviewer] added: the observable the connectivity hypothesis commits the paper to; tested by the insula-IFG and STS-IFG PPI results.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**reviewer-reader evidence:**
> Deduced from the connectivity hypothesis ('We hypothesized that connectivity with regions that showed guilt- and responsibility-related responses during the outcome phase might change depending on whether participants made decisions for themselves only or for themselves and their partner, and depending on the type of choice'); the paper then runs seed-to-voxel PPI analyses 'to search for connectivity changes, during the choice phase of the trial, as a function of Condition and Choice'. The draft carried the connectivity hypothesis and its tests (fig5, fig5s1) but not the prediction linking them.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 13. `neural-substrate-tracks-participant-responsibility-2`

**prediction** · type `prediction` · panel `—` · epistemic `prediction` · stance `asserts`

> If a neural substrate tracks the participant's responsibility for the partner's outcomes, then within regions sensitive to the outcomes of risky choices, BOLD should respond more strongly to the partner's reward prediction errors resulting from the participant's own choices than from the partner's choices.

Relations: `derived-from` → `neural-substrate-tracks-participant-responsibility`


**Notes from extraction:** [reviewer] added: the conditional the responsibility-tracking hypothesis commits the paper to, tested by the left-STS model-based result; kept distinct from that empirical result.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**reviewer-reader evidence:**
> Deduced from the responsibility-tracking hypothesis; the paper states the corresponding search directly ('we thus used this model to search for voxels responding more to partner reward prediction errors resulting from participant rather than partner choices, within the regions sensitive to outcomes of risky choices'). The draft carries the result (left STS, fig4h) but not the prediction it tests.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 14. `responsibility-outcomes-generates-guilt-participant`

**prediction** · type `prediction` · panel `—` · epistemic `prediction` · stance `asserts`

> If responsibility for outcomes generates guilt, then participant happiness should decrease more after low lottery outcomes for the partner when the participant rather than the partner chose the lottery.

Relations: `derived-from` → `responsibility-social-choice-yields-low`


**Notes from extraction:** The conditional deduced from the guilt hypothesis; the paper states it as an operational definition and then tests it. Kept distinct from the result that tests it (the guilt-effect interaction).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> In our definition, guilt occurs due to responsibility for low lottery outcomes for the partner.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 15. `responsibility-partner-outcomes-influences-participant`

**prediction** · type `prediction` · panel `—` · epistemic `prediction` · stance `asserts`

> If responsibility for the partner's outcomes influences the participant's momentary happiness, then a computational model that includes the partner's reward prediction errors arising from the participant's own choices (social_pRPE) should explain the happiness data better than models omitting them, and social_pRPE weights should be reliably greater than zero.

Relations: `derived-from` → `responsibility-social-choice-yields-low`


**Notes from extraction:** [reviewer] added: the computational-route prediction the behavioural guilt/responsibility hypothesis commits the paper to, tested by the model comparison (Responsibility / Responsibility Redux best fit) and by the positive social_pRPE weights; kept distinct from the behavioural happiness-comparison prediction.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**reviewer-reader evidence:**
> Deduced from the guilt/responsibility hypothesis and the stated modelling aim ('we aimed to assess whether responsibility for these rewards, that is, taking into account whether the rewards occurred following choices made by the participant or the partner, would also influence variations in happiness'). The draft carried the tests - the Responsibility model's superior fit and the greater-than-zero social_pRPE weights - but not the prediction that motivates the computational analysis.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 16. `decisions-social-compared-solo-condition`

**empirical** · type `empirical` · panel `fig4b` · epistemic `tentative` · stance `asserts`

> Decisions in the Social compared with the Solo condition engaged three clusters — the precuneus (d = 0.79), left temporo-parietal junction (d = 0.59), and medial prefrontal cortex (d = 0.54).

Relations: `requires` → `all-reported-clusters-survive-whole-brain`

Reproductions: 2 record(s) (carried from `precuneus-tpj-mpfc-social-decisions`)  

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Three significant clusters of voxels were identified (Figure 4B and Appendix 1—table 3), in the precuneus (d = 0.79), the left temporo-parietal junction (TPJ; d = 0.59) and the medial prefrontal cortex (mPFC; d = 0.54).

**caption-reader evidence:**
> ( B ) Regions showing a greater response when participants chose for both themselves and their partner rather than just for themselves (Social > Solo).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 17. `difference-response-between-low-high`

**empirical** · type `empirical` · panel `app1table10` · epistemic `tentative` · stance `asserts`

> The difference in response between low and high lottery outcomes was greater in the Social than the Partner condition in left insula (0.44***), right insula (0.19***), and right middle temporal cortex (0.67***).

Relations: `supports` → `insula-rois-responded-more-low`


**Notes from extraction:** Columns are InsulaL (0.44***), InsulaR (0.19***) and MidTempR (0.67***). Table-level breakdown supplementing the fig4e insula ROI result; kept separate by panel.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> Social 0.44*** 0.19*** 0.67***

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 18. `during-outcome-phase-responses-low`

**empirical** · type `empirical` · panel `app1table9` · epistemic `tentative` · stance `asserts`

> During the outcome phase, responses to low lottery outcomes were higher in the Social than the Partner condition in both left and right insula (InsulaL 0.41***, InsulaR 0.18***) and lower in the right middle temporal cortex (–0.12**).

Relations: `supports` → `insula-rois-responded-more-low`


**Notes from extraction:** Columns are InsulaL (0.41***), InsulaR (0.18***) and MidTempR (–0.12**). Table-level breakdown supplementing the fig4e insula ROI result; kept separate by panel and by the added middle-temporal region.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> Social 0.41*** 0.18*** –0.12**

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 19. `during-receipt-lottery-versus-safe`

**empirical** · type `empirical` · panel `fig4d` · epistemic `tentative` · stance `asserts`

> During receipt of lottery versus safe outcomes (across all conditions), clusters were more active in the bilateral anterior insula, dmPFC, right STS, bilateral ventral striatum, right dorsolateral prefrontal cortex, and bilateral inferior parietal lobe.

Relations: `requires` → `all-reported-clusters-survive-whole-brain`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> A cluster of voxels more active during receipt of lottery outcomes than outcomes of safe choices was identified in the bilateral anterior insula, dorsal mPFC (dmPFC), right superior temporal sulcus (STS), bilateral ventral striatum, right dorsolateral prefrontal cortex, and bilateral inferior parietal lobe (Figure 4D).

**caption-reader evidence:**
> ( D ) Brain regions more active during receipt of the outcomes of lotteries than safe choices (all conditions).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 20. `functional-connectivity-between-left-anterior`

**empirical** · type `empirical` · panel `fig5` · epistemic `tentative` · stance `asserts`

> Functional connectivity between the left anterior insula (seed) and a cluster in the right inferior frontal gyrus varied with condition and choice, being highest when participants made Risky choices for themselves and Safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, 115 voxels, peak MNI [46 16 22]).

Relations: `tests` → `connectivity-between-guilt-responsibility-related-outcome-ph`; `requires` → `two-gppi-seed-to-voxel-connectivity-analyses`; `requires` → `all-reported-clusters-survive-whole-brain`


**Notes from extraction:** The caption reader (tentative) stated the analysis but not the direction; the results reader supplied the direction and statistics.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The first analysis revealed a cluster in the right IFG whose connectivity to the insula (the seed region) was highest when participants made Risky choices for themselves and Safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, Z = 4.21, 115 voxels, peak at MNI [46 16 22]; Figure 5).

**caption-reader evidence:**
> Changes in functional connectivity between the left anterior insula (seed) and a cluster in the right inferior frontal gyrus at the time of the choice as a function of condition (Social vs. Solo) and choice (Risky or Safe).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 21. `insula-rois-responded-more-low`

**empirical** · type `empirical` · panel `fig4e` · epistemic `tentative` · stance `asserts`

> The insula ROIs responded more to low lottery outcomes for the partner in the Social than the Partner condition — even after subtracting responses to high outcomes — mirroring the behavioural guilt effect.

Relations: `tests` → `anterior-insula-tracks-guilt-insula`


**Notes from extraction:** Caption states all coefficients and differences are significantly different from 0 (see Appendix 1—table 6).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Thus, activation in our insula ROIs increased in situations during which participants experienced guilt for low outcomes impacting their partner, compared to similar outcomes resulting from the partner’s choices.

**caption-reader evidence:**
> voxels here responded more to low lottery outcomes (L) for the partner when these resulted from participant’s rather than the partner’s choices, even when responses to high outcomes were subtracted (L–H).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 22. `left-ifg-cluster-showed-opposite`

**empirical** · type `empirical` · panel `fig5s1` · epistemic `tentative` · stance `asserts`

> A left IFG cluster showed the opposite pattern of connectivity with the left STS seed — highest for Safe-self / Risky-both-players choices — but did not survive correction for multiple comparisons (p uncorrected = 0.001, T = 4.44, 35 voxels, peak MNI [–48 14 6]).

Relations: `tests` → `connectivity-between-guilt-responsibility-related-outcome-ph`; `requires` → `two-gppi-seed-to-voxel-connectivity-analyses`


**Notes from extraction:** Reported at an uncorrected threshold; did not survive multiple-comparison correction. The caption reader classified it as a control while the results reader classified it as empirical; both agree on panel and direction, resolved to empirical.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The second analysis revealed a smaller cluster in the left IFG that did not survive corrections for multiple tests, where connectivity with the left STS (the seed region) showed the opposite pattern: connectivity was highest when participants made Safe choices for themselves and Risky choices for both players (p uncorrected = 0.001, T = 4.44, Z = 4.30, 35 voxels, peak at MNI [–48 14 6]; Figure 5—figure supplement 1).

**caption-reader evidence:**
> connectivity was highest when participants made Safe choices for themselves and Risky choices for both players (p uncorrected  = 0.001,  T  = 4.44,  Z  = 4.30, 35 voxels, peak at MNI [–48 14 6]).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 23. `left-superior-temporal-sulcus-cluster`

**empirical** · type `empirical` · panel `fig4i` · epistemic `tentative` · stance `asserts`

> The left superior temporal sulcus cluster responded to model-based regressors coding participant reward prediction resulting from participant and partner choices across both sessions of the experiment.

Relations: `tests` → `neural-substrate-tracks-participant-responsibility-2`; `requires` → `model-based-glm-entered-best-fitting-computational`


**Notes from extraction:** Caption describes what is plotted (coefficients with 95% confidence intervals) rather than stating a directional result; the caption reader marked it tentative.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> ( I ) Response in this cluster to the computational-model-based regressors coding participant reward prediction resulting from participant and partner choices, for both sessions of the experiment.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 24. `likelihood-ratio-test-showed-responsibility`

**empirical** · type `empirical` · panel `table1` · epistemic `tentative` · stance `asserts`

> A likelihood ratio test showed the Responsibility model fitted the happiness data better than all other models, including the Responsibility Redux model (Study 1: all LR ≥ 47.36, p < 0.0001; Study 2: all LR ≥ 77.83, p < 0.0001).

Relations: `requires` → `momentary-happiness-modelled-five-computational`; `requires` → `model-selection-among-happiness-models`

Reproductions: 1 record(s) (carried from `responsibility-modulates-guilt-computational`)  

**Notes from extraction:** Kept separate from the R² comparison to preserve the results reader's distinct verbatim quote for each statistic.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> a likelihood ratio test (Equation 9) revealed that the Responsibility model fitted better than all the other models, including the Responsibility Redux model (Study 1: all LR ≥47.36, p < 0.0001; Study 2: all LR ≥77.83, p < 0.0001).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 25. `mass-univariate-voxel-wise-analysis-found-small`

**empirical** · type `empirical` · panel `fig4f` · epistemic `tentative` · stance `asserts`

> A mass-univariate voxel-wise analysis found a small left anterior insula cluster (peak T = 3.95, d = 0.59, 22 voxels) responding more to low partner outcomes following participant than partner choices, which survived small-volume family-wise-error correction (p = 0.024).

Relations: `tests` → `anterior-insula-tracks-guilt-insula`; `requires` → `all-reported-clusters-survive-whole-brain`

Reproductions: 2 record(s) (carried from `insula-tracks-guilt-effect`)  

**Notes from extraction:** The caption reader treated this as a control — convergent voxel-wise confirmation of the ROI-based insula guilt effect in panel E; the results reader treated it as the empirical voxel-wise guilt result. The small-volume FWE correction (p = 0.024) is reported in a following sentence by the results reader. Both are empirical measurements agreeing on panel and direction; resolved to empirical.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found a weak response in a small cluster within the left anterior insula (peak T = 3.95, d = 0.59, 22 voxels, peak intensity at [–28 24 –4]; Figure 4F).

**caption-reader evidence:**
> A cluster of voxels within the left insula ROI showed higher responses to low lottery outcomes for the partner if these resulted from participant rather than partner choices.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 26. `mixed-effects-regressions-choices-social-condition`

**empirical** · type `empirical` · panel `app1table1` · epistemic `tentative` · stance `asserts`

> In mixed-effects regressions on choices, the Social condition significantly increased choice of the risky option in Study 1 but not in Study 2.

Relations: none


**Notes from extraction:** Row values are Study 1 probit (0.14*), Study 1 linear (0.03^), Study 2 probit (0.01), Study 2 linear (0.01). This is the regression-table counterpart to the fig2a/fig2d proportion effect, which the results reader described as Solo > Social; the sign of the 'Social' coefficient depends on the regression's reference condition, so the two are kept separate by panel rather than merged.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> Condition Social 0.14* 0.03^ 0.01 0.01

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 27. `one-cluster-left-sts-responded`

**empirical** · type `empirical` · panel `fig4h` · epistemic `tentative` · stance `asserts`

> One cluster in the left STS responded more to partner reward prediction errors resulting from participant rather than partner choices (pFWE = 0.022, T = 4.70, d = 0.53, 100 voxels, peak MNI [−52 –32 0]).

Relations: `tests` → `neural-substrate-tracks-participant-responsibility-2`; `requires` → `model-based-glm-entered-best-fitting-computational`; `requires` → `all-reported-clusters-survive-whole-brain`

Reproductions: 2 record(s) (carried from `sts-tracks-partner-reward-prediction-errors`)  

**Notes from extraction:** Caption notes this is restricted to brain regions sensitive to outcomes of risky choices.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found this effect in one cluster within the left STS (pFWE = 0.022, T = 4.70, d = 0.53, Z = 4.57, 100 voxels, peak at MNI [−52 –32 0]; Figure 4H).

**caption-reader evidence:**
> one cluster in the left superior temporal sulcus region showed a higher response to partner reward prediction errors resulting from participant rather than partner choices.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 28. `only-precuneus-tpj-showed-positive`

**empirical** · type `empirical` · panel `fig4c` · epistemic `tentative` · stance `asserts`

> Only the precuneus and TPJ showed positive Risky–Safe differences in both the Social>Solo and Social>Partner comparisons, being most active when participants chose the lottery in the Social condition.

Relations: `requires` → `all-reported-clusters-survive-whole-brain`


**Notes from extraction:** Caption states all coefficients and differences are significantly different from 0 (see Appendix 1—table 4).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Only the precuneus and TPJ showed positive differences in both comparisons (Figure 4C), indicating that these regions were most active when participants chose the lottery in the Social condition, the critical situation in which participants assume responsibility over others.

**caption-reader evidence:**
> Coefficients of linear mixed models (LMMs) indicate that two of these regions, precuneus and TPJ, were most active when participants chose the lottery in the Social condition.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 29. `participant-happiness-lower-when-participant`

**empirical** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> Participant happiness was lower when the participant was the decision-maker (Social + Solo vs. Partner), independent of outcome (Study 1: t(3600) = –3.92, p < 0.0001, β = –0.14; Study 2: t(2870) = –6.07, p < 0.0001, β = –0.24).

Relations: `rules-out` → `alt-agency-aversion-not-guilt`

Reproductions: 2 record(s) (carried from `agency-reduces-happiness`)  

**Notes from extraction:** The agency effect on happiness, distinct from the guilt (partner-outcome-contingent) effect.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> we assessed whether happiness varied depending on the participant’s agency (Social + Solo vs. Partner), and found happiness to be lower when the participant chose, independent of the outcome (Study 1: t(3600) = –3.92, p < 0.0001, β = –0.14, 95% CI = [−0.20 to 0.07]; Study 2: t(2870) = –6.07, p < 0.0001, β = –0.24, 95% CI = [−0.31 to 0.16]).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 30. `participant-momentary-happiness-varied-rewards`

**empirical** · type `empirical` · panel `fig3a,fig3e` · epistemic `tentative` · stance `asserts`

> Participant momentary happiness varied with the rewards the participant received in the current trial.

Relations: `supports` → `responsibility-redux-model-incorporating-expected`


**Notes from extraction:** The results reader stated the participant- and partner-reward correlations jointly; the caption reader anchored the participant-reward correlation to fig3a/fig3e specifically, so it is split from the partner-reward claim by panel.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Across all trials, in both studies, participant momentary happiness correlated with rewards obtained in the current trial by the participant and by the partner.

**caption-reader evidence:**
> Happiness varied with rewards received by the participant ( A, E ) and by the partner ( B, F ).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 31. `participant-momentary-happiness-varied-rewards-2`

**empirical** · type `empirical` · panel `fig3b,fig3f` · epistemic `tentative` · stance `asserts`

> Participant momentary happiness varied with the rewards the partner received in the current trial.

Relations: `supports` → `responsibility-redux-model-incorporating-expected`

Reproductions: 2 record(s) (carried from `happiness-correlates-partner-reward`)  

**Notes from extraction:** The results reader stated the participant- and partner-reward correlations jointly; the caption reader anchored the partner-reward correlation to fig3b/fig3f specifically, so it is split from the participant-reward claim by panel.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Across all trials, in both studies, participant momentary happiness correlated with rewards obtained in the current trial by the participant and by the partner.

**caption-reader evidence:**
> Happiness varied with rewards received by the participant ( A, E ) and by the partner ( B, F ).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 32. `participants-chose-risky-option-lottery`

**empirical** · type `empirical` · panel `fig2a,fig2d` · epistemic `tentative` · stance `asserts`

> Participants chose the risky option (lottery) more often in the Solo than the Social condition in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164) but not in Study 2 (t(3829) = 0.23, p = 0.82, β = 0.015).

Relations: `supports` → `participants-showed-very-similar-risk`

Reproductions: 2 record(s) (carried from `solo-vs-social-choice-difference`)  

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Participants chose the lottery more often in the Solo condition than in the Social condition in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164, 95% CI = [0.038 0.291]), but this difference was not found in Study 2 (t(3829) = 0.23, p = 0.82, β = 0.015, 95% CI = [–0.109 0.138]).

**caption-reader evidence:**
> Participants chose the risky option slightly more often in the Solo condition than in the Social condition in Study 1 ( A ) but not in Study 2 ( D ).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 33. `participants-own-reward-prediction-errors`

**empirical** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> Participants' own reward prediction errors (sRPE) influenced happiness more than the partner's reward prediction errors (social_pRPE and partner_pRPE) (Study 1: all Z > 6.0, p < 0.001; Study 2: all Z > 3.7, p < 0.003).

Relations: `requires` → `momentary-happiness-modelled-five-computational`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> weights for sRPE were higher than for social_pRPE or partner_pRPE (Study 1: all Z > 6.0, p < 0.001; Study 2: all Z > 3.7, p < 0.003).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 34. `participants-slightly-more-risk-averse`

**empirical** · type `empirical` · panel `fig2c,fig2f` · epistemic `tentative` · stance `asserts`

> Participants were slightly more risk averse (higher ρ) in the Social than the Solo condition in Study 1 (t(39) = 2.27, p = 0.03, d = 0.36, BF10 = 1.69) but not in Study 2 (t(43) = 1.40, p = 0.17, d = 0.21, BF10 = 0.41).

Relations: `requires` → `risk-attitude-quantified-risk-premium`; `supports` → `participants-showed-very-similar-risk`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found that participants were slightly more risk averse in the Social than in the Solo condition in Study 1 (Figure 2C, t(39) = 2.27, p = 0.03, d = 0.36, BF10 = 1.69) but not in Study 2 (Figure 2F, t(43) = 1.40, p = 0.17, d = 0.21, BF10 = 0.41).

**caption-reader evidence:**
> Values of the risk aversion parameter ρ in the Solo and Social conditions were broadly consistent with Risk premium values, but showed that participants were slightly more risk averse in the Social than in the Solo condition in Study 1 only (see Results).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 35. `partner-reward-prediction-errors-resulting`

**empirical** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> The partner's reward prediction errors resulting from the participants' own choices (social_pRPE) had weights greater than 0 (Responsibility model: Study 1: Z = 2.85, p = 0.004; Study 2: Z = 3.26, p = 0.001), contributing to explaining participants' momentary happiness.

Relations: `tests` → `responsibility-partner-outcomes-influences-participant`; `requires` → `momentary-happiness-modelled-five-computational`; `supports` → `both-studies-participants-felt-worse`

Reproductions: 2 record(s) (carried from `social-prpe-weight-positive`)  

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> weights for social_pRPE were greater than 0: Responsibility model: Study 1: Z = 2.85, p = 0.004, Study 2: Z = 3.26, p = 0.001; ResponsibilityRedux model: Study 1: Z = 2.93, p = 0.003, Study 2: Z = 3.30, p = 0.001.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 36. `responsibility-model-yielded-higher-values`

**empirical** · type `empirical` · panel `table1` · epistemic `tentative` · stance `asserts`

> The Responsibility model yielded higher R² values than all other models (Study 1: all t > 3.6, p < 0.007; Study 2: all t > 2.9, p < 0.034), except the Guilt-envy model in Study 1 (t = 2.19, p = 0.17).

Relations: `requires` → `momentary-happiness-modelled-five-computational`; `supports` → `likelihood-ratio-test-showed-responsibility`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The Responsibility model yielded higher R2 values than all the other models (Study 1: all t > 3.6, p < 0.007; Study 2: all t > 2.9, p < 0.034; Bonferroni-corrected t-tests) except for the Guilt-envy model in the data of Study 1 (t = 2.19, p = 0.17).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 37. `responsibility-redux-model-incorporating-expected`

**empirical** · type `empirical` · panel `fig3c,fig3g` · epistemic `tentative` · stance `asserts`

> The Responsibility Redux model — incorporating expected, previous and current rewards, reward prediction errors for both participant and partner, and decision-maker — predicted the variations in participants' momentary happiness well.

Relations: `tests` → `responsibility-partner-outcomes-influences-participant`; `requires` → `momentary-happiness-modelled-five-computational`; `requires` → `happiness-ratings-z-scored-per-participant`


**Notes from extraction:** The model-based regressors used in the fMRI analyses depend on this fit.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> A computational model taking into account expected, previous and current rewards, reward prediction errors for both participant and partner, and decision-maker (Responsibility Redux model, see Results) predicted the variations in participants’ momentary happiness well

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 38. `when-partner-received-low-lottery`

**empirical** · type `empirical` · panel `fig3d,fig3h` · epistemic `tentative` · stance `asserts`

> When the partner received the low lottery outcome, participant happiness was lower when the participant rather than the partner had chosen the lottery — a significant partner-outcome × decision-maker interaction (Study 1: t(1180) = 3.52, p = 0.0004, β = 0.37; Study 2: t(937) = 2.85, p = 0.0045, β = 0.33) — operationalizing interpersonal guilt.

Relations: `tests` → `responsibility-outcomes-generates-guilt-participant`; `requires` → `linear-mixed-model-containing-all`; `requires` → `hold-partner-behaviour-constant-across`; `supports` → `both-studies-participants-felt-worse`

Reproductions: 2 record(s) (carried from `guilt-reduces-happiness-after-partner-loss`)  

**Notes from extraction:** The core behavioural 'guilt effect'; this is the empirical result that tests the guilt prediction.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Crucially, the interaction between partner outcome and decision-maker was significant (Study 1: t(1180) = 3.52, p = 0.0004, β = 0.37, 95% CI = [0.16 0.58]; Study 2: t(937) = 2.85, p = 0.0045, β = 0.33, 95% CI = [0.10 0.56]). When the partner received the low lottery outcome, participant happiness was lower when they rather than the partner had chosen the lottery (Figure 3D, H).

**caption-reader evidence:**
> Crucially, responsibility for low lottery outcomes for the partner decreased participant happiness more than the same outcomes following partner choices (see Results), which fits the definition of interpersonal guilt.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 39. `bilateral-ventral-striatum-more-active`

**control** · type `empirical` · panel `fig4a` · epistemic `tentative` · stance `asserts`

> The bilateral ventral striatum was more active when participants chose the risky rather than the safe option (Cohen's d = 0.72 left, 0.85 right), irrespective of Social or Solo condition, replicating previous findings.

Relations: `rules-out` → `alt-imaging-contrast-invalid`; `requires` → `all-reported-clusters-survive-whole-brain`

Reproductions: 2 record(s) (carried from `ventral-striatum-tracks-risky-choices`)  

**Notes from extraction:** The results reader treated this as a control replicating a known risk-related effect and validating the imaging analysis; the caption reader described it as a plain empirical result. Both are empirical measurements agreeing on panel and direction; resolved to control.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We searched for brain regions engaged more when participants chose the risky instead of the safe option and found such responses in the bilateral ventral striatum (Cohen’s d = 0.72 and 0.85 in the left and right clusters, respectively; Figure 4A and Appendix 1—table 3), which replicates previous findings (Cui et al., 2022; Preuschoff et al., 2006).

**caption-reader evidence:**
> ( A ) Regions showing a greater response when participants chose the risky (lottery) rather than the safe option, irrespective of Social or Solo condition.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 40. `dot-products-between-individual-neural`

**control** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> Dot products between individual neural guilt responses and the Yu et al. (2020) guilt-related brain signature (GRBS) were overall positive (mean = 5.22, median = 6.97, sign test p = 0.017, Cliff's Delta = 0.4), providing convergent validity with a previously published neural guilt signature.

Relations: `supports` → `anterior-insula-neural-substrate-guilt`

Reproductions: 2 record(s) (carried from `insula-guilt-replicates-yu-koban-signature`)  

**Notes from extraction:** [reviewer] role: empirical → control. The comparison against an independent, previously published neural guilt signature (Yu et al., 2020) is a convergent-validity check: its specific outcome - positive dot products - strengthens the warrant for the anterior insula as a guilt-tracking substrate rather than establishing a new primary finding, so its work in the argument is to validate the insula/guilt result. Provides convergent validity with a previously published neural guilt signature.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The dot products between individual responses and the GRBS varied between –40.1 and 36.7, but overall these values were positive (mean = 5.22; median = 6.97; sign test: p = 0.017; Cliff’s Delta = 0.4 = medium effect size; data are not normally distributed).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 41. `guilt-effect-occurred-whether-participant`

**control** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> The guilt effect occurred whether the participant received the high lottery outcome (Study 1: t(39) = –3.58, p < 0.001, d = 0.56; Study 2: t(43) = –2.68, p = 0.01, d = 0.4) or the low outcome (Study 1: t(39) = –3.39, p = 0.002, d = 0.54; Study 2: t(43) = –3.58, p < 0.001, d = 0.54).

Relations: `rules-out` → `alt-guilt-effect-driven-by-own-outcome`; `supports` → `both-studies-participants-felt-worse`

Reproductions: 2 record(s) (carried from `guilt-effect-independent-of-own-outcome`)  

**Notes from extraction:** Shows the guilt effect does not depend on the participant's own outcome, strengthening (validating) the guilt interpretation.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The ‘guilt effect’ occurred whether the participant received the high lottery outcome (Study 1: t(39) = –3.58, p < 0.001, d = 0.56, BF10 = 32; Study 2: t(43) = –2.68, p = 0.01, d = 0.4, BF10 = 3.8) or the low lottery outcome (Study 1: t(39) = –3.39, p = 0.002, d = 0.54, BF10 = 19; Study 2: t(43) = –3.58, p < 0.001, d = 0.54, BF10 = 33.5).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 42. `individual-grbs-dot-product-values-not`

**control** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> Individual GRBS dot-product values did not correlate with the behavioural guilt responses (Spearman's Rho = –0.058, p = 0.725), indicating the neural signature does not track individual differences in behavioural guilt sensitivity.

Relations: none

Reproductions: 2 record(s) (carried from `guilt-signature-no-individual-difference`)  

**Notes from extraction:** Null result: the neural signature does not track individual differences in behavioural guilt sensitivity.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We assessed whether inter-individual differences in these dot product values correlated with the behavioural guilt responses, but did not find a significant association [Spearman’s Rho = –0.058, p = 0.725].

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 43. `manipulation-check-bilateral-ventral-striatum`

**control** · type `empirical` · panel `fig4g` · epistemic `tentative` · stance `asserts`

> As a manipulation check, bilateral ventral striatum activation increased with expected certain rewards and the expected values of chosen lotteries, explained by a model-based regressor coding participant rewards (left: pFWE = 0.002, T = 5.63, d = 0.75; right: pFWE = 0.005, T = 5.46, d = 0.70).

Relations: `rules-out` → `alt-model-based-glm-invalid`; `requires` → `model-based-glm-entered-best-fitting-computational`

Reproductions: 2 record(s) (carried from `ventral-striatum-tracks-computational-reward`)  

**Notes from extraction:** The results reader treated this as a manipulation check validating the model-based BOLD analysis; the caption reader described it as a plain empirical result. Both agree on panel and direction; resolved to control.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We found that activation in bilateral ventral striatum indeed increased with the amount of expected certain rewards and the expected values of chosen lotteries (left: pFWE = 0.002, T = 5.63, d = 0.75, Z = 5.41, 110 voxels, peak at MNI [–14 8 –8], right: pFWE = 0.005, T = 5.46, d = 0.70, Z = 5.26, 80 voxels, peak at MNI [10 10 −4]).

**caption-reader evidence:**
> ( G ) Activation in bilateral ventral striatum explained by a computational model-based regressor coding participant rewards.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 44. `no-significant-interaction-between-difference`

**control** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> There was no significant interaction between the difference in expected values and experimental conditions in either study (p > 0.52).

Relations: none


**Notes from extraction:** Null result.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> There was no significant interaction between the difference in expected values and experimental conditions in either study (p > 0.52).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 45. `participants-probability-choosing-risky-option`

**control** · type `empirical` · panel `fig2a,fig2d` · epistemic `tentative` · stance `asserts`

> Participants' probability of choosing the risky option (lottery) increased with the difference between the expected value of the lottery and the value of the safe option (Study 1: t(4796) = 9.26, p < 3.1e–20, β = 0.074; Study 2: t(3829) = 10.62, p < 5.3e–26, β = 0.093).

Relations: `rules-out` → `alt-participants-insensitive-to-value`

Reproductions: 2 record(s) (carried from `lottery-choice-increases-with-ev`)  

**Notes from extraction:** Manipulation check that choices tracked expected value as intended.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> As expected, participants’ probability of choosing the risky option (lottery) increased with the difference between the expected value of the lottery and the value of the safe option (Study 1: Figure 2A, t(4796) = 9.26, p < 3.1e–20, β = 0.074, 95% CI = [0.059 0.090]; Study 2: Figure 2D, t(3829) = 10.62, p < 5.3e–26, β = 0.093, 95% CI = [0.075 0.110]).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 46. `pre-task-icebreaker-succeeded-establishing-positive`

**control** · type `empirical` · panel `app1table11` · epistemic `tentative` · stance `asserts`

> A pre-task icebreaker succeeded in establishing a positive attitude toward the partner: participants rated their partners highly (all above 8 on a 1–10 scale) on sympathy, cooperativity, honesty, openness, and sociability in both studies.

Relations: none


**Notes from extraction:** Manipulation check that the social relationship was positive and non-competitive; the caption reader anchored it to Appendix 1—table 11 (ratings across the five items range roughly 8.35–9.34 across Studies 1 and 2).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> How honest did they seem? 9.05 (1.11) 9.34 (1.10)

**structure-reader evidence:**
> participants’ average ratings of their partners in terms of sympathy, cooperativity, honesty, openness and sociability were all above 8 on a scale of 1–10, in both studies ( Appendix 1—table 11 ).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 47. `responsibility-choices-not-influence-happiness`

**control** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> Responsibility for choices did not influence happiness following positive (high) lottery outcomes for the partner (both studies, all |t| < 1.3, p > 0.2, BF10 < 0.2).

Relations: `supports` → `both-studies-participants-felt-worse`


**Notes from extraction:** Null result establishing that the guilt effect is specific to negative partner outcomes.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Responsibility for choices did not influence happiness following positive lottery outcomes for the partner (both studies, all |t| < 1.3, p > 0.2, BF10 < 0.2).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 48. `risk-aversion-parameter-not-differ-between`

**control** · type `empirical` · panel `—` · epistemic `tentative` · stance `asserts`

> The risk-aversion parameter ρ did not differ between gain and loss trials (Study 1: t(17) = 0.21, p = 0.84, d = 0.05; Study 2: t(15) = –0.61, p = 0.55, d = 0.15), justifying pooling across gain and loss trials.

Relations: none


**Notes from extraction:** Null result justifying pooling across gain and loss trials.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> As ρ did not vary between gain and loss trials (Study 1: t(17) = 0.21, p = 0.84, d = 0.05; Study 2: t(15) = –0.61, p = 0.55, d = 0.15; paired t-test), we then pooled across gain and loss trials.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 49. `risk-premiums-not-differ-between`

**control** · type `empirical` · panel `fig2b,fig2e` · epistemic `tentative` · stance `asserts`

> Risk premiums did not differ between Solo and Social conditions in either study (Study 1: t(39) = 1.53, p = 0.134, d = 0.24, BF10 = 0.49; Study 2: t(43) = –0.21, p = 0.84, d = –0.03, BF10 = 0.17).

Relations: `rules-out` → `alt-social-context-shifts-risk-attitude`; `requires` → `risk-attitude-quantified-risk-premium`; `supports` → `participants-showed-very-similar-risk`

Reproductions: 1 record(s) (carried from `risk-premiums-null-social-solo`)  

**Notes from extraction:** Null result; evidence against social-context-driven changes in risk aversion.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Risk premiums did not differ between Social and Solo conditions (Study 1: Figure 2B, t(39) = 1.53, p = 0.134, Cohen’s d = 0.24, BF10 = 0.49; Study 2: Figure 2E, t(43) = –0.21, p = 0.84, d = –0.03, BF10 = 0.17).

**caption-reader evidence:**
> ( B, E ) Risk premiums did not differ between Solo and Social conditions.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 50. `all-reported-clusters-survive-whole-brain`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> All reported clusters survive a whole-brain family-wise-error-corrected threshold of p < 0.05 with a cluster-forming voxel-wise threshold of p < 0.001 (or a smaller volume where explicitly mentioned).

Relations: none


**Notes from extraction:** The statistical threshold that licenses every reported fMRI cluster.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> All clusters reported survive a significance threshold of p < 0.05 with family-wise error correction for multiple comparisons across the whole brain or a smaller volume when explicitly mentioned, based on an uncorrected voxel-wise (cluster-forming) threshold of p < 0.001.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 51. `among-computational-models-fitted-momentary`

**methodological** · type `assessment` · panel `table1` · epistemic `tentative` · stance `asserts`

> Among the computational models fitted to momentary happiness data, the Responsibility Redux model achieved the best (lowest) AIC in both studies (Study 1 AIC –1499; Study 2 AIC –1195).

Relations: none


**Notes from extraction:** Best-fitting model inferred from the lowest AIC values (Study 2 Responsibility Redux AIC –1195). Note the apparent tension: the results reader instead reported the (non-Redux) Responsibility model as the best fit by likelihood-ratio test and R²; which model is 'best' depends on the metric, and the two readers anchored different models to Table 1, so they are not merged.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> Responsibility Redux 4 0.361 0.331 –999 –1499

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 52. `happiness-ratings-z-scored-per-participant`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> Happiness ratings were Z-scored per participant to remove the influence of differing rating variability across participants.

Relations: none


**Notes from extraction:** Because ratings are Z-scored, happiness effects are expressed in standardized units and no constant term is used in the happiness models.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> For analysis, happiness ratings were Z -scored to cancel out effects of different rating variabilities across participants.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 53. `hold-partner-behaviour-constant-across`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> To hold the partner's behaviour constant across participants, the partner's decisions were simulated by an algorithm that always selected the option with the highest expected value.

Relations: none

Reproductions: 1 record(s) (carried from `partner-algorithm-deception-assumption`)  

**Notes from extraction:** The partner was not a free agent; partner choices in the Partner condition were deterministic, which the responsibility/guilt contrasts rely on.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> In order to ascertain constant decisions by the partner, the partner’s decisions were simulated using a simple algorithm that always selected the option with the highest expected value

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 54. `linear-mixed-model-containing-all`

**methodological** · type `assessment` · panel `app1table2` · epistemic `tentative` · stance `asserts`

> The linear mixed model containing all three two-way interaction terms (Model 5, Equation 10) explained the happiness data significantly better than simpler models without interactions (p < 2e−5) and no worse than the model with all interactions (p > 0.5), warranting reporting the crucial partnerHigh:participantDecided (guilt) interaction from it.

Relations: none


**Notes from extraction:** Contested role/type: the caption reader classified this as an empirical result (Model 5 best-fitting, with its partnerHigh:participantDecided guilt coefficient significant — 0.39*** Study 1, 0.31** Study 2), while the structure reader classified it as a methodological warrant licensing the reported interaction. Resolved to methodological.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**caption-reader evidence:**
> In both studies, Model 5 ( Equation 9  in the Results section of the main text), which contained all three two-way interaction terms, explained the data best, so its parameters for the crucial partnerHigh:participantDecided interaction are reported in the main text.

**structure-reader evidence:**
> the model reported in Equation 10 fitted the data significantly better (p < 2e−5) than the simpler models without interactions (higher total and adjusted R 2 , see Appendix 1—table 2 ), but not significantly worse than the model with all interactions (p > 0.5; tested with the ANOVA function in R).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 55. `model-based-glm-entered-best-fitting-computational`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> A model-based GLM (GLM2) entered the best-fitting computational (Responsibility) model's variables — certain rewards (CR), expected value (EV), participant RPE (sRPE), and partner RPE from participant choices (social_pRPE) and from partner choices (partner_pRPE) — as regressors to locate brain regions reflecting them.

Relations: `enables-method` → `momentary-happiness-modelled-five-computational`


**Notes from extraction:** The neural claims about tracking social_pRPE versus partner_pRPE depend on this model-based GLM being interpretable, which in turn depends on the model comparison.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We used the model to create expected BOLD responses for each participant (see Methods) and as a manipulation check searched for responses in ventral striatum evoked by participant rewards (O’Doherty et al., 2004; O’Doherty et al., 2007).

**structure-reader evidence:**
> In addition, we created another GLM (GLM2) with regressors designed to identify brain regions whose activation reflected the variables of the best-fitting computational model (see above).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 56. `model-selection-among-happiness-models`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> Model selection among the happiness models used likelihood-ratio tests comparing the Responsibility model pairwise against each other model, supplementing the AIC, BIC, R² and adjusted R² values.

Relations: none


**Notes from extraction:** The model-comparison method that licenses treating the best-fitting model's variables as the regressors entered into the model-based fMRI GLM (GLM2). Kept distinct from the results reader's report of the likelihood-ratio outcome, which is an empirical result rather than a method.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> we supplemented the AIC, BIC, R 2 and adjusted R 2 values reported in Table 1 with a series of likelihood ratio tests : we compared pair-wise the likelihoods of the Responsibility model given the data to the likelihoods of all the other models.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 57. `momentary-happiness-modelled-five-computational`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> Momentary happiness was modelled with five computational models (Basic, Inequality, Guilt-envy, Responsibility, and Responsibility Redux) sharing separate, exponentially decaying terms for certain rewards, expected value, and reward prediction errors.

Relations: none


**Notes from extraction:** The Basic, Inequality and Guilt-envy models are identical to those in Rutledge et al., 2016.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> All models contained separate terms for certain rewards, expected value for lotteries and reward prediction errors, with influences that decayed exponentially over trials.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 58. `parameter-recovery-procedure-synthetic-data-generated`

**methodological** · type `assessment` · panel `fig3s1` · epistemic `tentative` · stance `asserts`

> A parameter-recovery procedure on synthetic data generated from each participant's estimated parameters showed the happiness-model parameters could be reliably recovered, verifying their stability.

Relations: `supports` → `responsibility-redux-model-incorporating-expected`


**Notes from extraction:** All three readers surfaced this and agree on the substance and panel (fig3s1), but disagree on role/type: the results and caption readers classified it as a methodological assessment (a capability warranting the model-based analysis), while the structure reader classified it as an empirical control (claim_type empirical) validating parameter stability. Resolved to methodological by majority; recorded as contested because they disagree on whether it is an assessment or a result.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> The stability of these estimated parameters was verified using a parameter recovery procedure (see Methods and Figure 3—figure supplement 1).

**caption-reader evidence:**
> Stability of the estimated parameters of the temporal difference models was evaluated by attempting to recover parameters from synthetic data created using each participant’s real estimated parameters.

**structure-reader evidence:**
> The results show that the estimated parameters could be reliably recovered from noisy synthetic data.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 59. `risk-attitude-quantified-risk-premium`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> Risk attitude was quantified as a risk premium — the EVdiff value yielding 50% risky choices from a fitted logistic regression — and compared between Solo and Social conditions with paired t-tests in both studies.

Relations: none


**Notes from extraction:** A parallel CARA expected-utility model estimated a risk-preference parameter rho, also compared between Solo and Social conditions with paired t-tests; this defines the measure behind the null risk-premium comparison.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> The risk premium for each condition was defined as the EVdiff value corresponding to 50% risky choices indicated by the fitted logistic regression model. In both studies, these risk premium values were compared between Solo and Social conditions using paired t -tests.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 60. `study-sample-size-fixed-priori`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> The Study 2 sample size of 44 was fixed a priori by a G*Power analysis based on Study 1's effect size (Cohen's d = 0.56), with alpha = 0.05 and power = 0.95.

Relations: `requires` → `guilt-effect-occurred-whether-participant`


**Notes from extraction:** Warrants that Study 2 was adequately powered to detect the guilt effect established in Study 1.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> based on the results of Study 1 (Cohen’s d = 0.56), with alpha error = 0.05 and power (1 − beta) = 0.95, the required sample size was 44.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 61. `two-gppi-seed-to-voxel-connectivity-analyses`

**methodological** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> Two gPPI seed-to-voxel connectivity analyses used functionally defined seeds: the left insula cluster more sensitive to Risky versus Safe outcomes (GLM3) and the left STS cluster responding more to social_pRPE than partner_pRPE (GLM4), with identical seeds across participants.

Relations: none


**Notes from extraction:** The seeds are themselves defined from prior contrasts, so the connectivity results are conditional on those seed definitions.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> We ran two models for each participant, both based on GLM1, with the following seeds: the left insula cluster more sensitive to the outcomes of Risky vs . Safe choices, yielding GLM3 (see Figure 4D, E ), and the left STS cluster responding more to social_pRPE than partner_pRPE , yielding GLM4 ( Figure 4H ).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 62. `each-trial-participants-chose-between`

**scope** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> On each trial participants chose between a safe and a risky monetary option under three conditions: choosing for oneself (Solo), for oneself and the partner (Social), and having the partner choose for both (Partner).

Relations: `scopes` → `participants-chose-risky-option-lottery`; `scopes` → `participants-slightly-more-risk-averse`; `scopes` → `participant-happiness-lower-when-participant`; `scopes` → `when-partner-received-low-lottery`


**Notes from extraction:** The within-subject responsibility manipulation on which the guilt and agency contrasts depend.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> There were three kinds of trials: decisions by the participant only for themselves ( Solo condition), decisions by the participant for themselves and the partner ( Social condition), and decisions by the partner for both themselves and the participant ( Partner condition).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 63. `findings-rest-two-samples-healthy`

**scope** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> The findings rest on two samples of healthy adults — Study 1 (behaviour only, N = 40) and Study 2 (fMRI, N = 44); all BOLD/fMRI results derive from Study 2, while the behavioural results come from both studies.

Relations: `scopes` → `participants-showed-very-similar-risk`; `scopes` → `both-studies-participants-felt-worse`

Reproductions: 1 record(s) (carried from `scope-two-study-design`)  

**Notes from extraction:** Global scope condition bounding the empirical claims; distinguishes the behavioural study from the fMRI study. The results reader emphasised that BOLD results come only from Study 2; the structure reader gave the two sample sizes.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> We analysed the BOLD responses of brain regions engaged during decision-making and at the time of receiving the outcomes of the choice using conventional as well as computational model-based analyses, using the fMRI data collected in Study 2.

**structure-reader evidence:**
> Forty healthy participants (14 male, mean age 26.1, range 22–31) participated in Study 1 (behaviour only study), and 44 healthy participants (19 male, mean (SD) age = 30.6 (6.5), range 23–50) participated in Study 2 (fMRI study).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 64. `fmri-data-four-study-participants`

**scope** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> The fMRI data of four Study 2 participants were excluded from the fMRI analysis for excessive head motion (>3 mm or >3°).

Relations: none


**Notes from extraction:** Bounds the effective N for all fMRI results in Study 2.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> The fMRI data from four participants in Study 2 were excluded from the fMRI data analysis because of excessive head motion (>3 mm or >3°).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 65. `study-reproduced-study-design-inside`

**scope** · type `assessment` · panel `—` · epistemic `tentative` · stance `asserts`

> Study 2 reproduced the Study 1 design inside the fMRI scanner with identical parameters except for longer inter-stimulus intervals (3–11 s) and partners who were experimenters positioned outside the scanner.

Relations: `scopes` → `during-receipt-lottery-versus-safe`; `scopes` → `insula-rois-responded-more-low`; `scopes` → `one-cluster-left-sts-responded`; `scopes` → `functional-connectivity-between-left-anterior`


**Notes from extraction:** In Study 2 the partner was experimenter MG or TW rather than another participant, so any replication of the Study 1 guilt effect holds under this changed social pairing.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**structure-reader evidence:**
> In Study 2, participants performed two sessions of the experiment described above inside the fMRI scanner. All parameters were identical except that ISIs varied from 3 to 11 s (drawn randomly from a gamma distribution).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 66. `both-studies-participants-felt-worse`

**synthesis** · type `synthesis` · panel `—` · epistemic `tentative` · stance `asserts`

> In both studies, participants felt worse after low lottery outcomes for the partner when those outcomes followed their own choice rather than the partner's, which the authors interpret as interpersonal guilt.

Relations: none


**Notes from extraction:** Integrates the guilt-effect results across both studies; synthesis is expected to be single-source (results reader only).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Within these outcomes, participants felt worse following low lottery outcomes for the partner if those outcomes were consequences of their own choice rather than the partner’s, which we interpret as interpersonal guilt.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 67. `participants-showed-very-similar-risk`

**synthesis** · type `synthesis` · panel `—` · epistemic `tentative` · stance `asserts`

> Participants showed very similar risk preferences whether deciding only for themselves (Solo) or for themselves and their partner (Social), with only a tendency toward higher risk aversion in the Social condition in Study 1.

Relations: none


**Notes from extraction:** Integrates the choice, risk-premium and ρ results across both studies; synthesis is expected to be single-source (results reader only).

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> In sum, participants showed very similar risk preferences when making decisions affecting only themselves (Solo condition) or themselves and their partner (Social condition), with a tendency towards higher risk aversion in the Social condition in Study 1.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 68. `authors-suggest-left-sts-region`

**interpretation** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> The authors suggest this left STS region tracks a partner's unexpected outcomes less when they do not follow from the participant's decisions.

Relations: `interprets` → `one-cluster-left-sts-responded`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> This finding suggests that this region of the left STS tracks a partner’s unexpected outcomes less when they do not follow from the participant’s decisions.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 69. `behavioural-guilt-effect-larger-happiness`

**interpretation** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> The behavioural guilt effect (larger happiness decrease after low partner outcomes following participant rather than partner choices) is compatible with 'simple guilt'.

Relations: `interprets` → `when-partner-received-low-lottery`


<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> This behavioural effect (difference in happiness obtained when the partner received low lottery outcomes after participant rather than partner choices) is thus compatible with ‘simple guilt’, and we will thus refer to it as ‘guilt effect’.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 70. `connectivity-between-left-anterior-insula`

**interpretation** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> Connectivity between the left anterior insula and the right inferior frontal gyrus varied with choice and condition, suggesting this prefrontal region is sensitive to guilt-related information during social choices.

Relations: `interprets` → `functional-connectivity-between-left-anterior`

Reproductions: 2 record(s) (carried from `insula-ifg-connectivity-guilt`)  

**Notes from extraction:** Interpretation stated in the abstract.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Connectivity between this region and the right inferior frontal gyrus varied depending on choice and experimental condition, suggesting that this part of prefrontal cortex is sensitive to guilt-related information during social choices.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 71. `lower-happiness-when-participant-decision-maker`

**interpretation** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> The lower happiness when the participant is the decision-maker may reflect responsibility aversion — a cost of the 'weight of the responsibility'.

Relations: `interprets` → `participant-happiness-lower-when-participant`


**Notes from extraction:** Interpretation of the agency effect through the responsibility-aversion literature.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> This is interesting in itself and may reflect the drive behind responsibility aversion reported by Edelson et al.’s 2018 study: being assigned the role of the decider in a social setting may make people slightly unhappy, perhaps due to ‘weight of the responsibility’.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 72. `prior-functional-connectivity-work-shown`

**literature-context** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> Prior functional connectivity work has shown network differences between social and self-only choices, midbrain–anterior cingulate interactions during guilt compensation, and links between insula connectivity and responsibility aversion.

Relations: `supports` → `functional-connectivity-between-guilt-responsibility-related`


**Notes from extraction:** Prior-work premises motivating the connectivity analysis.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Functional connectivity analyses have revealed differences in networks engaged by social and self-only choices (Jung et al., 2013; Ogawa et al., 2018), interactions between midbrain and anterior cingulate during compensation for guilt (Yu et al., 2014), and links between insula connectivity and responsibility aversion (Edelson et al., 2018).

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 73. `prior-literature-documents-association-between`

**literature-context** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> Prior literature documents an association between the anterior insula and guilt.

Relations: `supports` → `anterior-insula-neural-substrate-guilt`


**Notes from extraction:** Inherited premise motivating the insula small-volume correction.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Given the documented association between anterior insula and guilt (see Introduction), we proceeded to test whether this result survived correction for family-wise errors due to multiple comparisons restricted to the left anterior insula grey matter.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes: 

## 74. `rutledge-colleagues-established-changes-momentary`

**literature-context** · type `interpretive` · panel `—` · epistemic `tentative` · stance `asserts`

> Rutledge and colleagues established that changes in momentary happiness during a probabilistic reward task are explained by recent reward expectations and the prediction errors arising from them.

Relations: `supports` → `momentary-happiness-modelled-five-computational`


**Notes from extraction:** Prior-work premise the happiness-modelling approach inherits.

<!-- Evidence quotes from the extraction agents — preserved for audit. Edit or remove as appropriate. -->

**results-reader evidence:**
> Following Rutledge and colleagues’ methodology, which considers that changes in momentary happiness in response to outcomes of a probabilistic reward task are explained by the combined influence of recent reward expectations and prediction errors arising from those expectations, we fitted computational models to each participant’s happiness data.

- [ ] claim ✓/✗/?  
- [ ] role ✓/✗/?  
- [ ] panel ✓/✗/?  
- [ ] relations ✓/✗/?  
- notes:
