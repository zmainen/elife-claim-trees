# Feedback of peripheral saccade targets to early foveal cortex

<!-- kammer-2026-foveal-feedback · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Human vision is characterized by frequent eye movements and constant shifts in visual input, yet our perception of the world remains remarkably stable.

Here, we directly demonstrate image-specific foveal feedback to primary visual cortex in the context of saccadic eye movements.

To this end, we used a gaze-contingent fMRI paradigm, in which peripheral saccade targets disappeared before they could be fixated.

Despite no direct foveal stimulation, we were able to decode peripheral saccade targets from foveal retinotopic areas, demonstrating that image-specific feedback during saccade preparation may underlie this effect.

Decoding was sensitive to shape but not semantic category of natural images, indicating feedback of only low-to-mid-level information.

Cross-decoding to a control condition with foveal stimulus presentation indicates a shared representational format between foveal feedback and direct stimulation.

Moreover, eccentricity-dependent analyses showed a U-shaped decoding curve, confirming that these results are not explained by spillover of peripheral activity or large receptive fields.

Finally, fluctuations in foveal decodability covaried with activity in the intraparietal sulcus, thus providing a candidate region for driving foveal feedback.

These findings suggest that foveal cortex predicts the features of incoming stimuli through feedback from higher cortical areas, which offers a candidate mechanism underlying stable perception.


## results

Results Given the fast time scale of saccade-related processes, it is challenging to investigate foveal feedback using fMRI, which is based mostly on a sluggish hemodynamic response.

To address this challenge and dissociate neural processes elicited by direct visual input from those related to foveal feedback, we designed a gaze-contingent functional MRI study where the saccade target was removed before it could reach the central 2 degrees of visual angle (dva) of the fovea (1 dva radius), from which we decoded.

To maximise statistical power, we implemented the paradigm using a block design ( Figure 1A ).⟦>zach claim=no-assertion: @{To maximise statistical power, we implemented the paradigm using a block design ( Figure 1A ).} Design narration: it says why a block design was chosen and reports no result of its own.⟧

During a block, participants fixated a fixation point until a stimulus appeared in the periphery, cueing them to execute a saccade toward the stimulus.

As soon as their gaze came within 6.5 dva of the saccade target, the stimulus disappeared, ensuring that no part of the stimulus ever appeared in the central 2 dva of the fovea.

On subsequent trials of the block, the same stimulus appeared in the participant’s periphery to cue another saccade, a process which was repeated until the end of a block.

The presentation time of each stimulus depended on the saccade latency (M=240.70 ms).

While the fovea is commonly defined as the central 5 dva of the visual field ( Curcio and Allen, 1990 ; Hendrickson, 2009 ; Hendrickson, 2005 ), we focused here on the central part of the fovea, commonly referred to as the foveola ( Poletti et al., 2017 ; Heckenlively and Arden, 2006 ), within 2 dva (1 dva radius), to avoid any overlap of the stimulus and the area from which we decoded.

This narrow definition also allowed for enough space to execute a saccade without the stimulus breaching this region.

Figure 1C shows that this paradigm was successful in preventing the target from reaching the central 2 dva of the fovea in 99.27% of saccades.⟦>zach claim=fe6f5cc9-f01d-4c96-89fa-9932ae396b77: @{Figure 1C shows that this paradigm was successful in preventing the target from reaching the central 2 dva of the fovea in 99.27% of saccades.} target-excluded-fovea-in-99pct-saccades⟧

All blocks in which the target could have appeared in this region were removed from further analysis (see methods section quantification and statistical analysis).

Figure 1. Experimental setup.⟦>zach claim=fe6f5cc9-f01d-4c96-89fa-9932ae396b77: @{Figure 1. Experimental setup.} target-excluded-fovea-in-99pct-saccades⟧

( A ) Illustration of one block of the experimental and control conditions, respectively.⟦>zach claim=no-assertion: @{( A ) Illustration of one block of the experimental and control conditions, respectively.} A bare panel label telling the reader what the illustration depicts, not a finding.⟧

During each block in the experimental condition, a peripheral saccade target was shown, which participants were instructed to fixate.

The target disappeared before it could be foveated, and once fixation was achieved, a new target appeared, until the block was over (duration: 11 s).

The timing of target appearance and disappearance from the experimental condition was recorded and used in the control condition, where targets appeared at fixation.

