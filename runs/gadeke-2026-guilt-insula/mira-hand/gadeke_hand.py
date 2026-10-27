#!/usr/bin/env python3
"""Gädeke et al. 2026 (eLife 105391, Reviewed Preprint v2) as a hand-built MIRA graph.

Built for eLife Pathways' claims-tree prototype, against the text their page serves (v2), so that
every anchor docks to it. MIRA's seven node types and eight relations, plus three declared
subclasses: Hypothesis and Alternative (of Claim), Check (of Evidence). Every node carries a
statement (`text`), a plain-language summary (`description`) and a verbatim anchor; every
Evidence names its study and its figure panel or table; every figure panel is accounted for.

Run:  python3 gadeke_hand.py            → gadeke-hand.graph.json (extractor shape) + .mira.jsonld + report
The builder refuses to emit if any anchor is not found character-for-character in gadeke-v2.txt.
"""
import json, os, re, sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TEXT = open(os.path.join(HERE, "gadeke-v2.txt"), encoding="utf-8").read()
PAPER_DOI = "https://doi.org/10.7554/eLife.105391.2"

N = []   # nodes
E = []   # edges

def node(id, type, text, description, anchor, subtype=None, **extra):
    n = {"id": id, "type": type, "text": text, "description": description, "anchor": anchor}
    if subtype: n["subtype"] = subtype
    n.update(extra); N.append(n); return id

def edge(relation, subject, object, anchor=None):
    e = {"relation": relation, "subject": subject, "object": object}
    if anchor: e["anchor"] = anchor
    E.append(e)

# ═══════════════════════════════════════════════════════════════════════════════════════════
# QUESTIONS — one per hypothesis the paper commits to
# ═══════════════════════════════════════════════════════════════════════════════════════════
node("q1", "Question",
     "How does being responsible for a risky choice that affects a partner change how the decision-maker feels?",
     "The behavioural question. The paper's answer is interpersonal guilt, defined operationally as feeling worse about a partner's bad outcome when you caused it than when they did; the alternatives are the other answers.",
     "The neural mechanisms underlying guilt evoked during such situations of social responsibility are still unknown.")
node("q2", "Question",
     "Which brain regions carry guilt and responsibility for a partner's outcomes, and how do they interact with prefrontal cortex?",
     "The imaging question: where the guilt effect shows up (the paper's answer: anterior insula), what tracks responsibility for the partner's surprises as such (left STS), and how these regions couple with prefrontal cortex during choice.",
     "Next we sought to uncover the neural mechanisms associated with our guilt effect")

# ═══════════════════════════════════════════════════════════════════════════════════════════
# STUDIES, PROTOCOLS, SOURCE DOCUMENTS
# ═══════════════════════════════════════════════════════════════════════════════════════════
node("st1", "Study", "Study 1: behavioural experiment, 40 participants, three sessions outside the scanner",
     "Participants chose between safe and risky options for themselves (Solo), for themselves and a partner (Social), or watched the partner choose (Partner), rating happiness every two trials. The partner was another participant.",
     "40 healthy participants (14 male, mean age 26.1, range 22 to 31) participated in Study 1 (behaviour only study)")
node("st2", "Study", "Study 2: fMRI experiment, 44 participants, two sessions in the scanner",
     "The same task inside a 3T scanner, with longer and variable intervals between events; the partner was an experimenter. All brain results come from this study.",
     "44 healthy participants (19 male, mean (SD) age = 30.6 (6.5), range 23 to 50) participated in Study 2 (fMRI study)")

node("p_task", "Protocol", "Lottery choice task with Solo, Social and Partner conditions",
     "On each trial a safe amount against a lottery with two equiprobable outcomes. Solo: the choice affects only the participant. Social: the participant chooses for both. Partner: the partner chooses for both. In Social and Partner, each player's lottery is drawn independently.",
     "participants were presented with pairs of monetary options (a safe and a risky option; the risky option was a lottery with equally probable high and low outcomes)")
node("p_partner", "Protocol", "Partner choices simulated by an expected-value-maximising algorithm",
     "To keep the partner's behaviour identical across participants, the partner's choices were made by an algorithm that always picked the higher expected value. Participants were not told.",
     "We contrasted this condition with similar choices made by a simple expected-value-maximizing algorithm posing for the partner")
node("p_ice", "Protocol", "Icebreaker game to create a social bond before the task",
     "Participant and partner met for about fifteen minutes and played a cooperative game, so that the partner's outcomes would matter emotionally.",
     "participants were paired with a partner and played an “ice-breaker” game that created a positive social bond between them")
node("p_happy", "Protocol", "Momentary happiness probe every two trials",
     "After every second outcome, participants rated how happy they felt on a continuous scale; the ratings are the dependent measure for the behavioural analyses.",
     "Momentary happiness was assessed every two trials in a similar manner to previous studies by Rutledge and colleagues")
node("p_risk", "Protocol", "Risk-attitude estimation: risk premium and CARA expected utility",
     "Two measures of how risk-averse each participant was in each condition: a risk premium from a fitted logistic regression, and a constant-absolute-risk-aversion parameter ρ from expected utility theory.",
     "we calculated for each participant a “risk premium”, defined as the difference between the expected value of a lottery and its certainty equivalent")
node("p_models", "Protocol", "Five computational models of momentary happiness",
     "Basic, Inequality, Guilt-envy, Responsibility and Responsibility Redux: exponentially decaying influences of certain rewards, expected values and reward prediction errors, with the Responsibility models adding the partner's prediction errors split by who chose. Compared by AIC, BIC, R² and likelihood-ratio tests; parameter recovery on synthetic data.",
     "we fitted computational models to each participant’s happiness data")
node("p_lmm", "Protocol", "Linear mixed models of happiness after lottery outcomes",
     "Happiness after Social and Partner lottery outcomes modelled with the participant's outcome, the partner's outcome, who chose, and their interactions; the guilt effect is the partner-outcome × decision-maker interaction.",
     "we analysed happiness values reported after outcomes of lottery choices in the Social and Partner conditions using conventional linear mixed models")
node("p_fmri", "Protocol", "fMRI acquisition, GLMs and region-of-interest mixed models",
     "3T EPI BOLD; a conventional GLM of the trial events (GLM1) and a model-based GLM with the Responsibility model's variables as regressors (GLM2); regions of interest from the lottery-versus-safe outcome contrast analysed with linear mixed models.",
     "We analysed the BOLD responses of brain regions engaged during decision-making and at the time of receiving the outcomes of the choice using conventional as well as computational model-based analyses")
node("p_ppi", "Protocol", "Seed-to-voxel psychophysiological interaction from left insula and left STS",
     "Whole-brain connectivity during the choice phase from two seeds, looking for a Condition × Choice interaction.",
     "we used the left insula and left STS as seed regions for whole-brain seed-to-voxel psychophysiological interaction analyses")
node("p_grbs", "Protocol", "Comparison with the published guilt-related brain signature",
     "Each participant's guilt-related activation map was projected onto Yu et al.'s multivariate guilt signature; a positive dot product means resemblance.",
     "we compared this brain signature to the neural responses obtained in our task")

for st in ("st1", "st2"):
    for p in ("p_task", "p_partner", "p_ice", "p_happy", "p_risk", "p_models", "p_lmm"):
        edge("follows", st, p)
for p in ("p_fmri", "p_ppi", "p_grbs"):
    edge("follows", "st2", p)

node("s_paper", "SourceDocument", "Gädeke et al. (2026), Contributions of insula and superior temporal sulcus to interpersonal guilt and responsibility in social decisions, eLife 105391 v2",
     "The paper this graph is extracted from.", "Contributions of insula and superior temporal sulcus to interpersonal guilt and responsibility in social decisions", doi=PAPER_DOI)
edge("describesActivity", "s_paper", "st1"); edge("describesActivity", "s_paper", "st2")

