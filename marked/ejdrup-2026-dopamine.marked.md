# Computational modelling identifies key determinants of subregion-specific dopamine dynamics in the striatum

<!-- ejdrup-2026-dopamine · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Striatal dopamine (DA) release regulates reward-related learning and motivation and is believed to consist of a short-lived phasic and continuous tonic component.

Here, we build a large-scale three-dimensional model of extracellular DA dynamics in dorsal (DS) and ventral striatum (VS).

The model predicts rapid dynamics in DS with little to no basal DA and slower dynamics in the VS enabling build-up of tonic DA levels.

These regional differences do not reflect release-related phenomena but rather differential dopamine transporter (DAT) activity.

Interestingly, our simulations posit DAT nanoclustering as a possible regulator of this activity.

Receptor binding simulations show that D1 receptor occupancy follows extracellular DA concentration with milliseconds delay, while D2 receptors do not respond to brief pauses in firing but rather integrate DA signal over seconds.

Summarised, our model distills recent experimental observations into a computational framework that challenges prevailing paradigms of striatal DA signalling.


## introduction

Introduction Striatal dopamine (DA) release is essential for regulating reward-related learning, incentive motivation, and motor function ( Berke, 2018 ; Klaus et al., 2019 ).

DA exerts these roles over a broad range of time scales, yet DA primarily operates as a volume transmitter that targets metabotropic receptors located within a micrometre range from the sites of release ( Agnati et al., 1995 ; Borroto-Escuela et al., 2018 ; Cragg and Rice, 2004 ; Gonon et al., 2000 ; Sulzer et al., 2016 ).

The temporal and spatial dynamics of DA release in the striatum, however, remain a highly contested topic.

Classically, DA release has been divided into tonic release, driven by pacemaker-like spontaneous firing, and phasic release from coordinated bursts of firing across neurons ( Niv et al., 2007 ; Schultz, 2007 ; Sulzer et al., 2016 ).

However, this sharp distinction in release modes, as well as the existence of a basal DA level, has recently been challenged ( Berke, 2018 ; Ejdrup et al., 2023 ; Jørgensen et al., 2023 ; Liu et al., 2021 ; Sippy and Tritsch, 2023 ).

The picture is further complicated by major regional differences across striatal subdomains.

These include differences in Ca 2+ -channel and nicotinic acetylcholine receptor (nAChR) expression profiles on DA terminals, as well as differential regulation and expression of the DA transporter (DAT; Brown et al., 2011 ; Cardozo and Bean, 1995 ; Kearney et al., 2023 ; Richards and Zahniser, 2009 ; Threlfell et al., 2010 ).

In addition, we and others have found remarkable differences in extracellular DA release dynamics between the dorsal (DS) and ventral striatum (VS; Jørgensen et al., 2023 ; Mohebi et al., 2024 ; Salinas et al., 2023 ).

Fibre photometry recordings in the DS in mice using the DA sensor dLight1.3b during self-paced exploratory activity showed a rapidly fluctuating signal, whereas we observed up to minutes-long DA dynamics in VS that correlated with behavioural output ( Jørgensen et al., 2023 ).

Concurrent measurements of extracellular DA by microdialysis and fibre photometry have furthermore corroborated the lack of tonic levels of DA in DS while supporting its presence in VS ( Ejdrup et al., 2023 ; Jørgensen et al., 2023 ).

Despite these reported differences in striatal DA dynamics, electrophysiological recordings suggest that DA neurons from the primary innervators of DS, substantia nigra par compacta (SNc) and VS, ventral tegmental area (VTA), have remarkably similar firing patterns at rest ( Dodson et al., 2016 ).

We therefore set out to better understand the fundamental principles governing extracellular DA dynamics by constructing a new computational model of the striatal DA system.

Extracellular DA dynamics have been modelled before; either one-dimensionally or with a primary focus on single release events or post-synaptic receptor binding ( Beyene et al., 2017 ; Dreyer et al., 2010 ; Dreyer and Hounsgaard, 2013 ; Dreyer et al., 2016 ; Venton et al., 2003 ; Wiencke et al., 2020 ).

Here, we present a three-dimensional model of tens of thousands of release sites, focused on larger-scale signalling and based on experimentally observed biological parameters.

The model faithfully replicates experimentally observed results as well as the difference in DA dynamics between DS and VS. Importantly, it offers compelling evidence that these differences do not primarily reflect different release phenomena but rather arise from differential expression and possibly nanoscale localisation of the DAT.


## results

Results Construction of a model of DA dynamics in the striatum We constructed a novel model of DA release using experimentally determined parameters from DS, including release, uptake, and cytoarchitecture ( Doucet et al., 1986 ; Dreyer et al., 2010 ; Dreyer and Hounsgaard, 2013 ; Liu et al., 2021 ; Olson et al., 1972 ; Sulzer et al., 2016 ).

DA release sites on axons projecting from the midbrain were randomly simulated as uniformly distributed discrete points in a three-dimensional space ( Figure 1A ).⟦>zach claim=no-assertion: @{DA release sites on axons projecting from the midbrain were randomly simulated as uniformly distributed discrete points in a three-dimensional space ( Figure 1A ).} This describes how release sites were laid out in the model, not a result the model produced.⟧

The release events themselves were simulated as point source events ( Cragg and Rice, 2004 ) driven by action potentials (AP).

We then modelled DA release for each voxel in the simulation containing a release site as a function of three key parameters: firing rate, release probability, and quantal size: (1) r e l e a s e n , t = P o i s s o n ( f r a t e d t ) n P ( R % ) t Q d t \begin{document}$$\displaystyle {\rm release_{n,t}}={\rm Poisson}\left (\rm f_{rate} \, dt\right)_{\rm n} {\rm P}\left ({\rm R}_{\% }\right)_{t}\rm Q \, dt$$\end{document} Figure 1. Large-scale 3D model of the dorsal striatum.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{We then modelled DA release for each voxel in the simulation containing a release site as a function of three key parameters: firing rate, release probability, and quantal size: (1) r e l e a s e n , t = P o i s s o n ( f r a t e d t ) n P ( R % ) t Q d t \begin{document}}$$\displaystyle {\rm release_{n,t}}}}={\rm Poisson}}\left (\rm f_{rate}} \, dt\right)_{\rm n}} {\rm P}}\left ({\rm R}}_{\% }}\right)_{t}}\rm Q \, dt$$\end{document}} Figure 1. Large-scale 3D model of the dorsal striatum.} d1r-tracks-da-50ms-delay⟧

( A ) Self-enveloped simulation space of 100 µm 3 with approximately 40,000 release sites from 150 neurons.

Colours of individual release sites are not matched to neurons.

( B ) Simulation of a single release event after 5 ms and 10 ms. Colour-coded by DA concentration.

( C ) Comparison of analytical solution and simulation of diffusion after a single release event at three different time points.

( D ) Representative snapshot of steady state DA dynamics at 4 Hz tonic firing with parameters mirroring the dorsal striatum.

( E ) Cross-section of temporal dynamics for a midway section through the simulation space shown in ( d ).

( F ) Histogram of DA concentrations ([DA]) across the entire space in ( d ).

( G ) DA release during three burst activity scenarios for all release sites in a 10 x 10 × 10 µm cube (black boxes) and spill-over into the surrounding space.

Burst simulated as an increase in firing rate on top of continued tonic firing of the surrounding space.

Traces on top are average DA concentrations for the marked cubes, with bursts schematised by coloured lines below.

The first image row is at the end of the burst, and the second row is 100 ms after.

Scale bars for traces are 200 ms and 500 nM.

Scale bar for the images is 20 µm.

( H ) Top: representative [DA] trace for a voxel with a release site during pacemaker and burst activity.

Bottom: Occupancy of D1Rs and D2Rs for the same site.

( I ) Zoom on a DA burst as in ( h ), with [DA] in blue and D1R occupancy in teal with line style indicating different affinities.

The shaded area indicates the period of bursting with 6 APs at 20 Hz.

( J ) Effect of complete pause in firing for 1 s on both average [DA] and D1R and D2R occupation.

Figure 1—source code 1. Source code used to generate data in A, D, E, and F. Figure 1—source code 2. Source code used to generate data in B and C. Figure 1—source code 3. Source code used to generate data in G. Figure 1—source code 4. Source code used to generate data in J. Figure 1—source code 5. Source code used to generate data in H. Figure 1—source code 6. Source code used to generate data in I. Figure 1—figure supplement 1. Average concentration and receptor kinetics.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{Figure 1—source code 1. Source code used to generate data in A, D, E, and F. Figure 1—source code 2. Source code used to generate data in B and C. Figure 1—source code 3. Source code used to generate data in G. Figure 1—source code 4. Source code used to generate data in J. Figure 1—source code 5. Source code used to generate data in H. Figure 1—source code 6. Source code used to generate data in I. Figure 1—figure supplement 1. Average concentration and receptor kinetics.} d1r-tracks-da-50ms-delay⟧

( A ) Average DA concentration across a 100 x 100 × 100 µm volume of simulated DS at pacemaker activity.⟦>zach claim=gap: @{( A ) Average DA concentration across a 100 x 100 × 100 µm volume of simulated DS at pacemaker activity.} No claim records what the volume-averaged DA concentration in DS looks like during pacemaker activity, only how the spatial distribution is structured.⟧

( B ) Mean concentration change in response to a single event with 60% release probability (see supplementary notes on electrical stimulation) in all neurons at time zero.⟦>zach claim=gap: @{( B ) Mean concentration change in response to a single event with 60% release probability (see supplementary notes on electrical stimulation) in all neurons at time zero.} The simulated mean response to a single synchronous release event is a result no claim in the tree states.⟧

Blue trace is output directly from simulation, grey trace is the predicted FSCV measurement.

( C ) Modelling of predicted FSCV measurement and representative snapshot of simulation space just after a release event.⟦>zach claim=gap: @{( C ) Modelling of predicted FSCV measurement and representative snapshot of simulation space just after a release event.} The model's predicted FSCV signal for a single release event is not recorded by any claim; the tree's FSCV claim covers only the 10/30/60 Hz May and Wightman replication.⟧

( D ) Peak DA concentration reached at different distances from the area with phasic activity for the three firing scenarios.⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{( D ) Peak DA concentration reached at different distances from the area with phasic activity for the three firing scenarios.} ds-lacks-pervasive-tonic-da⟧

( E ) Volume of space exposed to greater than 100 nM DA after firing relative to volume of space where terminals actively burst.⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{( E ) Volume of space exposed to greater than 100 nM DA after firing relative to volume of space where terminals actively burst.} ds-lacks-pervasive-tonic-da⟧

