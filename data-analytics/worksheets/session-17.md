---
course: Data Analytics
session: 17
title: Portfolio Presentations and Wrap-Up
subtitle: Course-wide revision and reflection — from the warehouse to forecasts and Spark, a case study review and a look ahead to the semester-6 project
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet helps you revise the whole course (sessions 2–15) and reflect on your own work. It contains no new content: every task uses terms and methods from the session slides — grain and KPI definitions, window functions, leakage and baselines, experiments and trust checks, time series cross-validation, MAE, MAPE and the Winkler score, global models and reconciliation, partitions and shuffles in Spark. It is practice material only: it is not part of the portfolio assessment, and the official briefs and rubrics are published separately.

Tasks 1–4 need only paper, pencil and a calculator. Task 5 is a portfolio-style review of a case study presentation, in the format of the peer feedback sheet of session 17. Task 6 is a reflection on your own portfolio and your semester-6 project. The companies, people and numbers in all tasks are invented for practice.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. A fact table that holds order-level shipping fees and line-level revenue in the same rows saves joins and is good dimensional design.
2. A window function such as `sum(revenue) OVER (PARTITION BY region)` returns one row per region, like `GROUP BY`.
3. Half-hourly electricity demand in MW is a level, so daily values are averaged, not summed.
4. A model with a higher AUC always gives a higher profit at the capacity of a retention campaign.
5. Randomisation balances known **and** unknown confounders between the groups of an experiment — on average.
6. Comparing forecasting methods over many forecast origins (time series cross-validation) is more reliable than one train/test split.
7. MAPE is a good error measure for a spare part that sells zero units on most days.
8. For a 7-day-ahead forecast with one model for all horizons, a lag-1 feature ("yesterday's value") may be used.
9. After reconciliation, the forecasts of the regions add up to the forecast of the national total.
10. If a dataset fits on one machine, Spark is faster than DuckDB because it runs in parallel.

::: answer lines=10
:::

::: solution
1. **False.** It mixes two grains: summing the fee over lines counts it once per line. Keep one grain per fact table (an order-level fact table for fees) or allocate the fee to the lines (session 3; Kimball & Ross, 2013).
2. **False.** A window function keeps every input row and adds the result as a column; `GROUP BY` collapses the rows (session 4).
3. **True.** Levels and rates are averaged, flows are summed (session 11). Summing 48 half-hourly MW values gives no meaningful unit; energy would be MW × hours.
4. **False.** AUC measures ranking over all thresholds; the profit depends on the few customers above the capacity cut-off and on the cost matrix. Compare models by lift and profit at the capacity (session 7).
5. **True.** That is why a randomised experiment can estimate a causal effect where historical correlations cannot (session 9; Kohavi et al., 2020) — in a single small experiment the groups can still differ by chance, which the confidence interval reflects.
6. **True.** One split can be lucky or unlucky; many origins average over seasons and show the variation between folds (session 12; Hyndman & Athanasopoulos, 2021).
7. **False.** MAPE divides by the actual value and is undefined or extreme at zero. Use MAE or MASE, and methods and measures for intermittent demand (sessions 12, 14).
8. **False.** At the origin, yesterday's value is unknown for horizons 2–7. Use lags of at least 7 days, or one model per horizon (session 13).
9. **True.** Reconciliation makes forecasts **coherent** with the hierarchy (session 14).
10. **False.** On one machine DuckDB was faster in our session 15 tests (and usually is); Spark pays for coordination and shuffles. It is needed when data, workload or platform exceed one machine — measure (session 15; Zaharia et al., 2016).

Marking: 1 point per statement (verdict and, for false statements, a correct correction), 10 points.
:::

## Diagnose the Symptom

Each situation shows a **symptom** from a real-world analytics project. Name the **concept** from the course that explains it, the **session**, and **one fix**.

1. The marketing dashboard shows 48,200 "active users" in September, the finance report 41,700.
2. A model that predicts which hotel bookings will be cancelled reaches a top-decile lift of 9.4. The most important feature is `deposit_refunded`.
3. A demand forecast had an excellent MAE in cross-validation with shuffled folds — and performs much worse in its first month in production.
4. The autocorrelation function of the residuals of a daily forecast model shows clear peaks at lags 7, 14 and 21.
5. An A/B test of a new checkout page assigned 101,800 users to variant A and 98,200 to variant B, although the split was planned as 50/50.
6. A Spark job that ranks 20 million customers by revenue is slow; `explain()` shows an `Exchange SinglePartition` before the window.
7. The forecasts of the 35 stores of a region add up to 12 % more than the separate forecast of the region.
8. The 80 % prediction intervals of a heating-oil demand forecast cover 81 % of all test days — but only 58 % in December and January.

