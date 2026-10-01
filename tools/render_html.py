"""Render a laid-out Deck to a reveal.js HTML page for GitHub Pages.

Uses the same layout as the PPTX (absolute positions in a 960x540 canvas that
reveal.js scales), so both outputs look the same.
"""
import html
import shutil
from pathlib import Path

import theme
from slidemd import inline_runs

REVEAL = "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0"


def esc(s):
    return html.escape(s, quote=True)


def inline(text):
    out = []
    for t, st in inline_runs(text):
        s = esc(t)
        if st.get("code"):
            s = f"<code>{s}</code>"
        if st.get("b"):
            s = f"<strong>{s}</strong>"
        if st.get("i"):
            s = f"<em>{s}</em>"
        if st.get("link"):
            s = f'<a href="{esc(st["link"])}" target="_blank" rel="noopener">{s}</a>'
        out.append(s)
    return "".join(out)


def box(el, cls, inner="", extra=""):
    return (f'<div class="{cls}" style="left:{el["x"]:.1f}px;top:{el["y"]:.1f}px;'
            f'width:{el["w"]:.1f}px;height:{el["h"]:.1f}px;{extra}">{inner}</div>')


def text_el(el, refs):
    parts = []
    for p in el["paras"]:
        size = p.get("size", el["size"])
        style = f"font-size:{size}px;"
        if p.get("bold"):
            style += "font-weight:700;"
        if p.get("color"):
            style += f"color:#{theme.COLORS[p['color']]};"
        if "level" in p:
            ind = theme.BULLET_INDENT * (p["level"] + 1)
            style += f"padding-left:{ind}px;margin-bottom:{p['space']:.1f}px;"
            marker = "" if refs else ("&bull;" if p["level"] == 0 else "&ndash;")
            if p["ordered"] and not refs:
                marker = '<span class="num"></span>'
            cls = "li ol" if p["ordered"] else "li"
            parts.append(f'<div class="{cls}" style="{style}"><span class="mk" '
                         f'style="width:{theme.BULLET_INDENT}px;left:{ind - theme.BULLET_INDENT}px">{marker}</span>'
                         f'{inline(p["text"])}</div>')
        else:
            parts.append(f'<p style="{style}">{inline(p["text"])}</p>')
    cls = "txt muted" if el.get("muted") else "txt"
    return box({**el, "h": el["h"] + 4}, cls, "".join(parts))


def table_el(el):
    b = el["block"]
    cols = "".join(f'<col style="width:{w:.1f}px">' for w in el["colw"])
    al = {"l": "left", "c": "center", "r": "right"}
    head = "".join(f'<th style="text-align:{al[a]}">{inline(c)}</th>' for c, a in zip(b["header"], b["aligns"]))
    rows = ""
    for r in b["rows"]:
        rows += "<tr>" + "".join(f'<td style="text-align:{al[a]}">{inline(c)}</td>' for c, a in zip(r, b["aligns"])) + "</tr>"
    inner = (f'<table style="font-size:{el["size"]}px"><colgroup>{cols}</colgroup>'
             f"<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>")
    return box(el, "tbl", inner)


