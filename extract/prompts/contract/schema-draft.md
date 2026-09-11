# What the reconciler and the reviewer return

Generated from `extract/elife_extract/schema.py` by `elife-extract contract --write`. Do not edit.

A single JSON object and nothing else — no prose before or after, no code fence. Top level:

| Field | Value | Meaning |
|:--|:--|:--|
| `paper_slug` | `string` | As given in the input. |
| `paper_doi` | `string` | As given in the input. |
| `paper_title` (optional) | `string` or `null` | As given in the input. |
| `extraction_path` (optional) | `jats` / `pdf` or `null` | Filled by the runner from prepared.json. Leave null. |
| `extraction_path_note` (optional) | `string` or `null` |  |
| `per_agent_counts` (optional) | object | How many candidates each reader proposed. |
| `model` (optional) | `string` or `null` |  |
| `claims` | list of ReconciledClaim | Every surviving claim. |
| `config_snapshot` (optional) | object | Filled by the runner: models and prompt variant. Leave empty. |

Each element of `claims`:

| Field | Value | Meaning |
|:--|:--|:--|
| `claim` | `string` | The canonical sentence. Where readers phrased one proposition differently, the most precise phrasing, grounded in their evidence. |
| `panel` (optional) | `string` or `null` | As for a reader. Where readers disagree, the caption reader's panel. |
| `claim_type` | `empirical` / `interpretive` / `existence` / `synthesis` / `assessment` / `hypothesis` / `prediction` | See the vocabulary. |
| `role` | `hypothesis` / `prediction` / `empirical` / `control` / `scope` / `methodological` / `synthesis` / `interpretation` / `literature-context` | See the vocabulary. |
| `addresses` (optional) | `string` or `null` | For a hypothesis or an alternative explanation, the research question it answers, as the paper states it or in one sentence; null for every other role. |
| `confidence` | `high` / `contested` / `single-source` | A fact about agreement: single-source for one reader, high for several who agree, contested for several who disagree. |
| `sources` | list of `results` / `caption` / `structure` / `reviewer` | The readers that surfaced this claim: results, caption, structure; reviewer for a claim the review pass added. |
| `evidence_by_agent` (optional) | object | For each reader in sources, the verbatim quote it gave. |
| `span_by_agent` (optional) | object | For each reader in sources that cited one, the span id its evidence quote came from. |
| `evidence_verified` (optional) | object | Filled by the runner. Leave null. |
| `evidence_verified_against` (optional) | object | Filled by the runner: per reader, `span` or `slice`. Leave null. |
| `notes` (optional) | `string` or `null` | What the readers disagreed about, or why a single-source claim deserves a second look. A review pass prefixes its notes with [reviewer]. |
| `part_of` (optional) | `string` or `null` | The exact `claim` sentence of another claim in this same table that this one is a component of — one comparison, condition, measure or study of a proposition that claim states whole. Keep both; the writer resolves the sentence to the whole's slug and writes `part-of`. null when this claim is not a part of another. |

```json
{
  "paper_slug": "headley-2026-inhibitory-rhythms",
  "paper_doi": "10.7554/eLife.95562",
  "paper_title": "Spatially targeted inhibitory rhythms differentially affect neuronal integration",
  "per_agent_counts": {
    "results": 18,
    "caption": 22,
    "structure": 7
  },
  "claims": [
    {
      "claim": "Doubling distal dendritic inhibition reduces somatic firing from approximately 5.5 Hz to approximately 0.2 Hz.",
      "panel": "fig4a",
      "claim_type": "empirical",
      "role": "empirical",
      "confidence": "high",
      "sources": [
        "results",
        "caption"
      ],
      "evidence_by_agent": {
        "results": "distal inhibition nearly silenced the cell (0.2 Hz)",
        "caption": "Doubling the strength of distal inhibition reduced the firing rate from 5.5 \u00b1 0.9 Hz to 0.2 \u00b1 0.2 Hz."
      },
      "notes": null
    }
  ]
}
```
