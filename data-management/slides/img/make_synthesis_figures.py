"""Draw the course map for session 20 (project presentations and exam Q&A).

Run from the Lectures folder: python data-management/slides/img/make_synthesis_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
The map summarises the four parts of the course (SESSION_PLAN.md) and the
milestones of the design project (session 4).
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
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, fc="white", ec=GREY, lw=1.3, r=1.2, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw, linestyle=ls))


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.6):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                                 color=color, lw=lw, shrinkA=0, shrinkB=0))


def milestone(ax, x, y, label, w=17):
    box(ax, x - w / 2, y - 2.6, w, 5.2, fc=RED, ec=RED, r=1.0)
    ax.text(x, y, label, ha="center", va="center", fontsize=8.5, weight="bold", color="white")


def course_map():
    """Four parts as columns: question, sessions, result; the project milestones below."""
    fig, ax = canvas(18, 8.4)
    W, GAP, X0 = 38, 6.5, 2
    xs = [X0 + i * (W + GAP) for i in range(4)]
    parts = [
        ("Part A · Foundations", "How do we describe the data?",
         [("1–2", "data, information, data types, lifecycle"),
          ("3–4", "ER model, weak entities, specialisation"),
          ("5", "relational model, keys, mapping"),
          ("6", "functional dependencies, 1NF–BCNF")],
         "a normalised schema"),
        ("Part B · SQL and databases", "How do we store and query it?",
         [("7–8", "DDL, constraints, DML, SELECT, NULL"),
          ("9", "inner, outer and self joins"),
          ("10", "GROUP BY, subqueries, views, ACID"),
          ("11", "NoSQL: CAP, BASE, four store types")],
         "a database that answers questions"),
        ("Part C · Quality and access", "How do we get good data in?",
         [("13", "quality dimensions, rules, metrics"),
          ("14", "cleaning with pandas"),
          ("15", "files and REST APIs"),
          ("16", "ETL and ELT, pipelines, monitoring")],
         "clean, integrated data"),
        ("Part D · Storage and rules", "Where does it live, who may use it?",
         [("17", "data warehouse, star schema, OLAP"),
          ("18", "lake, lakehouse, mesh, fabric, cloud"),
          ("19", "GDPR, Data Act, DGA, AI Act, licences"),
          ("19", "governance: owner, steward, CDO")],
         "data the organisation can use"),
    ]
    top = 80
    for x, (title, question, rows, result) in zip(xs, parts):
        # header
        box(ax, x, top - 11, W, 11, fc=GREY, ec=GREY)
        ax.text(x + W / 2, top - 3.6, title, ha="center", va="center", fontsize=10.5,
                weight="bold", color="white")
        ax.text(x + W / 2, top - 8.0, question, ha="center", va="center", fontsize=8.8,
                color="white", style="italic")
        # session rows
        y = top - 15
        for sess, text in rows:
            box(ax, x, y - 8, W, 8, fc=LIGHT, ec=BORDER, lw=1.0, r=0.8)
            ax.text(x + 2, y - 4, sess, ha="left", va="center", fontsize=8.5, color=MUTED,
                    weight="bold")
            ax.text(x + 8.5, y - 4, text, ha="left", va="center", fontsize=8.6, color=TEXT)
            y -= 9.6
        # result
        box(ax, x, y - 8.5, W, 8.5, fc="white", ec=GREY, lw=1.5)
        ax.text(x + W / 2, y - 4.25, "→ " + result, ha="center", va="center", fontsize=9.3,
                weight="bold", color=TEXT)
    # arrows between results
    yr = top - 15 - 4 * 9.6 - 4.25
    for i in range(3):
        arrow(ax, xs[i] + W + 0.4, yr, xs[i + 1] - 0.4, yr)
    # milestones under the parts
    ym = yr - 14
    ax.text(X0, ym + 6.4, "Design project", fontsize=9.5, weight="bold", color=TEXT,
            va="center")
    milestone(ax, xs[0] + W * 0.27, ym, "M1 ER model", w=16)
    milestone(ax, xs[0] + W * 0.73, ym, "M2 schema", w=16)
    milestone(ax, xs[1] + W * 0.5, ym, "M3 database + SQL", w=22)
    milestone(ax, xs[2] + W * 0.5, ym, "M4 loading + quality", w=24)
    milestone(ax, xs[3] + W * 0.26, ym, "M5 star schema", w=18)
    milestone(ax, xs[3] + W * 0.75, ym, "Presentation", w=17)
    ax.text(X0, top + 4.2, "Running example: Velo Neckar bike shop · SQLite + Jupyter"
            " · session 12: workshop · session 20: presentations and Q&A",
            ha="left", va="center", fontsize=9, color=MUTED)
    save(fig, "synthesis-course-map.png")


if __name__ == "__main__":
    course_map()
