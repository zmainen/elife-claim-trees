"""Steps 6-7 — Dependency mapping and claim file emission.

Step 6 — Dependency mapping: typed edges between claims (the edge inventory
in `docs/method.md` § 4.3). This used to be left to the analyst, with the
writer emitting `belongings: []` and a TODO. It is now inferred by a model
call — see `edges.py`, which carries the vocabulary mapping and the rule for
where each relation type is stored. Pass --no-infer-edges to skip it.

Step 7 — Write claim files: generate UUID4 per claim, derive a slug, and
write each claim as <corpus_dir>/<paper_slug>/<claim_slug>.md per the
schema in § 4. Also write a paper index.md with title, DOI, authors,
abstract, and any deposit URLs (best-effort — these come from prepare,
which has heuristic-quality metadata).
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import uuid
from datetime import date
from pathlib import Path

import yaml

from .config import Config
from .prepare import _ascii_fold
from .edges import edges_for_slug
from .schema import DraftClaimTable, ReconciledClaim
from .oxa import (
    Claim, ClaimGraph, ClaimRelation, ClaimMetadata, SourceSpan,
    Document, text_node, claim_from_reconciled, build_document, EDGE_MAP,
)

logger = logging.getLogger(__name__)


# ── Editing a claim file's frontmatter in place ──────────────────────────
# The claim files are hand-edited and machine-written both, so a re-dump of the whole
# frontmatter would reorder and reflow keys nobody touched. These edit it as text: drop the
# key if it is already there and write the new value, leaving every other line untouched. The
# questions layer and the carry-over both write keys back into an existing tree this way; the
# pattern is verify_refs.py's DOI write-back, minus the full re-serialisation.


def _read_frontmatter(path: Path) -> dict:
    """One claim file's YAML frontmatter, tolerating the empty-list-at-column-0 quirk."""
    m = re.match(r"^---\n(.*?)\n---", path.read_text(encoding="utf-8"), re.S)
    if not m:
        return {}
    body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2", m.group(1), flags=re.M)
    try:
        return yaml.safe_load(body) or {}
    except yaml.YAMLError:
        return {}


def _split_frontmatter(text: str) -> tuple[str, list[str], str] | None:
    """(opening `---\\n`, frontmatter lines, rest) or None if there is no frontmatter."""
    m = re.match(r"(?s)^(---\n)(.*?)(\n---\n.*)$", text)
    if not m:
        return None
    return m.group(1), m.group(2).split("\n"), m.group(3)


def _drop_key(lines: list[str], key: str) -> list[str]:
    """Remove a top-level `key:` and any block that hangs under it (indented or list lines)."""
    out, i = [], 0
    while i < len(lines):
        if re.match(rf"^{re.escape(key)}\s*:", lines[i]):
            i += 1
            while i < len(lines) and lines[i][:1] in (" ", "\t", "-"):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return out


def _write_key(path: Path, key: str, block: str, *, after: str | None = None) -> None:
    """Set a top-level frontmatter key to `block`, in place, without reordering other keys.

    `block` is the whole rendered value including the `key:` line. Inserted after the `after:`
    key when given and present, else appended to the end of the frontmatter.
    """
    parts = _split_frontmatter(path.read_text(encoding="utf-8"))
    if parts is None:
        return
    opening, lines, rest = parts
    lines = _drop_key(lines, key)
    new = block.split("\n")
    at = len(lines)
    if after:
        for i, l in enumerate(lines):
            if re.match(rf"^{re.escape(after)}\s*:", l):
                at = i + 1
                break
    lines[at:at] = new
    path.write_text(opening + "\n".join(lines) + rest, encoding="utf-8")


# ── Slug derivation for individual claims ────────────────────────────────


