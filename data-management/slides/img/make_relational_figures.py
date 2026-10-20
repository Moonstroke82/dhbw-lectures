"""Draw the relational-model figures for session 5.

Run from the Lectures folder: python data-management/slides/img/make_relational_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

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


def note(ax, x, y, text, ha="left"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=12, color=RED, weight="bold")


def arrow(ax, a, b, color=RED, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=12, color=color, lw=1.4,
                                 connectionstyle=f"arc3,rad={rad}", zorder=4))


def anatomy():
    """A relation CUSTOMER drawn as a table, with the formal terms labelled."""
    fig, ax = canvas(12, 5.0)
    cols = ["customer_no", "name", "city"]
    widths = [26, 26, 22]
    rows = [["C-101", "Anna Berger", "Mannheim"], ["C-102", "Luca Rossi", "Heidelberg"],
            ["C-103", "Mia Schmidt", "Mannheim"]]
    x0, ytop, rh = 22, 40, 6
    # relation name
    ax.text(x0, ytop + 4, "CUSTOMER", ha="left", va="center", fontsize=13, weight="bold", color=TEXT)
    # header
    x = x0
    for c, w in zip(cols, widths):
        ax.add_patch(Rectangle((x, ytop - rh), w, rh, fc=GREY, ec=GREY, lw=1.5))
        ax.text(x + w / 2, ytop - rh / 2, c, ha="center", va="center", fontsize=11, color="white",
                weight="bold")
        x += w
    # rows
    for i, r in enumerate(rows):
        y = ytop - rh * (i + 2)
        x = x0
        for j, (v, w) in enumerate(zip(r, widths)):
            fc = LIGHT if i == 1 else "white"
            ax.add_patch(Rectangle((x, y), w, rh, fc=fc, ec=GREY, lw=1.2))
            ax.text(x + w / 2, y + rh / 2, v, ha="center", va="center", fontsize=11, color=TEXT,
                    weight="bold" if j == 0 else "normal")
            x += w
    xr = x0 + sum(widths)
    # labels
    note(ax, xr + 10, ytop - rh / 2, "attribute (column)")
    arrow(ax, (xr + 9, ytop - rh / 2), (xr - 2, ytop - rh / 2))
    note(ax, xr + 10, ytop - rh * 2.5, "tuple (row)")
    arrow(ax, (xr + 9, ytop - rh * 2.5), (xr - 2, ytop - rh * 2.5))
    note(ax, xr + 10, ytop - rh * 3.8, "cardinality = 3 tuples")
    ax.plot([xr + 3, xr + 3], [ytop - rh * 4, ytop - rh], color=RED, lw=1.2)
    ax.plot([xr + 2, xr + 4], [ytop - rh * 4, ytop - rh * 4], color=RED, lw=1.2)
    ax.plot([xr + 2, xr + 4], [ytop - rh, ytop - rh], color=RED, lw=1.2)
    ax.plot([xr + 3, xr + 9], [ytop - rh * 3.8, ytop - rh * 3.8], color=RED, lw=1.2)
    # degree
    yb = ytop - rh * 4 - 4
    ax.plot([x0, xr], [yb, yb], color=RED, lw=1.2)
    ax.plot([x0, x0], [yb - 1, yb + 1], color=RED, lw=1.2)
    ax.plot([xr, xr], [yb - 1, yb + 1], color=RED, lw=1.2)
    note(ax, (x0 + xr) / 2, yb - 3.5, "degree = 3 attributes", ha="center")
    # primary key + domain (left side)
    note(ax, 1, ytop - rh * 5.4, "primary key")
    arrow(ax, (10, ytop - rh * 5.0), (x0 + 12, ytop - rh * 4 - 0.3), rad=-0.25)
    note(ax, 1, ytop + 4, "relation name")
    arrow(ax, (17, ytop + 4), (x0 - 1, ytop + 4))
    ax.text(x0 + widths[0] + widths[1] + widths[2] / 2, ytop + 4,
            "domain of city: names of German cities", ha="center", va="center", fontsize=10.5,
            color=MUTED, style="italic")
    save(fig, "rel-anatomy.png")


def table(ax, x, y, name, attrs, w=30):
    """attrs: list of (name, kind) with kind in {'pk', 'fk', 'pkfk', ''}. Returns {attr: y_centre}."""
    rh = 5.2
    h = rh * (len(attrs) + 1)
    ax.add_patch(Rectangle((x, y - h), w, h, fc="white", ec=GREY, lw=1.8))
    ax.add_patch(Rectangle((x, y - rh), w, rh, fc=GREY, ec=GREY, lw=1.8))
    ax.text(x + w / 2, y - rh / 2, name, ha="center", va="center", fontsize=11.5, weight="bold", color="white")
    pos = {}
    for i, (a, kind) in enumerate(attrs):
        yc = y - rh * (i + 1.5)
        tag = {"pk": "PK", "fk": "FK", "pkfk": "PK, FK", "": ""}[kind]
        ax.text(x + 1.5, yc, tag, ha="left", va="center", fontsize=8.5, color=RED, weight="bold")
        ax.text(x + (10 if kind == "pkfk" else 7), yc, a, ha="left", va="center", fontsize=10.5, color=TEXT,
                weight="bold" if "pk" in kind else "normal", style="italic" if "fk" in kind else "normal")
        pos[a] = yc
    return pos


def bikeshop_part():
    """Customer - Bike - RepairJob: two 1:N relationships mapped to foreign keys."""
    fig, ax = canvas(12.5, 4.4)
    w = 30
    c = table(ax, 2, 41, "CUSTOMER", [("customer_no", "pk"), ("name", ""), ("e_mail", ""),
                                      ("street", ""), ("postcode", ""), ("city", "")], w=w)
    b = table(ax, 47, 41, "BIKE", [("frame_no", "pk"), ("brand", ""), ("model", ""), ("price", ""),
                                   ("customer_no", "fk")], w=w)
    r = table(ax, 92, 41, "REPAIR_JOB", [("job_no", "pk"), ("job_date", ""), ("description", ""),
                                         ("cost", ""), ("frame_no", "fk")], w=w)
    # FK arrows: from FK attribute to referenced PK
    arrow(ax, (47, b["customer_no"]), (2 + w, c["customer_no"]), rad=-0.25)
    arrow(ax, (92, r["frame_no"]), (47 + w, b["frame_no"]), rad=-0.25)
    save(fig, "rel-bikeshop-part.png")


if __name__ == "__main__":
    anatomy()
    bikeshop_part()
