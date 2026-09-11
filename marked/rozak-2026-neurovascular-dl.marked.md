# A deep learning pipeline for mapping in situ network-level neurovascular coupling in multi-photon fluorescence microscopy

<!-- rozak-2026-neurovascular-dl · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Functional hyperemia is a well-established hallmark of healthy brain function, whereby local brain blood flow adjusts in response to a change in the activity of the surrounding neurons.

Although functional hyperemia has been extensively studied at the level of both tissue and individual vessels, vascular network-level coordination remains largely unknown.

To bridge this gap, we developed a deep learning-based pipeline that uses two-photon fluorescence microscopy images of cerebral microcirculation to enable automated reconstruction and quantification of the geometric changes across the microvascular network, comprising hundreds of interconnected blood vessels, pre and post-activation of the neighboring neurons.

The pipeline’s utility was demonstrated in the Thy1-ChR2 optogenetic mouse model, where we observed network-wide vessel radius changes to depend on the photostimulation intensity, with both dilations and constrictions occurring across the cortical depth, at an average of 16.1±14.3 μm (mean ± SD) away from the most proximal neuron for dilations; and at 21.9±14.6 μm away for constrictions.

We observed a significant heterogeneity of the vascular radius changes within vessels, with radius adjustment varying by an average of 24 ± 28% of the resting diameter, likely reflecting the heterogeneity of the distribution of contractile cells on the vessel walls.

A graph theory-based network analysis revealed that the assortativity of adjacent blood vessel responses rose by 152 ± 65% at 4.3 mW/mm 2 of blue photostimulation vs . the control, with a 4% median increase in the efficiency of the capillary networks during this level of blue photostimulation in relation to the baseline.

Interrogating individual vessels is thus not sufficient to predict how the blood flow is modulated in the network.

Our pipeline, enables tracking of the microvascular network geometry over time, relating caliber adjustments to vessel wall-associated cells’ state, and mapping network-level flow distribution impairments in experimental models of disease.


## results

Results Application of our computational pipeline resulted in robust segmentation of the vasculature and neurons from 4D in situ 2PFM images and rendering of the microvasculature as a graph.

The vessel-wise and vertex-wise calibers were tracked across stimulation conditions and related to the cortical depth and the distance to the closest YFP-expressing neuron, mapping the network-level vascular responses to ChR2 activation and revealing the coordination of the microvascular responses following neuronal activation.

Segmentation model results and comparisons We compared an ensemble of UNETR models, an ensemble of U-Net models, and an ilastik random forest model on a test dataset of nine images (507x507x250 μm each) from six mice.

Examples of segmentation masks produced by each of the models are shown in Figure 3 and Appendix 1—figure 4 .⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{Examples of segmentation masks produced by each of the models are shown in Figure 3 and Appendix 1—figure 4 .} novas3d-outperforms-ilastik⟧

When evaluating model performance, we paid close attention to the smoothness of the surface of the segmentation masks due to the sensitivity of the centerline extraction algorithms to irregularities in the surface of the masks: smoother vascular segmentation masks resulted in fewer falsely identified vessel branches.

Ilastik tended to over-segment vessels, that is the model returned numerous false positives, having a high recall (0.89±0.19) but low precision (0.37±0.33; Figure 4 , Supplementary file 3, table 3 ).⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{Ilastik tended to over-segment vessels, that is the model returned numerous false positives, having a high recall (0.89±0.19) but low precision (0.37±0.33; Figure 4 , Supplementary file 3, table 3 ).} novas3d-outperforms-ilastik⟧

When comparing the UNETR and U-Net models, we focused on the surface-based mean surface distance and HD95 distance metrics.

Since we observed no significant differences in these metrics between the two models, we selected the UNETR model as our final model because it produced more consistent segmentations on visual inspection and showed significantly better performance than ilastik on HD95 for both vessel and neuron segmentation (p < 0.05).⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{Since we observed no significant differences in these metrics between the two models, we selected the UNETR model as our final model because it produced more consistent segmentations on visual inspection and showed significantly better performance than ilastik on HD95 for both vessel and neuron segmentation (p < 0.05).} unetr-outperforms-ilastik-hd95⟧

Figure 3. Model performance metrics.⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{Figure 3. Model performance metrics.} novas3d-outperforms-ilastik⟧

The Dice, precision, recall, mean surface distance, and HD95 distance for the vascular ( A ) and neuron ( B ) channels.⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{The Dice, precision, recall, mean surface distance, and HD95 distance for the vascular ( A ) and neuron ( B ) channels.} novas3d-outperforms-ilastik — These are the segmentation metrics on which the claim asserts the deep-learning pipeline beats the ilastik baseline for both channels.⟧

Each model was evaluated on the same test dataset composed of nine images (250 x 507 × 507 μm each) from six mice.

A Wilcoxon signed-rank test was used to compare the model’s performance on each performance metric for images from the test dataset. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{A Wilcoxon signed-rank test was used to compare the model’s performance on each performance metric for images from the test dataset. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.} unetr-outperforms-ilastik-hd95⟧

Figure 4. Visual model comparison.⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{Figure 4. Visual model comparison.} novas3d-outperforms-ilastik⟧

( A ) Raw images of the vascular channel with the neuron channel subtracted to facilitate vessel visualization.⟦>zach claim=no-assertion: @{( A ) Raw images of the vascular channel with the neuron channel subtracted to facilitate vessel visualization.} A description of how the displayed raw images were prepared for visualisation, not a result.⟧

The first and last stacks in each row span from the cortical surface to 250 μm below the surface, while the middle stack spans from 250 μm below the surface to 500 μm below the surface.

All images were from the test dataset, which was unseen during model training.

( B ) Ground truth segmentation masks for the vasculature were generated by a rater who utilized ilastik-assisted manual segmentation.⟦>zach claim=no-assertion: @{( B ) Ground truth segmentation masks for the vasculature were generated by a rater who utilized ilastik-assisted manual segmentation.} A statement of how the ground-truth masks were produced - dataset preparation rather than a finding.⟧

( C ) Ilastik predictions generated via a random forest model.⟦>zach claim=no-assertion: @{( C ) Ilastik predictions generated via a random forest model.} A bare panel label naming which model produced the displayed masks.⟧

( D ) Binary segmentation masks generated by an ensemble of 3D UNet models.⟦>zach claim=no-assertion: @{( D ) Binary segmentation masks generated by an ensemble of 3D UNet models.} A bare panel label naming which model produced the displayed masks.⟧

( E ) Binary segmentation masks generated by an ensemble of 3D UNETR models.⟦>zach claim=no-assertion: @{( E ) Binary segmentation masks generated by an ensemble of 3D UNETR models.} A bare panel label naming which model produced the displayed masks.⟧

Vessel extraction improvements via image registration Rigid registration across all time points from the same field of view improved the ability to trace vascular paths from in situ 2PFM data.

Firstly, registration decreased the mean squared error (MSE) between acquisitions from 1306±747–0.008±0.003 Signal Units.

The number of images acquired per field of view ranged from a total of 2–10 depending on how many repeats were able to be acquired.

