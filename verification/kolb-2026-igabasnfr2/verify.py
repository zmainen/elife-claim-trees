#!/usr/bin/env python3
"""
Verification script for Kolb et al. 2026 — iGABASnFR2 Crystal Structure.
eLife | doi:10.7554/eLife.kolb2026

FAST MODE (default, ~1 min):
  Downloads PDB 9D57 from RCSB and checks structure metadata.
  Requirements: none (stdlib only)
  Data: https://files.rcsb.org/download/9D57.pdb (~3 MB)

FULL MODE (--full, not applicable):
  The crystal structure is a deposited artifact — there is no computational
  pipeline to re-run. Full reproduction would require re-solving the structure
  from diffraction data, which requires synchrotron access and crystallography
  software (CCP4, Phenix). This is a wet-lab-only claim.
  Note: Diffraction data may be available in the PDB entry; contact authors.

Usage:
  python verify.py           # fast mode
  python verify.py --full    # prints wet-lab instructions
  python verify.py --claim crystal-structure-pdb-9d57
"""

import argparse
import sys
import os
import time
import urllib.request

PDB_ID = "9D57"
PDB_URL = f"https://files.rcsb.org/download/{PDB_ID}.pdb"
CACHE_DIR = "/tmp/kolb-2026"
os.makedirs(CACHE_DIR, exist_ok=True)
PDB_PATH = os.path.join(CACHE_DIR, f"{PDB_ID}.pdb")

ROWS = []

def row(slug, paper_val, repro_val, status, measured=True):
    """`measured=False` when repro_val is a remembered observation this run did not make.

    The status still says what the evidence would mean if it held; the flag says whether this
    run is the thing that found it. Downstream needs to tell those apart, and the status field
    alone cannot: a PASS carrying numbers copied from notes is indistinguishable from a PASS
    carrying numbers a simulation just produced.
    """
    ROWS.append((slug, paper_val, repro_val, status, measured))

def print_table():
    col_w = [42, 30, 48, 6]
    header = ["CLAIM SLUG", "PAPER VALUE", "REPRODUCED", "STATUS"]
    sep = "-+-".join("-" * w for w in col_w)
    print("\n" + sep)
    print(" | ".join(h.ljust(w) for h, w in zip(header, col_w)))
    print(sep)
    for r in ROWS:
        cells = list(r[:4])
        if len(r) >= 5 and not r[4]:
            cells[3] = f"{cells[3]}*"
        print(" | ".join(str(v).ljust(w) for v, w in zip(cells, col_w)))
    print(sep)
    if any(len(r) >= 5 and not r[4] for r in ROWS):
        print("* not measured in this run — the value is from notes taken when the "
              "analysis was first done.")
    print()

# ── Download PDB ───────────────────────────────────────────────────────────────

