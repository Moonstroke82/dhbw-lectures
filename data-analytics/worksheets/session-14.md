---
course: Data Analytics
session: 14
title: Forecasting at Scale and Use Cases
subtitle: Practice tasks on global models, reconciliation, intermittent demand and anomaly screening — plus a portfolio-style forecast for many series
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 14 on your own or in the lab. Tasks 1–4 need only paper, pencil and a calculator (task 4 has an optional Python part). Tasks 5 and 6 use Python with pandas, statsmodels (Seabold & Perktold, 2010) and scikit-learn (Pedregosa et al., 2011). The data come from the pinned Rdatasets copies used in the session (Arel-Bundock, n.d.): tourism from the R package tsibble (Wang et al., 2020), PBS and vic_elec from tsibbledata (O'Hara-Wild et al., 2022).

```python
BASE = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
        "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/")
TOURISM = BASE + "tsibble/tourism.csv"       # 304 quarterly series
PBS     = BASE + "tsibbledata/PBS.csv"       # monthly prescriptions
VIC     = BASE + "tsibbledata/vic_elec.csv"  # demand, sessions 11-13
```

The terms follow the slides (Hyndman & Athanasopoulos, 2021): **local** model = one model per series, **global** model = one model for all series; summing matrix *S* with **y** = *S* **b** (all series = *S* × bottom series); base, bottom-up, top-down and reconciled forecasts; MASE = MAE divided by the in-sample MAE of the seasonal naive method. For intermittent demand, ADI = number of periods divided by the number of periods with demand, CV² = squared coefficient of variation of the non-zero demand sizes (standard deviation with *n* in the denominator); cut-offs 1.32 and 0.49 (Syntetos et al., 2005). The 3 IQR rule flags residuals more than 3 interquartile ranges below the first or above the third quartile.

## True or False?

Decide whether each statement is true or false and give a one-sentence reason.

1. A global model only works if all series behave in a similar way.
2. Bottom-up forecasts are always coherent.
3. After optimal reconciliation, every series is forecast at least as accurately as by its base forecast.
4. For a series with 70 % zero months, the constant forecast that minimises the MAE is usually zero.
5. During a long run of months without demand, Croston's forecast decreases month by month.
6. A day flagged by the 3 IQR rule on decomposition residuals is a data error and should be removed before modelling.

::: answer lines=8
:::

::: solution
1. **False.** A global model does not assume similar series; it can produce the same forecasts as local models, and simple global models were competitive even on heterogeneous data (Montero-Manso & Hyndman, 2021). Scaling each window to its own level is what makes series comparable.
2. **True.** The upper levels are computed as sums of the bottom forecasts (*S* **b̂**), so they add up by construction.
3. **False.** Reconciliation improves accuracy on average and on many levels, but not for every series: in the session, the total forecast got worse (MASE 1.71 base, 1.75 OLS, 2.18 MinT).
4. **True.** Minimising the MAE leads to the median; with 70 % zeros the median is zero. This is why MAE is a poor measure for intermittent demand (Hyndman & Athanasopoulos, 2021, Section 13.2).
5. **False.** Croston's method updates the size and interval estimates only when demand occurs, so the forecast stays constant during zero runs; this is why it handles obsolescence poorly (Teunter et al., 2011).
6. **False.** Flagged days can be real events (heat waves, holidays, a burst pipe); only data errors should be corrected. Ask why the value is unusual before replacing it (Hyndman & Athanasopoulos, 2021, Section 13.9).

Marking: 1 point per statement with a correct reason (6 points); no point for a correct verdict without reason.
:::

## Coherent Forecasts for a Bike-Sharing Company

A bike-sharing company forecasts rentals for next Saturday. The city has two districts, West (stations W1, W2) and East (stations E1, E2). The analytics team produced these base forecasts, each from a separate model:

| Total | West | East | W1 | W2 | E1 | E2 |
|---|---|---|---|---|---|---|
| 1,000 | 560 | 400 | 300 | 240 | 250 | 170 |

1. Write down the summing matrix *S* (rows: Total, West, East, W1, W2, E1, E2; columns: W1, W2, E1, E2).
2. Show three places where the base forecasts are incoherent, with the size of each gap.
3. Compute the **bottom-up** forecasts for all seven series and the **top-down** forecasts with historical shares W1 32 %, W2 24 %, E1 26 %, E2 18 %.
4. The OLS-reconciled forecasts are: Total 982.9, West 564.8, East 418.1, W1 312.4, W2 252.4, E1 249.0, E2 169.0. Check that they are coherent. Which base forecasts were changed most, and why does that make sense here?
5. The fleet manager plans bikes per station, the city council receives the total. Which approach would you recommend, and what would you check before using it?

::: answer lines=12
:::

::: hint
Each row of *S* has a 1 for every station that belongs to that series. Coherent means: every aggregate equals the sum of its children.
:::

::: solution
1. *S* (columns W1, W2, E1, E2): Total (1, 1, 1, 1); West (1, 1, 0, 0); East (0, 0, 1, 1); W1 (1, 0, 0, 0); W2 (0, 1, 0, 0); E1 (0, 0, 1, 0); E2 (0, 0, 0, 1).
2. W1 + W2 = 540, but West = 560 (gap 20). E1 + E2 = 420, but East = 400 (gap −20). West + East = 960, but Total = 1,000 (gap 40); the bottom forecasts also sum to 960.
3. Bottom-up: W1 300, W2 240, E1 250, E2 170, West 540, East 420, Total 960. Top-down: W1 320, W2 240, E1 260, E2 180, West 560, East 440, Total 1,000.
4. Coherence: 312.4 + 252.4 = 564.8 (West), 249.0 + 169.0 = 418.1 (East, rounding), 564.8 + 418.1 = 982.9 (Total). Changes: Total −17.1, East +18.1, W1 and W2 +12.4 each, West +4.8, E1 and E2 −1.0 each. OLS moves all forecasts so that the gaps close with the smallest total squared change: the total was "too high" compared with the stations, East "too low" compared with E1 + E2 — these two move most. E1 and E2 hardly change because East and its stations conflict in the opposite direction to the total, and the effects cancel.
5. Optimal reconciliation (OLS, or MinT if past forecast errors are available): one coherent set for both users, using the information of all levels (Hyndman & Athanasopoulos, 2021, Section 11.3; Wickramasuriya et al., 2019). Check on past Saturdays (rolling origin) whether the reconciled forecasts are at least as accurate as the base forecasts at station level, and that no reconciled value is negative (possible for small stations). Bottom-up alone would ignore the more stable district and total forecasts; top-down ignores station-level information such as a closed station.

Marking (10 points): 1 matrix (2); 2 three gaps (2); 3 both sets of forecasts (2); 4 coherence check and explanation (2); 5 recommendation with a check (2).
:::

## Spare Parts: Classify and Forecast

A machine builder records the monthly demand of three spare parts over the last 12 months:

| Part | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 0 | 0 | 4 | 0 | 0 | 0 | 5 | 0 | 0 | 3 | 0 | 0 |
| B | 2 | 0 | 15 | 1 | 0 | 0 | 30 | 0 | 1 | 0 | 0 | 8 |
| C | 10 | 12 | 9 | 11 | 0 | 10 | 13 | 8 | 11 | 12 | 9 | 10 |

1. Compute ADI and CV² for each part and classify it as smooth, erratic, intermittent or lumpy.
2. Apply **Croston's method** with α = 0.2 to part A. Start with the first demand (size 4, interval 3 months). Give the forecast per month and the SBA version (factor 1 − α/2).
3. Compare with the mean of the 12 months and with SES (α = 0.2, starting level = first value). In the next six months, part A has demand 0, 0, 6, 0, 0, 0. Compute the MAE and the mean error (actual − forecast) of the zero forecast, the mean and Croston.
4. The planner orders six months' forecast at once. Which forecast would you use, and why is the MAE misleading here?

::: answer lines=14
:::

::: hint
For CV², use only the months with demand. In Croston's method, size and interval are updated only in months with demand; the interval is the number of months since the previous demand.
:::

::: solution
1. Classification:

| Part | Months with demand | ADI | Mean size | SD of sizes | CV² | Class |
|---|---|---|---|---|---|---|
| A | 3 | 12 / 3 = **4.0** | 4.0 | 0.82 | **0.04** | Intermittent |
| B | 6 | 12 / 6 = **2.0** | 9.5 | 10.44 | **1.21** | Lumpy |
| C | 11 | 12 / 11 = **1.09** | 10.45 | 1.44 | **0.02** | Smooth |

2. Croston for part A: start *q* = 4, *p* = 3. Month 7 (demand 5, interval 4): *q* = 0.2 · 5 + 0.8 · 4 = 4.2; *p* = 0.2 · 4 + 0.8 · 3 = 3.2. Month 10 (demand 3, interval 3): *q* = 0.2 · 3 + 0.8 · 4.2 = 3.96; *p* = 0.2 · 3 + 0.8 · 3.2 = 3.16. Forecast = 3.96 / 3.16 = **1.25 per month**; SBA: 1.25 × 0.9 = **1.13** (Croston, 1972; Syntetos & Boylan, 2005).
3. Mean of 12 months: 12 / 12 = **1.0**. SES (α = 0.2, start 0): **0.82** after month 12 — it is pulled down by the two zero months after the last demand.

| Forecast | MAE | Mean error | Six-month order |
|---|---|---|---|
| Zero | **1.00** | +1.00 | 0 |
| Mean (1.0) | 1.67 | 0.00 | 6.0 |
| Croston (1.25) | 1.84 | −0.25 | 7.5 |

4. The MAE prefers the zero forecast, which would leave the customer without the part in month 3; the actual six-month demand was 6. The mean or Croston/SBA give an order of 6–7.5 parts and cover it. For intermittent items, judge forecasts by their bias and by the stock outcome (service level, holding cost), not by the MAE (Hyndman & Athanasopoulos, 2021, Section 13.2). With only three demands, any forecast is uncertain; the planner should also look at lead time and the cost of a stock-out.

Marking (12 points): 1 ADI, CV² and class for three parts (4); 2 Croston steps and both forecasts (4); 3 table (2); 4 recommendation with the MAE argument (2).
:::

## Screening Residuals for Anomalies

A water utility forecasts daily consumption (thousand m³) with a model that includes weekday, holidays and temperature. The residuals (actual − model value) of 14 days are:

| Day | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Residual | 2 | −3 | 1 | 0 | 4 | −1 | −2 | 3 | 25 | 1 | −2 | −18 | 0 | 2 |

1. Compute the quartiles (median of the lower and of the upper seven values), the IQR and the bounds of the 3 IQR rule. Which days are flagged?
2. The operations log says: day 9 — a water main burst, repaired in the evening; day 12 — a meter at the main inlet sent no data from noon. For each day, decide whether it is an **event** or a **data error**, and what to do with it for (a) the training data of the forecast model and (b) the monthly report.
3. Why are the residuals of a model with temperature a better basis than the remainder of a plain seasonal decomposition?
4. *(Python, optional)* Apply the 3 IQR rule to the MSTL remainder of the daily vic_elec demand (session 11 lab starter). How many days are flagged? Then halve the demand of 20 August 2014 and run it again: is the planted error found?

::: answer lines=12
:::

::: hint
Sorted residuals: −18, −3, −2, −2, −1, 0, 0, 1, 1, 2, 2, 3, 4, 25.
:::

::: solution
1. Lower half −18, −3, −2, −2, −1, 0, 0 → Q1 = **−2**; upper half 1, 1, 2, 2, 3, 4, 25 → Q3 = **2**; IQR = 4. Bounds: −2 − 3 · 4 = **−14** and 2 + 3 · 4 = **14**. Flagged: day 9 (+25) and day 12 (−18). The quartiles are hardly affected by the two extreme values — that is why the rule is robust.
2. Day 9: an **event** (water really flowed out). (a) Exclude it from training or add an indicator, so the model does not learn a "normal" day with +25; (b) keep it in the report — the loss is real and costs money. Day 12: a **data error** (missing half-day). (a) Set it to missing and impute it, e.g. from the model value; (b) report the corrected value and note the meter failure. Never replace values without knowing why they are unusual (Hyndman & Athanasopoulos, 2021, Section 13.9; Blázquez-García et al., 2021).
3. A plain decomposition knows only the calendar pattern: every hot day would be flagged, and with few years the seasonal component can absorb extreme periods. A model with the known drivers (temperature, holidays) explains these days, so the remaining residuals point to what is really unexplained. In the session, MSTL did not flag the record heat-wave day of 16 January 2014, and it missed a planted data error that the model residuals found.
4. Code and results (tested with statsmodels 0.15.0):

```python
from statsmodels.tsa.seasonal import MSTL
def flags(r, k=3):
    q1, q3 = r.quantile([0.25, 0.75])
    return r[(r < q1 - k * (q3 - q1)) | (r > q3 + k * (q3 - q1))]
R = MSTL(y, periods=(7, 365)).fit().resid
print(len(flags(R)))                                  # 34 days, 26 of them in 2013
yp = y.copy(); yp["2014-08-20"] *= 0.5                # planted error: 5,152 -> 2,576 MW
Rp = MSTL(yp, periods=(7, 365)).fit().resid
print(Rp["2014-08-20"], "2014-08-20" in flags(Rp).index.strftime("%Y-%m-%d"))
```

34 days are flagged (bounds about −485 and +481 MW): mostly heat days and holidays in 2013. The planted error is **not** found: its remainder is only −445 MW because trend and seasonal components absorb part of it. The cross-validated errors of the session 13 gradient boosting model (calendar and observed temperature) flag it with −2,700 MW.

Marking (10 points): 1 quartiles, bounds and flagged days (3); 2 event vs. error with treatment for training and report (3); 3 argument for model residuals (2); 4 count and planted-error result, or a well-argued expectation without Python (2).
:::

## Is Reconciliation Robust? {.optional}

Repeat the reconciliation of the session on the tourism data for a second forecast origin and add MinT.

1. Build *S* and *Y* as in the lab starter. Produce ETS base forecasts for 8 quarters from two origins: training to **2013 Q4** (test 2014–2015) and to **2015 Q4** (test 2016–2017). Keep the in-sample residuals (`fit.resid`) of each chosen model.
2. Reconcile with bottom-up, OLS, WLS (structural) and MinT with a shrinkage covariance of the residuals.
3. Report the mean MASE per level and over all 425 series for both origins. Is the ranking stable?
4. Count the reconciled forecasts below zero for each method. What would you do with them?

::: answer lines=10
:::

::: hint
Shrinkage covariance (Schäfer–Strimmer, as used for MinT): standardise the residuals, shrink the off-diagonal correlations towards zero by an estimated factor λ, and scale back. The function `shrink_cov` in the session's figure script (make_fc3_figures.py) does this in 15 lines; then `reconcile(base, W)` from the lab starter.
:::

::: solution
Code (tested with pandas 3.0.6, statsmodels 0.15.0):

```python
def shrink_cov(R):                                    # R: 425 series x T residuals
    T = R.shape[1]
    X = R - R.mean(axis=1, keepdims=True)
    sd = X.std(axis=1, ddof=1)
    Z = X / sd[:, None]
    C = Z @ Z.T / (T - 1)                             # correlation matrix
    V = np.einsum("it,jt->ijt", Z, Z)
    var = T / (T - 1) ** 3 * ((V - (C * (T - 1) / T)[:, :, None]) ** 2).sum(axis=2)
    off = ~np.eye(len(sd), dtype=bool)
    lam = np.clip(var[off].sum() / (C[off] ** 2).sum(), 0, 1)
    Cs = C * (1 - lam); np.fill_diagonal(Cs, 1)
    return Cs * np.outer(sd, sd)

def run(last, h=8):
    tr, te = Y[:, :last], Y[:, last:last + h]
    base, res = [], []
    for y in tr:
        fits = [ETSModel(y, error="add", trend=t_, damped_trend=t_ is not None, seasonal=s_,
                         seasonal_periods=4).fit(disp=False)
                for t_ in (None, "add") for s_ in (None, "add")]
        f = min(fits, key=lambda f: f.aicc)
        base.append(f.forecast(h)); res.append(f.resid)
    base, res = np.array(base), np.array(res)
    F = {"base": base, "bottom-up": S @ base[-304:], "OLS": reconcile(base, np.eye(425)),
         "WLS": reconcile(base, np.diag(S.sum(axis=1))), "MinT": reconcile(base, shrink_cov(res))}
    scale = np.abs(tr[:, 4:] - tr[:, :-4]).mean(axis=1)
    return {k: np.abs(te - f).mean(axis=1) / scale for k, f in F.items()}, F

mase_2013, F_2013 = run(64)                           # training to 2013 Q4
mase_2015, F_2015 = run(72)                           # training to 2015 Q4
```

Mean MASE (State = mean over the 8 state series, Region = over the 76 region series):

| Method | Total | State | Region | Bottom | All 425 | Total | State | Region | Bottom | All 425 |
|---|---|---|---|---|---|---|---|---|---|---|
| | *Origin 2013 Q4* | | | | | *Origin 2015 Q4* | | | | |
| Base | 3.44 | 2.37 | 1.24 | 1.03 | 1.16 | 1.71 | 1.34 | 1.12 | 0.99 | 1.04 |
| Bottom-up | 3.71 | 2.40 | 1.24 | 1.03 | 1.17 | 3.31 | 2.04 | 1.24 | 0.99 | 1.11 |
| OLS | 3.45 | 2.35 | 1.21 | 1.05 | 1.17 | 1.75 | 1.32 | 1.00 | 1.00 | 1.01 |
| WLS | 3.55 | 2.34 | 1.21 | 1.03 | 1.16 | 2.27 | 1.51 | 1.04 | 0.98 | 1.02 |
| MinT | 3.54 | 2.35 | 1.22 | **1.01** | **1.15** | 2.19 | 1.47 | 1.03 | **0.93** | **0.99** |

- Stable: MinT is best over all series and at the bottom level for both origins; bottom-up is worst at the top. Not stable: the size of the differences. From 2013 Q4, all methods are poor at the top (MASE above 3) because the growth from 2014 was not visible in the training data — reconciliation cannot add information that no base forecast has.
- Negative values: OLS produced 14 (origin 2013 Q4) and 19 (2015 Q4) negative forecasts, the lowest −15.6 thousand trips; WLS 0 and 8; MinT none. Negative trips are impossible: set them to zero and report how many were changed (this breaks coherence slightly), or use a method that keeps forecasts non-negative.

Marking (12 points): base forecasts and residuals for two origins without using test data (3); four reconciliations incl. MinT (3); table and stability judgement (4); negative forecasts counted and handled (2).
:::

## Portfolio-Style Task: Prescriptions for 84 Drug Groups

A pharmaceutical wholesaler plans purchases one year ahead. It asks: *"Can one model forecast the monthly prescriptions of all 84 drug groups (ATC2) as well as 84 separate models — and what should we watch out for?"* Write a short notebook on the PBS data (O'Hara-Wild et al., 2022) that answers the question. This task is practice in the style of the notebooks, not part of notebook 3.

- **Data:** monthly scripts summed per ATC2 group (all concession types), July 1991 to June 2008; months without a row count as zero. Screen the series: zeros, groups that stop or restart.
- **Evaluation:** horizon 12 months; validation origin June 2006 (test July 2006–June 2007) for all choices, test origin June 2007 (test July 2007–June 2008) used once. Only groups with scripts in the last two training years are forecast.
- **Methods:** seasonal naive, ETS per group (additive, chosen by AICc), and a global linear autoregression (lab starter, adapted to monthly data) with 12 or 24 months of input, scaled by the mean of the last 12 months.
- **Results:** mean and median MASE, overall bias, the number of groups where the global model wins.
- **Memo:** answer first, evidence, limits, next step — at most eight sentences.

::: answer lines=8
:::

::: hint
In `global_ar`, use the mean of the last 12 months as the level and cut forecasts at zero. Compare the input lengths 12 and 24 on the validation origin only.
:::

::: solution
Code (tested with pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1):

```python
p = pd.read_csv(PBS)
p["M"] = pd.PeriodIndex(pd.to_datetime(p["Month"], format="%Y %b"), freq="M")
W = p.pivot_table(index="M", columns="ATC2", values="Scripts", aggfunc="sum")
W = W.reindex(pd.period_range("1991-07", "2008-06", freq="M")).fillna(0)
Y = W.to_numpy(float).T                                  # 84 groups x 204 months

def ets(y, h=12):
    fits = [ETSModel(y, error="add", trend=t_, damped_trend=t_ is not None, seasonal=s_,
                     seasonal_periods=12).fit(disp=False)
            for t_ in (None, "add") for s_ in (None, "add")]
    return min(fits, key=lambda f: f.aicc).forecast(h)

def global_ar(B, h, L):
    lvl = lambda w: np.maximum(w[:, -12:].mean(axis=1), 0.1 * B.mean(axis=1))
    X, y = [], []
    for o in range(L, B.shape[1] - h + 1):
        w = B[:, o - L:o]; X.append(w / lvl(w)[:, None]); y.append(B[:, o + h - 1] / lvl(w))
    m = LinearRegression().fit(np.vstack(X), np.concatenate(y))
    w = B[:, -L:]
    return np.maximum(m.predict(w / lvl(w)[:, None]) * lvl(w), 0)

def evaluate(last, H=12):
    tr, te = Y[:, :last], Y[:, last:last + H]
    act = tr[:, -24:].sum(axis=1) > 0                    # active in the last two years
    tr, te = tr[act], te[act]
    scale = np.abs(tr[:, 12:] - tr[:, :-12]).mean(axis=1)
    F = {"snaive": tr[:, -12:], "ets": np.array([ets(y) for y in tr])}
    for L in (12, 24):
        F[f"global L={L}"] = np.column_stack([global_ar(tr, h, L) for h in range(1, H + 1)])
    mase = {k: np.abs(te - f).mean(axis=1) / scale for k, f in F.items()}
    bias = {k: (te - f).sum() / te.sum() for k, f in F.items()}
    return act, mase, bias

val = evaluate(W.index.get_loc(pd.Period("2006-06", "M")) + 1)
test = evaluate(W.index.get_loc(pd.Period("2007-06", "M")) + 1)
```

Screening: 84 groups, 120 group-months without a row (set to zero). Seven groups had no scripts in the last two training years (C05, D, G01, J06, M02, R, R01) — codes that were phased out or reclassified; two of them return in the test year (C05 with 7,281 scripts, G01 with 128), which no forecast can anticipate. A05 is still active but has zero scripts in 58 % of the training months — a candidate for an intermittent method. 77 groups are forecast at the test origin (78 at the validation origin).

| 12 months ahead | Validation: mean MASE | Test: mean MASE | Test: median MASE | Test: bias |
|---|---|---|---|---|
| Seasonal naive | 1.026 | 1.318 | 1.379 | +1.6 % |
| ETS per group | 0.879 | 1.038 | **1.075** | +0.6 % |
| Global linear, 12 months input | 0.884 | 1.021 | 1.137 | −0.5 % |
| Global linear, 24 months input | **0.834** | **0.980** | 1.089 | −1.6 % |

Bias = sum of errors / sum of actual scripts (positive: under-forecast).

- On the validation origin, the global model with 24 months of input was best, so it is the choice; on the test year it has the lowest mean MASE (0.98 vs. 1.04 for ETS) and beats ETS in 47 of 77 groups and seasonal naive in 64.
- The median MASE is slightly better for ETS: the global model wins on average because it avoids a few bad local fits, not in every group.
- The hardest groups are hard for both (e.g. V03 and S02 with MASE above 2): look at them individually (code changes, supply issues).

Example memo: "One global model for all drug groups forecasts the next twelve months at least as well as 77 separate ETS models: mean MASE 0.98 vs. 1.04, better in 47 of 77 groups, and it was chosen on a separate validation year. It is simpler to run and monitor — one model with 25 coefficients per horizon instead of 77 model selections. Both approaches miss groups whose codes change: seven groups looked inactive, two of them returned in the test year. We recommend the global model with a data-quality check on new, stopped and restarted codes, and a review list of the groups with the largest errors. Limits: one test year, scripts not units of medicine, no prices or policy changes in the model. Next step: add the concession and safety-net structure as a hierarchy and reconcile."

Marking guide (30 points; training only):

- **Data screening** (6 points): missing months set to zero with a reason (1); inactive and restarting groups identified and handled (3); intermittent candidates noted (2).
- **Evaluation design** (6 points): validation origin for all choices (3); test year used once (2); only information up to the origin (1).
- **Methods** (8 points): seasonal naive and ETS correct (3); global model with correct windows, scaling and no leakage (4); forecasts cut at zero (1).
- **Results and interpretation** (6 points): mean and median MASE, bias, win counts (3); why mean and median disagree (2); hardest groups named (1).
- **Memo** (4 points): answer first (1); evidence and limits (2); next step (1).

A strong submission notices that the global model wins on average but not everywhere, and treats the reclassified codes as a data problem rather than a forecasting problem.
:::

## References {.references}

- Arel-Bundock, V. (n.d.). *Rdatasets: A collection of datasets originally distributed in R packages*. Retrieved October 22, 2026, from https://vincentarelbundock.github.io/Rdatasets/
- Blázquez-García, A., Conde, A., Mori, U., & Lozano, J. A. (2021). A review on outlier/anomaly detection in time series data. *ACM Computing Surveys, 54*(3). https://doi.org/10.1145/3444690
- Croston, J. D. (1972). Forecasting and stock control for intermittent demands. *Operational Research Quarterly, 23*(3), 289–303. https://doi.org/10.1057/jors.1972.50
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- Montero-Manso, P., & Hyndman, R. J. (2021). Principles and algorithms for forecasting groups of time series: Locality and globality. *International Journal of Forecasting, 37*(4), 1632–1653. https://doi.org/10.1016/j.ijforecast.2021.03.004
- O'Hara-Wild, M., Hyndman, R., Wang, E., & Godahewa, R. (2022). *tsibbledata: Diverse datasets for 'tsibble'* (R package version 0.4.1) [Computer software]. https://CRAN.R-project.org/package=tsibbledata
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*(85), 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 92–96). https://doi.org/10.25080/Majora-92bf1922-011
- Syntetos, A. A., & Boylan, J. E. (2005). The accuracy of intermittent demand estimates. *International Journal of Forecasting, 21*(2), 303–314. https://doi.org/10.1016/j.ijforecast.2004.10.001
- Syntetos, A. A., Boylan, J. E., & Croston, J. D. (2005). On the categorization of demand patterns. *Journal of the Operational Research Society, 56*(5), 495–503. https://doi.org/10.1057/palgrave.jors.2601841
- Teunter, R. H., Syntetos, A. A., & Babai, M. Z. (2011). Intermittent demand: Linking forecasting to inventory obsolescence. *European Journal of Operational Research, 214*(3), 606–615. https://doi.org/10.1016/j.ejor.2011.05.018
- Wang, E., Cook, D., & Hyndman, R. J. (2020). A new tidy data structure to support exploration and modeling of temporal data. *Journal of Computational and Graphical Statistics, 29*(3), 466–478. https://doi.org/10.1080/10618600.2019.1695624
- Wickramasuriya, S. L., Athanasopoulos, G., & Hyndman, R. J. (2019). Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization. *Journal of the American Statistical Association, 114*(526), 804–819. https://doi.org/10.1080/01621459.2018.1448825
