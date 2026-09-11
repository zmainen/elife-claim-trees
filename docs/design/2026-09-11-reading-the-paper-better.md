# Reading the paper better

**Status:** proposed
**Issue:** [#56](https://github.com/zmainen/elife-claim-trees/issues/56)
**Frames:** [#18](https://github.com/zmainen/elife-claim-trees/issues/18) · [#19](https://github.com/zmainen/elife-claim-trees/issues/19) · [#28](https://github.com/zmainen/elife-claim-trees/issues/28) · [#37](https://github.com/zmainen/elife-claim-trees/issues/37)
**Depends on:** `pipeline/layers.yaml`, `extract/prompts/*`, `extract/elife_extract/{prepare,agents,reconcile,edges,external_review,evaluate}.py`

The induction layers are seven model calls: three readers, a reconciler, a reviewer, an edge
inferrer and a coverage adjudicator. This note reads each call as what it is given, what it is
asked, and what came back, and argues that the largest gains are upstream of the prompts — in
what the readers are allowed to read and in whether the answer can be measured — and that the
prompts themselves should be split into a contract every model gets and scaffolding that varies
by model. The plan at the end is ordered so that nothing is tuned before it can be scored.

## What the pipeline reads, and what it cannot

`prepare` cuts a JATS article into abstract, results, captions, methods, appendices and tables.
For Gädeke that is 34k characters of results, 33k of methods, 8k of captions and 14k of tables.
Two sections are cut and thrown away: the Introduction and the Discussion. The parser knows how
to find both (`_section_text` has branches for `intro` and `discussion`) and is never asked to.
No reader, and not the external reviewer either, ever sees them.

This matters more than any prompt. The external reviewer prompt spends its two longest sections
on "hypothesis under-coverage" and "literature-context under-recognition", and asks the model to
*infer* the organising hypothesis from the empirical sequence. In an eLife paper the organising
hypothesis is stated in the last paragraph of the Introduction, and the cited prior findings the
paper builds on are stated there and in the Discussion. The pipeline is asking a model to
reconstruct from evidence what the authors wrote down in a section it was not shown. The
measured role-agreement gain from the reviewer (65% to 96% on Headley) is real, but it is the
gain from a model guessing well; giving it the text would be cheaper and would not be a guess.

The second structural loss is the panel inventory. Panel agreement is the standing failure
(55–61% across the ten-paper evaluations, the lowest of the three metrics). The caption reader
gets a `[panels detected: a, b, c]` line per figure; the results reader, which is the one that
reads the sentences saying *what each panel is for*, is given no list of panels at all and is
told not to guess panel ids. On the recorded Gädeke run the results reader returned eight of
thirteen claims with no panel while the results text names a figure thirty-one times. And a
claim the reference anchors to `fig4, fig5` cannot survive a caption reader that reads one
caption at a time and a reconciler told to prefer the caption reader's panel.

The third is that the readers are asked for a verbatim `evidence` quote and are given no way
to name where it came from. The quote is never checked against the slice — the one check that
would catch quantitative hallucination for free — and downstream, `coverage` has to re-find
those sentences by string match, which is why an adjudication layer exists at all. The
coverage segmenter already cuts the paper into numbered spans. If `prepare` numbered the spans
and the readers cited span ids, evidence would be verifiable at write time and coverage would
be exact rather than a matcher plus a judgement layer to correct the matcher.

## What the prompts say, and what the models did with it

The seven prompts total 54 KB. The three reader prompts (8–10 KB each) and the reviewer
(14 KB) are written as a persona narrative: who the agent is, what the other agents are doing,
which numbered failure modes (#1–#10) it is "most prone to" — numbers that refer to a list the
model is never shown. The edge-inference prompt is 1.7 KB and gives nine relation types one
gloss each, no direction rule, no example, and the numbered claims truncated at 220 characters
with no evidence and no paper text. That inversion is the first thing to fix: the call that
decides the graph's structure is the least specified call in the pipeline.

Three inconsistencies in the prompts are visible in the outputs.

- **The reconciler's confidence labels have a gap.** The prompt defines `high` as all three
  readers, `contested` as two agree and one differs, `single-source` as one. Two readers
  agreeing while the third is silent — the commonest case, since the partition means most
  claims are visible to at most two readers — has no label. DeepSeek resolved it by calling
  every two-source claim `high`; the seven `high` claims in the Gädeke run all have exactly two
  sources. `contested` also conflates "surfaced by two with a disagreement" with "surfaced by
  three who disagree".
- **`claim_type` has two vocabularies.** The results-reader prompt says `claim_type:
  hypothesis` and `claim_type: prediction` in its load-bearing section and lists `empirical |
  interpretive | existence | synthesis | assessment` in its field guidance. `schema.py` was
  widened to twelve values to accept both, so the corpus's five-type vocabulary from
  `docs/claim-format.md` is not what the pipeline enforces.
- **The edge vocabulary cannot produce a third of the corpus.** The prompt's nine types map to
  `supports, tests, entails, requires, scopes, enables-method, dissociates-with, interprets,
  rules-out`. The corpus carries `validates` 49 times, `confirms` 69, `extends` 29, `refutes`
  and `qualifies` once each. None of those can be emitted. `derived-from` is synthesised as the
  reciprocal of `entails`, which is right; `confirms` as the reciprocal of `predicts` is not
  synthesised because `predicts` is not in the prompt.

The recorded runs show how the same prompts land on different models, which is the empirical
basis for the model-tier argument below.

| Model (run) | What came back |
|:--|:--|
| DeepSeek-chat, Gädeke, all four roles (Sept 2026) | Results reader: 13 claims, 8 unanchored. Caption reader: 26 claims, exactly one per panel, every one `empirical` — no control, no methodological panel, although the prompt asks for both. Structure reader: 8 claims, of which "implemented in MATLAB using Psychtoolbox" and "recruited through flyers" — the prompt's *scope* and *methodological warrant* concepts did not transfer. Reconciler: 47 claims, notes on 2, confidence mislabelled as above. |
| Sonnet 4.6 readers + Opus 4.6 reconcile/review, ten papers (May 2026) | Recovery 97%, but 43–91 CLI claims per paper against 17–31 in the reference: systematic over-splitting, which the "quantity guidance" paragraphs did not prevent. Role agreement 83%, panel 61%. |
| Opus (as a reasoning agent), Gädeke edges | 95 edges for 47 claims: `requires` 31, `supports` 23, `scopes` 17, `tests` 10, `entails` 4. Structural relations dominate; the deductive spine is thin, and the prompt's "hypotheses typically ENTAIL predictions" rule is the only guidance it had. |

The weaker model under-extracts and drops the role distinctions; the stronger model over-splits
and over-wires. Both are prompt failures, and they are different failures, which is the answer
to whether prompts should differ by model.

## Contract and scaffolding

Every model should receive the same **contract**: the schema, the definition of each role and
each relation, the direction rule for each relation, one corpus example per role and per
relation, and a contrastive example for each confusable pair (`requires` versus `supports`;
`entails` versus `tests`; `rules-out` versus `refutes`; `dissociates-with` versus
`contradicts`; `scopes` versus `requires`; `synthesis` versus `interpretation`; `control` versus
`empirical`). The corpus already holds canonical examples — `docs/method.md` §4.6 has one per
role — and `scripts/relations.py` already holds the relation definitions once, after four
copies disagreed. The contract should be generated from those two sources, so the prompt, the
checker and the exporter cannot drift, which is the repository's own pattern applied to its
prompts.

What should vary by model is the **scaffolding** around the contract:

| Tier | Models | Scaffolding |
|:--|:--|:--|
| Frontier | Opus 5, Fable 5.1 | Contract plus a one-page task statement. No persona narrative, no numbered failure modes, no quantity guidance. Whole slice in one call; adaptive thinking with `effort: high` (or `xhigh` for edges and review). Over-prescriptive prompts measurably reduce output quality on this tier, so the current 10 KB reader prompts are probably costing accuracy, not buying it. |
| Standard | Sonnet 5 | Contract plus task statement plus the signal-phrase tables and the explicit "emit two claims, prediction and test" instruction that the results-reader prompt already has. Keep a quantity ceiling, since this tier over-splits. |
| Open | DeepSeek, Mistral, Gemini Flash | Contract with the full example set, and the work chunked so each call has one job: the caption reader per figure with the panel list enumerated ("for each of fig2a … fig2f, zero or more claims"); edge inference per hypothesis arc rather than over the whole table; JSON mode (`response_format`) enforced by the provider rather than by post-hoc salvage. Expect to pay in calls what the frontier tier pays in tokens. |

The relation types, then, should be explained in more detail *and* with examples, for every
tier — the current edge prompt is under-specified even for Opus, and five corpus relations are
unreachable from it. What the tiers change is how much of the explanation is example versus
definition, and whether the model is trusted to hold the whole table at once.

Two further changes apply to every tier and are independent of the prompt text. Every call
should use provider-enforced structured output — `output_config.format` with the schema
generated from the pydantic models on the Anthropic path, `response_format` through litellm
elsewhere — which retires the fence-stripping, bracket-walking and object-salvage code that
currently stands between the model and the schema. And the external review should return a
patch (edits and additions keyed to the draft's claims) rather than a complete rewritten
table: a rewrite costs the full 32k output budget, can silently drop or alter claims it was told
to leave alone, and cannot be diffed.

## Measuring before tuning

None of the above can be judged today. The `evaluate` command scores a re-extraction against
the committed claim trees, and `runs/README.md` records that no committed tree was produced by
this pipeline — Gädeke's 33 claims share no text with the 47 the recorded run drafted, and the
other nine papers have no trace at all. "Role agreement 83%" therefore measures agreement
between two model drafts made by different processes, not agreement with a reading a person
has stood behind. It also runs its own copy of the chain (`prepare → run_all_agents →
reconcile → external_review → write`) outside the layers, so it does not score the code the
layers actually execute, and it measures recall but never precision: a run that emits ninety
claims to recover twenty-five scores 100%.

The prerequisite for every prompt change is a gold set a person has read. The machinery for
recording that exists — `scripts/pipeline.py approve` writes to `approvals.jsonl` and nothing
has ever called it in anger. Two papers, adjudicated claim by claim and edge by edge, with the
approval recorded, turns `evaluate` from a comparison between two drafts into a score.

## Organisation

The call path exists three times. `agents.stream_text` in the package is the one the layers use
and the one that streams, retries and records the model. `api/llm.py` has a second (`call_llm`,
`stream_llm`) and `api/server.py` a third pair (`_run_agent_litellm`, `_run_agent_streaming`,
and the same again for reconcile and review). `api/infer_edges.py` is an older copy of
`edges.py` with its own copy of the prompt and weaker validation. The prompt loader exists three
times (`load_prompt`, `load_reconciler_prompt`, `load_reviewer_prompt`), and the edge prompt is
read at import time, which bypasses `--prompt-variant`. One `call()` in the package, imported by
the API, and one `prompt(role, variant)` would remove roughly four hundred lines and one class of
drift.

Seven declared layers have no runner: `adjudication`, `summaries`, `synthesis`, `abstract-map`,
`stance`, `replication` and `epistemic-vocab`. Three of those are model calls whose prompts are
not in the repository — the paper summary is the block at the top of every paper page and has no
reproducible producer. `claim-tree` refuses to overwrite, so re-inducing a paper that already
has a tree (which is what #18 asks for, nine times) has no path: the layer needs to write a new
version beside the old one and the site needs to show the difference.

Three small robustness gaps sit in the same code. The readers run sequentially when they are
independent by design. `max_tokens` is 32,768 on every call regardless of what the call can
emit, which is how the edge step once failed with a 402 on a provider that reserves the budget.
Nothing is cached, although every reader prompt is well above the minimum cacheable prefix and
`evaluate` sends each one ten times.

## Display and navigation

The site renders the pipeline well as a graph and a matrix, and the layer page now shows the
prompt and one worked output. Three things it cannot show are exactly the things prompt work
needs.

There is no comparison between two versions of a cell. The `comparison` view is declared on six
layers and built for none of the induction layers, so a prompt change that produces reader
output v2 has no page that puts v1 beside it. The single most useful view for this note's
purpose — same paper, two prompt variants or two models, claims aligned by the matcher, with
what each found that the other did not — does not exist, and the evaluate scorecards that come
closest are static markdown under `extract/tests/`, off the site.

The agreement matrix (claim × reader, with the evidence each quoted) is the artifact the whole
three-reader design exists to produce, and it is rendered once, by hand, for Gädeke on the
`induction` page. It should be the `overlap` view of `reconcile`, generic to any paper.

Navigation has grown overlapping routes: `/method`, `/methodology` and `/pipeline/method`;
`/agents` and `/pipeline/induction`; `/layers` and `/pipeline`. Each pair says the same thing at
a different age. The `groups` mechanism in the declaration has two entries where the design
note's own diagram has five (source, induction, tree, measures, interchange); grouping the
matrix columns by those five would make the seventeen rotated labels legible as phases.

## Plan

Ordered by what each item unlocks. Effort is in working days for one person.

| # | Change | Effort | Why this position |
|:--|:--|:--|:--|
| 1 | **Gold set.** Two papers (Headley, Gädeke) adjudicated claim by claim and edge by edge by a person; recorded with `pipeline.py approve`. `evaluate` gains precision, edge recovery and per-role confusion, and runs through `pipeline.py run --root <tmp>` so it scores the layers as declared. | 3 | Nothing below can be judged without it. Also closes the loop the design note calls "output approval as evidence about the declaration". |
| 2 | **Evidence verification.** At reconcile and write, check every `evidence` quote against the slice the reader was given; record `evidence_verified` per claim and per reader. | 1 | Free hallucination metric per model; makes the quote field mean something. |
| 3 | **Prepare reads the whole paper.** Add `introduction_text`, `discussion_text`, a panel inventory (figure id, panel ids, one-line caption head) and numbered spans. Results reader gets abstract + introduction + results + inventory; reviewer gets the full paper; readers cite span ids. | 2 | The hypothesis and literature-context losses are input losses. Span ids make coverage exact and shrink adjudication to the residue. |
| 4 | **Contract extracted from the prompts.** One generated `vocabulary.md` (roles, relations, directions, corpus examples, confusable pairs) from `relations.py` and `method.md` §4.6; one generated schema block from the pydantic models; per-role task files of about a page. Fix the confidence-label gap and the `claim_type` split. | 3 | Every model gets the same definitions; the checker and the prompt cannot disagree. |
| 5 | **Edge inference rewritten.** Full corpus vocabulary with direction rules; the draft's evidence quotes and the relevant spans as input; a one-sentence `why` per edge citing a span; mechanical direction checks at validation (`tests` runs empirical → prediction; `rules-out` targets an entertained or rejected claim; `entails` from a hypothesis). Optional per-arc chunking. | 3 | The least specified call decides the graph. Direction checks also serve #19, #28 and #37. |
| 6 | **Structured outputs and call hygiene.** Provider-enforced schemas; per-call token budgets; readers in parallel; system prompts cached; reviewer returns a patch. | 2 | Removes ~300 lines of salvage code and the DeepSeek wrapping and truncation failures. |
| 7 | **Model profiles and the model sweep.** `--profile frontier|standard|open` selecting prompt variant, chunking and output mode; defaults moved to the current generation (Sonnet 5 readers, Opus 5 for reconcile, review and edges, adaptive thinking); the ten-paper corpus run through the Batch API at half price. Run items 1–6 against the gold set per profile and publish the scorecard as a corpus-scope `evaluation` layer. | 3 | This is the experiment the user asked about, and it is only meaningful after 1–6. |
| 8 | **One call path.** The API imports the package's `call()` and `prompt()`; `api/llm.py` and `api/infer_edges.py` go. | 1 | Drift removal; no behaviour change. |
| 9 | **Runners for the undeclared layers.** Commit the summary, synthesis, abstract-map and adjudicator prompts; give each a command; `claim-tree` writes versions beside each other. | 3 | Makes #18 runnable and the paper page's top block reproducible. |
| 10 | **Site: comparison and overlap views.** A generic two-version diff for any records layer (aligned by the matcher); the agreement matrix as `reconcile`'s `overlap` view; the evaluation scorecard on the site; matrix columns grouped by phase; the three route pairs collapsed to one each. | 4 | The review surface for everything above. Last because it renders what the earlier items produce. |

Items 1–3 are the floor: after them the pipeline reads the paper it was given and can say how
well. Items 4–6 are the prompt work proper, and 7 is the measured answer to the model question.
Items 8–10 make the result maintainable and visible. Roughly five weeks in sequence, less with
two people, since 4–5 and 8–9 are independent of each other.

## What this note does not decide

Whether the three-reader partition should survive frontier models that can hold the whole paper
at once. The partition buys independence — three readings that cannot copy each other — and
that is worth keeping even when context is not the constraint. But the plan above gives every
reader more of the paper than it has now, and at the frontier tier a fourth reading of the whole
paper as a single pass, scored against the three-reader reconciliation on the gold set, is the
experiment that would settle it. It is not in the plan because the gold set has to exist first.
