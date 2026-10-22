"""Draw the figures for session 16 (EAM frameworks I: TOGAF).

- togaf-adm-cycle.png: the phases of the TOGAF Architecture Development Method (ADM) as a cycle of boxes around
  requirements management, with the preliminary phase in front of the cycle and the three groups of phases
  (vision and definition, planning, governance of implementation and change).
- togaf-governance-flow.png: an architecture compliance review with the possible decisions of the architecture board
  (approve, approve with dispensation, rework, change the architecture), with examples of the fictitious
  Rhein-Neckar Mobil Group.
Own illustrations based on The Open Group (2022), The TOGAF Standard, 10th Edition (Architecture Development Method;
Content, Capability, and Governance). Layout, wording, colours and examples are our own and do not reproduce a figure
of the standard.

Run from the Lectures folder: python it-management-eam/slides/img/make_togaf_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).
"""
import math
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


def arrow(ax, a, b, color=RED, lw=1.8, style="-|>", scale=14, rad=0.0, ls="-", z=1):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, linestyle=ls, zorder=z))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


# (letter, name, short purpose in own words, group)
PHASES = [
    ("A", "Architecture vision", "scope, stakeholders,\nvision, approval", "def"),
    ("B", "Business\narchitecture", "capabilities, processes,\norganisation", "def"),
    ("C", "Information systems\narchitectures", "data and\napplications", "def"),
    ("D", "Technology\narchitecture", "platforms,\ninfrastructure", "def"),
    ("E", "Opportunities\nand solutions", "work packages,\ntransitions", "plan"),
    ("F", "Migration\nplanning", "roadmap, sequence,\nbudget", "plan"),
    ("G", "Implementation\ngovernance", "compliance reviews,\ncontracts", "gov"),
    ("H", "Architecture change\nmanagement", "monitor changes,\nnew cycle?", "gov"),
]


def adm_cycle():
    """Eight phases on an ellipse, clockwise from the top; requirements management in the centre."""
    fig, ax = canvas(12.2, 8.2)
    cx, cy, rx, ry = 61, 40, 46, 26
    bw, bh = 27, 12
    n = len(PHASES)
    angles = [math.pi / 2 - 2 * math.pi * i / n for i in range(n)]
    pts = [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in angles]
    # the cycle as a ring behind the boxes, with arrowheads (clockwise) in the gaps between phases
    ts = [2 * math.pi * k / 400 for k in range(401)]
    ax.plot([cx + rx * math.cos(t) for t in ts], [cy + ry * math.sin(t) for t in ts], color=RED, lw=2.0, zorder=1)
    for a in angles:
        m = a - math.pi / n
        x, y = cx + rx * math.cos(m), cy + ry * math.sin(m)
        tx, ty = rx * math.sin(m), -ry * math.cos(m)  # clockwise tangent
        d = math.hypot(tx, ty)
        tx, ty = tx / d, ty / d
        arrow(ax, (x - tx * 1.5, y - ty * 1.5), (x + tx * 1.5, y + ty * 1.5), color=RED, lw=2.0, scale=18, z=2)
    # two-way links to requirements management in the centre
    cw, ch = 28, 11
    for (px, py) in pts:
        dx, dy = px - cx, py - cy
        s_in = min(abs((cw / 2 + 0.6) / dx) if abs(dx) > 1e-6 else 9, abs((ch / 2 + 0.6) / dy) if abs(dy) > 1e-6 else 9)
        s_out = min(abs((bw / 2 + 0.6) / dx) if abs(dx) > 1e-6 else 9, abs((bh / 2 + 0.6) / dy) if abs(dy) > 1e-6 else 9)
        arrow(ax, (cx + dx * s_in, cy + dy * s_in), (px - dx * s_out, py - dy * s_out), color=BORDER, lw=1.3,
              style="<|-|>", scale=9)
    for (px, py), (letter, name, sub, grp) in zip(pts, PHASES):
        fc = LIGHT if grp == "def" else "white"
        ec = RED if grp == "gov" else GREY
        ax.add_patch(FancyBboxPatch((px - bw / 2, py - bh / 2), bw, bh, boxstyle="round,pad=0,rounding_size=1",
                                    fc=fc, ec=ec, lw=1.8, zorder=3))
        ax.text(px - bw / 2 + 2.6, py, letter, ha="center", va="center", fontsize=17, weight="bold", color=RED,
                zorder=4)
        ax.text(px + 1.8, py + 2.2, name, ha="center", va="center", fontsize=11, weight="bold", color=TEXT,
                linespacing=1.05, zorder=4)
        ax.text(px + 1.8, py - 3.6, sub, ha="center", va="center", fontsize=9.4, color=MUTED, linespacing=1.05,
                zorder=4)
    box(ax, cx - cw / 2, cy - ch / 2, cw, ch, "Requirements\nmanagement\n(continuous)", fc="white", ec=RED,
        tc=RED, size=11.5, bold=True, lw=2.0, z=3)
    # preliminary phase in front of the cycle, top left
    ax_, ay_ = pts[0]
    px0, py0 = cx - 40, ay_ + 8
    box(ax, px0 - 15, py0 - 5.5, 30, 11, "Preliminary phase\nprepare the organisation,\nprinciples, tailoring",
        fc=GREY, ec=GREY, tc="white", size=10.2, bold=True, z=3)
    arrow(ax, (px0 + 15.4, py0 - 1), (ax_ - bw / 2 - 0.6, ay_ + 2), color=GREY, lw=1.8)
    # legend
    ly = 2.5
    for k, (fc, ec, label) in enumerate([(LIGHT, GREY, "Vision and architecture definition"),
                                         ("white", GREY, "Planning the transformation"),
                                         ("white", RED, "Governing implementation and change")]):
        x = 6 + k * 39
        ax.add_patch(FancyBboxPatch((x, ly - 1.4), 4, 2.8, boxstyle="round,pad=0,rounding_size=0.4", fc=fc, ec=ec,
                                    lw=1.6, zorder=2))
        ax.text(x + 5.5, ly, label, ha="left", va="center", fontsize=11, color=TEXT)
    save(fig, "togaf-adm-cycle.png")


