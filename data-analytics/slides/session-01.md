---
course: Data Analytics
session: 1
title: Introduction to Data Analytics
subtitle: Course overview · development and types of analytics · partner projects
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Introduction to Data Analytics {.title}

::: notes
Welcome. Short introduction of yourself and of the two partner companies (they are present for their pitches later today).
Time plan for today (3 h): course intro 25 min · development of analytics 30 min · break 10 min · types and application areas 30 min · partner project pitches 45 min · team formation 20 min · wrap-up and setup check 10 min · ~10 min buffer.
Agree the exact pitch slot with the companies beforehand; the pitches can also come first if their schedule requires it.
:::

---

# Today's Agenda

1. Welcome and course overview
2. How data analysis developed: from reporting to AI
3. Types of analytics and application areas
4. Partner projects for semester 6
5. Team formation
6. Outlook and tool setup

::: notes
Time and format guide (not shown to students):
0:00 Welcome and course overview (input) · 0:25 Development of analytics (input + discussion) · 0:55 Break · 1:05 Types and application areas (input + quick check) · 1:35 Partner pitches (company presentations + Q&A) · 2:20 Team formation · 2:40 Outlook and setup check · ~10 min buffer.
If the companies need more time for Q&A, shorten the application areas part; the quick check can be done at home.
:::

---

# What You Will Be Able to Do After This Module

- **Explain** how data analysis developed and where it is applied
- **Interpret and evaluate** data in typical data warehouse architectures, using analytical SQL and OLAP
- **Select, adapt and assess** machine learning methods for concrete business use cases
- **Analyse** temporal data and build time series forecasts
- **Analyse** large data volumes with big data frameworks
- **Present** results in visualisations and analytics portals

::: source
Based on the module description *Data Analytics* (W4DSKI_402), DHBW, Data Science and Artificial Intelligence.
:::

::: notes
Paraphrased from the official module description (MODULE.md).
:::

---

# Focus of This Module: Application

::: callout
You already know how the most important algorithms work. In this module, we ask: **which method fits this use case, how do I adapt it, and is the result fit for purpose?**
:::

- Every session starts from a **business use case**
- Hands-on **lab work** takes a large share of each session
- We judge methods by their **suitability**, not only by their accuracy

::: source
Based on the module description *Data Analytics* (W4DSKI_402), section "Besonderheiten".
:::

::: notes
The module handbook explicitly says the focus is not on the foundations of the algorithms but on their application to specific use cases. Prerequisite: Foundations of Data Science and AI.
:::

---

# Course Roadmap: Four Parts

| Part | Sessions | Topics |
|---|---|---|
| A · Analytics foundations and data warehousing | 1–6 | Analytics types, DWH architectures, OLAP, analytical SQL, visualisation, analytics portals |
| B · Machine learning use cases and experiments | 7–10 | From business question to ML use case, ML use-case lab, A/B testing, lab workshop |
| C · Temporal data and time series | 11–14 | Temporal data, forecasting methods, forecasting at scale and use cases |
| D · Big data analytics and case study | 15–17 | Analytics with Spark, case study workshop, portfolio presentations |

::: notes
You know the ML methods from Foundations of Data Science and AI and from AI and Machine Learning, and Spark from Cloud Computing and Big Data — here we apply them to use cases. Session 10 is a buffer: no new content, time for catching up, portfolio work and consultations. Session 17 is a shorter block with the portfolio presentations.
:::

---

# How We Work

::: cards
### Input and lab
Short input, then hands-on lab work on real, public datasets.

### Core and optional slides
Core slides are relevant for the portfolio. Slides marked **Optional · Self-study** are for deeper reading.

### Tools
Python, Jupyter, DuckDB, scikit-learn, statsmodels, PySpark and Streamlit. All run on Windows and macOS.

### Questions welcome
Discussion is part of the course. If a topic needs more time, we take it.
:::

::: notes
Ask students to bring a laptop from session 2 on. Setup instructions are at the end of this deck.
:::

---

# Assessment: Portfolio

| Component | Form | Weight |
|---|---|---|
| Lab notebooks | Three notebooks in pairs: data warehouse and analytical SQL · machine learning use case · time series forecast — each with a short assessment of method suitability | 45 % |
| Group case study | End-to-end analytics case on a public dataset in larger groups, incl. a big data framework or dashboard; notebook and presentation | 40 % |
| Individual research brief | Short paper on a topic not covered in class, researched on your own | 15 % |

