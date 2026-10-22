---
course: Data Management
session: 18
title: Modern Data Architectures
subtitle: Data lake · lakehouse · data mesh · data fabric · cloud data platforms · choosing an architecture
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Modern Data Architectures {.title}

::: notes
Time plan for today (3 h): recap 7 min · today's data 3 min · data lake: limits of the warehouse, definition, schema-on-read with the live demo 17 min · from lake to swamp, the catalogue 6 min · mini exercise warehouse or lake 8 min · break 10 min · lakehouse and medallion layers 13 min · data mesh 12 min · data fabric 6 min · mini exercise mesh or fabric 8 min · cloud data platforms 8 min · comparison and choosing an architecture 6 min · hands-on part 1: a mini lake for the bike shop 22 min · hands-on part 2: architecture case comparison 25 min · team step 10 min · wrap-up 5 min · ~14 min buffer.
Input is about 71 minutes, hands-on, exercises and discussion about 80 minutes. Priorities if time runs short: data lake vs. warehouse (schema-on-read vs. schema-on-write), the data swamp and the catalogue, the lakehouse idea (one copy, warehouse features on lake storage) with bronze/silver/gold, the four data mesh principles, data fabric as a metadata-driven layer, mesh vs. fabric, the three cloud service models and the criteria for choosing an architecture are the exam core. Product names (Databricks, Snowflake, Fabric, BigQuery …) are examples, not exam content. Today is an overview: Data Analytics (semester 5) and the DSKI project modules go deeper into platforms. If time is short, shorten hands-on part 1 to questions 1–4 but keep the case comparison: it is the transfer task of today.
How the results were produced: every SQL statement was run with SQLite 3.45.1 on a fresh database built from the new bikeshop-lake-catalog-session18.sql (a fictional catalogue of a small data lake: 24 files, 14 lineage links); the pandas demo was run with Python 3.13 and pandas 3.0.6 on the two saved Bright Sky files of session 15 (brightsky-mannheim-2026-10-05.json, brightsky-heidelberg-2026-09-28.json; DWD data, CC BY 4.0). No cloud service was used; the cloud slides contain no prices on purpose (they change too often).
:::

---

# Today's Agenda

1. Recap: what does not fit into the star schema?
2. The data lake — and how it becomes a swamp
3. The lakehouse: bronze, silver, gold
4. Data mesh and data fabric: architecture as an organisational question
5. Cloud data platforms
6. Hands-on: a mini lake for the bike shop and an architecture case comparison

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:07 Today's data (everyone) · 0:10 Data lake, schema-on-read (input, live demo in Jupyter) · 0:33 Mini exercise warehouse or lake (pairs) · 0:41 Break · 0:51 Lakehouse, medallion (input) · 1:04 Data mesh and data fabric (input, discussion) · 1:22 Mini exercise mesh or fabric (pairs) · 1:30 Cloud, choosing an architecture (input) · 1:44 Hands-on part 1 (pairs, each student on their own laptop) · 2:06 Hands-on part 2 (groups of 4, one case per group, short presentations) · 2:31 Team step (project teams) · 2:41 Wrap-up · buffer.
Live demo: copy the two weather files into a lake folder and read them with pandas without defining any table first — then show the six extra columns of the Heidelberg file. The "who defined this schema?" moment is the aha of the session.
:::

---

# Recap: Where Session 17 Left Us

- The **star schema** answers questions by day, product, salesperson and weather — fast and easy
- But it only holds what we **modelled in advance**: structured, cleaned, at a declared grain
- The preparation question: **photos of damaged bikes** and the **raw API responses** — into the star?
- Today: architectures for data that **does not fit** into a warehouse — and for organisations too big for **one** team

::: callout
**Your answer?** Photos have no columns, raw JSON changes its fields, and nobody knows yet which questions the shop will ask of them.
:::

::: source
Session 17 of this course; Kimball and Ross (2013, Chapter 1).
:::

::: notes
Collect two or three answers to the preparation question. Typical answers: "a BLOB column in the database" (possible for a few photos, but the warehouse is not built for files of several MB and cannot query their content), "a folder on the shop PC" (close to a data lake — but who finds the photo of job 504 in a year?), "not at all" (then the data is lost for later questions, e.g. training an image model for damage detection). Keep the answers on the board: the folder answer becomes the data lake in a few minutes, the "who finds it?" question becomes the catalogue. Remind: session 16 already kept the raw API response in raw_weather — a first landing zone.
:::

