"""Draw the figures for session 12 (time series forecasting I).

Run from the Lectures folder: python data-analytics/slides/img/make_fc_figures.py
Needs matplotlib, pandas, statsmodels and scikit-learn, and an internet connection:
the script downloads the lab dataset (vic_elec from the R package tsibbledata,
O'Hara-Wild et al., 2022) from the Rdatasets copy on GitHub, pinned to one commit,
and prepares the daily series exactly as in session 11 (local days, daily mean).
Colours from tools/theme.py (DHBW corporate design).

Tested with pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1, NumPy 2.5.4 and
matplotlib 3.11.2. The cross-validation refits ETS and SARIMA 26 times (about a minute).

- fc-baselines.png: four baseline forecasts for 14 days from the origin 13 August 2014.
- fc-tscv.png: time series cross-validation with an expanding window (26 folds of 14 days).
- fc-folds.png: MAE per fold for seasonal naive, ETS(M,N,M) and SARIMA(2,0,2)(0,1,1)7.
  Own illustrations based on Hyndman and Athanasopoulos (2021, Sections 5.2, 5.8 and 5.10).
"""
import logging
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.tsa.statespace.sarimax import SARIMAX

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
MUTED, LIGHT, BORDER = "#" + theme.COLORS["muted"], "#" + theme.COLORS["light"], "#" + theme.COLORS["border"]
SOFT = "#B8C0C5"  # light grey for context data
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # quiet Arial fallback
warnings.filterwarnings("ignore")  # convergence notes of statsmodels
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = MUTED
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT

URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/tsibbledata/vic_elec.csv")
H = 14


def load():
    df = pd.read_csv(URL).drop(columns="rownames")
    df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
    daily = df.set_index("Time")["Demand"].resample("D").mean()
    daily.index = daily.index.tz_localize(None)
    return daily.asfreq("D")


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=11, length=3)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def baselines(y):
    origin = pd.Timestamp("2014-08-13")
    tr, te = y[:origin], y[origin + pd.Timedelta(days=1):].iloc[:H]
    fc = {
        "Mean": np.repeat(tr.mean(), H),
        "Naive": np.repeat(tr.iloc[-1], H),
        "Seasonal naive": np.array([tr.iloc[-7 + i % 7] for i in range(H)]),
        "Drift": tr.iloc[-1] + (tr.iloc[-1] - tr.iloc[0]) / (len(tr) - 1) * np.arange(1, H + 1),
    }
    fig, ax = plt.subplots(figsize=(11, 4.2))
    hist = tr[origin - pd.Timedelta(days=27):]
    ax.plot(hist.index, hist.values, color=GREY, lw=1.6, label="Observed (training)")
    ax.plot(te.index, te.values, color=TEXT, lw=2.2, marker="o", ms=3.5, label="Observed (test)")
    styles = {"Mean": (SOFT, "-"), "Naive": (MUTED, "--"), "Seasonal naive": (RED, "-"), "Drift": (MUTED, ":")}
    for name, f in fc.items():
        colour, ls = styles[name]
        mae = np.mean(np.abs(te.values - f))
        ax.plot(te.index, f, color=colour, lw=2, ls=ls, label=f"{name} (MAE {mae:,.0f})")
    ax.axvline(origin + pd.Timedelta(hours=12), color=MUTED, lw=0.8)
    ax.text(origin + pd.Timedelta(hours=18), 5650, "forecast origin\n13 Aug 2014", fontsize=10, color=MUTED, va="top")
    ax.set_ylabel("Demand (MW, daily mean)", fontsize=11)
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d %b"))
    ax.set_ylim(4000, 5700)
    ax.legend(frameon=False, fontsize=10, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncols=3)
    clean(ax)
    ax.tick_params(axis="x", labelsize=10)
    ax.grid(axis="y", color=BORDER, lw=0.6)
    save(fig, "fc-baselines.png")


def tscv_diagram(y):
    folds = list(TimeSeriesSplit(n_splits=26, test_size=H).split(y))
    show = [0, 1, 2, 3, None, 24, 25]
    fig, ax = plt.subplots(figsize=(11, 3.4))
    for row, k in enumerate(show):
        yy = len(show) - row
        if k is None:
            ax.text(len(y) * 0.83, yy, "⋮", fontsize=16, color=MUTED, ha="center", va="center")
            continue
        tr, te = folds[k]
        ax.barh(yy, len(tr), left=0, height=0.6, color=SOFT)
        ax.barh(yy, len(te), left=te[0], height=0.6, color=RED)
        ax.text(-12, yy, f"Fold {k + 1}", fontsize=10, color=TEXT, ha="right", va="center")
    ticks = [0, 366, 731, 1096]
    ax.set_xticks(ticks, ["1 Jan 2012", "1 Jan 2013", "1 Jan 2014", "31 Dec 2014"])
    ax.set_yticks([])
    ax.set_xlim(-5, len(y) + 5)
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=SOFT, label="Training: all days up to the origin"),
                       Patch(color=RED, label="Test: next 14 days")],
              frameon=False, fontsize=10, loc="upper left", bbox_to_anchor=(0, 1.18), ncols=2)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10)
    save(fig, "fc-tscv.png")


def folds_plot(y):
    methods = {
        "Seasonal naive": lambda tr: np.array([tr.iloc[-7 + i % 7] for i in range(H)]),
        "ETS(M,N,M)": lambda tr: ETSModel(tr, error="mul", seasonal="mul", seasonal_periods=7)
        .fit(disp=False).forecast(H).to_numpy(),
        "SARIMA(2,0,2)(0,1,1)7": lambda tr: SARIMAX(tr, order=(2, 0, 2), seasonal_order=(0, 1, 1, 7))
        .fit(disp=False).forecast(H).to_numpy(),
    }
    rows = []
    for tri, tei in TimeSeriesSplit(n_splits=26, test_size=H).split(y):
        tr, te = y.iloc[tri], y.iloc[tei]
        rows.append({n: np.mean(np.abs(te.to_numpy() - f(tr))) for n, f in methods.items()} | {"start": te.index[0]})
    res = pd.DataFrame(rows).set_index("start")
    fig, ax = plt.subplots(figsize=(11, 3.8))
    for name, colour, marker in [("Seasonal naive", SOFT, "o"), ("ETS(M,N,M)", MUTED, "s"),
                                 ("SARIMA(2,0,2)(0,1,1)7", RED, "D")]:
        ax.plot(res.index, res[name], color=colour, lw=1.6, marker=marker, ms=4,
                label=f"{name}: mean {res[name].mean():,.0f}")
    ax.annotate("January heat waves", xy=(res.index[1], res.iloc[1].max()), xytext=(res.index[3], 1550),
                fontsize=10, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    ax.set_ylabel("MAE per fold (MW)", fontsize=11)
    ax.set_xlabel("First day of the 14-day test window (2014)", fontsize=11)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    clean(ax)
    ax.grid(axis="y", color=BORDER, lw=0.6)
    save(fig, "fc-folds.png")
    print(res.round(0))


if __name__ == "__main__":
    y = load()
    baselines(y)
    tscv_diagram(y)
    folds_plot(y)