# cited works the argument leans on — each with the study it reports and the one finding used here
BIB = {   # reference-list entries as the eLife page gives them
    "rutledge": {"doi": "10.1038/ncomms11825", "fields": {"authors": ["Rutledge RB", "de Berker AO", "Espenhahn S", "Dayan P", "Dolan RJ"], "year": 2016, "journal": "Nature Communications", "volume": "7", "pages": "11825", "title": "The social contingency of momentary subjective well-being"}},
    "edelson": {"doi": "10.1126/science.aat0036", "fields": {"authors": ["Edelson MG", "Polania R", "Ruff CC", "Fehr E", "Hare TA"], "year": 2018, "journal": "Science", "volume": "361", "pages": "eaat0036", "title": "Computational and neurobiological foundations of leadership decisions"}},
    "yu2014": {"doi": "10.1093/scan/nst090", "fields": {"authors": ["Yu H", "Hu J", "Hu L", "Zhou X"], "year": 2014, "journal": "Social Cognitive and Affective Neuroscience", "volume": "9", "pages": "1150–1158", "title": "The voice of conscience: neural bases of interpersonal guilt and compensation"}},
    "yu2020": {"doi": "10.1093/cercor/bhz326", "fields": {"authors": ["Yu H", "Koban L", "Chang LJ", "Wagner U", "Krishnan A", "Vuilleumier P", "Zhou X", "Wager TD"], "year": 2020, "journal": "Cerebral Cortex", "volume": "30", "pages": "3558–3572", "title": "A generalizable multivariate brain pattern for interpersonal guilt"}},
}
for b in BIB.values():
    f = b["fields"]; b["entry"] = f"{', '.join(f['authors'])} ({f['year']}). {f['title']}. {f['journal']} {f['volume']}:{f['pages']}."
cited = [
    ("rutledge", "Rutledge et al. (2016)", "The paper whose happiness-modelling method this study adopts and extends to a social setting.",
     "Following Rutledge and colleagues’ methodology, which considers that changes in momentary happiness in response to outcomes of a probabilistic reward task are explained by the combined influence of recent reward expectations and prediction errors",
     "Changes in momentary happiness during a probabilistic reward task are explained by recent reward expectations and the prediction errors arising from them.", "f_rewards"),
    ("edelson", "Edelson et al. (2018)", "The leadership study this paper compares its agency effect and its connectivity results with.",
     "most participants displayed responsibility aversion, and this effect could not be explained by guilt, suggesting people associate a psychological cost with assuming responsibility for others’ outcomes",
     "Most participants show responsibility aversion — a psychological cost of deciding for others — that guilt does not explain.", "f_agency"),
    ("yu2014", "Yu et al. (2014)", "The guilt paradigm that motivates the insula hypothesis.",
     "The level of pain taken, indicative of guilt, and activations in anterior middle cingulate cortex and aIns were higher when the pain followed errors made only by the participant rather than by both players",
     "Anterior insula and anterior middle cingulate activity were higher when a partner's pain followed the participant's own errors.", "h2"),
    ("yu2020", "Yu et al. (2020)", "The source of the guilt-related brain signature this paper uses as an external yardstick.",
     "A multivariate reanalysis of these two datasets revealed a neural signature for guilt (Yu et al., 2020)",
     "A multivariate reanalysis of two guilt studies yields a distributed guilt-related brain signature spanning anterior midcingulate, insula, IFG, inferior temporal cortex, thalamus and cerebellum.", "f_grbs"),
]
# A cited finding is Evidence whose sourceDocument is the cited work. MIRA's full provenance spine
# would add a Study the cited work describes; the extractor's own prompt allows omitting that chain
# when the study is not identified, and a placeholder Study carries nothing, so it is collapsed.
for key, label, desc, anchor, finding, target in cited:
    node(f"s_{key}", "SourceDocument", BIB[key]["entry"], desc, anchor, doi=BIB[key]["doi"], url="https://doi.org/" + BIB[key]["doi"], **BIB[key]["fields"])
    node(f"e_{key}", "Evidence", finding, f"Cited finding from {label}, as this paper states it.", anchor, subtype="Cited", sourceDocument=f"s_{key}", panel=f"cited: {label}")
    edge("supports", f"e_{key}", target)

# ═══════════════════════════════════════════════════════════════════════════════════════════
# HYPOTHESES (Claim / Hypothesis)
# ═══════════════════════════════════════════════════════════════════════════════════════════
node("h1", "Claim", "Responsibility for a social choice that yields a low outcome for a partner produces interpersonal guilt, felt as a larger decrease in momentary happiness than when the partner made the same choice.",
     "The paper's central bet: it is being responsible for the partner's bad outcome, not the bad outcome itself, that hurts.",
     "choosing a risky option in such a case may evoke guilt when the outcome for others is negative", subtype="Hypothesis")
node("h2", "Claim", "The anterior insula is the neural substrate of that guilt, responding more when the participant is responsible for a low outcome affecting the partner.",
     "The insula has been linked to guilt in earlier work; the bet is that it carries the guilt effect here.",
     "Given the documented association between anterior insula and guilt (see Introduction)", subtype="Hypothesis")
node("h3", "Claim", "Connectivity between the guilt- and responsibility-related regions and prefrontal cortex changes with who decides and with the type of choice.",
     "A bet about how the insula and STS talk to prefrontal cortex during choice, depending on whether the choice is risky and whether it affects the partner.",
     "We hypothesized that connectivity with regions that showed guilt- and responsibility-related responses during the outcome phase (see previous paragraph) might change depending on whether participants made decisions for themselves only or for themselves and their partner", subtype="Hypothesis")
node("h4", "Claim", "A neural substrate tracks the participant's responsibility for the partner's outcomes, representing the partner's reward prediction errors more strongly when they arise from the participant's own choice.",
     "A bet about responsibility rather than guilt: some region should care who caused the partner's surprise, good or bad.",
     "search for networks sensitive to reward prediction errors resulting from participant or partner choices", subtype="Hypothesis")
edge("addresses", "h1", "q1"); edge("addresses", "h2", "q2"); edge("addresses", "h3", "q2"); edge("addresses", "h4", "q2")

# ═══════════════════════════════════════════════════════════════════════════════════════════
# FINDINGS (Claim) — the results as propositions, one per figure-panel group
# ═══════════════════════════════════════════════════════════════════════════════════════════
node("f_guilt", "Claim", "Responsibility for a partner's bad lottery outcomes decreases participant happiness more than the same outcomes following partner choices, consistent with interpersonal guilt.",
     "The guilt effect, in both studies: the same bad outcome for the partner hurts more when you caused it. Figure 3D and 3H. The authors read it as 'simple guilt'.",
     "When the partner received the low lottery outcome, participant happiness was lower when they rather than the partner had chosen the lottery")
node("f_model", "Claim", "Computational models incorporating partner reward prediction errors differentiated by decision-maker (participant vs partner) best explain momentary happiness variations.",
     "Of five computational models, the Responsibility model wins the likelihood-ratio tests in both studies, and the term for the partner's surprises caused by the participant is reliably positive. Table 1, Figure 3C and 3G.",
     "the Responsibility model fitted better than all the other models, including the Responsibility Redux model")
node("f_ownrpe", "Claim", "The participant's own reward prediction errors influenced happiness more than the partner's.",
     "Responsibility matters, but one's own surprises matter more.",
     "Participants’ reward prediction errors (sRPE) influenced happiness more than partner’s reward prediction errors")
node("f_rewards", "Claim", "Momentary happiness tracked the rewards both the participant and the partner received on the current trial.",
     "The basic premise of the modelling, replicated here: happiness follows recent rewards, one's own and the partner's. Figure 3A, 3B, 3E, 3F.",
     "participant momentary happiness correlated with rewards obtained in the current trial by the participant and by the partner")
node("f_agency", "Claim", "Being the decision-maker lowered happiness, independent of the outcome.",
     "A separate finding, not the guilt effect: deciding for others costs something even when nothing bad happens. The authors read it as the 'weight of responsibility', as in Edelson et al.",
     "found happiness to be lower when the participant chose, independent of the outcome")
node("f_null_good", "Claim", "Responsibility did not change happiness after good outcomes for the partner.",
     "The guilt effect is specific to bad outcomes, as guilt predicts.",
     "Responsibility for choices did not influence happiness following positive lottery outcomes for the partner")