---

# Today's Data

| Source | Content | Used for |
|---|---|---|
| `brightsky-mannheim-2026-10-05.json` (session 15) | hourly weather, station Mannheim | a mini lake: schema-on-read |
| `brightsky-heidelberg-2026-09-28.json` (session 15) | hourly weather, station Heidelberg | the same, from a second station |
| `bikeshop-lake-catalog-session18.sql` | **new**: catalogue of the shop's lake, 24 files | metadata, swamp check, lineage |
| four architecture cases | **new**: on the exercise slide | case comparison |

::: source
Own example based on the bike shop case; catalogue fictional. Weather data: Deutscher Wetterdienst via de Maeyer (n.d.), CC BY 4.0.
:::

::: notes
Everyone checks now that the two Bright Sky files from session 15 are in their course folder (both are in the data folder next to worksheet 15). The catalogue script is independent of the other bike shop tables: it can go into bikeshop.db or a database of its own. Check after loading: lake_file 24 rows, lake_lineage 14 rows. The catalogue describes files (paths, sizes, owners) — the photos and clickstream files themselves are not in the course folder, only their metadata.
:::

---

# The Data Lake {.section}

Store everything first, decide later

---

# What Does Not Fit into the Warehouse?

| Data | Why the warehouse struggles |
|---|---|
| Damage photos, scanned invoices | **unstructured**: no columns to load |
| Raw API responses, app logs | **semi-structured**, fields change over time |
| Web shop clickstream: GBs per day | **volume**: expensive to model and store as tables |
| Data for machine learning | needs **raw detail**, not cleaned aggregates |
| Data with no question yet | the warehouse needs the **model before the load** |

::: callout
A **data lake** stores data of **any type** in its **raw, native format**, usually as files in cheap storage, and applies a structure only when the data is **read**.
:::

::: source
Based on Serra (2024, Chapter 5), Reis and Housley (2022, Chapter 3) and DAMA International (2017, Chapter 14).
:::

::: notes
Serra (2024, Chapter 5) explains that data lakes appeared because relational warehouses handle structured data well but struggle with semi-structured and unstructured data, large volumes and frequent ingestion. Reis and Housley (2022, Chapter 3) describe the data lake among the types of data architecture and how lakes and warehouses later converged. DAMA International (2017, Chapter 14, Big Data and Data Science) treats the lake as a storage environment for big data. Link to session 2: structured, semi-structured, unstructured — the warehouse covers mainly the first. Typical storage: object storage in the cloud (Amazon S3, Azure Data Lake Storage, Google Cloud Storage) or a Hadoop file system on premises — examples only.
:::

---

# Schema-on-Write vs. Schema-on-Read

| | Warehouse: schema-on-**write** | Lake: schema-on-**read** |
|---|---|---|
| Structure defined | **before** loading (`CREATE TABLE`) | **when reading**, by each reader |
| Wrong data | rejected at the door (constraints) | stored anyway — found later, or never |
| New source | model, table, ETL first | copy the file in — done |
| Typical users | business users, reports | data engineers, data scientists |
| Risk | slow to change | nobody knows what the data means |

- Sessions 7 and 11 met both: `CHECK` and `FOREIGN KEY` vs. "schemaless" JSON documents
- Schema-on-read does not remove the schema — it moves the work to **every reader**

::: source
Based on Serra (2024, Chapter 5) and Reis and Housley (2022, Chapter 3).
:::

::: notes
Link to session 11: "schemaless does not mean no structure — the structure moves into the application code." The same is true for the lake: the pandas code that reads a file *is* the schema. Ask: which approach did the session 16 pipeline use? → both: raw_weather kept the JSON body unchanged (schema-on-read, ELT), weather_daily had a CREATE TABLE with CHECK constraints (schema-on-write). Exam: be able to explain both with an example and name one advantage and one risk of each.
:::

---

# Schema-on-Read with pandas

```python
import json
from pathlib import Path
import pandas as pd

frames = []
for path in sorted(Path("lake").glob("bronze/brightsky/*/*.json")):
    with open(path, encoding="utf-8") as f:
        df = pd.json_normalize(json.load(f)["weather"])   # structure decided now
    df["station"] = path.parent.name                       # meaning from the folder name
    frames.append(df)
weather = pd.concat(frames, ignore_index=True)             # shape: (338, 16)
```

