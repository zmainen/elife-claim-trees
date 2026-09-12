# Self-association enhances early attentional selection through automatic prioritization of socially salient signals

<!-- scheller-2026-self-prioritization · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Efficiently processing self-related information is critical for cognition, yet the earliest mechanisms enabling this self-prioritization in humans remain unclear.

By combining a temporal order judgement task with computational modeling based on the Theory of Visual Attention (TVA), we show how mere, arbitrary associations with the self can fundamentally alter attentional selection of sensory information into aware short-term memory, by enhancing the attentional weights and processing capacity devoted to encoding socially loaded information.

This self-prioritization in attentional selection occurs automatically at early perceptual stages but reduces when active social decoding is required.

Importantly, the processing benefits obtained from attentional selection via self-relatedness and via physical salience were additive, suggesting that social and perceptual salience captured attention via separate mechanisms.

Furthermore, intra-individual correlations revealed an ‘obligatory’ self-prioritization effect, whereby self-relatedness overpowered the contribution of perceptual salience in guiding attentional selection.

Together, our findings provide evidence for the influence of self-relatedness during earlier, automatic stages of attentional selection at the gateway to perception, distinct from later post-attentive processing stages.


## introduction

Introduction The ability to prioritize self-related information is crucial for adaptive cognition and behavior.

It enables us to efficiently process cues pertaining to our own safety, goals, and well-being in complex, social environments ( Conway, 2005 ; Enock et al., 2018 ; Humphreys and Sui, 2015 ; Moray, 1959 ; Rogers et al., 1977 ).

Decades of research have revealed that this self-relatedness boosts information processing not only for long-term established self-associated information (e.g. own names, owned objects), but also for completely arbitrary information newly associated with the self ( Cunningham et al., 2008 ; Golubickis et al., 2018 ; Moray, 1959 ; Scheller and Sui, 2022b ; Sui et al., 2012 ).

However, the mechanisms underlying such self-prioritization remain unclear.

While higher-level contributions from memory, decision making, and motor planning to the emergence of these self-prioritization effects (SPEs) are well established ( Caughey et al., 2021 ; Constable et al., 2011 ; Desebrock et al., 2018 ; Falbén et al., 2020a ; Falbén et al., 2020b ; Scheller and Sui, 2022b ; Yin et al., 2019 ), the role of earlier, perceptual processing stages is still debated ( Macrae et al., 2017 ; Macrae et al., 2018 ; Reuther and Chakravarthi, 2017 ; Scheller and Sui, 2022a ; Scheller and Sui, 2022b ; Stein et al., 2016 ; Sui et al., 2012 ).

Some evidence suggests that self-relatedness can alter perceptual representations specifically through the integration of the sensory input with prior expectations ( Scheller et al., 2024 ; Scheller and Sui, 2022a ) or through attentional modulations ( Humphreys and Sui, 2016 ; Macrae et al., 2018 ).

Nevertheless, its specific effects on attentional selection during perception remain unanswered, particularly since socially associated stimuli often do not contain inherent sensory salience that automatically captures attention in a purely bottom-up fashion.

The putative role of social salience in driving self-prioritization ( Humphreys and Sui, 2015 ; Liu and Sui, 2016 ; Moradi et al., 2020 ; Siebold et al., 2015 ; Sui et al., 2012 ; Sui et al., 2015 ) begs the question whether the active decoding of higher-order social identities is strictly required to drive attentional selection, or whether more ‘automatic’ effects may arise from modulations of early perceptual attentional deployment.

The first goal of the present study was to outline the mechanisms by which self-relatedness influences attentional selection of visual information.

To address this, we assessed whether and how social association of arbitrary, sensory information alters attentional selection, leading to prior entry ( Schneider and Bavelier, 2003 ; Spence and Parise, 2010 ; Titchener, 1908 ; Weiß et al., 2013 ).

Prior entry refers to the phenomenon that attention can boost processing of a stimulus so that it can sometimes be perceived as appearing earlier than another one, even if the other one was presented earlier.

The magnitude of this catching up and overtaking in processing can be used to index the differential assignment of attentional resources to the stimuli.

As a model of attention-biased stimulus encoding, the Theory of Visual Attention (TVA; Bundesen, 1990 ) formally describes mechanisms underpinning prior entry (; Tünnermann et al., 2017 ; Figure 1 ).⟦>zach claim=gap: @{As a model of attention-biased stimulus encoding, the Theory of Visual Attention (TVA; Bundesen, 1990 ) formally describes mechanisms underpinning prior entry (; Tünnermann et al., 2017 ; Figure 1 ).}⟧

