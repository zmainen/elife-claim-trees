# Self-association enhances early attentional selection through automatic prioritization of socially salient signals

<!-- scheller-2026-self-prioritization · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Efficiently processing self-related information is critical for cognition, yet the earliest mechanisms enabling this self-prioritization in humans remain unclear.

By combining a temporal order judgement task with computational modeling based on the Theory of Visual Attention (TVA), we show how mere, arbitrary associations with the self can fundamentally alter attentional selection of sensory information into aware short-term memory, by enhancing the attentional weights and processing capacity devoted to encoding socially loaded information.

This self-prioritization in attentional selection occurs automatically at early perceptual stages but reduces when active social decoding is required.

Importantly, the processing benefits obtained from attentional selection via self-relatedness and via physical salience were additive, suggesting that social and perceptual salience captured attention via separate mechanisms.

Furthermore, intra-individual correlations revealed an ‘obligatory’ self-prioritization effect, whereby self-relatedness overpowered the contribution of perceptual salience in guiding attentional selection.

Together, our findings provide evidence for the influence of self-relatedness during earlier, automatic stages of attentional selection at the gateway to perception, distinct from later post-attentive processing stages.


## results

Results Does mere self-association lead to a bias in early attentional selection, and what are the underlying mechanisms?

To assess whether and how self-association leads to biases in early attentional selection, we estimated TVA-based parameters within a hierarchical Bayesian estimation procedure.

Parameters were estimated by embedding the TVA-based TOJ equation ( Equation 1 ) for the probability of reporting the probe stimulus as appearing first in hierarchical Bayesian models ( Tünnermann et al., 2015 ).

The model structure ( Figure 4 ) shows that parameters were estimated, for each participant and each condition: the neutral baseline condition (N) and the social salience condition (S) with the social decision dimension.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{The model structure ( Figure 4 ) shows that parameters were estimated, for each participant and each condition: the neutral baseline condition (N) and the social salience condition (S) with the social decision dimension.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Within both conditions, the self-associated shape (salient) was defined as the probe, and the other-associated shape (non-salient) was defined as the reference.

Crucially, the neutral baseline condition was used as an individual-specific correction, allowing us to measure the effects that were induced by social salience alone.

Hence, any individual-specific biases or processing differences are corrected in the reported parameter values, which is indicated in the change scores ( w p e f f e c t \begin{document}$w_{peffect}$\end{document} , C e f f e c t \begin{document}$C_{effect}$\end{document} , Δ v p \begin{document}$\Delta v_{p}$\end{document} , and Δ v r \begin{document}$\Delta v_{r}$\end{document} ).

Figure 4. Model structure and cross-experimental social salience effects.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Figure 4. Model structure and cross-experimental social salience effects.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Hierarchical model structure shows how the parameters of interest ( w p e f f e c t \begin{document}$w_{peffect}$\end{document} , C e f f e c t \begin{document}$C_{effect}$\end{document} , Δ v p \begin{document}$\Delta v_{p}$\end{document} , and Δ v r \begin{document}$\Delta v_{r}$\end{document} ) were estimated from within-participant differences between the neutral baseline (gray) and social salience (blue) condition.

The better model is depicted, in which processing capacity was estimated for each condition separately, suggesting that changes in absolute processing rates, rather than relative attentional weights, have been underlying attentional selection effects of social salience.

Mathematical formalization of the relation between the model nodes is given on the right.

Density plots indicate the highest density estimates for the different processing parameters of interest.

Neutral baseline parameters are given in absolute parameter values, with processing capacity shown as items/ms and the relative attentional weight for the probe (a shape that was subsequently associated with the self).

Social salience parameters are shown in change scores, relative to baseline, depicting an increase and decrease in processing capacity and attentional weight, respectively.

Absolute processing rate changes for the probe (self-associated) and reference (other-associated) shapes, as well as their relative change, are shown on the bottom right.

Figure 4—figure supplement 1. Individual estimates: Absolute processing rates ( v p \begin{document}$v_{p}$\end{document} ) for the probe stimulus (self-associated), shown for individual participants for the social baseline (gray; v p B a s e S o c \begin{document}$v_{pBaseSoc}$\end{document} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c \begin{document}$v_{pSoc}$\end{document} ).⟦>zach claim=no-assertion: @{Figure 4—figure supplement 1. Individual estimates: Absolute processing rates ( v p \begin{document}}$v_{p}}$\end{document}} ) for the probe stimulus (self-associated), shown for individual participants for the social baseline (gray; v p B a s e S o c \begin{document}}$v_{pBaseSoc}}$\end{document}} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c \begin{document}}$v_{pSoc}}$\end{document}} ).} A supplementary-figure title with its colour key; it names what is plotted rather than stating a result.⟧

Points show the estimated posterior means, thick lines indicate the central quartiles, and thin lines indicate the 95 highest density interval.

Processing rates are given in items/ms.

To arbitrate between the mechanisms underlying effects of social salience, we compared two models, applied to data from two experiments ( N \begin{document}$N$\end{document} =140): one that estimated a single processing capacity parameter across conditions, and one that estimated processing capacity parameters for every single condition.

These define different assumptions we may have about the mechanisms underlying the attentional selection of socially relevant information.

If more or fewer processing resources are required to encode socially relevant information into visual short-term memory, we would expect a condition-specific change in processing capacity.

This should favor the model that estimates condition-specific processing C \begin{document}$C$\end{document} s.

On the other hand, if the same processing resources are used for encoding and selecting neutral and socially relevant information, but distributed differently, this should be reflected in a better fit of a model with a single C \begin{document}$C$\end{document} parameter.

We used the leave-one-out (loo) cross-validation Information Criterion ( Vehtari et al., 2017 ), which accounts for model complexity, to compare a model with condition-specific C \begin{document}$C$\end{document} parameters vs a model with a single, condition-unspecific C \begin{document}$C$\end{document} parameter.

This comparison showed that the best estimated model used condition-specific C \begin{document}$C$\end{document} parameters ( Δ l o o \begin{document}$\Delta{loo}$\end{document} = 14.2; Δ s e \begin{document}$\Delta{se}$\end{document} = 6.41; w e i g h t i n d i v \begin{document}$weight_{indiv}$\end{document} = 0.86, which can loosely be interpreted as the probability of the model compared to the other).

Consequently, social salience introduced not only a change in attentional weights across the perceptual objects, but also a change in processing capacity (see Figure 1c ).⟦>zach claim=24c24fef-2404-41a6-a0ea-edfe81cd3707: @{Consequently, social salience introduced not only a change in attentional weights across the perceptual objects, but also a change in processing capacity (see Figure 1c ).} tva-capacity-model-wins — This is the conclusion of the model comparison: social salience changed absolute processing capacity, not only the relative attentional weights.⟧

Hence, changes in absolute processing rates, rather than relative attentional weights, are underlying attentional selection effects of social salience.

The full model structure of the better model is depicted in Figure 4 .⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{The full model structure of the better model is depicted in Figure 4 .} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Note that changes in absolute processing rates, relative to baseline, were estimated for each of the perceptual objects separately: the self-associated shape, defined as the probe ( Δ v p \begin{document}$\Delta v_{p}$\end{document} ), and the other-associated shape, defined as the reference ( Δ v r \begin{document}$\Delta v_{r}$\end{document} ).

Inspecting the impact of social association on processing rates, relative to the neutral baseline condition, showed a relative processing advantage for the other-associated stimulus (i.e. Δ v r > Δ v p \begin{document}$\Delta v_{r} \gt \Delta v_{p} $\end{document} ).

That is, surprisingly, the other-associated stimulus was processed 1.2 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0 to 2.4] Hz faster after social association, while the self-associated stimulus was processed 0.26 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –1.4 to 0.93] Hz slower.

Relatively, there was an advantage of the other-associated stimulus over the self-associated stimulus of 1.5 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0.45 to 2.5] Hz.

Across perceptual objects, there was a slight increase in processing capacity C \begin{document}$C$\end{document} from 53 Hz to 54 Hz; however, the evidence for a substantial increase was not strong (75.6% of the HDI suggested an increase in processing capacity; Figure 4 ).⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Across perceptual objects, there was a slight increase in processing capacity C \begin{document}}$C$\end{document}} from 53 Hz to 54 Hz; however, the evidence for a substantial increase was not strong (75.6% of the HDI suggested an increase in processing capacity; Figure 4 ).} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

