---
course: Data Analytics
session: 17
title: Portfolio Presentations and Wrap-Up
subtitle: Group case study presentations · peer feedback · the course in review · outlook to the semester-6 project
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Portfolio Presentations and Wrap-Up {.title}

::: notes
Final session, 2 h block, no new content. Time plan (planned for four teams): welcome, recap and running order 5 min · presentation and feedback criteria 5 min · presentations, block 1 (teams 1–2) 31 min · break 10 min · presentations, block 2 (teams 3–4) 31 min · course wrap-up incl. exercise 15 min · outlook to semester 6 12 min · course feedback 6 min · ~5 min buffer.
Per team: about 10 min talk incl. demo, 4 min questions, 1–2 min for the audience to finish the feedback sheet. With five teams, add a third block of 15 min: move the wrap-up exercise to worksheet 17 (task 4 covers the same idea) and shorten the outlook to the two partner slides. Never cut the questions after a talk — they are part of the assessment and the most valuable part for the audience.
Before class: fill in the running order (offline copy or whiteboard), test the projector with each team's laptop or collect the slides on one machine, print or share the feedback sheet, and have the official rubric of the case study at hand (published separately on the course platform, not in this deck).
:::

---

# Today's Agenda

1. Recap: from the workshop to today
2. Group case study presentations
3. Peer feedback
4. The course in review: four parts, one thread
5. Outlook: the semester-6 project
6. Your feedback on the course

::: notes
Time and format guide (not shown to students):
0:00 Welcome, recap, running order (plenary) · 0:05 Criteria and feedback sheet (input) · 0:10 Presentations block 1 · 0:41 Break · 0:51 Presentations block 2 · 1:22 Course in review (input + exercise in pairs) · 1:37 Semester-6 outlook (input + questions) · 1:49 Course feedback · 1:55 Close · ~5 min buffer.
If a partner company contact joins for the outlook, move the outlook directly after the break and the second block after it.
:::

---

# Recap: From the Workshop to Today

- In the **case study workshop** your team reviewed approach, results and dashboard, got feedback from another team and storyboarded today's talk in action titles
- Open points from the consultations should now be **closed — or named as limits**
- Today: each team presents its **end-to-end case**; everyone else gives structured feedback

::: callout
**Your preparation:** a notebook that runs top to bottom on a fresh kernel, the workshop feedback worked in, one rehearsal with a timer — and a fallback for the demo.
:::

::: notes
Ask one person per team: "What was the most important change after the workshop feedback?" — one sentence each, no discussion. This warms up the room and shows that feedback was used. Remind teams that the notebook and the presentation are assessed together (group case study, 40 % of the portfolio); the hand-in date for the notebook is the one in the portfolio brief.
:::

---

# Case Study Presentations {.section}

End-to-end analytics on public data

---

# Running Order

| Slot | Team | Case study | Feedback first from |
|---|---|---|---|
| 1 | Team 1 | [title of the case study] | Team 2 |
| 2 | Team 2 | [title of the case study] | Team 3 |
| 3 | Team 3 | [title of the case study] | Team 4 |
| 4 | Team 4 | [title of the case study] | Team 1 |
| (5) | (Team 5) | [title of the case study] | (Team 1) |

- Each talk is followed by **questions** from the audience and the lecturer
- The team named in the last column opens the questions and hands in its feedback sheet first

::: notes
Fill in team names and titles in the offline copy or on the whiteboard; do not write student names into this file (the Markdown is public). Order: draw lots at the start, or use the order agreed in the workshop. Keep strict time per talk with a visible signal (one minute left), but do not cut questions. The rotating "feedback first" team makes sure every talk gets at least one prepared question.
:::

---

# What a Strong Case Study Presentation Shows

1. **Big idea:** the question, the decision it serves and the answer — in one sentence, at the start
2. **Data:** source, licence, size, time span — and the limits that matter
3. **Method:** why this method fits the question, compared with a **baseline**
4. **Evidence:** honest evaluation on unseen data, with **uncertainty**
5. **Scale or portal:** why this tool — Spark or DuckDB with a measurement, or a dashboard demo
6. **Recommendation:** what to do, how sure we are, what comes next

::: callout
**Action titles:** if the audience reads only your slide titles, do they get the story?
:::

::: source
Own compilation based on Knaflic (2015), Chapman et al. (2000) and Provost and Fawcett (2013).
:::