def governance_flow():
    """Project solution -> compliance review -> architecture board -> four outcomes."""
    fig, ax = canvas(12.5, 6.4)
    # left: inputs
    box(ax, 2, 40, 24, 13, "Project\nsolution design\ne.g. booking platform\nfor on-demand buses", fc="white",
        ec=GREY, size=9.6)
    box(ax, 2, 18, 24, 15, "Architecture\nprinciples, standards,\ntarget architecture,\nreference models",
        fc=LIGHT, ec=GREY, size=9.6)
    box(ax, 34, 29, 26, 15, "Compliance review\nchecklists by domain;\nlevel of conformance\nassessed", fc="white",
        ec=RED, tc=TEXT, size=9.8, lw=2.0)
    arrow(ax, (26.4, 46.5), (33.6, 40), color=GREY)
    arrow(ax, (26.4, 25.5), (33.6, 33), color=GREY)
    box(ax, 66, 29, 20, 15, "Architecture\nboard\ndecides", fc=GREY, ec=GREY, tc="white", size=11, bold=True)
    arrow(ax, (60.4, 36.5), (65.6, 36.5), color=RED)
    outs = [
        (55, "Approve", "build under an\narchitecture contract", RED),
        (40, "Approve with\ndispensation", "time-limited exception,\nconditions, logged", GREY),
        (25, "Rework", "change the design,\nreview again", GREY),
        (10, "Change the\narchitecture", "change request,\nPhase H", GREY),
    ]
    for y, title, sub, ec in outs:
        ax.add_patch(FancyBboxPatch((93, y - 5.5), 30, 11, boxstyle="round,pad=0,rounding_size=1", fc="white",
                                    ec=ec, lw=1.8, zorder=2))
        ax.text(101, y, title, ha="center", va="center", fontsize=9.8, weight="bold", color=TEXT, linespacing=1.05,
                zorder=3)
        ax.text(115.5, y, sub, ha="center", va="center", fontsize=8.2, color=MUTED, linespacing=1.05, zorder=3)
        arrow(ax, (86.4, 36.5), (92.6, y), color=ec if ec == RED else GREY, lw=1.6)
    ax.text(50, 6.5, "Governance log: every decision, dispensation and contract is recorded in the repository",
            ha="center", va="center", fontsize=9.2, color=MUTED, style="italic")
    save(fig, "togaf-governance-flow.png")


if __name__ == "__main__":
    adm_cycle()
    governance_flow()
