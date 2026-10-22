---
course: Data Analytics
session: 16
title: Case Study Workshop
subtitle: Practice in reviewing a case study — approach, results, dashboard, reproducibility and tool choice — on a fictional parking case, plus a portfolio-style review and storyboard
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the review of a group case study on your own or with your team, before you review your partner team's work and your own. All tasks use one **fictional** case: a student team analyses the occupancy of the 42 public car parks of a mid-sized German city. The team, the city, the data and all numbers are invented for practice; they are not taken from a real case study and say nothing about the assessment of yours. Tasks 1–5 need paper, pencil and a calculator. Task 6 is a portfolio-style review task; task 7 is an optional task for your own case study.

The terms follow the session 16 slides: the four **review checklists** (approach, results, dashboard, reproducible team notebook), the **common pitfalls** of sessions 1–15, the feedback format **two strengths, three suggestions, one question** (Hattie & Timperley, 2007) and a storyline in **action titles** (Knaflic, 2015).

### The fictional case: "Where Can I Park?"

::: callout
A team of five students uses open data from a city portal: the number of free spaces in each of the **42 car parks**, recorded **every 5 minutes** since 1 January 2023; the team's download ends on 15 June 2025 (almost 11 million rows, a CSV file of about 420 MB). The occupancy rate is 1 − free spaces ÷ capacity. The team builds a forecast of the **hourly occupancy rate** of each car park for the **next 24 hours**, and a **Streamlit dashboard** for the city's mobility department, which uses it to plan the guidance signs at the city entrances and the staff for the car parks.
:::

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. "The seasonal naive forecast is good enough, our model adds nothing" can be the main finding of a good case study.
2. If the test period gives a disappointing result, the team may tune the model again on that period and report the new test error.
3. A good dashboard shows as many KPIs as possible, so that every user finds their number.
4. A Streamlit select box that only lists a user's own car parks is enough to keep the data of the other car parks private.
5. An average error over all folds can hide one fold in which the model fails badly.
6. A forecast evaluated with the **observed** weather of the target day is an ex ante evaluation.
7. "Restart the kernel and run all" is a quick test of whether a notebook is reproducible.
8. Using Spark always makes a case study stronger, whatever the data size.
9. "The analysis should go deeper" is useful, actionable feedback.
10. An action title states the message of the slide, not only its topic.

::: answer lines=10
:::

::: solution
1. **True.** A well-argued negative result is a result: the baseline sets the bar, and saying honestly that a simple method is enough is valuable (sessions 8, 12 and 15).
2. **False.** The test period may be used only **once**; choosing or tuning on it makes the reported error optimistic. Tune on validation folds, then report the test error as it is.
3. **False.** A dashboard shows the **most important** information for one goal on one screen, with context (Few, 2013); more tiles hide the message.
4. **False.** A widget filter can be bypassed; access rules must be enforced where the data is queried (session 6).
5. **True.** Report errors per fold, season or segment, not only the mean (sessions 12–13).
6. **False.** Observed weather is not known at the forecast origin, so this is **ex post**; ex ante uses only information available at the origin, e.g. a weather forecast or climatology (session 13).
7. **True.** It is a necessary first test (Sandve et al., 2013); it does not check that data are loaded by script and versions are pinned, so it is not sufficient on its own.
8. **False.** Choose the smallest tool that meets the requirements; on one machine DuckDB was 6–40 times faster than Spark in session 15 (McSherry et al., 2015). Spark is justified by data size, platform or the explicit goal of showing it — with a measurement.
9. **False.** Feedback must say what to change and how, e.g. "show the error per car park and per week, not only the overall mean".
10. **True.** E.g. "Forecasts fail in the Christmas market weeks" instead of "Results".

Marking: 1 point per statement (verdict and, for false statements, a correct correction), 10 points.
:::

## Review the Approach

The team's notebook starts with the following approach section. Find **at least six** problems. For each, name the pitfall or checklist item and the session where it was taught, and propose a fix.

::: callout
- **Question:** We analyse parking in the city.
- **Data:** We downloaded the data on 15 June 2025 and resampled it to hours by **summing** the 5-minute occupancy rates of each hour. The licence is on the portal.
- **Features:** hour of day, weekday, month, the occupancy rate of the same car park **one hour earlier**, and the number of cars that left the car park **during the hour** being forecast.
- **Evaluation:** We split all hourly rows **randomly** into 80 % training and 20 % test data and measure the **MAPE**.
- **Baseline:** none — parking is too complex for simple methods.
- **Tool:** We use Spark, because 5-minute data from 42 car parks is big data.
:::

::: answer lines=14
:::

