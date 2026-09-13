# iGABASnFR2 is an improved genetically encoded protein sensor of GABA

<!-- kolb-2026-igabasnfr2 · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Monitoring GABAergic inhibition in the nervous system has been enabled by the development of an intensiometric molecular sensor that directly detects GABA.

However, the first generation iGABASnFR exhibits low signal-to-noise and suboptimal kinetics, making in vivo experiments challenging.

To improve sensor performance, we targeted several sites in the protein for near-saturation mutagenesis and evaluated the resulting sensor variants in a high-throughput screening system using evoked synaptic release in primary cultured neurons.

This identified a sensor variant, iGABASnFR2, with 4.1-fold improved sensitivity and 30% faster rise time, and binding affinity that remained in a range sensitive to changes in GABA concentration at synapses.

We also identified sensors with an inverted response, decreasing fluorescence intensity upon GABA binding.

We termed the best such negative-going sensor iGABASnFR2n, which can be used to corroborate observations with the positive-going sensor.

These improvements yielded a qualitative enhancement of in vivo performance when compared directly to the original sensor. iGABASnFR2 enabled the first measurements of direction-selective GABA release in the retina.

In vivo imaging in somatosensory cortex revealed that iGABASnFR2 can report volume-transmitted GABA release following whisker stimulation.

Overall, the improved sensitivity and kinetics of iGABASnFR2 make it a more effective tool for imaging GABAergic transmission in intact neural circuits.


## introduction

Introduction Genetically encoded neurotransmitter sensors have significantly advanced neuroscience by enabling direct, real-time monitoring of neurotransmitter dynamics.

These tools have facilitated the study of synaptic transmission, input-output relationships within individual neurons, and large-scale network activity.

Among these, genetically encoded sensors for GABA are particularly desirable due to the inherent challenges of detecting inhibitory signaling.

GABAergic neurotransmission plays a crucial role in shaping neural circuit dynamics and maintaining the balance between excitation and inhibition across the brain.

Disruptions in GABAergic signaling have been implicated in neurological and psychiatric disorders, including epilepsy, schizophrenia, and autism, highlighting the importance of developing sensitive tools to study inhibitory transmission ( Sohal and Rubenstein, 2019 ).

Although there are other techniques to measure GABA levels in the brain, they are limited in their sensitivity and/or spatiotemporal resolution.

Microdialysis allows direct, quantitative measurement of extracellular GABA, even in human patients, but its temporal resolution is restricted to the scale of minutes ( van der Zeyden et al., 2008 ).

Electrophysiological approaches, while offering high sensitivity and temporal precision, do not scale to large neuronal populations and cannot independently distinguish GABAergic signaling from other hyperpolarizing currents ( Macdonald and Olsen, 1994 ).

These limitations underscore the need for improved genetically encoded fluorescent sensors capable of resolving GABA dynamics with greater sensitivity, specificity, and temporal resolution.

We previously developed an i ntensity-based GABA S e n sing F luorescent R eporter, iGABASnFR, that increases fluorescence in the presence of GABA ( Marvin et al., 2019 ), from here on referred to as iGABASnFR1. Like many sensors ( Marvin et al., 2011 ), this design used a periplasmic binding protein from bacteria as the ligand-binding domain, in this case Pf622 from the bacterium Pseudomonas fluorescens .

A circularly permuted superfolder GFP (cpSFGFP) was then inserted at a site that supports fluorescence changes associated with GABA binding, and the protein was given trafficking sequences to localize it to the membrane.

While this sensor enabled optical monitoring of GABAergic activity, its sensitivity and dynamic range remained limited compared to extensively optimized sensors like jGCaMP and iGluSnFR ( Aggarwal et al., 2023 ; Zhang et al., 2023 ).

In neuronal culture, the original iGABASnFR1 exhibited a half-maximal effective concentration (EC 50 ) of ~30 µM and maximal ΔF/F of ~0.6. A binding pocket mutation (F102G) increased the maximal ΔF/F of the sensor but at the cost of an increased EC 50 and poor membrane localization.

As such, the overall performance of iGABASnFR1 was not well-suited for high-resolution, photon-limited imaging applications.

To address these limitations, we used site-directed mutagenesis to engineer two next-generation GABA sensors, iGABASnFR2 and iGABASnFR2n.

These sensors exhibit improved sensitivities and affinities for GABA, with positive- and negative-going fluorescence responses, respectively.

Here, we describe the development and characterization of these enhanced GABA sensors and demonstrate their application in imaging inhibitory neurotransmission.


## results

Results Screening for improved variants The original iGABASnFR1 ( Figure 1a , top) was engineered to increase fluorescence in the presence of GABA and express robustly in mammalian neurons, making it a valuable addition to the suite of biosensors available to study the brain ( Dong et al., 2022 ; Looger and Griesbeck, 2012 ; Marvin et al., 2019 ; Yang et al., 2024 ).⟦>zach claim=gap: @{Results Screening for improved variants The original iGABASnFR1 ( Figure 1a , top) was engineered to increase fluorescence in the presence of GABA and express robustly in mammalian neurons, making it a valuable addition to the suite of biosensors available to study the brain ( Dong et al., 2022 ; Looger and Griesbeck, 2012 ; Marvin et al., 2019 ; Yang et al., 2024 ).} The tree never states what iGABASnFR1 was engineered to do or how it performed, so this baseline characterisation of the predecessor sensor rests on no claim.⟧

However, iGABASnFR1 is a first-generation sensor, with low sensitivity in vivo, particularly in comparison to other sensors, such as jGCaMP and iGluSnFR, which have been subjected to multiple generations of engineering.

Consequently, we applied the same screening pipeline used to optimize jGCaMP ( Dana et al., 2016 ; Wardill et al., 2013 ; Zhang et al., 2023 ) to the task of improving iGABASnFR performance.

This pipeline uses field stimulation to evoke activity of cultured primary neurons expressing different sensor variants.

Stimulation elicits synaptic release, allowing us to screen for improved sensor performance by measuring response amplitude and kinetics ( Figure 1b ), in an experimental setting that approximates in vivo conditions.⟦>zach claim=c0396bdd-9084-4a13-8dd8-f616c5cdecd9: @{Stimulation elicits synaptic release, allowing us to screen for improved sensor performance by measuring response amplitude and kinetics ( Figure 1b ), in an experimental setting that approximates in vivo conditions.} mutagenesis-3947-variants-screened⟧

Figure 1. Field stimulation screen for improved iGABASnFR.⟦>zach claim=f1d695b7-88cd-49d5-9fdc-f66cad65e1c8: @{Figure 1. Field stimulation screen for improved iGABASnFR.} igabasnfr2-fourfold-sensitivity-gain⟧

( a ) Top: Schematic representation of iGABASnFR1 and the amino acid substitutions that gave rise to iGABASnFR2 and iGABASnFR2n.

White, IgG secretion signal (cleaved off during trafficking to cell surface); blue, GABA binding protein Pf622; green, cpSFGFP; dark green, Myc epitope tag; red, PDGFR transmembrane domain.

Numbering is relative to each of the constituent protein domains; the relationship to sequential numbering of the entire polypeptide is shown in Figure 1—figure supplement 1 .⟦>zach claim=no-assertion: @{Numbering is relative to each of the constituent protein domains; the relationship to sequential numbering of the entire polypeptide is shown in Figure 1—figure supplement 1 .} A note on residue-numbering convention pointing to a supplementary sequence figure, asserting nothing about the sensor.⟧

Bottom: Crystal structure of a preliminary version of iGABASnFR (PDB ID 6DGV) with the 39 sites targeted for mutagenesis.

Gray spheres indicate the approximate position of GABA, based on homology to the liganded structure of GABA-binding protein Atu4243 ( Planamente et al., 2012 ).

( b ) Mutagenesis and screening strategy.

Variants with single-site mutations are screened for ΔF/F and expression in an initial field stimulation assay, strong performers identified and then combined and re-screened in a second round.

The top-performing mutants (positive-going quadruple mutant iGABASnFR2 and negative-going triple mutant iGABASnFR2n) are characterized further.

( c ) Joint optimization of sensitivity (ΔF/F, x-axis) and expression, measured with responsive pixels (y-axis). ΔF/F is normalized to in-plate iGABASnFR1 controls.

Black circle: (1,1) position represents iGABASnFR.

Plus signs: mutants from the first round that were put together to form combos in the second round. iGABASnFR2 and 2 n exhibited increased ΔF/F (4.3-fold and –2.2-fold of iGABASnFR, respectively) and greater numbers of responsive pixels (13.1-fold and 10.3-fold).

Illumination: 0.34 mW/mm 2 , imaging framerate: 50 Hz.

( d ) Performance measures of sensor variants from the screen.

Single-site variants are shown in gray, and double-site combinations are shown in black.

Variants are ranked according to the ΔF/F0 values measured for 40 AP, and those rankings are maintained for the lower displays of sensor F0, tau on, the time constant of the rising phase of the response, and tau off for the decay.

All values are normalized to in-plate iGABASnFR1 controls.

Figure 1—figure supplement 1. Annotated amino acid sequence of iGABASnFRs.⟦>zach claim=no-assertion: @{Figure 1—figure supplement 1. Annotated amino acid sequence of iGABASnFRs.} A bare figure title for the annotated sequence supplement, carrying no finding of its own.⟧

( a ) iGABASnFR1 sequence shown in gray text, with sites targeted for mutagenesis in black.

Shading indicates domains according to: IgG secretion signal Pf622 2–276 SFGFP 147–238 Junction SFGFP 1–146 Pf622 277–320 Myc epitope PDGFR transmembrane domain 513–561 ( b ) iGABASnFR2 sequence, with mutations shown in red text.

Mutations are listed according to domain numbers, with sequential numbering through the polypeptide indicated at the left.

Sequential numbering through the polypeptide is indicated on the left, while mutations in the text are listed according to domain numbers: S99 Pf A.F102 Pf Y.F104 Pf Y.L178 gfp S. S99 Pf A.F102 Pf Y.F104 Pf Y.L178 gfp S, which we subsequently refer to as iGABASnFR2, and the best variant with inverted signal, iGABASnFR.S99 Pf A.F104 Pf H.R168 gfp P was chosen to be iGABASnFR2n.

( c ) iGABASnFR2n sequence, with mutations shown in red text.

