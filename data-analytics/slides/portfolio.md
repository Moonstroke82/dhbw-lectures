---
course: Data Analytics
title: Portfolio Tasks
subtitle: Three lab notebooks · group case study · Lastenheft and Pflichtenheft · kickoffs and hand-ins
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Portfolio Tasks {.title}

::: notes
Separate deck, shown after the course overview in session 1. It replaces the assessment slide of the session 1 deck: the individual research brief is dropped and replaced by a Lastenheft and Pflichtenheft for the partner project, written in groups.
Rule of thumb for all three notebooks: kickoff in a fixed session, hand-in two weeks later. Replace "+ 2 weeks" with calendar dates once the timetable is final, and publish the same dates on the course platform.
:::

---

# The Portfolio at a Glance

| Component | Work form | Weight |
|---|---|---|
| Three lab notebooks: (1) warehouse and analytical SQL · (2) machine learning use case · (3) time series forecast | Pairs | 45 % (15 % each) |
| Group case study: end-to-end analytics case on a public dataset, with a dashboard or a big data framework | Project group | 40 % |
| Lastenheft and Pflichtenheft for your partner project | Project group | 15 % |

::: callout
Every task has a **dedicated kickoff** in class and a **fixed hand-in**. Notebooks: hand-in **two weeks after the kickoff**.
:::

::: notes
The 45/40/15 split is the one agreed on 2026-10-07; the 15 % of the dropped research brief go to the Lastenheft and Pflichtenheft. Equal weights of the three notebooks (15 % each) — confirm before showing. The DHBW study and examination regulations on portfolios still apply (late hand-ins, illness, plagiarism); point students to them rather than inventing rules on the slide.
:::

---

# Four Groups, Two Group Tasks

Each group works on **both** group tasks: the Lastenheft and Pflichtenheft for the partner, and the case study.

| Group | Members |
|---|---|
| Project 1 | {{private:group_1|Group list on the course platform}} |
| Project 2 | {{private:group_2|Group list on the course platform}} |
| Project 3 | {{private:group_3|Group list on the course platform}} |
| Project 4 | {{private:group_4|Group list on the course platform}} |

::: callout
Same group, **different data**: the case study uses a public dataset, never partner data.
:::

::: notes
Names come from tools/local.json (gitignored) and appear only in the offline PPTX; the public web version shows the fallback text. Never write student names or e-mail addresses into this file. The lab notebooks are done in pairs, ideally within the same group.
:::

---

# Timeline: Kickoffs and Hand-ins

| Session | Kickoff | Hand-in |
|---|---|---|
| 1 · Introduction (today) | **Lastenheft and Pflichtenheft** | |
| 4 · Analytical SQL | **Notebook 1** | |
| 6 · Analytics portals | **Group case study** | Notebook 1 (session 4 + 2 weeks) |
| 8 · ML use-case lab | **Notebook 2** | Case study proposal (session 6 + 2 weeks) |
| 10 · Lab workshop | | Notebook 2 (session 8 + 2 weeks) · Lastenheft |
| 14 · Forecasting at scale | **Notebook 3** | Pflichtenheft (session 10 + 2 weeks) |
| 16–17 · Workshop and presentations | | Notebook 3 (session 14 + 2 weeks) · Case study |

::: notes
Hand-ins are listed in the row of the first session on or after the deadline; the exact dates depend on the timetable. The case study starts in session 6 on purpose: Part A is complete, the dashboard option (Streamlit) has just been taught, and groups have more than half of the semester — not only the last weeks before the exams. The case study proposal is short and only checked (go / adjust), not graded on its own.
:::

---

# How to Hand In

- Upload to the **course platform** by 23:59 on the hand-in day
- Notebooks: the `.ipynb` file **and** an HTML export, names of both partners at the top
- The notebook runs **top to bottom** on a fresh kernel; data are loaded by URL or script
- Every notebook ends with a short written **assessment of method suitability**
- Partner documents are **confidential**: never in public repositories or chats

::: source
Based on Sandve et al. (2013).
:::

::: notes
The suitability assessment is what the module description asks for ("assess the suitability" of methods); five to ten sentences are enough. Session 10 has full checklists for notebooks 1 and 2 and for reproducibility.
:::

---

# Lab Notebooks {.section}

Three notebooks in pairs · kickoff in class · hand-in two weeks later

---

# Notebook 1: Warehouse, OLAP and Analytical SQL

**Kickoff:** session 4 · **Hand-in:** session 4 + 2 weeks · builds on the labs of sessions 2–4

- **Data:** the TPC-H star schema in DuckDB from session 3
- Answer **business questions** with OLAP operations and analytical SQL: rankings, shares, running totals, cohorts or funnels
- State the **grain** of each fact table and **define every measure**: formula, filters, time reference
- Check **completeness**: incomplete periods excluded or marked
- **Interpret** every result table, then write the suitability assessment