Prior entry could arise in different ways: (1) There may be a mere change in relative attentional weights (TVA’s parameter w ), where the attended stimulus receives resources at the expense of the other stimuli, with the overall employed processing resources (TVA’s capacity parameter C \begin{document}$C$\end{document} ) remaining constant.

(2) According to TVA, objects in the visual field progress toward encoding at different processing rates (TVA’s v \begin{document}$v$\end{document} parameters).

Therefore, alternatively, there may be an absolute boost of processing resources to the advantage of the attended stimulus (or an absolute decrease of processing resources towards the unattended stimuli, see Tünnermann et al., 2015 ).

In combination, these lead to a higher absolute processing rate v of the attended compared to the unattended stimulus and consequently to prior entry.

By estimating TVA parameters with a hierarchical Bayesian model ( Tünnermann et al., 2017 ), the present study quantified whether SPEs can be explained by changes in relative attentional weights, or absolute changes in processing rates of the self-related (salient) versus other-related (non-salient) stimuli.

These mechanisms have previously been used to explain effects of low-level perceptual salience ( Krüger et al., 2016 ; Krüger et al., 2017 ; Krüger and Scharlau, 2021a ).

Figure 1. Mechanisms of attentional selection.⟦>zach claim=gap: @{Figure 1. Mechanisms of attentional selection.}⟧

Attentional selection can occur via different mechanisms: changes in the allocation or the availability and allocation of attentional resources.

Panel A shows an example stimulus display with two identical perceptual objects (gray hexagons) on a dark background, and the processing resources ( C \begin{document}$C$\end{document} , blue columns) that are distributed equally across these stimuli.

In this case, the attentional weights for the reference ( w r \begin{document}${w}_{r}$\end{document} ; left stimulus) and probe ( w p \begin{document}$w_{p}$\end{document} ; right stimulus) are identical.

The processing rates for the reference ( v r \begin{document}$v_{r}$\end{document} ) and probe ( v p \begin{document}$v_{p}$\end{document} ) stimuli are given as the processing resources that are allocated to each of the two stimuli, i.e. w p , r ∗ C \begin{document}$w_{p,r}*C$\end{document} .

Panels B and C show example stimulus displays with two perceptual objects, where one has a higher perceptual salience (luminance and color contrast).

Panel B indicates a mechanism whereby the same processing resources are distributed differentially across the stimulus display, with more resources being given to the more salient stimulus.

This is reflected in a change of relative weight, with constant processing capacity.

Panel C indicates a mechanism whereby the amount of processing resources increases, along with a differential distribution of these resources.

To arbitrate between these two mechanisms, we employed model comparisons to assess whether changes in relative attentional weight or changes in absolute processing rates (capacity and weights) better explained experimental data.

The second aim of the present study was to establish at what representational level (perceptual, social) visual attention spreads across stimuli with varying different degrees of social salience.

Prior work suggests that self-relatedness of owned objects ( Constable et al., 2019 ; Truong et al., 2017 ) and physical features (self-face; Jublie and Kumar, 2021 ) can lead to prior entry.

While the mechanistic underpinnings of this attentional capture by self-relatedness have not been directly investigated, the authors manipulated the decisional dimension to be orthogonal to the social association.

Findings from one study ( Constable et al., 2019 ) suggested that self-prioritization only emerged when the self was a relevant decisional category.

Crucially, though, their manipulation was also orthogonal to the perceptual feature of interest (the color of the object, rather than the location, which was random).

Expecting self-prioritization under such conditions, however, would assume not just a perceptual modulation, but rather a modulation of a completely unrelated feature.

This, in turn, assumes an automatic fusion of social representations across all its instantaneous, unrelated perceptual features.

However, it is well-established that information that is transferred via different cues does not instantly underlie fusion of all its features ( Enock et al., 2018 ).

Hence, it remains unclear whether self-relatedness leads to prior entry at the level of the perceptual feature or requires decoding of the associated identity in a social feature dimension.

Lastly, the third and final aim of the present study was to qualitatively compare the effects of and quantitatively probe the interactions of perceptual and social salience.

Using a temporal order judgement (TOJ) task with simple, colored shape stimuli arbitrarily associated with social identities, the present study can, for the first time, directly compare social and perceptual salience on the same mechanistic metrics.