Sequential numbering through the polypeptide is indicated on the left, while mutations in the text are listed according to domain numbers: S99 Pf A.F104 Pf H.R168 gfp P. ( d ) Schematic showing the relationship between domain-based numbering scheme and sequential numbering through the entire polypeptide (top) and the domain-based numbering scheme.

In both schemes, numbering starts at the residue exposed after signal sequence cleavage.

Sensor variants were derived by near-saturation mutagenesis of selected sites within the protein, and performance was evaluated in a first round of screening.

To select improved variants, we jointly optimized for both the ΔF/F of the sensor and its expression levels.

Screening for expression was necessary because, in our previous effort to engineer iGABASnFR ( Marvin et al., 2019 ), we discovered several mutations, most notably F102G, that increased the maximal ΔF/F but exhibited expression problems in neurons, with low baseline fluorescence and intracellular aggregates.

We quantified the expression levels of different variants by counting the total number of pixels in a well that showed a significant increase in fluorescence during the field stimulation period.

These pixels were classified as responsive pixels.

To guide our site-selection efforts, we used the unliganded crystal structure of a preliminary version of iGABASnFR https://www.rcsb.org/structure/6dgv ; ( Marvin et al., 2019 ), a strategy that worked well for optimizing GCaMP ( Akerboom et al., 2009 ).

Specifically, we identified 39 sites to target: 14 near the GABA binding site, 6 at or around the protein hinge area, 10 on the cpSFGFP, and 9 at the interface between the two ligand-binding and cpGFP domains ( Figure 1a , bottom).⟦>zach claim=c0396bdd-9084-4a13-8dd8-f616c5cdecd9: @{Specifically, we identified 39 sites to target: 14 near the GABA binding site, 6 at or around the protein hinge area, 10 on the cpSFGFP, and 9 at the interface between the two ligand-binding and cpGFP domains ( Figure 1a , bottom).} mutagenesis-3947-variants-screened — The claim that 3,947 variants were generated from 39 targeted sites accounts for this breakdown of where those 39 sites lie.⟧

In the first round of screening, these 39 sites were targeted for mutagenesis, generating 9±5 substitutions at each site (range: 1–19) for a total of 3947 variants.

Sensor variants were arrayed in 96-well plates, with each plate containing four replicate wells of the same variant and eight replicate wells of the original iGABASnFR, which served as part of our quality control measures.

Each well received 1, 10, and 40 field stimulation pulses separated by 12 ms, and we calculated responses by averaging fluorescence changes over all the responsive pixels in each well.

We found 93 mutants with ΔF/F significantly higher than in-plate iGABASnFR1 controls, and 22 of those also had a higher fraction of responsive pixels than iGABASnFR, indicating improved expression ( Figure 1c ).⟦>zach claim=a8787aa1-9028-4ed0-827a-cdb38e9f59cb: @{We found 93 mutants with ΔF/F significantly higher than in-plate iGABASnFR1 controls, and 22 of those also had a higher fraction of responsive pixels than iGABASnFR, indicating improved expression ( Figure 1c ).} igabasnfr2-13fold-expression-increase⟧

Interestingly, at least 20 sequence-confirmed mutations, located in 5 different positions - R168 gfp , D276 Pf , T203 gfp , V150 gfp , and V272 Pf - inverted the response of the sensor, making it decrease in fluorescence with field stimulation (number refers to location in the protein domain denoted by subscript, either cpSFGFP or the ligand binding Pf622).

However, none of the inverted sensors exhibited |ΔF/F| greater than that of iGABASnFR.

Among them, the R168 gfp P mutant was the most promising, with relatively high ΔF/F (0.6x of iGABASnFR) and expression (2x responsive pixels of iGABASnFR; Figure 1c ).⟦>zach claim=a8787aa1-9028-4ed0-827a-cdb38e9f59cb: @{Among them, the R168 gfp P mutant was the most promising, with relatively high ΔF/F (0.6x of iGABASnFR) and expression (2x responsive pixels of iGABASnFR; Figure 1c ).} igabasnfr2-13fold-expression-increase⟧

Although we found many marginally improved variants in the first round of screening, there was no clear winner that could be considered to be a major improvement over iGABASnFR.

The most sensitive positive-going mutant in the screen was the previously known mutation F102 Pf G (ΔF/F 2.5x of iGABASnFR) which was confirmed to have poor expression (0.3x responsive pixels of iGABASnFR).

Similarly, the top-expressing mutant in the screen (L178 gfp Y; 14.8x responsive pixels of iGABASnFR) had only a modest ΔF/F (1.1x of iGABASnFR).

Therefore, in the first round of screening, we succeeded in improving ΔF/F and expression separately but not jointly.

Enhancing performance with combinations of single-site mutants We hypothesized that we could generate variants with both improved sensitivity and expression by combining mutations that conveyed each property separately.

To test this, the mutations S99 Pf →A/G/C, F102 Pf →G/Y, F104 Pf →Y/H, R168 gfp →P, L178 gfp →R/S, and K253 Pf →I/Y (labeled in Figure 1d as plus signs) were chosen based on their performance in the first round and combined to create 635 double mutants, which were then screened in a second round.⟦>zach claim=305140b5-5720-45d7-8706-593e29243fb6: @{To test this, the mutations S99 Pf →A/G/C, F102 Pf →G/Y, F104 Pf →Y/H, R168 gfp →P, L178 gfp →R/S, and K253 Pf →I/Y (labeled in Figure 1d as plus signs) were chosen based on their performance in the first round and combined to create 635 double mutants, which were then screened in a second round.} igabasnfr2n-negative-going-variant⟧

A large percentage of these mutants (49%) did not pass quality control to be considered for further analysis.

The majority of these mutants had poor expression, no detectable response to field stimulation, or both.

Of the remaining mutants, 52 exhibited improved expression and ΔF/F over iGABASnFR.

More importantly, 27 mutants exhibited ΔF/F higher than F102 Pf G and expression better than iGABASnFR, suggesting that our hypothesis was correct and the beneficial properties of the mutants could be additive.

Interestingly, many of the mutations that improved ΔF/F and expression in positive-going sensors did the same in negative-going sensors.

Of these variants, the best combination of dynamic range and expression was the mutant iGABASnFR.S99 Pf A.F102 Pf Y.F104 Pf Y.L178 gfp S (hereafter iGABASnFR2).

The best variant with inverted signal, iGABASnFR.S99 Pf A.F104 Pf H.R168 gfp P was designated iGABASnFR2n (for n egative-going).

When we quantified rise and decay time constants, peak ΔF/F, and signal-to-noise, iGABASnFR2 performance was broadly superior to the original across all field stimulation conditions ( Figure 2 ).⟦>zach claim=f1d695b7-88cd-49d5-9fdc-f66cad65e1c8: @{When we quantified rise and decay time constants, peak ΔF/F, and signal-to-noise, iGABASnFR2 performance was broadly superior to the original across all field stimulation conditions ( Figure 2 ).} igabasnfr2-fourfold-sensitivity-gain⟧

For 10 action potentials (APs), iGABASnFR2 exhibited a peak ΔF/F 4.1-fold greater than iGABASnFR1 (iGABASnFR2 0.77±0.13; iGABASnFR1 0.19±0.02; p <0.001 Tukey’s HSD post hoc test following one-way ANOVA), and a signal-to-noise ratio (SNR) threefold higher (iGABASnFR2 67.6±11.9; iGABASnFR1 22.7±5.5; p <0.001).⟦>zach claim=f1d695b7-88cd-49d5-9fdc-f66cad65e1c8: @{For 10 action potentials (APs), iGABASnFR2 exhibited a peak ΔF/F 4.1-fold greater than iGABASnFR1 (iGABASnFR2 0.77±0.13; iGABASnFR1 0.19±0.02; p <0.001 Tukey’s HSD post hoc test following one-way ANOVA), and a signal-to-noise ratio (SNR) threefold higher (iGABASnFR2 67.6±11.9; iGABASnFR1 22.7±5.5; p <0.001).} igabasnfr2-fourfold-sensitivity-gain — This is the 4.1-fold peak dF/F improvement the claim asserts, reported here with its statistics and the accompanying SNR gain.⟧

Rise time constants were slightly faster (iGABASnFR2 43±9 ms; iGABASnFR1 61±13 ms; p <0.001), while decay times were slower (iGABASnFR2 73±26 ms; iGABASnFR1 62±29 ms; p <0.001).⟦>zach claim=a56b114d-fbe5-422f-91cd-00a7de8b98ee: @{Rise time constants were slightly faster (iGABASnFR2 43±9 ms; iGABASnFR1 61±13 ms; p <0.001), while decay times were slower (iGABASnFR2 73±26 ms; iGABASnFR1 62±29 ms; p <0.001).} igabasnfr2-kinetics-rise-decay — The claim states exactly this pairing of a faster rise and a slower decay for iGABASnFR2 relative to iGABASnFR1.⟧

The negative-going iGABASnFR2n exhibited slightly reduced performance relative to iGABASnFR2 but still achieved a 3.3-fold greater peak ΔF/F (iGABASnFR2n 0.62±0.12; iGABASnFR1 0.19±0.02; p <0.001), and 40% higher SNR compared to iGABASnFR1 (iGABASnFR2n 32.5±7.5; iGABASnFR1 22.7±5.5; p <0.01).⟦>zach claim=gap: @{The negative-going iGABASnFR2n exhibited slightly reduced performance relative to iGABASnFR2 but still achieved a 3.3-fold greater peak ΔF/F (iGABASnFR2n 0.62±0.12; iGABASnFR1 0.19±0.02; p <0.001), and 40% higher SNR compared to iGABASnFR1 (iGABASnFR2n 32.5±7.5; iGABASnFR1 22.7±5.5; p <0.01).} The tree's only claim about iGABASnFR2n covers its screening dF/F and responsive-pixel count, not its evoked-release performance in neurons (3.3-fold peak dF/F, 40% higher SNR).⟧

However, its kinetics were slower, with a rise time of 72±8 ms. These measures clearly indicate that this next generation of GABASnFRs exhibits broadly improved performance in detecting GABA dynamics during synaptic release.

Figure 2. Characterization of iGABASnFR variants in cultured neurons.⟦>zach claim=f1d695b7-88cd-49d5-9fdc-f66cad65e1c8: @{Figure 2. Characterization of iGABASnFR variants in cultured neurons.} igabasnfr2-fourfold-sensitivity-gain⟧

