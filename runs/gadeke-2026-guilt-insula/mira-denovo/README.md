# Gädeke, blind de novo MIRA run (2026-11-15)

This is the first real run of the staged de novo extraction (`scripts/mira_denovo.py` in claim-graphs) on eLife 105391v2. "Blind" means the model never saw the hand-built graph in `../mira-hand/`. That graph was used only after assembly, to score the result.

- **Model.** `claude:claude-sonnet-4-5`, run through `claude -p` on the Max subscription. Each call ran isolated: in an empty temporary folder, with no settings, CLAUDE.md, memory, tools or MCP. Every call's meta file records `auth: none`, meaning no API key was used.
- **Calls.** There were 21, taking 33.5 minutes in total. At API prices they would have cost about $3.59, though nothing was billed. Claude Code turns on extended thinking by default and temperature can't be set, so this is not the same configuration as an OpenRouter run.
- **Text.** `text.txt` is the eLife Pathways page text, the same file as `../mira-hand/gadeke-v2.txt`. `references.txt` is the page's reference list, with 71 entries.
- **Machinery.** The run used claim-graphs `fix/mira-denovo-nulls` at 7e8056c, which is the pin 08ecc21 plus four fixes found during this run:
  - null-safe string checks;
  - a reference list for stage 6;
  - eLife's "Figure N:" labels;
  - an empty alignment map.

## How the run went

The first attempt crashed at stage 6 on a cited work whose DOI came back as `null`. After that fix, stage 6 refused every cited work, because the text carries no reference list and the model had no titles, journals or DOIs to give.

`references.txt` was then added, and stages 6–8 were re-run. Stages 1–5 kept their original replies. The replaced stage 6 and 7 calls and outputs are in `superseded/stage6-without-references/`. The first stage 6 reply was also checked once more without a new call, which is how the null-DOI crash was confirmed fixed.

## Result

The assembled graph has 176 nodes and 242 edges. The hand-built graph has 97 nodes.

| Type | De novo | Hand-built |
|---|---|---|
| Evidence | 81 | 35 |
| Check | 8 | 8 |
| Cited evidence | 10 | 4 |
| Finding | 35 | 15 |
| Hypothesis | 6 | 4 |
| Alternative | 2 | 6 |
| Question | 6 | 2 |
| Request | 4 | 6 |
| Protocol | 11 | 10 |
| Study | 2 | 2 |
| Source document | 11 | 5 |

What the checkers refused:
- **Stage 2:** 12 evidence items whose anchors weren't word for word in the text.
- **Stage 3:** 3 findings.
- **Stage 4:** 1 hypothesis.
- **Stage 5:** 3 alternatives. Each had an anchor that wasn't verbatim, and each cited a finding where its edge needed evidence.
- **Stage 6:** 3 cited works with anchors that weren't verbatim.

Four panels were never covered by any evidence item: Figure 1, Figure 4A, Figure 4I and Supplementary Table 7.

Verification passed 141 of 176 nodes:
- 22 fail only because they point to Table 1, which has no image.
- 11 Evidence nodes, including checks, support no claim.
- 6 findings reach no question.
- 2 summaries are missing.

The automatic alignment matches 28 of the hand graph's 97 nodes. It pairs evidence only, by shared statistics. Claims, questions, requests and protocols need a hand-written `alignment.map.json` before the two graphs can be compared fully.

## Files

- `stageN.json` and `stageN.rejected.json`: what each stage accepted and refused.
- `calls/`: every prompt, raw reply and meta file.
- `gadeke-2026-guilt-insula-denovo.graph.json` and its `.verification.json`.
- `alignment.json`.
- `gadeke-2026-guilt-insula-denovo.viewer.html`: the viewer, with a compare tab against the hand graph.
- `harness.html`: the specification, prompts, calls and refusals on one page.