::: callout
The case study uses **public data**, not data from the partner companies. The partner projects are assessed separately in semester 6.
:::

::: notes
Portfolio agreed 2026-10-07. Detailed briefs, deadlines and grading rubrics will be published separately. Explain why partner data is excluded: confidentiality, and no double assessment of the same work in two modules.
:::

---

# Core Literature

| Topic | Book |
|---|---|
| BI and analytics, data warehousing | Baars and Kemper (2021) |
| Data analytics methods | Runkler (2020); Berthold et al. (2020) |
| Big data analytics | Ghavami (2020); Dulhare et al. (2020) |
| Spark | Parsian (2022); Tandon et al. (2022) |

Full references at the end of this deck.

::: notes
Check e-book availability in the DHBW library before the first lecture. Runkler: a newer edition may exist; check the library catalogue and update the reference if needed.
:::

---

# How Data Analysis Developed {.section}

From reporting to AI

---

# From Decision Support to Analytics

| Period | Typical systems | Main question |
|---|---|---|
| 1970s–1980s | Management information systems, decision support systems | Which reports does management need? |
| 1990s | Data warehouse, OLAP, data mining | How do we integrate data for analysis? |
| 2000s | Business intelligence suites, dashboards, web analytics | Where do we stand right now? |
| 2010s | Big data platforms, data science, cloud analytics | What can we predict from all our data? |
| 2020s | Machine learning in production, AI, real-time analytics | How do we embed analytics into processes? |

::: source
Own summary based on Baars and Kemper (2021, Chapter 1) and Chen et al. (2012).
:::

::: notes
The decades are approximate; the systems overlap and coexist in most companies today. Ask students which of these systems they have seen in their training companies (most will know reporting and dashboards, fewer production ML).
:::

---

# BI&A 1.0, 2.0, 3.0

::: cards
### BI&A 1.0
Structured data from internal systems; data warehouse, ETL, OLAP, reports and dashboards.

### BI&A 2.0
Web data: clickstreams, user-generated content, text and opinion mining, social networks.

### BI&A 3.0
Mobile and sensor data: location, context, Internet of Things.
:::

::: source
Chen et al. (2012).
:::

::: notes
Chen, Chiang and Storey describe the evolution of business intelligence and analytics (BI&A) by data source. The key point: each stage adds new data types and methods, but does not replace the earlier ones. A data warehouse (BI&A 1.0) is still at the core of most analytics landscapes.
:::

---

# Analytics 1.0, 2.0, 3.0

::: layers
- Analytics 3.0: Analytics embedded in products, services and operational processes — at scale
- Analytics 2.0: Big data, mostly in online firms; data scientists; new technologies
- Analytics 1.0: Internal, structured data; descriptive reports; analysts in back rooms
:::

::: source
Based on Davenport (2013).
:::

::: notes
Davenport describes a shift from analytics as back-office reporting (1.0) via the big data era of online companies (2.0) to analytics built directly into products and operational decisions (3.0) — in all industries, not only tech firms. Earlier, Davenport (2006) argued that some firms "compete on analytics" — analytics as a source of competitive advantage. Discussion question: in which era is your training company?
:::

---

# Types of Analytics {.section}

What happened? Why? What will happen? What should we do?

---

# Four Types of Analytics

::: layers
- Prescriptive: What should we do? — optimisation, simulation, recommendation
- Predictive: What will happen? — forecasting, classification, regression
- Diagnostic: Why did it happen? — drill-down, correlation, root-cause analysis
- Descriptive: What happened? — reports, dashboards, OLAP
:::

::: source
Based on Delen and Ram (2018).
:::

::: notes
Read the diagram bottom-up: value and complexity usually increase towards the top. Delen and Ram describe descriptive, predictive and prescriptive analytics; the diagnostic level is a common addition in practice. In this module: Part A is mostly descriptive and diagnostic, Parts B and C predictive; prescriptive analytics appears in the use cases (e.g. what to do with a churn score).
:::

---

# The Analytics Process in Practice

- Analytics projects rarely go in a straight line from data to model
- Most of the effort is in **understanding the business problem** and **preparing the data**
- A model is only useful if it is **deployed** and its results are **used** in decisions
- We use **CRISP-DM** as a process model from session 7 on

::: source
Chapman et al. (2000).
:::

