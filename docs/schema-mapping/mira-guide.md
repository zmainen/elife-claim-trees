# MIRA: a working guide

What MIRA is, how its data is actually shaped, how we convert to it, and where our
conversion currently falls short. Written because we nearly published a criticism of MIRA
that was a fact about our own exporter, and because almost nothing here is discoverable
without reading the schema source.

Every claim below is either quoted from a source or was checked by running something. Where
we are guessing, it says so.

## Official sources

| | |
|---|---|
| Docs site | <https://mira.science/schema/> |
| Schema repository | <https://github.com/MIRA-science/schema> |
| Ontology namespace | `http://purl.org/mira-science/mira#` |
| **JSON-LD context** | **<https://purl.org/mira-science/mira.jsonld>** |
| Reference instance | `sampleData.json` in the schema repo |

Two URLs that look right and are not:

- `https://mira.science/schema/context.jsonld` — **404s.** We shipped it for a week.
- `https://mira-science.github.io/schema/mira.jsonld` — **stale and wrong.** GitHub Pages
  for that repo is served from the `schema-explainer` branch, which predates PR #28; the copy
  there still contains `"Study": "mira:Protocol"`, silently retyping every `Study` node as a
  `Protocol`. MIRA's own demo corpus points at it.

Do not use the ontology namespace as a context either. `http://purl.org/mira-science/mira#`
is a namespace, not a context document: a JSON-LD parser fetches it, gets RDF, and fails
before validating anything. We shipped that too, which is how we discovered it.

## Status: this is a draft, and it moves

> `mira.ttl` — `bibo:status status:draft ; owl:versionInfo "0.1 (tentative)"`

> `README.md` — "This is a **DRAFT** version of the preliminary schema we have begun
> sketching at the MIRA workshop"

No tags, no releases, no changelog. **Pin by commit.** MIRA's own extractor does
(`MIRA-extraction/schema/Makefile` pins `483f0b21`), and so should we.

## The shape of the data

MIRA has 14 classes and 30 properties. The ones that matter for a claim graph:

- **Nodes** — `Claim`, `Evidence`, `Question`, `Study`, `Protocol`, `SourceDocument`,
  `Request`.
- **Relations** — `AbstractRelationDef`, `RelationDef`, `RelationInstance`.
- **Core relation predicates** — `supports`, `opposes`, and their inverses `supportedBy`,
  `opposedBy`.

### Relations are reified, not inlined

This is the single most important thing, and it is not written down anywhere in MIRA's prose.

The context defines `supports` as a usable predicate:

> `mira.jsonld` — `"supports": { "@id": "mira:supports", "@type": "@id" }`

But **no node class carries that slot.** `supports`/`opposes` sit on an `Argument` mixin, and
in `mira.yaml` neither `Claim` nor `Evidence` mixes `Argument` in:

> `mira.yaml` — `Claim: … mixins: [NodeSchema]  slots: [addresses]`

Every generated node shape is closed:

> `mira.shacl` — `mira:Claim a sh:NodeShape ; … sh:closed true`

so a `Claim` carrying `supports` is rejected outright. MIRA's own data authors hit this and
wrote the rule down:

> `MIRA-science/demo-MIRA-graph-data` — "the closed Evidence node shape rejects it as an
> inline attribute. **Resolve the relation, not a node property.**"

> `MIRA-science/MIRA-extraction` #1 — "**relations reified as `RelationInstance` objects with
> `source` / `destination` / `predicate`**"

So an edge is a *node*:

```json
{ "@id": "…/edge/1", "@type": ["…/reldef/supports"],
  "source": "…/claim/B", "destination": "…/claim/A",
  "title": "[[B]] -supports-> [[A]]",
  "creator": "…", "created": "…", "modified": "…" }
```

### Declaring a relation MIRA does not define

Three classes, and the difference between the first two is exactly `domain` and `range`:

> `discoursegraphs_base.yaml` —
> `AbstractRelationDef: … abstract: true; mixin: true` — no slots
> `RelationDef: … slots: [domain, range]; mixins: [AbstractRelationDef]`
> `RelationInstance: … slots: [source, destination]`

`AbstractRelationDef` names the relation type; `RelationDef` binds what it may connect;
`RelationInstance` is the edge. **`AbstractRelationDef` is a neutral root** — it carries no
supporting or opposing commitment — which is what lets us declare relations that are neither.

That matters for us. Six of our fourteen relations are not specialisations of support or
opposition, and `subClassOf: ["mira:supports"]` would misstate them rather than compress
them. Making `scopes` a kind of `supports` would assert that a boundary condition is
*evidence for* the claim it limits, which reverses the meaning. So:

- **`supports`, `tests`, `validates`, `confirms`, `extends`, `replicates`** → declare
  `subClassOf: ["mira:supports"]`.
- **`contradicts`, `rules-out`, `dissociates-with`** → `subClassOf: ["mira:opposes"]`.
- **`scopes`, `requires`, `entails`, `derived-from`, `interprets`, `enables-method`** →
  `AbstractRelationDef` and nothing more.

Mint these in **our** namespace, not `mira:`. MIRA's demo corpus mints `mira:informs` for a
term MIRA does not own; that is a mistake worth not copying.

### Inverses are declared, never materialised

> `mira.ttl` — `mira:is_grounded_in a dgb:RelationDef ; … owl:inverseOf mira:grounds`

The inverse is a property of the *declaration*. Nothing in MIRA's 942-node demo graph emits
inverse edges. So for our genuine pair — `entails` / `derived-from` — declare both types,
link them with `inverseOf`, and emit edges **one direction only**.

### Two traps

