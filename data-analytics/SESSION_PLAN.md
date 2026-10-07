# Data Analytics — Session Plan (approved 2026-10-07)

50 h (60-minute hours) = **16 sessions × 3 h + 1 final session × 2 h**. Semester 5, DSKI. Assessment: portfolio.

**Focus (module handbook):** apply algorithms to specific use cases, rather than teach how they work. Students already know the ML basics from *Foundations of Data Science and AI*. So every session starts from a business use case and asks: *which method, how to adapt it, and is it suitable?*

**Hands-on tooling:** Python + Jupyter; **DuckDB** for the data warehouse, OLAP and analytical SQL (runs in-process on macOS and Windows, no server needed); scikit-learn and statsmodels for ML and time series; **PySpark** for big data (local mode, or a free cloud notebook if local Java setup is a problem); **Streamlit** for a small analytics portal/dashboard. All labs use public datasets.

**Link to semester 6:** in session 1 the two partner companies present their projects for *Project Data Engineering and Analytics*, and students split into two teams. Company names go only in the offline PPTX.

Legend for learning-outcome links: **SC** subject competence · **MC** methodological competence · **PSC** personal/social · **OC** overarching (see [MODULE.md](MODULE.md)).

## Part A — Analytics Foundations and Data Warehousing

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 1 | **Introduction to data analytics and project pitches** | Course overview and portfolio; development of data analysis from reporting and BI to advanced analytics and AI; descriptive, diagnostic, predictive, prescriptive analytics; application areas; partner companies present the semester-6 projects; team formation | Map use cases to analytics types; choose a project team | SC, PSC |
| 2 | **Data warehouse architectures** | OLTP vs. OLAP; DWH reference architecture (sources, staging, core DWH, data marts); Inmon vs. Kimball; DWH in the lakehouse era | Explore a sample warehouse in DuckDB: what data is where? | SC |
| 3 | **Dimensional data and OLAP** | Star and snowflake schema; facts, measures, dimensions, hierarchies; slowly changing dimensions; OLAP cube and operations (slice, dice, drill-down, roll-up, pivot) | Answer business questions with OLAP operations | SC, MC |
| 4 | **Analytical SQL** | Window functions, `ROLLUP`/`CUBE`/`GROUPING SETS`, CTEs; typical analyses: rankings, running totals, cohorts, funnels; interpreting the results | SQL lab on the sample warehouse | MC |
| 5 | **Data visualisation** | Purpose-driven chart choice; perception and visual encoding; misleading charts; storytelling with data; KPI design | Redesign bad charts; visualise lab results | SC, MC |
| 6 | **Analytics portals** | Structure and infrastructure of analytics portals: BI tools, semantic layer, self-service BI, dashboards, embedded analytics, access and governance | Build a small dashboard on the warehouse (Streamlit) | SC, MC, OC |

## Part B — Machine Learning for Data Analysis

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 7 | **From business question to ML task** | Analytics process (CRISP-DM); framing a use case as supervised or unsupervised problem; data understanding; feature engineering; baselines; data leakage | Frame three business cases as ML tasks | MC, OC |
| 8 | **Supervised learning I: classification use cases** | Use cases such as churn, fraud, credit risk; choosing a model; evaluation metrics and cost of errors; class imbalance; is the model fit for purpose? | Churn prediction lab | MC |
| 9 | **Supervised learning II: regression use cases and model tuning** | Use cases such as demand and price prediction; validation strategies; hyperparameter tuning; adapting models to a use case; interpretability (feature importance, SHAP) | Price prediction lab with tuning | MC |
| 10 | **Unsupervised learning use cases** | Customer segmentation (clustering), market basket analysis (association rules), anomaly detection; evaluating results without labels; turning segments into actions | Segmentation and basket analysis lab | MC, OC |
| 11 | **Lab workshop and catch-up** | Buffer block: no new content; catch up on Parts A–B; portfolio work and consultations; teams' first findings for the partner projects | Portfolio lab work, consultations | PSC |

## Part C — Temporal Data and Time Series

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 12 | **Temporal data and time series fundamentals** | Characteristics of temporal data; time in the warehouse (time dimension, validity periods, bitemporal data); trend, seasonality, autocorrelation, stationarity; resampling and decomposition | Explore and decompose a real time series | SC, MC |
| 13 | **Time series forecasting I** | Baselines (naive, seasonal naive); exponential smoothing; ARIMA family; forecast evaluation (time-series cross-validation, MAE, MAPE) | Sales or energy forecast lab | MC |
| 14 | **Time series forecasting II and use cases** | ML-based forecasting with lag features; forecasting many series; anomaly detection in time series; choosing a method for a use case | Demand forecasting case | MC, OC |

## Part D — Big Data Analytics

| # | Session | Contents | Lab / activity | LO |
|---|---|---|---|---|
| 15 | **Big data analytics with Spark** | Typical big data questions; distributed processing; Spark architecture; DataFrames and Spark SQL; when big data tools are (not) needed | Analyse a large public dataset with PySpark | SC, MC |
| 16 | **Scalable machine learning** | ML pipelines with Spark MLlib; evaluating models at scale; costs and limits; course synthesis | Spark ML lab | MC, OC |
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
- Session 11 is a buffer block, so earlier sessions can overrun without cutting topics.

## Notes

- No exam Q&A needed: the portfolio has no written exam. The 2 h block is used for the presentations.
- Sources (module literature plus primary sources such as Kimball & Ross, Inmon, Chapman et al. for CRISP-DM, Hyndman & Athanasopoulos for forecasting, Zaharia et al. for Spark) are checked and cited on the slides when each session is built.
