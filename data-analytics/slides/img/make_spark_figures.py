"""Draw the figures for session 15 (big data analytics with Spark).

Run from the Lectures folder: python data-analytics/slides/img/make_spark_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

- spark-architecture.png: driver, cluster manager and executors with partitions and tasks;
  local mode on a laptop. Own illustration based on Zaharia et al. (2016) and the Spark 4.2.0
  documentation (Cluster Mode Overview).
- ppd-yearly.png: sales per year and median price, HM Land Registry Price Paid Data, standard
  entries (category A), 1995 to August 2026. The values below are the output of query Q1 of the
  session (Spark 4.2.0 and DuckDB 1.5.6 return identical counts and exact medians) on the
  complete file downloaded on 22 October 2026 (31,610,742 rows). Contains HM Land Registry data
  (c) Crown copyright and database right 2021, licensed under the Open Government Licence v3.0.
- spark-ml-pipeline.png: the MLlib pipeline of the lab (StringIndexer, OneHotEncoder,
  VectorAssembler, LinearRegression) and fit/transform. Own illustration based on the Spark 4.2.0
  documentation (ML Pipelines).
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

# Q1: year, sales (category A), exact median price (GBP)
YEARLY = [
    (1995, 797147, 54950), (1996, 965419, 57000), (1997, 1094660, 60000), (1998, 1050692, 65000),
    (1999, 1195074, 72950), (2000, 1129560, 80000), (2001, 1246023, 90000), (2002, 1351952, 110000),
    (2003, 1235619, 130000), (2004, 1232133, 150000), (2005, 1061739, 157500), (2006, 1326222, 166000),
    (2007, 1272348, 175000), (2008, 649537, 170000), (2009, 625214, 168900), (2010, 663173, 182000),
    (2011, 660983, 176000), (2012, 668548, 180000), (2013, 791662, 185000), (2014, 919368, 195000),
    (2015, 918957, 208000), (2016, 922625, 219950), (2017, 906886, 228500), (2018, 875564, 235000),
    (2019, 843019, 239995), (2020, 753388, 257500), (2021, 1086934, 276000), (2022, 909941, 290000),
    (2023, 708315, 286500), (2024, 763905, 291000), (2025, 809461, 298000), (2026, 331125, 290000),
]


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, text, face, colour="white", size=12, bold=True, edge="none", ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                facecolor=face, edgecolor=edge, lw=1.4, linestyle=ls))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=colour, fontsize=size,
                fontweight="bold" if bold else "normal")


def arrow(ax, p, q, colour=MUTED, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=14, color=colour, lw=1.6,
                                 shrinkA=2, shrinkB=2))


def architecture():
    fig, ax = plt.subplots(figsize=(12, 5.0))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    # driver
    box(ax, 0.2, 1.55, 2.9, 2.0, "", LIGHT, edge=BORDER)
    ax.text(1.65, 3.2, "Driver", ha="center", va="center", color=TEXT, fontsize=13, fontweight="bold")
    ax.text(1.65, 2.45, "SparkSession\nplans the job:\nDAG → stages → tasks", ha="center", va="center",
            color=TEXT, fontsize=10.5)
    # cluster manager
    box(ax, 4.0, 4.0, 3.4, 0.75, "Cluster manager\n(standalone, YARN, Kubernetes)", "white", TEXT, 10, False, BORDER)
    arrow(ax, (3.1, 3.3), (4.0, 4.3))
    # executors
    for i, y0 in enumerate([2.05, 0.15]):
        box(ax, 4.0, y0, 7.7, 1.55, "", "white", edge=GREY)
        ax.text(4.15, y0 + 1.3, f"Executor {i + 1}  (JVM on a worker node, memory + disk)", ha="left",
                va="center", color=GREY, fontsize=10.5, fontweight="bold")
        for j in range(4):
            x0 = 4.25 + j * 1.85
            box(ax, x0, y0 + 0.15, 1.65, 0.85, f"task\npartition {i * 4 + j + 1}", GREY, size=9.5)
        arrow(ax, (3.1, 2.55), (4.0, y0 + 0.8))
    ax.text(6.0, 4.88, "", ha="center")
    ax.text(0.2, 0.55, "Local mode, local[*]:\ndriver and one executor in\none JVM on your laptop;\none task per core at a time",
            ha="left", va="center", color=RED, fontsize=10.5)
    save(fig, "spark-architecture.png")


def yearly():
    years = [r[0] for r in YEARLY]
    sales = [r[1] / 1e6 for r in YEARLY]
    med = [r[2] / 1000 for r in YEARLY]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 5.4), sharex=True,
                                 gridspec_kw={"hspace": 0.28, "height_ratios": [1, 1]})
    colours = [SOFT if y >= 2024 else GREY for y in years]
    a1.bar(years, sales, color=colours, width=0.78)
    a1.set_title("Sales per year (million, standard entries)", loc="left", color=TEXT, fontsize=12)
    a1.annotate("2008: financial crisis", xy=(2008, 0.66), xytext=(2008.6, 1.06), color=MUTED, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
    a1.annotate("2021: stamp duty holiday", xy=(2021, 1.09), xytext=(2013.4, 1.33), color=MUTED, fontsize=10,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
    a1.text(2025.7, 1.03, "light: probably\nincomplete (late\nregistration);\n2026 to August", ha="center",
            va="bottom", color=RED, fontsize=9.5)
    a1.set_ylim(0, 1.5)
    a2.plot([y for y in years if y <= 2025], [m for y, m in zip(years, med) if y <= 2025], color=GREY, lw=2.2)
    a2.plot([2025, 2026], [med[-2], med[-1]], color=SOFT, lw=2.2, linestyle="--")
    a2.set_title("Median price (thousand GBP)", loc="left", color=TEXT, fontsize=12)
    a2.set_ylim(0, 330)
    for y, m in [(1995, 55), (2007, 175), (2025, 298)]:
        a2.annotate(f"{m}", xy=(y, m), xytext=(0, 7), textcoords="offset points", ha="center",
                    color=TEXT, fontsize=10)
    for a in (a1, a2):
        for s in ["top", "right"]:
            a.spines[s].set_visible(False)
        a.grid(axis="y", color=BORDER, lw=0.8)
        a.set_axisbelow(True)
        a.tick_params(labelsize=10.5)
    a2.set_xticks(range(1995, 2027, 5))
    save(fig, "ppd-yearly.png")


def ml_pipeline():
    fig, ax = plt.subplots(figsize=(12, 4.4))
    ax.set_xlim(0, 12)
    ax.set_ylim(-0.4, 4.2)
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((1.95, 0.85), 9.9, 2.95, boxstyle="round,pad=0.02,rounding_size=0.2",
                                facecolor="white", edgecolor=GREY, lw=1.8, linestyle="--"))
    ax.text(2.15, 3.52, "Pipeline(stages=[...])  —  an Estimator", ha="left", va="center", color=GREY,
            fontsize=12, fontweight="bold")
    box(ax, 0.05, 1.45, 1.6, 1.4, "DataFrame\nptype, new_build,\ntenure, outcode,\nmonth, log_price",
        "white", TEXT, 9.5, False, BORDER)
    stages = [("StringIndexer", "category → index\n(Estimator)"), ("OneHotEncoder", "index → sparse\nvector (Estimator)"),
              ("VectorAssembler", "all inputs → one\n\"features\" column"), ("LinearRegression", "learns weights\n(Estimator)")]
    xs = [2.2, 4.65, 7.1, 9.55]
    for (name, sub), x in zip(stages, xs):
        face = RED if name == "LinearRegression" else GREY
        box(ax, x, 1.55, 2.1, 1.2, "", face)
        ax.text(x + 1.05, 2.42, name, ha="center", va="center", color="white", fontsize=11, fontweight="bold")
        ax.text(x + 1.05, 1.92, sub, ha="center", va="center", color="white", fontsize=9.5)
    arrow(ax, (1.65, 2.15), (2.2, 2.15))
    for a, b in zip(xs[:-1], xs[1:]):
        arrow(ax, (a + 2.1, 2.15), (b, 2.15))
    ax.text(6.9, 1.12, "fit(train) → PipelineModel: every Estimator replaced by its fitted Transformer",
            ha="center", va="center", color=TEXT, fontsize=10.5)
    ax.text(6.9, 0.35, "model.transform(test) adds a \"prediction\" column — same indexes, same encoding as in training",
            ha="center", va="center", color=RED, fontsize=11)
    save(fig, "spark-ml-pipeline.png")


if __name__ == "__main__":
    architecture()
    yearly()
    ml_pipeline()