::: callout
A query without an interpretation is not an answer.
:::

::: source
Own compilation based on Kimball and Ross (2013).
:::

::: notes
This is the checklist of session 10 turned into a brief. Session 2 is the first look at the warehouse, session 3 builds the star schema, session 4 adds window functions and ROLLUP/CUBE/GROUPING SETS — so the kickoff in session 4 comes when students have all methods. Charts from session 5 are welcome but not required. TPC-H is synthetic and almost flat: "there is no trend" is a valid, well-founded finding.
:::

---

# Notebook 2: Machine Learning Use Case

**Kickoff:** session 8 · **Hand-in:** session 8 + 2 weeks · builds on session 7

- **One** use case: churn prediction, customer segmentation or anomaly detection
- Data: the TPC-H star schema or a public dataset of the same depth
- From the business question to a **recommendation**: framing, features, baseline, model, evaluation, interpretation
- Features only from before the cut-off; the test period used **once**
- Judge the model in **business terms** — lift, profit, hits at capacity

::: callout
The question is not "which algorithm is best?" but "**does ML improve this decision — and how sure are we?**"
:::

::: source
Own compilation based on Chapman et al. (2000) and Provost and Fawcett (2013).
:::

::: notes
Full brief and suggested rubric: session 8 deck. The feature table from the session 7 lab is the starting point. Session 10 (lab workshop) falls inside the two weeks and gives time for consultations. A negative result ("a simple rule is enough") is not penalised if it is shown and argued well.
:::

---

# Notebook 3: Time Series Forecast

**Kickoff:** session 14 · **Hand-in:** session 14 + 2 weeks · builds on sessions 11–13

- **Track A — Energy demand:** the daily electricity series of sessions 11–13, 14 days ahead
- **Track B — Tourism demand:** many regional series, 8 quarters ahead, at all levels
- Or a public dataset of comparable depth, agreed with the lecturer
- Baselines first, rolling evaluation, at least one model beyond the baselines
- Uncertainty (A: prediction intervals) or coherence (B: reconciled forecasts)

::: callout
The question is not "which model is best?" but "**which forecast helps this decision — and how sure are we?**"
:::

::: source
Own compilation based on Hyndman and Athanasopoulos (2021).
:::

::: notes
Full brief: session 14 deck. Track A reuses the lab work of sessions 11–13; track B is new and closer to retail practice; both are equally valued. Students should keep their lab tables from sessions 12 and 13 — notebook 3 starts from them.
:::

---

# Group Case Study {.section}

End-to-end analytics on a public dataset

---

# Group Case Study: The Brief

**Kickoff:** session 6 · **Presentation and hand-in:** session 17

- Choose a **public dataset** and a **business decision** it can support
- Go end to end: question, data, approach, results, recommendation
- Include **one** of: a **dashboard** (session 6) or a **big data framework** (session 15) — with a reason for the choice
- Hand in a reproducible notebook (plus app or Spark code); present in session 17

::: callout
**No partner data.** The case study uses public data only: confidentiality, and no double assessment with the semester-6 project.
:::

::: source
Own compilation based on Chapman et al. (2000).
:::

::: notes
Groups: the four project groups formed in session 1 (the module handbook allows larger groups). The kickoff in session 6 is deliberate: groups have more than half of the semester and are not squeezed into the exam period. Datasets must be public with a licence that allows the use; groups load them by URL or script. Tool choice is part of the assessment: "DuckDB was enough — here is the measurement" is as good as a justified Spark pipeline.
:::

---

# Group Case Study: Milestones

| When | Milestone |
|---|---|
| Session 6 | **Kickoff:** in your project group, collect dataset ideas |
| Session 6 + 2 weeks | **Proposal** (one page): question, decision, dataset, planned dashboard or big data part |
| Session 10 | **Consultation** on the proposal and first results |
| Session 15 | Spark material for the big data option |
| Session 16 | **Workshop:** review checklists, feedback between groups, presentation storyboard |
| Session 17 | **Presentation** and hand-in of the notebook |

::: notes
The proposal is checked (go / adjust within a week), not graded. It forces an early decision on the dataset — the most common reason for late trouble. Session 16 contains the review checklists for approach, results and dashboard; groups should arrive with a working notebook, not a plan.
:::

---

# Lastenheft and Pflichtenheft {.section}

Getting your partner project ready for semester 6

---

# Why Write Them Now?

- In semester 6 the partner project has only a few plenary meetings — the team must be able to **start on day one**
- Requirements that are unclear at the start are the most expensive ones later
- Two documents, two perspectives:

::: cards
### Lastenheft
**What and why.** The partner's requirements: goals, users, data, constraints — confirmed by the partner.

### Pflichtenheft
**How.** Your answer: how your team will meet the requirements in semester 6, with what data, methods and plan.
:::

