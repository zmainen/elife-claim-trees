# Spatially targeted inhibitory rhythms differentially affect neuronal integration

<!-- headley-2026-inhibitory-rhythms · claim assignments as tika v2 notes · &#x27E6;&gt;author claim=KEY: @{span} what the claim says&#x27E7; · KEY is the claim's UUID, or `gap` (a result no claim accounts for), or `no-assertion` (the span states no result). An unmarked sentence carries no result and was never an obligation. -->


## abstract

Pyramidal neurons form dense recurrently connected networks with multiple types of inhibitory interneurons.

A major differentiator between interneuron subtypes is whether they synapse onto perisomatic or dendritic regions.

They can also engender local inhibitory rhythms, beta (12–35 Hz) and gamma (40–80 Hz).

The interaction between the rhythmicity of inhibition and its spatial targeting on the neuron may determine how it regulates neuronal integration.

Thus, we sought to understand how rhythmic perisomatic and distal dendritic inhibition impacted integration in a layer 5 pyramidal neuron model with realistic dendrites supporting Na + , NMDA, and Ca 2+ spikes.

We found that inhibition regulated the coupling between dendritic spikes and action potentials in a location and rhythm-dependent manner.

Perisomatic inhibition principally regulated action potential generation, while distal dendritic inhibition regulated the incidence of dendritic spikes and their temporal coupling with action potentials.

Perisomatic inhibition was most effective when provided at gamma frequencies, while distal dendritic inhibition functioned best at beta.

Moreover, beta modulated responsiveness to distal inputs in a phase-dependent manner, while gamma did so for proximal inputs.

These results may provide a functional interpretation for the reported association of soma-targeting parvalbumin-positive interneurons with gamma and dendrite-targeting somatostatin interneurons with beta.


## results

Results Construction of a model cortical L5 pyramidal neuron To study the effect of inhibitory rhythms on synaptic integration and somatic spiking, we adapted a previously published morphologically and biophysically detailed model of a cortical L5 pyramidal neuron ( Figure 1A ; see Methods for details).⟦>zach claim=5037933c-103b-4f19-992e-1abb330ea4f1: @{Results Construction of a model cortical L5 pyramidal neuron To study the effect of inhibitory rhythms on synaptic integration and somatic spiking, we adapted a previously published morphologically and biophysically detailed model of a cortical L5 pyramidal neuron ( Figure 1A ; see Methods for details).} l5-model-single-cell-scope⟧

Modifications to the model were done in accordance with the published literature.

In brief, this model featured a multicompartmental dendritic tree that produced dendritic Na + , NMDA, and Ca 2+ spikes, along with somatic action potentials that could backpropagate ( Figure 1B ).⟦>zach claim=gap: @{In brief, this model featured a multicompartmental dendritic tree that produced dendritic Na + , NMDA, and Ca 2+ spikes, along with somatic action potentials that could backpropagate ( Figure 1B ).} No claim in the tree records that the model itself reproduces all three classes of dendritic spike plus backpropagating action potentials.⟧

We distributed conductance-based synapses across the dendritic and somatic compartments with an average density of 2.16 excitatory and 0.22 inhibitory contacts per µm.

PreCSIUYX synaptic drivers of excitatory synapses were drawn from a pool of 5200 point process sources that emulated correlated afferent drive with 2–8 synaptic contacts from the same presynaptic neuron.

Inhibitory synapses were divided into two populations, those targeting the soma and proximal 100 µm of the dendrites (referred to as perisomatic) and those synapsing outside that area (referred to as distal).

To capture excitatory/inhibitory (E/I) balance, a hallmark of cortical activity, the rate of inhibitory synaptic drive was a rescaled version of the rate of excitatory drive, lagged by 4 ms to emulate feedforward inhibition.

Naturalistic presynaptic drive elicited a median firing rate of 5.3 Hz, in agreement with in vivo rates in cortex ( Figure 1A inset, Saiki et al., 2018 ).⟦>zach claim=5037933c-103b-4f19-992e-1abb330ea4f1: @{Naturalistic presynaptic drive elicited a median firing rate of 5.3 Hz, in agreement with in vivo rates in cortex ( Figure 1A inset, Saiki et al., 2018 ).} l5-model-single-cell-scope⟧

Figure 1. A model layer 5 pyramidal neuron with active dendrites.⟦>zach claim=5037933c-103b-4f19-992e-1abb330ea4f1: @{Figure 1. A model layer 5 pyramidal neuron with active dendrites.} l5-model-single-cell-scope⟧

( A ) The morphology of the neuron.⟦>zach claim=5037933c-103b-4f19-992e-1abb330ea4f1: @{( A ) The morphology of the neuron.} l5-model-single-cell-scope⟧

Virtual recordings can be obtained from any desired compartment (colored pipettes).

Inset, naturalistic presynaptic activity drives firing rates in our model like those in vivo.

Each black cross is the mean rate for a different simulation.

( B ) Examples of membrane potentials recorded simultaneously across the dendritic tree (in color) and soma (black) during naturalistic drive.⟦>zach claim=no-assertion: @{( B ) Examples of membrane potentials recorded simultaneously across the dendritic tree (in color) and soma (black) during naturalistic drive.} A panel label naming the example traces and their colour coding, not a finding.⟧

Regenerative events are indicated with arrows or text (AP: action potential, bAP: backpropagating action potential).

( C1–3 ) Demonstration of our detection of dendritic spike events (top) and characterization of their properties (bottom).

Events are binned according to the properties that were used in their detection.

Bin edges for the event durations were not evenly set for panels C2 and C3 .

Dendrites were endowed with the following voltage-dependent conductances: a fast-inactivating Na + current (I NaT ), muscarinic K + current (I m ), fast non-inactivating K + current (I Kv3.1 ), high voltage-activated Ca 2+ current (I Ca_HVA ), low voltage-activated Ca 2+ current (I Ca_LVA ), and Ca 2+ activated K + current (I SK ).

As a result, the basal and apical dendrites could generate Na + and NMDA spikes ( Figure 1B ; Goetz et al., 2021 ).⟦>zach claim=gap: @{As a result, the basal and apical dendrites could generate Na + and NMDA spikes ( Figure 1B ; Goetz et al., 2021 ).} That the model's basal and apical dendrites generate Na+ and NMDA spikes is asserted here but claimed nowhere in the tree.⟧

Dendritic Na + spikes were regenerative events lasting less than 1 ms that were not preceded by somatic action potentials ( Figure 1C1 ; Golding and Spruston, 1998 ).⟦>zach claim=gap: @{Dendritic Na + spikes were regenerative events lasting less than 1 ms that were not preceded by somatic action potentials ( Figure 1C1 ; Golding and Spruston, 1998 ).} The sub-millisecond, non-backpropagation-driven character of dendritic Na+ spikes is asserted here but no claim characterises the spike types the model produces.⟧

An Na + spike was detected when the dendritic Na + channel conductance (gNa) was higher than 0.3 mS/cm 2 , except when this threshold was reached within 5 ms after a somatic action potential, to distinguish from backpropagating action potentials.

NMDA spikes occur when adjacent NMDA-bearing synapses were synergistically recruited by a combination of glutamatergic activation and local depolarization ( Figure 1C2 ; Larkum et al., 2009 ; Schiller et al., 2000 ).⟦>zach claim=gap: @{NMDA spikes occur when adjacent NMDA-bearing synapses were synergistically recruited by a combination of glutamatergic activation and local depolarization ( Figure 1C2 ; Larkum et al., 2009 ; Schiller et al., 2000 ).} The generative conditions for NMDA spikes are asserted here, and the tree has no claim describing how the model's NMDA spikes arise.⟧

They typically lasted between 20 and 80 ms. They were detected when a compartment’s membrane voltage exceeded –40 mV for at least 26 ms and NMDA current exceeded –100 pA ms of charge.

Ca 2+ spikes are depolarizations generated at the nexus of the apical trunk upon activation of voltage-gated Ca 2+ channels ( Figure 1C3 ; Schiller et al., 1997 ; Larkum and Zhu, 2002 ).⟦>zach claim=gap: @{Ca 2+ spikes are depolarizations generated at the nexus of the apical trunk upon activation of voltage-gated Ca 2+ channels ( Figure 1C3 ; Schiller et al., 1997 ; Larkum and Zhu, 2002 ).} The nexus origin and Ca2+-channel basis of Ca2+ spikes is asserted here with no corresponding claim in the tree.⟧

They lasted between 20 and 50 ms. To detect them, the membrane potential must exceed –40 mV for at least 26 ms, and the combined Ca 2+ currents (LVA and HVA) had to be 1.3 times higher than when the voltage criterion was reached ( t v ).

The Ca 2+ spike ended when this value fell to 1.15 times its value at t v .

Altogether, under conditions that mirror in vivo afferent drive, our model reproduces the dendritic spikes of an L5 pyramidal neuron.

Relationship between dendritic and somatic spikes Dendritic spikes induced by synaptic activity are the principal drivers of somatic action potentials.

Prior experimental and modeling work has found this to be the case for L2/3 and L5 pyramidal neurons ( Goetz et al., 2021 ; Larkum et al., 2009 ; Smith et al., 2013 ; Helmchen et al., 1999 ; Xu et al., 2012 ).

L5 pyramidal neurons have a substantially longer apical trunk, which increases the electrotonic distance of their apical tuft from the soma ( Figure 2A ) and diminishes the ability of tuft synapses to elicit action potentials.⟦>zach claim=gap: @{L5 pyramidal neurons have a substantially longer apical trunk, which increases the electrotonic distance of their apical tuft from the soma ( Figure 2A ) and diminishes the ability of tuft synapses to elicit action potentials.} The long apical trunk of L5 neurons and its consequence for tuft-driven spiking is background the tree never states as a claim.⟧

Voltage-gated Ca 2+ channels at the apical nexus compensate for this by producing a robust Ca 2+ spike that drives a burst of action potentials at the soma ( Poirazi et al., 2003 ; Larkum et al., 2009 ).

Underscoring that Ca 2+ spikes compensate for morphology, pyramidal neurons with shorter apical dendrites have weaker Ca 2+ spikes that only elicit a single spike ( Fletcher and Williams, 2019 ; Gidon et al., 2020 ; Larkum et al., 2007 ).

We thus assessed how dendritic spikes at different electronic distances from the soma were related to action potential generation.

Figure 2. Influence of Na + and NMDA spikes on action potential generation.⟦>zach claim=9c3d1464-1a51-4381-a466-fcb1ca6fca65: @{Figure 2. Influence of Na + and NMDA spikes on action potential generation.} ca-spikes-couple-20ms-before-ap⟧

