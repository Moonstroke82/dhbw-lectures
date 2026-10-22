"""Draw the figures and compute the numbers for session 13 (time series forecasting II).

Run from the Lectures folder: python data-analytics/slides/img/make_fc2_figures.py
Needs matplotlib, pandas, statsmodels and scikit-learn, and an internet connection:
the script downloads the lab dataset (vic_elec from the R package tsibbledata,
O'Hara-Wild et al., 2022) from the Rdatasets copy on GitHub, pinned to one commit,
and prepares the daily series exactly as in session 11 (local days, daily mean demand,
daily maximum temperature, holiday flag). Colours from tools/theme.py (DHBW corporate design).

Evaluation as in session 12: 26 folds of 14 days across 2014 (TimeSeriesSplit); the same
scheme on data up to 31 December 2013 is the validation year (feature choice, interval
calibration). Tested with pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1, NumPy 2.5.4
and matplotlib 3.11.2. Runtime about five minutes (many gradient boosting and SARIMAX fits).

- fc2-lagrule.png: which lags a 14-day-ahead forecast may use (direct strategy, one model).
- fc2-mae.png: MAE of baselines, SARIMA, SARIMAX and gradient boosting, ex ante vs. ex post.
- fc2-intervals.png: 80 % intervals of SARIMA and gradient boosting for two folds.
  Own illustrations based on Hyndman and Athanasopoulos (2021, Sections 5.5, 5.9, 7.6 and 10.3).
"""
import logging
import os
import pickle
import sys
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit
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
CAL = ["dow", "doy", "holiday", "xmas"]
LAGS = ["lag14", "lag21", "lag28", "lag364", "mean7_lag14"]


def load(path=URL):
    df = pd.read_csv(path).drop(columns="rownames")
    df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
    daily = df.set_index("Time").resample("D").agg(
        {"Demand": "mean", "Temperature": "max", "Holiday": "max"})
    daily.index = daily.index.tz_localize(None)
    return daily.asfreq("D")


def features(daily):
    """Calendar features of the target day and lags of at least 14 days."""
    y, idx = daily["Demand"], daily.index
    X = pd.DataFrame(index=idx)
    X["dow"] = idx.dayofweek
    X["doy"] = idx.dayofyear
    X["holiday"] = daily["Holiday"]
    md = idx.month * 100 + idx.day
    X["xmas"] = ((md >= 1224) | (md <= 102)).astype(int)   # 24 Dec to 2 Jan
    for k in (14, 21, 28, 364):
        X[f"lag{k}"] = y.shift(k)
    X["mean7_lag14"] = y.shift(14).rolling(7).mean()        # mean of days t-20 ... t-14
    X["temp"] = daily["Temperature"]
    return X


def climatology(temp_train, idx, window=7):
    """Ex-ante temperature: mean daily maximum of the training years within +-7 calendar days."""
    doy, v = temp_train.index.dayofyear.to_numpy(), temp_train.to_numpy()
    out = []
    for d in idx.dayofyear:
        diff = np.abs(doy - d)
        out.append(v[np.minimum(diff, 365 - diff) <= window].mean())
    return np.array(out)


def gbm(**kw):
    return HistGradientBoostingRegressor(**({"max_iter": 300, "learning_rate": 0.05,
                                             "random_state": 0} | kw))


def snaive(tr, h, m=7):
    return np.array([tr.iloc[-m + i % m] for i in range(h)])


def guarded(fc, tr):
    """Session 12 rule: fall back to seasonal naive if a refit gives implausible forecasts."""
    ok = np.all(np.isfinite(fc)) and fc.min() > 0.5 * tr.min() and fc.max() < 1.5 * tr.max()
    return ok


