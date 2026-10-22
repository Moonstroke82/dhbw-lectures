"""Draw the figures for session 19 (access to data: legal and organisational aspects).

Run from the Lectures folder: python data-management/slides/img/make_legal_figures.py
Needs matplotlib. Colours from tools/theme.py (DHBW corporate design).

legal-consent-check.png: own illustration of the shop's check whether a newsletter consent
in the log counts, based on Regulation (EU) 2016/679 (Art. 4(11), Art. 7(1) and (3),
Recital 32); counts from bikeshop-privacy-session19.sql. Teaching material, not legal advice.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


def box(ax, x, y, w, h, fill=LIGHT, edge=BORDER, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.1",
                                facecolor=fill, edgecolor=edge, lw=lw))


def arrow(ax, x1, y1, x2, y2, color=GREY, lw=1.8):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=16))


def consent_check():
    """A chain of three questions from 'given' to 'valid', with the accounts that drop out."""
    fig, ax = plt.subplots(figsize=(12.6, 4.0), dpi=200)
    ax.set_xlim(0, 12.6)
    ax.set_ylim(0, 3.95)
    ax.axis("off")

    # start box
    box(ax, 0.05, 2.55, 2.0, 1.25, fill="white", edge=GREY, lw=1.6)
    ax.text(1.05, 3.4, "consent 'given'", ha="center", va="center", fontsize=12, weight="bold",
            color=TEXT)
    ax.text(1.05, 2.92, "in the log:\n11 accounts", ha="center", va="center", fontsize=10,
            color=MUTED)

    questions = [
        ("Box ticked\nby the person?", "pre-ticked box is no\nconsent (Recital 32)",
         "W03, W15, W18\n(old app APP-1)"),
        ("Confirmed by\ne-mail link?", "the shop's proof of\nconsent (Art. 7(1))",
         "W08\n(not confirmed)"),
        ("Not withdrawn\nsince then?", "withdrawal stops\nit (Art. 7(3))",
         "W02, W09\n(unsubscribed)"),
    ]
    x = 2.55
    w = 2.2
    arrow(ax, 2.07, 3.17, x - 0.03, 3.17)
    for i, (q, rule, out) in enumerate(questions):
        box(ax, x, 2.55, w, 1.25, fill=LIGHT, edge=BORDER, lw=1.4)
        ax.text(x + w / 2, 3.17, q, ha="center", va="center", fontsize=11.5, weight="bold",
                color=TEXT)
        # "no" branch down
        arrow(ax, x + w / 2, 2.53, x + w / 2, 1.62, color=RED)
        ax.text(x + w / 2 + 0.1, 2.08, "no", ha="left", va="center", fontsize=10, color=RED,
                weight="bold")
        box(ax, x + 0.05, 0.12, w - 0.1, 1.48, fill="white", edge=RED, lw=1.2)
        ax.text(x + w / 2, 1.2, out, ha="center", va="center", fontsize=10, color=TEXT,
                weight="bold")
        ax.text(x + w / 2, 0.52, rule, ha="center", va="center", fontsize=9, color=MUTED)
        # "yes" branch right
        nx = x + w + 0.45
        arrow(ax, x + w + 0.02, 3.17, nx - 0.03, 3.17)
        ax.text(x + w + 0.22, 3.36, "yes", ha="center", va="bottom", fontsize=10, color=GREY,
                weight="bold")
        x = nx

    box(ax, x, 2.55, 2.0, 1.25, fill=GREY, edge=GREY, lw=1.6)
    ax.text(x + 1.0, 3.4, "valid consent", ha="center", va="center", fontsize=12,
            weight="bold", color="white")
    ax.text(x + 1.0, 2.92, "W01, W04, W05,\nW12, W14", ha="center", va="center", fontsize=10,
            color="white")
    ax.text(x + 1.0, 1.9, "5 accounts =\n5 people may get\nthe newsletter", ha="center",
            va="center", fontsize=10, color=TEXT)
    ax.text(x + 1.0, 0.75, "session 14: 9 people\nfrom the export's\nnewsletter column",
            ha="center", va="center", fontsize=9, color=MUTED, style="italic")
    save(fig, "legal-consent-check.png")


if __name__ == "__main__":
    consent_check()