( F ) Least-squares fit linear regression of the dLight and GRAB DA sensors based on reported kinetics ( Labouesse and Patriarchi, 2021 ) and newest experimental characterisation of D2R ( Ågren et al., 2021 ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{( F ) Least-squares fit linear regression of the dLight and GRAB DA sensors based on reported kinetics ( Labouesse and Patriarchi, 2021 ) and newest experimental characterisation of D2R ( Ågren et al., 2021 ).} ds-lacks-pervasive-tonic-da⟧

Shaded areas indicate 95% C.I.

( G ) Top: representative [DA] trace for a voxel with a release site during pacemaker and a triple burst scenario (300 ms long bursts of 3 APs at 10 Hz, three times in a row with 300 ms in between).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{( G ) Top: representative [DA] trace for a voxel with a release site during pacemaker and a triple burst scenario (300 ms long bursts of 3 APs at 10 Hz, three times in a row with 300 ms in between).} low-burst-no-spillover-high-burst-does⟧

Bottom: Occupancy of D1Rs and D2Rs for the same site.

( H ) Effect of complete pause in firing for 1 s on both average [DA] and D2R occupation at different affinities.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{( H ) Effect of complete pause in firing for 1 s on both average [DA] and D2R occupation at different affinities.} d1r-tracks-da-50ms-delay⟧

Figure 1—figure supplement 1—source code 1. Source code used to generate data in Figure 1—figure supplement 1 .⟦>zach claim=no-assertion: @{Figure 1—figure supplement 1—source code 1. Source code used to generate data in Figure 1—figure supplement 1 .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

Figure 1—figure supplement 2. Simulation size and granularity.⟦>zach claim=no-assertion: @{Figure 1—figure supplement 2. Simulation size and granularity.} A bare figure-supplement title.⟧

( A ) Schematic of different simulation sizes.⟦>zach claim=no-assertion: @{( A ) Schematic of different simulation sizes.} A schematic of the simulation geometry illustrates the setup rather than reporting a result.⟧

( B ) Concentration percentiles at different simulation diameters.⟦>zach claim=gap: @{( B ) Concentration percentiles at different simulation diameters.} The convergence of concentration percentiles with simulation diameter is a validation result no claim in the tree captures.⟧

Results are not robust until a diameter close to 50 µm is reached (line runs behind 100 µm line).

( C ) Schematic of simulation granularity.⟦>zach claim=no-assertion: @{( C ) Schematic of simulation granularity.} A schematic of voxel granularity illustrates the setup rather than reporting a result.⟧

( D ) Effect of simulation voxel diameter on concentration percentiles.⟦>zach claim=gap: @{( D ) Effect of simulation voxel diameter on concentration percentiles.} The effect of voxel size on the concentration profile is a discretisation result the claim tree never states.⟧

Virtually no difference in concentration profiles below the 99.9 th percentile of [DA], with the 1.0 µm voxel size still following 0.1 and 0.5 µm well above that level.

The inset shows 99.75 th to 100 th percentile with y-axis matching main y-axis.

( E ) Absolute difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.⟦>zach claim=gap: @{( E ) Absolute difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.} The absolute error introduced by coarser voxels is a validation result absent from the claim tree.⟧

The inset shows 99 th to 100 th percentile with y-axis matching main y-axis.

( F ) Percentage difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.⟦>zach claim=gap: @{( F ) Percentage difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.} The percentage error introduced by coarser voxels is a validation result absent from the claim tree.⟧

Figure 1—figure supplement 2—source code 1. Source code used to generate data in Figure 1—figure supplement 2 .⟦>zach claim=no-assertion: @{Figure 1—figure supplement 2—source code 1. Source code used to generate data in Figure 1—figure supplement 2 .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

Figure 1—video 1. Representative video of steady-state dynamics at 4 Hz tonic firing in a 100 x 100 × 100 µm volume with parameters mirroring those experimentally observed in dorsal (left) and ventral (right) striatum.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{Figure 1—video 1. Representative video of steady-state dynamics at 4 Hz tonic firing in a 100 x 100 × 100 µm volume with parameters mirroring those experimentally observed in dorsal (left) and ventral (right) striatum.} d1r-tracks-da-50ms-delay⟧

Slowed down 10 x for illustrative purposes.

Figure 1—video 2. Representative video of a cross-section of a burst firing of 6 action potentials (AP) at 20 Hz the centre of the plane (circle) for the dorsal (upper row) and ventral (bottom row) striatum during steady state dynamics at 4 Hz tonic firing.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{Figure 1—video 2. Representative video of a cross-section of a burst firing of 6 action potentials (AP) at 20 Hz the centre of the plane (circle) for the dorsal (upper row) and ventral (bottom row) striatum during steady state dynamics at 4 Hz tonic firing.} d1r-tracks-da-50ms-delay⟧

The left column shows DA concentration, middle D1 occupancy and right D2 occupancy.

The scale bar in the upper left-hand field shows 10 µm and is kept identical for all views.

Slowed down 15 x for illustrative purposes. where P o i s s o n ( f r a t e d t ) n \begin{document}$\rm Poisson\left (f_{rate} \, dt\right)_{n}$\end{document} is a Poisson distribution of action potentials (AP) for the given neuron (n) with the firing rate f r a t e ( l ) \begin{document}${\rm f_{rate}}(l)$\end{document} , P ( R % ) t \begin{document}${\rm P}\left ({\rm R}_{\% }\right)_{\rm t}$\end{document} is the probability of release at the individual terminal (t) for each AP, while Q \begin{document}$Q$\end{document} is the number of DA molecules released per event (dopaminergic quantal size) and d t \begin{document}$\rm dt$\end{document} the time step.

Changing f r a t e \begin{document}$\rm f_{rate}$\end{document} can be used to model both pacemaker firing, typically reported at 2–10 Hz, and burst firing, which can exceed 20 Hz ( Sulzer et al., 2016 ).

DA reuptake in the striatum is almost exclusively mediated by the DAT ( Jones et al., 1998 ), which is widely distributed along DA axons and varicosities ( Block et al., 2015 ; Eriksen et al., 2010 ; Eriksen et al., 2009 ).

As reuptake follows concentration-dependent Michaelis-Menten kinetics ( Nicholson, 1995 ), we simulated uptake as follows: (2) u p t a k e = V m a x [ D A ] K m + [ D A ] d t \begin{document}$$\displaystyle \rm uptake=\frac{V_{max}\left [DA\right ]}{K_{m}+\left [DA\right ]}dt$$\end{document} where [ D A ] \begin{document}$\left [DA\right ]$\end{document} is the concentration of DA for each voxel in the model, V m a x \begin{document}$\rm V_{max}$\end{document} is the maximal uptake capacity in the region and K m \begin{document}$\rm K_{m}$\end{document} is the concentration of DA at which half of V m a x \begin{document}$\rm V_{max}$\end{document} is reached.

The spatial distribution of released DA is a complex interplay between release, uptake, and diffusion.

Diffusion in an open 3D space can be simulated for each voxel with a Laplacian operator: (3) d i f f u s i o n = ∂ D A x , y , z , t ∂ t = D a d t ( ∂ 2 D A x , y , z , t ∂ x 2 + ∂ 2 D A x , y , z , t ∂ y 2 + ∂ 2 D A x , y , z , t ∂ z 2 ) \begin{document}$$\displaystyle \rm diffusion=\frac{\partial DA_{x,y,z,t}}{\partial t}=D_{a}dt\left (\frac{\partial ^{2}DA_{x,y,z,t}}{\partial x^{2}}+\frac{\partial ^{2}DA_{x,y,z,t}}{\partial y^{2}}+\frac{\partial ^{2}DA_{x,y,z,t}}{\partial z^{2}}\right)$$\end{document} where D a \begin{document}$\rm D_{a}$\end{document} is a corrected diffusion coefficient and dt is the timestep.

As the extracellular space of the striatum is tortuous, we modified the conventional diffusion coefficient D \begin{document}$D$\end{document} to an apparent diffusion coefficient ( D a \begin{document}$\rm D_{a}$\end{document} ) to correct for the tortuosity ( λ \begin{document}$\lambda $\end{document} ) of the striatum ( Cragg and Rice, 2004 ; Nicholson, 1985 ): (4) D a = D λ 2 \begin{document}$$\displaystyle {\rm D_{a}}=\frac{\rm D}{\lambda ^{2}}$$\end{document} As the cerebellum exhibits a tortuosity similar to that recorded in the striatum, we assumed a uniform tortuosity throughout the striatum ( Nicholson and Phillips, 1981 ).

Combining Equations 1–4 , we model DA changes in each voxel with a single conceptual equation: (5) d D A d t = r e l e a s e − u p t a k e + d i f f u s i o n \begin{document}$$\displaystyle \frac{\rm dDA}{\rm dt}=\rm release- uptake+diffusion$$\end{document} We first compared our 3D model of DA dynamics to the analytical solution of a single release event ( Cragg and Rice, 2004 ; Gonon et al., 2000 ).

To do this, we simulated a quantal event of 3000 DA molecules and calculated DA concentrations across space at three separate time points ( Figure 1B and C ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{To do this, we simulated a quantal event of 3000 DA molecules and calculated DA concentrations across space at three separate time points ( Figure 1B and C ).} ds-lacks-pervasive-tonic-da⟧

The analytic solution and our model predicted almost identical results.

Slight differences were introduced as the analytical solution assumes linear uptake from DAT while our model incorporates non-linear Michaelis-Menten kinetics.

These differences, however, were almost negligible.

The main difference between the two models lies in scalability across both space and time.

Summarised, the model enables a dynamic incorporation of the surrounding DA concentration, release events, and uptake and can be scaled to cover DA dynamics of a large 3D space, whose size and granularity is only limited by computing power (see Code Availability Section for the Python code with numerical implementations of the equations listed and scripts to run the simulations and plot the main figures).

We also tested the validity of our model by examining the response to electrical stimulation.

Importantly, our model faithfully mirrored DA release seen with fast-scan cyclic voltammetry (FSCV) recordings upon direct stimulation of striatal slices when we corrected for kinetics of the typical FSCV recording setup ( Figure 1—figure supplement 1A, B and Appendix 1 - supplementary text) ( Atcherley et al., 2015 ; Brimblecombe et al., 2019 ; Stuber et al., 2010 ; Xie et al., 2020 ).⟦>zach claim=gap: @{Importantly, our model faithfully mirrored DA release seen with fast-scan cyclic voltammetry (FSCV) recordings upon direct stimulation of striatal slices when we corrected for kinetics of the typical FSCV recording setup ( Figure 1—figure supplement 1A, B and Appendix 1 - supplementary text) ( Atcherley et al., 2015 ; Brimblecombe et al., 2019 ; Stuber et al., 2010 ; Xie et al., 2020 ).} No claim records that the model reproduces slice FSCV responses to direct stimulation once the recording kinetics are corrected for; the tree's FSCV claim covers only the May and Wightman frequency series.⟧

Simulating large-scale DA dynamics of the dorsal striatum To better understand the extracellular DA dynamics that arise from the balance between dopaminergic pacemaker activity and uptake, we simulated DA dynamics in the DS generated by pacemaker activity (4 Hz) of 150 neurons in the midbrain in a 100 x 100 × 100 µm space ( Figure 1D , see parameters in Table 1 ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{Simulating large-scale DA dynamics of the dorsal striatum To better understand the extracellular DA dynamics that arise from the balance between dopaminergic pacemaker activity and uptake, we simulated DA dynamics in the DS generated by pacemaker activity (4 Hz) of 150 neurons in the midbrain in a 100 x 100 × 100 µm space ( Figure 1D , see parameters in Table 1 ).} ds-lacks-pervasive-tonic-da⟧

Our simulations yielded a pattern of partially segregated DA hot spots with large fractions of the simulated space devoid of DA, suggesting that release events in DS only elevate DA in the immediate surroundings, with DAT-dependent clearance preventing a larger spread in space ( Figure 1D and Figure 1—video 1 ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{Our simulations yielded a pattern of partially segregated DA hot spots with large fractions of the simulated space devoid of DA, suggesting that release events in DS only elevate DA in the immediate surroundings, with DAT-dependent clearance preventing a larger spread in space ( Figure 1D and Figure 1—video 1 ).} ds-lacks-pervasive-tonic-da⟧

This was also illustrated by a cross-section in time ( Figure 1E ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{This was also illustrated by a cross-section in time ( Figure 1E ).} ds-lacks-pervasive-tonic-da⟧

In line with our recent in vivo microdialysis experiments, the average DA concentration in the simulations during pacemaker activity was approximately 10 nM ( Ejdrup et al., 2023 ).

Further, when we calculated the average concentration of a larger area across time, which fibre photometry conceivably does, the results resembled a tonic DA concentration ( Figure 1—figure supplement 1C ).⟦>zach claim=gap: @{Further, when we calculated the average concentration of a larger area across time, which fibre photometry conceivably does, the results resembled a tonic DA concentration ( Figure 1—figure supplement 1C ).} That spatially averaged simulation output looks like a tonic DA level — the reconciliation with fibre photometry — is asserted here but stated by no claim.⟧

However, our model predicted a spatial distribution that is highly heterogenous and devoid of pervasive resting or tonic DA levels ( Figure 1D–F ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{However, our model predicted a spatial distribution that is highly heterogenous and devoid of pervasive resting or tonic DA levels ( Figure 1D–F ).} ds-lacks-pervasive-tonic-da⟧

Table 1. List of variables used in the simulation of the dorsal striatum.⟦>zach claim=no-assertion: @{Table 1. List of variables used in the simulation of the dorsal striatum.} A table title introducing the parameter list.⟧

Variable Abbreviation Value Reference Firing rate 4 Hz Paladini et al., 2003 Release probability 6% Dreyer et al., 2010 DA molecules per vesicle 3000 Klaus et al., 2019 Diffusion coefficient 763 µm 2 s -1 Nicholson, 1995 Tortuosity 1.54 Rice and Nicholson, 1991 Vmax 6.0 µm s -1 See Appendix 2—table 2 Km 210 nM Hovde et al., 2019 Active terminal density - 0.04 µm -3 Liu et al., 2021 Extracellular volume fraction 0.21 Rice and Nicholson, 1991 Number of neurons in simulation space - 150 Matsuda et al., 2009 To ensure our simulations were performed within a sufficiently large space to yield consistent results, we tested different sizes of the simulated area and found a diameter of 50 μm to faithfully mimic the results of larger simulations ( Figure 1—figure supplement 2A, B ).⟦>zach claim=gap: @{Variable Abbreviation Value Reference Firing rate 4 Hz Paladini et al., 2003 Release probability 6% Dreyer et al., 2010 DA molecules per vesicle 3000 Klaus et al., 2019 Diffusion coefficient 763 µm 2 s -1 Nicholson, 1995 Tortuosity 1.54 Rice and Nicholson, 1991 Vmax 6.0 µm s -1 See Appendix 2—table 2 Km 210 nM Hovde et al., 2019 Active terminal density - 0.04 µm -3 Liu et al., 2021 Extracellular volume fraction 0.21 Rice and Nicholson, 1991 Number of neurons in simulation space - 150 Matsuda et al., 2009 To ensure our simulations were performed within a sufficiently large space to yield consistent results, we tested different sizes of the simulated area and found a diameter of 50 μm to faithfully mimic the results of larger simulations ( Figure 1—figure supplement 2A, B ).} Beyond the parameter table, this span carries the finding that a 50 um simulation diameter already reproduces larger simulations, which no claim records.⟧

Additionally, we tested our simulations at different granularity (0.1, 0.5, 1, and 2 μm).

The finer the spatial grain, the higher the detail close to a release event; however, at a spatial granularity of 1 μm, [DA] deviated by <2% across most percentiles and only by >1 nM above the 99.5 th percentile ( Figure 1—figure supplement 2C-F ), leading us to use this voxel size for our simulations.⟦>zach claim=gap: @{The finer the spatial grain, the higher the detail close to a release event; however, at a spatial granularity of 1 μm, [DA] deviated by <2% across most percentiles and only by >1 nM above the 99.5 th percentile ( Figure 1—figure supplement 2C-F ), leading us to use this voxel size for our simulations.} The finding that 1 um voxels deviate by under 2% across most percentiles, justifying the chosen grain, is recorded by no claim.⟧

Burst firing and receptor occupancy DA neurons are known to fire short bursts of APs, which is a phenomenon strongly linked to reward-prediction error and learning ( Schultz, 2007 ).

These bursts can also be induced locally in the striatum by nicotinic receptor activation ( Liu et al., 2022 ; Matityahu et al., 2023 ).

To gain insights into extracellular DA dynamics following a locally induced burst, we simulated three different firing scenarios for a group of terminals within a 10 x 10 × 10 µm field encompassing roughly 40 release sites from the randomly simulated 150 neurons: 3 pulses at 10 Hz, 6 pulses at 20 Hz, and 12 pulses at 40 Hz ( Figure 1G – burst properties matched to be the same duration).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{To gain insights into extracellular DA dynamics following a locally induced burst, we simulated three different firing scenarios for a group of terminals within a 10 x 10 × 10 µm field encompassing roughly 40 release sites from the randomly simulated 150 neurons: 3 pulses at 10 Hz, 6 pulses at 20 Hz, and 12 pulses at 40 Hz ( Figure 1G – burst properties matched to be the same duration).} low-burst-no-spillover-high-burst-does⟧

The middle scenario most closely resembles the physiological burst behaviour reported in the literature, whereas the high-activity burst is above what is typically seen.

Unsurprisingly, peak DA concentration was reached at the end of the bursts ( Figure 1G ).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{Unsurprisingly, peak DA concentration was reached at the end of the bursts ( Figure 1G ).} low-burst-no-spillover-high-burst-does⟧

The 3 APs/10 Hz bursting scenario generated no significant spill-over of DA outside the region of activity, whereas the 6 APs/20 Hz and 12 APs/40 Hz bursting scenarios markedly overwhelmed uptake ( Figure 1G ).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{The 3 APs/10 Hz bursting scenario generated no significant spill-over of DA outside the region of activity, whereas the 6 APs/20 Hz and 12 APs/40 Hz bursting scenarios markedly overwhelmed uptake ( Figure 1G ).} low-burst-no-spillover-high-burst-does⟧

The relationship between firing rate and the sphere of influence by DA became further evident when plotting maximal concentration of the surrounding space ( Figure 1—figure supplement 1D ) and the volume of space with a DA concentration above 100 nM ( Figure 1—figure supplement 1E ).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{The relationship between firing rate and the sphere of influence by DA became further evident when plotting maximal concentration of the surrounding space ( Figure 1—figure supplement 1D ) and the volume of space with a DA concentration above 100 nM ( Figure 1—figure supplement 1E ).} low-burst-no-spillover-high-burst-does — This is the frequency dependence of DA spread that the burst-spillover claim states, here shown via peak concentration and supra-100 nM volume.⟧

We found that the 3 APs/10 Hz stimulation produced DA responses that largely resembled that of a single pulse.

In both cases, DA was mostly cleared after 100ms and the volume exposed to greater than 100 nM was similar ( Figure 1G , Figure 1—figure supplement 1E ).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{In both cases, DA was mostly cleared after 100ms and the volume exposed to greater than 100 nM was similar ( Figure 1G , Figure 1—figure supplement 1E ).} low-burst-no-spillover-high-burst-does⟧

In contrast, the high bursting activities caused a frequency-dependent spill-over, where the areas exposed to a DA concentration above 100 nM were 10 and 30 times larger than the terminal origin for 6 APs/20 Hz and 12 APs/40 Hz, respectively.

Even after 100ms, a considerable amount of DA remained in the 12 APs/40 Hz scenario ( Figure 1G ).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{Even after 100ms, a considerable amount of DA remained in the 12 APs/40 Hz scenario ( Figure 1G ).} low-burst-no-spillover-high-burst-does⟧

To understand how these DA dynamics could affect the postsynaptic response, we modelled receptor binding.

D1 receptors (-Rs) were assumed to have a half maximal effective concentration (EC 50 ) of 1000 nM, and we extrapolated the reverse rate constant ( k off ) to 19.5 s –1 based on a linear fit of the recently characterised DA-receptor-based sensors ( Figure 1—figure supplement 1E ; Labouesse and Patriarchi, 2021 ).⟦>zach claim=no-assertion: @{D1 receptors (-Rs) were assumed to have a half maximal effective concentration (EC 50 ) of 1000 nM, and we extrapolated the reverse rate constant ( k off ) to 19.5 s –1 based on a linear fit of the recently characterised DA-receptor-based sensors ( Figure 1—figure supplement 1E ; Labouesse and Patriarchi, 2021 ).} This sets the D1R binding parameters used in the simulation rather than reporting a result.⟧

We set the EC 50 of D2Rs to 7 nM and k off to 0.2 s –1 based on the DA sensor kinetic fit ( Figure 1—figure supplement 1F ), which matches a recent binding study (0.197 s –1 for binding study vs. 0.204 s –1 based on linear fit), indicating the receptor-based sensor fit can be extrapolated to the endogenous receptors ( Ågren et al., 2021 ).⟦>zach claim=gap: @{We set the EC 50 of D2Rs to 7 nM and k off to 0.2 s –1 based on the DA sensor kinetic fit ( Figure 1—figure supplement 1F ), which matches a recent binding study (0.197 s –1 for binding study vs. 0.204 s –1 based on linear fit), indicating the receptor-based sensor fit can be extrapolated to the endogenous receptors ( Ågren et al., 2021 ).} Besides setting the D2R parameters, this asserts that the sensor-based kinetic fit can be extrapolated to endogenous receptors because it matches an independent binding study — a validation claim the tree does not make.⟧

To determine how these receptors would respond to our predicted DA dynamics, we simulated pacemaker activity at 4 Hz with an added burst of 6 APs/20 Hz.

Figure 1H shows a representative trace of DA concentration and occupancy of the D1R and D2R for a voxel with a release site.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{Figure 1H shows a representative trace of DA concentration and occupancy of the D1R and D2R for a voxel with a release site.} d1r-tracks-da-50ms-delay⟧

During pacemaker activity, D1R showed an occupancy close to 0, whereas D2R occupancy was approximately 0.55 ( Figure 1H ).⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{During pacemaker activity, D1R showed an occupancy close to 0, whereas D2R occupancy was approximately 0.55 ( Figure 1H ).} d1r-tracks-da-50ms-delay⟧

Both D1R and D2R occupancies were due to a high diffusion rate mostly invariant to individual release events caused by pacemaker activity.

However, upon coordinated burst firing, the occupancy rapidly increased ( Figure 1H and Figure 1—video 2 ) as diffusion no longer equilibrates the extracellular concentrations on a timescale faster than the receptors.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{However, upon coordinated burst firing, the occupancy rapidly increased ( Figure 1H and Figure 1—video 2 ) as diffusion no longer equilibrates the extracellular concentrations on a timescale faster than the receptors.} d1r-tracks-da-50ms-delay⟧

D1R receptor occupancy closely tracked extracellular DA with a delay of only ~50 ms for the typically reported affinity of 1 µM ( Figure 1I ).

By contrast, it took at least 5 s before the burst-induced increase in D2R occupancy had declined to baseline levels ( Figure 1H and Figure 1—video 2 ).⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{By contrast, it took at least 5 s before the burst-induced increase in D2R occupancy had declined to baseline levels ( Figure 1H and Figure 1—video 2 ).} d1r-tracks-da-50ms-delay⟧

This made the D2R incapable of temporally separating closely linked bursts of activity and rather summarised the output, whereas the D1R occupancy reset between each individual burst ( Figure 1—figure supplement 1G ).⟦>zach claim=d6a177f1-603e-4318-a7e0-3ec10fe39da9: @{This made the D2R incapable of temporally separating closely linked bursts of activity and rather summarised the output, whereas the D1R occupancy reset between each individual burst ( Figure 1—figure supplement 1G ).} d2r-integrates-over-seconds — The claim states exactly this: slow D2R off-kinetics leave it unable to separate closely spaced bursts, while D1R resets between them.⟧

Perhaps more surprisingly, the D2R occupancy only fell from approximately from 0.55 to 0.45 when simulating a full second pause in firing due to the slow off kinetics ( Figure 1J ).

Indeed, this finding was robust across an order of magnitude of D2R affinity (2 nm - 20 nM), although the sensitivity to a one-second pause was larger at an affinity of 20 nM ( Figure 1—figure supplement 1H ).⟦>zach claim=06c675dd-5a37-4e64-8af8-f02b15870215: @{Indeed, this finding was robust across an order of magnitude of D2R affinity (2 nm - 20 nM), although the sensitivity to a one-second pause was larger at an affinity of 20 nM ( Figure 1—figure supplement 1H ).} d2r-insensitive-to-brief-pauses — The claim already records that the pause insensitivity holds across an order of magnitude of D2R affinity, 2 to 20 nM.⟧

These simulations suggest that the dopaminergic architecture of the DS limits DA overflow during physiologically relevant bursting activity.

Further, DA receptors had a temporally mostly uniform response to DA release caused by pacemaker activity, with D1R occupancy responding rapidly to both onset and offset extracellular DA concentrations following bursts, while D2R showed seconds-long delays in offset.

Ventral striatum maintains pervasive DA tone Mounting evidence points to considerable differences in DA dynamics across striatal subregions ( Jørgensen et al., 2023 ; Mohebi et al., 2024 ), which might reflect differences in the cytoarchitectural and/or molecular dopaminergic makeup.

In line with this, most studies report lower dopaminergic density in the VS than in DS regardless of methodological modality with a median value of ~90% in VS relative to DS ( Appendix 2—table 1 ).⟦>zach claim=gap: @{In line with this, most studies report lower dopaminergic density in the VS than in DS regardless of methodological modality with a median value of ~90% in VS relative to DS ( Appendix 2—table 1 ).} The literature summary that VS dopaminergic density is about 90% of DS is the basis for the VS terminal density used later, yet no claim records it; the tree's literature claims cover only the Vmax ratio.⟧

Further, DAT-mediated uptake capacity is reported to be lower in VS with a median capacity at ~30% of DS ( Appendix 2—Tables 1 and 2 ).⟦>zach claim=39079ccf-d87a-4e0b-83a9-a01369e54836: @{Further, DAT-mediated uptake capacity is reported to be lower in VS with a median capacity at ~30% of DS ( Appendix 2—Tables 1 and 2 ).} Prior voltammetry sets a 3:1 DS:VS DAT Vmax ratio used as a model parameter. — The claim records the prior literature establishing roughly threefold lower DAT uptake capacity in VS than DS.⟧

Consistently, we observed a clear dorsoventral gradient for DAT expression when analysing immunostainings in striatal mouse brain slices from a previous publication ( Sørensen et al., 2021 ; Figure 2—figure supplement 1A, B ).⟦>zach claim=c714f46f-4715-4d61-90d8-fdac5fffa159: @{Consistently, we observed a clear dorsoventral gradient for DAT expression when analysing immunostainings in striatal mouse brain slices from a previous publication ( Sørensen et al., 2021 ; Figure 2—figure supplement 1A, B ).} dat-immunostaining-dorsoventral-gradient⟧

By contrast, the VMAT2 staining only decreased slightly from VS to DS ( Figure 2—figure supplement 1A–C ).⟦>zach claim=c714f46f-4715-4d61-90d8-fdac5fffa159: @{By contrast, the VMAT2 staining only decreased slightly from VS to DS ( Figure 2—figure supplement 1A–C ).} dat-immunostaining-dorsoventral-gradient⟧

We simulated DA release during pacemaker activity in both DS and VS. DS values were set as previously described (25 µm 3 per terminal, uptake capacity of 6.0 μM s –1 ), but for VS we reduced the terminal density to 90% (27.8 µm 3 per terminal) and DAT uptake capacity to 33% (2.0 µM s –1 ) ( Appendix 2—Tables 1 and 2 ).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{We simulated DA release during pacemaker activity in both DS and VS. DS values were set as previously described (25 µm 3 per terminal, uptake capacity of 6.0 μM s –1 ), but for VS we reduced the terminal density to 90% (27.8 µm 3 per terminal) and DAT uptake capacity to 33% (2.0 µM s –1 ) ( Appendix 2—Tables 1 and 2 ).} ds-vs-vmax-ratio-assumed — The claim records these exact regional parameter choices and flags the 3:1 Vmax ratio as assumed from the literature rather than measured here.⟧

The remaining parameters were kept identical.

With these two differences, our simulations revealed markedly different spatiotemporal DA distributions during pacemaker activity.

While DS formed segregated domains with low DA concentrations in the inter-domain space ( Figure 2A and Figure 1—video 1 ), DA diffused further throughout the simulated space in VS, before being cleared by DAT.⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{While DS formed segregated domains with low DA concentrations in the inter-domain space ( Figure 2A and Figure 1—video 1 ), DA diffused further throughout the simulated space in VS, before being cleared by DAT.} ds-vs-vmax-ratio-assumed⟧

This gave rise to what may be considered a tonic DA level with hotspots of higher DA concentrations, although the concentration distribution is continuous ( Figure 2A–C and Figure 1—video 1 ).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{This gave rise to what may be considered a tonic DA level with hotspots of higher DA concentrations, although the concentration distribution is continuous ( Figure 2A–C and Figure 1—video 1 ).} ds-vs-vmax-ratio-assumed⟧

Figure 2. Regional differences in uptake greatly impact DA dynamics.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{Figure 2. Regional differences in uptake greatly impact DA dynamics.} d2r-occupancy-higher-in-vs⟧

( A ) Representative snapshots of steady state dynamics at 4 Hz tonic firing with parameters mirroring the dorsal (left) and ventral striatum (right).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{( A ) Representative snapshots of steady state dynamics at 4 Hz tonic firing with parameters mirroring the dorsal (left) and ventral striatum (right).} ds-vs-vmax-ratio-assumed⟧

( B ) Cross-section of temporal dynamics for data shown in a.⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( B ) Cross-section of temporal dynamics for data shown in a.} vs-maintains-pervasive-tonic-da⟧

The bottom row shows concentrations of the dashed lines in the top panels.

( C ) Normalised density of DA concentration of simulations in ( a ).⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( C ) Normalised density of DA concentration of simulations in ( a ).} vs-maintains-pervasive-tonic-da⟧

Thick lines are for the entire space, and thin lines are across time for five randomly sampled locations.

Dashed red line is for simulation of the ventral striatum with lowest reported innervation density in the literature.

( D ) Same data as in ( c ), but for concentration percentiles.⟦>zach claim=897a3449-e5bd-4f12-99f2-e701f5989c74: @{( D ) Same data as in ( c ), but for concentration percentiles.} vs-lowest-percentiles-above-10nm⟧

Note that even the lowest percentiles of VS were above 10 nM in [DA].

( E ) Convolved model response (Figure S1c) to mimic FSCV measurements mirroring the experimentally tested stimulation paradigm in May and Wightman, 1989 for the dorsal (left) and ventral striatum (right) ( F ) DA release during three burst activity scenarios for all release sites in a 10 x 10 × 10 µm cube (black boxes) and spill-over into the surrounding space.⟦>zach claim=cc992651-67bd-4d1b-9237-fa13d9f9ec94: @{( E ) Convolved model response (Figure S1c) to mimic FSCV measurements mirroring the experimentally tested stimulation paradigm in May and Wightman, 1989 for the dorsal (left) and ventral striatum (right) ( F ) DA release during three burst activity scenarios for all release sites in a 10 x 10 × 10 µm cube (black boxes) and spill-over into the surrounding space.} fscv-matches-may-wightman-1989⟧

Burst simulated as an increase in firing rate on top of continued tonic firing of the surrounding space.

Traces on top are average DA concentrations for the marked cubes, with bursts schematised by coloured lines below.

The first image row is at the end of the burst, and the second row is another 100 ms after.

Scale bars for traces are 200 ms and 500 nM.

Scale bar for the images is 20 µm.

( G ) Top: representative [DA] trace 1 µm away from a release site during pacemaker and burst activity.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{( G ) Top: representative [DA] trace 1 µm away from a release site during pacemaker and burst activity.} d2r-occupancy-higher-in-vs⟧

Bottom: Occupancy of D1Rs and D2Rs for the same site.

Occupancy data from the corresponding DS simulation on Figure 1k shown as a dotted line.

( H ) Peak occupancy at different distances from the area bursting, normalised to maximal and minimum occupancy.⟦>zach claim=gap: @{( H ) Peak occupancy at different distances from the area bursting, normalised to maximal and minimum occupancy.} How peak receptor occupancy falls off with distance from the bursting region is a result no claim in the tree states.⟧

Figure 2—source code 1. Source code used to generate data in A-F.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{Figure 2—source code 1. Source code used to generate data in A-F.} d2r-occupancy-higher-in-vs⟧

Figure 2—source code 2. Source code used to generate data in G and H. Figure 2—figure supplement 1. Histochemical gradient of DAT and VMAT2 fluorescence.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{Figure 2—source code 2. Source code used to generate data in G and H. Figure 2—figure supplement 1. Histochemical gradient of DAT and VMAT2 fluorescence.} d2r-occupancy-higher-in-vs⟧

( A ) Representative image of the mouse striatal slices analysed in B. Dashed white line indicates the quantified dorsoventral gradient (length 2 mm).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{( A ) Representative image of the mouse striatal slices analysed in B. Dashed white line indicates the quantified dorsoventral gradient (length 2 mm).} ds-vs-vmax-ratio-assumed⟧

( B ) Relative intensity of the DAT and VMAT2 immunosignal in the dorsoventral axis of striatal mouse brain slices from Sørensen et al., 2021 .⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( B ) Relative intensity of the DAT and VMAT2 immunosignal in the dorsoventral axis of striatal mouse brain slices from Sørensen et al., 2021 .} vs-maintains-pervasive-tonic-da⟧

All slices show a drop at the anterior commissure (AC).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{All slices show a drop at the anterior commissure (AC).} ds-vs-vmax-ratio-assumed⟧

Shaded areas around lines denote S.E.M.

( C ) Mean relative intensity of the DAT and VMAT2 signal before and after AC.⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( C ) Mean relative intensity of the DAT and VMAT2 signal before and after AC.} vs-maintains-pervasive-tonic-da⟧

Two-sided t-test, VS-DAT:VMAT2, p=0.012(*), n=4 mice; one-sided t-tests, DAT-DS:VS, p=0.0021(**), VMAT2-DS:VS, p=0.0086(**), n=4 mice.⟦>zach claim=498bf1d1-2d0f-42d4-bdf7-c9996ed5af78: @{Two-sided t-test, VS-DAT:VMAT2, p=0.012(*), n=4 mice; one-sided t-tests, DAT-DS:VS, p=0.0021(**), VMAT2-DS:VS, p=0.0086(**), n=4 mice.} dat-clustering-greater-in-vs⟧

( D ) Peak DA concentration reached at different distances from area with phasic activity for the three firing scenarios in VS. ( E ) Volume of space in VS exposed to greater than 100 nM after firing relative to volume of space where terminals actively burst.⟦>zach claim=897a3449-e5bd-4f12-99f2-e701f5989c74: @{( D ) Peak DA concentration reached at different distances from area with phasic activity for the three firing scenarios in VS. ( E ) Volume of space in VS exposed to greater than 100 nM after firing relative to volume of space where terminals actively burst.} vs-lowest-percentiles-above-10nm⟧

( F ) Effect of complete pause in firing in VS for 1 s on both average [DA] and D1R and D2R occupation.⟦>zach claim=gap: @{( F ) Effect of complete pause in firing in VS for 1 s on both average [DA] and D1R and D2R occupation.} The effect of a one-second pause in VS is unclaimed; the pause claim in the tree concerns the dorsal striatum only.⟧

We compared our model of the two regions with existing experimental data.

In an earlier study by May and Wightman, 120 stimulus pulses were delivered in the medial forebrain bundle (MFB) at either 10, 30, or 60 Hz and DA responses were recorded by FSCV in both caudate-putamen (CPu) and nucleus accumbens (Nac; May and Wightman, 1989 ).

To mirror this, we simulated 120 action potentials at similar frequencies (10, 30, and 60 Hz) at 6% release probability and ran the result through convolution, as in Figure 1—figure supplement 1A and B , to generate an FSCV read-out ( Figure 2E ).⟦>zach claim=cc992651-67bd-4d1b-9237-fa13d9f9ec94: @{To mirror this, we simulated 120 action potentials at similar frequencies (10, 30, and 60 Hz) at 6% release probability and ran the result through convolution, as in Figure 1—figure supplement 1A and B , to generate an FSCV read-out ( Figure 2E ).} fscv-matches-may-wightman-1989⟧

Since May and Wightman reported no significant difference in DA released per electrically delivered pulse ([DA] p ) between VS and DS, we applied equal quantal size and R % for DS and VS in our simulations, while uptake capacity in VS was kept to a third of DS and terminal density was set to 90% as specified above.

Importantly, our simulated FSCV data closely resembled the earlier findings, with VS reaching considerably higher DA levels for all three stimulation frequencies ( Figure 2E – see May and Wightman, 1989 ).⟦>zach claim=cc992651-67bd-4d1b-9237-fa13d9f9ec94: @{Importantly, our simulated FSCV data closely resembled the earlier findings, with VS reaching considerably higher DA levels for all three stimulation frequencies ( Figure 2E – see May and Wightman, 1989 ).} fscv-matches-may-wightman-1989⟧

This regional difference presumably arises from differences in DAT capacity between DS and VS, as the lower terminal density in VS would have the opposite effect (see below) and the remaining parameters were held identical.

To compare with our results for DS, we tested how VS responded during simulated burst activity.

Using firing patterns identical to the DS simulations ( Figure 1G ), we found a larger spill-over of DA into the surrounding areas in VS ( Figure 2F , Figure 2—figure supplement 1D, E ).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{Using firing patterns identical to the DS simulations ( Figure 1G ), we found a larger spill-over of DA into the surrounding areas in VS ( Figure 2F , Figure 2—figure supplement 1D, E ).} low-burst-no-spillover-high-burst-does⟧

Significant amounts of extracellular DA also remained 100 ms after the physiologically relevant 6 APs/20 Hz firing stimulus.

At the receptor level, D1R occupancy in VS showed a similar response to that in DS during the burst ( Figures 1I and 2G and Figure 1—video 2 ).⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{At the receptor level, D1R occupancy in VS showed a similar response to that in DS during the burst ( Figures 1I and 2G and Figure 1—video 2 ).} d1r-tracks-da-50ms-delay⟧

By contrast, D2R occupancy during pacemaker activity was higher in VS than DS (~0.8 versus ~0.55 in DS), in accordance with the higher prevailing basal DA concentration.

Additionally, the larger DA overflow in VS after a burst caused a higher relative increase in receptor occupancy further away from the area actively bursting than compared to DS ( Figure 2H ).⟦>zach claim=gap: @{Additionally, the larger DA overflow in VS after a burst caused a higher relative increase in receptor occupancy further away from the area actively bursting than compared to DS ( Figure 2H ).} No claim states that VS shows a larger relative rise in receptor occupancy far from the bursting region than DS does.⟧

A pause in firing had the same effect on D2R as in DS ( Figure 2—figure supplement 1F ).⟦>zach claim=c714f46f-4715-4d61-90d8-fdac5fffa159: @{A pause in firing had the same effect on D2R as in DS ( Figure 2—figure supplement 1F ).} dat-immunostaining-dorsoventral-gradient⟧

Changes to uptake capacity greatly affect [DA] in the ventral striatum The values used to model the striatum ( Table 1 ) in the previous simulations were chosen to best mimic the physiological system found in vivo.⟦>zach claim=59c0aba5-a0e0-41d8-8961-fa5e927d83e7: @{Changes to uptake capacity greatly affect [DA] in the ventral striatum The values used to model the striatum ( Table 1 ) in the previous simulations were chosen to best mimic the physiological system found in vivo.} vmax-modulation-larger-impact-in-vs — This section heading states the finding the claim records, that DA in VS is far more sensitive to changes in uptake capacity than DA in DS.⟧

However, to test the robustness of the results, we performed simulations across wide ranges of the variable key parameters on which the model is based.

First, we varied the number of varicosities actively releasing DA by setting the varicosity density to one site per 9 µm 3 ( Doucet et al., 1986 ) and simulating 4 Hz pacemaker activity with the release-capable fraction ranging from 5% to 100% (reported values range from 20% to virtually all) ( Ducrot et al., 2021 ; Liu et al., 2021 ; Liu et al., 2018 ; Pereira et al., 2016 ; Figure 3A ).⟦>zach claim=no-assertion: @{First, we varied the number of varicosities actively releasing DA by setting the varicosity density to one site per 9 µm 3 ( Doucet et al., 1986 ) and simulating 4 Hz pacemaker activity with the release-capable fraction ranging from 5% to 100% (reported values range from 20% to virtually all) ( Ducrot et al., 2021 ; Liu et al., 2021 ; Liu et al., 2018 ; Pereira et al., 2016 ; Figure 3A ).} This describes the parameter range swept in the simulation rather than what the sweep produced.⟧

As the fraction of active sites increased, DA concentrations increased at both the median level (50 th percentile), which we consider a measure of tonic or baseline DA levels, and at peak levels (99.5 th percentile) in both DS and VS ( Figure 3B , see Figure 3—figure supplement 1A for schematic of tonic and peak DA).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{As the fraction of active sites increased, DA concentrations increased at both the median level (50 th percentile), which we consider a measure of tonic or baseline DA levels, and at peak levels (99.5 th percentile) in both DS and VS ( Figure 3B , see Figure 3—figure supplement 1A for schematic of tonic and peak DA).} vmax-only-parameter-driving-regional-difference⟧

We then used the 99.5 th /50 th percentile ratio as a measure of the focality of the DA distribution (i.e. hotspot DA relative to baseline DA).

This was intended as a measure of heterogeneity, that is, the higher focality, the greater competence for spatially heterogenous signalling, as has been reported in Hamid et al., 2021 ; Howe and Dombeck, 2016 .

Quantifying this across the percentage of active terminals showed that the focality of the DA distribution dropped as the active fraction increased in both regions ( Figure 3C ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{Quantifying this across the percentage of active terminals showed that the focality of the DA distribution dropped as the active fraction increased in both regions ( Figure 3C ).} vmax-only-parameter-driving-regional-difference⟧

However, the percentage of active sites in VS needed to drop to 5% to reach a relative distribution resembling the DS at a full 100% active sites, underscoring a marked difference in the spatial confinement of DA signals in VS and DS.

Figure 3. Sensitivity of the model to parameter changes.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{Figure 3. Sensitivity of the model to parameter changes.} vmax-only-parameter-driving-regional-difference⟧

( A ) Schematic of the fraction of active release sites.⟦>zach claim=no-assertion: @{( A ) Schematic of the fraction of active release sites.} A schematic of the swept parameter, asserting nothing about the world.⟧

Black dots are inactive sites, and green dots indicate actively releasing sites.

( B ) Effect of changing fraction of active release sites on DA concentrations.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( B ) Effect of changing fraction of active release sites on DA concentrations.} vmax-only-parameter-driving-regional-difference⟧

Blue line, DS peak DA concentration (99.5 th percentile); Red line, VS peak DA concentration (99.5 th percentile); Dotted blue line, DS tonic DA concentration (50 th percentile); Dotted red line, VS tonic DA concentration (50 th percentile).

( C ) Ratio between peak (99.5 th percentile) and tonic (50 th percentile) concentrations across fractions of active release sites in the DS (blue line) and VS (red line) as a measure of DA signal focality.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( C ) Ratio between peak (99.5 th percentile) and tonic (50 th percentile) concentrations across fractions of active release sites in the DS (blue line) and VS (red line) as a measure of DA signal focality.} vmax-only-parameter-driving-regional-difference⟧

( D ) Schematic of changing quantal size ( Q ).⟦>zach claim=no-assertion: @{( D ) Schematic of changing quantal size ( Q ).} A schematic of the swept parameter, asserting nothing about the world.⟧

( E ) Effect of changing quantal size on tonic and peak DA concentrations in DS (blue lines) and VS (red lines).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( E ) Effect of changing quantal size on tonic and peak DA concentrations in DS (blue lines) and VS (red lines).} vmax-only-parameter-driving-regional-difference⟧

( F ) Ratio between peak and tonic concentrations across various quantal sizes in in DS (blue line) and VS (red line).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( F ) Ratio between peak and tonic concentrations across various quantal sizes in in DS (blue line) and VS (red line).} vmax-only-parameter-driving-regional-difference⟧

( G ) Relative difference between the DS and VS for peak (black line) and tonic DA (dotted line) at different quantal sizes.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( G ) Relative difference between the DS and VS for peak (black line) and tonic DA (dotted line) at different quantal sizes.} vmax-only-parameter-driving-regional-difference⟧