::: hint
Go through the approach checklist in order: question and decision, data (aggregation, completeness, licence), features (known at the prediction point for a 24-hour horizon?), evaluation design, baseline, tool choice. Also think about what the occupancy rate is at 3 a.m. and what that does to a percentage error.
:::

::: solution
Any six, 1 point each (problem with concept and a workable fix):

1. **No decision (approach checklist, session 7):** "analyse parking" is a topic. Fix: "Which car parks will be full in the next 24 hours, so that the mobility department can set the guidance signs and plan staff?" with a success metric (e.g. error in percentage points at peak hours, or hits for "full" hours).
2. **Wrong aggregation of a level (session 11):** an occupancy rate is a level, so summing twelve 5-minute values gives numbers up to 1,200 %. Fix: average per hour (or take the maximum, if the question is "full or not").
3. **Incomplete last period (sessions 2, 5, 15):** the data ends on 15 June, so June 2025 contains only half a month (and 2025 only five and a half months). Fix: state the end date and exclude or mark the partial month and year in charts and comparisons.
4. **Licence not documented (reproducibility checklist):** "on the portal" is not enough. Fix: name the licence and the attribution in the notebook header, with the download date.
5. **Lag shorter than the horizon (session 13):** for a 24-hour-ahead forecast, the occupancy one hour earlier is not known for most target hours. Fix: lags of at least 24 hours (e.g. same hour yesterday and last week), or one model per horizon.
6. **Leakage — feature from the target period (sessions 7, 13; Kaufman et al., 2012):** cars leaving during the forecast hour are only known after that hour. Fix: remove it; use only information available at the origin.
7. **Random split of time-ordered data (sessions 8, 12):** neighbouring hours of the same day land in training and test. Fix: rolling origins, e.g. weekly origins over the last months, training only on data before each origin.
8. **MAPE near zero (session 12):** occupancy at night is close to 0 %, so percentage errors explode. Fix: MAE in percentage points (and MASE to compare car parks), perhaps evaluated at the daytime hours that matter for the decision.
9. **No baseline (sessions 7, 12):** without one, the error cannot be judged. Fix: seasonal naive with lag 7 days (same hour last week) and lag 1 day.
10. **Tool choice without a measurement (session 15):** almost 11 million rows and 420 MB fit easily on a laptop. Fix: measure DuckDB and Spark on the same query, or say explicitly that Spark is used to show the framework.

Marking: 6 points (6 correct problems with a fix). A strong answer puts the leak (6) and the lag (5) first: with them, every error number is too good.
:::

## Check the Results

After the review, the team fixed its approach. It now evaluates on **8 weekly origins** between September 2024 and January 2025, choosing the model on earlier data only; each fold forecasts the next 7 days, 24 hours ahead each time. Mean absolute error (MAE) in **percentage points** of occupancy, averaged over all car parks and hours of the fold:

| Fold (week starting) | 1 (2 Sep) | 2 (23 Sep) | 3 (14 Oct) | 4 (4 Nov) | 5 (18 Nov) | 6 (2 Dec) | 7 (16 Dec) | 8 (13 Jan) |
|---|---|---|---|---|---|---|---|---|
| Seasonal naive (lag 7 days) | 6.1 | 5.8 | 6.4 | 7.0 | 5.9 | 6.2 | 9.8 | 6.3 |
| Gradient boosting (GBM) | 4.9 | 4.7 | 5.1 | 5.6 | 4.8 | 5.0 | 16.4 | 5.2 |
| Coverage of the GBM 80 % interval | 82 % | 80 % | 79 % | 84 % | 81 % | 83 % | 41 % | 80 % |

The draft results section says: *"GBM has an average MAE of 6.46 against 6.69 for seasonal naive — only 3 % better, so the model is hardly worth it. The 80 % intervals are well calibrated (average coverage 76 %)."*

1. Check the two averages and compute the **median** MAE of both methods. In how many folds does GBM beat seasonal naive?
2. Compute the relative improvement of GBM over seasonal naive in folds 1–6 and 8 together, and in fold 7 alone. What does fold 7 have in common with the weeks of the year? Suggest a cause.
3. Is "well calibrated (average coverage 76 %)" a fair summary? Compute the coverage without fold 7.
4. Propose a forecasting rule for the mobility department that uses these results, and estimate its average MAE over the 8 folds.
5. Rewrite the results section in two or three sentences with an action title.

::: answer lines=14
:::

::: hint
For 2, compute the mean MAE of both methods without fold 7 first. For 4, think of the fallback rule from session 12: what would the error be in fold 7 if you had used seasonal naive there?
:::