def cross_validate(daily, end):
    y, T, hol = daily["Demand"][:end], daily["Temperature"], daily["Holiday"]
    X = features(daily)
    out, fallbacks = {}, {}

    def put(k, v):
        out.setdefault(k, []).append(np.asarray(v))

    for tri, tei in TimeSeriesSplit(n_splits=26, test_size=H).split(y):
        tr, te = y.index[tri], y.index[tei]
        ytr = y.loc[tr]
        put("y", y.loc[te]); put("origin", np.datetime64(tr[-1]))
        put("snaive7", snaive(ytr, H)); put("snaive364", ytr.iloc[-364:-364 + H])
        temps = {"obs": T.loc[te].to_numpy(), "clim": climatology(T.loc[tr], te)}
        # gradient boosting, one model for all horizons (lags >= 14)
        sets = {"gbm_cal": CAL, "gbm_lags": CAL + LAGS,
                "gbm_clim": CAL + LAGS + ["temp"], "gbm_obs": CAL + LAGS + ["temp"]}
        for name, cols in sets.items():
            Xtr, Xte = X.loc[tr, cols].copy(), X.loc[te, cols].copy()
            if name == "gbm_clim":
                Xte["temp"] = temps["clim"]
            put(name, gbm().fit(Xtr, ytr).predict(Xte))
            if name in ("gbm_lags", "gbm_obs"):
                for tag, kw in {"q": {}, "qreg": {"max_iter": 100, "min_samples_leaf": 50}}.items():
                    lo = gbm(loss="quantile", quantile=0.1, **kw).fit(Xtr, ytr).predict(Xte)
                    hi = gbm(loss="quantile", quantile=0.9, **kw).fit(Xtr, ytr).predict(Xte)
                    put(f"{name}_{tag}", np.vstack([lo, hi]))
        # SARIMA and regression with SARIMA errors (dynamic regression)
        ex_tr = np.column_stack([hol.loc[tr], T.loc[tr], T.loc[tr] ** 2])
        variants = {"sarima": (None, None), "sarimax_hol": (ex_tr[:, :1], hol.loc[te].to_numpy()[:, None])}
        for tk, tv in temps.items():
            variants[f"sarimax_{tk}"] = (ex_tr, np.column_stack([hol.loc[te], tv, tv ** 2]))
        for name, (etr, ete) in variants.items():
            fit = SARIMAX(ytr.to_numpy(), exog=etr, order=(2, 0, 2), seasonal_order=(0, 1, 1, 7)).fit(disp=False)
            g = fit.get_forecast(H, exog=ete)
            fc, pi = g.predicted_mean, g.conf_int(alpha=0.2).T
            if not guarded(fc, ytr):
                fallbacks.setdefault(name, []).append(str(tr[-1].date()))
                fc = snaive(ytr, H)
                pi = np.vstack([fc - 1.28 * ytr.diff(7).std(), fc + 1.28 * ytr.diff(7).std()])
            put(name, fc); put(name + "_pi", pi)
    return {k: np.array(v) for k, v in out.items()}, fallbacks


def interval_scores(y, lo, hi, alpha=0.2):
    inside = (y >= lo) & (y <= hi)
    wink = (hi - lo) + 2 / alpha * np.clip(lo - y, 0, None) + 2 / alpha * np.clip(y - hi, 0, None)
    return {"coverage %": 100 * inside.mean(), "Jan-Feb %": 100 * inside[:4].mean(),
            "Mar-Dec %": 100 * inside[4:].mean(), "below %": 100 * (y < lo).mean(),
            "above %": 100 * (y > hi).mean(), "width": (hi - lo).mean(),
            "width h1": (hi - lo)[:, 0].mean(), "width h14": (hi - lo)[:, -1].mean(), "Winkler": wink.mean()}