- 169 hourly records per station — but the Heidelberg file has **6 extra fields** (`fallback_source_ids.…`)
- They say that Heidelberg's temperature, sunshine, wind, humidity and cloud cover come from source **184401** — the Mannheim source of session 15
- No error, no warning: the reader must **notice** it

::: source
Own example; weather data: Deutscher Wetterdienst via de Maeyer (n.d.), CC BY 4.0.
:::

::: notes
All observed (pandas 3.0.6). Folder layout used: lake/bronze/brightsky/mannheim/2026-10-05.json and lake/bronze/brightsky/heidelberg/2026-09-28.json, copied with shutil.copy from the course folder. Mannheim rows have NaN in the six fallback columns; in the Heidelberg file the five fields temperature, sunshine, wind speed, relative humidity and cloud cover carry fallback source 184401 in all 169 records, condition in 12 records; Heidelberg's own source id is 128157. Read literally from the field names: the "Heidelberg" temperature was measured at the source used for Mannheim — so comparing the two towns' temperatures compares a station with itself. The file does not explain this; the API documentation and the person who fetched the file must. This is the lake's typical risk: easy to store, easy to misread. The code syntax is not exam content; the idea (structure decided at read time, by the reader) is.
:::

---

# From Data Lake to Data Swamp

- A lake without **metadata** becomes a **data swamp** (Inmon: a "garbage dump"): files nobody can find, trust or explain
- The cure is a **catalogue**: one entry per dataset with owner, description, source, format, date, licence, personal data, lineage

| File (bronze/workshop/photos/) | Owner | Description | Personal data |
|---|---|---|---|
| 2027-02-02_RIE420_01.jpg | Katrin Vogel | damage photo, repair job 504 | unknown |
| IMG_0412.jpg | — | — | unknown |

- Zones keep order: **raw** data is never changed; cleaned and modelled data live in their own zones

::: source
Based on Inmon (2016), DAMA International (2017, Chapter 12) and Serra (2024, Chapter 5); rows from bikeshop-lake-catalog-session18.sql.
:::

::: notes
Inmon (2016) is subtitled "Designing the data lake and avoiding the garbage dump": a lake without structure and context is useless for analysis. DAMA International (2017, Chapter 12) treats metadata management as a knowledge area of its own — the catalogue is metadata (session 2: data about data). Ask: what can the shop do with IMG_0412.jpg? → nothing reliable: no owner to ask, no job number, unknown whether a customer's face or a licence plate of a car in the background is on it (session 19: personal data). The hands-on uses this catalogue. The zones are the bridge to the lakehouse: bronze, silver, gold.
:::

---

# Mini Exercise: Warehouse, Lake — or Both? {.exercise}

Where should the bike shop keep each item? Give a reason.

1. Photos of damaged bikes, taken on the workshop tablet
2. The till's receipt lines for the monthly revenue report
3. Raw responses of the weather API
4. The web shop's clickstream: every page view, several GB per month
5. Scanned supplier invoices (PDF)
6. Training data for a model that predicts which bikes come back for repairs

**And:** the till supplier renames the column `Umsatz` to `Revenue`. Who notices it first — in the warehouse, in the lake?

::: notes
About 5 min in pairs, 3 min collection. Expected answers:
1 Lake (unstructured; keep with job number and owner in the catalogue; the job number can go into the warehouse as a reference). 2 Warehouse (structured, cleaned, the fact table of session 17) — the raw export also in the lake's raw zone. 3 Lake raw zone (or a landing table such as raw_weather): reprocess later; the daily values go into the warehouse. 4 Lake (volume, semi-structured; aggregates such as visits per day can go into the warehouse). 5 Lake (unstructured); the invoice amounts belong in the purchasing tables. 6 Both: raw detail from the lake (photos, repair history), cleaned features often from the warehouse.
Rename: warehouse — the ETL load fails at once (column not found, or NOT NULL violated): loud and early. Lake — the file is stored without complaint; the first reader whose code expects Umsatz gets an error or, worse, NaN in a report: silent and late. Good answers: both are fine if the pipeline checks the schema (session 16, checks).
:::

---

# The Lakehouse {.section}

Warehouse features on lake storage

---

# Three Generations of Architectures