Registration enabled the computation of the union of segmentation masks from all time points.

This increased the number of vessel segments identified in each field of view from 241±174 based on a single time point to 412±281 vessel segments per field of view (507 x 507 × 250 μm, n=107 fields of view).⟦>zach claim=2d67695f-3ee3-45e9-b4bc-ff547691c4bc: @{This increased the number of vessel segments identified in each field of view from 241±174 based on a single time point to 412±281 vessel segments per field of view (507 x 507 × 250 μm, n=107 fields of view).} registration-doubles-vessel-count⟧

Taking the union of segmentation masks of an image stack across all time points substantially decreased the incidence of gaps in capillaries, likely arising due to ‘transient RBC plugs’.

The pipeline’s ability to reconstruct the cortical vascular network was thus significantly improved by registering data obtained at different time points.

Validation of pipeline sensitivity to geometric changes To evaluate the ability of our computational pipeline to detect vessel caliber changes of various magnitudes, we simulated a range of vascular caliber changes and injected various levels of Gaussian noise.

Across > 100,000 simulations, the fit of the estimated radius following rescaling against the simulated radius had an R 2 value of 0.68. Figure 5B presents a heatmap of the estimated radius post-scaling vs. simulated radius, across different vertices of vessel centerlines, highlighting the ability of our pipeline to estimate vascular radii accurately.⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{Across > 100,000 simulations, the fit of the estimated radius following rescaling against the simulated radius had an R 2 value of 0.68. Figure 5B presents a heatmap of the estimated radius post-scaling vs. simulated radius, across different vertices of vessel centerlines, highlighting the ability of our pipeline to estimate vascular radii accurately.} radius-estimation-r2-0p68 — This is the R-squared of 0.68 against simulated radii across more than 100,000 simulations that the claim states.⟧

The addition of Gaussian noise revealed the robustness of the pipeline: radius estimates remained stable with increasing noise levels, until the addition of noise with a standard deviation of over 200 SU (with the intensity of the images ranging from 0 to 1023 SU).

Figure 5. Estimation of simulated radii changes.⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{Figure 5. Estimation of simulated radii changes.} radius-estimation-r2-0p68⟧

( A ) An image in the plane orthogonal to the local tangent to a capillary with the detected boundary (in blue) and with the estimated radius of 2.28 μm.⟦>zach claim=no-assertion: @{( A ) An image in the plane orthogonal to the local tangent to a capillary with the detected boundary (in blue) and with the estimated radius of 2.28 μm.} An illustrative cross-section showing the method's detected boundary on one example capillary, not a reported result.⟧

On the right, this image was resized (upsampling, via bicubic interpolation, by 1.10 times) to simulate dilation.

( B ) The plot shows correspondence between the estimated radius following scaling and the simulated level of scaling.⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{( B ) The plot shows correspondence between the estimated radius following scaling and the simulated level of scaling.} radius-estimation-r2-0p68 — The claim that the estimator recovers known simulated radii is what this correspondence plot displays.⟧

( C ) An image in the plane orthogonal to the local tangent of a capillary with the detected boundary (in blue) and with the estimated radius of 3.65 μm.⟦>zach claim=no-assertion: @{( C ) An image in the plane orthogonal to the local tangent of a capillary with the detected boundary (in blue) and with the estimated radius of 3.65 μm.} An illustrative cross-section showing the method's detected boundary on one example capillary, not a reported result.⟧

On the right, Gaussian noise with a sigma of 205.36 SU was added to the image.

( D ) The estimated % change in the vessel’s radius after the addition of varying levels of Gaussian noise, demonstrating the robustness of the radius estimated to noise.⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{( D ) The estimated % change in the vessel’s radius after the addition of varying levels of Gaussian noise, demonstrating the robustness of the radius estimated to noise.} radius-estimation-r2-0p68 — The claim's assertion that the estimate stays stable under added Gaussian noise is exactly what this panel shows.⟧

Our boundary detection algorithm successfully estimated the radius of precisely specified fluorescent beads.

The bead images had a signal-to-noise ratio of 6.79±0.16 (about 35% higher than our in vivo images): to match their SNR to that of in vivo vessel data, following deconvolution, we added Gaussian noise with a standard deviation of 85 SU to the images, bringing the SNR down to 5.05±0.15. The data processing pipeline was kept unaltered except for the bead segmentation, performed via image thresholding instead of our deep learning model (trained on vessel data).

The bead boundary was computed following the same algorithm used on vessel data: that is by the average of the minimum intensity gradients computed along 36 radial spokes emanating from the centerline vertex in the orthogonal plane.

To demonstrate an averaging-induced decrease in the uncertainty of the bead radius estimates on a scale that is finer than the nominal resolution of the imaging configuration, we tested four averaging levels in 289 beads.

Three of these averaging levels were lower than that used on the vessels, and one matched that used on the vessels (36 spokes per orthogonal plane and a minimum of 10 orthogonal planes per vessel).

As the amount of averaging increased, the uncertainty on the diameter of the beads decreased, and our estimate of the bead’s diameter converged upon the manufacturer’s Coulter counter-based specifications (7.32±0.27 μm), as tabulated below in Table 1 .⟦>zach claim=gap: @{As the amount of averaging increased, the uncertainty on the diameter of the beads decreased, and our estimate of the bead’s diameter converged upon the manufacturer’s Coulter counter-based specifications (7.32±0.27 μm), as tabulated below in Table 1 .} No claim covers the microsphere phantom validation - that averaging more orthogonal planes and spokes converges the diameter estimate onto the manufacturer's 7.32 um specification; the radius claim rests on simulations only.⟧

Table 1. Bead diameter estimates.⟦>zach claim=no-assertion: @{Table 1. Bead diameter estimates.} A bare table title.⟧

Number of orthogonal planes Number of spokes per plane Mean diameter estimate (μm) 1 3 7.54±0.68 2 4 7.44±0.51 4 12 7.34±0.38 10 36 7.34±0.32 Vascular morphology and heterogeneity within and among vessels Segmentation coupled with graph extraction enabled a detailed characterization of the microvascular network properties.

The morphological properties of extracted networks are listed in Table 2 , with the probability densities of the vessel length, baseline vessel radius, mean vessel segment depth, and vessel branch point depth shown in Appendix 1—figure 5 .⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{The morphological properties of extracted networks are listed in Table 2 , with the probability densities of the vessel length, baseline vessel radius, mean vessel segment depth, and vessel branch point depth shown in Appendix 1—figure 5 .} radius-estimation-r2-0p68⟧

On the extracted graphs, the vascular radius and distance to labeled neurons were sampled every 1–1.73 μm, enabling detailed analysis of the relationship between the vessel radius change and the proximity to the YFP-expressing neurons.

The radius was tracked across different time points, permitting the analysis of the stimulation-induced change in the vascular caliber.

