---
course: Data Analytics
session: 13
title: Time Series Forecasting II
subtitle: Practice tasks on lag and calendar features, external regressors, quantile forecasts and interval scores — plus a portfolio-style reserve forecast for the grid operator
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 13 on your own or in the lab. Tasks 1–4 need only paper, pencil and a calculator. Tasks 5 and 6 use Python with pandas, statsmodels (Seabold & Perktold, 2010) and scikit-learn (Pedregosa et al., 2011) on the electricity demand data from the lab (O'Hara-Wild et al., 2022). Load the data as in the session 11 lab starter and build the feature table `X` as in the session 13 lab starter:

```python
import numpy as np, pandas as pd
URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/tsibbledata/vic_elec.csv")
df = pd.read_csv(URL).drop(columns="rownames")
df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
df = df.set_index("Time")
daily = df.resample("D").agg({"Demand": "mean", "Temperature": "max", "Holiday": "max"})
daily.index = daily.index.tz_localize(None)
daily = daily.asfreq("D")
y = daily["Demand"]                                 # 1,096 days
```

The terms follow the slides (Hyndman & Athanasopoulos, 2021): forecast origin *T*, horizon *h*, target day *t* = *T* + *h*; error *e* = *y* − *ŷ*; lag *k* of day *t* = the value *k* days before *t*; ex ante and ex post forecasts; an 80 % prediction interval [ℓ, *u*] with α = 0.2; coverage, width and Winkler score; pinball loss for a quantile *p*: *p* · (*y* − *q*) if the actual *y* lies above the quantile forecast *q*, otherwise (1 − *p*) · (*q* − *y*). The evaluation always uses the 26 folds of 14 days in 2014 from session 12.

## True or False?

Decide whether each statement is true or false and give a one-sentence reason.

1. A gradient boosting model that uses yesterday's demand as a feature can be used directly to forecast the next 14 days.
2. The holiday flag of a future day may be used in an ex ante forecast.
3. An ex post forecast that uses the observed temperature shows how well the model would have worked in practice.
4. A prediction interval from a regression model with temperature as a regressor includes the uncertainty of the temperature forecast.
5. If the 80 % intervals of a method cover 80 % of all test days, they also cover about 80 % of the days in each season.
6. With the pinball loss for *p* = 0.9, an actual that is 100 MW above the forecast costs nine times as much as one that is 100 MW below.

::: answer lines=8
:::

::: solution
1. **False.** For *h* ≥ 2, yesterday's demand of the target day is not known at the origin; the model needs lags ≥ *h* (direct strategy) or must feed its own forecasts back (recursive strategy; Ben Taieb et al., 2012).
2. **True.** The calendar, including public holidays, is known in advance — calendar features are always ex ante.
3. **False.** Ex post forecasts use later information on the regressors; they show the error of the model alone and are a lower bound for the error with a real temperature forecast (Hyndman & Athanasopoulos, 2021, Section 7.6).
4. **False.** Regression prediction intervals treat the regressor values as known; with forecast regressors, the intervals are too narrow (Hyndman & Athanasopoulos, 2021, Section 7.6).
5. **False.** Coverage can differ strongly between seasons: in the lab, SARIMA intervals covered 85.7 % of all days, but only 39.3 % in January–February and 94.2 % in March–December.
6. **True.** Above the forecast: 0.9 × 100 = 90; below: 0.1 × 100 = 10. The asymmetry pushes the forecast up to the 90 % quantile.

Marking: 1 point per statement with a correct reason (6 points); no point for a correct verdict without reason.
:::

## A Feature Table by Hand

A bike rental station records its rentals per day (Monday, day 1, to Sunday, day 21):

| | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| Week 1 (days 1–7) | 120 | 115 | 130 | 125 | 150 | 210 | 190 |
| Week 2 (days 8–14) | 118 | 122 | 128 | 131 | 160 | 225 | 200 |
| Week 3 (days 15–21) | 110 | 126 | 135 | 129 | 155 | 198 | 205 |

On Sunday evening (origin, day 21) the operator forecasts days 22–28 (*h* = 1 … 7) with **one** gradient boosting model for all horizons.

1. Which lags of the target day may this model use? Explain with the target day 28.
2. Compute the features *lag 7*, *lag 14* and *mean7_lag7* (mean of lags 7 to 13) for the target days 22 (Monday), 24 (Wednesday) and 28 (Sunday).
3. The operator wants to add: (a) the rentals of day 23 for target day 24, (b) a city festival planned for day 26, (c) the rain forecast for days 22–28 issued on day 21, (d) the measured rainfall of days 22–28. Which may be used, and which kind of forecast would each make?
4. For *h* = 1 a second model could use lag 1. Name one advantage and one disadvantage of using seven separate models (one per horizon).

::: answer lines=12
:::

::: hint
Lag *k* of day *t* is day *t* − *k*. For the hardest target day (*h* = 7), the newest known day is the origin.
:::

::: solution
1. Lags **≥ 7**. For day 28 (*h* = 7), the last known day is day 21 = lag 7; lags 1–6 (days 22–27) lie after the origin. One model for all horizons must use features that are known for the longest horizon.
2. Features:

| Target day | lag 7 | lag 14 | mean7_lag7 (days) | mean7_lag7 |
|---|---|---|---|---|
| 22 (Mon) | 110 (day 15) | 118 (day 8) | days 9–15: 1,076 / 7 | **153.7** |
| 24 (Wed) | 135 (day 17) | 128 (day 10) | days 11–17: 1,087 / 7 | **155.3** |
| 28 (Sun) | 205 (day 21) | 200 (day 14) | days 15–21: 1,058 / 7 | **151.1** |

3. (a) **Not allowed**: day 23 is unknown on day 21 (leakage). (b) **Allowed**, ex ante: planned events are known in advance — if the plan is stored as it was known on day 21. (c) **Allowed**, ex ante: a forecast available at the origin; training data should also contain forecasts as issued, not measurements. (d) **Not allowed** for a real forecast; usable only for an ex post analysis of how much a perfect rain forecast would help.
4. Advantage: short horizons can use recent lags (day 21 for *h* = 1), which usually improves the first days. Disadvantages: seven models to train, monitor and explain; each model sees the same amount of data, and forecasts for neighbouring days can be inconsistent (Ben Taieb et al., 2012, compare such strategies).

Marking (10 points): 1 rule with reason (2); 2 nine values (3, deduct 1 per two errors); 3 four inputs (4); 4 one advantage and one disadvantage (1).
:::

## Known in Advance, Forecast or Not Available?

For each business, sort the candidate regressors into **known in advance**, **must be forecast** and **not available** at the origin, and say how you would evaluate the model honestly.

| Business and forecast | Candidate regressors |
|---|---|
| A supermarket chain forecasts sales per store and day, 7 days ahead | Own promotion calendar; competitor's promotions; outdoor temperature; public holidays; number of customers in the store on the target day; payday at the start of the month |
| A hospital forecasts emergency department arrivals per day, 3 days ahead | Weekday; school holidays; daily maximum temperature; flu cases reported to the health authority on the target day; a large music festival nearby |
| A call centre forecasts calls per hour, 14 days ahead | Planned mailing of 200,000 invoices; a website outage on the target day; the number of open complaints at the origin; public holidays |

Afterwards: the supermarket's warehouse stores only the promotions that were **executed**, with their final dates. Why is this a problem for training the model, and how does the bitemporal idea from session 11 help?

::: answer lines=12
:::

::: solution
| Business | Known in advance | Must be forecast | Not available |
|---|---|---|---|
| Supermarket | Own promotion calendar, public holidays, payday | Outdoor temperature; competitor promotions (if they can be anticipated, e.g. from leaflets — otherwise not available) | Customers in the store on the target day |
| Hospital | Weekday, school holidays, the music festival (planned event) | Maximum temperature; flu activity (forecast or the latest report as a lag) | Flu cases reported on the target day |
| Call centre | Planned mailing, public holidays, open complaints at the origin (a value known at *T*, used as a lag-type feature) | — | The website outage (unplanned; at most a scenario) |

Honest evaluation: **ex ante**, i.e. in every fold use only what was known at the origin — regressor forecasts as they were issued, plans as they existed. An additional **ex post** run with observed values shows how much better regressor forecasts would help (Hyndman & Athanasopoulos, 2021, Section 7.6).

Executed promotions: the warehouse shows the promotions as they finally happened (moved, extended or cancelled ones are corrected or missing). A model trained on them learns from better information than the planner had at the origin, so the backtest is too optimistic. With a bitemporal promotion table (valid time = promotion period, transaction time = when the plan was recorded), the feature for each fold can be taken "as known on the origin day" (Snodgrass, 1999).

Marking (10 points): classification of the 15 regressors (6, deduct 1 per two errors; accept well-argued alternatives, e.g. competitor promotions as not available); ex ante / ex post evaluation (2); executed promotions and as-of features (2).
:::

## Scoring Interval and Quantile Forecasts

A call centre receives 80 % interval forecasts of the daily number of calls from two providers:

| Day | Actual | A: lower | A: upper | B: lower | B: upper |
|---|---|---|---|---|---|
| 1 | 520 | 500 | 560 | 450 | 600 |
| 2 | 610 | 540 | 600 | 480 | 630 |
| 3 | 480 | 470 | 530 | 420 | 570 |
| 4 | 700 | 560 | 620 | 500 | 650 |
| 5 | 550 | 520 | 580 | 460 | 610 |

1. Compute coverage, mean width and the mean Winkler score (α = 0.2) of A and B.
2. The upper bounds are the 90 % quantile forecasts. Compute the mean pinball loss (*p* = 0.9) of A and B.
3. Which provider would you choose for staffing, where too few agents (long waiting times) is much worse than too many? Why are five days not enough for the decision?
4. A third provider uses a model with point forecast 560 and forecast standard deviation σ̂ₕ = 50 for day 1. Give its 80 % and 95 % model-based intervals and state the assumption behind them.

::: answer lines=14
:::

::: hint
Winkler score per day: width, plus 2/α = 10 times the distance by which the actual lies outside the interval.
:::

::: solution
1. Widths: A 60 every day, B 150 every day.

| Day | A inside? | A Winkler | B inside? | B Winkler |
|---|---|---|---|---|
| 1 | yes | 60 | yes | 150 |
| 2 | no, 10 above | 60 + 100 = 160 | yes | 150 |
| 3 | yes | 60 | yes | 150 |
| 4 | no, 80 above | 60 + 800 = 860 | no, 50 above | 150 + 500 = 650 |
| 5 | yes | 60 | yes | 150 |

A: coverage **60 %**, width **60**, Winkler **240**. B: coverage **80 %**, width **150**, Winkler **250**.

2. Pinball loss (*p* = 0.9) per day — A: 0.1 × 40 = 4; 0.9 × 10 = 9; 0.1 × 50 = 5; 0.9 × 80 = 72; 0.1 × 30 = 3 → mean **18.6**. B: 0.1 × 80 = 8; 0.1 × 20 = 2; 0.1 × 90 = 9; 0.9 × 50 = 45; 0.1 × 60 = 6 → mean **14.0**.
3. **B**: its coverage is close to 80 % and its upper bound (the staffing-relevant quantile) has the lower pinball loss; A's narrow intervals look precise but were exceeded on two of five days, exactly the costly case. The Winkler score slightly favours A here because it rewards narrowness — one more large miss would reverse it. Five days give a coverage estimate with a huge uncertainty (one day = 20 percentage points); evaluate over many origins and per season or weekday (Hyndman & Athanasopoulos, 2021, Sections 5.9 and 5.10).
4. 80 %: 560 ± 1.28 × 50 = **496 to 624**; 95 %: 560 ± 1.96 × 50 = **462 to 658**. Assumption: normally distributed, uncorrelated forecast errors with the stated standard deviation (Hyndman & Athanasopoulos, 2021, Section 5.5).

Marking (12 points): 1 coverage, width and Winkler for both (5); 2 pinball loss for both (3); 3 choice with reason and the sample-size argument (2); 4 both intervals and the assumption (2).
:::

## One Model or One Model per Horizon?

The lab model uses only lags ≥ 14 for all horizons. Test the **direct strategy** with one model per horizon *h* = 1 … 14 on the 26 folds in 2014.

1. For each *h*, build the features: calendar (weekday, day of year, holiday, Christmas period), *lag h*, the latest same weekday (lag 7 · ⌈*h*/7⌉), the mean of lags *h* to *h* + 6, and lag 364.
2. In each fold, train model *h* on the training days and forecast only the test day at position *h*. Compute the MAE per horizon and overall.
3. Compare per horizon with the single model (lags ≥ 14) and with SARIMA(2,0,2)(0,1,1)₇ from session 12. For which horizons is which method best?
4. Explain the result. What would you recommend for a planner who needs days 1–3 and days 8–14?

::: answer lines=10
:::

::: hint
Use `HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0)` as in the lab. For the single model and SARIMA, store the error matrix (26 × 14) from the lab and average over axis 0.
:::

::: solution
Code (tested with pandas 3.0.6, scikit-learn 1.9.1; 14 × 26 model fits):

```python
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import TimeSeriesSplit

cal = pd.DataFrame(index=y.index)
cal["dow"], cal["doy"] = y.index.dayofweek, y.index.dayofyear
cal["holiday"] = daily["Holiday"].astype(int)
md = y.index.month * 100 + y.index.day
cal["xmas"] = ((md >= 1224) | (md <= 102)).astype(int)

def feats(h):
    X = cal.copy()
    X["lag_h"] = y.shift(h)
    X["same_wd"] = y.shift(7 * int(np.ceil(h / 7)))
    X["mean7"] = y.shift(h).rolling(7).mean()
    X["lag364"] = y.shift(364)
    return X

Xs = {h: feats(h) for h in range(1, 15)}
E = []
for tr, te in TimeSeriesSplit(n_splits=26, test_size=14).split(y):
    row = []
    for h in range(1, 15):
        m = HistGradientBoostingRegressor(max_iter=300, learning_rate=0.05, random_state=0)
        m.fit(Xs[h].iloc[tr], y.iloc[tr])
        row.append(y.iloc[te[h - 1]] - m.predict(Xs[h].iloc[[te[h - 1]]])[0])
    E.append(row)
E = np.array(E)
print(np.abs(E).mean(), np.abs(E).mean(axis=0).round(0))
```

MAE (MW) per horizon, 26 folds in 2014:

| *h* | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | All |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Direct (per *h*) | 191 | 267 | 186 | 217 | 268 | 269 | 261 | 274 | 261 | 196 | 228 | 200 | 310 | 316 | 245.9 |
| Single model, lags ≥ 14 | 236 | 221 | 214 | 228 | 222 | 224 | 221 | 276 | 256 | 241 | 223 | 214 | 322 | 335 | 245.2 |
| SARIMA | 140 | 218 | 157 | 236 | 215 | 225 | 218 | 303 | 356 | 313 | 303 | 349 | 399 | 361 | 270.9 |

- Days 1–7: SARIMA best on average (MAE 201, single GBM 224, direct 237); SARIMA wins at *h* = 1, 2, 3, 5, 6 and 7 against the direct models.
- Days 8–14: gradient boosting clearly better (direct 255, single 267, SARIMA 341).
- Overall, the direct strategy is **not** better than the single model (245.9 vs. 245.2); it wins in only 10 of 26 folds. Recent lags help at *h* = 1 (191 vs. 236), but the per-horizon MAEs jump around: each model sees noisy, partly redundant lags, and with 26 values per horizon one heat-wave day can move an MAE by 50 MW.

Interpretation and recommendation: short horizons profit from the autocorrelation (yesterday's level), long horizons from the calendar — so the best method depends on the horizon. For days 1–3 use SARIMA (or a model with recent lags), for days 8–14 gradient boosting with calendar features; a combination by horizon must then be chosen on the validation year 2013, not on these 2014 results, to avoid selecting on the test data.

Marking (12 points): 1–2 correct features without leakage and correct test position per *h* (5); 3 table and per-horizon comparison (3); 4 explanation (autocorrelation vs. calendar; noise with 26 folds) and a recommendation that keeps the selection on validation data (4).
:::

## Portfolio-Style Task: A Reserve Forecast for the Grid Operator

The grid operator from worksheet 12 now asks: *"Give us, two weeks ahead, a demand level that is exceeded on at most one day in ten — using only information we really have on the forecast day."* Write a short notebook that answers the question.

- **Point model (ex ante):** gradient boosting with calendar, lags ≥ 14 and the temperature climatology (mean daily maximum of the training years within ±7 calendar days of the target day, computed per fold).
- **Three 90 % bounds:** (a) the point forecast plus the 90 % quantile of the forecast errors of the validation year 2013; (b) quantile gradient boosting with `quantile=0.9`, `max_iter=100`, `min_samples_leaf=50`; (c) the upper bound of the 80 % SARIMA interval.
- **Evaluation** on the 26 folds of 2014: exceedance rate overall, January–February and March–December; mean bound; mean pinball loss (*p* = 0.9); the largest shortfall.
- **Improvement:** one seasonal variant of bound (a), chosen on 2013 only.
- **Memo** for the grid operator: answer first, evidence, limits, next step — at most eight sentences.

::: answer lines=8
:::

::: hint
Exceedance = share of days with actual > bound; the target is 10 %. For the seasonal variant, compute the 90 % error quantile separately for target days in December–February and in the other months of 2013.
:::

::: solution
Code outline (tested with pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1; `X` from the lab starter, `cv_gbm`-style loop with a per-fold climatology):

```python
def climatology(temp_train, idx, window=7):
    doy, v = temp_train.index.dayofyear.to_numpy(), temp_train.to_numpy()
    return np.array([v[np.minimum(abs(doy - d), 365 - abs(doy - d)) <= window].mean()
                     for d in idx.dayofyear])

cols = ["dow", "doy", "holiday", "xmas", "lag14", "lag21", "lag28", "lag364", "mean7_lag14", "temp"]
def run(end, **kw):                       # kw: e.g. loss="quantile", quantile=0.9, ...
    yy, F, Y = y[:end], [], []
    for tr, te in TimeSeriesSplit(n_splits=26, test_size=14).split(yy):
        Xtr, Xte = X.iloc[tr][cols].copy(), X.iloc[te][cols].copy()
        Xte["temp"] = climatology(daily["Temperature"].iloc[tr], yy.index[te])
        m = HistGradientBoostingRegressor(**({"max_iter": 300, "learning_rate": 0.05,
                                              "random_state": 0} | kw)).fit(Xtr, yy.iloc[tr])
        F.append(m.predict(Xte)); Y.append(yy.iloc[te].to_numpy())
    return np.array(F), np.array(Y)

F_val, Y_val = run("2013-12-31"); F, Y = run("2014-12-31")
k = np.quantile(Y_val - F_val, 0.9)                          # 386 MW
bound_a = F + k
bound_b, _ = run("2014-12-31", loss="quantile", quantile=0.9, max_iter=100, min_samples_leaf=50)
pinball = lambda u: np.where(Y >= u, 0.9 * (Y - u), 0.1 * (u - Y)).mean()
```

Results, 26 folds × 14 days in 2014 (point model: MAE 228.5 MW; January–February 639, March–December 154):

| 90 % bound | Exceeded overall | Jan–Feb | Mar–Dec | Mean bound (MW) | Pinball loss |
|---|---|---|---|---|---|
| (a) Point + error quantile 2013 (+386 MW) | 7.1 % | 30.4 % | 2.9 % | 4,982 | 79.4 |
| (b) Quantile gradient boosting | 22.5 % | 30.4 % | 21.1 % | 4,792 | 85.1 |
| (c) SARIMA, upper 80 % bound | 7.1 % | 33.9 % | 2.3 % | 5,124 | 83.9 |
| Seasonal (a): +780 MW in Dec–Feb, +307 MW otherwise | 6.9 % | 21.4 % | 4.2 % | 5,018 | **69.1** |
| For comparison: point forecast only | 47.0 % | 44.6 % | 47.4 % | 4,596 | 120.9 |

- (a) and (c) meet the 10 % target **on average**, but the bound is exceeded on almost a third of the January–February days and is far too high for the rest of the year (only 2–3 % exceedances).
- (b) is too low everywhere (22.5 %): quantile trees learn the spread of their training residuals, which is too small; on 2013 the same model was exceeded on 22.3 % of the days, so this was visible before the test year.
- The seasonal bound, with the quantiles chosen on 2013, has the best pinball loss and halves the gap in March–December; summer is still under-covered (21.4 %). The largest shortfall of bound (a) was 2,121 MW (15 January 2014, heat wave); 9 days were more than 500 MW above the bound, all in January–February.

Example memo: "For two-week reserve planning, use the gradient boosting forecast plus a seasonal safety margin of about 780 MW in December–February and 310 MW in the other months. Over 2014 this level was exceeded on 6.9 % of the days, close to the one-in-ten target, and it is more efficient than a single margin. In January and February, however, it was exceeded on about one day in five, by up to 2,100 MW on the heat-wave days — history and average temperatures cannot anticipate a 43 °C day. For summer reserve decisions, add current weather forecasts and heat-wave scenarios; we recommend buying archived weather forecasts so the model can be trained and tested ex ante. Limits: one test year, three years of history, margins estimated from one validation year."

Marking guide (30 points; training only — the portfolio brief and rubric are published separately):

- **Point model** (5 points): features without leakage (2); climatology computed per fold from training years only (2); MAE reported against the session 12 baselines (1).
- **Bounds** (8 points): empirical quantile from 2013 errors, not 2014 (3); quantile model (2); SARIMA bound correctly identified as the upper end of the 80 % interval (1); seasonal variant chosen on 2013 (2).
- **Evaluation** (8 points): exceedance overall and by season (3); pinball loss and mean bound (3); largest shortfalls identified and dated (2).
- **Interpretation and memo** (7 points): answer first (1); average vs. seasonal coverage (2); why quantile trees are too narrow (2); limits and next step (2).
- **Reproducibility** (2 points): runs top to bottom from the URL, versions printed, random states fixed.

A strong submission notices that a bound that is "right on average" fails exactly in the season the grid operator worries about, and keeps every choice (margins, settings) on the validation year.
:::

## References {.references}

- Ben Taieb, S., Bontempi, G., Atiya, A. F., & Sorjamaa, A. (2012). A review and comparison of strategies for multi-step ahead time series forecasting based on the NN5 forecasting competition. *Expert Systems with Applications, 39*(8), 7067–7083. https://doi.org/10.1016/j.eswa.2012.01.039
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- O'Hara-Wild, M., Hyndman, R., Wang, E., & Godahewa, R. (2022). *tsibbledata: Diverse datasets for 'tsibble'* (R package version 0.4.1) [Computer software]. https://CRAN.R-project.org/package=tsibbledata
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*(85), 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 92–96). https://doi.org/10.25080/Majora-92bf1922-011
- Snodgrass, R. T. (1999). *Developing time-oriented database applications in SQL*. Morgan Kaufmann.
