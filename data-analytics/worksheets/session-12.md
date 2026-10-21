---
course: Data Analytics
session: 12
title: Time Series Forecasting I
subtitle: Practice tasks on baselines, exponential smoothing and error measures by hand, reading ETS and ARIMA output, cross-validation with a delivery gap — plus a portfolio-style forecast of peak demand
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 12 on your own or in the lab. Tasks 1–4 need only paper, pencil and a calculator. Tasks 5 and 6 use Python with pandas, statsmodels (Seabold & Perktold, 2010) and scikit-learn (Pedregosa et al., 2011) on the electricity demand data from the lab (O'Hara-Wild et al., 2022). Load the data as in the session 11 lab starter:

```python
import numpy as np, pandas as pd
URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/tsibbledata/vic_elec.csv")
df = pd.read_csv(URL).drop(columns="rownames")
df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
df = df.set_index("Time")
daily = df.resample("D").agg({"Demand": "mean", "Temperature": "max", "Holiday": "max"})
daily.index = daily.index.tz_localize(None)
y = daily["Demand"].asfreq("D")                     # 1,096 days
```

The terms and notation follow the slides (Hyndman & Athanasopoulos, 2021): forecast origin and horizon *h*; error *e* = *y* − *ŷ* (actual minus forecast); MAE, RMSE, MAPE and MASE (scaled by the in-sample MAE of the seasonal naive method); simple exponential smoothing with level ℓₜ = α yₜ + (1 − α) ℓₜ₋₁; ETS(error, trend, season); seasonal ARIMA(*p*,*d*,*q*)(*P*,*D*,*Q*)ₘ.

## True or False?

Decide whether each statement is true or false and give a one-sentence reason.

1. The seasonal naive method is a special case of seasonal ARIMA.
2. A model with a MAPE of 3 % on its training data will forecast well.
3. Simple exponential smoothing with α = 1 gives the same forecasts as the naive method.
4. If two ARIMA models differ in the order of differencing *d*, the one with the lower AIC should be preferred.
5. A MASE of 0.9 means the forecasts are 10 % more accurate than those of the seasonal naive method on the same test days.
6. In time series cross-validation with `TimeSeriesSplit`, each later training set contains all earlier ones.

::: answer lines=8
:::

::: solution
1. **True.** Seasonal ARIMA(0,0,0)(0,1,0)ₘ forecasts each value by the value one season earlier (likewise ARIMA(0,1,0), the random walk, gives the naive method).
2. **False.** Training error (residuals) measures the fit to the past, not forecast accuracy; a flexible model can fit the past closely and forecast badly. Use a hold-out period or time series cross-validation and compare with a baseline.
3. **True.** With α = 1 the level equals the last observation, and SES forecasts the level for all horizons.
4. **False.** Differencing changes the data on which the likelihood is computed, so AIC values for different *d* are not comparable. Choose *d* (and *D*) with tests such as KPSS first, then *p* and *q* by AIC (Hyndman & Athanasopoulos, 2021, Section 9.6).
5. **False.** The scale of MASE is the in-sample (training) MAE of one-season-ahead seasonal naive forecasts, not the error of seasonal naive forecasts on the test days. MASE < 1 means: smaller errors than that in-sample benchmark.
6. **True.** `TimeSeriesSplit` uses an expanding window: successive training sets are supersets of the earlier ones (unless `max_train_size` sets a sliding window).

Marking: 1 point per statement with a correct reason (6 points); no point for a correct verdict without reason.
:::

## Baselines and Smoothing by Hand

A city hotel records its overnight stays (in thousands) per quarter:

| | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 2023 | 42 | 55 | 71 | 48 |
| 2024 | 44 | 58 | 75 | 50 |
| 2025 (actual, for evaluation) | 47 | 60 | | |

1. At the end of 2024, forecast Q1 and Q2 2025 with the **mean**, **naive**, **seasonal naive** (*m* = 4) and **drift** methods.
2. For each method, compute **MAE**, **RMSE** and **MAPE** over the two quarters.
3. Compute the MASE scale (in-sample MAE of the seasonal naive method on 2023–2024) and the **MASE** of each method. Which method wins?
4. A second hotel has no seasonality. Its weekly bookings are 120, 132, 126, 141, 135. Apply **simple exponential smoothing** with α = 0.4 and initial level ℓ₀ = 120: give the one-step forecast for each week, the level after each week and the forecast for week 6.

::: answer lines=14
:::

::: hint
Drift: the slope is (last value − first value) / (number of values − 1). For MASE, the seasonal naive in-sample errors are 2024 minus 2023, quarter by quarter.
:::

::: solution
1. Mean of the eight quarters: 443 / 8 = **55.375** for both quarters. Naive: **50**, 50. Seasonal naive: **44**, **58** (Q1 and Q2 of 2024). Drift: slope (50 − 42) / 7 = 1.143; **51.14** and **52.29**.
2. and 3. Errors *e* = actual − forecast; MASE scale = mean(|44 − 42|, |58 − 55|, |75 − 71|, |50 − 48|) = (2 + 3 + 4 + 2) / 4 = **2.75**.

| Method | Errors | MAE | RMSE | MAPE | MASE |
|---|---|---|---|---|---|
| Mean | −8.38, 4.63 | 6.50 | 6.77 | 12.76 % | 2.36 |
| Naive | −3, 10 | 6.50 | 7.38 | 11.52 % | 2.36 |
| Seasonal naive | 3, 2 | **2.50** | **2.55** | **4.86 %** | **0.91** |
| Drift | −4.14, 7.71 | 5.93 | 6.19 | 10.84 % | 2.16 |

Seasonal naive wins on every measure — the quarterly pattern dominates. Mean and naive have the same MAE but different RMSE: the naive method has one large error (10), which RMSE punishes more. Two forecasts from one origin are a very small test (session 12, "Why one test period is not enough").

4. SES, α = 0.4:

| Week | Forecast (= previous level) | Actual | Level after the week |
|---|---|---|---|
| 1 | 120.00 | 120 | 120.00 |
| 2 | 120.00 | 132 | 124.80 |
| 3 | 124.80 | 126 | 125.28 |
| 4 | 125.28 | 141 | 131.57 |
| 5 | 131.57 | 135 | 132.94 |

Forecast for week 6 (and all later weeks): **132.94**. The forecast is flat; SES has no trend component. One-step errors 0, 12, 1.2, 15.72, 3.43, MAE 6.47.

Marking (12 points): 1 four methods (3); 2 measures (4, deduct 1 per wrong method); 3 scale (1), MASE (1), winner with reason (1); 4 levels and forecast (2).
:::

## Which Error Measure?

A retailer forecasts the daily sales of two products for four days with a constant forecast:

| Day | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Product A, actual | 980 | 1,040 | 1,010 | 950 |
| Product A, forecast | 1,000 | 1,000 | 1,000 | 1,000 |
| Product B (spare part), actual | 2 | 0 | 1 | 3 |
| Product B, forecast | 1 | 1 | 1 | 1 |

1. Compute MAE, mean error (ME = mean of *e*) and MAPE for both products. What goes wrong for product B?
2. The category manager averages the MAE of A and B to "one accuracy figure". Why is that misleading, and what would you use instead?
3. A forecast of 100 meets an actual of 50 on one day and an actual of 150 on another. Compute both absolute percentage errors. Which kind of error does MAPE punish more — over- or under-forecasting — and how could a forecaster who is paid by MAPE exploit this?
4. What does the mean error tell you that MAE does not?

::: answer lines=10
:::

::: solution
1. **A:** errors −20, 40, 10, −50 → MAE **30**, ME **−5**, MAPE (2.04 + 3.85 + 0.99 + 5.26) / 4 = **3.04 %**. **B:** errors 1, −1, 0, 2 → MAE **1.0**, ME **0.5**, MAPE **undefined**: on day 2 the actual is 0, and division by zero gives an infinite percentage error. Measures based on percentages fail for intermittent demand (Hyndman & Koehler, 2006).
2. MAE is scale-dependent: (30 + 1) / 2 = 15.5 is driven almost entirely by product A and says nothing about B. Use a scale-free measure: **MASE** (defined with zeros, as long as the in-sample seasonal naive errors are not all zero), or report MAE per product; with weighting if products differ in importance.
3. Actual 50, forecast 100: |50 − 100| / 50 = **100 %**. Actual 150, forecast 100: 50 / 150 = **33.3 %**. The same absolute error counts more when the actual is low — i.e. when the forecast was too high (negative error *e* = *y* − *ŷ*). MAPE therefore punishes **over-forecasting** more (Hyndman & Athanasopoulos, 2021, Section 5.8: a heavier penalty on negative errors). A forecaster judged by MAPE can lower the MAPE by forecasting systematically **low** — with stock-outs as the business consequence.
4. **Bias:** ME shows whether forecasts are too high (ME < 0) or too low (ME > 0) on average; errors of both signs cancel. MAE shows the size of the errors only. A good forecast has an ME close to 0 and a small MAE.

Marking (8 points): 1 (3); 2 (2); 3 numbers (1) and interpretation (1); 4 (1).
:::

## Reading Model Output

An analyst fits two models to the **daily peak demand** (maximum of the half-hourly values per day) of the lab data, using 2012–2013 as training data, and gets:

| | ETS(M,N,M), *m* = 7 | SARIMA(2,0,2)(1,1,1)₇ |
|---|---|---|
| AIC | 11,174 | 11,036 |
| Parameters | α = 1.00, γ = 0.00 | φ₁ = 1.30, φ₂ = −0.30, θ₁ = −0.51, θ₂ = −0.37, Φ₁ = 0.08, Θ₁ = −1.00 |
| Ljung–Box test of the residuals, lag 14 | p < 0.001 | p = 0.85 |

1. Write out in words what ETS(M,N,M) and SARIMA(2,0,2)(1,1,1)₇ contain. Which difference is applied in the SARIMA model?
2. Interpret α = 1.00 and γ = 0.00. Which baseline does this ETS model resemble?
3. What does φ₁ + φ₂ ≈ 1 suggest? What does Θ₁ = −1.00 mean for the weekly pattern?
4. Interpret both Ljung–Box results. Which model has used the information in the data better?
5. Can you conclude from the AIC values that SARIMA forecasts better than ETS? Give two reasons why not.

::: answer lines=12
:::

::: solution
1. **ETS(M,N,M):** multiplicative errors, no trend, multiplicative seasonal component with period 7 (a weekday factor times the level). **SARIMA(2,0,2)(1,1,1)₇:** two autoregressive terms and two moving-average terms at lags 1–2, no ordinary difference (*d* = 0), one seasonal difference (*D* = 1: yₜ − yₜ₋₇), one seasonal AR and one seasonal MA term at lag 7.
2. α = 1: the level is updated completely with each new observation — the forecast is the last value, adjusted for the weekday. γ = 0: the weekday factors never change. So the model resembles a **seasonal naive** method applied to yesterday's seasonally adjusted value (a "naive level times weekday factor" forecast). Consequence: an extreme day (e.g. a heat wave) is carried forward for the whole horizon.
3. φ₁ + φ₂ ≈ 1: the AR part is close to a **unit root** — in the short term the level wanders almost like a random walk, so a first difference would nearly have been justified. Θ₁ = −1: the seasonal MA term cancels the seasonal difference, which corresponds to a **fixed (deterministic) weekly pattern**; Φ₁ = 0.08 adds almost nothing.
4. ETS: p < 0.001 — significant autocorrelation remains in the residuals up to lag 14; the model leaves usable information (persistence from day to day) unused. SARIMA: p = 0.85 — no evidence of remaining autocorrelation; residuals look like white noise. SARIMA has used the autocorrelation structure better (Ljung & Box, 1978).
5. No. (a) AIC measures in-sample fit with a penalty, not out-of-sample forecast accuracy at the horizon of interest; (b) ETS and ARIMA are different model classes whose likelihoods are computed differently, so their AIC values cannot be compared at all — AIC only chooses within one class (Hyndman & Athanasopoulos, 2021, Section 9.10). The decision must come from time series cross-validation against baselines. Further valid reasons: an estimate at the boundary (Θ₁ = −1) can make refits unstable; one training period may not represent all seasons.

Marking (10 points): 1 (2); 2 (2); 3 (2); 4 (2); 5 two reasons (2).
:::

## Forecasts with a Delivery Gap

The planning team receives the forecast for the **next week (Monday–Sunday)** every **Thursday evening**, when Thursday's demand is known. So Friday, Saturday and Sunday of the current week are unknown when the forecast is made.

1. Use `TimeSeriesSplit(n_splits=52, test_size=7, gap=3)` on the series up to Sunday, 28 December 2014. Check that every training set ends on a Thursday and every test window runs from Monday to Sunday.
2. Forecast with seasonal naive (*m* = 7), ETS(M,N,M) and SARIMA(2,0,2)(0,1,1)₇: each model forecasts 10 days from Thursday and you keep the last 7. Compute MAE, RMSE and MAPE.
3. Repeat without the gap (forecast made on Sunday). How much accuracy does the gap cost?
4. For seasonal naive, compute the MAE per weekday with and without the gap. Explain why Monday to Thursday are unchanged.
5. Check every fold for failed fits. If a forecast is implausible, fall back to seasonal naive and report how often that happened.

::: answer lines=12
:::

::: hint
`snaive(train, 10)[3:]` takes the last *available* value of each weekday. A simple plausibility rule: all forecasts between 0.5 × minimum and 1.5 × maximum of the training data.
:::

::: solution
Code (tested with pandas 3.0.6, statsmodels 0.15.0 and scikit-learn 1.9.1):

```python
import warnings
from sklearn.model_selection import TimeSeriesSplit
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.tsa.statespace.sarimax import SARIMAX
warnings.filterwarnings("ignore")

def snaive(tr, h): return np.array([tr.iloc[-7 + i % 7] for i in range(h)])
def ets(tr, h):
    return ETSModel(tr, error="mul", seasonal="mul", seasonal_periods=7).fit(disp=False).forecast(h).to_numpy()
def sarima(tr, h):
    return SARIMAX(tr, order=(2, 0, 2), seasonal_order=(0, 1, 1, 7)).fit(disp=False).forecast(h).to_numpy()
def guarded(f, tr, h):                         # fall back to seasonal naive if implausible
    fc = f(tr, h)
    ok = np.all(np.isfinite(fc)) and fc.min() > 0.5 * tr.min() and fc.max() < 1.5 * tr.max()
    return (fc, False) if ok else (snaive(tr, h), True)

yw = y[:"2014-12-28"]
for gap in (3, 0):
    for name, f in {"snaive": snaive, "ets": ets, "sarima": sarima}.items():
        E, Y, fallbacks = [], [], 0
        for tr, te in TimeSeriesSplit(n_splits=52, test_size=7, gap=gap).split(yw):
            fc, used = guarded(f, yw.iloc[tr], gap + 7)
            fallbacks += used
            E.append(yw.iloc[te].to_numpy() - fc[gap:]); Y.append(yw.iloc[te].to_numpy())
        E, Y = np.array(E), np.array(Y)
        print(gap, name, np.abs(E).mean().round(1), np.sqrt((E**2).mean()).round(1),
              (100 * np.abs(E) / Y).mean().round(2), fallbacks, np.abs(E).mean(axis=0).round(0))
```

1. First fold: training ends Thursday, 26 December 2013; test Monday, 30 December 2013 to Sunday, 5 January 2014. Because the series ends on a Sunday and each step is 7 days, all 52 folds have the same pattern.
2. and 3. Results (52 weeks, 364 forecasts per method):

| Method | MAE with gap | RMSE with gap | MAPE with gap | MAE without gap | MAPE without gap |
|---|---|---|---|---|---|
| Seasonal naive | 340.0 | 562.2 | 7.23 % | 298.1 | 6.29 % |
| ETS(M,N,M) | 315.2 | 531.7 | 6.74 % | 267.8 | 5.66 % |
| SARIMA(2,0,2)(0,1,1)₇ | **297.0** | **464.4** | **6.33 %** | **258.9** | **5.52 %** |

The gap costs 38–47 MW of MAE (14–18 %) for every method: the forecast is 4–10 days ahead instead of 1–7. The ranking stays the same.

4. Seasonal naive MAE per weekday (Mon … Sun), with gap: 289, 386, 317, 333, **449**, **291**, **316**; without gap: 289, 386, 317, 333, **303**, **234**, **225**. For Monday to Thursday, the same weekday of the current week is known on Thursday, so both setups use lag 7. For Friday to Sunday, the current week's values are not yet known; the method must use the week before (lag 14), which is less similar.
5. SARIMA fails in **one** of 52 folds with the gap (origin Thursday, 16 October 2014): the optimiser converged to a degenerate solution (φ₂ = 1.0, θ₂ = −1.0) whose forecasts explode to millions of MW. Without the guard, the SARIMA MAE would be about 65,600 MW — one fold destroys the average. With the fallback, SARIMA uses seasonal naive in that fold; ETS and seasonal naive never fail. Lesson: inspect fold errors (or the median) before trusting an average, and build a fallback into any automated refit — the same rule applies in production.

Marking (12 points): 1 check of origins and windows (2); 2 three methods with correct slicing (3); 3 comparison and cost of the gap (2); 4 weekday table and explanation lag 7 vs. lag 14 (3); 5 detection and handling of the failed fit (2).
:::

## Portfolio-Style Task: A Peak Demand Forecast for the Grid Operator

The grid operator plans reserve capacity two weeks ahead and cares about the **daily peak**: the largest half-hourly demand of each local day. *"How well can we forecast the daily peak 14 days ahead from history alone — and which method should we use until temperature forecasts are included?"* Write a short notebook that answers the question.

- **Data:** daily maximum of the half-hourly demand per local day; describe the series (mean, highest and lowest day).
- **Model choice on 2012–2013:** stationarity tests (KPSS on the series and on its lag-7 difference); ETS with additive and multiplicative errors and seasonality, compared by AIC; SARIMA with *d* = 0, *D* = 1 and *p*, *q* ≤ 2, *P*, *Q* ≤ 1, chosen by AIC; Ljung–Box test for both selected models.
- **Evaluation:** time series cross-validation with 26 folds of 14 days on 2014 for mean, naive, seasonal naive (lag 7 and lag 364), the selected ETS and SARIMA models, with the guard from task 5. Report MAE, RMSE, MAPE and ME, and MAE separately for the first four folds (January–February) and the rest.
- **Memo** for the grid operator: answer first, evidence, limits, next step — at most eight sentences.

::: answer lines=8
:::

::: hint
`peak = df["Demand"].resample("D").max()`, then remove the time zone and set the frequency as for `y`. Reuse the `guarded` function and the cross-validation loop from task 5 with `gap=0`, `n_splits=26`, `test_size=14`.
:::

::: solution
Code outline (tested with pandas 3.0.6, statsmodels 0.15.0, scikit-learn 1.9.1; functions from task 5):

```python
import itertools
from statsmodels.tsa.stattools import kpss
from statsmodels.stats.diagnostic import acorr_ljungbox

peak = df["Demand"].resample("D").max()
peak.index = peak.index.tz_localize(None)
peak = peak.asfreq("D")
tr = peak[:"2013-12-31"]
print(kpss(tr, nlags="auto")[1], kpss(tr.diff(7).dropna(), nlags="auto")[1])
for e in ("add", "mul"):
    print(e, ETSModel(tr, error=e, seasonal=e, seasonal_periods=7).fit(disp=False).aic)
aic = {}
for p, q, P, Q in itertools.product(range(3), range(3), range(2), range(2)):
    aic[(p, q, P, Q)] = SARIMAX(tr, order=(p, 0, q), seasonal_order=(P, 1, Q, 7)).fit(disp=False).aic
best = min(aic, key=aic.get)                           # (2, 2, 1, 1)
fit = SARIMAX(tr, order=(2, 0, 2), seasonal_order=(1, 1, 1, 7)).fit(disp=False)
print(acorr_ljungbox(fit.resid[8:], lags=[14]))
```

| Result | Value |
|---|---|
| Peak series | 1,096 days, mean 5,627 MW; highest 9,345 MW (16 January 2014, 43.2 °C); lowest 3,916 MW (26 December 2014) |
| KPSS p, series / lag-7 difference | 0.044 / > 0.10 (reported as 0.1) → *d* = 0, *D* = 1 |
| ETS AIC: (A,N,A) / (M,N,M) | 11,395 / **11,174**; α = 1.00, γ = 0.00; Ljung–Box p < 0.001 |
| SARIMA by AIC | **(2,0,2)(1,1,1)₇**, AIC 11,036 (second: (2,0,2)(0,1,1)₇, 11,037); Ljung–Box p = 0.85 |

Cross-validation, 26 folds × 14 days in 2014:

| Method | MAE | RMSE | MAPE | ME | MAE Jan–Feb | MAE Mar–Dec |
|---|---|---|---|---|---|---|
| Mean | 636 | 842 | 11.7 % | −98 | 1,150 | 542 |
| Naive | 642 | 1,027 | 11.9 % | −220 | 1,722 | 446 |
| Seasonal naive (lag 7) | 558 | 947 | 9.9 % | −22 | 1,649 | 359 |
| Seasonal naive (lag 364) | 540 | 887 | 9.6 % | −76 | 1,424 | 379 |
| ETS(M,N,M) | 524 | 912 | 9.3 % | 25 | 1,656 | 318 |
| SARIMA(2,0,2)(1,1,1)₇ | **472** | **711** | **8.2 %** | 44 | **1,135** | 352 |

The guard was needed once: SARIMA failed in the fold with origin 7 May 2014 and fell back to seasonal naive. Without the guard, the MAE would be about 1,360 MW.

Interpretation:

- The peak is harder to forecast than the daily mean (MAPE 8.2 % vs. 5.8 % in the lab): peaks react more strongly to temperature.
- SARIMA is best overall and has the smallest RMSE — it avoids the very large misses of ETS, which (with α = 1) carries heat-wave peaks forward. From March to December, ETS is slightly better (318 vs. 352 MW): the ranking depends on the season.
- In January–February, all methods miss by 1,100–1,700 MW on average; the five highest peaks of 2014 (14–17 and 28 January, 41–43 °C) were under-forecast by SARIMA by 1,500–4,200 MW. For reserve planning, exactly these days matter most.
- The lag-364 seasonal naive beats lag 7: the season matters for peaks.

Example memo: "Use the SARIMA model for two-week peak forecasts for now: its average error is about 470 MW (8 %), 15 % lower than repeating last week's peaks. It is reliable from March to December (errors about 350 MW), but in summer heat waves it misses the highest peaks by up to 4,000 MW, because history alone cannot anticipate a 43 °C day. Reserve planning for January and February should therefore not rely on this forecast alone. Next step: add the temperature forecast and the holiday calendar as regressors and provide prediction intervals (session 13). Limits: one year of evaluation, three years of history, an automated fallback was needed once."

Marking guide (30 points; training only — the portfolio brief and rubric are published separately):

- **Data** (3 points): daily maximum per local day, description with the extreme days.
- **Model choice** (8 points): KPSS before and after differencing and the resulting *d*, *D* (2); ETS comparison by AIC with parameter interpretation (2); SARIMA grid with *d* fixed (2); Ljung–Box for both models, interpreted (2).
- **Evaluation** (10 points): correct folds without leakage (2); all six methods (3); four measures (2); seasonal split of the MAE (1); failed fit detected and handled (2).
- **Interpretation and memo** (7 points): answer first (1); evidence against the baselines (2); seasonal dependence and the heat-wave problem (2); limits and next step (2).
- **Reproducibility** (2 points): runs top to bottom from the URL, versions printed, warnings handled consciously.

A strong submission notices that the best model on average is not the best in every season, and argues that the decision (reserve capacity for extreme days) needs more than a point forecast.
:::

## References {.references}

- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy. *International Journal of Forecasting, 22*(4), 679–688.
- Ljung, G. M., & Box, G. E. P. (1978). On a measure of lack of fit in time series models. *Biometrika, 65*(2), 297–303. https://doi.org/10.1093/biomet/65.2.297
- O'Hara-Wild, M., Hyndman, R., Wang, E., & Godahewa, R. (2022). *tsibbledata: Diverse datasets for 'tsibble'* (R package version 0.4.1) [Computer software]. https://CRAN.R-project.org/package=tsibbledata
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*(85), 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 92–96). https://doi.org/10.25080/Majora-92bf1922-011