( a ) Fluorescence images of primary neurons expressing iGABASnFR1 (orange), iGABASnFR2 (green), iGABASnFR2n (blue) under the CAG promoter at baseline, at peak brightness after field stimulation with 40 action potentials (APs), and the corresponding ΔF/F0. Scale bar, 20 μm.

( b ) Time courses of the ΔF/F0 response to 1, 10, and 40 APs delivered at 83 Hz. iGABASnFR2n signals are inverted for display.

Traces and error bars denote mean ± s.e.m., n=20 culture wells for each variant.⟦>zach claim=no-assertion: @{Traces and error bars denote mean ± s.e.m., n=20 culture wells for each variant.} A graphical-encoding note on what the traces and error bars represent.⟧

( c ) Rise time constants of the three sensor variants obtained from exponential fits for the 1 AP condition (n=24 culture wells for iGABASnFR1 and iGABASnFR2, n=18 for iGABASnFR2n).⟦>zach claim=gap: @{( c ) Rise time constants of the three sensor variants obtained from exponential fits for the 1 AP condition (n=24 culture wells for iGABASnFR1 and iGABASnFR2, n=18 for iGABASnFR2n).} The kinetics claim covers rise and decay at 10 action potentials; the single-AP rise-time comparison shown in this panel is stated nowhere in the tree.⟧

For panels ( c-f ), red lines indicate the mean and boxes indicate the 95% confidence interval.

( d ) Decay time constants of the three variants for the 1 AP condition.

( e ) Peak ΔF/F0 of the three variants over different levels of stimulation.

( f ) Signal-to-noise (d′) of the three variants over different levels of stimulation.

Structure of the iGABASnFR2-GABA complex To gain some insight into the structure-function relationship of this sensor, we solved the crystal structure of iGABASnFR2 in complex with GABA ( Figure 3 , Figure 3—source data 1 ; PDB ID 9D57).⟦>zach claim=f7d3b257-5ae5-4122-a122-0184b12b15f7: @{Structure of the iGABASnFR2-GABA complex To gain some insight into the structure-function relationship of this sensor, we solved the crystal structure of iGABASnFR2 in complex with GABA ( Figure 3 , Figure 3—source data 1 ; PDB ID 9D57).} crystal-structure-pdb-9d57⟧

To examine the conformational changes that accompany GABA binding, we compared this new liganded structure with the apo form of a precursor of the original iGABASnFR (PDB ID 6DGV).

Superimposing the structures, using cpGFP as a reference, revealed that the two lobes of the Venus flytrap domain in Pf622 shift closer together to secure GABA in the binding pocket ( Figure 3a ).⟦>zach claim=81a3fe0f-a268-4abf-8ad5-b4abbdb4b2dc: @{Superimposing the structures, using cpGFP as a reference, revealed that the two lobes of the Venus flytrap domain in Pf622 shift closer together to secure GABA in the binding pocket ( Figure 3a ).} GABA closes the Pf622 lobes of iGABASnFR2 while leaving cpGFP nearly rigid.⟧

This conformational change resembles those seen in other bacterial periplasmic amino acid-binding proteins ( Quiocho and Ledvina, 1996 ).

Figure 3. Crystal structure of iGABASnFR2 in complex with GABA.⟦>zach claim=f7d3b257-5ae5-4122-a122-0184b12b15f7: @{Figure 3. Crystal structure of iGABASnFR2 in complex with GABA.} crystal-structure-pdb-9d57⟧

( a ) Superposition of the structure of iGABASnFR2 in complex with GABA (green; PDB ID: 9D57) and unliganded iGABASnFR precursor (orange).

The bound GABA molecule is represented as colored spheres.

( b ) Cartoon representation of iGABASnFR2 with key mutations shown as yellow sticks.

Mutations in the original iGABASnFR1 are shown in magenta.

( c ) GABA binding site of iGABASnFR2. Residues involved in GABA binding are shown as lines and GABA is shown as sticks.

Figure 3—source data 1. Data collection and refinement statistics of iGABASnFR2 in complex with GABA.⟦>zach claim=f7d3b257-5ae5-4122-a122-0184b12b15f7: @{Figure 3—source data 1. Data collection and refinement statistics of iGABASnFR2 in complex with GABA.} crystal-structure-pdb-9d57⟧

The hinge region of Pf622, which connects the two lobes, likely plays a key role in allosteric modulation of ligand binding ( Marvin and Hellinga, 2001 ; Telmer and Shilton, 2003 ); ( Marvin et al., 2019 ; Planamente et al., 2012 ; Planamente et al., 2010 ).

Within that hinge region, the F101L mutation, introduced in the original iGABASnFR1 ( Marvin et al., 2019 ), increased binding affinity 10-fold ( Figure 3b ).⟦>zach claim=gap: @{Within that hinge region, the F101L mutation, introduced in the original iGABASnFR1 ( Marvin et al., 2019 ), increased binding affinity 10-fold ( Figure 3b ).} No claim states that the F101L hinge mutation of iGABASnFR1 raised binding affinity tenfold.⟧

Also in the hinge region, residue S99 forms hydrogen bonds with the OD2 atom of D59 and NE2 atom of Q17, while the S99A mutation in iGABASnFR2 abolishes these interactions, potentially making the hinge region more flexible.

The GABA binding site itself is defined by the side chains of W9, T13, F100, Y102, W202, R205, D228, and Y264 ( Figure 3c ).⟦>zach claim=gap: @{The GABA binding site itself is defined by the side chains of W9, T13, F100, Y102, W202, R205, D228, and Y264 ( Figure 3c ).} The structural claims cover the deposition and the rigidity of cpGFP on binding, but not the identity of the residues that form the GABA binding site.⟧

In iGABASnFR2, two mutations near the ligand binding site enhance interactions: F102Y forms a hydrogen bond via its hydroxyl group with D228, which, in turn, makes a hydrogen bond with the GABA amino group.

And F104Y, while farther from the binding site, helps position W202 to interact with GABA through van der Waals forces.

These likely contribute to the increased affinity for GABA we describe below.

Mutations at the interface between the ligand-binding domain and cpGFP modulate ligand-binding-induced fluorescence changes in many sensors ( Akerboom et al., 2009 ; Ding et al., 2014 ; Zhang et al., 2023 ).

In iGABASnFR2, the L178 gfp S mutation at this interface is likely involved in a hydrogen-bonding network with nearby hydrophilic residues, enhancing the GABA-induced fluorescence change ( Figure 3b ).⟦>zach claim=gap: @{In iGABASnFR2, the L178 gfp S mutation at this interface is likely involved in a hydrogen-bonding network with nearby hydrophilic residues, enhancing the GABA-induced fluorescence change ( Figure 3b ).} The proposed hydrogen-bonding role of the L178gfpS mutation in enhancing the fluorescence change is a mechanistic interpretation no claim carries.⟧

The N260A mutation in iGABASnFR1 eliminates side chain hydrogen bonding, removes a cryptic N-linked glycosylation site (N-X-S/T), and enhances protein expression.

Another critical mutation, F145 gfp W, introduced in the original iGABASnFR1 to improve ΔF/F0, interacts directly with the hydroxyl group in the chromophore and surrounding residues.

Interestingly, although the Venus flytrap domain undergoes significant conformational changes upon GABA binding, cpGFP and its flanking linkers (along with up to four adjacent residues) do not show notable conformational changes ( Figure 3a ).⟦>zach claim=81a3fe0f-a268-4abf-8ad5-b4abbdb4b2dc: @{Interestingly, although the Venus flytrap domain undergoes significant conformational changes upon GABA binding, cpGFP and its flanking linkers (along with up to four adjacent residues) do not show notable conformational changes ( Figure 3a ).} GABA closes the Pf622 lobes of iGABASnFR2 while leaving cpGFP nearly rigid.⟧

The structural difference between the unliganded and liganded forms shows a root mean square deviation of only 0.25 Å.

This finding contrasts with observations in GCaMP ( Akerboom et al., 2012 ; Akerboom et al., 2009 ; Zhang et al., 2023 ), where calcium binding to calmodulin induces substantial conformational changes at the interface, contributing to the large change in fluorescence with this sensor.

These differences suggest a potential strategy to further enhance the performance of iGABASnFR2. Biochemical characterization For in vivo applications, the effectiveness of the sensor depends on both its affinity for GABA, as well as the kinetics of GABA binding.

Sensor affinity should not be so high that it is saturated by tonic levels of GABA in the brain, but should of course be in a range sensitive to the changes in concentration achieved during synaptic release.

In mammals, extrasynaptic GABA concentrations lie in the low micromolar range 0.2–2.5 μM ( Glykys and Mody, 2007 ; Lerma et al., 1986 ; Roth and Draguhn, 2012 ; Tossman et al., 1986 ), while synaptically released GABA can transiently reach low millimolar concentrations (~1.5–3 mM Barberis et al., 2004 ; Mozrzymas et al., 2003 ; Roth and Draguhn, 2012 ).

The half-maximal effective concentration (EC 50 ) of iGABASnFR1 when it is expressed on the surface of neurons is 30 μM, so increasing sensor affinity could potentially lead to improved performance in vivo without contaminating signal from tonic GABA levels.

However, kinetics are also important - the rapid changes in GABA concentration during synaptic release mean that sensor kinetics have to be fast enough to detect the change before GABA concentrations drop back down due to reuptake and diffusion.

We first determined sensor affinities by titrating GABA concentration while monitoring fluorescence of purified protein.

Somewhat surprisingly, purified iGABASnFR2 showed a smaller dynamic range than iGABASnFR1, although its affinity was higher ( Figure 4a ; max dF/F0 iGABASnFR2: 0.45, iGABASnFR1: 1.82; EC 50 iGABASnFR2=1.1 μM, iGABASnFR1=5.7 μM).⟦>zach claim=gap: @{Somewhat surprisingly, purified iGABASnFR2 showed a smaller dynamic range than iGABASnFR1, although its affinity was higher ( Figure 4a ; max dF/F0 iGABASnFR2: 0.45, iGABASnFR1: 1.82; EC 50 iGABASnFR2=1.1 μM, iGABASnFR1=5.7 μM).} The affinity claim is about on-cell EC50; the purified-protein result that iGABASnFR2 has a smaller dynamic range than iGABASnFR1 despite higher solution affinity appears in no claim.⟧

