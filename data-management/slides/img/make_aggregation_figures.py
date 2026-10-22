"""Draw the GROUP BY figure for session 10.

Run from the Lectures folder: python data-management/slides/img/make_aggregation_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
The rows are an extract of the course sample data (bikeshop-data.sql, repair_line
for jobs 502, 504 and 511); the sums were checked in SQLite 3.45.1.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

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


def grid(ax, x, ytop, title, cols, widths, rows, shade=(), subtitle=None):
    """Draw a small table. shade: indices of rows drawn with the light background."""
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
            fc = LIGHT if i in shade else "white"
            ax.add_patch(Rectangle((cx, y), w, RH, fc=fc, ec=GREY, lw=1.0))
            ax.text(cx + w / 2, y + RH / 2, v, ha="center", va="center", fontsize=9.5, color=TEXT)
            cx += w


def group_by():
    """repair_line rows of three jobs, grouped by job_no, and the aggregated result."""
    fig, ax = canvas(14, 6.2)
    rows = [["502", "P-103", "1", "12.5", "12.5"],
            ["502", "P-106", "2", "4.5", "9.0"],
            ["504", "P-103", "2", "12.5", "25.0"],
            ["504", "P-107", "1", "4.5", "4.5"],
            ["511", "P-105", "1", "39.9", "39.9"],
            ["511", "P-108", "1", "59.0", "59.0"],
            ["511", "P-106", "1", "4.5", "4.5"]]
    top = 56
    grid(ax, 2, top, "REPAIR_LINE (extract)", ["job_no", "part_no", "quantity", "price_charged", "line_total"],
         [11, 12, 12, 17, 14], rows, shade=(2, 3), subtitle="7 rows")
    # group brackets
    groups = [(0, 2, "group 502"), (2, 4, "group 504"), (4, 7, "group 511")]
    for a, b, label in groups:
        y1 = top - RH * (a + 1) - 0.4
        y0 = top - RH * (b + 1) + 0.4
        ax.plot([70, 71.5, 71.5, 70], [y1, y1, y0, y0], color=RED, lw=1.6)
        ax.text(73, (y0 + y1) / 2, label, ha="left", va="center", fontsize=9.5, color=RED, weight="bold")
    # arrow
    ax.add_patch(FancyArrowPatch((86, 40), (100, 40), arrowstyle="-|>", mutation_scale=18, color=GREY, lw=1.6))
    ax.text(93, 44.5, "one row\nper group", ha="center", va="bottom", fontsize=9.5, color=MUTED, style="italic")
    # result
    grid(ax, 103, 50, "RESULT", ["job_no", "lines", "revenue"], [11, 10, 13],
         [["502", "2", "21.5"], ["504", "2", "29.5"], ["511", "3", "103.4"]], shade=(1,), subtitle="3 rows")
    ax.text(2, 13, "SELECT job_no, count(*) AS lines, sum(quantity * price_charged) AS revenue\n"
                   "FROM repair_line WHERE job_no IN (502, 504, 511) GROUP BY job_no;",
            ha="left", va="center", fontsize=9.5, color=TEXT, family="DejaVu Sans Mono", linespacing=1.5)
    save(fig, "groupby-groups.png")


if __name__ == "__main__":
    group_by()
