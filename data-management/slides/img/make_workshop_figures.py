"""Draw the review map for session 12 (project workshop and catch-up).

Run from the Lectures folder: python data-management/slides/img/make_workshop_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
The map summarises sessions 3-11 and the milestones of the design project (session 4).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, fc="white", ec=GREY, lw=1.3, r=1.2, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, linestyle=ls))


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.4, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=12,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0,
                                 connectionstyle=f"arc3,rad={rad}"))


def stage(ax, x, y, sessions, title, detail, w=30, h=17, fc=LIGHT, ec=GREY, ls="-"):
    box(ax, x, y, w, h, fc=fc, ec=ec, ls=ls)
    ax.text(x + w / 2, y + h - 3.2, sessions, ha="center", va="center", fontsize=8.5,
            color=MUTED)
    ax.text(x + w / 2, y + h - 7.6, title, ha="center", va="center", fontsize=10.5,
            weight="bold", color=TEXT)
    ax.text(x + w / 2, y + 4.4, detail, ha="center", va="center", fontsize=8.5, color=TEXT,
            linespacing=1.15)


def milestone(ax, x, y, label):
    box(ax, x - 7, y - 2.6, 14, 5.2, fc=RED, ec=RED, r=1.0)
    ax.text(x, y, label, ha="center", va="center", fontsize=8.5, weight="bold", color="white")


def review_map():
    """From a business case to answered business questions: Parts A and B with the milestones."""
    fig, ax = canvas(18, 7.2)
    W, H, GAP = 30, 17, 7
    xs = [4 + i * (W + GAP) for i in range(4)]
    ya, yb = 46, 9
    # part labels
    ax.text(4, ya + H + 5, "Part A  ·  Foundations: from case to schema", fontsize=11,
            weight="bold", color=TEXT, va="center")
    ax.text(4, yb + H + 4.5, "Part B  ·  SQL and databases: from schema to answers", fontsize=11,
            weight="bold", color=TEXT, va="center")
    part_a = [("Sessions 1–2", "Business case", "data, information,\ntypes of data"),
              ("Sessions 3–4", "ER model", "entities, relationships,\ncardinalities, weak, ISA"),
              ("Session 5", "Relational schema", "keys, foreign keys,\nmapping rules"),
              ("Session 6", "Normalised schema", "FDs, 1NF–3NF, BCNF,\nno anomalies")]
    part_b = [("Session 7", "Tables in SQLite", "CREATE TABLE, types,\nconstraints"),
              ("Session 8", "Data and queries", "INSERT, UPDATE, DELETE,\nSELECT, NULL"),
              ("Session 9", "Joins", "inner, outer, self,\njoin pitfalls"),
              ("Session 10", "Business answers", "GROUP BY, subqueries,\nviews, transactions")]
    for x, (s, t, d) in zip(xs, part_a):
        stage(ax, x, ya, s, t, d)
    for x, (s, t, d) in zip(xs, part_b):
        stage(ax, x, yb, s, t, d)
    for i in range(3):
        arrow(ax, xs[i] + W, ya + H / 2, xs[i + 1], ya + H / 2)
        arrow(ax, xs[i] + W, yb + H / 2, xs[i + 1], yb + H / 2)
    # from normalised schema down to SQL
    ye = 36.5
    ax.plot([xs[3] + W / 2 - 6, xs[3] + W / 2 - 6, 1, 1], [ya, ye, ye, yb + H / 2],
            color=GREY, lw=1.4)
    arrow(ax, 1, yb + H / 2, xs[0], yb + H / 2)
    # NoSQL side branch
    xn = xs[3] + W + 6
    stage(ax, xn, 26, "Session 11", "Other data stores?", "key-value, document,\ncolumn, graph",
          w=26, fc="white", ec=MUTED, ls="--")
    arrow(ax, xs[3] + W, ya + H / 2, xn + 13, 26 + H, color=MUTED, ls="--", rad=-0.25)
    arrow(ax, xs[3] + W, yb + H / 2, xn + 13, 26, color=MUTED, ls="--", rad=0.25)
    # milestones
    milestone(ax, xs[1] + W / 2, ya - 3.6, "M1 · after 6")
    milestone(ax, xs[3] + W / 2 + 7, ya - 3.6, "M2 · after 7")
    milestone(ax, xs[3] + W / 2, yb - 4.0, "M3 · after 12")
    save(fig, "workshop-parts-ab-map.png")


if __name__ == "__main__":
    review_map()
