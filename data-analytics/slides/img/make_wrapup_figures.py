"""Draw the figure for session 17 (portfolio presentations and wrap-up).

Run from the Lectures folder: python data-analytics/slides/img/make_wrapup_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

- wu-course-map.png: the four parts of the course, the questions they answer
  and how they lead to a decision and to the semester-6 project. Own
  illustration based on Kimball and Ross (2013), Chapman et al. (2000),
  Kohavi et al. (2020), Hyndman and Athanasopoulos (2021) and Zaharia et al. (2016).
"""
import logging
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
MUTED = "#" + theme.COLORS["muted"]
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # quiet Arial fallback
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, title, sub, colour=GREY, dashed=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.4,rounding_size=2",
                                fc="white", ec=colour, lw=2, ls="--" if dashed else "-"))
    ax.text(x, y + h / 2 - 5, title, ha="center", va="center", fontsize=11.5, color=TEXT, weight="bold")
    ax.text(x, y - 2.6, sub, ha="center", va="center", fontsize=10.5, color=MUTED, linespacing=1.35)


def arrow(ax, a, b, colour=GREY):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, lw=2, color=colour,
                                 shrinkA=0, shrinkB=0))


def course_map():
    fig, ax = plt.subplots(figsize=(11, 4.9))
    ax.set_xlim(0, 182)
    ax.set_ylim(0, 80)
    ax.axis("off")
    w, h, top = 40, 26, 62
    xs = [22, 68, 114, 160]
    parts = [
        ("A · What happened?", "Sessions 2–6\nwarehouse, grain, SQL,\ncharts, portal"),
        ("B · Who? Does it work?", "Sessions 7–9\nframing, leakage, baseline,\nlift, experiment"),
        ("C · What comes next?", "Sessions 11–14\ndecomposition, forecasts,\nintervals, many series"),
        ("D · At what scale?", "Sessions 15–17\nSpark or DuckDB,\ncase study"),
    ]
    for x, (t, s) in zip(xs, parts):
        box(ax, x, top, w, h, t, s)
    dec_x, dec_y = 68, 13
    box(ax, dec_x, dec_y, 58, 18, "Decision", "what we do — and how sure we are", colour=RED)
    for x in xs:
        arrow(ax, (x, top - h / 2 - 0.6), (dec_x + (x - dec_x) * 0.3, dec_y + 9 + 0.6), RED)
    box(ax, 148, dec_y, 52, 18, "Semester 6", "project with a partner company", dashed=True)
    arrow(ax, (dec_x + 29 + 0.6, dec_y), (148 - 26 - 0.6, dec_y))
    save(fig, "wu-course-map.png")


if __name__ == "__main__":
    course_map()
