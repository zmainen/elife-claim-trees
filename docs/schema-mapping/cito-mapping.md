# CiTO edge-type mapping

Maps the claim-trees edge vocabulary to CiTO (Citation Typing Ontology) IRIs. CiTO is designed for document-to-document relations, but its OWL axioms don't constrain domain/range — claim-level entities are valid subjects and objects.

Three categories: exact CiTO matches, close matches (usable with documented semantic narrowing), and extensions (new properties in our namespace, declared as subproperties of CiTO for entailment compatibility).

## Mapping table

| Claim-trees edge | CiTO property | IRI | Match | Notes |
|:-----------------|:-------------|:----|:------|:------|
| `supports` | `cito:supports` | `cito:supports` | Exact | "Provides intellectual or factual support" |
| `extends` | `cito:extends` | `cito:extends` | Exact | "Extends facts, ideas or understandings" |
| `qualifies` | `cito:qualifies` | `cito:qualifies` | Exact | "Places conditions upon statements, ideas or conclusions" |
| `derived-from` | `cito:citesAsSourceDocument` | `cito:citesAsSourceDocument` | Close | "Derived from" maps to "the entity from which the citing entity is derived" |
| `enables-method` | `cito:usesMethodIn` | `cito:usesMethodIn` | Close | "Uses a method detailed in the cited entity" — directionality fits |
| `dissociates-with` | `cito:disagreesWith` | `cito:disagreesWith` | Close | Dissociation is softer than disagreement; documented narrowing |
| `rules-out` | `claimrel:rulesOut` | subPropertyOf `cito:refutes` | Extension | Eliminates a hypothesis — narrower than refutation |
| `replicates` | `claimrel:replicates` | subPropertyOf `cito:confirms` | Extension | Empirical replication — specific mechanism of confirmation |
| `contradicts` | `claimrel:contradicts` | subPropertyOf `cito:disagreesWith` | Extension | Findings incompatible with the cited claim |
| `requires` | `claimrel:requires` | subPropertyOf `cito:cites` | Extension | Logical prerequisite — no CiTO equivalent |
| `tests` | `claimrel:tests` | subPropertyOf `cito:cites` | Extension | Empirical test of a prediction — outcome-neutral |
| `entails` | `claimrel:entails` | subPropertyOf `cito:cites` | Extension | Logical entailment — deductive, not evidential |
| `interprets` | `claimrel:interprets` | subPropertyOf `cito:cites` | Extension | Theoretical reframing of empirical results |
| `scopes` | `claimrel:scopes` | subPropertyOf `cito:cites` | Extension | Delimits domain of applicability |

## Coverage summary

- **3 exact matches**: supports, extends, qualifies
- **3 close matches**: derived-from, enables-method, dissociates-with
- **8 extensions**: rules-out, replicates, contradicts, requires, tests, entails, interprets, scopes

## Extension vocabulary

The 8 extensions are defined in a claim-relations namespace as subproperties of CiTO properties. This preserves entailment: a SPARQL query for `cito:cites` retrieves all edges; a query for `cito:refutes` retrieves `rulesOut` edges.

See `claim-relations.ttl` for the formal OWL definitions.

## Design decisions

**Why subproperties, not separate properties?** CiTO compatibility through entailment. Any tool that queries CiTO properties will find our edges. Our extensions add precision; CiTO provides the base.

**Why not just use CiTO directly?** Five of our edge types have no CiTO equivalent. The claim-level relationships CiTO misses (logical prerequisite, empirical test, deductive entailment, theoretical interpretation, scope delimitation) are the ones that define the argument structure of a scientific paper. These are precisely the relationships that distinguish a claim graph from a citation graph.

**Can these extensions become part of CiTO?** Potentially. CiTO is maintained by Shotton and Peroni (University of Bologna). The SPAR project is active. A proposal to add claim-level relation types would be well-motivated if we can demonstrate their use on a real corpus. This is independent of the OXA RFC but complementary.