It also displayed high selectivity for GABA over structurally related compounds ( Figure 4—figure supplement 1 ), none of which interfered with GABA binding ( Figure 4—figure supplement 2 ).⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{It also displayed high selectivity for GABA over structurally related compounds ( Figure 4—figure supplement 1 ), none of which interfered with GABA binding ( Figure 4—figure supplement 2 ).} igabasnfr2-gaba-selective-specificity⟧

In the experiments shown in Figure 4—figure supplement 2 , the apparent EC50 of iGABASnFR2 was similar to that measured under other conditions, although the shape of the dose-response curve differed from that observed in other assays for reasons that are not currently clear.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{In the experiments shown in Figure 4—figure supplement 2 , the apparent EC50 of iGABASnFR2 was similar to that measured under other conditions, although the shape of the dose-response curve differed from that observed in other assays for reasons that are not currently clear.} igabasnfr2-gaba-selective-specificity⟧

Importantly, despite this difference, none of the tested compounds acted as strong non-competitive allosteric antagonists or inhibitors of GABA binding.

Previous work with iGluSnFR has shown that titrations with purified protein can yield different affinity values than when expressed on the membrane of cultured neurons ( Aggarwal et al., 2023 ).

Although the origins of this discrepancy remain unclear, on-cell titrations more closely reflect the operating environment of the sensor and are, therefore, likely to better predict in vivo performance.

We found that on cells, the half-maximal effective concentration (EC 50 ) of iGABASnFR2 was 6.4±0.21 μM, a sevenfold higher affinity than iGABASnFR1 and 22-fold higher than iGABASnFR.F102 Pf G ( Figure 4b ).⟦>zach claim=10eb034c-f5b4-422e-a43b-8375a917111d: @{We found that on cells, the half-maximal effective concentration (EC 50 ) of iGABASnFR2 was 6.4±0.21 μM, a sevenfold higher affinity than iGABASnFR1 and 22-fold higher than iGABASnFR.F102 Pf G ( Figure 4b ).} igabasnfr2-oncell-affinity-sevenfold⟧

So the improved performance we observed likely stems, in part, from this increased on-cell affinity, which nevertheless remains above background levels of GABA measured in the mammalian brain.

Figure 4. Biophysical properties of iGABASnFR variants.⟦>zach claim=8e7427f6-8291-4eac-9f8f-7949b519beff: @{Figure 4. Biophysical properties of iGABASnFR variants.} igabasnfr2-2p-compatible⟧

( a ) GABA titrations with purified iGABASnFR protein.

Lines indicate fits to mean of n=5 titration series, error bars are s.e.m.⟦>zach claim=no-assertion: @{Lines indicate fits to mean of n=5 titration series, error bars are s.e.m.} A graphical-encoding note on what the fitted lines and error bars represent.⟧

( b ) GABA titrations with sensors expressed on the surface of cultured neurons.

Fits (bottom panel) show ΔF/F0 response to increasing concentrations of GABA measured with region of interests (ROIs) placed on individual cell bodies (top panel).

In these conditions, iGABASnFR2 shows a greater dynamic range than iGABASnFR1, in contrast to results with purified protein.

Color lookup table is the same for all images.

Scale bar: 50 µm.

Illumination: 5.6 mW/mm 2 , imaging at 1 frame per second.

( c ) Observed reaction rate constant ( K obs ) values from stopped-flow measurements for the three sensors.

( d ) Stopped-flow kinetics of iGABASnFR variants.

Lines indicate fits to mean of n=3 replicates from three separate batches of purified protein.⟦>zach claim=no-assertion: @{Lines indicate fits to mean of n=3 replicates from three separate batches of purified protein.} A graphical-encoding note on what the fitted lines represent and how many replicates they average.⟧

( e ) One-photon excitation and emission spectra of soluble iGABASnFR protein in the presence (10 mM) and absence of GABA.

( f ) Two-photon excitation spectra and the computed ΔF/F0 of iGABASnFR variants in the presence (10 mM) and absence of GABA.

Figure 4—figure supplement 1. Responses of iGABASnFR variants to GABA-related compounds.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{Figure 4—figure supplement 1. Responses of iGABASnFR variants to GABA-related compounds.} igabasnfr2-gaba-selective-specificity⟧

Different iGABASnFR variants (200 nM) were titrated with various concentrations of ligands of interest.

Estimated EC 50 values shown in insets.

Each titration has a minimum of n=3 replicates.⟦>zach claim=no-assertion: @{Each titration has a minimum of n=3 replicates.} A statement of replicate count for the titrations, not a result.⟧

Figure 4—figure supplement 2. Competition of GABA-related compounds for binding to iGABASnFR variants.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{Figure 4—figure supplement 2. Competition of GABA-related compounds for binding to iGABASnFR variants.} igabasnfr2-gaba-selective-specificity⟧

Different iGABASnFR variants (200 nM) were titrated with increasing concentrations of GABA in the presence of different potential competing compounds at 1 mM. Lines indicate fits to mean of n=3 titration series, error bars are s.e.m.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{Different iGABASnFR variants (200 nM) were titrated with increasing concentrations of GABA in the presence of different potential competing compounds at 1 mM. Lines indicate fits to mean of n=3 titration series, error bars are s.e.m.} igabasnfr2-gaba-selective-specificity — This describes the competition titrations against related compounds at 1 mM that the selectivity claim reports as showing no interference.⟧

Estimated EC 50 values shown in insets.

Figure 4—figure supplement 3. pH titrations of iGABASnFR variants.⟦>zach claim=8e7427f6-8291-4eac-9f8f-7949b519beff: @{Figure 4—figure supplement 3. pH titrations of iGABASnFR variants.} igabasnfr2-2p-compatible⟧

( a ) Fluorescence response of the three iGABASnFR variants across a pH titration, under GABA-saturated (10 mM GABA; sat-state, solid lines) and GABA-free (apo-state, dashed lines) conditions.

Fluorescence values are normalized to the peak fluorescence of the GABA-saturated form of each sensor, except for iGABASnFR2n, which is normalized to its apo-state fluorescence.

Measurements were performed at a sensor concentration of 200 nM.

Data points represent the mean of n=3 technical replicates; error bars indicate s.e.m.⟦>zach claim=no-assertion: @{Data points represent the mean of n=3 technical replicates; error bars indicate s.e.m.} A graphical-encoding note on what the plotted points and error bars represent.⟧

( b ) pH dependence of the difference in fluorescence between GABA-saturated and GABA-free conditions for the three different sensors. iGABASnFR1 shows stronger pH dependence than either of the v2 sensors.

We examined sensor kinetics to step changes in GABA concentration using stopped-flow measurements.

Relative to iGABASnFR1, the observed reaction rate constants were far greater for both iGABASnFR2 and iGABASnFR2n ( Figure 4c ). iGABASnFR1 exhibits biphasic kinetics, with a relatively fast initial change compounded with a much longer phase before sensor saturation is reached ( Marvin et al., 2019 ).⟦>zach claim=837eae22-f6f6-4d29-9696-c998ee633b7f: @{Relative to iGABASnFR1, the observed reaction rate constants were far greater for both iGABASnFR2 and iGABASnFR2n ( Figure 4c ). iGABASnFR1 exhibits biphasic kinetics, with a relatively fast initial change compounded with a much longer phase before sensor saturation is reached ( Marvin et al., 2019 ).} igabasnfr2-single-exponential-kinetics⟧

In contrast, both iGABASnFR2 and iGABASnFR2n kinetics were accurately captured by fitting with a single exponential function, indicating a less complex relationship between ligand binding and changes in fluorescence ( Figure 4d ).⟦>zach claim=837eae22-f6f6-4d29-9696-c998ee633b7f: @{In contrast, both iGABASnFR2 and iGABASnFR2n kinetics were accurately captured by fitting with a single exponential function, indicating a less complex relationship between ligand binding and changes in fluorescence ( Figure 4d ).} igabasnfr2-single-exponential-kinetics⟧

Although significantly faster than the first version, the kinetics of iGABASnFR2 and 2n are still slower than iGluSnFR3 ( Aggarwal et al., 2023 ), suggesting further improvements in sensor performance would be possible if kinetics could be accelerated.

The 1p and 2p spectra of all sensors were similar ( Figure 4e and f ), as were their apparent pKa values ( Figure 4—figure supplement 3 ).⟦>zach claim=8e7427f6-8291-4eac-9f8f-7949b519beff: @{The 1p and 2p spectra of all sensors were similar ( Figure 4e and f ), as were their apparent pKa values ( Figure 4—figure supplement 3 ).} igabasnfr2-2p-compatible⟧

Notably, iGABASnFR2 and 2n responses were less pH-dependent than those of the first-generation sensor.

Additional biophysical properties are reported in Table 1 .⟦>zach claim=no-assertion: @{Additional biophysical properties are reported in Table 1 .} A pure cross-reference to Table 1.⟧

Overall, both kinetic and thermodynamic observations suggest that iGABASnFR2 and 2n offer a major improvement in sensing GABA over the previously available sensor.

We next tested this by evaluating performance in vivo.