![Three lanes. 1 Data warehouse: sources go through ETL into a warehouse with tables and star schemas, which feeds BI and reports. 2 Data lake plus warehouse: all sources are loaded as is into a data lake with files in any format and schema-on-read; ETL copies part of it into a warehouse for BI, while data science and machine learning read the lake directly; two copies, two technologies, ETL in between. 3 Lakehouse: all sources are loaded as is into lake storage with bronze, silver and gold layers and a transaction log that adds ACID transactions, schema enforcement and versions; BI and machine learning both read from it](img/arch-evolution.png){width=74%}

::: source
Own illustration based on Armbrust et al. (2021) and Serra (2024, Chapters 10 and 12).
:::

::: notes
Lane 2 is what Serra (2024, Chapter 10) calls the modern data warehouse: a lake and a relational warehouse side by side. Armbrust et al. (2021) criticise this two-tier architecture: data is copied twice, the warehouse is stale compared with the lake, the second system costs money, and machine learning tools cannot read the warehouse's proprietary format well. Their proposal, the lakehouse, keeps one copy in open file formats (e.g. Apache Parquet) in the lake and adds the warehouse features on top. Do not present the lanes as "old, older, new": many companies run lane 1 or 2 successfully, and a small shop does not need any of them in the cloud.
:::

---

# What Makes a Lake a Lakehouse?

- Data stays in **open file formats** in cheap lake storage — one copy for BI **and** machine learning
- A **table format** with a **transaction log** on top of the files adds warehouse features:
  - **ACID** transactions: no half-written tables (session 10)
  - **Schema enforcement**: a file that does not fit the table is rejected (schema-on-write, where wanted)
  - **Versions**: read the table as it was yesterday ("time travel")
- Examples: Delta Lake, Apache Iceberg, Apache Hudi; platforms such as Databricks or Microsoft Fabric

::: callout
Lakehouse = **data lake storage** + **warehouse management** — one platform instead of two.
:::

::: source
Based on Armbrust et al. (2021) and Serra (2024, Chapter 12).
:::

::: notes
Serra (2024, Chapter 12) stresses that Delta Lake "is not storage": the data stays as Parquet files in folders, and a transaction log records every change — the log is what turns the folder into a table with transactions. Armbrust et al. (2021) list what the lakehouse adds: transactions, versioning, schema enforcement, and performance features such as caching and indexing, so that SQL queries run directly on the lake. Link to session 10: the transaction log is the same idea as a database's log for atomicity and durability. Product names are examples; not exam content. Ask: what is still hard? → the platform is complex; skills; small data does not need it.
:::

---

# Bronze, Silver, Gold — You Built One Already

![Three zones for the bike shop. Bronze, raw, as received and never changed, sessions 15 and 16: raw_weather with the API JSON, price list S1 as CSV, price list S2 as Excel, the till export as CSV, damage photos as JPG. Arrow clean to Silver, cleaned, typed, validated and deduplicated, sessions 14 and 16: weather_daily, supplier_price, till_daily, sale_line. Arrow model to Gold, modelled, ready for reports and analysis, session 17: fact_sales, dim_date and dim_product, dim_weather, revenue by bike day. Quality and value rise from left to right; bronze can always be reprocessed](img/arch-medallion.png){width=86%}

- The **medallion** pattern: data moves through layers and gains quality — **gold** is often a star schema

::: source
Own illustration based on Databricks (n.d.) and Armbrust et al. (2021); tables from sessions 14–17.
:::

::: notes
Databricks (n.d.) describes the medallion architecture: bronze holds raw, unvalidated source data in its original form; silver cleans and validates (deduplication, normalisation); gold holds dimensional models and aggregates for analytics and reporting — the star of session 17. Other names for the same idea: raw / cleansed / curated, or landing / staging / presentation zones. The point for students: the sessions 14–17 pipeline already followed this pattern, inside one SQLite file. Why keep bronze? If the cleaning code has a bug or the business rule changes (e.g. the bad bike day threshold), silver and gold are rebuilt from bronze — the API need not be called again (session 15, plan B).
:::

---

# Data Mesh and Data Fabric {.section}

When one central team is not enough

---

# From One Central Team to a Data Mesh

![Left: a central data platform. Sales, workshop, purchasing and rental send their data to one central data team that runs one lake or warehouse and all pipelines and serves analysts and reports; bottleneck: every new question waits for one team. Right: a data mesh. A sales, workshop, purchasing and rental team each own their data and publish data products; below them a self-serve data platform with storage, pipelines and a catalogue, and federated governance with global rules applied automatically; consumers use data products directly across domains](img/arch-mesh.png){width=78%}