::: solution
1. Means: seasonal naive (6.1 + 5.8 + 6.4 + 7.0 + 5.9 + 6.2 + 9.8 + 6.3) / 8 = 53.5 / 8 = **6.69**; GBM 51.7 / 8 = **6.46** — the draft is arithmetically right (6.46 is 3.4 % below 6.69). Medians: seasonal naive (6.2 + 6.3) / 2 = **6.25**; GBM (5.0 + 5.1) / 2 = **5.05**, 19.2 % lower. GBM wins in **7 of 8** folds.
2. Without fold 7: seasonal naive 43.7 / 7 = 6.24, GBM 35.3 / 7 = 5.04 → **19.2 % better** (per fold between 17.5 % and 20.3 %). Fold 7 alone: 16.4 vs. 9.8 → GBM **67 % worse**. Fold 7 is the week of 16 December — the last week before Christmas, with Christmas shopping, the Christmas market and the start of school holidays. The model learned from "normal" weeks and has no feature for it; seasonal naive copies the previous week, which was already busy. Fix: a feature for holidays and special events (session 13), or at least a flag for these weeks.
3. **No.** An 80 % interval should cover about 80 %; the 76 % average is driven by one week with **41 %**. Without fold 7 the coverage is 569 / 7 = **81.3 %**, close to 80 % — the intervals are well calibrated in normal weeks and fail exactly in the week where the department most needs them (same pattern as January–February in session 13).
4. Example rule: **GBM in normal weeks, seasonal naive in weeks flagged as special** (Christmas weeks, large events), until event features are added. Average MAE over the 8 folds: (35.3 + 9.8) / 8 = 45.1 / 8 = **5.64**, 15.7 % below seasonal naive. Other well-argued rules (e.g. GBM plus a manual check in event weeks) are fine if the estimate follows from the table.
5. Example: "**GBM cuts the forecast error by a fifth — except before Christmas.** In 7 of 8 test weeks GBM was about 19 % more accurate than the same-hour-last-week forecast (median MAE 5.1 vs. 6.3 percentage points), and its 80 % intervals covered 79–84 %. In the week before Christmas it failed (MAE 16.4, coverage 41 %); we recommend seasonal naive for such weeks until holiday and event features are added."

Marking: 1) 2 points; 2) 2 points; 3) 2 points; 4) 1 point; 5) 1 point — 8 points.
:::

## Review the Dashboard

The team describes the Streamlit dashboard for the mobility department like this:

| Element | Description |
|---|---|
| Header | "Parking Dashboard" |
| Row 1 | Twelve KPI tiles: total capacity, spaces free now, average occupancy 2023, 2024, 2025, maximum occupancy ever, number of 5-minute records, number of car parks, MAE, MAPE, GBM training time, R² |
| Row 2 | Pie chart of the occupancy of all 42 car parks right now |
| Row 3 | Line chart: occupancy of the city (left axis, 60–75 %) and number of events in the city (right axis), January 2023 to June 2025 |
| Row 4 | Bar chart of the average occupancy per year; the y-axis starts at 55 % |
| Filter | A select box "car park"; all times shown in UTC |

1. Find **five** problems, each with the checklist item and the session behind it.
2. Sketch an improved dashboard for the decision "which guidance signs and staff do we need in the next 24 hours?" — what goes top left, what below?

::: answer lines=14
:::

::: hint
Ask for each element: does it help the decision of the next 24 hours, is the number in context, is the chart honest, and does the user know how fresh and in which time zone the data is?
:::

::: solution
1. Any five, 1 point each:
   - **No purpose in the title, too many tiles (dashboard checklist: purpose, one screen; session 6; Few, 2013):** twelve tiles, most of them irrelevant for the decision (record count, training time, R²); model metrics belong in the notebook or an "about the forecast" page.
   - **KPIs without context (sessions 5–6):** "spaces free now" without a comparison (usual value at this hour, forecast) means little.
   - **Incomplete year (sessions 2, 5):** average occupancy 2025 covers only January–June and cannot be compared with full years; mark it or compare the same months.
   - **Pie chart with 42 slices (session 5; Cleveland & McGill, 1984):** angles of 42 similar slices cannot be compared — a sorted bar chart, or a map/table of car parks with colour for "nearly full".
   - **Dual axes (session 5):** any two series can be made to "move together"; the title would invite a causal reading. Two aligned panels instead.
   - **Truncated bar axis (session 5):** bars starting at 55 % exaggerate small differences between years.
   - **UTC times (session 11):** users in the city think in local time; convert to Europe/Berlin, and show "data as of" with the time zone.
   - **No data freshness and no forecast:** the decision is about the next 24 hours, but the dashboard shows only the past.
