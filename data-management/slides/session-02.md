---
course: Data Management
session: 2
title: Data Types and Data Management Fundamentals
subtitle: Structured, semi-structured and unstructured data · data, information, knowledge · tool setup
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Data Types and Data Management Fundamentals {.title}

::: notes
Time plan for today (3 h): recap 10 min · data, information, knowledge 25 min · types of data 35 min · break 10 min · classification exercise 25 min · metadata and lifecycle 20 min · tool setup 45 min · wrap-up 5 min · ~5 min buffer.
The tool setup takes longer than planned in most groups. If it does, move the optional slides to self-study and shorten the metadata part — every student must leave with a working setup.
:::

---

# Today's Agenda

1. Recap: key terms from session 1
2. Data, information, knowledge
3. Structured, semi-structured and unstructured data
4. Exercise: classify datasets
5. Metadata and the data lifecycle
6. Tool setup: Python, Jupyter and SQLite

::: notes
Time and format guide (not shown to students):
0:00 Recap (quiz) · 0:10 Data, information, knowledge (input + discussion) · 0:35 Types of data (input) · 1:10 Break · 1:20 Classification exercise (pairs) · 1:45 Metadata and lifecycle (input) · 2:05 Tool setup (hands-on, everyone) · 2:50 Wrap-up.
Ask students who already have Python installed to help their neighbours during the setup.
:::

---

# Recap: Which Term Fits?

- Defining who is responsible for the quality of customer data → ?
- A dashboard with weekly sales per store → ?
- Forecasting next month's demand with a statistical model → ?
- Processing millions of sensor readings per second → ?

::: notes
Answers: data management (data governance) · business intelligence / descriptive analytics · predictive analytics / data science · big data (velocity, volume). Keep it short — it is a warm-up.
:::

---

# Data, Information, Knowledge {.section}

What exactly do we manage?

---

# From Data to Wisdom

::: layers
- Wisdom: Judgement — knowing what to do and why
- Knowledge: Information combined with experience and context — knowing how
- Information: Data with meaning in a context — answers who, what, where, when
- Data: Symbols, facts and figures without context
:::

::: source
Based on Ackoff (1989) and Rowley (2007).
:::

::: notes
The data–information–knowledge–wisdom (DIKW) hierarchy goes back to Ackoff (1989). Rowley (2007) reviewed how textbooks define the levels and found broad agreement on the order but many different definitions. Example: "23" (data) → "23 °C in the server room at 14:00" (information) → "above 27 °C the servers shut down, so we have a margin of 4 °C" (knowledge) → "install a second cooling unit before summer" (wisdom/decision).
:::

---

# Why the Distinction Matters

- The **same data** can carry different information in different contexts: "1" can be a quantity, a flag or a customer ID
- Data only becomes information if its **meaning is documented** — this is the job of metadata and data models
- Organisations value information and knowledge, but they **manage data** — the layer everything else builds on

::: callout
Data management makes data **interpretable**: what does it mean, where does it come from, and how reliable is it?
:::

::: source
Own summary based on Rowley (2007) and DAMA International (2017).
:::

::: notes
Critical note for interested students: the DIKW pyramid is useful for teaching but is criticised as too simple — knowledge is not just "more processed" information. Rowley discusses this.
:::

---

# Types of Data {.section}

Structured · semi-structured · unstructured

---

# Three Types of Data

::: cards
### Structured
Fixed schema defined in advance: rows and columns with defined data types. Example: customer table in an ERP system.

### Semi-structured
Self-describing: tags or keys mark the elements, but the structure can vary from record to record. Example: JSON from a web API, XML invoices.

### Unstructured
No predefined data model. Example: e-mails, PDFs, images, audio, video, social media posts.
:::

::: source
Based on Abiteboul (1997) and Gandomi and Haider (2015).
:::

::: notes
Abiteboul characterises semi-structured data as data whose structure is irregular, implicit or only partially known, and which is often self-describing. Unstructured does not mean "no structure at all" — an image has pixels, a text has sentences — but no data model that a database can use directly.
:::

---

# The Same Order in Three Forms

::: columns
**Structured (table)**

| order_id | customer | amount |
|---|---|---|
| 4711 | C-102 | 249.90 |
|||
**Semi-structured (JSON)**

```json
{"order_id": 4711,
 "customer": "C-102",
 "items": [{"sku": "A-7", "qty": 2}],
 "amount": 249.90}
```
:::

**Unstructured (e-mail):** "Hi, I'd like to order two of the A-7 lamps again, same address as last time. Thanks, Anna"

::: source
Own example.
:::

