"""Draw the IT service management figures for session 6 (incident-problem-change flow, SLA/OLA/UC).

Own illustrations based on AXELOS (2019), ITIL Foundation: ITIL 4 edition, and Beims and
Ziegenbein (2023). The layout is our own and does not reproduce any published figure.

Run from the Lectures folder: python it-management-eam/slides/img/make_itsm_figures.py
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


def label(ax, x, y, text, size=10.5, color=GREY, italic=True):
    ax.text(x, y, text, ha="center", va="center", fontsize=size, color=color,
            style="italic" if italic else "normal", linespacing=1.2)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def flow():
    """Incident, problem and change: restore fast, then remove the cause."""
    fig, ax = canvas(12, 4.4)
    box(ax, 0, 25, 17, 12, "User or\nmonitoring", fc=LIGHT, size=12, bold=True)
    box(ax, 23, 25, 20, 12, "Service desk\n(single point\nof contact)", size=11.5, bold=True)
    box(ax, 49, 25, 28, 12, "Incident management\nrestore service quickly\n(fix or workaround)", ec=RED, lw=2.2,
        size=11.5)
    box(ax, 83, 25, 37, 12, "Service restored\nuser can work again", fc=RED, ec=RED, tc="white", size=12, bold=True)
    box(ax, 49, 2, 28, 13, "Problem management\nfind the root cause,\ndocument known error", size=11.5, ec=GREY,
        lw=2.2)
    box(ax, 83, 2, 37, 13, "Change enablement\nassess and authorise\nthe permanent fix", size=11.5, ec=GREY, lw=2.2)
    arrow(ax, (17.5, 31), (22.5, 31))
    arrow(ax, (43.5, 31), (48.5, 31))
    arrow(ax, (77.5, 31), (82.5, 31))
    arrow(ax, (63, 24.5), (63, 15.5), color=GREY, lw=1.8, scale=14)
    label(ax, 72, 20, "repeated or\nunknown cause")
    arrow(ax, (77.5, 8.5), (82.5, 8.5), color=GREY, lw=1.8, scale=14)
    arrow(ax, (101.5, 15.5), (101.5, 24.5), color=GREY, lw=1.8, scale=14, style="-|>")
    label(ax, 111, 20, "fewer future\nincidents")
    arrow(ax, (56, 15.5), (56, 24.5), color=GREY, lw=1.4, scale=12)
    label(ax, 45, 20, "workaround,\nknown error")
    save(fig, "itsm-flow.png")


def agreements():
    """SLA with the customer, OLAs with internal teams, underpinning contracts with suppliers."""
    fig, ax = canvas(12, 4.4)
    box(ax, 0, 15, 22, 14, "Customer\n(business unit)", fc=LIGHT, size=12.5, bold=True)
    box(ax, 40, 15, 30, 14, "IT service provider\n(service owner)", ec=RED, lw=2.4, size=12.5, bold=True)
    box(ax, 88, 29, 32, 12, "Internal teams\ne.g. network, database", size=11.5)
    box(ax, 88, 3, 32, 12, "External suppliers\ne.g. vendor, cloud provider", size=11.5)
    arrow(ax, (22.5, 22), (39.5, 22), style="<|-|>")
    ax.text(31, 25.5, "SLA", ha="center", va="center", fontsize=14, weight="bold", color=RED)
    label(ax, 31, 12, "service levels\nthe customer\ncan expect", size=10)
    arrow(ax, (70.5, 25), (87.5, 34), color=GREY, lw=2, style="<|-|>", scale=15)
    ax.text(77, 33, "OLA", ha="center", va="center", fontsize=13, weight="bold", color=GREY)
    arrow(ax, (70.5, 19), (87.5, 9), color=GREY, lw=2, style="<|-|>", scale=15)
    ax.text(76, 9, "UC", ha="center", va="center", fontsize=13, weight="bold", color=GREY)
    label(ax, 104, 22, "OLAs and UCs must support\n(underpin) the SLA targets", size=10)
    save(fig, "itsm-agreements.png")


if __name__ == "__main__":
    flow()
    agreements()
