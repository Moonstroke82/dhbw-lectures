"""Draw the figure for session 10 (one business process traced through the four EA domains).

Own illustration based on the four architecture domains of the TOGAF Standard (The Open Group, 2022)
and Hanschke (2023), with an own example from the course case Rhein-Neckar Mobil Group.
The layout is our own and does not reproduce a figure from these sources.

Run from the Lectures folder: python it-management-eam/slides/img/make_ea_figures.py
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


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def domains_trace():
    """'Sell a ticket on board' traced from business to technology architecture."""
    fig, ax = canvas(12, 5.6)
    bands = [  # (label, y)
        ("Business\narchitecture", 43),
        ("Data\narchitecture", 29.5),
        ("Application\narchitecture", 16),
        ("Technology\narchitecture", 2.5),
    ]
    bh = 11
    for label, y in bands:
        ax.add_patch(FancyBboxPatch((0, y), 120, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=LIGHT, ec=BORDER, lw=1.2))
        ax.add_patch(FancyBboxPatch((0, y), 19, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=GREY, ec=GREY, lw=1.2))
        ax.text(9.5, y + bh / 2, label, ha="center", va="center", fontsize=12, color="white",
                weight="bold", linespacing=1.15)

    # columns of elements: x positions
    cw, ch = 28, 7.4
    xs = [22.5, 56, 89.5]
    dy = (bh - ch) / 2
    elems = {
        "B": ["Process: sell ticket on board\n(drivers, bus and rail unit)", "Process: share revenue\nwith transport association",
              "Process: settle card\npayments (finance)"],
        "D": ["Data: fare\n(fare table)", "Data: ticket sale", "Data: card payment"],
        "A": ["Application: ticket\ndevice software", "Application: fare\nback-end",
              "External service:\npayment provider"],
        "T": ["Ticket device,\nmobile network", "Servers in the Group IT\ndata centre",
              "Platform of the\npayment provider"],
    }
    rows = {"B": bands[0][1], "D": bands[1][1], "A": bands[2][1], "T": bands[3][1]}
    ext = {("A", 2), ("T", 2)}
    for key, labels in elems.items():
        for i, lab in enumerate(labels):
            dashed = (key, i) in ext
            box(ax, xs[i], rows[key] + dy, cw, ch, lab, size=11.5, ec=MUTED if dashed else GREY,
                ls="--" if dashed else "-")

    # vertical dependencies (lower layer supports upper layer)
    def link(col_from, row_from, col_to, row_to, rad=0.0):
        x1 = xs[col_from] + cw / 2
        x2 = xs[col_to] + cw / 2
        y1 = rows[row_from] + dy + ch
        y2 = rows[row_to] + dy
        arrow(ax, (x1, y1 + 0.3), (x2, y2 - 0.3), rad=rad)

    for col in range(3):
        link(col, "D", col, "B")
        link(col, "A", col, "D")
        link(col, "T", col, "A")
    link(0, "A", 1, "D")   # device software creates ticket sales
    # application interface
    arrow(ax, (xs[0] + cw + 0.3, rows["A"] + dy + ch * 0.62), (xs[1] - 0.3, rows["A"] + dy + ch * 0.62),
          color=GREY, style="<|-|>")
    arrow(ax, (xs[1] + cw + 0.3, rows["A"] + dy + ch * 0.62), (xs[2] - 0.3, rows["A"] + dy + ch * 0.62),
          color=GREY, style="<|-|>")
    save(fig, "ea-domains-trace.png")


if __name__ == "__main__":
    domains_trace()