That is, qualitatively, we can assess similarities/differences in social and perceptual changes while, quantitatively, studying the interactions between social and perceptual salience.

Notably, if social and perceptual salience operate completely independently, such as at different processing levels, one would expect no interaction between social and perceptual salience.

On the other hand, if social associations systematically alter the effects of perceptual salience, this would be strongly suggestive of self-relatedness directly affecting bottom-up perceptual processing.

In summary, to characterize self-prioritization in early attentional selection, the study addresses three main research questions across two experiments.

The resulting hypotheses and hypothesis-relevant details will be outlined more explicitly below: (Q1) Does mere self-association bias early attentional selection, and what are the underlying mechanisms?

(Experiments 1+2) (H1) Based on previous findings of self-related prior entry findings ( Constable et al., 2019 ; Jublie and Kumar, 2021 ; Truong et al., 2017 ), we hypothesized that participants would show an attentional selection bias towards self-associated, relative to other-associated information.

Mechanistically, this could arise from an enhancement of relative attentional weights towards self-associated information (TVA parameter w p \begin{document}$w_{p}$\end{document} ) or an increase in processing rates for self-associated over other-associated information.

To arbitrate between these possible mechanisms, we compared hierarchical Bayesian models estimating: attentional weights for each condition with a single processing capacity parameter across conditions (indicative of changes in relative attentional weights), and attentional weights and processing capacity independently for each condition (indicative of changes in absolute processing rates).

(Q2) Does self-relatedness bias attentional selection automatically or does it require explicit social decoding?

(Experiment 1) (H2) Based on previous findings ( Constable et al., 2019 ; Jublie and Kumar, 2021 ; Truong et al., 2017 ), we hypothesized that participants would show a bias toward self-associated information when the decisional dimension requires the explicit decoding of the social identity ( Figure 2 , lower panel).⟦>zach claim=gap: @{(Experiment 1) (H2) Based on previous findings ( Constable et al., 2019 ; Jublie and Kumar, 2021 ; Truong et al., 2017 ), we hypothesized that participants would show a bias toward self-associated information when the decisional dimension requires the explicit decoding of the social identity ( Figure 2 , lower panel).}⟧

If self-relatedness also biases attentional selection automatically at the perceptual feature level, self-related information should show higher relative attentional weights/absolute processing rates even when the decisional dimension does not require the explicit decoding of social identities, but merely of their associated perceptual feature (shapes; Figure 2 , upper panel).⟦>zach claim=gap: @{If self-relatedness also biases attentional selection automatically at the perceptual feature level, self-related information should show higher relative attentional weights/absolute processing rates even when the decisional dimension does not require the explicit decoding of social identities, but merely of their associated perceptual feature (shapes; Figure 2 , upper panel).}⟧

As decisional criteria influence the expression of SPEs (e.g. Caughey et al., 2021 ; Falbén et al., 2020b ; Scheller and Sui, 2022b ), this automatic effect at perceptual levels was predicted to be smaller.

Figure 2. Decision dimensions.⟦>zach claim=gap: @{Figure 2. Decision dimensions.}⟧

Dissociating the processing stages at which social association may affect early attentional selection via different decisional dimensions.

Automatic effects of self-association would assume that active decoding of the associated social identity is not necessary.

In this case, the social identity associated with a specific perceptual feature renders this feature more salient, without having to be consciously recalled.

On the other hand, some studies suggested that the self needs to be a decisional criterion.

In this case, self-prioritization effects in attentional selection would require active decoding of the social associations.

Altering the decisional dimension (asking which shape vs whose shape), without shifting attention from the crucial perceptual feature (shape), allows disentangling these processes.

Note that the directionality of the sensory and social information does not make assumptions about the temporal dynamics of the underlying process.

(Q3) Does self-association affect attentional selection in a similar way to perceptual salience, and how do social and perceptual salience interact?

(Experiment 2) (H3) If social and perceptual salience bias attentional selection in similar ways, both manipulations were hypothesized to result in enhancements of relative attentional weights or similar enhancements in absolute processing rates towards the more salient stimulus (self).

Overall, we expected effects of social salience to be smaller than those of perceptual salience ( Liu and Sui, 2016 ; Mevorach et al., 2010 ; Sui et al., 2015 ).

Social and perceptual salience may interact or be processed independently.

If they operate completely independently, the combination of their attentional processing rate changes would be additive.

