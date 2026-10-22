"""Draw the figure for session 16 (case study workshop).

Run from the Lectures folder: python data-analytics/slides/img/make_casestudy_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

- cs-review-path.png: the stages of the group case study, the sessions that
  supply the methods, and the review checklist of session 16 that checks each
  stage. Own illustration based on Chapman et al. (2000) and Few (2013).
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
LIGHT = "#" + theme.COLORS["light"]
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # quiet Arial fallback
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]

W, H = 27, 18  # box size in axis units


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def node(ax, x, y, title, sub, colour=GREY):
    ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.4,rounding_size=2",
                                fc="white", ec=colour, lw=2))
    ax.text(x, y + 3.6, title, ha="center", va="center", fontsize=12, color=TEXT, weight="bold")
    ax.text(x, y - 3.0, sub, ha="center", va="center", fontsize=9.3, color=MUTED)


def arrow(ax, a, b, colour=GREY):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=14, lw=1.8, color=colour,
                                 shrinkA=0, shrinkB=0))


def bracket(ax, x0, x1, y, label, colour=GREY):
    """A labelled bar under the stages that one checklist reviews."""
    ax.add_patch(FancyBboxPatch((x0, y - 3.2), x1 - x0, 6.4, boxstyle="round,pad=0.2,rounding_size=1.5",
                                fc=LIGHT, ec=colour, lw=1.4))
    ax.text((x0 + x1) / 2, y, label, ha="center", va="center", fontsize=10.5, color=colour, weight="bold")


def review_path():
    fig, ax = plt.subplots(figsize=(11.5, 3.9))
    ax.set_xlim(0, 186)
    ax.set_ylim(0, 50)
    ax.axis("off")
    y = 38
    xs = [14.5, 45.9, 77.3, 108.7, 140.1, 171.5]
    stages = [
        ("Question", "decision, user,\nsuccess metric\n(S1, S7)"),
        ("Data", "source, licence,\ngrain, gaps\n(S2–3, S11)"),
        ("Approach", "method, baseline,\nevaluation design\n(S7–9, S12–14)"),
        ("Results", "vs. baseline,\nuncertainty, limits\n(S8, S12–13)"),
        ("Dashboard or\nbig data", "one screen, or a\nmeasured choice\n(S5–6, S15)"),
        ("Presentation", "answer first,\nevidence, decision\n(S5, S17)"),
    ]
    for x, (title, sub) in zip(xs, stages):
        colour = RED if title == "Presentation" else GREY
        if "\n" in title:
            ax.add_patch(FancyBboxPatch((x - W / 2, y - H / 2), W, H, boxstyle="round,pad=0.4,rounding_size=2",
                                        fc="white", ec=colour, lw=2))
            ax.text(x, y + 4.6, title, ha="center", va="center", fontsize=11, color=TEXT, weight="bold",
                    linespacing=1.0)
            ax.text(x, y - 3.9, sub, ha="center", va="center", fontsize=9.3, color=MUTED)
        else:
            node(ax, x, y, title, sub, colour)
    for i in range(len(xs) - 1):
        arrow(ax, (xs[i] + W / 2 + 0.7, y), (xs[i + 1] - W / 2 - 0.7, y))
    yb = 17
    bracket(ax, xs[0] - W / 2, xs[2] + W / 2, yb, "Approach")
    bracket(ax, xs[3] - W / 2, xs[3] + W / 2, yb, "Results")
    bracket(ax, xs[4] - W / 2, xs[4] + W / 2, yb, "Dashboard")
    bracket(ax, xs[5] - W / 2, xs[5] + W / 2, yb, "Storyline", RED)
    bracket(ax, xs[0] - W / 2, xs[5] + W / 2, 5, "Reproducible team notebook — checked across all stages")
    save(fig, "cs-review-path.png")


if __name__ == "__main__":
    review_path()