::: answer lines=12
:::

::: hint
Each symptom belongs to one session: 6 (semantic layer), 7 (leakage), 12 (evaluation), 11–12 (residual checks), 9 (trust checks), 15 (shuffles), 14 (hierarchies), 13 (intervals).
:::

::: solution
1. **Competing KPI definitions** (sessions 5–6): "active" means something different in the two reports (e.g. logged in vs. paid). Fix: define the metric once — formula, filters, time window, owner — in the semantic layer and use it in both reports.
2. **Leakage** (session 7; Kaufman et al., 2012): a refund is recorded only after a cancellation, so the feature is not known at the prediction point. Fix: rebuild all features with data before the cut-off only; distrust results that are "too good".
3. **Shuffled folds on time-ordered data** (session 12): training rows from after the test day leak the future. Fix: time series cross-validation with forecasts only from earlier origins.
4. **Unmodelled weekly seasonality** (sessions 11–12): the residuals are not white noise, so the model misses a pattern that repeats every 7 days. Fix: add weekly seasonality (seasonal terms, day-of-week features or a seasonal ARIMA part); check the ACF and a Ljung–Box test again.
5. **Sample ratio mismatch** (session 9): with 200,000 users a split of 50.9 % / 49.1 % is far too large for chance (χ² ≈ 64.8, p far below 0.001). Fix: do not analyse the result; find the cause in assignment, logging or filtering, fix it and rerun.
6. **A global window forces a shuffle into one partition** (session 15): a window without `PARTITION BY` moves all rows to one task. Fix: rank within partitions (e.g. by country), or compute top-N per partition first and rank only those rows globally; check the plan again with `explain()`.
7. **Incoherent forecasts of a hierarchy** (session 14): independently forecast levels do not add up. Fix: reconcile (bottom-up, or optimal reconciliation such as OLS or MinT), and decide which level drives the decision.
8. **Interval calibration differs by season** (session 13): the errors in winter are larger than the average errors used to build the interval. Fix: intervals per season (errors of the same months), a model with temperature forecasts, or wider quantiles in winter — and always report coverage per season.

Marking: 1 point per situation (concept with a fitting fix), 8 points.
:::

## Check a Forecast

A parcel depot forecasts the number of parcels per day (in thousands) for the next two weeks. The model was fitted on data up to Sunday of week 0; there is one forecast origin, and horizons 1–14 are evaluated. The **seasonal naive** forecast repeats the last observed week.

| Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| Week 0 (observed) | 52 | 48 | 47 | 49 | 58 | 41 | 12 |
| Week 1 actual | 55 | 50 | 46 | 51 | 61 | 44 | 13 |
| Week 1 forecast | 53 | 49 | 48 | 50 | 59 | 42 | 12 |
| Week 1 80 % interval | 49–57 | 45–53 | 44–52 | 46–54 | 54–64 | 38–46 | 10–14 |
| Week 2 actual | 54 | 49 | 48 | 50 | 66 | 43 | 12 |
| Week 2 forecast | 53 | 49 | 48 | 50 | 59 | 42 | 12 |
| Week 2 80 % interval | 48–58 | 44–54 | 43–53 | 45–55 | 53–65 | 37–47 | 10–14 |

1. Compute the **MAE** of the model and of the seasonal naive forecast over the 14 days, and the ratio of the two MAEs. Is the model worth using?
2. Compute the **MAPE** of the model. Which day has the largest percentage error, although its absolute error is small — and why does this matter?
3. Compute the **coverage** of the 80 % intervals, the mean **width** and the **Winkler score** (α = 0.2) for Friday of week 2 and on average.
4. The Friday of week 2 was the day before a public holiday. What would you change in the model, and is this information available **ex ante**?
5. A colleague says: "13 of 14 days covered — our intervals are too wide." Do you agree?

::: answer lines=14
:::

::: hint
Seasonal naive for week 1 **and** week 2 is the week-0 row. Winkler score: the width if the actual value is inside the interval; otherwise the width plus 2/α = 10 times the distance to the nearest bound.
:::

