"""Draw the figures for session 5 (data visualisation).

Run from the Lectures folder: python data-analytics/slides/img/make_viz_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

The TPC-H values are hard-coded so the script runs without DuckDB. They were
computed with DuckDB 1.5.5 on TPC-H sf 0.1 and the star schema of session 3
(fact_sales, dim_customer, dim_date); revenue = l_extendedprice * (1 - l_discount),
in million. Anscombe's quartet uses the data published by Anscombe (1973).
"""
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

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

# TPC-H sf 0.1, revenue 1997 per customer region (million)
REGIONS = ["Middle East", "America", "Europe", "Asia", "Africa"]
REGION_REV = [640.4, 626.2, 615.2, 604.3, 602.4]
# TPC-H sf 0.1, revenue 1997 per market segment (million)
SEGMENTS = ["Building", "Machinery", "Automobile", "Furniture", "Household"]
SEGMENT_REV = [650.0, 636.8, 615.4, 593.8, 592.5]
# TPC-H sf 0.1, revenue per order year (million) and number of months with orders
YEARS = [1992, 1993, 1994, 1995, 1996, 1997, 1998]
YEAR_REV = [3124.6, 3063.8, 3150.7, 3144.2, 3103.8, 3088.6, 1859.3]
REV_1998_JAN_JUL = [269.3, 238.2, 267.6, 271.3, 271.2, 250.8, 273.1]  # August 1998: 2 days only

ANSCOMBE_X = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
ANSCOMBE = [
    ("I", ANSCOMBE_X, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    ("II", ANSCOMBE_X, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    ("III", ANSCOMBE_X, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    ("IV", [8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
]


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=11, length=3)


def panel_title(ax, text, colour):
    ax.set_title(text, loc="left", fontsize=13, weight="bold", color=colour, pad=10)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def anscombe():
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.4), sharex=True, sharey=True)
    for ax, (name, x, y) in zip(axes, ANSCOMBE):
        ax.scatter(x, y, s=28, color=GREY, zorder=3)
        ax.plot([3, 20], [3 + 0.5 * 3, 3 + 0.5 * 20], color=RED, lw=1.5, zorder=2)  # y = 3 + 0.5x
        panel_title(ax, f"Data set {name}", TEXT)
        ax.set_xlim(2, 20)
        ax.set_ylim(2, 14)
        clean(ax)
    fig.text(0.5, -0.06, "All four: mean x = 9, mean y ≈ 7.50, correlation ≈ 0.82, "
             "regression line y ≈ 3 + 0.5x", ha="center", fontsize=12, color=MUTED)
    fig.tight_layout()
    save(fig, "viz-anscombe.png")


def pie_vs_bar():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw={"width_ratios": [1, 1.4]})
    colours = [GREY, RED, SOFT, MUTED, "#E8A0A8"]
    a1.pie(SEGMENT_REV, labels=SEGMENTS, colors=colours, startangle=90, counterclock=False,
           wedgeprops={"edgecolor": "white", "linewidth": 1.5}, textprops={"fontsize": 11, "color": TEXT})
    a1.set_aspect("equal")
    panel_title(a1, "Angle and area: which segment is largest?", TEXT)
    ypos = list(range(len(SEGMENTS)))[::-1]
    a2.barh(ypos, SEGMENT_REV, color=[RED] + [SOFT] * 4, height=0.6)
    a2.set_yticks(ypos, SEGMENTS)
    for y, v in zip(ypos, SEGMENT_REV):
        a2.text(v + 8, y, f"{v:.0f}", va="center", fontsize=11, color=TEXT)
    a2.set_xlim(0, 720)
    a2.set_xlabel("Revenue 1997 (million)", fontsize=11)
    panel_title(a2, "Position on a common scale: Building leads", TEXT)
    clean(a2)
    fig.tight_layout(w_pad=3)
    save(fig, "viz-pie-vs-bar.png")


def truncated_axis():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2))
    for ax in (a1, a2):
        ax.bar(REGIONS, REGION_REV, color=SOFT, width=0.6)
        ax.set_ylabel("Revenue 1997 (million)", fontsize=11)
        ax.tick_params(axis="x", labelsize=10)
        clean(ax)
    a1.set_ylim(595, 645)
    panel_title(a1, "Misleading: axis starts at 595", RED)
    a1.text(0.98, 0.95, "Middle East looks\nsix times larger than Africa", transform=a1.transAxes,
            ha="right", va="top", fontsize=11, color=RED)
    a2.set_ylim(0, 700)
    panel_title(a2, "Honest: bars start at zero", GREY)
    a2.text(0.98, 0.98, "Real difference: 6 %", transform=a2.transAxes, ha="right", va="top", fontsize=11, color=GREY)
    fig.tight_layout(w_pad=3)
    save(fig, "viz-truncated-axis.png")


def incomplete_year():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 4.2))
    labels = [str(y) for y in YEARS]
    a1.bar(labels, YEAR_REV, color=[SOFT] * 6 + [RED], width=0.6)
    a1.set_ylim(0, 3500)
    a1.set_ylabel("Revenue (million)", fontsize=11)
    panel_title(a1, "Misleading: “revenue collapsed in 1998”", RED)
    clean(a1)
    monthly = [v / 12 for v in YEAR_REV[:6]] + [sum(REV_1998_JAN_JUL) / 7]
    a2.bar(labels, monthly, color=[SOFT] * 6 + [GREY], width=0.6)
    a2.bar(labels[-1:], monthly[-1:], color="white", edgecolor=GREY, hatch="///", width=0.6)
    a2.set_ylim(0, 300)
    a2.set_ylabel("Average revenue per month (million)", fontsize=11)
    a2.text(6, monthly[-1] + 8, "Jan–Jul\nonly", ha="center", fontsize=10, color=GREY)
    panel_title(a2, "Honest: compare like with like", GREY)
    clean(a2)
    fig.tight_layout(w_pad=3)
    save(fig, "viz-incomplete-year.png")


if __name__ == "__main__":
    anscombe()
    pie_vs_bar()
    truncated_axis()
    incomplete_year()
