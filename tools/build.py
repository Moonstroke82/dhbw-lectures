"""Build lecture slides: Markdown -> PPTX (build/) + HTML (docs/, GitHub Pages).

Usage (from the Lectures folder):
    python tools/build.py                 build all sessions
    python tools/build.py data-management/slides/session-01.md
    python tools/build.py --preview ...   also export PPTX slides as PNG via PowerPoint (Windows)
    python tools/build.py --notes ...     include speaker notes in the HTML (not for publishing)
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import render_html  # noqa: E402
import render_pptx  # noqa: E402
import website  # noqa: E402
from slidemd import load_deck  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
COURSES = ["data-management", "it-management-eam", "data-analytics", "data-engineering-analytics-project"]  # metadata in <course>/course.json


def export_png(pptx, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.png"):
        old.unlink()
    ps = (f"$app = New-Object -ComObject PowerPoint.Application; "
          f"$p = $app.Presentations.Open('{pptx}', $true, $false, $false); "
          f"$i = 1; foreach ($s in $p.Slides) {{ $s.Export('{out_dir}\\slide-' + $i.ToString('00') + '.png', 'PNG', 1600, 900); $i++ }}; "
          f"$p.Close()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def build(src, args):
    course = src.parent.parent.name
    # private, gitignored: lecturer name for the PPTX title slide and values for
    # {{private:key|Fallback}} placeholders (e.g. partner company names) - PPTX only
    local = ROOT / "tools" / "local.json"
    private = json.loads(local.read_text(encoding="utf-8")) if local.exists() else {}
    deck = load_deck(src, private)
    for k, v in private.items():
        if isinstance(v, str):
            deck.meta.setdefault(k, v)
    name = src.stem
    pptx = ROOT / "build" / course / f"{name}.pptx"
    render_pptx.render(deck, pptx)
    public = load_deck(src)  # public web version: placeholders get their fallback text
    render_html.render(public, ROOT / "docs" / course / f"{name}.html", include_notes=args.notes)
    ok = True
    for n, sl in enumerate(deck.slides, 1):
        for w in sl.warnings:
            ok = False
            print(f"  WARNING slide {n} '{sl.title}': {w}")
    print(f"built {course}/{name}: {len(deck.slides)} slides -> {pptx.relative_to(ROOT)}, docs/{course}/{name}.html"
          + ("" if ok else "  (see warnings)"))
    if args.preview:
        export_png(pptx, ROOT / "build" / "preview" / course / name)
    return course, name, deck


def write_indexes(built):
    docs = ROOT / "docs"
    (docs / "assets").mkdir(parents=True, exist_ok=True)
    (docs / "assets" / "slides.css").write_text(render_html.css(), encoding="utf-8")
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    old = docs / "assets" / "index.css"
    if old.exists():
        old.unlink()
    website.write(ROOT, docs, COURSES)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--preview", action="store_true")
    ap.add_argument("--notes", action="store_true")
    args = ap.parse_args()
    files = [Path(f).resolve() for f in args.files] or sorted(ROOT.glob("*/slides/session-*.md"))
    built = [build(f, args) for f in files]
    write_indexes(built)


if __name__ == "__main__":
    main()
