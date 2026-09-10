#!/usr/bin/env python3
"""Reconcile what the verification runs did against what the claims say they did.

A reproduction record in a claim file is a set of assertions about an event: this script ran,
it opened this data file, it computed this value, and the claim therefore has this status.
Until now nothing checked those assertions against the event. Two were already found false in
the one script that was audited -- a `verified` status on a claim whose function raised an
exception, and a `data_file` naming a file the code never opens.

`verification/audit_run.py` observes each run and writes `provenance.json`. This compares the
two and reports every disagreement:

  missing        the claim says verified/partial but the run produced no result for it
  status         the claim's status and the run's verdict disagree
  data_file      the record names a file the run never opened
  unrecorded     the run produced a verdict for a claim that has no reproduction record
  no_run         the paper has a verify.py but no provenance -- it has never been observed
  self_contradiction  the record says `verified` while its own notes say it was partial

Exit status is non-zero if any disagreement is found, so this can gate a release.

Usage:
  python3 scripts/audit_verifications.py
  python3 scripts/audit_verifications.py <paper-slug>
  python3 scripts/audit_verifications.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from export_mira import CLAIMS_DIR, load_paper  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERIF = os.path.join(ROOT, "verification")

# How a run's verdict maps onto a claim's reproduction status.
VERDICT = {"PASS": "verified", "FAIL": "mismatch", "WARN": "partial"}
# Statuses that assert a run happened and settled something.
SETTLED = {"verified", "mismatch", "partial"}

# Only these roles are settleable by re-running code (scripts/check_reproductions.py). A
# `scope` or `methodological` claim is verified by reading the paper's methods -- "Confirmed
# by methods text: …" -- and no script will ever produce a result for it. Reporting those as
# missing buries the real findings: the first version of this tool called nine such claims
# errors and the two genuine disagreements were lost among them.
ELIGIBLE = {"empirical", "control"}

# How much a status claims. A record that asserts MORE than the run found is the dangerous
# direction and is an error; one that asserts LESS is a conservative judgement and is only
# worth showing.
STRENGTH = {"verified": 3, "partial": 2, "mismatch": 1, "blocked": 0, "unattempted": 0}


def provenance(paper):
    p = os.path.join(VERIF, paper, "provenance.json")
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


# A record whose notes say the reproduction was partial while its status says `verified`
# contradicts itself, and needs no run to detect. Four did.
#
# The pattern is deliberately narrow. A first attempt matched `ns` and any p-value, and
# returned 26 hits -- `ns` inside "conditions", "means" and "constraint", and non-significant
# p-values on claims that assert a null result, where a high p is exactly what verifies them.
# A check that cries wolf gets ignored, so this matches only unambiguous self-hedging, and
# excludes the phrase "supersedes … partial status", which is a record correctly explaining
# its own promotion.
HEDGE = re.compile(r"\bpartial(?:ly)?\b|\bnot identical\b|\bclose but\b|"
                   r"\bdoes not match\b|\bcould not (?:be )?(?:verif|reproduc|confirm)|"
                   r"\bunable to\b|\bmismatch\b", re.I)
SUPERSEDE = re.compile(r"supersede\w*[^.]{0,60}partial", re.I)


def self_contradiction(rec):
    """The record's own notes disagreeing with its own status."""
    if rec.get("status") != "verified":
        return None
    notes = str(rec.get("notes") or "")
    if SUPERSEDE.search(notes):
        return None
    m = HEDGE.search(notes)
    return m.group(0) if m else None


def base_slug(claim_label):
    """Run labels carry a suffix -- `lottery-choice-increases-with-ev [fMRI]`."""
    return re.sub(r"\s*[\[(].*$", "", str(claim_label)).strip()


def current_record(claim):
    recs = [r for r in (claim.get("reproductions") or []) if isinstance(r, dict)]
    return max(recs, key=lambda r: str(r.get("date", "")), default=None)


