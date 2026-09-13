# Distinct representational properties of cues and contexts shape fear and reversal learning

<!-- bouyeure-2026-fear-rsa · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

When we learn that something is dangerous, a fear memory is formed.

However, this memory is not fixed and can be updated through new experiences, such as learning that the threat is no longer present.

This process of updating, known as extinction or reversal learning, is highly dependent on the context in which it occurs.

How the brain represents cues, contexts, and their changing threat value remains a major question.

Here, we used functional magnetic resonance imaging and a novel fear learning paradigm to track the neural representations of stimuli across fear acquisition, reversal, and test phases.

We found that initial fear learning creates generalized neural representations for all threatening cues in the brain’s fear network.

During reversal learning, when threat contingencies switched for some of the cues, two distinct representational strategies were observed.

On the one hand, we still identified generalized patterns for currently threatening cues, whereas on the other hand, we observed highly stable representations of individual cues (i.e. item-specific) that changed their valence, particularly in the precuneus and prefrontal cortex.

Furthermore, we observed that the brain represents contexts more distinctly during reversal learning.

Furthermore, additional exploratory analyses showed that the degree of this context specificity in the prefrontal cortex predicted the subsequent return of fear, providing a potential neural mechanism for fear renewal.

Our findings reveal that the brain uses a flexible combination of generalized and specific representations to adapt to a changing world, shedding new light on the mechanisms that support cognitive flexibility and the treatment of anxiety disorders via exposure therapy.


## introduction

Introduction Fear acquisition describes the process by which a previously neutral cue, the conditioned stimulus (CS), becomes associated with an aversive, unconditioned stimulus (US), and eventually comes to evoke fear on its own.

It is typically a rapid and robust process that may create long-lasting fear memories that can persist after the threats have passed.

This persistence can be evolutionarily advantageous, since it may be adaptive to respond to a false alarm rather than miss a potential threat.

However, failing to suppress a fear response in the absence of actual danger can be maladaptive and has been proposed as a key etiological factor in conditions, such as anxiety disorders and post-traumatic stress disorder ( Milad and Quirk, 2012 ).

While fear acquisition is rapid and robust, the suppression of fear responses in the absence of the US – i.e., fear extinction – is strongly context-dependent and more flexible ( Maren et al., 2013 ; Milad and Quirk, 2012 ; Liu et al., 2024 ).

This is demonstrated by the phenomena of spontaneous recovery, renewal, and reinstatement, all of which show that the original fear memory can resurface under certain conditions ( Bouton, 2002 ).

Specifically, fear renewal reflects a return of fear responses after a change in context, showing that extinction does not erase the original fear memory trace but inhibits it selectively within the extinction context ( Greco and Liberzon, 2016 ).

Learning and extinction do not occur only in relation to fear but also during reinforcement learning and reversal, reflecting sensitivity to contingency changes more generally ( Schiller et al., 2008 ; Wisniewski et al., 2023 ).

In these cases, the context dependency of extinction may support cognitive flexibility since appropriate actions can be selected according to situational demands ( Schiller and Delgado, 2010 ; Chaby et al., 2019 ; Xin et al., 2024 ).

Contrastingly, the context specificity of extinction learning may be detrimental during treatments of anxiety disorders if therapy-induced fear reductions do not generalize beyond the therapeutic setting ( Maren et al., 2013 ).

Much of our fundamental understanding of the formation of fear memory traces and their suppression during extinction learning has been derived from optogenetic studies in rodents, which describe the formation and modification of fear engrams with valence and context representations in the amygdala and hippocampus, respectively ( Liu et al., 2015 ; Josselyn et al., 2015 ; Redondo et al., 2014 ).

These studies further show that extinction learning depends on plasticity of hippocampal context representations ( Redondo et al., 2014 ) as well as on prefrontal cortex engrams ( Ramanathan et al., 2018 ; Gu et al., 2022 ; Lissek and Tegenthoff, 2024 ).

In humans, neuroimaging studies have reported activation of a canonical ‘fear network’ during acquisition (with prominent roles of the dorsal anterior cingulate cortex and insula, and a more inconsistent role of the amygdala; Fullana et al., 2016 ), and recruitment of the hippocampus and ventromedial prefrontal cortex during extinction ( Fullana et al., 2016 ; Maren et al., 2013 ).

Taken together, these findings putatively reflect context dependency and safety learning, respectively ( Maren et al., 2013 ).

Indeed, meta-analyses have shown that despite some moderate overlap, the brain regions involved in extinction learning differ substantially from those involved in fear acquisition ( Maren et al., 2013 ).

Moreover, reversal – involving a change in contingencies rather than the mere absence of a US – particularly engages regions involved in prediction error detection and cognitive flexibility, such as the dorsomedial and lateral prefrontal cortex ( Wisniewski et al., 2023 ; Xin et al., 2024 ).

This points towards the inhibition of previously threatening stimuli via executive control during reversal, a process not typically observed in standard extinction paradigms.

While mass-univariate functional magnetic resonance imaging (fMRI) activation studies have been instrumental in identifying the brain regions involved in fear learning and extinction, they are insensitive to the patterns of neural activity that underlie the stimulus-specific representations of threat cues and contexts.

Contrastingly, multivariate pattern analysis methods, such as representational similarity analysis (RSA; Kriegeskorte et al., 2008 ), have emerged as a powerful tool to investigate the content and structure of these representations (e.g. Hennings et al., 2022 ).

This approach allows us to characterize the ‘representational geometry’ of a set of items – i.e., the structure of similarities and dissimilarities between their associated neural activity patterns.

This geometry reveals how the brain organizes information, for instance, by clustering items that are conceptually similar while separating those that are distinct.

This method has provided important novel insights into the representational signatures that support the formation, stabilization, and possible subsequent refinement and modification of memory traces ( Rissman and Wagner, 2012 ; Heinen et al., 2024 ).

This has informed our understanding of the basic mechanisms of learning and memory, while also contributing to more mechanistic theories of memory distortions in mental disorders.

For example, Visser et al., 2011 ; Visser et al., 2013 demonstrated that trial-by-trial similarities of blood oxygen level-dependent (BOLD) patterns increase during associative learning in regions of the fear network, such as the anterior cingulate cortex (ACC), ventromedial prefrontal cortex (vmPFC), or superior frontal cortex.

Similar representational signatures of ‘cue generalization’ – i.e., increasing levels of similarity among the memory traces of different items associated with the same valence – were observed in the amygdala related to memories of a stressful episode ( Bierbrauer et al., 2021 ), as well as in sensory regions and areas of the salience network for aversive trauma-analogue stimuli ( Kobelt et al., 2024 ).

Furthermore, RSA can be used to study how specific neural patterns are reactivated during memory, a mechanism also referred to as ‘encoding-retrieval similarity’ (e.g. Kobelt et al., 2024 ).

For example, Hennings et al., 2022 observed a selective reactivation of fear versus extinction memories in the medial PFC and hippocampus depending on encoding context.

Furthermore, we can measure the consistency of a neural pattern for a given item across multiple presentations.

This metric, which we refer to as ‘item stability,’ quantifies how consistently a specific stimulus (e.g. the image of a kettle) is represented in the brain across multiple repetitions of the same item.

Notably, higher item stability has been linked to successful episodic memory encoding ( Xue, 2018 ; Xue et al., 2010 ).

Finally, the difference between item stability and item generalization, commonly referred to as ‘specificity’ ( Xue et al., 2010 ; Xue et al., 2013 ; Zheng et al., 2018 ; Sommer et al., 2022 ), quantifies the amount of item-specific information in a representation.

This representational property could be particularly fruitful as a means to study the influence of fear reversal or extinction on context representations, which, despite some notable exceptions (e.g. Hennings et al., 2020 ), have been less systematically investigated than cue representations across different learning stages.

