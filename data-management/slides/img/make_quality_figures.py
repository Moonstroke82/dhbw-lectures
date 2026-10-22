"""Draw the figure for session 13 (data quality I).

Run from the Lectures folder: python data-management/slides/img/make_quality_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
The cost curves are qualitative (no data): own illustration of the idea in
Haug, Zachariassen and van Liempd (2011) that total cost is lowest below 100 % quality.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def cost_tradeoff():
    """Costs of poor data fall, costs of assuring quality rise; the total has a minimum."""
    q = np.linspace(0.05, 0.98, 300)
    poor = 0.9 * (1 - q) ** 2 + 0.04          # falls fast at first, then slowly
    assure = 0.05 + 0.75 * q ** 3             # rises, steeply near 100 %
    total = poor + assure
    i = int(np.argmin(total))

    fig, ax = plt.subplots(figsize=(9, 4.6), dpi=200)
    ax.plot(q, poor, color=GREY, lw=2.4, label="Costs caused by poor data")
    ax.plot(q, assure, color=GREY, lw=2.4, ls="--", label="Costs of assuring data quality")
    ax.plot(q, total, color=RED, lw=3, label="Total costs")
    ax.plot([q[i], q[i]], [0, total[i]], color=RED, lw=1.2, ls=":")
    ax.scatter([q[i]], [total[i]], color=RED, s=60, zorder=5)
    ax.annotate("lowest total cost:\n“good enough” for the use",
                xy=(q[i], total[i]), xytext=(q[i] - 0.33, total[i] + 0.38),
                fontsize=11, color=TEXT,
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
    ax.annotate("perfect data:\nvery expensive", xy=(0.96, assure[-8]), xytext=(0.70, 0.95),
                fontsize=11, color=TEXT, arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2))
    ax.set_xlim(0, 1.02)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([0.05, 0.98])
    ax.set_xticklabels(["low", "high"], fontsize=11, color=TEXT)
    ax.set_yticks([])
    ax.set_xlabel("Data quality", fontsize=12, color=TEXT)
    ax.set_ylabel("Costs", fontsize=12, color=TEXT)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.legend(loc="upper center", frameon=False, fontsize=11, ncol=3,
              bbox_to_anchor=(0.5, 1.1), labelcolor=TEXT)
    save(fig, "quality-cost-tradeoff.png")


if __name__ == "__main__":
    cost_tradeoff()