Table 1. Photophysical properties of iGABASnFR variants as purified proteins. λ abs (nm) λ Ex (nm) λ Em (nm) ΔF/F ε (M/cm 2 ) Φ τ (ns) GABA PBS GABA PBS GABA PBS iGABASnFR1 490 489 508 1.9 14,070±600 5375±220 0.58±0.01 0.54±0.03 2.22±0.05 2.32±0.01 iGABASnFR2 490 490 508 0.46 26,195±390 19,800±380 0.61±0.02 0.54±0.01 2.29±0.08 2.30±0.02 iGABASnFR2n 493 496 509 –0.13 12,390±690 13,000±220 0.72±0.02 0.76±0.01 2.71±0.02 2.72±0.02 Evaluating sensor performance in intact retina To evaluate indicator performance in an intact neural circuit, we examined synaptic transmission in the retina.⟦>zach claim=gap: @{Table 1. Photophysical properties of iGABASnFR variants as purified proteins. λ abs (nm) λ Ex (nm) λ Em (nm) ΔF/F ε (M/cm 2 ) Φ τ (ns) GABA PBS GABA PBS GABA PBS iGABASnFR1 490 489 508 1.9 14,070±600 5375±220 0.58±0.01 0.54±0.03 2.22±0.05 2.32±0.01 iGABASnFR2 490 490 508 0.46 26,195±390 19,800±380 0.61±0.02 0.54±0.01 2.29±0.08 2.30±0.02 iGABASnFR2n 493 496 509 –0.13 12,390±690 13,000±220 0.72±0.02 0.76±0.01 2.71±0.02 2.72±0.02 Evaluating sensor performance in intact retina To evaluate indicator performance in an intact neural circuit, we examined synaptic transmission in the retina.} This table is the only place the purified-protein photophysics appear - extinction coefficients (iGABASnFR2 roughly double iGABASnFR1's), quantum yields, fluorescence lifetimes and peak wavelengths - and no claim states any of them.⟧

GABAergic inhibition is believed to play a pivotal role in generating direction-selective responses to motion in the retina ( Briggman et al., 2011 ; Yonehara et al., 2011 ).

Direction selectivity is thought to originate in starburst amacrine cells (SACs), which extend radially symmetric dendrites from a centrally located soma.

Inputs to SACs are sprinkled across the entire dendritic arbor, while the outputs are confined to varicosities located near the dendritic tips.

Motion selectivity is proposed to arise from differential GABA release.

Specifically, the hypothesis is that GABA release is stronger when a visual stimulus moves so that excitation sweeps down the dendritic branch from root to tip (centrifugal motion) rather than when it sweeps from tip to root (centripetal motion) ( Figure 5a ).⟦>zach claim=gap: @{Specifically, the hypothesis is that GABA release is stronger when a visual stimulus moves so that excitation sweeps down the dendritic branch from root to tip (centrifugal motion) rather than when it sweeps from tip to root (centripetal motion) ( Figure 5a ).} The retina claim asserts that direction-selective GABA release was demonstrated, but no claim states the centrifugal-versus-centripetal hypothesis being tested.⟧

The resulting direction-selective inhibition is relayed to direction-selective retinal ganglion cells (DSGCs) through asymmetric synaptic connections ( Briggman et al., 2011 ; Yonehara et al., 2011 ; Figure 5b ).⟦>zach claim=gap: @{The resulting direction-selective inhibition is relayed to direction-selective retinal ganglion cells (DSGCs) through asymmetric synaptic connections ( Briggman et al., 2011 ; Yonehara et al., 2011 ; Figure 5b ).} The relay of direction-selective inhibition to DSGCs through asymmetric connections is background from prior work that no claim in the tree carries.⟧

By inhibiting DSGC responses to motion in the null direction, SAC inputs ensure that DSGC output is highly selective for motion in the preferred direction, which is subsequently transmitted to the brain.

Figure 5. iGABASnFR2 reliably reports direction selectivity in the retina.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{Figure 5. iGABASnFR2 reliably reports direction selectivity in the retina.} igabasnfr2-retina-direction-selectivity⟧

( a ) Schematic illustration of centrifugal direction selectivity in starburst cell motion responses.

( b ) Spatially asymmetric inhibitory connections (red dots) between starburst cells (SACs) and direction-selective ganglion cells (DSGCs), which are proposed to generate direction selectivity in DSGCs.

( c ) Example field of view of SAC processes expressing iGABASnFR1. The yellow region of interest (ROI) is analyzed to evaluate responses to visual stimuli.

( d ) Responses to static flash from ROI in c but with SACs expressing iGABASnFR2. ( e ) Responses to motion stimulus.

( f–h ) Results of imaging using iGABASnFR2. ( i ) Histograms of response amplitude index (left) and response reliability (right) from SACs expressing iGABASnFR. n=147 ROIs collected across five retinae.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( f–h ) Results of imaging using iGABASnFR2. ( i ) Histograms of response amplitude index (left) and response reliability (right) from SACs expressing iGABASnFR. n=147 ROIs collected across five retinae.} igabasnfr2-retina-direction-selectivity — The claim's comparison of response reliability between the two sensors accounts for these amplitude and reliability distributions from iGABASnFR-expressing SACs.⟧

( j ) As in i but with SACs expressing iGABASnFR2. n=346 ROIs collected from three retinae.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( j ) As in i but with SACs expressing iGABASnFR2. n=346 ROIs collected from three retinae.} igabasnfr2-retina-direction-selectivity — The matching iGABASnFR2 distributions are the other half of the sensor comparison the claim makes.⟧

Responses to motion stimulus.

( k ) Average signals during preferred direction motion with iGABASnFR1 (top, gray) and iGABASnFR2 (bottom, cyan).

Line and shading indicate mean ± s.d (n=147 for iGABASnFR, n=346 for iGABASnFR2).⟦>zach claim=no-assertion: @{Line and shading indicate mean ± s.d (n=147 for iGABASnFR, n=346 for iGABASnFR2).} A graphical-encoding note on what the line and shading represent.⟧

( l ) Comparison of signal-to-noise ratio (SNR) of the motion response detected with the two sensor versions. p =0. Two-tailed Mann-Whitney-Wilcoxon test.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( l ) Comparison of signal-to-noise ratio (SNR) of the motion response detected with the two sensor versions. p =0. Two-tailed Mann-Whitney-Wilcoxon test.} igabasnfr2-retina-direction-selectivity — The claim asserts significantly higher SNR for iGABASnFR2 in retina, which is what this comparison tests.⟧

( m ) Comparison of direction selectivity (CV, circular variance) for the two sensor versions. p =7.812×10 –6 .⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( m ) Comparison of direction selectivity (CV, circular variance) for the two sensor versions. p =7.812×10 –6 .} igabasnfr2-retina-direction-selectivity — The claim that iGABASnFR2 resolves direction selectivity where iGABASnFR1 cannot accounts for this circular-variance comparison.⟧

Two-tailed Mann-Whitney-Wilcoxon test.

Notably, the evidence for this centrifugal selectivity has been obtained by electrophysiological membrane potential recording and two-photon Ca 2+ imaging from starburst cells ( Euler et al., 2002 ; Vaney et al., 2012 ).

Direct evidence for direction-selective GABA release has been lacking, and imaging GABA release from the starburst cell dendrites would provide important confirmation of the origin of retinal direction selectivity.

We virally transfected starburst amacrine cells with iGABASnFR1 or iGABASnFR2, using a Cre-Lox system for cellular specificity.

Six to eight weeks after injection, we dissected retinae and performed two-photon imaging, analyzing activity within small fields of view expected to contain multiple release sites on the amacrine cell dendrites.

We first tested whether we could detect responses to light flashes with a 500 μm spot that covered the entire field of view. iGABASnFR1 showed weak but measurable signals to this full-field stimulation, although detecting responses on single trials was challenging.

However, when presented with moving dots, the weak signal made it very difficult to detect direction selectivity, even after trial-averaging.

By contrast, iGABASnFR2 responses to static flashes were large enough to be detected on single trials, and robust direction selectivity of GABA release was readily observed in response to motion stimuli.

We quantified the quality of the signals by computing two measures: (1) response amplitude index (RAI), which denotes the light-evoked response strength and (2) response reliability, which reflects trial-to-trial variance (Methods) ( Baden et al., 2016 ).

Overall, both the response amplitudes and the reliability of the responses were significantly higher with iGABASnFR2 than with iGABASnFR1 ( Figure 5i and j ).

In particular, response reliability was much improved in iGABASnFR2 (mean ± SD iGABASnFR2: 0.66±0.14; iGABASnFR: 0.41±0.11), indicating that this sensor reveals activity that previously would have been below detection threshold.

We also examined the signal-to-noise ratio (SNR) of the responses to motion, comparing response amplitude to the variance of signals at baseline.

Compared with iGABASnFR1 signals, iGABASnFR2 signals had significantly higher SNR with both larger signals and lower variance of the baseline ( Figure 5k and l ).

The improved SNR and higher response reliability across trials resulted in stable motion responses with lower circular variance (CV; Figure 5m ), yielding better direction selectivity measurements overall.

Overall, the improved performance of iGABASnFR2 not only enabled us to detect more responses but also provided a more accurate measure of GABA release evoked by visual motion, directly demonstrating that starburst cells release GABA in a direction-selective manner.

Sensor performance at individual cell axons and in vivo As a first step toward in vivo application, we tested whether iGABASnFR could detect GABA release from single interneuron activation in brain slices.

We expressed either iGABASnFR1 or iGABASnFR2 in hippocampal neurons, using viral delivery in mice to obtain acute slices (viral titre 0.1E10), or by biolistic transfection in organotypic hippocampal slice cultures (see Methods).

We performed simultaneous two-photon imaging and whole-cell recordings of individual interneurons, using an intracellular dye to trace their axons and identify presumptive presynaptic boutons.

Once individual boutons were identified, we triggered brief bursts of action potentials and monitored iGABASnFR signals using a rapid spiral (‘Tornado’) scanning approach previously developed for imaging glutamate sensors ( Jensen et al., 2019 ).

In interneurons expressing iGABASnFR1, we were unable to detect any spike-evoked fluorescence signals, despite conducting 15 trials per cell across five separate experiments (example in Figure 6a ).⟦>zach claim=ff5506c7-eac9-42f7-8643-d38068feafd5: @{In interneurons expressing iGABASnFR1, we were unable to detect any spike-evoked fluorescence signals, despite conducting 15 trials per cell across five separate experiments (example in Figure 6a ).} igabasnfr2-single-bouton-hippocampus⟧

In contrast, iGABASnFR2-expressing cells consistently displayed evoked signals at individual axonal boutons (although obtaining a signal-to-noise ratio >3 might require 5–10 trial averaging; example in Figure 6b ).⟦>zach claim=ff5506c7-eac9-42f7-8643-d38068feafd5: @{In contrast, iGABASnFR2-expressing cells consistently displayed evoked signals at individual axonal boutons (although obtaining a signal-to-noise ratio >3 might require 5–10 trial averaging; example in Figure 6b ).} igabasnfr2-single-bouton-hippocampus⟧

Figure 6. iGABASnFR2 reliably detects synaptic GABA release in slices and sensory-evoked GABA in vivo.⟦>zach claim=f2fccd5f-8ee8-4138-9e97-055ebda75cd8: @{Figure 6. iGABASnFR2 reliably detects synaptic GABA release in slices and sensory-evoked GABA in vivo.} igabasnfr2-invivo-barrel-cortex⟧

( a ) Top : Image from a whole-cell recording of an iGABASnFR1-expressing hippocampal interneuron in area CA3 of an acute brain slice.

