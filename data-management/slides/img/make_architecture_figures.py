"""Draw the figures for session 18 (modern data architectures).

Run from the Lectures folder: python data-management/slides/img/make_architecture_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

arch-evolution.png: own illustration of three architectures (data warehouse, data lake plus
warehouse, lakehouse), based on Armbrust et al. (2021) and Serra (2024, Chapters 10 and 12).
arch-medallion.png: own illustration of the bronze, silver and gold layers with the bike shop
tables of sessions 15-17, based on Databricks (n.d.) and Armbrust et al. (2021).
arch-mesh.png: own illustration of a central data platform vs. a data mesh, based on
Dehghani (2020, 2022) and Serra (2024, Chapter 13).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, fill=LIGHT, edge=BORDER, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor=fill, edgecolor=edge, lw=lw))


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.8, style="-|>"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, mutation_scale=16))


def labelled(ax, x, y, w, h, title, sub="", fill=LIGHT, edge=BORDER, title_color=TEXT, lw=1.4,
             fs=11, sfs=9):
    box(ax, x, y, w, h, fill=fill, edge=edge, lw=lw)
    if sub:
        ax.text(x + w / 2, y + h * 0.66, title, ha="center", va="center", fontsize=fs,
                weight="bold", color=title_color)
        ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=sfs,
                color=MUTED)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=fs,
                weight="bold", color=title_color)


def evolution():
    """Three lanes: warehouse, lake + warehouse (two tiers), lakehouse."""
    fig, ax = plt.subplots(figsize=(12.6, 7.0), dpi=200)
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    def sources(yc, labels):
        n = len(labels)
        for i, name in enumerate(labels):
            y = yc + (n - 1) * 0.22 - i * 0.44 - 0.18
            box(ax, 0.05, y, 1.55, 0.36, fill="white", edge=BORDER)
            ax.text(0.82, y + 0.18, name, ha="center", va="center", fontsize=8.8, color=TEXT)
            arrow(ax, 1.62, y + 0.18, 2.0, yc, color=MUTED, lw=1.0)

    def lane_title(y, title, sub):
        ax.text(0.05, y, title, fontsize=13.5, weight="bold", color=RED)
        ax.text(0.05 + len(title) * 0.135 + 0.25, y + 0.02, sub, fontsize=10, color=GREY,
                style="italic")

    # 1 Data warehouse
    lane_title(6.7, "1  Data warehouse", "structured data, schema-on-write (session 17)")
    yc = 5.85
    sources(yc, ["till", "web shop", "repairs"])
    labelled(ax, 2.0, yc - 0.42, 1.25, 0.84, "ETL", "clean, model")
    arrow(ax, 3.27, yc, 3.75, yc)
    labelled(ax, 3.75, yc - 0.5, 2.7, 1.0, "Data warehouse", "tables, star schemas",
             fill="white", edge=GREY, title_color=GREY, lw=1.8)
    arrow(ax, 6.47, yc, 9.33, yc)
    labelled(ax, 9.35, yc - 0.42, 3.15, 0.84, "BI and reports")
    ax.plot([0.05, 12.55], [4.85, 4.85], color=BORDER, lw=1.2)

    # 2 Lake + warehouse
    lane_title(4.5, "2  Data lake + warehouse", "two tiers: all data raw in the lake, a copy in the DWH")
    yc = 3.55
    sources(yc, ["till, web shop", "photos, PDFs", "clickstream, API"])
    labelled(ax, 2.0, yc - 0.42, 1.25, 0.84, "load", "as is")
    arrow(ax, 3.27, yc, 3.75, yc)
    labelled(ax, 3.75, yc - 0.55, 2.7, 1.1, "Data lake", "files in any format,\nschema-on-read",
             fill="white", edge=GREY, title_color=GREY, lw=1.8)
    arrow(ax, 6.47, yc + 0.25, 6.95, yc + 0.25)
    labelled(ax, 6.95, yc - 0.05, 1.0, 0.6, "ETL", fs=10)
    arrow(ax, 7.97, yc + 0.25, 8.25, yc + 0.25)
    labelled(ax, 8.25, yc - 0.1, 1.55, 0.7, "DWH", "copy", fill="white", edge=GREY,
             title_color=GREY, fs=10.5, sfs=8.5)
    arrow(ax, 9.82, yc + 0.25, 10.18, yc + 0.25)
    labelled(ax, 10.2, yc - 0.05, 2.3, 0.6, "BI and reports", fs=10)
    arrow(ax, 6.47, yc - 0.35, 10.18, yc - 0.42)
    labelled(ax, 10.2, yc - 0.72, 2.3, 0.6, "data science, ML", fs=10)
    ax.text(8.0, yc - 0.98, "two copies, two technologies, ETL in between", ha="center",
            fontsize=9.3, color=MUTED, style="italic")
    ax.plot([0.05, 12.55], [2.3, 2.3], color=BORDER, lw=1.2)

    # 3 Lakehouse
    lane_title(1.95, "3  Lakehouse", "one copy in open files + a table format with a transaction log")
    yc = 1.0
    sources(yc, ["till, web shop", "photos, PDFs", "clickstream, API"])
    labelled(ax, 2.0, yc - 0.42, 1.25, 0.84, "load", "as is")
    arrow(ax, 3.27, yc, 3.75, yc)
    box(ax, 3.75, yc - 0.75, 5.95, 1.5, fill="white", edge=GREY, lw=1.8)
    ax.text(6.72, yc + 0.5, "Lakehouse: lake storage with warehouse features", ha="center",
            va="center", fontsize=10.5, weight="bold", color=GREY)
    for i, (name, sub) in enumerate([("bronze", "raw"), ("silver", "cleaned"),
                                     ("gold", "modelled")]):
        x = 3.95 + i * 1.9
        labelled(ax, x, yc - 0.2, 1.65, 0.55, name, fs=10, fill=LIGHT)
        ax.text(x + 0.82, yc - 0.32, sub, ha="center", va="center", fontsize=8.5, color=MUTED)
        if i:
            arrow(ax, x - 0.24, yc + 0.07, x - 0.02, yc + 0.07, color=MUTED, lw=1.1)
    box(ax, 3.95, yc - 0.68, 5.55, 0.24, fill=LIGHT, edge=RED)
    ax.text(6.72, yc - 0.56, "transaction log: ACID, schema enforcement, versions", ha="center",
            va="center", fontsize=8.6, color=RED)
    arrow(ax, 9.72, yc + 0.25, 10.18, yc + 0.3)
    arrow(ax, 9.72, yc - 0.25, 10.18, yc - 0.35)
    labelled(ax, 10.2, yc + 0.05, 2.3, 0.55, "BI and reports", fs=10)
    labelled(ax, 10.2, yc - 0.65, 2.3, 0.55, "data science, ML", fs=10)
    save(fig, "arch-evolution.png")


def medallion():
    """Bronze, silver and gold with the bike shop tables of sessions 15-17."""
    fig, ax = plt.subplots(figsize=(13.0, 4.6), dpi=200)
    ax.set_xlim(0, 13.0)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    cols = [
        ("Bronze: raw", "as received, never changed", "sessions 15–16",
         ["raw_weather (API JSON)", "price list S1 (.csv)", "price list S2 (.xlsx)",
          "till export (.csv)", "damage photos (.jpg)"]),
        ("Silver: cleaned", "typed, validated, deduplicated", "sessions 14 and 16",
         ["weather_daily", "supplier_price", "till_daily", "sale_line", ""]),
        ("Gold: modelled", "ready for reports and analysis", "session 17",
         ["fact_sales", "dim_date, dim_product", "dim_weather", "revenue by bike day", ""]),
    ]
    w, gap, x0 = 3.6, 0.9, 0.2
    for i, (title, sub, sess, items) in enumerate(cols):
        x = x0 + i * (w + gap)
        edge = RED if i == 2 else GREY
        box(ax, x, 0.35, w, 3.85, fill="white", edge=edge, lw=1.8)
        ax.text(x + w / 2, 3.88, title, ha="center", va="center", fontsize=13, weight="bold",
                color=RED if i == 2 else GREY)
        ax.text(x + w / 2, 3.52, sub, ha="center", va="center", fontsize=9.5, color=MUTED,
                style="italic")
        for j, item in enumerate(items):
            if not item:
                continue
            y = 2.9 - j * 0.5
            box(ax, x + 0.25, y - 0.2, w - 0.5, 0.4, fill=LIGHT, edge=BORDER)
            ax.text(x + w / 2, y, item, ha="center", va="center", fontsize=9.5, color=TEXT,
                    family=MONO if "(" not in item and " " not in item else None)
        ax.text(x + w / 2, 0.55, sess, ha="center", va="center", fontsize=9, color=MUTED)
        if i:
            arrow(ax, x - gap + 0.08, 2.3, x - 0.08, 2.3, color=GREY, lw=2.2)
    ax.text(x0 + w + gap / 2, 2.55, "clean", ha="center", fontsize=9, color=GREY)
    ax.text(x0 + 2 * w + 1.5 * gap, 2.55, "model", ha="center", fontsize=9, color=GREY)
    ax.text(6.5, 0.05, "quality and value rise from left to right; bronze can always be "
            "reprocessed", ha="center", fontsize=9.5, color=GREY, style="italic")
    save(fig, "arch-medallion.png")


def mesh():
    """Central platform vs. data mesh."""
    fig, ax = plt.subplots(figsize=(12.6, 5.4), dpi=200)
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    domains = ["sales", "workshop", "purchasing", "rental"]

    # left: central
    ax.text(0.05, 5.1, "Central data platform", fontsize=13.5, weight="bold", color=RED)
    for i, d in enumerate(domains):
        box(ax, 0.1 + i * 1.32, 3.9, 1.2, 0.5, fill="white", edge=BORDER)
        ax.text(0.7 + i * 1.32, 4.15, d, ha="center", va="center", fontsize=9.5, color=TEXT)
        arrow(ax, 0.7 + i * 1.32, 3.88, 2.68, 3.12, color=MUTED, lw=1.1)
    labelled(ax, 1.0, 2.15, 3.4, 0.95, "central data team", "one lake / warehouse,\nall pipelines",
             fill="white", edge=GREY, title_color=GREY, lw=1.8)
    arrow(ax, 2.7, 2.13, 2.7, 1.47)
    labelled(ax, 1.0, 0.85, 3.4, 0.6, "analysts and reports", fs=10)
    ax.text(2.7, 0.45, "bottleneck: every new question waits for one team", ha="center",
            fontsize=9.3, color=MUTED, style="italic")

    ax.plot([5.75, 5.75], [0.2, 5.25], color=BORDER, lw=1.2)

    # right: mesh
    ax.text(6.0, 5.1, "Data mesh", fontsize=13.5, weight="bold", color=RED)
    for i, d in enumerate(domains):
        x = 6.05 + i * 1.62
        box(ax, x, 2.75, 1.48, 2.0, fill="white", edge=GREY, lw=1.6)
        ax.text(x + 0.74, 4.5, d + " team", ha="center", va="center", fontsize=9.5,
                weight="bold", color=GREY)
        ax.text(x + 0.74, 4.18, "owns its data", ha="center", va="center", fontsize=8.2,
                color=MUTED)
        for k in range(2):
            box(ax, x + 0.14, 3.0 + k * 0.5, 1.2, 0.38, fill=LIGHT, edge=RED)
            ax.text(x + 0.74, 3.19 + k * 0.5, "data product", ha="center", va="center",
                    fontsize=8.0, color=RED)
    box(ax, 6.05, 1.75, 6.34, 0.6, fill=LIGHT, edge=GREY, lw=1.4)
    ax.text(9.22, 2.05, "self-serve data platform (storage, pipelines, catalogue)", ha="center",
            va="center", fontsize=9.8, color=TEXT)
    box(ax, 6.05, 0.9, 6.34, 0.6, fill="white", edge=RED, lw=1.4)
    ax.text(9.22, 1.2, "federated governance: global rules, applied automatically", ha="center",
            va="center", fontsize=9.8, color=RED)
    ax.text(9.22, 0.45, "consumers use data products directly, across domains", ha="center",
            fontsize=9.3, color=MUTED, style="italic")
    save(fig, "arch-mesh.png")


if __name__ == "__main__":
    evolution()
    medallion()
    mesh()