node("f_risk", "Claim", "Participants show similar risk preferences when deciding for themselves versus for themselves and a partner, with a tendency toward higher risk aversion in the Social condition only in Study 1.",
     "Risk premiums did not differ in either study; the ρ parameter was slightly higher in Social in Study 1 only. Figure 2. The authors conclude they have no strong evidence of a difference.",
     "participants showed very similar risk preferences when making decisions affecting only themselves (Solo condition) or themselves and their partner (Social condition)")
node("f_insula", "Claim", "The guilt effect is associated with increased BOLD signal in the left anterior insula.",
     "The guilt effect in the brain: insula regions of interest mirrored the behavioural interaction, and a voxel-wise analysis found a small left anterior insula cluster doing the same. Figure 4E and 4F.",
     "activation in our insula ROIs increased in situations during which participants experienced guilt for low outcomes impacting their partner")
node("f_ppi_insula", "Claim", "Functional connectivity between the left anterior insula and the right inferior frontal gyrus varies with choice and condition: highest for risky choices for oneself and safe choices for both players.",
     "How the insula talks to prefrontal cortex depends on what is chosen and for whom. Figure 5. The authors suggest the right IFG is sensitive to guilt-related information.",
     "a cluster in the right inferior frontal gyrus (IFG) whose connectivity to the insula (the seed region) was highest when participants made Risky choices for themselves and Safe choices for both players")
node("c_ifg", "Claim", "The right inferior frontal gyrus is sensitive to guilt-related information during social choices.",
     "The authors' reading of the connectivity result: a prefrontal region whose coupling with the insula tracks what is chosen and for whom.",
     "suggesting that this part of prefrontal cortex is sensitive to guilt-related information during social choices")
edge("supports", "f_ppi_insula", "c_ifg"); edge("supports", "c_ifg", "h3")
node("f_ppi_sts", "Claim", "Connectivity between the left STS and left inferior frontal gyrus showed the opposite pattern, but did not survive correction.",
     "A weak, uncorrected result the authors call anecdotal, read as information from STS being relayed to IFG. Supplementary Figure 2.",
     "connectivity with the left STS (the seed region) showed the opposite pattern")
node("f_sts", "Claim", "The left superior temporal sulcus tracks partner reward prediction errors specifically when they result from the participant's choices.",
     "The responsibility signal: a region that tracks the partner's surprises more when the participant caused them. Figure 4H and 4I. The authors read it as monitoring the consequences of one's decisions on others.",
     "We found this effect in one cluster within the left STS")
node("f_network", "Claim", "Choosing for both oneself and the partner, rather than for oneself alone, engaged the precuneus, left temporo-parietal junction and medial prefrontal cortex.",
     "The social-decision network, replicating earlier work; precuneus and TPJ were most active for risky choices in the Social condition. Figure 4B and 4C.",
     "Three significant clusters of voxels were identified (Figure 4B and Supplementary Table 3), in the precuneus")
node("f_outcome_net", "Claim", "Receiving lottery outcomes, compared with safe outcomes, engaged bilateral anterior insula, dorsomedial prefrontal cortex, right STS, ventral striatum, right dorsolateral prefrontal cortex and inferior parietal lobe.",
     "The regions sensitive to risky outcomes, which define the regions of interest for the guilt analyses. Figure 4D.",
     "Cluster of voxels more active during receipt of lottery outcomes than outcomes of safe choices were identified in the bilateral anterior insula")
node("f_grbs", "Claim", "The guilt-related activation patterns resembled the published guilt-related brain signature.",
     "Convergent evidence that what the insula analysis found is guilt: individual maps projected positively onto Yu et al.'s signature, though the match did not track individual differences in the behavioural effect.",
     "The “neurometrics” analysis of our guilt-related activation maps showed a significant similarity to a published guilt-related brain signature")

# findings support hypotheses
for f, h in [("f_guilt", "h1"), ("f_model", "h1"), ("f_null_good", "h1"), ("f_insula", "h2"), ("f_grbs", "h2"),
             ("f_ppi_insula", "h3"), ("f_ppi_sts", "h3"), ("f_sts", "h4")]:
    edge("supports", f, h)
# findings that bear on a question without testing a hypothesis address it directly, so a
# question → claims tree has somewhere to put them
for f, q in [("f_rewards", "q1"), ("f_ownrpe", "q1"), ("f_agency", "q1"), ("f_risk", "q1"), ("f_network", "q2"), ("f_outcome_net", "q2")]:
    edge("addresses", f, q)

# ═══════════════════════════════════════════════════════════════════════════════════════════
# ALTERNATIVES (Claim / Alternative) — stated as their proponent would
# ═══════════════════════════════════════════════════════════════════════════════════════════
node("a_own", "Claim", "The larger drop in happiness after the partner's low outcome is disappointment at the participant's own outcome, not guilt about the partner's.",
     "Rival to the guilt reading. Argued against: the effect holds whether the participant's own lottery came out high or low.",
     "The “guilt effect” occurred whether the participant received the high lottery outcome", subtype="Alternative")
node("a_general", "Claim", "Being responsible simply amplifies the participant's reaction to all of the partner's outcomes, good or bad.",
     "Rival to the guilt reading. Argued against: responsibility made no difference after good partner outcomes.",
     "Responsibility for choices did not influence happiness following positive lottery outcomes for the partner", subtype="Alternative")
node("a_risk", "Claim", "Choosing for two people changes how much risk participants take, so the differences between conditions reflect different choices rather than guilt.",
     "Rival, handled by checking risk attitudes directly. Risk premiums did not differ; a slight shift in ρ in Study 1 gives it weak support. The authors conclude they have no strong evidence of a difference.",
     "To better assess whether people’s risk preferences varied between the Solo and the Social condition", subtype="Alternative")
node("a_inequality", "Claim", "Happiness tracks the inequality between the participant's and the partner's rewards; responsibility for the partner's surprises adds nothing.",
     "Rival account built into the model comparison as the Inequality and Guilt-envy models. Argued against: the Responsibility model beat both in both studies.",
     "we assessed the fit of an ‘Inequality’ model that included one term modelling the difference between the participant and partner outcomes", subtype="Alternative")
node("a_emotion", "Claim", "What participants felt was empathy for the partner, a sense of failure or bad luck, or some emotion other than guilt.",
     "Raised by the authors themselves, since no one was asked what they felt. Left open on the behavioural measure ('we cannot exclude'), then argued against on the neural one: the activation maps resembled a published guilt signature, 'we thus believe that our participants did experience guilt'.",
     "we cannot exclude the possibility that they have instead or in addition felt empathy for their partner, a feeling of failure or bad luck, or some other emotion", subtype="Alternative")
node("a_algorithm", "Claim", "Because the partner's choices were really an algorithm, participants were emotionally detached from the partner's outcomes and the effects do not reflect a social interaction.",
     "A limitation the authors raise and answer: partner outcomes did move participants' happiness, so they were not detached.",
     "The first limitation is that the partner’s decisions were in fact taken by an algorithm", subtype="Alternative")
for a, q in [("a_own", "q1"), ("a_general", "q1"), ("a_risk", "q1"), ("a_inequality", "q1"), ("a_emotion", "q1"), ("a_algorithm", "q1")]:
    edge("addresses", a, q)

# ═══════════════════════════════════════════════════════════════════════════════════════════
# EVIDENCE — one node per study and panel/statistic; Check marks a result that defends rather than argues
# ═══════════════════════════════════════════════════════════════════════════════════════════
IIIF = "https://iiif.elifesciences.org/epp/105391%2Fv2%2Fcontent%2F107300v6_{key}.tif/full/{w},/0/default.jpg"
PAGE = "https://epp.elifepathways.org/mira/105391#{key}"
def figure_for(panel):
    m = re.match(r"(Figure|Table) (\d)", panel)
    if not m: return None
    key = ("fig" if m.group(1) == "Figure" else "tbl") + m.group(2)
    return {"label": panel, "image": IIIF.format(key=key, w="max"), "thumbnail": IIIF.format(key=key, w=480), "page": PAGE.format(key=key)}

