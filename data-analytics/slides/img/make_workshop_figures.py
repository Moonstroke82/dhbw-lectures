"""Draw the figure for session 10 (lab workshop and catch-up).

Run from the Lectures folder: python data-analytics/slides/img/make_workshop_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

- ws-parts-ab-map.png: how the sessions of Parts A and B connect, from the
  warehouse to a decision. Own illustration based on Kimball and Ross (2013),
  Chapman et al. (2000) and Kohavi et al. (2020).
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

W, H = 30, 15  # box size in axis units


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def node(ax, x, y, title, sub, colour=GREY):
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.4,rounding_size=2",
                                fc="white", ec=colour, lw=2))
    ax.text(x, y + 2.6, title, ha="center", va="center", fontsize=12.5, color=TEXT, weight="bold")
    ax.text(x, y - 3.2, sub, ha="center", va="center", fontsize=10.5, color=MUTED)


def arrow(ax, a, b, colour=GREY):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, lw=2, color=colour,
                                 shrinkA=0, shrinkB=0))


def parts_map():
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.set_xlim(0, 182)
    ax.set_ylim(0, 72)
    ax.axis("off")
    top, bottom = 52, 16
    xs = [18, 54, 90, 126, 162]
    # Part A (top row)
    node(ax, xs[0], top, "Warehouse", "Sessions 2–3\nlayers, star schema")
    node(ax, xs[1], top, "Analytical SQL", "Session 4\nwindows, ROLLUP")
    node(ax, xs[2], top, "Charts", "Session 5\nencoding, KPIs")
    node(ax, xs[3], top, "Portal", "Session 6\ndashboard, access")
    # Part B (bottom row)
    node(ax, xs[1], bottom, "Feature table", "Session 7\ncut-off, leakage")
    node(ax, xs[2], bottom, "Model", "Session 8\nvs. baseline, lift")
    node(ax, xs[3], bottom, "Experiment", "Session 9\neffect with interval")
    node(ax, xs[4], 34, "Decision", "What do we do,\nhow sure are we?", colour=RED)
    for i in range(3):
        arrow(ax, (xs[i] + W / 2 + 0.6, top), (xs[i + 1] - W / 2 - 0.6, top))
    for i in (1, 2):
        arrow(ax, (xs[i] + W / 2 + 0.6, bottom), (xs[i + 1] - W / 2 - 0.6, bottom))
    arrow(ax, (xs[0] + 4, top - H / 2 - 0.6), (xs[1] - W / 2 - 0.6, bottom + 2))
    arrow(ax, (xs[3] + W / 2 + 0.6, top - 2), (xs[4] - 6, 34 + H / 2 + 0.6), RED)
    arrow(ax, (xs[3] + W / 2 + 0.6, bottom + 2), (xs[4] - 6, 34 - H / 2 - 0.6), RED)
    ax.text(1, 69, "Part A · what happened?", fontsize=11.5, color=GREY, weight="bold")
    ax.text(1, 1, "Part B · what will happen, and what works?", fontsize=11.5, color=GREY, weight="bold")
    save(fig, "ws-parts-ab-map.png")


if __name__ == "__main__":
    parts_map()
