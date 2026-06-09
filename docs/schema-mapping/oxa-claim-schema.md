# OXA Claim Node Schema

Draft schema for a Claim node type in OXA. Follows the patterns established by RFC0002 (node structure), RFC0003 (core types), and RFC0005 (citations with CiTO intent).

## Node definition

```typescript
interface Claim {
  type: "Claim";

  // Proposition text — inline content (can contain emphasis, math, citations)
  children: Inline[];

  // Unique identifier for cross-referencing (xref target)
  identifier: string;

  // Human-readable slug
  slug?: string;

  // ── Claim-specific fields ────────────────────────────────────

  // Rhetorical function in the paper's argument
  role: ClaimRole;

  // Figure panel(s) this claim is grounded in
  panel?: string[];

  // Epistemic strength of the assertion
  epistemicStrength?: EpistemicStrength;

  // Typed edges to other claims
  relations?: ClaimRelation[];

  // ── Standard OXA fields ──────────────────────────────────────

  // Extensible metadata (RFC0006) — provenance, authorship, confidence
  metadata?: Metadata;

  // Freeform extension data (RFC0002)
  data?: Record<string, unknown>;
}
```

## Enumerations

### ClaimRole

The rhetorical function a claim serves in a paper's argument. Determines what edges it can carry and how synthesis pipelines reconstruct the argument.

```typescript
type ClaimRole =
  | "hypothesis"         // The paper's central bet — often implicit
  | "prediction"         // Testable consequence of a hypothesis
  | "empirical"          // Measured or computed result, panel-grounded
  | "control"            // Empirical result that rules out an alternative
  | "scope"              // Boundary condition on other claims
  | "methodological"     // Capability of the apparatus or analysis
  | "synthesis"          // Integrates multiple results into one statement
  | "interpretation"     // Reframes results through a theoretical lens
  | "literature-context" // Cited prior result the paper depends on
  ;
```

### EpistemicStrength

How strongly the paper asserts the claim.

```typescript
type EpistemicStrength =
  | "strong"       // Directly demonstrated by the evidence
  | "moderate"     // Supported but with caveats
  | "suggestive"   // Consistent with the evidence but not conclusive
  | "speculative"  // Proposed without direct evidence
  ;
```

## ClaimRelation

Typed edge to another claim, following the `Cite` node's `xref` + `intent` pattern from RFC0005. Relation types use the CiTO vocabulary (exact matches) or the claim-relations extension vocabulary (for types CiTO doesn't cover).

```typescript
interface ClaimRelation {
  // Target claim identifier (same as Cite.xref)
  xref: string;

  // Relation type — CiTO IRI or claim-relations extension IRI
  relationType: string;
}
```

### Relation type vocabulary

CiTO exact matches:
- `cito:supports` — provides factual or intellectual support
- `cito:extends` — extends facts, ideas, or understandings
- `cito:qualifies` — places conditions upon

CiTO close matches:
- `cito:citesAsSourceDocument` — derived from
- `cito:usesMethodIn` — enables method
- `cito:disagreesWith` — dissociates with

Claim-relations extensions (subproperties of CiTO, see `claim-relations.ttl`):
- `claimrel:requires` — logical prerequisite
- `claimrel:tests` — empirical test (outcome-neutral)
- `claimrel:entails` — logical entailment (deductive)
- `claimrel:interprets` — theoretical reframing
- `claimrel:scopes` — delimits domain of applicability
- `claimrel:rulesOut` — eliminates a hypothesis (sub of `cito:refutes`)
- `claimrel:replicates` — empirical replication (sub of `cito:confirms`)
- `claimrel:contradicts` — incompatible findings (sub of `cito:disagreesWith`)

## Example: one claim in OXA JSON

