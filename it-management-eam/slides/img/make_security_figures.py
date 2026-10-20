"""Draw the figures for session 8 (IT-Grundschutz procedure, recovery parameters of a BIA).

Own illustrations. The IT-Grundschutz procedure is based on BSI-Standard 200-2 (BSI, 2017b); the recovery
parameters are based on ISO 22301:2019, ISO 22300:2025 and BSI-Standard 200-4 (BSI, 2023a). The layouts are
our own and do not reproduce figures from these documents.

Run from the Lectures folder: python it-management-eam/slides/img/make_security_figures.py
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
LIGHT, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(-1, w * 10 + 1)
    ax.set_ylim(-1, h * 10 + 1)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc="white", ec=GREY, tc=TEXT, size=12, bold=False, lw=1.8, pad=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={pad}", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, color=tc,
            weight="bold" if bold else "normal", linespacing=1.25)


def arrow(ax, a, b, color=RED, lw=2.2, style="-|>", scale=18, rad=0.0):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=scale, color=color, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def grundschutz():
    """Standard protection (Standard-Absicherung) as a flow of six steps with a branch to the risk analysis."""
    fig, ax = canvas(12, 3.5)
    y, h, w = 10, 15, 17.5
    steps = [
        "Scope and\nstructure\nanalysis",
        "Protection\nrequirements\n(C, I, A)",
        "Modelling\nwith modules",
        "IT-Grundschutz\ncheck",
        "Risk analysis\nfor high needs\n(200-3)",
        "Implement,\naudit,\nimprove",
    ]
    xs = [0, 20.5, 41, 61.5, 82, 102.5]
    for i, (x, s) in enumerate(zip(xs, steps)):
        if i == 4:
            box(ax, x, y, w, h, s, ec=RED, lw=2.4, size=11.5)
        elif i == 5:
            box(ax, x, y, w, h, s, fc=RED, ec=RED, tc="white", size=11.5, bold=True)
        else:
            box(ax, x, y, w, h, s, size=11.5, bold=(i == 1))
    for x in xs[:-1]:
        arrow(ax, (x + w + 0.3, y + h / 2), (x + w + 2.7, y + h / 2))
    # what each step produces
    outs = ["processes,\napplications,\nsystems, rooms", "normal / high /\nvery high", "requirements\nfrom the\nKompendium",
            "target vs.\nactual", "extra measures\nor risk\nacceptance", "PDCA cycle\n(200-1)"]
    for x, o in zip(xs, outs):
        ax.text(x + w / 2, y - 2.2, o, ha="center", va="top", fontsize=9.8, color=GREY, style="italic",
                linespacing=1.15)
    box(ax, 0, 29, 120, 5.5, "Information security policy, roles and organisation set up first (BSI-Standard 200-1)",
        fc=LIGHT, ec=BORDER, size=11.5, bold=True)
    save(fig, "grundschutz-process.png")


def recovery():
    """Performance level of a process over time: last backup, disruption, RPO, RTO, MBCO, MTPD."""
    fig, ax = plt.subplots(figsize=(11, 4.6), dpi=200)
    ax.set_xlim(-3.2, 13)
    ax.set_ylim(-1.9, 1.35)
    ax.axis("off")
    # time axis
    ax.add_patch(FancyArrowPatch((-3.1, 0), (12.8, 0), arrowstyle="-|>", mutation_scale=16, color=GREY, lw=1.6))
    ax.text(12.8, -0.12, "time", ha="right", va="top", fontsize=11, color=GREY)
    # performance curve: normal 1.0, drop to 0 at t=0, emergency level 0.45 from t=4, back to 1.0 at t=9
    xs = [-3.0, 0, 0, 4, 4, 8, 9.2, 12.5]
    ys = [1.0, 1.0, 0.04, 0.04, 0.45, 0.45, 1.0, 1.0]
    ax.plot(xs, ys, color=RED, lw=3, solid_joinstyle="miter")
    ax.text(-2.9, 1.07, "normal operation", fontsize=11, color=TEXT, va="bottom")
    ax.text(6.0, 0.52, "emergency operation", fontsize=11, color=TEXT, ha="center", va="bottom")
    ax.text(11.75, 1.07, "back to normal", fontsize=11, color=TEXT, ha="center", va="bottom")
    # MBCO level
    ax.plot([4, 12.5], [0.45, 0.45], color=GREY, lw=1.2, ls=(0, (4, 3)))
    ax.text(12.6, 0.45, "MBCO\n(minimum level)", fontsize=10.5, color=GREY, va="center", ha="left", weight="bold")
    # events
    for x, label in [(-2.2, "last\nbackup"), (0, "disruption"), (4, "emergency\nsolution runs")]:
        ax.plot([x, x], [-0.08, 0.08], color=TEXT, lw=1.6)
        ax.text(x, -0.18, label, ha="center", va="top", fontsize=10.5, color=TEXT, linespacing=1.1)
    # RPO bracket (backwards)
    def span(x0, x1, yv, label, color, bold=True):
        ax.add_patch(FancyArrowPatch((x0, yv), (x1, yv), arrowstyle="<|-|>", mutation_scale=13, color=color, lw=1.8))
        ax.text((x0 + x1) / 2, yv - 0.07, label, ha="center", va="top", fontsize=11, color=color,
                weight="bold" if bold else "normal", linespacing=1.1)
    span(-2.2, 0, -0.78, "RPO\nmax. data loss", GREY)
    span(0, 4, -0.78, "RTO\nrequired recovery time", RED)
    span(0, 10.5, -1.42, "MTPD: after this, the impact becomes unacceptable (RTO must be shorter)", TEXT,
         bold=False)
    ax.plot([10.5, 10.5], [-1.5, 0.92], color=TEXT, lw=1.2, ls=(0, (2, 2)))
    save(fig, "recovery-parameters.png")


if __name__ == "__main__":
    grundschutz()
    recovery()