( B ) Depiction of the four stimuli used in the experiment, which were matched in either visual shape (horizontal/vertical) or semantic category (animal/instrument).⟦>zach claim=a4af1338-dbef-4dad-ba5d-699735dc08df: @{( B ) Depiction of the four stimuli used in the experiment, which were matched in either visual shape (horizontal/vertical) or semantic category (animal/instrument).} foveal-v1-decodes-peripheral-saccade-target — The claim already specifies the four saccade targets as varying in shape and semantic category, which is exactly the stimulus set this panel depicts.⟧

Each stimulus appeared equally often in both conditions.

( C ) Histogram of the gaze distance from the stimulus right after stimulus disappearance, including all trial from all 28 participants .⟦>zach claim=fe6f5cc9-f01d-4c96-89fa-9932ae396b77: @{( C ) Histogram of the gaze distance from the stimulus right after stimulus disappearance, including all trial from all 28 participants .} target-excluded-fovea-in-99pct-saccades⟧

The blocks in which the stimulus edge may have appeared in the participants’ fovea during at least one saccade were excluded.

To compare the experimental condition to activation elicited by direct foveal input, we included a control condition in which participants were instructed to fixate a point at the center of the screen, with the stimulus appearing directly in the center of the fovea ( Figure 1A , bottom).⟦>zach claim=no-assertion: @{To compare the experimental condition to activation elicited by direct foveal input, we included a control condition in which participants were instructed to fixate a point at the center of the screen, with the stimulus appearing directly in the center of the fovea ( Figure 1A , bottom).} Narration of how the control condition was run; it states no outcome of its own.⟧

To keep visual stimulation frequency comparable, the timing of stimulus appearance and disappearance was recorded for each participant in the experimental condition and replayed in the control condition.

To elucidate the content of the stimulus information fed back to foveal retinotopic areas, we used four different natural stimuli (one stimulus per block) allowing us to disentangle the nature of the representation in the foveal retinotopic cortex ( Figure 1B ).⟦>zach claim=no-assertion: @{To elucidate the content of the stimulus information fed back to foveal retinotopic areas, we used four different natural stimuli (one stimulus per block) allowing us to disentangle the nature of the representation in the foveal retinotopic cortex ( Figure 1B ).} Narration of why four natural stimuli were used, asserting nothing about what was found.⟧

The stimuli were manipulated to match in either shape (horizontal vs. vertical) or semantic category (animals vs. instruments).

Decoding foveal feedback To test for the presence of stimulus-specific activation in foveal regions of early visual cortex, we used cross-validated multivariate decoding ( Hebart and Baker, 2018 ), which reveals information that allows discriminating between different stimuli.

We compared all pairs of stimuli in the experimental and control conditions, respectively (chance level: 50%).

In the experimental condition, we found above-chance decoding in central foveal V1 (t(27) = 8.81, p <0.001, mean = 57.43%) ( Figure 2A ).⟦>zach claim=a4af1338-dbef-4dad-ba5d-699735dc08df: @{In the experimental condition, we found above-chance decoding in central foveal V1 (t(27) = 8.81, p <0.001, mean = 57.43%) ( Figure 2A ).} foveal-v1-decodes-peripheral-saccade-target⟧

This result demonstrates that information about the peripheral saccade targets is present in central foveal regions of V1, despite never appearing in the corresponding part of the fovea.

To compare this finding to direct foveal stimulus presentation, we repeated the same analysis for the control condition, where we also found strong significant decoding (t(27) = 19.92, p <0.001, mean = 84.06%) ( Figure 2A ).⟦>zach claim=6271606c-1989-4bb6-a6da-a14145a46145: @{To compare this finding to direct foveal stimulus presentation, we repeated the same analysis for the control condition, where we also found strong significant decoding (t(27) = 19.92, p <0.001, mean = 84.06%) ( Figure 2A ).} foveal-feedback-below-direct-stimulation⟧

To further examine the nature of the neural representation elicited by foveal feedback, we cross-decoded from experimental to control trials by training a classifier on data from central foveal V1 in the experimental condition and testing it on the control condition.