The mean of the relative attentional weight of the self-associated perceptual object was 0.50 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0.50 to 0.51] at baseline, suggesting there were no strong object-specific biases at the group level.

After social association, there was a decrease in relative attentional weight attributed to the self-associated stimulus to 0.488 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0.474 to 0.498].

This cross-experimental parameter inspection revealed that participants exhibited an attentional selection bias toward socially associated information.

Interestingly, enhanced processing speed was observed for other-associated rather than self-associated information, a pattern that diverged from our prediction.

Does self-relatedness bias attentional selection automatically or does it require explicit social decoding?

(Experiment 1) Changing the decisional dimension, either requiring explicit decoding of the social associations, or merely the perceptual features, allowed testing whether social relevance biases attentional selection automatically at perceptual feature representations or whether it requires explicit decoding of the social identity.

The differentiation between these mechanisms holds the inherent assumption that automatic alterations in the perceptual feature representation are faster, while active decoding of the social identity requires more processing time.

Indeed, an exploratory analysis on reaction time data showed that participants responded significantly quicker in the perceptual decision dimension (RT μ : 763.91 [ C I 95 \begin{document}$CI^{95}$\end{document} : 729 to 799]ms) than in the social decision dimension (RT μ : 897.33 [ C I 95 \begin{document}$CI^{95}$\end{document} : 850 to 944]ms; B F 10 = 1.064 1011 \begin{document}$BF_{10}=1.064^{1011}$\end{document} ).

Note that the order in which the perceptual decision dimension and social decision dimensions were tested was counterbalanced across participants, ruling out the possibility that the reaction time difference was merely a training effect.

Instead, this may suggest that additional processing stages were involved in the condition that required active decoding of the social identity association.

To assess whether, in line with the cross-experimental analysis, processing capacity changes contributed to explaining the attentional selection of socially relevant information, we conducted model comparisons on all conditions included in this experiment: neutral baseline, social salience with the perceptual decision, social salience with the social decision.

In Experiment 1 ( N =69), the condition-specific individual C \begin{document}$C$\end{document} model ( Figure 5 ) was favored ( Δ l o o \begin{document}$\Delta{loo}$\end{document} = 7.65; Δ s e \begin{document}$\Delta{se}$\end{document} = 6.07; w e i g h t i n d i v \begin{document}$weight_{indiv}$\end{document} = 0.71).⟦>zach claim=121d0b37-99b6-459e-8093-bce99c94b708: @{In Experiment 1 ( N =69), the condition-specific individual C \begin{document}}$C$\end{document}} model ( Figure 5 ) was favored ( Δ l o o \begin{document}}$\Delta{loo}}$\end{document}} = 7.65; Δ s e \begin{document}}$\Delta{se}}$\end{document}} = 6.07; w e i g h t i n d i v \begin{document}}$weight_{indiv}}$\end{document}} = 0.71).} scope-toj-tva-paradigm⟧

This, as above, suggested that social salience introduced changes in relative attentional weights and processing capacity, hence, in the absolute processing rates.

Figure 5. Social salience effects with different decision dimensions.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Figure 5. Social salience effects with different decision dimensions.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Hierarchical model structure shows how social salience effects were estimated between social salience conditions (blue: social decision dimension; turquoise: perceptual decision dimension) and the neutral baseline condition (gray; see Figure 4 caption for details and formalizations) in Experiment 1. The right plot shows how relative processing rates were calculated, at the individual participant level, from social salience-induced processing rate changes for the self-associated and other-associated shapes.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Hierarchical model structure shows how social salience effects were estimated between social salience conditions (blue: social decision dimension; turquoise: perceptual decision dimension) and the neutral baseline condition (gray; see Figure 4 caption for details and formalizations) in Experiment 1. The right plot shows how relative processing rates were calculated, at the individual participant level, from social salience-induced processing rate changes for the self-associated and other-associated shapes.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Density plots indicate the group-level highest density intervals for the processing capacity and absolute processing rate estimates, given in items/ms.

Additionally, the 95% HDIs are presented alongside the group means.

The relative change in processing rates ( Δ v p − Δ v r \begin{document}$\Delta v_{p}-\Delta v_{r}$\end{document} ) can be interpreted directly as the processing rate advantage of the self-associated over the other-associated stimuli.

Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplement 1 and 2 , respectively.⟦>zach claim=no-assertion: @{Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplement 1 and 2 , respectively.} A pure cross-reference pointing to where the individual-participant data live.⟧

Figure 5—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.⟦>zach claim=no-assertion: @{Figure 5—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.} A supplementary-figure title describing what the individual psychometric functions plot, with no finding.⟧

Different conditions are shown in different shadings.

The panel on the right shows an example participant with a group-representative response pattern: an increase of ‘probe first’ responses when the probe was self-associated and the shape of the stimulus had to be reported.

This pattern is specifically visible at low onset asynchronies.

Furthermore, this participant shows a decreased proportion of ‘probe first’ responses when the probe was self-associated and the social identity had to be reported.

Figure 5—figure supplement 2. Individual estimates: absolute processing rates ( v p \begin{document}${v}_{p}$\end{document} ) for the probe stimulus (self-associated), shown for individual participants in Experiment 1. Different colors indicate different conditions: the baseline (gray; v p B a s e \begin{document}$v_{pBase}$\end{document} ), the social salience condition in which the shape had to be reported (light blue; v p S o c P e r \begin{document}$v_{pSocPer}$\end{document} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c S o c \begin{document}$v_{pSocSoc}$\end{document} ).⟦>zach claim=no-assertion: @{Figure 5—figure supplement 2. Individual estimates: absolute processing rates ( v p \begin{document}}${v}}_{p}}$\end{document}} ) for the probe stimulus (self-associated), shown for individual participants in Experiment 1. Different colors indicate different conditions: the baseline (gray; v p B a s e \begin{document}}$v_{pBase}}$\end{document}} ), the social salience condition in which the shape had to be reported (light blue; v p S o c P e r \begin{document}}$v_{pSocPer}}$\end{document}} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c S o c \begin{document}}$v_{pSocSoc}}$\end{document}} ).} A supplementary-figure title with its colour key for the three conditions, stating no outcome.⟧

Points show the estimated posterior means, thick lines indicate the central quartiles, and thin lines indicate the 95 highest density interval.

Processing rates are given in items/ms.

Relative to the neutral baseline condition, self-associated stimuli showed increased absolute processing rates compared to other-associated stimuli (i.e. Δ v p − Δ v r \begin{document}$\Delta v_{p}-\Delta v_{r}$\end{document} ).

However, this was only the case when participants were asked to report which perceptual object flickered first, that is in the perceptual decision dimension ( Figure 5 ).⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{However, this was only the case when participants were asked to report which perceptual object flickered first, that is in the perceptual decision dimension ( Figure 5 ).} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Here, the self-associated stimulus was processed 1.5 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –0.16 to 3.2] Hz faster than the other-associated stimulus.

This was driven by an overall increase in processing capacity by 2.6 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –1.7 to 6.8] Hz, specifically for the self-associated stimulus (2.1 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0.13 to 4.1] Hz).

The processing rate for the other-associated stimulus did not show a consistent increase (0.53 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –1.4 to 2.5] Hz).

When participants had to report whose shape flickered first based on the social association, there was no advantage of the self-associated stimulus (0.87 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –0.96 to 2.7] Hz; Figure 5 ).⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{When participants had to report whose shape flickered first based on the social association, there was no advantage of the self-associated stimulus (0.87 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : –0.96 to 2.7] Hz; Figure 5 ).} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Instead, the Bayesian parameter estimates provided more evidence in favor of the other-associated stimulus (1.2 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –0.78 to 3.1] Hz) being processed faster (0.29 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –1.9 to 1.3] Hz), in line with the cross-experimental analysis (63.9% of the HDI suggested an advantage of the other-associated stimulus).

Results from experiment 2 demonstrated a faster, more automatic attentional selection for self-associated information when the decision did not require explicit social decoding.

When the social identity had to be judged, processing speed for self-associated information decreased.

Contrary to the hypothesis that social decoding is necessary for self-prioritization to emerge, these findings suggest that attentional selection can operate automatically to prioritize self-associated information.

Does self-association affect attentional selection in a similar way to perceptual salience, and how do social and perceptual salience interact with each other?