Sub- or supra-additive effects of social and perceptual salience would suggest interacting processes during attentional selection.

The difference in degree of additivity for perceptual salience with either self- or other-related information (interference of social and perceptual salience) would suggest that self-relatedness affects information processing via distinct attentional streams from information linked to other social identities.

Using a TOJ task with stimuli in which shape features have been arbitrarily associated with the self and a stranger identity ( Figure 3 ), we measured whether mere social associations lead to a differential allocation of attention across the visual field, or an increase/decrease in processing rates for self- and other-associated stimuli.⟦>zach claim=gap: @{Using a TOJ task with stimuli in which shape features have been arbitrarily associated with the self and a stranger identity ( Figure 3 ), we measured whether mere social associations lead to a differential allocation of attention across the visual field, or an increase/decrease in processing rates for self- and other-associated stimuli.}⟧

Perceptual salience effects were quantified within the same task and stimuli, by altering local color features.

Baseline TOJ measures were conducted for each participant, thereby allowing control for individual, pre-existing biases towards specific perceptual features.

Hence, reported difference scores between baseline and social association conditions (i.e. in w p e f f e c t \begin{document}$w_{peffect}$\end{document} , Δ v p \begin{document}$\Delta v_{p}$\end{document} , or Δ v r \begin{document}$\Delta v_{r}$\end{document} ) are directly indicative of processing changes resulting from social/perceptual salience.

Figure 3. Task design.⟦>zach claim=gap: @{Figure 3. Task design.}⟧

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

Furthermore, to establish the extent to which early attentional selection contributes to frequently observed SPEs using shape-label matching tasks ( Sui et al., 2012 ), we determined SPEs via this well-established paradigm.

Employing the shape-label matching paradigm allowed us to form and practice associations between shapes and identities, while at the same time providing a (crude) independent measure of individual SPEs in matching.

Within this task, self-relatedness biases build up over several processing stages including perception, attention, memory, and decision-making, leading to a behaviorally meaningful response-facilitation towards stimuli associated with the self.

Group-level SPE measures were used to assess whether the included stimuli elicit self-prioritization benefits in the present sample, while, at the individual level, SPE measures were regressed over TVA parameters that indicated self-biases.

The latter allowed us to determine whether the effects that attentional selection elicits in the perceptual or social representations contribute substantially to the SPE observed in the shape-label matching performance.

Material availability statement Research questions, analyses, models, and additional details have been preregistered on the Open Science Framework: https://osf.io/ehu75 .

The analysis notebooks and data are also available via the OSF project repository: https://osf.io/a62df .


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


## discussion

Discussion The present study investigated the mechanisms by which social salience biases attentional selection.

Using a theory-informed Bayesian modeling framework of visual attention (TVA), we established evidence for effects of social and perceptual salience and assessed their interaction.

In conjunction with the TOJ paradigm, TVA offers a clearly formalized, systematic framework for understanding attentional selection, allowing researchers to probe mechanisms via which attention facilitates encoding of sensory information into visual short-term memory.

Its reliability and theoretical importance in describing attention and attentional selection of perceptually salient information have been demonstrated in previous studies ( Krüger et al., 2016 ; Krüger et al., 2017 ).

The present study demonstrates the applicability of TVA in examining attentional selection of socially salient information, and its interaction with perceptual salience.

Social salience effects in attentional selection – processing levels (Experiment 1) For the first time, we established that mere social relevance influences how attentional resources are allocated across the visual field: self-reference leads to changes in processing capacity and the allocation of resources across the visual field.

That is, when sensory information becomes associated with social identities, its social connotation affects early attentional selection.

Interestingly, the active decoding of social information was not necessary for this effect to take place.

When participants had to decide which of two shapes flickered first, processing rates for self-associated shapes increased, relative to other-associated shapes, as a result of social association (i.e. relative to baseline).

The conscious decoding of social associations was unnecessary for this effect to emerge, providing evidence against the claim that self-relatedness strictly has to be a conscious, goal-related feature in order to induce self-prioritization (e.g. Golubickis and Macrae, 2023 ; Woźniak and Knoblich, 2022 ).

Instead, it supports further evidence showing that self-prioritization may emerge from the intrinsic nature of self-processing ( Lee et al., 2021 ; Zhang et al., 2023 ) and unfolds across different stages of the processing hierarchy ( Desebrock and Spence, 2021 ; Reuther and Chakravarthi, 2017 ; Scheller and Sui, 2022b ), with early processing stages being affected in an almost automatic fashion ( Alexopoulos et al., 2012 ; Geng and Xu, 2011 ; Humphreys and Sui, 2015 ; Sui et al., 2014 ; Yin et al., 2019 ).