Decoding was significantly above chance (t(27) = 5.22, p <0.001, mean = 57.2%), indicating a similar representational format between the neural representation elicited by direct presentation of the stimulus in the fovea and that elicited by foveal feedback ( Figure 2A ).⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{Decoding was significantly above chance (t(27) = 5.22, p <0.001, mean = 57.2%), indicating a similar representational format between the neural representation elicited by direct presentation of the stimulus in the fovea and that elicited by foveal feedback ( Figure 2A ).} cross-decoding-experimental-to-control⟧

Figure 2. Foveal feedback can be decoded from V1. ( A ) Average decoding accuracy over all pairwise comparisons for control (t(27) = 19.92, p <0.001, mean = 84.06%) and experimental (t(27) = 8.81, p <0.001, mean = 57.43%) conditions and for cross-decoding from experimental to control condition (t(27) = 5.22, p <0.001, mean = 57.2%).⟦>zach claim=6271606c-1989-4bb6-a6da-a14145a46145: @{Figure 2. Foveal feedback can be decoded from V1. ( A ) Average decoding accuracy over all pairwise comparisons for control (t(27) = 19.92, p <0.001, mean = 84.06%) and experimental (t(27) = 8.81, p <0.001, mean = 57.43%) conditions and for cross-decoding from experimental to control condition (t(27) = 5.22, p <0.001, mean = 57.2%).} foveal-feedback-below-direct-stimulation⟧

( B ) Average decoding accuracies for all early visual areas as a function of eccentricity for both experimental and control conditions.⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{( B ) Average decoding accuracies for all early visual areas as a function of eccentricity for both experimental and control conditions.} cross-decoding-experimental-to-control⟧

Error bars represent standard error of the mean.

Note that the graphs have different scales of decoding accuracy.

The central eccentricities (1–5 dva) were measured using a retinotopic localizer, the outer ones (6–10 dva) were inferred from structural data using Neuropythy ( Benson and Winawer, 2018 ).

This pattern of results may alternatively be explained by spillover from peripheral regions or large receptive fields in the fovea reaching into the periphery (cf Williams et al., 2008 ).

To address this issue, we investigated decoding as a function of eccentricity in early visual regions ( Figure 2B ).⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{To address this issue, we investigated decoding as a function of eccentricity in early visual regions ( Figure 2B ).} cross-decoding-experimental-to-control⟧

Foveal decoding due to peripheral spillover would predict a monotonic relationship between peripheral and foveal decoding in the experimental condition.

Instead, we found a U-shaped relationship, with stronger decoding from peripheral and foveal regions compared to parafoveal regions.

We tested this relationship using a weighted quadratic regression and found significant positive curvature for decoding in all early visual areas (V1: t(27) = 3.98, p =0.008, V2: t(27) = 3.03, p =0.02, V3: t(27) = 2.776, p =0.025, one-sided).⟦>zach claim=5e63c146-b0e8-457b-8fdc-5751afaefb2a: @{We tested this relationship using a weighted quadratic regression and found significant positive curvature for decoding in all early visual areas (V1: t(27) = 3.98, p =0.008, V2: t(27) = 3.03, p =0.02, V3: t(27) = 2.776, p =0.025, one-sided).} u-shaped-eccentricity-rejects-spillover⟧

These results highlight the spatial pattern of foveal feedback, separating decoding due to direct stimulus presentation in the periphery and decoding due to feedback to foveal regions.

As expected, in the control condition, decoding was the highest in the center of gaze and dropped off towards the periphery.

Foveal feedback is sensitive to stimulus shape, not semantic category Our use of natural stimuli allowed us to test the effects of shape and category on decoding accuracy to better understand the nature of the information fed back to foveal areas ( Figure 3A ).⟦>zach claim=5476d15d-5249-43b3-a1db-ec0fa4ede39b: @{Foveal feedback is sensitive to stimulus shape, not semantic category Our use of natural stimuli allowed us to test the effects of shape and category on decoding accuracy to better understand the nature of the information fed back to foveal areas ( Figure 3A ).} Foveal feedback carries low-to-mid-level shape, not semantic category. — The section heading states the shape-sensitive, category-insensitive result that this claim makes.⟧

Decoding was assessed between visually similar yet semantically dissimilar stimuli (across category), between semantically similar yet visually dissimilar stimuli (across shape), and between visually and semantically dissimilar stimuli (across both).

The latter comparison served as a baseline, assessing how good decoding is for maximally different stimuli.