::: source
Based on DIN 69901-5 (2009) and VDI 2519 Blatt 1 (2001).
:::

::: notes
DIN 69901-5 defines the Lastenheft as the client's requirements for the deliverables and services of a project, and the Pflichtenheft as the contractor's implementation proposals based on the Lastenheft. In practice the client often does not write a Lastenheft for an analytics project: here the groups draft it from interviews with the partner, and the partner confirms it. English equivalents: requirements specification (Lastenheft) and functional or solution specification (Pflichtenheft).
:::

---

# Lastenheft: What It Contains

1. **Background:** the company, the business problem, the current process (as-is)
2. **Goals and success criteria:** which decision improves, measured how
3. **Stakeholders and users:** who uses the result, who decides
4. **Requirements:** functional and non-functional, each prioritised as must, should or could
5. **Data:** sources, systems, volume, quality, access, confidentiality
6. **Constraints:** technology, data protection, time, budget
7. **Expected deliverables** and open questions

::: source
Based on VDI 2519 Blatt 1 (2001) and Chapman et al. (2000, business understanding).
:::

::: notes
The questions from the partner pitches in session 1 ("Questions to Ask the Partners") are the starting point. Each requirement should be testable: "the dashboard is fast" is not a requirement, "the daily report is available by 8:00" is. The Lastenheft is presented in session 10 together with the first findings, and the partner confirms it.
:::

---

# Pflichtenheft: What It Contains

1. **Starting point:** reference to the Lastenheft; scope — what is in and what is out
2. **Solution concept:** data pipeline, storage, analytics methods, outputs such as a dashboard or a model
3. **Data plan:** access, preparation, data protection, test data
4. **Acceptance criteria:** how partner and team check that a requirement is met
5. **Project plan for semester 6:** milestones aligned with kickoff, mid-term and final presentation; roles in the team
6. **Risks and assumptions**, each with a countermeasure

::: callout
Every requirement in the Lastenheft is **traced** to a part of the solution — or explicitly marked as out of scope.
:::

::: source
Based on DIN 69901-5 (2009) and VDI 2519 Blatt 1 (2001).
:::

::: notes
The solution concept uses what students learn in this module: warehouse and analytical SQL (Part A), ML use cases (Part B), time series (Part C), Spark and dashboards (Part D). A traceability table (requirement → solution part → acceptance criterion) is the simplest way to show completeness.
:::

---

# Lastenheft and Pflichtenheft: Milestones

| When | Milestone |
|---|---|
| Session 1 (today) | **Kickoff:** partner pitch, four project groups, first questions |
| Sessions 2–9 | Interviews with the partner; draft the Lastenheft |
| Session 10 | **Hand-in Lastenheft** (confirmed by the partner), presented with the first findings |
| Session 10 + 2 weeks | **Hand-in Pflichtenheft** |
| Semester 6 | Kickoff of the project: start from the Pflichtenheft |

::: callout
Partner information is **confidential**: no names, data or documents in public repositories or chats.
:::

::: notes
The Pflichtenheft hand-in lies in the middle of the semester, well before the exam period. The Lastenheft and Pflichtenheft replace the ungraded "project brief" of the session 1 deck. Agree a contact person and an interview schedule with the partner today. Both documents are graded together (15 %); a suggested split is Lastenheft 40 % and Pflichtenheft 60 %, to be confirmed in the official brief.
:::

---

# Key Takeaways

- **Three notebooks** in pairs: kickoff in sessions **4, 8 and 14**, hand-in **two weeks** later
- **Four project groups** do both group tasks: case study and Lastenheft and Pflichtenheft
- **Group case study:** kickoff in session **6**, proposal two weeks later, presentation in session **17**
- **Lastenheft and Pflichtenheft:** kickoff **today**, Lastenheft in session **10**, Pflichtenheft two weeks later
- Every notebook ends with an **assessment of method suitability**
- Exact dates and the rubrics are on the **course platform**

::: notes
Open the floor for questions. Typical questions: Can we choose our own pairs? (yes, keep the same pair for all three notebooks if possible) · Is the case study group the same as the project group? (yes; the datasets must differ — public data only) · What if a pair splits up? (talk to the lecturer early).
:::

---

# References {.references}

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS.
- Deutsches Institut für Normung. (2009). *Projektmanagement – Projektmanagementsysteme – Teil 5: Begriffe* (DIN 69901-5:2009-01). Beuth.
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and practice* (3rd ed.). OTexts. https://otexts.com/fpp3/
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Provost, F., & Fawcett, T. (2013). *Data science for business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). Ten simple rules for reproducible computational research. *PLoS Computational Biology, 9*(10), Article e1003285. https://doi.org/10.1371/journal.pcbi.1003285
- Verein Deutscher Ingenieure. (2001). *Vorgehensweise bei der Erstellung von Lasten-/Pflichtenheften* (VDI 2519 Blatt 1). Beuth.