( H ) Schematic of changing DAT K m .⟦>zach claim=no-assertion: @{( H ) Schematic of changing DAT K m .} A schematic of the swept parameter, asserting nothing about the world.⟧

( i ) Effect of changing DAT K m on DA concentrations in DS (blue lines) and VS (red lines).

( J ) Schematic of changing DAT V max .

( K ) Effect of changing DAT V max on DA concentrations.

Shaded areas are median V max of the two regions (DS and VS) as found in the literature shown in Appendix 2—table 2 ± 50%.⟦>zach claim=no-assertion: @{Shaded areas are median V max of the two regions (DS and VS) as found in the literature shown in Appendix 2—table 2 ± 50%.} This explains what the shaded band on the plot represents.⟧

( L ) Effect of changing DAT V max , with tonic (50 th percentile) and peak (99.5 th percentile) DA concentrations normalised to their value at 2 µm s –1 (median value for VS).

The shaded area indicates median V max for VS found in the literature shown in Appendix 2—table 2 ± 50%.⟦>zach claim=no-assertion: @{The shaded area indicates median V max for VS found in the literature shown in Appendix 2—table 2 ± 50%.} This explains what the shaded band on the plot represents.⟧

Figure 3—source code 1. Source code used to generate data in B, C, E-G. Figure 3—source code 2. Source code used to generate data in I. Figure 3—source code 3. Source code used to generate data in K and L. Figure 3—figure supplement 1. Model parameter testing.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{Figure 3—source code 1. Source code used to generate data in B, C, E-G. Figure 3—source code 2. Source code used to generate data in I. Figure 3—source code 3. Source code used to generate data in K and L. Figure 3—figure supplement 1. Model parameter testing.} vmax-only-parameter-driving-regional-difference⟧

