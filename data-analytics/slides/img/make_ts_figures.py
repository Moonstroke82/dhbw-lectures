"""Draw the figures for session 11 (temporal data and time series fundamentals).

Run from the Lectures folder: python data-analytics/slides/img/make_ts_figures.py
Needs matplotlib, pandas and statsmodels, and an internet connection: the script
downloads the lab dataset (vic_elec from the R package tsibbledata, O'Hara-Wild et
al., 2022; source: Australian Energy Market Operator and Bureau of Meteorology) from
the Rdatasets copy on GitHub, pinned to one commit so the numbers stay the same.
Colours from tools/theme.py (DHBW corporate design).

Tested with pandas 3.0.6, statsmodels 0.15.0, NumPy 2.5.4 and matplotlib 3.11.2.
Daily demand is the mean of the half-hourly values of a local calendar day
(Australia/Melbourne), daily temperature the maximum, as on the slides.

- ts-overview.png: daily demand and daily maximum temperature, 2012-2014.
- ts-profiles.png: three seasonal patterns: average day (weekdays vs. weekends),
  day of week, month (one line per year).
- ts-temperature.png: daily demand against daily maximum temperature (U shape).
- ts-acf.png: autocorrelation function of the half-hourly and the daily series.
- ts-mstl.png: MSTL decomposition of daily demand with weekly and yearly seasonality.
  Own illustrations based on Hyndman and Athanasopoulos (2021, Sections 2.4, 2.8, 3.6)
  and Bandara et al. (2025).
"""
import logging
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import MSTL
from statsmodels.tsa.stattools import acf

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
MUTED, LIGHT, BORDER = "#" + theme.COLORS["muted"], "#" + theme.COLORS["light"], "#" + theme.COLORS["border"]
SOFT = "#B8C0C5"  # light grey for context data
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)  # quiet Arial fallback
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = MUTED
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT

URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/tsibbledata/vic_elec.csv")


def load():
    df = pd.read_csv(URL).drop(columns="rownames")
    df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
    df = df.set_index("Time")
    daily = df.resample("D").agg({"Demand": "mean", "Temperature": "max", "Holiday": "max"})
    daily.columns = ["demand", "temp_max", "holiday"]
    daily.index = daily.index.tz_localize(None)
    return df, daily.asfreq("D")


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=11, length=3)


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def year_axis(ax):
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 7, 10]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))


def overview(daily):
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 4.6), sharex=True, height_ratios=[1.6, 1])
    a1.plot(daily.index, daily.demand, color=GREY, lw=0.9)
    top = daily.demand.idxmax()
    a1.annotate(f"{top:%d %b %Y}: {daily.demand.max():,.0f} MW\nheat wave, {daily.temp_max.max():.1f} °C",
                xy=(top, daily.demand.max()), xytext=(top - pd.Timedelta(days=260), 6900),
                fontsize=11, color=RED, arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    low = daily.demand.idxmin()
    a1.annotate(f"{low:%d %b %Y}: {daily.demand.min():,.0f} MW", xy=(low, daily.demand.min()),
                xytext=(low - pd.Timedelta(days=330), 3450), fontsize=11, color=TEXT,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=1))
    a1.set_ylabel("Demand (MW,\ndaily mean)", fontsize=11)
    a2.plot(daily.index, daily.temp_max, color=RED, lw=0.8)
    a2.set_ylabel("Max. temp.\n(°C)", fontsize=11)
    for ax in (a1, a2):
        clean(ax)
        ax.grid(axis="y", color=BORDER, lw=0.6)
    year_axis(a2)
    save(fig, "ts-overview.png")