( A ) Electrotonic distance between each dendritic compartment and the soma.⟦>zach claim=no-assertion: @{( A ) Electrotonic distance between each dendritic compartment and the soma.} A bare panel label naming the quantity plotted.⟧

( B ) Dendritic compartments were grouped by their type (apical or basal) and electrotonic distance (percentile) from the soma.⟦>zach claim=no-assertion: @{( B ) Dendritic compartments were grouped by their type (apical or basal) and electrotonic distance (percentile) from the soma.} Describes how compartments were grouped for the analysis rather than stating a result.⟧

The percent change in Na + spike presence in those compartments relative to somatic spiking.

Na + spikes increased immediately prior to action potentials in dendritic compartments that were electrotonically close to the soma.

( C ) Same format as B , but for NMDA spikes.⟦>zach claim=no-assertion: @{( C ) Same format as B , but for NMDA spikes.} A bare panel label pointing to the format of an earlier panel.⟧

These showed a similar degree of change, but a broader temporal coupling.

Dendritic compartments differed in their degree of passive electrical coupling to the soma (i.e. electrotonic distance; Figure 2A ).⟦>zach claim=gap: @{Dendritic compartments differed in their degree of passive electrical coupling to the soma (i.e. electrotonic distance; Figure 2A ).} That the model's compartments differ systematically in electrotonic coupling to the soma is asserted here but not claimed anywhere.⟧

We measured this by injecting a 20 Hz sinusoidal current in each dendritic compartment and then calculating the ratio of the membrane voltage response at the soma over that at the dendrite.

The apical trunk exhibited a relatively small attenuation ratio of ~10%.

Progressing distally into the apical tuft, attenuation reached 0.1%.

Basal dendrites showed greater attenuation than the apical trunk due to their smaller diameter.

However, with an attenuation ratio reaching ~1%, their distal tips were still electrotonically closer than the apical tuft.

Thus, large and long-lasting changes in membrane potential, like those produced by dendritic spikes, would be required to have any effect on the soma.

We examined this by measuring the spike-triggered average between somatic action potentials and the presence of dendritic spikes across the dendritic tree.

To simplify the complex geometry of our model neuron, dendritic compartments were grouped into deciles by their electrotonic distance and whether they were on apical or basal branches.

For each time lag from the somatic action potential, we measured the percent change in dendritic spike incidence from the mean rate across the entire simulation.

Dendritic Na + spikes increased 2–3 ms prior to somatic action potentials in both basal and apical dendrites ( Figure 2B ).⟦>zach claim=fb9ac5da-3094-4370-b277-fe34853856b1: @{Dendritic Na + spikes increased 2–3 ms prior to somatic action potentials in both basal and apical dendrites ( Figure 2B ).} na-spikes-couple-2to3ms-before-ap — This is the 2-3 ms lead of dendritic Na+ spikes over somatic action potentials that the claim states.⟧

This relationship was strongest for the compartments nearest the soma, with the rate of Na + spikes in the apical trunk increasing 300% over baseline prior to somatic action potentials and 100% in basal compartments.

This relationship fell off as the dendritic spikes moved farther away from the soma, indicating that Na + spikes in distal branches had little direct influence on somatic spiking.

The incidence of NMDA spikes increased ~25 ms prior to somatic action potentials, much earlier than seen with dendritic Na + spikes ( Figure 2C ).⟦>zach claim=920d7adb-9ab1-4bc0-8185-de3e5de3a71e: @{The incidence of NMDA spikes increased ~25 ms prior to somatic action potentials, much earlier than seen with dendritic Na + spikes ( Figure 2C ).} nmda-spikes-couple-25ms-before-ap — This is the ~25 ms NMDA-spike lead over somatic action potentials that the claim states.⟧

But, like dendritic Na + spikes, NMDA spikes in the apical branch had a stronger coupling with somatic spiking than those in basal branches, and this effect dropped with distance from the soma.

NMDA spikes in the apical branch persisted after an action potential, while those in basal dendrites did not, potentially because of the action potential after-hyperpolarization.

Ca 2+ spikes originate at the nexus, when the apical trunk first branches into the apical tuft.

This region is electrotonically close to the entire apical trunk, facilitating the propagation of Ca 2+ spikes ( Figure 3A ).⟦>zach claim=gap: @{This region is electrotonically close to the entire apical trunk, facilitating the propagation of Ca 2+ spikes ( Figure 3A ).} The electrotonic proximity of the nexus to the apical trunk, and its role in Ca2+ spike propagation, is asserted here with no claim behind it.⟧

In our model, Ca 2+ spike occurrence increased within 20 ms of somatic action potentials ( Figure 3B ).⟦>zach claim=9c3d1464-1a51-4381-a466-fcb1ca6fca65: @{In our model, Ca 2+ spike occurrence increased within 20 ms of somatic action potentials ( Figure 3B ).} ca-spikes-couple-20ms-before-ap — This is the ~20 ms lead of nexus Ca2+ spikes over somatic action potentials that the claim states.⟧

Furthermore, we found that NMDA spikes in the apical dendrites tended to precede Ca 2+ spikes ( Figure 3C ).⟦>zach claim=gap: @{Furthermore, we found that NMDA spikes in the apical dendrites tended to precede Ca 2+ spikes ( Figure 3C ).} The ordering of apical NMDA spikes before Ca2+ spikes is a result with no claim in the tree.⟧

Our ionic current-based detection criteria distinguished between these phenomena despite their similar membrane voltage profiles.

Since NMDA spikes in the apical tuft normally have a weak relationship to somatic spiking ( Figure 2C ), they may elicit somatic spiking indirectly by driving Ca 2+ spikes.⟦>zach claim=gap: @{Since NMDA spikes in the apical tuft normally have a weak relationship to somatic spiking ( Figure 2C ), they may elicit somatic spiking indirectly by driving Ca 2+ spikes.} The proposal that tuft NMDA spikes drive somatic output indirectly, via Ca2+ spikes, is not stated by any claim.⟧

Put another way, the apical nexus may serve as a thresholded nonlinearity for NMDA spikes in the apical tuft to drive action potentials ( Larkum et al., 2009 ).

To test this, we measured how a Ca 2+ spike changed the spike-triggered average between apical tuft NMDA spikes and action potentials ( Figure 3D , top).⟦>zach claim=no-assertion: @{To test this, we measured how a Ca 2+ spike changed the spike-triggered average between apical tuft NMDA spikes and action potentials ( Figure 3D , top).} Narrates the analysis performed rather than reporting its outcome.⟧

This revealed that action potentials preceded by a Ca 2+ spike (by up to 20 ms) had increased coupling with apical NMDA spikes.

No such change was seen in basal dendrites ( Figure 3D , bottom).⟦>zach claim=gap: @{No such change was seen in basal dendrites ( Figure 3D , bottom).} The null result for basal dendrites is a reported finding that no claim accounts for.⟧

Figure 3. Influence of Ca 2+ spikes on action potential generation and their behavior as a second integrative mechanism.⟦>zach claim=9c3d1464-1a51-4381-a466-fcb1ca6fca65: @{Figure 3. Influence of Ca 2+ spikes on action potential generation and their behavior as a second integrative mechanism.} ca-spikes-couple-20ms-before-ap⟧

( A ) Electrotonic distance between dendritic compartments and the apical nexus, where Ca 2+ spikes are generated.⟦>zach claim=no-assertion: @{( A ) Electrotonic distance between dendritic compartments and the apical nexus, where Ca 2+ spikes are generated.} A bare panel label naming the quantity plotted.⟧

( B ) Change in the incidence of Ca 2+ spikes at the nexus surrounding action potentials.⟦>zach claim=no-assertion: @{( B ) Change in the incidence of Ca 2+ spikes at the nexus surrounding action potentials.} A bare panel label naming the quantity plotted.⟧

( C ) Percent change in NMDA spike presence in the apical dendrites centered on Ca 2+ spike initiation.⟦>zach claim=no-assertion: @{( C ) Percent change in NMDA spike presence in the apical dendrites centered on Ca 2+ spike initiation.} A bare panel label naming the quantity plotted.⟧

( D ) Percent change in NMDA spike coupling with action potentials during Ca 2+ spikes.⟦>zach claim=no-assertion: @{( D ) Percent change in NMDA spike coupling with action potentials during Ca 2+ spikes.} A bare panel label naming the quantity plotted.⟧

Top, NMDA spikes in apical dendrites were more strongly coupled with action potentials during Ca 2+ spikes.

Bottom, this was not the case for basal dendrites.

Effect of perisomatic and distal dendritic inhibition on controlling response gain Subtypes of inhibitory interneurons synapse on distinct dendritic zones.

PV interneurons mainly synapse perisomatically, while SOM interneurons target distal dendrites ( Kawaguchi and Kubota, 1997 ; Wang et al., 2004 ; Kubota, 2014 ; Kubota et al., 2015 ).

These differences may affect their modulation of synaptic integration ( Doiron et al., 2001 ), either by shifting the threshold for evoking action potentials (a subtractive effect) or altering the slope of the relationship between excitation and firing rate (a divisive effect).

There is some disagreement about the degree to which PV and SOM interneurons produce either of these effects ( Wilson et al., 2012 ; Lee et al., 2012 ; Atallah et al., 2012 ), depending on the source of excitation and local circuitry ( Seybold et al., 2015 ).

So, before we applied beta and gamma rhythmic inhibition in our model, we studied the effect of tonically activating PV- and SOM-like inhibitory synapses.

We doubled the rate of the inhibitory presynaptic drive onto either the PV-targeted perisomatic compartments (somatic and dendritic compartments within 100 µm) or the SOM-targeted distal (>100 µm) dendritic branches.

Both decreased the firing rate of the pyramidal cell from 5.5 Hz to less than 1 Hz ( Figure 4A ; control: 5.5±0.85 Hz; distal: 0.20±0.15 Hz; perisomatic: 0.70±0.31 Hz; mean ± SD).⟦>zach claim=26819b09-5b20-4c90-b9f3-8bdd29a2a57c: @{Both decreased the firing rate of the pyramidal cell from 5.5 Hz to less than 1 Hz ( Figure 4A ; control: 5.5±0.85 Hz; distal: 0.20±0.15 Hz; perisomatic: 0.70±0.31 Hz; mean ± SD).} distal-inhib-drops-firing-02hz — These are the control, distal and perisomatic firing rates the claim states, 5.5 Hz falling to 0.2 Hz under doubled distal inhibition.⟧

