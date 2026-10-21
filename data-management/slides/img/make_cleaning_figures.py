"""Draw the figure for session 14 (data quality II: data cleaning with Python).

Run from the Lectures folder: python data-management/slides/img/make_cleaning_figures.py
Needs matplotlib and pandas. Colours from tools/theme.py (DHBW corporate design).
Data: data-management/worksheets/data/webshop-orders-session14.csv (fictional), after
fixing the decimal comma and removing the exact duplicate row (23 amounts, 1 missing).
Fences after Tukey (1977): quartiles -/+ 1.5 x IQR (pandas quantile, linear interpolation).
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import logging
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
LIGHT, MUTED, BORDER = "#" + theme.COLORS["light"], "#" + theme.COLORS["muted"], "#" + theme.COLORS["border"]
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]

DATA = HERE.parents[1] / "worksheets" / "data" / "webshop-orders-session14.csv"


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print("wrote", HERE / name)


WHITE = dict(facecolor="white", edgecolor="none", pad=1.5)


def order_outliers():
    """Order amounts on a log axis with the IQR fence and a business-rule limit."""
    orders = pd.read_csv(DATA)
    orders["amount_eur"] = pd.to_numeric(orders["amount_eur"].str.replace(",", ".", regex=False))
    orders = orders.drop_duplicates()
    x = orders["amount_eur"].dropna()
    q1, q3 = x.quantile([0.25, 0.75])
    upper = q3 + 1.5 * (q3 - q1)
    pos = x[x > 0]

    fig, ax = plt.subplots(figsize=(10, 3.6), dpi=200)
    ax.axvspan(5, upper, color=LIGHT, zorder=0)
    ax.axvline(upper, color=GREY, lw=1.5, ls="--")
    ax.axvline(5899, color=RED, lw=1.5, ls=":")
    ax.axvline(x.median(), color=GREY, lw=1.2)
    ax.axvline(x.mean(), color=GREY, lw=1.2, ls="-.")
    flagged = pos > upper
    ax.scatter(pos[~flagged], [0] * (~flagged).sum(), s=70, color=GREY, zorder=3)
    ax.scatter(pos[flagged], [0] * flagged.sum(), s=90, color=RED, zorder=3)
    for oid, val in orders.loc[orders["amount_eur"] > upper, ["order_id", "amount_eur"]].values:
        ax.annotate(f"{oid}\n{val:,.2f} €", xy=(val, 0), xytext=(val, 0.36), ha="center",
                    fontsize=10, color=TEXT, bbox=WHITE, arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
    ax.text(x.median(), -0.55, f"median\n{x.median():.2f} €", ha="center", fontsize=10, color=TEXT, bbox=dict(facecolor=LIGHT, edgecolor="none", pad=1.5))
    ax.text(x.mean(), -0.55, f"mean\n{x.mean():.2f} €", ha="center", fontsize=10, color=TEXT, bbox=WHITE)
    ax.text(upper * 1.06, 0.80, f"upper fence\nQ3 + 1.5 × IQR = {upper:.2f} €", fontsize=10, color=GREY, va="top", bbox=WHITE)
    ax.text(5899 * 1.08, -0.2, "business rule:\nmost expensive\nbike 5,899 €", fontsize=10, color=RED, va="top")
    ax.text(5.5, 0.78, "inside the fences", fontsize=10, color=MUTED, va="top")
    ax.set_xscale("log")
    ax.set_xlim(5, 30000)
    ax.set_ylim(-0.85, 0.85)
    ax.set_yticks([])
    ax.set_xticks([10, 100, 1000, 10000])
    ax.set_xticklabels(["10 €", "100 €", "1,000 €", "10,000 €"], fontsize=10, color=TEXT)
    ax.set_xlabel("Order amount (log scale); not shown: O-2021 with −34.90 € and O-2017 without amount",
                  fontsize=10, color=TEXT)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    save(fig, "cleaning-outliers.png")


if __name__ == "__main__":
    order_outliers()