def report(val, test):
    pts = ["snaive7", "snaive364", "sarima", "sarimax_hol", "sarimax_clim", "sarimax_obs",
           "gbm_cal", "gbm_lags", "gbm_clim", "gbm_obs"]
    rows = {}
    for n in pts:
        E, Ev = test["y"] - test[n], val["y"] - val[n]
        fold = np.abs(E).mean(1)
        rows[n] = {"MAE": np.abs(E).mean(), "RMSE": np.sqrt((E ** 2).mean()),
                   "MAPE": (100 * np.abs(E) / test["y"]).mean(), "ME": E.mean(),
                   "MAE Jan-Feb": np.abs(E[:4]).mean(), "MAE Mar-Dec": np.abs(E[4:]).mean(),
                   "median fold": np.median(fold), "MAE val": np.abs(Ev).mean(),
                   "MAE h1": np.abs(E[:, 0]).mean(), "MAE h14": np.abs(E[:, -1]).mean(),
                   "folds better than sarima": int((fold < np.abs(test["y"] - test["sarima"]).mean(1)).sum())}
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)
    print(pd.DataFrame(rows).T.round(1))
    iv = {"sarima": test["sarima_pi"], "sarimax_hol": test["sarimax_hol_pi"],
          "sarimax_obs": test["sarimax_obs_pi"]}
    for n in ("gbm_lags", "gbm_obs"):
        iv[n + "_q"], iv[n + "_qreg"] = test[n + "_q"], test[n + "_qreg"]
        e = (val["y"] - val[n]).ravel()
        lo, hi = np.quantile(e, [0.1, 0.9])
        print(f"validation error quantiles {n}: 10 % {lo:.0f}, 90 % {hi:.0f}")
        iv[n + "_emp"] = np.stack([test[n] + lo, test[n] + hi], axis=1)
        vq = val[n + "_qreg"]
        print(f"validation coverage {n}_q {100 * ((val['y'] >= val[n + '_q'][:, 0]) & (val['y'] <= val[n + '_q'][:, 1])).mean():.1f}"
              f", {n}_qreg {100 * ((val['y'] >= vq[:, 0]) & (val['y'] <= vq[:, 1])).mean():.1f}")
    print(pd.DataFrame({k: interval_scores(test["y"], v[:, 0], v[:, 1]) for k, v in iv.items()}).T.round(1))
    return iv


def lagrule():
    fig, ax = plt.subplots(figsize=(11, 3.0))
    for d in range(-30, 1):
        ax.add_patch(plt.Rectangle((d - 0.45, 0.6), 0.9, 0.8, color=SOFT, lw=0))
    for d in range(1, 15):
        ax.add_patch(plt.Rectangle((d - 0.45, 0.6), 0.9, 0.8, facecolor="white", edgecolor=RED, lw=1.2))
    ax.axvline(0.5, ymin=0.2, ymax=0.6, color=MUTED, lw=1)
    ax.text(0.2, 0.25, "origin T", fontsize=11, color=TEXT, ha="right")
    ax.text(-16, 0.25, "known at the origin", fontsize=11, color=GREY, ha="center")
    ax.text(7.2, 0.25, "forecast h = 1 … 14", fontsize=11, color=RED, ha="center")
    ax.text(14, 0.25, "t = T + 14", fontsize=10, color=TEXT, ha="center")
    t = 14  # the hardest target day: its lags must be at least 14 days old
    for k, lab in [(14, "lag 14"), (21, "lag 21"), (28, "lag 28")]:
        ax.annotate("", xy=(t - k, 1.42), xytext=(t, 1.42),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=1.2, connectionstyle="arc3,rad=0.35"))
        ax.text(t - k - 0.6, 1.5, lab, fontsize=10, color=RED, ha="right")
    ax.text(15.3, 1.0, "lags 1–13 of day t:\nnot known at T", fontsize=10, color=MUTED, ha="left", va="center")
    ax.set_xlim(-31, 23)
    ax.set_ylim(0, 2.6)
    ax.axis("off")
    save(fig, "fc2-lagrule.png")