Here, we aimed to systematically investigate how the neural representations of cues and contexts change across different phases of learning.

The phases include acquisition, reversal, and two consecutive test phases with new contexts and previous contexts, respectively, in which all cues are extinguished.

We presented the CS cues in each phase in multiple different contexts that changed between phases, which allowed us to study the role of context specificity by comparing the similarity between same vs. different contexts in each phase (see Figure 1 ).⟦>zach claim=d903f2eb-e683-43c7-8feb-1bc1ee72597b: @{We presented the CS cues in each phase in multiple different contexts that changed between phases, which allowed us to study the role of context specificity by comparing the similarity between same vs. different contexts in each phase (see Figure 1 ).} trace-conditioning-hippocampus-engaged⟧

For clarity, we use the term ‘test’ interchangeably with ‘test phase’ throughout the manuscript.

Figure 1. Overview of the paradigm and analysis approach.⟦>zach claim=d903f2eb-e683-43c7-8feb-1bc1ee72597b: @{Figure 1. Overview of the paradigm and analysis approach.} trace-conditioning-hippocampus-engaged⟧

(A) Example structure of a trial.⟦>zach claim=gap: @{(A) Example structure of a trial.}⟧

Each trial comprises the presentation of a context video, cue, and unconditioned stimulus (US) expectancy rating.

Electric shocks (US) are administered in reinforced trials during acquisition (following CS++ and CS+- cues) and reversal (following CS++ and CS-+ cues), with reinforcement rates of 50%.

( B ) Paradigm structure with four different experimental phases (rows) and four different cue types (columns).⟦>zach claim=gap: @{( B ) Paradigm structure with four different experimental phases (rows) and four different cue types (columns).}⟧

Each cue type consists of two possible items.

( C ) Conditioned stimulus (CS) items (left) and context videos (right).⟦>zach claim=gap: @{( C ) Conditioned stimulus (CS) items (left) and context videos (right).}⟧

Each color indicates a set of four thematically related context videos.

Different sets are used across phases (see Table in B).

( D ) Representational Similarity Matrices (RSMs) for each experimental phase, shown here from the dorsal anterior cingulate cortex (ACC) for illustrative purposes.⟦>zach claim=gap: @{( D ) Representational Similarity Matrices (RSMs) for each experimental phase, shown here from the dorsal anterior cingulate cortex (ACC) for illustrative purposes.}⟧

Lightning images represent reinforced cue types in the different learning phases.

Representations of threatening cues are more similar to each other (warmer colors), reflecting cue generalization.

( E ) Top: Cue generalization mask for the representational similarity analysis (RSA) matrices estimated within each searchlight.⟦>zach claim=gap: @{( E ) Top: Cue generalization mask for the representational similarity analysis (RSA) matrices estimated within each searchlight.}⟧

The mask is superimposed on the RSMs (shown in C ) to compute the average similarity between the different cues of each CS type (different colors).

Average cue generalization values are then compared between CS types.

Bottom: Item stability mask estimated within each searchlight.

The mask is superimposed on the RSMs to compute the average similarity across trials of each cue, separately for each CS type (different colors).

Average item stability values are then compared between CS types.

We hypothesized that the representational geometry of CS cues changes across learning phases, reflecting the inhibition of fear memories during reversal, as well as the formation of novel memories of cues with updated contingencies.

More specifically, we expected cue generalization effects in regions of the fear network, item stability in areas related to episodic memory, and context-specific representations in the hippocampus and PFC.

Finally, we hypothesized that increased context specificity during reversal would influence the reinstatement of fear memory traces during the test phases.

To test our hypotheses regarding the representational geometry of threat and safety, we used a multi-day fMRI paradigm that dissociates cue-specific learning from contextual modulation.

The task was presented through a narrative (‘Nina the Unlucky Backpacker’) to provide an ecologically valid framework for fear acquisition and reversal.

We employed a trace conditioning design, using a temporal gap between stimulus and reinforcement to specifically engage hippocampus-dependent memory systems.

In each trial, participants viewed a Context (2 s video of a natural scene) followed by a CS (1 s image of a household appliance) embedded within that scene.

Throughout the task, participants provided real-time US expectancy ratings, allowing us to correlate neural representational changes with behavioral indices of learning.

The experiment was divided into four phases across two days to capture the evolution of memory traces (see Figure 1 for a detailed schema).⟦>zach claim=d903f2eb-e683-43c7-8feb-1bc1ee72597b: @{The experiment was divided into four phases across two days to capture the evolution of memory traces (see Figure 1 for a detailed schema).} trace-conditioning-hippocampus-engaged⟧

Day 1 (Acquisition and Reversal): We first established fear associations (Acquisition) and subsequently altered them (Reversal).

This created four distinct functional cue types: stable threat (CS++), extinguished threat (CS+-), newly acquired threat (CS-+), and stable safety (CS--).

Day 2 (Test phases).

To assess the context-dependency of these memories, we conducted two test phases under extinction (no US delivery): In the ‘Test new ’ phase, CS cues were presented in novel natural scenes; in the ‘Test old ’ phase, cues were returned to their original acquisition or reversal contexts, while the US remained absent.

By presenting each CS across multiple different contexts and repetitions within each phase, we were able to apply RSA methods to quantify item stability (consistency of a cue’s representation across repetition), cue generalization (similarity between cues of the same valence), and context specificity (the difference between context stability and context generalization, quantifying the amount of context-specific information for each phase).

The following Results section details how these representational metrics evolved as Nina (and the participants) learned to navigate changing threats across different environments.

For a full description of the stimulus sets, counterbalancing procedures, and the statistical procedures, please refer to the Methods section at the end of the manuscript.


## results

Results Behavioral results We first examined the trial-wise US expectancy ratings across experimental phases.

A linear mixed effects (LME) model with ‘CS type’ and ‘experimental phase’ as fixed effects and ‘participant’ as a random effect revealed significant effects of CS type (F(1816.6, 605.54)=479.35, p <0.0001) and experimental phase (F(476.3, 158.78)=125.6, p <0.001) as well as a significant interaction (F(334.8, 37.2)=29.45, p <0.001), showing that both CS type and experimental phases affected US expectancy ( Figure 2A ).⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{A linear mixed effects (LME) model with ‘CS type’ and ‘experimental phase’ as fixed effects and ‘participant’ as a random effect revealed significant effects of CS type (F(1816.6, 605.54)=479.35, p <0.0001) and experimental phase (F(476.3, 158.78)=125.6, p <0.001) as well as a significant interaction (F(334.8, 37.2)=29.45, p <0.001), showing that both CS type and experimental phases affected US expectancy ( Figure 2A ).} behavioral-learning-confirms-contingencies⟧

Post-hoc paired Wilcoxon tests (Bonferroni-corrected) showed that ratings to all CS types were significantly different from each other across all the experimental phases (CS++ > CS+- > CS-+ >CS--; all p <0.01) except during fear acquisition, in which CS ++ and CS+- cues on the one hand, and CS-+ and CS-- cues on the other hand were equivalent, as expected at this stage.⟦>zach claim=7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d: @{Post-hoc paired Wilcoxon tests (Bonferroni-corrected) showed that ratings to all CS types were significantly different from each other across all the experimental phases (CS++ > CS+- > CS-+ >CS--; all p <0.01) except during fear acquisition, in which CS ++ and CS+- cues on the one hand, and CS-+ and CS-- cues on the other hand were equivalent, as expected at this stage.} context-specificity-predicts-acquisition-reinstatement-regional-dissociation⟧

Indeed, during fear acquisition, CS+- and CS ++ on the one hand, and CS-+ and CS-- on the other, are still functionally identical, since fear acquisition occurs before the valence change of CS-+ (newly acquired threat: from CS- to CS+) and CS+- (extinguished threat: from CS + to CS-) operated during fear reversal.