def ev(id, study, panel, text, anchor, supports=(), opposes=(), check=False, description=None):
    desc = (f"{'Check. ' if check else ''}{study.replace('st', 'Study ')} · {panel}." + (f" {description}" if description else ""))
    fig = figure_for(panel)
    node(id, "Evidence", text, desc, anchor, subtype="Check" if check else None, sourceDocument=PAPER_DOI, panel=panel, study=study, **({"figure": fig} if fig else {}))
    edge("grounds", study, id)
    for s in supports: edge("supports", id, s)
    for o in opposes: edge("opposes", id, o)

# behaviour: choices
ev("e_value_s1", "st1", "Figure 2A", "In Study 1, the probability of choosing the lottery rose with the lottery's expected-value advantage over the safe option (t(4796) = 9.26, p < 3.1e-20, β = 0.074).",
   "participants’ probability of choosing the risky option (lottery) increased with the difference between the expected value of the lottery and the value of the safe option", supports=("f_guilt",), check=True, description="Manipulation check: choices were value-sensitive, so the behavioural measures mean something.")
ev("e_value_s2", "st2", "Figure 2D", "In Study 2, the probability of choosing the lottery rose with its expected-value advantage (t(3829) = 10.62, p < 5.3e-26, β = 0.093).",
   "Study 2: Figure 2D, t(3829) = 10.62, p < 5.3e-26, β = 0.093", supports=("f_guilt",), check=True, description="Manipulation check, Study 2.")
ev("e_choice_s1", "st1", "Figure 2A", "In Study 1, participants chose the lottery more often in the Solo than the Social condition (t(4796) = 2.54, p = 0.011, β = 0.164).",
   "Participants chose the lottery more often in the Solo condition than in the Social condition in Study 1 (t(4796) = 2.54, p = 0.011, β = 0.164", supports=("f_risk", "a_risk"))
ev("e_choice_s2", "st2", "Figure 2D", "In Study 2, lottery choice did not differ between Solo and Social (t(3829) = 0.23, p = 0.82, β = 0.015).",
   "this difference was not found in Study 2 (t(3829) = 0.23, p = 0.82, β = 0.015", supports=("f_risk",), opposes=("a_risk",))
ev("e_ev_x_cond", "st1", "Figure 2A, 2D", "The expected-value effect on choice did not interact with condition in either study (p > 0.52).",
   "There was no significant interaction between the difference in expected values and experimental conditions in either study (p > 0.52)", supports=("f_risk",), opposes=("a_risk",))
ev("e_premium_s1", "st1", "Figure 2B", "In Study 1, risk premiums did not differ between Social and Solo (t(39) = 1.53, p = 0.134, d = 0.24, BF10 = 0.49).",
   "Risk premiums did not differ between Social and Solo conditions (Study 1: Figure 2B, t(39) = 1.53, p = 0.134, Cohen’s d = 0.24, BF10 = 0.49", supports=("f_risk",), opposes=("a_risk",))
ev("e_premium_s2", "st2", "Figure 2E", "In Study 2, risk premiums did not differ between Social and Solo (t(43) = -0.21, p = 0.84, d = -0.03, BF10 = 0.17).",
   "Study 2: Figure 2E, t(43) = -0.21, p = 0.84, d = -0.03, BF10 = 0.17", supports=("f_risk",), opposes=("a_risk",))
ev("e_rho_gainloss", "st1", "Methods", "The risk-aversion parameter ρ did not differ between gain and loss trials in either study (Study 1: t(17) = 0.21, p = 0.84; Study 2: t(15) = -0.61, p = 0.55), justifying pooling.",
   "As ρ did not vary between gain and loss trials (Study 1: t(17) = 0.21, p = 0.84, d = 0.05; Study 2: t(15) = - 0.61, p = 0.55, d = 0.15; paired t-test)", supports=("f_risk",), check=True, description="Assumption check before pooling gain and loss trials.")
ev("e_rho_s1", "st1", "Figure 2C", "In Study 1, ρ was slightly higher in the Social than the Solo condition (t(39) = 2.27, p = 0.03, d = 0.36, BF10 = 1.69).",
   "participants were slightly more risk averse in the Social than in the Solo condition in Study 1 (Figure 2C, t(39) = 2.27, p = 0.03, d = 0.36, BF10 = 1.69)", supports=("f_risk", "a_risk"), description="The one result that gives the risk-attitude alternative any support; the authors note ρ could be estimated in only 18 of 40 participants.")
ev("e_rho_s2", "st2", "Figure 2F", "In Study 2, ρ did not differ between Social and Solo (t(43) = 1.40, p = 0.17, d = 0.21, BF10 = 0.41).",
   "but not in Study 2 (Figure 2F, t(43) = 1.40, p = 0.17, d = 0.21, BF10 = 0.41)", supports=("f_risk",), opposes=("a_risk",))
ev("e_rho_premium", "st1", "Figure 2", "Risk premium and ρ were highly consistent across participants in both conditions and both studies (all F > 42, p < 0.001, R² 0.55–0.65).",
   "Risk premium and ρ were highly consistent with each other across participants in both conditions for both studies", supports=("f_risk",), check=True, description="Convergence of the two risk measures.")

# behaviour: happiness and models
ev("e_rewards_s1", "st1", "Figure 3A, 3B", "In Study 1, happiness correlated with the participant's reward (F(1,3598) = 691.5, R² = 0.16) and the partner's reward (F(1,2426) = 128.6, R² = 0.05) on the current trial.",
   "Correlations with participant reward, Study 1: F(1,3598) = 691.5, p < 0.001, R2 = 0.16; partner reward, Study 1: F(1,2426) = 128.6, p < 0.001, R2 = 0.05", supports=("f_rewards",), opposes=("a_algorithm",))
ev("e_rewards_s2", "st2", "Figure 3E, 3F", "In Study 2, happiness correlated with the participant's reward (F(1,2630) = 650.8, R² = 0.20) and the partner's reward (F(1,1735) = 111.8, R² = 0.06).",
   "participant reward, Study 2: F(1,2630) = 650.8, p < 0.001, R2 = 0.20; partner reward, Study 2: F(1,1735) = 111.8, p < 0.001, R2 = 0.06", supports=("f_rewards",), opposes=("a_algorithm",))
ev("e_lr_s1", "st1", "Table 1", "In Study 1, the Responsibility model fitted better than every other model by likelihood-ratio test (all LR ≥ 47.36, p < 0.0001).",
   "Study 1: all LR ≥ 47.36, p < 0.0001", supports=("f_model",), opposes=("a_inequality",))
ev("e_lr_s2", "st2", "Table 1", "In Study 2, the Responsibility model fitted better than every other model by likelihood-ratio test (all LR ≥ 77.83, p < 0.0001).",
   "Study 2: all LR ≥ 77.83, p < 0.0001", supports=("f_model",), opposes=("a_inequality",))
ev("e_fit_s1", "st1", "Figure 3C, Table 1", "In Study 1 the Responsibility and Responsibility Redux models had the highest R² and adjusted R² and lowest AIC/BIC of the five models.",
   "the Responsibility and Responsibility Redux (Figure 3C and 3G) models explained the data best (highest R2 / adjusted R2 or lowest AIC / BIC)", supports=("f_model",))
ev("e_fit_s2", "st2", "Figure 3G, Table 1", "In Study 2 the Responsibility and Responsibility Redux models likewise explained the happiness data best.",
   "All models explained variations in happiness reasonably well (Table 1 and Supplementary Materials)", supports=("f_model",))
ev("e_weights_s1", "st1", "Table 1", "In Study 1 the weight on the partner's prediction errors from the participant's own choices was above zero (Responsibility model Z = 2.85, p = 0.004; Redux Z = 2.93, p = 0.003).",
   "Responsibility model: Study 1: Z = 2.85, p = 0.004, Study 2: Z = 3.26, p = 0.001", supports=("f_model",))
ev("e_weights_s2", "st2", "Table 1", "In Study 2 that weight was above zero (Responsibility model Z = 3.26, p = 0.001; Redux Z = 3.30, p = 0.001), and tended to exceed the weight on partner-caused errors.",
   "ResponsibilityRedux model: Study 1: Z = 2.93, p = 0.003, Study 2: Z = 3.30, p = 0.001", supports=("f_model",))