To highlight the ability of the pipeline to detect vessels that significantly change their radius after stimulation, Figure 6A shows the standard deviation of the average radii on each vessel segment during baseline frames for three mice.⟦>zach claim=083ef4c3-9e93-4927-9867-3c785b2c03c0: @{To highlight the ability of the pipeline to detect vessels that significantly change their radius after stimulation, Figure 6A shows the standard deviation of the average radii on each vessel segment during baseline frames for three mice.} baseline-intra-vessel-radius-varies-24pct — The claim about baseline variability in vessel radius accounts for this display of per-segment baseline standard deviations.⟧

There was a large difference in this standard deviation across various blood vessels, showcasing the model’s ability to reveal baseline variations within each subject.

We examined the average change in the vascular radius of each vessel segment after vs. before photostimulation ( Figure 6B ), with even finer spatial patterns detected by analyzing the vertex-wise radius changes ( Figure 6C ).⟦>zach claim=de368a2f-dfdf-4cb5-9c5f-24e3e0cf3aae: @{We examined the average change in the vascular radius of each vessel segment after vs. before photostimulation ( Figure 6B ), with even finer spatial patterns detected by analyzing the vertex-wise radius changes ( Figure 6C ).} vessel-radius-heterogeneity-stimulation — The claim that radius adjustments during stimulation vary within vessels accounts for this segment-wise and vertex-wise comparison.⟧

The vascular diameter changes were related to the distance from the vessel’s surface to the closest labeled pyramidal neuron at each vertex of the centerline ( Figure 6D ).⟦>zach claim=c1381a0c-47be-4721-9022-ddec7d45b3fd: @{The vascular diameter changes were related to the distance from the vessel’s surface to the closest labeled pyramidal neuron at each vertex of the centerline ( Figure 6D ).} dilations-nearer-neurons-than-constrictions — The claim relates the direction of the radius change to distance from the nearest labelled pyramidal neuron, which is the relation shown here.⟧

The vertex-wise radii estimation allowed the assessment of the variations in radii changes within individual blood vessels ( Figure 7 ).⟦>zach claim=083ef4c3-9e93-4927-9867-3c785b2c03c0: @{The vertex-wise radii estimation allowed the assessment of the variations in radii changes within individual blood vessels ( Figure 7 ).} baseline-intra-vessel-radius-varies-24pct⟧

Notably, capillary radius varied along the vessel length across the baseline frames by 24±28% of the mean resting radius.

Consequently, point measurements in vessel calibers - that are widely reported in the literature - do not permit accurate estimation of the microvessel volume changes.

Together, the within- and across-vessel radii estimations illustrate the pipeline’s ability to capture spatial variations in the vascular reactivity and relate it to other morphological features (e.g. the distance to the closest labeled neuron).

Table 2. S1FL vascular network morphological properties.⟦>zach claim=no-assertion: @{Table 2. S1FL vascular network morphological properties.} A bare table title.⟧

Metric Mean ±SD N=17 Mice (9 M/8 F) Number of individual vessels per volume 368±239 32 FOVs Vessel density 5705±3705 mm –3 32 FOVs Number of vascular junctions per volume 207±154 32 FOVs Vascular junction density 3215±2385 mm –3 32 FOVs Number of terminal vessels per volume 128±52 32 FOVs Individual vessel length 70.7±61.1 μm 12555 vessel segments Cumulative vessel length density 0.40±0.22 m/mm 3 32 FOVs Baseline vessel radius 2.19±1.66 μm Range: 0.66–15.88 μm 12555 vessel segments Baseline intra-vessel radius standard deviation 0.53±0.47 μm 12555 vessel segments Baseline vascular volume density 0.010±0.007 mm 3 /mm 3 32 FOVs Number of pyramidal neurons per volume 313±202 neuronal somas 32 FOVs Pyramidal neuron density 4872±3145 neuronal somas/mm 3 32 FOVs Figure 6. Vascular graph examples.⟦>zach claim=1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d: @{Metric Mean ±SD N=17 Mice (9 M/8 F) Number of individual vessels per volume 368±239 32 FOVs Vessel density 5705±3705 mm –3 32 FOVs Number of vascular junctions per volume 207±154 32 FOVs Vascular junction density 3215±2385 mm –3 32 FOVs Number of terminal vessels per volume 128±52 32 FOVs Individual vessel length 70.7±61.1 μm 12555 vessel segments Cumulative vessel length density 0.40±0.22 m/mm 3 32 FOVs Baseline vessel radius 2.19±1.66 μm Range: 0.66–15.88 μm 12555 vessel segments Baseline intra-vessel radius standard deviation 0.53±0.47 μm 12555 vessel segments Baseline vascular volume density 0.010±0.007 mm 3 /mm 3 32 FOVs Number of pyramidal neurons per volume 313±202 neuronal somas 32 FOVs Pyramidal neuron density 4872±3145 neuronal somas/mm 3 32 FOVs Figure 6. Vascular graph examples.} scope-pipeline-and-application-paper⟧

( A ) Baseline variability in vessel diameter estimated by the standard deviation of each vessel’s mean radius across baseline time frames.⟦>zach claim=083ef4c3-9e93-4927-9867-3c785b2c03c0: @{( A ) Baseline variability in vessel diameter estimated by the standard deviation of each vessel’s mean radius across baseline time frames.} baseline-intra-vessel-radius-varies-24pct — The claim about baseline variability in vessel radius is the quantity this table panel tabulates.⟧

( B ) Mean change in the vessel radius induced by optogenetic stimulation.⟦>zach claim=de368a2f-dfdf-4cb5-9c5f-24e3e0cf3aae: @{( B ) Mean change in the vessel radius induced by optogenetic stimulation.} vessel-radius-heterogeneity-stimulation — The stimulation-evoked radius changes tabulated here are the ones the claim quantifies.⟧

( C ) Mean change in the vertexwise radius, allowing the visualization of heterogeneity of radius changes within each vessel.⟦>zach claim=de368a2f-dfdf-4cb5-9c5f-24e3e0cf3aae: @{( C ) Mean change in the vertexwise radius, allowing the visualization of heterogeneity of radius changes within each vessel.} vessel-radius-heterogeneity-stimulation — Within-vessel heterogeneity of the radius change is precisely what the claim asserts.⟧

( D ) Distance from each vertex to the closest pyramidal neuron.⟦>zach claim=c1381a0c-47be-4721-9022-ddec7d45b3fd: @{( D ) Distance from each vertex to the closest pyramidal neuron.} dilations-nearer-neurons-than-constrictions — The claim states the vertex-to-nearest-neuron distances for dilating and constricting vessels that this panel tabulates.⟧

Each row corresponds to the vascular graph of a different mouse.

Figure 7. Vertex-wise radii along vessel lengths of a sample artery, capillary, and venule at baseline vs. post-stimulation.⟦>zach claim=083ef4c3-9e93-4927-9867-3c785b2c03c0: @{Figure 7. Vertex-wise radii along vessel lengths of a sample artery, capillary, and venule at baseline vs. post-stimulation.} baseline-intra-vessel-radius-varies-24pct⟧