(Experiment 2) To investigate the similarities and interactions between social and perceptual salience in attentional selection, we asked participants ( N \begin{document}$N$\end{document} =71) to complete the TOJ task with socially salient (shape) and perceptually salient (local color) stimuli separately, as well as together.

As such, there were four conditions of interest: mere social salience (social decision dimension), mere perceptual salience, social + perceptual salience (self perceptually salient), social + perceptual salience (other perceptually salient).

Similar to the previous experiment, participants completed a baseline task to reduce the effects of any participant-specific pre-existing biases.

Note that the definition of the probe differed between the mere perceptual and mere social salience conditions and required the neutral baseline condition to be coded accordingly.

This did not affect the stimulus presentation in any way, but merely the interpretation of the ‘probe’: in the social salience condition and the respective neutral baseline condition, the probe was always a specific shape.

In the perceptual salience condition and the respective neutral baseline condition, the probe was randomly defined as one of the two shapes on each trial.

This is because, in the perceptual salience condition, the local color that feature induced salience had a random chance of affecting each shape.

As such, the probe in the baseline was always defined in such a way that it provided a direct comparison for the respective salience condition.

To quantitatively assess the interaction of perceptual and social salience, the effect of perceptual salience was measured with the same defined probe as the perceptual salience condition; however, after shapes had been associated with social identities.

This allowed us to draw direct comparisons between the effects of perceptual salience on self- versus other-associated perceptual objects.

In contrast to the previous experiment, the single- C \begin{document}$C$\end{document} model was favored in this experiment ( Δ l o o \begin{document}$\Delta loo$\end{document} = 33.0; Δ s e \begin{document}$\Delta se$\end{document} = 9.96; weight single = 0.84).

Notably, while this affects the interpretation of underlying mechanisms of social and perceptual salience manipulations together, we report changes in processing rates for consistency and comparability.

As absolute processing rates indicate the product of processing capacity and relative attentional weight, a non-meaningful change in processing capacity does not alter the interpretation of processing rates.

Hence, changes in relative processing rates (self/other, salient/non-salient) can be interpreted in the same way between experiments.

Across conditions, there was a slight decrease in processing capacity: mere social salience: –1.3 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –5.3 to 0.28] Hz; mere perceptual salience: –0.92 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –3.9 to 2.1] Hz; social + perceptual salience (self): –1.9 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –5.5 to 1.8] Hz; social + perceptual salience (other): –1.1 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –5.6 to 3.5] Hz.

As indicated in the cross-experimental analysis, the processing rates for other-associated stimuli showed a relative processing advantage compared to self-associated stimuli (i.e. Δ v r > Δ v p \begin{document}$\Delta v_{r} \gt \Delta v_{p}$\end{document} > Δ v p \begin{document}$\Delta v_{p}$\end{document} ; –1.6 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –3 to –0.26] Hz), relative to the neutral baseline condition ( Figure 6 , blue).⟦>zach claim=08433979-b40e-4b78-91f6-80537bb4c971: @{As indicated in the cross-experimental analysis, the processing rates for other-associated stimuli showed a relative processing advantage compared to self-associated stimuli (i.e. Δ v r > Δ v p \begin{document}}$\Delta v_{r}} \gt \Delta v_{p}}$\end{document}} > Δ v p \begin{document}}$\Delta v_{p}}$\end{document}} ; –1.6 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : –3 to –0.26] Hz), relative to the neutral baseline condition ( Figure 6 , blue).} other-association-advantage-social-condition⟧

Here, the processing rate of the self-associated stimulus decreased by 1.3 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –5.3 to 0.28] Hz, while the processing rate of the other-associated stimulus stayed approximately the same, with a 0.17 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –1.6 to 1.9] Hz increase.

Figure 6. Social and perceptual salience effects.⟦>zach claim=08433979-b40e-4b78-91f6-80537bb4c971: @{Figure 6. Social and perceptual salience effects.} other-association-advantage-social-condition⟧

Hierarchical model structure shows how social salience only (blue) and perceptual salience only (orange) effects were estimated relative to their respective neutral baseline conditions (gray; see Figure 4 caption for formalizations and main text for details) in Experiment 2. To assess processing parameters for the interaction of social and perceptual salience (purple, pink), we calculated change scores, indicative of perceptual salience effects, relative to the perceptual neutral baseline.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Hierarchical model structure shows how social salience only (blue) and perceptual salience only (orange) effects were estimated relative to their respective neutral baseline conditions (gray; see Figure 4 caption for formalizations and main text for details) in Experiment 2. To assess processing parameters for the interaction of social and perceptual salience (purple, pink), we calculated change scores, indicative of perceptual salience effects, relative to the perceptual neutral baseline.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

This can be interpreted as the effect of perceptual salience that is present when shapes are associated with the own or another social identity.

Density plots indicate the group-level highest density intervals for the processing capacity and processing speed estimates, given in items/ms.

Additionally, the 95% HDIs are presented alongside the group means.

The relative speed change ( Δ v p − Δ v r \begin{document}$\Delta v_{p}-\Delta v_{r}$\end{document} ) can be interpreted directly as the processing rate advantage of the self-associated over the other-associated stimuli (social salience only), or the perceptually salient over the perceptually non-salient stimuli (perceptual salience only, social + perceptual salience).

Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplements 1 and 2 , respectively.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplements 1 and 2 , respectively.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Figure 6—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.⟦>zach claim=no-assertion: @{Figure 6—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.} A supplementary-figure title describing what the individual psychometric functions plot, with no finding.⟧

Different conditions are shown in different shadings.

Figure 6—figure supplement 2. Individual estimates: Absolute processing rates ( v p \begin{document}$v_{p}$\end{document} ) for the probe stimulus (perceptually salient), shown for individual participants for the baseline (gray; v p B a s e \begin{document}$v_{pBase}$\end{document} ), for the mere perceptual salience condition (orange; v p P e r c \begin{document}$v_{pPerc}$\end{document} ), for the perceptual salience condition in which the probe was self-associated (purple; v p P e r S e l f \begin{document}$v_{pPerSelf}$\end{document} ), and the perceptual salience condition in which the probe was other-associated (pink; v p P e r O t h e r \begin{document}$v_{pPerOther}$\end{document} ).⟦>zach claim=no-assertion: @{Figure 6—figure supplement 2. Individual estimates: Absolute processing rates ( v p \begin{document}}$v_{p}}$\end{document}} ) for the probe stimulus (perceptually salient), shown for individual participants for the baseline (gray; v p B a s e \begin{document}}$v_{pBase}}$\end{document}} ), for the mere perceptual salience condition (orange; v p P e r c \begin{document}}$v_{pPerc}}$\end{document}} ), for the perceptual salience condition in which the probe was self-associated (purple; v p P e r S e l f \begin{document}}$v_{pPerSelf}}$\end{document}} ), and the perceptual salience condition in which the probe was other-associated (pink; v p P e r O t h e r \begin{document}}$v_{pPerOther}}$\end{document}} ).} A supplementary-figure title with its colour key for the four conditions, stating no outcome.⟧

Points show the estimated posterior means, thick lines indicate the central quartiles, and thin lines indicate the 95 highest density interval.

Processing rates are given in items/ms.

Assessing the effects of mere perceptual salience on processing suggested an increase in the salient stimulus, relative to the non-salient stimulus (i.e. Δ v p > Δ v r \begin{document}$\Delta v_{p}\gt \Delta v_{r}$\end{document} ; 6 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 4.6 to 7.3] Hz; Figure 6 , orange).⟦>zach claim=08433979-b40e-4b78-91f6-80537bb4c971: @{Assessing the effects of mere perceptual salience on processing suggested an increase in the salient stimulus, relative to the non-salient stimulus (i.e. Δ v p > Δ v r \begin{document}}$\Delta v_{p}}\gt \Delta v_{r}}$\end{document}} ; 6 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : 4.6 to 7.3] Hz; Figure 6 , orange).} other-association-advantage-social-condition⟧

This was driven both by an increase in processing rates of the salient (2.5 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0.8 to 4.2] Hz) and a decrease in processing rates of the non-salient (–3.4 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –4.9 to –2] Hz) stimuli.

Taken together, as also confirmed in the cross-experimental analysis, attentional selection favored the other-related information when social identity had to be judged.

In contrast, perceptual salience, as predicted, led to increased processing speed for the more salient stimulus.