2. Example (2 points): top left one tile per city entrance or district: "car parks expected full in the next 24 hours", with the hours; next to it the forecast for the city centre as a line for the next 24 hours with the 80 % interval and today's observed values; below, a sorted table of the 42 car parks with current and forecast peak occupancy (highlight ≥ 90 %); a line "Data as of 14:05 local time; forecasts updated hourly"; a filter by district; model quality (MAE per week, coverage) on a separate page. Access: if staff should see only their car parks, enforce it in the query.

Marking: 7 points (5 problems, 2 for the sketch with a clear top-left element linked to the decision).
:::

## Reproducible — and the Right Tool?

The team's notebook contains the following cells and notes:

```python
# Cell 1
!pip install pyspark scikit-learn streamlit
# Cell 2
df = pd.read_csv("C:/Users/lena/Downloads/parking_final_v3.csv")   # cleaned in Excel
# Cell 3
train, test = train_test_split(features, test_size=0.2)           # before the fix of task 2
# Markdown cell 14
# "GBM reaches an MAE of 4.9 percentage points." (the cell above prints 5.04)
```

The team also measured the hourly aggregation of all rows on one laptop: **DuckDB 1.8 s**, **Spark in local mode 14 s** (plus about half a minute to start the Spark session). The team's justification: *"Spark is the standard for big data, so it was the obvious choice."*

1. Name **four** reproducibility problems and a fix for each.
2. Is Spark justified for this case study? Write a better three-sentence justification for the tool choice — you may decide for either tool.

::: answer lines=12
:::

::: solution
1. 1 point each (any four):
   - **No versions pinned:** `pip install` without versions; results may change with a new release. Fix: `requirements.txt` with versions, and print versions in the notebook.
   - **Absolute local path to a renamed file:** runs only on Lena's laptop; nobody knows which download it was. Fix: download by URL in the notebook (or a script), with the download date and licence; relative paths in a shared repository.
   - **Manual cleaning in Excel:** the steps cannot be repeated or checked. Fix: clean in code, in a cell that explains each decision.
   - **No random seed:** `train_test_split` without `random_state` gives different numbers in every run (and a random split was the wrong design anyway). Fix: `random_state=…` wherever randomness enters, and a split in time.
   - **Number in the text not from a cell:** 4.9 vs. 5.04 printed. Fix: write numbers after "restart and run all", or format them from variables.
2. **Not by data size:** almost 11 million rows fit on a laptop, and DuckDB was about 8 times faster (14 s vs. 1.8 s, without the start-up time). Example justification (DuckDB): "Our data has almost 11 million rows (420 MB) and fits on one laptop; DuckDB aggregated it in 1.8 s against 14 s for Spark in local mode. We therefore use DuckDB and pandas. Spark would be the right choice if the city streamed all sensors of the region continuously into a data lake." Example justification (Spark): "We use Spark to show how the pipeline would run on the city's data platform, although DuckDB is about eight times faster on our laptop (1.8 s vs. 14 s). The same SQL runs on both engines, so the choice can be revised. On one machine, Spark brings no speed advantage for data of this size." Either is acceptable if it is based on the measurement and states the requirement that decides.

Marking: 4 points for 1, 3 points for 2 (uses the measurement 1, names the deciding requirement 1, clear decision 1) — 7 points.
:::

## Portfolio-Style Task: Write the Review

The team's (fictional) **summary cell** reads:

::: callout
**Summary.** We built a GBM forecast of hourly car park occupancy with an MAE of 6.46 percentage points, better than seasonal naive. Our dashboard shows all important KPIs. We used Spark because the data is big. The model should be used by the city.
:::

Use your results from tasks 2–5. This task is practice in the style of the feedback round, not part of a portfolio component; the official case study brief and its assessment criteria are published separately.

1. Write the feedback for the team in the format **two strengths, three suggestions, one question**. The three suggestions must be the most important ones, each with a concrete next step.
2. Rewrite the summary in the structure **answer first, evidence against the baseline, decision, limits, next step** (five to seven sentences, numbers from task 3).
3. Write a **storyboard of six to eight action titles** for the team's presentation, in order.

::: answer lines=18
:::

::: hint
The strengths must be specific (which part, which decision). For the suggestions, ask: which problem would change the conclusion if it were not fixed? For the storyboard, the titles alone should tell the story, including what did not work.
:::

