"""Draw the figures for session 14 (Enterprise Application Integration).

- eai-p2p-vs-hub.png: six applications of the fictitious Rhein-Neckar Mobil Group, connected point-to-point
  (every pair has its own interface) and via a central integration platform (one connection per application).
- eai-event-driven.png: event-driven integration with a publish-subscribe channel: the fare back-end publishes
  "ticket sold" events to an event broker, several applications subscribe.
Own illustrations based on Hohpe and Woolf (2004) and Ebert et al. (2017); applications and layout are our own
example and do not reproduce a figure from these sources.

Run from the Lectures folder: python it-management-eam/slides/img/make_integration_figures.py
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


APPS = ["Fare\nback-end", "ERP\nbus and rail", "Car-sharing\nback-end", "Customer\ndatabase", "Payment\nprovider",
        "Passenger\ninformation"]


def ring(cx, cy, r, n):
    return [(cx + r * math.cos(math.pi / 2 - 2 * math.pi * i / n), cy + r * math.sin(math.pi / 2 - 2 * math.pi * i / n))
            for i in range(n)]


def p2p_vs_hub():
    """Left: full mesh of six applications (15 interfaces). Right: hub with six connections."""
    fig, ax = canvas(13, 6.2)
    bw, bh = 15, 6.4
    for k, (cx, title, sub) in enumerate([(31, "Point-to-point", "6 applications: 6 × 5 / 2 = 15 interfaces"),
                                          (99, "Integration platform (hub)", "6 applications: 6 connections")]):
        cy, r = 30, 21
        pos = ring(cx, cy, r, len(APPS))
        if k == 0:
            for i in range(len(pos)):
                for j in range(i + 1, len(pos)):
                    ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]], color=RED, lw=1.6, zorder=1)
        else:
            box(ax, cx - 11, cy - 4.2, 22, 8.4, "Integration\nplatform", fc=GREY, ec=GREY, tc="white", size=11.5,
                bold=True, z=3)
            for (px, py) in pos:
                ax.plot([px, cx], [py, cy], color=RED, lw=1.8, zorder=1)
        for (px, py), name in zip(pos, APPS):
            box(ax, px - bw / 2, py - bh / 2, bw, bh, name, size=9.5, z=3)
        ax.text(cx, 61, title, ha="center", va="center", fontsize=13, color=TEXT, weight="bold")
        ax.text(cx, 1.0, sub, ha="center", va="center", fontsize=10.5, color=MUTED, style="italic")
    ax.plot([65, 65], [4, 58], color=BORDER, lw=1.2)
    save(fig, "eai-p2p-vs-hub.png")


def event_driven():
    """Publisher -> event broker (publish-subscribe channel) -> subscribers."""
    fig, ax = canvas(13, 5.4)
    # publisher side
    box(ax, 1, 31, 22, 9, "Ticket devices\n(400 buses)", size=10.5)
    box(ax, 1, 13, 22, 9, "Fare back-end", size=11, bold=True)
    arrow(ax, (12, 31), (12, 22.2), color=GREY, lw=1.6, scale=12)
    ax.text(13.2, 26.6, "sales upload", fontsize=9, color=MUTED, va="center")
    ax.text(12, 6.5, "Publisher", ha="center", fontsize=11, color=TEXT, weight="bold")
    # event
    box(ax, 30, 14.5, 18, 6, "Event\n“ticket sold”", fc=LIGHT, ec=RED, tc=RED, size=9.5, bold=True, lw=1.4)
    arrow(ax, (23, 17.5), (29.6, 17.5), color=RED, lw=1.8, scale=13)
    arrow(ax, (48.2, 17.5), (55.6, 17.5), color=RED, lw=1.8, scale=13)
    # broker as a channel
    box(ax, 56, 4, 14, 41, "Event broker\n\npublish–\nsubscribe\nchannel", fc=GREY, ec=GREY, tc="white", size=10.5,
        bold=True)
    subs = [("Revenue sharing\n(report to the association)", 38),
            ("Cloud ERP: finance\n(daily revenue posting)", 27.5),
            ("Mobility app\n(ticket in customer account)", 17),
            ("Reporting and analytics", 6.5)]
    for name, y in subs:
        box(ax, 84, y - 4, 36, 8, name, size=10)
        arrow(ax, (70.2, y), (83.6, y), color=RED, lw=1.6, scale=12)
    ax.text(102, 48.5, "Subscribers", ha="center", fontsize=11, color=TEXT, weight="bold")
    ax.text(63, 48.5, "Middleware", ha="center", fontsize=11, color=TEXT, weight="bold")
    ax.text(1, -2.5, "The publisher does not know its subscribers; a new subscriber is added without changing "
            "the fare back-end. Own example.", fontsize=9.5, color=MUTED, style="italic", va="center")
    save(fig, "eai-event-driven.png")


if __name__ == "__main__":
    p2p_vs_hub()
    event_driven()
