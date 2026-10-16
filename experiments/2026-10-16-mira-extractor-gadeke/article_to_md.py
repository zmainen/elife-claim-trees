"""Article JSON (site/src/data/article/<slug>.json) -> clean markdown for MIRA-extraction."""
import html, json, re, sys

src, dst = sys.argv[1], sys.argv[2]
d = json.load(open(src))
figs = {f["id"]: f for f in d["figures"]}
tabs = {t["id"]: t for t in d["tables"]}

def plain(h):
    h = re.sub(r"<[^>]+>", "", h or "")
    return html.unescape(h).strip()

out = [f"# {d['title']}", "", ", ".join(d["authors"]), "", f"eLife {d['year']}. DOI: {d['doi']}", ""]
out += ["## Abstract", ""] + [" ".join(a["text"] for a in d["abstract"]), ""]

def fig_block(f):
    cap = plain(f["caption"]).replace("\n", " ")
    return [f"**{f['label']}. {plain(f['title'])}** {cap}", ""]

def table_block(t):
    lines = [f"**{t['label']}. {plain(t['title'])}**", ""]
    for i, row in enumerate(t["rows"]):
        cells = [plain(c["html"]) for c in row]
        lines.append("| " + " | ".join(cells) + " |")
        if i == 0: lines.append("|" + "---|" * len(cells))
    if t.get("caption"): lines += ["", plain(t["caption"])]
    return lines + [""]

def walk(blocks, depth):
    for b in blocks:
        if b["type"] == "p": out.extend([b["text"].strip(), ""])
        elif b["type"] == "sec":
            s = b["sec"]; out.extend(["#" * min(s["depth"] + 1, 6) + " " + plain(s["title"]), ""]); walk(s["blocks"], s["depth"])
        elif b["type"] == "fig" and b["id"] in figs: out.extend(fig_block(figs[b["id"]]))
        elif b["type"] == "table" and b["id"] in tabs: out.extend(table_block(tabs[b["id"]]))

for s in d["sections"]:
    out.extend(["## " + plain(s["title"]), ""]); walk(s["blocks"], 1)

text = "\n".join(out)
open(dst, "w").write(text)
print(len(text), "chars")
