# MIRA's own extractor on Gädeke — 2026-10-16

MIRA-science/MIRA-extraction (SciOS's extractor, pure MIRA output) run on the Gädeke paper with
the one model call answered by a Claude Code subagent (`claude-fable-5-1`), then compared with the
hand-built MIRA-native graph in claim-graphs (`docs/design/2026-10-07-gadeke-core.jsonld`).
The comparison is `COMPARISON.md`. The committed corpus was not touched.

## What is here

    gadeke-2026-guilt-insula.md          the paper as fed to the extractor (from site/src/data/article/)
    article_to_md.py                     the converter that made it
    prompt.md                            the extractor's exact prompt, as its CLI dumped it
    answer.json                          the raw subagent reply
    gadeke-2026-guilt-insula.mira.jsonld the replayed, SHACL-validated MIRA JSON-LD
    gadeke-2026-guilt-insula.graph.json  the working graph + the engine's report
    anchors.py                           counts, verbatim-anchor check, node/edge dump
    COMPARISON.md                        the note

## Reproducing it

In a checkout of MIRA-extraction on branch `feat/claude-subagent-runner`:

```bash
python3 article_to_md.py site/src/data/article/gadeke-2026-guilt-insula.json runs/gadeke/gadeke-2026-guilt-insula.md
npm run extract -- runs/gadeke/gadeke-2026-guilt-insula.md --dump-prompt runs/gadeke/prompt.md
# answer runs/gadeke/prompt.md with one mira-extractor subagent (.claude/agents/mira-extractor.md)
npm run extract -- runs/gadeke/gadeke-2026-guilt-insula.md --answer runs/gadeke/answer.json --answered-by "<model>" --out runs/gadeke
make -C schema vendor && python schema/validate.py runs/gadeke/gadeke-2026-guilt-insula.mira.jsonld
```