def render_slide(sl, deck, n, include_notes, img_map):
    m = deck.meta
    cls = " ".join(sl.classes)
    if "title" in sl.classes:
        lines = [m.get(k, "") for k in ("subtitle", "program")]  # no lecturer name on the public web version
        sub = "".join(f'<p class="{"sub" if i == 0 else "meta"}">{inline(l)}</p>' for i, l in enumerate(lines) if l)
        inner = (f'<div class="titleslide"><p class="course">{esc(m.get("course", ""))}</p>'
                 f'<h1>Session {esc(m.get("session", ""))}: {inline(m.get("title", ""))}</h1>'
                 f'<div class="bar"></div>{sub}</div>')
    elif "section" in sl.classes:
        paras = "".join(f"<p>{inline(b['text'])}</p>" for b in sl.blocks if b["type"] == "para")
        inner = f'<div class="sectionslide"><h1>{inline(sl.title)}</h1><div class="bar"></div>{paras}</div>'
    else:
        refs = "references" in sl.classes
        parts = [f'<h2 class="stitle">{inline(sl.title)}</h2><div class="rule"></div>']
        if "optional" in sl.classes:
            parts.append('<div class="badge optional">OPTIONAL · SELF-STUDY</div>')
        elif "exercise" in sl.classes:
            parts.append('<div class="badge exercise">EXERCISE</div>')
        for el in sl.layout:
            k = el["kind"]
            if k == "text":
                parts.append(text_el(el, refs))
            elif k == "table":
                parts.append(table_el(el))
            elif k == "code":
                parts.append(box(el, "code", f'<pre style="font-size:{el["size"]}px">{esc(el["text"])}</pre>'))
            elif k == "card":
                parts.append(box(el, "card"))
            elif k == "callout":
                parts.append(box(el, "callout"))
            elif k == "layer":
                fill = "primary" if el["index"] % 2 == 0 else "accent"
                parts.append(box(el, "layer", f'<div class="lab" style="width:{el["lw"]:.1f}px;background:#{theme.COLORS[fill]};'
                                              f'font-size:{el["size"]}px">{inline(el["label"])}</div>'
                                              f'<div class="desc" style="font-size:{el["size"]}px">{inline(el["desc"])}</div>'))
            elif k == "image":
                parts.append(box(el, "img", f'<img src="{img_map[el["src"]]}" alt="{esc(el["alt"])}">'))
        foot = f'{esc(m.get("course", ""))} · Session {esc(m.get("session", ""))}: {inline(m.get("title", ""))}'
        parts.append(f'<div class="footer">{foot}</div><div class="pageno">{n}</div>')
        inner = "".join(parts)
    notes = f'<aside class="notes">{esc(sl.notes)}</aside>' if include_notes and sl.notes else ""
    return f'<section class="{cls}" data-title="{esc(sl.title)}">{inner}{notes}</section>'


def render(deck, out_path, include_notes=False):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img_map = {}
    for sl in deck.slides:
        for el in sl.layout:
            if el["kind"] == "image":
                src = Path(el["src"])
                dst = out_path.parent / "img" / src.name
                dst.parent.mkdir(exist_ok=True)
                shutil.copy2(src, dst)
                img_map[el["src"]] = f"img/{src.name}"
    m = deck.meta
    title = f'{m.get("course", "")} – Session {m.get("session", "")}: {m.get("title", "")}'
    slides = "\n".join(render_slide(sl, deck, n, include_notes, img_map) for n, sl in enumerate(deck.slides, 1))
    plugins = "[RevealNotes]" if include_notes else "[]"
    notes_js = f'<script src="{REVEAL}/plugin/notes/notes.js"></script>' if include_notes else ""
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{REVEAL}/dist/reveal.css">
<link rel="stylesheet" href="../assets/slides.css">
</head>
<body>
<div class="reveal"><div class="slides">
{slides}
</div></div>
<script src="{REVEAL}/dist/reveal.js"></script>
{notes_js}
<script>
Reveal.initialize({{width: {theme.SLIDE_W}, height: {theme.SLIDE_H}, margin: 0.03, center: false,
  hash: true, slideNumber: false, transition: 'none', plugins: {plugins}}});