These comparable changes may reflect either subtractive or divisive effects and could derive from different mechanisms.

Figure 4. Distal dendritic and perisomatic inhibition reduce action potential generation through different mechanisms.⟦>zach claim=26819b09-5b20-4c90-b9f3-8bdd29a2a57c: @{Figure 4. Distal dendritic and perisomatic inhibition reduce action potential generation through different mechanisms.} distal-inhib-drops-firing-02hz⟧

( A ) Action potential rate during periods with normal inhibitory tone (control), double rate on distal branches, or double rate on perisomatic.⟦>zach claim=no-assertion: @{( A ) Action potential rate during periods with normal inhibitory tone (control), double rate on distal branches, or double rate on perisomatic.} A bare panel label naming the three conditions plotted.⟧

Both increases in inhibition dramatically reduced the firing of somatic action potentials.

( B ) Somatic excitability was measured by delivering current steps during the control, distal, and perisomatic inhibition states.⟦>zach claim=no-assertion: @{( B ) Somatic excitability was measured by delivering current steps during the control, distal, and perisomatic inhibition states.} Describes the current-step measurement used, not a result.⟧

Left, example somatic voltage responses to current steps.

Right, spike frequency versus current (f–I) curve for each condition.

The threshold for evoking an action potential shifted with 2× distal and perisomatic inhibition.

Perisomatic, but not dendritic, inhibition changed the f-I slope (compare dashed lines with solid black).

( C ) Impact of altered dendritic inhibition on rate of Na + spikes in apical and basal dendrites.⟦>zach claim=no-assertion: @{( C ) Impact of altered dendritic inhibition on rate of Na + spikes in apical and basal dendrites.} A bare panel label naming the quantity plotted.⟧

( D ) Same format as C , but for NMDA spikes.⟦>zach claim=no-assertion: @{( D ) Same format as C , but for NMDA spikes.} A bare panel label pointing to the format of an earlier panel.⟧

( E ) Rate of Ca 2+ spikes in the apical dendrites.⟦>zach claim=no-assertion: @{( E ) Rate of Ca 2+ spikes in the apical dendrites.} A bare panel label naming the quantity plotted.⟧

Basal dendrites lacked Ca 2+ spikes and were excluded.

All error bars are mean ± standard deviation.

( F ) Examples of membrane potential recorded in control (top), and both distal (middle) and proximal (bottom) inhibition lagged by 500 ms. ( G ) Change in firing rate for control (black dot) and for perisomatic (blue) and distal (red) lags in inhibition from 0 to 500 ms. ( H ) Change in incidence of Ca 2+ spikes for distal (red, top) and proximal (blue, bottom) inhibition.⟦>zach claim=no-assertion: @{( F ) Examples of membrane potential recorded in control (top), and both distal (middle) and proximal (bottom) inhibition lagged by 500 ms. ( G ) Change in firing rate for control (black dot) and for perisomatic (blue) and distal (red) lags in inhibition from 0 to 500 ms. ( H ) Change in incidence of Ca 2+ spikes for distal (red, top) and proximal (blue, bottom) inhibition.} Panel labels and their colour coding, stating no finding of their own.⟧

The control case is shown in black in both panels.

( I ) Same as ( H ) but for NMDA spikes.⟦>zach claim=no-assertion: @{( I ) Same as ( H ) but for NMDA spikes.} A bare panel label pointing to the format of an earlier panel.⟧

To isolate these factors, we first assessed how doubling inhibition affected action potential initiation at the soma.

A series of current pulses were injected into the soma to measure the relationship between firing rate and injected current (f-I curve), which captures the gain function of the neuron ( Figure 4B ).⟦>zach claim=no-assertion: @{A series of current pulses were injected into the soma to measure the relationship between firing rate and injected current (f-I curve), which captures the gain function of the neuron ( Figure 4B ).} Describes the f-I measurement procedure rather than its outcome.⟧

This revealed that both perisomatic and dendritic inhibition shifted the current threshold for action potential initiation.

Such an effect is subtractive.

In addition, perisomatic inhibition decreased the slope of the f-I relationship compared with the control, which is consistent with a divisive effect.

Although perisomatic inhibition produced the strongest subtractive effect, distal dendritic inhibition reduced firing rate the most ( Figure 4A ).⟦>zach claim=26819b09-5b20-4c90-b9f3-8bdd29a2a57c: @{Although perisomatic inhibition produced the strongest subtractive effect, distal dendritic inhibition reduced firing rate the most ( Figure 4A ).} distal-inhib-drops-firing-02hz — The claim's 0.2 Hz under distal versus 0.7 Hz under perisomatic inhibition is exactly this comparison of which manipulation cuts firing most.⟧

How can we reconcile these discordant findings?

One possibility is that distal inhibition substantially reduces Na + , NMDA, or Ca 2+ spikes.

To determine this, we examined the overall rate of dendritic spike events.

Perisomatic inhibition did not affect dendritic events compared to the control condition ( Figure 4C–E ).⟦>zach claim=27009c70-e2bf-49c1-81c5-2663096ca45b: @{Perisomatic inhibition did not affect dendritic events compared to the control condition ( Figure 4C–E ).} perisomatic-inhib-drops-firing-07hz — The claim states that perisomatic inhibition leaves dendritic spike rates relatively preserved, which is what this reports.⟧

By contrast, dendritic inhibition decreased NMDA and Ca 2+ spikes ( Figure 4D and E ).⟦>zach claim=26819b09-5b20-4c90-b9f3-8bdd29a2a57c: @{By contrast, dendritic inhibition decreased NMDA and Ca 2+ spikes ( Figure 4D and E ).} distal-inhib-drops-firing-02hz — The claim attributes the distal effect to suppression of Ca2+ and NMDA spikes, which is the decrease reported here.⟧

Na + spikes were relatively unaffected ( Figure 4C ).⟦>zach claim=gap: @{Na + spikes were relatively unaffected ( Figure 4C ).} No claim states that Na+ spike rates survive tonic distal inhibition, which matters because the rhythmic case later behaves differently.⟧

This lack of effect may arise from a shortening of the inactivation for voltage-gated Na + channels balancing out the loss of excitatory drive.

Distinct excitation/inhibition balance effects of perisomatic and distal dendritic inhibition The previous analysis found distinct effects on neuronal gain and dendritic spiking from tonic changes in perisomatic and distal dendritic inhibition.

But in vivo inhibition is dynamic and time-varying.

PV and SOM interneurons form dense interconnections with local pyramidal neurons, supplying time-lagged feedback inhibition.

This helps maintain the balance of excitation and inhibition (E/I) in the network by ensuring that an overall increase in excitatory activity is rapidly counterbalanced by proportionate inhibition.

To emulate situations where E/I balance is important, we increased the dynamic variation in excitatory drive (see Methods).

As with the previous simulations, the rate of inhibitory synaptic drive was a lagged and rescaled version of the overall excitation rate.

Normally, that lag is 4 ms, in line with experimental estimates ( Wehr and Zador, 2003 ).

To probe whether perisomatic or distal dendritic inhibition has distinct effects on E/I balance, we independently varied their lags ( Figure 4F–I ).⟦>zach claim=no-assertion: @{To probe whether perisomatic or distal dendritic inhibition has distinct effects on E/I balance, we independently varied their lags ( Figure 4F–I ).} States the purpose of the lag manipulation rather than any result.⟧

One was kept at the nominal 4 ms lag, while the other was extended.

Increasing either of their lags by 500 ms produced obvious differences in the emission of dendritic spikes and their coordination with action potentials ( Figure 4F ).⟦>zach claim=b88c89df-7f9c-4d11-9dc4-1ec829d6b413: @{Increasing either of their lags by 500 ms produced obvious differences in the emission of dendritic spikes and their coordination with action potentials ( Figure 4F ).} ei-lag-sensitivity-firing-rate — The claim that E-I lag reshapes dendritic spiking and its coupling to output is what this example illustrates.⟧

Normally, dendritic spikes are evenly distributed in time and drive somatic action potentials.

Lagging distal dendritic inhibition clustered dendritic spikes together in time, during which action potentials were emitted.

Lagging perisomatic inhibition did not affect the spacing of dendritic spikes but decreased their coupling with somatic spiking.

We systematically characterized these lag effects for the following spiking events modulated by tonic changes in inhibition: action potentials, Ca 2+ , and NMDA spikes ( Figure 4G ).⟦>zach claim=no-assertion: @{We systematically characterized these lag effects for the following spiking events modulated by tonic changes in inhibition: action potentials, Ca 2+ , and NMDA spikes ( Figure 4G ).} Lists which events were analysed, not what was found.⟧

Increasing the lag of perisomatic inhibition lowered action potential firing, while for distal dendritic inhibition, the firing rate decreased out to a lag of 125 ms and then returned to normal at 500 ms. To better understand these effects, we calculated the cross-correlation (CC) between dendritic spikes and action potentials.⟦>zach claim=gap: @{Increasing the lag of perisomatic inhibition lowered action potential firing, while for distal dendritic inhibition, the firing rate decreased out to a lag of 125 ms and then returned to normal at 500 ms. To better understand these effects, we calculated the cross-correlation (CC) between dendritic spikes and action potentials.} The non-monotonic lag profile, with distal suppression peaking near 125 ms and recovering by 500 ms, is a specific result the tree's lag claim does not capture.⟧

Increasing the lag decreased the coordination between Ca 2+ and somatic spikes ( Figure 4H ).⟦>zach claim=b88c89df-7f9c-4d11-9dc4-1ec829d6b413: @{Increasing the lag decreased the coordination between Ca 2+ and somatic spikes ( Figure 4H ).} ei-lag-sensitivity-firing-rate — Loss of Ca2+-to-soma coordination with increasing lag is the claim's point that timing reshapes dendritic contribution.⟧

For distal dendritic inhibition, this decrease was accompanied by a broadening of their temporal relationship, while a sharp temporal relationship was maintained in the perisomatic case.

A similar pattern was observed with NMDA spikes on apical branches ( Figure 4I ).

Basal branches, on the other hand, were relatively unaffected.

In summary, distal and perisomatic inhibition modulate the coupling between synaptic drive and spiking through distinct processes.

And while for both cases, the normal 4 ms E/I lag produced maximal conversion of dendritic spiking events into action potentials, extending this lag exerted distinct effects.