Presenting stimuli that were both self-associated and perceptually salient reduced the relative processing rate advantage of perceptual salience ( Figure 6 , purple).⟦>zach claim=08433979-b40e-4b78-91f6-80537bb4c971: @{Presenting stimuli that were both self-associated and perceptually salient reduced the relative processing rate advantage of perceptual salience ( Figure 6 , purple).} other-association-advantage-social-condition⟧

That is, while there was still a processing rate increase of perceptually salient, self-associated stimuli (2.5 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 0.86 to 4.1] Hz), it was much smaller compared to perceptually salient, non-associated stimuli (6 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 4.6 to 7.3] Hz) or other-associated stimuli (5.2 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : 3.6 to 6.9] Hz; Figure 6 , pink).⟦>zach claim=08433979-b40e-4b78-91f6-80537bb4c971: @{That is, while there was still a processing rate increase of perceptually salient, self-associated stimuli (2.5 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : 0.86 to 4.1] Hz), it was much smaller compared to perceptually salient, non-associated stimuli (6 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : 4.6 to 7.3] Hz) or other-associated stimuli (5.2 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : 3.6 to 6.9] Hz; Figure 6 , pink).} other-association-advantage-social-condition⟧

This was specifically driven by a smaller processing rate increase towards the salient, self-associated stimulus (0.78 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –0.93 to 2.4]), but also less suppression of the non-salient stimulus, suggesting that self-relatedness and perceptual salience interacted somewhere along the processing hierarchy.

To elucidate more directly whether perceptual and social salience are processed independently or interact, we assessed whether the effects of social and perceptual salience were additive, or whether there were deviations in processing rates when social and perceptual salience were present simultaneously.

To that end, we added the processing rate changes resulting from perceptual salience alone and social associations alone and subtracted them from the processing rate changes in the condition in which perceptual salience and social associations were presented together (see Figure 7—figure supplement 1 ).⟦>zach claim=no-assertion: @{To that end, we added the processing rate changes resulting from perceptual salience alone and social associations alone and subtracted them from the processing rate changes in the condition in which perceptual salience and social associations were presented together (see Figure 7—figure supplement 1 ).} Narration of how the additivity contrast was computed, with no result attached.⟧

In the salient stimulus, there were no systematic deviations between perceptual salience alone and perceptual salience when it was presented on a self-related stimulus (–0.28 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –2.1 to 1.6] Hz; see Figure 7 ) or an other-related stimulus (–0.54 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –2.4 to 1.4] Hz).⟦>zach claim=d5cc37f8-3738-4acf-95de-3c10a177aa69: @{In the salient stimulus, there were no systematic deviations between perceptual salience alone and perceptual salience when it was presented on a self-related stimulus (–0.28 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : –2.1 to 1.6] Hz; see Figure 7 ) or an other-related stimulus (–0.54 [ H D I 95 \begin{document}}$HDI^{95}}$\end{document}} : –2.4 to 1.4] Hz).} self-salience-reduces-perceptual-benefit⟧

Figure 7. Interaction of social and perceptual salience.⟦>zach claim=d5cc37f8-3738-4acf-95de-3c10a177aa69: @{Figure 7. Interaction of social and perceptual salience.} self-salience-reduces-perceptual-benefit⟧

Interaction effects of social and perceptual salience on processing rates.

Probability density plots of processing rate change parameters when the stimulus was perceptually salient and self-associated (left panel) or other-associated (middle panel).

The right panel shows the difference in perceptual-salience induced processing benefit between the self- and other-associated stimuli.

Figure 7—figure supplement 1. Formalization of interaction: formalization of interaction effect assessment, using attentional weights.⟦>zach claim=no-assertion: @{Figure 7—figure supplement 1. Formalization of interaction: formalization of interaction effect assessment, using attentional weights.} A bare supplementary-figure title for the formalisation schematic.⟧

Note that, instead of attentional weights, we report processing rates.

However, the same effects that are reported in the main text are reproduced when attentional weights are used in the analysis.

Next, we quantified the differences in perceptual salience effects between self-associated and other-associated stimuli, taking the individual social and perceptual only effects into account.

Parameter inspection of the processing rates suggested that stimuli were not systematically more or less attended when perceptually salient stimuli were self-related compared to other-related (0.26 [ H D I 95 \begin{document}$HDI^{95}$\end{document} : –1.4 to 1.9] Hz).

This indicates an additive effect, which would be expected if social and perceptual salience were processed independently.

Can self-relatedness effects in attentional selection explain self-prioritization in perceptual matching?

To ascertain that participants learned the correct association and exhibited a typical SPE, they completed a common shape-label matching task ( Sui et al., 2012 ).

Across both experiments, strong SPEs were present, indicated by an enhanced accuracy towards match-trials of self-associated, compared to other-associated, stimuli (see Figure 8 ; Experiment 1: δ \begin{document}$\delta$\end{document} = –1.064 [ C I 95 \begin{document}$CI^{95}$\end{document} : –1.38 to –0.75], B F 10 = 3.23 109 \begin{document}$BF_{10}=3.23^{109}$\end{document} ; Experiment 2: δ \begin{document}$\delta$\end{document} = –0.982 [ C I 95 \begin{document}$CI^{95}$\end{document} : –1.20 to –0.77], B F 10 = 4.47 1017 \begin{document}$BF_{10}=4.47^{1017}$\end{document} ).⟦>zach claim=0eef258f-1e89-4298-a762-c0c4a877ab9a: @{Across both experiments, strong SPEs were present, indicated by an enhanced accuracy towards match-trials of self-associated, compared to other-associated, stimuli (see Figure 8 ; Experiment 1: δ \begin{document}}$\delta$\end{document}} = –1.064 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –1.38 to –0.75], B F 10 = 3.23 109 \begin{document}}$BF_{10}}=3.23^{109}}$\end{document}} ; Experiment 2: δ \begin{document}}$\delta$\end{document}} = –0.982 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –1.20 to –0.77], B F 10 = 4.47 1017 \begin{document}}$BF_{10}}=4.47^{1017}}$\end{document}} ).} spe-robust-matching-both-experiments⟧

Figure 8. Self-prioritization in matching.⟦>zach claim=0eef258f-1e89-4298-a762-c0c4a877ab9a: @{Figure 8. Self-prioritization in matching.} spe-robust-matching-both-experiments⟧

Matching task results showing robust self-prioritization effects in both experiments, indicated by the enhanced accuracy towards self-associated information compared to other-associated information on match-trials.

Colored points indicate individual participants.

Black superimposed points and error bands indicate group means and C I 95 \begin{document}$CI^{95}$\end{document} .

Interestingly, while self-associated stimuli were prioritized in shape-label matching, they showed reduced processing rates in attentional selection (as outlined above), at least when the decisional dimension was in the social domain.

To assess the degree to which social biases in early attentional selection contribute to the expression of SPEs in perceptual matching, we correlated the differences in processing rate differences between the self and other associated stimulus, that is the self-induced change in processing rates, with the SPE magnitude.

Note that, as SPEs measured in the matching paradigm are likely the cumulative result of self-biases at different levels of processing, we would not expect predictive effects to be particularly strong.

In Experiment 1, the individual SPE benefits in the shape-label matching task correlated with the socially-induced processing rate changes in the social decision dimension ( r \begin{document}$r$\end{document} =0.354 [ C I 95 \begin{document}$CI^{95}$\end{document} : 0.11 to 0.54]; B F 10 \begin{document}$BF_{10}$\end{document} = 8.23; see Figure 9 ), but not in the perceptual decision dimension ( r \begin{document}$r$\end{document} =0.069 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.18 to 0.31]; B F 10 \begin{document}$BF_{10}$\end{document} = 0.181).⟦>zach claim=25ad6b4e-1066-424b-b337-98b5188b5553: @{In Experiment 1, the individual SPE benefits in the shape-label matching task correlated with the socially-induced processing rate changes in the social decision dimension ( r \begin{document}}$r$\end{document}} =0.354 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : 0.11 to 0.54]; B F 10 \begin{document}}$BF_{10}}$\end{document}} = 8.23; see Figure 9 ), but not in the perceptual decision dimension ( r \begin{document}}$r$\end{document}} =0.069 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –0.18 to 0.31]; B F 10 \begin{document}}$BF_{10}}$\end{document}} = 0.181).} decisional-dimension-tradeoff⟧

