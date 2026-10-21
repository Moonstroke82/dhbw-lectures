"""Draw the figure for session 9 (ISO 9001 clauses 4-10 arranged in the plan-do-check-act cycle).

Own illustration based on the clause structure of ISO 9001 (ISO, 2015, 2026b). The layout is our own and
does not reproduce the figure in the standard.

Run from the Lectures folder: python it-management-eam/slides/img/make_quality_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
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
LIGHT, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(-1, w * 10 + 1)
    ax.set_ylim(-1, h * 10 + 1)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc="white", ec=GREY, tc=TEXT, size=12, bold=False, lw=1.8, pad=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={pad}", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=tc,
            weight="bold" if bold else "normal", linespacing=1.25)


def arrow(ax, a, b, color=RED, lw=2.2, style="-|>", scale=18, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def pdca():
    """Clauses 4-10 of ISO 9001 in the PDCA cycle, with leadership in the centre."""
    fig, ax = canvas(12, 5)
    ax.set_xlim(-3, 123)
    # input and output
    box(ax, -2, 13, 22, 24, "Context of the\norganisation (4)\n\nneeds of\ncustomers and\nother parties",
        fc=LIGHT, ec=BORDER, size=13)
    box(ax, 100, 13, 22, 24, "Results\n\nconforming\nservices and\nproducts,\nsatisfied\ncustomers",
        fc=LIGHT, ec=BORDER, size=13)
    # cycle boxes
    w, h = 24, 13
    plan = (33, 32)
    do = (63, 32)
    check = (63, 5)
    act = (33, 5)
    box(ax, *plan, w, h, "PLAN\nPlanning (6)\nrisks, objectives", size=15, bold=False)
    box(ax, *do, w, h, "DO\nSupport (7)\nOperation (8)", size=15)
    box(ax, *check, w, h, "CHECK\nPerformance\nevaluation (9)", size=15)
    box(ax, *act, w, h, "ACT\nImprovement (10)", size=15)
    # centre
    box(ax, 48.5, 20.5, 23, 9, "Leadership (5)", fc=RED, ec=RED, tc="white", size=15, bold=True)
    # cycle arrows (clockwise)
    arrow(ax, (plan[0] + w + 0.5, plan[1] + h / 2), (do[0] - 0.5, do[1] + h / 2))
    arrow(ax, (do[0] + w / 2, do[1] - 0.5), (check[0] + w / 2, check[1] + h + 0.5))
    arrow(ax, (check[0] - 0.5, check[1] + h / 2), (act[0] + w + 0.5, act[1] + h / 2))
    arrow(ax, (act[0] + w / 2, act[1] + h + 0.5), (plan[0] + w / 2, plan[1] - 0.5))
    # input/output arrows
    arrow(ax, (20.5, 25), (32.5, 38.5), color=GREY, lw=1.8)
    arrow(ax, (87.5, 38.5), (99.5, 25), color=GREY, lw=1.8)
    save(fig, "pdca-iso9001.png")


if __name__ == "__main__":
    pdca()