Effect of beta and gamma rhythmic inhibition on neuronal integration The mechanisms modulating neuronal responsiveness during tonic inhibition of somatic and dendritic compartments may extend to rhythmic inhibition.

Thus, we emulated beta and gamma rhythmic input ( Figure 5A and F ).⟦>zach claim=no-assertion: @{Thus, we emulated beta and gamma rhythmic input ( Figure 5A and F ).} Announces the simulation that follows rather than reporting a result.⟧

Depths of modulation were set to similarly entrain action potentials ( Figure 5B and G ) and were comparable to spontaneous and optogenetically induced gamma and beta bursts seen in vivo ( Amir et al., 2018 ; Onorato et al., 2020 ; Adesnik, 2018 ; Murthy and Fetz, 1992 ).⟦>zach claim=gap: @{Depths of modulation were set to similarly entrain action potentials ( Figure 5B and G ) and were comparable to spontaneous and optogenetically induced gamma and beta bursts seen in vivo ( Amir et al., 2018 ; Onorato et al., 2020 ; Adesnik, 2018 ; Murthy and Fetz, 1992 ).} The paper's parameterization claim covers synaptic drive but not this calibration of rhythm modulation depth against in vivo beta and gamma bursts.⟧

Beta rhythmic inhibition was modeled as a 16 Hz sinusoidally modulated rate (20% depth) of the Poisson processes driving inhibitory synapses.

Gamma rhythmic inhibition was a 64 Hz sinusoidal modulation (40%) of inhibitory synapses.

For both cases, excitatory synaptic drive was a stable Poisson process.

Figure 5. Phase-dependent effects of beta and gamma rhythmic inhibition on dendritic spikes.⟦>zach claim=bf7efeee-2819-485d-a06d-1fc3782ce66f: @{Figure 5. Phase-dependent effects of beta and gamma rhythmic inhibition on dendritic spikes.} beta-bidirectional-dendritic-control⟧

( A ) Example data from the beta rhythmic inhibition simulation.⟦>zach claim=no-assertion: @{( A ) Example data from the beta rhythmic inhibition simulation.} A bare panel label naming example data.⟧

Top, presynaptic spike counts.

Bottom, voltage traces from somatic and dendritic compartments.

Grayed periods are when inhibitory presynaptic spikes are peaking.

( B ) Action potential rate as a function of the phase of the beta rhythm.⟦>zach claim=no-assertion: @{( B ) Action potential rate as a function of the phase of the beta rhythm.} A bare panel label naming the quantity plotted.⟧

Dashed gray line shows the modulation of inhibitory drive with respect to phase.

( C ) Percent change in Ca 2+ spike presence at apical nexus by beta phase.⟦>zach claim=no-assertion: @{( C ) Percent change in Ca 2+ spike presence at apical nexus by beta phase.} A bare panel label naming the quantity plotted.⟧

( D1–2 ) Percent change of NMDA spike presence in apical (1) and basal (2) dendrites stratified by electronic distance from the soma.

( E1–2 ) Same as C , but for Na + spikes.

( F, G, H, I1–2, J1–2 ) Same format as above, but with events binned by the phase of gamma rhythmic inhibition.

For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. Figure 5—figure supplement 1. Phase-dependent effects on dendritic spikes of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.⟦>zach claim=no-assertion: @{For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. Figure 5—figure supplement 1. Phase-dependent effects on dendritic spikes of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.} States the phase convention used in the plots and repeats a figure title.⟧

Beta was delivered perisomatically, while gamma was supplied to the distal dendrites.

( A ) Action potential rate as a function of the phase of the beta rhythm.⟦>zach claim=no-assertion: @{( A ) Action potential rate as a function of the phase of the beta rhythm.} A bare panel label naming the quantity plotted.⟧

Dashed gray line shows the modulation of inhibitory drive with respect to phase.

( B ) Percent change in Ca 2+ spike presence at apical nexus by beta phase.⟦>zach claim=no-assertion: @{( B ) Percent change in Ca 2+ spike presence at apical nexus by beta phase.} A bare panel label naming the quantity plotted.⟧

( C1–2 ) Percent change of NMDA spike presence in apical (1) and basal (2) dendrites stratified by electronic distance from the soma.

( D1–2 ) Same as C , but for Na + spikes.

( E, F, G1–2, H1–2 ) Same format as above, but with events binned by the phase of gamma rhythmic inhibition.

For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. Initially, we delivered beta rhythmic inhibition to the distal dendritic compartments and gamma to the perisomatic.

Even though both rhythms produced similar depths of modulation of somatic action potentials, the underlying causes were distinct.

The phase of beta modulated the occurrence of Ca 2+ , NMDA, and Na + spikes, with each showing an ~75% depth of modulation with respect to their mean level ( Figure 5C–E ).⟦>zach claim=bf7efeee-2819-485d-a06d-1fc3782ce66f: @{The phase of beta modulated the occurrence of Ca 2+ , NMDA, and Na + spikes, with each showing an ~75% depth of modulation with respect to their mean level ( Figure 5C–E ).} beta-bidirectional-dendritic-control — The claim asserts phase-dependent control of dendritic spike occurrence by distal beta, which is the modulation reported here.⟧

These changes were seen across the entire dendritic tree, spanning sites electrotonically close to and far from the soma.

In addition, the impact on Na + spikes was unexpected ( Figure 5E ), since delivery of the same inhibition tonically had little effect.⟦>zach claim=gap: @{In addition, the impact on Na + spikes was unexpected ( Figure 5E ), since delivery of the same inhibition tonically had little effect.} The dissociation between rhythmic and tonic distal inhibition for Na+ spikes is flagged as unexpected here but no claim states it.⟧

By contrast, gamma had virtually no effect on dendritic spikes ( Figure 5F–H ).⟦>zach claim=b7b55f60-7438-47fd-a42a-431bcbaf696b: @{By contrast, gamma had virtually no effect on dendritic spikes ( Figure 5F–H ).} gamma-perisomatic-no-dendritic-spike-change — The claim states that perisomatic gamma leaves dendritic spike rates substantially unaltered.⟧

Its strongest impact was on Na + spikes in basal dendritic compartments that were electronically close to the soma.

To uncover the modulation of action potentials by gamma, we turned our attention to somatic action potential initiation ( Figure 6 ).⟦>zach claim=702332b6-1ba1-40b9-9319-f9f3053d59dd: @{To uncover the modulation of action potentials by gamma, we turned our attention to somatic action potential initiation ( Figure 6 ).} perisomatic-inhib-subtractive-divisive⟧

For these analyses, we divided the inhibitory rhythm into two phases.

During the peak phase, inhibition was greater than its mean rate, while during the trough phase, inhibition was lower (see Figure 5A and F ).⟦>zach claim=no-assertion: @{During the peak phase, inhibition was greater than its mean rate, while during the trough phase, inhibition was lower (see Figure 5A and F ).} Defines what peak and trough phase mean in these plots.⟧

We found that the somatic action potential voltage threshold shifted lower during the ‘trough’ phase of gamma, when inhibition was at its weakest ( Figure 6A1 ) and without any change in the mean membrane voltage ( Figure 6A2 ).⟦>zach claim=568bd16c-91dc-4bf0-8841-1836968cf68e: @{We found that the somatic action potential voltage threshold shifted lower during the ‘trough’ phase of gamma, when inhibition was at its weakest ( Figure 6A1 ) and without any change in the mean membrane voltage ( Figure 6A2 ).} gamma-optimal-perisomatic-ap-modulation — The claim asserts phase-dependent modulation of somatic AP voltage threshold by perisomatic gamma, which is the trough-phase threshold drop reported here.⟧

This is consistent with gamma phase modulating the shunting of voltage-gated Na + channel currents, which occurs when GABAergic synapses co-locate with the channels mediating action potential initiation ( Rojas et al., 2011 ).

We also observed changes in action potential initiation to beta rhythmic inhibition, but through a different mechanism.

During the ‘peak’ phase of beta, when inhibition was maximal, the threshold for evoking an action potential increased, which may reflect an ‘off-path’ shunting of excitatory current away from the soma and toward the dendrites ( Figure 6B1 ; Gidon and Segev, 2012 ).⟦>zach claim=gap: @{During the ‘peak’ phase of beta, when inhibition was maximal, the threshold for evoking an action potential increased, which may reflect an ‘off-path’ shunting of excitatory current away from the soma and toward the dendrites ( Figure 6B1 ; Gidon and Segev, 2012 ).} A threshold increase during the beta peak, and the off-path shunting account of it, is asserted here while the tree's distal claims predict little threshold change.⟧

Additionally, there was a decrease in membrane voltage during the peak phase, which may correspond to decreased excitation arising from the suppression of dendritic spikes ( Figure 6B2 ).⟦>zach claim=gap: @{Additionally, there was a decrease in membrane voltage during the peak phase, which may correspond to decreased excitation arising from the suppression of dendritic spikes ( Figure 6B2 ).} The membrane-potential decrease during the beta peak, and its attribution to suppressed dendritic spikes, is claimed nowhere.⟧

Figure 6. Phase-dependent effects of gamma and beta rhythmic inhibition on somatic excitability.⟦>zach claim=702332b6-1ba1-40b9-9319-f9f3053d59dd: @{Figure 6. Phase-dependent effects of gamma and beta rhythmic inhibition on somatic excitability.} perisomatic-inhib-subtractive-divisive⟧

( A1 ) A cumulative probability plot of the distribution of somatic membrane potentials 1 ms prior to an action potential, sorted by whether they occurred during the gamma phase with maximal (peak, red line) or minimal (trough, blue line) inhibitory drive.

Poisson (black) had no rhythmic modulation, but the same mean inhibitory rate.

( A2 ) Probability distribution of somatic membrane voltage as a function of gamma phase, normalized to the peak probability value.

Lines have the same color scheme as in A1 .

( B1 ) Same format as A1 , but for the beta rhythm.

( B2 ) Same format as A2 , but for the beta rhythm.

Figure 6—figure supplement 1. Phase-dependent effects on somatic excitability of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.⟦>zach claim=no-assertion: @{Figure 6—figure supplement 1. Phase-dependent effects on somatic excitability of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.} A figure-supplement title, not a stated finding.⟧

Beta was delivered perisomatically, while gamma was supplied to the distal dendrites.

( A1 ) A cumulative probability plot of the distribution of somatic membrane potentials 1 ms prior to an action potential, sorted by whether they occurred during the gamma phase with maximal (peak, red line) or minimal (trough, blue line) inhibitory drive.