In Experiment 2, the individual SPE benefits in the shape-label matching task negatively correlated with the socially induced processing rate changes in the perceptual decision dimension ( r \begin{document}$r$\end{document} =–0.328 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.52 to –0.08]; B F 10 \begin{document}$BF_{10}$\end{document} = 4.53; see Figure 9 ), but not the processing rate changes in the social decision dimension ( r \begin{document}$r$\end{document} =–0.138 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.37 to 0.11]; B F 10 \begin{document}$BF_{10}$\end{document} = 0.278).⟦>zach claim=25ad6b4e-1066-424b-b337-98b5188b5553: @{In Experiment 2, the individual SPE benefits in the shape-label matching task negatively correlated with the socially induced processing rate changes in the perceptual decision dimension ( r \begin{document}}$r$\end{document}} =–0.328 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –0.52 to –0.08]; B F 10 \begin{document}}$BF_{10}}$\end{document}} = 4.53; see Figure 9 ), but not the processing rate changes in the social decision dimension ( r \begin{document}}$r$\end{document}} =–0.138 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –0.37 to 0.11]; B F 10 \begin{document}}$BF_{10}}$\end{document}} = 0.278).} decisional-dimension-tradeoff⟧

Figure 9. Individual differences reveal how task parameters are related.⟦>zach claim=25ad6b4e-1066-424b-b337-98b5188b5553: @{Figure 9. Individual differences reveal how task parameters are related.} decisional-dimension-tradeoff⟧

Scatter plots for Experiments 1 and 2 showing individual self-prioritization effect benefits in the shape-label matching task predicting socially induced changes in attentional processing rates for the self-associated/salient (positive) or other-associated/non-salient (negative) stimuli.

Solid lines indicate linear best fit.

The right scatter plot shows the changes in individual, absolute processing rates in response to social versus perceptual decision judgements, for both experiments.

Experiments and respective best linear prediction lines are color-coded in darker (Experiment 1) and lighter (Experiment 2) gray, to allow distinguishing between conditions that used social salience (dark gray) or perceptual salience (light gray) with the perceptual decision dimension.

Bayes factors assessing the probability of a linear correlation and posterior estimation info is provided above each plot.

Pooling data across experiments indicated no correlations between the SPE benefits and processing rate changes obtained either through perceptual or social decision dimensions (perceptual: r \begin{document}$r$\end{document} = –0.087 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.25 to 0.09]; B F 10 \begin{document}$BF_{10}$\end{document} = 0.177; social: r \begin{document}$r$\end{document} = –0.029 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.20 to 0.15]; B F 10 \begin{document}$BF_{10}$\end{document} = 0.117).

However, it showed that the processing rate changes in the social decision dimension were negatively correlated with the processing rate changes in the perceptual decision dimension (processing rates r \begin{document}$r$\end{document} = –0.243 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.39 to –0.08]), B F 10 \begin{document}$BF_{10}$\end{document} = 6.58; see Figure 9 , presented with individual experiment data superimposed, which was driven by a differential allocation of relative attentional weights w \begin{document}$w$\end{document} ( r \begin{document}$r$\end{document} =–0.268 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.41 to –0.11]; B F 10 \begin{document}$BF_{10}$\end{document} = 16.93).⟦>zach claim=25ad6b4e-1066-424b-b337-98b5188b5553: @{However, it showed that the processing rate changes in the social decision dimension were negatively correlated with the processing rate changes in the perceptual decision dimension (processing rates r \begin{document}}$r$\end{document}} = –0.243 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –0.39 to –0.08]), B F 10 \begin{document}}$BF_{10}}$\end{document}} = 6.58; see Figure 9 , presented with individual experiment data superimposed, which was driven by a differential allocation of relative attentional weights w \begin{document}}$w$\end{document}} ( r \begin{document}}$r$\end{document}} =–0.268 [ C I 95 \begin{document}}$CI^{95}}$\end{document}} : –0.41 to –0.11]; B F 10 \begin{document}}$BF_{10}}$\end{document}} = 16.93).} decisional-dimension-tradeoff⟧

In other words, individuals who showed a faster selection of (socially or perceptually) salient information at the perceptual shape feature level showed the least processing facilitation towards self-associated shapes when reporting the social association.

At the same time, those who showed a faster selection of perceptually non-salient or other-associated information when reporting the perceptual feature showed the strongest attentional facilitation for self-associated shapes when reporting the social association.

This suggests a trade-off in attentional selection between the two decisional dimensions, leading to opposing effects.

Lastly, we explored the contribution of perceptual and social salience to attentional selection of information that is both perceptually and socially salient in Experiment 2 via the correlation of shifts in relative attentional weights.

This indicated that perceptual salience effects in other-associated stimuli were more strongly correlated with the mere perceptual-salience effects ( r \begin{document}$r$\end{document} =0.532 [ C I 95 \begin{document}$CI^{95}$\end{document} : 0.33 to 0.67]; B F 10 \begin{document}$BF_{10}$\end{document} = 10317.1) rather than the mere social-salience effects ( r \begin{document}$r$\end{document} =–0.285 [ C I 95 \begin{document}$CI^{95}$\end{document} : –0.48 to –0.05]; B F 10 \begin{document}$BF_{10}$\end{document} = 2.56).

In contrast to that, perceptual salience effects in self-associated stimuli were more strongly correlated with mere social salience effects ( r \begin{document}$r$\end{document} =0.429 [ C I 95 \begin{document}$CI^{95}$\end{document} : 0.21 to 0.59]; B F 10 \begin{document}$BF_{10}$\end{document} = 137.87) than mere perceptual salience effects ( r \begin{document}$r$\end{document} =0.31 [ C I 95 \begin{document}$CI^{95}$\end{document} : 0.08 to 0.50]; B F 10 \begin{document}$BF_{10}$\end{document} = 4.45).

Bayesian regression model selection supported this: While a model that included perceptual and social salience effects together explained the perceptual salience effects in self- and other-associated stimuli best (Other: P ( M | D a t a ) \begin{document}$P(M|Data)$\end{document} = 0.504; B F M \begin{document}$BF_{M}$\end{document} = 4.07; R 2 \begin{document}$R^{2}$\end{document} = 0.328; Self: P ( M | D a t a ) \begin{document}$P(M|Data)$\end{document} = 0.682; B F M \begin{document}$BF_{M}$\end{document} = 8.60; R 2 \begin{document}$R^{2}$\end{document} = 0.324), inspection of the posteriors indicated that, for perceptually salient, other-associated shapes, mere perceptual salience effects were the best predictor ( B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} =4638.74; vs social: B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} = 2.83; Table 1 ).⟦>zach claim=fcc24782-2506-4c9e-908a-baa03bb791fb: @{Bayesian regression model selection supported this: While a model that included perceptual and social salience effects together explained the perceptual salience effects in self- and other-associated stimuli best (Other: P ( M | D a t a ) \begin{document}}$P(M|Data)$\end{document}} = 0.504; B F M \begin{document}}$BF_{M}}$\end{document}} = 4.07; R 2 \begin{document}}$R^{2}}$\end{document}} = 0.328; Self: P ( M | D a t a ) \begin{document}}$P(M|Data)$\end{document}} = 0.682; B F M \begin{document}}$BF_{M}}$\end{document}} = 8.60; R 2 \begin{document}}$R^{2}}$\end{document}} = 0.324), inspection of the posteriors indicated that, for perceptually salient, other-associated shapes, mere perceptual salience effects were the best predictor ( B F i n c l u s i o n \begin{document}}$BF_{inclusion}}$\end{document}} =4638.74; vs social: B F i n c l u s i o n \begin{document}}$BF_{inclusion}}$\end{document}} = 2.83; Table 1 ).} Social salience dominates for self-associated stimuli — perceptual salience dominates for other.⟧

For self-associated shapes, on the other hand, mere social salience effects were the best predictor ( B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} =2458.52) while a susceptibility to mere perceptual salience also contributed ( B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} =153.25; Table 2 ).⟦>zach claim=fcc24782-2506-4c9e-908a-baa03bb791fb: @{For self-associated shapes, on the other hand, mere social salience effects were the best predictor ( B F i n c l u s i o n \begin{document}}$BF_{inclusion}}$\end{document}} =2458.52) while a susceptibility to mere perceptual salience also contributed ( B F i n c l u s i o n \begin{document}}$BF_{inclusion}}$\end{document}} =153.25; Table 2 ).} Social salience dominates for self-associated stimuli — perceptual salience dominates for other. — The claim states this same result for self-associated shapes: social salience is the stronger predictor with perceptual salience contributing as well.⟧