def profiles(df, daily):
    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(12, 3.6), width_ratios=[1.3, 1, 1.3])
    weekend = df.index.dayofweek >= 5
    hours = df.index.hour + df.index.minute / 60
    for mask, colour, label in [(~weekend, RED, "Monday–Friday"), (weekend, GREY, "Saturday–Sunday")]:
        prof = df.Demand[mask].groupby(hours[mask]).mean()
        a1.plot(prof.index, prof.values, color=colour, lw=2, label=label)
    a1.set_xticks([0, 6, 12, 18, 24])
    a1.set_xlabel("Time of day (local)", fontsize=11)
    a1.set_ylabel("Demand (MW)", fontsize=11)
    a1.set_title("Within the day", fontsize=12, color=TEXT)
    a1.legend(frameon=False, fontsize=10, loc="upper left")

    wd = daily.demand.groupby(daily.index.dayofweek).mean()
    a2.plot(range(7), wd.values, color=GREY, lw=1, zorder=1)  # dot plot: no bars on a cut axis
    a2.scatter(range(7), wd.values, s=60, color=[GREY] * 5 + [RED] * 2, zorder=2)
    a2.set_xticks(range(7), ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    a2.set_ylim(3900, 5100)
    a2.set_title("Within the week (daily mean)", fontsize=12, color=TEXT)

    for year, colour in zip([2012, 2013, 2014], [SOFT, MUTED, RED]):
        part = daily.demand[daily.index.year == year]
        mon = part.groupby(part.index.month).mean()
        a3.plot(mon.index, mon.values, color=colour, lw=2, marker="o", ms=3, label=str(year))
    a3.set_xticks(range(1, 13), list("JFMAMJJASOND"))
    a3.set_title("Within the year (monthly mean)", fontsize=12, color=TEXT)
    a3.legend(frameon=False, fontsize=10, ncols=3, loc="upper left")
    a3.set_ylim(4100, 5400)
    for ax in (a1, a2, a3):
        clean(ax)
        ax.grid(axis="y", color=BORDER, lw=0.6)
    fig.tight_layout(w_pad=2)
    save(fig, "ts-profiles.png")


def temperature(daily):
    fig, ax = plt.subplots(figsize=(7.5, 4))
    hol_or_we = daily.holiday.astype(bool) | (daily.index.dayofweek >= 5)
    ax.scatter(daily.temp_max[~hol_or_we], daily.demand[~hol_or_we], s=9, color=GREY, alpha=0.7,
               label="Working days")
    ax.scatter(daily.temp_max[hol_or_we], daily.demand[hol_or_we], s=9, color=RED, alpha=0.7,
               label="Weekends and public holidays")
    r = np.corrcoef(daily.temp_max, daily.demand)[0, 1]
    ax.text(0.03, 0.95, f"Pearson correlation r = {r:.2f}", transform=ax.transAxes, fontsize=11, color=TEXT,
            va="top")
    ax.set_xlabel("Daily maximum temperature in Melbourne (°C)", fontsize=11)
    ax.set_ylabel("Demand (MW, daily mean)", fontsize=11)
    ax.legend(frameon=False, fontsize=10, loc="upper center", bbox_to_anchor=(0.6, 1.0))
    clean(ax)
    ax.grid(color=BORDER, lw=0.6)
    save(fig, "ts-temperature.png")


def acf_plot(df, daily):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(12, 3.6))
    for ax, series, nlags, title, ticks, unit in [
        (a1, df.Demand.values, 48 * 7, "Half-hourly series: lags up to 7 days", range(0, 337, 48), 48),
        (a2, daily.demand.values, 400, "Daily series: lags up to 400 days", [0, 91, 182, 273, 364], 1),
    ]:
        r = acf(series, nlags=nlags)
        lags = np.arange(len(r))
        ax.vlines(lags[1:], 0, r[1:], color=GREY, lw=1.0 if nlags < 350 else 0.8)
        bound = 1.96 / np.sqrt(len(series))
        ax.axhspan(-bound, bound, color=RED, alpha=0.15, lw=0)
        ax.axhline(0, color=MUTED, lw=0.8)
        ax.set_xticks(list(ticks))
        if unit == 48:
            ax.set_xticklabels([f"{t // 48} d" for t in ticks])
        ax.set_ylim(-0.4, 1.02)
        ax.set_title(title, fontsize=12, color=TEXT)
        ax.set_xlabel("Lag (days)" if unit == 1 else "Lag", fontsize=11)
        clean(ax)
    a1.set_ylabel("Autocorrelation", fontsize=11)
    a2.annotate("lag 7: 0.60", xy=(7, 0.601), xytext=(40, 0.85), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    a2.annotate("lag 364: 0.41", xy=(364, 0.406), xytext=(250, 0.8), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    a1.annotate("lag 1 day: 0.79", xy=(48, 0.786), xytext=(70, 0.98), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    a1.annotate("lag 7 days: 0.78", xy=(336, 0.78), xytext=(215, 0.98), fontsize=10, color=RED,
                arrowprops=dict(arrowstyle="-", color=RED, lw=1))
    fig.tight_layout(w_pad=3)
    save(fig, "ts-acf.png")


def mstl_plot(daily):
    res = MSTL(daily.demand, periods=(7, 365)).fit()
    parts = [("Observed", daily.demand, GREY), ("Trend", res.trend, RED),
             ("Weekly", res.seasonal["seasonal_7"], GREY), ("Yearly", res.seasonal["seasonal_365"], GREY),
             ("Remainder", res.resid, MUTED)]
    fig, axes = plt.subplots(5, 1, figsize=(11, 6.4), sharex=True, height_ratios=[1.4, 0.8, 0.9, 1.1, 1])
    for ax, (name, s, colour) in zip(axes, parts):
        ax.plot(s.index, s.values, color=colour, lw=0.8 if name != "Trend" else 1.6)
        ax.set_ylabel(name, fontsize=11, rotation=0, ha="right", va="center")
        clean(ax)
        ax.grid(axis="y", color=BORDER, lw=0.6)
        ax.tick_params(labelsize=9)
    axes[1].set_ylim(4400, 4900)
    year_axis(axes[-1])
    axes[-1].tick_params(axis="x", labelsize=11)
    save(fig, "ts-mstl.png")


if __name__ == "__main__":
    df, daily = load()
    overview(daily)
    profiles(df, daily)
    temperature(daily)
    acf_plot(df, daily)
    mstl_plot(daily)
