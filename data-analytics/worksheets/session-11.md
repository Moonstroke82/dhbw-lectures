---
course: Data Analytics
session: 11
title: Temporal Data and Time Series Fundamentals
subtitle: Practice tasks on aggregating temporal data, calendars and time zones, bitemporal queries, reading ACF plots, hourly decomposition — plus a portfolio-style decomposition memo
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 11 on your own or in the lab. Tasks 1, 2 and 4 need only paper and pencil (task 2 has an optional Python check). Task 3 uses DuckDB. Tasks 5 and 6 use Python with pandas and statsmodels (Seabold & Perktold, 2010) on the electricity demand data from the lab (O'Hara-Wild et al., 2022), which you can download without login:

```python
import pandas as pd
URL = ("https://raw.githubusercontent.com/vincentarelbundock/Rdatasets/"
       "1dcc2bf5f955cc1224a3e1307256e1fe86b68dae/csv/tsibbledata/vic_elec.csv")
df = pd.read_csv(URL).drop(columns="rownames")          # 52,608 half-hours
df["Time"] = pd.to_datetime(df["Time"], utc=True).dt.tz_convert("Australia/Melbourne")
df = df.set_index("Time")
```

The terms follow the slides: events, flows, rates and levels, states with validity; valid time and transaction time; trend, seasonality, cycle and remainder; autocorrelation function (ACF); stationarity and seasonal differencing; STL and MSTL; strength of a component F = max(0, 1 − Var(R) / Var(component + R)) (Hyndman & Athanasopoulos, 2021). As on the slides, we treat `Demand` as the average load in MW of each half hour.

## Sum, Mean, Last or Count?

A bike-sharing company stores the following measures. For each one, say what **kind** of measure it is (event, flow, rate or level, state with validity) and how you would aggregate it from **hourly to daily** values. Name one aggregate that would be **wrong** and why.

| Measure | Recorded |
|---|---|
| 1. Rentals started | One row per rental with a start timestamp |
| 2. Bikes available at a station | Every hour (snapshot) |
| 3. Kilometres ridden | Per hour, summed over all rentals |
| 4. Air temperature | Every hour |
| 5. Price per minute | Price list with `valid_from` / `valid_to` |
| 6. Share of bikes out of service | Per hour, in percent of the fleet |

::: answer lines=10
:::

::: hint
Ask: does the value describe **what happened during** the hour (it can be added up), or **how things were at** a moment (it cannot)?
:::

::: solution
1. **Events.** Count per day (hours without rentals count as 0, not missing). Wrong: averaging the hourly counts and calling it "rentals per day" (that is per hour).
2. **Level (snapshot).** Daily mean, minimum (empty stations matter for service) or the value at a fixed time (e.g. 6:00, before the morning peak). Wrong: the **sum** — 24 snapshots of 10 bikes are not 240 bikes.
3. **Flow.** Sum per day. Wrong: the mean — it gives km per hour, not per day.
4. **Level.** Daily mean, maximum or minimum depending on the question (maximum for hot days, minimum for frost). Wrong: the sum.
5. **State with validity.** The price **valid on** the day (point-in-time lookup with `valid_from <= d < valid_to`); if it changes during a day, either time-weighted or per rental. Wrong: averaging all price rows of the table regardless of validity.
6. **Rate (ratio).** Recompute from the parts: bikes out of service summed over the hours ÷ fleet size summed over the hours (equivalent to a time-weighted mean). Wrong: summing percentages; a plain average is only correct if the fleet size is the same every hour (non-additive ratio, session 6).

Marking: 1 point per measure (kind and correct aggregate), 6 points; deduct nothing for a missing "wrong aggregate" if the correct one is well justified.
:::

## Calendars and Clocks in Germany

A municipal utility in Mannheim stores hourly electricity consumption of its customers in **local time without a time zone** (`2025-03-30 01:00`, `2025-03-30 03:00`, …). An analyst pivots the data into a table with one row per day and 24 columns, one per hour.

1. In 2025, daylight saving time in Germany starts on **30 March** and ends on **26 October**. How many hours do these two local days have? What happens in the pivot table on each day?
2. The analyst computes the **daily consumption** as the sum per local day and compares it with the previous Sunday. By how much, roughly, is the comparison distorted on the two days (assume a constant load)?
3. How should the data be stored and processed instead? Give two concrete rules.
4. The utility wants to compare **Easter Monday 2025** (21 April) with **Easter Monday 2024**. Why is "same date last year" the wrong comparison here, and what would you compare with instead? Which column would you add to the date dimension?

::: answer lines=10
:::

::: hint
Optional check in Python: `t = pd.date_range("2025-01-01", "2026-01-01", freq="h", tz="Europe/Berlin", inclusive="left")`, then count the hours per `t.date`.
:::

::: solution
1. **30 March: 23 hours** (02:00–03:00 does not exist); **26 October: 25 hours** (02:00–03:00 occurs twice). In the pivot, the 02:00 column is empty on 30 March, and on 26 October two rows have the same local timestamp: depending on the code, one value is lost, the two are summed into one cell, or the pivot fails with a duplicate-key error. The Python check gives 8,760 hours in 2025, two days with 23 and 25 hours, and one duplicate naive local timestamp.
2. With a constant load, the 23-hour day is about **4 % lower** (23/24 = 0.958) and the 25-hour day about **4 % higher** (25/24 = 1.042) than a normal day — a "change" caused only by the clock. A daily **mean** load (kW) is not distorted; or compare energy per hour.
3. Store timestamps in **UTC** (or with an explicit offset, e.g. `2025-10-26 02:00+02:00` and `+01:00`), convert to local time only for analysis and reporting; aggregate to **local** days with a time-zone-aware tool, and choose aggregates that are fair to 23- and 25-hour days (mean, or energy with the number of hours as a check column). Keep a check: hours per day = 23, 24 or 25, nothing else.
4. Easter moves (2024: 1 April; 2025: 21 April), so 21 April 2024 was an ordinary Sunday. Compare **Easter Monday with Easter Monday** (a holiday-to-holiday comparison), or a holiday with the average of comparable holidays/Sundays. Add a **holiday flag** and a **holiday name** (and, for Germany, the federal state, because holidays differ by state) to the date dimension — a working-day flag as well.

Marking (8 points): 1 (2); 2 (2); 3 two rules (2); 4 reason and alternative (1), date dimension columns (1).
:::

## Corrected Meter Readings: A Bitemporal Query

A utility records monthly meter readings. The reading for March is entered on **2 April 2025** as 1,250 kWh. On **3 May** the April reading (1,050 kWh) is entered. On **10 May** a technician finds that March was misread; the correct value is 1,180 kWh. Old values are **never** overwritten.

```sql
CREATE TABLE meter_reading (
  meter_id VARCHAR, month DATE, kwh INTEGER,
  recorded_from DATE, recorded_to DATE);   -- [recorded_from, recorded_to)
```

1. Which column holds the **valid time** and which the **transaction time**?
2. Write the `INSERT` statement with all rows after the three events (use `9999-12-31` for "still current").
3. Write a query that returns all readings of meter `M-17` **as known on** a given date. What do you get for 30 April, 5 May and 1 June 2025?
4. A forecasting team backtests a model: "forecast May consumption, as it would have been made on 5 May". Which March value must the backtest use, and why?
5. Write a query that lists every month whose value was **corrected**, with the first and the latest value.

::: answer lines=14
:::

::: hint
For task 5, DuckDB has `arg_min(value, ordering)` and `arg_max(value, ordering)`.
:::

::: solution
1. **Valid time:** `month` — the period the consumption belongs to in the real world. **Transaction time:** `recorded_from` / `recorded_to` — when the database held the value.
2. Tested with DuckDB 1.5.6:

```sql
INSERT INTO meter_reading VALUES
  ('M-17', DATE '2025-03-01', 1250, DATE '2025-04-02', DATE '2025-05-10'),
  ('M-17', DATE '2025-03-01', 1180, DATE '2025-05-10', DATE '9999-12-31'),
  ('M-17', DATE '2025-04-01', 1050, DATE '2025-05-03', DATE '9999-12-31');
```

The correction **closes** the old row (`recorded_to = 2025-05-10`) and inserts a new one starting on the same day — half-open intervals, no gap, no overlap.

3. Query:

```sql
SELECT month, kwh FROM meter_reading
WHERE meter_id = 'M-17'
  AND DATE '2025-05-05' >= recorded_from AND DATE '2025-05-05' < recorded_to
ORDER BY month;
```

30 April: March 1,250 (April not yet recorded). 5 May: March **1,250**, April 1,050. 1 June: March **1,180**, April 1,050.

4. **1,250 kWh** — the value known on 5 May. Using the corrected 1,180 would give the backtest information that the forecaster did not have at that time (leakage through revisions, session 7); the backtest would look better or worse than the real forecast was. For an evaluation of the *method* on clean data, both versions can be reported — but labelled.
5. Example:

```sql
SELECT meter_id, month, count(*) AS versions,
       arg_min(kwh, recorded_from) AS first_value,
       arg_max(kwh, recorded_from) AS latest_value
FROM meter_reading
GROUP BY meter_id, month
HAVING count(*) > 1;
```

Result: M-17, March 2025, 2 versions, 1,250 → 1,180.

Marking (10 points): 1 (1); 2 three correct rows with closed old interval (3); 3 query (2) and three results (1); 4 (2); 5 (1).
:::

## Which ACF Belongs to Which Series?

Match each series to one ACF description and say whether the series is **stationary**. If not, which transformation would you try first?

| Series | ACF description |
|---|---|
| A. Cars entering a city-centre car park, per hour, over eight weeks | 1. All bars inside the band ±1.96/√T, no pattern |
| B. Monthly sunscreen sales of a drugstore chain over eight years, growing every year | 2. Starts close to 1 and decreases very slowly, no peaks |
| C. Daily closing price of a share over three years | 3. Waves with peaks at lags 24, 48, 72, … and an even higher peak at 168 |
| D. Remainder of a good decomposition | 4. Slowly decreasing, with extra peaks at lags 12, 24, 36 |

::: answer lines=8
:::

::: solution
- **A – 3:** daily pattern (24 hours) and weekly pattern (168 hours = 7 × 24); the peak at 168 is higher because the same hour **and** weekday are compared. Not stationary (seasonal); first try a seasonal difference at lag 168 (or 24), or decompose with both seasonal periods (MSTL).
- **B – 4:** trend (slow decrease) plus yearly seasonality (peaks at multiples of 12). Not stationary; growing sales with growing seasonal swings suggest a **log** transform first, then a seasonal difference at lag 12 (and possibly a first difference).
- **C – 2:** a share price behaves like a random walk: today's price is close to yesterday's. Not stationary; a **first difference** (daily change or return) usually is.
- **D – 1:** white noise — what we want the remainder to look like. Stationary. If bars stick out at seasonal lags, the decomposition missed part of the seasonality.

Marking: 1 point per correct pair with a correct stationarity verdict and transformation, 4 points.
:::

## The Hourly View: One Winter Month

The slides decomposed **daily** demand. Now look **inside** the week: take the hourly series of **June 2014** (winter in Melbourne).

1. Resample the half-hourly demand to **hourly** values. Which aggregate is correct, and why? Check that June 2014 has the expected number of hours.
2. Compute the ACF up to lag 168. Report the values at lags 1, 12, 24 and 168 and explain the negative value at lag 12.
3. Decompose the month with MSTL using the periods 24 and 168. Report the strength of both seasonal components and of the trend.
4. At which hour is demand highest and lowest? How do Saturday and Sunday compare with the weekdays?
5. Find the three largest remainders. What happened on that day? (Hint: look at the `Holiday` column.)
6. Why does a classical decomposition with period 24 lose values at the start and end, and how many?

::: answer lines=12
:::

::: hint
`june = df["Demand"].resample("h").mean().loc["2014-06"].tz_localize(None).asfreq("h")` gives an hourly series without a time zone. `MSTL(june, periods=(24, 168)).fit()` returns `trend`, `seasonal` (one column per period) and `resid`.
:::

::: solution
Code (tested with pandas 3.0.6 and statsmodels 0.15.0):

```python
from statsmodels.tsa.seasonal import MSTL, seasonal_decompose
from statsmodels.tsa.stattools import acf

june = df["Demand"].resample("h").mean().loc["2014-06"].tz_localize(None).asfreq("h")
print(len(june), june.isna().sum())                      # 720 0
r = acf(june, nlags=168)
print({k: round(r[k], 2) for k in [1, 12, 24, 168]})
res = MSTL(june, periods=(24, 168)).fit()
R = res.resid
for c in res.seasonal.columns:
    print(c, round(max(0, 1 - R.var() / (res.seasonal[c] + R).var()), 2))
print(round(max(0, 1 - R.var() / (res.trend + R).var()), 2))
print(june.groupby(june.index.hour).mean().agg(["idxmin", "min", "idxmax", "max"]))
print(june.groupby(june.index.dayofweek).mean().round(0))
print(R.loc[R.abs().nlargest(3).index])
print(seasonal_decompose(june, period=24).trend.isna().sum())   # 24
```

1. **Mean** of the two half-hours: `Demand` is a load in MW (a rate), so the hourly load is the average; the sum would double it. June has no daylight saving change: **720 hours** (30 × 24), no missing values.
2. Lag 1: **0.92**; lag 12: **−0.19**; lag 24: **0.78**; lag 168: **0.70**. Twelve hours apart, a high value (evening) is paired with a low one (early morning) — half a daily cycle — so the correlation is negative.
3. Strength: daily seasonality (24) **0.97**, weekly (168) **0.92**, trend **0.63**. Within one month, the trend component contains the slow weather-driven changes from week to week.
4. Highest at **18:00** (mean 5,882 MW), lowest at **04:00** (3,485 MW). Weekdays 4,920–5,090 MW, Saturday **4,398**, Sunday **4,274** MW.
5. All three on **Monday, 9 June 2014**, 07:00–09:00, about **−600 to −700 MW**: a public holiday (the `Holiday` flag is true; in Victoria this was the Queen's Birthday holiday). The weekly component expects a Monday morning ramp-up that does not happen. A decomposition cannot know the calendar — a holiday feature is needed (session 13).
6. The trend is a centred moving average over 24 hours (2×24-MA): the first and last 12 hours have no complete window, so **24 values** are missing (Hyndman & Athanasopoulos, 2021, Section 3.4). STL and MSTL do not have this problem.

Marking (12 points): 1 (2); 2 values (1) and explanation (1); 3 (2); 4 (2); 5 identification of the holiday and interpretation (2); 6 (2).
:::

## Portfolio-Style Task: A Decomposition Memo for the Energy Planner

The energy planner of a grid operator asks: *"Before you start forecasting: what drives daily demand, how strong is each pattern, and what will a forecast need beyond the history?"* Write a short notebook on the **daily** series of the lab data (2012–2014) that answers the question.

- **Data preparation:** daily mean demand, daily maximum temperature and holiday flag per local day; check that the series is complete.
- **Decomposition:** MSTL with periods 7 and 365; strength of trend, weekly and yearly components. Compare with a robust STL with period 7 only — what changes, and why?
- **Where did the holidays and the heat go?** Mean remainder for four groups: holidays on a **fixed date** (1 January, 25 April, 25 and 26 December), holidays on a **moving date**, days with maximum temperature ≥ 35 °C, all other days. Explain the differences.
- **Stationarity:** ADF and KPSS on the series and on its lag-7 difference; interpret both tests together.
- **Memo** for the planner: answer first, evidence, consequences for forecasting, limits — at most ten sentences.

::: answer lines=8
:::

::: hint
Build the groups in this order, so that a hot holiday counts as a holiday: first all days "other", then hot days, then moving holidays, then fixed holidays. `daily.index.strftime("%m-%d").isin([...])` finds the fixed dates.
:::

::: solution
Code and results (tested with pandas 3.0.6 and statsmodels 0.15.0; `df` from the introduction):

```python
from statsmodels.tsa.seasonal import MSTL, STL
from statsmodels.tsa.stattools import adfuller, kpss

daily = df.resample("D").agg({"Demand": "mean", "Temperature": "max", "Holiday": "max"})
daily.index = daily.index.tz_localize(None)
daily = daily.asfreq("D")                                  # 1,096 days, no gaps

def strength(comp, resid):
    return round(max(0, 1 - resid.var() / (comp + resid).var()), 2)

res = MSTL(daily["Demand"], periods=(7, 365)).fit()
R = res.resid
st = STL(daily["Demand"], period=7, robust=True).fit()
hol = daily["Holiday"].astype(bool)
fixed = daily.index.strftime("%m-%d").isin(["01-01", "04-25", "12-25", "12-26"])
groups = pd.Series("other day", index=daily.index)
groups[daily["Temperature"] >= 35] = "max. temp. >= 35 °C"
groups[hol & ~fixed] = "holiday, moving date"
groups[hol & fixed] = "holiday, fixed date"
print(R.groupby(groups).agg(["count", "mean"]))
```

| Result | Value |
|---|---|
| MSTL strength: trend / weekly / yearly | 0.09 / 0.77 / 0.80 |
| Robust STL, period 7: trend / weekly | 0.53 / 0.55 |
| Mean remainder: fixed-date holidays (12 days) | +11 MW |
| Mean remainder: moving-date holidays (19 days) | −215 MW |
| Mean remainder: max. temperature ≥ 35 °C (28 days) | +310 MW |
| Mean remainder: other days (1,037 days) | −6 MW |
| Remainder variance / variance of the series | 0.116 |
| ADF p / KPSS p, original series | 0.010 / 0.015 |
| ADF p / KPSS p, lag-7 difference | < 0.001 / > 0.10 (reported as 0.1) |

Interpretation:

- **STL with period 7 only** puts the yearly pattern into the "trend" (its strength rises from 0.09 to 0.53) and has a weaker weekly component (0.55): the trend window must follow winter and summer, so "trend" no longer means long-term change. With two seasonal periods, MSTL separates them.
- **Fixed-date holidays** have a remainder near zero because they fall on the same calendar day every year: the **yearly component** has learned them (its values on 25 and 26 December are between about −960 and −1,280 MW). This works only because the yearly component is estimated from three years, and it would also "learn" a heat wave (January 2014). **Moving holidays** (Easter, the Australia Day and Queen's Birthday Mondays, Melbourne Cup day) cannot be learned that way and stay in the remainder (−215 MW on average, up to −1,331 MW on 28 January 2013); some of them, close to the same date each year, are partly absorbed.
- **Hot days** have a positive remainder (+310 MW): air conditioning on heat-wave days is not a calendar pattern.
- **Stationarity:** ADF rejects a unit root, KPSS rejects stationarity — the series does not drift like a random walk, but its level moves with the seasons; after the lag-7 difference both tests agree on stationarity (Hyndman & Athanasopoulos, 2021, Section 9.1).

Example memo: "Daily demand is driven by the working week and the seasons; there is almost no long-term trend. The weekly pattern (strength 0.77) and the yearly pattern (0.80) explain most of the variation; about 12 % of the variance remains. That remainder is not random: moving public holidays lower demand by about 215 MW on average, and days of 35 °C or more raise it by about 310 MW. A forecast therefore needs the holiday calendar and a temperature forecast — history alone will repeat past heat waves on the wrong days. After removing the weekly pattern, the series is stationary, so standard models apply (session 12). Limits: three years only, one state, and the yearly component mixes season with the weather of 2012–2014."

Marking guide (30 points; training only — the portfolio brief and rubric are published separately):

- **Data preparation** (4 points): local days, mean (not sum) for the load, maximum temperature, holiday flag, completeness check (1,096 days, no gaps).
- **Decomposition** (8 points): MSTL with correct periods and strengths (3); robust STL with period 7 and strengths (2); explanation of the difference — yearly pattern in the trend (3).
- **Holiday and heat analysis** (8 points): groups built correctly (3); correct means (2); explanation why fixed-date holidays vanish into the yearly component and moving ones do not (3).
- **Stationarity** (4 points): both tests on both series (2); joint interpretation with the opposite null hypotheses (2).
- **Memo** (4 points): answer first, numbers, consequence for forecasting (external regressors), limits.
- **Reproducibility** (2 points): runs top to bottom from the URL, versions printed, no manual steps.

A strong submission notices that the yearly component of a three-year series contains weather and fixed-date holidays, and argues that both should be modelled explicitly instead.
:::

## References {.references}

- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- O'Hara-Wild, M., Hyndman, R., Wang, E., & Godahewa, R. (2022). *tsibbledata: Diverse datasets for 'tsibble'* (R package version 0.4.1) [Computer software]. https://CRAN.R-project.org/package=tsibbledata
- Seabold, S., & Perktold, J. (2010). Statsmodels: Econometric and statistical modeling with Python. In S. van der Walt & J. Millman (Eds.), *Proceedings of the 9th Python in Science Conference* (pp. 92–96). https://doi.org/10.25080/Majora-92bf1922-011
