"""The source seam: prepare() resolves a reference, and only a source knows a publisher (#130).

These exist because the refactor that moved the eLife CDN out of prepare.py passed the whole
suite unchanged — prepare() and parse_jats were at 0% coverage, so 97 green tests proved only
that the package still imported. What is pinned here is the seam itself: that a reference is
resolved by whichever source claims it, that eLife knowledge lives in ElifeSource and nowhere
else, that provenance reaches PreparedPaper instead of being reconstructed from a hardcoded
URL, and that a reference no source handles fails with a message naming what to do.

No LLM and no network — ElifeSource is exercised against a pre-seeded cache, which also pins
that a cache hit does not reach out. Runs under pytest or standalone.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from elife_extract import prepare as prepare_mod
from elife_extract import segment as segment_mod
from elife_extract import sources
from elife_extract.prepare import PreparedPaper, parse_jats, prepare
from elife_extract.segment import segment
from elife_extract.sources import ElifeSource, FileSource, Resolved

DOI = "10.7554/eLife.95562"

MINIMAL_JATS = """<?xml version="1.0"?>
<article xmlns:xlink="http://www.w3.org/1999/xlink">
  <front><article-meta>
    <title-group><article-title>Spatially targeted inhibitory rhythms</article-title></title-group>
    <contrib-group>
      <contrib contrib-type="author"><name><surname>Headley</surname><given-names>D</given-names></name></contrib>
    </contrib-group>
    <pub-date date-type="pub"><year>2026</year></pub-date>
    <abstract><p>An abstract.</p></abstract>
  </article-meta></front>
  <body>
    <sec sec-type="results"><title>Results</title><p>Beta entrains distal dendrites.</p></sec>
    <sec sec-type="methods"><title>Methods</title><p>A compartmental model.</p></sec>
  </body>