Post-hoc pairwise comparisons between experimental phases across all CS types were significant as well (reversal >acquisition > test new >test old ; all p <0.0001), and fear reversal and acquisition were the experimental phases with the highest US expectancy.⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{Post-hoc pairwise comparisons between experimental phases across all CS types were significant as well (reversal >acquisition > test new >test old ; all p <0.0001), and fear reversal and acquisition were the experimental phases with the highest US expectancy.} behavioral-learning-confirms-contingencies⟧

The CS type with the highest US expectancy was, as expected, CS++.

Figure 2. US expectancy ratings and univariate activation results.⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{Figure 2. US expectancy ratings and univariate activation results.} behavioral-learning-confirms-contingencies⟧

( A ) Unconditioned stimulus (US) expectancy ratings and univariate activity difference between cue types across experimental phases.⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{( A ) Unconditioned stimulus (US) expectancy ratings and univariate activity difference between cue types across experimental phases.} behavioral-learning-confirms-contingencies⟧

Dotted lines separate the four experimental phases.

Participants quickly learned the contingencies of each cue type and their changes across the experimental phases.

( B ) Univariate activation results.⟦>zach claim=e5023cc6-f631-4d2b-b768-ed36dbef9edb: @{( B ) Univariate activation results.} no-bold-differences-test-phases⟧

Significant second-level results are shown for different contrasts in the different experimental phases.

Significance was assessed at the cluster level with 10 k permutations (p uncorr <0.001).

To examine the interaction between US expectancy and CS type, we conducted post-hoc Wilcoxon tests (Bonferroni-corrected), which revealed different patterns of CS differences between experimental phases ( Supplementary file 1a ).

Activation of fear network by cues signaling current and prior threats Next, we assessed activity differences between CS types during each experimental phase ( Figure 2B ).⟦>zach claim=e5023cc6-f631-4d2b-b768-ed36dbef9edb: @{Activation of fear network by cues signaling current and prior threats Next, we assessed activity differences between CS types during each experimental phase ( Figure 2B ).} no-bold-differences-test-phases⟧

During acquisition, the CS+ > CS- contrast (aggregating CS ++ and CS+- on the one hand, CS-+ and CS-- on the other) showed significantly increased BOLD activity in several clusters across the fear network, such as the dACC, superior frontal gyrus, caudate nucleus, and middle temporal gyrus (MTG; see Figure 2Bi ), in line with previous work (e.g. Fullana et al., 2016 ).

The opposite contrast CS- > CS+ showed no significant clusters.

During fear reversal, a contrast of current valence, i.e., (CS ++ and CS-+) > (CS+- and CS--) showed activation patterns similar to those during fear acquisition, spanning across the fear network ( Figure 2Bii ), reflecting the newly learned status of ‘newly acquired threat’ for CS-+ and of ‘extinguished threat’ for CS+-.

We then contrasted currently threatening and safe cues depending on their previous valence (i.e. their fear acquisition valence), (CS++ > CS+-) > (CS-+ > CS--), which also revealed activation in the fear learning network, although to a lesser extent ( Figure 2Biii ).

This result may reflect the impact of the lingering fear memory trace (remaining from acquisition) and/or the time required to learn contingency changes during reversal.

During the two test phases, none of the contrasts between CS types (CS++ > CS--, CS-+ > CS--, CS+- > CS--) revealed any significant activity differences.

Thus, BOLD responses were similar for all CS types in the absence of a US, even though differences in US expectancy ratings were observed at the behavioral level.

This further underlines the necessity for an analysis of representational patterns rather than mere univariate activity differences.

Generalized representations of threat cues during acquisition and reversal We thus focused our analyses on the representational geometry of cues across experimental phases.

We examined the effect of cue type on two distinct representational properties, cue generalization (between-cue similarity) and item stability (within-cue similarity), using a whole-brain searchlight approach ( Figure 3A ).⟦>zach claim=e645b7b4-05c4-4b37-b75f-3e47c0d585b2: @{We examined the effect of cue type on two distinct representational properties, cue generalization (between-cue similarity) and item stability (within-cue similarity), using a whole-brain searchlight approach ( Figure 3A ).} cue-generalization-increases-acquisition⟧

Figure 3. Enhanced cue generalization and item stability of threat cues.⟦>zach claim=e645b7b4-05c4-4b37-b75f-3e47c0d585b2: @{Figure 3. Enhanced cue generalization and item stability of threat cues.} cue-generalization-increases-acquisition⟧

( A ) Cue representations during acquisition showing higher cue generalization of conditioned stimulus (CS)+ than CS- cues.⟦>zach claim=e645b7b4-05c4-4b37-b75f-3e47c0d585b2: @{( A ) Cue representations during acquisition showing higher cue generalization of conditioned stimulus (CS)+ than CS- cues.} cue-generalization-increases-acquisition⟧

No differences in item stability were found.

( B ) Cue representations during reversal.⟦>zach claim=no-assertion: @{( B ) Cue representations during reversal.} A bare panel label naming what the panel shows.⟧

( Bi ) Higher cue generalization of CS++ than CS-- cues.

( Bii ) Higher cue generalization of currently threatening than non-threatening cues i.e., (CS-+ and CS++) > (CS+- and CS--).

( Biii ) Higher item stability of cues with changing valence than cues with consistent valence, i.e., (CS-+ and CS+-) > (CS++ and CS--).

( C ) Cue representations during test new showing higher item stability of previously safe cues vs. always threatening cues (CS+-) > (CS++).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{( C ) Cue representations during test new showing higher item stability of previously safe cues vs. always threatening cues (CS+-) > (CS++).} item-stability-persists-test-phases⟧

( D ) Cue representations during test old showing higher item stability of ‘always threatening’ vs. ‘never threatening’ cues (CS++) > (CS--).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{( D ) Cue representations during test old showing higher item stability of ‘always threatening’ vs. ‘never threatening’ cues (CS++) > (CS--).} item-stability-persists-test-phases⟧

All plots depict t-values from searchlight analyses within family-wise error-corrected clusters (uncorrected p <0.001, corrected p <0.025 for Acquisition, and p <0.0125 for the other phases) with 10 k permutations.⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{All plots depict t-values from searchlight analyses within family-wise error-corrected clusters (uncorrected p <0.001, corrected p <0.025 for Acquisition, and p <0.0125 for the other phases) with 10 k permutations.} behavioral-learning-confirms-contingencies⟧

During fear acquisition, we again combined CS ++ and CS+- cues (both followed by a US in 50% of trials) into a common CS + category, and CS-- and CS-+ cues (never followed by a US) into a common CS- category.

We found that item stability did not differ between CS + and CS- cues.

Importantly, however, cue generalization was significantly higher for CS + compared to CS- cues in several clusters across the fear network, with a pattern reminiscent of the results during the corresponding univariate analyses.

Thus, the dACC, superior frontal gyrus, caudate nucleus, and insula were among the regions showing higher cue generalization of CS + compared to CS- cues ( Figure 3C ; Supplementary file 1b ).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{Thus, the dACC, superior frontal gyrus, caudate nucleus, and insula were among the regions showing higher cue generalization of CS + compared to CS- cues ( Figure 3C ; Supplementary file 1b ).} item-stability-persists-test-phases⟧

This suggests the formation of a higher-order association (i.e. a category-level stability) between threatening cues and less so between safe cues during fear acquisition.

The opposite contrast (CS- > CS+) did not reveal any significant effects.

Distinct functional roles, spatial distributions, and subsequent persistence of item stability and cue generalization during reversal Next, we compared item stability and cue generalization between the four CS types during fear reversal ( Figure 3B–D ).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{Distinct functional roles, spatial distributions, and subsequent persistence of item stability and cue generalization during reversal Next, we compared item stability and cue generalization between the four CS types during fear reversal ( Figure 3B–D ).} item-stability-persists-test-phases⟧