( A ) Schematic of our definitions of tonic (50 th percentile/median, dashed lines) and peak (99.5 th percentile, solid line) DA for both the dorsal and ventral striatum.⟦>zach claim=no-assertion: @{( A ) Schematic of our definitions of tonic (50 th percentile/median, dashed lines) and peak (99.5 th percentile, solid line) DA for both the dorsal and ventral striatum.} A schematic defining the tonic and peak percentile conventions and their line styles.⟧

( B ) Effect of changing release probability (R % ) on DA concentrations.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( B ) Effect of changing release probability (R % ) on DA concentrations.} vmax-only-parameter-driving-regional-difference⟧

( C ) Relative difference between the ventral and dorsal striatum at different percentiles for different release probabilities.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( C ) Relative difference between the ventral and dorsal striatum at different percentiles for different release probabilities.} vmax-only-parameter-driving-regional-difference⟧

( D ) Ratio between 99.5 th and 50 th percentiles as a measure of focality for both regions.⟦>zach claim=gap: @{( D ) Ratio between 99.5 th and 50 th percentiles as a measure of focality for both regions.} The focality ratio between regions under the release-probability sweep is displayed here but no claim states how focality itself behaves.⟧

As R % increases, the concentrations become more homogeneous.

( E ) Effect of changing firing rate on DA concentrations.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( E ) Effect of changing firing rate on DA concentrations.} vmax-only-parameter-driving-regional-difference⟧

( F ) Relative difference between the ventral and dorsal striatum at different percentiles for different firing rates.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( F ) Relative difference between the ventral and dorsal striatum at different percentiles for different firing rates.} vmax-only-parameter-driving-regional-difference⟧

( G ) Ratio between 99.5 th and 50 th percentiles for both regions.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( G ) Ratio between 99.5 th and 50 th percentiles for both regions.} vmax-only-parameter-driving-regional-difference⟧

As the firing rate increases, the concentrations become more homogeneous.

