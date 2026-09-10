# vendor/

MIRA's schema, copied here unmodified so validation is reproducible offline and gives the
same answer next year as it does today.

| | |
|---|---|
| Source | <https://github.com/MIRA-science/schema> |
| Commit | `483f0b21480c0f4ced9c1519fc0f6df2b8617cfe` |
| Licence | Apache-2.0 — see the upstream `LICENSE` |
| Files | `mira.shacl` (shapes), `mira.ttl` (ontology), `mira.jsonld` (context) |

**Why pinned rather than fetched.** MIRA is a draft — `bibo:status status:draft`,
`owl:versionInfo "0.1 (tentative)"` — with no tags, no releases and no changelog. It moves.
MIRA's own extractor pins this same commit. A validation result is only meaningful next to
the schema version it was produced against.

Re-fetch, or check these copies against upstream:

```bash
SHA=483f0b21480c0f4ced9c1519fc0f6df2b8617cfe
for f in mira.shacl mira.ttl mira.jsonld; do
  curl -fsSL "https://raw.githubusercontent.com/MIRA-science/schema/$SHA/$f" -o "vendor/$f"
done
```

Do not fetch the context from `https://mira.science/schema/context.jsonld` (404) or from
`https://mira-science.github.io/schema/mira.jsonld` (stale: it still retypes every `Study` as
a `Protocol`). `docs/schema-mapping/mira-guide.md` records both traps and how we hit them.

Used by `scripts/validate_mira.py`.
