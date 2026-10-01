"""Landing page and course pages for GitHub Pages (docs/).

Course facts come from <course>/course.json, the session roadmap from
<course>/SESSION_PLAN.md; a session links to its slides once
<course>/slides/session-NN.md exists. Self-contained: no external fonts or
trackers (students' IP addresses are not sent to third parties).
"""
import datetime
import html
import json
import re
from pathlib import Path

import theme

C = theme.COLORS

ICONS = {
    # simple line icons, stroke = currentColor
    "database": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><ellipse cx="12" cy="5" rx="8" ry="3"/>'
                '<path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/></svg>',
    "architecture": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="5" rx="1"/>'
                    '<rect x="3" y="10" width="8" height="5" rx="1"/><rect x="13" y="10" width="8" height="5" rx="1"/>'
                    '<rect x="3" y="17" width="18" height="4" rx="1"/></svg>',
    "keys": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="2" y="6" width="20" height="13" rx="2"/>'
            '<path d="M6 10h.01M10 10h.01M14 10h.01M18 10h.01M7 15h10"/></svg>',
    "screen": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>',
    "print": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 9V3h12v6"/>'
             '<rect x="3" y="9" width="18" height="8" rx="2"/><path d="M6 14h12v7H6z"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M5 12.5l4.5 4.5L19 7"/></svg>',
    "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2z"/>'
            '<path d="M4 21V5M8 7h7"/></svg>',
}


def esc(s):
    return html.escape(str(s), quote=True)


def md_inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)