Figure 3—figure supplement 1—source code 1. Source code used to generate data in Figure 3—figure supplement 1 .⟦>zach claim=no-assertion: @{Figure 3—figure supplement 1—source code 1. Source code used to generate data in Figure 3—figure supplement 1 .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

Figure 3—figure supplement 2. Fold change during inhibition, V max -sensitivity at different release parameters and release-uptake balance.⟦>zach claim=no-assertion: @{Figure 3—figure supplement 2. Fold change during inhibition, V max -sensitivity at different release parameters and release-uptake balance.} A bare figure-supplement title.⟧

( A ) Fold change over baseline (K m of 210 nM) for mean DA concentration in the dorsal (DS) and ventral striatum (VS) with changing DAT K m .⟦>zach claim=gap: @{( A ) Fold change over baseline (K m of 210 nM) for mean DA concentration in the dorsal (DS) and ventral striatum (VS) with changing DAT K m .} The Km sweep is unclaimed: the tree's parameter-sweep claim covers active fraction, quantal size, release probability, firing rate and Vmax, but not DAT affinity.⟧

( B ) Relative difference between the dorsal and ventral striatum for both phasic and tonic DA at different K m values.⟦>zach claim=gap: @{( B ) Relative difference between the dorsal and ventral striatum for both phasic and tonic DA at different K m values.} How the regional difference in phasic and tonic DA varies with Km is a result no claim records.⟧

( C ) Effect of changing DAT V max on DA concentrations for three different quantal sizes ( Q ).⟦>zach claim=gap: @{( C ) Effect of changing DAT V max on DA concentrations for three different quantal sizes ( Q ).} That the Vmax effect is unchanged across quantal sizes is a robustness result no claim in the tree states.⟧

[DA] normalised to highest values within each Q. Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.⟦>zach claim=no-assertion: @{[DA] normalised to highest values within each Q. Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.} This explains the normalisation and the shaded band used in the plot.⟧

( D ) Effect of changing DAT V max on DA concentrations for three different release probabilities (R % ).⟦>zach claim=gap: @{( D ) Effect of changing DAT V max on DA concentrations for three different release probabilities (R % ).} That the Vmax effect is unchanged across release probabilities is a robustness result no claim in the tree states.⟧

[DA] normalised to highest values within each R % .

Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.⟦>zach claim=no-assertion: @{Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.} This explains what the shaded band on the plot represents.⟧

( E ) Least-square fit linear regression between release rate and autocorrelation decay rate (τ) ( Ejdrup et al., 2023 ).⟦>zach claim=gap: @{( E ) Least-square fit linear regression between release rate and autocorrelation decay rate (τ) ( Ejdrup et al., 2023 ).} The regression between release rate and autocorrelation decay from the reanalysed photometry data is a result no claim records.⟧

Shaded area highlights 95% C.I.

( F ) Partial regression plot error of the regression in ( f ) and error between DA response to amphetamine as measured by microdialysis and the release rate from Ejdrup et al., 2023 to show that the less release and uptake correlate, the less release rate can explain the microdialysis response, suggesting release and uptake are partially independent of each other.⟦>zach claim=gap: @{( F ) Partial regression plot error of the regression in ( f ) and error between DA response to amphetamine as measured by microdialysis and the release rate from Ejdrup et al., 2023 to show that the less release and uptake correlate, the less release rate can explain the microdialysis response, suggesting release and uptake are partially independent of each other.} The inference that release and uptake vary partially independently across animals is asserted here but appears in no claim.⟧

Shaded area highlights 95% C.I.

Figure 3—figure supplement 2—source code 1. Source code used to generate data in Figure 3—figure supplement 2A-D .⟦>zach claim=no-assertion: @{Figure 3—figure supplement 2—source code 1. Source code used to generate data in Figure 3—figure supplement 2A-D .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

The predicted total DA content of a vesicle and the fraction of content released per fusion event is reported to range from 1,000–30,000 molecules ( Garris et al., 1994 ; Pothos et al., 1998 ; Staal et al., 2004 ; Sulzer and Pothos, 2000 ; Figure 3D ).⟦>zach claim=no-assertion: @{The predicted total DA content of a vesicle and the fraction of content released per fusion event is reported to range from 1,000–30,000 molecules ( Garris et al., 1994 ; Pothos et al., 1998 ; Staal et al., 2004 ; Sulzer and Pothos, 2000 ; Figure 3D ).} This reports the literature range used to set the bounds of the quantal-size sweep rather than a result of this study.⟧

As expected, tonic and peak concentrations increased in both DS and VS as quantal size was increased ( Figure 3E ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{As expected, tonic and peak concentrations increased in both DS and VS as quantal size was increased ( Figure 3E ).} vmax-only-parameter-driving-regional-difference⟧

Also, as expected, the focality of the DA distributions dropped for both regions as quantal size increased ( Figure 3F ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{Also, as expected, the focality of the DA distributions dropped for both regions as quantal size increased ( Figure 3F ).} vmax-only-parameter-driving-regional-difference⟧

The relative difference in tonic DA, however, remained persistently higher in VS and even increased as quantal size increased, indicating a tendency for VS to maintain basal levels of DA regardless of release content ( Figure 3G ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{The relative difference in tonic DA, however, remained persistently higher in VS and even increased as quantal size increased, indicating a tendency for VS to maintain basal levels of DA regardless of release content ( Figure 3G ).} vmax-only-parameter-driving-regional-difference⟧

The higher end of quantal sizes, however, resulted in median concentrations far beyond what is typically reported ( Figure 3E ; Sulzer et al., 2016 ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{The higher end of quantal sizes, however, resulted in median concentrations far beyond what is typically reported ( Figure 3E ; Sulzer et al., 2016 ).} vmax-only-parameter-driving-regional-difference⟧

We observed a largely similar pattern when changing either release probability or firing rate ( Figure 3—figure supplement 1B-G ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{We observed a largely similar pattern when changing either release probability or firing rate ( Figure 3—figure supplement 1B-G ).} vmax-only-parameter-driving-regional-difference — The claim states that release probability and firing rate, like the other release parameters, shift both regions alike without altering the regional contrast.⟧

DAT activity is governed by two parameters: K m and V max ( Kristensen et al., 2011 ).

To mimic competitive inhibition of DAT by, for example cocaine, we ran a simulation across various K m values ( Figure 3H ) showing that increasing K m caused a linear increase in DA levels, consistent with DAT uptake rate responding almost linearly to increases in [DA] below K m ( Figure 3I ).⟦>zach claim=gap: @{To mimic competitive inhibition of DAT by, for example cocaine, we ran a simulation across various K m values ( Figure 3H ) showing that increasing K m caused a linear increase in DA levels, consistent with DAT uptake rate responding almost linearly to increases in [DA] below K m ( Figure 3I ).} The linear rise in DA with increasing Km, the model's stand-in for competitive DAT inhibition, is recorded by no claim.⟧

Of note, most microdialysis studies have reported that cocaine increases [DA] to the same degree in both DS and VSBEsrt wishes; however, these quantifications are usually derived as a ratio of the absolute baseline level ( Carboni et al., 2001 ; Maisonneuve and Glick, 1992 ).

If we divide our simulations of increasing K m with the basal levels estimated in Figure 3A-C a similar response for DS and VS is found ( Figure 3—figure supplement 2A ).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{If we divide our simulations of increasing K m with the basal levels estimated in Figure 3A-C a similar response for DS and VS is found ( Figure 3—figure supplement 2A ).} vmax-only-parameter-driving-regional-difference⟧

Further, we observe a convergence on a twofold difference in the absolute values at both tonic and peak levels, which matches reports from earlier FSCV studies ( Figure 3—figure supplement 2B ; Wu et al., 2001 ).⟦>zach claim=gap: @{Further, we observe a convergence on a twofold difference in the absolute values at both tonic and peak levels, which matches reports from earlier FSCV studies ( Figure 3—figure supplement 2B ; Wu et al., 2001 ).} The convergence on a twofold DS-VS difference and its agreement with earlier FSCV reports is a result no claim states.⟧

This regionally differential response to cocaine matches our observations in a previous biosensor-based study ( Jørgensen et al., 2023 ).

Finally, we changed V max by ±50% in both regions and observed a smaller change in tonic level in DS (11 nM) than in VS (38 nM) ( Figure 3K ).

This suggests modulation of V max has higher impact in VS than DS.

Further, the impact of changing V max in VS was independent of both Q and R % within values typically reported in the literature ( Figure 3—figure supplement 2C, D ).⟦>zach claim=gap: @{Further, the impact of changing V max in VS was independent of both Q and R % within values typically reported in the literature ( Figure 3—figure supplement 2C, D ).} That the impact of Vmax in VS is independent of quantal size and release probability is a robustness result absent from the claim tree.⟧

In contrast to the changes in tonic levels, the relative effect V max had on peak levels was much more modest ( Figure 3L ).

Changes to uptake rate may be mediated by DAT internalisation pathways, but to our knowledge, there is not in vivo evidence of differential release-uptake balances between animals that could lead to varying tonic DA levels across animals.

We therefore reanalysed data from our previously published comparison of fibre photometry and microdialysis ( Ejdrup et al., 2023 ) and found evidence of natural variations in the release-uptake balance of the mice ( Figure 3—figure supplement 2E, F ), which may underlie different tonic levels of DA in the striatum between animals.⟦>zach claim=gap: @{We therefore reanalysed data from our previously published comparison of fibre photometry and microdialysis ( Ejdrup et al., 2023 ) and found evidence of natural variations in the release-uptake balance of the mice ( Figure 3—figure supplement 2E, F ), which may underlie different tonic levels of DA in the striatum between animals.} The reanalysis showing natural between-animal variation in release-uptake balance, offered as an explanation of differing tonic DA, is claimed nowhere in the tree.⟧

DAT nanoclustering affects steady state [DA] and clearance after bursts Our simulations highlight DAT V max as an effective regulator of extracellular DA levels in VS ( Figure 3K ).

Internalisation of DAT can serve as a mechanism for this control but is a relatively slow process operating on the order of minutes ( Kristensen et al., 2011 ).

Interestingly, our recent studies have provided evidence that DAT move laterally in the plasma membrane and transition from a clustered to an unclustered nanoscale distribution in response to excitatory drive and other inputs ( Lycas et al., 2022 ; Rahbek-Clemmensen et al., 2017 ).

This led us to hypothesise that DAT nanoclustering serves as a mechanism for regulating DAT activity on a faster time scale.

We speculated that dense nanoclusters of DAT would produce domains of low [DA] due to uptake overpowering diffusion ( Figure 4A ).⟦>zach claim=08b37324-70f4-4ff9-bf37-c73d2b8a43c4: @{We speculated that dense nanoclusters of DAT would produce domains of low [DA] due to uptake overpowering diffusion ( Figure 4A ).} DAT nanoclustering lowers effective Vmax and helps set regional dopamine dynamics. — This is the nanoclustering hypothesis as the claim states it: dense DAT clusters locally deplete DA because uptake outpaces diffusion.⟧

As the uptake rate is concentration dependent, this would reduce uptake efficiency ( Figure 4B ).⟦>zach claim=08b37324-70f4-4ff9-bf37-c73d2b8a43c4: @{As the uptake rate is concentration dependent, this would reduce uptake efficiency ( Figure 4B ).} DAT nanoclustering lowers effective Vmax and helps set regional dopamine dynamics. — The claim contains this step of the argument, that concentration-dependent uptake makes the depleted cluster surface less efficient.⟧

To address this hypothesis, we simulated a single ellipsoid varicosity of 1.5 μm in length and 800 nm thick with surrounding extracellular space ( Ducrot et al., 2021 ).

The surface was unfolded to a square of equal area ( Figure 4D ), and as 9–16.4% of terminals in the striatum are estimated to be dopaminergic ( Hökfelt, 1968 ; Tennyson et al., 1974 ), we set the volume of the surrounding space to seven times the varicosity volume.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{The surface was unfolded to a square of equal area ( Figure 4D ), and as 9–16.4% of terminals in the striatum are estimated to be dopaminergic ( Hökfelt, 1968 ; Tennyson et al., 1974 ), we set the volume of the surrounding space to seven times the varicosity volume.} dat-nanoclustering-slows-clearance⟧

On the surface of the varicosity, we randomly distributed eight DAT nanoclusters ( Figure 4C ) and ran simulations of how DAT clustering density influenced the DA clearance from the surrounding space.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{On the surface of the varicosity, we randomly distributed eight DAT nanoclusters ( Figure 4C ) and ran simulations of how DAT clustering density influenced the DA clearance from the surrounding space.} dat-nanoclustering-slows-clearance⟧

The observed DA concentration in the space surrounding the varicosity shown in Figure 4C is illustrated by the cross-section shown in Figure 4D .⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{The observed DA concentration in the space surrounding the varicosity shown in Figure 4C is illustrated by the cross-section shown in Figure 4D .} dat-nanoclustering-slows-clearance⟧

Mean DA uptake capacity of the entire space was kept constant at 4 μM s –1 (between the values observed for DS and VS) throughout the simulations, representing a constant amount of DAT molecules on the surface of the varicosity.

We only changed the fraction of the surface of the varicosity that was uptake competent by altering the cluster size from small clusters of high density to large clusters of lower density.

We ran simulations of eight identical clusters at either 20, 40, 80, or 160 nm in diameter to mirror experimentally observed cluster sizes on DA varicosities, as well as a scenario with DAT fully dispersed ( Figure 4E ; Lycas et al., 2022 ; Rahbek-Clemmensen et al., 2017 ).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{We ran simulations of eight identical clusters at either 20, 40, 80, or 160 nm in diameter to mirror experimentally observed cluster sizes on DA varicosities, as well as a scenario with DAT fully dispersed ( Figure 4E ; Lycas et al., 2022 ; Rahbek-Clemmensen et al., 2017 ).} dat-nanoclustering-slows-clearance⟧

We first performed a test to see the effect clustering would have at steady state concentrations during pacemaker activity.

In the unclustered scenario, average [DA] in the simulation hovered at ~15 nM ( Figure 4F ).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{In the unclustered scenario, average [DA] in the simulation hovered at ~15 nM ( Figure 4F ).} dat-nanoclustering-slows-clearance⟧

However, upon changing to a clustered architecture, [DA] rapidly increased up to 100% (~30 nM) in just 400 ms depending on the degree of clustering ( Figure 4F ).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{However, upon changing to a clustered architecture, [DA] rapidly increased up to 100% (~30 nM) in just 400 ms depending on the degree of clustering ( Figure 4F ).} dat-nanoclustering-slows-clearance⟧

We further wanted to test what effect nanoclustering would have on clearance after burst activity.

To do this, we set the extracellular space to a [DA] of 100 nM and performed simulations for the same clustering scenarios ( Figure 4G ).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{To do this, we set the extracellular space to a [DA] of 100 nM and performed simulations for the same clustering scenarios ( Figure 4G ).} dat-nanoclustering-slows-clearance⟧

Cluster size dramatically affected clearance time, with the most dense clusters taking almost 400ms to reduce [DA] to 5 nM, compared to just ~200 ms for the unclustered scenario.

The hyper-local low-[DA] environment that arose around the dense DAT clusters became apparent when we plotted the [DA] at the centre of a cluster compared to the mean [DA] of the extracellular space ( Figure 4H – unclustered also showed a drop from surface of varicosity to mean of extracellular space; see general gradient of [DA] in Figure 4D ).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{The hyper-local low-[DA] environment that arose around the dense DAT clusters became apparent when we plotted the [DA] at the centre of a cluster compared to the mean [DA] of the extracellular space ( Figure 4H – unclustered also showed a drop from surface of varicosity to mean of extracellular space; see general gradient of [DA] in Figure 4D ).} dat-nanoclustering-slows-clearance⟧

For the 20 nm cluster scenario, the clearance was almost entirely limited by how quickly DA diffused to the nanocluster, as the local [DA] dropped to near zero.

We originally hypothesised the effect would mainly be due to a depression in [DA] at the very cluster centre, but a concentration profile of the 80 nm cluster scenario revealed the entirety of the cluster was enveloped in a low-[DA] environment ( Figure 4I ).

Accordingly, if DA receptors are located directly next to a dense nanocluster, this effect could feasibly alter the concentration the individual receptors are exposed to.

Figure 4. DAT nanoclustering reduces uptake and shows regional variation.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4. DAT nanoclustering reduces uptake and shows regional variation.} dat-nanoclustering-slows-clearance⟧

( A ) Schematic of dense DA cluster.⟦>zach claim=no-assertion: @{( A ) Schematic of dense DA cluster.} A schematic of the modelled cluster geometry, asserting nothing about the world.⟧

White dots represent individual DAT molecules, and colour gradient the surrounding DA concentration.

( B ) Effective transport rate dependent on local concentration.⟦>zach claim=no-assertion: @{( B ) Effective transport rate dependent on local concentration.} This panel plots the assumed Michaelis-Menten dependence of uptake on concentration, a model ingredient rather than a finding.⟧

( C ) Top view of unfolded DA varicosity.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( C ) Top view of unfolded DA varicosity.} dat-nanoclustering-slows-clearance⟧

Black shapes denote clusters of DAT.

A dashed white line indicates placement of cross-section shown in ( d ).

( D ) Cross-section showing DA concentration in space surrounding varicosity unfolded in c.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( D ) Cross-section showing DA concentration in space surrounding varicosity unfolded in c.} dat-nanoclustering-slows-clearance⟧

The grey line at the bottom is the surface of the varicosity.

Colour-coded for DA concentration.

( E ) Top view from ( c ), but colour coded for DA concentration immediately above membrane surface at different DAT cluster sizes.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( E ) Top view from ( c ), but colour coded for DA concentration immediately above membrane surface at different DAT cluster sizes.} dat-nanoclustering-slows-clearance⟧

( F ) Changes in [DA] from 15 nM unclustered (Un.) steady state with constant release after changing to four different cluster size scenarios (ø=diameter).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( F ) Changes in [DA] from 15 nM unclustered (Un.) steady state with constant release after changing to four different cluster size scenarios (ø=diameter).} dat-nanoclustering-slows-clearance⟧

( G ) Clearance of 100 nM [DA] for different DAT cluster sizes.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( G ) Clearance of 100 nM [DA] for different DAT cluster sizes.} dat-nanoclustering-slows-clearance⟧

( H ) Difference between DA concentration at the centre of clusters (or general surface of varicosity for unclustered) and mean concentration of the full simulation space ( I ) Concentrations across a cross section of a surface with 80 nm diameter clusters.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( H ) Difference between DA concentration at the centre of clusters (or general surface of varicosity for unclustered) and mean concentration of the full simulation space ( I ) Concentrations across a cross section of a surface with 80 nm diameter clusters.} dat-nanoclustering-slows-clearance — The claim states this local depletion, that DA at the cluster surface falls far below the bulk concentration.⟧

Shaded areas highlight cluster locations.

( J ) Location of images of the dorsal (DS) and ventral striatum (VS) in striatal slices from mice as imaged in Sørensen et al., 2021 with direct stochastic optical reconstruction microscopy (dSTORM).

( K ) Two representative DA varicosities from DS and VS with VMAT2 in white and DAT in magenta.

Images are 1.5x2 µm (scale bar 0.5 µm).

( L ) Individual DAT localisations (locs.) from images in ( k ) coloured by clustering.

Black indicates localisation identified as clustered based on DBSCAN with parameters 80 nm diameter and 40 localisations.

Grey indicates unclustered localisations.

( M ) Quantification of clustering across all images in ( j ) with parameters in ( l ).

Welch’s two-sample t-test, p=0.012(*), n=12 (DS) and 13 (VS).⟦>zach claim=498bf1d1-2d0f-42d4-bdf7-c9996ed5af78: @{Welch’s two-sample t-test, p=0.012(*), n=12 (DS) and 13 (VS).} dat-clustering-greater-in-vs⟧

( N ) Absolute difference in percentage of clustering as assessed with DBSCAN across a range of parameters.

VS has a higher propensity to cluster across cluster sizes typically reported for DAT clusters.

Figure 4—source code 1. Source code for simulation.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4—source code 1. Source code for simulation.} dat-nanoclustering-slows-clearance⟧

Figure 4—source code 2. Source code used to generate data in A-E and G-I.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4—source code 2. Source code used to generate data in A-E and G-I.} dat-nanoclustering-slows-clearance⟧

Figure 4—source code 3. Source code used to generate data in F. Summarised, the data supports that DAT nanoclusters produce domains of low [DA] as uptake outcompetes diffusion.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4—source code 3. Source code used to generate data in F. Summarised, the data supports that DAT nanoclusters produce domains of low [DA] as uptake outcompetes diffusion.} dat-nanoclustering-slows-clearance⟧

As transporter uptake is concentration dependent, the overall uptake efficiency is reduced, which in turn may lead to higher extracellular concentrations of DA.

The simulations therefore posit DAT nanoclustering as an efficient way to regulate the extracellular levels of both tonic DA and the spatiotemporal [DA] profiles following release.

DAT clusters more in the ventral striatum As our simulations suggest that nanodomain clustering is a way of regulating uptake, and this may be particularly efficient at controlling extracellular DA in VS, we hypothesised nanoscale clustering would be more prominent in VS. To investigate this, we reanalysed data from a previous publication ( Sørensen et al., 2021 ), where we acquired super-resolution images of coronally sliced striatal sections from mice stained for DAT.

For the present study, images were split into DS and VS based on where in the slices they were taken ( Figure 4J ).