Figure 3. Foveal feedback is sensitive to stimulus shape, not semantic category.⟦>zach claim=5476d15d-5249-43b3-a1db-ec0fa4ede39b: @{Figure 3. Foveal feedback is sensitive to stimulus shape, not semantic category.} Foveal feedback carries low-to-mid-level shape, not semantic category.⟧

( A ) Schematic depiction of comparisons to assess the information content of the neural representations.⟦>zach claim=no-assertion: @{( A ) Schematic depiction of comparisons to assess the information content of the neural representations.} A schematic panel label explaining which comparisons are drawn, not a result.⟧

Comparisons across categories assess similarity of representations in terms of visual stimulus properties, with lower decoding accuracies indicating coding for visual information.

Similarly, comparing across shape assesses categorical information.

Comparing across both serves as a baseline, showing how high decoding accuracy is between maximally different stimuli.

( B ) Decoding accuracies for all comparisons using data from foveal regions of V1 and from the lateral occipital area (LO) (n=28).⟦>zach claim=99ca4e8a-6fac-41f6-b901-5b63c1802a66: @{( B ) Decoding accuracies for all comparisons using data from foveal regions of V1 and from the lateral occipital area (LO) (n=28).} lo-shows-reversed-specificity⟧

Error bars represent the standard error from the mean.

Note that the graphs have different y-axes of decoding accuracy.

Figure 3—figure supplement 1. Decoding stimulus content from all early foveal areas.⟦>zach claim=no-assertion: @{Figure 3—figure supplement 1. Decoding stimulus content from all early foveal areas.} A bare supplementary-figure title with no finding attached.⟧

Decoding accuracies for all comparisons using data from foveal regions of V1, V2, and V3 for all 28 participants.

Error bars represent the standard error from the mean.

These graphs show that the results from V1 outlined in this publication generalize to other regions of the early visual cortex.

A similar pattern of decoding accuracies emerged in both experimental and control conditions: Decoding from foveal V1 across category dropped significantly relative to baseline (experimental condition: t(27) = 2.25, p =0.033, difference = 3.03%; control condition: t(27) = 14.74, p <0.001, difference = 16.64%), while decoding across shape remained high ( Figure 3B ).⟦>zach claim=96991fa1-856f-4b2e-875d-715d254696d0: @{A similar pattern of decoding accuracies emerged in both experimental and control conditions: Decoding from foveal V1 across category dropped significantly relative to baseline (experimental condition: t(27) = 2.25, p =0.033, difference = 3.03%; control condition: t(27) = 14.74, p <0.001, difference = 16.64%), while decoding across shape remained high ( Figure 3B ).} v1-category-decoding-drops-in-feedback⟧

This pattern indicates that the nature of the feedback signal in the experimental condition was related to stimulus shape information and not semantic category.

The fact that the overall pattern of results across conditions looks similar in the experimental and control conditions is in line with the notion that direct stimulus presentation and foveal feedback elicit similar neural representation, as suggested by the cross-decoding results described above ( Figure 2A ).⟦>zach claim=6271606c-1989-4bb6-a6da-a14145a46145: @{The fact that the overall pattern of results across conditions looks similar in the experimental and control conditions is in line with the notion that direct stimulus presentation and foveal feedback elicit similar neural representation, as suggested by the cross-decoding results described above ( Figure 2A ).} foveal-feedback-below-direct-stimulation⟧

To test the degree to which the classifier was able to pick up on category information, we repeated the same analysis in the lateral occipital area (LO), which has been shown to capture higher-level information about object category ( Grill-Spector et al., 2001 ).

In this area, the pattern was reversed: Decoding dropped across shape relative to baseline (experimental condition: t(27) = 3.41, p =0.002, difference = 5.31%; control condition: t(27) = 7.25, p <0.001, difference = 6.7%), while it remained high across category, which suggests that this activation more strongly reflects information about the semantic category than stimulus shape.⟦>zach claim=99ca4e8a-6fac-41f6-b901-5b63c1802a66: @{In this area, the pattern was reversed: Decoding dropped across shape relative to baseline (experimental condition: t(27) = 3.41, p =0.002, difference = 5.31%; control condition: t(27) = 7.25, p <0.001, difference = 6.7%), while it remained high across category, which suggests that this activation more strongly reflects information about the semantic category than stimulus shape.} lo-shows-reversed-specificity⟧