</article>
"""


def _jats(tmp: Path) -> Path:
    p = tmp / "article.xml"
    p.write_text(MINIMAL_JATS, encoding="utf-8")
    return p


# ── ElifeSource owns the eLife knowledge ──────────────────────────────────


def test_elife_source_claims_only_elife_dois():
    e = ElifeSource()
    assert e.handles(DOI)
    assert e.handles("10.7554/ELIFE.105391")            # the regex is case-insensitive
    assert not e.handles("10.1101/2025.08.01.668048")   # the bioRxiv preprint in the corpus
    assert not e.handles("10.1038/nature12373")
    assert e.doc_id(DOI) == "95562"


def test_elife_source_rejects_a_non_elife_doi_with_the_expected_form():
    try:
        ElifeSource().doc_id("10.1038/nature12373")
    except ValueError as exc:
        assert "10.7554/eLife.<article-id>" in str(exc)
    else:
        raise AssertionError("a non-eLife DOI should not yield an article id")


def test_a_cache_hit_does_not_reach_the_network():
    """Seed the cache, then resolve. Any HTTP call here would fail the test by raising."""
    with tempfile.TemporaryDirectory() as td:
        cache = Path(td)
        (cache / "elife-95562-v1.xml").write_text(MINIMAL_JATS, encoding="utf-8")

        def _no_network(*a, **k):
            raise AssertionError("resolve() fetched despite a warm cache")

        import httpx
        real_client, httpx.Client = httpx.Client, _no_network
        try:
            r = ElifeSource().resolve(DOI, cache_dir=cache)
        finally:
            httpx.Client = real_client
        assert r.format == "jats" and r.doc_id == "95562" and r.source == "elife"
        assert r.url.endswith("elife-95562-v1.xml")
        assert len(r.sha256) == 64


def test_elife_source_serves_pdf_when_asked_and_refuses_what_it_has_not_got():
    with tempfile.TemporaryDirectory() as td:
        cache = Path(td)
        (cache / "elife-95562-v1.pdf").write_bytes(b"%PDF-1.4 stub")
        r = ElifeSource().resolve(DOI, cache_dir=cache, prefer="pdf")
        assert r.format == "pdf" and r.path.suffix == ".pdf"
    try:
        ElifeSource().resolve(DOI, prefer="epub")              # type: ignore[arg-type]
    except ValueError as exc:
        assert "does not serve" in str(exc)
    else:
        raise AssertionError("an unsupported format should be refused, not guessed")


# ── FileSource is the no-network fallback ─────────────────────────────────


def test_file_source_reads_the_format_off_the_suffix():
    f = FileSource()
    with tempfile.TemporaryDirectory() as td:
        xml, pdf = _jats(Path(td)), Path(td) / "p.pdf"
        pdf.write_bytes(b"%PDF-1.4 stub")
        assert f.handles(str(xml)) and f.handles(str(pdf))
        assert not f.handles(str(Path(td) / "missing.pdf"))    # a path that does not exist
        assert not f.handles(DOI)
        assert f.resolve(str(xml)).format == "jats"
        assert f.resolve(str(pdf)).format == "pdf"
        assert f.resolve(str(xml)).sha256 == sources.sha256_of(xml)


# ── the registry ──────────────────────────────────────────────────────────


def test_built_ins_come_first_so_a_plugin_cannot_shadow_elife():
    class Greedy:
        name = "greedy"
        def handles(self, ref): return True
        def resolve(self, ref, cache_dir=None, prefer=None): raise AssertionError("shadowed eLife")

    original = sources.registry
    sources.registry = lambda: [ElifeSource(), FileSource(), Greedy()]
    try:
        assert sources.for_ref(DOI).name == "elife"
        assert sources.for_ref("10.1038/nature12373").name == "greedy"
    finally:
        sources.registry = original


def test_an_unhandled_reference_says_what_to_do():
    try:
        sources.for_ref("10.1101/2025.08.01.668048")
    except ValueError as exc:
        msg = str(exc)
        assert "no source handles" in msg
        assert "elife" in msg and "file" in msg            # what is built in
        assert sources.SOURCE_ENTRY_POINT_GROUP in msg     # how to add one
    else:
        raise AssertionError("an unhandled reference should raise, not fall back")


# ── provenance reaches PreparedPaper ──────────────────────────────────────


def test_parse_jats_takes_its_document_id_and_note_from_the_source():
    with tempfile.TemporaryDirectory() as td:
        xml = _jats(Path(td))
        prov = Resolved(path=xml, format="jats", ref=DOI, source="elife",
                        url="https://cdn.elifesciences.org/articles/95562/elife-95562-v1.xml",
                        doc_id="95562", sha256="0" * 64)
        paper = parse_jats(xml, DOI, "headley-2026-inhibitory-rhythms", provenance=prov)
        assert paper.article_id == "95562"
        assert paper.extraction_path == "jats"
        assert paper.extraction_path_note == (
            "JATS-XML from https://cdn.elifesciences.org/articles/95562/elife-95562-v1.xml")
        assert paper.title == "Spatially targeted inhibitory rhythms"
        assert "Beta entrains" in paper.results_text
        assert "compartmental model" in paper.methods_text


def test_parse_jats_without_provenance_leaves_the_id_empty_rather_than_guessing():
    """Only a source can read an id out of a DOI. Absent one, the field is blank, not wrong."""
    with tempfile.TemporaryDirectory() as td:
        xml = _jats(Path(td))
        paper = parse_jats(xml, DOI)
        assert paper.article_id == ""
        assert str(xml) in paper.extraction_path_note


# ── prepare() routes through the registry ─────────────────────────────────


def test_prepare_routes_a_doi_to_the_source_that_claims_it():
    seen = {}

    class Recording:
        name = "recording"
        def handles(self, ref): return ref == DOI
        def resolve(self, ref, cache_dir=None, prefer=None):
            seen["ref"], seen["prefer"] = ref, prefer
            return Resolved(path=self.xml, format="jats", ref=ref, source=self.name,
                            url="https://example.test/a.xml", doc_id="95562", sha256="1" * 64)

    with tempfile.TemporaryDirectory() as td:
        rec = Recording()
        rec.xml = _jats(Path(td))
        original = sources.registry
        sources.registry = lambda: [rec]
        try:
            paper = prepare(doi=DOI, paper_slug_override="a-slug")
        finally:
            sources.registry = original

    assert seen == {"ref": DOI, "prefer": None}            # "auto" asks for no format
    assert isinstance(paper, PreparedPaper)
    assert paper.article_id == "95562" and paper.paper_slug == "a-slug"
    assert paper.extraction_path_note == "JATS-XML from https://example.test/a.xml"


def test_prepare_forwards_an_explicit_format_as_a_requirement():
    asked = {}

    class Recording:
        name = "recording"
        def handles(self, ref): return True
        def resolve(self, ref, cache_dir=None, prefer=None):
            asked["prefer"] = prefer
            return Resolved(path=self.xml, format="jats", ref=ref, source=self.name,
                            doc_id="95562", sha256="2" * 64)

    with tempfile.TemporaryDirectory() as td:
        rec = Recording()
        rec.xml = _jats(Path(td))
        original = sources.registry
        sources.registry = lambda: [rec]
        try:
            prepare(doi=DOI, input_format="jats")
        finally:
            sources.registry = original
    assert asked["prefer"] == "jats"


def test_prepare_needs_a_doi_or_a_path():
    try:
        prepare()
    except ValueError as exc:
        assert "DOI or a local pdf_path" in str(exc)
    else:
        raise AssertionError("prepare() with neither argument should raise")


# ── the seam holds ────────────────────────────────────────────────────────


def test_prepare_module_names_no_publisher_in_its_logic():
    """The point of the refactor, and the thing no other test would notice regressing.

    Prose may cite where a heuristic came from — several docstrings legitimately explain that a
    caption regex was written against eLife's layout. Code may not branch on a publisher. The
    only exception is the PDF-furniture skip lists, whose whole job is to hold such strings.
    """
    import ast
    import io
    import token as toktypes
    import tokenize

    path = Path(prepare_mod.__file__)
    src = path.read_text(encoding="utf-8")
    allowed = {a for a in set(prepare_mod.TITLE_SKIP) | set(prepare_mod.AUTHOR_SKIP)
               if "elife" in a}

    # Docstrings are prose about the code, not code. Collect their line spans from the AST
    # rather than guessing at quote characters.
    prose: set[int] = set()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        body = getattr(node, "body", None)
        if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                and isinstance(body[0].value.value, str):
            doc = body[0]
            prose.update(range(doc.lineno, (doc.end_lineno or doc.lineno) + 1))

    offenders = []
    for tok in tokenize.tokenize(io.BytesIO(src.encode()).readline):
        if tok.type == toktypes.COMMENT or tok.start[0] in prose:
            continue
        if tok.type == toktypes.STRING and tok.string.strip("\"'") in allowed:
            continue
        if "elife" in tok.string.lower():
            offenders.append(f"{tok.start[0]}: {tok.line.strip()}")

    assert not offenders, "eLife in prepare.py's logic:\n" + "\n".join(offenders)
    assert "cdn.elifesciences.org" not in src, "the CDN belongs in sources.py"


# ── the section vocabulary is declared once ───────────────────────────────


def _paper(**over) -> PreparedPaper:
    base = dict(doi=DOI, article_id="95562", paper_slug="p", title="T", authors=["A"],
                abstract="An abstract.", results_text="A result.", captions_text="A caption.",
                methods_text="A method.", extraction_path="jats",
                introduction_text="An intro.", discussion_text="A discussion.",
                appendix_text="An appendix.",
                supplementary_text="Figure 1—source code 1. Source code for A and F.")
    return PreparedPaper(**{**base, **over})


def test_every_text_field_on_the_type_is_in_the_section_vocabulary():
    """The bug this guards: supplementary_text existed on PreparedPaper and was missing from
    segment()'s list, so it was stored and never segmented. Any future text field added to the
    type without a SECTIONS entry fails here rather than going quietly unread (#137)."""
    from dataclasses import fields
    declared = {attr for _, attr, _ in prepare_mod.SECTIONS}
    text_fields = {f.name for f in fields(PreparedPaper)
                   if f.name.endswith("_text") or f.name == "abstract"}
    missing = text_fields - declared
    assert not missing, f"text fields on PreparedPaper with no SECTIONS entry: {sorted(missing)}"
    # And the reverse: a SECTIONS entry naming something the type cannot supply.
    paper = _paper()
    unreachable = [attr for _, attr, _ in prepare_mod.SECTIONS if not hasattr(paper, attr)]
    assert not unreachable, f"SECTIONS names attributes PreparedPaper has not got: {unreachable}"


def test_supplementary_is_segmented_and_kept_out_of_the_coverage_denominator():
    """Both halves matter. It must reach the readers, because its lines map source code to
    figure panels. It must not reach coverage, because a file manifest asserts nothing and
    would lower measured coverage with spans nothing should ever claim."""
    read_by_agents = {s.section for s in segment(_paper(), include_methods=True)}
    measured_by_coverage = {s.section for s in segment(_paper(), include_methods=False)}
    assert "supplementary" in read_by_agents
    assert "supplementary" not in measured_by_coverage
    assert {"methods", "appendix"} <= read_by_agents
    assert not {"methods", "appendix"} & measured_by_coverage
    assert {"abstract", "introduction", "results", "discussion"} <= measured_by_coverage


def test_sections_drops_empties_rather_than_emitting_blank_spans():
    paper = _paper(supplementary_text="", appendix_text="   ")
    names = [name for name, _ in paper.sections()]
    assert "supplementary" not in names and "appendix" not in names
    assert "results" in names


def test_segment_reads_the_vocabulary_rather_than_restating_it():
    """The duplication itself is what regressed. Pin that segment.py holds no section-name
    literals: it must go through PreparedPaper.sections()."""
    import re
    src = Path(segment_mod.__file__).read_text(encoding="utf-8")
    body = src[src.index("def segment("):]
    body = body[:body.index("\ndef ", 1)] if "\ndef " in body[1:] else body
    for name, _, _ in prepare_mod.SECTIONS:
        assert not re.search(rf'["\']{name}["\']', body), (
            f"segment() names the section {name!r} itself; it should read SECTIONS")


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