def download_pdb():
    if os.path.exists(PDB_PATH):
        print(f"[data] PDB {PDB_ID} already cached at {PDB_PATH}")
        return True
    print(f"[data] Downloading {PDB_URL} ...")
    try:
        req = urllib.request.Request(PDB_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp, open(PDB_PATH, "wb") as f:
            content = resp.read()
            f.write(content)
        print(f"[data] Downloaded {len(content)//1024} KB")
        return True
    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        return False

# ── Parse PDB ─────────────────────────────────────────────────────────────────

def parse_pdb(path):
    result = {}
    with open(path) as f:
        lines = f.readlines()

    header_lines = [l for l in lines if l.startswith("HEADER")]
    result["header"] = header_lines[0].strip() if header_lines else ""

    title_lines = [l[10:].strip() for l in lines if l.startswith("TITLE")]
    result["title"] = " ".join(title_lines)

    method_lines = [l[10:].strip() for l in lines if l.startswith("EXPDTA")]
    result["method"] = " ".join(method_lines)

    res_lines = [l for l in lines if l.startswith("REMARK   2 ") and "RESOLUTION" in l]
    result["resolution"] = res_lines[0].strip() if res_lines else ""

    abu_atoms = [l for l in lines if l.startswith("HETATM") and " ABU " in l]
    result["abu_count"] = len(abu_atoms)
    result["abu_residues"] = list(set(l[22:26].strip() for l in abu_atoms)) if abu_atoms else []

    chain_ids = list(set(l[21] for l in lines if l.startswith("ATOM")))
    result["chains"] = sorted(chain_ids)

    cro_atoms = [l for l in lines if l.startswith("HETATM") and " CRO " in l]
    result["cro_count"] = len(cro_atoms)

    return result

# ── Claim: crystal-structure-pdb-9d57 ─────────────────────────────────────────

def verify_pdb_9d57():
    slug = "crystal-structure-pdb-9d57"
    t0 = time.time()

    if not download_pdb():
        row(slug, "9D57 exists, 2.60Å, GABA as ABU@600",
            f"Download failed from {PDB_URL}", "FAIL")
        return 0

    try:
        pdb = parse_pdb(PDB_PATH)
    except Exception as e:
        row(slug, "9D57 exists, 2.60Å, GABA as ABU@600", f"Parse error: {e}", "FAIL")
        return 0

    print(f"[pdb] Header: {pdb['header']}")
    print(f"[pdb] Title: {pdb['title']}")
    print(f"[pdb] Method: {pdb['method']}")
    print(f"[pdb] Resolution: {pdb['resolution']}")
    print(f"[pdb] Chains: {pdb['chains']}")
    print(f"[pdb] ABU (GABA) atoms: {pdb['abu_count']}, residues: {pdb['abu_residues']}")
    print(f"[pdb] CRO (chromophore) atoms: {pdb['cro_count']}")
    print()

    checks = {
        "accession_9d57": True,
        "title_igabasnfr2": any(kw in pdb["title"].upper() for kw in ["IGABASNFR", "GABA", "FLUORESCENT"])
                            or any(kw in pdb["header"].upper() for kw in ["IGABASNFR", "GABA", "FLUOR"]),
        "method_xray": "X-RAY" in pdb["method"].upper(),
        "resolution_260": "2.60" in pdb["resolution"] or "2.6" in pdb["resolution"],
        "gaba_abu_present": pdb["abu_count"] > 0,
        "abu_residue_600": "600" in pdb["abu_residues"] if pdb["abu_residues"] else False,
        "multiple_chains": len(pdb["chains"]) >= 4,
    }

    all_pass = all(checks.values())
    res_str = pdb["resolution"].split()[-1] if pdb["resolution"] else "?"
    repro = (
        f"X-RAY={checks['method_xray']}, res={res_str}, "
        f"ABU={pdb['abu_count']}@{pdb['abu_residues']}, chains={pdb['chains']}"
    )

    row(slug, "9D57 exists, X-RAY 2.60Å, iGABASnFR2+GABA, ABU@600",
        repro[:80], "PASS" if all_pass else "FAIL")

    if not all_pass:
        for k, v in checks.items():
            if not v:
                print(f"  [FAIL] Check failed: {k}")

    print(f"  {slug}: → {'PASS' if all_pass else 'FAIL'} ({time.time()-t0:.1f}s)")
    return 1 if all_pass else 0

# ── Full pipeline ──────────────────────────────────────────────────────────────

def full_pipeline():
    """Crystal structures are deposited artifacts — no computational re-derivation."""
    print("\nFULL PIPELINE MODE — Crystal Structure")
    print("=" * 60)
    print("The crystal structure (PDB 9D57) is a deposited artifact.")
    print("Re-solving from diffraction data requires:")
    print("  - Raw diffraction images (contact corresponding author or check PDB entry)")
    print("  - Synchrotron beamline data processing (XDS, HKL2000)")
    print("  - Structure refinement (CCP4 suite or Phenix)")
    print("  - Validation against RCSB standards")
    print()
    print("The fast mode (downloading 9D57.pdb) is the maximum computational")
    print("reproduction possible without synchrotron access.")
    raise NotImplementedError(
        "Crystal structure re-determination requires synchrotron access and "
        "crystallography software. The deposited PDB is the verifiable artifact."
    )

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Verify Kolb et al. 2026 — iGABASnFR2 Crystal Structure"
    )
    parser.add_argument('--full', action='store_true', help='Print wet-lab re-determination instructions')
    parser.add_argument('--claim', help='Verify a single claim by slug')
    args = parser.parse_args()

    print(f"{'FULL' if args.full else 'FAST'} MODE — estimated time: {'N/A (wet lab only)' if args.full else '~1 min'}")
    print("=" * 60)

    if args.full:
        full_pipeline()
        return 0

    print(f"Data source: RCSB PDB {PDB_ID} — {PDB_URL}")
    print()

    if args.claim and args.claim != "crystal-structure-pdb-9d57":
        print(f"Unknown claim: {args.claim}. Valid slug: crystal-structure-pdb-9d57")
        return 1

    verify_pdb_9d57()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print_table()

    n_pass = sum(1 for r in ROWS if r[3] == "PASS")
    n_fail = sum(1 for r in ROWS if r[3] == "FAIL")
    print(f"{n_pass}/{len(ROWS)} claims verified")
    return 0 if n_fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