::: solution
1. Model errors (actual − forecast): week 1: 2, 1, −2, 1, 2, 2, 1; week 2: 1, 0, 0, 0, 7, 1, 0. **MAE model = 20 / 14 = 1.43** thousand parcels. Seasonal naive errors: week 1: 3, 2, −1, 2, 3, 3, 1; week 2: 2, 1, 1, 1, 8, 2, 0. **MAE seasonal naive = 30 / 14 = 2.14**. Ratio **0.67**: the model's errors are a third smaller than those of the baseline — worth using, if this holds over **many origins** (one origin is a single, possibly lucky, test; session 12).
2. Absolute percentage errors of the model add up to 42.3 %, so **MAPE = 3.0 %** (seasonal naive: 4.4 %). The largest percentage error is on **Sunday of week 1**: 1 / 13 = **7.7 %**, although the error is only 1,000 parcels; the 7,000-parcel miss on Friday of week 2 counts only 10.6 %. MAPE weights low-volume days heavily — misleading if the decision (staff, trucks) depends on absolute volumes; then MAE is the better yardstick (session 12).
3. Covered: 13 of 14 days = **92.9 %**; the only miss is Friday of week 2 (66 > 65). Mean width = 120 / 14 = **8.6**. Winkler on that Friday: width 12 + 10 × (66 − 65) = **22**; on all other days the width (4, 8 or 10). Mean Winkler score = 130 / 14 = **9.3**.
4. Add a **holiday-eve** (or "working day before a holiday") feature, or an event adjustment, so that the model learns the extra volume. Public holidays are known in advance, so the feature is **ex ante** and can be used without forecasting it (session 13) — unlike weather.
5. Not from these numbers. With only 14 test days, coverage is very noisy: the standard error is √(0.8 × 0.2 / 14) ≈ 0.11, so anything between about 70 % and 90 % — and even 13 of 14 — is compatible with well-calibrated 80 % intervals; the days are also correlated (one origin). Judge coverage over many origins and per season, together with the Winkler score (session 13). Note also that the intervals were too narrow exactly where it mattered (the holiday eve).

Marking (10 points): MAEs and ratio with interpretation 2; MAPE and the Sunday argument 2; coverage, width and Winkler score 3; holiday feature and ex ante 1; sampling argument 2.
:::

## One Case, Four Parts

A chain of **120 bakery branches** has sales per branch, product and day since January 2019 from its till system (about 40 products), and a daily waste record per branch and product. The board asks two questions:

- **Production:** how many of each product should each branch bake each morning?
- **Waste:** does a **30 % discount in the last opening hour** reduce waste without losing revenue?

Plan the analysis. For each part, give a short answer.

1. **Part A:** define the grain of the fact table(s), two KPIs with their formula, and one rule for access to the dashboard.
2. **Part C:** what exactly do you forecast — granularity, horizon, origin, baseline, external regressors, evaluation? Name one problem with using **sales** as the target.
3. **Part C at scale:** how do you handle 120 × 40 series, including products that sell only a few units per week?
4. **Part B:** design the test of the evening discount: unit of randomisation, primary metric, guardrail, a threat to the design.
5. **Part D:** estimate the number of rows of the sales fact table. DuckDB or Spark?
6. What is the **simplest useful first result** you would deliver to the board, and why?

::: answer lines=16
:::

::: hint
Bakeries often sell out in the afternoon. What does the till record on such a day — the demand, or something else? For the test, think about what would happen if regular customers saw a discount in one branch but not in the next.
:::

::: solution
1. **Grain:** one row per branch, product and day (sales quantity, revenue, waste quantity) — a periodic snapshot; if available, a transaction fact table at receipt-line level for time-of-day analyses. Dimensions: date (with holidays and school holidays), branch (region, location type), product (category). **KPIs**, for example: waste rate = waste quantity ÷ baked quantity (per branch, product group and week); sell-out rate = share of branch-product-days on which the product was sold out before closing; revenue per branch-day. **Access:** branch managers see only their branch, regional managers their region — enforced where the data is queried (session 6).
2. **Target:** daily quantity per branch and product; **horizon** 1 day (bake plan for tomorrow, origin the afternoon before) — possibly 2–3 days for orders of ingredients; **baseline:** seasonal naive (same weekday last week); **regressors:** weekday, public and school holidays, weather forecast, local events, promotions; **evaluation:** time series cross-validation over many origins with MAE (or MASE across products); intervals checked by coverage (sessions 12–13). **Problem:** on sold-out days, sales are **censored** — they show what was baked, not what customers wanted. A model trained on sales learns to under-produce. Mark or exclude sold-out days, or use the time of sell-out to estimate the lost demand.
3. 4,800 series: a **global model** (e.g. gradient boosting with lags ≥ horizon, calendar, branch and product features) instead of 4,800 hand-tuned local models; a **hierarchy** (product → category → branch → region) with reconciliation if plans are made at several levels; **intermittent** products with rate methods such as Croston or SBA and an error measure that does not reward forecasting zero; automatic guards and monitoring (session 14).
4. **Unit:** the **branch** (or branch-week), not the customer — the discount is visible to everyone in the shop, and regular customers would shift their purchases. Randomise e.g. 60 branches to discount and 60 to control, stratified by region and size. **Primary metric:** waste rate; **guardrail:** revenue per branch-day (and the share of full-price sales in the last hour); run for several full weeks and analyse once. **Threats:** customers learning to wait for the discount (effect grows over time — run long enough), spill-over between nearby branches, and too few units (120 branches — check the sample size; session 9; Kohavi et al., 2020).
5. About 120 × 40 × 365 × 7 ≈ **12.3 million rows** for seven years — a few hundred MB as Parquet. **DuckDB** (or pandas) on one machine is enough; Spark only if the till data already lives on a cluster platform or must be processed continuously from many branches (session 15).
6. A **dashboard of waste rate and sell-out rate** per branch and product group, with clear definitions — it shows where the problem is, needs no model, and gives the baseline every later forecast must beat. A good second step: compare the current bake plan with a seasonal naive plan on past data. The model and the experiment come after.

