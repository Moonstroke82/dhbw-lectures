"""Draw the NoSQL figures for session 11.

Run from the Lectures folder: python data-management/slides/img/make_nosql_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
The examples use the course sample data (bikeshop-data.sql); the two-server
online shop in the CAP figure is a fictional extension of the case.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
MONO = "DejaVu Sans Mono"


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


def box(ax, x, y, w, h, fc="white", ec=GREY, lw=1.3, r=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                fc=fc, ec=ec, lw=lw))


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.4, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=12,
                                 color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0))


def server(ax, x, y, name, stock, stale=False):
    """A replica: a box with a name and the stored stock value."""
    box(ax, x, y, 26, 15, fc=LIGHT)
    ax.text(x + 13, y + 11, name, ha="center", va="center", fontsize=10.5, weight="bold", color=TEXT)
    ax.text(x + 13, y + 5, f"GZT886 in stock: {stock}", ha="center", va="center", fontsize=9.5,
            color=RED if stale else TEXT, weight="bold" if stale else "normal")


def cap_partition():
    """Two replicas of an online shop, a network partition, and the choice between C and A."""
    fig, ax = canvas(14, 5.6)
    # left: the situation
    ax.text(2, 53, "1  The network between the two servers fails (partition)", fontsize=11,
            weight="bold", color=TEXT, va="center")
    server(ax, 4, 22, "Server A", "0")
    server(ax, 46, 22, "Server B", "1", stale=True)
    # broken replication link
    ax.plot([30, 37], [29.5, 29.5], color=GREY, lw=1.6)
    ax.plot([39, 46], [29.5, 29.5], color=GREY, lw=1.6)
    ax.plot([36, 38, 37, 40], [33, 30.5, 28.5, 26], color=RED, lw=2.4)
    ax.text(38, 36.5, "replication\ninterrupted", ha="center", va="bottom", fontsize=9, color=RED,
            linespacing=1.1)
    # clients
    ax.text(17, 46, "Customer 1 buys the\nlast GZT886", ha="center", va="center", fontsize=9.5,
            color=TEXT, linespacing=1.2)
    arrow(ax, 17, 41.5, 17, 37.5)
    ax.text(59, 46, "Customer 2 asks:\nis GZT886 available?", ha="center", va="center", fontsize=9.5,
            color=TEXT, linespacing=1.2)
    arrow(ax, 59, 41.5, 59, 37.5)
    ax.text(38, 13, "Server B cannot know about the sale.", ha="center", va="center", fontsize=9.5,
            color=MUTED, style="italic")
    ax.plot([80, 80], [4, 56], color=BORDER, lw=1.2, ls=(0, (3, 3)))

    # right: the two options
    ax.text(84, 53, "2  Server B must choose", fontsize=11, weight="bold", color=TEXT, va="center")
    box(ax, 84, 29, 54, 18, fc="white", ec=GREY)
    ax.text(87, 42.5, "Consistency first (CP)", fontsize=10.5, weight="bold", color=GREY, va="center")
    ax.text(87, 35, "refuse or wait: \"Availability cannot be\nconfirmed, please try again later\"",
            fontsize=9.5, color=TEXT, va="center", linespacing=1.25)
    box(ax, 84, 6, 54, 18, fc="white", ec=RED)
    ax.text(87, 19.5, "Availability first (AP)", fontsize=10.5, weight="bold", color=RED, va="center")
    ax.text(87, 12, "answer with its own data: \"1 in stock\"\n(possibly stale; reconcile later)",
            fontsize=9.5, color=TEXT, va="center", linespacing=1.25)
    save(fig, "cap-partition.png")


def nosql_models():
    """The four NoSQL families, each with a small bike-shop example."""
    fig, ax = canvas(14, 7.4)
    panels = [(1, 38, "Key-value store"), (71, 38, "Document store"),
              (1, 1, "Column-family store"), (71, 1, "Graph database")]
    for x, y, title in panels:
        box(ax, x, y, 68, 34, fc="white", ec=BORDER, lw=1.2)
        ax.text(x + 2.5, y + 30.5, title, fontsize=12, weight="bold", color=GREY, va="center")

    # key-value: key -> opaque value
    x, y = 1, 38
    rows = [("cart:101", "P-111 x1; P-101 x2"), ("session:7f3a", "(serialised login data)"),
            ("price:P-109", "649.00")]
    ax.text(x + 4, y + 24.5, "key", fontsize=9.5, color=MUTED, weight="bold")
    ax.text(x + 30, y + 24.5, "value (opaque to the store)", fontsize=9.5, color=MUTED, weight="bold")
    for i, (k, v) in enumerate(rows):
        yy = y + 17 - i * 6.5
        ax.add_patch(Rectangle((x + 3, yy), 20, 5, fc=LIGHT, ec=GREY, lw=1.0))
        ax.text(x + 13, yy + 2.5, k, ha="center", va="center", fontsize=9, family=MONO, color=TEXT)
        arrow(ax, x + 24, yy + 2.5, x + 28, yy + 2.5)
        ax.add_patch(Rectangle((x + 29, yy), 36, 5, fc="#333333", ec="#333333", lw=1.0))
        ax.text(x + 47, yy + 2.5, v, ha="center", va="center", fontsize=8.5, family=MONO, color="white")

    # document: JSON with embedded parts
    x, y = 71, 38
    doc = ('{ "job_no": 511, "date": "2027-04-06",\n'
           '  "bike":  { "brand": "Trek",\n'
           '             "owner": { "name": "Tobias Krämer" } },\n'
           '  "lines": [ { "part": "Chain 11-speed", "price": 39.9 },\n'
           '             { "part": "Brake cable",    "price": 4.5 }, … ],\n'
           '  "mechanics": [ "Katrin Vogel", "Deniz Arslan" ] }')
    ax.add_patch(Rectangle((x + 3, y + 3), 62, 24, fc=LIGHT, ec=GREY, lw=1.0))
    ax.text(x + 5, y + 15, doc, ha="left", va="center", fontsize=7.9, family=MONO, color=TEXT,
            linespacing=1.45)

    # column-family: row key, two families, sparse columns
    x, y = 1, 1
    ax.text(x + 3, y + 25, "row key", fontsize=9, color=MUTED, weight="bold")
    ax.text(x + 19, y + 25, "family: profile", fontsize=9, color=MUTED, weight="bold")
    ax.text(x + 43, y + 25, "family: visits", fontsize=9, color=MUTED, weight="bold")
    crow = [("cust:101", ["name=Anna Berger", "city=Mannheim"], ["2027-01-12", "2027-04-07"]),
            ("cust:106", ["name=Felix Wagner"], []),
            ("cust:110", ["name=Tobias Krämer", "city=Mannheim"], ["2027-04-06"])]
    for i, (k, prof, vis) in enumerate(crow):
        yy = y + 16 - i * 6.8
        ax.add_patch(Rectangle((x + 3, yy), 14, 5.5, fc=GREY, ec=GREY, lw=1.0))
        ax.text(x + 10, yy + 2.75, k, ha="center", va="center", fontsize=8.5, family=MONO, color="white")
        ax.add_patch(Rectangle((x + 18, yy), 23, 5.5, fc=LIGHT, ec=GREY, lw=1.0))
        ax.text(x + 19, yy + 2.75, "  ".join(prof) if len(prof) == 1 else "\n".join(prof), ha="left",
                va="center", fontsize=7.3, family=MONO, color=TEXT, linespacing=1.1)
        ax.add_patch(Rectangle((x + 42, yy), 23, 5.5, fc=LIGHT, ec=GREY, lw=1.0))
        ax.text(x + 43, yy + 2.75, "\n".join(vis) if vis else "(no columns)", ha="left", va="center",
                fontsize=7.3, family=MONO, color=TEXT if vis else MUTED, linespacing=1.1)

    # graph: nodes and labelled edges
    x, y = 71, 1
    nodes = {"Katrin\nVogel": (x + 14, y + 20), "Deniz\nArslan": (x + 14, y + 7),
             "Tim\nKrause": (x + 40, y + 7), "Job 511": (x + 40, y + 20), "TRK312": (x + 59, y + 20)}
    edges = [("Deniz\nArslan", "Katrin\nVogel", "SUPERVISED_BY"), ("Tim\nKrause", "Deniz\nArslan", "SUPERVISED_BY"),
             ("Katrin\nVogel", "Job 511", "WORKED_ON"), ("Deniz\nArslan", "Job 511", "WORKED_ON"),
             ("Job 511", "TRK312", "REPAIRS")]
    for a, b, lab in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        ux, uy = (x2 - x1) / d, (y2 - y1) / d
        ax.add_patch(FancyArrowPatch((x1 + 4.6 * ux, y1 + 4.6 * uy), (x2 - 4.6 * ux, y2 - 4.6 * uy),
                                     arrowstyle="-|>", mutation_scale=11, color=GREY, lw=1.3,
                                     shrinkA=0, shrinkB=0, zorder=1))
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mx, my, lab, ha="center", va="center", fontsize=6.8, color=RED, weight="bold",
                bbox=dict(fc="white", ec="none", pad=0.6), zorder=2)
    for name, (cx, cy) in nodes.items():
        ax.add_patch(Circle((cx, cy), 4.6, fc=LIGHT, ec=GREY, lw=1.3, zorder=3))
        ax.text(cx, cy, name, ha="center", va="center", fontsize=7.6, color=TEXT, zorder=4,
                linespacing=1.0)
    save(fig, "nosql-models.png")


if __name__ == "__main__":
    cap_partition()
    nosql_models()