In other words, when information was not self-related, attentional selection was mostly driven by perceptual salience.

In contrast, when information was related to the self, attentional selection was driven more strongly by social than perceptual salience.

Table 1. Posterior coefficient summaries for perceptual salience and other-association.⟦>zach claim=fcc24782-2506-4c9e-908a-baa03bb791fb: @{Table 1. Posterior coefficient summaries for perceptual salience and other-association.} Social salience dominates for self-associated stimuli — perceptual salience dominates for other.⟧

Coefficient P(incl) P(incl|Data) B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} Mean SD C I 95 \begin{document}$CI^{95}$\end{document} Lower C I 95 \begin{document}$CI^{95}$\end{document} Upper Intercept 1.000 1.000 1.0 0.052 0.011 0.031 0.073 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} 0.556 1.000 4638.74 0.833 0.200 0.434 1.232 Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.556 0.779 2.83 –1.191 0.624 –2.435 0.053 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} * Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.333 0.414 1.42 6.081 6.667 –7.216 19.378 Table 2. Posterior coefficient summaries for perceptual salience and self-association.⟦>zach claim=gap: @{Coefficient P(incl) P(incl|Data) B F i n c l u s i o n \begin{document}}$BF_{inclusion}}$\end{document}} Mean SD C I 95 \begin{document}}$CI^{95}}$\end{document}} Lower C I 95 \begin{document}}$CI^{95}}$\end{document}} Upper Intercept 1.000 1.000 1.0 0.052 0.011 0.031 0.073 Δ w p P e r \begin{document}}$\Delta{w_{p}}^{Per}}}}$\end{document}} 0.556 1.000 4638.74 0.833 0.200 0.434 1.232 Δ w p S o c \begin{document}}$\Delta{w_{p}}^{Soc}}}}$\end{document}} 0.556 0.779 2.83 –1.191 0.624 –2.435 0.053 Δ w p P e r \begin{document}}$\Delta{w_{p}}^{Per}}}}$\end{document}} * Δ w p S o c \begin{document}}$\Delta{w_{p}}^{Soc}}}}$\end{document}} 0.333 0.414 1.42 6.081 6.667 –7.216 19.378 Table 2. Posterior coefficient summaries for perceptual salience and self-association.} This table is the only place the inclusion Bayes factors for the social-salience coefficient (BF=2.83) and for the perceptual-by-social interaction (BF=1.42, inconclusive) are reported, and no claim carries either.⟧

Coefficient P(incl) P(incl|Data) B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} Mean SD C I 95 \begin{document}$CI^{95}$\end{document} Lower C I 95 \begin{document}$CI^{95}$\end{document} Upper Intercept 1.000 1.000 1.0 0.021 0.006 0.008 0.034 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} 0.556 0.995 153.25 0.405 0.119 0.167 0.643 Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.556 1.000 2458.52 0.630 0.372 –0.111 1.372 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} * Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.333 0.573 2.68 4.323 3.976 –3.606 12.252


## captions

=== Figure 1 === Figure 1. Mechanisms of attentional selection.⟦>zach claim=no-assertion: @{=== Figure 1 === Figure 1. Mechanisms of attentional selection.} A bare figure title for the schematic of attentional-selection mechanisms.⟧

Attentional selection can occur via different mechanisms: changes in the allocation or the availability and allocation of attentional resources.

Panel A shows an example stimulus display with two identical perceptual objects (gray hexagons) on a dark background, and the processing resources ( C \begin{document}$C$\end{document} , blue columns) that are distributed equally across these stimuli.

In this case, the attentional weights for the reference ( w r \begin{document}${w}_{r}$\end{document} ; left stimulus) and probe ( w p \begin{document}$w_{p}$\end{document} ; right stimulus) are identical.

The processing rates for the reference ( v r \begin{document}$v_{r}$\end{document} ) and probe ( v p \begin{document}$v_{p}$\end{document} ) stimuli are given as the processing resources that are allocated to each of the two stimuli, i.e. w p , r ∗ C \begin{document}$w_{p,r}*C$\end{document} .

Panels B and C show example stimulus displays with two perceptual objects, where one has a higher perceptual salience (luminance and color contrast).

Panel B indicates a mechanism whereby the same processing resources are distributed differentially across the stimulus display, with more resources being given to the more salient stimulus.

This is reflected in a change of relative weight, with constant processing capacity.

Panel C indicates a mechanism whereby the amount of processing resources increases, along with a differential distribution of these resources.

To arbitrate between these two mechanisms, we employed model comparisons to assess whether changes in relative attentional weight or changes in absolute processing rates (capacity and weights) better explained experimental data. === Figure 2 === Figure 2. Decision dimensions.⟦>zach claim=no-assertion: @{To arbitrate between these two mechanisms, we employed model comparisons to assess whether changes in relative attentional weight or changes in absolute processing rates (capacity and weights) better explained experimental data. === Figure 2 === Figure 2. Decision dimensions.} Narration of the model-comparison strategy followed by a bare figure title; no result is stated.⟧

Dissociating the processing stages at which social association may affect early attentional selection via different decisional dimensions.

Automatic effects of self-association would assume that active decoding of the associated social identity is not necessary.

In this case, the social identity associated with a specific perceptual feature renders this feature more salient, without having to be consciously recalled.

On the other hand, some studies suggested that the self needs to be a decisional criterion.

In this case, self-prioritization effects in attentional selection would require active decoding of the social associations.

Altering the decisional dimension (asking which shape vs whose shape), without shifting attention from the crucial perceptual feature (shape), allows disentangling these processes.

Note that the directionality of the sensory and social information does not make assumptions about the temporal dynamics of the underlying process. === Figure 3 === Figure 3. Task design.⟦>zach claim=no-assertion: @{Note that the directionality of the sensory and social information does not make assumptions about the temporal dynamics of the underlying process. === Figure 3 === Figure 3. Task design.} A note on how to read the schematic's arrows, warning that they encode no temporal claim.⟧

( a ) Temporal order judgement task (TOJ) design.

Following an initial presentation of the complete stimulus array, target shapes, which were relatively larger in size compared to background shapes, flickered with a variable stimulus onset asynchrony that was systematically varied between -/+ 83 ms with a higher presentation frequency at small SOAs.

After the stimulus presentation, participants had to indicate which of the two shapes flickered first by selecting the correct shape (baseline conditions, perceptual salience conditions, social salience condition with perceptual decision boundary), or the identity label of the shape-associated social identity (social salience condition with social decision boundary).

Stimulus displays consisted of two types of colored shapes (perceptual objects), distributed across two hemifields in an 8 x 8 grid.

Targets would appear on each side at either of the four central locations.

Lateralization of the specific perceptual objects was randomized across trials.

( b ) Perceptual matching task design.

Participants associated one of the two shapes with themselves, and one with another, anonymous participant.

Associations between social identities and perceptual objects were counterbalanced across participants.

Pairs of shapes and social identity labels were presented on screen.

These could either be congruent (matching) or incongruent (mismatching).

Participants had to respond whether the pair matched in the learned association or mismatched.

Location of the shapes and labels (above, below fixation) was counterbalanced across the task.

( c ) Task structures for Experiments 1 and 2. Both experiments began with a TOJ baseline task.

Experiment 1 utilized non-salient targets exclusively, while Experiment 2 included both perceptually salient and non-salient targets.

These were presented in randomly intermixed order.

Next, targets were associated with social identities through a matching task.

Following this association learning phase, which establishes social salience in the shapes, participants completed the same TOJ task again.

In Experiment 1, they completed one block using a social decision dimension and one block using a perceptual decision dimension.

The order of these blocks was counterbalanced across participants to reduce the influence of order effects in the results.

In Experiment 2, perceptually salient and non-salient stimuli were presented in an intermixed fashion, and participants responded within the social decision dimension.

Each task block was preceded by 8 (matching) to 14 (TOJ) practice trials.

