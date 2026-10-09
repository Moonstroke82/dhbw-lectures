"""Draw the ER figures for session 3 (Chen and crow's-foot notation).

Run from the Lectures folder: python data-management/slides/img/make_er_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch, Polygon, Rectangle

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT = "#" + theme.COLORS["light"]
plt.rcParams["font.family"] = "Arial"


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def entity(ax, x, y, name, w=22, h=9, weak=False):
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=GREY, lw=2))
    if weak:
        ax.add_patch(Rectangle((x - w / 2 + 1.2, y - h / 2 + 1.2), w - 2.4, h - 2.4, fc="none", ec=GREY, lw=1.2))
    ax.text(x, y, name, ha="center", va="center", fontsize=13, weight="bold", color=TEXT)


def relationship(ax, x, y, name, w=26, h=13):
    ax.add_patch(Polygon([(x - w / 2, y), (x, y + h / 2), (x + w / 2, y), (x, y - h / 2)], fc=LIGHT, ec=RED, lw=2))
    ax.text(x, y, name, ha="center", va="center", fontsize=12, color=TEXT)


def attribute(ax, x, y, name, key=False, w=24, h=7):
    ax.add_patch(Ellipse((x, y), w, h, fc="white", ec=GREY, lw=1.3))
    t = ax.text(x, y, name, ha="center", va="center", fontsize=11, color=TEXT)
    if key:
        t.set_text(name)
        ax.plot([x - len(name) * 0.75, x + len(name) * 0.75], [y - 1.8, y - 1.8], color=TEXT, lw=1)


def line(ax, a, b, label=None, at=0.5, off=(0, 2.5)):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=GREY, lw=1.5, zorder=0)
    if label:
        lx, ly = a[0] + (b[0] - a[0]) * at + off[0], a[1] + (b[1] - a[1]) * at + off[1]
        ax.text(lx, ly, label, ha="center", va="center", fontsize=13, weight="bold", color=RED)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def chen():
    fig, ax = canvas(12, 4.2)
    entity(ax, 18, 20, "Customer")
    relationship(ax, 60, 20, "places")
    entity(ax, 102, 20, "Order")
    line(ax, (29, 20), (47, 20), "1", 0.5)
    line(ax, (73, 20), (91, 20), "N", 0.5)
    for (x, y, n, k) in [(13, 36, "customer_no", True), (38, 36, "name", False), (18, 4, "e-mail", False)]:
        attribute(ax, x, y, n, k)
        line(ax, (18, 20), (x, y))
    for (x, y, n, k) in [(82, 36, "order_no", True), (107, 36, "order_date", False), (102, 4, "total", False)]:
        attribute(ax, x, y, n, k)
        line(ax, (102, 20), (x, y))
    entity(ax, 18, 20, "Customer")
    entity(ax, 102, 20, "Order")
    save(fig, "er-chen.png")


def crow_end(ax, x, y, direction, many, optional):
    """Draw a crow's-foot end at (x, y); direction +1 = line comes from the left."""
    d = direction
    if many:
        for dy in (-3, 0, 3):
            ax.plot([x - d * 5, x], [y, y + dy], color=GREY, lw=1.5)
    else:
        ax.plot([x - d * 3, x - d * 3], [y - 3, y + 3], color=GREY, lw=1.5)
    mx = x - d * 8
    if optional:
        ax.add_patch(Ellipse((mx - d * 1.5, y), 3, 3, fc="white", ec=GREY, lw=1.5, zorder=3))
    else:
        ax.plot([mx, mx], [y - 3, y + 3], color=GREY, lw=1.5)


def table(ax, x, y, name, attrs, w=34):
    rh = 6
    h = rh * (len(attrs) + 1)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="square,pad=0", fc="white", ec=GREY, lw=2))
    ax.add_patch(Rectangle((x, y - rh), w, rh, fc=GREY, ec=GREY, lw=2))
    ax.text(x + w / 2, y - rh / 2, name, ha="center", va="center", fontsize=12, weight="bold", color="white")
    for i, (a, key) in enumerate(attrs):
        ax.text(x + 2, y - rh * (i + 1.5), ("PK  " if key else "      ") + a, ha="left", va="center",
                fontsize=11, color=TEXT, weight="bold" if key else "normal")
    return y - rh * 1.5


def crowsfoot():
    fig, ax = canvas(12, 3.6)
    ly = table(ax, 4, 32, "Customer", [("customer_no", True), ("name", False), ("e-mail", False)])
    table(ax, 82, 32, "Order", [("order_no", True), ("order_date", False), ("total", False)])
    ax.plot([38, 82], [ly, ly], color=GREY, lw=1.5)
    crow_end(ax, 38, ly, -1, many=False, optional=False)  # exactly one customer
    crow_end(ax, 82, ly, +1, many=True, optional=True)    # zero or many orders
    ax.text(60, ly + 4, "places", ha="center", va="bottom", fontsize=12, style="italic", color=TEXT)
    save(fig, "er-crowsfoot.png")


def crow_legend():
    fig, ax = canvas(12, 2.4)
    items = [("exactly one", False, False), ("zero or one", False, True), ("one or many", True, False), ("zero or many", True, True)]
    for i, (lab, many, opt) in enumerate(items):
        x0 = 4 + i * 30
        ax.plot([x0, x0 + 20], [14, 14], color=GREY, lw=1.5)
        crow_end(ax, x0 + 20, 14, +1, many, opt)
        if not many:
            ax.plot([x0 + 20 - 3, x0 + 20 - 3], [11, 17], color=GREY, lw=1.5)
        ax.text(x0 + 10, 4, lab, ha="center", va="center", fontsize=12, color=TEXT)
    save(fig, "er-crowsfoot-legend.png")


if __name__ == "__main__":
    chen()
    crowsfoot()
    crow_legend()
