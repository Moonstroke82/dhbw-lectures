"""Draw the figures for session 16 (ETL and data integration).

Run from the Lectures folder: python data-management/slides/img/make_etl_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

etl-pipeline.png: own illustration of the bike shop pipeline of session 16 (sources,
landing zone, transformation, load, target tables, run log), based on the ETL process
in Kimball and Ross (2013, Chapters 19-20) and Rahm and Do (2000).
etl-vs-elt.png: own illustration of where the transformation runs in ETL and in ELT,
based on Serra (2024, Chapter 9) and Reis and Housley (2022, Chapter 7).
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


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.8):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=16))


def stage(ax, x, y, w, h, title, lines, title_color=GREY, edge=GREY):
    box(ax, x, y, w, h, fill="white", edge=edge, lw=1.6)
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontsize=12.5,
            weight="bold", color=title_color)
    for i, line in enumerate(lines):
        ax.text(x + 0.15, y + h - 0.8 - i * 0.36, line, ha="left", va="center",
                fontsize=9.6, color=TEXT)


def etl_pipeline():
    """Sources -> extract -> landing -> transform -> load -> target, with the run log."""
    fig, ax = plt.subplots(figsize=(12, 5.4), dpi=200)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5.4)
    ax.axis("off")

    # sources
    ax.text(1.05, 5.2, "Sources", ha="center", fontsize=12.5, weight="bold", color=GREY)
    sources = [("Bright Sky API", "JSON over HTTP"), ("saved copy", "JSON file (plan B)"),
               ("price list S1", "CSV, cp1252, ;"), ("price list S2", "Excel, title rows"),
               ("till export", "CSV, German dates")]
    for i, (name, fmt) in enumerate(sources):
        y = 4.3 - i * 0.82
        box(ax, 0.05, y, 2.0, 0.66)
        ax.text(1.05, y + 0.44, name, ha="center", fontsize=10, weight="bold", color=TEXT)
        ax.text(1.05, y + 0.17, fmt, ha="center", fontsize=8.8, color=MUTED)

    # stages
    stage(ax, 2.6, 1.75, 2.05, 3.1, "1 Extract",
          ["call or read", "timeout, status", "full or", "incremental"], title_color=RED, edge=RED)
    stage(ax, 5.05, 1.75, 1.85, 3.1, "Landing",
          ["raw files,", "unchanged", "+ retrieval", "time"])
    stage(ax, 7.3, 1.75, 2.05, 3.1, "2 Transform",
          ["parse, map", "columns, keys", "aggregate", "validate"], title_color=RED, edge=RED)
    stage(ax, 9.75, 1.75, 2.2, 3.1, "3 Load",
          ["upsert in one", "transaction", "into bikeshop.db:"])
    ax.text(9.9, 2.83, "weather_daily", fontsize=9.4, family=MONO, color=TEXT)
    ax.text(9.9, 2.47, "supplier_price", fontsize=9.4, family=MONO, color=TEXT)
    ax.text(9.9, 2.11, "till_daily", fontsize=9.4, family=MONO, color=TEXT)

    for i in range(5):
        arrow(ax, 2.07, 4.63 - i * 0.82, 2.58, 3.3 + (2 - i) * 0.25, color=MUTED, lw=1.2)
    arrow(ax, 4.67, 3.3, 5.03, 3.3)
    arrow(ax, 6.92, 3.3, 7.28, 3.3)
    arrow(ax, 9.37, 3.3, 9.73, 3.3)

    # rejected rows
    box(ax, 7.3, 0.25, 2.05, 0.8, fill=LIGHT, edge=RED)
    ax.text(8.32, 0.78, "rejected rows", ha="center", va="center", fontsize=9.6, color=RED)
    ax.text(8.32, 0.45, "logged, not loaded", ha="center", va="center", fontsize=9, color=TEXT)
    arrow(ax, 8.32, 1.73, 8.32, 1.07, color=RED, lw=1.4)

    # run log and scheduler
    box(ax, 2.6, 0.05, 4.3, 1.0, fill=LIGHT, edge=GREY)
    arrow(ax, 3.6, 1.07, 3.6, 1.73, color=GREY, lw=1.4)
    ax.text(4.75, 0.75, "Scheduler", ha="center", fontsize=11, weight="bold", color=GREY)
    ax.text(4.75, 0.33, "starts the run: daily 06:15, cron / Task Scheduler", ha="center",
            fontsize=9, color=TEXT)
    box(ax, 9.75, 0.05, 2.2, 1.0, fill=LIGHT, edge=GREY)
    ax.text(10.85, 0.75, "Run log", ha="center", fontsize=11, weight="bold", color=GREY)
    ax.text(10.85, 0.33, "etl_run: status,", ha="center", fontsize=9, color=TEXT)
    ax.text(10.85, 0.12, "rows, source", ha="center", fontsize=9, color=TEXT)
    arrow(ax, 10.85, 1.73, 10.85, 1.07, color=GREY, lw=1.4)
    save(fig, "etl-pipeline.png")


def etl_vs_elt():
    """Two lanes: transformation before the load (ETL) or inside the target (ELT)."""
    fig, ax = plt.subplots(figsize=(12.9, 4.3), dpi=200)
    ax.set_xlim(0, 12.9)
    ax.set_ylim(0, 4.3)
    ax.axis("off")

    def lane(y, label, steps, target_from):
        ax.text(0.05, y + 0.45, label, fontsize=15, weight="bold", color=RED, va="center")
        x = 1.1
        for i, (title, sub) in enumerate(steps):
            inside = i >= target_from
            w = 2.0
            box(ax, x, y, w, 0.9, fill=LIGHT if inside else "white",
                edge=GREY if inside else BORDER, lw=1.4)
            ax.text(x + w / 2, y + 0.6, title, ha="center", fontsize=11, weight="bold", color=TEXT)
            ax.text(x + w / 2, y + 0.25, sub, ha="center", fontsize=9, color=MUTED)
            if i < len(steps) - 1:
                arrow(ax, x + w + 0.02, y + 0.45, x + w + 0.38, y + 0.45)
            x += w + 0.4
        return x

    lane(2.75, "ETL", [("Source", "API, files"), ("Extract", "Python"),
                       ("Transform", "pandas, outside"), ("Load", "clean rows only"),
                       ("Target", "tables")], target_from=4)
    lane(0.75, "ELT", [("Source", "API, files"), ("Extract", "Python"),
                       ("Load", "raw, unchanged"), ("Transform", "SQL, inside"),
                       ("Target", "tables, views")], target_from=2)
    # database brackets
    ax.plot([10.7, 12.7], [2.6, 2.6], color=GREY, lw=2)
    ax.text(11.7, 2.4, "inside the database", ha="center", fontsize=9.5, color=GREY)
    ax.plot([5.9, 12.7], [0.6, 0.6], color=GREY, lw=2)
    ax.text(9.3, 0.38, "inside the database", ha="center", fontsize=9.5, color=GREY)
    save(fig, "etl-vs-elt.png")


if __name__ == "__main__":
    etl_pipeline()
    etl_vs_elt()