::: source
Own illustration based on Dehghani (2020, 2022) and Serra (2024, Chapter 13).
:::

::: notes
Dehghani (2020, 2022) argues that central lakes and warehouses fail at scale for organisational reasons: one central data team sits between dozens of source domains and dozens of consumers, does not understand each domain's data, and becomes the bottleneck. Her answer is to decentralise ownership by business domain — like microservices for operational systems. Serra (2024, Chapter 13) calls data mesh "a concept, not a technology": an organisational and cultural shift; the technology underneath can be a lake, a lakehouse or a warehouse. The rental domain is the Velo Neckar chain of the case comparison (a fictional future); today's single shop has no such domains.
:::

---

# Data Mesh: Four Principles

| Principle | Meaning | Velo Neckar as a chain (fictional) |
|---|---|---|
| **Domain ownership** | the business domain that knows the data owns and serves it | the rental team owns the e-bike telemetry |
| **Data as a product** | data is served like a product: documented, trustworthy, easy to use | "battery health per bike and day" with owner, schema, quality figures |
| **Self-serve data platform** | a platform team gives domains tools, not finished pipelines | storage, pipeline templates, catalogue — used by every domain |
| **Federated computational governance** | global rules agreed together, enforced by the platform | every product has an owner; personal data is masked automatically |

- Data mesh is **organisational**: you cannot buy it as a product
- It pays off only with **many domains** and **data skills in each domain**

::: source
Based on Dehghani (2020, 2022), Serra (2024, Chapters 13–14) and Strengholt (2023).
:::

::: notes
The four principles in Dehghani's (2020) wording: domain-oriented decentralised data ownership and architecture; data as a product; self-serve data infrastructure as a platform; federated computational governance. "Computational" means that rules are applied by the platform automatically (e.g. a product cannot be published without an owner and a schema), not checked by hand in a committee. Serra (2024, Chapter 14) discusses concerns: duplicated effort and cost in every domain, scarce skills, hard cross-domain integration (conformed dimensions of session 17 do not appear by themselves), and long organisational change. Strengholt (2023) describes how large organisations combine mesh ideas with central platforms. Exam: name the four principles and explain one with an example.
:::

---

# Data Fabric

- A **metadata-driven layer** across many systems: data stays where it is, the fabric makes it **findable, accessible and governed**
- Typical building blocks: **metadata catalogue**, **data virtualisation** (query without copying), **access policies**, master data management, APIs and real-time integration

| | Data mesh | Data fabric |
|---|---|---|
| Main idea | **organisation**: decentralise ownership | **technology**: integrate through metadata |
| Who owns data products | domain teams | often a central team |
| Typical driver | central team is a bottleneck | data spread over many systems |

- Not exclusive: a mesh can run on a fabric-like platform

::: source
Based on Serra (2024, Chapters 11 and 13) and Strengholt (2023).
:::

::: notes
Serra (2024, Chapter 11) describes the data fabric as an evolution of the modern data warehouse: "an advanced layer built onto the MDW to enhance data accessibility, security, discoverability, and availability", with data access policies, a metadata catalogue, master data management, data virtualisation, real-time processing, APIs, services and products. He notes that some analysts (e.g. Gartner) see virtualisation as its core, which he does not; terms are used inconsistently in the market — say so openly. Chapter 13 compares data mesh and data fabric. Link to the catalogue slide: the lake catalogue is a tiny piece of what a fabric automates. Keep this slide short: the distinction mesh = who owns, fabric = how it is connected is the exam core.
:::

---

# Mini Exercise: Mesh, Fabric — or Neither? {.exercise}

Which architecture idea does each statement describe — or which mistake?

1. "Each of our eight business units publishes its sales data with an owner, a description and quality figures."
2. "A catalogue scans our 40 systems; analysts query customer data from SAP and the CRM without copying it."
3. "We are introducing a data mesh — we have bought the licence for tool X."
4. "Velo Neckar (one shop, seven staff) plans a data mesh to be ready for growth."
5. "Our lake holds 2 PB; nobody knows which files are still valid."
6. "The platform refuses to publish a dataset without an owner and a schema."