ev("e_srpe", "st1", "Table 1", "Weights on the participant's own prediction errors exceeded those on the partner's in both studies (Study 1: all Z > 6.0, p < 0.001; Study 2: all Z > 3.7, p < 0.003).",
   "weights for sRPE were higher than for social_pRPE or partner_pRPE (Study 1: all Z > 6.0, p < 0.001; Study 2: all Z > 3.7, p < 0.003)", supports=("f_ownrpe",))
ev("e_recovery", "st1", "Supplementary Materials", "A parameter-recovery procedure on synthetic data recovered the happiness-model parameters reliably.",
   "The stability of these estimated parameters was verified using a parameter recovery procedure", supports=("f_model",), check=True, description="Parameter recovery for the computational models.")
ev("e_agency_s1", "st1", "Methods / Results", "In Study 1, happiness was lower when the participant chose, independent of outcome (t(3600) = -3.92, p < 0.0001, β = -0.14).",
   "Study 1: t(3600) = -3.92, p < 0.0001, β = -0.14", supports=("f_agency",))
ev("e_agency_s2", "st2", "Methods / Results", "In Study 2, happiness was lower when the participant chose, independent of outcome (t(2870) = -6.07, p < 0.0001, β = -0.24).",
   "Study 2: t(2870) = -6.07, p < 0.0001, β = -0.24", supports=("f_agency",))
ev("e_lmm_select", "st1", "Supplementary Table 2", "Across several linear mixed models, lottery outcomes and the identity of the decision-maker both influenced happiness.",
   "Fitting several models revealed that lottery outcomes influenced happiness, and that the identity of the decision-maker played a role", supports=("f_guilt",), check=True, description="Model selection for the happiness LMMs.")
ev("e_guilt_s1", "st1", "Figure 3D", "In Study 1, the partner-outcome × decision-maker interaction on happiness was significant (t(1180) = 3.52, p = 0.0004, β = 0.37).",
   "Study 1: t(1180) = 3.52, p = 0.0004, β = 0.37", supports=("f_guilt",))
ev("e_guilt_s2", "st2", "Figure 3H", "In Study 2, the partner-outcome × decision-maker interaction on happiness was significant (t(937) = 2.85, p = 0.0045, β = 0.33).",
   "Study 2: t(937) = 2.85, p = 0.0045, β = 0.33", supports=("f_guilt",))
ev("e_ownhigh", "st1", "Figure 3D, 3H", "The guilt effect held when the participant's own outcome was high (Study 1: t(39) = -3.58, p < 0.001, d = 0.56, BF10 = 32; Study 2: t(43) = -2.68, p = 0.01, d = 0.4, BF10 = 3.8).",
   "Study 1: t(39) = -3.58, p < 0.001, d = 0.56, BF10 = 32; Study 2: t(43) = -2.68, p = 0.01, d = 0.4, BF10 = 3.8", supports=("f_guilt",), opposes=("a_own",))
ev("e_ownlow", "st1", "Figure 3D, 3H", "The guilt effect held when the participant's own outcome was low (Study 1: t(39) = -3.39, p = 0.002, d = 0.54, BF10 = 19; Study 2: t(43) = -3.58, p < 0.001, d = 0.54, BF10 = 33.5).",
   "Study 1: t(39) = -3.39, p = 0.002, d = 0.54, BF10 = 19; Study 2: t(43) = -3.58, p < 0.001, d = 0.54, BF10 = 33.5", supports=("f_guilt",), opposes=("a_own",))
ev("e_null_good", "st1", "Results", "After good outcomes for the partner, responsibility did not affect happiness in either study (all |t| < 1.3, p > 0.2, BF10 < 0.2).",
   "both studies, all |t| < 1.3, p > 0.2, BF10 < 0.2", supports=("f_null_good",), opposes=("a_general",))

# imaging (Study 2)
ev("e_vs_risky", "st2", "Figure 4A", "Bilateral ventral striatum responded more when participants chose the lottery than the safe option (d = 0.72 left, 0.85 right), replicating earlier work.",
   "found such responses in the bilateral ventral striatum (Cohen’s d = 0.72 and 0.85 in the left and right clusters, respectively", supports=("f_insula", "f_network"), check=True, description="Positive control: the pipeline recovers a known effect of risky choice.")
ev("e_social_solo", "st2", "Figure 4B", "Social versus Solo decisions engaged the precuneus (d = 0.79), left TPJ (d = 0.59) and medial prefrontal cortex (d = 0.54).",
   "in the precuneus (d = 0.79), the left temporo-parietal junction (TPJ; d = 0.59) and the medial prefrontal cortex (mPFC; d = 0.54)", supports=("f_network",))
ev("e_precuneus_tpj", "st2", "Figure 4C", "Only precuneus and TPJ showed a larger risky-minus-safe response in Social than in both Solo and Partner conditions.",
   "Only Precuneus and TPJ showed positive differences in both comparisons (Figure 4C)", supports=("f_network",))
ev("e_outcome_net", "st2", "Figure 4D", "Lottery outcomes versus safe outcomes engaged bilateral anterior insula, dmPFC, right STS, ventral striatum, right dlPFC and inferior parietal lobe.",
   "bilateral anterior insula, dorsal mPFC (dmPFC), right superior temporal sulcus (STS), bilateral ventral striatum, right dorsolateral prefrontal cortex, and bilateral inferior parietal lobe (Figure 4D", supports=("f_outcome_net",))
ev("e_insula_roi", "st2", "Figure 4E", "Insula ROIs responded more to the partner's low outcomes in the Social than the Partner condition, also after subtracting responses to high outcomes.",
   "the insulae showed the sought-after effect (see Supplementary Table 6 and Figure 4E)", supports=("f_insula",))
ev("e_insula_voxel", "st2", "Figure 4F", "A voxel-wise analysis found a small left anterior insula cluster responding more to the partner's low outcomes after participant than partner choices (peak T = 3.95, d = 0.59, 22 voxels), surviving small-volume correction (p = 0.024).",
   "We found a weak response in a small cluster within the left anterior insula (peak T = 3.95, d = 0.59, 22 voxels", supports=("f_insula",))
ev("e_vs_model", "st2", "Figure 4G", "Ventral striatum activation increased with expected certain rewards and the expected values of chosen lotteries under the model-based regressor (left pFWE = 0.002, T = 5.63; right pFWE = 0.005, T = 5.46).",
   "activation in bilateral ventral striatum indeed increased with the amount of expected certain rewards and the expected values of chosen lotteries", supports=("f_sts",), check=True, description="Manipulation check for the model-based GLM before it is used to find the STS effect.")
ev("e_sts", "st2", "Figure 4H", "One left STS cluster responded more to the partner's reward prediction errors from participant than partner choices (pFWE = 0.022, T = 4.70, d = 0.53, 100 voxels, peak MNI [-52 -32 0]).",
   "We found this effect in one cluster within the left STS (pFWE = 0.022, T = 4.70, d = 0.53, Z = 4.57, 100 voxels", supports=("f_sts",))
ev("e_sts_sessions", "st2", "Figure 4I", "The STS cluster's responses to partner prediction errors from participant and partner choices are shown for both sessions.",
   "Responses to the computational-model-based regressors coding for partner reward prediction errors resulting from participant and from partner choices in this cluster are shown in Figure 4I", supports=("f_sts",))
ev("e_ppi_insula", "st2", "Figure 5", "Right IFG connectivity with the left insula seed was highest for risky choices for oneself and safe choices for both players (pFWE = 0.020, T = 4.34, d = 0.80, 115 voxels).",
   "pFWE = 0.020, T = 4.34, d = 0.80, Z = 4.21, 115 voxels, peak at MNI [46 16 22]; Figure 5", supports=("f_ppi_insula",))
ev("e_ppi_insula_left", "st2", "Figure 5", "A smaller left IFG cluster showed the same connectivity pattern with the insula seed but did not survive correction (puncorrected = 0.001, T = 4.08, 38 voxels).",
   "A smaller cluster in the left IFG showed the same effect but did not survive correction for multiple tests", supports=("f_ppi_insula",))
