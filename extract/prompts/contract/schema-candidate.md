# What a reader returns

Generated from `extract/elife_extract/schema.py` by `elife-extract contract --write`. Do not edit.

A JSON array of candidate claims and nothing else — no prose before or after, no code fence. Each element:

| Field | Value | Meaning |
|:--|:--|:--|
| `claim` | `string` | One declarative sentence in active voice, with the paper's own numbers and the paper's own epistemic verb. |
| `panel` (optional) | `string` or `null` | The panel that shows the result, lowercase, as the paper labels it: fig3a, fig5d-h, fig3s1c, table1. Several panels separated by commas when the claim spans them. null for a claim no panel shows. |
| `claim_type` | `empirical` / `interpretive` / `existence` / `synthesis` / `assessment` / `hypothesis` / `prediction` | The kind of proposition; see the vocabulary. |
| `role` | `hypothesis` / `prediction` / `empirical` / `control` / `scope` / `methodological` / `synthesis` / `interpretation` / `literature-context` | The work it does in the argument; see the vocabulary. |
| `evidence` | `string` | A verbatim quote from the text you were given, at most two sentences, that grounds the claim. It is checked against the source. |
| `confidence` | `high` / `tentative` | high or tentative; see the vocabulary. |
| `notes` (optional) | `string` or `null` | Hedges, alternative readings, or what made this tentative. null when there is nothing to say. |

```json
[
  {
    "claim": "Doubling distal dendritic inhibition reduces somatic firing from approximately 5.5 Hz to approximately 0.2 Hz.",
    "panel": "fig4a",
    "claim_type": "empirical",
    "role": "empirical",
    "evidence": "Doubling the strength of distal inhibition reduced the firing rate from 5.5 \u00b1 0.9 Hz to 0.2 \u00b1 0.2 Hz.",
    "confidence": "high",
    "notes": null
  }
]
```