( A ) MIP of an artery, vein, and capillary segments before (left) and after (right) optogenetic stimulation with 458 nm light at 1.1 mW/mm 2 .⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{( A ) MIP of an artery, vein, and capillary segments before (left) and after (right) optogenetic stimulation with 458 nm light at 1.1 mW/mm 2 .} artery-dilates-venule-unchanged-at-low-power⟧

The artery and capillary dilated by 1.33±0.86 μm and 0.42±0.39 μm, respectively (for both p<1e-4, Mann-Whitney U test), whereas there was no significant change in the venular caliber upon photostimulation (p=0.22, Mann-Whitney U test).⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{The artery and capillary dilated by 1.33±0.86 μm and 0.42±0.39 μm, respectively (for both p<1e-4, Mann-Whitney U test), whereas there was no significant change in the venular caliber upon photostimulation (p=0.22, Mann-Whitney U test).} artery-dilates-venule-unchanged-at-low-power⟧

( B ) Estimates of the vertex-wise radius obtained along each of the three vessels’ centrelines, before and after stimulation.⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{( B ) Estimates of the vertex-wise radius obtained along each of the three vessels’ centrelines, before and after stimulation.} artery-dilates-venule-unchanged-at-low-power — The claim reports the radius responses of the sample artery, capillary and venule whose before-and-after centreline profiles this panel shows.⟧

( C ) Vertex-wise radii changes in response to optogenetic stimulation.⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{( C ) Vertex-wise radii changes in response to optogenetic stimulation.} artery-dilates-venule-unchanged-at-low-power — These vertex-wise changes for the three sample vessels are the responses the claim quantifies.⟧

( D ).⟦>zach claim=no-assertion: @{( D ).} A bare panel label with no text.⟧

The vertex-wise distance from the vascular surface to the closest YFP-expressing neuron.

Vascular reactivity to optogenetic stimulation The ability of the pipeline to reveal novel spatial relationships between the vascular network reactivity and labeled neurons was demonstrated by examining the relationship between photostimulation-induced microvascular radii responses and (1) the closest YFP-labeled pyramidal neurons within 80 μm, and (2) the cortical depth, at the vertex-wise level and across different photostimulations ( Figure 8 ).⟦>zach claim=a68ebd2f-95bf-43a9-b0e0-f9ce7a3fa5bd: @{Vascular reactivity to optogenetic stimulation The ability of the pipeline to reveal novel spatial relationships between the vascular network reactivity and labeled neurons was demonstrated by examining the relationship between photostimulation-induced microvascular radii responses and (1) the closest YFP-labeled pyramidal neurons within 80 μm, and (2) the cortical depth, at the vertex-wise level and across different photostimulations ( Figure 8 ).} blue-light-dilations-exceed-green-control⟧

Vessels were coarsely segregated into small (average radius <5 μm) and large (average radius >5 μm) vessels, as we expected them to respond differently due to their differential wall-associated cell composition ( Hartmann et al., 2021 ; Bisht et al., 2021 ; Wu et al., 2022 ; Kirabali et al., 2019 ; Ren et al., 2021 ; Steinman et al., 2017 ; Berthiaume et al., 2018 ; Katz et al., 2023 ; Drouin-Ouellet et al., 2015 ).

Only vessels longer than 20 μm (i.e. vessels whose radius was computed by averaging over many cross-sectional planes) that significantly responded following optogenetic stimulation were analyzed: a vessel was deemed a responder if its radius changed by more than twice the baseline standard deviation in the vessel’s radius.

The morphometric properties of the responders, under different stimulation conditions, are listed in Table 3 .⟦>zach claim=no-assertion: @{The morphometric properties of the responders, under different stimulation conditions, are listed in Table 3 .} A pure cross-reference to Table 3.⟧

The average magnitude of significant microvascular radius changes across all stimulation conditions was 1.04±1.11 μm (62 ± 47%).

The variability in the radius change within the vessel was higher in the dilating vessels, 0.77±0.61 μm (66 ± 72%) than in the constricting vessels, 0.69±0.49 μm (46 ± 18%), for 458 nm, 4.3 m W m m 2 \begin{document}$4.3\frac{mW}{mm^{2}}$\end{document} photostimulation (p<1e-4; with no statistically significant changes detected for either 458 nm, 1.1 m W m m 2 \begin{document}$1.1\frac{mW}{mm^{2}}$\end{document} photostimulation or 552 nm, 4.3 m W m m 2 \begin{document}$4.3\frac{mW}{mm^{2}}$\end{document} photostimulation).⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{The variability in the radius change within the vessel was higher in the dilating vessels, 0.77±0.61 μm (66 ± 72%) than in the constricting vessels, 0.69±0.49 μm (46 ± 18%), for 458 nm, 4.3 m W m m 2 \begin{document}}$4.3\frac{mW}}{mm^{2}}}}$\end{document}} photostimulation (p<1e-4; with no statistically significant changes detected for either 458 nm, 1.1 m W m m 2 \begin{document}}$1.1\frac{mW}}{mm^{2}}}}$\end{document}} photostimulation or 552 nm, 4.3 m W m m 2 \begin{document}}$4.3\frac{mW}}{mm^{2}}}}$\end{document}} photostimulation).} artery-dilates-venule-unchanged-at-low-power⟧

Excluding vessels that did not change their radius by over twice the baseline standard deviation removed almost all large vessels from this analysis.

(Notwithstanding, Appendix 1—figure 5 depicts unfiltered large vessel constrictions and dilations).⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{(Notwithstanding, Appendix 1—figure 5 depicts unfiltered large vessel constrictions and dilations).} radius-estimation-r2-0p68⟧

We ran mixed effects models (at the vessel level) separately on constricting and dilating vessels to investigate the effect of optogenetic stimulation power on the vessel radius changes.

Each of the models was run separately on small and large vessels.

Table 3. Details of responder (Δ R >2 * σR baseline ) vessels.⟦>zach claim=no-assertion: @{Table 3. Details of responder (Δ R >2 * σR baseline ) vessels.} A bare table title, which restates the responder threshold rather than reporting a result.⟧

