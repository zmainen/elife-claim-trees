# The claim vocabulary

Generated from `extract/elife_extract/vocabulary.py` and `scripts/relations.py` by `elife-extract contract --write`. Do not edit; edit the source and regenerate. Every example is a claim in the corpus, quoted from its file.

A claim is one declarative sentence in active voice, quantitative where the result is quantitative, carrying the paper's own epistemic verb. It has a **claim type** (what kind of proposition it is), a **role** (the work it does in this paper's argument), and **relations** to other claims. Type and role are independent axes: a measurement can play the role of a result, a control or a scope condition.

## Claim types

| `claim_type` | Meaning |
|:--|:--|
| `empirical` | a directly observed or computed result |
| `interpretive` | an inference drawn from one or more empirical claims |
| `existence` | an assertion that a phenomenon, entity or resource exists |
| `synthesis` | a claim integrating results across several analyses or papers |
| `assessment` | a methodological, scope or quality claim about how the work was done |
| `hypothesis` | a proposition bet on, not yet evidenced by this paper's results |
| `prediction` | a deduced expectation, to be tested by an empirical claim |

## Roles

Nine roles. The signal phrases are what the prose says when it is doing that work; they are cues, not tests.

### `hypothesis`

The proposition the paper bets on: the organising question, stated as a claim about the world. It carries no empirical content of its own; it is what the predictions are deduced from and what the results are gathered for. Most papers have one to three.

- Typical claim type: `hypothesis`
- Signals: “we hypothesize”, “we propose that”, “we asked whether”, “we sought to test”, “the central question is whether”
- Carries: `entails` to each of its predictions; usually `panel: null`
- Example: `hypothesis-distinct-compartmental-roles` (hypothesis, Headley): “Perisomatic and distal dendritic inhibition serve distinct computational roles in layer 5 pyramidal neurons: perisomatic inhibition principally regulates somatic action potential generation (gain and threshold of axonal output), while distal dendritic inhibition principally regulates dendritic spike incidence and the temporal coupling of dendritic spikes to somatic APs.”

### `prediction`

What should be observed if the hypothesis holds, under stated conditions. A prediction is deduced, not measured: it is anchored in the model or in principled reasoning, and an empirical claim then tests it. Write it as a conditional when the paper does not.

- Typical claim type: `prediction`
- Signals: “if X, then we should observe Y”, “this predicts that”, “the model predicts”, “should be maximally effective at”, “is predicted to”
- Carries: `derived-from` back to its hypothesis (written mechanically); is the target of `tests`
- Example: `prediction-beta-optimal-distal` (prediction, Headley): “If the optimal frequency of rhythmic inhibition at a compartment is set by matching the rhythm period to the local spike timescale, then distal inhibition — where apical Ca²⁺ and NMDA spikes lead the soma by ~20 ms and ~25 ms respectively — should be maximally effective at beta frequencies (~20 Hz), whose period (~50 ms) matches the dendritic-spike lead time.”

### `empirical`

A measured or computed result, anchored to the panel that shows it, carrying the paper's own numbers and the paper's own epistemic verb. The largest role.

- Typical claim type: `empirical`
- Signals: “we found that”, “we observed”, “we measured”, “increased”, “did not differ”
- Carries: `tests` to the prediction it checks; `supports` and `requires` as the argument needs
- Example: `distal-inhib-drops-firing-02hz` (empirical, Headley): “Doubling the strength of distal dendritic inhibition reduces somatic firing rate from a baseline of approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing the occurrence of dendritic Ca²⁺ and NMDA spikes rather than by directly raising AP threshold.”

### `control`

An empirical result whose work in the argument is to eliminate an alternative explanation or to show a manipulation did what it should. Its content is a measurement; what makes it a control is what it rules out. A null result is usually a control.