def mae_chart(val, test):
    items = [("Seasonal naive (lag 7)", "snaive7", "ante"), ("Seasonal naive (lag 364)", "snaive364", "ante"),
             ("SARIMA", "sarima", "ante"), ("SARIMA + holiday", "sarimax_hol", "ante"),
             ("GBM: calendar", "gbm_cal", "ante"), ("GBM: calendar + lags", "gbm_lags", "ante"),
             ("GBM: + temperature climatology", "gbm_clim", "ante"),
             ("SARIMA + holiday + observed temperature", "sarimax_obs", "post"),
             ("GBM: + observed temperature", "gbm_obs", "post")]
    fig, ax = plt.subplots(figsize=(11, 4.4))
    for i, (lab, k, kind) in enumerate(items[::-1]):
        m = np.abs(test["y"] - test[k]).mean()
        colour = RED if kind == "post" else (GREY if k.startswith("gbm") else SOFT)
        ax.barh(i, m, color=colour, height=0.65)
        ax.text(m + 5, i, f"{m:,.0f}", va="center", fontsize=11, color=TEXT)
    ax.set_yticks(range(len(items)), [it[0] for it in items[::-1]], fontsize=11)
    ax.set_xlabel("MAE (MW), 26 folds × 14 days in 2014", fontsize=11)
    ax.axvline(np.abs(test["y"] - test["sarima"]).mean(), color=MUTED, lw=0.8, ls="--")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=SOFT, label="Baselines and SARIMA, ex ante"),
                       Patch(color=GREY, label="Gradient boosting, ex ante"),
                       Patch(color=RED, label="Ex post: observed temperature")],
              frameon=False, fontsize=10, loc="lower right")
    clean(ax)
    ax.set_xlim(0, 380)
    save(fig, "fc2-mae.png")


def interval_plot(daily, test, iv):
    origins = pd.to_datetime(test["origin"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9), sharey=False)
    for ax, k in zip(axes, (1, 13)):
        idx = pd.date_range(origins[k] + pd.Timedelta(days=1), periods=H)
        hist = daily["Demand"][origins[k] - pd.Timedelta(days=13):origins[k]]
        ax.plot(hist.index, hist.values, color=GREY, lw=1.4)
        s, g = iv["sarima"][k], iv["gbm_lags_emp"][k]
        ax.fill_between(idx, s[0], s[1], color=SOFT, alpha=0.55, lw=0, label="SARIMA, model-based 80 %")
        ax.fill_between(idx, g[0], g[1], color=RED, alpha=0.18, lw=0, label="GBM (calendar + lags), empirical 80 %")
        ax.plot(idx, test["gbm_lags"][k], color=RED, lw=1.6)
        ax.plot(idx, test["y"][k], color=TEXT, lw=2, marker="o", ms=3)
        inside = ((test["y"][k] >= g[0]) & (test["y"][k] <= g[1])).sum()
        ax.set_title(f"Origin {origins[k]:%d %b %Y}: {inside} of 14 days inside the GBM interval",
                     fontsize=11, color=TEXT)
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
        clean(ax)
        ax.grid(axis="y", color=BORDER, lw=0.6)
    axes[0].set_ylabel("Demand (MW, daily mean)", fontsize=11)
    h, lab = axes[0].get_legend_handles_labels()
    fig.legend(h, lab, frameon=False, fontsize=10, loc="lower center", bbox_to_anchor=(0.5, 0.98), ncols=2)
    save(fig, "fc2-intervals.png")


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10, length=3)


if __name__ == "__main__":
    daily = load(sys.argv[1] if len(sys.argv) > 1 else URL)
    val, fb_val = cross_validate(daily, "2013-12-31")
    test, fb_test = cross_validate(daily, "2014-12-31")
    if os.environ.get("FC2_CACHE"):                  # optional: keep the results for re-use
        with open(os.environ["FC2_CACHE"], "wb") as f:
            pickle.dump({"val": val, "test": test}, f)
    print("fallbacks validation:", fb_val, "test:", fb_test)
    iv = report(val, test)
    lagrule()
    mae_chart(val, test)
    interval_plot(daily, test, iv)