Stimulation condition Total number of vessel estimates Average minimum distance to the closest neuron (μm) Number of dilators Minimum distance from dilators to the closest neuron (μm) Average vessel depth of dilators (μm) Diameter change (μm) Number of constrictors Minimum distance from constrictors to the closest neuron (μm) Average vessel depth of constrictors (μm) Diameter change (μm) All vessels Dilators Constrictors Capillaries 552 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 5036 21.2±16.2 144 (2.9%) 25.5±19.0 186±114 0.58±0.92 49 (1.0%) 26.5±19.5 247±122 –0.37±0.30 458 nm 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 10136 18.7±14.5 317 (3.1%) 16.8±13.5 196±138 0.90±0.93 255 (2.5%) 22.7±16.3 254±126 –1.39±1.51 458 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 12537 20.6±15.4 575 (4.6%) 16.1±14.3 237±146 0.90±0.77 874 (7.0%) 21.9±14.6 274±103 –1.19±1.13 Large vessels 552 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 225 43.1±19.5 1 (0.4%) 75.4 82 13.98 0 (0%) NA NA NA 458 nm 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 545 38.4±19.5 1 (0.2%) 26.1 402 1.97 1 (0.2%) 19.0 179 –3.65 458 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 569 38.4±20.1 2 (0.35%) 53.1±6.3 84±34 2.47±2.93 6 (1.1%) 43.1±16.3 290±125 –6.07±2.45 Figure 8. Optogenetic activation-induced changes in vessel-wise microvascular radii.⟦>zach claim=a68ebd2f-95bf-43a9-b0e0-f9ce7a3fa5bd: @{Stimulation condition Total number of vessel estimates Average minimum distance to the closest neuron (μm) Number of dilators Minimum distance from dilators to the closest neuron (μm) Average vessel depth of dilators (μm) Diameter change (μm) Number of constrictors Minimum distance from constrictors to the closest neuron (μm) Average vessel depth of constrictors (μm) Diameter change (μm) All vessels Dilators Constrictors Capillaries 552 nm 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} 5036 21.2±16.2 144 (2.9%) 25.5±19.0 186±114 0.58±0.92 49 (1.0%) 26.5±19.5 247±122 –0.37±0.30 458 nm 1.1 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} 10136 18.7±14.5 317 (3.1%) 16.8±13.5 196±138 0.90±0.93 255 (2.5%) 22.7±16.3 254±126 –1.39±1.51 458 nm 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} 12537 20.6±15.4 575 (4.6%) 16.1±14.3 237±146 0.90±0.77 874 (7.0%) 21.9±14.6 274±103 –1.19±1.13 Large vessels 552 nm 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} 225 43.1±19.5 1 (0.4%) 75.4 82 13.98 0 (0%) NA NA NA 458 nm 1.1 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} 545 38.4±19.5 1 (0.2%) 26.1 402 1.97 1 (0.2%) 19.0 179 –3.65 458 nm 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} 569 38.4±20.1 2 (0.35%) 53.1±6.3 84±34 2.47±2.93 6 (1.1%) 43.1±16.3 290±125 –6.07±2.45 Figure 8. Optogenetic activation-induced changes in vessel-wise microvascular radii.} blue-light-dilations-exceed-green-control⟧

Capillary responses included both dilatations, shown in (A), and constrictions, shown in ( B ), with changes in the magnitude of the capillary response with increased photostimulation power. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{Capillary responses included both dilatations, shown in (A), and constrictions, shown in ( B ), with changes in the magnitude of the capillary response with increased photostimulation power. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.} unetr-outperforms-ilastik-hd95⟧

( C ) Probability density function of constrictions and dilations for the 4.3 mW/mm 2 photostimulation.⟦>zach claim=gap: @{( C ) Probability density function of constrictions and dilations for the 4.3 mW/mm 2 photostimulation.} The control claim compares only dilation magnitudes between blue and green light; the distribution of constriction magnitudes shown alongside them is stated by no claim.⟧

( D ) Changes to capillary radii are displayed in relation to the closest pyramidal neurons.⟦>zach claim=c1381a0c-47be-4721-9022-ddec7d45b3fd: @{( D ) Changes to capillary radii are displayed in relation to the closest pyramidal neurons.} dilations-nearer-neurons-than-constrictions — The claim states how capillary radius changes are distributed relative to the closest pyramidal neurons, which is what this panel displays.⟧

The proportion of vessels constricting increased with the higher intensity of blue light stimulation, and constrictions tended to occur further away from pyramidal neurons than did dilations.

( E ) Mean cortical depth of responding capillaries showed a tendency for dilators to be closer to the surface and for constrictors to be deeper in the tissue.⟦>zach claim=a3ca491f-f3b6-456f-b69c-6f9449183c4a: @{( E ) Mean cortical depth of responding capillaries showed a tendency for dilators to be closer to the surface and for constrictors to be deeper in the tissue.} constrictions-deeper-than-dilations — The claim asserts that constrictors sit deeper and dilators nearer the surface, exactly the tendency this panel reports.⟧

Vessels further away from labeled neurons constrict while those closer to the activated neurons dilate We examined the relationship between vascular radius changes and the distance to the closest labeled pyramidal neuron, as microvascular response is thought to result from neuronal activation-elicited generation of vasoactive molecules that diffuse to the neighboring vessels.

For the control condition (552 nm, 4.3 m W m m 2 \begin{document}$4.3\frac{mW}{mm^{2}}$\end{document} photostimulation), 2.9% of small capillaries dilated while 1.0% of small capillaries constricted; in larger vessels, barely any responded (0.4% dilated).

For this control condition, there was no significant difference in the distance from constrictors or dilators to the closest pyramidal neuron.

For the 458 nm photostimulation, capillary constrictors were on average farther away than were dilators from the labeled pyramidal neuron: dilations occurred 16.8±13.5 μm away from labeled neurons while constrictions occurred 22.7±16.3 μm for 1.1 m W m m 2 \begin{document}$1.1\frac{mW}{mm^{2}}$\end{document} photostimulation (p=1.5e-3) whereas the 4.3 m W m m 2 \begin{document}$4.3\frac{mW}{mm^{2}}$\end{document} photostimulation had dilations occur 16.1±14.3 μm away and 21.9±14.6 μm for constrictors (p<1e-4).⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{For the 458 nm photostimulation, capillary constrictors were on average farther away than were dilators from the labeled pyramidal neuron: dilations occurred 16.8±13.5 μm away from labeled neurons while constrictions occurred 22.7±16.3 μm for 1.1 m W m m 2 \begin{document}}$1.1\frac{mW}}{mm^{2}}}}$\end{document}} photostimulation (p=1.5e-3) whereas the 4.3 m W m m 2 \begin{document}}$4.3\frac{mW}}{mm^{2}}}}$\end{document}} photostimulation had dilations occur 16.1±14.3 μm away and 21.9±14.6 μm for constrictors (p<1e-4).} artery-dilates-venule-unchanged-at-low-power⟧

There was no significant shift between the distance from vessels to neurons for the 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} and 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} stimulations with 458 nm light.

Dilations in capillaries following 458 nm photostimulation were larger than those following the 552 nm control photostimulation: 0.90±0.93 μm dilatations occurred with 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} and 0.90±0.78 μm with 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} at 458 nm; vs. 0.58±0.92 μm with 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} at 552 nm (p<1e-4).⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{Dilations in capillaries following 458 nm photostimulation were larger than those following the 552 nm control photostimulation: 0.90±0.93 μm dilatations occurred with 1.1 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} and 0.90±0.78 μm with 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} at 458 nm; vs. 0.58±0.92 μm with 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} at 552 nm (p<1e-4).} artery-dilates-venule-unchanged-at-low-power⟧

For constrictions, 458 nm photostimulations led to –1.39±1.51 μm radius changes with 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} and –1.20±1.13 μm radius changes with 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} (p=4.4e-3), whereas 552 nm photostimulation induced –0.37±0.30 μm radius changes with 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} of power, which was smaller than the 458 nm induced responses (p=0.02).⟦>zach claim=gap: @{For constrictions, 458 nm photostimulations led to –1.39±1.51 μm radius changes with 1.1 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} and –1.20±1.13 μm radius changes with 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} (p=4.4e-3), whereas 552 nm photostimulation induced –0.37±0.30 μm radius changes with 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} of power, which was smaller than the 458 nm induced responses (p=0.02).} The tree's light-control claim covers dilations only; the constriction magnitudes under 458 nm and their excess over the 552 nm control are reported by no claim.⟧