def audit(paper):
    prov = provenance(paper)
    script = os.path.isfile(os.path.join(VERIF, paper, "verify.py"))
    findings = []

    if not script:
        return findings, None, None
    if prov is None:
        return [{"kind": "no_run", "level": "error", "claim": None,
                 "detail": "verify.py exists but has never been run under audit_run.py, so "
                           "nothing has observed what it does"}], None, None

    # A run that died tells you nothing about the records. Reporting every unsettled claim
    # as a separate error turns one fact -- the script timed out -- into nine, and buries the
    # findings that are about the corpus rather than about the run.
    run_died = bool(prov.get("exception"))
    if run_died:
        e = prov["exception"]
        findings.append({"kind": "run_failed", "level": "error", "claim": None,
                         "detail": f"the run raised {e['type']}: {e['message'][:160]} — no "
                                   f"claim in this paper could be checked against it"})

    by_run = {}
    for r in prov.get("results", []):
        by_run.setdefault(base_slug(r["claim"]), []).append(r)

    opened = {os.path.basename(o["path"]) for o in prov.get("opened", [])}
    opened |= {o["path"] for o in prov.get("opened", [])}

    claims = {c["slug"]: c for c in load_paper(paper)}

    for slug, c in claims.items():
        rec = current_record(c)
        if not rec:
            continue
        status = rec.get("status")
        runs = by_run.get(slug)

        hedge = self_contradiction(rec)
        if hedge:
            findings.append({"kind": "self_contradiction", "level": "error", "claim": slug,
                             "detail": f"status is `verified` but its own notes say "
                                       f"\u201c{hedge}\u201d"})

        role = c.get("role") or c.get("claim-type") or "empirical"

        if status in SETTLED and not runs:
            if run_died:
                pass                      # the run is why, not the record
            elif role in ELIGIBLE:
                findings.append({"kind": "missing", "level": "error", "claim": slug,
                                 "detail": f"recorded `{status}` but the run produced no "
                                           f"result for this claim, and a re-run is the only "
                                           f"thing that could settle a {role} claim"})
            else:
                findings.append({"kind": "by_inspection", "level": "info", "claim": slug,
                                 "detail": f"`{status}` by reading, not by running — a "
                                           f"{role} claim, which no script settles"})
        elif runs:
            verdicts = {VERDICT.get(r["status"], r["status"].lower()) for r in runs}
            if status not in verdicts:
                best = max((STRENGTH.get(v, 0) for v in verdicts), default=0)
                over = STRENGTH.get(status, 0) > best
                findings.append({
                    "kind": "status",
                    "level": "error" if over else "review",
                    "claim": slug,
                    "detail": (f"recorded `{status}`; the run reported "
                               f"{', '.join(sorted(verdicts))} "
                               f"({'; '.join(r['reproduced_value'][:70] for r in runs)})"
                               + ("" if over else
                                  " — the record is the more conservative of the two"))})

        # `data_file` is sometimes a list of paths, and stringifying the list instead of
        # walking it reported both of Gaedeke's files as never opened when the run had opened
        # each of them. An archive in the deposit also counts as opened when its extracted
        # member is: the record names `…nii.zip`, the code reads `…nii`.
        df = rec.get("data_file")
        for one in ([df] if isinstance(df, str) else list(df or [])):
            if not one or not opened:
                continue
            base = os.path.basename(str(one))
            stem = re.sub(r"\.(zip|gz|tar|tgz|bz2|xz)$", "", base)
            if any(base == os.path.basename(o) or stem == os.path.basename(o)
                   or stem in o or str(one) in o for o in opened):
                continue
            findings.append({"kind": "data_file", "level": "error", "claim": slug,
                             "detail": f"record names `{one}`, which the run never opened"})

    # How much of the paper the script actually covers. Most remaining "missing" findings are
    # claims verified by reading a deposit rather than by running verify.py -- legitimate, but
    # it means a paper can show a wall of `verified` while its script tests a third of them,
    # and nothing anywhere says so.
    settleable = [s for s, c in claims.items()
                  if (c.get("role") or c.get("claim-type") or "empirical") in ELIGIBLE
                  and current_record(c)]
    covered = [s for s in settleable if s in by_run]
    coverage = {"settleable": len(settleable), "covered": len(covered)}

    for slug in by_run:
        if slug not in claims:
            findings.append({"kind": "unrecorded", "level": "error", "claim": slug,
                             "detail": "the run reported on this claim, but no claim file of "
                                       "that slug exists in this paper"})
        elif not current_record(claims[slug]):
            findings.append({"kind": "unrecorded", "level": "review", "claim": slug,
                             "detail": "the run produced a verdict but the claim has no "
                                       "reproduction record"})

    return findings, prov, coverage