::: notes
Guidance, not the official rubric (published separately). The six points mirror the course: big idea and action titles (session 5, Knaflic's lessons — the standard announced there for today), framing and baseline (session 7), honest evaluation (sessions 8, 12), uncertainty (sessions 9, 13), tool choice with a measurement (session 15: "choose the smallest tool that meets the requirements"), and the suitability assessment that ends every notebook (session 10). The case study must include a big data framework or a dashboard (portfolio brief); point 5 asks teams to justify which one.
:::

---

# Peer Feedback Sheet {.exercise}

For each talk, note one point per row — specific, with a slide or a number.

| Criterion | Works well | Next step |
|---|---|---|
| Big idea and decision clear from the start | | |
| Data and its limits | | |
| Method fits the question; baseline | | |
| Evaluation and uncertainty | | |
| Tool choice or dashboard justified | | |
| Story: action titles, honest charts | | |

**One question** you would ask the team: ______

::: source
Based on Hattie and Timperley (2007) and Knaflic (2015).
:::

::: notes
Hand the sheet out on paper or as a shared form. Feedback is formative: the sheets go to the presenting team after the session and are not part of the grade. Hattie and Timperley: feedback works when it says where the work is going, how it is going and where to go next, and when it addresses the task and the process rather than the person — hence "works well" and "next step" per criterion and no overall score. Same spirit as the format "two strengths, three suggestions, one question" from session 10. Collect the sheets per team at the end and hand them over; check briefly that no comment is personal.
:::

---

# The Course in Review {.section}

Four parts, one thread

---

# From Data to Decision — the Whole Course

![Four boxes for the course parts: A what happened (sessions 2–6, warehouse, grain, SQL, charts, portal), B who and does it work (sessions 7–9, framing, leakage, baseline, lift, experiment), C what comes next (sessions 11–14, decomposition, forecasts, intervals, many series), D at what scale (sessions 15–17, Spark or DuckDB, case study); all arrows lead to a decision, which leads on to the semester-6 project with a partner company](img/wu-course-map.png){width=90%}

::: source
Own illustration based on Kimball and Ross (2013), Chapman et al. (2000), Kohavi et al. (2020), Hyndman and Athanasopoulos (2021) and Zaharia et al. (2016).
:::

::: notes
The session 10 map showed Parts A and B; this one adds C and D. Each part answers a different kind of question: A describes the past from an integrated warehouse at a declared grain; B predicts for single units and tests whether an action works; C predicts how a quantity develops over time, with uncertainty; D asks whether the analysis still works when data, workload or platform exceed one machine. All four end in a decision — and the semester-6 project is the first time the decision is a real one at a partner company. Ask: which part did your case study use most, and which part was missing?
:::

---

# Parts C–D at a Glance

| Session | Core idea | Typical mistake |
|---|---|---|
| 11 Temporal data | Order, granularity, calendar; decompose before modelling | Summing a rate; ignoring time zones and incomplete periods |
| 12 Forecasting I | Baselines and time series cross-validation over many origins | Shuffled folds; judging one lucky split |
| 13 Forecasting II | Features known at the origin; intervals checked by coverage | Lags shorter than the horizon; observed weather in an "ex ante" test |
| 14 Forecasting at scale | Global models, coherent hierarchies, guards and monitoring | Hand-tuning hundreds of series; MAE that rewards forecasting zero |
| 15 Spark | Partitions, lazy plans, Parquet; smallest tool that works | Spark for data that fits on one machine — without measuring |

::: source
Own summary of sessions 11–15, based on Hyndman and Athanasopoulos (2021) and Zaharia et al. (2016).
:::

::: notes
Parts A–B were summarised in the same format in session 10 — refer students to that slide. Numbers to recall if asked: on daily electricity demand the SARIMA model beat seasonal naive by a modest margin (MAE 271 vs. 316 MW over 26 folds, session 12), and gradient boosting with lags and temperature climatology reached 228 MW ex ante (session 13); on 31 million property sales the simple median baseline beat linear regression (median error 18.3 % vs. 19.1 %, session 15), and DuckDB was faster than Spark on one machine. The common lesson: a strong, simple baseline is hard to beat, and the honest test design matters more than the model.
:::

---

# Five Questions That Ran Through Every Session

1. **Decision:** what will someone do differently because of this result?
2. **Definitions:** what exactly is measured — grain, formula, filters, time reference?
3. **Time:** was everything used known at the moment of the decision?
4. **Baseline:** how much better than the simple alternative, on unseen data?
5. **Uncertainty:** how sure are we — interval, coverage, trust checks — and is the method **suitable**?

::: callout
These five questions are also the best checklist for your **semester-6 project** — and for any analysis you will be asked to trust.
:::

::: source
Own synthesis based on Chapman et al. (2000), Kimball and Ross (2013), Kohavi et al. (2020) and Hyndman and Athanasopoulos (2021).
:::

::: notes
Ask the class to name one session example per question before revealing the list (if the projector allows, show it line by line). Examples: 1 framing slide of session 7 and the business evaluation by lift and profit; 2 grain and KPI definition sheets (sessions 3, 5, 6); 3 leakage and point-in-time features (session 7), lags at least the horizon (session 13); 4 majority class and simple rules (sessions 7–8), seasonal naive (12), median by district (15); 5 confidence intervals and SRM checks (9), prediction intervals and coverage (13), the suitability assessment at the end of every notebook (10).
:::

---

# Exercise: One Case, Four Parts {.exercise}

A city's bike-sharing operator has trip data for five years (60 million trips) and wants to put the right number of bikes at each station every morning. In pairs:

1. **Part A:** which fact table and grain, and which KPI would you put on the operations dashboard?
2. **Part B:** which station-level prediction or classification could help — and which leaky feature would you exclude?
3. **Part C:** what would you forecast, at what granularity and horizon, against which baseline?
4. **Part B again:** how would you test whether a new rebalancing rule reduces empty stations?
5. **Part D:** DuckDB or Spark — what decides?

::: notes
Pairs 6 min, plenary 6 min. Expected answers (several are acceptable):
1 Fact table of trips at the grain "one trip" (start/end station, times, bike, user type), plus a periodic snapshot of station fill levels (e.g. every 15 minutes); KPI: share of minutes a station is empty or full during peak hours, defined once with formula and time window; dashboard per district with row-level access for the field teams.
2 Classification: will station X run empty before 9:00 tomorrow? Features: fill level at the cut-off, recent departures, weekday, weather forecast. Leaky: the actual weather or trips after the cut-off, or a "rebalanced" flag set because the station ran empty. Baseline: yesterday's status or a rule from the fill level.
3 Departures and arrivals per station and hour (or the net flow), horizon one day, origin the evening before; seasonal naive (same hour last week) as baseline; external regressors: calendar, holidays, weather forecast; evaluate with time series cross-validation over many origins and check intervals by coverage; many series → a global model (session 14).
4 Randomise districts or days (not single stations — rebalancing trucks serve neighbouring stations, so stations interfere); primary metric: empty-station minutes; guardrails: truck kilometres, cost; plan sample size and duration in advance; if randomisation is impossible, difference-in-differences with comparable districts.
5 60 million trips fit comfortably on one machine as Parquet — DuckDB is enough for analysis; Spark if the data already lives in a cluster/lakehouse, if streaming fill levels must be processed continuously, or if the nightly pipeline must be fault tolerant. Measure before deciding (COST argument, session 15).
:::

---

# Outlook: The Semester-6 Project {.section}

Project Data Engineering and Analytics

---

# Semester 6 at a Glance

| Milestone | What happens | Result |
|---|---|---|
| Kickoff | Charter, scope and goals; roles and sub-teams; working agreements; toolchain | Project charter, sprint plan |
| Data engineering sprints | Requirements, architecture, ingestion, data model, data quality checks | Working data pipeline |
| Mid-term presentation | Status, architecture, first results, risks; feedback from company and lecturer | Course correction |
| Analytics and integration sprints | Analyses and models, evaluation, dashboard or data product, tests | Data product, documentation |
| Final presentation | Demo for the partner company; each student explains their contribution | Code, documentation, reflection |

- **Assessment:** project result 40 % · project management 15 % · presentations 25 % · individual contribution 20 %

::: source
Based on the module description *Project Data Engineering and Analytics* (W4DSKI_404), DHBW, Data Science and Artificial Intelligence.
:::

::: notes
From the approved project plan of W4DSKI_404 (data-engineering-analytics-project/SESSION_PLAN.md): semester 6 is implementation only. Plenary meetings: kickoff (3 h), mid-term presentation (3 h), final presentation (4 h) — about 10 h; the remaining ~40 h are team work that teams plan themselves. Each team is about half the course, so it organises itself into sub-teams (e.g. data engineering, analytics, product and project management) with a product owner contact at the company and rotating roles. Individual grades can differ within a team through the individual component (reflection, own contribution defended in the final presentation, peer assessment as input).
:::

---

# What Carries Over from This Course

| Project phase | From Data Analytics |
|---|---|
| Understanding the problem | Framing: decision, unit, target, success metric (S7); KPI definitions (S5–6) |
| Data engineering | Grain, conformed dimensions, history and validity periods (S2–3, S11); data quality checks |
| Analytics | Baselines, time-aware validation, forecasts with intervals, experiments (S7–9, S12–14) |
| Data product | Dashboard with defined metrics and access rules (S6); the smallest tool that works (S15) |
| Reviews and presentations | Big idea, action titles, structured feedback (S5, S10, today) |

::: callout
A **sprint review** is a working session with stakeholders, not only a show: bring results, open questions and a proposal for what comes next.
:::

::: source
Own mapping; sprint review based on Schwaber and Sutherland (2020).
:::

::: notes
The project plan suggests Scrum with sprints (module W4DSKI_404). The Scrum Guide describes the sprint review as an inspection of the outcome with stakeholders to decide on future adaptations, explicitly "a working session" rather than a presentation, and the retrospective as the team's planning of improvements. Teams that used the feedback round of the case study workshop well have already practised both. Data engineering topics in depth come from the parallel module Data Engineering (W4DSKI_401); this course contributes the analyst's view.
:::

---

# Project A: {{private:partner_a|Partner Company A}}

**Topic:** {{private:partner_a_topic|Presented by the partner company in session 1}}

- Status of the project brief: goal, stakeholders, as-is process, data inventory
- Agreements still open: data access, confidentiality, results, code hosting
- First steps for the kickoff: charter draft, sub-teams, contact person

::: notes
Team A states in two minutes where it stands. Company name and topic are filled in only in the offline PPTX (from tools/local.json); the public web version shows a placeholder. Do not write any project details into this file — notes are public. The open agreements (data access, NDA, intellectual property of results, where code is hosted) must be settled with the company before the kickoff; note them in the lecturer's private notes for the project module.
:::

---

# Project B: {{private:partner_b|Partner Company B}}

**Topic:** {{private:partner_b_topic|Presented by the partner company in session 1}}

- Status of the project brief: goal, stakeholders, as-is process, data inventory
- Agreements still open: data access, confidentiality, results, code hosting
- First steps for the kickoff: charter draft, sub-teams, contact person

::: notes
Team B, same structure as team A so the two teams can compare. Same confidentiality rule: no project details in this public file. If a team has no data access yet, agree today who requests it formally and by when — access delays were the most common risk named in session 10.
:::

---

# Your Feedback on the Course {.exercise}

On a card or in the online form — anonymous:

- **Keep:** what helped you learn most?
- **Change:** what should be different next year?
- **Add or drop:** which topic deserves more time — and which less?

::: callout
Your answers change the next run of this course: the session plan is revised after every semester.
:::

::: notes
Collect cards or use the online form; the official DHBW course evaluation runs separately and does not replace this. Ask especially about timing (input vs. lab share, the 3 h blocks), the worksheets, the datasets (TPC-H, vic_elec, Price Paid Data) and the portfolio workload. Record the results in the lecturer's private notes for the course. Thank the class — and the teams for their presentations.
:::

---

# Key Takeaways

- A case study convinces with a **big idea**, an **honest evaluation** against a baseline and a **clear recommendation with its limits**
- Good feedback is **specific and actionable** — on the work, not the person
- The course follows one thread: **data → method → evaluation → decision**, from warehouse to forecast to scale
- Five questions travel with you: **decision, definitions, time, baseline, uncertainty**
- Semester 6 turns this into a **real project**: plan it, review it with stakeholders, and keep partner information confidential

---

# What Comes Next: Kickoff in Semester 6

- **Portfolio:** hand in the case study notebook and the research brief by the dates in the portfolio brief
- **Project brief:** finish it with your team before the end of semester 5
- **Agreements:** data access, confidentiality, results and code hosting — settled before the kickoff
- **Toolchain:** a private repository for the team; no partner data or code in public places

::: callout
**Preparation for the kickoff:** bring the project brief, a first draft of roles and sub-teams, and the list of open questions for your partner company.
:::

::: notes
There is no session 18: the next plenary meeting is the kickoff of Project Data Engineering and Analytics in semester 6 (3 h: charter, roles, project management approach, working agreements, toolchain, assessment criteria). Worksheet 17 is a revision and reflection set across the whole course — useful for the remaining portfolio work and as a refresher before the kickoff.
:::

---

# References {.references}

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS.
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Knaflic, C. N. (2015). *Storytelling with data: A data visualization guide for business professionals*. Wiley.
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy online controlled experiments: A practical guide to A/B testing*. Cambridge University Press. https://doi.org/10.1017/9781108653985
- Provost, F., & Fawcett, T. (2013). *Data science for business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.
- Schwaber, K., & Sutherland, J. (2020). *The Scrum guide: The definitive guide to Scrum: The rules of the game*. https://scrumguides.org/docs/scrumguide/v2020/2020-Scrum-Guide-US.pdf
- Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., Meng, X., Rosen, J., Venkataraman, S., Franklin, M. J., Ghodsi, A., Gonzalez, J., Shenker, S., & Stoica, I. (2016). Apache Spark: A unified engine for big data processing. *Communications of the ACM, 59*(11), 56–65. https://doi.org/10.1145/2934664
