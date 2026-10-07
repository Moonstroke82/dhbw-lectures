"""Parser and layout engine for the lecture slide Markdown format.

One Markdown file per session is the single source for both outputs
(PPTX via render_pptx.py, HTML via render_html.py). Format: see tools/FORMAT.md.
"""
import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageFont

import theme

# ---------------------------------------------------------------- data model


@dataclass
class Slide:
    title: str = ""
    classes: list = field(default_factory=list)
    blocks: list = field(default_factory=list)
    notes: str = ""
    source: list = field(default_factory=list)  # list of blocks
    base: float = theme.BASE_SIZES[0]  # fitted body font size (pt)
    layout: list = field(default_factory=list)  # placed elements (pptx coords)
    warnings: list = field(default_factory=list)


@dataclass
class Deck:
    meta: dict
    slides: list
    path: Path


# ---------------------------------------------------------------- inline


INLINE_RE = re.compile(
    r"(\*\*(?P<b>.+?)\*\*)|(`(?P<code>[^`]+)`)|(\[(?P<lt>[^\]]+)\]\((?P<lu>[^)]+)\))|(\*(?P<i>[^*]+?)\*)"
)


def inline_runs(text, base=None):
    """Split inline Markdown into runs: (text, {'b','i','code','link'})."""
    base = dict(base or {})
    runs, pos = [], 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            runs.append((text[pos:m.start()], dict(base)))
        if m.group("b") is not None:
            runs += inline_runs(m.group("b"), {**base, "b": True})
        elif m.group("code") is not None:
            runs.append((m.group("code"), {**base, "code": True}))
        elif m.group("lt") is not None:
            runs += inline_runs(m.group("lt"), {**base, "link": m.group("lu")})
        else:
            runs += inline_runs(m.group("i"), {**base, "i": True})
        pos = m.end()
    if pos < len(text):
        runs.append((text[pos:], dict(base)))
    return runs


def plain(text):
    return "".join(t for t, _ in inline_runs(text))


# ---------------------------------------------------------------- block parser

LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
HEAD_RE = re.compile(r"^#\s+(.*?)\s*(\{([^}]*)\})?\s*$")
IMG_RE = re.compile(r"^!\[(.*?)\]\((.*?)\)\s*(\{([^}]*)\})?\s*$")


def _is_block_start(line):
    s = line.strip()
    return (s.startswith(":::") or s.startswith("```") or s.startswith("|")
            or LIST_RE.match(line) or IMG_RE.match(s) or s.startswith("### "))


def _collect_fenced(lines, i):
    """Collect lines of a ::: block starting at lines[i]; returns (name, inner, next_i)."""
    name = lines[i].strip()[3:].strip()
    depth, inner, i = 1, [], i + 1
    while i < len(lines):
        s = lines[i].strip()
        if s.startswith(":::") and s[3:].strip():
            depth += 1
        elif s == ":::":
            depth -= 1
            if depth == 0:
                return name, inner, i + 1
        inner.append(lines[i])
        i += 1
    raise ValueError(f"unclosed ::: {name} block")


def _split_table_row(line):
    s = line.strip().strip("|")
    return [c.strip() for c in s.split("|")]


def parse_blocks(lines):
    blocks, i = [], 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith(":::"):
            name, inner, i = _collect_fenced(lines, i)
            blocks.append(_fenced_block(name, inner))
            continue
        if s.startswith("```"):
            lang, code = s[3:].strip(), []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code.append(lines[i])
                i += 1
            blocks.append({"type": "code", "lang": lang, "text": "\n".join(code)})
            i += 1
            continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_split_table_row(lines[i]))
                i += 1
            header, body = rows[0], rows[1:]
            aligns = ["l"] * len(header)
            if body and all(re.fullmatch(r":?-+:?", c) for c in body[0]):
                aligns = ["c" if c.startswith(":") and c.endswith(":") else "r" if c.endswith(":") else "l"
                          for c in body[0]]
                body = body[1:]
            blocks.append({"type": "table", "header": header, "rows": body, "aligns": aligns})
            continue
        m = IMG_RE.match(s)
        if m:
            attrs = dict(a.split("=", 1) for a in (m.group(4) or "").split() if "=" in a)
            blocks.append({"type": "image", "alt": m.group(1), "src": m.group(2), "attrs": attrs})
            i += 1
            continue
        if LIST_RE.match(line):
            items = []
            while i < len(lines):
                lm = LIST_RE.match(lines[i])
                if lm:
                    level = len(lm.group(1).replace("\t", "  ")) // 2
                    ordered = lm.group(2)[0].isdigit()
                    items.append({"level": level, "ordered": ordered, "text": lm.group(3),
                                  "num": int(lm.group(2)[:-1]) if ordered else None})
                elif lines[i].strip() and lines[i].startswith("  ") and items:
                    items[-1]["text"] += " " + lines[i].strip()
                else:
                    break
                i += 1
            blocks.append({"type": "list", "items": items})
            continue
        para = [s]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_start(lines[i]):
            para.append(lines[i].strip())
            i += 1
        blocks.append({"type": "para", "text": " ".join(para)})
    return blocks