It further supports the framework of the Self-Attention Network (SAN; Humphreys and Sui, 2016 ), which outlines the crucial role of attention in the behavioral facilitation of self-related information.

This framework suggests that early self-prioritization arises in an automatic fashion while subsequent, active suppression is required when non-self-related information becomes goal-relevant.

Further evidence for the multi-stage nature of self-prioritization in information processing is given by the fact that SPEs, measured via the shape-label matching tasks ( Sui et al., 2012 ), which involves several higher-level processing stages, only correlated with the processing rate changes at higher processing levels in the current TVA-TOJ task.

In other words, the SPEs measured via shape-label matching are more similar to the individuals’ attentional selection effects at higher-level, social decoding stages.

Note, however, that self-relatedness biases at later processing levels do not rule out its automatic capture of attention at earlier levels of perceptual processing.

Previous studies that established that self-ownership can favor attentional selection ( Constable et al., 2019 ; Jublie and Kumar, 2021 ; Truong et al., 2017 ) suggested that a social decision dimension was necessary ( Constable et al., 2019 ).

The present investigation, therefore, contrasted perceptual and social salience across corresponding decisional dimensions: shape-specific (perceptual) versus identity-specific (social) decisions.

Interestingly, we found that the decisional dimension had differential effects on social salience effects.

Automatic biases that were favoring the self-associated stimulus were only present at the perceptual decision level, but not at the social decision level.

When active decoding of social information was required, the same participant group that showed self-prioritization in early attentional selection instead showed no bias for the self, but a bias towards other-associated shapes.

However, the relative slowing in processing rates for the self-associated stimuli was individual-specific.

That is, those with the strongest self-relatedness benefit in shape-label matching showed the smallest decrease/the largest increase in processing rates for the self.

This suggests that, rather than a general self-bias in the population, the benefit depended on the strength of self-representation.

In contrast to previous studies, we controlled for any individual-specific, pre-existing biases, such as shape-preference biases, by including a baseline task prior to social association induction.

This control allowed us to ensure that the attentional biases we measured were the direct result of perceptual and social salience.

While we observed automatic attentional allocation effects towards the self-associated stimulus, the explicit decoding of the associated social identity led to a relative slowing of processing rates for the self-associated stimulus.

This is opposite to what we expected and what was reported in previous studies (e.g. Constable et al., 2019 ; Jublie and Kumar, 2021 ), begging the question as to why this pattern emerged in the present task.

One possibility is the type of social association that was being used: mere social association with arbitrary objects versus ownership ( Constable et al., 2019 ) or bodily self-representation (faces; Jublie and Kumar, 2021 ).

Another alternative may be that the present study used a different type of event, for which the temporal order had to be established: Instead of assessing the order of stimulus onset, we asked participants to determine the order in which two stimuli flickered.

We chose this particular event as TVA posits that attentional selection requires an initial wave of unselective attentional capacity buildup across the visual field, before attentional weights are selectively distributed across the processing channels to alter the rate at which information is subsequently processed ( Bundesen et al., 2005 ).

Even bottom-up driven perceptual salience effects require an initial 150–200 ms to build up sufficient attentional processing capacity to show the typical, beneficial perceptual salience effects ( Krüger and Scharlau, 2021a ).

A previous series of experiments on perceptual salience effects using TVA-TOJ showed that other events such as stimulus onset and stimulus offset failed to elicit expected benefit of pure bottom-up perceptual salience manipulations (orientation, color), likely because they induced more permanent changes in the salience of the display ( Krüger et al., 2016 ).

Instead, a brief stimulus flicker allowed to probe the mechanisms of perceptual salience.

Together with our findings of the differential effects of decision dimension in Experiment 1, this suggests that previous reports of prior entry (stimulus onset, social decision dimension in Constable et al., 2019 ; Truong et al., 2017 ) likely resulted from higher-level processing stages.

Hence, the present study provides the first account of subconscious, automatic effects of mere self-relatedness on early attentional selection during perception.

The factors that lead to changes in directionality of these effects remain to be explored in future studies.

Comparing social and perceptual salience (Experiment 2) By combining social associations with perceptual salience, the present study allowed establishing, for the first time, similarities, differences, and interactions between social and perceptual salience effects.