To identify axonal boutons, morphology was visualized using Alexa Fluor 594 (red channel), included in the internal solution.

The image shown is from the red channel.

The axonal segment (dotted rectangle) is shown magnified in the inset, with the position of a schematized 1.5 µm-wide Tornado scan path indicated.

The image is the average projection of a z-stack covering 50 µm.

Bottom : iGABASnFR1 fluorescence signal acquired using a 0.5 kHz Tornado scan at the bouton shown above.

Horizontal axis: time (700 ms scan duration); vertical axis: spiral turn angle.

Trace shows mean ΔF/F₀ response (± SEM) across 15 trials of five action potentials at 50 Hz (arrows).

( b ) Top : As in ( a ), except the image shows iGABASnFR2 fluorescence from an interneuron in area CA1 in an organotypic slice.

The image is the average projection of a 30 µm z-stack.

Bottom : As in ( a ), but showing iGABASnFR2 signal from the Tornado scan.

Trace shows the mean ΔF/F₀ response (± SEM) across 11 trials of four action potentials delivered at 20 Hz (arrows).

( c ) Brief rhythmic whisker stimulus triggers volume-transmitted extracellular elevations of GABA in the barrel cortex detected by iGABASnFR2 fluorescence.

Left : Schematic of experimental arrangement, with whisker stimulation via four air puffs at 20 Hz while imaging the contralateral barrel cortex.

Right : The image panel shows the barrel cortex area (~300 µm depth) and position of a 1 kHz Tornado scan.

Trace is the single-trial fluorescence response of iGABASnFR2 to a contralateral 200 ms whisker stimulation, as indicated.

Figure 6—video 1. iGABASnFR2 detects volume-transmitted GABA signals evoked by sensory stimulation in vivo in the barrel cortex.⟦>zach claim=f2fccd5f-8ee8-4138-9e97-055ebda75cd8: @{Figure 6—video 1. iGABASnFR2 detects volume-transmitted GABA signals evoked by sensory stimulation in vivo in the barrel cortex.} igabasnfr2-invivo-barrel-cortex⟧

Fluorescence (ΔF = F – F₀) signal from iGABASnFR2 imaged in vivo from a 200×30 µm region of barrel cortex (~150 µm depth).

A brief whisker stimulus (four pulses at 20 Hz; red dot indicates onset) triggered a macroscopic extracellular GABA elevation.

Data were acquired at 1 kHz using resonant scanning and displayed with a 250 ms sliding average to suppress heartbeat-related noise.

We next sought to detect GABA release signals in vivo.

In vivo imaging of GABA transients poses additional challenges due to overlapping biological and instrumental noise sources, making detection at single boutons more difficult than in quiescent brain slices.

However, GABA released from interneuron bursts can diffuse tens of microns from its release sites, generating extracellular ‘volume-transmitted’ signals ( Oláh et al., 2009 ).

These GABA waves have previously been detected with iGABASnFR2 in brain slices during highly synchronized, pathological network discharges ( Magloire et al., 2023 ).

Here, we tested whether iGABASnFR2 could resolve volume-transmitted GABA release in response to physiological sensory stimulation in vivo.

We focused our imaging on areas of thalamocortical input in the barrel cortex L1-L3 and applied rhythmic whisker stimulation (RWS), a paradigm known to evoke reliable Ca² + signals in thalamocortical axons ( Petreanu et al., 2012 ), also shown in our own prior work ( Henneberger et al., 2020 ).

Following expression of AAV9-hSyn-iGABASnFR2 in cortical neurons, a brief RWS protocol (four 20 Hz air puffs over 200 ms) consistently triggered robust fluorescence increases across a ~150 µm-wide area in the barrel cortex layers L2-L3 (see Figure 6c , or L1-L2 layers, Figure 6—video 1 ).⟦>zach claim=f2fccd5f-8ee8-4138-9e97-055ebda75cd8: @{Following expression of AAV9-hSyn-iGABASnFR2 in cortical neurons, a brief RWS protocol (four 20 Hz air puffs over 200 ms) consistently triggered robust fluorescence increases across a ~150 µm-wide area in the barrel cortex layers L2-L3 (see Figure 6c , or L1-L2 layers, Figure 6—video 1 ).} igabasnfr2-invivo-barrel-cortex⟧

Fluorescence changes were clearly visible across sensor-expressing neuronal processes, consistent with the interpretation that these are volume-transmitted signals generated by interneurons.

Based on prior calibration of iGABASnFR2 in brain slices ( Magloire et al., 2023 ), the observed ΔF/F₀ corresponds to a transient extracellular GABA concentration increase of approximately 2–2.5 µM at peak.


## discussion

Discussion Here we report an improved GABASnFR, developed using a high-throughput mutagenesis and screening pipeline that has previously been used to optimize calcium indicators ( Dana et al., 2016 ; Wardill et al., 2013 ; Zhang et al., 2023 ).

Despite the fact that only 20% of primary cultured neurons are expected to be inhibitory ( Wonders and Anderson, 2006 ), this pipeline was still capable of identifying improved sensor variants. iGABASnFR2 has a sevenfold increase in affinity for GABA, as well as a 30% increase in rise time kinetics compared to the first-generation sensor.

Importantly, sensor affinity remains in a range where it is not likely to be saturated by tonic levels of GABA.

Additionally, the improved kinetics make it more likely the sensor can capture the rapid changes in GABA concentration that occur at the synaptic cleft as GABA is released and rapidly reuptaken.

The throughput of the screening platform made it possible to target 39 different sites in the protein for saturation mutagenesis.

Such an extensive screen was important to get enough coverage that many sites with relatively small improvements could be combined to derive an overall more effective sensor.

Of the 39 sites targeted, we found 12 mutations across 6 sites that contributed to improved sensor performance or expression.

However, no single mutation produced an especially large improvement in performance.

It was particularly challenging to identify single-site variants with both strong expression and high signal-to-noise.

Fortunately, many of the single-site mutations interacted additively when combined.

However, it was also the case that many double mutant combinations failed to pass our basic quality control standards, which may indicate that the combinations resulted in a failed, non-fluorescent sensor.

Whether higher-order combinations can realistically yield sensors with improved performance remains an open question—functional variants may prove even more rare when more mutations are combined, and/or the increase in performance may come in smaller increments as higher-order combinations are produced.

No single mutation produced an especially large improvement in performance.

Identifying single-site variants with both strong expression and high signal-to-noise was particularly challenging.

Many of the single-site mutations interacted additively when combined.

Still, numerous double mutant combinations failed to pass basic quality control standards, possibly indicating that the combinations produced non-functional, non-fluorescent sensors.

Whether higher-order combinations can realistically yield sensors with improved performance remains an open question—functional variants may become even rarer as more mutations are added, and any performance gains may diminish with each additional layer of complexity.

The extensive screening also enabled the serendipitous discovery of negative-going sensors.

Of course, positive- and negative-going variants cannot be combined in a single experiment because they have identical spectral properties.

However, in experiments where precisely timed GABA release is expected, replicating an observation with sensors of different polarities could increase confidence in a result, particularly given the lower signal-to-noise of current GABA indicators compared to widely used sensors, such as GCaMP and iGluSnFR.

More importantly, negative-going sensors convert decreases in extracellular GABA into positive fluorescence signals.

Decreases in extrasynaptic GABA are a hallmark of changes in excitation–inhibition balance that accompany several important brain-state transitions.

These include arousal and attention, where neuromodulatory drive increases GABA uptake and suppresses tonic interneuron and astrocytic GABA release, as well as stress- or antidepressant-responsive states linked to reduced astrocytic GABA production and increased transporter activity ( Semyanov et al., 2004 ; Farrant and Nusser, 2005 ; Brickley and Mody, 2012 ; Rusakov et al., 2011 ; Yoon et al., 2014 ; Ferguson and Gao, 2018 ).

In these contexts, a negative-going sensor offers a distinct advantage by providing a direct optical readout of shifts toward heightened network excitability that are difficult to infer from synaptic measurements alone.

There are several promising avenues that could be taken to further optimize iGABASnFR.

First, although several sites contributed small improvements in sensor performance, we did not attempt to go much beyond two-site combinations in this study, so higher-order combinations are one straightforward route to further optimization.

Second, sensor expression is evidently an aspect which could be improved.

We attempted to capture this in our screening criteria by measuring the fraction of responsive pixels for each variant.

However, this partly conflates the amplitude of the sensor’s signal with its expression level, and a more direct measure of expression would be preferable.

Third, trafficking the sensor efficiently to the membrane is likely another point of improvement.

In work with iGluSnFR ( Aggarwal et al., 2023 ) and eLACCO ( Nasu et al., 2023 ), a panel of different transmembrane anchors were evaluated for sensor localization, and some were found to be more effective than the PDGFR domain that anchors iGABASnFR2. Finally, the high throughput of our screening pipeline may provide sufficient training data that machine learning approaches used to further optimize jGCaMP8 ( Wait et al., 2024 ) can be applied to iGABASnFR.

When assessing sensor performance, we observed consistent discrepancies between in vitro and cell-based measurements, with purified protein typically exhibiting higher apparent affinity and larger dynamic range than neuronal measurements.

These discrepancies likely reflect both the addition of the ~60-amino-acid transmembrane anchor, which can constrain conformational flexibility, and the distinct physicochemical environment experienced by a membrane-tethered sensor at the neuronal surface.

The magnitude and even direction of these effects are difficult to predict a priori, as illustrated by iGluSnFR3, which exhibits a higher apparent affinity when membrane-tethered than in soluble form ( Aggarwal et al., 2023 ).

Accordingly, we view biochemical characterization as an important guide during sensor optimization, but consider neuronal measurements the most informative indicator of in vivo sensor performance.

Importantly, even within these constraints, the improvements we identified resulted in a qualitative advance in the ability to detect inhibition in the retina.

While the first-generation sensor showed some signal, direction-selective inhibition was reliably detectable on single trials only with iGABASnFR2. This sensor has also been used to detect inhibitory transmission during epileptiform activity in hippocampal slices ( Magloire et al., 2023 ).

These are strong signals, but here we further show that iGABASnFR2 is sensitive enough to detect GABA release triggered by activation of single neurons in brain slices—a critical benchmark for in vivo applicability.

In intact animals, the sensor reported GABA release in somatosensory cortex in response to physiological sensory stimulation.

