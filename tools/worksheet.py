"""Render a worksheet (Markdown) to a printable HTML page.

One file per session: <course>/worksheets/session-NN.md (format: see tools/FORMAT.md).
Two outputs from the same source:
- student version without solutions -> docs/<course>/worksheet-NN.html (published)
- lecturer version with solutions   -> build/<course>/worksheet-NN-solutions.html (not published)
"""
import html
import re
import shutil
from pathlib import Path

import theme
from render_html import inline
from slidemd import PRIVATE_RE, parse_blocks

HEAD_RE = re.compile(r"^(#{2,3})\s+(.*?)\s*(\{([^}]*)\})?\s*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?!https?:|mailto:|#)([^)\s]+)\)")


def esc(s):
    return html.escape(str(s), quote=True)


def load(path, private=None):
    """Returns (meta, sections); a section is {'level', 'title', 'classes', 'blocks'}."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    text = PRIVATE_RE.sub(lambda m: (private or {}).get(m.group(1), m.group(2)), text)
    meta = {}
    if text.startswith("---"):
        head, _, text = text[3:].partition("\n---")
        for ln in head.strip().splitlines():
            k, _, v = ln.partition(":")
            if k.strip():
                meta[k.strip()] = v.strip()
    sections, cur, in_code = [], {"level": 0, "title": "", "classes": [], "lines": []}, False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_code = not in_code
        m = None if in_code else HEAD_RE.match(ln)
        if m:
            sections.append(cur)
            cur = {"level": len(m.group(1)), "title": m.group(2),
                   "classes": [c.lstrip(".") for c in (m.group(4) or "").split()], "lines": []}
        else:
            cur["lines"].append(ln)
    sections.append(cur)
    for s in sections:
        s["blocks"] = parse_blocks(s.pop("lines"))
    return meta, [s for s in sections if s["title"] or s["blocks"]]


def blocks_html(blocks, solutions, img_map):
    out = []
    for b in blocks:
        t = b["type"]
        if t == "para":
            out.append(f"<p>{inline(b['text'])}</p>")
        elif t == "list":
            out.append(list_html(b["items"]))
        elif t == "table":
            al = {"l": "left", "c": "center", "r": "right"}
            head = "".join(f'<th style="text-align:{al[a]}">{inline(c)}</th>' for c, a in zip(b["header"], b["aligns"]))
            rows = "".join("<tr>" + "".join(f'<td style="text-align:{al[a]}">{inline(c)}</td>'
                                            for c, a in zip(r, b["aligns"])) + "</tr>" for r in b["rows"])
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>")
        elif t == "code":
            out.append(f"<pre><code>{esc(b['text'])}</code></pre>")
        elif t == "image":
            width = b["attrs"].get("width", "70%")
            out.append(f'<p class="fig"><img src="{img_map.get(b["src"], b["src"])}" alt="{esc(b["alt"])}" '
                       f'style="width:{esc(width)}"></p>')
        elif t == "callout":
            out.append(f'<div class="callout">{blocks_html(b["blocks"], solutions, img_map)}</div>')
        elif t == "hint":
            out.append(f'<details class="hint"><summary>Hint</summary>{blocks_html(b["blocks"], solutions, img_map)}</details>')
        elif t == "answer":
            if not solutions:
                inner = blocks_html(b["blocks"], solutions, img_map)
                out.append(f'<div class="answer" style="--lines:{b["lines"]}">{inner}</div>')
        elif t == "solution":
            if solutions:
                out.append(f'<div class="solution"><p class="lab">Solution</p>{blocks_html(b["blocks"], solutions, img_map)}</div>')
        elif t == "columns":
            cols = "".join(f'<div>{blocks_html(c, solutions, img_map)}</div>' for c in b["cols"])
            out.append(f'<div class="columns">{cols}</div>')
        elif t == "cards":
            cards = "".join(f'<div class="card"><h4>{inline(c["title"])}</h4>{blocks_html(c["blocks"], solutions, img_map)}</div>'
                            for c in b["cards"])
            out.append(f'<div class="cards">{cards}</div>')
        elif t == "source":
            out.append(f'<div class="source">{blocks_html(b["blocks"], solutions, img_map)}</div>')
        # "notes" and "layers" are slide-only and ignored here
    return "".join(out)


def list_html(items):
    out, stack = [], []
    for it in items:
        tag = "ol" if it["ordered"] else "ul"
        while len(stack) > it["level"] + 1:
            out.append(f"</li></{stack.pop()}>")
        if len(stack) < it["level"] + 1:
            start = f' start="{it["num"]}"' if it["ordered"] and it["num"] and it["num"] != 1 else ""
            out.append(f"<{tag}{start}>")
            stack.append(tag)
        else:
            out.append("</li>")
        out.append(f"<li>{inline(it['text'])}" + blocks_html(it.get("more", []), False, {}))
    while stack:
        out.append(f"</li></{stack.pop()}>")
    return "".join(out)


def render(src, out_path, solutions=False, private=None):
    meta, sections = load(src, private)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img_map = {}
    for s in sections:
        for b in s["blocks"]:
            if b["type"] == "image":
                p = (Path(src).parent / b["src"]).resolve()
                dst = out_path.parent / "img" / p.name
                dst.parent.mkdir(exist_ok=True)
                shutil.copy2(p, dst)
                img_map[b["src"]] = f"img/{p.name}"
    # local files linked from the worksheet (e.g. data/orders.csv) are copied next to the page
    for rel in set(LINK_RE.findall(Path(src).read_text(encoding="utf-8"))):
        f = Path(src).parent / rel
        if f.is_file():
            dst = out_path.parent / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, dst)
    body, n_task = [], 0
    for s in sections:
        inner = blocks_html(s["blocks"], solutions, img_map)
        if not s["title"]:
            body.append(f'<div class="intro">{inner}</div>')
            continue
        cls = " ".join(s["classes"])
        badge = '<span class="badge optional">Optional</span>' if "optional" in s["classes"] else ""
        if s["level"] == 2 and "references" not in s["classes"]:
            n_task += 1
            body.append(f'<section class="task {cls}"><h2><span class="no">{n_task}</span>{inline(s["title"])}{badge}</h2>{inner}</section>')
        elif s["level"] == 2:
            body.append(f'<section class="refs"><h2>{inline(s["title"])}</h2>{inner}</section>')
        else:
            body.append(f'<h3>{inline(s["title"])}{badge}</h3>{inner}')
    title = f'{meta.get("course", "")} – Worksheet {meta.get("session", "")}: {meta.get("title", "")}'
    version = '<p class="version">Lecturer version with solutions – do not publish</p>' if solutions else ""
    slides = f'<a href="session-{str(meta.get("session", "")).zfill(2)}.html">Slides</a> · ' if not solutions else ""
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{'../assets/' if not solutions else ''}worksheet.css">
</head>
<body>
<nav class="top">{'<a href="index.html">&larr; All sessions</a> · ' + slides if not solutions else ''}<a href="javascript:window.print()">Print / PDF</a></nav>
<main>
<header><p class="course">{esc(meta.get("course", ""))} · Session {esc(meta.get("session", ""))}</p>
<h1>Worksheet: {inline(meta.get("title", ""))}</h1>
{f'<p class="sub">{inline(meta["subtitle"])}</p>' if meta.get("subtitle") else ''}
<p class="meta">{esc(meta.get("program", ""))}</p>{version}
<div class="namefield"><span>Name / team:</span><span>Date:</span></div></header>
{"".join(body)}
</main>
</body>
</html>
"""
    out_path.write_text(page, encoding="utf-8")
    if solutions:
        (out_path.parent / "worksheet.css").write_text(css(), encoding="utf-8")
    return meta, n_task


