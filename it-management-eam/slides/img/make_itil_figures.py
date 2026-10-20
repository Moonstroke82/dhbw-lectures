"""Draw the ITIL 4 figures for session 5 (service value system, service value chain).

Own illustrations based on AXELOS (2019), ITIL Foundation: ITIL 4 edition. The layout is
deliberately our own and does not reproduce the AXELOS figures.

Run from the Lectures folder: python it-management-eam/slides/img/make_itil_figures.py
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


def arrow(ax, a, b, color=RED, lw=2.2, style="-|>", scale=18):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def svs():
    """Service value system: demand in, value out; five components as horizontal bands."""
    fig, ax = canvas(12, 4.6)
    box(ax, 0, 15, 16, 16, "Opportunity\nand demand", fc=LIGHT, size=12, bold=True)
    box(ax, 104, 15, 16, 16, "Value", fc=RED, ec=RED, tc="white", size=14, bold=True)
    # frame of the SVS
    ax.add_patch(FancyBboxPatch((22, 1), 76, 44, boxstyle="round,pad=0,rounding_size=2", fc="white", ec=GREY, lw=2.2))
    ax.text(60, 41.5, "Service value system", ha="center", va="center", fontsize=13, weight="bold", color=GREY)
    bands = [(33, "Guiding principles"), (27.5, "Governance")]
    for y, lab in bands:
        box(ax, 26, y, 68, 4.4, lab, fc=LIGHT, ec=BORDER, size=11, lw=1.2, pad=0.8)
    box(ax, 26, 16, 68, 10, "Service value chain\n(six value chain activities, combined into value streams)",
        fc="white", ec=RED, size=11.5, bold=False, lw=2.2)
    for y, lab in [(10.5, "Practices (34 sets of organisational resources)"), (5, "Continual improvement")]:
        box(ax, 26, y, 68, 4.4, lab, fc=LIGHT, ec=BORDER, size=11, lw=1.2, pad=0.8)
    arrow(ax, (16.5, 23), (25.5, 21))
    arrow(ax, (94.5, 21), (103.5, 23))
    save(fig, "itil-svs.png")


def svc():
    """Service value chain: engage as the interface, three delivery activities, plan and improve across."""
    fig, ax = canvas(12, 4.6)
    box(ax, 0, 25, 13, 10, "Demand", fc=LIGHT, size=12, bold=True)
    box(ax, 0, 9, 13, 10, "Value", fc=RED, ec=RED, tc="white", size=12, bold=True)
    box(ax, 18, 6, 18, 32, "Engage", fc="white", ec=RED, size=13, bold=True, lw=2.2)
    box(ax, 41, 38, 79, 7, "Plan: shared vision, direction and priorities for all activities",
        fc=LIGHT, ec=BORDER, size=11.5, lw=1.2)
    box(ax, 41, 0, 79, 7, "Improve: continual improvement of products, services and practices",
        fc=LIGHT, ec=BORDER, size=11.5, lw=1.2)
    mids = [(41, "Design and\ntransition"), (69, "Obtain/build"), (97, "Deliver and\nsupport")]
    for x, lab in mids:
        box(ax, x, 14, 23, 16, lab, fc="white", ec=GREY, size=12.5, bold=True, lw=2)
    arrow(ax, (13.5, 30), (17.5, 30))
    arrow(ax, (17.5, 14), (13.5, 14))
    for x0, x1 in [(36.5, 40.5), (64.5, 68.5), (92.5, 96.5)]:
        arrow(ax, (x0, 22), (x1, 22), color=GREY, lw=1.8, scale=14)
    ax.text(80.5, 33.5, "Value streams combine the activities in different orders",
            ha="center", va="center", fontsize=10.5, style="italic", color=GREY)
    save(fig, "itil-svc.png")


if __name__ == "__main__":
    svs()
    svc()
