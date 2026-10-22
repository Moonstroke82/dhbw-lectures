"""Draw the figures for session 9 (experiments and A/B testing).

Run from the Lectures folder: python data-analytics/slides/img/make_ab_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

The numbers are hard-coded so the script runs without the dataset. They were
computed with pandas 3.0.6, SciPy 1.18.1 and statsmodels 0.15.0:

- ab-confounding.png: why a correlation is not a causal effect (confounder) and
  how randomisation removes the arrow into the treatment. Own illustration based
  on Kohavi et al. (2020, Chapters 1 and 11).
- ab-hillstrom-effects.png: treatment effects with 95 % confidence intervals in the
  Hillstrom (2008) e-mail test (64,000 customers, three arms of about 21,300 each;
  difference to "No E-Mail"; Wald intervals for proportions, Welch for spend).
- ab-peeking.png: share of A/A tests declared "significant" at least once when the
  analyst checks a two-proportion z-test every day (10,000 simulated A/A tests,
  14 days, 1,000 users per arm and day, true rate 10 %, numpy seed 42), compared
  with a single analysis at the planned end. The simulation code is in worksheet 9.
"""
import logging
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
MUTED, LIGHT, BORDER = "#" + theme.COLORS["muted"], "#" + theme.COLORS["light"], "#" + theme.COLORS["border"]
SOFT = "#B8C0C5"  # light grey for context data
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # quiet Arial fallback
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = MUTED
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT

# Hillstrom (2008): difference treatment - control (No E-Mail), 95 % CI
EFFECTS = {  # metric: [(arm, diff, low, high), ...]
    "Visit rate (percentage points)": [("Mens E-Mail", 7.66, 7.00, 8.32), ("Womens E-Mail", 4.52, 3.89, 5.16)],
    "Conversion rate (percentage points)": [("Mens E-Mail", 0.68, 0.50, 0.86), ("Womens E-Mail", 0.31, 0.15, 0.47)],
    "Spend per customer (USD)": [("Mens E-Mail", 0.77, 0.49, 1.05), ("Womens E-Mail", 0.42, 0.17, 0.68)],
}
CONTROL = {"Visit rate (percentage points)": "control 10.62 %",
           "Conversion rate (percentage points)": "control 0.57 %",
           "Spend per customer (USD)": "control USD 0.65"}

# A/A simulation: share of tests with p < 0.05 on at least one day up to day d
PEEK_EVER = [0.050, 0.080, 0.105, 0.124, 0.139, 0.153, 0.166, 0.175, 0.185, 0.194, 0.202, 0.210, 0.216, 0.220]
FINAL_ONLY = 0.0508


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=11, length=3)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def node(ax, x, y, text, colour=GREY, w=30, h=11):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.4,rounding_size=2",
                                fc="white", ec=colour, lw=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=12, color=TEXT)


def arrow(ax, a, b, colour=GREY, dashed=False, label=None, off=(0, 3)):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=16, lw=2, color=colour,
                                 linestyle=(0, (4, 3)) if dashed else "-", shrinkA=2, shrinkB=2))
    if label:
        ax.text((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1], label, ha="center", va="center",
                fontsize=11, color=colour, weight="bold")