DA terminals were identified by vesicular monoamine transporter 2 (VMAT2) expression, and qualitatively, DAT appeared more clustered in VS than DS ( Figure 4K ).

To quantify this, we applied the clustering algorithm Density-Based Spatial Clustering of Applications with Noise (DBSCAN) ( Figure 4L ).

This confirmed a regional difference with more DAT localised clusters when using DBSCAN to identify clusters with scanning diameter of 80 nm in VS compared to DS ( Figure 4L and M ), and we observed a similar regional difference across the range of cluster sizes typically reported (20–200 nm; Figure 4N ; Lycas et al., 2022 ; Rahbek-Clemmensen et al., 2017 ) supporting the conclusion that DAT nanoclustering is more prevalent in VS than DS.


## discussion

Discussion We developed a three-dimensional, finite-difference computational model to investigate spatiotemporal DA dynamics of striatal subregions in detail.

Leveraging prior experimental information on regional differences in dopaminergic innervation density and DAT uptake capacity, our model predicts important differences in dopaminergic dynamics between DS and VS. Strikingly, our simulations suggest that large areas of the DS are effectively devoid of a basal level of DA at pacemaker activity, whereas VS maintain a more homogenous tonic-like basal DA concentration with only small changes in uptake activity powerfully regulating the extracellular DA tone.

Furthermore, we modelled receptor binding kinetics and found that D1R binding faithfully followed recently described rapid DA dynamics of the striatum ( Ejdrup et al., 2023 ; Jørgensen et al., 2023 ; Markowitz et al., 2023 ), while D2R, with an off-rate of ~5 s, appeared better suited for detecting background tone and integrating prolonged activity ( Howe et al., 2013 ; Jørgensen et al., 2023 ).

Collectively, these observations have important implications for our understanding of striatal function in behaviour, including decoding of inputs from the prefrontal cortex (PFC) and limbic system as well as the influential phasic-tonic model of dopaminergic signalling ( Grace et al., 2007 ; Niv et al., 2007 ; Schultz, 2007 ).

It has been assumed for long that there are tonic levels of DA in the striatum ( Niv et al., 2007 ; Schultz, 2007 ; Sulzer et al., 2016 ), although the phenomenon has no clear definition ( Berke, 2018 ).

Our simulation of DA dynamics in DS during pacemaker activity showed no evidence for a homogenous extracellular distribution.

Rather, elevated [DA] was transiently present around release sites during pacemaker activity, with the remaining space mostly depleted of DA.

The absence of a general tonic DA level in DS predicted by our model directly supports the notion that DA release sites in DS establish distinct and only partially overlapping DA domains rather than diffuse, tonic DA levels (see Liu et al., 2021 ).

This conclusion aligns with recent data where we found that DA concentrations measured by microdialysis correlate with the average of rapid activity recorded with fibre photometry rather than a baseline DA tone ( Ejdrup et al., 2023 ).

Earlier modelling work by Wickens and colleagues predicted pacemaker activity would generate a tonic, uniform concentration ( Arbuthnott and Wickens, 2007 ).

But our modelling suggested this is prevented by the significant DA uptake capacity of the DS, as measured by more recent reuptake studies (see Appendix 2—table 2 ).⟦>zach claim=gap: @{But our modelling suggested this is prevented by the significant DA uptake capacity of the DS, as measured by more recent reuptake studies (see Appendix 2—table 2 ).}⟧

In contrast to the DS, our model predicted VS to hold a considerable basal level of DA even in spaces without an immediately adjacent release site.

This is conceivably what most refer to as tonic DA.

In this study, we quantified tonic DA as the median concentration of the entire space (50 th percentile), which appeared significantly higher in VS than DS because of the lower VS uptake capacity.

Importantly, this matches the results of our direct in vivo comparison of DS and VS in freely moving mice ( Jørgensen et al., 2023 ), as well as supporting a spatial gradient of time horizons in the striatum previously predicted in a separate work by Wickens et al., 2007 and measured in vivo by Mohebi et al., 2024 .

To challenge our model predictions, we performed our simulations across a wide range of parameters.

Only changes to V max for uptake generated differential responses in the two regions.

With release and uptake parameters at values from the literature, VS was at a critical point where minor changes to uptake significantly impacted the tonic levels without any major effect on peak concentrations.

Contrary to our observations, some previous microdialysis experiments have suggested higher basal DA levels in the DS compared to VS ( Kuczenski and Segal, 1992 ; Shen et al., 2004 ) and have reported two to four times higher [DA] in DS compared to VS ( Kuczenski and Segal, 1992 ; Shen et al., 2004 ).

However, there are disparate observations in the literature (e.g. Carboni et al., 2001 reported 20% higher [DA] in VS Carboni et al., 2001 ).

Moreover, it is important to note that regional comparisons in microdialysis might be confounded by the considerably higher uptake rate in DS.

This will increase the extraction fraction and possibly lead to a significant overestimation of the extracellular concentration as compared to a region with lower uptake rate, such as the VS ( Chefer et al., 2009 ).

Our three-dimensional simulations highlight DAT-mediated reuptake as a key mechanism governing striatal DA dynamics and as a key mediator of regional-specific DA dynamics.

A physiologically relevant way to regulate uptake capacity is moving DAT to and from the plasma membrane.

Indeed, DAT is subject to such regulation and some of these mechanisms may even be exclusive to the ventral region, including protein kinase C-induced DAT internalisation and Vav2 regulation of DAT surface expression ( Fagan et al., 2020 ; Zhu et al., 2015 ).

Chemogenetic G q -coupled DREADD activation of DA neurons also results in differential DAT trafficking in the two regions ( Fagan et al., 2020 ; Kearney et al., 2023 ).

The findings position DAT regulation as an excellent candidate for changing tonic DA levels in VS, which has been proposed to selectively attenuate afferent drive from the PFC through D2R activation ( Grace et al., 2007 ).

Recent studies of D2R-expressing spiny projection neurons (SPNs) in the VS also suggest that the receptor is not fully saturated under basal firing ( Lee et al., 2020 ), matching both our simulations of receptor binding and the notion that tonic DA can be manipulated to alter D2R activation.

If changing uptake capacity is to have a behavioural relevance on a fast timescale, a mechanism to regulate DAT function faster than internalisation must exist.

Importantly, the transporter does not only move to and from the surface, but also laterally in the plasma membrane.

We have reported that DAT forms nanoclusters in the plasma membrane that dynamically reshape based on excitatory and inhibitory input ( Lycas et al., 2022 ; Rahbek-Clemmensen et al., 2017 ).

Moreover, we have previously shown that cocaine, which both competitively inhibits DAT and reorganises the transporter nanodomains ( Lycas et al., 2022 ), changes the DA signal of the DS to dynamics akin to the VS ( Jørgensen et al., 2023 ).

Importantly, our simulations showed that nanoclustering may be an effective way to sequester DAT in a dense domain where uptake overpowers diffusion and, as a result, brings down effective uptake speed through local DA depletion.

This is in line with evidence that these DAT nanoclusters are enriched in phosphatidylinositol-4,5-bisphosphate (PIP2), and that metabolism of PIP2 decreases uptake rate of DAT ( Lycas et al., 2022 ; Carvelli et al., 2002 ).

We also found that the nanoclustering phenomenon was considerably more prevalent in VS than in DS.

Taken together, these data point to DAT nanoclustering as a way to shape both the spatiotemporal profile of DA release as well as the tonic levels of DA in the striatum – particularly in the VS. Our incorporation of receptor binding was inspired by important previous modelling work ( Dreyer et al., 2010 ; Dreyer and Hounsgaard, 2013 ; Hunger et al., 2020 ).

However, earlier models by Dreyer & colleagues assumed instantaneous equilibrium between extracellular DA and receptor occupation, which disregards differences in kinetics of the DA receptors that greatly impact transmission dynamics.

While later work by Hunger and colleagues introduced more complex receptor modelling, they based their kinetics parameters on early pharmacological studies, whose values likely would prevent DA receptors from decoding signal below the order of minutes ( Burt et al., 1976 ; Maeno, 1982 ; Nishikori et al., 1980 ; Sano et al., 1979 ).

Instead, we based our receptor kinetics on newer pharmacological experiments in live cells ( Ågren et al., 2021 ) and properties of the recently developed DA receptor-based biosensors ( Labouesse and Patriarchi, 2021 ), whose receptor values match well despite different methodological approaches.

The biosensors are mutated receptors whose kinetics may not be identical to the endogenous receptors, but only the intracellular domains are altered, with no apparent changes of the binding site ( Labouesse and Patriarchi, 2021 ).

Indeed, these biosensors exhibit kinetics that are well aligned with both modelled and experimentally reported extracellular DA dynamics using non-biosensor-based methods ( Atcherley et al., 2015 ; Gonon et al., 2000 ; Venton et al., 2002 ).

We believe accordingly that our updated parameters are more accurate portrayals of in vivo conditions; however, as shown throughout the study, the affinity values greatly affect the results.

Therefore, we find it important that our model will be available to the research community, allowing others to test their own estimates of receptor kinetics and assess their impact on the model’s behaviour.

The presented simulations suggested that receptor binding was largely invariant to single release events during pacemaker activity, while bursts of activity rapidly changed occupancy.

Both D1R and D2R immediately responded to burst onset; however, while D1R occupancy rapidly declined to zero within approximately 50 ms, the slow D2R kinetics resulted in an occupancy decline over ~5 s, returning to the baseline maintained by tonic firing.

This means that D1R is better suited to discriminate inputs in rapid succession and allow for postsynaptic decoding of the fast-paced in vivo dynamics described particularly for DS ( Ejdrup et al., 2023 ; Jørgensen et al., 2023 ; Markowitz et al., 2023 ).

By contrast, our analysis shows that D2Rs integrate DA signals over several seconds.

As D1R occupancy is negligible during pacemaker activity and D2R kinetics are too slow to pick up rapid changes in DA concentration, our simulations moreover suggest pauses in firing of less than 1 s are not an effective way of signalling for the striatal dopaminergic system.

Notably, this finding was apparent even when the D2 affinity was increased an order of magnitude.

This challenges the effectiveness of proposed negative reward prediction errors, as even a long pause in firing would have a limited effect on D2 receptor occupation and downstream signalling.

This may explain why DA drops during reward omissions are not nearly as prominent as positive signals ( Farrell et al., 2022 ; Greenstreet et al., 2025 ).

In conclusion, we have developed a three-dimensional model for DA release dynamics and receptor binding that integrates a wealth of experimentally determined parameters and generates responses to electrical and pharmacological input that fits robustly with literature observations.

The model offers an important theoretical framework and a predictive tool that can serve as the basis for future experimental endeavours and help guide the interpretation of new as well as older empirical findings on DA signalling dynamics under both physiological conditions and in disease.


## captions

=== Figure 1 === Figure 1. Large-scale 3D model of the dorsal striatum.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{=== Figure 1 === Figure 1. Large-scale 3D model of the dorsal striatum.} d1r-tracks-da-50ms-delay⟧

( A ) Self-enveloped simulation space of 100 µm 3 with approximately 40,000 release sites from 150 neurons.

Colours of individual release sites are not matched to neurons.

( B ) Simulation of a single release event after 5 ms and 10 ms. Colour-coded by DA concentration.

( C ) Comparison of analytical solution and simulation of diffusion after a single release event at three different time points.

( D ) Representative snapshot of steady state DA dynamics at 4 Hz tonic firing with parameters mirroring the dorsal striatum.

( E ) Cross-section of temporal dynamics for a midway section through the simulation space shown in ( d ).

( F ) Histogram of DA concentrations ([DA]) across the entire space in ( d ).

( G ) DA release during three burst activity scenarios for all release sites in a 10 x 10 × 10 µm cube (black boxes) and spill-over into the surrounding space.

Burst simulated as an increase in firing rate on top of continued tonic firing of the surrounding space.

Traces on top are average DA concentrations for the marked cubes, with bursts schematised by coloured lines below.

The first image row is at the end of the burst, and the second row is 100 ms after.

Scale bars for traces are 200 ms and 500 nM.

Scale bar for the images is 20 µm.

( H ) Top: representative [DA] trace for a voxel with a release site during pacemaker and burst activity.

Bottom: Occupancy of D1Rs and D2Rs for the same site.

( I ) Zoom on a DA burst as in ( h ), with [DA] in blue and D1R occupancy in teal with line style indicating different affinities.

The shaded area indicates the period of bursting with 6 APs at 20 Hz.

( J ) Effect of complete pause in firing for 1 s on both average [DA] and D1R and D2R occupation.

Figure 1—source code 1. Source code used to generate data in A, D, E, and F. Figure 1—source code 2. Source code used to generate data in B and C. Figure 1—source code 3. Source code used to generate data in G. Figure 1—source code 4. Source code used to generate data in J. Figure 1—source code 5. Source code used to generate data in H. Figure 1—source code 6. Source code used to generate data in I. [panels detected: a, b, c, d, e, f, g, h, i, j] === Figure 1s1 === Figure 1—figure supplement 1. Average concentration and receptor kinetics.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{Figure 1—source code 1. Source code used to generate data in A, D, E, and F. Figure 1—source code 2. Source code used to generate data in B and C. Figure 1—source code 3. Source code used to generate data in G. Figure 1—source code 4. Source code used to generate data in J. Figure 1—source code 5. Source code used to generate data in H. Figure 1—source code 6. Source code used to generate data in I. [panels detected: a, b, c, d, e, f, g, h, i, j] === Figure 1s1 === Figure 1—figure supplement 1. Average concentration and receptor kinetics.} d1r-tracks-da-50ms-delay⟧

( A ) Average DA concentration across a 100 x 100 × 100 µm volume of simulated DS at pacemaker activity.⟦>zach claim=gap: @{( A ) Average DA concentration across a 100 x 100 × 100 µm volume of simulated DS at pacemaker activity.} No claim records what the volume-averaged DA concentration in DS looks like during pacemaker activity, only how the spatial distribution is structured.⟧

( B ) Mean concentration change in response to a single event with 60% release probability (see supplementary notes on electrical stimulation) in all neurons at time zero.⟦>zach claim=gap: @{( B ) Mean concentration change in response to a single event with 60% release probability (see supplementary notes on electrical stimulation) in all neurons at time zero.} The simulated mean response to a single synchronous release event is a result no claim in the tree states.⟧

Blue trace is output directly from simulation, grey trace is the predicted FSCV measurement.

( C ) Modelling of predicted FSCV measurement and representative snapshot of simulation space just after a release event.⟦>zach claim=gap: @{( C ) Modelling of predicted FSCV measurement and representative snapshot of simulation space just after a release event.} The model's predicted FSCV signal for a single release event is not recorded by any claim; the tree's FSCV claim covers only the 10/30/60 Hz May and Wightman replication.⟧

( D ) Peak DA concentration reached at different distances from the area with phasic activity for the three firing scenarios.⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{( D ) Peak DA concentration reached at different distances from the area with phasic activity for the three firing scenarios.} ds-lacks-pervasive-tonic-da⟧

( E ) Volume of space exposed to greater than 100 nM DA after firing relative to volume of space where terminals actively burst.⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{( E ) Volume of space exposed to greater than 100 nM DA after firing relative to volume of space where terminals actively burst.} ds-lacks-pervasive-tonic-da⟧

( F ) Least-squares fit linear regression of the dLight and GRAB DA sensors based on reported kinetics ( Labouesse and Patriarchi, 2021 ) and newest experimental characterisation of D2R ( Ågren et al., 2021 ).⟦>zach claim=2ac9b38d-8f72-436d-905a-b98b7e8dc3ba: @{( F ) Least-squares fit linear regression of the dLight and GRAB DA sensors based on reported kinetics ( Labouesse and Patriarchi, 2021 ) and newest experimental characterisation of D2R ( Ågren et al., 2021 ).} ds-lacks-pervasive-tonic-da⟧

Shaded areas indicate 95% C.I.

( G ) Top: representative [DA] trace for a voxel with a release site during pacemaker and a triple burst scenario (300 ms long bursts of 3 APs at 10 Hz, three times in a row with 300 ms in between).⟦>zach claim=961ce4c4-5809-4b6b-aaa4-c5f52373612c: @{( G ) Top: representative [DA] trace for a voxel with a release site during pacemaker and a triple burst scenario (300 ms long bursts of 3 APs at 10 Hz, three times in a row with 300 ms in between).} low-burst-no-spillover-high-burst-does⟧

