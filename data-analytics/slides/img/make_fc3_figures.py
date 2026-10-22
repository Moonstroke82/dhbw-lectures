"""Draw the figures and compute the numbers for session 14 (forecasting at scale and use cases).

Run from the Lectures folder: python data-analytics/slides/img/make_fc3_figures.py [data_dir]
Needs matplotlib, pandas, statsmodels and scikit-learn, and an internet connection (or a
folder with the three CSV files): all data come from the Rdatasets copies on GitHub, pinned
to one commit (Arel-Bundock, n.d.):

- tourism (R package tsibble): quarterly overnight trips in Australia 1998-2017, 304 series
  by state, region and purpose; used in Hyndman and Athanasopoulos (2021, Chapter 11).
- PBS (R package tsibbledata, O'Hara-Wild et al., 2022): monthly prescriptions; the series
  J06 (immune sera and immunoglobulins), concessional co-payments, is intermittent
  (see Hyndman and Athanasopoulos, 2021, Section 13.2 for the J06 total).
- vic_elec (tsibbledata): the daily demand series of sessions 11-13.

Tested with pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1, NumPy 2.5.4 and
matplotlib 3.11.2. Runtime about three minutes (425 x 4 ETS fits twice, gradient boosting).

- fc3-hierarchy.png: the tourism hierarchy (own illustration based on Hyndman and
  Athanasopoulos, 2021, Section 11.1).
- fc3-intermittent.png: the intermittent J06 series with SES and Croston forecasts.
- fc3-anomalies.png: anomalies in daily demand from the MSTL remainder (3 IQR rule).
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
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.tsa.seasonal import MSTL

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[2] / "tools"))
import theme  # noqa: E402

GREY, RED, TEXT = "#" + theme.COLORS["primary"], "#" + theme.COLORS["accent"], "#" + theme.COLORS["text"]
MUTED, LIGHT, BORDER = "#" + theme.COLORS["muted"], "#" + theme.COLORS["light"], "#" + theme.COLORS["border"]
SOFT = "#B8C0C5"
logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = ["Arial", "Liberation Sans", "DejaVu Sans"]
plt.rcParams["axes.edgecolor"] = MUTED
plt.rcParams["axes.labelcolor"] = TEXT
plt.rcParams["xtick.color"] = TEXT
plt.rcParams["ytick.color"] = TEXT

BASE = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
        "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/")
FILES = {"tourism": "tsibble/tourism.csv", "pbs": "tsibbledata/PBS.csv",
         "vic_elec": "tsibbledata/vic_elec.csv"}


def path(key, data_dir=None):
    if data_dir:
        return Path(data_dir) / FILES[key].replace("/", "_")
    return BASE + FILES[key]


# ---------------------------------------------------------------- tourism: many series
LEVELS = ["Total", "Purpose", "State", "State x Purpose", "Region", "Bottom"]


def load_tourism(src):
    t = pd.read_csv(src).drop(columns="rownames")
    t["Q"] = pd.PeriodIndex(t["Quarter"].str.replace(" ", ""), freq="Q")
    return t.pivot_table(index="Q", columns=["State", "Region", "Purpose"], values="Trips")


def hierarchy(bottom):
    """All 425 series (6 levels) and the summing matrix S (425 x 304)."""
    parts = {"Total": bottom.sum(axis=1).to_frame("all"),
             "Purpose": bottom.T.groupby(level="Purpose").sum().T,
             "State": bottom.T.groupby(level="State").sum().T,
             "State x Purpose": bottom.T.groupby(level=["State", "Purpose"]).sum().T,
             "Region": bottom.T.groupby(level=["State", "Region"]).sum().T,
             "Bottom": bottom}
    frames = []
    for k, g in parts.items():
        g = g.copy()
        g.columns = [(k,) + (c if isinstance(c, tuple) else (c,)) for c in g.columns]
        frames.append(g)
    Y = pd.concat(frames, axis=1)
    S = np.zeros((Y.shape[1], bottom.shape[1]))
    for i, (lev, *key) in enumerate(Y.columns):
        for j, (st, rg, pu) in enumerate(bottom.columns):
            S[i, j] = {"Total": True, "Purpose": key[0] == pu, "State": key[0] == st,
                       "State x Purpose": tuple(key) == (st, pu), "Region": tuple(key) == (st, rg),
                       "Bottom": tuple(key) == (st, rg, pu)}[lev]
    assert np.allclose(S @ bottom.to_numpy().T, Y.to_numpy().T)
    return Y, S


def ets_auto(y):
    """Additive ETS models (data contain zeros), chosen by AICc."""
    best = None
    for trend, damped, seas in [(None, False, None), ("add", True, None),
                                (None, False, "add"), ("add", True, "add")]:
        try:
            f = ETSModel(y, error="add", trend=trend, damped_trend=damped, seasonal=seas,
                         seasonal_periods=4).fit(disp=False)
        except Exception:
            continue
        if best is None or f.aicc < best[0]:
            best = (f.aicc, f, (trend, seas))
    return best[1], best[2]


def shrink_cov(R):
    """Covariance with shrinkage of the correlations towards zero (Schaefer & Strimmer, 2005),
    as used by MinT-shrink (Wickramasuriya et al., 2019)."""
    T = R.shape[1]
    X = R - R.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, ddof=1)
    Z = X / sd[:, None]
    C = Z @ Z.T / (T - 1)
    W = np.einsum("it,jt->ijt", Z, Z)
    var = T / (T - 1) ** 3 * ((W - (C * (T - 1) / T)[:, :, None]) ** 2).sum(axis=2)
    off = ~np.eye(len(sd), dtype=bool)
    lam = float(np.clip(var[off].sum() / (C[off] ** 2).sum(), 0, 1))
    Cs = C * (1 - lam)
    np.fill_diagonal(Cs, 1)
    return Cs * np.outer(sd, sd), lam


def reconcile(base, S, W):
    Wi = np.linalg.pinv(W)
    return S @ np.linalg.solve(S.T @ Wi @ S, S.T @ Wi) @ base


def global_forecast(Bv, last, H, L=12, kind="linear"):
    """One global model per horizon h for all series (direct strategy). Inputs: the last L
    quarters up to the origin, divided by the series level (mean of the last 4 quarters)."""
    floor = 0.1 * Bv[:, :last].mean(axis=1)            # avoid dividing by ~0 in tiny series
    out = np.zeros((Bv.shape[0], H))
    for h in range(1, H + 1):
        X, y = [], []
        for o in range(L - 1, last - h):                # origin o, target o + h, both in training
            w = Bv[:, o - L + 1:o + 1]
            lvl = np.maximum(w[:, -4:].mean(axis=1), floor)
            X.append(w / lvl[:, None]); y.append(Bv[:, o + h] / lvl)
        X, y = np.vstack(X), np.concatenate(y)
        w = Bv[:, last - L:last]
        lvl = np.maximum(w[:, -4:].mean(axis=1), floor)
        m = (LinearRegression() if kind == "linear" else
             HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0))
        out[:, h - 1] = m.fit(X, y).predict(w / lvl[:, None]) * lvl
    return out, len(y)


def scores(Ytr, Yte, F, lev):
    sc = np.mean(np.abs(Ytr[:, 4:] - Ytr[:, :-4]), axis=1)      # MASE scale: seasonal naive
    rows = {}
    for k, f in F.items():
        e = Yte - f
        mase = np.mean(np.abs(e), axis=1) / sc
        rmse = np.sqrt(np.mean(e ** 2, axis=1))
        rows[k] = {**{f"MASE {l}": mase[lev == l].mean() for l in LEVELS},
                   "MASE all": mase.mean(),
                   **{f"RMSE {l}": rmse[lev == l].mean() for l in LEVELS}}
    return pd.DataFrame(rows).T, sc


def tourism(src):
    bottom = load_tourism(src)
    Y, S = hierarchy(bottom)
    lev = np.array([c[0] for c in Y.columns])
    isb = lev == "Bottom"
    print(f"tourism: {bottom.shape[1]} bottom series, {Y.shape[1]} series in total, "
          f"{bottom.shape[0]} quarters {bottom.index[0]}-{bottom.index[-1]}; "
          f"zeros {np.mean(bottom.to_numpy() == 0):.3f}")
    print("bottom series mean trips (thousand):", bottom.mean().describe().round(1).to_dict())
    H = 8
    Bv = bottom.to_numpy(dtype=float).T
    result = {}
    for name, end in [("validation", "2013Q4"), ("test", "2015Q4")]:
        last = int(np.sum(Y.index <= pd.Period(end, "Q")))
        Ytr, Yte = Y.to_numpy().T[:, :last], Y.to_numpy().T[:, last:last + H]
        F = {}
        if name == "test":
            fc, res, spec = [], [], []
            for i in range(Y.shape[1]):
                f, s = ets_auto(pd.Series(Ytr[i]))
                fc.append(np.asarray(f.forecast(H))); res.append(np.asarray(f.resid)); spec.append(s)
            fc, res = np.array(fc), np.array(res)
            W, lam = shrink_cov(res)
            print("ETS specs (bottom):", pd.Series([str(s) for s, b in zip(spec, isb) if b]).value_counts().to_dict())
            print(f"MinT shrinkage intensity lambda = {lam:.3f}")
            F["ETS base (incoherent)"] = fc
            F["ETS bottom-up"] = S @ fc[isb]
            F["ETS + OLS"] = reconcile(fc, S, np.eye(len(fc)))
            F["ETS + WLS structural"] = reconcile(fc, S, np.diag(S.sum(axis=1)))
            F["ETS + MinT shrink"] = reconcile(fc, S, W)
            F["Seasonal naive (each series)"] = np.tile(Ytr[:, -4:], 2)
            print("Total: actual", Yte[0].round(0), "\n  ETS base", fc[0].round(0),
                  "\n  sum of bottom ETS", (S @ fc[isb])[0].round(0),
                  "\n  MinT", F["ETS + MinT shrink"][0].round(0))
        for kind in ("linear", "gbm"):
            for L in (4, 8, 12):
                g, n = global_forecast(Bv, last, H, L, kind)
                F[f"Global {kind} L={L}, bottom-up"] = S @ g
        R, sc = scores(Ytr, Yte, F, lev)
        result[name] = (R, F, Ytr, Yte, sc)
        pd.set_option("display.width", 250)
        print(f"\n--- tourism {name}: train to {end}, {H} quarters, training windows per h up to {n}")
        print(R.filter(like="MASE").round(3).to_string())
        print(R.filter(like="RMSE").round(1).to_string())
    R, F, Ytr, Yte, sc = result["test"]
    m = lambda k: np.mean(np.abs(Yte - F[k]), axis=1)[isb] / sc[isb]
    print("bottom series where global linear L=12 beats ETS:",
          int(np.sum(m("Global linear L=12, bottom-up") < m("ETS base (incoherent)"))), "of", isb.sum())
    tot = lambda k: F[k][0].sum()
    print("2-year total trips: actual", round(Yte[0].sum()), {k: round(tot(k)) for k in F})
    return bottom, Y


# ---------------------------------------------------------------- intermittent demand
def ses(x, a=0.1):
    level = x[0]
    for v in x[1:]:
        level = a * v + (1 - a) * level
    return level


def croston(x, a=0.1, sba=False):
    """Croston (1972): SES of the non-zero demands and of the intervals; forecast = ratio.
    sba=True: Syntetos-Boylan approximation, multiplied by (1 - a/2)."""
    nz = np.flatnonzero(x)
    if len(nz) == 0:
        return 0.0
    q, p, last = x[nz[0]], nz[0] + 1.0, nz[0]
    for i in nz[1:]:
        q = a * x[i] + (1 - a) * q
        p = a * (i - last) + (1 - a) * p
        last = i
    return q / p * (1 - a / 2 if sba else 1)


def intermittent(src):
    p = pd.read_csv(src)
    q = p[(p.ATC2 == "J06") & (p.Concession == "Concessional") & (p.Type == "Co-payments")]
    j = q.set_index(pd.PeriodIndex(pd.to_datetime(q["Month"], format="%Y %b"), freq="M"))["Scripts"].sort_index()
    y = j.to_numpy(dtype=float)
    act = j[:"2003-12"].to_numpy(dtype=float)
    nz = np.flatnonzero(act)
    adi, cv2 = np.mean(np.diff(nz)), (act[nz].std() / act[nz].mean()) ** 2
    print(f"\nJ06 concessional co-payments: {len(j)} months {j.index[0]}-{j.index[-1]}, "
          f"zeros {np.mean(y == 0):.3f}, to 2003: zeros {np.mean(act == 0):.3f}, mean {act.mean():.3f}, "
          f"max {act.max():.0f}, ADI {adi:.2f}, CV2 {cv2:.2f}")
    print("values to 2003:", pd.Series(act).value_counts().sort_index().to_dict(),
          "last non-zero month:", j[j > 0].index[-1])
    H = 6
    meth = {"Zero": lambda x: 0.0, "Mean of all months": lambda x: x.mean(),
            "Mean of last 12 months": lambda x: x[-12:].mean(), "SES (α = 0.1)": ses,
            "Croston (α = 0.1)": croston, "SBA (α = 0.1)": lambda x: croston(x, sba=True)}
    o0, o1 = j.index.get_loc(pd.Period("1996-01", "M")), j.index.get_loc(pd.Period("2003-07", "M"))
    rows = {}
    for k, f in meth.items():
        E = np.array([y[o:o + H] - f(y[:o]) for o in range(o0, o1 + 1)])
        Fc = np.array([f(y[:o]) for o in range(o0, o1 + 1)])
        rows[k] = {"MAE": np.abs(E).mean(), "RMSE": np.sqrt((E ** 2).mean()), "ME": E.mean(),
                   "mean forecast": Fc.mean(), "6-month demand > 6 x forecast": (E.sum(axis=1) > 0).mean()}
    print(f"{o1 - o0 + 1} origins, test months 1996-01 to 2003-12, h = 1..{H}")
    print(pd.DataFrame(rows).T.round(3).to_string())
    for end in ["2003-12", "2005-12", "2008-06"]:
        o = j.index.get_loc(pd.Period(end, "M")) + 1
        print(f"forecast at end {end}: Croston {croston(y[:o]):.3f}, SBA {croston(y[:o], sba=True):.3f}, "
              f"SES {ses(y[:o]):.3f}, mean last 12 {y[o-12:o].mean():.3f}")
    # figure
    fig, ax = plt.subplots(figsize=(9.6, 3.4))
    t = j.index.to_timestamp()
    ax.vlines(t, 0, y, color=GREY, lw=1.6)
    ax.plot(t[y > 0], y[y > 0], "o", color=GREY, ms=3)
    cro = [croston(y[:o]) if o > 12 else np.nan for o in range(1, len(y) + 1)]
    ses_ = [ses(y[:o]) if o > 12 else np.nan for o in range(1, len(y) + 1)]
    ax.step(t, cro, where="post", color=RED, lw=2, label="Croston forecast for the next month")
    ax.step(t, ses_, where="post", color=MUTED, lw=1.4, ls="--", label="SES forecast for the next month")
    ax.set_ylabel("Scripts per month", fontsize=11)
    ax.set_yticks([0, 1, 2, 3])
    ax.axvspan(pd.Timestamp("1996-01-01"), pd.Timestamp("2004-01-01"), color=LIGHT, zorder=0)
    ax.text(pd.Timestamp("2000-01-01"), 3.55, "Evaluation period", ha="center", fontsize=10, color=MUTED)
    ax.set_ylim(0, 3.9)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    clean(ax)
    save(fig, "fc3-intermittent.png")


# ---------------------------------------------------------------- anomalies in vic_elec
def load_daily(src):
    df = pd.read_csv(src).drop(columns="rownames")
    df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
    daily = df.set_index("Time").resample("D").agg({"Demand": "mean", "Temperature": "max", "Holiday": "max"})
    daily.index = daily.index.tz_localize(None)
    return daily.asfreq("D")


def iqr_flags(r, k=3):
    q1, q3 = np.quantile(r, [0.25, 0.75])
    return (r < q1 - k * (q3 - q1)) | (r > q3 + k * (q3 - q1)), (q1 - k * (q3 - q1), q3 + k * (q3 - q1))


def anomalies(src):
    daily = load_daily(src)
    y = daily["Demand"]
    R = MSTL(y, periods=(7, 365)).fit().resid
    flag, (lo, hi) = iqr_flags(R.to_numpy())
    fl = daily[flag].assign(resid=R[flag].round(0))
    hot = fl["Temperature"] >= 33
    print(f"\nMSTL remainder: IQR {np.subtract(*np.quantile(R, [0.75, 0.25])):.0f} MW, bounds {lo:.0f} / {hi:.0f}; "
          f"{flag.sum()} days flagged: {int((fl.resid > 0).sum())} high, {int((fl.resid < 0).sum())} low; "
          f"holidays {int(fl.Holiday.sum())}, days >= 33 C {int(hot.sum())}, of which high {int((hot & (fl.resid > 0)).sum())}")
    print("flagged by year:", fl.index.year.value_counts().sort_index().to_dict())
    print(fl[["Demand", "Temperature", "Holiday", "resid"]].round(1).to_string())
    # model-based: cross-validated errors of gradient boosting with calendar + observed temperature (2014)
    X = pd.DataFrame(index=y.index)
    X["dow"], X["doy"] = y.index.dayofweek, y.index.dayofyear
    X["holiday"] = daily["Holiday"].astype(int)
    md = y.index.month * 100 + y.index.day
    X["xmas"] = ((md >= 1224) | (md <= 102)).astype(int)
    for k in (14, 21, 28, 364):
        X[f"lag{k}"] = y.shift(k)
    X["mean7_lag14"] = y.shift(14).rolling(7).mean()
    X["temp"] = daily["Temperature"]
    planted = pd.Timestamp("2014-08-20")              # a planted data error: half a day missing
    yp = y.copy()
    yp[planted] = y[planted] * 0.5
    Rp = MSTL(yp, periods=(7, 365)).fit().resid
    fp, _ = iqr_flags(Rp.to_numpy())
    print(f"planted error {planted.date()}: demand {y[planted]:.0f} -> {yp[planted]:.0f} MW; "
          f"MSTL remainder {Rp[planted]:.0f} MW, flagged: {bool(fp[Rp.index.get_loc(planted)])}")
    seas = MSTL(y, periods=(7, 365)).fit().seasonal["seasonal_365"]
    print("yearly component 13-18 Jan 2014:", seas["2014-01-13":"2014-01-18"].round(0).tolist(),
          "remainder:", R["2014-01-13":"2014-01-18"].round(0).tolist())
    for label, ys in [("observed", y), ("with planted error on 2014-08-20", yp)]:
        idx, err = [], []
        for tr, te in TimeSeriesSplit(n_splits=26, test_size=14).split(ys):
            m = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0)
            m.fit(X.iloc[tr], ys.iloc[tr])
            err.append(ys.iloc[te].to_numpy() - m.predict(X.iloc[te]))
            idx.append(ys.index[te])
        e = pd.Series(np.concatenate(err), index=np.concatenate(idx))
        f2, (l2, h2) = iqr_flags(e.to_numpy())
        print(f"GBM ex post errors 2014 ({label}): MAE {e.abs().mean():.0f}, bounds {l2:.0f} / {h2:.0f}, "
              f"flagged {f2.sum()}:", {str(d.date()): int(v) for d, v in e[f2].items()})
        if label == "observed":
            print("MSTL flags in 2014:", [str(d.date()) for d in R.index[flag] if d.year == 2014])
    # figure: MSTL remainder with flagged days, 2012-2014
    fig, axes = plt.subplots(2, 1, figsize=(9.6, 4.6), sharex=True, gridspec_kw={"height_ratios": [1.4, 1]})
    ax = axes[0]
    ax.plot(y.index, y, color=SOFT, lw=0.8)
    ax.plot(y.index[flag], y[flag], "o", color=RED, ms=4, label="Flagged day")
    ax.set_ylabel("Demand (MW)", fontsize=11)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    ax = axes[1]
    ax.plot(R.index, R, color=GREY, lw=0.7)
    ax.axhspan(lo, hi, color=LIGHT, zorder=0)
    for b in (lo, hi):
        ax.axhline(b, color=MUTED, lw=0.8, ls="--")
    ax.plot(R.index[flag], R[flag], "o", color=RED, ms=4)
    ax.set_ylabel("Remainder (MW)", fontsize=11)
    ax.text(R.index[1000], lo - 90, "Bounds: 3 IQR beyond the quartiles", fontsize=9, color=MUTED, ha="center", va="top")
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    for a in axes:
        clean(a)
    save(fig, "fc3-anomalies.png")


# ---------------------------------------------------------------- hierarchy diagram
def hierarchy_figure():
    fig, ax = plt.subplots(figsize=(9.6, 3.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 40); ax.axis("off")

    def box(x, y, w, txt, fill=LIGHT, edge=BORDER, color=TEXT, bold=False):
        ax.add_patch(plt.Rectangle((x - w / 2, y - 2.6), w, 5.2, facecolor=fill, edgecolor=edge, lw=1))
        ax.text(x, y, txt, ha="center", va="center", fontsize=10, color=color,
                fontweight="bold" if bold else "normal")

    def line(x0, y0, x1, y1):
        ax.plot([x0, x1], [y0 - 2.6, y1 + 2.6], color=MUTED, lw=0.9)

    box(32, 35, 18, "Australia (total)", fill=GREY, edge=GREY, color="white", bold=True)
    states = [("NSW", 10), ("VIC", 22), ("QLD", 32), ("...", 40), ("TAS", 47), ("NT", 55)]
    for s, x in states:
        if s != "...":
            line(32, 35, x, 22)
        box(x, 22, 7.5, s, fill="white" if s == "..." else LIGHT, edge="white" if s == "..." else BORDER)
    regions = [("Sydney", 5, "NSW"), ("Blue Mtns", 15, "NSW"), ("Melbourne", 25, "VIC"),
               ("...", 37, None), ("Kakadu", 50, "NT"), ("Darwin", 60, "NT")]
    sx = dict(states)
    for r, x, s in regions:
        if s:
            line(sx[s], 22, x, 9)
        box(x, 9, 9, r, fill="white" if s is None else LIGHT, edge="white" if s is None else BORDER)
    ax.text(32, 2.2, "1 total  ·  8 states and territories  ·  76 regions", ha="center", fontsize=10, color=MUTED)
    # grouping by purpose
    ax.add_patch(plt.Rectangle((69, 4), 30.5, 34, facecolor="white", edgecolor=RED, lw=1.2))
    ax.text(84.5, 34.5, "Crossed with purpose", ha="center", fontsize=10.5, color=RED, fontweight="bold")
    for i, p in enumerate(["Business", "Holiday", "Visiting friends/relatives", "Other"]):
        box(84.5, 29 - i * 6, 27, p)
    ax.text(84.5, 6.2, "304 bottom series: region × purpose", ha="center", fontsize=9.5, color=TEXT)
    ax.text(66.5, 21, "×", ha="center", va="center", fontsize=20, color=RED)
    save(fig, "fc3-hierarchy.png")


def save(fig, name):
    fig.savefig(HERE / name, bbox_inches="tight", pad_inches=0.08, facecolor="white", dpi=200)
    plt.close(fig)
    print("wrote", HERE / name)


def clean(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=10, length=3)


if __name__ == "__main__":
    data_dir = sys.argv[1] if len(sys.argv) > 1 else None
    hierarchy_figure()
    intermittent(path("pbs", data_dir))
    anomalies(path("vic_elec", data_dir))
    tourism(path("tourism", data_dir))
