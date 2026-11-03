# MIRA community-extractor baseline — Gädeke 2026

Step 1 of the programme agreed on claim-graphs#77: a reproducible baseline from the MIRA
community extractor (MIRA-science/MIRA-extraction @ main, 2026-08-11) on the same prepared text
our readers used, before any of our own machinery is judged against it. Then the first step-2
experiment: one altered prompt, run against the original under identical conditions.

Every run here is one page at https://claude.ai/artifact/PzYJYiQtBPxx5nkgK6MMen (private).

## How these runs were made

The extractor's single model call was reproduced exactly — its system message verbatim
(`src/prompt.ts`), its user message (`USER_PREAMBLE_PAPER + "\n\n---\n" + paper`), temperature
0.2, a 60,000-token output cap, streaming with usage accounting, bounded retries and its parse
(strip one ```fence, else first `{` to last `}`) — by `scripts/mira_baseline.py` in claim-graphs
rather than by running the extractor's own TypeScript, which is unlicensed third-party code. Not
reproduced: the post-call exact-text duplicate fold, the one-pass model consolidation, and the
JSON-LD projection. Per run: the raw graph the model returned (`*.graph.json`), the raw reply
(`*.raw.txt`) and metadata (`*.meta.json`: model that answered, seconds, tokens, cost, attempts,
errors, which prompt, which route). `summary.json` is one record per run.

Input, identical for every run: `prepared.json` assembled as title · authors · DOI · abstract ·
Introduction · Results · Discussion · Methods · figure captions · appendix — 113,836 characters,
under the extractor's 400K single-call limit.

Two routes. **API**: the call to OpenRouter with the paper inside the prompt. **Subagent**: a
Claude Code subagent reads the system message and the user message from files (the paper arrives
as three page reads, not inside the prompt) and writes the JSON, which is then parsed as the
extractor parses a reply — the extractor's own `--answer` mode. The two routes are not equivalent:
both subagent runs came out at about half the node count of the same model through the API.

| run | prompt | model | route | result |
|:--|:--|:--|:--|:--|
| `nemotron-free.run1–3` | original | `nvidia/nemotron-3-ultra-550b-a55b:free` (the pinned default) | API | **no graph**: 9 attempts, each a 300 s timeout at OpenRouter ("A Timeout Occurred") |
| `sonnet-4.5.run1` | original | `anthropic/claude-sonnet-4.5` | API | 49 nodes · 1 Q · 8 C · 21 E · 0 opposes · 124 s · $0.22 |
| `sonnet-4.5.run2` | original | same | API | 33 nodes · 1 Q · 8 C · 11 E · 0 opposes · 87 s · $0.19 |
| `sonnet-subagent-control.run1` | original | same | subagent | 28 nodes · 2 Q · 6 C · 7 E · 0 opposes |
| `sonnet-subagent-variant1.run1` | **variant-1** | same | subagent | 36 nodes · **4 Q** · 6 C (1 open alternative) · 9 E · 0 opposes |
| `sonnet-4.5-variant1.run1` | **variant-1** | same | API | 54 nodes · 1 Q · 8 C · 12 E · 8 Studies · 0 opposes · 156 s |

Two graphs made elsewhere are compared alongside: eLife's design prototype carries the
extractor's own July run (free model, from the PDF, marked `edited: true`; 34 nodes, 6 Claims,
0 opposes), and zmainen/elife-claim-trees#178 holds a run of the extractor's full pipeline with
a Fable 5.1 subagent on a markdown rendering of the paper (95 nodes, 18 Claims, 3 opposes, all
108 anchors verbatim).

## Variant-1 of the prompt

`extract/prompts/external/mira-extraction/system_message.variant-1.txt` in claim-graphs, with the
diff in `VARIANTS.md` beside it. Output shape, node types and relations unchanged. Seven changes,
each from a failure observed in the baseline: Claim redefined to admit what the paper argues
against; a rule for eliminated alternatives and the four places they live; rival distinguished
from check; hypotheses as Claims that findings support; one Question per hypothesis in place of
"at most one or two"; Evidence per study with its numbers; Study per analysis.

**Result, two runs.** The structural rules took. Through the API: eight Studies (the two
experiments and six analyses), every Evidence node naming its study. Through the subagent: four
Questions, one per hypothesis the paper commits to, and the Discussion's empathy caveat as an
open alternative addressing the insula question. The argument rules did not take in either run:
no eliminated rival as a Claim, no `opposes` edge, and the hypothesis/finding split only once.
The eliminating results themselves — the guilt effect holding for own high and own low outcomes,
no effect after good partner outcomes, equal risk premiums — were not extracted as Evidence in
either variant run, so rule 8 had nothing to draw an edge from. Run-to-run variance on identical
inputs is large (49 against 33 nodes for the original prompt via the API), so two runs do not
settle it, but the direction is consistent with the Fable run: a stronger model and a better
prompt change the size and the provenance, not the eliminative shape.

## The alternatives pass — the first added stage

`alternatives_pass.txt`: a second model call given an existing run's graph (its nodes and argument
edges) plus the whole paper, with one job — find the alternatives the paper argues against or
leaves open, state each as a Claim as its proponent would, `addresses` the favoured explanation's
Question, draw `opposes` from the results that count against it, and add any eliminating result
the first pass dropped as Evidence grounded in its Study; checks become `supports`, open
alternatives get no opposing edge. The reply is a patch merged onto the base graph (new ids
`a…`, `ae…`), so the stage's contribution is exactly the diff. ~25 s and ~$0.15 a run.

| run | base | added | `opposes` | what it found |
|:--|:--|:--|--:|:--|
| `sonnet-4.5-alternatives.run1` | variant-1 (API) | 6 nodes, 10 edges | 1 | empathy-vs-guilt as open (correct, anchored); insula-empathy as open; responsibility aversion, but *supported* by the agency main effect rather than opposed (the same mis-wiring our own tree had); the algorithm partner as a limitation opposed by the partner-reward correlation; e11→c6 check wired |
| `sonnet-4.5-alternatives.run2` | variant-1 (API) | 8 nodes, 15 edges | 4 | empathy as open; **the general-responsibility rival correctly opposed by the null after good partner outcomes** (`ae2`, anchored) — the first Results-based elimination any run has produced; risk premiums added as Evidence (`ae1`) but aimed at a mis-stated rival ("strategic considerations about the partner's expectations"); insula-empathy opposed by the guilt-signature match; the algorithm partner again |
| `sonnet-4.5-alternatives-over-run1.run1` | original (API, run 1) | 7 nodes, 11 edges | 5 | empathy, shame and bad luck split into three rivals from the one caveat sentence, all three plus insula-empathy opposed by the guilt-signature match. **Correction (2026-10-16, later the same day):** this was first recorded here as fabrication; on rereading the v2 Discussion it is an inference the paper makes — "The 'neurometrics' analysis of our guilt-related activation maps showed a significant similarity to a published guilt-related brain signature … We thus believe that our participants did experience guilt." The authors leave the emotion-labelling alternative open on the behavioural measure and argue against it on the neural one. The run read that correctly; the split into three rivals is still padding. |

**Reproducible:** the open empathy alternative, with a verbatim anchor, in all three runs. **Once:**
a genuine Results-based elimination (run 2). **Never, in three runs:** own-outcome disappointment
(the high/low split — present as Evidence in the run-1 base and still not wired) and inequality
aversion (the model comparison). **Over-reach:** the signature-match run invents an eliminative
argument; new Claim anchors are verbatim in about half the cases, new Evidence anchors in most.

So the stage changes the shape — `opposes` goes from 0 to between 1 and 5 — and its recall is
concentrated where the paper uses explicit eliminative phrasing ("rather than", "cannot exclude",
"did not influence"). The two alternatives that are never found are the ones that have to be
constructed from a design (the own-outcome split) or from a model comparison, which is also
where the single-pass prompts failed. Precision needs a guard: an `opposes` edge should require
that the paper itself draws the inference, and the anchor rule for new Claims needs enforcing.

## Error catalogue

Entries tie each observed failure to the passage of the paper that shows it.

1. **No eliminative structure, under either prompt.** The paper argues against four rival
   accounts of its central finding with specific results — own-outcome disappointment (guilt
   effect holds for own high *and* own low outcomes, Results §"effects of agency, responsibility,
   and guilt"); a general responsibility effect (no effect after *good* partner outcomes, same
   section); a shift in risk attitude (risk premiums equal, §"risk preferences"; Discussion: "we
   do not have strong evidence of differences"); inequality aversion (Responsibility model beats
   Inequality and Guilt-envy on likelihood-ratio tests, Table 1) — and raises one it leaves open
   (empathy rather than guilt: Discussion, "we cannot exclude the possibility that they have
   instead or in addition felt empathy"). No run under the original prompt produced an `opposes`
   edge aimed at a rival. The variant prompt, which asks for exactly this, produced none either in
   two runs; the Fable run's three `opposes` edges are two results opposing the authors' own risk
   conclusion and the caveat opposing their guilt conclusion. The alternatives are not stated as
   propositions anywhere in the paper; they have to be constructed from eliminating sentences,
   compared models, control rationale and limitations, and a single pass that is also extracting
   fifty other records does not do that construction. This is the strongest evidence so far for a
   separate stage.

2. **The controls are the first thing dropped.** Under "prefer a smaller, accurate graph", the
   results whose only job is to eliminate an alternative are absent from most runs as Evidence
   (present in `sonnet-4.5.run1` as free-standing Evidence supporting nothing; absent from the
   smaller runs). Rule 8 cannot fire without them.

3. **Hypotheses flattened into findings.** The paper states what it set out to test
   (Introduction: "we hypothesized that connectivity … might change"; Results: "To specifically
   search for a sign of interpersonal guilt"). Every run emits the confirmed result and never the
   proposition it tested; the variant's instruction to keep them apart took once (subagent) and
   not at all through the API.

4. **One Question, under the original prompt, when Sonnet answers.** Rule 5's "at most one or
   two" plus the paper never posing a question as a question: Sonnet took the abstract's first
   sentence three times out of three. The free model and Fable found three. The variant's
   one-per-hypothesis rule gave four through the subagent and one through the API.

5. **Evidence pooled across studies, under the original prompt.** `sonnet-4.5.run1`: 8 of 21
   Evidence nodes say "in both studies"; 2 name a study. The variant's rule fixed this completely
   (12 of 12 name their study).

6. **Provenance flattened, under the original prompt.** Both Studies `follow` the union of their
   protocols. The variant's Study-per-analysis rule fixed this (8 Studies).

7. **The pinned default does not serve this paper.** Nine attempts, nine 300-second timeouts.
   The extractor's no-fallback policy would fail identically; the only completed baselines are on
   paid models.

8. **Route changes size by half.** Same model, prompt and text: 49 and 33 nodes via the API, 28
   via the subagent; variant 54 via the API, 36 via the subagent. A subagent reading the paper in
   pages under-extracts. Comparisons must hold the route fixed.
