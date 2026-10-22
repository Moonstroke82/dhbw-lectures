"""Draw the figures for session 7 (from business question to ML use case).

Run from the Lectures folder: python data-analytics/slides/img/make_ml_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

- ml-crisp-dm.png: the six CRISP-DM phases as a cycle, own illustration based on
  Chapman et al. (2000).
- ml-churn-timeline.png: observation window, cut-off and label window of the churn
  example on TPC-H (orders 1992-01-01 to 1998-08-02), with the leaky feature
  "purchase days in 1997" that crosses the cut-off.
"""
import logging
import math
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


def crisp_dm():
    phases = ["Business\nunderstanding", "Data\nunderstanding", "Data\npreparation",
              "Modelling", "Evaluation", "Deployment"]
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-3.6, 3.6)
    ax.set_aspect("equal")
    ax.axis("off")
    rx, ry = 3.7, 2.55
    w, h = 2.5, 1.0
    pos = []
    for i, name in enumerate(phases):
        a = math.radians(120 - i * 60)   # start top left, clockwise
        x, y = rx * math.cos(a), ry * math.sin(a)
        pos.append((x, y))
        face = RED if i == 0 else GREY
        ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.05,rounding_size=0.15",
                                    facecolor=face, edgecolor="none"))
        ax.text(x, y, name, ha="center", va="center", color="white", fontsize=12.5, fontweight="bold")
    # centre: data
    ax.add_patch(FancyBboxPatch((-0.95, -0.5), 1.9, 1.0, boxstyle="round,pad=0.05,rounding_size=0.3",
                                facecolor=LIGHT, edgecolor=BORDER))
    ax.text(0, 0, "Data", ha="center", va="center", color=TEXT, fontsize=14, fontweight="bold")

    def arrow(p, q, two_way=False, style="-", colour=MUTED, rad=0.0, shrink=48):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="<|-|>" if two_way else "-|>", mutation_scale=16,
                                     color=colour, lw=1.8, linestyle=style, shrinkA=shrink, shrinkB=shrink,
                                     connectionstyle=f"arc3,rad={rad}"))
    arrow(pos[0], pos[1], two_way=True)          # BU <-> DU
    arrow(pos[1], pos[2])                        # DU -> DP
    arrow(pos[2], pos[3], two_way=True)          # DP <-> modelling
    arrow(pos[3], pos[4])                        # modelling -> evaluation
    arrow(pos[4], pos[5])                        # evaluation -> deployment
    arrow(pos[4], pos[0], style="--", colour=RED, rad=0.15, shrink=40)  # back to business understanding
    ax.text(0.45, -1.15, "not good enough for the business?\nback to the question", ha="center", va="center",
            color=RED, fontsize=10.5)
    save(fig, "ml-crisp-dm.png")


def churn_timeline():
    fig, ax = plt.subplots(figsize=(12, 3.9))
    start, cut, label_end, data_end = date(1992, 1, 1), date(1997, 7, 1), date(1998, 1, 1), date(1998, 8, 2)
    row_main, row_leak = 1.0, 0.0
    ax.barh(row_main, mdates.date2num(cut) - mdates.date2num(start), left=mdates.date2num(start), height=0.5,
            color=SOFT, edgecolor="none")
    ax.text(mdates.date2num(date(1994, 10, 1)), row_main, "Observation window: features from history before the cut-off",
            ha="center", va="center", color=TEXT, fontsize=12)
    ax.barh(row_main, mdates.date2num(label_end) - mdates.date2num(cut), left=mdates.date2num(cut), height=0.5,
            color=RED, edgecolor="none")
    ax.text(mdates.date2num(date(1997, 10, 1)), row_main, "Label\nwindow", ha="center", va="center",
            color="white", fontsize=11, fontweight="bold")
    ax.barh(row_main, mdates.date2num(data_end) - mdates.date2num(label_end), left=mdates.date2num(label_end),
            height=0.5, color=LIGHT, edgecolor=BORDER)
    ax.text(mdates.date2num(date(1998, 4, 16)), row_main, "not\nused", ha="center", va="center", color=MUTED, fontsize=10)
    # leaky feature
    ax.barh(row_leak, mdates.date2num(date(1998, 1, 1)) - mdates.date2num(date(1997, 1, 1)),
            left=mdates.date2num(date(1997, 1, 1)), height=0.5, color="white", edgecolor=RED, hatch="///", lw=1.5)
    ax.text(mdates.date2num(date(1996, 12, 1)), row_leak, "Leaky feature “purchase days in 1997” →\n"
            "looks into the label window", ha="right", va="center", color=RED, fontsize=12)
    # cut-off
    ax.axvline(mdates.date2num(cut), color=TEXT, lw=1.6, ymin=0.02, ymax=0.84)
    ax.text(mdates.date2num(cut), 1.62, "Cut-off 1997-07-01 = prediction point", ha="center", va="bottom",
            color=TEXT, fontsize=12, fontweight="bold")
    ax.set_ylim(-0.6, 1.95)
    ax.set_yticks([])
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_xlim(mdates.date2num(start), mdates.date2num(data_end) + 20)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="x", labelsize=11)
    save(fig, "ml-churn-timeline.png")


if __name__ == "__main__":
    crisp_dm()
    churn_timeline()