def confounding():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.9), dpi=200)
    for ax in axes:
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 48)
        ax.axis("off")
    ax = axes[0]
    ax.set_title("Observational data: who saw the box is not random", loc="left", fontsize=13,
                 weight="bold", color=TEXT)
    node(ax, 50, 38, "Customer activity\n(confounder)", colour=MUTED, w=34)
    node(ax, 18, 9, "Saw the\nrecommendation box")
    node(ax, 82, 9, "Revenue")
    arrow(ax, (40, 32), (24, 16), colour=MUTED)
    arrow(ax, (60, 32), (76, 16), colour=MUTED)
    arrow(ax, (35, 9), (71, 9), colour=RED, dashed=True, label="causal effect?", off=(0, 4))
    ax = axes[1]
    ax.set_title("Experiment: a coin decides who sees the box", loc="left", fontsize=13,
                 weight="bold", color=TEXT)
    node(ax, 50, 38, "Customer activity", colour=SOFT, w=34)
    node(ax, 14, 38, "Random\nassignment", colour=RED, w=22)
    node(ax, 18, 9, "Saw the\nrecommendation box")
    node(ax, 82, 9, "Revenue")
    arrow(ax, (16, 31), (18, 16), colour=RED)
    arrow(ax, (60, 32), (76, 16), colour=SOFT)
    arrow(ax, (35, 9), (71, 9), colour=RED, label="effect = B − A", off=(0, 4))
    ax.text(32, 25, "no arrow from activity\nto the box", ha="center", va="center", fontsize=10.5, color=MUTED)
    fig.tight_layout()
    save(fig, "ab-confounding.png")


def effects():
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.3), dpi=200)
    for ax, (metric, rows) in zip(axes, EFFECTS.items()):
        for i, (arm, d, lo, hi) in enumerate(rows):
            y = 1 - i
            c = RED if arm.startswith("Mens") else GREY
            ax.plot([lo, hi], [y, y], color=c, lw=2.5, solid_capstyle="round")
            ax.plot([d], [y], "o", ms=9, color=c, mec="white", mew=2, zorder=3)
            ax.text(hi, y + 0.22, f"{d:.2f}  [{lo:.2f}, {hi:.2f}]", ha="right", va="bottom", fontsize=10, color=TEXT)
        ax.axvline(0, color=MUTED, lw=1)
        ax.set_yticks([1, 0])
        ax.set_yticklabels(["Mens E-Mail", "Womens E-Mail"], fontsize=11)
        ax.set_ylim(-0.6, 1.75)
        xmax = max(r[3] for r in rows) * 1.12
        ax.set_xlim(-0.08 * xmax, xmax)
        ax.set_title(metric, loc="left", fontsize=12, weight="bold", color=TEXT, pad=8)
        ax.set_xlabel(f"difference to No E-Mail ({CONTROL[metric]})", fontsize=10, color=MUTED)
        ax.grid(axis="x", color=BORDER, lw=0.8)
        ax.set_axisbelow(True)
        clean(ax)
        ax.spines["left"].set_visible(False)
        ax.tick_params(axis="y", length=0)
    for ax in axes[1:]:
        ax.set_yticklabels([])
    fig.tight_layout()
    save(fig, "ab-hillstrom-effects.png")


def peeking():
    fig, ax = plt.subplots(figsize=(10, 3.9), dpi=200)
    days = list(range(1, len(PEEK_EVER) + 1))
    ax.plot(days, [100 * v for v in PEEK_EVER], color=RED, lw=2.5, marker="o", ms=6, mec="white", mew=1.5)
    ax.axhline(5, color=GREY, lw=2, linestyle=(0, (4, 3)))
    ax.text(14, 6.2, f"one analysis at the planned end: {100 * FINAL_ONLY:.1f} %", ha="right", va="bottom",
            fontsize=11, color=GREY)
    ax.text(14, 100 * PEEK_EVER[-1] + 1.3, f"check every day, stop at p < 0.05: {100 * PEEK_EVER[-1]:.1f} %",
            ha="right", va="bottom", fontsize=11, color=RED, weight="bold")
    ax.set_xlim(0.5, 14.5)
    ax.set_ylim(0, 26)
    ax.set_xticks(days)
    ax.set_xlabel("day of the test", fontsize=11)
    ax.set_ylabel("A/A tests declared\n'significant' (%)", fontsize=11)
    ax.grid(axis="y", color=BORDER, lw=0.8)
    ax.set_axisbelow(True)
    clean(ax)
    fig.tight_layout()
    save(fig, "ab-peeking.png")


if __name__ == "__main__":
    confounding()
    effects()
    peeking()
