"""Where a document comes from — resolving a reference to a local file.

`prepare.py` slices a document into the agent inputs and knows nothing about publishers. This
module is the seam: a Source turns a reference (a DOI, a URL, a path) into a cached local file
and says what format it is in. eLife lives here and nowhere else, which is what lets the
machinery be published without the corpus (docs/design/2026-09-13-the-split.md § 4).

A source is registered in `BUILT_IN` or discovered through the `claim_graphs.sources` entry
point group, so an adapter for another publisher ships in its own package:

    [project.entry-points."claim_graphs.sources"]
    elife-jats = "elife_claim_trees.sources:ElifeSource"

`Resolved.sha256` is not decoration. The pipeline decides staleness by hashing what a layer
read (`runs/<paper>/ledger.jsonl`), so a source that cached by URL alone — returning a stale
file under a live-looking name — would defeat it silently.
"""

from __future__ import annotations

import hashlib
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Protocol, runtime_checkable

import httpx

logger = logging.getLogger(__name__)

Format = Literal["jats", "pdf"]

SOURCE_ENTRY_POINT_GROUP = "claim_graphs.sources"

# Kept at the historical path: moving it would silently re-download every cached paper. The
# rename belongs with the package rename (§ 7 step 4), not here.
DEFAULT_CACHE_DIR = Path.home() / ".cache" / "elife-extract"


@dataclass(frozen=True)
class Resolved:
    """A document located on disk, with enough provenance to reproduce the fetch."""

    path: Path
    format: Format
    ref: str
    source: str
    url: str | None = None
    doc_id: str | None = None          # the publisher's own id, where it has one
    sha256: str = ""

    # The exact wording matters: it is written into runs/<paper>/prepared.json, the ledger
    # hashes that file, and a cosmetic change would mark every paper stale.
    FORMAT_LABEL = {"jats": "JATS-XML", "pdf": "PDF"}

    @property
    def note(self) -> str:
        """One line for `PreparedPaper.extraction_path_note`."""
        where = self.url or f"local file at {self.path}"
        return f"{self.FORMAT_LABEL.get(self.format, self.format.upper())} from {where}"


@runtime_checkable
class Source(Protocol):
    """Resolves a document reference to a local file a reader layer can parse."""

    name: str

    def handles(self, ref: str) -> bool:
        """True if this source can resolve `ref`."""

    def resolve(self, ref: str, cache_dir: Path | None = None,
                prefer: Format | None = None) -> Resolved:
        """Retrieve `ref`, caching under `cache_dir`. `prefer` picks among formats it offers."""


def _cached_fetch(url: str, cached: Path, cache_dir: Path) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    if cached.is_file() and cached.stat().st_size > 0:
        logger.info("using cached %s", cached)
        return cached
    logger.info("fetching %s", url)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        resp = client.get(url)
        resp.raise_for_status()
        cached.write_bytes(resp.content)
    return cached


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class ElifeSource:
    """eLife: a DOI of the form 10.7554/eLife.<id>, served from the eLife CDN.

    JATS is preferred because every eLife article has it, and it carries labelled sections,
    typed figures and structured references that the PDF heuristics can only guess at.
    """

    name = "elife"
    formats: tuple[Format, ...] = ("jats", "pdf")

    PDF_URL = "https://cdn.elifesciences.org/articles/{doc_id}/elife-{doc_id}-v1.pdf"
    XML_URL = "https://cdn.elifesciences.org/articles/{doc_id}/elife-{doc_id}-v1.xml"
    DOI_RE = re.compile(r"10\.7554/eLife\.(\d+)", re.IGNORECASE)

    def handles(self, ref: str) -> bool:
        return bool(self.DOI_RE.match(str(ref).strip()))

    def doc_id(self, ref: str) -> str:
        m = self.DOI_RE.match(str(ref).strip())
        if not m:
            raise ValueError(
                f"Not a recognized eLife DOI: {ref!r}. Expected 10.7554/eLife.<article-id>"
            )
        return m.group(1)

    def resolve(self, ref: str, cache_dir: Path | None = None,
                prefer: Format | None = None) -> Resolved:
        fmt: Format = prefer or "jats"
        if fmt not in self.formats:
            raise ValueError(f"{self.name} does not serve {fmt!r}")
        doc_id = self.doc_id(ref)
        cache_dir = cache_dir or DEFAULT_CACHE_DIR
        url = (self.XML_URL if fmt == "jats" else self.PDF_URL).format(doc_id=doc_id)
        suffix = "xml" if fmt == "jats" else "pdf"
        path = _cached_fetch(url, cache_dir / f"elife-{doc_id}-v1.{suffix}", cache_dir)
        return Resolved(path=path, format=fmt, ref=ref, source=self.name, url=url,
                        doc_id=doc_id, sha256=sha256_of(path))


class FileSource:
    """A document already on disk. The fallback that makes the package usable with no network."""

    name = "file"
    SUFFIX_FORMAT: dict[str, Format] = {".pdf": "pdf", ".xml": "jats", ".nxml": "jats"}

    def handles(self, ref: str) -> bool:
        p = Path(str(ref)).expanduser()
        return p.suffix.lower() in self.SUFFIX_FORMAT and p.is_file()

    def resolve(self, ref: str, cache_dir: Path | None = None,
                prefer: Format | None = None) -> Resolved:
        path = Path(str(ref)).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(path)
        fmt = self.SUFFIX_FORMAT.get(path.suffix.lower())
        if fmt is None:
            raise ValueError(f"cannot tell the format of {path.name} from its suffix")
        if prefer and prefer != fmt:
            raise ValueError(f"{path.name} is {fmt}, not {prefer}")
        return Resolved(path=path, format=fmt, ref=str(ref), source=self.name,
                        doc_id=None, sha256=sha256_of(path))


BUILT_IN: tuple[type, ...] = (ElifeSource, FileSource)


def registry() -> list[Source]:
    """Built-in sources first, then any registered through the entry point group.

    Built-ins come first so a plugin cannot silently shadow eLife handling; a plugin claiming a
    reference no built-in handles is the supported case.
    """
    sources: list[Source] = [cls() for cls in BUILT_IN]
    try:
        from importlib.metadata import entry_points
        for ep in entry_points(group=SOURCE_ENTRY_POINT_GROUP):
            try:
                sources.append(ep.load()())
            except Exception:                                   # noqa: BLE001
                logger.warning("source plugin %r failed to load", ep.name, exc_info=True)
    except Exception:                                           # noqa: BLE001
        logger.debug("entry-point discovery unavailable", exc_info=True)
    return sources


def for_ref(ref: str) -> Source:
    """The first source that handles `ref`."""
    for source in registry():
        if source.handles(ref):
            return source
    raise ValueError(
        f"no source handles {ref!r}. Built-in sources: "
        f"{', '.join(cls.name for cls in BUILT_IN)}. "
        f"Pass a local PDF or XML path, or register a source in the "
        f"{SOURCE_ENTRY_POINT_GROUP!r} entry point group."
    )


def resolve(ref: str, cache_dir: Path | None = None, prefer: Format | None = None) -> Resolved:
    return for_ref(ref).resolve(ref, cache_dir=cache_dir, prefer=prefer)