</script>
</body>
</html>
"""
    out_path.write_text(page, encoding="utf-8")


def css():
    c = theme.COLORS
    return f""":root {{ --primary:#{c['primary']}; --accent:#{c['accent']}; --optional:#{c['optional']};
  --text:#{c['text']}; --muted:#{c['muted']}; --light:#{c['light']}; --border:#{c['border']}; }}
.reveal {{ font-family: {theme.WEB_FONT}; color: var(--text); }}
.reveal .slides {{ text-align: left; }}
.reveal .slides section {{ width: {theme.SLIDE_W}px; height: {theme.SLIDE_H}px; padding: 0; background: #fff; }}
.reveal p {{ margin: 0; line-height: {theme.LINE_HEIGHT}; }}
.reveal a {{ color: var(--accent); }}
.reveal code {{ font-family: {theme.WEB_FONT_MONO}; }}
.stitle {{ position:absolute; left:{theme.TITLE[0]}px; top:{theme.TITLE[1]}px; width:{theme.TITLE[2]}px; height:{theme.TITLE[3]}px;
  margin:0; display:flex; align-items:flex-end; font-family:inherit; font-size:{theme.TITLE_SIZE}px; font-weight:700;
  color:var(--primary); text-transform:none; line-height:1.1; letter-spacing:0; }}
.rule {{ position:absolute; left:{theme.TITLE[0]}px; top:{theme.RULE_Y}px; width:60px; height:3px; background:var(--accent); }}
.txt, .tbl, .code, .card, .callout, .layer, .img {{ position:absolute; }}
.txt {{ line-height:{theme.LINE_HEIGHT}; }}
.txt.muted {{ color: var(--muted); }}
.li {{ position:relative; line-height:{theme.LINE_HEIGHT}; }}
.li .mk {{ position:absolute; color:var(--accent); }}
.txt {{ counter-reset: n; }}
.li.ol {{ counter-increment: n; }}
.li .num::before {{ content: counter(n) "."; color: var(--accent); }}
.card {{ background:var(--light); border:1px solid var(--border); border-radius:8px; box-sizing:border-box; }}
.callout {{ background:var(--light); border-left:{theme.CALLOUT_BAR}px solid var(--accent); box-sizing:border-box; }}
.layer {{ display:flex; }}
.layer .lab {{ color:#fff; font-weight:700; padding:0 {theme.BOX_PAD}px; display:flex; align-items:center; box-sizing:border-box; line-height:{theme.LINE_HEIGHT}; }}
.layer .desc {{ flex:1; background:var(--light); padding:0 {theme.BOX_PAD}px; display:flex; align-items:center; line-height:{theme.LINE_HEIGHT}; }}
.tbl table {{ border-collapse:collapse; table-layout:fixed; width:100%; margin:0; }}
.tbl th, .tbl td {{ padding:{theme.CELL_PAD}px; line-height:{theme.LINE_HEIGHT}; border:none; vertical-align:top; }}
.tbl th {{ background:var(--primary); color:#fff; font-weight:700; }}
.tbl tbody tr:nth-child(odd) td {{ background:var(--light); }}
.code {{ background:var(--light); border:1px solid var(--border); box-sizing:border-box; }}
.code pre {{ margin:0; padding:{theme.BOX_PAD}px; box-shadow:none; width:auto; font-family:{theme.WEB_FONT_MONO}; line-height:{theme.LINE_HEIGHT}; }}
.img img {{ width:100%; height:100%; margin:0; }}
.badge {{ position:absolute; right:43px; top:30px; padding:2px 10px; border-radius:6px; color:#fff; font-size:10px; font-weight:700; }}
.badge.optional {{ background:var(--optional); }} .badge.exercise {{ background:var(--accent); }}
.footer, .pageno {{ position:absolute; top:{theme.FOOTER_Y}px; font-size:{theme.FOOTER_SIZE}px; color:var(--muted); }}
.footer {{ left:43px; }} .pageno {{ right:43px; }}
section.title, section.section {{ background: var(--primary) !important; }}
.titleslide, .sectionslide {{ position:absolute; left:60px; top:110px; width:840px; color:#fff; }}
.titleslide .course {{ font-size:20px; margin-bottom:12px; }}
.reveal .titleslide h1, .reveal .sectionslide h1 {{ color:#fff; font-family:inherit; font-size:40px; font-weight:700; text-transform:none;
  letter-spacing:0; line-height:1.15; margin:0; }}
.reveal .sectionslide h1 {{ font-size:36px; margin-top:60px; }}
.bar {{ width:80px; height:4px; background:var(--accent); margin:18px 0; }}
.titleslide .sub, .sectionslide p {{ font-size:18px; margin-bottom:6px; }}
.titleslide .meta {{ font-size:14px; margin-bottom:6px; }}
"""


def index_page(title, intro, items, depth):
    """items: list of (href, label, sublabel)."""
    lis = "".join(f'<li><a href="{esc(h)}">{esc(l)}</a>{" – " + esc(s) if s else ""}</li>' for h, l, s in items)
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><link rel="stylesheet" href="{up}assets/index.css"></head>
<body><main><h1>{esc(title)}</h1><p>{intro}</p><ul>{lis}</ul></main></body></html>
"""


INDEX_CSS = f"""body {{ font-family: {theme.WEB_FONT}; color:#{theme.COLORS['text']}; margin:0; background:#{theme.COLORS['light']}; }}
main {{ max-width: 760px; margin: 48px auto; background:#fff; padding: 32px 40px; border-top: 6px solid #{theme.COLORS['primary']}; }}
h1 {{ color:#{theme.COLORS['primary']}; }}
a {{ color:#{theme.COLORS['accent']}; font-weight:700; }}
li {{ margin: 8px 0; }}
"""