::: notes
About 5 min in pairs, 3 min collection. Expected answers: 1 data mesh — domain ownership and data as a product. 2 data fabric — metadata catalogue and virtualisation over existing systems. 3 mistake: data mesh is organisational, a tool alone does not create domain ownership (Serra, 2024, Chapter 13: "a concept, not a technology"). 4 neither: one shop has no domains and no data team; a mesh would add overhead without benefit — a small warehouse (or the SQLite star) is enough. 5 a data swamp: missing metadata and governance; fix with a catalogue, owners and retention rules (fabric ideas help, but the first step is governance). 6 federated computational governance (mesh principle 4) — a fabric's access policies are a similar idea; accept both with a reason.
:::

---

# Platforms and Choices {.section}

Cloud data platforms and choosing an architecture

---

# Cloud Computing: Service Models

| Model | The provider runs … | You run … | Data example |
|---|---|---|---|
| **IaaS** | servers, storage, network | operating system, database, backups | a virtual machine with your own PostgreSQL |
| **PaaS** | also the platform | your data and code | a managed database or warehouse service |
| **SaaS** | the whole application | your data and settings | a cloud BI tool or a CRM |

- NIST characteristics: **on-demand self-service**, broad network access, resource pooling, **rapid elasticity**, **measured service** (pay per use)
- Data platforms separate **storage** (cheap, object storage) from **compute** (rented per query or hour)
- Watch: **costs** of careless queries, **lock-in**, **where** the data is stored (GDPR, session 19)

::: source
Based on Mell and Grance (2011), Armbrust et al. (2021) and Reis and Housley (2022, Chapter 4).
:::

::: notes
Mell and Grance (2011) give the NIST definition: five essential characteristics, three service models (SaaS, PaaS, IaaS) and four deployment models (private, community, public, hybrid cloud). Armbrust et al. (2021) build the lakehouse on cloud object storage with compute that can be started and stopped separately — the reason lakes became cheap. Reis and Housley (2022, Chapter 4) discuss choosing technologies, including cloud vs. on premises and cost. Prices are deliberately not on the slide: they change too often. Typical student misconception: "the cloud is always cheaper" — for a constant small workload, a small server or SQLite can be cheaper; elasticity pays off for varying loads. Data location and contracts are part of session 19.
:::

---

# Five Architectures at a Glance

| | Warehouse | Lake | Lakehouse | Mesh | Fabric |
|---|---|---|---|---|---|
| Kind | storage + model | storage | storage + management | **organisation** | **integration layer** |
| Data | structured | any | any | any | any, where it is |
| Schema | on write | on read | both | per data product | per source |
| Strength | trusted reports | cheap, flexible | one copy for BI and ML | scales with domains | connects many systems |
| Risk | rigid, costly to change | swamp | complex platform | cost, skills, duplicated effort | tool-driven, vague term |

::: source
Own summary based on Serra (2024, Chapters 10–14), Armbrust et al. (2021) and Dehghani (2022).
:::

::: notes
This table is exam-relevant. Remind: mesh and fabric are on a different level than the first three — they say who owns and how data is connected; underneath there is still a warehouse, a lake or a lakehouse. Serra (2024) presents the modern data warehouse, data fabric, data lakehouse and data mesh as the four options his subtitle names. Many real organisations are hybrids: a lakehouse as the platform, mesh ideas in the organisation, fabric tools for the catalogue. Ask: which column describes your project database? → a small warehouse (star of milestone 5) on top of an operational schema.
:::

---

# Choosing: Questions Before Technology

1. Which **business questions** must the data answer — reports, ad-hoc analysis, machine learning?
2. Which **data**: structured only, or also files, logs, images? How much, how fast?
3. How many **domains and teams** — and where are the data skills?
4. Which **rules** apply: personal data, retention, data location, audits?
5. What may it **cost**, and how soon must it deliver?

::: callout
Choose the **simplest** architecture that answers today's questions and can grow with tomorrow's. The architecture follows the **organisation** — not the other way round.
:::

::: source
Based on Serra (2024, Chapters 2–3) and Reis and Housley (2022, Chapter 3).
:::

::: notes
Serra (2024, Chapter 3) recommends starting with an architecture design session that asks about the business, its data and its people before any tool. Reis and Housley (2022, Chapter 3) describe good data architecture as flexible and reversible ("two-way doors") and serving the business. "Choose the simplest" is the lecturer's rule of thumb, as in session 11 ("start relational unless a clear reason speaks against it"), not a quote. Question 3 is most often forgotten — a mesh without skills in the domains fails, however good the tool.
:::

