"""Draw the figures for session 8 (ML use-case lab).

Run from the Lectures folder: python data-analytics/slides/img/make_lab_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

- ml-pipeline.png: the churn starter pipeline (ColumnTransformer with a numeric and a
  categorical branch, then a model), own illustration based on the scikit-learn
  documentation on pipelines and composite estimators.
- ml-snapshot-folds.png: time-aware validation with customer snapshots: train on all
  earlier cut-offs, validate on the next one, final test on the 1997-07-01 cut-off.
"""
import logging
import sys
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
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


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, text, face, colour="white", size=12, bold=True, edge="none"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=face, edgecolor=edge, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=colour, fontsize=size,
            fontweight="bold" if bold else "normal")


def arrow(ax, p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=MUTED, lw=1.6,
                                 shrinkA=2, shrinkB=2))


def pipeline():
    fig, ax = plt.subplots(figsize=(12, 4.6))
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.45, 4.6)
    ax.axis("off")
    # outer Pipeline frame
    ax.add_patch(FancyBboxPatch((2.55, 0.25), 9.3, 4.0, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor="white", edgecolor=GREY, lw=1.8, linestyle="--"))
    ax.text(2.75, 3.98, 'Pipeline  ("prep" → "model")', ha="left", va="center", color=GREY, fontsize=12,
            fontweight="bold")
    # ColumnTransformer frame
    ax.add_patch(FancyBboxPatch((2.8, 0.5), 5.9, 3.15, boxstyle="round,pad=0.02,rounding_size=0.15",
                                facecolor=LIGHT, edgecolor=BORDER, lw=1.2))
    ax.text(3.0, 3.4, "ColumnTransformer", ha="left", va="center", color=TEXT, fontsize=11.5,
            fontweight="bold")
    # input
    box(ax, 0.1, 2.15, 2.1, 1.05, "numeric columns\nrecency, purchase days,\nrevenue, tenure, trend",
        "white", TEXT, 9.5, False, BORDER)
    box(ax, 0.1, 0.75, 2.1, 0.95, "categorical columns\nsegment, region", "white", TEXT, 9.5, False, BORDER)
    # numeric branch
    box(ax, 3.1, 2.3, 2.4, 0.75, "SimpleImputer\n(median + indicator)", GREY, size=10.5)
    box(ax, 5.95, 2.3, 2.4, 0.75, "StandardScaler", GREY, size=10.5)
    # categorical branch
    box(ax, 3.1, 0.85, 5.25, 0.75, "OneHotEncoder (handle_unknown=\"ignore\")", GREY, size=10.5)
    # model
    box(ax, 9.3, 1.45, 2.3, 1.05, "Model\nLogisticRegression\nor other estimator", RED, size=10.5)
    arrow(ax, (2.2, 2.68), (3.1, 2.68))
    arrow(ax, (2.2, 1.22), (3.1, 1.22))
    arrow(ax, (5.5, 2.68), (5.95, 2.68))
    arrow(ax, (8.35, 2.68), (9.3, 2.15))
    arrow(ax, (8.35, 1.22), (9.3, 1.8))
    ax.text(7.2, -0.35, "fit() learns medians, means, scales, categories and model weights from the training rows only",
            ha="center", va="bottom", color=RED, fontsize=11)
    save(fig, "ml-pipeline.png")


def snapshot_folds():
    cutoffs = [date(1995, 7, 1), date(1996, 1, 1), date(1996, 7, 1), date(1997, 1, 1), date(1997, 7, 1)]
    ends = cutoffs[1:] + [date(1998, 1, 1)]
    rows = [("Fold 1", ["T", "V", "", "", ""]), ("Fold 2", ["T", "T", "V", "", ""]),
            ("Fold 3", ["T", "T", "T", "V", ""]), ("Final model", ["T", "T", "T", "T", "X"])]
    fig, ax = plt.subplots(figsize=(12, 4.2))
    style = {"T": (GREY, "train", "white"), "V": (RED, "validate", "white"), "X": (TEXT, "test", "white")}
    for r, (name, roles) in enumerate(rows):
        yv = len(rows) - 1 - r
        ax.text(mdates.date2num(date(1995, 6, 1)), yv, name, ha="right", va="center", color=TEXT, fontsize=12,
                fontweight="bold")
        for c0, c1, role in zip(cutoffs, ends, roles):
            x0, x1 = mdates.date2num(c0), mdates.date2num(c1)
            if not role:
                ax.barh(yv, x1 - x0 - 6, left=x0 + 3, height=0.62, color="white", edgecolor=BORDER)
                continue
            face, label, col = style[role]
            ax.barh(yv, x1 - x0 - 6, left=x0 + 3, height=0.62, color=face, edgecolor="none")
            ax.text((x0 + x1) / 2, yv, label, ha="center", va="center", color=col, fontsize=11, fontweight="bold")
    for c in cutoffs:
        ax.axvline(mdates.date2num(c), color=BORDER, lw=1, zorder=0)
    ax.set_yticks([])
    ax.set_ylim(-0.5, len(rows) - 0.5)
    ax.set_xticks([mdates.date2num(c) for c in cutoffs] + [mdates.date2num(date(1998, 1, 1))])
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.set_xlim(mdates.date2num(date(1994, 11, 1)), mdates.date2num(date(1998, 1, 20)))
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="x", labelsize=10.5)
    ax.set_title("Each block = one snapshot: features before its cut-off, label from the 6 months after it",
                 color=MUTED, fontsize=11.5, loc="right")
    save(fig, "ml-snapshot-folds.png")


if __name__ == "__main__":
    pipeline()
    snapshot_folds()