Poisson (black) had no rhythmic modulation, but the same mean inhibitory rate.

( A2 ) Probability distribution of somatic membrane voltage as a function of gamma phase, normalized to the peak probability value.

Lines have the same color scheme as in A1 .

( B1 ) Same format as A1 , but for the beta rhythm.

( B2 ) Same format as A2 , but for the beta rhythm.

Accompanying these effects were changes in the rate of dendritic spikes compared with the Poisson inhibition case.

Beta increased the rate of Na + (+16.6%) and Ca 2+ spikes (+15.1%) but decreased the rate of NMDA spikes (–10.7%).

Gamma caused no change in NMDA (+0.2%) and a weak increase in Na + spikes (+6.4%), but a robust gain in Ca 2+ spikes (+37.9%).

We next switched the locations on the pyramidal neuron targeted by the beta and gamma rhythms to disassociate the frequency of inhibition from its location.

Beta rhythmic inhibition was delivered perisomatically and gamma rhythmic inhibition to distal dendrites.

While phase modulation of firing rate was maintained with both rhythms, the overall level of spiking was dramatically reduced ( Figure 5—figure supplement 1A and E ).⟦>zach claim=gap: @{While phase modulation of firing rate was maintained with both rhythms, the overall level of spiking was dramatically reduced ( Figure 5—figure supplement 1A and E ).} The swapped-location control, where phase modulation of firing survives but overall spiking collapses, has no claim behind it.⟧

Neither rhythm modulated Ca 2+ or NMDA spikes ( Figure 5—figure supplement 1B, C, F, and G ).⟦>zach claim=gap: @{Neither rhythm modulated Ca 2+ or NMDA spikes ( Figure 5—figure supplement 1B, C, F, and G ).} The null effect on Ca2+ and NMDA spikes when each rhythm is delivered to the wrong compartment is an unclaimed control result.⟧

It is likely that the slow timescale of Ca 2+ and NMDA spikes, ~50 ms, is not optimal for the fast periodicity of the gamma rhythm, which cycles every ~15 ms. In agreement with this, Na + spikes, which last less than 1 ms, did show modulation by gamma rhythms delivered to the distal dendrites ( Figure 5—figure supplement 1D and H ).⟦>zach claim=163fe42f-c4ee-480c-8f49-927d6bc22ef1: @{It is likely that the slow timescale of Ca 2+ and NMDA spikes, ~50 ms, is not optimal for the fast periodicity of the gamma rhythm, which cycles every ~15 ms. In agreement with this, Na + spikes, which last less than 1 ms, did show modulation by gamma rhythms delivered to the distal dendrites ( Figure 5—figure supplement 1D and H ).} Each compartment's best rhythm matches its local spike timescale: gamma soma, beta distal. — This is the claim's timescale-matching logic in action: slow Ca2+ and NMDA processes escape gamma while sub-millisecond Na+ spikes follow it.⟧

Swapping the location of beta and gamma synapses altered their effects on somatic excitability.

Gamma rhythmic inhibition on the dendrites had minimal or no impact on action potential threshold, but did shift the somatic membrane potential more negative ( Figure 6—figure supplement 1A ).⟦>zach claim=gap: @{Gamma rhythmic inhibition on the dendrites had minimal or no impact on action potential threshold, but did shift the somatic membrane potential more negative ( Figure 6—figure supplement 1A ).} Dendritic gamma sparing AP threshold while hyperpolarizing the soma is a control result with no claim in the tree.⟧

This hyperpolarization was not dependent on gamma phase and likely reflected an overall decrease in the rate of dendritic spikes that could supply excitatory drive to the soma (NMDA: –26.1%, Na + : –12.2%, and Ca 2+ : –39.9% compared with the Poisson inhibition case).

By contrast, delivering beta rhythmic inhibition to the soma raised the action potential threshold and hyperpolarized the membrane potential during the peak phase ( Figure 6—figure supplement 1B ).⟦>zach claim=gap: @{By contrast, delivering beta rhythmic inhibition to the soma raised the action potential threshold and hyperpolarized the membrane potential during the peak phase ( Figure 6—figure supplement 1B ).} Somatically delivered beta raising threshold and hyperpolarizing at the peak is a control result the tree does not claim.⟧

It also reduced the incidence of dendritic spikes (NMDA: –17.1%, Na + : –11.5%, and Ca 2+ : –7.6%).

Putting all this together, the effectiveness of rhythmic inhibition depends on where it impinges upon the neuron.

Beta rhythms targeting the distal dendrites modulate the incidence of dendritic spikes in a phase-dependent manner, while gamma rhythms delivered perisomatically phase-modulate somatic excitability.

Swapping the locations of these rhythms diminishes these effects and lowers overall excitability.

Frequency-specific effects of rhythmic inhibition on neuronal integration Having demonstrated that the location of beta and gamma rhythmic inhibition impacts their effectiveness, we next determined its frequency specificity.

To do this, we varied the frequency of rhythmic inhibition between 0.5 and 80 Hz on either the perisomatic or distal dendritic neuronal compartments.

Starting with distal dendrites, increasing inhibition frequency above 20 Hz diminished its entrainment of NMDA, Na + , and Ca 2+ spike onsets ( Figure 7A ).⟦>zach claim=4ee66306-a11b-4333-86cf-47ea92155e76: @{Starting with distal dendrites, increasing inhibition frequency above 20 Hz diminished its entrainment of NMDA, Na + , and Ca 2+ spike onsets ( Figure 7A ).} beta-optimal-distal-dendritic-entrainment — The claim locates peak distal entrainment near 20 Hz, which is the fall-off above 20 Hz reported here.⟧

The falloff in entrainment was most pronounced above 20 Hz.

Curiously, Na + spikes exhibited a preferential entrainment at 20 Hz.

In general, entrainment was strongest in the apical dendrites.

Figure 7. Frequency- and phase-dependent effects of inhibitory rhythms on the distal dendrites.⟦>zach claim=bf7efeee-2819-485d-a06d-1fc3782ce66f: @{Figure 7. Frequency- and phase-dependent effects of inhibitory rhythms on the distal dendrites.} beta-bidirectional-dendritic-control⟧

( A ) Entrainment to an inhibitory rhythm delivered to the distal dendrites varied with its frequency.⟦>zach claim=4ee66306-a11b-4333-86cf-47ea92155e76: @{( A ) Entrainment to an inhibitory rhythm delivered to the distal dendrites varied with its frequency.} beta-optimal-distal-dendritic-entrainment — The caption states the frequency dependence of distal entrainment that the claim makes.⟧

Higher frequencies were less able to entrain dendritic spikes.

Entrainment tended to be strongest for apical (blue) over basal (orange) compartments.

( B ) Example voltage traces from dendritic compartments in either the distal basal or apical branches.⟦>zach claim=no-assertion: @{( B ) Example voltage traces from dendritic compartments in either the distal basal or apical branches.} A bare panel label naming the example traces shown.⟧

Gray shading denotes the period where the inhibitory rhythm troughs occurred.

For the basal segment, NMDA spikes were shaded in purple, while in the apical segment, Ca 2+ spikes were shaded in green.

Dendritic spike onsets denote with red lines, and offsets with blue lines.

( C ) Percent change from the mean in the rate of dendritic spike onsets (red gradient) and offsets (blue gradient) as a function of rhythm frequency and phase.⟦>zach claim=no-assertion: @{( C ) Percent change from the mean in the rate of dendritic spike onsets (red gradient) and offsets (blue gradient) as a function of rhythm frequency and phase.} Explains the colour gradients used to encode onsets and offsets.⟧

Purple regions denote phase/frequency combinations where both onsets and offsets were elevated, while regions with either just blue or red indicate that offsets or onsets preferentially occurred, respectively.

We did not determine an offset for Na + spikes due to their transience (~1 ms).

The previous analysis considered the entrainment of dendritic spike onsets , but NMDA and Ca 2+ spikes also exhibit offsets that could also be modulated by rhythmic inhibition.

Indeed, examination of voltage traces in the dendrites during beta rhythmic inhibition revealed that NMDA and Ca 2+ spike onsets tended to occur during the trough, while offsets happened during the peaks ( Figure 7B ).⟦>zach claim=bf7efeee-2819-485d-a06d-1fc3782ce66f: @{Indeed, examination of voltage traces in the dendrites during beta rhythmic inhibition revealed that NMDA and Ca 2+ spike onsets tended to occur during the trough, while offsets happened during the peaks ( Figure 7B ).} beta-bidirectional-dendritic-control — Onsets in the trough and offsets at the peak is precisely the bidirectional, within-cycle control the claim asserts.⟧

To quantify this, we plotted the percent change in the probability of dendritic spike onsets and offsets with respect to both the phase and frequency of the inhibitory rhythm ( Figure 7C ).⟦>zach claim=no-assertion: @{To quantify this, we plotted the percent change in the probability of dendritic spike onsets and offsets with respect to both the phase and frequency of the inhibitory rhythm ( Figure 7C ).} Narrates the quantification performed rather than its result.⟧

For frequencies less than 5 Hz, there was minimal phase separation between the onsets and offsets of Ca 2+ or NMDA spikes; both events occurred near the rhythm trough, when inhibition was at its weakest.

As frequency increased up to 20 Hz, the preferred phase of dendritic spike offsets migrated toward the peak phase, where inhibition is strongest.

This phase separation effect was strongest for Ca 2+ spikes.

Thus, beta band frequencies exhibit unique coordination with dendritic spikes: they are the fastest rhythm capable of entraining them and align with their initiation and cessation in a phase-dependent manner.

Turning to perisomatic inhibition, we again varied the frequency of the inhibitory rhythm.

Lower frequency inhibition produced phase-dependent shifts in the mean membrane potential ( Figure 8A ).⟦>zach claim=gap: @{Lower frequency inhibition produced phase-dependent shifts in the mean membrane potential ( Figure 8A ).} Phase-dependent shifts in mean somatic membrane potential at low rhythm frequencies are unclaimed; the tree's perisomatic sweep claim covers threshold only.⟧

The trough of inhibition depolarized the soma, while the peak of inhibition had the opposite effect.

As the frequency increased, this phase-dependent difference went away, vanishing above 50 Hz.

By contrast, as frequency increased, the bias in momentary changes in the membrane potential diverged between peaks and troughs ( Figure 8B ).⟦>zach claim=gap: @{By contrast, as frequency increased, the bias in momentary changes in the membrane potential diverged between peaks and troughs ( Figure 8B ).} The divergence of momentary membrane-potential fluctuations between peak and trough as frequency rises is a separate result no claim states.⟧