Bottom: Occupancy of D1Rs and D2Rs for the same site.

( H ) Effect of complete pause in firing for 1 s on both average [DA] and D2R occupation at different affinities.⟦>zach claim=2ec8fd67-7f5e-432f-b400-4e608348a74e: @{( H ) Effect of complete pause in firing for 1 s on both average [DA] and D2R occupation at different affinities.} d1r-tracks-da-50ms-delay⟧

Figure 1—figure supplement 1—source code 1. Source code used to generate data in Figure 1—figure supplement 1 .⟦>zach claim=no-assertion: @{Figure 1—figure supplement 1—source code 1. Source code used to generate data in Figure 1—figure supplement 1 .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

[panels detected: a, b, c, d, e, f, g, h] === Figure 1s2 === Figure 1—figure supplement 2. Simulation size and granularity.⟦>zach claim=no-assertion: @{[panels detected: a, b, c, d, e, f, g, h] === Figure 1s2 === Figure 1—figure supplement 2. Simulation size and granularity.} A bare figure-supplement title with its panel list.⟧

( A ) Schematic of different simulation sizes.⟦>zach claim=no-assertion: @{( A ) Schematic of different simulation sizes.} A schematic of the simulation geometry illustrates the setup rather than reporting a result.⟧

( B ) Concentration percentiles at different simulation diameters.⟦>zach claim=gap: @{( B ) Concentration percentiles at different simulation diameters.} The convergence of concentration percentiles with simulation diameter is a validation result no claim in the tree captures.⟧

Results are not robust until a diameter close to 50 µm is reached (line runs behind 100 µm line).

( C ) Schematic of simulation granularity.⟦>zach claim=no-assertion: @{( C ) Schematic of simulation granularity.} A schematic of voxel granularity illustrates the setup rather than reporting a result.⟧

( D ) Effect of simulation voxel diameter on concentration percentiles.⟦>zach claim=gap: @{( D ) Effect of simulation voxel diameter on concentration percentiles.} The effect of voxel size on the concentration profile is a discretisation result the claim tree never states.⟧

Virtually no difference in concentration profiles below the 99.9 th percentile of [DA], with the 1.0 µm voxel size still following 0.1 and 0.5 µm well above that level.

The inset shows 99.75 th to 100 th percentile with y-axis matching main y-axis.

( E ) Absolute difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.⟦>zach claim=gap: @{( E ) Absolute difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.} The absolute error introduced by coarser voxels is a validation result absent from the claim tree.⟧

The inset shows 99 th to 100 th percentile with y-axis matching main y-axis.

( F ) Percentage difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.⟦>zach claim=gap: @{( F ) Percentage difference in [DA] between simulations at 0.1 µm voxel diameter and 0.5, 1.0, and 2.0 µm.} The percentage error introduced by coarser voxels is a validation result absent from the claim tree.⟧

Figure 1—figure supplement 2—source code 1. Source code used to generate data in Figure 1—figure supplement 2 .⟦>zach claim=no-assertion: @{Figure 1—figure supplement 2—source code 1. Source code used to generate data in Figure 1—figure supplement 2 .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

[panels detected: a, b, c, d, e, f] === Figure 2 === Figure 2. Regional differences in uptake greatly impact DA dynamics.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{[panels detected: a, b, c, d, e, f] === Figure 2 === Figure 2. Regional differences in uptake greatly impact DA dynamics.} d2r-occupancy-higher-in-vs⟧

( A ) Representative snapshots of steady state dynamics at 4 Hz tonic firing with parameters mirroring the dorsal (left) and ventral striatum (right).⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( A ) Representative snapshots of steady state dynamics at 4 Hz tonic firing with parameters mirroring the dorsal (left) and ventral striatum (right).} vs-maintains-pervasive-tonic-da — These side-by-side steady-state snapshots are the regional contrast the claim states, diffuse coverage in VS against hotspots in DS.⟧

( B ) Cross-section of temporal dynamics for data shown in a.⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( B ) Cross-section of temporal dynamics for data shown in a.} vs-maintains-pervasive-tonic-da — The temporal cross-section shows the same DS-VS contrast in tonic coverage that the claim records.⟧

The bottom row shows concentrations of the dashed lines in the top panels.

( C ) Normalised density of DA concentration of simulations in ( a ).⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( C ) Normalised density of DA concentration of simulations in ( a ).} vs-maintains-pervasive-tonic-da — The concentration density distributions are how the claim's diffuse-versus-segregated contrast is quantified.⟧

Thick lines are for the entire space, and thin lines are across time for five randomly sampled locations.

Dashed red line is for simulation of the ventral striatum with lowest reported innervation density in the literature.

( D ) Same data as in ( c ), but for concentration percentiles.⟦>zach claim=897a3449-e5bd-4f12-99f2-e701f5989c74: @{( D ) Same data as in ( c ), but for concentration percentiles.} vs-lowest-percentiles-above-10nm — This is the percentile panel on which the claim that even the lowest VS percentiles exceed 10 nM rests.⟧

Note that even the lowest percentiles of VS were above 10 nM in [DA].

( E ) Convolved model response (Figure S1c) to mimic FSCV measurements mirroring the experimentally tested stimulation paradigm in May and Wightman, 1989 for the dorsal (left) and ventral striatum (right) ( F ) DA release during three burst activity scenarios for all release sites in a 10 x 10 × 10 µm cube (black boxes) and spill-over into the surrounding space.⟦>zach claim=cc992651-67bd-4d1b-9237-fa13d9f9ec94: @{( E ) Convolved model response (Figure S1c) to mimic FSCV measurements mirroring the experimentally tested stimulation paradigm in May and Wightman, 1989 for the dorsal (left) and ventral striatum (right) ( F ) DA release during three burst activity scenarios for all release sites in a 10 x 10 × 10 µm cube (black boxes) and spill-over into the surrounding space.} fscv-matches-may-wightman-1989 — The first half is the May and Wightman replication the claim states; the burst-spillover half is covered by low-burst-no-spillover-high-burst-does.⟧

Burst simulated as an increase in firing rate on top of continued tonic firing of the surrounding space.

Traces on top are average DA concentrations for the marked cubes, with bursts schematised by coloured lines below.

The first image row is at the end of the burst, and the second row is another 100 ms after.

Scale bars for traces are 200 ms and 500 nM.

Scale bar for the images is 20 µm.

( G ) Top: representative [DA] trace 1 µm away from a release site during pacemaker and burst activity.⟦>zach claim=gap: @{( G ) Top: representative [DA] trace 1 µm away from a release site during pacemaker and burst activity.} The VS DA time course near a release site through pacemaker and burst firing is displayed here, but the tree's claim for this panel concerns only D2R occupancy levels.⟧

Bottom: Occupancy of D1Rs and D2Rs for the same site.

Occupancy data from the corresponding DS simulation on Figure 1k shown as a dotted line.

( H ) Peak occupancy at different distances from the area bursting, normalised to maximal and minimum occupancy.⟦>zach claim=gap: @{( H ) Peak occupancy at different distances from the area bursting, normalised to maximal and minimum occupancy.} How peak receptor occupancy falls off with distance from the bursting region is a result no claim in the tree states.⟧

Figure 2—source code 1. Source code used to generate data in A-F.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{Figure 2—source code 1. Source code used to generate data in A-F.} d2r-occupancy-higher-in-vs⟧

Figure 2—source code 2. Source code used to generate data in G and H. [panels detected: a, b, c, d, e, f, g, h] === Figure 2s1 === Figure 2—figure supplement 1. Histochemical gradient of DAT and VMAT2 fluorescence.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{Figure 2—source code 2. Source code used to generate data in G and H. [panels detected: a, b, c, d, e, f, g, h] === Figure 2s1 === Figure 2—figure supplement 1. Histochemical gradient of DAT and VMAT2 fluorescence.} d2r-occupancy-higher-in-vs⟧

( A ) Representative image of the mouse striatal slices analysed in B. Dashed white line indicates the quantified dorsoventral gradient (length 2 mm).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{( A ) Representative image of the mouse striatal slices analysed in B. Dashed white line indicates the quantified dorsoventral gradient (length 2 mm).} ds-vs-vmax-ratio-assumed⟧

( B ) Relative intensity of the DAT and VMAT2 immunosignal in the dorsoventral axis of striatal mouse brain slices from Sørensen et al., 2021 .⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( B ) Relative intensity of the DAT and VMAT2 immunosignal in the dorsoventral axis of striatal mouse brain slices from Sørensen et al., 2021 .} vs-maintains-pervasive-tonic-da⟧

All slices show a drop at the anterior commissure (AC).⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{All slices show a drop at the anterior commissure (AC).} ds-vs-vmax-ratio-assumed⟧

Shaded areas around lines denote S.E.M.

( C ) Mean relative intensity of the DAT and VMAT2 signal before and after AC.⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( C ) Mean relative intensity of the DAT and VMAT2 signal before and after AC.} vs-maintains-pervasive-tonic-da⟧

Two-sided t-test, VS-DAT:VMAT2, p=0.012(*), n=4 mice; one-sided t-tests, DAT-DS:VS, p=0.0021(**), VMAT2-DS:VS, p=0.0086(**), n=4 mice.⟦>zach claim=498bf1d1-2d0f-42d4-bdf7-c9996ed5af78: @{Two-sided t-test, VS-DAT:VMAT2, p=0.012(*), n=4 mice; one-sided t-tests, DAT-DS:VS, p=0.0021(**), VMAT2-DS:VS, p=0.0086(**), n=4 mice.} dat-clustering-greater-in-vs⟧

( D ) Peak DA concentration reached at different distances from area with phasic activity for the three firing scenarios in VS. ( E ) Volume of space in VS exposed to greater than 100 nM after firing relative to volume of space where terminals actively burst.⟦>zach claim=897a3449-e5bd-4f12-99f2-e701f5989c74: @{( D ) Peak DA concentration reached at different distances from area with phasic activity for the three firing scenarios in VS. ( E ) Volume of space in VS exposed to greater than 100 nM after firing relative to volume of space where terminals actively burst.} vs-lowest-percentiles-above-10nm⟧

( F ) Effect of complete pause in firing in VS for 1 s on both average [DA] and D1R and D2R occupation.⟦>zach claim=gap: @{( F ) Effect of complete pause in firing in VS for 1 s on both average [DA] and D1R and D2R occupation.} The effect of a one-second pause in VS is unclaimed; the pause claim in the tree concerns the dorsal striatum only.⟧

[panels detected: a, b, c, d, e, f] === Figure 3 === Figure 3. Sensitivity of the model to parameter changes.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{[panels detected: a, b, c, d, e, f] === Figure 3 === Figure 3. Sensitivity of the model to parameter changes.} vmax-only-parameter-driving-regional-difference⟧

( A ) Schematic of the fraction of active release sites.⟦>zach claim=c3130ba5-465d-4f1a-a851-6796e72a1d72: @{( A ) Schematic of the fraction of active release sites.} ds-vs-vmax-ratio-assumed⟧

Black dots are inactive sites, and green dots indicate actively releasing sites.

( B ) Effect of changing fraction of active release sites on DA concentrations.⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( B ) Effect of changing fraction of active release sites on DA concentrations.} vs-maintains-pervasive-tonic-da⟧

Blue line, DS peak DA concentration (99.5 th percentile); Red line, VS peak DA concentration (99.5 th percentile); Dotted blue line, DS tonic DA concentration (50 th percentile); Dotted red line, VS tonic DA concentration (50 th percentile).

( C ) Ratio between peak (99.5 th percentile) and tonic (50 th percentile) concentrations across fractions of active release sites in the DS (blue line) and VS (red line) as a measure of DA signal focality.⟦>zach claim=1ef1d1ae-1c10-4951-bd72-5fe9e3df202d: @{( C ) Ratio between peak (99.5 th percentile) and tonic (50 th percentile) concentrations across fractions of active release sites in the DS (blue line) and VS (red line) as a measure of DA signal focality.} vs-maintains-pervasive-tonic-da⟧

( D ) Schematic of changing quantal size ( Q ).⟦>zach claim=897a3449-e5bd-4f12-99f2-e701f5989c74: @{( D ) Schematic of changing quantal size ( Q ).} vs-lowest-percentiles-above-10nm⟧

( E ) Effect of changing quantal size on tonic and peak DA concentrations in DS (blue lines) and VS (red lines).⟦>zach claim=cc992651-67bd-4d1b-9237-fa13d9f9ec94: @{( E ) Effect of changing quantal size on tonic and peak DA concentrations in DS (blue lines) and VS (red lines).} fscv-matches-may-wightman-1989⟧

( F ) Ratio between peak and tonic concentrations across various quantal sizes in in DS (blue line) and VS (red line).⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( F ) Ratio between peak and tonic concentrations across various quantal sizes in in DS (blue line) and VS (red line).} vmax-only-parameter-driving-regional-difference — The claim records that quantal size shifts both regions alike, which is what this peak-to-tonic ratio across quantal sizes shows.⟧

( G ) Relative difference between the DS and VS for peak (black line) and tonic DA (dotted line) at different quantal sizes.⟦>zach claim=db68e131-734a-4471-a7e6-e027f38048ac: @{( G ) Relative difference between the DS and VS for peak (black line) and tonic DA (dotted line) at different quantal sizes.} d2r-occupancy-higher-in-vs⟧

( H ) Schematic of changing DAT K m .⟦>zach claim=no-assertion: @{( H ) Schematic of changing DAT K m .} A schematic of the swept parameter, asserting nothing about the world.⟧

( i ) Effect of changing DAT K m on DA concentrations in DS (blue lines) and VS (red lines).

( J ) Schematic of changing DAT V max .

( K ) Effect of changing DAT V max on DA concentrations.

Shaded areas are median V max of the two regions (DS and VS) as found in the literature shown in Appendix 2—table 2 ± 50%.⟦>zach claim=no-assertion: @{Shaded areas are median V max of the two regions (DS and VS) as found in the literature shown in Appendix 2—table 2 ± 50%.} This explains what the shaded band on the plot represents.⟧

( L ) Effect of changing DAT V max , with tonic (50 th percentile) and peak (99.5 th percentile) DA concentrations normalised to their value at 2 µm s –1 (median value for VS).

The shaded area indicates median V max for VS found in the literature shown in Appendix 2—table 2 ± 50%.⟦>zach claim=no-assertion: @{The shaded area indicates median V max for VS found in the literature shown in Appendix 2—table 2 ± 50%.} This explains what the shaded band on the plot represents.⟧

Figure 3—source code 1. Source code used to generate data in B, C, E-G. Figure 3—source code 2. Source code used to generate data in I. Figure 3—source code 3. Source code used to generate data in K and L. [panels detected: a, b, c, d, e, f, g, h, i, j, k, l] === Figure 3s1 === Figure 3—figure supplement 1. Model parameter testing.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{Figure 3—source code 1. Source code used to generate data in B, C, E-G. Figure 3—source code 2. Source code used to generate data in I. Figure 3—source code 3. Source code used to generate data in K and L. [panels detected: a, b, c, d, e, f, g, h, i, j, k, l] === Figure 3s1 === Figure 3—figure supplement 1. Model parameter testing.} vmax-only-parameter-driving-regional-difference⟧

( A ) Schematic of our definitions of tonic (50 th percentile/median, dashed lines) and peak (99.5 th percentile, solid line) DA for both the dorsal and ventral striatum.⟦>zach claim=no-assertion: @{( A ) Schematic of our definitions of tonic (50 th percentile/median, dashed lines) and peak (99.5 th percentile, solid line) DA for both the dorsal and ventral striatum.} A schematic defining the tonic and peak percentile conventions and their line styles.⟧

( B ) Effect of changing release probability (R % ) on DA concentrations.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( B ) Effect of changing release probability (R % ) on DA concentrations.} vmax-only-parameter-driving-regional-difference⟧

( C ) Relative difference between the ventral and dorsal striatum at different percentiles for different release probabilities.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( C ) Relative difference between the ventral and dorsal striatum at different percentiles for different release probabilities.} vmax-only-parameter-driving-regional-difference⟧

