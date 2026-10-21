"""Draw the figures for session 12 (business model transformation and business-IT alignment).

- eam-capability-map.png: a level-1 business capability map of the fictitious Rhein-Neckar Mobil Group in
  three tiers (strategic, core, supporting), with level 2 of one capability.
- eam-capability-heatmap.png: the same map as a heat map with the lens "IT support today".
- eam-value-stream.png: the value stream "subscribe to a monthly ticket" with its stages and the
  capabilities that enable each stage.
Own illustrations based on Hanschke (2023) and The Open Group (2022); the capabilities, ratings and the
layout are our own example and do not reproduce a figure from these sources.

Run from the Lectures folder: python it-management-eam/slides/img/make_capability_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, BORDER, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"], "#" + theme.COLORS["muted"]
PINK = "#F7C6CC"  # light tint of DHBW red for "partial" in the heat map
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


def arrow(ax, a, b, color=RED, lw=1.8, style="-|>", scale=14, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, linestyle=ls))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


TIERS = [
    ("Strategic", [
        "Strategy and\nbusiness development", "Network and\ntimetable planning",
        "Partner\nmanagement", "Risk and compliance\nmanagement"]),
    ("Core", [
        "Customer\nmanagement", "Product and\nfare management", "Sales and\nticketing",
        "Vehicle sharing\nmanagement",
        "Fleet\nmaintenance", "Customer\nservice", "Payment and revenue\nmanagement",
        "Transport\noperations"]),
    ("Supporting", [
        "Financial\nmanagement", "Procurement", "Human resources\nmanagement", "IT and information\nmanagement"]),
]

# Lens "IT support today" for the heat map: 0 good, 1 partial or redundant, 2 weak
HEAT = {
    "Partner\nmanagement": 1, "Risk and compliance\nmanagement": 1,
    "Customer\nmanagement": 2, "Sales and\nticketing": 1, "Fleet\nmaintenance": 1,
    "Customer\nservice": 2, "Payment and revenue\nmanagement": 1,
    "Financial\nmanagement": 1, "Procurement": 1,
}


def capability_map(heat=False):
    """Level-1 map in three tiers; level 2 of 'Transport operations' on the right (plain version only)."""
    fig, ax = canvas(13, 5.4)
    ax.set_ylim(10, 64)
    x0, x1 = 16, 100
    cols, gap = 4, 1.6
    cw = (x1 - x0 - (cols - 1) * gap) / cols
    ch, rgap = 7.2, 1.4
    band_pad = 1.4
    y = 62
    positions = {}
    for tier, caps in TIERS:
        rows = (len(caps) + cols - 1) // cols
        bh = rows * ch + (rows - 1) * rgap + 2 * band_pad
        y -= bh
        ax.add_patch(FancyBboxPatch((0, y), x1 + 1.4, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=LIGHT, ec=BORDER, lw=1.2))
        ax.add_patch(FancyBboxPatch((0, y), 14, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=GREY, ec=GREY, lw=1.2))
        ax.text(7, y + bh / 2, tier, ha="center", va="center", fontsize=12, color="white", weight="bold")
        for i, cap in enumerate(caps):
            r, c = divmod(i, cols)
            bx = x0 + c * (cw + gap)
            by = y + bh - band_pad - (r + 1) * ch - r * rgap
            positions[cap] = (bx, by)
            if heat:
                level = HEAT.get(cap, 0)
                fc, tc, ec = [("white", TEXT, GREY), (PINK, TEXT, RED), (RED, "white", RED)][level]
                box(ax, bx, by, cw, ch, cap, fc=fc, tc=tc, ec=ec, size=10.5, bold=level == 2)
            else:
                hl = cap == "Transport\noperations"
                box(ax, bx, by, cw, ch, cap, size=10.5, ec=RED if hl else GREY, lw=2.4 if hl else 1.8, bold=hl)
        y -= 1.6
    if heat:
        lx, ly = 104, 46
        ax.text(lx, ly + 9, "Lens: IT support today", fontsize=11.5, color=TEXT, weight="bold", va="center")
        for k, (lab, fc, ec) in enumerate([("Good", "white", GREY), ("Partial or redundant", PINK, RED),
                                           ("Weak", RED, RED)]):
            yy = ly + 3 - k * 6.5
            ax.add_patch(FancyBboxPatch((lx, yy - 2), 6, 4, boxstyle="round,pad=0,rounding_size=0.8",
                                        fc=fc, ec=ec, lw=1.6))
            ax.text(lx + 8, yy, lab, fontsize=11, color=TEXT, va="center")
        ax.text(lx, 26, "Example ratings for\nteaching; rated by the\narchitecture team with\nthe capability owners",
                fontsize=10, color=MUTED, style="italic", va="center", linespacing=1.25)
        save(fig, "eam-capability-heatmap.png")
        return
    # level 2 of transport operations
    px, pw = 106, 22
    l2 = ["Duty and vehicle\nscheduling", "Dispatching and\noperations control", "Passenger\ninformation",
          "Incident handling\nin operations"]
    ax.text(px + pw / 2, 57, "Level 2 of\nTransport operations", ha="center", va="center", fontsize=11.5,
            color=TEXT, weight="bold", linespacing=1.2)
    top = 52
    for i, s in enumerate(l2):
        box(ax, px, top - i * 8.6 - 6.6, pw, 6.6, s, size=10.5, ec=RED, lw=1.4, fc="white")
    bx, by = positions["Transport\noperations"]
    yy = by + ch / 2
    arrow(ax, (bx + cw, yy), (px - 1.2, yy), color=RED, style="-", lw=1.4, ls="--")
    ax.plot([px - 1.2, px - 1.2], [top - 6.6 * 0.5 - 8.6 * 3, top - 6.6 * 0.5], color=RED, lw=1.4, ls="--")
    for i in range(4):
        ax.plot([px - 1.2, px], [top - 3.3 - i * 8.6] * 2, color=RED, lw=1.4, ls="--")
    ax.text(px + pw / 2, 13, "Each level-1 capability\nhas 3–8 at level 2", ha="center", va="center",
            fontsize=10, color=MUTED, style="italic", linespacing=1.2)
    save(fig, "eam-capability-map.png")


def value_stream():
    """Value stream as chevrons, with the enabling level-1 capabilities below each stage."""
    fig, ax = canvas(13, 5.2)
    stages = ["Apply for a\nsubscription", "Check and\nconclude contract", "Issue\nticket", "Collect monthly\npayments",
              "Change or\ncancel"]
    caps = [
        ["Customer\nmanagement", "Sales and\nticketing"],
        ["Customer\nmanagement", "Product and\nfare management"],
        ["Sales and\nticketing"],
        ["Payment and revenue\nmanagement"],
        ["Customer\nservice", "Customer\nmanagement"],
    ]
    n = len(stages)
    x0, w, tip, y, h = 14, 21.5, 3.2, 36, 10
    ax.text(x0 - 1.5, y + h / 2, "Stages", ha="right", va="center", fontsize=11.5, color=TEXT, weight="bold")
    ax.text(x0 - 1.5, 21, "Enabling\ncapabilities", ha="right", va="center", fontsize=11.5, color=TEXT,
            weight="bold", linespacing=1.2)
    for i, s in enumerate(stages):
        x = x0 + i * (w + 1.0)
        pts = [(x, y), (x + w, y), (x + w + tip, y + h / 2), (x + w, y + h), (x, y + h)]
        if i > 0:
            pts.append((x + tip, y + h / 2))
        ax.add_patch(Polygon(pts, closed=True, fc=GREY, ec=GREY, lw=1.2))
        ax.text(x + w / 2 + (tip / 2 if i > 0 else 0), y + h / 2, s, ha="center", va="center", fontsize=11,
                color="white", weight="bold", linespacing=1.2)
        for j, c in enumerate(caps[i]):
            cy = 25 - j * 9
            crit = c == "Customer\nmanagement"
            box(ax, x + 2, cy - 3.3, w - 2.5, 6.6, c, size=10.5, ec=RED if crit else GREY, lw=2.4 if crit else 1.6,
                bold=crit)
        ax.plot([x + w / 2 + 0.6, x + w / 2 + 0.6], [y - 0.2, 28.4], color=BORDER, lw=1.4, zorder=0)
    # stakeholder and value
    ax.text(x0, 51, "Stakeholder: customer (subscriber)     Value: travel all month with one ticket, "
            "without buying single tickets", fontsize=11, color=TEXT, va="center")
    ax.text(x0, 3.2, "Red border: a capability that enables several stages, so it is critical for this value stream",
            fontsize=10.5, color=MUTED, style="italic", va="center")
    save(fig, "eam-value-stream.png")


if __name__ == "__main__":
    capability_map()
    capability_map(heat=True)
    value_stream()