---

# Exercise: A Mini Lake for the Bike Shop {.exercise}

Load `bikeshop-lake-catalog-session18.sql`. Predict first, then run.

1. **Schema-on-read**: copy the two Bright Sky files into `lake/bronze/brightsky/<station>/` and read both with pandas. How many rows and columns? Which columns exist for only one station — and what do they mean?
2. **Overview**: number of files and total size per zone
3. **Swamp check**: which files have no owner or no description?
4. **Duplicates**: which files have the same `checksum`?
5. **Dark data**: which bronze files are used by no other file (`lake_lineage`)? What share of the bronze volume is that?
6. **Personal data**: which files contain personal data or might? Which gold file depends on them?
7. **Lineage**: from which bronze files is `gold/report_revenue_by_weather.csv` built?

::: notes
About 20 min + 2 min comparison. Expected answers (all observed; SQLite 3.45.1, pandas 3.0.6):
1 (338, 16): 169 hourly records per station; the six fallback_source_ids columns (cloud_cover, sunshine, temperature, wind_speed, relative_humidity, condition) exist only in the Heidelberg file and are NaN for Mannheim. Five of them are filled in all 169 Heidelberg records with source 184401, condition in 12 — the Heidelberg values for these fields come from the Mannheim source. Copy code: `shutil.copy("brightsky-mannheim-2026-10-05.json", "lake/bronze/brightsky/mannheim/2026-10-05.json")` after `Path(...).mkdir(parents=True, exist_ok=True)`.
2 `SELECT zone, count(*), sum(size_kb) FROM lake_file GROUP BY zone` → bronze 15 files 66,548 KB (about 65 MB), silver 5 files 17 KB, gold 4 files 9 KB.
3 Files 8, 9, 12, 14, 15 (clickstream of 5 and 6 Oct, IMG_0412.jpg, old_stuff.zip, "pricelist-2027 (1).csv"); file 8 has a description but no owner.
4 Checksum 0d44b7e9: file 3 (S1 price list) and file 15 (the copy in misc) — delete 15 after checking.
5 `WHERE zone = 'bronze' AND NOT EXISTS (SELECT 1 FROM lake_lineage WHERE source_id = file_id)` → files 2, 8, 9, 10, 11, 12, 13, 14, 15: 66,492 of 66,548 KB = 99.9 % of the bronze volume. Not all of it is waste (photos and invoices are kept for the business), but it is unused for analysis.
6 yes: 7 (accounts export), 8, 9 (clickstream with IP addresses), 20 (cleaned accounts); unknown: 10, 11, 12 (photos), 14, 15. No gold file depends on them (check the lineage of 21–24) — so why keep 20? Leads to session 19 (purpose, storage limitation).
7 Two joins, or WITH RECURSIVE over lake_lineage starting at file 24 → bronze files 1 (Mannheim weather), 3 and 4 (price lists, via supplier_price and dim_product) and 6 (receipts). The lineage answers "if the S1 price list was wrong, which reports must be rebuilt?".
:::

---

# Exercise: Architecture Case Comparison {.exercise}

One case per group. Use the five questions of the last slide, recommend an architecture, and name **one risk**.

::: cards
### A · Velo Neckar today
One shop, seven staff, till, web shop, workshop. The owner wants monthly reports. Nobody works in IT.
### B · Velo Neckar 2030
15 shops, 2,000 rental e-bikes sending battery and GPS data every 10 s, damage photos from an app. Three data engineers; a data scientist wants to predict battery failures.
### C · Rheinmarkt (retail)
400 stores, 12 business units with their own analysts. The central data team has a waiting list of four months for new reports.
### D · Stadtwerke after a merger
Energy and water utility, 25 systems (ERP, meter data, maps, CRM), partly on premises. Strict regulation; data may not be copied freely. Management wants one view of each customer.
:::

