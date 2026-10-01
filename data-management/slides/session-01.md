---
course: Data Management
session: 1
title: Why Data Matters
subtitle: Course introduction · value of data · key terms
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Why Data Matters {.title}

::: notes
Welcome. Introduce yourself briefly (background, why data matters in your own work).
Time plan for today (3 h): course intro 20 min · warm-up 15 min · value of data 25 min · break 10 min · key terms 40 min · group exercise 50 min · wrap-up 10 min · ~10 min buffer.
:::

---

# Today's Agenda

1. Welcome and course overview
2. Warm-up: where do you meet data?
3. Why data matters for organisations and society
4. Key terms: Data Management, BI, Business Analytics, Data Science, Big Data
5. Group exercise: a data-driven business case
6. Wrap-up and outlook

::: notes
Time and format guide (not shown to students):
0:00 Welcome and course overview (input) · 0:20 Warm-up (pair discussion) · 0:35 Why data matters (input + discussion) · 1:00 Break · 1:10 Key terms (input + quiz) · 1:50 Group exercise (team work + pitches) · 2:40 Wrap-up (input) · ~10 min buffer.
Times are a guide, not a contract. If the warm-up or the value-of-data discussion runs long, shorten the key-terms input (the comparison slide is enough) and keep the group exercise — it is the most important part of today.
:::

---

# What You Will Be Able to Do After This Module

- **Distinguish** types of data (structured, semi-structured, unstructured) and choose suitable data structures
- **Model** business situations as entity-relationship models and design simple relational databases
- **Write SQL** to define, extract, filter and aggregate data
- **Compare** relational and NoSQL databases, data warehouses and data lakes
- **Assess and improve** data quality; load and prepare data with Python
- **Reflect** on legal and organisational conditions for using data

::: source
Based on the module description *Data Management*, DHBW, Digital Business Management.
:::

::: notes
Paraphrased from the official module description (MODULE.md). Point out that the module combines conceptual work (modelling), technical skills (SQL, Python) and business judgement (is this data suitable and allowed for this question?).
:::

---

# Course Roadmap: 20 Sessions in Four Parts

| Part | Sessions | Topics |
|---|---|---|
| A · Foundations | 1–6 | Key terms, data types, ER modelling, relational model, normalisation |
| B · SQL and databases | 7–12 | SQL (DDL, DML, joins, aggregation), NoSQL, project workshop |
| C · Data quality and data access | 13–16 | Data quality, data cleaning in Python, files and APIs, ETL |
| D · Storage systems and access to data | 17–20 | Data warehouse, data lake and lakehouse, legal and organisational aspects, presentations and exam Q&A |

::: notes
Session 12 is a buffer: no new content, time for catching up and project consultations. Session 20: project presentations (2 h) and exam Q&A (1 h).
:::

---

# How We Work

::: cards
### Input and practice
Each 3-hour block mixes short input with hands-on work, discussion and time for questions.

### Core and optional slides
Core slides are exam-relevant. Slides marked **Optional · Self-study** are for deeper reading.

### Tools
SQLite and Jupyter notebooks run on Windows and macOS. We set them up together in session 2.

### Questions welcome
Discussion is part of the course. If a topic needs more time, we take it.
:::

::: notes
Make the core/optional rule explicit: optional slides are never exam-relevant unless covered in class. Ask students to bring a laptop from session 2 on.
:::

---

# Assessment

::: columns
**Written exam**

- Concepts, modelling and SQL
- Exam-style questions in the sessions and in the final Q&A
|||
**Design project (team work)**

- Design and build a small database for a business case
- Load, clean and query real data
- Kick-off in session 4, presentations in session 20
:::

::: callout
The weighting between exam and project will be announced before the project kick-off.
:::

::: notes
Weighting is not yet decided (status 2026-10). Update this slide once it is fixed.
:::

---

# Core Literature

| Topic | Book |
|---|---|
| Data management overview | Gronwald (2024); Strengholt (2023) |
| Data modelling | Gadatsch (2019); Staud (2005) |
| Data quality | Hildebrand et al. (2025) |
| SQL | Tanimura (2021) |
| Python and data preparation | McKinney (2022) |
| Data architectures | Serra (2024) |

Full references at the end of this deck. Most titles are available as e-books via the DHBW library.

::: notes
Check e-book availability in the DHBW library before the first lecture and adjust the last sentence if needed. McKinney is also available in German (Datenanalyse mit Python, 3rd ed., 2023) and as a free online edition from the author.
:::

---

# Warm-up: Where Do You Meet Data? {.exercise}

**Think – pair – share**

1. **Think:** List five situations from the last 24 hours in which data about you was created or used.
2. **Pair:** Compare with your neighbour. Who collected the data? What was it used for?
3. **Share:** Which example surprised you most? Which one creates value — and for whom?