ev("e_ppi_sts", "st2", "Supplementary Figure 2", "Left IFG connectivity with the left STS seed showed the opposite pattern — highest for safe choices for oneself and risky choices for both — uncorrected (p = 0.001, T = 4.44, 35 voxels).",
   "connectivity was highest when participants made Safe choices for themselves and Risky choices for both players (puncorrected = 0.001, T = 4.44, Z = 4.30, 35 voxels", supports=("f_ppi_sts",))
ev("e_grbs", "st2", "Results (neurometrics)", "Dot products between individual guilt-related maps and the published guilt signature were overall positive (mean 5.22, median 6.97, sign test p = 0.017, Cliff's delta 0.4).",
   "overall these values were positive (mean = 5.22; median = 6.97; sign test: p = 0.017; Cliff’s Delta = 0.4 = medium effect size", supports=("f_grbs",), opposes=("a_emotion",))
ev("e_grbs_indiv", "st2", "Results (neurometrics)", "The signature match did not correlate with individual behavioural guilt effects (Spearman's ρ = -0.058, p = 0.725).",
   "did not find a significant association [Spearman’s Rho = -0.058, p = 0.725]", description="A null that qualifies the convergent-validity reading; attached to the finding it bears on.")
edge("supports", "e_grbs_indiv", "f_grbs")   # bears on it; the description says how

# ═══════════════════════════════════════════════════════════════════════════════════════════
# REQUESTS — the Discussion's future work
# ═══════════════════════════════════════════════════════════════════════════════════════════
req = [
    ("r_emotions", "Ask participants directly which emotions they felt at each stage of the task, to link subjective experience to the analytical measures of guilt.",
     "asking participants directly about which emotions they have felt during the different stages of this task would allow us to link subjective experience with our analytical measures", ["f_guilt", "a_emotion"]),
    ("r_traits", "Test more participants to assess how personality traits shape the experience and the behavioural and neural correlates of guilt and responsibility.",
     "Testing more participants would allow us to assess the impact of inter-individual variations in personality traits", ["f_guilt", "f_insula"]),
    ("r_trials", "Run more trials so risk preferences can be modelled separately for gains and losses per condition, and to test whether happiness changes affect later choices.",
     "Using more trials in the experiment would allow separate modelling of risk preferences in gain and loss trials in each experimental condition", ["f_risk"]),
    ("r_partners", "Vary the partner's identity — friend, stranger, artificial agent — to measure social discounting of guilt and responsibility.",
     "Varying partner identities (friends, stranger, artificial agent) could reveal the impact of social discounting on guilt and responsibility", ["f_guilt", "a_algorithm"]),
    ("r_feedback_ppi", "Run the connectivity analyses on the outcome (feedback) phase of the task.",
     "Functional connectivity analyses could also be performed for the data obtained in the feedback part of the paradigm", ["f_ppi_insula", "f_ppi_sts"]),
    ("r_computations", "Run experiments that isolate the specific computations the left STS/TPJ and anterior insula perform, to explain how guilt and responsibility shape social decisions.",
     "More experiments investigating specific computations in which these regions are involved", ["f_sts", "f_insula"]),
]
for rid, text, anchor, targets in req:
    node(rid, "Request", text, "Future work the Discussion calls for.", anchor)
    for t in targets: edge("request_target", rid, t)