These signals reflect relatively slow volume-transmitted extracellular GABA ‘waves’ that result from spatiotemporal summation and dissipation of multiple GABA hotspots generated by rapid GABA release at individual synapses ( Boddum et al., 2016 ; Oláh et al., 2009 ; Pavlov et al., 2014 ; Sylantyev et al., 2020 ).

Although we did not distinguish synaptic from extrasynaptic GABA in this study, further improvements in kinetics and signal-to-noise may be needed to reliably resolve synaptic events and broaden the utility of the sensor for more demanding in vivo applications.

Even in its current form, however, iGABASnFR2 is well suited for contexts where GABA signals are spatially integrated or temporally averaged, such as photometry or strong population-level activity.

Given the longstanding difficulty of directly visualizing inhibitory signaling in the brain, we anticipate that these improved sensors will serve as valuable tools for the neuroscience community.


## captions

=== Figure 1 === Figure 1. Field stimulation screen for improved iGABASnFR.⟦>zach claim=f1d695b7-88cd-49d5-9fdc-f66cad65e1c8: @{=== Figure 1 === Figure 1. Field stimulation screen for improved iGABASnFR.} igabasnfr2-fourfold-sensitivity-gain⟧

( a ) Top: Schematic representation of iGABASnFR1 and the amino acid substitutions that gave rise to iGABASnFR2 and iGABASnFR2n.

White, IgG secretion signal (cleaved off during trafficking to cell surface); blue, GABA binding protein Pf622; green, cpSFGFP; dark green, Myc epitope tag; red, PDGFR transmembrane domain.

Numbering is relative to each of the constituent protein domains; the relationship to sequential numbering of the entire polypeptide is shown in Figure 1—figure supplement 1 .⟦>zach claim=no-assertion: @{Numbering is relative to each of the constituent protein domains; the relationship to sequential numbering of the entire polypeptide is shown in Figure 1—figure supplement 1 .} A note on residue-numbering convention pointing to a supplementary sequence figure, asserting nothing about the sensor.⟧

Bottom: Crystal structure of a preliminary version of iGABASnFR (PDB ID 6DGV) with the 39 sites targeted for mutagenesis.

Gray spheres indicate the approximate position of GABA, based on homology to the liganded structure of GABA-binding protein Atu4243 ( Planamente et al., 2012 ).

( b ) Mutagenesis and screening strategy.

Variants with single-site mutations are screened for ΔF/F and expression in an initial field stimulation assay, strong performers identified and then combined and re-screened in a second round.

The top-performing mutants (positive-going quadruple mutant iGABASnFR2 and negative-going triple mutant iGABASnFR2n) are characterized further.

( c ) Joint optimization of sensitivity (ΔF/F, x-axis) and expression, measured with responsive pixels (y-axis). ΔF/F is normalized to in-plate iGABASnFR1 controls.

Black circle: (1,1) position represents iGABASnFR.

Plus signs: mutants from the first round that were put together to form combos in the second round. iGABASnFR2 and 2 n exhibited increased ΔF/F (4.3-fold and –2.2-fold of iGABASnFR, respectively) and greater numbers of responsive pixels (13.1-fold and 10.3-fold).

Illumination: 0.34 mW/mm 2 , imaging framerate: 50 Hz.

( d ) Performance measures of sensor variants from the screen.

Single-site variants are shown in gray, and double-site combinations are shown in black.

Variants are ranked according to the ΔF/F0 values measured for 40 AP, and those rankings are maintained for the lower displays of sensor F0, tau on, the time constant of the rising phase of the response, and tau off for the decay.

All values are normalized to in-plate iGABASnFR1 controls.

[panels detected: a, b, c, d] === Figure 1s1 === Figure 1—figure supplement 1. Annotated amino acid sequence of iGABASnFRs.⟦>zach claim=no-assertion: @{[panels detected: a, b, c, d] === Figure 1s1 === Figure 1—figure supplement 1. Annotated amino acid sequence of iGABASnFRs.} A bare figure title for the annotated sequence supplement, carrying no finding of its own.⟧

( a ) iGABASnFR1 sequence shown in gray text, with sites targeted for mutagenesis in black.

Shading indicates domains according to: IgG secretion signal Pf622 2–276 SFGFP 147–238 Junction SFGFP 1–146 Pf622 277–320 Myc epitope PDGFR transmembrane domain 513–561 ( b ) iGABASnFR2 sequence, with mutations shown in red text.

Mutations are listed according to domain numbers, with sequential numbering through the polypeptide indicated at the left.

Sequential numbering through the polypeptide is indicated on the left, while mutations in the text are listed according to domain numbers: S99 Pf A.F102 Pf Y.F104 Pf Y.L178 gfp S. S99 Pf A.F102 Pf Y.F104 Pf Y.L178 gfp S, which we subsequently refer to as iGABASnFR2, and the best variant with inverted signal, iGABASnFR.S99 Pf A.F104 Pf H.R168 gfp P was chosen to be iGABASnFR2n.

( c ) iGABASnFR2n sequence, with mutations shown in red text.

Sequential numbering through the polypeptide is indicated on the left, while mutations in the text are listed according to domain numbers: S99 Pf A.F104 Pf H.R168 gfp P. ( d ) Schematic showing the relationship between domain-based numbering scheme and sequential numbering through the entire polypeptide (top) and the domain-based numbering scheme.

In both schemes, numbering starts at the residue exposed after signal sequence cleavage.

[panels detected: a, b, c, d] === Figure 2 === Figure 2. Characterization of iGABASnFR variants in cultured neurons.⟦>zach claim=f1d695b7-88cd-49d5-9fdc-f66cad65e1c8: @{[panels detected: a, b, c, d] === Figure 2 === Figure 2. Characterization of iGABASnFR variants in cultured neurons.} igabasnfr2-fourfold-sensitivity-gain⟧

( a ) Fluorescence images of primary neurons expressing iGABASnFR1 (orange), iGABASnFR2 (green), iGABASnFR2n (blue) under the CAG promoter at baseline, at peak brightness after field stimulation with 40 action potentials (APs), and the corresponding ΔF/F0. Scale bar, 20 μm.

( b ) Time courses of the ΔF/F0 response to 1, 10, and 40 APs delivered at 83 Hz. iGABASnFR2n signals are inverted for display.

Traces and error bars denote mean ± s.e.m., n=20 culture wells for each variant.⟦>zach claim=no-assertion: @{Traces and error bars denote mean ± s.e.m., n=20 culture wells for each variant.} A graphical-encoding note on what the traces and error bars represent.⟧

( c ) Rise time constants of the three sensor variants obtained from exponential fits for the 1 AP condition (n=24 culture wells for iGABASnFR1 and iGABASnFR2, n=18 for iGABASnFR2n).⟦>zach claim=gap: @{( c ) Rise time constants of the three sensor variants obtained from exponential fits for the 1 AP condition (n=24 culture wells for iGABASnFR1 and iGABASnFR2, n=18 for iGABASnFR2n).} The kinetics claim covers rise and decay at 10 action potentials; the single-AP rise-time comparison shown in this panel is stated nowhere in the tree.⟧

For panels ( c-f ), red lines indicate the mean and boxes indicate the 95% confidence interval.

( d ) Decay time constants of the three variants for the 1 AP condition.

( e ) Peak ΔF/F0 of the three variants over different levels of stimulation.

( f ) Signal-to-noise (d′) of the three variants over different levels of stimulation.

[panels detected: a, b, c, d, e, f] === Figure 3 === Figure 3. Crystal structure of iGABASnFR2 in complex with GABA.⟦>zach claim=f7d3b257-5ae5-4122-a122-0184b12b15f7: @{[panels detected: a, b, c, d, e, f] === Figure 3 === Figure 3. Crystal structure of iGABASnFR2 in complex with GABA.} crystal-structure-pdb-9d57⟧

( a ) Superposition of the structure of iGABASnFR2 in complex with GABA (green; PDB ID: 9D57) and unliganded iGABASnFR precursor (orange).

The bound GABA molecule is represented as colored spheres.

( b ) Cartoon representation of iGABASnFR2 with key mutations shown as yellow sticks.

Mutations in the original iGABASnFR1 are shown in magenta.

( c ) GABA binding site of iGABASnFR2. Residues involved in GABA binding are shown as lines and GABA is shown as sticks.

Figure 3—source data 1. Data collection and refinement statistics of iGABASnFR2 in complex with GABA.⟦>zach claim=f7d3b257-5ae5-4122-a122-0184b12b15f7: @{Figure 3—source data 1. Data collection and refinement statistics of iGABASnFR2 in complex with GABA.} crystal-structure-pdb-9d57⟧

[panels detected: a, b, c] === Figure 4 === Figure 4. Biophysical properties of iGABASnFR variants.⟦>zach claim=8e7427f6-8291-4eac-9f8f-7949b519beff: @{[panels detected: a, b, c] === Figure 4 === Figure 4. Biophysical properties of iGABASnFR variants.} igabasnfr2-2p-compatible⟧

( a ) GABA titrations with purified iGABASnFR protein.

Lines indicate fits to mean of n=5 titration series, error bars are s.e.m.⟦>zach claim=no-assertion: @{Lines indicate fits to mean of n=5 titration series, error bars are s.e.m.} A graphical-encoding note on what the fitted lines and error bars represent.⟧

( b ) GABA titrations with sensors expressed on the surface of cultured neurons.

Fits (bottom panel) show ΔF/F0 response to increasing concentrations of GABA measured with region of interests (ROIs) placed on individual cell bodies (top panel).

In these conditions, iGABASnFR2 shows a greater dynamic range than iGABASnFR1, in contrast to results with purified protein.

Color lookup table is the same for all images.

Scale bar: 50 µm.

Illumination: 5.6 mW/mm 2 , imaging at 1 frame per second.

( c ) Observed reaction rate constant ( K obs ) values from stopped-flow measurements for the three sensors.

( d ) Stopped-flow kinetics of iGABASnFR variants.

Lines indicate fits to mean of n=3 replicates from three separate batches of purified protein.⟦>zach claim=no-assertion: @{Lines indicate fits to mean of n=3 replicates from three separate batches of purified protein.} A graphical-encoding note on what the fitted lines represent and how many replicates they average.⟧

( e ) One-photon excitation and emission spectra of soluble iGABASnFR protein in the presence (10 mM) and absence of GABA.