The role of IPS in mediating foveal feedback While the previous analyses revealed the pattern of foveal feedback in early visual regions, they left open which neural regions might be involved in driving or mediating this effect.

To this end, we conducted an exploratory analysis looking at the block-by-block fluctuations in foveal decodability in the experimental condition.

As a measure of decodability, we used the continuous decision value of the classifier, which signifies the distance to the classifier’s hyperplane on a given trial.

Using a parametric modulation analysis, we explored which brain region’s activity increased or decreased as a function of foveal decodability.

To control for the effects of the direct peripheral presentation of the stimulus, we used the block-by-block fluctuations of peripheral decoding in the experimental condition as a baseline.

Since foveal feedback is a process tightly linked to saccadic eye movements ( Kroell and Rolfs, 2022 ), we hypothesized that regions associated with eye movements are most likely involved in driving this effect.

We focused on three regions that have consistently been associated with eye movements and object representations: Frontal eye fields (FEF) ( Paus, 1996 ; Vernet et al., 2014 ), intraparietal sulcus (IPS) ( Andersen et al., 1992 ; Andersen, 1989 ), and lateral occipital area (LO) ( Kawawaki et al., 2006 ; Figure 4A ).⟦>zach claim=no-assertion: @{We focused on three regions that have consistently been associated with eye movements and object representations: Frontal eye fields (FEF) ( Paus, 1996 ; Vernet et al., 2014 ), intraparietal sulcus (IPS) ( Andersen et al., 1992 ; Andersen, 1989 ), and lateral occipital area (LO) ( Kawawaki et al., 2006 ; Figure 4A ).} Narration of ROI selection with supporting citations; the analysis result comes in the sentences that follow.⟧

Not all voxels in these regions were expected to be functionally active.

Therefore, to focus analyses on the most relevant voxels, we selected the 100 voxels in each of these regions that activated most strongly in the experimental condition in general.

The region of interest (ROI) analyses showed that all of these areas were significantly related to both foveal and peripheral decoding in the experimental condition ( Figure 4B ).⟦>zach claim=3190bd67-2477-4174-b65f-7e70b8128535: @{The region of interest (ROI) analyses showed that all of these areas were significantly related to both foveal and peripheral decoding in the experimental condition ( Figure 4B ).} fef-lo-nonsignificant-after-correction⟧

Specifically, IPS showed significantly larger activation related to foveal decoding compared to peripheral decoding (t(27) = 2.53, p =0.026, difference = 4.22), suggesting that IPS may be involved in foveal feedback.⟦>zach claim=49adf84d-f957-4524-a9e4-0caf34bebe13: @{Specifically, IPS showed significantly larger activation related to foveal decoding compared to peripheral decoding (t(27) = 2.53, p =0.026, difference = 4.22), suggesting that IPS may be involved in foveal feedback.} IPS activity tracks foveal decoding, nominating it as source of the feedback signal.⟧

While effects in the other regions went in the expected direction, they remained non-significant after correcting for multiple comparisons (LO: t(27) = 0.67, p =0.767, difference = 0.53; FEF: t(27) = 2.07, p =0.072, difference = 1.98).⟦>zach claim=3190bd67-2477-4174-b65f-7e70b8128535: @{While effects in the other regions went in the expected direction, they remained non-significant after correcting for multiple comparisons (LO: t(27) = 0.67, p =0.767, difference = 0.53; FEF: t(27) = 2.07, p =0.072, difference = 1.98).} fef-lo-nonsignificant-after-correction⟧

We conducted the same analysis in the control condition, which showed a significant decrease in FEF (t(27) = –4.62, p <0.001, difference = 10.36) and IPS (t(27) = –3.61, p =0.004, difference = 11.6) and an increase in LO (t(27) = 5.11, p <0.001, difference = 16.89) in association with foveal decoding compared to peripheral decoding.⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{We conducted the same analysis in the control condition, which showed a significant decrease in FEF (t(27) = –4.62, p <0.001, difference = 10.36) and IPS (t(27) = –3.61, p =0.004, difference = 11.6) and an increase in LO (t(27) = 5.11, p <0.001, difference = 16.89) in association with foveal decoding compared to peripheral decoding.} cross-decoding-experimental-to-control⟧

