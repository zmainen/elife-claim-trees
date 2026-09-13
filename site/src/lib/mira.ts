// Which relation types a reader of core MIRA can actually interpret.
//
// The table is not written here, and must not be. corpus-facts.json carries
// `mira_mapping.relations`, generated from scripts/export_mira.py — the exporter's own
// declaration table — and `declared_under` on each row names the core MIRA predicate the
// type is declared beneath. A row with `declared_under: null` is exported as a bare
// `haak:reldef/<type>` hanging at AbstractRelationDef with no core parent.
//
// That distinction is the honest one, and it is narrower than "MIRA drops the edge". Every
// paper's formats.json reports `mira.lost: 0` — the triples survive into the strict file.
// What does not survive is their meaning: a consumer that knows only `mira:supports` and
// `mira:opposes` reads a `haak:reldef/entails` triple and cannot tell whether it asserts
// support, opposition, or something else entirely. The exporter's own counters call these
// `neutral`, against `inherits_core` for the rest, and that is the split the graph's MIRA
// view draws.
import facts from '../data/corpus-facts.json';

export type MiraParent = 'mira:supports' | 'mira:opposes' | null;

interface MappingRow {
  relation: string;
  declared_under: MiraParent;
  inverse_of: string | null;
}

const ROWS = ((facts as any).mira_mapping?.relations ?? []) as MappingRow[];

/** The core MIRA predicate each relation type is declared beneath, or null for none. */
export const MIRA_PARENT: Record<string, MiraParent> =
  Object.fromEntries(ROWS.map(r => [r.relation, r.declared_under ?? null]));

/** Types the exporter emits only as the inverse of another type — `derived-from` is the
 *  inverse of `entails`, so it reaches MIRA only as an entails triple pointing the other
 *  way, and entails itself declares no core parent. */
export const MIRA_INVERSE_OF: Record<string, string | null> =
  Object.fromEntries(ROWS.map(r => [r.relation, r.inverse_of ?? null]));

/** True when a core-MIRA consumer can read this relation as support or opposition. */
export function readableInCoreMira(rel: string): boolean {
  return MIRA_PARENT[rel] === 'mira:supports' || MIRA_PARENT[rel] === 'mira:opposes';
}

/** The relation types this corpus uses that declare no core MIRA predicate, in the order
 *  the exporter's table lists them. Derived, never typed out. */
export const NO_CORE_PREDICATE: string[] =
  ROWS.filter(r => !readableInCoreMira(r.relation)).map(r => r.relation);