We first compared CS++ and CS-- cues, corresponding to the CS+ vs. CS- contrast during fear acquisition ( Figure 3B ).⟦>zach claim=no-assertion: @{We first compared CS++ and CS-- cues, corresponding to the CS+ vs. CS- contrast during fear acquisition ( Figure 3B ).} Narration of which contrast was run first; the result follows in the next sentences.⟧

Again, we observed higher cue generalization for CS++ compared to CS-- cues in the dACC, but not in any of the other regions where cue generalization effects were observed during acquisition.

Comparing the cue generalization of all CS cues that are threatening in reversal (CS++ and CS-+) to the ones that are not (CS+- and CS--) revealed similar results to fear acquisition, with increased cue generalization across fear learning network regions, including the dACC, superior frontal gyrus (SFG), medial temporal gyrus, and inferior frontal gyrus (IFG) ( Figure 3C ).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{Comparing the cue generalization of all CS cues that are threatening in reversal (CS++ and CS-+) to the ones that are not (CS+- and CS--) revealed similar results to fear acquisition, with increased cue generalization across fear learning network regions, including the dACC, superior frontal gyrus (SFG), medial temporal gyrus, and inferior frontal gyrus (IFG) ( Figure 3C ).} item-stability-persists-test-phases⟧

Item stability, in line with results from fear acquisition, did not differ between currently threatening and non-threatening cues.

Moreover, we found no significant clusters when comparing item stability between CS++ vs. CS-- cues.

We then investigated representational effects of contingency changes and compared cues that changed their contingency between acquisition and reversal (CS+- and CS-+) to cues with consistent contingencies (CS-- and CS++), resulting in the ‘change vs. no-change’ contrast, i.e., (CS+- & CS-+) > (CS++ and CS--).

Item stability was significantly higher for changing than consistent cues in the precuneus and IFG, i.e., in regions that overlapped with those showing higher cue generalization for threatening cues ( Supplementary file 1c ; Figure 3Biii ).

Conversely, this contrast did not reveal any differences in cue generalization.

We next investigated item stability and cue generalization during test new and test old , i.e., when USs are absent for all CS types.

In order to understand the impact of prior contingencies – i.e., of lingering fear memory traces – on test new and test old , we examined the contrast between CS++, CS-+, and CS+- with CS-- (safe baseline), as well as the contrast between CS-+ and CS+- with CS++ (unsafe baseline) in these two phases.

Cue generalization did not differ between CS types during either test new or test old .

However, item stability was higher for CS+- vs. CS ++cues in a middle temporal cluster during test new ( Figure 3E ), and for CS++ compared to CS-- cues in an inferior temporal cluster during test old ( Figure 3F ; Supplementary file 1d ).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{However, item stability was higher for CS+- vs. CS ++cues in a middle temporal cluster during test new ( Figure 3E ), and for CS++ compared to CS-- cues in an inferior temporal cluster during test old ( Figure 3F ; Supplementary file 1d ).} item-stability-persists-test-phases — The claim states exactly these two effects: higher CS+- than CS++ item stability in middle temporal cortex at test_new, and higher CS++ than CS-- in inferior temporal cortex at test_old.⟧

To summarize, cue generalization and item stability showed a dissociation during reversal, with higher cue generalization for threatening vs. non-threatening cues and higher item stability for changing vs. consistent cues.

This suggests that these two representational properties could capture distinct aspects of contingency learning; the threatening (vs. safe) nature of cues increased cue generalization, while a changing (vs. consistent) nature of contingencies enhanced item stability.

We also found that item stability, but not cue generalization effects, persisted in the absence of a US.

Memory traces from previous learning phases compete for reinstatement during test Fear extinction is commonly described as an inhibitory process, in which a new safety memory trace is created and competes with the previous threat memory trace that is concurrently inhibited ( Lebois et al., 2019 ; Santini et al., 2008 ; Szeska et al., 2020 ).

In our paradigm, the memory traces formed during acquisition and reversal might compete for reinstatement, particularly during the test old phase, because both fear and reversal memories may reoccur during this phase due to context overlap.

We compared the magnitude of reinstatement effects between acquisition and reversal during test old , by using an LME with experimental phase, CS type, and their interaction as predictors, and reinstatement as the predicted variable.

Reinstatement was estimated by comparing either the similarities of identical items across phases (item reinstatement) or the similarities of different items from one cue type across phases (generalized reinstatement).

We extracted these reinstatement values from significant clusters observed in our previous searchlight analyses ( Figure 4A ) and correlated them across participants (see Graner et al., 2020 for a similar approach).⟦>zach claim=7d932232-9c15-45f3-8296-958d3fe84d2a: @{We extracted these reinstatement values from significant clusters observed in our previous searchlight analyses ( Figure 4A ) and correlated them across participants (see Graner et al., 2020 for a similar approach).} rsa-roi-derived-from-searchlight⟧

Figure 4. Different reinstatement patterns are observed for the previous experimental phases during Test old .⟦>zach claim=6ea9d399-1100-4329-8a02-ac61dd04e3d1: @{Figure 4. Different reinstatement patterns are observed for the previous experimental phases during Test old .} Reversal recruits two parallel strategies: generalize threat cues and specify changing-valence cues.⟧

( A ) Region of interests (ROIs) derived from the previous searchlight analyses (see Figure 3 ), by extracting the significant clusters from the previous statistical analyses.⟦>zach claim=e645b7b4-05c4-4b37-b75f-3e47c0d585b2: @{( A ) Region of interests (ROIs) derived from the previous searchlight analyses (see Figure 3 ), by extracting the significant clusters from the previous statistical analyses.} cue-generalization-increases-acquisition⟧

ROIs are color-coded depending on the experimental phase they are derived from: red for acquisition, orange for reversal, green for test new , blue for test old .

When several ROIs overlapped, only the ROI with the bigger voxel size was included in the analyses.

MTG: Middle Temporal Gyrus.

InfTemp: Inferior Temporal Gyrus.

IFG: Inferior Frontal Gyrus. dmPFC: Dorsomedial Prefrontal Cortex.

ACC: Anterior Cingulate Cortex.

SFG: Superior Frontal Gyrus.

( B ) Reinstatement during test old differed between experimental phases, such that: ( Bi ) in IFG, item reinstatement was higher for memory traces from reversal compared to those from acquisition and test new ; and ( Bii ) in dmPFC, generalized reinstatement was higher for memory traces from acquisition compared to those from test new . *:p<0.05. **p<0.01. n=255 for Bi and n=261 for Bii.⟦>zach claim=7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d: @{( B ) Reinstatement during test old differed between experimental phases, such that: ( Bi ) in IFG, item reinstatement was higher for memory traces from reversal compared to those from acquisition and test new ; and ( Bii ) in dmPFC, generalized reinstatement was higher for memory traces from acquisition compared to those from test new . *:p<0.05. **p<0.01. n=255 for Bi and n=261 for Bii.} context-specificity-predicts-acquisition-reinstatement-regional-dissociation⟧

Errors bars represent standard error.

We observed a significant effect of experimental phases on item reinstatement in IFG (F(2,253)=5.50, p <0.01) ( Figure 4Bi ).⟦>zach claim=bcf69f08-b30f-4571-9ecd-69ea60d15414: @{We observed a significant effect of experimental phases on item reinstatement in IFG (F(2,253)=5.50, p <0.01) ( Figure 4Bi ).} ifg-reinstates-reversal-traces-item-specific⟧

Post-hoc Wilcoxon t-tests showed that reversal-test old item reinstatement was significantly higher than acquisition-test old item reinstatement (t(253)=-3.01, p <0.01) and test new -test old item reinstatement (t(253)=-2.7, p <0.05).⟦>zach claim=7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d: @{Post-hoc Wilcoxon t-tests showed that reversal-test old item reinstatement was significantly higher than acquisition-test old item reinstatement (t(253)=-3.01, p <0.01) and test new -test old item reinstatement (t(253)=-2.7, p <0.05).} context-specificity-predicts-acquisition-reinstatement-regional-dissociation⟧