README = os.path.join(VERIF, "README.md")
MARK_A = "<!-- generated: papers-covered -->"
MARK_B = "<!-- /generated -->"


def papers_table():
    """The Papers Covered table, built from the directories and the audit records.

    It was hand-typed, and drifted: it listed seven papers when nine scripts existed, missing
    both Meijer method examples, and its "Claims Verified" column was a number somebody wrote
    down rather than one any run produced. Generating it is the same fix applied to the site's
    corpus counts -- not correcting the number, but ceasing to write it down.
    """
    # `public_papers()` is every public paper, which includes the two bioRxiv method
    # examples; labelling those "site corpus" would restate the error this table is being
    # generated to stop. corpus_facts.corpora() is the split the site itself uses.
    import corpus_facts as CF
    site_list, example_list = CF.corpora()
    site, examples = set(site_list), set(example_list)
    rows = []
    for d in sorted(os.listdir(VERIF)):
        if not os.path.isfile(os.path.join(VERIF, d, "verify.py")):
            continue
        prov = provenance(d)
        _, _, cov = audit(d)
        res = prov.get("results", []) if prov else []
        counts = {}
        for r in res:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        tally = " · ".join(f"{v} {k}" for k, v in sorted(counts.items())) or "not yet run"
        if prov and prov.get("missing_dependencies"):
            tally += " ⚠ degraded environment"
        elif prov and prov.get("exception"):
            tally += f" ⚠ {prov['exception']['type']}"
        corpus = ("site corpus" if d in site
                  else "method example" if d in examples else "not in a public corpus")
        covtxt = f"{cov['covered']}/{cov['settleable']}" if cov else "—"
        rows.append((d, corpus, covtxt, tally,
                     (prov or {}).get("recorded", "—")[:10]))

    # Split the total by corpus. Pooling them reported "40 of 131", which flatters the
    # eLife corpus: the two bioRxiv method examples are the best-covered scripts in the
    # repository and contributed 21 of those 40. Counting a number over the wrong population
    # is the error this whole directory keeps finding, so it is not made here.
    def sub(pred):
        c = sum(int(r[2].split("/")[0]) for r in rows if "/" in r[2] and pred(r))
        s = sum(int(r[2].split("/")[1]) for r in rows if "/" in r[2] and pred(r))
        return c, s

    site_c, site_s = sub(lambda r: r[1] == "site corpus")
    ex_c, ex_s = sub(lambda r: r[1] == "method example")

    import corpus_facts as CF
    site_papers, _ = CF.corpora()
    no_script = [s for s in site_papers
                 if not os.path.isfile(os.path.join(VERIF, s, "verify.py"))]
    facts_path = os.path.join(ROOT, "site", "src", "data", "corpus-facts.json")
    all_settleable = None
    if os.path.isfile(facts_path):
        with open(facts_path, encoding="utf-8") as fh:
            all_settleable = json.load(fh).get("eligible_claims")
    out = [MARK_A,
           "",
           "| Directory | Corpus | Claims covered | Last observed run | Run on |",
           "|:----------|:-------|:---------------|:------------------|:-------|"]
    for d, corpus, covtxt, tally, when in rows:
        out.append(f"| `{d}/` | {corpus} | {covtxt} | {tally} | {when} |")
    lines = [
        "",
        "**Claims covered** is how many of the paper's claims that a re-run could settle "
        "— its `empirical` and `control` claims carrying a reproduction record — the script "
        "actually produces a result for.",
        "",
        f"- **eLife corpus: {site_c} of {site_s}.**",
        f"- bioRxiv method examples: {ex_c} of {ex_s}. Counted apart, and never folded in: "
        f"they are the best-covered scripts here, and pooling them once reported "
        f"\"{site_c + ex_c} of {site_s + ex_s}\" for a corpus whose own figure is "
        f"{site_c} of {site_s}.",
    ]
    if no_script and all_settleable:
        lines.append(
            f"- {len(no_script)} of the ten eLife papers have no verification script at all "
            f"({', '.join('`' + s + '`' for s in no_script)}), so across the corpus's "
            f"{all_settleable} settleable claims, **{site_c} have a status that running this "
            f"code produced** — {round(100 * site_c / all_settleable)}%.")
    lines += [
        "",
        "Every other settleable claim carries a status an agent reached by reading a deposit "
        "rather than by running code. That is a weaker kind of verification, and these "
        "numbers are here because nothing else says so.",
        "",
    ]
    out += lines + [
            f"{len(rows)} scripts. Generated by `scripts/audit_verifications.py "
            "--update-readme` from the directories and from each run's `provenance.json` "
            "— never typed by hand.",
            MARK_B]
    return "\n".join(out)