def derive_claim_slug(claim_text: str, panel: str | None = None) -> str:
    """Produce a 3-6 word hyphenated slug from a claim's text.

    Drop stopwords; take the first 3-5 content words; lowercase + hyphenate.
    Append a panel suffix if the slug would otherwise be ambiguous.
    """
    stopwords = {
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did",
        "of", "to", "in", "on", "at", "by", "for", "with", "from", "as",
        "and", "or", "but", "if", "then", "than", "that", "this", "these",
        "these", "those", "their", "its", "it", "they", "there",
        "approximately", "approximately,", "almost", "nearly",
    }
    words = re.findall(r"\b[A-Za-z][A-Za-z\-]+\b", _ascii_fold(claim_text))
    keep = []
    for w in words:
        wl = w.lower()
        if wl in stopwords:
            continue
        keep.append(re.sub(r"[^a-z0-9]+", "-", wl).strip("-"))
        if len(keep) >= 5:
            break
    if not keep:
        keep = ["claim"]
    slug = "-".join(keep)[:60].rstrip("-")
    return slug


def number_questions(claims: list[ReconciledClaim]) -> tuple[list[dict], list[str | None]]:
    """The paper's questions, numbered, and the q-id each claim addresses.

    A question is not a claim, so it lives on the paper: the distinct `addresses` texts a
    hypothesis or a rejected alternative carried, numbered q1, q2, … in order of first
    appearance. Whitespace and case are normalised for de-duplication only — two claims that
    answer the same question in slightly different words collapse to one — and the first
    spelling seen is the one kept. Returns the question list for `index.md` and, per claim in
    order, the q-id it addresses or None.
    """
    seen: dict[str, str] = {}
    order: list[tuple[str, str]] = []
    per_claim: list[str | None] = []
    for c in claims:
        text = (getattr(c, "addresses", None) or "").strip()
        if not text:
            per_claim.append(None)
            continue
        key = " ".join(text.lower().split())
        if key not in seen:
            seen[key] = f"q{len(order) + 1}"
            order.append((seen[key], text))
        per_claim.append(seen[key])
    return [{"id": qid, "text": text} for qid, text in order], per_claim


def _unique_slugs(claims: list[ReconciledClaim]) -> list[str]:
    """Generate per-claim slugs; disambiguate with counter on collision."""
    raw = [derive_claim_slug(c.claim, c.panel) for c in claims]
    seen: dict[str, int] = {}
    out: list[str] = []
    for s in raw:
        if s in seen:
            seen[s] += 1
            out.append(f"{s}-{seen[s]}")
        else:
            seen[s] = 1
            out.append(s)
    return out


# ── Schema mapping: ReconciledClaim → claim file frontmatter ────────────


# Map our claim_type vocabulary to the elife-claim-trees schema (§ 4.1).
# Same vocabulary; pass through directly for now.
_CLAIM_TYPE_PASSTHROUGH = {
    "empirical", "interpretive", "existence", "synthesis", "assessment"
}


def _claim_frontmatter(
    claim: ReconciledClaim,
    slug: str,
    paper_slug: str,
    paper_doi: str,
    edges: list[dict] | None = None,
    addresses: str | None = None,
) -> dict:
    """Build the YAML frontmatter dict for one claim."""
    today = date.today().isoformat()
    fm: dict = {
        "uuid": str(uuid.uuid4()),
        "slug": slug,
        # None serialises as YAML null, matching curated files. Writing the
        # string "~" produced a quoted '~' that parsers read as text.
        "doi": None,  # per § 4.1 — claims aren't yet citable units
        "claim": claim.claim,
        "claim-type": claim.claim_type,
        "role": claim.role,
        # The question this hypothesis or alternative answers, numbered q<N> on the paper.
        # Only these two roles carry it; every other claim gets no key.
        **({"addresses": addresses} if addresses else {}),
        "concepts": [],  # § 4.1 — analyst fills in at review or in a later pass
        "priority": today,
        # Roles that are not empirical carry their role as the epistemic
        # value in the curated corpus; the rest start unassessed.
        "epistemic": (
            claim.role if claim.role in ("hypothesis", "prediction") else "tentative"
        ),
    }

    # Step 6 — dependency mapping. `requires`/`supports` live under
    # `belongings:`; every other relation is a top-level key. See
    # edges.BELONGINGS_RELATIONS for why.
    top, belongings = edges_for_slug(edges or [], slug)
    fm.update(top)
    fm["belongings"] = belongings

    # Assertions block — link the claim to its panel and source paper
    if claim.panel:
        fm["assertions"] = [
            {
                "paper-slug": paper_slug,
                "doi": paper_doi,
                "panel": claim.panel,
                "confidence": "tentative",
            }
        ]
    else:
        fm["assertions"] = [
            {
                "paper-slug": paper_slug,
                "doi": paper_doi,
                "panel": None,
                "confidence": "tentative",
            }
        ]

    # Reproductions — empty list; verification is per-paper and not
    # something extract produces. Analyst or verify.py downstream fills.
    fm["reproductions"] = []

    return fm