In addition, we observed a significant effect of experimental phases on generalized reinstatement in dmPFC (F(2,259)=4.01, p <0.05) ( Figure 4Bii ), where acquisition-test old generalized reinstatement was higher than test new -test old generalized reinstatement (t(259)=2.96, p <0.05).⟦>zach claim=ebc27c8f-666b-474f-8980-f41e0d25843c: @{In addition, we observed a significant effect of experimental phases on generalized reinstatement in dmPFC (F(2,259)=4.01, p <0.05) ( Figure 4Bii ), where acquisition-test old generalized reinstatement was higher than test new -test old generalized reinstatement (t(259)=2.96, p <0.05).} dmpfc-reinstates-acquisition-traces-generalized⟧

In summary, during the test old , we observed prominent reinstatement of item-specific reversal memory traces in IFG and of generalized acquisition memory traces in dmPFC, suggesting that memories from these two phases tend to come back in different representational formats and in dissociable brain regions.

Context specificity increases during reversal in prefrontal cortex and predicts the reoccurrence of fear memory traces We followed our analyses of cue generalization, item stability, and reinstatement with exploratory analyses of the neural representation of contexts across experimental phases.

Given that memories built during extinction learning tend to be more context-specific than those acquired during initial fear learning ( Maren et al., 2013 ), we established a measure of context specificity, namely the difference between neural representations of same vs. different contexts in each phase.

We also compared this measure across experimental phases and related it to the representational geometries of cues ( Figure 5A ).⟦>zach claim=no-assertion: @{We also compared this measure across experimental phases and related it to the representational geometries of cues ( Figure 5A ).} Narration of which comparisons were made next, with no result.⟧

Figure 5. Context specificity during reversal and its role for reinstatement of fear memory traces.⟦>zach claim=2ff7f5ea-efaf-408e-9ef3-ab46fe395e74: @{Figure 5. Context specificity during reversal and its role for reinstatement of fear memory traces.} pfc-context-specificity-predicts-renewal⟧

( A ) Calculation of context specificity as the difference of within-context similarity and between-context similarity.⟦>zach claim=no-assertion: @{( A ) Calculation of context specificity as the difference of within-context similarity and between-context similarity.} A panel label defining how the context-specificity measure is computed, not a finding.⟧

( B ) Difference in context specificity between acquisition and reversal.⟦>zach claim=4dbc065d-daa5-45e9-96d6-9012b33cb24c: @{( B ) Difference in context specificity between acquisition and reversal.} context-specificity-increases-reversal⟧

Positive values indicate higher context specificity in reversal.

( C ) Calculation of item reinstatement and generalized reinstatement (similarities of item representations across different phases; left) and context specificity (difference between acquisition and reversal; right).⟦>zach claim=no-assertion: @{( C ) Calculation of item reinstatement and generalized reinstatement (similarities of item representations across different phases; left) and context specificity (difference between acquisition and reversal; right).} A panel label defining how the reinstatement and context-specificity measures are computed, not a finding.⟧

An LME model was used to predict these reinstatement measures by the interaction of context specificity and conditioned stimulus (CS) types.

( D ) Higher context specificity during reversal predicted reinstatement during test old , as a function of CS type: ( Di ) Higher reversal context specificity predicted more pronounced generalized reinstatement of CS+- vs. CS-+ acquisition memory traces in anterior cingulate cortex (ACC)/superior frontal gyrus (SFG) (left), and reversely, more pronounced generalized reinstatement of CS-+ vs. CS+- acquisition memory traces in the precuneus (right).⟦>zach claim=7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d: @{( D ) Higher context specificity during reversal predicted reinstatement during test old , as a function of CS type: ( Di ) Higher reversal context specificity predicted more pronounced generalized reinstatement of CS+- vs. CS-+ acquisition memory traces in anterior cingulate cortex (ACC)/superior frontal gyrus (SFG) (left), and reversely, more pronounced generalized reinstatement of CS-+ vs. CS+- acquisition memory traces in the precuneus (right).} context-specificity-predicts-acquisition-reinstatement-regional-dissociation — The claim carries this same regional dissociation: reversal context specificity predicts generalized reinstatement favouring CS+- in ACC/SFG and CS-+ in precuneus.⟧

CS+-, which is threatening in acquisition, is shown in red, and CS-+, which is not threatening in acquisition, is shown in green.

( Dii ) Higher reversal context specificity predicted more pronounced item reinstatement of CS-+ than CS+- reversal memory traces in dorsomedial Prefrontal Cortex (dmPFC).

CS-+, which is threatening in acquisition, is shown in red, and CS+-, which is not threatening in acquisition, is shown in green.

( Diii ) Higher reversal context specificity also predicted more pronounced item reinstatement of CS-+ than CS+- memory traces from reversal in MFG during test new .

As hypothesized, we found that context specificity during reversal was significantly higher than it was during acquisition, an effect that occurred in a cluster, including both dorsomedial PFC and lateral PFC (i.e. superior frontal gyrus), areas known to be involved in contextual processing ( Maren et al., 2013 ; Figure 5B , Supplementary file 1e ).⟦>zach claim=4dbc065d-daa5-45e9-96d6-9012b33cb24c: @{As hypothesized, we found that context specificity during reversal was significantly higher than it was during acquisition, an effect that occurred in a cluster, including both dorsomedial PFC and lateral PFC (i.e. superior frontal gyrus), areas known to be involved in contextual processing ( Maren et al., 2013 ; Figure 5B , Supplementary file 1e ).} context-specificity-increases-reversal⟧

Context specificity did not differ between the other experimental phases.

Previous research has suggested that higher context specificity during extinction learning predicts a more pronounced reoccurrence of fear memories ( LaBar and Phelps, 2005 ; Milad et al., 2005 ; Vansteenwegen et al., 2005 ; Neumann, 2006 ; Navarro-Sánchez et al., 2024 ).

To investigate this hypothesis, we compared the neural representations of cues between experimental phases and correlated the magnitude of reinstatement effects with the increase in context specificity from acquisition to reversal (across participants).

We extracted subject-wise measures of context specificity from the PFC cluster in Figure 4B and compared them to both item reinstatement and generalized reinstatement.⟦>zach claim=no-assertion: @{We extracted subject-wise measures of context specificity from the PFC cluster in Figure 4B and compared them to both item reinstatement and generalized reinstatement.} Narration of how the subject-wise context-specificity values were extracted, with no result.⟧

We extracted these reinstatement values from significant clusters resulting from our previous searchlight analyses ( Figures 4A and 5C ).⟦>zach claim=7d932232-9c15-45f3-8296-958d3fe84d2a: @{We extracted these reinstatement values from significant clusters resulting from our previous searchlight analyses ( Figures 4A and 5C ).} rsa-roi-derived-from-searchlight⟧

We focused our analyses on cues that changed their contingencies (i.e. CS-+ and CS+-), which were expected to reveal differential reinstatement of acquisition vs. reversal memory traces.

We used LME models with ‘context specificity’ and ‘cue type’ as predictors and ‘item reinstatement’ or ‘generalized reinstatement’ as the dependent variable ( Figure 5C ).⟦>zach claim=no-assertion: @{We used LME models with ‘context specificity’ and ‘cue type’ as predictors and ‘item reinstatement’ or ‘generalized reinstatement’ as the dependent variable ( Figure 5C ).} Narration of the LME model specification, with no result.⟧

Correction for multiple comparisons was done (FDR) within each item reinstatement/generalized reinstatement pair of each ROI.

