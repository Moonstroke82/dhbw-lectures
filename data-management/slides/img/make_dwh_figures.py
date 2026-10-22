"""Draw the figures for session 17 (data warehousing).

Run from the Lectures folder: python data-management/slides/img/make_dwh_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

dwh-inmon-kimball.png: own illustration of the two classic data warehouse architectures,
based on Inmon (2005), Kimball and Ross (2013, Chapter 1) and Serra (2024, Chapter 8).
dwh-star.png: own illustration of the bike shop star schema of session 17 (data file
bikeshop-star-session17.sql), based on Kimball and Ross (2013, Chapters 1-3).
dwh-snowflake.png: own illustration of the same schema with a snowflaked product
dimension, based on Kimball and Ross (2013, Chapter 3) and Chaudhuri and Dayal (1997).
dwh-cube.png: own illustration of a data cube with a slice, based on Chaudhuri and
Dayal (1997) and Elmasri and Navathe (2016, Chapter 29).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
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


def labelled(ax, x, y, w, h, title, sub, fill=LIGHT, edge=BORDER, title_color=TEXT, lw=1.4):
    box(ax, x, y, w, h, fill=fill, edge=edge, lw=lw)
    ax.text(x + w / 2, y + h * 0.64, title, ha="center", va="center", fontsize=11,
            weight="bold", color=title_color)
    ax.text(x + w / 2, y + h * 0.3, sub, ha="center", va="center", fontsize=9, color=MUTED)


def inmon_kimball():
    """Two lanes: enterprise warehouse first (Inmon) or dimensional marts first (Kimball)."""
    fig, ax = plt.subplots(figsize=(12.6, 5.2), dpi=200)
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 5.2)
    ax.axis("off")

    def sources(y0):
        for i, name in enumerate(["till", "web shop", "repairs"]):
            box(ax, 1.1, y0 + 1.0 - i * 0.5, 1.45, 0.4, fill="white", edge=BORDER)
            ax.text(1.82, y0 + 1.2 - i * 0.5, name, ha="center", va="center", fontsize=9.5,
                    color=TEXT)
        return y0 + 0.7

    # Inmon lane
    ax.text(0.05, 4.95, "Inmon: top-down", fontsize=14, weight="bold", color=RED)
    ym = sources(3.0)
    labelled(ax, 2.95, ym - 0.45, 1.3, 0.9, "ETL", "integrate")
    labelled(ax, 4.65, ym - 0.75, 2.5, 1.5, "Enterprise DWH", "normalised (3NF),\nall subjects",
             fill="white", edge=GREY, title_color=GREY, lw=1.8)
    for i, mart in enumerate(["sales mart", "workshop mart", "purchasing mart"]):
        y = ym + 0.45 - i * 0.6
        box(ax, 7.75, y - 0.22, 1.9, 0.46, fill=LIGHT, edge=BORDER)
        ax.text(8.7, y, mart, ha="center", va="center", fontsize=9.5, color=TEXT)
        arrow(ax, 7.17, ym, 7.73, y, color=MUTED, lw=1.2)
    labelled(ax, 10.25, ym - 0.45, 2.2, 0.9, "BI and reports", "dashboards, OLAP")
    for i in range(3):
        arrow(ax, 2.57, ym + 0.5 - i * 0.5, 2.93, ym, color=MUTED, lw=1.1)
    arrow(ax, 4.27, ym, 4.63, ym)
    arrow(ax, 9.67, ym, 10.23, ym)
    ax.text(7.15, ym - 1.22, "first: one integrated model of the whole company, then marts "
            "derived from it", ha="center", fontsize=9.5, color=GREY, style="italic")

    ax.plot([0.05, 12.55], [2.3, 2.3], color=BORDER, lw=1.2)

    # Kimball lane
    ax.text(0.05, 2.02, "Kimball: bottom-up", fontsize=14, weight="bold", color=RED)
    yk = sources(0.25)
    labelled(ax, 2.95, yk - 0.45, 1.3, 0.9, "ETL", "staging")
    for i in range(3):
        arrow(ax, 2.57, yk + 0.5 - i * 0.5, 2.93, yk, color=MUTED, lw=1.1)
    box(ax, 4.65, yk - 0.85, 5.0, 1.7, fill="white", edge=GREY, lw=1.8)
    ax.text(7.15, yk + 0.6, "Dimensional DWH = the stars together", ha="center",
            fontsize=11, weight="bold", color=GREY)
    for i, (mart, x) in enumerate([("sales star", 4.85), ("workshop star", 6.45),
                                   ("purchasing star", 8.05)]):
        box(ax, x, yk - 0.1, 1.45, 0.46, fill=LIGHT, edge=BORDER)
        ax.text(x + 0.72, yk + 0.13, mart, ha="center", va="center", fontsize=9.2, color=TEXT)
    box(ax, 4.85, yk - 0.72, 4.65, 0.42, fill=LIGHT, edge=RED)
    ax.text(7.17, yk - 0.51, "conformed dimensions: date, product, employee", ha="center",
            va="center", fontsize=9.3, color=RED)
    arrow(ax, 4.27, yk, 4.63, yk)
    labelled(ax, 10.25, yk - 0.45, 2.2, 0.9, "BI and reports", "dashboards, OLAP")
    arrow(ax, 9.67, yk, 10.23, yk)
    ax.text(7.15, yk - 1.15, "first: one business process as a star, then the next one",
            ha="center", fontsize=9.5, color=GREY, style="italic")
    save(fig, "dwh-inmon-kimball.png")


def table(ax, x, y, w, name, cols, edge=GREY, head=GREY, fs=9.6, row_h=0.34):
    """A table box: header with the name, one line per column (top-left corner at x, y)."""
    h = 0.46 + row_h * len(cols) + 0.1
    box(ax, x, y - h, w, h, fill="white", edge=edge, lw=1.6)
    ax.add_patch(FancyBboxPatch((x, y - 0.46), w, 0.46, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor=head, edgecolor=edge, lw=1.6))
    ax.text(x + w / 2, y - 0.23, name, ha="center", va="center", fontsize=10.5, weight="bold",
            color="white", family=MONO)
    for i, col in enumerate(cols):
        weight = "bold" if col.startswith("PK") else "normal"
        color = RED if col.startswith("FK") else TEXT
        ax.text(x + 0.12, y - 0.46 - row_h * (i + 0.5) - 0.04, col, ha="left", va="center",
                fontsize=fs, family=MONO, color=color, weight=weight)
    return h


def star_parts(ax, product_cols, product_name="dim_product"):
    fact = ["FK date_key", "FK product_key", "FK salesperson_key", "FK weather_key",
            "   receipt_no, line_no", "   quantity", "   revenue"]
    table(ax, 4.15, 4.45, 3.3, "fact_sales", fact, edge=RED, head=RED)
    table(ax, 0.1, 5.55, 3.0, "dim_date",
          ["PK date_key", "   full_date", "   weekday", "   day_type", "   month, quarter",
           "   year"])
    table(ax, 0.1, 2.2, 3.0, "dim_salesperson", ["PK salesperson_key", "   employee_no",
                                                 "   name"])
    table(ax, 8.5, 5.55, 3.1, product_name, product_cols)
    table(ax, 8.5, 2.2, 3.1, "dim_weather", ["PK weather_key", "   weather_type",
                                             "   bike_day", "   rule"])
    arrow(ax, 4.13, 3.65, 3.12, 4.3, color=GREY, lw=1.5, style="-")
    arrow(ax, 4.13, 2.95, 3.12, 1.6, color=GREY, lw=1.5, style="-")
    arrow(ax, 7.47, 3.65, 8.48, 4.3, color=GREY, lw=1.5, style="-")
    arrow(ax, 7.47, 2.95, 8.48, 1.6, color=GREY, lw=1.5, style="-")


def star():
    fig, ax = plt.subplots(figsize=(11.7, 5.7), dpi=200)
    ax.set_xlim(0, 11.7)
    ax.set_ylim(0, 5.7)
    ax.axis("off")
    star_parts(ax, ["PK product_key", "   product_no", "   name", "   product_group",
                    "   category"])
    ax.text(5.8, 0.75, "grain: one line on a till receipt", ha="center", fontsize=10.5,
            color=RED, style="italic")
    ax.text(5.8, 0.4, "PK = primary key   FK = foreign key to a dimension", ha="center",
            fontsize=9.5, color=MUTED)
    save(fig, "dwh-star.png")


def snowflake():
    fig, ax = plt.subplots(figsize=(15.3, 5.7), dpi=200)
    ax.set_xlim(0, 15.3)
    ax.set_ylim(0, 5.7)
    ax.axis("off")
    star_parts(ax, ["PK product_key", "   product_no", "   name", "FK group_key"])
    table(ax, 12.1, 5.2, 3.1, "dim_product_group",
          ["PK group_key", "   product_group", "   category"], edge=RED, head=GREY)
    arrow(ax, 11.62, 4.1, 12.08, 4.6, color=RED, lw=1.5, style="-")
    ax.text(5.8, 0.75, "snowflake: the product dimension is normalised into two tables",
            ha="center", fontsize=10.5, color=RED, style="italic")
    ax.text(5.8, 0.4, "one more join for every question by product group or category",
            ha="center", fontsize=9.5, color=MUTED)
    save(fig, "dwh-snowflake.png")


def cube():
    """A data cube product group x weather type x salesperson, with one slice."""
    fig, ax = plt.subplots(figsize=(10.2, 5.6), dpi=200)
    ax.set_xlim(-0.6, 10.2)
    ax.set_ylim(-0.9, 5.6)
    ax.axis("off")
    nx, ny, nz = 4, 5, 2            # weather types, product groups, salespeople
    cw, ch = 0.95, 0.72              # cell width and height on the front face
    dx, dy = 0.75, 0.5               # depth offset per salesperson
    x0, y0 = 1.9, 0.3

    def front(i, j, k):
        x = x0 + i * cw + k * dx
        y = y0 + j * ch + k * dy
        return [(x, y), (x + cw, y), (x + cw, y + ch), (x, y + ch)]

    def top(i, k):
        x = x0 + i * cw + k * dx
        y = y0 + ny * ch + k * dy
        return [(x, y), (x + cw, y), (x + cw + dx, y + dy), (x + dx, y + dy)]

    def side(j, k):
        x = x0 + nx * cw + k * dx
        y = y0 + j * ch + k * dy
        return [(x, y), (x + dx, y + dy), (x + dx, y + ch + dy), (x, y + ch)]

    slice_i = 3                     # heavy rain
    for k in range(nz - 1, -1, -1):
        for i in range(nx):
            ax.add_patch(Polygon(top(i, k), closed=True,
                                 facecolor="#F6C9CE" if i == slice_i else LIGHT,
                                 edgecolor=GREY, lw=1))
        for j in range(ny):
            ax.add_patch(Polygon(side(j, k), closed=True, facecolor="#E4E7E9",
                                 edgecolor=GREY, lw=1))
    for i in range(nx):
        for j in range(ny):
            ax.add_patch(Polygon(front(i, j, 0), closed=True,
                                 facecolor="#F6C9CE" if i == slice_i else "white",
                                 edgecolor=RED if i == slice_i else GREY,
                                 lw=1.6 if i == slice_i else 1))

    weather = ["dry and\nwarm", "dry and\ncool", "light\nrain", "heavy\nrain"]
    for i, w in enumerate(weather):
        ax.text(x0 + (i + 0.5) * cw, y0 - 0.3, w, ha="center", va="top", fontsize=9,
                color=RED if i == slice_i else TEXT)
    ax.text(x0 + nx * cw / 2, -0.85, "weather type", ha="center", fontsize=11, weight="bold",
            color=GREY)
    groups = ["E-bikes", "Bikes", "Parts", "Accessories", "Service"]
    for j, g in enumerate(groups):
        ax.text(x0 - 0.12, y0 + (j + 0.5) * ch, g, ha="right", va="center", fontsize=9.5,
                color=TEXT)
    ax.text(x0 - 1.85, y0 + ny * ch / 2, "product\ngroup", ha="center", va="center",
            fontsize=11, weight="bold", color=GREY)
    for k, s in enumerate(["Marco", "Laura"]):
        ax.text(x0 + nx * cw + (k + 1) * dx + 0.08, y0 + (k + 0.6) * dy, s, ha="left",
                va="center", fontsize=9.5, color=TEXT)
    ax.text(x0 + nx * cw + 2.2 * dx + 0.4, y0 + 1.9 * dy + 0.25, "salesperson", ha="left",
            fontsize=11, weight="bold", color=GREY)

    # legend
    lx = 7.6
    box(ax, lx, 2.3, 2.5, 2.6, fill="white", edge=BORDER)
    ax.text(lx + 0.15, 4.6, "one cell =", fontsize=10, weight="bold", color=GREY)
    ax.text(lx + 0.15, 4.25, "revenue of one product", fontsize=9.3, color=TEXT)
    ax.text(lx + 0.15, 3.95, "group, weather type and", fontsize=9.3, color=TEXT)
    ax.text(lx + 0.15, 3.65, "salesperson", fontsize=9.3, color=TEXT)
    ax.add_patch(Polygon([(lx + 0.15, 2.95), (lx + 0.45, 2.95), (lx + 0.45, 3.2),
                          (lx + 0.15, 3.2)], closed=True, facecolor="#F6C9CE", edgecolor=RED))
    ax.text(lx + 0.6, 3.07, "slice:", fontsize=9.6, weight="bold", color=RED, va="center")
    ax.text(lx + 0.15, 2.6, "weather type = heavy rain", fontsize=9.3, color=TEXT)
    save(fig, "dwh-cube.png")


if __name__ == "__main__":
    inmon_kimball()
    star()
    snowflake()
    cube()