def _claim_body(claim: ReconciledClaim) -> str:
    """Build the prose body of a claim file.

    The body is for caveats, alternative interpretations, and reasoning
    that doesn't compress into frontmatter. We seed it with the agent
    evidence quotes and the reconciler's notes — the analyst can revise.
    """
    parts = []
    if claim.notes:
        parts.append(f"**Notes from extraction:** {claim.notes}")
        parts.append("")

    if claim.evidence_by_agent:
        parts.append(
            "<!-- Evidence quotes from the extraction agents — preserved for "
            "audit. Edit or remove as appropriate. -->"
        )
        parts.append("")
        for agent, quote in claim.evidence_by_agent.items():
            parts.append(f"**{agent}-reader evidence:**")
            parts.append(f"> {quote}")
            parts.append("")

    if not parts:
        return ""
    return "\n".join(parts).rstrip() + "\n"


def _format_claim_file(fm: dict, body: str) -> str:
    """Render frontmatter + body to a claim .md file."""
    fm_yaml = yaml.safe_dump(
        fm,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=100,
    )
    text = f"---\n{fm_yaml}---\n"
    if body:
        text += "\n" + body
    return text


# ── Paper-level index.md ─────────────────────────────────────────────────


def _format_paper_index(
    draft: DraftClaimTable,
    claim_slugs: list[str],
    questions: list[dict] | None = None,
) -> str:
    """Render <paper_slug>/index.md with title, DOI, authors, summary."""
    fm = {
        "paper-slug": draft.paper_slug,
        "title": draft.paper_title or "(title not detected)",
        "doi": draft.paper_doi,
        "url": f"https://doi.org/{draft.paper_doi}",
        "added": date.today().isoformat(),
        "claim-count": len(draft.claims),
        "extraction-path": draft.extraction_path,
        # The paper's research questions live here, not in the claim graph: a question is not
        # a claim. Each hypothesis and rejected alternative names one via `addresses`.
        **({"questions": questions} if questions else {}),
    }
    fm_yaml = yaml.safe_dump(
        fm, sort_keys=False, allow_unicode=True, default_flow_style=False
    )

    body = ["## Claims", ""]
    for c, slug in zip(draft.claims, claim_slugs):
        body.append(f"- [{slug}]({slug}.md) ({c.confidence}) — {c.claim[:120]}")
    body.append("")
    body.append("## Extraction provenance")
    body.append("")
    body.append(f"- per-agent counts: {draft.per_agent_counts}")
    body.append(f"- reconciliation strategy: {draft.config_snapshot.get('reconcile_strategy', '?')}")
    body.append(f"- prompt variant: {draft.config_snapshot.get('prompt_variant', '?')}")
    body.append("")
    return f"---\n{fm_yaml}---\n\n" + "\n".join(body)


# ── OXA write path ───────────────────────────────────────────────────────


def _reconciled_to_oxa_claim(
    claim: ReconciledClaim,
    slug: str,
) -> Claim:
    """Convert a ReconciledClaim to an OXA Claim node."""
    return claim_from_reconciled(
        claim_text=claim.claim,
        slug=slug,
        role=claim.role,
        panel=claim.panel,
        epistemic=None,  # ReconciledClaim doesn't carry epistemic strength
        confidence=claim.confidence,
        sources=[str(s) for s in claim.sources],
        evidence_by_agent={str(k): v for k, v in claim.evidence_by_agent.items()},
    )