We tested whether increased context specificity during reversal predicted the reinstatement of acquisition memory traces during test old (the test phase with the acquisition/reversal contexts).

We found that an interaction between context specificity and cue type predicted generalized reinstatement of acquisition memory traces in both ACC/SFG (t(22)=6.25, p <0.05) and precuneus (t(22)=4.89, p <0.01) ( Figure 5Di ).⟦>zach claim=7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d: @{We found that an interaction between context specificity and cue type predicted generalized reinstatement of acquisition memory traces in both ACC/SFG (t(22)=6.25, p <0.05) and precuneus (t(22)=4.89, p <0.01) ( Figure 5Di ).} context-specificity-predicts-acquisition-reinstatement-regional-dissociation⟧

In the precuneus, higher context specificity during reversal predicted more generalized reinstatement of the initially non-threatening cues (CS-+), i.e., a cue type that is safe during both acquisition and test, as compared to initially threatening cues (CS-+).

Reversely, in the ACC/SFG, higher context specificity during reversal predicted more generalized reinstatement of the initially threatening cues (CS+-) than of the initially safe cues (CS-+).

In addition, higher context specificity during reversal predicted higher item reinstatement of reversal memory traces for CS-+ than CS+- cues in the dmPFC (t(22)=5.56, p <0.05).⟦>zach claim=711a9296-c951-4455-b0bb-99e3d48ab36e: @{In addition, higher context specificity during reversal predicted higher item reinstatement of reversal memory traces for CS-+ than CS+- cues in the dmPFC (t(22)=5.56, p <0.05).} context-specificity-predicts-reversal-reinstatement-dmpfc⟧

Thus, similar to reinstatement in ACC/SFG, higher context specificity again favored reinstatement of memory traces of threatening over safe cues, even though these memory traces were now from the reversal rather than the acquisition phase ( Figure 5Dii ).

As a control, we also analyzed reinstatement during the test new phase.

We tested whether increased context specificity during reversal predicted the reinstatement of acquisition memory traces during this phase with new contexts.

We found that an interaction between context specificity and CS type predicted the reinstatement of acquisition memory traces in MTG (t(22)=2.51, p <0.05) ( Figure 5Diii ).⟦>zach claim=d0bcf69c-c791-4b94-9d82-92a43bccc4ed: @{We found that an interaction between context specificity and CS type predicted the reinstatement of acquisition memory traces in MTG (t(22)=2.51, p <0.05) ( Figure 5Diii ).} context-specificity-predicts-reinstatement-new-context-mtg⟧

Specifically, higher reversal context specificity predicted more item reinstatement of CS-+ cues, i.e., cues that were safe during acquisition, than of the initially threatening CS+- cues.

Together, these results indicate more specific context representations during reversal than acquisition ( Figure 5B ) and show that acquisition memory traces are predominantly reinstatement in a generalized format, while reversal memory traces are reinstated at the level of individual items ( Figure 4B ).⟦>zach claim=4dbc065d-daa5-45e9-96d6-9012b33cb24c: @{Together, these results indicate more specific context representations during reversal than acquisition ( Figure 5B ) and show that acquisition memory traces are predominantly reinstatement in a generalized format, while reversal memory traces are reinstated at the level of individual items ( Figure 4B ).} context-specificity-increases-reversal⟧

They suggest a possible mechanism for the previously observed impact of extinction contexts on fear renewal, because higher levels of context specificity during reversal favored the reinstatement of threat memory traces in areas of the fear network (ACC and dmPFC; Figure 5Di left and Figure 5Dii ).

These effects were not observed in the precuneus ( Figure 5Di right) and for reinstatement during new contexts ( Figure 5Diii ).


## discussion

Discussion The present study investigated the dynamic changes in neural representations of cues and contexts during acquisition, reversal, test in new contexts (test new ), and test in previous acquisition/reversal contexts (test old ).

Our main findings demonstrate distinct representational properties of CS cues and contexts during these different phases, suggesting that representational geometries reflect the fate of memory traces.

We found that (1) cue generalization and item stability play complementary roles during initial fear learning and reversal, by being associated with threatening-vs-safe cues and changing-vs-consistent cues, respectively; (2) during test new and test old , differences of cue generalization between CS types disappear, while some differences of item stability remain; (3) context representations become more specific following contingency changes during reversal learning, and (4) the context specificity during reversal predicts the reinstatement of fear memories during subsequent tests, providing a mechanistic basis for clinically relevant phenomena, such as renewal.

These results offer new insights into the regional distributions, representational geometries, and functional relevance of cues and contexts across distinct stages of fear learning, opening new avenues of understanding fear-guided behavior.

Complementary representational properties during initial fear learning Our results demonstrate how different representational properties of CS cues are associated with distinct aspects of fear learning: cue generalization with the threatening vs. safe nature of the CS, and item stability with the changing vs. consistent nature of the CS.

Consistent with previous studies ( Visser et al., 2011 ; Visser et al., 2013 ), we found that cue generalization was greater for CS + than for CS- cues during fear acquisition in regions of the fear network (e.g. ACC) and salience network.

This suggests that fear acquisition leads to the formation of a higher-order association between different reinforced cues, but less so between unreinforced ones.

This category-level learning could allow for efficient threat detection and generalization — an adaptive behavior in potentially dangerous environments.

Moreover, previous studies showed that the role of cue generalization in the coding of threat extends beyond fear conditioning, as shown by Dunsmoor et al., 2015 who found enhanced memory consolidation of items sharing conceptual similarity with threat-associated stimuli.

In stark contrast, item stability of CS cues, i.e., their within-stimulus similarity across repetitions, did not differ between CS + and CS- cues during fear acquisition.

This indicates that while acquisition induces a category-level representation for reinforced cues, it does not differentially modify the item-level representations of CS + compared to CS- cues.

Contrastingly, item stability was particularly sensitive to changes in CS valence between experimental phases, suggesting that it plays a crucial role in tracking and updating the specific threat associations of individual stimuli.

Indeed, in fear reversal, cue generalization remained greater for reinforced compared to unreinforced cues (CS--), mirroring the pattern observed during acquisition.

However, item stability specifically increased for cues that changed valence between acquisition and reversal (CS-+ and CS+-).

This finding suggests that when the contingencies change, the participants might focus more on the individual properties of cues to interpret the new contingencies, leading them to fine-tune their representations.

Indeed, item stability has been linked to successful memory encoding and retrieval in several studies ( Xue et al., 2010 ; Zheng et al., 2018 ).

Neural correlates of item stability have been reported in regions of the episodic memory network, such as the IFG and precuneus ( Xue et al., 2010 ), where we found a significant effect of item stability during reversal.

Therefore, item stability might be more akin to an episodic-like type of learning, while cue generalization might be more reflective of category-level learning ( Visser et al., 2013 ).

Furthermore, our use of a trace conditioning paradigm, which is known to engage the hippocampus more than delay conditioning does, may have facilitated the detection of item-specific, episodic-like memory traces and their interaction with context.

This strengthens the relevance of our findings for understanding the interplay between aversive learning and the mechanisms of episodic memory.

Previous findings by Visser et al., 2011 ; Visser et al., 2013 demonstrate distinct learning curves for item stability between CS + and CS- cues from trial to trial.

This discrepancy could be caused by methodological differences, as our study focused on session-wise differences of item stability for each cue type and not on trial-by-trial differences.

In line with our conclusions, however, Visser et al., 2013 found that item stability was increased for subsequently remembered cues, while cue generalization was associated with the later behavioral expression of fear memory.

Overall, the increased item stability during reversal of the items that change contingency could reflect a process of stabilizing the new valence at the item level.

This is because the change of contingency may lead to the temporary representation of individual items as ‘categories’ themselves, without being formed yet into generalized representations encompassing multiple different items sharing the same valence.