def load_plan(course_dir):
    """Parse SESSION_PLAN.md into [(part_title, [session dicts])]."""
    parts, cur = [], None
    for ln in (course_dir / "SESSION_PLAN.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^## (Part [A-Z])\s*[—-]\s*(.+)$", ln)
        if m:
            cur = (m.group(1), m.group(2).strip(), [])
            parts.append(cur)
            continue
        if cur and ln.startswith("| ") and not ln.startswith("| #"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 3 or set(cells[0]) <= {"-"}:
                continue
            num = cells[0]
            title = re.sub(r"\*\*(.+?)\*\*", r"\1", cells[1])
            title = re.sub(r"\s*\(\d+ h\)", "", title)          # no timings on the public site
            desc = re.sub(r"\s*\(\d+ h\)", "", cells[2])
            if num == "—":
                num = ""
            cur[2].append({"num": num, "title": title, "desc": desc})
    return parts


def head(title, depth):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><link rel="stylesheet" href="{up}assets/site.css"></head><body>"""


def nav(courses, depth, active=None):
    up = "../" * depth
    links = "".join(f'<a href="{up}{slug}/index.html"{" class=active" if slug == active else ""}>{esc(c["short"])}</a>'
                    for slug, c in courses)
    return (f'<header class="nav"><div class="wrap"><a class="brand" href="{up}index.html">'
            f'<span class="logo">{ICONS["book"]}</span>DHBW Lectures</a><nav>{links}</nav></div></header>')


def footer():
    year = datetime.date.today().year
    return (f'<footer><div class="wrap"><p>Digital Business Management (Business IT) · DHBW · {year}</p>'
            '<p class="small">All sources are cited on the slides and in the reference list of each session. '
            'Slides are built with <a href="https://revealjs.com">reveal.js</a>.</p></div></footer></body></html>')


HOWTO = f"""<section class="howto"><div class="wrap"><h2>Using the slides</h2><div class="tips">
<div class="tip"><span class="ic">{ICONS['keys']}</span><h3>Navigate</h3><p>Arrow keys or space bar. Press <kbd>Esc</kbd> for an overview of all slides.</p></div>
<div class="tip"><span class="ic">{ICONS['screen']}</span><h3>Full screen</h3><p>Press <kbd>F</kbd> for full screen, <kbd>Esc</kbd> to leave it.</p></div>
<div class="tip"><span class="ic">{ICONS['print']}</span><h3>Print or PDF</h3><p>Add <code>?print-pdf</code> to the address, then print to PDF from your browser.</p></div>
</div></div></section>"""


def landing(courses, available):
    cards = ""
    for slug, c in courses:
        n_avail = len(available.get(slug, []))
        n_total = sum(len(p[2]) for p in c["plan"])
        if n_avail:
            status = f'<span class="badge live">{n_avail} of {n_total} sessions online</span>'
        else:
            status = f'<span class="badge soon">Starts {c["first_run"]}</span>'
        cards += f"""<a class="course-card" href="{slug}/index.html">
<div class="band"><span class="icon">{ICONS[c['icon']]}</span></div>
<div class="body"><p class="meta">Semester {c['semester']} · {c['hours']} hours</p><h3>{esc(c['title'])}</h3>
<p>{esc(c['tagline'])}</p><div class="foot">{status}<span class="go">View course →</span></div></div></a>"""
    return (head("DHBW Lectures", 0) + nav(courses, 0) +
            f"""<section class="hero landing"><div class="wrap"><p class="eyebrow">DHBW · Digital Business Management (Business IT)</p>
<h1>Lecture slides</h1><p class="lead">Slides, exercises and references for the courses. Open a course to see the full session roadmap.</p></div></section>
<main class="wrap"><div class="courses">{cards}</div></main>""" + HOWTO + footer())


def course_page(slug, c, courses, available):
    chips = "".join(f'<span class="chip">{esc(t)}</span>' for t in (
        f"Semester {c['semester']}", f"{c['hours']} hours", f"{sum(len(p[2]) for p in c['plan'])} sessions", c["assessment"]))
    outcomes = "".join(f'<li><span class="ck">{ICONS["check"]}</span>{esc(o)}</li>' for o in c["outcomes"])
    parts = ""
    for code, title, sessions in c["plan"]:
        items = ""
        for s in sessions:
            num = s["num"].zfill(2) if s["num"] else ""
            live = num and num in available.get(slug, [])
            label = s["num"] or "Q&A"
            inner = (f'<span class="num">{esc(label)}</span><div><h4>{esc(s["title"])}</h4>'
                     f'<p>{md_inline(s["desc"])}</p>'
                     f'{"<span class=open>Open slides →</span>" if live else "<span class=pending>Coming soon</span>"}</div>')
            items += (f'<a class="session live" href="session-{num}.html">{inner}</a>' if live
                      else f'<div class="session">{inner}</div>')
        parts += f'<div class="part"><h3><span>{esc(code)}</span>{esc(title)}</h3><div class="sessions">{items}</div></div>'
    return (head(c["title"], 1) + nav(courses, 1, slug) +
            f"""<section class="hero small"><div class="wrap"><span class="hero-icon">{ICONS[c['icon']]}</span>
<p class="eyebrow">DHBW · Digital Business Management (Business IT)</p><h1>{esc(c['title'])}</h1>
<p class="lead">{esc(c['tagline'])}</p><div class="chips">{chips}</div></div></section>
<main class="wrap"><section class="outcomes"><h2>What you will learn</h2><ul>{outcomes}</ul></section>
<section class="roadmap"><h2>Session roadmap</h2>{parts}</section></main>""" + HOWTO + footer())


CSS = f""":root {{ --primary:#{C['primary']}; --accent:#{C['accent']}; --optional:#{C['optional']}; --text:#{C['text']};
  --muted:#{C['muted']}; --light:#{C['light']}; --border:#{C['border']}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:{theme.WEB_FONT}; color:var(--text); background:#fff; line-height:1.55; }}
a {{ color:var(--accent); }}
.wrap {{ max-width:1100px; margin:0 auto; padding:0 24px; }}
.nav {{ background:#fff; border-bottom:1px solid var(--border); position:sticky; top:0; z-index:10; }}
.nav .wrap {{ display:flex; align-items:center; justify-content:space-between; height:60px; }}
.brand {{ display:flex; align-items:center; gap:10px; font-weight:700; color:var(--primary); text-decoration:none; font-size:18px; }}
.logo {{ width:28px; height:28px; color:var(--accent); display:inline-flex; }}
.nav nav a {{ margin-left:24px; color:var(--muted); text-decoration:none; font-weight:600; font-size:15px; }}
.nav nav a:hover, .nav nav a.active {{ color:var(--primary); }}
.hero {{ background:linear-gradient(135deg, var(--primary) 0%, #16304f 55%, var(--accent) 140%); color:#fff; padding:88px 0 96px;
  position:relative; overflow:hidden; }}
.hero::after {{ content:""; position:absolute; right:-120px; top:-120px; width:420px; height:420px; border-radius:50%;
  border:60px solid rgba(255,255,255,.06); }}
.hero.landing {{ padding-bottom:170px; }}
.hero.small {{ padding:64px 0 72px; }}
.hero h1 {{ font-size:48px; line-height:1.1; margin:8px 0 16px; max-width:820px; }}
.hero.small h1 {{ font-size:40px; }}
.eyebrow {{ text-transform:uppercase; letter-spacing:.08em; font-size:13px; font-weight:700; color:#9fe0d6; margin:0; }}
.lead {{ font-size:20px; max-width:680px; opacity:.92; margin:0; }}
.hero-icon {{ display:inline-flex; width:48px; height:48px; color:#9fe0d6; margin-bottom:12px; }}
.chips {{ margin-top:24px; display:flex; flex-wrap:wrap; gap:10px; }}
.chip {{ background:rgba(255,255,255,.12); border:1px solid rgba(255,255,255,.25); padding:6px 14px; border-radius:999px; font-size:14px; }}
main {{ padding:56px 24px; }}
h2 {{ color:var(--primary); font-size:30px; margin:0 0 24px; }}
.courses {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:28px; margin-top:-120px; position:relative; }}
.course-card {{ background:#fff; border-radius:14px; overflow:hidden; text-decoration:none; color:var(--text);
  box-shadow:0 10px 30px rgba(15,23,42,.12); border:1px solid var(--border); transition:transform .15s, box-shadow .15s; display:flex; flex-direction:column; }}
.course-card:hover {{ transform:translateY(-4px); box-shadow:0 16px 40px rgba(15,23,42,.18); }}
.band {{ height:96px; background:linear-gradient(120deg, var(--accent), var(--primary)); display:flex; align-items:center; padding:0 28px; }}
.band .icon {{ width:52px; height:52px; color:#fff; display:inline-flex; }}
.course-card .body {{ padding:24px 28px 28px; display:flex; flex-direction:column; flex:1; }}
.course-card h3 {{ font-size:23px; color:var(--primary); margin:4px 0 10px; line-height:1.25; }}
.course-card p {{ margin:0; }}
.meta {{ color:var(--muted); font-size:14px; font-weight:600; }}
.foot {{ margin-top:auto; padding-top:22px; display:flex; justify-content:space-between; align-items:center; }}
.go {{ color:var(--accent); font-weight:700; }}
.badge {{ font-size:13px; font-weight:700; padding:4px 12px; border-radius:999px; }}
.badge.live {{ background:#e3f4f1; color:#1d7a6f; }}
.badge.soon {{ background:var(--light); color:var(--muted); }}
.howto {{ background:var(--light); padding:56px 0; }}
.tips {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:24px; }}
.tip {{ background:#fff; border-radius:12px; padding:24px; border:1px solid var(--border); }}
.tip .ic {{ display:inline-flex; width:36px; height:36px; color:var(--accent); }}
.tip h3 {{ margin:8px 0 6px; color:var(--primary); }}
.tip p {{ margin:0; color:var(--muted); }}
kbd {{ background:var(--light); border:1px solid var(--border); border-bottom-width:2px; border-radius:4px; padding:0 6px; font-size:13px; }}
code {{ background:var(--light); padding:1px 5px; border-radius:4px; }}
.outcomes ul {{ list-style:none; padding:0; margin:0 0 56px; display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:14px 32px; }}
.outcomes li {{ display:flex; gap:12px; align-items:flex-start; }}
.ck {{ flex:none; width:24px; height:24px; border-radius:50%; background:#e3f4f1; color:var(--accent); display:inline-flex; padding:4px; }}
.part {{ margin-bottom:40px; }}
.part h3 {{ display:flex; align-items:center; gap:12px; color:var(--primary); font-size:21px; margin:0 0 16px; }}
.part h3 span {{ background:var(--primary); color:#fff; font-size:13px; padding:3px 10px; border-radius:6px; letter-spacing:.04em; }}
.sessions {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:16px; }}
.session {{ display:flex; gap:16px; padding:18px 20px; border:1px solid var(--border); border-radius:12px; background:#fff;
  color:var(--text); text-decoration:none; }}
.session.live {{ border-color:var(--accent); box-shadow:0 4px 14px rgba(42,157,143,.12); transition:transform .15s; }}
.session.live:hover {{ transform:translateY(-2px); }}
.session .num {{ flex:none; width:40px; height:40px; border-radius:50%; background:var(--light); color:var(--primary); font-weight:700;
  display:flex; align-items:center; justify-content:center; font-size:15px; }}
.session.live .num {{ background:var(--accent); color:#fff; }}
.session h4 {{ margin:0 0 4px; color:var(--primary); font-size:17px; line-height:1.3; }}
.session p {{ margin:0 0 8px; color:var(--muted); font-size:14px; display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical; overflow:hidden; }}
.open {{ color:var(--accent); font-weight:700; font-size:14px; }}
.pending {{ color:var(--muted); font-size:13px; font-style:italic; }}
footer {{ background:var(--primary); color:rgba(255,255,255,.85); padding:32px 0; font-size:15px; }}
footer p {{ margin:4px 0; }} footer .small {{ font-size:13px; opacity:.8; }} footer a {{ color:#9fe0d6; }}
@media (max-width:640px) {{ .hero h1 {{ font-size:34px; }} .hero.small h1 {{ font-size:30px; }} .nav nav {{ display:none; }} }}
"""


def write(root, docs, course_slugs):
    courses = []
    for slug in course_slugs:
        c = json.loads((root / slug / "course.json").read_text(encoding="utf-8"))
        c["plan"] = load_plan(root / slug)
        courses.append((slug, c))
    available = {slug: [p.stem.split("-")[1] for p in sorted((root / slug / "slides").glob("session-*.md"))]
                 for slug, _ in courses if (root / slug / "slides").exists()}
    (docs / "assets").mkdir(parents=True, exist_ok=True)
    (docs / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (docs / "index.html").write_text(landing(courses, available), encoding="utf-8")
    for slug, c in courses:
        (docs / slug).mkdir(parents=True, exist_ok=True)
        (docs / slug / "index.html").write_text(course_page(slug, c, courses, available), encoding="utf-8")