def write_oxa_document(draft: DraftClaimTable, cfg: Config) -> Path:
    """Emit an OXA Document JSON file for a paper's claims.

    Produces <corpus_dir>/<paper_slug>.oxa.json containing a Document
    with a ClaimGraph of Claim nodes. This is the OXA-native output
    path — the source of truth for downstream tools.

    Also writes per-claim YAML markdown files for human browsing
    (backward compatibility with the existing corpus format).
    """
    if cfg.corpus_dir is None:
        raise ValueError("corpus_dir not set; cannot write OXA document")

    slugs = _unique_slugs(draft.claims)

    # Convert each reconciled claim to an OXA Claim node
    oxa_claims = []
    for claim, slug in zip(draft.claims, slugs):
        oxa_claims.append(_reconciled_to_oxa_claim(claim, slug))

    # Build the OXA Document
    doc = build_document(
        paper_slug=draft.paper_slug,
        paper_doi=draft.paper_doi,
        paper_title=draft.paper_title,
        claims=oxa_claims,
    )

    # Write the OXA JSON
    cfg.corpus_dir.mkdir(parents=True, exist_ok=True)
    oxa_path = cfg.corpus_dir / f"{draft.paper_slug}.oxa.json"

    import json
    out = doc.model_dump(mode="json", exclude_none=True)
    oxa_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))

    logger.info("OXA document: %s (%d claims)", oxa_path, len(oxa_claims))
    return oxa_path


# ── Top-level write ──────────────────────────────────────────────────────


def resolve_edges(draft: DraftClaimTable, slugs: list[str], cfg: Config) -> list[dict]:
    """The edges to write, when the caller has not already got them.

    A supplied edge answer wins over calling a backend, and goes through exactly the same
    validation — unknown slugs dropped, self-edges dropped, reciprocals synthesised. The
    route in differs; the checks do not. This exists because the deductive spine is the
    part of a claim tree that matters most and the part most easily lost to a provider
    outage: on a live Gädeke run every other stage succeeded and the edges were gone.
    """
    supplied = getattr(cfg, "edges_json", None)
    if supplied:
        from .edges import edges_from_raw
        try:
            return edges_from_raw(Path(supplied).read_text(encoding="utf-8"),
                                  slugs, source=f"supplied:{supplied}")
        except Exception as e:                                   # noqa: BLE001
            logger.warning("supplied edge file unusable (%s); writing claims without edges", e)
            return []
    if getattr(cfg, "infer_edges", True):
        from .edges import infer_edges
        try:
            return infer_edges(draft, slugs, cfg)
        except Exception as e:                                   # noqa: BLE001
            logger.warning("edge inference failed (%s); writing claims without edges", e)
    return []


# ── replacing a version, and keeping the one replaced ────────────────────


def current_claim_tree_version(cfg: Config, paper_slug: str) -> int:
    """The `claim-tree` version the ledger records for this paper, or 1 if none.

    A run of the layer is by definition the *next* version; the tree on disk is the *current*
    one, so it is archived under the version it holds now. The ledger is the authority — read
    it directly rather than importing scripts/pipeline.py, which is not on this package's path.
    """
    p = cfg.root / "runs" / paper_slug / "ledger.jsonl"
    if not p.is_file():
        return 1
    versions = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except json.JSONDecodeError:
            continue
        if e.get("layer") == "claim-tree":
            versions.append(e.get("v", 0))
    return max(versions) if versions else 1


def archive_dir(cfg: Config, paper_slug: str) -> Path:
    """Where the current tree is moved when it is replaced: runs/<paper>/claim-tree.v<N>/."""
    return cfg.root / "runs" / paper_slug / f"claim-tree.v{current_claim_tree_version(cfg, paper_slug)}"


def _archive_tree(paper_dir: Path, dest: Path) -> None:
    """Move a paper's claim files aside so every version's bytes stay addressable.

    A move, not a copy: what is left in `claims/` must be only the new tree, and the old bytes
    must survive somewhere a run can point at. `dest` is emptied first, so replacing twice in
    one session does not fold two versions together.
    """
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)
    for f in sorted(paper_dir.iterdir()):
        shutil.move(str(f), str(dest / f.name))
    paper_dir.rmdir()


