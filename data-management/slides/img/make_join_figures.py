"""Draw the join figure for session 9.

Run from the Lectures folder: python data-management/slides/img/make_join_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
The rows are a small extract of the course sample data (bikeshop-data.sql).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]

RH = 4.6  # row height


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


def grid(ax, x, ytop, title, cols, widths, rows, marks=(), subtitle=None):
    """Draw a small table. rows: list of value lists; marks: indices of rows added by an outer join."""
    ax.text(x, ytop + 3.2, title, ha="left", va="center", fontsize=11.5, weight="bold", color=TEXT)
    if subtitle:
        ax.text(x + sum(widths), ytop + 3.2, subtitle, ha="right", va="center", fontsize=9.5,
                color=MUTED, style="italic")
    cx = x
    for c, w in zip(cols, widths):
        ax.add_patch(Rectangle((cx, ytop - RH), w, RH, fc=GREY, ec=GREY, lw=1.2))
        ax.text(cx + w / 2, ytop - RH / 2, c, ha="center", va="center", fontsize=9.5, color="white",
                weight="bold")
        cx += w
    for i, r in enumerate(rows):
        y = ytop - RH * (i + 2)
        cx = x
        for v, w in zip(r, widths):
            fc = LIGHT if i in marks else "white"
            ax.add_patch(Rectangle((cx, y), w, RH, fc=fc, ec=GREY, lw=1.0))
            isnull = v == "NULL"
            ax.text(cx + w / 2, y + RH / 2, v, ha="center", va="center", fontsize=9.5,
                    color=RED if isnull else TEXT, weight="bold" if isnull else "normal")
            cx += w


def join_types():
    """CUSTOMER and BIKE (extract) and the results of the four join types."""
    fig, ax = canvas(14, 6.6)
    # input tables
    grid(ax, 2, 62, "CUSTOMER", ["customer_no", "name"], [17, 19],
         [["101", "Anna Berger"], ["106", "Felix Wagner"], ["107", "Hannah Schulz"]])
    grid(ax, 2, 34, "BIKE", ["frame_no", "customer_no"], [15, 17],
         [["WAX123", "101"], ["CUB202", "107"], ["GZT884", "NULL"]])
    ax.text(2, 8, "FROM customer … JOIN bike\n  ON bike.customer_no\n   = customer.customer_no",
            ha="left", va="center", fontsize=9.5, color=TEXT, family="DejaVu Sans Mono", linespacing=1.4)
    ax.plot([45, 45], [4, 66], color=MUTED, lw=1.0, ls=(0, (3, 3)))

    cols, widths = ["name", "frame_no"], [19, 15]
    a = ["Anna Berger", "WAX123"]
    h = ["Hannah Schulz", "CUB202"]
    felix = ["Felix Wagner", "NULL"]
    stock = ["NULL", "GZT884"]
    x1, x2 = 52, 96
    grid(ax, x1, 62, "INNER JOIN", cols, widths, [a, h], subtitle="2 rows")
    grid(ax, x2, 62, "LEFT JOIN", cols, widths, [a, felix, h], marks=(1,), subtitle="3 rows")
    grid(ax, x1, 30, "RIGHT JOIN", cols, widths, [a, h, stock], marks=(2,), subtitle="3 rows")
    grid(ax, x2, 30, "FULL JOIN", cols, widths, [a, felix, h, stock], marks=(1, 3), subtitle="4 rows")
    ax.add_patch(Rectangle((x1, 1.5), 4, 3, fc=LIGHT, ec=GREY, lw=1.0))
    ax.text(x1 + 6, 3, "row added by the outer join: no partner, so the other side is NULL",
            ha="left", va="center", fontsize=9.5, color=TEXT)
    save(fig, "join-types.png")


if __name__ == "__main__":
    join_types()