# ═══════════════════════════════════════════════════════════════════════════════════════════
# SUMMARIES — what a reader sees beside each node: one or two plain sentences, no editorial
# remarks (those go to `notes`). Study, panel and check status are structured fields, not prose.
# ═══════════════════════════════════════════════════════════════════════════════════════════
SUMMARIES = {
    "q1": "Does it feel different to have caused a bad outcome for someone than to have watched them cause it themselves?",
    "q2": "Which parts of the brain respond to guilt and to being responsible for a partner, and how do they communicate with the prefrontal cortex?",
    "h1": "Being the one who chose, when the choice turns out badly for a partner, should hurt more than the same bad luck under the partner's own choice.",
    "h2": "The anterior insula, already linked to guilt, should respond more when the participant is responsible for the partner's bad outcome.",
    "h3": "How the insula and STS couple with prefrontal cortex during a choice should depend on whether the choice is risky and whether it affects the partner.",
    "h4": "Some brain region should track the partner's surprises more strongly when the participant, not the partner, caused them.",
    "f_guilt": "The same bad outcome for the partner lowered happiness more when the participant had made the choice, in both studies.",
    "f_model": "Among five models of what drives happiness, the one that separates out the partner's surprises caused by the participant's own choice fitted best, and that term mattered.",
    "f_ownrpe": "A participant's own surprises affected their happiness more than the partner's did.",
    "f_rewards": "Happiness rose and fell with the rewards both players had just received.",
    "f_agency": "Simply being the one who decided made participants slightly less happy, whatever the outcome.",
    "f_null_good": "When the partner's outcome was good, it made no difference who had chosen.",
    "f_risk": "Participants were about as willing to take risks for themselves and a partner as for themselves alone.",
    "f_insula": "Insula activity rose more for the partner's bad outcomes when the participant had made the choice, mirroring the behavioural guilt effect.",
    "f_ppi_insula": "How strongly the insula and the right inferior frontal gyrus were coupled depended on what was chosen and for whom.",
    "c_ifg": "The authors suggest this prefrontal region handles guilt-related information while a social choice is being made.",
    "f_ppi_sts": "A weaker, uncorrected result suggested the STS and the left inferior frontal gyrus couple in the opposite pattern.",
    "f_sts": "A region of the left superior temporal sulcus tracked the partner's surprises more when the participant had caused them.",
    "f_network": "Choosing for two people engaged regions associated with thinking about others: precuneus, temporo-parietal junction and medial prefrontal cortex.",
    "f_outcome_net": "Receiving a lottery outcome engaged a set of regions associated with risk, including the anterior insula and ventral striatum.",
    "f_grbs": "Brain activity during the guilt effect resembled a published brain signature of guilt from other studies.",
    "a_own": "Perhaps participants were just disappointed about their own outcome, not the partner's.",
    "a_general": "Perhaps being responsible simply makes every outcome for the partner matter more, good or bad.",
    "a_risk": "Perhaps people take different risks when choosing for two, and the differences between conditions follow from that rather than from guilt.",
    "a_inequality": "Perhaps happiness just tracks the gap between what the two players got, with no role for who was responsible.",
    "a_emotion": "Perhaps what participants felt was empathy, or a sense of failure or bad luck, rather than guilt.",
    "a_algorithm": "Perhaps, because the partner was really an algorithm, participants were not emotionally engaged with the partner's outcomes at all.",
    "r_emotions": "Ask participants what they felt, to connect the measures of guilt to their own experience.",
    "r_traits": "Study more people, to see how personality shapes guilt and responsibility and their brain correlates.",
    "r_trials": "Collect more trials, so risk preferences can be modelled separately for gains and losses in each condition.",
    "r_partners": "Vary who the partner is, from friend to stranger to machine, to see how closeness changes guilt and responsibility.",
    "r_feedback_ppi": "Analyse connectivity during the moment outcomes are revealed, not only during the choice.",
    "r_computations": "Design experiments that isolate what the STS and anterior insula each compute during social decisions.",
    "e_value_s1": "Participants took the lottery more often the better it was, showing their choices were sensible.",
    "e_value_s2": "The same held in the scanner study.",
    "e_choice_s1": "In the first study, participants chose the lottery a little more often when choosing for themselves alone.",
    "e_choice_s2": "In the scanner study, choosing for two made no difference to how often the lottery was chosen.",
    "e_ev_x_cond": "How much the lottery's value swayed choices was the same whether choosing for one or for two.",
    "e_premium_s1": "The premium participants demanded for taking a risk was the same whether choosing for one or for two.",
    "e_premium_s2": "The same held in the scanner study.",
    "e_rho_gainloss": "Risk attitude was the same for gains and losses, so the two could be pooled.",
    "e_rho_s1": "By one measure, participants in the first study were slightly more cautious when choosing for two.",
    "e_rho_s2": "By the same measure, participants in the scanner study were not more cautious when choosing for two.",
    "e_rho_premium": "The two ways of measuring risk attitude agreed closely.",
    "e_rewards_s1": "In the first study, happiness tracked the rewards both the participant and the partner had just received.",
    "e_rewards_s2": "The same held in the scanner study.",
    "e_lr_s1": "In the first study, the responsibility model fitted the happiness data better than every other model.",
    "e_lr_s2": "The same held in the scanner study.",
    "e_fit_s1": "The two responsibility models explained the first study's happiness data best by every fit measure.",
    "e_fit_s2": "The same held in the scanner study.",
    "e_weights_s1": "In the first study, the partner's surprises caused by the participant's own choice carried a reliable weight in happiness.",
    "e_weights_s2": "The same held in the scanner study, where that weight also tended to exceed the weight on surprises the partner caused.",
    "e_srpe": "A participant's own surprises weighed more on happiness than the partner's, in both studies.",
    "e_recovery": "The model's parameters could be recovered from simulated data, so the fits are stable.",
    "e_agency_s1": "In the first study, participants were less happy after trials in which they had been the one to choose, regardless of outcome.",
    "e_agency_s2": "The same held in the scanner study.",
    "e_lmm_select": "Across several statistical models, both the outcome and who chose affected happiness.",
    "e_guilt_s1": "In the first study, the partner's outcome and who had chosen interacted: a bad outcome hurt more after the participant's own choice.",
    "e_guilt_s2": "The same interaction held in the scanner study.",
    "e_ownhigh": "The guilt effect was present when the participant's own outcome was good.",
    "e_ownlow": "The guilt effect was present when the participant's own outcome was bad.",
    "e_null_good": "After a good outcome for the partner, who had chosen made no difference to happiness.",
    "e_vs_risky": "The ventral striatum responded more to risky than safe choices, as it has in earlier studies.",
    "e_social_solo": "Choosing for both players engaged the precuneus, left temporo-parietal junction and medial prefrontal cortex.",
    "e_precuneus_tpj": "The precuneus and temporo-parietal junction were most active for risky choices made on behalf of both players.",
    "e_outcome_net": "Receiving a lottery outcome engaged the anterior insula, ventral striatum and several other regions more than receiving a safe outcome.",
    "e_insula_roi": "Insula regions responded more to the partner's bad outcomes when the participant had chosen, even after discounting responses to good outcomes.",
    "e_insula_voxel": "A small cluster in the left anterior insula showed the same guilt-related response in a voxel-by-voxel analysis.",
    "e_vs_model": "The ventral striatum tracked the model's expected rewards, confirming the model-based analysis works.",
    "e_sts": "A cluster in the left superior temporal sulcus responded more to the partner's surprises when the participant had caused them.",
    "e_sts_sessions": "That cluster's responses are shown separately for the two scanning sessions.",
    "e_ppi_insula": "Coupling between the insula and the right inferior frontal gyrus was strongest for risky choices for oneself and safe choices for both.",
    "e_ppi_insula_left": "A smaller cluster on the left showed the same pattern but did not survive statistical correction.",
    "e_ppi_sts": "Coupling between the STS and the left inferior frontal gyrus showed the opposite pattern, but did not survive correction.",
    "e_grbs": "Participants' guilt-related brain maps resembled a published guilt signature more often than not.",
    "e_grbs_indiv": "How closely a participant's map resembled the signature did not predict the size of their behavioural guilt effect.",
    "e_rutledge": "Earlier work had shown that happiness in a gambling task follows recent rewards and surprises.",
    "e_edelson": "Earlier work had found that people dislike being responsible for others' outcomes, independently of guilt.",
    "e_yu2014": "Earlier work had found the anterior insula more active when a partner's pain followed the participant's own mistakes.",
    "e_yu2020": "Earlier work had derived a brain-wide signature of guilt from two studies.",
}
NOTES = {
    "a_own": "Rival to the guilt reading; argued against by the own-outcome split.",
    "a_general": "Rival to the guilt reading; argued against by the null after good outcomes.",
    "a_risk": "Handled by measuring risk attitudes directly; one Study 1 result gives it weak support, which is drawn as `supports`. The authors conclude they have no strong evidence of a difference.",
    "a_inequality": "Built into the model comparison as the Inequality and Guilt-envy models; argued against by the likelihood-ratio tests.",
    "a_emotion": "Raised by the authors. Left open on the behavioural measure ('we cannot exclude'); argued against on the neural one by the signature match ('we thus believe that our participants did experience guilt').",
    "a_algorithm": "A limitation the authors raise and answer with the partner-reward effect.",
    "f_agency": "A separate finding from the guilt effect, not an alternative to it; read by the authors as the 'weight of responsibility' (Edelson et al. 2018).",
    "f_guilt": "The authors call this 'simple guilt' (Battigalli & Dufwenberg 2007).",
    "f_ppi_insula": "The authors suggest the right IFG is sensitive to guilt-related information during social choice.",
    "f_ppi_sts": "Uncorrected; the authors call it anecdotal and read it as information relayed from STS to IFG.",
    "f_sts": "Read by the authors as monitoring the consequences of one's decisions for others.",
    "f_grbs": "The match did not track individual differences in the behavioural effect (e_grbs_indiv).",
    "f_outcome_net": "These regions define the regions of interest for the guilt analyses.",
    "e_rho_s1": "ρ could be estimated in only 18 of 40 participants; the authors judge the result unreliable.",
    "e_grbs_indiv": "A null that qualifies the convergent-validity reading of f_grbs.",
}
for n in N:
    if n["id"] in SUMMARIES:
        n["description"] = SUMMARIES[n["id"]]
    if n["id"] in NOTES:
        n["notes"] = NOTES[n["id"]]
    if n.get("subtype") == "Check":
        n["notes"] = ("Check: " + n["notes"]) if n.get("notes") else "Check: a result that defends a finding or a method rather than arguing for a hypothesis."

# ═══════════════════════════════════════════════════════════════════════════════════════════
# BUILD, CHECK, EMIT
# ═══════════════════════════════════════════════════════════════════════════════════════════
LEGAL = {"addresses": ({"Claim"}, {"Question"}), "supports": ({"Evidence", "Claim"}, {"Claim"}), "opposes": ({"Evidence", "Claim"}, {"Claim"}),
         "grounds": ({"Study"}, {"Evidence"}), "follows": ({"Study"}, {"Protocol"}), "describesActivity": ({"SourceDocument"}, {"Study"}),
         "request_target": ({"Request"}, {"Claim"}), "request_for": ({"Request"}, {"Study"})}
T = {n["id"]: n["type"] for n in N}
problems = []
for n in N:
    if n["anchor"] not in TEXT:
        problems.append(f"ANCHOR NOT VERBATIM  {n['id']}: {n['anchor'][:90]}")
ids = set(T)
for e in E:
    if e["subject"] not in ids or e["object"] not in ids:
        problems.append(f"DANGLING EDGE {e}"); continue
    s, o = LEGAL[e["relation"]]
    if T[e["subject"]] not in s or T[e["object"]] not in o:
        problems.append(f"ILLEGAL EDGE {e['relation']} {T[e['subject']]}→{T[e['object']]} ({e['subject']}→{e['object']})")
dups = [k for k, c in Counter(n["id"] for n in N).items() if c > 1]
if dups: problems.append(f"DUPLICATE IDS {dups}")

# figure-panel coverage
PANELS = ["Figure 1", "Figure 2A", "Figure 2B", "Figure 2C", "Figure 2D", "Figure 2E", "Figure 2F",
          "Figure 3A", "Figure 3B", "Figure 3C", "Figure 3D", "Figure 3E", "Figure 3F", "Figure 3G", "Figure 3H", "Table 1",
          "Figure 4A", "Figure 4B", "Figure 4C", "Figure 4D", "Figure 4E", "Figure 4F", "Figure 4G", "Figure 4H", "Figure 4I", "Figure 5", "Supplementary Figure 2"]
def covers(panel, p):
    if panel == "Figure 1": return False
    m = re.match(r"(Figure \d|Table \d|Supplementary Figure \d)([A-I]?)", panel)
    fig, letter = m.group(1), m.group(2)
    parts = [x.strip() for x in p.split(",")]
    num = fig.split()[-1]
    for x in parts:
        if x.startswith(fig): tail = x[len(fig):]
        elif re.match(rf"{num}[A-I]", x): tail = x[len(num):]
        else: continue
        if not letter or letter in tail: return True
    return False
