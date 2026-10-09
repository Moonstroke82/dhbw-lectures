# Data Analytics — Session Plan (approved 2026-10-07, revised 2026-10-09)

50 h (60-minute hours) = **16 sessions × 3 h + 1 final session × 2 h**. Semester 5, DSKI. Assessment: portfolio.

**Focus (module handbook):** apply algorithms to specific use cases, rather than teach how they work. So every session starts from a business use case and asks: *which method, how to adapt it, and is it suitable?*

**What students bring from other DSKI modules** (module handbook DSKI Mannheim, checked 2026-10-09). Students take the track *Data Engineering and Analytics* (W4DSKI_401–404); the track *Intelligence Engineering* (W4DSKI_410–413) runs in parallel and is not part of their studies.

| Prior or parallel module | Content students already know | Consequence for this course |
|---|---|---|
| W4DSKI_101 Foundations of Data Science and AI | Supervised/unsupervised learning, training and test data, over- and underfitting, regression, decision trees, clustering, association rules | No ML basics; at most a short recap |
| W4DSKI_201 AI and Machine Learning | Cross-validation, logistic regression, kNN, regularisation, ensembles, SVM, neural networks, PCA, k-means, hierarchical clustering, isolation forest, with lab | No method sessions; ML is reduced to use-case framing and one use-case lab |
| W4DSKI_204 Cloud Computing and Big Data | Data lake, lambda/kappa architecture, Hadoop and Spark, with lab | No Spark architecture introduction; one session on analytics with Spark |
| W4DSKI_401 Data Engineering (same track, year 3) | Data warehouse modelling (star, snowflake), design principles, ETL, data lake | This course *uses* the warehouse (queries, OLAP, interpretation); building it belongs to 401 — design details are optional slides here |
| W4DSKI_206 Stochastics | Estimation, confidence intervals, hypothesis tests, experimental design | Basis for the session on experiments and A/B testing |
| W4DSKI_BM305 Implementing DS and AI in companies (year 3) | Predictive modelling for business tasks, visualising model performance, DS and business strategy | Coordinate with its lecturer; semester of BM305 and 401 still to be confirmed |

Not covered elsewhere — and therefore the core of this course: analytical SQL and OLAP, visualisation and analytics portals, experiments, and **temporal data and time series forecasting**. Tuning and ML pipelines are taught only in the other track (W4DSKI_411), so they appear in applied form in the ML use-case lab.

**Hands-on tooling:** Python + Jupyter; **DuckDB** for the data warehouse, OLAP and analytical SQL (runs in-process on macOS and Windows, no server needed); scikit-learn and statsmodels for ML and time series; **PySpark** for big data (local mode, or a free cloud notebook if local Java setup is a problem); **Streamlit** for a small analytics portal/dashboard. All labs use public datasets.

**Link to semester 6:** in session 1 the two partner companies present their projects for *Project Data Engineering and Analytics*, and students split into two teams. Company names go only in the offline PPTX.

Legend for learning-outcome links: **SC** subject competence · **MC** methodological competence · **PSC** personal/social · **OC** overarching (see [MODULE.md](MODULE.md)).

## Part A — Analytics Foundations and Data Warehousing

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 1 | **Introduction to data analytics and project pitches** | Course overview and portfolio; development of data analysis from reporting and BI to advanced analytics and AI; descriptive, diagnostic, predictive, prescriptive analytics; application areas; partner companies present the semester-6 projects; team formation | Map use cases to analytics types; choose a project team | SC, PSC |
| 2 | **Data warehouse architectures** | The analyst's view of the warehouse: OLTP vs. OLAP; reference architecture (what data is in which layer, and how far to trust it); Inmon vs. Kimball and lakehouse as a short recap of Data Engineering | Explore a sample warehouse in DuckDB: what data is where? | SC |
| 3 | **Dimensional data and OLAP** | Reading a dimensional model: facts, measures, grain, dimensions, hierarchies; OLAP cube and operations (slice, dice, drill-down, roll-up, pivot); design steps and slowly changing dimensions as optional self-study (taught in Data Engineering) | Answer business questions with OLAP operations on a star schema | SC, MC |
| 4 | **Analytical SQL** | Window functions, `ROLLUP`/`CUBE`/`GROUPING SETS`, CTEs; typical analyses: rankings, running totals, cohorts, funnels; interpreting the results | SQL lab on the sample warehouse | MC |
| 5 | **Data visualisation** | Purpose-driven chart choice; perception and visual encoding; misleading charts; storytelling with data; KPI design | Redesign bad charts; visualise lab results | SC, MC |
| 6 | **Analytics portals** | Structure and infrastructure of analytics portals: BI tools, semantic layer, self-service BI, dashboards, embedded analytics, access and governance | Build a small dashboard on the warehouse (Streamlit) | SC, MC, OC |