( D ) Ratio between 99.5 th and 50 th percentiles as a measure of focality for both regions.⟦>zach claim=gap: @{( D ) Ratio between 99.5 th and 50 th percentiles as a measure of focality for both regions.} The focality ratio between regions under the release-probability sweep is displayed here but no claim states how focality itself behaves.⟧

As R % increases, the concentrations become more homogeneous.

( E ) Effect of changing firing rate on DA concentrations.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( E ) Effect of changing firing rate on DA concentrations.} vmax-only-parameter-driving-regional-difference⟧

( F ) Relative difference between the ventral and dorsal striatum at different percentiles for different firing rates.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( F ) Relative difference between the ventral and dorsal striatum at different percentiles for different firing rates.} vmax-only-parameter-driving-regional-difference⟧

( G ) Ratio between 99.5 th and 50 th percentiles for both regions.⟦>zach claim=1e689f9b-1bf5-4abd-98b9-daa3af67c795: @{( G ) Ratio between 99.5 th and 50 th percentiles for both regions.} vmax-only-parameter-driving-regional-difference⟧

As the firing rate increases, the concentrations become more homogeneous.

Figure 3—figure supplement 1—source code 1. Source code used to generate data in Figure 3—figure supplement 1 .⟦>zach claim=no-assertion: @{Figure 3—figure supplement 1—source code 1. Source code used to generate data in Figure 3—figure supplement 1 .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

[panels detected: a, b, c, d, e, f, g] === Figure 3s2 === Figure 3—figure supplement 2. Fold change during inhibition, V max -sensitivity at different release parameters and release-uptake balance.⟦>zach claim=no-assertion: @{[panels detected: a, b, c, d, e, f, g] === Figure 3s2 === Figure 3—figure supplement 2. Fold change during inhibition, V max -sensitivity at different release parameters and release-uptake balance.} A bare figure-supplement title with its panel list.⟧

( A ) Fold change over baseline (K m of 210 nM) for mean DA concentration in the dorsal (DS) and ventral striatum (VS) with changing DAT K m .⟦>zach claim=gap: @{( A ) Fold change over baseline (K m of 210 nM) for mean DA concentration in the dorsal (DS) and ventral striatum (VS) with changing DAT K m .} The Km sweep is unclaimed: the tree's parameter-sweep claim covers active fraction, quantal size, release probability, firing rate and Vmax, but not DAT affinity.⟧

( B ) Relative difference between the dorsal and ventral striatum for both phasic and tonic DA at different K m values.⟦>zach claim=gap: @{( B ) Relative difference between the dorsal and ventral striatum for both phasic and tonic DA at different K m values.} How the regional difference in phasic and tonic DA varies with Km is a result no claim records.⟧

( C ) Effect of changing DAT V max on DA concentrations for three different quantal sizes ( Q ).⟦>zach claim=gap: @{( C ) Effect of changing DAT V max on DA concentrations for three different quantal sizes ( Q ).} That the Vmax effect is unchanged across quantal sizes is a robustness result no claim in the tree states.⟧

[DA] normalised to highest values within each Q. Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.⟦>zach claim=no-assertion: @{[DA] normalised to highest values within each Q. Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.} This explains the normalisation and the shaded band used in the plot.⟧

( D ) Effect of changing DAT V max on DA concentrations for three different release probabilities (R % ).⟦>zach claim=gap: @{( D ) Effect of changing DAT V max on DA concentrations for three different release probabilities (R % ).} That the Vmax effect is unchanged across release probabilities is a robustness result no claim in the tree states.⟧

[DA] normalised to highest values within each R % .

Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.⟦>zach claim=no-assertion: @{Shaded area indicates median V max for DS and VS as found in the literature shown in Appendix 2—table 2 with ±50%.} This explains what the shaded band on the plot represents.⟧

( E ) Least-square fit linear regression between release rate and autocorrelation decay rate (τ) ( Ejdrup et al., 2023 ).⟦>zach claim=gap: @{( E ) Least-square fit linear regression between release rate and autocorrelation decay rate (τ) ( Ejdrup et al., 2023 ).} The regression between release rate and autocorrelation decay from the reanalysed photometry data is a result no claim records.⟧

Shaded area highlights 95% C.I.

( F ) Partial regression plot error of the regression in ( f ) and error between DA response to amphetamine as measured by microdialysis and the release rate from Ejdrup et al., 2023 to show that the less release and uptake correlate, the less release rate can explain the microdialysis response, suggesting release and uptake are partially independent of each other.⟦>zach claim=gap: @{( F ) Partial regression plot error of the regression in ( f ) and error between DA response to amphetamine as measured by microdialysis and the release rate from Ejdrup et al., 2023 to show that the less release and uptake correlate, the less release rate can explain the microdialysis response, suggesting release and uptake are partially independent of each other.} The inference that release and uptake vary partially independently across animals is asserted here but appears in no claim.⟧

Shaded area highlights 95% C.I.

Figure 3—figure supplement 2—source code 1. Source code used to generate data in Figure 3—figure supplement 2A-D .⟦>zach claim=no-assertion: @{Figure 3—figure supplement 2—source code 1. Source code used to generate data in Figure 3—figure supplement 2A-D .} A pointer to the source code, asserting nothing about dopamine dynamics.⟧

[panels detected: a, b, c, d, e, f] === Figure 4 === Figure 4. DAT nanoclustering reduces uptake and shows regional variation.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{[panels detected: a, b, c, d, e, f] === Figure 4 === Figure 4. DAT nanoclustering reduces uptake and shows regional variation.} dat-nanoclustering-slows-clearance⟧

( A ) Schematic of dense DA cluster.⟦>zach claim=no-assertion: @{( A ) Schematic of dense DA cluster.} A schematic of the modelled cluster geometry, asserting nothing about the world.⟧

White dots represent individual DAT molecules, and colour gradient the surrounding DA concentration.

( B ) Effective transport rate dependent on local concentration.⟦>zach claim=no-assertion: @{( B ) Effective transport rate dependent on local concentration.} This panel plots the assumed Michaelis-Menten dependence of uptake on concentration, a model ingredient rather than a finding.⟧

( C ) Top view of unfolded DA varicosity.⟦>zach claim=no-assertion: @{( C ) Top view of unfolded DA varicosity.} This describes the unfolded-varicosity view used to display the simulation, not a result.⟧

Black shapes denote clusters of DAT.

A dashed white line indicates placement of cross-section shown in ( d ).

( D ) Cross-section showing DA concentration in space surrounding varicosity unfolded in c.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( D ) Cross-section showing DA concentration in space surrounding varicosity unfolded in c.} dat-nanoclustering-slows-clearance — The cross-section shows the DA depletion around clustered transporters that the claim states.⟧

The grey line at the bottom is the surface of the varicosity.

Colour-coded for DA concentration.

( E ) Top view from ( c ), but colour coded for DA concentration immediately above membrane surface at different DAT cluster sizes.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( E ) Top view from ( c ), but colour coded for DA concentration immediately above membrane surface at different DAT cluster sizes.} dat-nanoclustering-slows-clearance — Surface DA concentration across cluster sizes is the depletion effect the claim records.⟧

( F ) Changes in [DA] from 15 nM unclustered (Un.) steady state with constant release after changing to four different cluster size scenarios (ø=diameter).⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( F ) Changes in [DA] from 15 nM unclustered (Un.) steady state with constant release after changing to four different cluster size scenarios (ø=diameter).} dat-nanoclustering-slows-clearance — The shift in steady-state DA on moving from unclustered to clustered DAT is the reduced effective uptake the claim describes.⟧

( G ) Clearance of 100 nM [DA] for different DAT cluster sizes.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( G ) Clearance of 100 nM [DA] for different DAT cluster sizes.} dat-nanoclustering-slows-clearance — This is the clearance comparison on which the claim's roughly 400 ms versus 200 ms result rests.⟧

( H ) Difference between DA concentration at the centre of clusters (or general surface of varicosity for unclustered) and mean concentration of the full simulation space ( I ) Concentrations across a cross section of a surface with 80 nm diameter clusters.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{( H ) Difference between DA concentration at the centre of clusters (or general surface of varicosity for unclustered) and mean concentration of the full simulation space ( I ) Concentrations across a cross section of a surface with 80 nm diameter clusters.} dat-nanoclustering-slows-clearance — The claim states this local depletion, that DA at the cluster surface falls far below the bulk concentration.⟧

Shaded areas highlight cluster locations.

( J ) Location of images of the dorsal (DS) and ventral striatum (VS) in striatal slices from mice as imaged in Sørensen et al., 2021 with direct stochastic optical reconstruction microscopy (dSTORM).

( K ) Two representative DA varicosities from DS and VS with VMAT2 in white and DAT in magenta.

Images are 1.5x2 µm (scale bar 0.5 µm).

( L ) Individual DAT localisations (locs.) from images in ( k ) coloured by clustering.

Black indicates localisation identified as clustered based on DBSCAN with parameters 80 nm diameter and 40 localisations.

Grey indicates unclustered localisations.

( M ) Quantification of clustering across all images in ( j ) with parameters in ( l ).

Welch’s two-sample t-test, p=0.012(*), n=12 (DS) and 13 (VS).⟦>zach claim=498bf1d1-2d0f-42d4-bdf7-c9996ed5af78: @{Welch’s two-sample t-test, p=0.012(*), n=12 (DS) and 13 (VS).} dat-clustering-greater-in-vs⟧

( N ) Absolute difference in percentage of clustering as assessed with DBSCAN across a range of parameters.

VS has a higher propensity to cluster across cluster sizes typically reported for DAT clusters.

Figure 4—source code 1. Source code for simulation.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4—source code 1. Source code for simulation.} dat-nanoclustering-slows-clearance⟧

Figure 4—source code 2. Source code used to generate data in A-E and G-I.⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4—source code 2. Source code used to generate data in A-E and G-I.} dat-nanoclustering-slows-clearance⟧

Figure 4—source code 3. Source code used to generate data in F. [panels detected: a, b, c, d, e, f, g, h, i, j, k, l, m, n]⟦>zach claim=dba3c7b4-0a96-48cb-97d4-9aca0edbe90f: @{Figure 4—source code 3. Source code used to generate data in F. [panels detected: a, b, c, d, e, f, g, h, i, j, k, l, m, n]} dat-nanoclustering-slows-clearance⟧


## tables

Table 1. List of variables used in the simulation of the dorsal striatum.⟦>zach claim=no-assertion: @{Table 1. List of variables used in the simulation of the dorsal striatum.} A table title introducing the parameter list.⟧

Variable Abbreviation Value Reference Firing rate 4 Hz Paladini et al., 2003 Release probability 6% Dreyer et al., 2010 DA molecules per vesicle 3000 Klaus et al., 2019 Diffusion coefficient 763 µm 2 s -1 Nicholson, 1995 Tortuosity 1.54 Rice and Nicholson, 1991 Vmax 6.0 µm s -1 See Appendix 2—table 2 Km 210 nM Hovde et al., 2019 Active terminal density - 0.04 µm -3 Liu et al., 2021 Extracellular volume fraction 0.21 Rice and Nicholson, 1991 Number of neurons in simulation space - 150 Matsuda et al., 2009 Key resources table Reagent type (species) or resource Designation Source or reference Identifiers Additional information Software, algorithm Python https://www.python.org v3.9.7 Software, algorithm Spyder IDE https://www.spyder-ide.org v5.1.5 Software, algorithm Model code https://github.com/GetherLab/striatal-dopamine-modelling Developed for this work Strain, strain background ( Mus musculus ) C57Bl/6 J Details provided in Sørensen et al., 2021 Data used are from Sørensen et al., 2021 Antibody anti-DAT Nt (rat monoclonal) Sigma-Aldrich MAB369 RRID: AB_2190413 IF (1:200) Sørensen et al., 2021 Antibody Anti-VMAT2 (rabbit polyclonal) Kind gift from Dr Gary W. Miller, Columbia University Sørensen et al., 2021 IF (1:4000) Sørensen et al., 2021 Appendix 2—table 1. Overview of reports on dopaminergic density and release in the striatum.⟦>zach claim=no-assertion: @{Variable Abbreviation Value Reference Firing rate 4 Hz Paladini et al., 2003 Release probability 6% Dreyer et al., 2010 DA molecules per vesicle 3000 Klaus et al., 2019 Diffusion coefficient 763 µm 2 s -1 Nicholson, 1995 Tortuosity 1.54 Rice and Nicholson, 1991 Vmax 6.0 µm s -1 See Appendix 2—table 2 Km 210 nM Hovde et al., 2019 Active terminal density - 0.04 µm -3 Liu et al., 2021 Extracellular volume fraction 0.21 Rice and Nicholson, 1991 Number of neurons in simulation space - 150 Matsuda et al., 2009 Key resources table Reagent type (species) or resource Designation Source or reference Identifiers Additional information Software, algorithm Python https://www.python.org v3.9.7 Software, algorithm Spyder IDE https://www.spyder-ide.org v5.1.5 Software, algorithm Model code https://github.com/GetherLab/striatal-dopamine-modelling Developed for this work Strain, strain background ( Mus musculus ) C57Bl/6 J Details provided in Sørensen et al., 2021 Data used are from Sørensen et al., 2021 Antibody anti-DAT Nt (rat monoclonal) Sigma-Aldrich MAB369 RRID: AB_2190413 IF (1:200) Sørensen et al., 2021 Antibody Anti-VMAT2 (rabbit polyclonal) Kind gift from Dr Gary W. Miller, Columbia University Sørensen et al., 2021 IF (1:4000) Sørensen et al., 2021 Appendix 2—table 1. Overview of reports on dopaminergic density and release in the striatum.} Raw parameter and key-resource rows: model inputs and reagents, not stated findings.⟧

Only studies that assessed both regions in rodents are included.

Studies that stimulate directly in the striatum are omitted due to the large activation of nicotinic receptors on DA terminals ( 1 , 2 ).

A.U.=arbitrary units, DS = dorsal striatum, VS=ventral striatum, TH = tyrosine hydroxylase.

Measure Ratio DS VS Units Species Source TH expression density 100 % ~90 ~90 A.U.

Mouse Alberquilla et al., 2020 TH immunoreactivity 95 % ~68 ~64 A.U.

Mouse Kuroda et al., 2010 TH protein content 150 % 0.07 0.11 ng TH/µg prot.

Mouse Salvatore et al., 2016 DA content 90 % ~155 ~140 ng DA/mg prot.

Mouse Salvatore et al., 2016 TH immunoreactivity 75 % 2.8 2.1 A.U.

Rat Huang et al., 2019 TH protein content 66 % 0.36 0.24 ng TH/µg prot.

Mouse Salvatore et al., 2005 FSCV - [DA] p 91 % 57 52 nM Rat May and Wightman, 1989 FSCV - [DA] p 76 % 89.3 67.5 nM Rat Garris and Wightman, 1994 Median 90 % - - - - - Appendix 2—table 2. Overview of reported V max values for DA uptake in the striatum.⟦>zach claim=no-assertion: @{Mouse Salvatore et al., 2005 FSCV - [DA] p 91 % 57 52 nM Rat May and Wightman, 1989 FSCV - [DA] p 76 % 89.3 67.5 nM Rat Garris and Wightman, 1994 Median 90 % - - - - - Appendix 2—table 2. Overview of reported V max values for DA uptake in the striatum.} Raw literature-survey rows; the medians they summarise are stated in the text and carried by the Vmax-ratio claims.⟧

Only studies that assessed both regions in rodents are included.

DS = dorsal striatum, VS=ventral striatum, FSCV = fast scan cyclic voltammetry.

Method VS/DS Ratio DS (uM/s) VS (uM/s) Species Source FSCV 29 % 7.0 2.0 Mouse Calipari et al., 2012 FSCV 28 % 6.0 1.7 Rat Calipari et al., 2012 FSCV 47 % 3.0 1.4 Rat May and Wightman, 1989 FSCV 31 % 6.5 2.0 Mouse Siciliano et al., 2014 FSCV 44 % 5.0 2.2 Rat Ferris et al., 2014 Median 31 % 6.0 2.0 - -
