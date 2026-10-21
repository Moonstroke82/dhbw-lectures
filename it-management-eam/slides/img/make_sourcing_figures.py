"""Draw the figures for session 15 (IT sourcing).

- sourcing-make-or-buy.png: a 2 x 2 make-or-buy matrix with the contribution of an IT activity to the competitive
  position (commodity vs. differentiator) and the maturity of the market offerings (low vs. high), with example
  activities of the fictitious Rhein-Neckar Mobil Group.
- sourcing-cloud-responsibility.png: who manages which layer in on-premises operation, IaaS, PaaS and SaaS.
- sourcing-vendor-lifecycle.png: the life cycle of a sourcing relationship from sourcing strategy to renewal or exit.
Own illustrations. The make-or-buy criteria are based on Lacity, Willcocks and Feeny (1996) and Prahalad and Hamel
(1990), the service models on Mell and Grance (2011); quadrant labels, layers, phases and examples are our own and do
not reproduce a figure from these sources.

Run from the Lectures folder: python it-management-eam/slides/img/make_sourcing_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import math
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


def box(ax, x, y, w, h, label, fc="white", ec=GREY, tc=TEXT, size=12, bold=False, lw=1.8, pad=1.0, ls="-",
        z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={pad}", fc=fc, ec=ec, lw=lw,
                                ls=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=tc,
            weight="bold" if bold else "normal", linespacing=1.15, zorder=z + 1)


def arrow(ax, a, b, color=RED, lw=1.8, style="-|>", scale=14, rad=0.0, ls="-", z=1):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, linestyle=ls, zorder=z))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def make_or_buy():
    """2 x 2 matrix: x = maturity of market offerings, y = contribution to competitive position."""
    fig, ax = canvas(11, 6.6)
    x0, y0, cw, ch = 16, 6, 44, 26
    quads = [
        # (col, row, title, text, examples, highlight)
        (0, 1, "Make", "Develop and run in-house,\nbuild own skills",
         "e.g. fare and journey logic\nof the mobility app", True),
        (1, 1, "Buy and differentiate", "Standard product or platform,\nown extensions, keep control",
         "e.g. customer master on a\nCRM platform, own app on top", False),
        (0, 0, "Standardise first", "Question the requirement,\nthen buy or share",
         "e.g. special fare macros\nin Excel", False),
        (1, 0, "Buy or outsource", "SaaS, managed service,\nselective outsourcing",
         "e.g. payroll, e-mail and office,\nhelpdesk tool, finance ERP", True),
    ]
    for col, row, title, text, ex, hi in quads:
        x, y = x0 + col * cw, y0 + row * ch
        ax.add_patch(FancyBboxPatch((x + 0.6, y + 0.6), cw - 1.2, ch - 1.2, boxstyle="round,pad=0,rounding_size=1",
                                    fc=LIGHT if not hi else "white", ec=RED if hi else GREY, lw=2.0 if hi else 1.4,
                                    zorder=1))
        ax.text(x + cw / 2, y + ch - 5, title, ha="center", va="center", fontsize=14, weight="bold",
                color=RED if hi else TEXT, zorder=3)
        ax.text(x + cw / 2, y + ch / 2 - 0.5, text, ha="center", va="center", fontsize=11, color=TEXT,
                linespacing=1.2, zorder=3)
        ax.text(x + cw / 2, y + 5, ex, ha="center", va="center", fontsize=9.8, color=MUTED, style="italic",
                linespacing=1.15, zorder=3)
    # axes
    arrow(ax, (x0, y0 - 0.2), (x0 + 2 * cw + 3, y0 - 0.2), color=GREY, lw=1.6, scale=14)
    arrow(ax, (x0 - 0.2, y0), (x0 - 0.2, y0 + 2 * ch + 3), color=GREY, lw=1.6, scale=14)
    ax.text(x0 + cw, y0 - 4.6, "Maturity of market offerings", ha="center", fontsize=12, color=TEXT, weight="bold")
    ax.text(x0 + cw / 2, y0 - 2.0, "low", ha="center", va="top", fontsize=10, color=MUTED)
    ax.text(x0 + 1.5 * cw, y0 - 2.0, "high", ha="center", va="top", fontsize=10, color=MUTED)
    ax.text(x0 - 9.5, y0 + ch, "Contribution to\ncompetitive position", ha="center", va="center", fontsize=12,
            color=TEXT, weight="bold", rotation=90, linespacing=1.2)
    ax.text(x0 - 2.2, y0 + ch / 2, "commodity", ha="center", va="center", fontsize=10, color=MUTED, rotation=90)
    ax.text(x0 - 2.2, y0 + 1.5 * ch, "differentiator", ha="center", va="center", fontsize=10, color=MUTED,
            rotation=90)
    save(fig, "sourcing-make-or-buy.png")


LAYERS = ["Data and access rights", "Application", "Runtime and middleware", "Operating system",
          "Virtualisation", "Servers and storage", "Network and data centre"]
# number of layers (from the bottom) managed by the provider in each model
MODELS = [("On-premises", 0), ("IaaS", 3), ("PaaS", 5), ("SaaS", 6)]


def cloud_responsibility():
    """Four stacked columns; customer-managed layers in red, provider-managed layers in grey."""
    fig, ax = canvas(13, 6.6)
    n = len(LAYERS)
    lh, gap = 6.2, 0.7
    cw, x0, step = 22, 22, 27
    ybase = 4
    for i, name in enumerate(LAYERS):
        y = ybase + (n - 1 - i) * (lh + gap)
        ax.text(x0 - 1.5, y + lh / 2, name, ha="right", va="center", fontsize=10.5, color=TEXT)
    for k, (model, prov) in enumerate(MODELS):
        x = x0 + k * step
        ax.text(x + cw / 2, ybase + n * (lh + gap) + 2.2, model, ha="center", va="center", fontsize=13,
                weight="bold", color=TEXT)
        for i, name in enumerate(LAYERS):
            layer_from_bottom = n - 1 - i
            y = ybase + layer_from_bottom * (lh + gap)
            provider = layer_from_bottom < prov
            if i == 0:  # data and access rights always stay with the customer
                provider = False
            fc = GREY if provider else "white"
            ec = GREY if provider else RED
            tc = "white" if provider else RED
            label = "Provider" if provider else "Customer"
            box(ax, x, y, cw, lh, label, fc=fc, ec=ec, tc=tc, size=10, bold=not provider, lw=1.6, pad=0.8)
    ax.text(x0, -1.5, "Red: managed by the customer · grey: managed by the provider. Data, users and access rights\n"
            "stay the customer's responsibility in every model. Own illustration; simplified.",
            fontsize=9.5, color=MUTED, style="italic", va="center")
    save(fig, "sourcing-cloud-responsibility.png")


PHASES = [("1 Sourcing\nstrategy", "what to buy,\nwhich model"),
          ("2 Selection", "requirements, tender,\nevaluation"),
          ("3 Contract", "services, SLAs, prices,\naudit and exit clauses"),
          ("4 Transition", "hand-over of staff,\ndata, knowledge"),
          ("5 Operation and\nsteering", "SLA reviews, changes,\nrelationship"),
          ("6 Renewal\nor exit", "re-tender, insource,\nswitch provider")]


def vendor_lifecycle():
    """Six phases on a ring with arrows; centre: retained organisation."""
    fig, ax = canvas(12, 6.6)
    cx, cy, rx, ry = 60, 32, 42, 22
    n = len(PHASES)
    pts = []
    for i in range(n):
        a = math.pi / 2 + math.pi / n - 2 * math.pi * i / n
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    bw, bh = 25, 12.5
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        # shorten arrows so they start and end at the box edges
        dx, dy = x2 - x1, y2 - y1
        d = math.hypot(dx, dy)
        sx = min(abs((bw / 2 + 0.8) / dx) if dx else 9, abs((bh / 2 + 0.8) / dy) if dy else 9)
        ax.add_patch(FancyArrowPatch((x1 + dx * sx, y1 + dy * sx), (x2 - dx * sx, y2 - dy * sx), arrowstyle="-|>",
                                     mutation_scale=14, color=RED, lw=1.8, connectionstyle="arc3,rad=-0.12",
                                     shrinkA=0, shrinkB=0, zorder=1))
        _ = d
    for (px, py), (title, sub) in zip(pts, PHASES):
        ax.add_patch(FancyBboxPatch((px - bw / 2, py - bh / 2), bw, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc="white", ec=GREY, lw=1.8, zorder=2))
        ax.text(px, py + 2.4, title, ha="center", va="center", fontsize=11, weight="bold", color=TEXT,
                linespacing=1.1, zorder=3)
        ax.text(px, py - 3.3, sub, ha="center", va="center", fontsize=9, color=MUTED, linespacing=1.1, zorder=3)
    box(ax, cx - 15, cy - 6, 30, 12, "Retained organisation\nsteers the provider:\nowner, architecture, contracts",
        fc=GREY, ec=GREY, tc="white", size=10, bold=True, z=3)
    save(fig, "sourcing-vendor-lifecycle.png")


if __name__ == "__main__":
    make_or_buy()
    cloud_responsibility()
    vendor_lifecycle()