def _fenced_block(name, inner):
    if name == "columns":
        cols, cur = [], []
        for ln in inner:
            if ln.strip() == "|||":
                cols.append(cur)
                cur = []
            else:
                cur.append(ln)
        cols.append(cur)
        return {"type": "columns", "cols": [parse_blocks(c) for c in cols]}
    if name == "cards":
        cards, cur = [], None
        for ln in inner:
            if ln.strip().startswith("### "):
                cur = {"title": ln.strip()[4:], "lines": []}
                cards.append(cur)
            elif cur is not None:
                cur["lines"].append(ln)
        return {"type": "cards", "cards": [{"title": c["title"], "blocks": parse_blocks(c["lines"])} for c in cards]}
    if name == "layers":
        layers = []
        for ln in inner:
            m = LIST_RE.match(ln)
            if m:
                label, _, desc = m.group(3).partition(":")
                layers.append({"label": label.strip(), "desc": desc.strip()})
        return {"type": "layers", "layers": layers}
    if name in ("callout", "notes", "source"):
        return {"type": name, "blocks": parse_blocks(inner), "raw": "\n".join(inner).strip()}
    raise ValueError(f"unknown block ::: {name}")


# ---------------------------------------------------------------- file parser


PRIVATE_RE = re.compile(r"\{\{private:(\w+)\|([^}]*)\}\}")


def parse_file(path, private=None):
    """private: dict from tools/local.json. Placeholders {{private:key|Fallback}} get the
    private value (PPTX) or the public fallback (HTML, when private is None)."""
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
    chunks, cur, in_code = [], [], False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_code = not in_code
        if ln.strip() == "---" and not in_code:
            chunks.append(cur)
            cur = []
        else:
            cur.append(ln)
    chunks.append(cur)
    slides = []
    for ch in chunks:
        if not any(l.strip() for l in ch):
            continue
        sl = Slide()
        body = []
        for ln in ch:
            m = HEAD_RE.match(ln)
            if m and not sl.title and not any(b.strip() for b in body):
                sl.title = m.group(1)
                sl.classes = [c.lstrip(".") for c in (m.group(3) or "").split()]
            else:
                body.append(ln)
        for b in parse_blocks(body):
            if b["type"] == "notes":
                sl.notes = b["raw"]
            elif b["type"] == "source":
                sl.source = b["blocks"]
            else:
                sl.blocks.append(b)
        slides.append(sl)
    return Deck(meta=meta, slides=slides, path=path)


# ---------------------------------------------------------------- measuring

_fonts = {}


def font(bold=False, mono=False):
    key = (bold, mono)
    if key not in _fonts:
        f = theme.MEASURE_MONO if mono else (theme.MEASURE_BOLD if bold else theme.MEASURE_REGULAR)
        _fonts[key] = ImageFont.truetype(f, 100)
    return _fonts[key]


def text_width(runs, size):
    w = 0.0
    for t, st in runs:
        w += font(st.get("b", False), st.get("code", False)).getlength(t) * size / 100
    return w


def wrap_lines(text, size, width_pt, bold=False):
    """Number of lines `text` (inline Markdown) needs at `size` pt in `width_pt`."""
    words = plain(text).split()
    if not words:
        return 1
    f = font(bold)
    space = f.getlength(" ") * size / 100
    lines, cur = 1, 0.0
    for w in words:
        wl = f.getlength(w) * size / 100
        if cur and cur + space + wl > width_pt:
            lines += 1
            cur = wl
        else:
            cur = cur + space + wl if cur else wl
    return lines


def lh(size):
    return size * theme.LINE_HEIGHT


# ---------------------------------------------------------------- layout
# Coordinates in points; slide origin top-left. Elements: dict(kind, x, y, w, h, ...).