In contrast, we found no significant association between peripheral decoding and any of the ROIs (FEF: t(27) = 0.49, p =1.0; IPS: t(27) = 1.35, p =0.56; LO: t(27) = 2.43, p =0.07).⟦>zach claim=gap: @{In contrast, we found no significant association between peripheral decoding and any of the ROIs (FEF: t(27) = 0.49, p =1.0; IPS: t(27) = 1.35, p =0.56; LO: t(27) = 2.43, p =0.07).} No claim carries this null: the tree states the IPS foveal effect and the FEF/LO non-significance, but never that peripheral decoding was unrelated to activity in any ROI.⟧

These findings confirm that our main effects were not simply explained by global brain fluctuations or signal-to-noise ratio, since under those conditions, we would have expected a similar relationship between foveal and peripheral decoding as in the experimental condition ( Figure 4—figure supplement 1 ).⟦>zach claim=gap: @{These findings confirm that our main effects were not simply explained by global brain fluctuations or signal-to-noise ratio, since under those conditions, we would have expected a similar relationship between foveal and peripheral decoding as in the experimental condition ( Figure 4—figure supplement 1 ).} The tree has no claim ruling out global brain fluctuations or signal-to-noise as explanations of the parametric modulation effects.⟧

Figure 4. Correlation of foveal decoding with region of interest (ROI) activation.⟦>zach claim=3af0625b-efea-46a1-93d6-60b55f7506e9: @{Figure 4. Correlation of foveal decoding with region of interest (ROI) activation.} ips-foveal-effect-reverses-in-control⟧

( A ) Cortical masks used in the ROI analyses.⟦>zach claim=no-assertion: @{( A ) Cortical masks used in the ROI analyses.} A bare panel label naming the cortical masks shown.⟧

These masks were generated using Neurosynth ( Yarkoni et al., 2011 ) with the keyword ‘eye movements.’ For later analyses, only the 100 most activating voxels were selected in each area.

( B ) Results of the ROI analyses comparing neural activation as a function of foveal and peripheral decoding in three key areas related to eye movements (n=28).⟦>zach claim=3190bd67-2477-4174-b65f-7e70b8128535: @{( B ) Results of the ROI analyses comparing neural activation as a function of foveal and peripheral decoding in three key areas related to eye movements (n=28).} fef-lo-nonsignificant-after-correction⟧

Activation in the intraparietal sulcus (IPS) was significantly higher in association with foveal decoding compared to peripheral decoding (t(27) = 2.53, p =0.026, difference = 4.22).⟦>zach claim=49adf84d-f957-4524-a9e4-0caf34bebe13: @{Activation in the intraparietal sulcus (IPS) was significantly higher in association with foveal decoding compared to peripheral decoding (t(27) = 2.53, p =0.026, difference = 4.22).} IPS activity tracks foveal decoding, nominating it as source of the feedback signal.⟧

Figure 4—figure supplement 1. Parametric modulation analysis in the control condition.⟦>zach claim=no-assertion: @{Figure 4—figure supplement 1. Parametric modulation analysis in the control condition.} A bare supplementary-figure title with no finding attached.⟧

We conducted the same parametric modulation analysis on the control condition (n=28).⟦>zach claim=no-assertion: @{We conducted the same parametric modulation analysis on the control condition (n=28).} Analysis narration stating which analysis was repeated, with no result.⟧

Foveal decoding was associated with significantly decreased activation in frontal eye field (FEF) (t(27) = –4.62, p <0.001, difference = 10.36) and intraparietal sulcus (IPS) (t(27) = –3.61, p =0.004, difference = 11.6), likely because eye movements in the control condition decrease foveal stimulation.⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{Foveal decoding was associated with significantly decreased activation in frontal eye field (FEF) (t(27) = –4.62, p <0.001, difference = 10.36) and intraparietal sulcus (IPS) (t(27) = –3.61, p =0.004, difference = 11.6), likely because eye movements in the control condition decrease foveal stimulation.} cross-decoding-experimental-to-control⟧

We also found increased activation in lateral occipital area (LO) (t(27) = 5.11, p <0.001, difference = 16.89).⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{We also found increased activation in lateral occipital area (LO) (t(27) = 5.11, p <0.001, difference = 16.89).} cross-decoding-experimental-to-control⟧