Vascular radius changes at increasing cortical depths Vascular responses were next segregated by the cortical depth of the vessel (i.e. the average vessel distance from the cortical surface; DeFelipe et al., 2002 ).

Dilators tended to be located closer to the cortical surface across all stimulation conditions.

Constricting vessels were located at an average 58±187 μm deeper than dilators for 458 nm stimulation at 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} (p=0.02), and 37±179 μm deeper for 458 nm photostimulation at 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} (p<1e-4; with no change in the mean depth of either constricting or dilating vessels with changes in the photostimulation power).⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{Constricting vessels were located at an average 58±187 μm deeper than dilators for 458 nm stimulation at 1.1 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} (p=0.02), and 37±179 μm deeper for 458 nm photostimulation at 4.3 m W m m 2 \begin{document}}$\frac{mW}}{mm^{2}}}}$\end{document}} (p<1e-4; with no change in the mean depth of either constricting or dilating vessels with changes in the photostimulation power).} artery-dilates-venule-unchanged-at-low-power⟧

Vascular network coordination following optogenetic stimulation We examined the coordination of changes in the microvascular network as a whole via assortativity of radius changes and network efficiency changes.

The vessel responses were observed to be assortative, that is capillaries mirrored the responses in their neighbors.

The increases in stimulation power were accompanied by increases in the assortativity of capillary responses: increasing stimulation level resulted in heightened coordination between adjacent capillaries ( Figure 9 ).⟦>zach claim=ad12a413-e736-4cb5-908f-e331c3a21478: @{The increases in stimulation power were accompanied by increases in the assortativity of capillary responses: increasing stimulation level resulted in heightened coordination between adjacent capillaries ( Figure 9 ).} capillary-efficiency-increases-4pct⟧

Figure 9. Microvascular network coordination following optogenetic stimulation.⟦>zach claim=ad12a413-e736-4cb5-908f-e331c3a21478: @{Figure 9. Microvascular network coordination following optogenetic stimulation.} capillary-efficiency-increases-4pct⟧

( A ) Graph representation of a vascular network of 425 vascular segments from a single image stack.⟦>zach claim=no-assertion: @{( A ) Graph representation of a vascular network of 425 vascular segments from a single image stack.} An illustrative rendering of one image stack's vascular graph, showing the representation rather than asserting a finding.⟧

Vessel segments are depicted as nodes of the graph; vascular segments that are joined at junctions are connected by edges.

Nodes are colored by the change in the mean vessel-wise radius following photostimulation with 458 nm light at 4.3 mW/mm 2 .

( B ) Assortativity of photostimulation-induced changes in mean capillary radius increased with increasing photostimulation power.⟦>zach claim=e93b7cce-2578-4075-8e9b-cc9910fc5fd4: @{( B ) Assortativity of photostimulation-induced changes in mean capillary radius increased with increasing photostimulation power.} network-assortativity-increases-stimulation⟧

( C ) Photostimulation-induced changes in the efficiency of the capillary network.⟦>zach claim=ad12a413-e736-4cb5-908f-e331c3a21478: @{( C ) Photostimulation-induced changes in the efficiency of the capillary network.} capillary-efficiency-increases-4pct⟧

The capillary network efficiency changed by a median –0.16 PΩ –1 (IQR: –0.39–0.10 PΩ –1 ) in response to green light; –0.14 PΩ –1 (IQR: –0.55–0.27 PΩ –1 ) in response to lower intensity blue light; and 0.22 PΩ –1 (IQR = –0.43;1.47 PΩ –1 ) in response to higher intensity blue light.

There was a significant increase (p=0.03) in the capillary network efficiency post 458 nm light at 4.3 mW/mm 2 , when compared to that following the control green illumination.⟦>zach claim=ad12a413-e736-4cb5-908f-e331c3a21478: @{There was a significant increase (p=0.03) in the capillary network efficiency post 458 nm light at 4.3 mW/mm 2 , when compared to that following the control green illumination.} capillary-efficiency-increases-4pct — The claim that capillary network efficiency rises during stimulation is this significant increase over the green-light control.⟧

The measurements came from 72 paired acquisitions of 32 image stacks acquired in 17 mice (9 M/8 F). * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{The measurements came from 72 paired acquisitions of 32 image stacks acquired in 17 mice (9 M/8 F). * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.} unetr-outperforms-ilastik-hd95⟧

The efficiency increased only at the strongest blue photostimulation, that is only at this level of stimulation did the resistivity along the average of all of the shortest paths between junctions in the vascular network decrease, resulting in attenuated resistance to flow through the network.

The distribution of changes to the efficiency was highly skewed (with a coefficient of skewness of –1.06 for green illumination, 2.92 for lower intensity blue photostimulation, and 4.87 for higher intensity blue photostimulation).

The median increase in the efficiency induced by the higher intensity blue photostimulation, of 4% (IQR: –8% to 38%), was significantly higher than the median –6% (IQR=−9–4%) efficiency change following the control green illumination.


## captions

=== Figure 1 === Figure 1. Photostimulation setup.⟦>zach claim=6fb7137d-c89c-4651-9271-014bd6823995: @{=== Figure 1 === Figure 1. Photostimulation setup.} dl-model-scope-single-pipeline⟧

The excitation and stimulation light pass through a FV30-NDM690 dichroic mirror with two notch filters, at 458 nm and 552 nm, to excite TexasRed, EYFP, and ChR2 within the mouse.

The emitted light passes through the objective, is reflected off the FV30-NDM690 dichroic mirror, and passes through a 650 nm barrier filter before reaching a 570 nm long pass filter (LPF) separating emitted light from EYFP and TexasRed, which respectively pass through 495–540 nm and 575–630 nm barrier filters to be collected via GaAsP detectors. === Figure 2 === Figure 2. Computational analysis pipeline.⟦>zach claim=no-assertion: @{The emitted light passes through the objective, is reflected off the FV30-NDM690 dichroic mirror, and passes through a 650 nm barrier filter before reaching a 570 nm long pass filter (LPF) separating emitted light from EYFP and TexasRed, which respectively pass through 495–540 nm and 575–630 nm barrier filters to be collected via GaAsP detectors. === Figure 2 === Figure 2. Computational analysis pipeline.} A description of the microscope's emission path and filters - instrument setup, not a finding.⟧

( A ) The stacks of 2PFM slices were registered using ANTS rigid registration and aligned to the reference time point.

( B ) Images were upsampled using bicubic interpolation to an isotropic resolution of 0.99 x 0.99 × 0.99 μm.

( C ) An ensemble of UNETR deep learning models with dropout generated segmentation masks at each time point, producing probability maps.

( D ) The mean and standard deviation of the probability of each pixel being vasculature were computed and used to create binary vascular segmentation masks.