coverage = {panel: [n["id"] for n in N if n.get("panel") and covers(panel, n["panel"])] for panel in PANELS}
coverage["Figure 1"] = ["p_task"]
FIG_LINKS = {p: figure_for(p) for p in PANELS}
uncovered = [p for p, v in coverage.items() if not v]

if problems:
    print("\n".join(problems)); sys.exit(1)

# ── typed short ids ─────────────────────────────────────────────────────────────────────────
# Readers cite nodes by id, so ids are short and typed: Q question, H hypothesis, F finding, A alternative,
# E evidence, K check, R request, S study, P protocol, D source document. The mnemonic ids above stay as `key`.
PREFIX = {("Question", None): "Q", ("Claim", "Hypothesis"): "H", ("Claim", None): "F", ("Claim", "Alternative"): "A",
          ("Evidence", None): "E", ("Evidence", "Check"): "K", ("Evidence", "Cited"): "E", ("Request", None): "R", ("Study", None): "S",
          ("Protocol", None): "P", ("SourceDocument", None): "D"}
counts, ID = Counter(), {}
for n in N:
    pre = "C" if n["type"] == "SourceDocument" and n.get("doi") != PAPER_DOI else PREFIX[(n["type"], n.get("subtype"))]
    counts[pre] += 1; ID[n["id"]] = f"{pre}{counts[pre]}"
for n in N:
    n["key"] = n["id"]; n["id"] = ID[n["key"]]
    for f in ("study", "sourceDocument"):
        if n.get(f) in ID: n[f] = ID[n[f]]
for e in E:
    e["subject"], e["object"] = ID[e["subject"]], ID[e["object"]]
coverage = {k: [ID[x] for x in v] for k, v in coverage.items()}

# ── extractor-shaped graph.json ───────────────────────────────────────────────────────────────
graph = {"source": "hand-built from eLife 105391 v2 as served by epp.elifepathways.org", "slug": "gadeke-2026-guilt-insula",
         "paper": {"title": "Contributions of insula and superior temporal sulcus to interpersonal guilt and responsibility in social decisions",
                   "doi": "10.7554/eLife.105391.2", "license": "CC BY 4.0",
                   "authors": [{"name": a} for a in ["Maria Gädeke", "Tom Willems", "Omar Salah Ahmed", "Bernd Weber", "René Hurlemann", "Johannes Schultz"]]},
         "subtypes": {"Hypothesis": "Claim", "Alternative": "Claim", "Check": "Evidence", "Cited": "Evidence"},
         "nodes": N, "edges": E, "models": ["hand-built (Zach Mainen, Claude)"], "edited": True,
         "coverage": coverage, "figures": FIG_LINKS}
json.dump(graph, open(os.path.join(HERE, "gadeke-hand.graph.json"), "w"), indent=1, ensure_ascii=False)

# ── MIRA JSON-LD ─────────────────────────────────────────────────────────────────────────────
WHO, STAMP, BASE = "urn:claim-graphs:hand-built-2026-10-16", "2026-10-16T00:00:00.000Z", "urn:claim-graphs:gadeke-2026-guilt-insula:hand:"
item = lambda c: {"@type": "Item", "format": "text/plain", "content": c}
def stamped(n): n.update({"creator": WHO, "created": STAMP, "modified": STAMP}); return n
g = [{"@id": WHO, "@type": "UserAccount", "accountName": "claim-graphs, hand-built"}]
for t in ["Question", "Claim", "Evidence", "Study", "Protocol", "SourceDocument", "Request", "Argument"]:
    g.append(stamped({"@id": f"cg:type/{t}", "@type": "NodeSchema", "subClassOf": [f"mira:{t}"], "label": t}))
for sub, sup in graph["subtypes"].items():
    g.append(stamped({"@id": f"cg:type/{sub}", "@type": "NodeSchema", "subClassOf": [f"cg:type/{sup}", f"mira:{sup}"], "label": sub,
                      "description": item({"Hypothesis": "A claim the paper commits to and sets out to test — an untested claim, in the Discourse Graphs sense.",
                                           "Alternative": "A claim the paper raises in order to test or argue against, or leaves open: a rival explanation of a finding.",
                                           "Check": "An observation whose job is to defend a finding or a method — a manipulation check, positive control, replication of a known effect, or assumption test — rather than to argue for or against a hypothesis.",
                                           "Cited": "A finding this paper takes from another publication, as this paper states it; its sourceDocument is the cited work, not this paper."}[sub])}))
RELS = {"addresses": ("mira:addresses", "Claim", "Question"), "supports": ("mira:supports", "Argument", "Claim"), "opposes": ("mira:opposes", "Argument", "Claim"),
        "grounds": ("mira:grounds", "Study", "Evidence"), "follows": ("mira:follows", "Study", "Protocol"), "describesActivity": ("mira:describesActivity", "SourceDocument", "Study"),
        "request_target": ("mira:request_target", "Request", "Claim")}
for key, (sup, dom, rng) in RELS.items():
    rid, did = f"cg:rel/{key}", f"cg:rel/{key}/def"
    g.append(stamped({"@id": rid, "@type": "AbstractRelationDef", "subClassOf": [sup, {"@type": "owl:Restriction", "onProperty": "rdf:predicate", "hasValue": rid}], "label": key}))
    g.append(stamped({"@id": did, "@type": "RelationDef", "domain": f"cg:type/{dom}", "range": f"cg:type/{rng}", "subClassOf": [rid, "dgb:RelationInstance"], "label": key}))
iri = {}
for n in N:
    i = n.get("url") or n.get("doi") or (BASE + n["id"]); iri[n["id"]] = i
    typ = ([f"cg:type/{n['subtype']}"] if n.get("subtype") else []) + [f"cg:type/{n['type']}", n["type"]]
    o = {"@id": i, "@type": typ, "title": n["text"] if n["type"] in ("Study", "Protocol", "SourceDocument", "Request") else n["description"].split(" · ")[-1][:200] if False else n["text"],
         "description": item(n["description"] + " — Anchor: “" + n["anchor"] + "”")}
    if n["type"] == "Evidence":
        sd = n.get("sourceDocument", PAPER_DOI)
        o["sourceDocument"] = sd if sd.startswith("http") else iri.get(sd, BASE + sd)
        if n.get("figure"): o["observationBase"] = n["figure"]["image"]
    g.append(o)
for k, e in enumerate(E, 1):
    g.append(stamped({"@id": f"{BASE}edge/{k}", "@type": [f"cg:rel/{e['relation']}", e["relation"]], "source": iri[e["subject"]], "destination": iri[e["object"]],
                      "title": f"[[{e['subject']}]] -{e['relation']}-> [[{e['object']}]]"}))
doc = {"@context": ["https://purl.org/mira-science/mira.jsonld", {"cg": "https://w3id.org/claim-graphs/schema#", "dgb": "https://discoursegraphs.com/schema/dg_base#",
       "owl": "http://www.w3.org/2002/07/owl#", "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", "onProperty": {"@id": "owl:onProperty", "@type": "@id"}, "hasValue": {"@id": "owl:hasValue", "@type": "@id"}}], "@graph": g}
json.dump(doc, open(os.path.join(HERE, "gadeke-hand.mira.jsonld"), "w"), indent=1, ensure_ascii=False)

# ── report ────────────────────────────────────────────────────────────────────────────────────
by = Counter(n["type"] for n in N); sub = Counter(n.get("subtype") for n in N if n.get("subtype")); rel = Counter(e["relation"] for e in E)
print("nodes", dict(by), "| subtypes", dict(sub)); print("edges", dict(rel), "total", len(E))
print("anchors verbatim:", sum(1 for n in N if n["anchor"] in TEXT), "/", len(N))
print("panels covered:", len(PANELS) - len(uncovered), "/", len(PANELS), "| uncovered:", uncovered)
alts = [n for n in N if n.get("subtype") == "Alternative"]
opp = defaultdict(list)
for e in E:
    if e["relation"] == "opposes": opp[e["object"]].append(e["subject"])
for a in alts: print(f"  Alternative {a['id']}: opposed by {opp.get(a['id'], [])}")