( f ) Two-photon excitation spectra and the computed ΔF/F0 of iGABASnFR variants in the presence (10 mM) and absence of GABA.

[panels detected: a, b, c, d, e, f] === Figure 4s1 === Figure 4—figure supplement 1. Responses of iGABASnFR variants to GABA-related compounds.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{[panels detected: a, b, c, d, e, f] === Figure 4s1 === Figure 4—figure supplement 1. Responses of iGABASnFR variants to GABA-related compounds.} igabasnfr2-gaba-selective-specificity⟧

Different iGABASnFR variants (200 nM) were titrated with various concentrations of ligands of interest.

Estimated EC 50 values shown in insets.

Each titration has a minimum of n=3 replicates. === Figure 4s2 === Figure 4—figure supplement 2. Competition of GABA-related compounds for binding to iGABASnFR variants.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{Each titration has a minimum of n=3 replicates. === Figure 4s2 === Figure 4—figure supplement 2. Competition of GABA-related compounds for binding to iGABASnFR variants.} igabasnfr2-gaba-selective-specificity⟧

Different iGABASnFR variants (200 nM) were titrated with increasing concentrations of GABA in the presence of different potential competing compounds at 1 mM. Lines indicate fits to mean of n=3 titration series, error bars are s.e.m.⟦>zach claim=669554c3-7a4d-453b-b9bd-893e935e630c: @{Different iGABASnFR variants (200 nM) were titrated with increasing concentrations of GABA in the presence of different potential competing compounds at 1 mM. Lines indicate fits to mean of n=3 titration series, error bars are s.e.m.} igabasnfr2-gaba-selective-specificity — This describes the competition titrations against related compounds at 1 mM that the selectivity claim reports as showing no interference.⟧

Estimated EC 50 values shown in insets. === Figure 4s3 === Figure 4—figure supplement 3. pH titrations of iGABASnFR variants.⟦>zach claim=8e7427f6-8291-4eac-9f8f-7949b519beff: @{Estimated EC 50 values shown in insets. === Figure 4s3 === Figure 4—figure supplement 3. pH titrations of iGABASnFR variants.} igabasnfr2-2p-compatible⟧

( a ) Fluorescence response of the three iGABASnFR variants across a pH titration, under GABA-saturated (10 mM GABA; sat-state, solid lines) and GABA-free (apo-state, dashed lines) conditions.

Fluorescence values are normalized to the peak fluorescence of the GABA-saturated form of each sensor, except for iGABASnFR2n, which is normalized to its apo-state fluorescence.

Measurements were performed at a sensor concentration of 200 nM.

Data points represent the mean of n=3 technical replicates; error bars indicate s.e.m.⟦>zach claim=no-assertion: @{Data points represent the mean of n=3 technical replicates; error bars indicate s.e.m.} A graphical-encoding note on what the plotted points and error bars represent.⟧

( b ) pH dependence of the difference in fluorescence between GABA-saturated and GABA-free conditions for the three different sensors. iGABASnFR1 shows stronger pH dependence than either of the v2 sensors.

[panels detected: a, b] === Figure 5 === Figure 5. iGABASnFR2 reliably reports direction selectivity in the retina.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{[panels detected: a, b] === Figure 5 === Figure 5. iGABASnFR2 reliably reports direction selectivity in the retina.} igabasnfr2-retina-direction-selectivity⟧

( a ) Schematic illustration of centrifugal direction selectivity in starburst cell motion responses.

( b ) Spatially asymmetric inhibitory connections (red dots) between starburst cells (SACs) and direction-selective ganglion cells (DSGCs), which are proposed to generate direction selectivity in DSGCs.

( c ) Example field of view of SAC processes expressing iGABASnFR1. The yellow region of interest (ROI) is analyzed to evaluate responses to visual stimuli.

( d ) Responses to static flash from ROI in c but with SACs expressing iGABASnFR2. ( e ) Responses to motion stimulus.

( f–h ) Results of imaging using iGABASnFR2. ( i ) Histograms of response amplitude index (left) and response reliability (right) from SACs expressing iGABASnFR. n=147 ROIs collected across five retinae.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( f–h ) Results of imaging using iGABASnFR2. ( i ) Histograms of response amplitude index (left) and response reliability (right) from SACs expressing iGABASnFR. n=147 ROIs collected across five retinae.} igabasnfr2-retina-direction-selectivity — The claim's comparison of response reliability between the two sensors accounts for these amplitude and reliability distributions from iGABASnFR-expressing SACs.⟧

( j ) As in i but with SACs expressing iGABASnFR2. n=346 ROIs collected from three retinae.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( j ) As in i but with SACs expressing iGABASnFR2. n=346 ROIs collected from three retinae.} igabasnfr2-retina-direction-selectivity — The matching iGABASnFR2 distributions are the other half of the sensor comparison the claim makes.⟧

Responses to motion stimulus.

( k ) Average signals during preferred direction motion with iGABASnFR1 (top, gray) and iGABASnFR2 (bottom, cyan).

Line and shading indicate mean ± s.d (n=147 for iGABASnFR, n=346 for iGABASnFR2).⟦>zach claim=no-assertion: @{Line and shading indicate mean ± s.d (n=147 for iGABASnFR, n=346 for iGABASnFR2).} A graphical-encoding note on what the line and shading represent.⟧

( l ) Comparison of signal-to-noise ratio (SNR) of the motion response detected with the two sensor versions. p =0. Two-tailed Mann-Whitney-Wilcoxon test.⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( l ) Comparison of signal-to-noise ratio (SNR) of the motion response detected with the two sensor versions. p =0. Two-tailed Mann-Whitney-Wilcoxon test.} igabasnfr2-retina-direction-selectivity — The claim asserts significantly higher SNR for iGABASnFR2 in retina, which is what this comparison tests.⟧

( m ) Comparison of direction selectivity (CV, circular variance) for the two sensor versions. p =7.812×10 –6 .⟦>zach claim=808a0591-b637-4f1a-9ff9-e05e779644bf: @{( m ) Comparison of direction selectivity (CV, circular variance) for the two sensor versions. p =7.812×10 –6 .} igabasnfr2-retina-direction-selectivity — The claim that iGABASnFR2 resolves direction selectivity where iGABASnFR1 cannot accounts for this circular-variance comparison.⟧

Two-tailed Mann-Whitney-Wilcoxon test.

[panels detected: a, b, c, d, e, f, g, h, i, j, k, l, m] === Figure 6 === Figure 6. iGABASnFR2 reliably detects synaptic GABA release in slices and sensory-evoked GABA in vivo.⟦>zach claim=f2fccd5f-8ee8-4138-9e97-055ebda75cd8: @{[panels detected: a, b, c, d, e, f, g, h, i, j, k, l, m] === Figure 6 === Figure 6. iGABASnFR2 reliably detects synaptic GABA release in slices and sensory-evoked GABA in vivo.} igabasnfr2-invivo-barrel-cortex⟧

( a ) Top : Image from a whole-cell recording of an iGABASnFR1-expressing hippocampal interneuron in area CA3 of an acute brain slice.

To identify axonal boutons, morphology was visualized using Alexa Fluor 594 (red channel), included in the internal solution.

The image shown is from the red channel.

The axonal segment (dotted rectangle) is shown magnified in the inset, with the position of a schematized 1.5 µm-wide Tornado scan path indicated.

The image is the average projection of a z-stack covering 50 µm.

Bottom : iGABASnFR1 fluorescence signal acquired using a 0.5 kHz Tornado scan at the bouton shown above.

Horizontal axis: time (700 ms scan duration); vertical axis: spiral turn angle.

Trace shows mean ΔF/F₀ response (± SEM) across 15 trials of five action potentials at 50 Hz (arrows).

( b ) Top : As in ( a ), except the image shows iGABASnFR2 fluorescence from an interneuron in area CA1 in an organotypic slice.

The image is the average projection of a 30 µm z-stack.

Bottom : As in ( a ), but showing iGABASnFR2 signal from the Tornado scan.

Trace shows the mean ΔF/F₀ response (± SEM) across 11 trials of four action potentials delivered at 20 Hz (arrows).

( c ) Brief rhythmic whisker stimulus triggers volume-transmitted extracellular elevations of GABA in the barrel cortex detected by iGABASnFR2 fluorescence.

Left : Schematic of experimental arrangement, with whisker stimulation via four air puffs at 20 Hz while imaging the contralateral barrel cortex.

Right : The image panel shows the barrel cortex area (~300 µm depth) and position of a 1 kHz Tornado scan.

Trace is the single-trial fluorescence response of iGABASnFR2 to a contralateral 200 ms whisker stimulation, as indicated.

[panels detected: a, b, c]


## tables

Table 1. Photophysical properties of iGABASnFR variants as purified proteins. λ abs (nm) λ Ex (nm) λ Em (nm) ΔF/F ε (M/cm 2 ) Φ τ (ns) GABA PBS GABA PBS GABA PBS iGABASnFR1 490 489 508 1.9 14,070±600 5375±220 0.58±0.01 0.54±0.03 2.22±0.05 2.32±0.01 iGABASnFR2 490 490 508 0.46 26,195±390 19,800±380 0.61±0.02 0.54±0.01 2.29±0.08 2.30±0.02 iGABASnFR2n 493 496 509 –0.13 12,390±690 13,000±220 0.72±0.02 0.76±0.01 2.71±0.02 2.72±0.02⟦>zach claim=gap: @{Table 1. Photophysical properties of iGABASnFR variants as purified proteins. λ abs (nm) λ Ex (nm) λ Em (nm) ΔF/F ε (M/cm 2 ) Φ τ (ns) GABA PBS GABA PBS GABA PBS iGABASnFR1 490 489 508 1.9 14,070±600 5375±220 0.58±0.01 0.54±0.03 2.22±0.05 2.32±0.01 iGABASnFR2 490 490 508 0.46 26,195±390 19,800±380 0.61±0.02 0.54±0.01 2.29±0.08 2.30±0.02 iGABASnFR2n 493 496 509 –0.13 12,390±690 13,000±220 0.72±0.02 0.76±0.01 2.71±0.02 2.72±0.02} This table is the only place the purified-protein photophysics appear - extinction coefficients (iGABASnFR2 roughly double iGABASnFR1's), quantum yields, fluorescence lifetimes and peak wavelengths - and no claim states any of them.⟧
