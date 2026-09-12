"""The prompt contract: one vocabulary, rendered, declared, and sent.

What these pin is that the four places a definition could live agree. `vocabulary.py` and
`scripts/relations.py` define the words; `schema.py` accepts them; `contract.py` renders them
into the files under `extract/prompts/contract/`; `prompts.py` composes those files into what a
role is sent; and `pipeline/layers.yaml` declares that same list as the layer's inputs so the
run ledger hashes it. Any two of those drifting apart is the failure these exist to catch, and
it is the failure the repository has already had twice — four relation lists, twelve claim
types.

No LLM and no network. Runs under pytest or standalone.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path
from typing import get_args

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import yaml

from elife_extract import cli, contract, prompts, schema, vocabulary
from elife_extract.config import Config
from elife_extract.reconcile import _normalise_confidence

REPO = Path(__file__).resolve().parents[2]
PROMPTS = REPO / "extract" / "prompts"

# prompt role → the layer that sends it
LAYER_OF = {
    "results-reader": "results-reader",
    "caption-reader": "caption-reader",
    "structure-reader": "structure-reader",
    "reconciler": "reconcile",
    "external-reviewer": "external-review",
    "edge-inference": "edge-inference",
    "coverage-adjudicator": "adjudication",
    "questions": "questions",
    "parts": "parts",
    "stance": "stance",
    "summaries": "summaries",
    "synthesis": "synthesis",
    "abstract-map": "abstract-map",
}


def _declaration() -> dict:
    return {l["id"]: l for l in yaml.safe_load((REPO / "pipeline" / "layers.yaml").read_text())["layers"]}


def _cfg(prompts_dir: Path = PROMPTS, variant: str = "default") -> Config:
    return Config.from_args(cli.build_parser().parse_args(
        ["reconcile", "--paper", "x", "--prompts-dir", str(prompts_dir),
         "--prompt-variant", variant]))


# ── the committed contract is the generated one ──────────────────────────


def test_committed_contract_matches_its_sources():
    """Edit vocabulary.py or relations.py and forget to regenerate, and the prompt says one
    thing while the checker enforces another. `make check` runs the same comparison."""
    stale = contract.check(PROMPTS, REPO)
    assert not stale, f"regenerate with `elife-extract contract --write`: {', '.join(stale)}"


def test_every_contract_example_is_a_claim_in_the_corpus():
    rel = contract._relations(REPO)
    for name, (paper, src, tgt) in rel.EXAMPLE.items():
        contract._claim(REPO, paper, src)
        if tgt != "*":
            contract._claim(REPO, paper, tgt)
    for r in vocabulary.ROLES:
        c = contract._claim(REPO, *r["example"])
        assert c["role"] == r["role"], f"{r['example']} is a {c['role']}, shown as {r['role']}"
    for a, b, _why, ex_a, ex_b in vocabulary.ROLE_CONFUSABLE:
        assert contract._claim(REPO, *ex_a)["role"] == a
        assert contract._claim(REPO, *ex_b)["role"] == b


# ── the code's vocabulary is the rendered vocabulary ─────────────────────


def test_schema_literals_are_the_vocabulary():
    assert set(get_args(schema.ClaimType)) == {n for n, _ in vocabulary.CLAIM_TYPES}
    assert set(get_args(schema.Role)) == {r["role"] for r in vocabulary.ROLES}
    assert set(get_args(schema.ReconciledConfidence)) == {n for n, _ in vocabulary.CONFIDENCE}
    assert set(get_args(schema.AgentConfidence)) == {n for n, _ in vocabulary.READER_CONFIDENCE}


def test_every_relation_has_a_direction():
    rel = contract._relations(REPO)
    assert set(rel.DIRECTION) == set(rel.EDGE_KEYS)
    assert set(rel.EXAMPLE) <= set(rel.EDGE_KEYS)
    for a, b, _ in rel.CONFUSABLE:
        assert a in rel.EDGE_KEYS and b in rel.EDGE_KEYS


def test_part_of_has_a_direction_and_an_example():
    """Composition is a first-class relation, so it points a direction, shows a corpus edge,
    and is set against `supports` — the pair the note exists to separate."""
    rel = contract._relations(REPO)
    assert "part-of" in rel.EDGE_KEYS and "part-of" not in rel.OPPOSES
    assert rel.DIRECTION.get("part-of")
    assert "part-of" in rel.EXAMPLE                     # a real edge, quoted by the contract
    assert any({a, b} == {"part-of", "supports"} for a, b, _ in rel.CONFUSABLE)


def test_edge_inference_reads_the_vocabulary_that_defines_the_relations():
    """Edge inference is rebuilt on the contract (#83): its prompt is the task plus the
    vocabulary — where the relations, their binding directions and the confusable pairs are
    defined — and the declaration lists exactly that, so the run hashes what the edges are
    inferred from and the checker cannot drift from the prompt."""
    reads = prompts.declared_reads("edge-inference")
    assert reads == ["extract/prompts/edge-inference.md",
                     f"extract/prompts/{contract.CONTRACT_DIR}/vocabulary.md"]
    decl = _declaration()
    assert [r for r in decl["edge-inference"]["reads"] if r.startswith("extract/prompts/")] == reads


def test_same_part_or_different_is_rendered():
    """The reconciler's three-way test is only as good as its examples; the section, and one
    real pair for each verdict, has to reach the prompt."""
    md = contract.render_vocabulary(REPO)
    assert "## Same, part, or different" in md
    for verdict, _a, _b, _why in vocabulary.SAME_CLAIM:
        assert f"**{verdict}." in md
    assert {v for v, *_ in vocabulary.SAME_CLAIM} == {"same", "part", "different"}


def test_what_is_not_a_claim_is_rendered_with_methodological_warrants():
    """The `methodological`-versus-procedure line needs both sides on the page, and every
    warrant — the positive side — has to resolve to a claim the corpus files as
    `methodological`."""
    md = contract.render_vocabulary(REPO)
    assert "What is not a claim" in md
    assert vocabulary.WARRANTS and vocabulary.NOT_CLAIMS
    for paper, slug in vocabulary.WARRANTS:
        c = contract._claim(REPO, paper, slug)
        assert c["role"] == "methodological", f"{paper}/{slug} is {c['role']}, shown as a warrant"


def test_parts_layer_reads_the_vocabulary_that_defines_composition():
    """The parts layer is sent its task and the vocabulary — where `part-of` is defined — and
    the declaration lists exactly that, so the run hashes what the layer composes its edges
    from."""
    reads = prompts.declared_reads("parts")
    assert reads == ["extract/prompts/parts.md",
                     f"extract/prompts/{contract.CONTRACT_DIR}/vocabulary.md"]
    decl = _declaration()
    assert [r for r in decl["parts"]["reads"] if r.startswith("extract/prompts/")] == reads


# ── what is sent is what is declared ─────────────────────────────────────


def test_declaration_reads_what_the_prompt_composes():
    """A prompt file sent but not declared is an input the ledger never hashes.

    A layer may also read scripts (`adjudication` reads `scripts/adjudicate.py`), so the
    comparison is over the prompt files only — the entries under `extract/prompts/` — kept
    exact and in order against what the runner composes.
    """
    decl = _declaration()
    for role, layer in LAYER_OF.items():
        prompt_reads = [r for r in (decl[layer].get("reads") or [])
                        if r.startswith("extract/prompts/")]
        assert prompt_reads == prompts.declared_reads(role), \
            f"{layer}: prompt reads {prompt_reads} but the runner sends {prompts.declared_reads(role)}"


def test_prompt_is_task_then_contract():
    text = prompts.prompt("results-reader", _cfg())
    task = (PROMPTS / "results-reader.md").read_text().strip()
    assert text.startswith(task)
    assert "# The claim vocabulary" in text
    assert "# What a reader returns" in text
    assert "# What the reconciler and the reviewer return" not in text

    draft = prompts.prompt("reconciler", _cfg())
    assert "# What the reconciler and the reviewer return" in draft
    assert "# What a reader returns" not in draft


def test_variant_overrides_the_task_and_inherits_the_contract():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp) / "prompts"
        shutil.copytree(PROMPTS, d)
        (d / "lean").mkdir()
        (d / "lean" / "results-reader.md").write_text("LEAN TASK\n")
        text = prompts.prompt("results-reader", _cfg(d, "lean"))
        assert text.startswith("LEAN TASK")
        assert "# The claim vocabulary" in text


def test_committed_variants_compose_task_then_shared_contract():
    """The `frontier` and `open` variant dirs override task files only (#85): each composes
    the variant's task, then the same contract the default variant inherits, and a role the
    variant does not override falls back to the default task."""
    fr = prompts.prompt("results-reader", _cfg(variant="frontier"))
    assert fr.startswith((PROMPTS / "frontier" / "results-reader.md").read_text().strip())
    assert "# The claim vocabulary" in fr                       # contract inherited
    # A quantity-guidance sentence the default task carries is gone from the lean task.
    assert "typically yields" not in (PROMPTS / "frontier" / "results-reader.md").read_text()

    op = prompts.prompt("caption-reader", _cfg(variant="open"))
    assert op.startswith((PROMPTS / "open" / "caption-reader.md").read_text().strip())
    assert "# The claim vocabulary" in op

    # open overrides only the caption task, so its results reader is the default one.
    op_results = prompts.prompt("results-reader", _cfg(variant="open"))
    assert op_results.startswith((PROMPTS / "results-reader.md").read_text().strip())


# ── confidence follows the source count ──────────────────────────────────


def test_writer_numbers_a_shared_question_once():
    """Two claims that answer the same question — modulo case and whitespace — collapse to one
    `q1` on the paper, and both claims carry `addresses: q1`. A question is not a claim."""
    from elife_extract import write
    from elife_extract.schema import DraftClaimTable

    with tempfile.TemporaryDirectory() as tmp:
        cfg = Config.from_args(cli.build_parser().parse_args(
            ["write", "--paper", "p", "--root", tmp]))
        draft = DraftClaimTable(
            paper_slug="p", paper_doi="10.0/x", paper_title="P",
            claims=[
                {"claim": "The insula encodes interpersonal guilt.", "panel": None,
                 "claim_type": "hypothesis", "role": "hypothesis",
                 "addresses": "Does the insula encode interpersonal guilt?",
                 "confidence": "high", "sources": ["results"]},
                {"claim": "Agency aversion explains the effect instead.", "panel": None,
                 "claim_type": "interpretive", "role": "hypothesis",
                 "addresses": "does the  INSULA encode   interpersonal guilt?",
                 "confidence": "high", "sources": ["results"]},
            ],
        )
        write.write_claim_files(draft, cfg, edges=[])

        d = cfg.corpus_dir / "p"
        idx = yaml.safe_load((d / "index.md").read_text().split("---", 2)[1])
        assert idx["questions"] == [
            {"id": "q1", "text": "Does the insula encode interpersonal guilt?"}], \
            "the two claims' shared question should be one q1, first spelling kept"
        for slug in write._unique_slugs(draft.claims):
            fm = yaml.safe_load((d / f"{slug}.md").read_text().split("---", 2)[1])
            assert fm["addresses"] == "q1", f"{slug} should address q1"


def test_confidence_is_a_fact_about_agreement():
    """DeepSeek called every two-source claim `high` and one-source claims `high` too; the
    count of sources is the fact, and the label has to follow it."""
    claims = [
        {"sources": ["results"], "confidence": "high"},
        {"sources": ["results", "caption"], "confidence": "single-source"},
        {"sources": ["results", "caption"], "confidence": "contested"},
        {"sources": ["caption"], "confidence": "single-source"},
    ]
    assert _normalise_confidence(claims) == 2
    assert [c["confidence"] for c in claims] == ["single-source", "high", "contested", "single-source"]


if __name__ == "__main__":
    import traceback
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
            passed += 1
        except Exception:
            print(f"FAIL  {t.__name__}")
            traceback.print_exc()
    print(f"\n{passed}/{len(tests)} passed")
    raise SystemExit(0 if passed == len(tests) else 1)