Peripheral decoding was not associated with significant changes in any of the region of interests (ROIs) (FEF: t(27) = 0.49, p =1.0; IPS: t(27) = 1.35, p =0.56; LO: t(27) = 2.43, p =0.07).⟦>zach claim=gap: @{Peripheral decoding was not associated with significant changes in any of the region of interests (ROIs) (FEF: t(27) = 0.49, p =1.0; IPS: t(27) = 1.35, p =0.56; LO: t(27) = 2.43, p =0.07).} The control-condition null for peripheral decoding across FEF, IPS and LO is reported nowhere in the claim tree.⟧


## captions

=== Figure 1 === Figure 1. Experimental setup.⟦>zach claim=fe6f5cc9-f01d-4c96-89fa-9932ae396b77: @{=== Figure 1 === Figure 1. Experimental setup.} target-excluded-fovea-in-99pct-saccades⟧

( A ) Illustration of one block of the experimental and control conditions, respectively.

During each block in the experimental condition, a peripheral saccade target was shown, which participants were instructed to fixate.

The target disappeared before it could be foveated, and once fixation was achieved, a new target appeared, until the block was over (duration: 11 s).

The timing of target appearance and disappearance from the experimental condition was recorded and used in the control condition, where targets appeared at fixation.

( B ) Depiction of the four stimuli used in the experiment, which were matched in either visual shape (horizontal/vertical) or semantic category (animal/instrument).

Each stimulus appeared equally often in both conditions.

( C ) Histogram of the gaze distance from the stimulus right after stimulus disappearance, including all trial from all 28 participants .

The blocks in which the stimulus edge may have appeared in the participants’ fovea during at least one saccade were excluded.

[panels detected: a, b, c] === Figure 2 === Figure 2. Foveal feedback can be decoded from V1. ( A ) Average decoding accuracy over all pairwise comparisons for control (t(27) = 19.92, p <0.001, mean = 84.06%) and experimental (t(27) = 8.81, p <0.001, mean = 57.43%) conditions and for cross-decoding from experimental to control condition (t(27) = 5.22, p <0.001, mean = 57.2%).⟦>zach claim=6271606c-1989-4bb6-a6da-a14145a46145: @{[panels detected: a, b, c] === Figure 2 === Figure 2. Foveal feedback can be decoded from V1. ( A ) Average decoding accuracy over all pairwise comparisons for control (t(27) = 19.92, p <0.001, mean = 84.06%) and experimental (t(27) = 8.81, p <0.001, mean = 57.43%) conditions and for cross-decoding from experimental to control condition (t(27) = 5.22, p <0.001, mean = 57.2%).} foveal-feedback-below-direct-stimulation⟧

( B ) Average decoding accuracies for all early visual areas as a function of eccentricity for both experimental and control conditions.

Error bars represent standard error of the mean.

Note that the graphs have different scales of decoding accuracy.

The central eccentricities (1–5 dva) were measured using a retinotopic localizer, the outer ones (6–10 dva) were inferred from structural data using Neuropythy ( Benson and Winawer, 2018 ).

[panels detected: a, b] === Figure 3 === Figure 3. Foveal feedback is sensitive to stimulus shape, not semantic category.⟦>zach claim=5476d15d-5249-43b3-a1db-ec0fa4ede39b: @{[panels detected: a, b] === Figure 3 === Figure 3. Foveal feedback is sensitive to stimulus shape, not semantic category.} Foveal feedback carries low-to-mid-level shape, not semantic category.⟧

( A ) Schematic depiction of comparisons to assess the information content of the neural representations.

Comparisons across categories assess similarity of representations in terms of visual stimulus properties, with lower decoding accuracies indicating coding for visual information.

Similarly, comparing across shape assesses categorical information.

Comparing across both serves as a baseline, showing how high decoding accuracy is between maximally different stimuli.

( B ) Decoding accuracies for all comparisons using data from foveal regions of V1 and from the lateral occipital area (LO) (n=28).⟦>zach claim=no-assertion: @{( B ) Decoding accuracies for all comparisons using data from foveal regions of V1 and from the lateral occipital area (LO) (n=28).} A panel label naming the quantity plotted and the sample size, without stating any outcome.⟧

Error bars represent the standard error from the mean.

Note that the graphs have different y-axes of decoding accuracy.