def write_claim_files(draft: DraftClaimTable, cfg: Config,
                      edges: list[dict] | None = None, *,
                      replace: bool = False) -> list[Path]:
    """Emit claim files into <corpus_dir>/<paper_slug>/.

    Returns the list of paths written (the index plus one per claim).

    Refuses to overwrite a non-empty directory: the claim files are edited afterwards by hand
    and by later layers, and a silent overwrite would discard work no ledger records. `replace`
    is the sanctioned way through — it moves the current tree to runs/<paper>/claim-tree.v<N>/
    first, so the version being replaced stays addressable as files, then writes the new one.

    `edges` comes from the edge-inference layer, which has already run and written them.
    Passing None re-derives them, which is a second paid call for an answer already on
    disk — kept only for `evaluate`, which runs the chain into a temp tree with no ledger.
    """
    if cfg.corpus_dir is None:
        raise ValueError("corpus_dir not set; cannot write claim files")

    paper_dir = cfg.corpus_dir / draft.paper_slug
    if paper_dir.exists() and any(paper_dir.iterdir()):
        if not replace:
            raise FileExistsError(
                f"refusing to overwrite non-empty {paper_dir}. "
                "Pass --replace to archive it to runs/<paper>/claim-tree.v<N>/ and write anew."
            )
        _archive_tree(paper_dir, archive_dir(cfg, draft.paper_slug))
    paper_dir.mkdir(parents=True, exist_ok=True)

    slugs = _unique_slugs(draft.claims)
    written: list[Path] = []

    # An edge names two slugs and both must be assigned before any file is written.
    if edges is None:
        edges = resolve_edges(draft, slugs, cfg)

    # The paper's questions, and the q-id each claim addresses (None for most claims).
    questions, addresses = number_questions(draft.claims)

    # Per-claim files
    for claim, slug, addr in zip(draft.claims, slugs, addresses):
        fm = _claim_frontmatter(
            claim, slug, draft.paper_slug, draft.paper_doi, edges, addresses=addr
        )
        body = _claim_body(claim)
        text = _format_claim_file(fm, body)
        path = paper_dir / f"{slug}.md"
        path.write_text(text)
        written.append(path)

    # Paper index.md
    index_path = paper_dir / "index.md"
    index_path.write_text(_format_paper_index(draft, slugs, questions))
    written.append(index_path)

    return written


# ── carrying a version's other-layer content across a replacement ─────────
# The induction chain writes claims, panels, evidence and edges. It does not produce the
# `stance` layer's rejected alternatives, or the `verification` layer's reproduction records —
# those were added to the previous version by other layers and by hand, and a straight replace
# would drop them. This carries them onto the new tree: the `alt-` files whole, the eliminative
# edges that named them re-aimed at the new claim that took each source's place, and each
# reproduction record copied onto the paired claim with a note that it was made against a
# differently worded one. The `questions` layer's `addresses:` links are not carried — they name
# slugs the new tree does not have, so that layer is re-run against the new tree instead.


def _find_pairs(cfg: Config, paper_slug: str) -> Path | None:
    """The slug map from the previous version to the new one: the paper's latest match pairs.

    Replacing a version needs to know which new claim took each old claim's place, and the
    evaluation harness already computed exactly that — one `{committed, rerun}` pair per old
    slug it could align. Pick the highest-versioned `match.v<N>.pairs.json`, which is the map
    for the re-run this write is landing. Absent for a paper never evaluated, in which case the
    edges and records that need a mapping are recorded unplaced rather than guessed at.
    """
    d = cfg.root / "runs" / paper_slug / "evaluation"
    if not d.is_dir():
        return None
    cands = sorted(d.glob("match.v*.pairs.json"),
                   key=lambda p: int(re.search(r"\.v(\d+)\.", p.name).group(1))
                   if re.search(r"\.v(\d+)\.", p.name) else 0)
    return cands[-1] if cands else None


