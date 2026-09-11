"""The prompt contract: the part of every prompt that is generated rather than written.

Every model call in induction receives two things. A *task* — a page saying what this role
reads and what to look for, written by hand in `extract/prompts/<role>.md`. And the *contract*
— what a claim is, what each role and relation means, and the exact shape to return — which is
the same for every role and is rendered here from the code that already defines it:

    scripts/relations.py             relations, direction, corpus examples, confusable pairs
    elife_extract/vocabulary.py      roles, claim types, confidence
    elife_extract/schema.py          the pydantic models the output is parsed into

The rendered files are committed under `extract/prompts/contract/` and declared as inputs of
the layers that receive them, so editing a definition regenerates the contract and the ledger
marks every run that read the old one stale. `contract --check` fails when the committed files
are not what the sources would generate, and `make check` runs it.

Examples are quoted from the claim files by (paper, slug). A slug the corpus no longer has
fails generation: the contract shows real claims or nothing.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import yaml

from . import schema, vocabulary

CONTRACT_DIR = "contract"
FILES = ("vocabulary.md", "schema-candidate.md", "schema-draft.md")


# ── sources ──────────────────────────────────────────────────────────────


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _relations(root: Path):
    """`scripts/relations.py`, loaded by path: it is a script's module, not a package's."""
    p = root / "scripts" / "relations.py"
    spec = importlib.util.spec_from_file_location("relations", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def _claim(root: Path, paper: str, slug: str) -> dict:
    p = root / "claims" / paper / f"{slug}.md"
    if not p.is_file():
        raise FileNotFoundError(f"contract example names {paper}/{slug}, which is not in claims/")
    m = re.match(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S)
    # Some committed files put an empty list at column 0 on the line after its key, which
    # strict YAML rejects; the same normalisation cli._load_claim_frontmatter applies.
    body = re.sub(r"^([A-Za-z0-9_-]+):\n(\[\]|\{\})\s*$", r"\1: \2", m.group(1) if m else "",
                  flags=re.M)
    fm = yaml.safe_load(body) or {}
    text = " ".join(str(fm.get("claim") or "").split())
    return {"slug": slug, "paper": paper, "claim": text, "role": fm.get("role")}


def _quote(root: Path, paper: str, slug: str) -> str:
    c = _claim(root, paper, slug)
    return f"`{slug}` ({c['role']}, {paper.split('-')[0].title()}): “{c['claim']}”"


# ── vocabulary.md ────────────────────────────────────────────────────────


def render_vocabulary(root: Path | None = None) -> str:
    root = root or _repo_root()
    rel = _relations(root)
    out: list[str] = []
    w = out.append

    w("# The claim vocabulary")
    w("")
    w("Generated from `extract/elife_extract/vocabulary.py` and `scripts/relations.py` by "
      "`elife-extract contract --write`. Do not edit; edit the source and regenerate. Every "
      "example is a claim in the corpus, quoted from its file.")
    w("")
    w("A claim is one declarative sentence in active voice, quantitative where the result is "
      "quantitative, carrying the paper's own epistemic verb. It has a **claim type** (what "
      "kind of proposition it is), a **role** (the work it does in this paper's argument), and "
      "**relations** to other claims. Type and role are independent axes: a measurement can "
      "play the role of a result, a control or a scope condition.")
    w("")

    # Claim types
    w("## Claim types")
    w("")
    w("| `claim_type` | Meaning |")
    w("|:--|:--|")
    for name, meaning in vocabulary.CLAIM_TYPES:
        w(f"| `{name}` | {meaning} |")
    w("")

    # Roles
    w("## Roles")
    w("")
    w("Nine roles. The signal phrases are what the prose says when it is doing that work; they "
      "are cues, not tests.")
    w("")
    for r in vocabulary.ROLES:
        paper, slug = r["example"]
        w(f"### `{r['role']}`")
        w("")
        w(r["definition"])
        w("")
        w(f"- Typical claim type: `{r['typical_claim_type']}`")
        w(f"- Signals: {', '.join(f'“{s}”' for s in r['signals'])}")
        w(f"- Carries: {r['carries']}")
        w(f"- Example: {_quote(root, paper, slug)}")
        w("")

    w("### Roles that are confused for each other")
    w("")
    for a, b, why, ex_a, ex_b in vocabulary.ROLE_CONFUSABLE:
        w(f"**`{a}` versus `{b}`.** {why}")
        w("")
        w(f"- `{a}`: {_quote(root, *ex_a)}")
        w(f"- `{b}`: {_quote(root, *ex_b)}")
        w("")

    # Relations
    w("## Relations")
    w("")
    w("A relation is a proposition about logical structure between two claims, not a citation. "
      "Each is directed; the direction column says which end is which. `derived-from` is "
      "written mechanically as the reciprocal of `entails` and should not be emitted.")
    w("")
    w("| Relation | Asserts | Direction |")
    w("|:--|:--|:--|")
    for name in sorted(rel.EDGE_KEYS):
        w(f"| `{name}` | {rel.DESCRIPTIONS[name]} | {rel.DIRECTION.get(name, '')} |")
    w("")
    w("### One example of each")
    w("")
    for name in sorted(rel.EDGE_KEYS):
        ex = rel.EXAMPLE.get(name)
        if not ex:
            w(f"- `{name}`: no use in the corpus yet.")
            continue
        paper, src, tgt = ex
        s = _claim(root, paper, src)
        if tgt == "*":
            w(f"- `{name}`: `{src}` → `*` ({paper.split('-')[0].title()}). “{s['claim']}” — "
              f"bounds every empirical claim in the paper.")
        else:
            t = _claim(root, paper, tgt)
            w(f"- `{name}`: `{src}` → `{tgt}` ({paper.split('-')[0].title()}). "
              f"Source: “{s['claim']}” Target: “{t['claim']}”")
    w("")
    w("### Relations that are confused for each other")
    w("")
    for a, b, why in rel.CONFUSABLE:
        w(f"**`{a}` versus `{b}`.** {why}")
        w("")

    # Confidence
    w("## Confidence")
    w("")
    w("A reader marks its own claim:")
    w("")
    for name, meaning in vocabulary.READER_CONFIDENCE:
        w(f"- `{name}` — {meaning}")
    w("")
    w("After reconciliation a claim's confidence is a fact about agreement between readers, "
      "not about the world:")
    w("")
    for name, meaning in vocabulary.CONFIDENCE:
        w(f"- `{name}` — {meaning}")
    w("")
    return "\n".join(out)


# ── schema-*.md ──────────────────────────────────────────────────────────


def _fields(model) -> list[tuple[str, str, str, bool]]:
    """(name, type, description, required) per field, from the pydantic JSON schema."""
    js = model.model_json_schema()
    defs = js.get("$defs", {})
    req = set(js.get("required", []))

    def typ(prop: dict) -> str:
        if "$ref" in prop:
            d = defs[prop["$ref"].split("/")[-1]]
            # " / " rather than " | ": these land in a markdown table cell.
            return " / ".join(f"`{v}`" for v in d["enum"]) if "enum" in d else d.get("title", "")
        if "enum" in prop:
            return " / ".join(f"`{v}`" for v in prop["enum"])
        if "anyOf" in prop:
            parts = [typ(p) for p in prop["anyOf"] if p.get("type") != "null"]
            return " or ".join(parts) + " or `null`"
        t = prop.get("type", "")
        if t == "array":
            return f"list of {typ(prop.get('items', {}))}"
        if t == "object":
            return "object"
        return f"`{t}`" if t else ""

    return [(name, typ(p), p.get("description", ""), name in req)
            for name, p in js["properties"].items()]


def _table(model) -> list[str]:
    rows = ["| Field | Value | Meaning |", "|:--|:--|:--|"]
    for name, t, desc, required in _fields(model):
        rows.append(f"| `{name}`{'' if required else ' (optional)'} | {t} | {desc} |")
    return rows


def render_schema_candidate() -> str:
    out = ["# What a reader returns", "",
           "Generated from `extract/elife_extract/schema.py` by `elife-extract contract --write`. "
           "Do not edit.", "",
           "A JSON array of candidate claims and nothing else — no prose before or after, no "
           "code fence. Each element:", ""]
    out += _table(schema.CandidateClaim)
    out += ["", "```json", json.dumps([{
        "claim": "Doubling distal dendritic inhibition reduces somatic firing from approximately "
                 "5.5 Hz to approximately 0.2 Hz.",
        "panel": "fig4a",
        "claim_type": "empirical",
        "role": "empirical",
        "evidence": "Doubling the strength of distal inhibition reduced the firing rate from "
                    "5.5 ± 0.9 Hz to 0.2 ± 0.2 Hz.",
        "confidence": "high",
        "notes": None,
    }], indent=2), "```", ""]
    return "\n".join(out)


def render_schema_draft() -> str:
    out = ["# What the reconciler and the reviewer return", "",
           "Generated from `extract/elife_extract/schema.py` by `elife-extract contract --write`. "
           "Do not edit.", "",
           "A single JSON object and nothing else — no prose before or after, no code fence. "
           "Top level:", ""]
    out += _table(schema.DraftClaimTable)
    out += ["", "Each element of `claims`:", ""]
    out += _table(schema.ReconciledClaim)
    out += ["", "```json", json.dumps({
        "paper_slug": "headley-2026-inhibitory-rhythms",
        "paper_doi": "10.7554/eLife.95562",
        "paper_title": "Spatially targeted inhibitory rhythms differentially affect neuronal integration",
        "per_agent_counts": {"results": 18, "caption": 22, "structure": 7},
        "claims": [{
            "claim": "Doubling distal dendritic inhibition reduces somatic firing from approximately "
                     "5.5 Hz to approximately 0.2 Hz.",
            "panel": "fig4a",
            "claim_type": "empirical",
            "role": "empirical",
            "confidence": "high",
            "sources": ["results", "caption"],
            "evidence_by_agent": {
                "results": "distal inhibition nearly silenced the cell (0.2 Hz)",
                "caption": "Doubling the strength of distal inhibition reduced the firing rate "
                           "from 5.5 ± 0.9 Hz to 0.2 ± 0.2 Hz.",
            },
            "notes": None,
        }],
    }, indent=2), "```", ""]
    return "\n".join(out)


RENDER = {
    "vocabulary.md": render_vocabulary,
    "schema-candidate.md": lambda root=None: render_schema_candidate(),
    "schema-draft.md": lambda root=None: render_schema_draft(),
}


# ── write and check ──────────────────────────────────────────────────────


def generated(root: Path | None = None) -> dict[str, str]:
    root = root or _repo_root()
    return {name: RENDER[name](root) for name in FILES}


def write(prompts_dir: Path, root: Path | None = None) -> list[Path]:
    d = prompts_dir / CONTRACT_DIR
    d.mkdir(parents=True, exist_ok=True)
    out = []
    for name, text in generated(root).items():
        p = d / name
        p.write_text(text, encoding="utf-8")
        out.append(p)
    return out


def check(prompts_dir: Path, root: Path | None = None) -> list[str]:
    """Names of committed contract files that differ from what the sources generate."""
    d = prompts_dir / CONTRACT_DIR
    stale = []
    for name, text in generated(root).items():
        p = d / name
        if not p.is_file() or p.read_text(encoding="utf-8") != text:
            stale.append(name)
    return stale