This dual representational signature may allow for both efficient threat detection (via category representations) and flexible updating of individual stimulus associations (via item-specific representations).

Dissolution of cue generalization and item stability in the absence of US During the test phases, we did not observe any differences in cue generalization between cue types.

However, some differences in item stability remained during test new (higher for CS+- vs. CS ++in the MTG) and test old (higher for CS ++ vs. CS-- in the inferior temporal cortex) ( Figure 3C–D ).⟦>zach claim=500caa5d-b636-4776-98fe-422b618f8e02: @{However, some differences in item stability remained during test new (higher for CS+- vs. CS ++in the MTG) and test old (higher for CS ++ vs. CS-- in the inferior temporal cortex) ( Figure 3C–D ).} item-stability-persists-test-phases⟧

These findings suggest that the disappearance of threat during the test phases may involve two concurrent processes: (1) An unlearning of generalized threat representations, evidenced by the absence of cue generalization differences during the test phases; and (2) a partial unlearning of item-level representations, particularly for cues with changing contingencies, reflected in diminished item stability.

Interestingly, these effects occurred during the test phases rather than during reversal, suggesting that they are driven by the absence of the US rather than by the contingency change.

During the reversal, the continued presence of the US, albeit with a different contingency, may still benefit from generalized representations at the item and category levels.

Contrastingly, the complete absence of the US during the test phases may promote a differentiation of CS representations, as the need for generalization diminishes.

This finding highlights the importance of the specific reinforcement history of cues on the dynamics of fear representations.

Reinstatement of item representations during the test is weaker for fear extinction Our results showed a differentiation of fear memories during the test phases, both at the item and category level.

Interestingly, representations from the first test phase were less reinstated during the second test phase (despite the fact that both test phases occurred during the second experimental day), compared with acquisition and reversal traces formed on the first experimental day ( Figure 4E ).⟦>zach claim=gap: @{Interestingly, representations from the first test phase were less reinstated during the second test phase (despite the fact that both test phases occurred during the second experimental day), compared with acquisition and reversal traces formed on the first experimental day ( Figure 4E ).}⟧

This may be explained by the greater differentiation of cue representations during test new ; the more differentiated the representations, the less likely they are to be subsequently reinstated.

The weaker reinstatement of memories from a phase without any US, compared to memories from acquisition and reversal phases with US, may contribute to the challenges of preventing relapse in anxiety disorders ( Vervliet et al., 2013 ).

If extinction learning results in less stable and less generalizable safety representations, individuals may remain vulnerable to the return of fear once they return to previous contexts ( Boschen et al., 2009 ).

Increased specificity of context representations following contingency changes Our analysis of context representations revealed an increased specificity of context encoding during reversal compared to initial acquisition.

This suggests that the brain may allocate more resources to the representation of contextual details when contingencies are changing, by potentially facilitating the adaptive updating of contingencies against a more stable contextual backdrop.

The dorsomedial PFC, including the superior frontal gyrus and ACC, have emerged from our analyses as key regions exhibiting higher context specificity in reversal learning.

Given their roles in attentional control ( Dosenbach et al., 2007 ) and conflict monitoring ( Stevens et al., 2011 ), the dmPFC’s involvement may reflect increased attentional and control demands induced by changing contingencies.

Computationally, the more precise contextual encoding in these regions during reversal could serve to disambiguate cues of changing contingencies, supporting the formation of new context-dependent associations ( Xu and Südhof, 2013 ).

Our findings extend prior work on the importance of the hippocampus and mPFC in representing context during fear learning and extinction ( Maren et al., 2013 ), as these regions could dynamically adjust their representational specificity in response to a change in environmental demands.

Context specificity is associated with reinstatement of fear memory traces The amount of reinstatement during the test old was related to the increase in context specificity from acquisition to reversal.

We quantified this increase in specificity in the dmPFC cluster identified in the previous analysis and correlated it with two measures of reinstatement: (1) item reinstatement, reflecting the similarity of individual cue representations between phases; and (2) generalized reinstatement, capturing the similarity of cue representations among their CS categories.

For regions involved in threat processing, such as the ACC/SFG, higher context specificity predicted stronger generalized reinstatement of representations of previously threatening cues (CS+-) from acquisition to test.

This suggests that for these cues, the more distinct the contextual encoding during reversal, the more strongly the original fear memory trace resurfaced, likely reflecting a return of fear ( Figure 5D ).⟦>zach claim=gap: @{This suggests that for these cues, the more distinct the contextual encoding during reversal, the more strongly the original fear memory trace resurfaced, likely reflecting a return of fear ( Figure 5D ).}⟧

Contrastingly, for areas implicated in cue-specific processing that could reflect more episodic-like learning, such as the precuneus ( Cavanna and Trimble, 2006 ), context specificity was associated with enhanced generalized reinstatement for cues with consistent meanings across phases (e.g. CS+- cues from reversal to test).

Regarding item reinstatement, the dmPFC behaved similarly to the ACC/SFG, with stronger item reinstatement of previously threatening cues (CS-+ from reversal to test), while the MTG showed a pattern similar to the precuneus, with stronger item reinstatement for cues with consistent meanings across phases.

These findings highlight the region-, phase-, and cue-specific effects of contexts on the reinstatement of cue representations.

In threat-responsive regions, context specificity may promote the resurgence of generalized threat representations, in line with notions of renewal and spontaneous recovery of fear ( Maren et al., 2013 ).

Conversely, in episodic learning regions, contextual encoding may support the reactivation of representations when meanings are maintained, reflecting memory stability.

Together, these results suggest a critical role of context representations in modulating the balance between generalization and specificity of fear memories over time.

Limitations and future directions While our study provides novel insights into the changes of neural representations across the different stages of fear learning, reversal, and test, several limitations should be noted.

First, our sample size was relatively small, and future studies with larger samples will be needed to replicate and extend our findings.

Second, while we examined the spatial patterns of neural activity using RSA, we did not assess potential changes in the temporal dynamics of these patterns.

Several studies have highlighted the importance of considering temporal information in understanding the neural mechanisms of fear learning ( Visser et al., 2013 ; Sperl et al., 2021 ).

Integrating spatial and temporal pattern analysis in future studies could provide a more comprehensive overview of how fear representations evolve over time.

Moreover, further examining the role of context manipulation, by using more classical approaches where only one context is presented per phase, could extend and generalize our current findings.

Finally, applying our approach to clinical populations could yield important insights into the neural mechanisms underlying the overgeneralization of fear and the impaired contextual regulation of fear responses in psychiatric disorders.

Conclusion Our study reveals the changes in neural representations of conditioned stimuli and contexts across fear learning phases.

Cue generalization and item stability play complementary roles in fear acquisition, reversal, and test, by capturing the formation of threat-related categories and updating the contingency of individual stimulus representations, respectively.

Phases devoid of US cues lead to a differentiation (or dissolution) of both category- and item-level representations.

Context specificity in the prefrontal cortex modulates the persistence of fear memories, with region-specific reinstatement effects.

These findings provide insights into the representational dynamics underlying fear learning and extinction, demonstrating the interplay between cue- and context-based representations in shaping the formation, updating, and reinstatement of fear memories.

Understanding these mechanisms might help optimize interventions targeting pathological fear in anxiety disorders.

Future research should extend these findings to clinical populations and investigate the identified representational properties as biomarkers for assessing the effectiveness of extinction-based therapies.


## captions

=== Figure 1 === Figure 1. Overview of the paradigm and analysis approach.⟦>zach claim=d903f2eb-e683-43c7-8feb-1bc1ee72597b: @{=== Figure 1 === Figure 1. Overview of the paradigm and analysis approach.} trace-conditioning-hippocampus-engaged⟧

(A) Example structure of a trial.

Each trial comprises the presentation of a context video, cue, and unconditioned stimulus (US) expectancy rating.