def measure(block, w, base, place=None, x=0, y=0):
    """Return height (pt) of block at width w; if place is a list, append positioned elements."""
    t = block["type"]
    if t == "para":
        h = wrap_lines(block["text"], base, w) * lh(base)
        if place is not None:
            place.append(dict(kind="text", x=x, y=y, w=w, h=h, size=base, paras=[{"text": block["text"]}]))
        return h
    if t == "list":
        h, paras = 0, []
        start = next((it["num"] for it in block["items"] if it["ordered"]), 1)  # e.g. list continued after a code block
        for it in block["items"]:
            size = base if it["level"] == 0 else base - 2
            ind = theme.BULLET_INDENT * (it["level"] + 1)
            ih = wrap_lines(it["text"], size, w - ind) * lh(size)
            sp = size * theme.ITEM_SPACING
            paras.append({"text": it["text"], "level": it["level"], "ordered": it["ordered"], "start": start, "num": it.get("num"),
                          "size": size, "space": sp})
            h += ih + sp
        h -= paras[-1]["space"] if paras else 0
        if place is not None:
            place.append(dict(kind="text", x=x, y=y, w=w, h=h, size=base, paras=paras))
        return h
    if t == "table":
        size = max(base - 4, theme.MIN_SIZE)
        ncol = len(block["header"])
        allrows = [block["header"]] + block["rows"]
        pad = theme.CELL_PAD
        cw = column_widths(allrows, ncol, size, w, pad)
        rh = []
        for ri, r in enumerate(allrows):
            n = max(wrap_lines(r[c] if c < len(r) else "", size, cw[c] - 2 * pad, bold=(ri == 0)) for c in range(ncol))
            rh.append(n * lh(size) + 2 * pad)
        h = sum(rh)
        if place is not None:
            place.append(dict(kind="table", x=x, y=y, w=w, h=h, size=size, colw=cw, rowh=rh, block=block))
        return h
    if t == "code":
        size = max(base - 4, theme.MIN_SIZE)
        lines = block["text"].splitlines() or [""]
        longest = max(font(mono=True).getlength(ln) for ln in lines) / 100  # width per pt of font size
        while size > theme.MIN_SIZE and longest * size > w - 2 * theme.BOX_PAD:
            size -= 1  # shrink the code only, not the whole slide
        block["too_wide"] = longest * size > w - 2 * theme.BOX_PAD
        n = len(lines)
        h = n * lh(size) + 2 * theme.BOX_PAD
        if place is not None:
            place.append(dict(kind="code", x=x, y=y, w=w, h=h, size=size, text=block["text"]))
        return h
    if t == "callout":
        inner_w = w - 2 * theme.BOX_PAD - theme.CALLOUT_BAR
        inner = []
        hh = stack(block["blocks"], inner_w, base, inner, x + theme.CALLOUT_BAR + theme.BOX_PAD, y + theme.BOX_PAD)
        h = hh + 2 * theme.BOX_PAD
        if place is not None:
            place.append(dict(kind="callout", x=x, y=y, w=w, h=h))
            place.extend(inner)
        return h
    if t == "cards":
        cards = block["cards"]
        n = len(cards)
        cols = n if n <= 3 else (2 if n == 4 else 3)
        gap = theme.GAP
        cwid = (w - gap * (cols - 1)) / cols
        tsize, bsize = base - 1, base - 3
        heights = []
        for c in cards:
            th = wrap_lines(c["title"], tsize, cwid - 2 * theme.BOX_PAD, bold=True) * lh(tsize)
            bh = stack(c["blocks"], cwid - 2 * theme.BOX_PAD, bsize, None, 0, 0)
            heights.append(th + (theme.TITLE_GAP + bh if c["blocks"] else 0) + 2 * theme.BOX_PAD)
        rows = [heights[i:i + cols] for i in range(0, n, cols)]
        rowh = [max(r) for r in rows]
        h = sum(rowh) + gap * (len(rows) - 1)
        if place is not None:
            for i, c in enumerate(cards):
                r, k = divmod(i, cols)
                cx, cy = x + k * (cwid + gap), y + sum(rowh[:r]) + gap * r
                place.append(dict(kind="card", x=cx, y=cy, w=cwid, h=rowh[r]))
                th = wrap_lines(c["title"], tsize, cwid - 2 * theme.BOX_PAD, bold=True) * lh(tsize)
                place.append(dict(kind="text", x=cx + theme.BOX_PAD, y=cy + theme.BOX_PAD, w=cwid - 2 * theme.BOX_PAD,
                                  h=th, size=tsize, paras=[{"text": c["title"], "bold": True, "color": "primary"}]))
                stack(c["blocks"], cwid - 2 * theme.BOX_PAD, bsize, place, cx + theme.BOX_PAD,
                      cy + theme.BOX_PAD + th + theme.TITLE_GAP)
        return h
    if t == "layers":
        size = base - 2
        lw = w * 0.28
        dw = w - lw
        hs = []
        for L in block["layers"]:
            n = max(wrap_lines(L["label"], size, lw - 2 * theme.BOX_PAD, bold=True),
                    wrap_lines(L["desc"], size, dw - 2 * theme.BOX_PAD) if L["desc"] else 1)
            hs.append(n * lh(size) + 2 * theme.BOX_PAD)
        h = sum(hs) + theme.LAYER_GAP * (len(hs) - 1)
        if place is not None:
            cy = y
            for i, (L, lhgt) in enumerate(zip(block["layers"], hs)):
                place.append(dict(kind="layer", x=x, y=cy, w=w, h=lhgt, lw=lw, size=size, index=i,
                                  count=len(hs), label=L["label"], desc=L["desc"]))
                cy += lhgt + theme.LAYER_GAP
        return h
    if t == "columns":
        n = len(block["cols"])
        gap = theme.GAP * 1.5
        cwid = (w - gap * (n - 1)) / n
        hs = []
        for k, col in enumerate(block["cols"]):
            hs.append(stack(col, cwid, base, place, x + k * (cwid + gap), y))
        return max(hs) if hs else 0
    if t == "image":
        frac = float(block["attrs"].get("width", "60%").rstrip("%")) / 100
        iw = w * frac
        try:
            with Image.open(block["abs"]) as im:
                ratio = im.height / im.width
        except Exception:
            ratio = 0.5
        h = iw * ratio
        if place is not None:
            place.append(dict(kind="image", x=x + (w - iw) / 2, y=y, w=iw, h=h, src=block["abs"], alt=block["alt"]))
        return h
    raise ValueError(f"cannot lay out {t}")