```json
{
  "type": "Claim",
  "identifier": "distal-inhib-drops-firing-02hz",
  "slug": "distal-inhib-drops-firing-02hz",
  "role": "empirical",
  "panel": ["fig4", "fig5"],
  "epistemicStrength": "strong",
  "children": [
    {
      "type": "Text",
      "value": "Doubling distal dendritic inhibition reduces somatic firing rate from approximately 5.5 Hz to approximately 0.2 Hz, primarily by suppressing dendritic Ca²⁺ and NMDA spikes."
    }
  ],
  "relations": [
    {
      "xref": "prediction-distal-dendritic-spike-mechanism",
      "relationType": "claimrel:tests"
    },
    {
      "xref": "perisomatic-inhib-drops-firing-07hz",
      "relationType": "cito:disagreesWith"
    },
    {
      "xref": "l5-model-single-cell-scope",
      "relationType": "claimrel:requires"
    }
  ],
  "metadata": {
    "confidence": "high",
    "sources": ["results-reader", "caption-reader"],
    "extractionPath": "jats"
  }
}
```

## Example: a paper's claim graph as an OXA document

A paper becomes an OXA `Article` (or equivalent document root) containing a `ClaimGraph` section — a container for all the paper's claims with their typed edges:

```json
{
  "type": "Article",
  "identifier": "headley-2026-inhibitory-rhythms",
  "metadata": {
    "doi": "10.7554/eLife.95562",
    "title": "Spatially targeted inhibitory rhythms differentially affect neuronal integration",
    "authors": ["Drew B Headley", "Benjamin Latimer", "Adin Aberbach", "Satish S Nair"]
  },
  "children": [
    {
      "type": "Heading",
      "level": 1,
      "children": [{ "type": "Text", "value": "Claims" }]
    },
    {
      "type": "Claim",
      "identifier": "hypothesis-distinct-compartmental-roles",
      "role": "hypothesis",
      "epistemicStrength": "moderate",
      "children": [
        {
          "type": "Text",
          "value": "Perisomatic and distal dendritic inhibition serve distinct computational roles in regulating neuronal output."
        }
      ],
      "relations": [
        { "xref": "prediction-distal-dendritic-spike-mechanism", "relationType": "claimrel:entails" },
        { "xref": "prediction-beta-optimal-distal", "relationType": "claimrel:entails" }
      ]
    },
    {
      "type": "Claim",
      "identifier": "prediction-distal-dendritic-spike-mechanism",
      "role": "prediction",
      "children": [
        {
          "type": "Text",
          "value": "Distal inhibition should selectively reduce burst firing by suppressing dendritic Ca²⁺ and NMDA spikes."
        }
      ],
      "relations": [
        { "xref": "hypothesis-distinct-compartmental-roles", "relationType": "cito:citesAsSourceDocument" },
        { "xref": "distal-inhib-drops-firing-02hz", "relationType": "claimrel:tests" }
      ]
    }
  ]
}
```

## How this fits in OXA

| OXA concept | How Claim uses it |
|:------------|:------------------|
| Node structure (RFC0002) | Parent node: `type` + `children` + type-specific fields |
| Naming convention (RFC0003) | PascalCase: `Claim`, `ClaimRelation` |
| Cross-references | `identifier` on claims, `xref` on relations (same pattern as `Cite`) |
| CiTO intent (RFC0005) | `relationType` field parallels `Cite.intent` |
| Metadata (RFC0006) | Extraction provenance, confidence, source agents |
| Extension data (RFC0002) | Experimental fields start in `data`, promote via RFC |
| AT Protocol | Block type in `pub.oxa.blocks.defs`; proposition as faceted text; edges as structured fields |

## What this replaces

Current claim files are YAML-frontmatter markdown:

```yaml
---
uuid: 26819b09-...
slug: distal-inhib-drops-firing-02hz
claim: Doubling distal dendritic inhibition...
claim-type: empirical
role: empirical
panel: fig4, fig5
epistemic: strong
tests:
  - prediction-distal-dendritic-spike-mechanism
dissociates-with:
  - perisomatic-inhib-drops-firing-07hz
requires:
  - l5-model-single-cell-scope
---
```

The OXA JSON carries the same information in a standards-aligned format that any OXA-aware tool can consume.