( E ) The union over the vascular segmentation masks for all time points was computed, and background pixel clusters within vessel masks were removed.

( F ) The vascular segmentation mask was thinned down to centerlines and rendered as a graph, where edges were vessel segments connecting branch points (nodes).

This skeleton was overlaid on the vasculature channel from which the neuron channel was subtracted.

( G ) The plane orthogonal to the tangent to the vessel’s travel direction was computed every micrometer along the centerline.

( H, I ) 1D signal intensity profiles at each centerline vertex were computed in the orthogonal plane every 10°.

( J ) The boundary for each profile was placed at the minimum of the signal gradient for that signal intensity profile.

( K ) The raw intensity image with the detected boundary points, where outlier boundary points (in green) were defined as points over 2 standard deviations from the mean were excluded.

( L ) Visualization of the changes in vertex-wise radii on a sample vascular network.

[panels detected: a, b, c, d, e, f, g, h, i, j, k, l] === Figure 3 === Figure 3. Model performance metrics.⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{[panels detected: a, b, c, d, e, f, g, h, i, j, k, l] === Figure 3 === Figure 3. Model performance metrics.} novas3d-outperforms-ilastik⟧

The Dice, precision, recall, mean surface distance, and HD95 distance for the vascular ( A ) and neuron ( B ) channels.

Each model was evaluated on the same test dataset composed of nine images (250 x 507 × 507 μm each) from six mice.

A Wilcoxon signed-rank test was used to compare the model’s performance on each performance metric for images from the test dataset. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{A Wilcoxon signed-rank test was used to compare the model’s performance on each performance metric for images from the test dataset. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.} unetr-outperforms-ilastik-hd95⟧

[panels detected: a, b] === Figure 4 === Figure 4. Visual model comparison.⟦>zach claim=73b97665-ce32-4361-81d0-40fb149cea2b: @{[panels detected: a, b] === Figure 4 === Figure 4. Visual model comparison.} novas3d-outperforms-ilastik⟧

( A ) Raw images of the vascular channel with the neuron channel subtracted to facilitate vessel visualization.

The first and last stacks in each row span from the cortical surface to 250 μm below the surface, while the middle stack spans from 250 μm below the surface to 500 μm below the surface.

All images were from the test dataset, which was unseen during model training.

( B ) Ground truth segmentation masks for the vasculature were generated by a rater who utilized ilastik-assisted manual segmentation.

( C ) Ilastik predictions generated via a random forest model.

( D ) Binary segmentation masks generated by an ensemble of 3D UNet models.

( E ) Binary segmentation masks generated by an ensemble of 3D UNETR models.

[panels detected: a, b, c, d, e] === Figure 5 === Figure 5. Estimation of simulated radii changes.⟦>zach claim=9639b9cb-4a39-4046-ba35-db6f8f88dfbb: @{[panels detected: a, b, c, d, e] === Figure 5 === Figure 5. Estimation of simulated radii changes.} radius-estimation-r2-0p68⟧

( A ) An image in the plane orthogonal to the local tangent to a capillary with the detected boundary (in blue) and with the estimated radius of 2.28 μm.

On the right, this image was resized (upsampling, via bicubic interpolation, by 1.10 times) to simulate dilation.

( B ) The plot shows correspondence between the estimated radius following scaling and the simulated level of scaling.

( C ) An image in the plane orthogonal to the local tangent of a capillary with the detected boundary (in blue) and with the estimated radius of 3.65 μm.

On the right, Gaussian noise with a sigma of 205.36 SU was added to the image.

( D ) The estimated % change in the vessel’s radius after the addition of varying levels of Gaussian noise, demonstrating the robustness of the radius estimated to noise.

[panels detected: a, b, c, d] === Figure 6 === Figure 6. Vascular graph examples.⟦>zach claim=de368a2f-dfdf-4cb5-9c5f-24e3e0cf3aae: @{[panels detected: a, b, c, d] === Figure 6 === Figure 6. Vascular graph examples.} vessel-radius-heterogeneity-stimulation⟧

( A ) Baseline variability in vessel diameter estimated by the standard deviation of each vessel’s mean radius across baseline time frames.

( B ) Mean change in the vessel radius induced by optogenetic stimulation.

( C ) Mean change in the vertexwise radius, allowing the visualization of heterogeneity of radius changes within each vessel.

( D ) Distance from each vertex to the closest pyramidal neuron.

Each row corresponds to the vascular graph of a different mouse.

[panels detected: a, b, c, d] === Figure 7 === Figure 7. Vertex-wise radii along vessel lengths of a sample artery, capillary, and venule at baseline vs. post-stimulation.⟦>zach claim=083ef4c3-9e93-4927-9867-3c785b2c03c0: @{[panels detected: a, b, c, d] === Figure 7 === Figure 7. Vertex-wise radii along vessel lengths of a sample artery, capillary, and venule at baseline vs. post-stimulation.} baseline-intra-vessel-radius-varies-24pct⟧

( A ) MIP of an artery, vein, and capillary segments before (left) and after (right) optogenetic stimulation with 458 nm light at 1.1 mW/mm 2 .

The artery and capillary dilated by 1.33±0.86 μm and 0.42±0.39 μm, respectively (for both p<1e-4, Mann-Whitney U test), whereas there was no significant change in the venular caliber upon photostimulation (p=0.22, Mann-Whitney U test).⟦>zach claim=af8bc967-3346-4e25-ac9e-8ad3536313fd: @{The artery and capillary dilated by 1.33±0.86 μm and 0.42±0.39 μm, respectively (for both p<1e-4, Mann-Whitney U test), whereas there was no significant change in the venular caliber upon photostimulation (p=0.22, Mann-Whitney U test).} artery-dilates-venule-unchanged-at-low-power⟧

( B ) Estimates of the vertex-wise radius obtained along each of the three vessels’ centrelines, before and after stimulation.

( C ) Vertex-wise radii changes in response to optogenetic stimulation.

( D ).

The vertex-wise distance from the vascular surface to the closest YFP-expressing neuron.

[panels detected: a, b, c, d] === Figure 8 === Figure 8. Optogenetic activation-induced changes in vessel-wise microvascular radii.⟦>zach claim=a68ebd2f-95bf-43a9-b0e0-f9ce7a3fa5bd: @{[panels detected: a, b, c, d] === Figure 8 === Figure 8. Optogenetic activation-induced changes in vessel-wise microvascular radii.} blue-light-dilations-exceed-green-control⟧

Capillary responses included both dilatations, shown in (A), and constrictions, shown in ( B ), with changes in the magnitude of the capillary response with increased photostimulation power. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{Capillary responses included both dilatations, shown in (A), and constrictions, shown in ( B ), with changes in the magnitude of the capillary response with increased photostimulation power. * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.} unetr-outperforms-ilastik-hd95⟧

( C ) Probability density function of constrictions and dilations for the 4.3 mW/mm 2 photostimulation.

( D ) Changes to capillary radii are displayed in relation to the closest pyramidal neurons.