Experiment 2 revealed that changing local color features of the targets, relative to the background objects, produced the expected perceptual-salience effects, which have been reported in previous studies using TVA-TOJ ( Krüger et al., 2016 ; Krüger et al., 2017 ).

That is, local color alterations produced a shift in attentional weights towards the more salient stimulus.

The increase in attentional weight in the present study w p e f f e c t \begin{document}$w_{peffect}$\end{document} = 0.059 [0.037 – 0.081] was similar, albeit slightly larger, in magnitude to the one reported by Krüger et al., 2016 ; w p e f f e c t \begin{document}$w_{peffect}$\end{document} = 0.043. Inducing social salience, on the other hand, led to decreases in processing rates for the self-associated (presumably salient) stimulus, at least when active decoding of the social identities was required – an unpredicted effect possibly reflecting later, compensatory mechanisms overriding automatic perceptual benefits obtained by self-relatedness (as outlined above).

We investigated whether the different decisional dimensions used for social salience versus perceptual salience contributed to any effect differences, by including two conditions assessing the effects of perceptual salience on specifically associated shapes (self, other) under the same decisional dimension.

Here, we observed that perceptual salience effects were diminished by social associations, with a stronger effect reduction in the self-associated shape.

Notably, the reduction in perceptual salience benefit corresponded to the decrease in processing rates for the self-associated and other-associated shapes, suggesting additive rather than interactive effects of perceptual and social salience.

This additive pattern may reflect that perceptual and social salience were induced in different features (color and shape, respectively) and may therefore have led to a trade-off in attentional resource allocation.

Indeed, even perceptual salience effects across two different feature dimensions, luminance and orientation contrasts, have previously been reported to be additive ( Krüger et al., 2017 ), reflected in the TVA parameter Kappa ( Nordfang et al., 2013 ).

The processing speeds at which this information races can be influenced both by social and perceptual salience.

While not completely ruling out that perceptual and social salience interact at any point in the processing hierarchy, our findings indicate that, when they are induced in different stimulus features, their salience effects on attentional selection are independent and additive.

Using TVA’s report categories and the modulatory Beta parameter, future work could investigate the interactions between perceptual and social categorizations.

Interestingly, while the average effects of social and perceptual salience were mostly additive, their respective contributions differed: prediction model comparisons revealed that when the self-related stimulus was also perceptually salient, the processing benefit magnitude was mostly predicted by the social salience of the stimulus, and to a lesser, even if substantial, extent by perceptual salience.

On the contrary, for other-related stimuli, the processing benefit magnitude was determined primarily by its perceptual salience alone.

This suggests that the trade-off between perceptual and social salience in attentional selection differs between self- and other-associated stimuli: Self-relatedness has the power to partially overwrite the effects of bottom-up perceptual salience on attentional selection, while other-association does not.

Conclusions Overall, a consistent finding that emerges across the literature is that prioritization of social information requires the deployment of attention ( Alexopoulos et al., 2012 ; Humphreys and Sui, 2016 ; Sui and Rotshtein, 2019 ; Wade and Vickery, 2018 ).

However, the mechanisms by which attention shapes different stages of information processing to facilitate self-related processing are not fully understood.

Here, we show that mere self-association with arbitrary shapes can alter attentional selection at early, perceptual processing stages, leading to increased processing rates for self-associated stimuli.

Crucially, this self-prioritization occurs in an automatic fashion that does not require the active decoding of the associated social identities.

Secondly, we show that varying the decisional dimension alters the degree of processing benefit obtained from social relevance, highlighting the multi-stage nature of self-relatedness effects in information processing.

Thirdly, our results suggest that social and perceptual salience do not interact during information processing but are likely processed in parallel: while perceptual salience showed robust increases in processing rates, this effect reduced in socially associated stimuli, consistent with the processing rate reductions associated with self and others.

Lastly, exploratory intra-individual correlations showed that the relative contribution of social and perceptual salience to attentional selection depended on the social association: self-relatedness was considered more strongly than perceptual salience, while perceptual salience was considered more strongly than other-relatedness.

This investigation provides the first evidence outlining how self-relatedness leads to automatic, perceptual benefits through early attentional selection, and how social and perceptual salience shape attentional deployment.

These findings shed light on core mechanisms underlying the pervasive SPEs that fundamentally shape human information processing hierarchy from early perceptual encoding to higher-order cognition and conscious awareness.


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