Marking (12 points): 1 grain, KPIs and access 2; 2 forecast design 2, censoring 1; 3 global model, hierarchy, intermittent 2; 4 unit and metric 1, guardrail and threat 1; 5 row estimate and tool 1; 6 simplest result with reason 2. Accept other well-argued answers.
:::

## Portfolio-Style Task: Review a Case Study Presentation

A fictional team presents its case study on **public hourly air-quality data** (nitrogen dioxide, NO₂, from 400 measuring stations, 2015–2024). These are their slide titles and the key content:

| Slide | Title | Content |
|---|---|---|
| 1 | Agenda | Data, results, model, forecast, dashboard, conclusion |
| 2 | Data | 12 GB of CSV files; "loaded with Spark, because this is big data" — no timing, no comparison |
| 3 | Results | One chart with two y-axes: NO₂ (left, from 20 to 45 µg/m³) and traffic volume (right) — "traffic causes pollution" |
| 4 | Our model | Gradient boosting predicts NO₂ **24 hours ahead**; features include "NO₂ one hour earlier"; random 80/20 split of all hourly rows; R² = 0.97 |
| 5 | Lockdown effect | NO₂ in April 2020 was 25 % lower than in April 2019, "so the lockdown reduced pollution by 25 %" |
| 6 | Forecast | Line chart of next week's forecast for one station, no baseline, no interval |
| 7 | Dashboard | National NO₂ = average of the 16 federal-state averages |
| 8 | Conclusion | "Our model is very accurate and should be used by all cities." |

1. Find at least **six** problems. For each, name the concept from the course and the consequence.
2. Rewrite the titles of slides 3, 4 and 8 as **action titles** that the team could defend with honest evidence (use placeholders such as "[MAE]" where a number is missing).
3. Fill in the **peer feedback sheet** of session 17 for this talk: for three criteria of your choice, one "works well" and one "next step" each — plus one question.

::: answer lines=18
:::

::: hint
Go through the six points of "What a Strong Case Study Presentation Shows": big idea, data, method and baseline, evidence and uncertainty, tool choice, recommendation. Then look at the charts with the eyes of session 5.
:::

::: solution
1. Problems (any six, 1 point each, up to 6):
   - **No big idea** (session 5; Knaflic, 2015): the talk opens with an agenda; neither the question nor the decision it serves is named.
   - **Tool choice without a measurement** (session 15): 12 GB fits on one machine; "big data" is not an argument. Measure DuckDB vs. Spark, or justify Spark by the platform or a scaling goal.
   - **Dual axis and truncated axis** (session 5): the scaling of two y-axes is arbitrary, and the NO₂ axis starts at 20; the chart can show almost any relation.
   - **Correlation presented as causation** (session 9): traffic and NO₂ share daily and weekly patterns and weather effects; the chart cannot show that traffic "causes" the level.
   - **Leakage** (sessions 7, 13): "NO₂ one hour earlier" is not known 24 hours before the target hour; lags must be at least the horizon.
   - **Random split of time-ordered data** (sessions 8, 12): neighbouring hours are almost identical, so the test rows are nearly copies of training rows. With the leak, this explains R² = 0.97. Use time series cross-validation over later periods.
   - **No baseline** (sessions 7, 12): compare with seasonal naive (same hour yesterday or last week) and report MAE, not only R².
   - **Causal claim from a before–after comparison** (session 9): April 2020 differs from April 2019 in weather, the long-term downward trend and the calendar; use a comparison (e.g. weather-adjusted model of the expected level, or difference-in-differences with periods or stations less affected) and report an interval.
   - **Forecast without baseline and interval** (session 13): a single line hides the uncertainty; show an 80 % interval and its coverage.
   - **Average of averages** (session 6): states with few stations count as much as states with many; define the national KPI once (e.g. mean over all stations, or population-weighted) in the semantic layer.
   - **Recommendation without limits** (sessions 8, 10): "very accurate" on a leaky, randomly split test says nothing; no decision, no user, no limits, no next step.