::: notes
Timing guide: 15 min in total — think 3 min, pair 5 min, share 7 min.
Typical answers: smartphone location, payments, public transport ticket, streaming recommendations, smart watch, employer systems (time tracking, SAP), university systems. Collect 4–5 examples on the whiteboard and keep them: they are reused when the terms are introduced (which examples are BI, analytics, data science?).
:::

---

# Why Data Matters {.section}

Value for organisations and for society

---

# How Data Creates Value for Organisations

::: cards
### Better decisions
Facts instead of gut feeling: reporting, forecasting, planning.

### Efficient operations
Automated, data-driven processes, e.g. inventory, logistics, maintenance.

### New products and services
Personalisation, recommendations, data-based services and business models.

### Compliance and risk
Trustworthy data for reporting duties, audits and risk management.
:::

::: notes
Ask students to map their warm-up examples to these four categories. Use examples from the students' training companies where possible (dual study!).
:::

---

# Evidence: Data-Driven Decisions Pay Off

::: callout
In a study of 179 large publicly traded US firms, companies that make decisions based on data and analytics showed **5–6 % higher output and productivity** than expected from their other investments and IT use.
:::

- The effect also appeared in asset utilisation, return on equity and market value
- Important: this is a statistical association, measured after controlling for IT investment — not a guarantee for every company

::: source
Brynjolfsson, Hitt and Kim (2011).
:::

::: notes
Use this to practise critical reading: what does "associated with" mean? Could successful firms simply be the ones that can afford analytics (reverse causality)? The authors tested for this with instrumental variables and found no evidence that the effect is due to reverse causality — but a single study is still a single study.
:::

---

# Data Matters for Society, Too

- **Public interest:** health research, mobility, climate and energy rely on shared data
- **European approach:** the EU aims for a single market for data with common European *data spaces*, in line with European values and fundamental rights
- **Follow-up laws:** Data Governance Act and Data Act (see session 19)
- **Risks:** privacy, discrimination through biased data, concentration of data power in few companies

::: source
European Commission (2020).
:::

::: notes
Short discussion question: "Should a car manufacturer have to share the data your car produces with you and with independent repair shops?" — this is exactly what the Data Act regulates (session 19). Do not go into legal detail today.
:::

---

# Data Alone Is Not Value

Data only creates value if it is:

- **Available** — people can find and access it
- **Fit for purpose** — correct, complete and up to date for the question at hand
- **Understood** — its meaning and origin are documented
- **Allowed to be used** — legally and ethically
- **Protected** — against loss and misuse

::: callout
Making this happen systematically is the job of **Data Management** — the topic of this module.
:::

::: notes
Bridge to the definitions. Each bullet maps to later sessions: availability (storage, sessions 17–18), fitness (data quality, 13–14), understanding (modelling, 3–6), legal use (19), protection (19).
:::

---

# Key Terms {.section}

Data Management · Business Intelligence · Business Analytics · Data Science · Big Data

---

# Data Management

::: callout
"Data Management is the development, execution, and supervision of plans, policies, programs, and practices that deliver, control, protect, and enhance the value of data and information assets throughout their lifecycles."
:::

- Data is treated as an **asset**, like money or machines
- It covers the **whole lifecycle**: create, store, use, share, archive, delete
- It is both a **business** and a **technical** responsibility

::: source
DAMA International (2017, Chapter 1).
:::

::: notes
DAMA-DMBOK is the reference framework of the data management profession. A revised 2nd edition appeared in 2024 with corrections; the definition is unchanged on DAMA's website. Verify page number in the library copy before quoting in written material.
:::

---

# DAMA: Eleven Knowledge Areas — and Where We Cover Them

| Knowledge area | Session(s) |
|---|---|
| Data Governance (at the centre of all others) | 19 |
| Data Architecture | 18 |
| Data Modeling and Design | 3–6 |
| Data Storage and Operations | 7–11 |
| Data Security | 19 |
| Data Integration and Interoperability | 15–16 |
| Document and Content Management | 2, 11 |
| Reference and Master Data | 13 |
| Data Warehousing and Business Intelligence | 17 |
| Metadata | 2, 18 |
| Data Quality | 13–14 |

::: source
Knowledge areas from DAMA International (2017); mapping to sessions: own illustration.
:::

::: notes
Do not explain each area now — this is a map for the whole course. Point out that governance is at the centre: without clear responsibilities, the technical areas do not work.
:::

---

# Business Intelligence (BI)

- Techniques, technologies, systems and practices that **analyse critical business data** so that a company understands its business and market better and makes **timely decisions**
- Classic BI focuses on **structured, internal data** in relational databases and data warehouses
- Typical outputs: **reports, dashboards, OLAP analyses, KPIs**
- Key question: *What happened — and where do we stand?*