::: notes
About 18 min in groups of four + 7 min short presentations (one minute per group). All cases are fictional. Expected recommendations (accept others with sound reasons):
A — a small warehouse: the SQLite star of session 17, or a SaaS BI tool on top of the till; raw files in a simple folder with a catalogue (a "mini lake"). No lakehouse, no mesh. Risk: depending on one person who knows the scripts.
B — a lakehouse in the cloud: telemetry (volume, velocity), photos (unstructured) and BI on one platform, bronze/silver/gold, one copy for reports and the battery model. Risk: platform complexity and running costs for a small team; telemetry contains GPS positions of customers (personal data, session 19).
C — data mesh (or mesh ideas): many domains with their own analysts, the central team is the bottleneck. Self-serve platform underneath (often a lakehouse), federated governance with conformed dimensions such as product and store. Risk: duplicated effort, inconsistent definitions, long change process.
D — data fabric: data stays in the 25 systems, a catalogue, access policies and virtualisation give one view of the customer; master data management for the customer. Risk: performance of virtual queries, vague product promises, many owners.
Debrief question: which cases differ mainly in technology (A vs. B), which mainly in organisation (C, D)?
:::

---

# Team Work: Your Project Architecture {.exercise}

1. Which parts of your project are already **bronze**, **silver** and **gold**?
2. Which data of your case would **not** fit into your SQLite database — files, logs, images?
3. Your case grows **100 times** and gets five departments: which architecture would you choose, and why?
4. Write **two sentences** on this for the "outlook" part of your final presentation

::: callout
**Final presentation (session 20):** design decisions, demo, lessons learned. An outlook on how your design would scale is welcome — keep it short.
:::

::: notes
About 10 min. Walk around and ask: where is your raw data kept — could you rebuild your tables from it? Which of your tables is the gold layer (usually the milestone 5 star)? Typical good answers for question 3: lakehouse if files or high-volume data appear, mesh only if the departments have their own data people. The outlook is optional and should not be longer than one slide; the exact requirements are in the project brief.
:::

---

# Key Takeaways

- A **data lake** stores any data raw and applies the structure on **read**; without a **catalogue** it becomes a **swamp**
- A **lakehouse** adds warehouse features (ACID, schema enforcement, versions) to lake storage: one copy for **BI and ML**, in **bronze, silver, gold** layers
- **Data mesh** decentralises ownership: domains, data as a product, self-serve platform, federated computational governance
- **Data fabric** connects data where it is, through metadata, virtualisation and access policies
- **Cloud** platforms rent infrastructure (IaaS, PaaS, SaaS) and separate storage from compute
- Choose by **questions, data, organisation, rules and cost** — the simplest architecture that fits

::: source
Serra (2024); Armbrust et al. (2021); Dehghani (2022); Mell and Grance (2011).
:::

---

# Next Session: Access to Data — Legal and Organisational Aspects

- **GDPR**, EU **Data Act**, **Data Governance Act**, **AI Act** (data aspects)
- **Data licences** and open data
- **Data governance**: data owner, data steward, CDO, data strategy
- Case discussion: may we use this data?

::: callout
**Preparation:** finish the hands-on and worksheet 18. List the data of your **project** that contains **personal data** and the **licence** of every external source. Think: may the shop keep the clickstream with IP addresses — and for how long?
:::

---

# References {.references}

- Armbrust, M., Ghodsi, A., Xin, R., & Zaharia, M. (2021). Lakehouse: A new generation of open platforms that unify data warehousing and advanced analytics. In *CIDR 2021: Conference on Innovative Data Systems Research*. https://vldb.org/cidrdb/2021/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics.html
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Databricks. (n.d.). *What is the medallion lakehouse architecture?* Databricks documentation. Retrieved October 22, 2026, from https://docs.databricks.com/aws/en/lakehouse/medallion.html
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Dehghani, Z. (2020, December 3). *Data mesh principles and logical architecture*. martinfowler.com. https://martinfowler.com/articles/data-mesh-principles.html
- Dehghani, Z. (2022). *Data mesh: Delivering data-driven value at scale*. O'Reilly Media.
- Inmon, B. (2016). *Data lake architecture: Designing the data lake and avoiding the garbage dump*. Technics Publications.

---

# References (continued) {.references}

- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Mell, P., & Grance, T. (2011). *The NIST definition of cloud computing* (NIST Special Publication 800-145). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-145
- Reis, J., & Housley, M. (2022). *Fundamentals of data engineering: Plan and build robust data systems*. O'Reilly Media.
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
- Strengholt, P. (2023). *Data management at scale: Modern data architecture with data mesh and data fabric* (2nd ed.). O'Reilly Media.