::: notes
Point out: the JSON can hold a variable number of items without changing a schema; the e-mail contains the same information, but a human (or NLP) has to extract it. Ask: which form is easiest to analyse? Which is easiest to create for a customer?
:::

---

# Comparison at a Glance

| | Structured | Semi-structured | Unstructured |
|---|---|---|---|
| Schema | Fixed, defined before storing | Flexible, part of the data | None |
| Typical formats | Relational tables, CSV | JSON, XML, YAML | Text, PDF, images, audio, video |
| Typical storage | Relational database, data warehouse | Document database, data lake | File system, object storage, data lake |
| Query and analysis | SQL | JSON/XML queries, SQL extensions | Search, NLP, computer vision |
| In this module | Sessions 3–10, 17 | Sessions 11, 15 | Session 18 |

::: source
Own summary based on Gandomi and Haider (2015) and DAMA International (2017).
:::

::: notes
The session column shows students where each type comes back. The design project focuses on structured data, but API data (semi-structured) is loaded in sessions 15–16.
:::

---

# How Much of the World's Data Is Unstructured?

- Often quoted: **most** of the data in organisations is unstructured
- Gandomi and Haider quote an estimate by Cukier that structured data makes up only about **5 %** of all existing data
- Such figures are **estimates** that are hard to verify — treat them with care

::: callout
For business decisions, structured data from operational systems is still the most important source — but the value of unstructured data grows with AI methods.
:::

::: source
Cukier (2010, as cited in Gandomi and Haider, 2015).
:::

::: notes
Good moment to practise source criticism: the 5 % figure is a second-hand estimate (Gandomi and Haider take it from a 2010 magazine report by Cukier), and the frequently quoted "80 % unstructured" figure has no clear original study. APA rule: if you have not read the original, cite it "as cited in" the source you read. Ask students how they would check such a claim.
:::

---

# Exercise: Classify the Data {.exercise}

Work in pairs. Is the data structured, semi-structured or unstructured? Where would you store it?

1. A CSV export of all invoices from the accounting system
2. Weather data from a public web API in JSON format
3. Scanned delivery notes from suppliers (PDF)
4. Product master data in an SAP system
5. Customer reviews in an online shop
6. Log files of a web server
7. Photos of damaged goods taken by warehouse staff
8. An XML e-invoice (e.g. XRechnung)

::: notes
About 20 min + discussion. Answers: 1 structured · 2 semi-structured · 3 unstructured (becomes structured after OCR and extraction) · 4 structured · 5 unstructured text, often with structured parts (stars, date) · 6 semi-structured (fixed line pattern, but varying content) · 7 unstructured (with structured metadata: date, location, camera) · 8 semi-structured.
Key insight: many real datasets are mixed. Ask for the storage choice — prepares sessions 11 (NoSQL) and 18 (data lake).
:::

---

# Metadata and the Data Lifecycle {.section}

Data about data · from creation to deletion

---

# Metadata: Data About Data

::: cards
### Business metadata
Meaning and rules: definitions, business terms, owner. Example: "Revenue = net sales after returns".

### Technical metadata
Structure and storage: tables, columns, data types, formats, lineage.

### Operational metadata
Processing: load times, number of records, errors, access logs.
:::

::: source
Based on DAMA International (2017).
:::

::: notes
Without metadata, data cannot be found, understood or trusted. Link to the photo example in the exercise: the image itself is unstructured, but its metadata (date, location, camera) is structured and can be queried. Metadata management is one of the eleven DAMA knowledge areas (session 1).
:::

---

# The Data Lifecycle

::: layers
- Plan: Which data do we need, for what purpose, under which rules?
- Create or acquire: Capture in processes, import from partners, buy, collect from APIs
- Store and maintain: Databases, files, backups, quality checks
- Use and share: Processes, reports, analytics, exchange with partners
- Archive and delete: Retention periods, legal obligations, secure deletion
:::

::: source
Own illustration based on DAMA International (2017).
:::

::: notes
Read top-down. Data management covers the whole lifecycle, not only storage. Deletion is often forgotten — but the GDPR requires that personal data is not kept longer than necessary (session 19). Ask: at which lifecycle stage do most data quality problems arise? (Usually at creation — garbage in, garbage out.)
:::

---

# Data Formats You Will Use in This Module {.optional}

| Format | Type | Typical use |
|---|---|---|
| CSV | Structured (text) | Exports, data exchange, open data |
| Excel (.xlsx) | Structured | Business users' data, small datasets |
| JSON | Semi-structured | Web APIs, configuration, document databases |
| XML | Semi-structured | E-invoices, B2B data exchange |
| SQLite (.db) | Structured (database file) | Our course database |
| Parquet | Structured (columnar, binary) | Data lakes and analytics at scale |