[panels detected: a, b, c] === Figure 4 === Figure 4. Model structure and cross-experimental social salience effects.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{[panels detected: a, b, c] === Figure 4 === Figure 4. Model structure and cross-experimental social salience effects.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Hierarchical model structure shows how the parameters of interest ( w p e f f e c t \begin{document}$w_{peffect}$\end{document} , C e f f e c t \begin{document}$C_{effect}$\end{document} , Δ v p \begin{document}$\Delta v_{p}$\end{document} , and Δ v r \begin{document}$\Delta v_{r}$\end{document} ) were estimated from within-participant differences between the neutral baseline (gray) and social salience (blue) condition.

The better model is depicted, in which processing capacity was estimated for each condition separately, suggesting that changes in absolute processing rates, rather than relative attentional weights, have been underlying attentional selection effects of social salience.

Mathematical formalization of the relation between the model nodes is given on the right.

Density plots indicate the highest density estimates for the different processing parameters of interest.

Neutral baseline parameters are given in absolute parameter values, with processing capacity shown as items/ms and the relative attentional weight for the probe (a shape that was subsequently associated with the self).

Social salience parameters are shown in change scores, relative to baseline, depicting an increase and decrease in processing capacity and attentional weight, respectively.

Absolute processing rate changes for the probe (self-associated) and reference (other-associated) shapes, as well as their relative change, are shown on the bottom right. === Figure 4s1 === Figure 4—figure supplement 1. Individual estimates: Absolute processing rates ( v p \begin{document}$v_{p}$\end{document} ) for the probe stimulus (self-associated), shown for individual participants for the social baseline (gray; v p B a s e S o c \begin{document}$v_{pBaseSoc}$\end{document} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c \begin{document}$v_{pSoc}$\end{document} ).⟦>zach claim=no-assertion: @{Absolute processing rate changes for the probe (self-associated) and reference (other-associated) shapes, as well as their relative change, are shown on the bottom right. === Figure 4s1 === Figure 4—figure supplement 1. Individual estimates: Absolute processing rates ( v p \begin{document}}$v_{p}}$\end{document}} ) for the probe stimulus (self-associated), shown for individual participants for the social baseline (gray; v p B a s e S o c \begin{document}}$v_{pBaseSoc}}$\end{document}} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c \begin{document}}$v_{pSoc}}$\end{document}} ).} A panel label naming which quantities appear where in the figure, without stating their values or direction.⟧

Points show the estimated posterior means, thick lines indicate the central quartiles, and thin lines indicate the 95 highest density interval.

Processing rates are given in items/ms. === Figure 5 === Figure 5. Social salience effects with different decision dimensions.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Processing rates are given in items/ms. === Figure 5 === Figure 5. Social salience effects with different decision dimensions.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Hierarchical model structure shows how social salience effects were estimated between social salience conditions (blue: social decision dimension; turquoise: perceptual decision dimension) and the neutral baseline condition (gray; see Figure 4 caption for details and formalizations) in Experiment 1. The right plot shows how relative processing rates were calculated, at the individual participant level, from social salience-induced processing rate changes for the self-associated and other-associated shapes.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Hierarchical model structure shows how social salience effects were estimated between social salience conditions (blue: social decision dimension; turquoise: perceptual decision dimension) and the neutral baseline condition (gray; see Figure 4 caption for details and formalizations) in Experiment 1. The right plot shows how relative processing rates were calculated, at the individual participant level, from social salience-induced processing rate changes for the self-associated and other-associated shapes.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Density plots indicate the group-level highest density intervals for the processing capacity and absolute processing rate estimates, given in items/ms.

Additionally, the 95% HDIs are presented alongside the group means.

The relative change in processing rates ( Δ v p − Δ v r \begin{document}$\Delta v_{p}-\Delta v_{r}$\end{document} ) can be interpreted directly as the processing rate advantage of the self-associated over the other-associated stimuli.

Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplement 1 and 2 , respectively. === Figure 5s1 === Figure 5—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.⟦>zach claim=no-assertion: @{Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplement 1 and 2 , respectively. === Figure 5s1 === Figure 5—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.} A cross-reference to the individual-participant supplements followed by a figure title.⟧

Different conditions are shown in different shadings.

The panel on the right shows an example participant with a group-representative response pattern: an increase of ‘probe first’ responses when the probe was self-associated and the shape of the stimulus had to be reported.

This pattern is specifically visible at low onset asynchronies.

Furthermore, this participant shows a decreased proportion of ‘probe first’ responses when the probe was self-associated and the social identity had to be reported. === Figure 5s2 === Figure 5—figure supplement 2. Individual estimates: absolute processing rates ( v p \begin{document}${v}_{p}$\end{document} ) for the probe stimulus (self-associated), shown for individual participants in Experiment 1. Different colors indicate different conditions: the baseline (gray; v p B a s e \begin{document}$v_{pBase}$\end{document} ), the social salience condition in which the shape had to be reported (light blue; v p S o c P e r \begin{document}$v_{pSocPer}$\end{document} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c S o c \begin{document}$v_{pSocSoc}$\end{document} ).⟦>zach claim=gap: @{Furthermore, this participant shows a decreased proportion of ‘probe first’ responses when the probe was self-associated and the social identity had to be reported. === Figure 5s2 === Figure 5—figure supplement 2. Individual estimates: absolute processing rates ( v p \begin{document}}${v}}_{p}}$\end{document}} ) for the probe stimulus (self-associated), shown for individual participants in Experiment 1. Different colors indicate different conditions: the baseline (gray; v p B a s e \begin{document}}$v_{pBase}}$\end{document}} ), the social salience condition in which the shape had to be reported (light blue; v p S o c P e r \begin{document}}$v_{pSocPer}}$\end{document}} ) and the social salience condition in which the identity had to be reported (dark blue; v p S o c S o c \begin{document}}$v_{pSocSoc}}$\end{document}} ).} This single-participant illustration of fewer 'probe first' responses when the self-associated probe required a social identity report is a result at the individual level that no claim in the tree accounts for.⟧

Points show the estimated posterior means, thick lines indicate the central quartiles, and thin lines indicate the 95 highest density interval.

Processing rates are given in items/ms. === Figure 6 === Figure 6. Social and perceptual salience effects.⟦>zach claim=08433979-b40e-4b78-91f6-80537bb4c971: @{Processing rates are given in items/ms. === Figure 6 === Figure 6. Social and perceptual salience effects.} other-association-advantage-social-condition⟧

Hierarchical model structure shows how social salience only (blue) and perceptual salience only (orange) effects were estimated relative to their respective neutral baseline conditions (gray; see Figure 4 caption for formalizations and main text for details) in Experiment 2. To assess processing parameters for the interaction of social and perceptual salience (purple, pink), we calculated change scores, indicative of perceptual salience effects, relative to the perceptual neutral baseline.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Hierarchical model structure shows how social salience only (blue) and perceptual salience only (orange) effects were estimated relative to their respective neutral baseline conditions (gray; see Figure 4 caption for formalizations and main text for details) in Experiment 2. To assess processing parameters for the interaction of social and perceptual salience (purple, pink), we calculated change scores, indicative of perceptual salience effects, relative to the perceptual neutral baseline.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

This can be interpreted as the effect of perceptual salience that is present when shapes are associated with the own or another social identity.

Density plots indicate the group-level highest density intervals for the processing capacity and processing speed estimates, given in items/ms.

Additionally, the 95% HDIs are presented alongside the group means.

The relative speed change ( Δ v p − Δ v r \begin{document}$\Delta v_{p}-\Delta v_{r}$\end{document} ) can be interpreted directly as the processing rate advantage of the self-associated over the other-associated stimuli (social salience only), or the perceptually salient over the perceptually non-salient stimuli (perceptual salience only, social + perceptual salience).

Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplements 1 and 2 , respectively. === Figure 6s1 === Figure 6—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.⟦>zach claim=4518f433-c0d6-4313-bbed-2d7357442d4e: @{Raw response data and parameter estimates for individual participants are provided in Figure 5—figure supplements 1 and 2 , respectively. === Figure 6s1 === Figure 6—figure supplement 1. Individual psychometric functions: Individual participant response data indicating the proportion with which participants responded that the probe flickered first as a function of stimulus onset (flicker) asynchrony.} TVA (Bundesen 1990) is the standard framework decomposing attention into C and w parameters.⟧

