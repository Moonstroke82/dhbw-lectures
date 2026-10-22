"""Draw the normalisation figures for session 6.

Run from the Lectures folder: python data-management/slides/img/make_normalisation_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"]
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


def fd(ax, boxes, src, dst, level, color, style="-", above=True):
    """Draw one functional dependency in the style of an FD diagram.

    boxes: {attr: (x_left, width)}; src/dst: lists of attributes; level: height of the
    horizontal line above (or below) the boxes. Lines leave the determinant boxes and
    end with an arrow head on the dependent boxes.
    """
    top, bottom = 30, 22  # box edges
    y = top + level if above else bottom - level
    y0 = top if above else bottom
    xs = []
    for i, a in enumerate(src):
        x, w = boxes[a]
        xc = x + w * (0.62 if above else 0.38)
        ax.plot([xc, xc], [y0, y], color=color, lw=1.6, ls=style, zorder=3)
        xs.append(xc)
    for a in dst:
        x, w = boxes[a]
        xc = x + w * (0.38 if above else 0.62)
        ax.annotate("", xy=(xc, y0), xytext=(xc, y), zorder=4,
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=1.6, ls=style,
                                    mutation_scale=12, shrinkA=0, shrinkB=0))
        xs.append(xc)
    ax.plot([min(xs), max(xs)], [y, y], color=color, lw=1.6, ls=style, zorder=3)


def fd_diagram():
    """The repair-job spreadsheet in 1NF with its functional dependencies."""
    attrs = ["job_no", "part_no", "quantity", "price_charged", "part_name", "job_date",
             "frame_no", "model", "customer_no", "customer_name"]
    widths = [11, 11, 11, 14, 12, 11, 11, 9, 14, 16]
    fig, ax = canvas(13, 5.0)
    boxes, x = {}, 2
    for a, w in zip(attrs, widths):
        key = a in ("job_no", "part_no")
        ax.add_patch(Rectangle((x, 22), w, 8, fc=GREY if key else "white", ec="white" if key else GREY,
                               lw=1.6, zorder=2))
        ax.text(x + w / 2, 26, a, ha="center", va="center", fontsize=10.5, zorder=5,
                color="white" if key else TEXT, weight="bold" if key else "normal")
        boxes[a] = (x, w)
        x += w
    ax.text(2, 49, "REPAIR (1NF)  ·  primary key {job_no, part_no}", ha="left", va="center",
            fontsize=12, weight="bold", color=TEXT)
    # full dependency (below)
    fd(ax, boxes, ["job_no", "part_no"], ["quantity", "price_charged"], 5, GREY, above=False)
    # partial dependencies
    fd(ax, boxes, ["part_no"], ["part_name"], 10, RED, above=False)
    fd(ax, boxes, ["job_no"], ["job_date", "frame_no"], 5, RED)
    # transitive dependencies
    fd(ax, boxes, ["frame_no"], ["model", "customer_no"], 10, MUTED, style="--")
    fd(ax, boxes, ["customer_no"], ["customer_name"], 15, MUTED, style="--")
    handles = [Line2D([0], [0], color=GREY, lw=2, label="full dependency on the key"),
               Line2D([0], [0], color=RED, lw=2, label="partial dependency (violates 2NF)"),
               Line2D([0], [0], color=MUTED, lw=2, ls="--", label="via a non-key attribute (transitive, violates 3NF)")]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.0, 0.0), ncol=3, frameon=False,
              fontsize=10, handlelength=2.6)
    save(fig, "norm-fd-diagram.png")


if __name__ == "__main__":
    fd_diagram()
