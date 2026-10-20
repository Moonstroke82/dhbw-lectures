"""Draw the risk management figures for session 7 (risk management process, risk matrix).

Own illustrations based on ISO (2018), ISO 31000:2018 Risk management - Guidelines. The layout is our
own and does not reproduce the figures of the standard. The risk matrix and the example risks are
own examples for the Rhein-Neckar Mobil Group case.

Run from the Lectures folder: python it-management-eam/slides/img/make_risk_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

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


def process():
    """Risk management process as a left-to-right flow with three accompanying activities."""
    fig, ax = canvas(12, 4.6)
    # accompanying activity on top
    box(ax, 0, 38, 120, 7, "Communication and consultation with stakeholders (throughout)", fc=LIGHT, ec=BORDER,
        size=12, bold=True)
    # main flow
    y, h = 14, 16
    box(ax, 0, y, 19, h, "Scope,\ncontext and\ncriteria", size=12, bold=True)
    box(ax, 25, y, 19, h, "Risk\nidentification", ec=RED, lw=2.2, size=12)
    box(ax, 49, y, 19, h, "Risk\nanalysis", ec=RED, lw=2.2, size=12)
    box(ax, 73, y, 19, h, "Risk\nevaluation", ec=RED, lw=2.2, size=12)
    box(ax, 98, y, 22, h, "Risk\ntreatment", fc=RED, ec=RED, tc="white", size=12.5, bold=True)
    for x0, x1 in [(19.5, 24.5), (44.5, 48.5), (68.5, 72.5), (92.5, 97.5)]:
        arrow(ax, (x0, y + h / 2), (x1, y + h / 2))
    # bracket for risk assessment
    ax.plot([25, 25, 92, 92], [31.5, 33.5, 33.5, 31.5], color=RED, lw=1.8)
    ax.text(58.5, 35.6, "Risk assessment", ha="center", va="center", fontsize=12, color=RED, weight="bold")
    # accompanying activities at the bottom
    box(ax, 0, 0, 58, 7, "Monitoring and review (throughout)", fc=LIGHT, ec=BORDER, size=12, bold=True)
    box(ax, 62, 0, 58, 7, "Recording and reporting (throughout)", fc=LIGHT, ec=BORDER, size=12, bold=True)
    # feedback loop from treatment back to identification
    arrow(ax, (109, 13.5), (34.5, 13.5), color=GREY, lw=1.6, scale=13, rad=-0.18)
    ax.text(72, 9.3, "residual risk is assessed again", ha="center", va="center", fontsize=10.5, color=GREY,
            style="italic")
    save(fig, "risk-process.png")


def matrix():
    """5 x 5 risk matrix with risk levels and three example risks."""
    fig, ax = plt.subplots(figsize=(7.6, 6.2), dpi=200)
    # risk levels: low 1-4, medium 5-9, high 10-16, very high 20-25
    level = {1: "#FFFFFF", 2: LIGHT, 3: "#F3A9B0", 4: RED}

    def lvl(score):
        if score <= 4:
            return 1
        if score <= 9:
            return 2
        if score <= 16:
            return 3
        return 4

    for c in range(1, 6):
        for l in range(1, 6):
            s = c * l
            ax.add_patch(Rectangle((c - 0.5, l - 0.5), 1, 1, fc=level[lvl(s)], ec=BORDER, lw=1.2))
            ax.text(c + 0.33, l + 0.33, str(s), ha="center", va="center", fontsize=8.5,
                    color="white" if lvl(s) == 4 else GREY)
    ax.set_aspect("equal")
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0.5, 5.5)
    ax.set_xticks(range(1, 6))
    ax.set_xticklabels(["1\nminor", "2\nmoderate", "3\nserious", "4\nmajor", "5\nsevere"], fontsize=9.5,
                       color=TEXT)
    ax.set_yticks(range(1, 6))
    ax.set_yticklabels(["1 rare", "2 unlikely", "3 possible", "4 likely", "5 almost\ncertain"], fontsize=9.5,
                       color=TEXT)
    ax.set_xlabel("Consequence", fontsize=11.5, color=GREY, weight="bold")
    ax.set_ylabel("Likelihood (per year)", fontsize=11.5, color=GREY, weight="bold")
    for side in ax.spines.values():
        side.set_visible(False)
    ax.tick_params(length=0)
    examples = [(5, 3, "R1"), (3, 4, "R2"), (4, 2, "R3")]
    for c, l, name in examples:
        ax.add_patch(plt.Circle((c - 0.08, l - 0.05), 0.24, fc="white", ec=TEXT, lw=1.6, zorder=3))
        ax.text(c - 0.08, l - 0.05, name, ha="center", va="center", fontsize=10, weight="bold", color=TEXT,
                zorder=4)
    save(fig, "risk-matrix.png")


if __name__ == "__main__":
    process()
    matrix()