def carry_over(cfg: Config, paper_slug: str, archive: Path,
               pairs_path: Path | None = None) -> dict:
    """Carry `alt-` claims, their `rules-out` edges, and reproduction records forward.

    `archive` is the tree just moved aside (the version being replaced); the new tree is in
    `cfg.corpus_dir/<paper>`. Returns a summary and writes it to `archive/carried.json`, which
    records what landed where and what could not be placed — an unmapped source is written down,
    not guessed. A no-op that still writes the summary when the archive holds nothing to carry.
    """
    new_dir = cfg.corpus_dir / paper_slug
    pairs_path = pairs_path or _find_pairs(cfg, paper_slug)
    v1_to_v2: dict[str, str] = {}
    if pairs_path and pairs_path.is_file():
        for p in json.loads(pairs_path.read_text(encoding="utf-8")):
            if p.get("committed") and p.get("rerun"):
                v1_to_v2[p["committed"]] = p["rerun"]

    summary: dict = {
        "paper": paper_slug,
        "archived_from": str(archive.relative_to(cfg.root)),
        "pairs": str(pairs_path.relative_to(cfg.root)) if pairs_path else None,
        "alt_claims": [], "rules_out": [], "reproductions": [], "unplaced": [],
    }

    def target_file(v1_slug: str, kind: str):
        """The new-tree file that took v1_slug's place, or None with an `unplaced` note logged."""
        v2 = v1_to_v2.get(v1_slug)
        if not v2:
            summary["unplaced"].append({"kind": kind, "from": v1_slug, "why": "no pair in the match map"})
            return None
        f = new_dir / f"{v2}.md"
        if not f.is_file():
            summary["unplaced"].append({"kind": kind, "from": v1_slug, "to": v2,
                                        "why": "paired claim not in the new tree"})
            return None
        return f

    # 1. The rejected alternatives, whole. They keep their own `alt-` slug — the new tree has no
    #    claim for them, so there is nothing to map and nothing to collide with.
    for f in sorted(archive.glob("alt-*.md")):
        shutil.copy2(f, new_dir / f.name)
        summary["alt_claims"].append(f.stem)

    # 2. Every `rules-out` edge that named one of those alternatives, re-aimed at the new claim
    #    that took its source's place. Unioned with any the edge-inference layer already wrote,
    #    so re-aiming adds an edge rather than replacing the file's own.
    for f in sorted(archive.glob("*.md")):
        if f.name == "index.md" or f.name.startswith("alt-"):
            continue
        alts = [t for t in (_read_frontmatter(f).get("rules-out") or [])
                if isinstance(t, str) and t.startswith("alt-")]
        if not alts:
            continue
        tf = target_file(f.stem, "rules-out")
        if tf is None:
            continue
        have = [t for t in (_read_frontmatter(tf).get("rules-out") or []) if isinstance(t, str)]
        merged = have + [a for a in alts if a not in have]
        block = yaml.safe_dump({"rules-out": merged}, sort_keys=False, allow_unicode=True,
                               default_flow_style=False, width=100).rstrip("\n")
        _write_key(tf, "rules-out", block, after="epistemic")
        summary["rules_out"].append({"alternatives": alts, "from": f.stem, "to": tf.stem})

    # 3. Every reproduction record, onto the paired claim, each block stamped `carried_from` so
    #    the record says it was made against a claim worded differently in the previous version.
    for f in sorted(archive.glob("*.md")):
        if f.name == "index.md":
            continue
        reps = _read_frontmatter(f).get("reproductions") or []
        if not reps:
            continue
        tf = target_file(f.stem, "reproductions")
        if tf is None:
            continue
        stamped = [{"carried_from": f.stem, **r} if isinstance(r, dict) else r for r in reps]
        block = yaml.safe_dump({"reproductions": stamped}, sort_keys=False, allow_unicode=True,
                               default_flow_style=False, width=100).rstrip("\n")
        _write_key(tf, "reproductions", block)
        summary["reproductions"].append({"from": f.stem, "to": tf.stem, "records": len(reps)})

    (archive / "carried.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
    return summary
