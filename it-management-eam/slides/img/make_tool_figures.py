"""Draw the figures for session 18 (EAM tools and course synthesis).

- eamtool-metamodel.png: the twelve fact sheet types of the SAP LeanIX meta model (version 4) in four layers,
  with a simplified selection of relations around the application.
- eamtool-reports.png: one repository, four kinds of report (landscape, matrix, portfolio, roadmap), drawn as
  schematic thumbnails with example data of the fictitious Rhein-Neckar Mobil Group.
- course-synthesis.png: how the instruments of Part A (IT management) and Part B (EAM) fit together.
Own illustrations based on SAP LeanIX (n.d.) documentation pages, Krcmar (2015), Hanschke (2023) and
Ahlemann et al. (2012). They are schematic drawings, not screenshots of the product; layout, applications and
ratings are our own example.

Run from the Lectures folder: python it-management-eam/slides/img/make_tool_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
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
LIGHT, BORDER, MUTED = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"], "#" + theme.COLORS["muted"]
PINK = "#F7C6CC"  # light tint of DHBW red
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc="white", ec=GREY, tc=TEXT, size=12, bold=False, lw=1.8, pad=1.0, ls="-",
        z=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={pad}", fc=fc, ec=ec, lw=lw,
                                ls=ls, zorder=z))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=tc,
            weight="bold" if bold else "normal", linespacing=1.15, zorder=z + 1)


def line(ax, a, b, color=GREY, lw=1.5, style="-", scale=12, rad=0.0, ls="-", z=1):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, linestyle=ls, zorder=z))


def label(ax, x, y, text, size=9, color=MUTED, ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=size, color=color, style="italic", zorder=5,
            bbox=dict(fc="white", ec="none", pad=0.6))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def metamodel():
    """Four layers with the twelve fact sheet types; selected relations around the application."""
    fig, ax = canvas(13, 6.6)
    bands = [
        ("Strategy and\ntransformation", 50),
        ("Business\narchitecture", 35),
        ("Application and\ndata architecture", 20),
        ("Technical\narchitecture", 5),
    ]
    bh, x0, xw = 12, 0, 130
    for name, y in bands:
        ax.add_patch(FancyBboxPatch((x0, y), xw, bh, boxstyle="round,pad=0,rounding_size=0.8", fc=LIGHT, ec=BORDER,
                                    lw=1.0, zorder=0))
        ax.text(1.2, y + bh / 2, name, ha="left", va="center", fontsize=10.5, color=TEXT, weight="bold",
                linespacing=1.15)
    w, h = 20, 7
    cols = [30, 62, 94]
    pos = {
        "Objective": (cols[0], 52.5), "Initiative": (cols[1], 52.5), "Platform": (cols[2], 52.5),
        "Organization": (cols[0], 37.5), "Business\nCapability": (cols[1], 37.5), "Business\nContext": (cols[2], 37.5),
        "Interface": (cols[0], 22.5), "Application": (cols[1], 22.5), "Data Object": (cols[2], 22.5),
        "Provider": (cols[0], 7.5), "IT Component": (cols[1], 7.5), "Tech Category": (cols[2], 7.5),
    }
    for name, (x, y) in pos.items():
        is_app = name == "Application"
        box(ax, x, y, w, h, name, fc=RED if is_app else "white", ec=RED if is_app else GREY,
            tc="white" if is_app else TEXT, size=11, bold=is_app, lw=1.6, z=3)

    def c(name, side):
        x, y = pos[name]
        return {"t": (x + w / 2, y + h), "b": (x + w / 2, y), "l": (x, y + h / 2), "r": (x + w, y + h / 2)}[side]

    # selected relations (simplified)
    line(ax, c("Application", "t"), c("Business\nCapability", "b"))
    label(ax, cols[1] + w / 2, 33, "supports")
    line(ax, (cols[1] + 2, 29.5), (cols[0] + w - 2, 37.5))
    label(ax, 50.5, 33.3, "used or owned by")
    line(ax, (cols[1] + w - 2, 29.5), (cols[2] + 2, 37.5))
    label(ax, 83.5, 33.3, "used in")
    line(ax, c("Interface", "r"), c("Application", "l"))
    label(ax, 56, 26, "provides /\nconsumes", size=8.5)
    line(ax, c("Application", "r"), c("Data Object", "l"))
    label(ax, 88, 26, "creates,\nreads ...", size=8.5)
    line(ax, c("Application", "b"), c("IT Component", "t"))
    label(ax, cols[1] + w / 2, 18, "runs on / uses")
    line(ax, c("IT Component", "l"), c("Provider", "r"))
    label(ax, 56, 11, "offered by", size=8.5)
    line(ax, c("IT Component", "r"), c("Tech Category", "l"))
    label(ax, 88, 11, "belongs to", size=8.5)
    line(ax, c("Initiative", "b"), (cols[1] + w / 2, 44.5), ls="--")
    label(ax, cols[1] + w / 2, 47.5, "affects", size=8.5)
    line(ax, c("Objective", "r"), c("Initiative", "l"), ls="--")
    label(ax, 56, 56, "is realised by", size=8.5)
    label(ax, cols[2] + w / 2, 50.8, "groups capabilities, applications\nor technologies", size=8.5)
    ax.text(xw, 63.6, "Simplified selection of relations; own drawing, not a product screenshot", ha="right",
            va="center", fontsize=9.5, color=MUTED, style="italic")
    ax.text(0, 63.6, "12 fact sheet types (meta model v4)", ha="left", va="center", fontsize=11.5, color=TEXT,
            weight="bold")
    save(fig, "eamtool-metamodel.png")


def panel(ax, x, y, w, h, title, question):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.0", fc="white", ec=GREY, lw=1.6,
                                zorder=0))
    ax.text(x + 1.5, y + h - 2.6, title, ha="left", va="center", fontsize=12, color=RED, weight="bold")
    ax.text(x + 1.5, y + h - 6.0, question, ha="left", va="center", fontsize=9.5, color=MUTED, style="italic")


ACT, OUT, PLAN = ("white", GREY), (PINK, RED), (LIGHT, MUTED)


def reports():
    """Schematic thumbnails of four report types fed by one repository."""
    fig, ax = canvas(13, 7.6)
    # repository in the middle
    box(ax, 50, 33, 30, 9, "One repository:\nfact sheets + relations", fc=GREY, ec=GREY, tc="white", size=11,
        bold=True, z=3)
    pw, ph = 58, 31
    P = {"land": (0, 42), "matrix": (72, 42), "port": (0, 2), "road": (72, 2)}
    panel(ax, *P["land"], pw, ph, "Landscape report", "Which applications support which capability?")
    panel(ax, *P["matrix"], pw, ph, "Matrix report", "Capability x organisation: who uses what?")
    panel(ax, *P["port"], pw, ph, "Portfolio report", "Functional fit x technical fit (TIME, session 13)")
    panel(ax, *P["road"], pw, ph, "Roadmap report", "How does the landscape change over time?")
    # landscape: capabilities as columns with applications stacked
    x, y = P["land"]
    caps = [("Sales and\nticketing", [("Ticket device\nsoftware", ACT), ("Car-sharing\napp", ACT)]),
            ("Payment and\nrevenue", [("Fare\nback-end", OUT), ("Revenue sharing\ndatabase", OUT)]),
            ("Operations", [("Dispatching\nsystem", ACT), ("Workshop\nsystem", ACT)])]
    cw = 17
    for i, (cap, apps) in enumerate(caps):
        cx = x + 2 + i * (cw + 1.5)
        box(ax, cx, y + 17.5, cw, 5, cap, fc=LIGHT, ec=BORDER, size=8.5, bold=True, lw=1.0)
        for k, (a, (fc, ec)) in enumerate(apps):
            box(ax, cx + 0.8, y + 11.2 - k * 6.3, cw - 1.6, 5.4, a, fc=fc, ec=ec, size=8, lw=1.3)
    # matrix: rows capabilities, columns units
    x, y = P["matrix"]
    units = ["Bus and rail", "Car sharing", "Maintenance"]
    rows = [("Sales", [("Ticket dev.", ACT), ("Car-sh. app", ACT), None]),
            ("Revenue", [("Fare b-end", OUT), ("CS payment", ACT), None]),
            ("Finance", [("ERP B&R", OUT), ("ERP CS", OUT), ("ERP maint.", OUT)])]
    cw, rh, x1 = 14, 5.2, x + 13
    for j, u in enumerate(units):
        box(ax, x1 + j * (cw + 0.8), y + 18.2, cw, 3.8, u, fc=GREY, ec=GREY, tc="white", size=8, bold=True, lw=1)
    for i, (r, cells) in enumerate(rows):
        yy = y + 12.2 - i * (rh + 0.8)
        ax.text(x + 1.5, yy + rh / 2, r, ha="left", va="center", fontsize=8.5, color=TEXT, weight="bold")
        for j, cell in enumerate(cells):
            if cell:
                (fc, ec) = cell[1]
                box(ax, x1 + j * (cw + 0.8), yy, cw, rh, cell[0], fc=fc, ec=ec, size=8, lw=1.3)
            else:
                ax.text(x1 + j * (cw + 0.8) + cw / 2, yy + rh / 2, "–", ha="center", va="center", fontsize=10,
                        color=MUTED)
    # portfolio: 2x2 with dots
    x, y = P["port"]
    s, ox, oy = 20, x + 6, y + 2.5
    for qx in (0, 1):
        for qy in (0, 1):
            ax.add_patch(FancyBboxPatch((ox + qx * s / 2, oy + qy * s / 2), s / 2, s / 2, boxstyle="square,pad=0",
                                        fc=LIGHT if qx == qy else "white", ec=BORDER, lw=1.0))
    for n, qx, qy in [("Migrate", 0, 1), ("Invest", 1, 1), ("Eliminate", 0, 0), ("Tolerate", 1, 0)]:
        ax.text(ox + qx * s / 2 + 0.6, oy + qy * s / 2 + s / 2 - 1.3, n, fontsize=8, color=RED, weight="bold",
                va="center")
    pts = [("Car-sharing app", 0.85, 0.78), ("Fare back-end", 0.22, 0.72), ("Workshop system", 0.70, 0.25),
           ("Old intranet", 0.25, 0.12)]
    for n, px, py in pts:
        ax.plot(ox + px * s, oy + py * s, "o", ms=6, color=GREY, mec="white", mew=1)
    lx = ox + s + 3
    for k, (n, px, py) in enumerate(pts):
        ax.text(lx, oy + s - 2 - k * 4.2, f"{n}: {'Invest' if k == 0 else 'Migrate' if k == 1 else 'Tolerate' if k == 2 else 'Eliminate'}",
                fontsize=8.5, color=TEXT, va="center")
    ax.text(lx, oy + 1.5, "colour by: life cycle,\ncost, criticality ...", fontsize=8.5, color=MUTED,
            style="italic", va="center", linespacing=1.15)
    # roadmap: life-cycle bars over years
    x, y = P["road"]
    years = ["2027", "2028", "2029", "2030"]
    tx0, tw = x + 17, 9.5
    for i, yr in enumerate(years):
        ax.text(tx0 + i * tw + tw / 2, y + 21.5, yr, ha="center", va="center", fontsize=8.5, color=MUTED)
        ax.plot([tx0 + i * tw, tx0 + i * tw], [y + 2, y + 20], color=BORDER, lw=0.8, zorder=0)
    bars = [("Fare back-end", [(0, 1.5, "white", GREY, "active"), (1.5, 3.0, PINK, RED, "phase-out")]),
            ("New fare platform", [(0.8, 1.8, LIGHT, MUTED, "plan"), (1.8, 4.0, "white", GREY, "active")]),
            ("ERP bus and rail", [(0, 1.0, "white", GREY, "active"), (1.0, 2.5, PINK, RED, "phase-out")])]
    for i, (n, segs) in enumerate(bars):
        yy = y + 15 - i * 5.8
        ax.text(x + 1.5, yy + 2, n, ha="left", va="center", fontsize=8.5, color=TEXT, weight="bold")
        for a, b, fc, ec, t in segs:
            box(ax, tx0 + a * tw + 0.2, yy, (b - a) * tw - 0.4, 4, t, fc=fc, ec=ec, size=7.5, lw=1.2, pad=0.6)
    ax.text(130, 76, "Schematic thumbnails; own drawing with example data, not product screenshots", ha="right",
            va="center", fontsize=9.5, color=MUTED, style="italic")
    save(fig, "eamtool-reports.png")


def synthesis():
    """Direct and steer on top, plan-build-run in the middle, protect and assure below, repository at the base."""
    fig, ax = canvas(13, 6.8)
    W = 130
    # top band: strategy and governance
    box(ax, 0, 56, 64, 9, "Strategy and alignment\nIT strategy, alignment (2) · capabilities, business models (12)",
        fc=GREY, ec=GREY, tc="white", size=10.5, bold=True)
    box(ax, 66, 56, 64, 9, "Governance\nIT governance, COBIT, ISO/IEC 38500 (3) · architecture governance (16)",
        fc=GREY, ec=GREY, tc="white", size=10.5, bold=True)
    # middle: plan build run
    cols = [
        ("Plan", "EA foundations (10)\nLandscape planning, TIME,\nroadmap (13)\nTOGAF ADM (16)"),
        ("Build / change", "Project portfolio and\nbusiness cases (4)\nIntegration (14)\nSourcing (15)"),
        ("Run", "Service management:\nITIL 4, SVS (5)\nIncident, problem, change,\nSLA (6)"),
    ]
    cw = 38
    for i, (h, t) in enumerate(cols):
        x = 4 + i * (cw + 5)
        box(ax, x, 47, cw, 6, h, fc=RED, ec=RED, tc="white", size=11.5, bold=True)
        box(ax, x, 27, cw, 19, t, fc="white", ec=GREY, size=10)
        if i < 2:
            line(ax, (x + cw + 0.3, 50), (x + cw + 4.7, 50), color=RED, lw=2, style="-|>", scale=14)
    # controlling at the side band (spans plan-build-run)
    box(ax, 0, 20, W, 5, "IT controlling (4): costs, chargeback, KPIs, IT balanced scorecard — across plan, build, run",
        fc=LIGHT, ec=BORDER, size=10)
    # protect and assure
    prot = [("Risk and compliance (7)", "GRC, GDPR, NIS2, DORA,\nISO 31000"),
            ("Security and continuity (8)", "ISMS, ISO/IEC 27001,\nIT-Grundschutz, BIA"),
            ("Quality (9)", "ISO 9001, ISO/IEC 25010,\nCMMI")]
    pw = 42
    for i, (h, t) in enumerate(prot):
        x = i * (pw + 2)
        box(ax, x, 8.5, pw, 10, f"{h}\n{t}", fc="white", ec=MUTED, size=9.5, ls="--")
    # base: repository
    box(ax, 0, 0, W, 6.5, "Shared information base: EA repository and meta-model (11), ArchiMate views (17), "
        "EAM tool such as SAP LeanIX (18), CMDB (6)", fc=PINK, ec=RED, size=10, bold=True)
    # feedback arrow run -> plan
    line(ax, (4 + 2 * (cw + 5) + cw / 2, 26.6), (4 + cw / 2, 26.6), color=MUTED, lw=1.3, style="-|>", scale=11,
         rad=0.0, ls="--")
    label(ax, 65, 26.6, "feedback: incidents, costs, risks, technical fit", size=8.5)
    ax.text(W, 67.3, "Numbers = sessions; own illustration", ha="right", va="center", fontsize=9.5, color=MUTED,
            style="italic")
    save(fig, "course-synthesis.png")


if __name__ == "__main__":
    metamodel()
    reports()
    synthesis()
