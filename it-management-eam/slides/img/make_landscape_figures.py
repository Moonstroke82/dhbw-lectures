"""Draw the figures for session 13 (strategic planning of the IT landscape).

- eam-landscape-map.png: an as-is landscape map ("Bebauungsplan") of the fictitious Rhein-Neckar Mobil Group:
  selected level-1 capabilities x business units, with the applications in the cells, coloured by life cycle.
- eam-time-model.png: the TIME model as a 2 x 2 portfolio (technical fit x functional fit) with example
  applications of the case company.
- eam-roadmap.png: a landscape roadmap from the as-is via two transition states to the target, with
  initiatives in swimlanes.
Own illustrations based on Hanschke (2023), Weill and Vitale (1999), SAP LeanIX (n.d.) and The Open Group (2022);
applications, ratings and the layout are our own example and do not reproduce a figure from these sources.

Run from the Lectures folder: python it-management-eam/slides/img/make_landscape_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Polygon

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, BORDER, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"], "#" + theme.COLORS["muted"]
PINK = "#F7C6CC"  # light tint of DHBW red for "phase-out"
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc="white", ec=GREY, tc=TEXT, size=12, bold=False, lw=1.8, pad=1.0, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={pad}", fc=fc, ec=ec, lw=lw,
                                ls=ls))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=tc,
            weight="bold" if bold else "normal", linespacing=1.15)


def arrow(ax, a, b, color=RED, lw=1.8, style="-|>", scale=14, rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, linestyle=ls))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


# life cycle styles: fc, ec, tc, linestyle
STYLE = {
    "active": ("white", GREY, TEXT, "-"),
    "phase-out": (PINK, RED, TEXT, "-"),
    "external": (LIGHT, MUTED, TEXT, "--"),
}


def landscape_map():
    """Capabilities (rows) x business units (columns); applications in the cells."""
    fig, ax = canvas(13, 6.4)
    units = ["Bus and rail", "Car sharing", "Vehicle maintenance"]
    rows = [
        ("Customer\nmanagement", [[("ERP B&R:\nsubscriptions", "phase-out")], [("Customer\ndatabase", "active")], []],
         None),
        ("Sales and\nticketing", [[("Ticket device\nsoftware", "active"), ("Association\napp", "external")],
                                  [("Car-sharing\napp", "active")], []], None),
        ("Payment and revenue\nmanagement", [[("Fare\nback-end", "active"), ("Payment\nprovider", "external")],
                                             [("Car-sharing\npayment", "active")], []], None),
        ("Operations", [[("Dispatching\nsystem", "active")], [("Car-sharing\nback-end", "active")],
                        [("Workshop\nsystem", "active")]], None),
        ("Financial\nmanagement", [[("ERP\nbus and rail", "phase-out")], [("ERP\ncar sharing", "phase-out")],
                                   [("ERP\nmaintenance", "phase-out")]], None),
        ("Human resources\nmanagement", None, ("Payroll service (group-wide)", "external")),
    ]
    x0, colw, gap = 21, 26, 1.2
    top, rowh, rgap = 58, 7.4, 1.0
    # column headers
    for j, u in enumerate(units):
        x = x0 + j * (colw + gap)
        box(ax, x, top, colw, 4.6, u, fc=GREY, ec=GREY, tc="white", size=11.5, bold=True)
    y = top - rgap
    for label, cells, span in rows:
        y -= rowh
        ax.add_patch(FancyBboxPatch((0, y), x0 + 3 * colw + 2 * gap, rowh, boxstyle="round,pad=0,rounding_size=0.8",
                                    fc=LIGHT, ec=BORDER, lw=1.0, zorder=0))
        ax.text(1.0, y + rowh / 2, label, ha="left", va="center", fontsize=10.5, color=TEXT, weight="bold",
                linespacing=1.15)
        if span:
            fc, ec, tc, ls = STYLE[span[1]]
            box(ax, x0 + 0.8, y + 0.9, 3 * colw + 2 * gap - 1.6, rowh - 1.8, span[0], fc=fc, ec=ec, tc=tc,
                size=10.5, ls=ls, lw=1.6)
        else:
            for j, apps in enumerate(cells):
                x = x0 + j * (colw + gap)
                n = len(apps)
                if n == 0:
                    ax.text(x + colw / 2, y + rowh / 2, "–", ha="center", va="center", fontsize=12, color=MUTED)
                    continue
                aw = (colw - 1.6 - (n - 1) * 1.0) / n
                for k, (name, status) in enumerate(apps):
                    fc, ec, tc, ls = STYLE[status]
                    box(ax, x + 0.8 + k * (aw + 1.0), y + 0.9, aw, rowh - 1.8, name, fc=fc, ec=ec, tc=tc, size=9.5,
                        ls=ls, lw=1.6)
        y -= rgap
    # gap marker: mobility account
    gy = y - 6.2
    box(ax, x0 + 0.8, gy, 3 * colw + 2 * gap - 1.6, 5.0, "Mobility account and mobility app: no application yet (gap)",
        fc="white", ec=RED, tc=RED, size=10.5, ls="--", lw=1.8, bold=True)
    ax.text(1.0, gy + 2.5, "Planned\ncapability", ha="left", va="center", fontsize=10.5, color=RED, weight="bold",
            linespacing=1.15)
    # legend
    lx, ly = 107, 50
    ax.text(lx, ly + 7, "Life cycle", fontsize=11.5, color=TEXT, weight="bold", va="center")
    for k, (lab, key) in enumerate([("Active", "active"), ("Phase-out planned", "phase-out"),
                                    ("External service\nor partner", "external")]):
        fc, ec, tc, ls = STYLE[key]
        yy = ly + 1 - k * 7
        ax.add_patch(FancyBboxPatch((lx, yy - 2), 6, 4, boxstyle="round,pad=0,rounding_size=0.8", fc=fc, ec=ec,
                                    lw=1.6, ls=ls))
        ax.text(lx + 8, yy, lab, fontsize=10.5, color=TEXT, va="center", linespacing=1.15)
    ax.text(lx, 18, "Selected capabilities\nand applications;\nown example", fontsize=10, color=MUTED,
            style="italic", va="center", linespacing=1.25)
    save(fig, "eam-landscape-map.png")


def time_model():
    """2 x 2 portfolio: technical fit (x) x functional fit (y), example applications as points."""
    fig, ax = canvas(7.4, 6.6)
    x0, y0, s = 8, 8, 52  # plot area: square of side s
    quads = [
        (0, 1, "Migrate", "Move to a new platform"),
        (1, 1, "Invest", "Develop further"),
        (0, 0, "Eliminate", "Retire or consolidate"),
        (1, 0, "Tolerate", "Keep with minimal spend"),
    ]
    h = s / 2
    for qx, qy, name, desc in quads:
        fc = {("Invest"): LIGHT, "Migrate": "white", "Tolerate": "white", "Eliminate": LIGHT}[name]
        ax.add_patch(FancyBboxPatch((x0 + qx * h, y0 + qy * h), h, h, boxstyle="square,pad=0", fc=fc, ec=BORDER,
                                    lw=1.2, zorder=0))
        ax.text(x0 + qx * h + 1.5, y0 + qy * h + h - 2.2, name, fontsize=13, color=RED, weight="bold", va="center")
        ax.text(x0 + qx * h + 1.5, y0 + qy * h + h - 5.6, desc, fontsize=9.5, color=MUTED, va="center")
    arrow(ax, (x0, y0), (x0 + s + 3, y0), color=GREY, lw=1.6)
    arrow(ax, (x0, y0), (x0, y0 + s + 3), color=GREY, lw=1.6)
    ax.text(x0 + s / 2, y0 - 3.5, "Technical fit (technical fitness)", ha="center", va="center", fontsize=11,
            color=TEXT, weight="bold")
    ax.text(x0 - 3.5, y0 + s / 2, "Functional fit (business value)", ha="center", va="center", fontsize=11,
            color=TEXT, weight="bold", rotation=90)
    ax.text(x0 + 1, y0 - 1.6, "low", fontsize=9, color=MUTED, va="center")
    ax.text(x0 + s - 1, y0 - 1.6, "high", fontsize=9, color=MUTED, va="center", ha="right")
    # example applications (x, y in 0..1) — own example ratings
    apps = [
        ("Car-sharing app", 0.88, 0.76, "right"),
        ("Ticket device software", 0.62, 0.60, "left"),
        ("Fare back-end", 0.22, 0.74, "left"),
        ("ERP bus and rail", 0.16, 0.58, "left"),
        ("Workshop system", 0.62, 0.24, "left"),
        ("Revenue sharing database", 0.04, 0.20, "left"),
        ("Old intranet", 0.30, 0.10, "left"),
    ]
    for name, px, py, ha in apps:
        cx, cy = x0 + px * s, y0 + py * s
        ax.plot(cx, cy, "o", ms=8, color=GREY, mec="white", mew=1.2, zorder=3)
        ax.text(cx + (1.4 if ha == "left" else -1.4), cy, name, fontsize=9.5, color=TEXT, va="center", ha=ha,
                zorder=3)
    ax.text(x0 + s, y0 + s + 2.5, "Own example ratings for teaching", fontsize=9.5, color=MUTED, style="italic",
            va="center", ha="right")
    save(fig, "eam-time-model.png")


def roadmap():
    """Landscape roadmap: four states on top, initiatives in swimlanes over three years."""
    fig, ax = canvas(13, 6.0)
    x0, x1 = 22, 128
    span = x1 - x0
    halves = ["H1\nYear 1", "H2\nYear 1", "H1\nYear 2", "H2\nYear 2", "H1\nYear 3", "H2\nYear 3"]
    hw = span / len(halves)

    def xt(t):  # t in half-years from 0..6
        return x0 + t * hw

    # states (chevrons) on top
    states = [("As-is", 0, 1.0), ("Transition 1", 1.0, 3.0), ("Transition 2", 3.0, 5.0), ("Target", 5.0, 6.0)]
    ty, th, tip = 50, 6.5, 2.0
    for i, (name, a, b) in enumerate(states):
        xa, xb = xt(a), xt(b) - 0.6
        pts = [(xa, ty), (xb - tip, ty), (xb, ty + th / 2), (xb - tip, ty + th), (xa, ty + th)]
        if i > 0:
            pts.append((xa + tip, ty + th / 2))
        fc = RED if name == "Target" else GREY
        ax.add_patch(Polygon(pts, closed=True, fc=fc, ec=fc, lw=1.0))
        ax.text((xa + xb) / 2 + (tip / 2 if i > 0 else 0) - tip / 2, ty + th / 2, name, ha="center", va="center",
                fontsize=11, color="white", weight="bold")
    ax.text(x0 - 2, ty + th / 2, "Landscape\nstates", ha="right", va="center", fontsize=10.5, color=TEXT,
            weight="bold", linespacing=1.15)
    # time axis
    for i, hl in enumerate(halves):
        ax.text(xt(i + 0.5), 45.5, hl, ha="center", va="center", fontsize=9, color=MUTED, linespacing=1.1)
    for i in range(len(halves) + 1):
        ax.plot([xt(i), xt(i)], [4, 43], color=BORDER, lw=1.0, zorder=0)
    lanes = [
        ("Customer and\nmobility app", [("Customer master and consent", 0.2, 2.6, GREY),
                                         ("Mobility app release 1", 2.6, 4.2, RED),
                                         ("Partner offers", 4.4, 6.0, GREY)]),
        ("Integration and\ntechnology", [("API platform", 0.2, 2.2, GREY), ("Retire data centre 1", 4.2, 6.0, GREY)]),
        ("Payment and\nrevenue", [("Payment platform for all units", 1.0, 3.4, GREY),
                                  ("Revenue sharing new", 3.6, 5.2, GREY)]),
        ("ERP", [("Cloud ERP: finance", 0.6, 3.4, GREY), ("Cloud ERP: maintenance", 3.4, 5.6, GREY)]),
    ]
    ly, lh, lg = 37, 6.6, 2.4
    for i, (lane, bars) in enumerate(lanes):
        yy = ly - i * (lh + lg)
        ax.text(x0 - 2, yy + lh / 2, lane, ha="right", va="center", fontsize=10.5, color=TEXT, weight="bold",
                linespacing=1.15)
        for name, a, b, col in bars:
            box(ax, xt(a) + 0.3, yy, xt(b) - xt(a) - 0.6, lh, name, fc=col, ec=col, tc="white", size=9.5, bold=True,
                pad=0.8)
    # dependencies
    arrow(ax, (xt(2.6) - 0.3, ly + lh / 2), (xt(2.6) + 0.3, ly + lh / 2), color=TEXT, lw=1.2, scale=10)
    yi = ly - (lh + lg)
    arrow(ax, (xt(2.2) - 0.3, yi + lh), (xt(2.75), ly), color=TEXT, lw=1.4, scale=11)
    yp = ly - 2 * (lh + lg)
    arrow(ax, (xt(3.3), yp + lh), (xt(3.3), ly), color=TEXT, lw=1.4, scale=11)
    ax.text(x0, 1.0, "Red: the milestone the strategy asks for. Arrows: dependencies of the app "
            "(customer master, API platform, payment platform). Own example.",
            fontsize=9.5, color=MUTED, style="italic", va="center")
    save(fig, "eam-roadmap.png")


if __name__ == "__main__":
    landscape_map()
    time_model()
    roadmap()