Different conditions are shown in different shadings. === Figure 6s2 === Figure 6—figure supplement 2. Individual estimates: Absolute processing rates ( v p \begin{document}$v_{p}$\end{document} ) for the probe stimulus (perceptually salient), shown for individual participants for the baseline (gray; v p B a s e \begin{document}$v_{pBase}$\end{document} ), for the mere perceptual salience condition (orange; v p P e r c \begin{document}$v_{pPerc}$\end{document} ), for the perceptual salience condition in which the probe was self-associated (purple; v p P e r S e l f \begin{document}$v_{pPerSelf}$\end{document} ), and the perceptual salience condition in which the probe was other-associated (pink; v p P e r O t h e r \begin{document}$v_{pPerOther}$\end{document} ).⟦>zach claim=no-assertion: @{Different conditions are shown in different shadings. === Figure 6s2 === Figure 6—figure supplement 2. Individual estimates: Absolute processing rates ( v p \begin{document}}$v_{p}}$\end{document}} ) for the probe stimulus (perceptually salient), shown for individual participants for the baseline (gray; v p B a s e \begin{document}}$v_{pBase}}$\end{document}} ), for the mere perceptual salience condition (orange; v p P e r c \begin{document}}$v_{pPerc}}$\end{document}} ), for the perceptual salience condition in which the probe was self-associated (purple; v p P e r S e l f \begin{document}}$v_{pPerSelf}}$\end{document}} ), and the perceptual salience condition in which the probe was other-associated (pink; v p P e r O t h e r \begin{document}}$v_{pPerOther}}$\end{document}} ).} A graphical-encoding note about the shading, plus a figure title.⟧

Points show the estimated posterior means, thick lines indicate the central quartiles, and thin lines indicate the 95 highest density interval.

Processing rates are given in items/ms. === Figure 7 === Figure 7. Interaction of social and perceptual salience.⟦>zach claim=d5cc37f8-3738-4acf-95de-3c10a177aa69: @{Processing rates are given in items/ms. === Figure 7 === Figure 7. Interaction of social and perceptual salience.} self-salience-reduces-perceptual-benefit⟧

Interaction effects of social and perceptual salience on processing rates.

Probability density plots of processing rate change parameters when the stimulus was perceptually salient and self-associated (left panel) or other-associated (middle panel).

The right panel shows the difference in perceptual-salience induced processing benefit between the self- and other-associated stimuli. === Figure 7s1 === Figure 7—figure supplement 1. Formalization of interaction: formalization of interaction effect assessment, using attentional weights.⟦>zach claim=no-assertion: @{The right panel shows the difference in perceptual-salience induced processing benefit between the self- and other-associated stimuli. === Figure 7s1 === Figure 7—figure supplement 1. Formalization of interaction: formalization of interaction effect assessment, using attentional weights.} A panel label naming the quantity plotted on the right, without stating its size or direction.⟧

Note that, instead of attentional weights, we report processing rates.

However, the same effects that are reported in the main text are reproduced when attentional weights are used in the analysis. === Figure 8 === Figure 8. Self-prioritization in matching.⟦>zach claim=0eef258f-1e89-4298-a762-c0c4a877ab9a: @{However, the same effects that are reported in the main text are reproduced when attentional weights are used in the analysis. === Figure 8 === Figure 8. Self-prioritization in matching.} spe-robust-matching-both-experiments⟧

Matching task results showing robust self-prioritization effects in both experiments, indicated by the enhanced accuracy towards self-associated information compared to other-associated information on match-trials.

Colored points indicate individual participants.

Black superimposed points and error bands indicate group means and C I 95 \begin{document}$CI^{95}$\end{document} . === Figure 9 === Figure 9. Individual differences reveal how task parameters are related.⟦>zach claim=25ad6b4e-1066-424b-b337-98b5188b5553: @{Black superimposed points and error bands indicate group means and C I 95 \begin{document}}$CI^{95}}$\end{document}} . === Figure 9 === Figure 9. Individual differences reveal how task parameters are related.} decisional-dimension-tradeoff⟧

Scatter plots for Experiments 1 and 2 showing individual self-prioritization effect benefits in the shape-label matching task predicting socially induced changes in attentional processing rates for the self-associated/salient (positive) or other-associated/non-salient (negative) stimuli.

Solid lines indicate linear best fit.

The right scatter plot shows the changes in individual, absolute processing rates in response to social versus perceptual decision judgements, for both experiments.

Experiments and respective best linear prediction lines are color-coded in darker (Experiment 1) and lighter (Experiment 2) gray, to allow distinguishing between conditions that used social salience (dark gray) or perceptual salience (light gray) with the perceptual decision dimension.

Bayes factors assessing the probability of a linear correlation and posterior estimation info is provided above each plot. === Figure 10 === Figure 10. Parameter estimates and their respective uncertainties for social and perceptual salience. === Figure 11 === Figure 11. Estimated power for observing a reliable self-bias in attentional selection for the perceptual salience (orange solid line) and social salience (green dashed line) conditions.⟦>zach claim=no-assertion: @{Bayes factors assessing the probability of a linear correlation and posterior estimation info is provided above each plot. === Figure 10 === Figure 10. Parameter estimates and their respective uncertainties for social and perceptual salience. === Figure 11 === Figure 11. Estimated power for observing a reliable self-bias in attentional selection for the perceptual salience (orange solid line) and social salience (green dashed line) conditions.} A note on where the Bayes factors are printed, plus two bare figure titles.⟧

Shaded bands indicate their respective 95% highest density intervals.


## tables

Table 1. Posterior coefficient summaries for perceptual salience and other-association.⟦>zach claim=fcc24782-2506-4c9e-908a-baa03bb791fb: @{Table 1. Posterior coefficient summaries for perceptual salience and other-association.} Social salience dominates for self-associated stimuli — perceptual salience dominates for other.⟧

Coefficient P(incl) P(incl|Data) B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} Mean SD C I 95 \begin{document}$CI^{95}$\end{document} Lower C I 95 \begin{document}$CI^{95}$\end{document} Upper Intercept 1.000 1.000 1.0 0.052 0.011 0.031 0.073 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} 0.556 1.000 4638.74 0.833 0.200 0.434 1.232 Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.556 0.779 2.83 –1.191 0.624 –2.435 0.053 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} * Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.333 0.414 1.42 6.081 6.667 –7.216 19.378 Table 2. Posterior coefficient summaries for perceptual salience and self-association.⟦>zach claim=gap: @{Coefficient P(incl) P(incl|Data) B F i n c l u s i o n \begin{document}}$BF_{inclusion}}$\end{document}} Mean SD C I 95 \begin{document}}$CI^{95}}$\end{document}} Lower C I 95 \begin{document}}$CI^{95}}$\end{document}} Upper Intercept 1.000 1.000 1.0 0.052 0.011 0.031 0.073 Δ w p P e r \begin{document}}$\Delta{w_{p}}^{Per}}}}$\end{document}} 0.556 1.000 4638.74 0.833 0.200 0.434 1.232 Δ w p S o c \begin{document}}$\Delta{w_{p}}^{Soc}}}}$\end{document}} 0.556 0.779 2.83 –1.191 0.624 –2.435 0.053 Δ w p P e r \begin{document}}$\Delta{w_{p}}^{Per}}}}$\end{document}} * Δ w p S o c \begin{document}}$\Delta{w_{p}}^{Soc}}}}$\end{document}} 0.333 0.414 1.42 6.081 6.667 –7.216 19.378 Table 2. Posterior coefficient summaries for perceptual salience and self-association.} Table 2 is the only place the inclusion Bayes factors for the social-salience coefficient (BF=2.83) and for the perceptual-by-social interaction (BF=1.42, inconclusive) are reported, and no claim carries either.⟧

Coefficient P(incl) P(incl|Data) B F i n c l u s i o n \begin{document}$BF_{inclusion}$\end{document} Mean SD C I 95 \begin{document}$CI^{95}$\end{document} Lower C I 95 \begin{document}$CI^{95}$\end{document} Upper Intercept 1.000 1.000 1.0 0.021 0.006 0.008 0.034 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} 0.556 0.995 153.25 0.405 0.119 0.167 0.643 Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.556 1.000 2458.52 0.630 0.372 –0.111 1.372 Δ w p P e r \begin{document}$\Delta{w_{p}^{Per}}$\end{document} * Δ w p S o c \begin{document}$\Delta{w_{p}^{Soc}}$\end{document} 0.333 0.573 2.68 4.323 3.976 –3.606 12.252