## Part B — Machine Learning Use Cases and Experiments

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 7 | **From business question to ML use case** | Short recap of ML methods (known from Foundations of DS and AI, AI and ML); analytics process (CRISP-DM); framing a business problem as an ML task; features from warehouse data; baselines; data leakage; judging a model by business cost (cost matrix, lift) and assessing suitability | Frame three business cases as ML tasks; build features from the star schema | MC, OC |
| 8 | **ML use-case lab** | Students choose a use case — churn prediction, customer segmentation or anomaly detection — and apply methods they know; scikit-learn pipelines and hyperparameter tuning in applied form; interpreting and communicating results | Use-case lab (portfolio notebook 2) | MC, OC |
| 9 | **Experiments and A/B testing** | Analytics for causal questions: correlation vs. causation; A/B test design (hypothesis, metric, sample size); analysing results and common pitfalls (peeking, multiple testing); when experiments are not possible | Analyse a public A/B test dataset | MC, OC |
| 10 | **Lab workshop and catch-up** | Buffer block: no new content; catch up on Parts A–B; portfolio work and consultations; teams' first findings for the partner projects | Portfolio lab work, consultations | PSC |

## Part C — Temporal Data and Time Series

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 11 | **Temporal data and time series fundamentals** | Characteristics of temporal data; time in the warehouse (time dimension, validity periods, bitemporal data); trend, seasonality, autocorrelation, stationarity; resampling and decomposition | Explore and decompose a real time series | SC, MC |
| 12 | **Time series forecasting I** | Baselines (naive, seasonal naive); exponential smoothing; ARIMA family; forecast evaluation (time-series cross-validation, MAE, MAPE) | Sales or energy forecast lab | MC |
| 13 | **Time series forecasting II** | ML-based forecasting with lag and calendar features; external regressors (holidays, promotions, weather); prediction intervals and forecast uncertainty | Demand forecast with features and intervals | MC |
| 14 | **Forecasting at scale and use cases** | Forecasting many series (global models, hierarchies and reconciliation); intermittent demand; anomaly detection in time series; choosing a method for a use case | Demand forecasting case (portfolio notebook 3) | MC, OC |

## Part D — Big Data Analytics and Case Study

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 15 | **Big data analytics with Spark** | Short recap of Spark (known from Cloud Computing and Big Data); analysing large data with Spark SQL and DataFrames; one ML pipeline with Spark MLlib; when DuckDB is enough and when a big data framework is needed | Analyse a large public dataset with PySpark | SC, MC |
| 16 | **Case study workshop** | Team work on the group case study; review of approach, results and dashboards; feedback round; preparation of the presentations | Team consultations | PSC, OC |
| 17 | **Portfolio presentations and wrap-up (2 h)** | Group case study presentations; feedback; outlook to semester 6 | Presentations | PSC, OC |

## Portfolio (agreed 2026-10-07)

| Component | Form | Weight |
|---|---|---|
| Lab notebooks | Three notebooks in pairs: (1) DWH / OLAP / analytical SQL, (2) ML use case, (3) time series forecast; each with a short written assessment of method suitability | 45 % |
| Group case study | End-to-end analytics case on a public dataset in larger groups (handbook allows this), incl. a big data framework or dashboard; notebook + presentation in session 17 | 40 % |
| Individual research brief | Short paper on a topic not covered in class (e.g. a new method or tool), researched independently | 15 % |

The case study deliberately does **not** use partner-company data (confidentiality, and no double assessment with the semester-6 project). Portfolio rules in the DHBW study and examination regulations still to be checked.

## Teaching principles (as for the other courses)

- **Don't squeeze.** Discussion is valuable and should never be cut just to get through the slides.
- **Each 3 h block is planned as roughly:** ~60 min input · ~90 min lab · ~15–30 min unplanned buffer. Labs are a large share here because of the application focus.
- **Core vs. optional slides.** Optional content moves to self-study if a session runs long, not to the next session.
- Session 10 is a buffer block, so earlier sessions can overrun without cutting topics.

## Notes

- No exam Q&A needed: the portfolio has no written exam. The 2 h block is used for the presentations.
- Sources (module literature plus primary sources such as Kimball & Ross, Inmon, Chapman et al. for CRISP-DM, Kohavi et al. for online experiments, Hyndman & Athanasopoulos for forecasting, Zaharia et al. for Spark) are checked and cited on the slides when each session is built.

## Changes

- 2026-10-09: ML part reduced from four sessions to two (framing + use-case lab) and big data from two sessions to one, because students already know ML methods (W4DSKI_101, 201) and Spark (204). Freed time: experiments and A/B testing (new), a fourth time series session, and a case study workshop. Data warehouse design moved to optional slides (taught in W4DSKI_401).