During the peak phase, membrane voltage fluctuations were biased negative, while during the trough, they were biased positive.

This effect increased with frequency, peaking at 50 Hz and then declining modestly.

Together, these effects make gamma frequencies unique in keeping the mean membrane potential equivalent between phases but biasing its fluctuations toward depolarizing or hyperpolarizing with phase.

During the trough, there was an excess of depolarizing membrane potential fluctuations.

Since the rate of excitatory synaptic drive was independent of phase, this suggests that its responsiveness to excitatory inputs increased in a phase-dependent manner with gamma.

Figure 8. Frequency- and phase-dependent effects of inhibitory rhythms on the perisomatic region.⟦>zach claim=568bd16c-91dc-4bf0-8841-1836968cf68e: @{Figure 8. Frequency- and phase-dependent effects of inhibitory rhythms on the perisomatic region.} gamma-optimal-perisomatic-ap-modulation⟧

( A ) The mean somatic membrane potential during either the trough or peak phase of the inhibitory rhythm.⟦>zach claim=no-assertion: @{( A ) The mean somatic membrane potential during either the trough or peak phase of the inhibitory rhythm.} A bare panel label naming the quantity plotted.⟧

( B ) Mean of the distribution of somatic membrane potential fluctuations as a function rhythm phase and frequency.⟦>zach claim=no-assertion: @{( B ) Mean of the distribution of somatic membrane potential fluctuations as a function rhythm phase and frequency.} A bare panel label naming the quantity plotted.⟧

Fluctuations were measured across the entire simulation time as the difference in membrane potential at 1 ms delays.

For both graphs, red lines are peaks and blue lines are troughs.

Modulation of dendritic spikes during oscillatory bursts In vivo, beta and gamma rhythms occur as bursts lasting less than a few hundred milliseconds.

Since the previous analyses relied on tonically delivered rhythms, we verified that similar effects were observed with oscillatory bursts.

Gamma and beta bursts were delivered to the same model with mean depth of modulation like the tonic case ( Figure 9A and F ; see Methods for details).⟦>zach claim=no-assertion: @{Gamma and beta bursts were delivered to the same model with mean depth of modulation like the tonic case ( Figure 9A and F ; see Methods for details).} Describes how the burst simulations were configured, not what they showed.⟧

Figure 9. Phase-dependent effects of gamma and beta bursts on dendritic spikes.⟦>zach claim=34c1a5fd-714f-4cde-ba8b-1c230af108db: @{Figure 9. Phase-dependent effects of gamma and beta bursts on dendritic spikes.} burst-effects-emerge-first-cycles⟧

( A ) Example data from the gamma rhythmic inhibition simulation.⟦>zach claim=no-assertion: @{( A ) Example data from the gamma rhythmic inhibition simulation.} A bare panel label naming example data.⟧

Top, somatic potential (black line), with firing rate of perisomatic inhibitory synapses (blue line).

Middle, voltage trace of apical compartment.

Bottom, voltage trace of basal compartment.

( B ) Action potential rate as a function of the phase of the gamma rhythm.⟦>zach claim=no-assertion: @{( B ) Action potential rate as a function of the phase of the gamma rhythm.} A bare panel label naming the quantity plotted.⟧

Blue line shows the modulation of inhibitory drive with respect to phase.

( C ) Percent change in Ca 2+ spike presence at apical nexus by gamma phase.⟦>zach claim=no-assertion: @{( C ) Percent change in Ca 2+ spike presence at apical nexus by gamma phase.} A bare panel label naming the quantity plotted.⟧

( D1–2 ) Percent change of NMDA spike presence in apical (1) and basal (2) dendrites stratified by electronic distance from the soma.

( E1–2 ) Same as C , but for Na + spikes.

( F, G, H, I1–2, J1–2 ) Same format as above, but with events binned by the phase of beta rhythmic inhibition.

For all graphs, cycle number is given relative to the amplitude peak of the burst.

Under the burst regime, both rhythms mirrored their behavioral effects.

Gamma bursts entrained spiking, with entrainment strongest during the middle of the burst ( Figure 9B ).⟦>zach claim=34c1a5fd-714f-4cde-ba8b-1c230af108db: @{Gamma bursts entrained spiking, with entrainment strongest during the middle of the burst ( Figure 9B ).} burst-effects-emerge-first-cycles — The claim asserts that gamma bursts phase-modulate action potential timing across the burst, which is the entrainment reported here.⟧

As with the tonically imposed rhythm, there was none or minimal modulation of Ca 2+ ( Figure 9C ), NMDA ( Figure 9D ), and Na + spikes ( Figure 9E ).⟦>zach claim=b7b55f60-7438-47fd-a42a-431bcbaf696b: @{As with the tonically imposed rhythm, there was none or minimal modulation of Ca 2+ ( Figure 9C ), NMDA ( Figure 9D ), and Na + spikes ( Figure 9E ).} gamma-perisomatic-no-dendritic-spike-change — The claim's orthogonality point, that perisomatic gamma leaves dendritic spikes alone, holds for bursts as well as tonic rhythms.⟧

Beta rhythms entrained somatic action potentials ( Figure 9G ), Ca 2+ spikes ( Figure 9H ), NMDA ( Figure 9I ), and Na + spikes ( Figure 9J ).⟦>zach claim=34c1a5fd-714f-4cde-ba8b-1c230af108db: @{Beta rhythms entrained somatic action potentials ( Figure 9G ), Ca 2+ spikes ( Figure 9H ), NMDA ( Figure 9I ), and Na + spikes ( Figure 9J ).} burst-effects-emerge-first-cycles — The claim asserts that beta bursts phase-modulate both dendritic spikes and action potential timing, which is the entrainment reported here.⟧

These modulations were evident within the first few cycles of a burst, suggesting that they did not require a buildup or evolving entrainment of an underlying process.

Effect of beta and gamma rhythms on responding to clustered synaptic drive The results so far suggest that beta and gamma rhythms modulate synaptic integration through different mechanisms depending on their phase and the location of the synapses on the dendritic tree.

To examine this further, we added patches of concentrated excitatory synaptic inputs onto either the distal or proximal dendrites ( Figure 10A ), with densities similar to functional clusters in vivo ( Iacaruso et al., 2017 ; Fu et al., 2012 ).⟦>zach claim=no-assertion: @{To examine this further, we added patches of concentrated excitatory synaptic inputs onto either the distal or proximal dendrites ( Figure 10A ), with densities similar to functional clusters in vivo ( Iacaruso et al., 2017 ; Fu et al., 2012 ).} Describes the clustered-input manipulation that was added, not a result of it.⟧

Coactivated inputs were simulated by driving each synapse with a jittered (2 ms) Poisson process.

We ran six separate simulations, either with the distal or proximal clusters engaged, and under conditions of Poisson, beta, or gamma rhythmic inhibition.

Figure 10. Effect of beta and gamma rhythms on responsiveness to synaptic inputs targeting distinct regions of the dendritic tree.⟦>zach claim=7b7dd3fd-3946-4947-9799-a4f8a8821aba: @{Figure 10. Effect of beta and gamma rhythms on responsiveness to synaptic inputs targeting distinct regions of the dendritic tree.} beta-gates-distal-apical-inputs⟧

( A ) Schematic of the location for clustered excitatory synaptic inputs.⟦>zach claim=no-assertion: @{( A ) Schematic of the location for clustered excitatory synaptic inputs.} A bare panel label describing a schematic.⟧

( B ) Normalized cross-correlation between synaptic drive onto a clustered input and spiking at the soma, stratified by whether the presynaptic spike arrived during the peak (red line) or trough (blue line) of the rhythm.⟦>zach claim=no-assertion: @{( B ) Normalized cross-correlation between synaptic drive onto a clustered input and spiking at the soma, stratified by whether the presynaptic spike arrived during the peak (red line) or trough (blue line) of the rhythm.} Explains what the panel plots and how peak and trough are colour coded.⟧

Solid bars correspond to the Poisson stimulation case where inhibition was not rhythmically modulated.

Top left, effect of beta on distal inputs.

Top right, effect of gamma on distal inputs.

Bottom left, effect of beta on proximal inputs.

Bottom right, effect of gamma on proximal inputs.

( C ) Summary of effects in panel B where the strength of each normalized cross-correlation was measured as its area under the curve.⟦>zach claim=no-assertion: @{( C ) Summary of effects in panel B where the strength of each normalized cross-correlation was measured as its area under the curve.} Explains how the summary measure was computed from the preceding panel.⟧

Dots are connected by dashed gray lines if the data points came from the same simulation but at different phases of the rhythm.

Solid horizontal lines reflect the cross-correlation strength in the Poisson inhibitory case (no rhythmicity).

To capture how beta and gamma influence synaptic integration, we measured the CC between presynaptic activations at the clustered input and somatic spiking.

Separate cross-correlograms were calculated depending on whether the presynaptic spikes occurred during the peak or trough phase of the inhibitory rhythm.

This necessarily introduced spurious periodicities into the cross-correlogram that were compensated (see Methods for details).

Relative to the arhythmic Poisson inhibition case, beta rhythms enhanced the transmission of distal inputs when inhibition was low (trough phase) and suppressed them when inhibition was high (peak phase, Figure 10B , top left).⟦>zach claim=7b7dd3fd-3946-4947-9799-a4f8a8821aba: @{Relative to the arhythmic Poisson inhibition case, beta rhythms enhanced the transmission of distal inputs when inhibition was low (trough phase) and suppressed them when inhibition was high (peak phase, Figure 10B , top left).} beta-gates-distal-apical-inputs — Transmission of distal inputs in the trough and blockade at the peak is exactly the gating the claim asserts.⟧

Proximal inputs were either unaffected or moderately suppressed during the trough and suppressed during the peak ( Figure 10B , bottom left).⟦>zach claim=gap: @{Proximal inputs were either unaffected or moderately suppressed during the trough and suppressed during the peak ( Figure 10B , bottom left).} Beta's suppressive effect on proximal clustered inputs is reported here but no claim covers what beta does outside the distal apical compartment.⟧

The opposite was the case for gamma.

It barely affected or moderately suppressed distal inputs ( Figure 10B , top right), while proximal inputs were enhanced during the trough and suppressed during the peak ( Figure 10B , bottom right).⟦>zach claim=e1ce7be2-5fe7-4cda-80cb-775473b52e21: @{It barely affected or moderately suppressed distal inputs ( Figure 10B , top right), while proximal inputs were enhanced during the trough and suppressed during the peak ( Figure 10B , bottom right).} gamma-gates-proximal-basal-inputs — Gamma enhancing proximal inputs in the trough and suppressing them at the peak, while barely touching distal inputs, is the claim's gating pattern.⟧