- Typical claim type: `empirical`
- Signals: “rules out”, “excludes”, “is not due to”, “no significant effect of”, “control condition”, “manipulation check”, “regardless of”
- Carries: `rules-out` to the alternative it eliminates; `validates` to the claim it defends
- Example: `risk-premiums-null-social-solo` (control, Gadeke): “Risk premiums do not differ between Solo and Social conditions in either study (Study 1: t(39)=1.53, p=0.134, Cohen's d=0.24, BF10=0.49; Study 2: t(43)=−0.21, p=0.84, d=−0.03, BF10=0.17), providing evidence against social-context-driven changes in risk aversion in this paradigm.”

### `scope`

A boundary condition on what the results can mean: the model class, the preparation, the population, the design. Often global. It asserts nothing about the world; it says where the paper's assertions apply.

- Typical claim type: `assessment`
- Signals: “all results come from”, “restricted to”, “in this preparation”, “was not a physiological pattern”, “N = ”
- Carries: `scopes` to the claims it bounds, or `scopes: ["*"]`
- Example: `l5-model-single-cell-scope` (scope, Headley): “All results derive from a single-cell compartmental model of one layer 5 pyramidal neuron; no network dynamics, recurrent excitation, or population-level inhibitory effects are simulated, and all firing rate effects are for a single isolated neuron receiving naturalistic presynaptic drive.”

### `methodological`

A capability or analytical commitment that a downstream result depends on for its interpretation: the sorting pipeline, the null distribution, the model fit that licenses a model-based analysis. Not procedure for its own sake — which software ran the task is not a claim unless a result turns on it.

- Typical claim type: `assessment`
- Signals: “analysis is on”, “nulls are”, “fit better than”, “validated against”
- Carries: `enables-method` to the results it warrants
- Example: `preregistered-design-validates-mvpa` (methodological, Kammer): “The preregistered analysis plan (osf.io/rxacd) specifies the MVPA decoding pipeline, ROI definitions, and statistical tests in advance, reducing the risk of analytic flexibility inflating the decoding accuracy results.”

### `synthesis`

A higher-order proposition that integrates several of the paper's own results into one claim, staying inside the paper's evidence: the dissociation, the reconciliation, the summary that several panels jointly establish.

- Typical claim type: `synthesis`
- Signals: “taken together”, “these results show”, “this dissociation establishes”, “in summary”
- Carries: is the target of `supports` from the results it integrates
- Example: `orthogonality-derived-from-additivity` (synthesis, Meijer): “In a 2 × 2 factorial choice × stimulation experimental design with linear (PCA) projection of the population response, additive 5-HT modulation entails geometric orthogonality between the stimulation-effect direction and the choice direction. Under additive modulation, every choice trajectory is displaced by the same vector (the stimulation effect), so the displacement that distinguishes the stimulated from the unstimulated trajectories — averaged across choice — is by definition orthogonal to the displacement that distinguishes the choice trajectories — averaged across stimulation. The orthogonality result in PCA space (`5ht-axis-orthogonal-to-choice-axis`) is therefore a geometric corollary of the GLM additivity finding, not an independent empirical claim.”

### `interpretation`

A reading of the results through a theoretical lens from outside the paper's own evidence: a mapping onto a framework, a proposed mechanism, a functional meaning. It is an act of mapping, not a derivation.

- Typical claim type: `interpretive`
- Signals: “may provide a functional interpretation”, “suggests a role for”, “points to a mechanism whereby”, “is consistent with the view that”
- Carries: `interprets` to the empirical claims it reframes
- Example: `pv-gamma-sst-beta-correspondence` (interpretation, Headley): “The model provides mechanistic grounding for the empirical association of parvalbumin-positive interneurons with gamma rhythms and somatostatin-positive interneurons with beta rhythms: PV+ neurons target perisomatic locations where gamma is optimal for AP threshold modulation, while SST+ neurons target distal dendrites where beta is optimal for dendritic spike entrainment.”

### `literature-context`

A finding from cited prior work that the paper's argument inherits as a premise, recorded as a claim of its own so the inheritance is auditable. The citation may be implicit: prose that paraphrases a prior empirical pattern as background is literature-context whether or not it names the paper.

- Typical claim type: `interpretive`
- Signals: “as shown by”, “previous work has established”, “the reported association of”, “(Author, Year) found”
- Carries: is the target of `requires` or `interprets` from the claims that lean on it
- Example: `interprets-pv-gamma-sst-beta-associations` (literature-context, Headley): “Empirical work across the cortical-interneuron literature has established two correlated associations: parvalbumin-positive (PV+) fast-spiking interneurons target perisomatic compartments and are implicated in the generation and entrainment of cortical gamma rhythms (40–80 Hz), while somatostatin-positive (SST+) interneurons target distal dendritic compartments and are preferentially associated with beta rhythms (12–35 Hz). These are literature claims about anatomical targeting patterns and their correlation with specific oscillatory bands, not results of the present paper.”

### Roles that are confused for each other

**`hypothesis` versus `prediction`.** A hypothesis says what is the case; a prediction says what will be observed if it is. "Compartments serve distinct roles" is the bet; "if so, doubling distal inhibition should suppress dendritic spikes more than doubling perisomatic inhibition" is what it commits the paper to seeing. Surface both, and keep them apart: adding predictions never reduces the number of hypotheses.

- `hypothesis`: `hypothesis-distinct-compartmental-roles` (hypothesis, Headley): “Perisomatic and distal dendritic inhibition serve distinct computational roles in layer 5 pyramidal neurons: perisomatic inhibition principally regulates somatic action potential generation (gain and threshold of axonal output), while distal dendritic inhibition principally regulates dendritic spike incidence and the temporal coupling of dendritic spikes to somatic APs.”
- `prediction`: `prediction-distal-dendritic-spike-mechanism` (prediction, Headley): “If perisomatic and distal dendritic inhibition serve dissociated computational roles, then doubling distal dendritic inhibition should reduce somatic firing primarily by suppressing apical Ca²⁺ and NMDA dendritic spikes, with little change in the somatic AP voltage threshold.”

**`control` versus `empirical`.** Both are measurements. Ask what the result is *for*: if it demonstrates the effect the paper is about, it is empirical; if it shows that something else does not explain that effect, or that the manipulation worked, it is a control.

- `control`: `risk-premiums-null-social-solo` (control, Gadeke): “Risk premiums do not differ between Solo and Social conditions in either study (Study 1: t(39)=1.53, p=0.134, Cohen's d=0.24, BF10=0.49; Study 2: t(43)=−0.21, p=0.84, d=−0.03, BF10=0.17), providing evidence against social-context-driven changes in risk aversion in this paradigm.”
- `empirical`: `guilt-reduces-happiness-after-partner-loss` (empirical, Gadeke): “Happiness ratings decrease more after negative partner outcomes when the participant made the choice (Social condition) than when the partner made the choice (Partner condition), operationalizing interpersonal guilt as responsibility-contingent unhappiness about partner harm.”

**`synthesis` versus `interpretation`.** Synthesis stays inside the paper's own evidence and says what several results jointly establish. Interpretation reaches outside it, to a framework, a mechanism or a literature, and says what the results mean there.

- `synthesis`: `orthogonality-derived-from-additivity` (synthesis, Meijer): “In a 2 × 2 factorial choice × stimulation experimental design with linear (PCA) projection of the population response, additive 5-HT modulation entails geometric orthogonality between the stimulation-effect direction and the choice direction. Under additive modulation, every choice trajectory is displaced by the same vector (the stimulation effect), so the displacement that distinguishes the stimulated from the unstimulated trajectories — averaged across choice — is by definition orthogonal to the displacement that distinguishes the choice trajectories — averaged across stimulation. The orthogonality result in PCA space (`5ht-axis-orthogonal-to-choice-axis`) is therefore a geometric corollary of the GLM additivity finding, not an independent empirical claim.”
- `interpretation`: `pv-gamma-sst-beta-correspondence` (interpretation, Headley): “The model provides mechanistic grounding for the empirical association of parvalbumin-positive interneurons with gamma rhythms and somatostatin-positive interneurons with beta rhythms: PV+ neurons target perisomatic locations where gamma is optimal for AP threshold modulation, while SST+ neurons target distal dendrites where beta is optimal for dendritic spike entrainment.”

**`scope` versus `methodological`.** Scope bounds where the results apply and usually qualifies every empirical claim at once. A methodological claim is a specific capability that specific results depend on for their meaning. "All results come from a single-cell model" is scope; "the preregistered plan fixed the decoding pipeline, the ROIs and the tests in advance" is methodological, because the decoding results count as confirmatory only if it did.

- `scope`: `l5-model-single-cell-scope` (scope, Headley): “All results derive from a single-cell compartmental model of one layer 5 pyramidal neuron; no network dynamics, recurrent excitation, or population-level inhibitory effects are simulated, and all firing rate effects are for a single isolated neuron receiving naturalistic presynaptic drive.”
- `methodological`: `preregistered-design-validates-mvpa` (methodological, Kammer): “The preregistered analysis plan (osf.io/rxacd) specifies the MVPA decoding pipeline, ROI definitions, and statistical tests in advance, reducing the risk of analytic flexibility inflating the decoding accuracy results.”

**`literature-context` versus `interpretation`.** Literature-context restates what a cited paper found; it is someone else's result, inherited. Interpretation is this paper's reading of its own results, even when that reading leans on the literature. The inherited premise and the reading that uses it are two claims.

- `literature-context`: `interprets-pv-gamma-sst-beta-associations` (literature-context, Headley): “Empirical work across the cortical-interneuron literature has established two correlated associations: parvalbumin-positive (PV+) fast-spiking interneurons target perisomatic compartments and are implicated in the generation and entrainment of cortical gamma rhythms (40–80 Hz), while somatostatin-positive (SST+) interneurons target distal dendritic compartments and are preferentially associated with beta rhythms (12–35 Hz). These are literature claims about anatomical targeting patterns and their correlation with specific oscillatory bands, not results of the present paper.”
- `interpretation`: `pv-gamma-sst-beta-correspondence` (interpretation, Headley): “The model provides mechanistic grounding for the empirical association of parvalbumin-positive interneurons with gamma rhythms and somatostatin-positive interneurons with beta rhythms: PV+ neurons target perisomatic locations where gamma is optimal for AP threshold modulation, while SST+ neurons target distal dendrites where beta is optimal for dendritic spike entrainment.”

## Relations

A relation is a proposition about logical structure between two claims, not a citation. Each is directed; the direction column says which end is which. `derived-from` is written mechanically as the reciprocal of `entails` and should not be emitted.

| Relation | Asserts | Direction |
|:--|:--|:--|
| `confirms` | the source confirms the target; reciprocal of predicts | from the result to the prediction or hypothesis it confirms; the reciprocal of predicts |
| `contradicts` | the source and target cannot both hold | from either claim to the other; they cannot both hold |
| `derived-from` | a prediction derived from its hypothesis (inverse of entails) | from the prediction back to its hypothesis; written mechanically as the reciprocal of entails |
| `dissociates-with` | the source and target jointly establish a dissociation (symmetric) | symmetric: between the two empirical claims that together establish the contrast |
| `enables-method` | a result makes a downstream method possible | from the methodological claim to the result whose interpretability it warrants |
| `entails` | a hypothesis entails its prediction — the deductive step | from the hypothesis to the prediction it deductively implies |
| `extends` | the source extends the target beyond its original conditions | from the later or broader result to the claim it extends |
| `interprets` | one claim interprets another | from the interpretation to the empirical claim it reframes |
| `opposes` | the source stands against the target | from the claim that stands against to the one it stands against |
| `predicts` | the source predicts the target, typically model to experiment | from the model or hypothesis to the observation it predicts |
| `qualifies` | a claim narrows another's applicability | from the qualifying result to the claim whose applicability it narrows |
| `refutes` | the source's evidence is incompatible with the target | from the evidence to the prediction, hypothesis or alternative it is incompatible with |
| `replicates` | an independent finding of the same result as the target | from the independent finding to the claim it reproduces |
| `requires` | a claim depends on another holding | from the dependent claim to its prerequisite: the source would be invalid if the target were false |
| `rules-out` | the source's evidence eliminates the target as an explanation | from the control or evidence to the alternative explanation it eliminates — a claim the paper entertains or rejects, never one it asserts |
| `scopes` | a scope constraint governs another claim's validity | from the scope claim to the claims it bounds, or to `*` for every empirical claim in the paper |
| `supports` | the source provides evidence for the target | from the evidence to the claim it is evidence for |
| `tests` | an empirical result tests the target prediction, closing the loop | from the empirical result to the prediction it tests |
| `validates` | a control whose specific result strengthens the target's warrant | from the control to the claim whose warrant it strengthens |

### One example of each

- `confirms`: `guilt-reduces-happiness-after-partner-loss` → `hypothesis-insula-tracks-interpersonal-guilt` (Gadeke). Source: “Happiness ratings decrease more after negative partner outcomes when the participant made the choice (Social condition) than when the partner made the choice (Partner condition), operationalizing interpersonal guilt as responsibility-contingent unhappiness about partner harm.” Target: “Anterior insula is the neural substrate of interpersonal guilt: when a participant bears responsibility for a choice that yields a negative outcome for another person, anterior insula activity tracks the resulting responsibility-contingent affect. The region is recruited specifically by the conjunction of self-agency over the choice and harm to the partner, distinguishing guilt from generic empathy for partner loss (which would be present in the Partner condition too) and from regret about one's own loss (which would be present in Solo trials too).”
- `contradicts`: no use in the corpus yet.
- `derived-from`: `prediction-distal-dendritic-spike-mechanism` → `hypothesis-distinct-compartmental-roles` (Headley). Source: “If perisomatic and distal dendritic inhibition serve dissociated computational roles, then doubling distal dendritic inhibition should reduce somatic firing primarily by suppressing apical Ca²⁺ and NMDA dendritic spikes, with little change in the somatic AP voltage threshold.” Target: “Perisomatic and distal dendritic inhibition serve distinct computational roles in layer 5 pyramidal neurons: perisomatic inhibition principally regulates somatic action potential generation (gain and threshold of axonal output), while distal dendritic inhibition principally regulates dendritic spike incidence and the temporal coupling of dendritic spikes to somatic APs.”
- `dissociates-with`: `distal-inhib-drops-firing-02hz` → `perisomatic-inhib-drops-firing-07hz` (Headley). Source: “Doubling the strength of distal dendritic inhibition reduces somatic firing rate from a baseline of approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing the occurrence of dendritic Ca²⁺ and NMDA spikes rather than by directly raising AP threshold.” Target: “Doubling perisomatic inhibition reduces somatic firing from approximately 5.5 Hz to approximately 0.7 Hz by elevating action potential voltage threshold, while dendritic spike rates are relatively preserved.”
- `enables-method`: `preregistered-design-validates-mvpa` → `foveal-v1-decodes-peripheral-saccade-target` (Kammer). Source: “The preregistered analysis plan (osf.io/rxacd) specifies the MVPA decoding pipeline, ROI definitions, and statistical tests in advance, reducing the risk of analytic flexibility inflating the decoding accuracy results.” Target: “Saccade target identity (4 stimuli varying in shape and semantic category) can be decoded from foveal V1 BOLD signal above chance in the experimental condition where targets disappear before fixation: 57.43% accuracy (t(27)=8.81, p<0.001), significantly above 50% chance.”
- `entails`: `hypothesis-distinct-compartmental-roles` → `prediction-distal-dendritic-spike-mechanism` (Headley). Source: “Perisomatic and distal dendritic inhibition serve distinct computational roles in layer 5 pyramidal neurons: perisomatic inhibition principally regulates somatic action potential generation (gain and threshold of axonal output), while distal dendritic inhibition principally regulates dendritic spike incidence and the temporal coupling of dendritic spikes to somatic APs.” Target: “If perisomatic and distal dendritic inhibition serve dissociated computational roles, then doubling distal dendritic inhibition should reduce somatic firing primarily by suppressing apical Ca²⁺ and NMDA dendritic spikes, with little change in the somatic AP voltage threshold.”
- `extends`: `guilt-signature-no-individual-difference` → `insula-guilt-replicates-yu-koban-signature` (Gadeke). Source: “Individual dot-product values between participants' guilt-related BOLD responses and the Yu & Koban neural guilt signature do not correlate with individual behavioral guilt effect scores (Spearman's Rho=−0.058, p=0.725), indicating the neural signature does not track individual differences in guilt sensitivity as measured behaviorally.” Target: “The anterior insula guilt effect is consistent with a previously published neural guilt signature map (Yu & Koban), providing convergent validity for the insula as a guilt-tracking region.”
- `interprets`: `pv-gamma-sst-beta-correspondence` → `beta-optimal-distal-dendritic-entrainment` (Headley). Source: “The model provides mechanistic grounding for the empirical association of parvalbumin-positive interneurons with gamma rhythms and somatostatin-positive interneurons with beta rhythms: PV+ neurons target perisomatic locations where gamma is optimal for AP threshold modulation, while SST+ neurons target distal dendrites where beta is optimal for dendritic spike entrainment.” Target: “In a frequency sweep from 0.5 to 80 Hz, beta frequencies near 20 Hz produce the strongest phase-dependent entrainment of dendritic Ca²⁺ and NMDA spike onsets by distal rhythmic inhibition, as measured by Pairwise Phase Consistency.”
- `opposes`: no use in the corpus yet.
- `predicts`: `hypothesis-state-switch-by-5ht` → `5ht-stim-dilates-pupil` (Meijer). Source: “A phasic burst of serotonin release from the dorsal raphe nucleus drives a rapid switch in internal arousal/behavioral state in the awake quiescent animal — from an "offline" state characterized by low arousal, hippocampal sharp-wave ripples, and minimal exploratory movement, to an "online" state characterized by pupil dilation, ripple suppression, and active exploration (whisking, sniffing).” Target: “A 1-second optogenetic activation of dorsal-raphe serotonergic neurons in SERT-Cre mice produces a significant increase in pupil size relative to baseline, with the divergence from wild-type controls becoming significant approximately 2 seconds after stimulation offset.”
- `qualifies`: `risk-premiums-null-social-solo` → `solo-vs-social-choice-difference` (Gadeke). Source: “Risk premiums do not differ between Solo and Social conditions in either study (Study 1: t(39)=1.53, p=0.134, Cohen's d=0.24, BF10=0.49; Study 2: t(43)=−0.21, p=0.84, d=−0.03, BF10=0.17), providing evidence against social-context-driven changes in risk aversion in this paradigm.” Target: “Participants chose lotteries more often in the Solo condition than in the Social condition in Study 1 (t(4796)=2.54, p=0.011, β=0.164, 95%CI=[0.038, 0.291]) but not in Study 2 (t(3829)=0.23, p=0.82, β=0.015), suggesting a weak and inconsistent effect of social context on risk-taking that does not replicate across studies.”
- `refutes`: `5ht-stim-leaves-decision-behavior-intact` → `prediction-5ht-shifts-psychometric` (Meijer). Source: “In the IBL steering-wheel perceptual decision-making task, optogenetic activation of dorsal-raphe serotonergic neurons starting at visual stimulus onset and lasting until choice (or 1 s, whichever is shorter) produces no detectable change in any of: psychometric slope (visual acuity), bias (prior influence), lapse rate (motivation), percent-correct, median reaction time, the speed of choice-bias updating after a prior-probability block switch, or the per-predictor weights of a probabilistic choice model fitting visual evidence, prior, and past choice with separate stimulated / unstimulated coefficients.” Target: “If phasic 5-HT release alters how the animal weighs sensory evidence against prior expectation, or alters motivation, attention, or visual sensitivity, then 5-HT stimulation should produce detectable changes in psychometric slope, lapse rate, bias, reaction time, or any of the predictor weights of a probabilistic choice model fitting visual evidence, prior, and past choice with separate stimulated/unstimulated coefficients.”
- `replicates`: no use in the corpus yet.
- `requires`: `distal-inhib-drops-firing-02hz` → `l5-model-single-cell-scope` (Headley). Source: “Doubling the strength of distal dendritic inhibition reduces somatic firing rate from a baseline of approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing the occurrence of dendritic Ca²⁺ and NMDA spikes rather than by directly raising AP threshold.” Target: “All results derive from a single-cell compartmental model of one layer 5 pyramidal neuron; no network dynamics, recurrent excitation, or population-level inhibitory effects are simulated, and all firing rate effects are for a single isolated neuron receiving naturalistic presynaptic drive.”
- `rules-out`: `agency-reduces-happiness` → `alt-agency-aversion-not-guilt` (Gadeke). Source: “Being the decision-maker (Social + Solo vs Partner condition) reduces participant happiness independently of outcome (Study 1: t(3600)=−3.92, p<0.0001, β=−0.14, 95%CI=[−0.20, −0.07]; Study 2: t(2870)=−6.07, p<0.0001, β=−0.24, 95%CI=[−0.31, −0.16]), consistent with a psychological cost of assuming responsibility for others.” Target: “The happiness cost observed in the Social condition is general agency aversion — the unpleasantness of being the decision-maker as such — and is not contingent on responsibility for a negative outcome befalling the partner.”
- `scopes`: `l5-model-single-cell-scope` → `*` (Headley). “All results derive from a single-cell compartmental model of one layer 5 pyramidal neuron; no network dynamics, recurrent excitation, or population-level inhibitory effects are simulated, and all firing rate effects are for a single isolated neuron receiving naturalistic presynaptic drive.” — bounds every empirical claim in the paper.
- `supports`: `distal-inhib-drops-firing-02hz` → `hypothesis-distinct-compartmental-roles` (Headley). Source: “Doubling the strength of distal dendritic inhibition reduces somatic firing rate from a baseline of approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing the occurrence of dendritic Ca²⁺ and NMDA spikes rather than by directly raising AP threshold.” Target: “Perisomatic and distal dendritic inhibition serve distinct computational roles in layer 5 pyramidal neurons: perisomatic inhibition principally regulates somatic action potential generation (gain and threshold of axonal output), while distal dendritic inhibition principally regulates dendritic spike incidence and the temporal coupling of dendritic spikes to somatic APs.”
- `tests`: `distal-inhib-drops-firing-02hz` → `prediction-distal-dendritic-spike-mechanism` (Headley). Source: “Doubling the strength of distal dendritic inhibition reduces somatic firing rate from a baseline of approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing the occurrence of dendritic Ca²⁺ and NMDA spikes rather than by directly raising AP threshold.” Target: “If perisomatic and distal dendritic inhibition serve dissociated computational roles, then doubling distal dendritic inhibition should reduce somatic firing primarily by suppressing apical Ca²⁺ and NMDA dendritic spikes, with little change in the somatic AP voltage threshold.”
- `validates`: `guilt-effect-independent-of-own-outcome` → `guilt-reduces-happiness-after-partner-loss` (Gadeke). Source: “The guilt effect (happiness decrease after low partner outcomes under participant vs partner choice) is present regardless of whether the participant received the high or low lottery outcome: high own outcome: Study 1 t(39)=−3.58, p<0.001, d=0.56, BF10=32; Study 2 t(43)=−2.68, p=0.01, d=0.40, BF10=3.8; low own outcome: Study 1 t(39)=−3.39, p=0.002, d=0.54, BF10=19; Study 2 t(43)=−3.58, p<0.001, d=0.54, BF10=33.5.” Target: “Happiness ratings decrease more after negative partner outcomes when the participant made the choice (Social condition) than when the partner made the choice (Partner condition), operationalizing interpersonal guilt as responsibility-contingent unhappiness about partner harm.”

### Relations that are confused for each other

**`requires` versus `supports`.** `requires` is a dependency: if the target were false the source would be invalid. `supports` is evidence: the source makes the target more credible and would survive its falsity. One empirical claim commonly carries both — it *requires* the scope claim that bounds the model it was computed in, and *supports* the hypothesis it was run to test.

**`entails` versus `tests`.** Both connect a hypothesis's arc, in opposite directions and from different roles. `entails` runs *down* from the hypothesis to a prediction and is deductive: the prediction follows if the hypothesis holds. `tests` runs *up* from an empirical result to the prediction it checks. A result never `entails` anything; a hypothesis never `tests`.

**`rules-out` versus `refutes`.** `rules-out` eliminates an alternative explanation — a claim the paper raises in order to reject, which has a node of its own with stance `entertains` or `rejects`. `refutes` is aimed at one of the paper's own predictions or hypotheses that the evidence came out against; a paper refuting its own prediction is the hypothetico-deductive loop closing. Never aim `rules-out` at a claim the same paper asserts.

**`dissociates-with` versus `contradicts`.** `dissociates-with` joins two results that are both true and *differ*: the contrast between them is the finding, and neither undermines the other. `contradicts` says two claims cannot both hold. Two conditions producing different effects is a dissociation, not a contradiction.

**`scopes` versus `requires`.** A scope claim bounds what a result can mean and is written from the scope claim *to* the results it bounds (or to `*`). `requires` is written from the result *to* what it depends on. The same pair of claims can carry both, in opposite directions: the result requires the scope; the scope scopes the result.

**`validates` versus `supports`.** `validates` is a control's edge: a check whose specific outcome (a null where a confound would have produced an effect, a sign-flip, a manipulation check) strengthens the warrant for a target. `supports` is ordinary evidence for a proposition. A control `validates`; a main result `supports`.

## Confidence

A reader marks its own claim:

- `high` — asserted directly in the text the reader was given, with a quotable sentence
- `tentative` — read between the lines, summarised across sentences, or ambiguous in the source; say why in `notes`

After reconciliation a claim's confidence is a fact about agreement between readers, not about the world:

- `high` — more than one reader surfaced the same proposition and they agree on its panel and its direction
- `contested` — more than one reader surfaced it and they disagree — about the panel, the direction, or whether it is a hypothesis, a prediction or a result. Record what each said in `notes`
- `single-source` — one reader surfaced it. Expected for panel-level numerics (caption reader only), scope and methodological claims (structure reader only) and synthesis (results reader only); not a mark against the claim