2. Example action titles (1 point each, up to 3): Slide 3: "NO₂ and traffic rise and fall together during the day — but weather and season move both, so the chart does not show cause." Slide 4: "Without the leaky one-hour lag, the model forecasts NO₂ 24 h ahead with an MAE of [MAE] — [x] % better than the same hour of the previous day." Slide 8: "A day-ahead forecast beats the simple baseline by [x] % at [n] of 400 stations; cities could use it for warnings once intervals are calibrated — next step: test it over a full winter." (Any title that states a finding the evidence can support, with numbers or placeholders, is acceptable.)
3. Example (5 points: three criteria with specific "works well" and actionable "next step" 4, a real question 1; Hattie & Timperley, 2007):
   - *Data and its limits* — works well: a large, public, well-documented dataset with ten years of hourly data. Next step: state station changes, missing hours and the licence; say why 12 GB needs (or does not need) Spark, with a timing.
   - *Method and baseline* — works well: gradient boosting with time features is a sensible choice for many series. Next step: remove the one-hour lag (lags ≥ 24 h), use time series cross-validation, and compare with seasonal naive by MAE.
   - *Story* — works well: the dashboard is a good idea for the audience of city administrations. Next step: replace the dual-axis chart by two aligned panels, start with the big idea, and give every slide an action title.
   - *Question:* which decision should the forecast support — for example a warning one day ahead — and how good must it be for that?

Marking guide (14 points; training only — the official rubric of the case study is published separately): problems 6, action titles 3, feedback sheet 5. A strong answer puts the leak and the random split first: as long as they are in the evaluation, R² = 0.97 and the conclusion are meaningless.
:::

## Reflection: Your Portfolio and Your Project

This task has no single right answer. Write it for yourself — or discuss it with your project team.

1. Choose **one method** you used in a portfolio notebook (e.g. a window-function analysis, a churn model, a forecast). Write a suitability assessment in five sentences: **fit, evidence, data, use, verdict** (session 10).
2. Which **two** of the five questions from the course — decision, definitions, time, baseline, uncertainty — will be hardest to answer in your semester-6 project? For each, name **one concrete action** for the first sprint.
3. Which piece of feedback from the case study presentations will you **act on** in the project, and how?

::: answer lines=14
:::

::: solution
No model answer — the answers are personal and the projects differ. Checklist for a self-check or a tutor:

- **Suitability assessment:** each of the five sentences does its job — the business question the method answers (fit); the improvement over a named baseline on unseen data, with uncertainty (evidence); at least one limit of the data that affects the result (data); whether the result can be produced and acted on in practice (use); a clear verdict (use it, use a simpler alternative, collect more evidence). "A simple rule is enough" is a valid verdict if it is argued.
- **Project questions:** the actions are concrete and fit into a sprint, e.g. "write a KPI definition sheet for the target metric and agree it with the product owner" (definitions); "find out at what time the data of each source is available, so that features are point-in-time correct" (time); "build a seasonal naive or rule-based baseline in the first sprint" (baseline); "agree how uncertain a result may be for the decision" (uncertainty). Vague actions ("do more analysis") do not count.
- **Feedback:** names a specific comment and a specific change (e.g. "start the mid-term presentation with the big idea"), in the spirit of "where to next" (Hattie & Timperley, 2007).
- **Confidentiality:** no partner company names, data or details are written down outside the team's private workspace.
:::

## References {.references}

- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data, 6*(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Knaflic, C. N. (2015). *Storytelling with data: A data visualization guide for business professionals*. Wiley.
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy online controlled experiments: A practical guide to A/B testing*. Cambridge University Press. https://doi.org/10.1017/9781108653985
- Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., Meng, X., Rosen, J., Venkataraman, S., Franklin, M. J., Ghodsi, A., Gonzalez, J., Shenker, S., & Stoica, I. (2016). Apache Spark: A unified engine for big data processing. *Communications of the ACM, 59*(11), 56–65. https://doi.org/10.1145/2934664