::: solution
1. Example feedback (4 points: specific strengths 1, three most important suggestions with concrete steps 2, a real question 1):
   - *Strengths:* the fixed evaluation with 8 weekly rolling origins from September 2024 to January 2025 and a seasonal naive baseline is a sound design; the intervals are evaluated by coverage per fold, which is what revealed the Christmas problem.
   - *Suggestions:* (1) Report the median and per-fold errors and treat fold 7 separately — the model is about 19 % better in normal weeks, not 3 %; add a holiday/event feature or a fallback rule. (2) Rebuild the dashboard around the 24-hour decision: forecast with intervals and "expected full" car parks top left, local time, data freshness; move model metrics to a separate page. (3) Make the notebook reproducible: download by URL with licence and date, pinned versions, seeds, no manual Excel steps — and justify the tool with the DuckDB/Spark measurement.
   - *Question:* how far in advance does the department need to set the guidance signs and plan staff — is 24 hours the right horizon, and which car parks matter most?
2. Example (5 points: answer first 1, evidence with numbers against the baseline 1, decision 1, limits 1, next step 1): "**The city can use the GBM forecast in normal weeks, but not yet before Christmas.** In 7 of 8 test weeks between September 2024 and January 2025, GBM was about 19 % more accurate than the same-hour-last-week forecast (median MAE 5.1 vs. 6.3 percentage points), and its 80 % intervals covered 79–84 % of the hours. In the week before Christmas it failed (MAE 16.4, coverage 41 %). We recommend GBM with seasonal naive as a fallback in flagged event weeks, which would have given an average MAE of 5.6 instead of 6.7. Limits: one half-year of test weeks, no event calendar, and occupancy data from a single city portal, ending in mid-June 2025. Next step: add holidays and events as features and re-test on the 2025 Christmas season."
3. Example storyboard (3 points: titles state messages 1, logical order from decision to recommendation 1, includes the failure and a limit 1):
   1. "The mobility department must set guidance signs a day ahead — it needs a 24-hour occupancy forecast"
   2. "Car parks fill up in two daily waves and before Christmas"
   3. "Same hour last week is already a strong baseline: 6.2 points median error"
   4. "Gradient boosting is about 19 % more accurate in 7 of 8 test weeks"
   5. "Before Christmas the model fails — event weeks need special treatment"
   6. "The dashboard shows which car parks will be full, with uncertainty"
   7. "On one laptop DuckDB is about eight times faster than Spark"
   8. "Use GBM with a fallback in event weeks; add an event calendar next"

Marking guide (12 points; training only): feedback 4, summary 5, storyboard 3. A strong answer quotes the per-fold evidence instead of the 3 % mean, and lets the recommendation follow from it.
:::

## Optional Team Task: Review Your Own Case Study {.optional}

Apply the four checklists from the session 16 slides (approach, results, dashboard, reproducible team notebook) to **your own** case study. For each checklist item, note: met / partly / not yet, the **evidence** (cell, chart or number), and the next step with an owner. Then write your one-sentence answer and the action titles of your presentation, and mark each title for which the evidence is still missing.

::: answer lines=12
:::

::: solution
No model answer — the case studies differ. Checklist for the team member or tutor reviewing the result:

- Every checklist item has a verdict **and** evidence; "met" without a cell, chart or number does not count.
- The question names a **decision** and a user; the success metric is in the unit of the business.
- A baseline exists and is evaluated exactly like the main method; the test data are used once.
- Results show spread (per fold, segment or season) and uncertainty; at least one limitation is stated.
- If there is a dashboard: one screen, context for every KPI, honest charts, data freshness and time zone.
- The tool choice is justified with a measurement or an explicit goal.
- The notebook runs top to bottom on a fresh kernel; data loaded by script; versions and seeds fixed; licence stated.
- Next steps have owners; titles without evidence are on the to-do list.
:::

## References {.references}

- Cleveland, W. S., & McGill, R. (1984). Graphical perception: Theory, experimentation, and application to the development of graphical methods. *Journal of the American Statistical Association, 79*(387), 531–554.
- Few, S. (2013). *Information dashboard design: Displaying data for at-a-glance monitoring* (2nd ed.). Analytics Press.
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487
- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data, 6*(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Knaflic, C. N. (2015). *Storytelling with data: A data visualization guide for business professionals*. Wiley.
- McSherry, F., Isard, M., & Murray, D. G. (2015). Scalability! But at what COST? In *15th Workshop on Hot Topics in Operating Systems (HotOS XV)*. USENIX Association. https://www.usenix.org/conference/hotos15/workshop-program/presentation/mcsherry
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). Ten simple rules for reproducible computational research. *PLoS Computational Biology, 9*(10), Article e1003285. https://doi.org/10.1371/journal.pcbi.1003285