The proportion of vessels constricting increased with the higher intensity of blue light stimulation, and constrictions tended to occur further away from pyramidal neurons than did dilations.

( E ) Mean cortical depth of responding capillaries showed a tendency for dilators to be closer to the surface and for constrictors to be deeper in the tissue.

[panels detected: a, b, c, d, e] === Figure 9 === Figure 9. Microvascular network coordination following optogenetic stimulation.⟦>zach claim=ad12a413-e736-4cb5-908f-e331c3a21478: @{[panels detected: a, b, c, d, e] === Figure 9 === Figure 9. Microvascular network coordination following optogenetic stimulation.} capillary-efficiency-increases-4pct⟧

( A ) Graph representation of a vascular network of 425 vascular segments from a single image stack.

Vessel segments are depicted as nodes of the graph; vascular segments that are joined at junctions are connected by edges.

Nodes are colored by the change in the mean vessel-wise radius following photostimulation with 458 nm light at 4.3 mW/mm 2 .

( B ) Assortativity of photostimulation-induced changes in mean capillary radius increased with increasing photostimulation power.

( C ) Photostimulation-induced changes in the efficiency of the capillary network.

The capillary network efficiency changed by a median –0.16 PΩ –1 (IQR: –0.39–0.10 PΩ –1 ) in response to green light; –0.14 PΩ –1 (IQR: –0.55–0.27 PΩ –1 ) in response to lower intensity blue light; and 0.22 PΩ –1 (IQR = –0.43;1.47 PΩ –1 ) in response to higher intensity blue light.

There was a significant increase (p=0.03) in the capillary network efficiency post 458 nm light at 4.3 mW/mm 2 , when compared to that following the control green illumination.⟦>zach claim=ad12a413-e736-4cb5-908f-e331c3a21478: @{There was a significant increase (p=0.03) in the capillary network efficiency post 458 nm light at 4.3 mW/mm 2 , when compared to that following the control green illumination.} capillary-efficiency-increases-4pct — The claim that capillary network efficiency rises during stimulation is this significant increase over the green-light control.⟧

The measurements came from 72 paired acquisitions of 32 image stacks acquired in 17 mice (9 M/8 F). * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.⟦>zach claim=db0a9448-8fe8-4336-b220-0a71aa19d870: @{The measurements came from 72 paired acquisitions of 32 image stacks acquired in 17 mice (9 M/8 F). * p<0.05, ** p<0.005, and *** p<0.0005. p-values were not adjusted.} unetr-outperforms-ilastik-hd95⟧

[panels detected: a, b, c]


## tables

Table 1. Bead diameter estimates.⟦>zach claim=no-assertion: @{Table 1. Bead diameter estimates.} A bare table title.⟧

Number of orthogonal planes Number of spokes per plane Mean diameter estimate (μm) 1 3 7.54±0.68 2 4 7.44±0.51 4 12 7.34±0.38 10 36 7.34±0.32 Table 2. S1FL vascular network morphological properties.⟦>zach claim=gap: @{Number of orthogonal planes Number of spokes per plane Mean diameter estimate (μm) 1 3 7.54±0.68 2 4 7.44±0.51 4 12 7.34±0.38 10 36 7.34±0.32 Table 2. S1FL vascular network morphological properties.} These rows are the only place the phantom accuracy figures appear - the bead diameter estimate tightening from 7.54 plus or minus 0.68 um to 7.34 plus or minus 0.32 um as averaging increases - and no claim states them.⟧

Metric Mean ±SD N=17 Mice (9 M/8 F) Number of individual vessels per volume 368±239 32 FOVs Vessel density 5705±3705 mm –3 32 FOVs Number of vascular junctions per volume 207±154 32 FOVs Vascular junction density 3215±2385 mm –3 32 FOVs Number of terminal vessels per volume 128±52 32 FOVs Individual vessel length 70.7±61.1 μm 12555 vessel segments Cumulative vessel length density 0.40±0.22 m/mm 3 32 FOVs Baseline vessel radius 2.19±1.66 μm Range: 0.66–15.88 μm 12555 vessel segments Baseline intra-vessel radius standard deviation 0.53±0.47 μm 12555 vessel segments Baseline vascular volume density 0.010±0.007 mm 3 /mm 3 32 FOVs Number of pyramidal neurons per volume 313±202 neuronal somas 32 FOVs Pyramidal neuron density 4872±3145 neuronal somas/mm 3 32 FOVs Table 3. Details of responder (Δ R >2 * σR baseline ) vessels.⟦>zach claim=1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d: @{Metric Mean ±SD N=17 Mice (9 M/8 F) Number of individual vessels per volume 368±239 32 FOVs Vessel density 5705±3705 mm –3 32 FOVs Number of vascular junctions per volume 207±154 32 FOVs Vascular junction density 3215±2385 mm –3 32 FOVs Number of terminal vessels per volume 128±52 32 FOVs Individual vessel length 70.7±61.1 μm 12555 vessel segments Cumulative vessel length density 0.40±0.22 m/mm 3 32 FOVs Baseline vessel radius 2.19±1.66 μm Range: 0.66–15.88 μm 12555 vessel segments Baseline intra-vessel radius standard deviation 0.53±0.47 μm 12555 vessel segments Baseline vascular volume density 0.010±0.007 mm 3 /mm 3 32 FOVs Number of pyramidal neurons per volume 313±202 neuronal somas 32 FOVs Pyramidal neuron density 4872±3145 neuronal somas/mm 3 32 FOVs Table 3. Details of responder (Δ R >2 * σR baseline ) vessels.} scope-pipeline-and-application-paper⟧

Stimulation condition Total number of vessel estimates Average minimum distance to the closest neuron (μm) Number of dilators Minimum distance from dilators to the closest neuron (μm) Average vessel depth of dilators (μm) Diameter change (μm) Number of constrictors Minimum distance from constrictors to the closest neuron (μm) Average vessel depth of constrictors (μm) Diameter change (μm) All vessels Dilators Constrictors Capillaries 552 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 5036 21.2±16.2 144 (2.9%) 25.5±19.0 186±114 0.58±0.92 49 (1.0%) 26.5±19.5 247±122 –0.37±0.30 458 nm 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 10136 18.7±14.5 317 (3.1%) 16.8±13.5 196±138 0.90±0.93 255 (2.5%) 22.7±16.3 254±126 –1.39±1.51 458 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 12537 20.6±15.4 575 (4.6%) 16.1±14.3 237±146 0.90±0.77 874 (7.0%) 21.9±14.6 274±103 –1.19±1.13 Large vessels 552 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 225 43.1±19.5 1 (0.4%) 75.4 82 13.98 0 (0%) NA NA NA 458 nm 1.1 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 545 38.4±19.5 1 (0.2%) 26.1 402 1.97 1 (0.2%) 19.0 179 –3.65 458 nm 4.3 m W m m 2 \begin{document}$\frac{mW}{mm^{2}}$\end{document} 569 38.4±20.1 2 (0.35%) 53.1±6.3 84±34 2.47±2.93 6 (1.1%) 43.1±16.3 290±125 –6.07±2.45