def css():
    c = theme.COLORS
    return f""":root {{ --primary:#{c['primary']}; --accent:#{c['accent']}; --optional:#{c['optional']};
  --text:#{c['text']}; --muted:#{c['muted']}; --light:#{c['light']}; --border:#{c['border']}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:{theme.WEB_FONT}; color:var(--text); background:var(--light); line-height:1.5; font-size:16px; }}
main {{ max-width:820px; margin:24px auto 64px; background:#fff; padding:40px 56px 56px; border-top:6px solid var(--accent);
  box-shadow:0 6px 24px rgba(15,23,42,.08); }}
nav.top {{ max-width:820px; margin:16px auto 0; font-size:14px; color:var(--muted); }}
nav.top a {{ color:var(--muted); text-decoration:none; }} nav.top a:hover {{ color:var(--accent); }}
a {{ color:var(--accent); }}
header {{ border-bottom:2px solid var(--border); padding-bottom:16px; margin-bottom:24px; }}
header .course {{ margin:0; color:var(--accent); font-weight:700; text-transform:uppercase; letter-spacing:.06em; font-size:13px; }}
h1 {{ color:var(--primary); font-size:30px; line-height:1.2; margin:6px 0 4px; }}
header .sub {{ margin:0; font-size:17px; }}
header .meta {{ margin:4px 0 0; color:var(--muted); font-size:14px; }}
.version {{ margin:8px 0 0; color:#fff; background:var(--accent); display:inline-block; padding:2px 10px; font-weight:700; font-size:13px; }}
.namefield {{ display:flex; gap:32px; margin-top:18px; font-size:14px; color:var(--muted); }}
.namefield span {{ flex:1; border-bottom:1px solid var(--border); padding-bottom:2px; }}
.namefield span:last-child {{ flex:0 0 200px; }}
.intro {{ margin-bottom:8px; }}
section.task {{ margin:28px 0; break-inside:auto; }}
h2 {{ color:var(--primary); font-size:21px; margin:0 0 10px; display:flex; align-items:center; gap:10px; line-height:1.25; }}
h2 .no {{ flex:none; width:30px; height:30px; border-radius:50%; background:var(--accent); color:#fff; font-size:15px;
  display:inline-flex; align-items:center; justify-content:center; }}
h3 {{ color:var(--primary); font-size:17px; margin:18px 0 6px; }}
.badge {{ font-size:11px; font-weight:700; color:#fff; background:var(--optional); padding:2px 8px; border-radius:4px; text-transform:uppercase; }}
p {{ margin:0 0 10px; }}
ul, ol {{ margin:0 0 10px; padding-left:26px; }} li {{ margin:2px 0; }}
table {{ border-collapse:collapse; width:100%; margin:6px 0 14px; font-size:15px; }}
th {{ background:var(--primary); color:#fff; text-align:left; padding:6px 8px; }}
td {{ padding:6px 8px; border-bottom:1px solid var(--border); vertical-align:top; }}
tbody tr:nth-child(odd) td {{ background:var(--light); }}
pre {{ background:var(--light); border:1px solid var(--border); padding:10px 12px; overflow-x:auto; font-size:14px; margin:6px 0 14px; }}
code {{ font-family:{theme.WEB_FONT_MONO}; font-size:.92em; }}
p code, li code, td code {{ background:var(--light); padding:1px 4px; border-radius:3px; }}
.callout {{ background:var(--light); border-left:6px solid var(--accent); padding:10px 14px; margin:8px 0 14px; }}
.callout p:last-child {{ margin-bottom:0; }}
.answer {{ min-height:calc(var(--lines) * 30px + 8px); margin:6px 0 16px; border:1px solid var(--border); border-radius:4px;
  background:repeating-linear-gradient(to bottom, transparent 0, transparent 29px, var(--border) 29px, var(--border) 30px);
  background-position:0 8px; padding:4px 10px; color:var(--muted); font-size:14px; }}
details.hint {{ margin:6px 0 14px; font-size:15px; }}
details.hint summary {{ cursor:pointer; color:var(--accent); font-weight:700; }}
details.hint > *:not(summary) {{ margin-top:6px; }}
.solution {{ border:2px solid var(--accent); background:#fdf2f3; padding:10px 14px; margin:8px 0 16px; border-radius:4px; }}
.solution .lab {{ color:var(--accent); font-weight:700; text-transform:uppercase; font-size:12px; letter-spacing:.06em; margin-bottom:4px; }}
.columns {{ display:grid; grid-template-columns:1fr 1fr; gap:24px; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px; margin:6px 0 14px; }}
.card {{ background:var(--light); border:1px solid var(--border); border-radius:6px; padding:10px 14px; }}
.card h4 {{ margin:0 0 4px; color:var(--primary); }}
.fig {{ text-align:center; }} .fig img {{ max-width:100%; }}
.source {{ font-size:13px; color:var(--muted); }}
section.refs {{ margin-top:36px; border-top:1px solid var(--border); padding-top:16px; font-size:14px; }}
section.refs h2 {{ font-size:17px; }}
@media (max-width:700px) {{ main {{ padding:24px 20px; }} .columns {{ grid-template-columns:1fr; }} }}
@media print {{
  @page {{ size:A4; margin:16mm 16mm 18mm; }}
  body {{ background:#fff; font-size:11pt; }}
  nav.top {{ display:none; }}
  main {{ margin:0; padding:0; max-width:none; box-shadow:none; border-top:none; }}
  h2, h3 {{ break-after:avoid; }}
  .answer, table, pre, .callout, .solution {{ break-inside:avoid; }}
  details.hint {{ display:none; }}
  a {{ color:inherit; text-decoration:none; }}
}}
"""
