# What the external reviewer returns

Generated from `extract/elife_extract/schema.py` by `elife-extract contract --write`. Do not edit.

A single JSON object with two keys — `edits` and `additions` — and nothing else: no prose before or after, no code fence.

Top level:

| Field | Value | Meaning |
|:--|:--|:--|
| `edits` (optional) | list of ReviewEdit | Zero or more targeted changes to existing claims, keyed by their `claim` sentence. |
| `additions` (optional) | list of ReconciledClaim | Zero or more new claims to append to the draft; each must carry confidence=single-source and sources=[reviewer]. |

Each element of `edits` (targeted changes to existing claims):

| Field | Value | Meaning |
|:--|:--|:--|
| `claim` | `string` | The exact `claim` sentence of the claim to edit, as it appears in the draft. |
| `role` (optional) | `hypothesis` / `prediction` / `empirical` / `control` / `scope` / `methodological` / `synthesis` / `interpretation` / `literature-context` or `null` | New role to assign; omit or null to leave unchanged. |
| `claim_type` (optional) | `empirical` / `interpretive` / `existence` / `synthesis` / `assessment` / `hypothesis` / `prediction` or `null` | New claim_type to assign; omit or null to leave unchanged. |
| `panel` (optional) | `string` or `null` | New panel value; omit or null to leave unchanged. |
| `notes` (optional) | `string` or `null` | Replacement notes string (prefix with [reviewer]); omit to leave unchanged. |

Each element of `additions` (new claims appended to the draft):

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
  "edits": [
    {
      "claim": "Doubling distal dendritic inhibition reduces somatic firing from approximately 5.5 Hz to approximately 0.2 Hz.",
      "role": "empirical",
      "notes": "[reviewer] role: empirical \u2192 control. This result rules out that somatic firing is driven by distal input rather than proximal."
    }
  ],
  "additions": [
    {
      "claim": "Distal inhibition more strongly reduces somatic firing than proximal inhibition.",
      "panel": null,
      "claim_type": "synthesis",
      "role": "synthesis",
      "addresses": null,
      "confidence": "single-source",
      "sources": [
        "reviewer"
      ],
      "evidence_by_agent": {
        "reviewer": "The contrast across fig4a (distal) and fig4b (proximal) is stated in the Discussion: distal inhibition is uniquely effective."
      },
      "notes": "[reviewer] added: synthesis across panels."
    }
  ]
}
```