def column_widths(rows, ncol, size, w, pad):
    """Natural (unwrapped) widths, shrinking the widest columns first when they don't fit."""
    nat = []
    for c in range(ncol):
        cells = [(r[c] if c < len(r) else "", ri == 0) for ri, r in enumerate(rows)]
        nat.append(max(text_width(inline_runs(t, {"b": hd}), size) for t, hd in cells) + 2 * pad + 2)
    if sum(nat) <= w:
        extra = w - sum(nat)
        return [n + extra * n / sum(nat) for n in nat]
    fixed, free = {}, set(range(ncol))
    while True:
        rest = w - sum(fixed.values())
        share = rest / len(free)
        small = {c for c in free if nat[c] <= share}
        if not small:
            break
        for c in small:
            fixed[c] = nat[c]
        free -= small
        if not free:
            break
    rest = w - sum(fixed.values())
    tot = sum(nat[c] for c in free) or 1
    return [fixed[c] if c in fixed else rest * nat[c] / tot for c in range(ncol)]


def stack(blocks, w, base, place, x, y):
    """Lay out blocks vertically; return total height."""
    h = 0
    for i, b in enumerate(blocks):
        if i:
            h += base * theme.BLOCK_GAP
        h += measure(b, w, base, place, x, y + h)
    return h


def layout_slide(sl):
    """Choose the largest base size at which the slide body fits; fill sl.layout."""
    if "title" in sl.classes or "section" in sl.classes:
        return
    sizes = theme.REF_SIZES if "references" in sl.classes else theme.BASE_SIZES
    bx, by, bw, bh = theme.BODY
    src_h = 0
    if sl.source:
        src_h = stack(sl.source, bw, theme.SOURCE_SIZE, None, 0, 0) + theme.SOURCE_GAP
    avail = bh - src_h
    for size in sizes:
        h = stack(sl.blocks, bw, size, None, bx, by)
        if h <= avail:
            break
    else:
        sl.warnings.append(f"content overflows by {h - avail:.0f} pt even at {size} pt")
    if any(b.get("too_wide") for b in sl.blocks):
        sl.warnings.append("code line too wide even at minimum size - break the line")
    sl.base = size
    sl.layout = []
    stack(sl.blocks, bw, size, sl.layout, bx, by)
    if sl.source:
        sy = by + bh - src_h + theme.SOURCE_GAP
        stack(sl.source, bw, theme.SOURCE_SIZE, sl.layout, bx, sy)
        for el in sl.layout[-len(sl.source):]:
            el["muted"] = True


def load_deck(path, private=None):
    deck = parse_file(path, private)
    for sl in deck.slides:
        _resolve_images(sl.blocks, deck.path.parent)
        layout_slide(sl)
    return deck


def _resolve_images(blocks, base_dir):
    for b in blocks:
        if b["type"] == "image":
            b["abs"] = str((base_dir / b["src"]).resolve())
        elif b["type"] == "columns":
            for c in b["cols"]:
                _resolve_images(c, base_dir)
        elif b["type"] in ("callout",):
            _resolve_images(b["blocks"], base_dir)
        elif b["type"] == "cards":
            for c in b["cards"]:
                _resolve_images(c["blocks"], base_dir)
