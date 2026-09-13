"""The verification check — does a re-run stand behind each claim, read beside its warrant.

The first checking layer. `warrant` reads what the tree's argument gives a reader grounds to
believe; a check reads what happened when someone tried to reproduce the result, and writes a
verdict *beside* the warrant rather than into it (docs/design/2026-09-13-verification-check.md).
Warrant and each check are separate fields, and only an adjudication verdict overwrites one.

For each claim there are two sources, and the layer reads both: the `reproductions:` records the
claim file carries (status `verified` / `partial` / `mismatch` / `blocked` / `unattempted`), and
the verification provenance the audited run wrote (`verification/<paper>/provenance.json`, a
per-claim `results` entry with a PASS/WARN/FAIL `status` and whether the value was `measured`).

`verdict(records, prov)` returns one of six words and the evidence it read. The rule is
precedence over that evidence — the most adverse informative verdict a claim's evidence supports
wins — so a claim carrying both a `blocked` record and a `mismatch` record reads `mismatch`:

  reproduced   a record marked `verified` whose provenance shows the script ran and measured
               the value (`measured: true`), or a provenance run that did on its own
  partial      recorded verified but not observed running, a `partial` record, or a run that
               executed without measuring the value (a PASS/WARN the auditor recalled)
  mismatch     a re-run that disagreed with the paper — a `mismatch` record or a FAIL run; the
               site shows it as contested-by-verification
  blocked      a record that could not be run (no data, no code, specialist compute)
  unattempted  a record that has not been tried, or a recorded status this rule does not name
  unrecorded   nothing — no reproduction record and no provenance for this claim

It never touches `warrant:`; MIRA/OXA export mapping for the check follows in a later change.
"""

from __future__ import annotations

VERDICTS = ("reproduced", "partial", "mismatch", "blocked", "unattempted", "unrecorded")

# Most adverse and informative first: a mismatch a reader must see outranks a clean re-run, and a
# re-run that stands outranks a blocked or untried attempt on the same claim.
_PRECEDENCE = ("mismatch", "reproduced", "partial", "blocked", "unattempted", "unrecorded")

_RAN_STATUSES = ("PASS", "WARN", "FAIL")


def _ran(prov: dict | None) -> bool:
    """The audited run executed this claim and measured its value — not a recalled deposit."""
    return bool(prov) and prov.get("measured") is True and prov.get("status") in _RAN_STATUSES


def verdict(records: list[dict] | None, prov: dict | None) -> tuple[str, list[str]]:
    """One claim's check verdict and the record statuses and provenance it was read from."""
    cand: set[str] = set()
    fired: list[str] = []
    for r in records or []:
        if not isinstance(r, dict):
            continue
        s = (r.get("status") or "").strip()
        fired.append(f"record:{s or '—'}")
        if s == "mismatch":
            cand.add("mismatch")
        elif s == "verified":
            cand.add("reproduced" if _ran(prov) else "partial")
        elif s in ("partial", "unverified"):
            cand.add("partial")
        elif s == "blocked":
            cand.add("blocked")
        else:                                   # unattempted, or any status this rule leaves unnamed
            cand.add("unattempted")
    if prov is not None:
        st = prov.get("status")
        fired.append(f"provenance:{st}" + (" measured" if prov.get("measured") else ""))
        if st == "FAIL":
            cand.add("mismatch")
        elif _ran(prov):
            cand.add("reproduced")
        elif st in ("PASS", "WARN"):            # ran, but the value was recalled rather than measured
            cand.add("partial")
    for v in _PRECEDENCE:
        if v in cand:
            return v, fired
    return "unrecorded", fired