::: source
Own compilation based on McKinney (2022).
:::

::: notes
Self-study. Reading these formats with pandas is the topic of session 15.
:::

---

# Tool Setup {.section}

Python · Jupyter · SQLite

---

# Our Toolset

::: cards
### Python
A programming language widely used for data work. We use it to load, clean and analyse data.

### Jupyter
Notebooks that mix code, results and text — ideal for exercises and documentation.

### SQLite
A complete relational database in a single file. It is built into Python — no server, no installation.

### pandas
A Python library for tables ("DataFrames"); it can read CSV, Excel, JSON and SQL.
:::

::: source
McKinney (2022); SQLite (n.d.).
:::

::: notes
Why SQLite: it supports standard SQL for everything we need in sessions 7–10, runs on Windows and macOS, and the database is a single file students can submit with their design project. Limits (e.g. no user management, limited ALTER TABLE) are discussed in session 7.
:::

---

# Step 1: Install Python and Jupyter

1. Install **Python 3.12 or newer** from python.org
   - Windows: tick *Add python.exe to PATH* in the installer
   - macOS: use the installer from python.org; in the terminal, type `python3` instead of `python`
2. Open a terminal (Windows: *PowerShell*, macOS: *Terminal*) and install the packages:

```bash
python -m pip install jupyterlab pandas openpyxl
```

3. Start Jupyter:

```bash
python -m jupyter lab
```

::: notes
Common problems: "jupyter is not recognised" → that is why we start it with python -m jupyter lab (pip's Scripts folder is not always on the PATH). "python is not recognised" on Windows → PATH not set; reinstall with the tick or use the "py" launcher (py -m pip install ...). On macOS, "pip: command not found" → use python3 -m pip. Company laptops may block installations — students should use a private laptop or ask their IT department in advance. If Anaconda or VS Code with Jupyter is already installed, that is fine too.
:::

---

# Step 2: Test Your Setup

Create a new notebook and run this cell:

```python
import sqlite3
import pandas as pd

con = sqlite3.connect("test.db")
con.execute("CREATE TABLE IF NOT EXISTS hello (id INTEGER PRIMARY KEY, msg TEXT)")
con.execute("INSERT INTO hello (msg) VALUES ('Setup works!')")
con.commit()
print(pd.read_sql("SELECT * FROM hello", con))
print("SQLite version:", sqlite3.sqlite_version)
```

::: callout
If you see a small table with "Setup works!", you are ready for the rest of the module.
:::

::: notes
The cell creates a file test.db in the notebook's folder — show it in the file browser to make clear that the whole database is one file. Running the cell twice inserts a second row; a good moment to mention primary keys (session 5).
:::

---

# Optional: A Graphical Tool for SQLite {.optional}

- **DB Browser for SQLite** is a free, open-source tool to look at SQLite files: tables, data, and SQL queries
- Available for Windows and macOS from sqlitebrowser.org
- Helpful for checking your design project database — but all exercises can be done in Jupyter

::: notes
Self-study. Some students prefer a visual tool when they start with SQL.
:::

---

# Key Takeaways

- **Data** becomes **information** through context and meaning, and **knowledge** through experience — data management makes data interpretable
- Data is **structured** (fixed schema), **semi-structured** (self-describing, flexible) or **unstructured** (no data model) — and real datasets are often mixed
- **Metadata** describes the meaning, structure and processing of data
- Data management covers the **whole lifecycle**, from planning to deletion

---

# Next Session: Semantic Data Modelling I

- Why we model data before we build databases
- Entities, attributes, relationships and cardinalities
- Chen notation vs. crow's-foot notation

::: callout
**Preparation:** think of a small business you know (a sports club, a café, a bike shop). Which "things" would it need to store data about?
:::

---

# References {.references}

- Abiteboul, S. (1997). Querying semi-structured data. In F. Afrati & P. Kolaitis (Eds.), *Database Theory — ICDT '97* (Lecture Notes in Computer Science, Vol. 1186, pp. 1–18). Springer.
- Ackoff, R. L. (1989). From data to wisdom. *Journal of Applied Systems Analysis, 16*, 3–9.
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Gandomi, A., & Haider, M. (2015). Beyond the hype: Big data concepts, methods, and analytics. *International Journal of Information Management, 35*(2), 137–144. https://doi.org/10.1016/j.ijinfomgt.2014.10.007
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- Rowley, J. (2007). The wisdom hierarchy: Representations of the DIKW hierarchy. *Journal of Information Science, 33*(2), 163–180. https://doi.org/10.1177/0165551506070706
- SQLite. (n.d.). *About SQLite*. Retrieved October 7, 2026, from https://www.sqlite.org/about.html