Summarizing these results ( Figure 10C ), we found that somatic spiking driven by clustered proximal synapses was bidirectionally modulated by gamma rhythms and suppressed by beta.⟦>zach claim=gap: @{Summarizing these results ( Figure 10C ), we found that somatic spiking driven by clustered proximal synapses was bidirectionally modulated by gamma rhythms and suppressed by beta.} The gamma half of this summary is claimed, but the suppression of proximal input transmission by beta is not stated anywhere in the tree.⟧

On the other hand, spiking driven by distal clusters was bidirectionally modulated by the beta rhythm and suppressed by gamma.

Thus, both rhythms regulate the sensitivity of pyramidal neurons to afferents throughout the dendritic tree, but in a counterposed location-dependent manner.


## captions

=== Figure 1 === Figure 1. A model layer 5 pyramidal neuron with active dendrites.⟦>zach claim=5037933c-103b-4f19-992e-1abb330ea4f1: @{=== Figure 1 === Figure 1. A model layer 5 pyramidal neuron with active dendrites.} l5-model-single-cell-scope⟧

( A ) The morphology of the neuron.

Virtual recordings can be obtained from any desired compartment (colored pipettes).

Inset, naturalistic presynaptic activity drives firing rates in our model like those in vivo.

Each black cross is the mean rate for a different simulation.

( B ) Examples of membrane potentials recorded simultaneously across the dendritic tree (in color) and soma (black) during naturalistic drive.

Regenerative events are indicated with arrows or text (AP: action potential, bAP: backpropagating action potential).

( C1–3 ) Demonstration of our detection of dendritic spike events (top) and characterization of their properties (bottom).

Events are binned according to the properties that were used in their detection.

Bin edges for the event durations were not evenly set for panels C2 and C3 .

[panels detected: a, b] === Figure 2 === Figure 2. Influence of Na + and NMDA spikes on action potential generation.⟦>zach claim=9c3d1464-1a51-4381-a466-fcb1ca6fca65: @{[panels detected: a, b] === Figure 2 === Figure 2. Influence of Na + and NMDA spikes on action potential generation.} ca-spikes-couple-20ms-before-ap⟧

( A ) Electrotonic distance between each dendritic compartment and the soma.

( B ) Dendritic compartments were grouped by their type (apical or basal) and electrotonic distance (percentile) from the soma.

The percent change in Na + spike presence in those compartments relative to somatic spiking.

Na + spikes increased immediately prior to action potentials in dendritic compartments that were electrotonically close to the soma.

( C ) Same format as B , but for NMDA spikes.

These showed a similar degree of change, but a broader temporal coupling.

[panels detected: a, b, c] === Figure 3 === Figure 3. Influence of Ca 2+ spikes on action potential generation and their behavior as a second integrative mechanism.⟦>zach claim=9c3d1464-1a51-4381-a466-fcb1ca6fca65: @{[panels detected: a, b, c] === Figure 3 === Figure 3. Influence of Ca 2+ spikes on action potential generation and their behavior as a second integrative mechanism.} ca-spikes-couple-20ms-before-ap⟧

( A ) Electrotonic distance between dendritic compartments and the apical nexus, where Ca 2+ spikes are generated.

( B ) Change in the incidence of Ca 2+ spikes at the nexus surrounding action potentials.

( C ) Percent change in NMDA spike presence in the apical dendrites centered on Ca 2+ spike initiation.

( D ) Percent change in NMDA spike coupling with action potentials during Ca 2+ spikes.

Top, NMDA spikes in apical dendrites were more strongly coupled with action potentials during Ca 2+ spikes.

Bottom, this was not the case for basal dendrites.

[panels detected: a, b, c, d] === Figure 4 === Figure 4. Distal dendritic and perisomatic inhibition reduce action potential generation through different mechanisms.⟦>zach claim=26819b09-5b20-4c90-b9f3-8bdd29a2a57c: @{[panels detected: a, b, c, d] === Figure 4 === Figure 4. Distal dendritic and perisomatic inhibition reduce action potential generation through different mechanisms.} distal-inhib-drops-firing-02hz⟧

( A ) Action potential rate during periods with normal inhibitory tone (control), double rate on distal branches, or double rate on perisomatic.

Both increases in inhibition dramatically reduced the firing of somatic action potentials.

( B ) Somatic excitability was measured by delivering current steps during the control, distal, and perisomatic inhibition states.

Left, example somatic voltage responses to current steps.

Right, spike frequency versus current (f–I) curve for each condition.

The threshold for evoking an action potential shifted with 2× distal and perisomatic inhibition.

Perisomatic, but not dendritic, inhibition changed the f-I slope (compare dashed lines with solid black).

( C ) Impact of altered dendritic inhibition on rate of Na + spikes in apical and basal dendrites.

( D ) Same format as C , but for NMDA spikes.

( E ) Rate of Ca 2+ spikes in the apical dendrites.

Basal dendrites lacked Ca 2+ spikes and were excluded.

All error bars are mean ± standard deviation.

( F ) Examples of membrane potential recorded in control (top), and both distal (middle) and proximal (bottom) inhibition lagged by 500 ms. ( G ) Change in firing rate for control (black dot) and for perisomatic (blue) and distal (red) lags in inhibition from 0 to 500 ms. ( H ) Change in incidence of Ca 2+ spikes for distal (red, top) and proximal (blue, bottom) inhibition.

The control case is shown in black in both panels.

( I ) Same as ( H ) but for NMDA spikes.

[panels detected: a, b, f, g, h, i, c, d, e] === Figure 5 === Figure 5. Phase-dependent effects of beta and gamma rhythmic inhibition on dendritic spikes.⟦>zach claim=bf7efeee-2819-485d-a06d-1fc3782ce66f: @{[panels detected: a, b, f, g, h, i, c, d, e] === Figure 5 === Figure 5. Phase-dependent effects of beta and gamma rhythmic inhibition on dendritic spikes.} beta-bidirectional-dendritic-control⟧

( A ) Example data from the beta rhythmic inhibition simulation.

Top, presynaptic spike counts.

Bottom, voltage traces from somatic and dendritic compartments.

Grayed periods are when inhibitory presynaptic spikes are peaking.

( B ) Action potential rate as a function of the phase of the beta rhythm.

Dashed gray line shows the modulation of inhibitory drive with respect to phase.

( C ) Percent change in Ca 2+ spike presence at apical nexus by beta phase.

( D1–2 ) Percent change of NMDA spike presence in apical (1) and basal (2) dendrites stratified by electronic distance from the soma.

( E1–2 ) Same as C , but for Na + spikes.

( F, G, H, I1–2, J1–2 ) Same format as above, but with events binned by the phase of gamma rhythmic inhibition.

For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. [panels detected: a, b, c] === Figure 5s1 === Figure 5—figure supplement 1. Phase-dependent effects on dendritic spikes of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.⟦>zach claim=no-assertion: @{For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. [panels detected: a, b, c] === Figure 5s1 === Figure 5—figure supplement 1. Phase-dependent effects on dendritic spikes of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.} States the phase convention used in the plots and gives a figure title.⟧

Beta was delivered perisomatically, while gamma was supplied to the distal dendrites.

( A ) Action potential rate as a function of the phase of the beta rhythm.

Dashed gray line shows the modulation of inhibitory drive with respect to phase.

( B ) Percent change in Ca 2+ spike presence at apical nexus by beta phase.

( C1–2 ) Percent change of NMDA spike presence in apical (1) and basal (2) dendrites stratified by electronic distance from the soma.

( D1–2 ) Same as C , but for Na + spikes.

( E, F, G1–2, H1–2 ) Same format as above, but with events binned by the phase of gamma rhythmic inhibition.

For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. [panels detected: a, b] === Figure 6 === Figure 6. Phase-dependent effects of gamma and beta rhythmic inhibition on somatic excitability.⟦>zach claim=702332b6-1ba1-40b9-9319-f9f3053d59dd: @{For all graphs, phase is given in radians with inhibition at a minimum for – π and maximum at 0. [panels detected: a, b] === Figure 6 === Figure 6. Phase-dependent effects of gamma and beta rhythmic inhibition on somatic excitability.} perisomatic-inhib-subtractive-divisive⟧

( A1 ) A cumulative probability plot of the distribution of somatic membrane potentials 1 ms prior to an action potential, sorted by whether they occurred during the gamma phase with maximal (peak, red line) or minimal (trough, blue line) inhibitory drive.

Poisson (black) had no rhythmic modulation, but the same mean inhibitory rate.

( A2 ) Probability distribution of somatic membrane voltage as a function of gamma phase, normalized to the peak probability value.

Lines have the same color scheme as in A1 .

( B1 ) Same format as A1 , but for the beta rhythm.

( B2 ) Same format as A2 , but for the beta rhythm. === Figure 6s1 === Figure 6—figure supplement 1. Phase-dependent effects on somatic excitability of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.⟦>zach claim=no-assertion: @{( B2 ) Same format as A2 , but for the beta rhythm. === Figure 6s1 === Figure 6—figure supplement 1. Phase-dependent effects on somatic excitability of beta and gamma rhythmic inhibition delivered to opposite areas of the neuron.} A panel label deferring to an earlier panel's format, plus a figure title.⟧

Beta was delivered perisomatically, while gamma was supplied to the distal dendrites.

( A1 ) A cumulative probability plot of the distribution of somatic membrane potentials 1 ms prior to an action potential, sorted by whether they occurred during the gamma phase with maximal (peak, red line) or minimal (trough, blue line) inhibitory drive.

Poisson (black) had no rhythmic modulation, but the same mean inhibitory rate.

( A2 ) Probability distribution of somatic membrane voltage as a function of gamma phase, normalized to the peak probability value.

Lines have the same color scheme as in A1 .

( B1 ) Same format as A1 , but for the beta rhythm.

( B2 ) Same format as A2 , but for the beta rhythm. === Figure 7 === Figure 7. Frequency- and phase-dependent effects of inhibitory rhythms on the distal dendrites.⟦>zach claim=bf7efeee-2819-485d-a06d-1fc3782ce66f: @{( B2 ) Same format as A2 , but for the beta rhythm. === Figure 7 === Figure 7. Frequency- and phase-dependent effects of inhibitory rhythms on the distal dendrites.} beta-bidirectional-dendritic-control⟧

