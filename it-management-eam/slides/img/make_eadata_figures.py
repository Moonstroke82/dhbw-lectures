"""Draw the figures for session 11 (collecting and modelling architecture information).

- eam-metamodel.png: a lean EA meta-model with element types and relationships across the four domains.
  Own illustration based on Hanschke (2023) and The Open Group (2022); the selection of element types,
  the relationship names and the layout are our own and do not reproduce a figure from these sources.
- eam-collection-steps.png: the steps of an EA data collection as a cycle.
  Own illustration based on Hanschke (2023) and Roth et al. (2013).

Run from the Lectures folder: python it-management-eam/slides/img/make_eadata_figures.py
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
LIGHT, BORDER, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"], "#" + theme.COLORS["muted"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc="white", ec=GREY, tc=TEXT, size=12, bold=False, lw=1.8, pad=1.2, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={pad}", fc=fc, ec=ec, lw=lw,
                                ls=ls))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=tc,
            weight="bold" if bold else "normal", linespacing=1.2)


def arrow(ax, a, b, color=RED, lw=1.8, style="-|>", scale=14, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def label(ax, x, y, text, size=10.5, color=MUTED, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=size, color=color, style="italic",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none"))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def metamodel():
    """Lean meta-model: element types (boxes) and relationship types (arrows) in four domain bands."""
    fig, ax = canvas(12, 6)
    bands = [("Business", 45), ("Data", 31.5), ("Application", 18), ("Technology", 4.5)]
    bh = 11
    for name, y in bands:
        ax.add_patch(FancyBboxPatch((0, y), 120, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=LIGHT, ec=BORDER, lw=1.2))
        ax.add_patch(FancyBboxPatch((0, y), 15, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=GREY, ec=GREY, lw=1.2))
        ax.text(7.5, y + bh / 2, name, ha="center", va="center", fontsize=12, color="white", weight="bold")
    yB, yD, yA, yT = (b[1] for b in bands)
    w, h = 23, 6.4
    dy = (bh - h) / 2
    pos = {
        "org": (18.5, yB + dy), "proc": (54, yB + dy), "cap": (92, yB + dy),
        "bo": (54, yD + dy),
        "app": (34, yA + dy), "if": (72, yA + dy),
        "tech": (36, yT + dy),
    }
    names = {
        "org": "Organisation unit", "proc": "Business process", "cap": "Business capability",
        "bo": "Business object", "app": "Application", "if": "Interface", "tech": "Technology component",
    }
    for k, (x, y) in pos.items():
        box(ax, x, y, w, h, names[k], size=11.5, bold=k == "app", ec=RED if k == "app" else GREY,
            lw=2.4 if k == "app" else 1.8)

    def top(k, f=0.5):
        x, y = pos[k]
        return (x + w * f, y + h)

    def bottom(k, f=0.5):
        x, y = pos[k]
        return (x + w * f, y)

    def left(k, f=0.5):
        x, y = pos[k]
        return (x, y + h * f)

    def right(k, f=0.5):
        x, y = pos[k]
        return (x + w, y + h * f)

    # business band
    arrow(ax, right("org"), left("proc"), color=GREY)
    label(ax, (pos["org"][0] + w + pos["proc"][0]) / 2, pos["org"][1] + h + 1.6, "performs")
    arrow(ax, right("proc"), left("cap"), color=GREY)
    label(ax, (pos["proc"][0] + w + pos["cap"][0]) / 2, pos["proc"][1] + h + 1.6, "realises")
    # application supports process
    arrow(ax, top("app", 0.55), bottom("proc", 0.2), rad=-0.05)
    label(ax, 41, yD + bh / 2 + 1.2, "supports")
    # org unit owns application
    arrow(ax, bottom("org", 0.5), left("app", 0.75), color=GREY, rad=0.25)
    label(ax, 23, yD + bh / 2 - 1.5, "is owner of")
    # application uses business object
    arrow(ax, top("app", 0.85), bottom("bo", 0.3), rad=-0.1)
    label(ax, 59, yA + bh + 1.2, "creates / reads")
    # interface connects applications and transfers business objects
    arrow(ax, left("if"), right("app"), style="<|-|>", color=GREY)
    label(ax, (pos["app"][0] + w + pos["if"][0]) / 2, pos["app"][1] - 1.3, "connects")
    arrow(ax, top("if", 0.5), bottom("bo", 0.85), rad=0.1)
    label(ax, 88, yD - 1.2, "transfers")
    # application runs on technology component
    arrow(ax, top("tech"), bottom("app"))
    label(ax, pos["app"][0] + w / 2 + 6.5, yT + bh + 1.2, "runs on")
    # attribute note
    ax.text(98, yD + bh / 2, "Each element type has attributes,\ne.g. Application: owner, life cycle,\ncriticality, cost",
            ha="center", va="center", fontsize=10.5, color=TEXT, linespacing=1.2)
    ax.text(98, yT + bh / 2, "Arrow = relationship type\nBox = element type",
            ha="center", va="center", fontsize=10.5, color=MUTED, linespacing=1.2)
    save(fig, "eam-metamodel.png")


def collection_steps():
    """Seven steps of an EA data collection, the last one feeding back into the first."""
    fig, ax = canvas(13, 2.5)
    steps = [
        "1 Purpose and\nquestions",
        "2 Meta-model\nand granularity",
        "3 Sources and\ndata owners",
        "4 Collect,\nexisting data first",
        "5 Consolidate\nand check quality",
        "6 Publish views\nand use them",
        "7 Maintain\ncontinuously",
    ]
    n = len(steps)
    w, h, gap = 16.2, 10, 2.2
    x0, y = 1, 13
    for i, s in enumerate(steps):
        x = x0 + i * (w + gap)
        hl = i in (0, 6)
        box(ax, x, y, w, h, s, size=10.5, fc=GREY if hl else "white", tc="white" if hl else TEXT,
            ec=GREY, bold=hl)
        if i < n - 1:
            arrow(ax, (x + w + 0.2, y + h / 2), (x + w + gap - 0.2, y + h / 2), color=RED)
    # feedback loop
    xl = x0 + (n - 1) * (w + gap) + w / 2
    xf = x0 + w / 2
    arrow(ax, (xl, y - 0.3), (xf, y - 0.3), color=RED, rad=-0.09)
    ax.text((xl + xf) / 2, 4.6, "Feedback: new questions and changes in the landscape",
            ha="center", va="center", fontsize=11, color=MUTED, style="italic")
    save(fig, "eam-collection-steps.png")


if __name__ == "__main__":
    metamodel()
    collection_steps()