::: source
Chen, Chiang and Storey (2012).
:::

::: notes
Chen et al. use the combined term "business intelligence and analytics" (BI&A) and describe its evolution from BI&A 1.0 (structured data in relational systems) via 2.0 (web data) to 3.0 (mobile and sensor data). Example: monthly sales dashboard by region in SAP Analytics Cloud or Power BI.
:::

---

# Business Analytics

All methods that turn data into **actionable insight** for better and faster decisions. A common classification:

::: layers
- Prescriptive: What should we do? — optimisation, simulation, decision support
- Predictive: What will happen? — forecasting, statistical models, machine learning
- Diagnostic: Why did it happen? — drill-down, correlation, root-cause analysis
- Descriptive: What happened? — reports, dashboards (BI)
:::

::: source
Based on Delen and Ram (2018).
:::

::: notes
Read the diagram bottom-up: value and difficulty increase towards the top. Descriptive analytics overlaps with classic BI, which is why the terms are often combined. Ask: at which level are the warm-up examples? (Streaming recommendation = predictive; route planning = prescriptive.)
:::

---

# Data Science

- Data science is the **set of fundamental principles** that guide the extraction of knowledge from data
- It connects **data-processing technologies** (including Big Data technologies) with **data-driven decision making**
- Combines statistics, computer science and domain knowledge
- Typical work: exploratory analysis, building and evaluating predictive models, experiments

::: source
Provost and Fawcett (2013).
:::

::: notes
Provost and Fawcett argue that the term risks becoming a buzzword if it is not distinguished from neighbouring terms — which is exactly what we do today. Data science overlaps with predictive and prescriptive analytics; the difference is mostly in emphasis (methods and scientific approach vs. business application).
:::

---

# Big Data

::: cards
### Volume
Amounts of data too large for traditional systems.

### Velocity
Data that arrives fast and must be processed quickly, e.g. streams.

### Variety
Many formats: tables, text, images, sensor data.
:::

Later additions include **veracity** (uncertain reliability), **variability** (changing data flow rates) and **value** (low value density until the data is analysed).

::: source
Three Vs: Laney (2001); further Vs: Gandomi and Haider (2015).
:::

::: notes
Laney wrote about the three dimensions in 2001 as a challenge for data management — the term "Big Data" became popular only later. Gandomi and Haider point out that the additional Vs were introduced by vendors (IBM, SAS, Oracle). Big Data describes characteristics of data, not a method: BI, analytics and data science can all work on big data.
:::

---

# How the Terms Fit Together

::: layers
- Business value: Better decisions, efficient processes, new products
- BI, Business Analytics, Data Science: Turn data into insight — from "what happened?" to "what should we do?"
- Data Management: Makes data available, trustworthy, understood, compliant and secure
- Data (incl. Big Data): Structured, semi-structured, unstructured — at any volume, velocity and variety
:::

::: source
Own illustration based on DAMA International (2017), Chen et al. (2012) and Provost and Fawcett (2013).
:::

::: notes
Key message of the session: analytics and data science stand on the foundation of data management. "Garbage in, garbage out" — without good data management, the upper layers fail.
:::

---

# Comparison at a Glance

| Term | Key question | Typical methods and tools |
|---|---|---|
| Data Management | Is our data available, correct, secure and allowed to be used? | Data models, databases, governance, quality rules |
| Business Intelligence | What happened? Where do we stand? | Data warehouse, reports, dashboards, OLAP |
| Business Analytics | Why? What will happen? What should we do? | Statistics, forecasting, optimisation |
| Data Science | What can we learn from data? | Exploratory analysis, machine learning, experiments |
| Big Data | — (describes the data itself) | Distributed storage and processing, streaming |

::: source
Own summary of the preceding slides.
:::

---

# Quick Check: Which Term Fits? {.exercise}

1. A retailer shows weekly sales per store on a dashboard.
2. A bank defines who is responsible for the correctness of customer addresses.
3. An energy supplier forecasts tomorrow's electricity demand.
4. A streaming service processes millions of play events per minute.
5. An airline calculates the best prices for each seat to maximise revenue.

::: notes
Answers: 1 BI / descriptive analytics · 2 Data management (data governance, data quality) · 3 Predictive analytics / data science · 4 Big Data (velocity, volume) · 5 Prescriptive analytics (revenue management). Discuss borderline cases — several answers can be defended, which shows the terms overlap.
:::

---

# Group Exercise: A Data-Driven Business Case {.exercise}

**Teams of 4–5 · short pitch per team at the end**

Choose a company — ideally one of your training companies — and answer:

1. Which **business question** should data help to answer?
2. Which **data** do you need? Where is it today (system, department, external)?
3. Is this BI, business analytics or data science? Why?
4. What could go wrong: **quality, legal, organisational**?
5. What is the **value** if it works?

::: callout
Do not share confidential information about your company. Generalise where necessary.
:::

::: notes
Timing guide: about 35 min team work + 3 min pitch per team (50 min in total).
Walk around and help teams sharpen their business question — it should be specific ("reduce late deliveries in region South"), not generic ("use AI"). Keep track of good cases: they can become design project cases in session 4. If time is short, let only 3–4 teams pitch and collect the rest in writing.
:::

---

# Critical Perspectives on Big Data {.optional}

- More data does not automatically mean better knowledge — size cannot replace good questions and sound methods
- Large datasets can still be biased or unrepresentative
- Access to big data is unequal, which creates new divides between those who have data and those who do not
- Ethical questions: just because data is accessible does not make its use ethical

::: source
boyd and Crawford (2012).
:::

::: notes
Self-study reading for interested students. Good preparation for session 19 (legal and organisational aspects).
:::

---

# Key Takeaways

- Data creates value through better decisions, efficient operations, new products and reliable compliance — but only if it is managed
- **Data Management** is the foundation: it makes data available, trustworthy, understood, compliant and secure
- **BI** looks at what happened; **business analytics** also asks why, what will happen and what to do; **data science** extracts knowledge from data with scientific methods
- **Big Data** describes data characteristics (volume, velocity, variety …), not a method

---

# Next Session: Data Types and Data Management Fundamentals

- Structured, semi-structured and unstructured data
- From data to information to knowledge
- **Tool setup:** Python, Jupyter and SQLite on your laptop

::: callout
**Preparation:** bring your laptop (Windows or macOS). Installation instructions will be published on the course page before the session.
:::

::: notes
Setup guide still to be written (part of the session 2 build).
:::

---

# References {.references}

- boyd, d., & Crawford, K. (2012). Critical questions for big data: Provocations for a cultural, technological, and scholarly phenomenon. *Information, Communication & Society, 15*(5), 662–679. https://doi.org/10.1080/1369118X.2012.678878
- Brynjolfsson, E., Hitt, L. M., & Kim, H. H. (2011). *Strength in numbers: How does data-driven decisionmaking affect firm performance?* SSRN. https://doi.org/10.2139/ssrn.1819486
- Chen, H., Chiang, R. H. L., & Storey, V. C. (2012). Business intelligence and analytics: From big data to big impact. *MIS Quarterly, 36*(4), 1165–1188. https://doi.org/10.2307/41703503
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Delen, D., & Ram, S. (2018). Research challenges and opportunities in business analytics. *Journal of Business Analytics, 1*(1), 2–12. https://doi.org/10.1080/2573234X.2018.1507324
- European Commission. (2020). *A European strategy for data* (COM(2020) 66 final). https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52020DC0066
- Gandomi, A., & Haider, M. (2015). Beyond the hype: Big data concepts, methods, and analytics. *International Journal of Information Management, 35*(2), 137–144. https://doi.org/10.1016/j.ijinfomgt.2014.10.007
- Laney, D. (2001). *3D data management: Controlling data volume, velocity, and variety* (Application Delivery Strategies, File 949). META Group.
- Provost, F., & Fawcett, T. (2013). Data science and its relationship to big data and data-driven decision making. *Big Data, 1*(1), 51–59. https://doi.org/10.1089/big.2013.1508

---

# References: Module Literature {.references}

- Gadatsch, A. (2019). *Datenmodellierung: Einführung in die Entity-Relationship-Modellierung und das Relationenmodell* (2nd ed.). Springer Vieweg. https://doi.org/10.1007/978-3-658-25730-9
- Gronwald, K.-D. (2024). *Data Management: Der Weg zum datengetriebenen Unternehmen*. Springer Vieweg. https://doi.org/10.1007/978-3-662-68668-3
- Hildebrand, K., Mielke, M., & Gebauer, M. (Eds.). (2025). *Daten- und Informationsqualität: Die Grundlage der Digitalisierung* (6th ed.). Springer Vieweg. https://doi.org/10.1007/978-3-658-47317-4
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
- Staud, J. L. (2005). *Datenmodellierung und Datenbankentwurf: Ein Vergleich aktueller Methoden*. Springer. https://doi.org/10.1007/b137949
- Strengholt, P. (2023). *Data management at scale: Modern data architecture with data mesh and data fabric* (2nd ed.). O'Reilly Media.
- Tanimura, C. (2021). *SQL for data analysis: Advanced techniques for transforming data into insights*. O'Reilly Media.