( A ) Entrainment to an inhibitory rhythm delivered to the distal dendrites varied with its frequency.

Higher frequencies were less able to entrain dendritic spikes.

Entrainment tended to be strongest for apical (blue) over basal (orange) compartments.

( B ) Example voltage traces from dendritic compartments in either the distal basal or apical branches.

Gray shading denotes the period where the inhibitory rhythm troughs occurred.

For the basal segment, NMDA spikes were shaded in purple, while in the apical segment, Ca 2+ spikes were shaded in green.

Dendritic spike onsets denote with red lines, and offsets with blue lines.

( C ) Percent change from the mean in the rate of dendritic spike onsets (red gradient) and offsets (blue gradient) as a function of rhythm frequency and phase.

Purple regions denote phase/frequency combinations where both onsets and offsets were elevated, while regions with either just blue or red indicate that offsets or onsets preferentially occurred, respectively.

We did not determine an offset for Na + spikes due to their transience (~1 ms).

[panels detected: a, b, c] === Figure 8 === Figure 8. Frequency- and phase-dependent effects of inhibitory rhythms on the perisomatic region.⟦>zach claim=568bd16c-91dc-4bf0-8841-1836968cf68e: @{[panels detected: a, b, c] === Figure 8 === Figure 8. Frequency- and phase-dependent effects of inhibitory rhythms on the perisomatic region.} gamma-optimal-perisomatic-ap-modulation⟧

( A ) The mean somatic membrane potential during either the trough or peak phase of the inhibitory rhythm.

( B ) Mean of the distribution of somatic membrane potential fluctuations as a function rhythm phase and frequency.

Fluctuations were measured across the entire simulation time as the difference in membrane potential at 1 ms delays.

For both graphs, red lines are peaks and blue lines are troughs.

[panels detected: a, b] === Figure 9 === Figure 9. Phase-dependent effects of gamma and beta bursts on dendritic spikes.⟦>zach claim=34c1a5fd-714f-4cde-ba8b-1c230af108db: @{[panels detected: a, b] === Figure 9 === Figure 9. Phase-dependent effects of gamma and beta bursts on dendritic spikes.} burst-effects-emerge-first-cycles⟧

( A ) Example data from the gamma rhythmic inhibition simulation.

Top, somatic potential (black line), with firing rate of perisomatic inhibitory synapses (blue line).

Middle, voltage trace of apical compartment.

Bottom, voltage trace of basal compartment.

( B ) Action potential rate as a function of the phase of the gamma rhythm.

Blue line shows the modulation of inhibitory drive with respect to phase.

( C ) Percent change in Ca 2+ spike presence at apical nexus by gamma phase.

( D1–2 ) Percent change of NMDA spike presence in apical (1) and basal (2) dendrites stratified by electronic distance from the soma.

( E1–2 ) Same as C , but for Na + spikes.

( F, G, H, I1–2, J1–2 ) Same format as above, but with events binned by the phase of beta rhythmic inhibition.

For all graphs, cycle number is given relative to the amplitude peak of the burst.

[panels detected: a, b, c] === Figure 10 === Figure 10. Effect of beta and gamma rhythms on responsiveness to synaptic inputs targeting distinct regions of the dendritic tree.⟦>zach claim=7b7dd3fd-3946-4947-9799-a4f8a8821aba: @{[panels detected: a, b, c] === Figure 10 === Figure 10. Effect of beta and gamma rhythms on responsiveness to synaptic inputs targeting distinct regions of the dendritic tree.} beta-gates-distal-apical-inputs⟧

( A ) Schematic of the location for clustered excitatory synaptic inputs.

( B ) Normalized cross-correlation between synaptic drive onto a clustered input and spiking at the soma, stratified by whether the presynaptic spike arrived during the peak (red line) or trough (blue line) of the rhythm.

Solid bars correspond to the Poisson stimulation case where inhibition was not rhythmically modulated.

Top left, effect of beta on distal inputs.

Top right, effect of gamma on distal inputs.

Bottom left, effect of beta on proximal inputs.

Bottom right, effect of gamma on proximal inputs.

( C ) Summary of effects in panel B where the strength of each normalized cross-correlation was measured as its area under the curve.

Dots are connected by dashed gray lines if the data points came from the same simulation but at different phases of the rhythm.

Solid horizontal lines reflect the cross-correlation strength in the Poisson inhibitory case (no rhythmicity).

[panels detected: a, b, c] === Figure 11 === Figure 11. A summary schematic of the principal findings.⟦>zach claim=no-assertion: @{[panels detected: a, b, c] === Figure 11 === Figure 11. A summary schematic of the principal findings.} A figure title for the summary schematic, asserting nothing on its own.⟧

( A ) The microcircuitry that was simulated in this study.

( B ) Beta rhythmic inhibition to the distal dendrites modulated dendritic spikes.

( C ) Gamma rhythmic inhibition to the perisomatic region modulated action potential initiation.

AP stands for action potentials.

[panels detected: a, b, c]


## tables

Table 1. Inputs to layer 5 (L5) PN.⟦>zach claim=no-assertion: @{Table 1. Inputs to layer 5 (L5) PN.} A table title.⟧

L5 PN dendrites can course up to L1 and receive both excitatory and inhibitory inputs to their dendrites.

Here, we quantified, where possible, the experimental values for synaptic magnitude, firing rate, divergence, and release probability.

We matched the model parameters to the experimental values as closely as possible while preserving a reasonable basal firing rate.

Synapse type Characteristics Model Experimental Excitatory (basal) Magnitude of EPSCs 37.0±32.3 pA 30.6±29.9 pA Morishima et al., 2011 Firing rate 4.43±2.9 Hz 4.43±2.9 Hz (Headley personal comm.

Divergence 2–8 2–8 ( Markram et al., 1997 ; Reimann et al., 2015 ; Deuchars et al., 1994 ) Number of synapses 10042 10042 ( Karimi et al., 2020 ) Release probability 0.53±0.22 0.53±0.22 ( Brémaud et al., 2007 ) Excitatory (apical) Magnitude 25.9±24.9 pA 30.6±29.9 pA ( Morishima et al., 2011 ) Firing rate 4.43±2.9 Hz 4.43±2.9 Hz (Headley personal comm.

Divergence 2–8 2–8 ( Markram et al., 1997 ; Reimann et al., 2015 ; Deuchars et al., 1994 ) Number of synapses 16070 16070 ( Karimi et al., 2020 ) Release probability 0.53±0.22 0.53±0.22 ( Brémaud et al., 2007 ) Inhibitory (perisomatic and somatic) Magnitude 162.5±103.1 pA 208.3±58.7 pA ( Xiang et al., 2002 ) Firing rate 16.9±14.3 Hz 16.9±14.3 Hz ( Yu et al., 2019 ) Divergence 2.8±1.9 2.8±1.9 Number of synapses 406 406 ( Karimi et al., 2020 ) Release probability 0.88±0.05 0.88±0.05 ( Xiang et al., 2002 ) Inhibitory (basal) Magnitude 24.3±18.4 pA 26.5±1.6 pA ( Xiang et al., 2002 ) Firing rate 3.9±4.9 Hz 3.9±4.9 Hz ( Yu et al., 2019 ) Divergence 2.7±1.6 2.7±1.6 ( Tanaka et al., 2011 ; Thomson et al., 1996 ) Number of synapses 1023 1023 ( Karimi et al., 2020 ; Jadi et al., 2012 ) Release probability 0.72±0.10 0.72±0.10 ( Xiang et al., 2002 ) Inhibitory (apical) Magnitude 24.3±33.1 pA 26.5±1.6 pA ( Xiang et al., 2002 ) Firing rate 3.9±4.9 Hz 3.9±4.9 Hz ( Yu et al., 2019 ) Divergence 12±3 12±3 ( Silberberg and Markram, 2007 ; Vezoli et al., 2021 ) Number of synapses 1637 1637 ( Karimi et al., 2020 ) Release probability 0.30±0.08 0.30±0.08 ( Silberberg and Markram, 2007 ) Table 2. Short-term presynaptic plasticity.⟦>zach claim=no-assertion: @{Divergence 2–8 2–8 ( Markram et al., 1997 ; Reimann et al., 2015 ; Deuchars et al., 1994 ) Number of synapses 16070 16070 ( Karimi et al., 2020 ) Release probability 0.53±0.22 0.53±0.22 ( Brémaud et al., 2007 ) Inhibitory (perisomatic and somatic) Magnitude 162.5±103.1 pA 208.3±58.7 pA ( Xiang et al., 2002 ) Firing rate 16.9±14.3 Hz 16.9±14.3 Hz ( Yu et al., 2019 ) Divergence 2.8±1.9 2.8±1.9 Number of synapses 406 406 ( Karimi et al., 2020 ) Release probability 0.88±0.05 0.88±0.05 ( Xiang et al., 2002 ) Inhibitory (basal) Magnitude 24.3±18.4 pA 26.5±1.6 pA ( Xiang et al., 2002 ) Firing rate 3.9±4.9 Hz 3.9±4.9 Hz ( Yu et al., 2019 ) Divergence 2.7±1.6 2.7±1.6 ( Tanaka et al., 2011 ; Thomson et al., 1996 ) Number of synapses 1023 1023 ( Karimi et al., 2020 ; Jadi et al., 2012 ) Release probability 0.72±0.10 0.72±0.10 ( Xiang et al., 2002 ) Inhibitory (apical) Magnitude 24.3±33.1 pA 26.5±1.6 pA ( Xiang et al., 2002 ) Firing rate 3.9±4.9 Hz 3.9±4.9 Hz ( Yu et al., 2019 ) Divergence 12±3 12±3 ( Silberberg and Markram, 2007 ; Vezoli et al., 2021 ) Number of synapses 1637 1637 ( Karimi et al., 2020 ) Release probability 0.30±0.08 0.30±0.08 ( Silberberg and Markram, 2007 ) Table 2. Short-term presynaptic plasticity.} Raw model-parameter rows drawn from cited measurements, which the paper's parameterization claim already frames as inputs rather than findings.⟧

Parameters were tuned to match experimental recordings reported in Campagnola et al., 2022 .

Synapse type tau D 1 (ms) d 1 tau D 2 (ms) d 2 Synaptic current @ 20 Hz Train induction vs. frequency Excitatory 35 0.95 250 0.8 Perisomatic inhibition 40 0.7 500 0.7 Dendritic inhibition 200 0.8 1 1