Electric shocks (US) are administered in reinforced trials during acquisition (following CS++ and CS+- cues) and reversal (following CS++ and CS-+ cues), with reinforcement rates of 50%.

( B ) Paradigm structure with four different experimental phases (rows) and four different cue types (columns).

Each cue type consists of two possible items.

( C ) Conditioned stimulus (CS) items (left) and context videos (right).

Each color indicates a set of four thematically related context videos.

Different sets are used across phases (see Table in B).

( D ) Representational Similarity Matrices (RSMs) for each experimental phase, shown here from the dorsal anterior cingulate cortex (ACC) for illustrative purposes.

Lightning images represent reinforced cue types in the different learning phases.

Representations of threatening cues are more similar to each other (warmer colors), reflecting cue generalization.

( E ) Top: Cue generalization mask for the representational similarity analysis (RSA) matrices estimated within each searchlight.

The mask is superimposed on the RSMs (shown in C ) to compute the average similarity between the different cues of each CS type (different colors).

Average cue generalization values are then compared between CS types.

Bottom: Item stability mask estimated within each searchlight.

The mask is superimposed on the RSMs to compute the average similarity across trials of each cue, separately for each CS type (different colors).

Average item stability values are then compared between CS types.

[panels detected: a, b, c, d, e] === Figure 2 === Figure 2. US expectancy ratings and univariate activation results.⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{[panels detected: a, b, c, d, e] === Figure 2 === Figure 2. US expectancy ratings and univariate activation results.} behavioral-learning-confirms-contingencies⟧

( A ) Unconditioned stimulus (US) expectancy ratings and univariate activity difference between cue types across experimental phases.

Dotted lines separate the four experimental phases.

Participants quickly learned the contingencies of each cue type and their changes across the experimental phases.

( B ) Univariate activation results.

Significant second-level results are shown for different contrasts in the different experimental phases.

Significance was assessed at the cluster level with 10 k permutations (p uncorr <0.001).

[panels detected: a, b] === Figure 3 === Figure 3. Enhanced cue generalization and item stability of threat cues.⟦>zach claim=e645b7b4-05c4-4b37-b75f-3e47c0d585b2: @{[panels detected: a, b] === Figure 3 === Figure 3. Enhanced cue generalization and item stability of threat cues.} cue-generalization-increases-acquisition⟧

( A ) Cue representations during acquisition showing higher cue generalization of conditioned stimulus (CS)+ than CS- cues.

No differences in item stability were found.

( B ) Cue representations during reversal.

( Bi ) Higher cue generalization of CS++ than CS-- cues.

( Bii ) Higher cue generalization of currently threatening than non-threatening cues i.e., (CS-+ and CS++) > (CS+- and CS--).

( Biii ) Higher item stability of cues with changing valence than cues with consistent valence, i.e., (CS-+ and CS+-) > (CS++ and CS--).

( C ) Cue representations during test new showing higher item stability of previously safe cues vs. always threatening cues (CS+-) > (CS++).

( D ) Cue representations during test old showing higher item stability of ‘always threatening’ vs. ‘never threatening’ cues (CS++) > (CS--).

All plots depict t-values from searchlight analyses within family-wise error-corrected clusters (uncorrected p <0.001, corrected p <0.025 for Acquisition, and p <0.0125 for the other phases) with 10 k permutations.⟦>zach claim=dc36ab32-bbed-480d-b05d-f833b100b1c3: @{All plots depict t-values from searchlight analyses within family-wise error-corrected clusters (uncorrected p <0.001, corrected p <0.025 for Acquisition, and p <0.0125 for the other phases) with 10 k permutations.} behavioral-learning-confirms-contingencies⟧

[panels detected: a, b, c, d] === Figure 4 === Figure 4. Different reinstatement patterns are observed for the previous experimental phases during Test old .⟦>zach claim=6ea9d399-1100-4329-8a02-ac61dd04e3d1: @{[panels detected: a, b, c, d] === Figure 4 === Figure 4. Different reinstatement patterns are observed for the previous experimental phases during Test old .} Reversal recruits two parallel strategies: generalize threat cues and specify changing-valence cues.⟧

( A ) Region of interests (ROIs) derived from the previous searchlight analyses (see Figure 3 ), by extracting the significant clusters from the previous statistical analyses.⟦>zach claim=e645b7b4-05c4-4b37-b75f-3e47c0d585b2: @{( A ) Region of interests (ROIs) derived from the previous searchlight analyses (see Figure 3 ), by extracting the significant clusters from the previous statistical analyses.} cue-generalization-increases-acquisition⟧

ROIs are color-coded depending on the experimental phase they are derived from: red for acquisition, orange for reversal, green for test new , blue for test old .

When several ROIs overlapped, only the ROI with the bigger voxel size was included in the analyses.

MTG: Middle Temporal Gyrus.

InfTemp: Inferior Temporal Gyrus.

IFG: Inferior Frontal Gyrus. dmPFC: Dorsomedial Prefrontal Cortex.

ACC: Anterior Cingulate Cortex.

SFG: Superior Frontal Gyrus.

( B ) Reinstatement during test old differed between experimental phases, such that: ( Bi ) in IFG, item reinstatement was higher for memory traces from reversal compared to those from acquisition and test new ; and ( Bii ) in dmPFC, generalized reinstatement was higher for memory traces from acquisition compared to those from test new . *:p<0.05. **p<0.01. n=255 for Bi and n=261 for Bii.⟦>zach claim=7ca6bb4e-6e66-47c1-bf7c-52c64d17d80d: @{( B ) Reinstatement during test old differed between experimental phases, such that: ( Bi ) in IFG, item reinstatement was higher for memory traces from reversal compared to those from acquisition and test new ; and ( Bii ) in dmPFC, generalized reinstatement was higher for memory traces from acquisition compared to those from test new . *:p<0.05. **p<0.01. n=255 for Bi and n=261 for Bii.} context-specificity-predicts-acquisition-reinstatement-regional-dissociation⟧

Errors bars represent standard error.

[panels detected: a, b] === Figure 5 === Figure 5. Context specificity during reversal and its role for reinstatement of fear memory traces.⟦>zach claim=2ff7f5ea-efaf-408e-9ef3-ab46fe395e74: @{[panels detected: a, b] === Figure 5 === Figure 5. Context specificity during reversal and its role for reinstatement of fear memory traces.} pfc-context-specificity-predicts-renewal⟧

( A ) Calculation of context specificity as the difference of within-context similarity and between-context similarity.

( B ) Difference in context specificity between acquisition and reversal.

Positive values indicate higher context specificity in reversal.

( C ) Calculation of item reinstatement and generalized reinstatement (similarities of item representations across different phases; left) and context specificity (difference between acquisition and reversal; right).

An LME model was used to predict these reinstatement measures by the interaction of context specificity and conditioned stimulus (CS) types.

( D ) Higher context specificity during reversal predicted reinstatement during test old , as a function of CS type: ( Di ) Higher reversal context specificity predicted more pronounced generalized reinstatement of CS+- vs. CS-+ acquisition memory traces in anterior cingulate cortex (ACC)/superior frontal gyrus (SFG) (left), and reversely, more pronounced generalized reinstatement of CS-+ vs. CS+- acquisition memory traces in the precuneus (right).

CS+-, which is threatening in acquisition, is shown in red, and CS-+, which is not threatening in acquisition, is shown in green.

( Dii ) Higher reversal context specificity predicted more pronounced item reinstatement of CS-+ than CS+- reversal memory traces in dorsomedial Prefrontal Cortex (dmPFC).

CS-+, which is threatening in acquisition, is shown in red, and CS+-, which is not threatening in acquisition, is shown in green.

( Diii ) Higher reversal context specificity also predicted more pronounced item reinstatement of CS-+ than CS+- memory traces from reversal in MFG during test new .

[panels detected: a, b, c, d]