def update_readme():
    with open(README, encoding="utf-8") as fh:
        text = fh.read()
    table = papers_table()
    if MARK_A in text and MARK_B in text:
        pre, rest = text.split(MARK_A, 1)
        _, post = rest.split(MARK_B, 1)
        text = pre + table + post
    else:
        raise SystemExit(f"{README} has no {MARK_A} … {MARK_B} block to fill")
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"updated {os.path.relpath(README, ROOT)}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--all-levels", action="store_true",
                    help="show reviews and notes, not only errors")
    ap.add_argument("--update-readme", action="store_true",
                    help="regenerate the Papers Covered table in verification/README.md")
    a = ap.parse_args()

    if a.update_readme:
        update_readme()
        return 0

    papers = [a.paper] if a.paper else sorted(
        d for d in os.listdir(CLAIMS_DIR)
        if os.path.isfile(os.path.join(VERIF, d, "verify.py")))

    out = {}
    tally = {"error": 0, "review": 0, "info": 0}
    for p in papers:
        findings, prov, coverage = audit(p)
        out[p] = {"findings": findings,
                  "coverage": coverage,
                  "results": len(prov.get("results", [])) if prov else 0,
                  "files_opened": len(prov.get("opened", [])) if prov else 0,
                  "degraded": bool(prov and prov.get("missing_dependencies"))}
        for f in findings:
            tally[f.get("level", "error")] = tally.get(f.get("level", "error"), 0) + 1

    if a.json:
        print(json.dumps(out, indent=2))
        return 1 if tally["error"] else 0

    order = {"error": 0, "review": 1, "info": 2}
    for p, r in out.items():
        cov = r.get("coverage")
        covtxt = (f" · covers {cov['covered']}/{cov['settleable']} settleable claim(s)"
                  if cov else "")
        head = f"{p:38} {r['results']:>3} result(s) · {r['files_opened']:>3} file(s){covtxt}"
        errs = [f for f in r["findings"] if f.get("level") == "error"]
        if not r["findings"]:
            print(f"  {head}  ok")
            continue
        if not errs and not a.all_levels:
            n = len(r["findings"])
            print(f"  {head}  ok · {n} note(s), --all-levels to see")
            continue
        print(f"\n{head}{'  ⚠ degraded environment' if r['degraded'] else ''}")
        for f in sorted(r["findings"], key=lambda f: order.get(f.get("level"), 0)):
            if f.get("level") != "error" and not a.all_levels:
                continue
            lvl = {"error": "ERROR", "review": "review", "info": "note"}[f.get("level", "error")]
            print(f"    {lvl:6} {f['kind']:13} {f['claim'] or '—'}")
            print(f"           {f['detail']}")

    print(f"\n{tally['error']} error(s) — a record asserting more than the run supports, or a "
          f"run that did not happen")
    print(f"{tally['review']} to review — the record is more conservative than the run")
    print(f"{tally['info']} verified by reading rather than by running"
          + ("" if a.all_levels else "   (--all-levels to list)"))
    return 1 if tally["error"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