::: notes
CRISP-DM phases: business understanding, data understanding, data preparation, modelling, evaluation, deployment. Only a preview today; details in session 7. Mention that the partner projects in semester 6 follow the same logic.
:::

---

# Application Areas

| Area | Typical use cases |
|---|---|
| Sales and marketing | Customer segmentation, churn prediction, recommendation, campaign analysis |
| Finance and risk | Fraud detection, credit scoring, liquidity forecasting |
| Operations and supply chain | Demand forecasting, inventory optimisation, route planning |
| Production and maintenance | Predictive maintenance, quality inspection, energy optimisation |
| Human resources | Workforce planning, attrition analysis |
| Public sector and health | Traffic planning, epidemiology, resource planning in hospitals |

::: source
Own compilation based on Baars and Kemper (2021) and Chen et al. (2012).
:::

::: notes
Many of these use cases come back in the labs: churn (session 8), price prediction (9), segmentation and basket analysis (10), demand forecasting (13–14).
:::

---

# Quick Check: Which Type of Analytics? {.exercise}

1. A dashboard shows monthly revenue per product group.
2. An analyst investigates why returns increased in one region.
3. A model estimates how many customers will cancel their contract next quarter.
4. A system suggests the best order quantity for each store.
5. A machine learning model predicts the remaining useful life of a pump.

::: notes
Answers: 1 descriptive · 2 diagnostic · 3 predictive · 4 prescriptive (optimisation, usually based on a forecast) · 5 predictive (predictive maintenance) — becomes prescriptive if it also schedules the maintenance. Discuss borderline cases: prescriptive analytics almost always builds on predictive models.
:::

---

# Partner Projects for Semester 6 {.section}

Project Data Engineering and Analytics

---

# The Semester-6 Project at a Glance

- **Two partner companies, two real projects** in data engineering and analytics
- The course splits into **two project teams**
- **Semester 5:** get to know the project, the stakeholders and the data — alongside this module
- **Semester 6:** implementation; plenary meetings only for kickoff, mid-term and final presentation
- Assessment: **project** (result, project management, presentations, individual contribution)

::: callout
Starting now gives you a head start: use what you learn in this module for your project.
:::

::: notes
Hours in semester 6: about 10 h of plenary meetings; the remaining ~40 h are team work that teams plan themselves. Details in the kickoff deck of the project module.
:::

---

# Project A: {{private:partner_a|Partner Company A}}

**Topic:** {{private:partner_a_topic|Presented by the partner company in class}}

- Who are we, and what do we do?
- What is the business problem?
- What data is available?
- What should the result be?
- Who are your contacts?

::: notes
Hand over to the first partner company. The company names and topics are filled in only in the offline PPTX (from tools/local.json); the public web version shows a placeholder.
Remind students to note open questions for the Q&A.
:::

---

# Project B: {{private:partner_b|Partner Company B}}

**Topic:** {{private:partner_b_topic|Presented by the partner company in class}}

- Who are we, and what do we do?
- What is the business problem?
- What data is available?
- What should the result be?
- Who are your contacts?

::: notes
Hand over to the second partner company. Same structure as project A so the two pitches are comparable.
:::

---

# Questions to Ask the Partners {.exercise}

- What **decision** or process should the result improve?
- How will **success** be measured?
- What **data** exists, in which systems, at what volume and quality?
- What are the **constraints**: data access, confidentiality, technology?
- Who are the **stakeholders**, and who will use the result?

::: notes
Use this slide during the Q&A after each pitch if students hesitate to ask questions. Information shared by the companies is confidential: remind students not to post it in public repositories or chats.
:::

---

# Team Formation

- Choose the project you want to work on
- Both teams should be roughly the **same size** and have a **mix of skills**
- Inside each team, plan **sub-teams** later, e.g. data engineering, analytics, project management

::: callout
Information from the partner companies is **confidential**. Do not share it outside the team, and never put company data or code in public repositories.
:::

::: notes
Procedure: students write their first and second choice; balance the teams if needed. Record team lists offline (STATUS.md of the project module, which is not published).
:::

---

# Preparation in Semester 5

By the end of semester 5, each team prepares a short **project brief**:

1. Business goals and success criteria
2. Stakeholders and their interests
3. Current process (as-is)
4. First data inventory: sources, volume, quality, access
5. Open questions, risks and first ideas for the solution

::: notes
The project brief is not graded in this module; it prepares the kickoff in semester 6. Agree a submission date with the teams.
:::

