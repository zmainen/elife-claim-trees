"""Export one version as JSON-LD carrying the standards mapping: PROV for the run, the claim
vocabulary's mapped IRIs for each claim, CiTO/MIRA/DG terms for each relation. Reads
standards.yaml; changes there change the export."""

from __future__ import annotations

from pathlib import Path

import yaml

from . import claims as C
from .process import Process
from .store import Store

HERE = Path(__file__).resolve().parent


def standards() -> dict:
    return yaml.safe_load((HERE / "standards.yaml").read_text(encoding="utf-8"))


def export(proc: Process, store: Store, root: Path, sid: str, step_id: str, v: int | None = None) -> dict:
    std = standards()
    v = v or store.latest(sid, step_id)
    vd = store.version_dir(sid, step_id, v)
    rec = store.run_record(sid, step_id, v) or {}
    cs = C.load(vd) or {}
    step = proc.steps[step_id]
    agent_type = "prov:SoftwareAgent" if step.automatic else "prov:Agent"   # a player may be either; the record says who
    graph = [
        {"@id": f"urn:chain:{sid}:{step_id}:v{v}", "@type": ["prov:Entity", "docmaps:Output"],
         "prov:wasGeneratedBy": f"urn:chain:{sid}:{step_id}:v{v}:run",
         "prov:wasRevisionOf": f"urn:chain:{sid}:{step_id}:v{v-1}" if v > 1 else None,
         "prov:wasDerivedFrom": [f"urn:chain:{i['ref']}:v{i['v']}" for i in rec.get("in", []) if i["kind"] == "step"],
         "chain:sha": rec.get("out", {}).get("sha")},
        {"@id": f"urn:chain:{sid}:{step_id}:v{v}:run", "@type": ["prov:Activity", "docmaps:Action"],
         "prov:startedAtTime": rec.get("asked"), "prov:endedAtTime": rec.get("answered"),
         "prov:wasAssociatedWith": {"@id": f"urn:chain:agent:{rec.get('by')}", "@type": agent_type},
         "prov:used": [{"@id": i.get("ref") and f"urn:chain:{i['ref']}:v{i['v']}" or f"urn:chain:file:{i['path']}",
                        "chain:sha": i["sha"], "chain:kind": i["kind"]} for i in rec.get("in", [])]},
    ]
    for c in cs.get("claims") or []:
        m = std["types"].get(c["type"], {})
        graph.append({"@id": f"urn:chain:{C.gid(sid, step_id, c['id'])}",
                      "@type": ["chain:" + c["type"]] + [f"{k}:{val}" for k, val in m.items() if k != "note"],
                      "schema:text": c.get("text"), "prov:wasAttributedTo": c.get("by"),
                      "schema:about": [f"urn:chain:{a}" for a in c.get("about") or []] or None,
                      "chain:verdict": c.get("verdict"), "chain:standardsNote": m.get("note")})
    for e in cs.get("edges") or []:
        m = std["relations"].get(e["rel"], {})
        graph.append({"@id": f"urn:chain:{_g(sid, step_id, e['from'])}",
                      "chain:" + e["rel"]: f"urn:chain:{_g(sid, step_id, e['to'])}",
                      **{f"{k}:{val}": f"urn:chain:{_g(sid, step_id, e['to'])}" for k, val in m.items()
                         if k != "note" and " " not in str(val)}})
    return {"@context": dict(std["contexts"], chain="urn:chain:vocab#"),
            "@graph": [{k: v for k, v in n.items() if v is not None} for n in graph]}


def _g(sid, step, ref):
    return ref if ":" in ref else C.gid(sid, step, ref)