[panels detected: a, b] === Figure 3s1 === Figure 3—figure supplement 1. Decoding stimulus content from all early foveal areas.⟦>zach claim=no-assertion: @{[panels detected: a, b] === Figure 3s1 === Figure 3—figure supplement 1. Decoding stimulus content from all early foveal areas.} A bare supplementary-figure title with no finding attached.⟧

Decoding accuracies for all comparisons using data from foveal regions of V1, V2, and V3 for all 28 participants.

Error bars represent the standard error from the mean.

These graphs show that the results from V1 outlined in this publication generalize to other regions of the early visual cortex. === Figure 4 === Figure 4. Correlation of foveal decoding with region of interest (ROI) activation.⟦>zach claim=3af0625b-efea-46a1-93d6-60b55f7506e9: @{These graphs show that the results from V1 outlined in this publication generalize to other regions of the early visual cortex. === Figure 4 === Figure 4. Correlation of foveal decoding with region of interest (ROI) activation.} ips-foveal-effect-reverses-in-control⟧

( A ) Cortical masks used in the ROI analyses.

These masks were generated using Neurosynth ( Yarkoni et al., 2011 ) with the keyword ‘eye movements.’ For later analyses, only the 100 most activating voxels were selected in each area.

( B ) Results of the ROI analyses comparing neural activation as a function of foveal and peripheral decoding in three key areas related to eye movements (n=28).⟦>zach claim=no-assertion: @{( B ) Results of the ROI analyses comparing neural activation as a function of foveal and peripheral decoding in three key areas related to eye movements (n=28).} A panel label naming which analysis is displayed, without stating its outcome.⟧

Activation in the intraparietal sulcus (IPS) was significantly higher in association with foveal decoding compared to peripheral decoding (t(27) = 2.53, p =0.026, difference = 4.22).⟦>zach claim=49adf84d-f957-4524-a9e4-0caf34bebe13: @{Activation in the intraparietal sulcus (IPS) was significantly higher in association with foveal decoding compared to peripheral decoding (t(27) = 2.53, p =0.026, difference = 4.22).} IPS activity tracks foveal decoding, nominating it as source of the feedback signal.⟧

[panels detected: a, b] === Figure 4s1 === Figure 4—figure supplement 1. Parametric modulation analysis in the control condition.⟦>zach claim=no-assertion: @{[panels detected: a, b] === Figure 4s1 === Figure 4—figure supplement 1. Parametric modulation analysis in the control condition.} A bare supplementary-figure title with no finding attached.⟧

We conducted the same parametric modulation analysis on the control condition (n=28).⟦>zach claim=no-assertion: @{We conducted the same parametric modulation analysis on the control condition (n=28).} Analysis narration stating which analysis was repeated, with no result.⟧

Foveal decoding was associated with significantly decreased activation in frontal eye field (FEF) (t(27) = –4.62, p <0.001, difference = 10.36) and intraparietal sulcus (IPS) (t(27) = –3.61, p =0.004, difference = 11.6), likely because eye movements in the control condition decrease foveal stimulation.⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{Foveal decoding was associated with significantly decreased activation in frontal eye field (FEF) (t(27) = –4.62, p <0.001, difference = 10.36) and intraparietal sulcus (IPS) (t(27) = –3.61, p =0.004, difference = 11.6), likely because eye movements in the control condition decrease foveal stimulation.} cross-decoding-experimental-to-control⟧

We also found increased activation in lateral occipital area (LO) (t(27) = 5.11, p <0.001, difference = 16.89).⟦>zach claim=b5f7aa26-4228-4741-8680-93ebd04474fa: @{We also found increased activation in lateral occipital area (LO) (t(27) = 5.11, p <0.001, difference = 16.89).} cross-decoding-experimental-to-control⟧

Peripheral decoding was not associated with significant changes in any of the region of interests (ROIs) (FEF: t(27) = 0.49, p =1.0; IPS: t(27) = 1.35, p =0.56; LO: t(27) = 2.43, p =0.07).⟦>zach claim=gap: @{Peripheral decoding was not associated with significant changes in any of the region of interests (ROIs) (FEF: t(27) = 0.49, p =1.0; IPS: t(27) = 1.35, p =0.56; LO: t(27) = 2.43, p =0.07).} This caption is one of the only places the control-condition peripheral-decoding null across all three ROIs is reported, and no claim states it.⟧