---

# Critical Perspective: Analytics Is Not Always the Answer {.optional}

- Many analytics initiatives fail for **organisational** rather than technical reasons: unclear goals, missing data, no one acts on the results
- A simple report can be the **better solution** than a complex model
- Predictions change behaviour — and models trained on past data can **repeat past biases**

::: source
Own summary; see also Davenport (2013) and Provost and Fawcett (2013).
:::

::: notes
Self-study. Good discussion material for the partner projects: what would make the project fail?
:::

---

# Key Takeaways

- Data analysis developed from **reporting and decision support** via the **data warehouse** and **big data** to **analytics embedded in processes and products**
- **Descriptive, diagnostic, predictive and prescriptive** analytics answer different questions
- This module is about **applying** methods to use cases and judging whether they **fit**
- The **partner projects** start now: use semester 5 to understand the problem and the data

---

# Next Session: Data Warehouse Architectures

- OLTP vs. OLAP
- Data warehouse reference architecture
- Inmon vs. Kimball, and the data warehouse in the lakehouse era
- **Lab:** explore a sample warehouse in DuckDB

::: callout
**Preparation:** bring your laptop and complete the tool setup on the next slide.
:::

---

# Tool Setup

1. Install **Python 3.12 or newer** from python.org (Windows: tick *Add python.exe to PATH*)
2. Open a terminal and install the packages:

```bash
python -m pip install jupyterlab duckdb pandas matplotlib scikit-learn statsmodels streamlit
```

3. Start Jupyter with `python -m jupyter lab` and run this test cell:

```python
import duckdb
duckdb.sql("SELECT 'setup works' AS status").show()
```

::: notes
On macOS use python3 instead of python. We start Jupyter via python -m because pip's Scripts folder is not always on the PATH on Windows. If students already use Anaconda, Miniconda or VS Code with Jupyter, that is fine. PySpark is installed later (session 15) because it needs Java. If the test fails, collect the error messages and solve them at the start of session 2.
:::

---

# References {.references}

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS.
- Chen, H., Chiang, R. H. L., & Storey, V. C. (2012). Business intelligence and analytics: From big data to big impact. *MIS Quarterly, 36*(4), 1165–1188. https://doi.org/10.2307/41703503
- Davenport, T. H. (2006). Competing on analytics. *Harvard Business Review, 84*(1), 98–107.
- Davenport, T. H. (2013). Analytics 3.0. *Harvard Business Review, 91*(12), 64–72.
- Delen, D., & Ram, S. (2018). Research challenges and opportunities in business analytics. *Journal of Business Analytics, 1*(1), 2–12. https://doi.org/10.1080/2573234X.2018.1507324
- Provost, F., & Fawcett, T. (2013). Data science and its relationship to big data and data-driven decision making. *Big Data, 1*(1), 51–59. https://doi.org/10.1089/big.2013.1508

---

# References: Module Literature {.references}

- Baars, H., & Kemper, H.-G. (2021). *Business Intelligence & Analytics: Grundlagen und praktische Anwendungen* (4th ed.). Springer Vieweg. https://doi.org/10.1007/978-3-8348-2344-1
- Berthold, M. R., Borgelt, C., Höppner, F., Klawonn, F., & Silipo, R. (2020). *Guide to intelligent data science: How to intelligently make use of real data* (2nd ed.). Springer. https://doi.org/10.1007/978-3-030-45574-3
- Dulhare, U. N., Ahmad, K., & Bin Ahmad, K. A. (Eds.). (2020). *Machine learning and big data: Concepts, algorithms, tools and applications*. Wiley-Scrivener.
- Ghavami, P. (2020). *Big data analytics methods: Analytics techniques in data mining, deep learning and natural language processing* (2nd ed.). De Gruyter. https://doi.org/10.1515/9781547401567
- Parsian, M. (2022). *Data algorithms with Spark: Recipes and design patterns for scaling up using PySpark*. O'Reilly Media.
- Runkler, T. A. (2020). *Data analytics: Models and algorithms for intelligent data analysis* (3rd ed.). Springer Vieweg. https://doi.org/10.1007/978-3-658-29779-4
- Tandon, A., Ryza, S., Laserson, U., Owen, S., & Wills, J. (2022). *Advanced analytics with PySpark: Patterns for learning from data at scale using Python and Spark*. O'Reilly Media.