**Write full CURIEs in `subClassOf`.** The context declares it `"@type": "@id"`, not
`"@vocab"`, so a bare `"Claim"` resolves against the document's base URI. In MIRA's own
`sampleData.json`, none of the `subClassOf` links actually point at MIRA — they dangle into
`https://example.org/`. Write `"mira:Claim"`.

**Do not put `RelationInstance` in an edge's `@type`.** `sampleData.json` does not; the demo
corpus and MIRA's extractor do, and both fail validation because of it. We follow the sample.
This is a place where our best guess diverges from two of three MIRA artifacts, and it may
reverse — see the open questions.

## What MIRA has no vocabulary for

**Verification.** Not "what a claim rests on" — MIRA has `observationBase` and
`observationOriginActivity` for that — but *whether anyone recomputed the value and what came
out*.

`prov.yaml` is deliberately two classes (`Activity`, `Entity`) and says so. `Protocol` has no
slots at all. A search across the whole MIRA organisation returns zero hits for "verif",
"replicat" or "reproduc" outside a licence file. The nearest live proposal, PR #32, adds an
`Evaluation` — a subjective rating on a named scale — which does not carry "I ran this code
against that deposited file and got 0.184 where the paper printed 0.185".

This is the one place where our earlier claim survives contact with the source, and it is
worth stating as a contribution rather than a complaint: we have a corpus that motivates a
`Verification` node, and MIRA has an open issue (#35) already proposing adjacent vocabulary.

## How we convert

`scripts/export_mira.py` reads a claim tree and writes three files per paper into `exports/`.

| File | What it is |
|---|---|
| `<slug>.mira.jsonld` | the graph, intended to be MIRA-conformant |
| `<slug>.mira-extended.jsonld` | the same plus a `haak:` namespace for what MIRA cannot express |
| `<slug>.gap-report.md` | what the conversion could not carry, and why |

Mapping, which is data in `ROLE_TO_TYPE` rather than logic, because every row is a decision
someone should be able to disagree with:

| Claim role | MIRA type |
|---|---|
| `hypothesis`, `prediction`, `interpretation`, `synthesis`, `assessment`, `scope` | `mira:Claim` |
| `empirical`, `control` | `mira:Evidence` |
| `methodological` | `mira:Protocol` |
| `literature-context` | `dg:SourceDocument` |

MIRA requires every `Claim` to address a `Question`, and a claim tree has no such node, so
the exporter derives one from each hypothesis and **flags it as synthesised** rather than
presenting it as ours.

### Our export does not currently validate

Verified, not assumed. Against the pinned shapes:

```
Conforms: False
Results (323)
```

The cause is the encoding: we emit relations as predicates on claim nodes, and every node
shape is closed. Rewriting the exporter to the reified form is outstanding work, and until it
lands **the files in `exports/` should be treated as a lossless intermediate rather than as
conformant MIRA.**

Two things are already fixed: the context URL, and the loss. Every relation the tree holds is
now carried — 916 of 916 corpus-wide — where the exporter previously dropped 623.

### Validating

```bash
SHA=483f0b21480c0f4ced9c1519fc0f6df2b8617cfe
mkdir -p vendor
for f in mira.shacl mira.ttl mira.jsonld; do
  curl -fsSL "https://raw.githubusercontent.com/MIRA-science/schema/$SHA/$f" -o "vendor/$f"
done
pyshacl -s vendor/mira.shacl -sf turtle -e vendor/mira.ttl \
        -df json-ld exports/<slug>.mira.jsonld
```

A caveat that matters when reading any result: **the generated shapes have bugs of their
own.** `gen-shacl` renders `subproperty_of` as an `sh:in` value list of slot *names*, which
no IRI can satisfy, disabling eight predicates. `prov:Activity` and `prov:Entity` are closed
shapes with zero allowed properties, so every `Study` fails. MIRA's own demo corpus produces
3,707 violations against its own schema; its extractor passes only through a patch harness
that says so. "Validates against MIRA" currently means "validates against MIRA plus
acknowledged patches", and that is worth stating whenever a green result is reported.

## Open questions for the MIRA authors

Ours to ask, not to decide:

1. Should `Claim` and `Evidence` mix in `Argument` in `mira.yaml`? They already do in
   `discoursegraphs.yaml` and `mira.ttl`. This decides whether an inline `supports` is ever
   legal.
2. Is the reified relation node the intended encoding? A line in the README would save every
   consumer deriving it from closed-shape failures, as at least three of us now have.
3. `RelationSchema` appears in `mira.jsonld` with no class behind it anywhere in the repo.
   Remove, or is a definition missing?
4. `sh:closed true` on every node shape leaves no extension point. Is a sanctioned mechanism
   planned? (Already blocking issue #25.)
5. `prov:Activity` and `prov:Entity` as closed empty shapes make every `Study` invalid.
6. The `gen-shacl` `sh:in` artifact — known LinkML issue with the forked generator?
7. `subClassOf` is `@type: "@id"`, so bare terms in `sampleData.json` resolve to the document
   base rather than the vocabulary. Should it be `"@vocab"`?
8. GitHub Pages serves a stale context with `"Study": "mira:Protocol"`.
9. **Would MIRA accept a `Verification` node type** — a recomputation of a claim's value from
   deposited data, carrying the code, the data identity, the reproduced value and the
   published value? We have the corpus to motivate it.
10. `mira:scope` is already taken on the `grants-proposal-1` branch, for a project's
    subject-matter scope. If `scopes` ever goes upstream, the name needs settling.

## Provenance of this guide

The schema reading was done by an agent against the sources named above, and the load-bearing
claims were re-checked directly: the context URL failure and the 323 validation violations
were reproduced here before being written down. Claims about MIRA's *intent* — as opposed to
its files — are marked as uncertain throughout, because intent is not in the repository.
