"""Draw the figures for session 17 (EAM frameworks II: modelling and other frameworks).

- archimate-framework.png: the ArchiMate core framework as a grid of layers (strategy, business, application,
  technology with physical, implementation and migration) and aspects (passive structure, behaviour, active
  structure), with motivation elements as an extra column, filled with example element types.
- archimate-relationships.png: the eleven ArchiMate relationships in four groups with a simplified drawing of
  their line style and line ends and a reading example.
- archimate-ticketing-view.png: a layered view of the on-board ticket sale of the fictitious Rhein-Neckar Mobil
  Group (business, application and technology layer) in simplified ArchiMate notation.
- zachman-grid.png: the Zachman framework as a grid of six interrogatives (columns) and six perspectives (rows),
  with a few example cells for the on-demand bus pilot of Rhein-Neckar Mobil Group.
Own illustrations based on The Open Group (2023), ArchiMate 3.2 Specification, Zachman (1987) and Sowa and
Zachman (1992). Layout, wording, colours, icons and examples are our own and do not reproduce a figure of the
specification or of Zachman International. The layer colours follow the usual (non-normative) convention.

Run from the Lectures folder: python it-management-eam/slides/img/make_archimate_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design) plus conventional layer tints.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, BORDER, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"], "#" + theme.COLORS["muted"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]

# conventional (non-normative) ArchiMate layer tints, kept light so text stays readable
TINT = {
    "strategy": "#F8E6CC",
    "business": "#FFF6BF",
    "application": "#D5ECF8",
    "technology": "#DCF2D2",
    "impl": "#F4DDE3",
    "motivation": "#E7E0F3",
}


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


# ---------------------------------------------------------------------------------------------------------------
# small icons (drawn in the top-right corner of an element)
# ---------------------------------------------------------------------------------------------------------------

def icon(ax, kind, x, y, s=1.0, color=GREY, z=5):
    """Draw a small icon centred at (x, y); s scales it (1 = about 3 units wide)."""
    lw = 1.1
    if kind == "actor":
        ax.add_patch(Circle((x, y + 0.9 * s), 0.45 * s, fill=False, ec=color, lw=lw, zorder=z))
        ax.plot([x, x], [y + 0.45 * s, y - 0.6 * s], color=color, lw=lw, zorder=z)
        ax.plot([x - 0.7 * s, x + 0.7 * s], [y + 0.1 * s, y + 0.1 * s], color=color, lw=lw, zorder=z)
        ax.plot([x - 0.6 * s, x, x + 0.6 * s], [y - 1.3 * s, y - 0.6 * s, y - 1.3 * s], color=color, lw=lw,
                zorder=z)
    elif kind == "role":
        ax.add_patch(FancyBboxPatch((x - 1.0 * s, y - 0.45 * s), 1.7 * s, 0.9 * s,
                                    boxstyle=f"round,pad=0,rounding_size={0.44 * s}", fill=False, ec=color, lw=lw,
                                    zorder=z))
        ax.add_patch(Circle((x + 0.7 * s, y), 0.45 * s, fc="white", ec=color, lw=lw, zorder=z + 1))
    elif kind == "component":
        ax.add_patch(Rectangle((x - 0.6 * s, y - 0.8 * s), 1.5 * s, 1.6 * s, fill=False, ec=color, lw=lw,
                               zorder=z))
        for dy in (0.25, -0.45):
            ax.add_patch(Rectangle((x - 0.95 * s, y + dy * s), 0.7 * s, 0.35 * s, fc="white", ec=color, lw=lw,
                                   zorder=z + 1))
    elif kind == "interface":
        ax.add_patch(Circle((x + 0.45 * s, y), 0.45 * s, fill=False, ec=color, lw=lw, zorder=z))
        ax.plot([x - 0.9 * s, x], [y, y], color=color, lw=lw, zorder=z)
    elif kind == "process":
        ax.add_patch(Polygon([(x - 1.0 * s, y - 0.25 * s), (x + 0.2 * s, y - 0.25 * s), (x + 0.2 * s, y - 0.6 * s),
                              (x + 1.0 * s, y), (x + 0.2 * s, y + 0.6 * s), (x + 0.2 * s, y + 0.25 * s),
                              (x - 1.0 * s, y + 0.25 * s)], closed=True, fill=False, ec=color, lw=lw, zorder=z))
    elif kind == "function":
        ax.add_patch(Polygon([(x - 0.7 * s, y - 0.8 * s), (x - 0.7 * s, y + 0.4 * s), (x, y + 0.9 * s),
                              (x + 0.7 * s, y + 0.4 * s), (x + 0.7 * s, y - 0.8 * s), (x, y - 0.3 * s)],
                             closed=True, fill=False, ec=color, lw=lw, zorder=z))
    elif kind == "service":
        ax.add_patch(FancyBboxPatch((x - 0.9 * s, y - 0.4 * s), 1.8 * s, 0.8 * s,
                                    boxstyle=f"round,pad=0,rounding_size={0.39 * s}", fill=False, ec=color, lw=lw,
                                    zorder=z))
    elif kind == "event":
        ax.add_patch(Polygon([(x - 0.9 * s, y - 0.45 * s), (x + 0.5 * s, y - 0.45 * s), (x + 0.95 * s, y),
                              (x + 0.5 * s, y + 0.45 * s), (x - 0.9 * s, y + 0.45 * s), (x - 0.5 * s, y)],
                             closed=True, fill=False, ec=color, lw=lw, zorder=z))
    elif kind == "object":
        ax.add_patch(Rectangle((x - 0.9 * s, y - 0.6 * s), 1.8 * s, 1.2 * s, fill=False, ec=color, lw=lw,
                               zorder=z))
        ax.plot([x - 0.9 * s, x + 0.9 * s], [y + 0.25 * s, y + 0.25 * s], color=color, lw=lw, zorder=z)
    elif kind == "node":
        d = 0.35 * s
        ax.add_patch(Rectangle((x - 0.9 * s, y - 0.7 * s), 1.4 * s, 1.1 * s, fill=False, ec=color, lw=lw,
                               zorder=z))
        ax.plot([x - 0.9 * s, x - 0.9 * s + d, x + 0.5 * s + d, x + 0.5 * s], [y + 0.4 * s, y + 0.4 * s + d,
                y + 0.4 * s + d, y + 0.4 * s], color=color, lw=lw, zorder=z)
        ax.plot([x + 0.5 * s + d, x + 0.5 * s + d, x + 0.5 * s], [y + 0.4 * s + d, y - 0.7 * s + d, y - 0.7 * s],
                color=color, lw=lw, zorder=z)
    elif kind == "device":
        ax.add_patch(FancyBboxPatch((x - 0.8 * s, y - 0.2 * s), 1.6 * s, 1.0 * s,
                                    boxstyle=f"round,pad=0,rounding_size={0.15 * s}", fill=False, ec=color, lw=lw,
                                    zorder=z))
        ax.add_patch(Polygon([(x - 0.4 * s, y - 0.2 * s), (x + 0.4 * s, y - 0.2 * s), (x + 0.8 * s, y - 0.75 * s),
                              (x - 0.8 * s, y - 0.75 * s)], closed=True, fill=False, ec=color, lw=lw, zorder=z))
    elif kind == "network":
        ax.plot([x - 0.9 * s, x + 0.9 * s], [y, y], color=color, lw=lw, zorder=z)
        for dx in (-0.9, 0.9):
            ax.add_patch(Circle((x + dx * s, y), 0.25 * s, fc="white", ec=color, lw=lw, zorder=z + 1))
    elif kind == "sysw":
        ax.add_patch(Circle((x, y), 0.7 * s, fill=False, ec=color, lw=lw, zorder=z))
        ax.add_patch(Circle((x + 0.25 * s, y + 0.25 * s), 0.55 * s, fc="white", ec=color, lw=lw, zorder=z + 1))
    elif kind == "capability":
        for i in range(3):
            for j in range(i + 1):
                ax.add_patch(Rectangle((x - 0.9 * s + i * 0.6 * s, y - 0.7 * s + j * 0.5 * s), 0.55 * s, 0.45 * s,
                                       fill=False, ec=color, lw=0.9, zorder=z))
    elif kind == "valuestream":
        ax.add_patch(Polygon([(x - 1.0 * s, y - 0.45 * s), (x + 0.55 * s, y - 0.45 * s), (x + 1.0 * s, y),
                              (x + 0.55 * s, y + 0.45 * s), (x - 1.0 * s, y + 0.45 * s), (x - 0.6 * s, y)],
                             closed=True, fill=False, ec=color, lw=lw, zorder=z))
    elif kind == "goal":
        for r in (0.75, 0.45, 0.15):
            ax.add_patch(Circle((x, y), r * s, fill=False, ec=color, lw=0.9, zorder=z))
    elif kind == "workpackage":
        ax.add_patch(matplotlib.patches.Arc((x, y), 1.4 * s, 1.1 * s, theta1=40, theta2=330, ec=color, lw=lw,
                                            zorder=z))
        ax.annotate("", xy=(x + 0.55 * s, y + 0.35 * s), xytext=(x + 0.62 * s, y - 0.05 * s),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=6), zorder=z)
    elif kind == "plateau":
        for k, dx in enumerate((0.0, 0.3, 0.6)):
            ax.plot([x - 0.9 * s + dx * s, x + 0.3 * s + dx * s], [y + 0.4 * s - k * 0.4 * s] * 2, color=color,
                    lw=1.6, zorder=z)


def element(ax, x, y, w, h, name, kind, layer, shape="rect", size=9.5, typ=None, z=3):
    """Draw an ArchiMate-style element: rect (active structure), round (behaviour), pill (service) or
    object (passive structure with a header band)."""
    fc = TINT[layer]
    if shape == "pill":
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={h / 2 - 0.05}", fc=fc,
                                    ec=GREY, lw=1.3, zorder=z))
    elif shape == "round":
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.4", fc=fc, ec=GREY, lw=1.3,
                                    zorder=z))
    else:
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=GREY, lw=1.3, zorder=z))
        if shape == "object":
            ax.plot([x, x + w], [y + h - 2.0, y + h - 2.0], color=GREY, lw=1.1, zorder=z + 1)
    if kind and shape != "pill":
        icon(ax, kind, x + w - 2.3, y + h - 2.0, s=0.85, z=z + 2)
    ty = y + h / 2 - (0.6 if shape == "object" else 0)
    ax.text(x + w / 2 - (0.8 if shape != "pill" else 0), ty, name, ha="center", va="center", fontsize=size,
            color=TEXT, linespacing=1.1, zorder=z + 3)
    if typ:
        ax.text(x + 0.8, y + h - 1.3, typ, ha="left", va="center", fontsize=6.6, color=MUTED, style="italic",
                zorder=z + 3)


# ---------------------------------------------------------------------------------------------------------------
# relationship drawing
# ---------------------------------------------------------------------------------------------------------------

def rel(ax, a, b, kind, color=GREY, lw=1.4, z=2):
    """Draw relationship `kind` from a (source) to b (target) in simplified ArchiMate notation."""
    ls = {"realisation": (0, (4, 2)), "access": (0, (1, 1.6)), "influence": (0, (4, 2)), "flow": (0, (4, 2))}.get(
        kind, "-")
    head = {"serving": "->", "triggering": "-|>", "flow": "-|>", "access": "->", "influence": "->",
            "assignment": "-|>"}.get(kind, "-")
    if kind in ("realisation", "specialisation"):
        # hollow triangle at the target
        ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=15, color=color, lw=lw, linestyle=ls,
                                     shrinkA=0, shrinkB=0, zorder=z, fc="white"))
        return
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=head, mutation_scale=11 if head != "-" else 1, color=color,
                                 lw=lw, linestyle=ls, shrinkA=0, shrinkB=0, zorder=z))
    if kind in ("composition", "aggregation"):
        # diamond at the source (the whole)
        import math
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy)
        ux, uy = dx / d, dy / d
        px, py = -uy, ux
        L, W = 1.9, 0.75
        pts = [a, (a[0] + ux * L / 2 + px * W, a[1] + uy * L / 2 + py * W), (a[0] + ux * L, a[1] + uy * L),
               (a[0] + ux * L / 2 - px * W, a[1] + uy * L / 2 - py * W)]
        ax.add_patch(Polygon(pts, closed=True, fc=color if kind == "composition" else "white", ec=color, lw=lw,
                             zorder=z + 1))
    if kind == "assignment":
        ax.add_patch(Circle(a, 0.45, fc=color, ec=color, zorder=z + 1))


# ---------------------------------------------------------------------------------------------------------------
# figure 1: the framework
# ---------------------------------------------------------------------------------------------------------------

def framework():
    fig, ax = canvas(12.4, 7.0)
    x0, y0 = 22, 4
    cw, mw, rh = 24, 22, 11.6
    cols = ["Passive structure", "Behaviour", "Active structure"]
    rows = [
        ("Strategy", "strategy", ["Capability · value stream · resource · course of action"]),
        ("Business", "business", ["Business object ·\ncontract · product", "Business process · function ·\nservice · event",
                                  "Business actor · role ·\ninterface"]),
        ("Application", "application", ["Data object", "Application process ·\nfunction · service",
                                        "Application component ·\ninterface"]),
        ("Technology\nand physical", "technology", ["Artifact · material",
                                                    "Technology process ·\nservice", "Node · device ·\nsystem software ·\nnetwork · equipment"]),
        ("Implementation\nand migration", "impl", ["Work package · deliverable · implementation event · "
                                                   "plateau · gap"]),
    ]
    top = y0 + rh * len(rows)
    for j, c in enumerate(cols):
        ax.text(x0 + cw * j + cw / 2, top + 3, c, ha="center", va="center", fontsize=11.5, weight="bold",
                color=TEXT)
    ax.text(x0 + cw * 3 + 2 + mw / 2, top + 3, "Motivation", ha="center", va="center", fontsize=11.5,
            weight="bold", color=TEXT)
    for i, (label, layer, cells) in enumerate(rows):
        y = top - rh * (i + 1)
        ax.text(x0 - 2, y + rh / 2, label, ha="right", va="center", fontsize=11.5, weight="bold", color=TEXT,
                linespacing=1.05)
        if layer in ("strategy", "impl"):
            # these layers span the core aspects: drawn as one band
            ax.add_patch(Rectangle((x0, y + 0.6), cw * 3, rh - 1.2, fc=TINT[layer], ec=GREY, lw=1.2, zorder=1))
            text = cells[0]
            ax.text(x0 + cw * 1.5, y + rh / 2, text, ha="center", va="center", fontsize=9.6, color=TEXT,
                    zorder=3)
        else:
            for j, t in enumerate(cells):
                ax.add_patch(Rectangle((x0 + cw * j, y + 0.6), cw - 0.8, rh - 1.2, fc=TINT[layer], ec=GREY, lw=1.2,
                                       zorder=1))
                ax.text(x0 + cw * j + (cw - 0.8) / 2, y + rh / 2, t, ha="center", va="center", fontsize=9.6,
                        color=TEXT, linespacing=1.1, zorder=3)
    # motivation column spans all rows
    mx = x0 + cw * 3 + 2
    ax.add_patch(Rectangle((mx, y0 + 0.6), mw, rh * len(rows) - 1.2, fc=TINT["motivation"], ec=GREY, lw=1.2,
                           zorder=1))
    ax.text(mx + mw / 2, y0 + rh * len(rows) / 2,
            "Stakeholder\n\nDriver · assessment\n\nGoal · outcome\n\nPrinciple\n\nRequirement ·\nconstraint\n\n"
            "Meaning · value",
            ha="center", va="center", fontsize=9.8, color=TEXT, linespacing=1.05, zorder=3)
    # arrows: "is served by" between layers (left side)
    ax.annotate("", xy=(x0 - 15.5, top - 2), xytext=(x0 - 15.5, y0 + rh + 2),
                arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.8, mutation_scale=14))
    ax.text(x0 - 17.2, (top + y0 + rh) / 2, "lower layers serve\nand realise upper layers", rotation=90,
            ha="center", va="center", fontsize=9, color=RED, linespacing=1.0)
    ax.text(x0 + cw * 1.5, y0 - 2.2, "Read each row from right to left: an active structure element performs behaviour that "
            "accesses passive structure", ha="center", va="center", fontsize=9, color=MUTED, style="italic")
    save(fig, "archimate-framework.png")


# ---------------------------------------------------------------------------------------------------------------
# figure 2: relationships
# ---------------------------------------------------------------------------------------------------------------

def relationships():
    fig, ax = canvas(12.6, 7.4)
    groups = [
        ("Structural", [("composition", "Composition", "the whole consists of the part;\nthe part cannot exist alone"),
                        ("aggregation", "Aggregation", "the whole groups the part;\nthe part can belong to several"),
                        ("assignment", "Assignment", "who or what performs\nthe behaviour"),
                        ("realisation", "Realisation", "something concrete makes\nsomething abstract real")]),
        ("Dependency", [("serving", "Serving", "provides its functions to\n(arrow points to the user)"),
                        ("access", "Access", "behaviour reads or writes\na passive element"),
                        ("influence", "Influence", "affects a motivation\nelement (+/–)"),
                        ("association", "Association", "any other relation\n(may be directed)")]),
        ("Dynamic", [("triggering", "Triggering", "causes the next behaviour\n(time or cause)"),
                     ("flow", "Flow", "passes something on to\nthe next behaviour")]),
        ("Other", [("specialisation", "Specialisation", "is a kind of")]),
    ]
    col_x = [2, 66]
    placement = [(0, 70), (1, 70), (0, 32), (1, 32)]
    for (gname, items), (ci, gy) in zip(groups, placement):
        x = col_x[ci]
        ax.text(x, gy, gname + " relationships", ha="left", va="center", fontsize=12, weight="bold", color=RED)
        for k, (kind, name, expl) in enumerate(items):
            yy = gy - 6.8 - k * 7.6
            ax.text(x, yy, name, ha="left", va="center", fontsize=10.5, weight="bold", color=TEXT)
            rel(ax, (x + 15, yy), (x + 30, yy), kind, color=GREY, lw=1.5)
            ax.text(x + 33, yy, expl, ha="left", va="center", fontsize=9, color=MUTED, linespacing=1.05)
    ax.text(63, 2.5, "Simplified drawing; the source is on the left, the target on the right. In access, an arrow "
            "towards the object means write.", ha="center", va="center", fontsize=8.8, color=MUTED, style="italic")
    save(fig, "archimate-relationships.png")


# ---------------------------------------------------------------------------------------------------------------
# figure 3: layered view of the on-board ticket sale
# ---------------------------------------------------------------------------------------------------------------

def ticketing_view():
    fig, ax = canvas(12.6, 8.4)  # noqa
    # layer bands
    bands = [("Business", "business", 58, 24), ("Application", "application", 30, 26), ("Technology", "technology",
                                                                                         2, 26)]
    for label, layer, y, h in bands:
        ax.add_patch(Rectangle((0, y), 126, h, fc="white", ec=BORDER, lw=1.0, zorder=0))
        ax.text(2, y + h - 2.2, label, ha="left", va="center", fontsize=10.5, weight="bold", color=MUTED)
    W, H = 22, 8.5
    # business layer
    element(ax, 4, 68, 17, H, "Passenger", "actor", "business", typ="Business actor")
    element(ax, 30, 70, 24, 7.5, "Ticket sale\non board", None, "business", shape="pill", typ=None)
    element(ax, 63, 60, 26, H, "Sell ticket\non board", "process", "business", shape="round", typ="Business process")
    element(ax, 101, 68, 21, H, "Bus driver", "role", "business", typ="Business role")
    element(ax, 101, 59.5, 21, 7.5, "Ticket", "object", "business", shape="object", size=9.2)
    # application layer
    element(ax, 30, 44, 24, 7.5, "Fare\ncalculation", None, "application", shape="pill")
    element(ax, 98, 44, 26, 7.5, "Card payment\nauthorisation", None, "application", shape="pill")
    element(ax, 64, 43.5, 22, 7.5, "Sale record", "object", "application", shape="object", size=9.2)
    element(ax, 22, 32.5, 24, H, "Ticket device\nsoftware", "component", "application", typ="Application component")
    element(ax, 63, 32.5, 26, H, "Fare\nback-end", "component", "application", typ="Application component")
    element(ax, 98, 32.5, 26, H, "Payment provider\n(external)", "component", "application",
            typ="Application component")
    # technology layer
    element(ax, 22, 14, 24, H, "On-board\nticket device", "device", "technology", typ="Device")
    element(ax, 63, 14, 26, H, "Server in Group\nIT data centre", "node", "technology", typ="Node")
    element(ax, 98, 14, 26, H, "Mobile\nnetwork", "network", "technology", typ="Communication network")

    # relationships (source -> target)
    # business: service serves passenger; process realises service; role assigned to process; process writes ticket
    rel(ax, (30, 73.75), (21.2, 72.25), "serving")
    rel(ax, (76, 68.5), (54.3, 72.5), "realisation")
    rel(ax, (101, 70), (89, 66), "assignment")
    rel(ax, (89, 63.5), (100.8, 63.25), "access")
    # application services serve the business process
    rel(ax, (42, 51.5), (63, 62), "serving")
    rel(ax, (111, 51.5), (89.2, 60.6), "serving")
    # components realise application services; fare back-end writes the sale record
    rel(ax, (34, 41), (40, 43.8), "realisation")
    rel(ax, (111, 41), (111, 43.8), "realisation")
    rel(ax, (75, 41), (75, 43.3), "access")
    # ticket device software passes sale data to the fare back-end
    rel(ax, (46, 36.5), (62.8, 36.5), "flow")
    ax.text(54.5, 38.3, "sale data", ha="center", va="center", fontsize=7.8, color=MUTED, style="italic")
    # technology: device and server assigned to the software; the network connects device and server
    rel(ax, (34, 22.5), (34, 32.3), "assignment")
    rel(ax, (76, 22.5), (76, 32.3), "assignment")
    rel(ax, (98, 18.25), (89, 18.25), "association")
    ax.plot([111, 111, 34, 34], [14, 8, 8, 14], color=GREY, lw=1.4, zorder=2)
    ax.text(72, 6.2, "the mobile network connects the ticket devices with the data centre", ha="center",
            va="center", fontsize=7.8, color=MUTED, style="italic")
    save(fig, "archimate-ticketing-view.png")


# ---------------------------------------------------------------------------------------------------------------
# figure 4: Zachman grid
# ---------------------------------------------------------------------------------------------------------------

def zachman_grid():
    fig, ax = canvas(12.6, 6.6)
    cols = ["What\n(things, data)", "How\n(processes)", "Where\n(locations)", "Who\n(people, roles)",
            "When\n(events, timing)", "Why\n(goals, rules)"]
    rows = ["Planner\n(scope)", "Owner\n(business model)", "Designer\n(system model)", "Builder\n(technology model)",
            "Subcontractor\n(detailed parts)", "Functioning\nenterprise"]
    x0, y0, cw, rh = 20, 2, 17.2, 8.6
    top = y0 + rh * len(rows)
    for j, c in enumerate(cols):
        ax.add_patch(Rectangle((x0 + cw * j, top + 0.4), cw - 0.6, 8, fc=GREY, ec=GREY, zorder=1))
        ax.text(x0 + cw * j + (cw - 0.6) / 2, top + 4.4, c, ha="center", va="center", fontsize=9.6, color="white",
                weight="bold", linespacing=1.05, zorder=2)
    examples = {
        (0, 0): "list of business\nthings: trips,\nvehicles, fares",
        (0, 2): "two pilot\ndistricts",
        (1, 1): "process \"book an\non-demand trip\"",
        (1, 3): "dispatcher, driver,\nphone booking team",
        (2, 0): "logical data model:\ntrip request,\nvehicle position",
        (2, 4): "booking cut-off and\nservice hours",
        (3, 2): "SaaS in an EU\ncloud region;\nmobile network",
        (1, 5): "goal: rural access\nwithout a car",
    }
    for i, r in enumerate(rows):
        y = top - rh * (i + 1)
        ax.add_patch(Rectangle((2, y + 0.3), x0 - 2.6, rh - 0.6, fc=LIGHT, ec=BORDER, zorder=1))
        ax.text(2 + (x0 - 2.6) / 2, y + rh / 2, r, ha="center", va="center", fontsize=9.4, color=TEXT,
                weight="bold", linespacing=1.05, zorder=2)
        for j in range(len(cols)):
            ex = examples.get((i, j))
            ax.add_patch(Rectangle((x0 + cw * j, y + 0.3), cw - 0.6, rh - 0.6, fc="white" if not ex else "#FDE8EA",
                                   ec=RED if ex else BORDER, lw=1.3 if ex else 1.0, zorder=1))
            if ex:
                ax.text(x0 + cw * j + (cw - 0.6) / 2, y + rh / 2, ex, ha="center", va="center", fontsize=8.2,
                        color=TEXT, linespacing=1.05, zorder=2)
    save(fig, "zachman-grid.png")


if __name__ == "__main__":
    framework()
    relationships()
    ticketing_view()
    zachman_grid()
