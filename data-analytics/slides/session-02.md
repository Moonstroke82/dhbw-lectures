---
course: Data Analytics
session: 2
title: Data Warehouse Architectures
subtitle: OLTP and OLAP · reference architecture · Inmon and Kimball · lakehouse
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Data Warehouse Architectures {.title}

::: notes
Time plan for today (3 h): setup check 15 min · OLTP vs. OLAP 25 min · DWH definition and reference architecture 30 min · break 10 min · Inmon vs. Kimball and lakehouse 25 min · lab 60 min · wrap-up 5 min · ~10 min buffer.
Start with the setup check: anyone whose test cell from session 1 failed gets help first; pair them with a neighbour for the lab if it cannot be fixed quickly.
:::

---

# Today's Agenda

1. Setup check
2. Two worlds of data processing: OLTP and OLAP
3. What is a data warehouse?
4. Reference architecture: from sources to data marts
5. Inmon vs. Kimball — and the data warehouse in the lakehouse era
6. Lab: explore a sample warehouse in DuckDB

::: notes
Time and format guide (not shown to students):
0:00 Setup check · 0:15 OLTP vs. OLAP (input + discussion) · 0:40 DWH definition and architecture (input) · 1:10 Break · 1:20 Inmon vs. Kimball, lakehouse (input + discussion) · 1:45 Lab (pairs) · 2:45 Wrap-up · ~10 min buffer.
If the setup check takes longer, shorten the lakehouse part (the optional slide can be self-study) and keep the lab.
:::

---

# Use Case: A Retailer Asks Questions

A retail company runs an online shop and 200 stores. Management asks:

- How did **revenue per region** develop over the last three years?
- Which **product groups** grow, which shrink?
- Do **promotions** pay off, or do they only shift sales in time?

::: callout
Every order is stored in the shop system. Why can't we simply run these questions on the shop database?
:::

::: notes
Fictional case used throughout the session. Collect answers before showing the next slide: load on the production system, data spread over several systems (shop, stores, ERP), no history (prices and customer addresses are overwritten), data in a structure built for transactions, not for analysis.
:::

---

# Two Worlds: OLTP and OLAP {.section}

Running the business vs. analysing the business

---

# OLTP vs. OLAP

| | OLTP (operational systems) | OLAP (analytical systems) |
|---|---|---|
| Purpose | Run day-to-day business processes | Support analysis and decisions |
| Typical operation | Insert, update, read single records | Read and aggregate many records |
| Query example | "Show order 4711" | "Revenue per region and quarter" |
| Data | Current state, detailed | Historical, integrated, often summarised |
| Data model | Normalised (avoid redundancy) | Dimensional (easy and fast to query) |
| Users | Many clerks and customers | Fewer analysts and managers |
| Priority | Throughput, consistency, availability | Query performance on large volumes |

::: source
Based on Chaudhuri and Dayal (1997).
:::

::: notes
Chaudhuri and Dayal explain why analytical workloads are kept separate from operational databases: different queries, different data models, different performance requirements, and historical data from several sources. Note: today, some database systems (HTAP, in-memory systems such as SAP HANA) serve both workloads on one platform — but the logical distinction remains.
:::

---

# Same Data, Different Questions {.exercise}

Which questions belong to OLTP, which to OLAP?

1. Is product 123 still in stock in the Mannheim store?
2. Which stores had falling sales in the last four quarters?
3. Change the delivery address of order 98765.
4. What is the average basket size per customer segment and month?
5. Has customer 555 already paid invoice 2024-0815?

::: notes
Answers: 1 OLTP · 2 OLAP · 3 OLTP · 4 OLAP · 5 OLTP. Point out the pattern: OLTP = single business objects, current state; OLAP = many records, aggregated, over time.
:::

---

# What Is a Data Warehouse? {.section}

Definition and characteristics

---

# The Classic Definition

::: callout
A data warehouse is a **subject-oriented, integrated, time-variant** and **non-volatile** collection of data in support of management's decisions.
:::

::: cards
### Subject-oriented
Organised around business subjects (customer, product, sales), not around applications.

### Integrated
Data from different sources is brought to common keys, formats and meanings.

### Time-variant
Data is stored with a time reference, so history can be analysed.

### Non-volatile
Data is loaded and read, but not changed by daily transactions.
:::

::: source
Inmon (2005).
:::

::: notes
Inmon's definition from the early 1990s is still the most cited one. Verify the page number in the library copy before quoting it in written material. Link to the use case: integrated (shop + stores + ERP), time-variant (three years of history), non-volatile (no overwriting of old prices).
:::

---

# Reference Architecture

::: layers
- Analysis and presentation: Reports, dashboards, OLAP, ad-hoc queries, data mining and ML
- Data marts: Subject- or department-specific extracts, often dimensional
- Core data warehouse: Integrated, historised, quality-assured data
- Staging area: Raw copies of source data for transformation and cleaning
- Data sources: ERP, CRM, shop system, external data
:::

::: source
Own illustration based on Baars and Kemper (2021, Chapter 2) and Chaudhuri and Dayal (1997).
:::

::: notes
Read bottom-up. ETL (extract, transform, load) moves data from sources via staging into the core DWH. Metadata management and data quality run across all layers. Students from the Data Management or Data Engineering modules know ETL already; here we focus on what the layers mean for the analyst: where do I find which data, and how much can I trust it?
:::

---

# What the Layers Mean for the Analyst

| Layer | What you find there | What to watch out for |
|---|---|---|
| Staging | Raw source data | Not cleaned, source-specific codes; rarely accessible |
| Core DWH | Integrated, historised data | Complex model; good for detailed analysis |
| Data marts | Prepared data for a subject | Already aggregated or filtered — check the definitions |
| Reports and dashboards | Agreed KPIs | Fast answers, but only to predefined questions |

::: callout
Before you analyse, find out **which layer** your data comes from and **how its measures are defined**.
:::

::: source
Own illustration based on Baars and Kemper (2021).
:::

::: notes
Typical pitfall: two departments report different "revenue" figures because one mart counts net revenue after returns, the other gross revenue. Ask students if they know such cases from their companies.
:::

---

# Inmon vs. Kimball {.section}

Two schools of data warehouse design

---

# Two Design Approaches

::: columns
**Inmon: enterprise data warehouse first**

- Central, normalised core data warehouse for the whole enterprise
- Dependent data marts are derived from it
- Top-down: strong integration, but long time to first result
|||
**Kimball: dimensional bus architecture**

- Data marts built as dimensional models (star schemas) per business process
- Integrated through shared, **conformed dimensions** (e.g. one customer, one calendar)
- Bottom-up: fast results, integration needs discipline
:::

::: source
Inmon (2005); Kimball and Ross (2013).
:::

::: notes
In practice, most data warehouses are hybrids: a normalised or data-vault-based core plus dimensional marts. The exam-relevant point is the trade-off between integration and speed of delivery. Data vault is a third modelling approach for the core layer; mention it only if asked.
:::

---

# Star Schema: A First Look

- A **fact table** in the centre holds the measures of a business process, e.g. revenue and quantity per sales line
- **Dimension tables** around it describe the context: *who* (customer), *what* (product), *where* (store), *when* (date)
- Queries filter and group by dimension attributes and aggregate the facts

::: callout
"Revenue per region and quarter" = sum of a **fact** grouped by attributes of two **dimensions**.
:::

::: source
Kimball and Ross (2013).
:::

::: notes
Only a preview — dimensional modelling, hierarchies and slowly changing dimensions are the topic of session 3. Draw a small star schema on the whiteboard for the retail case: fact_sales with dim_date, dim_store, dim_product, dim_customer.
:::

---

# The Data Warehouse in the Lakehouse Era

::: cards
### Data lake
Stores raw data of any format cheaply, e.g. in cloud object storage. Flexible, but quality and structure are often unclear.

### Data warehouse
Structured, quality-assured data with fast SQL. Reliable, but less flexible for unstructured data and ML.

### Lakehouse
Open table formats on the data lake add warehouse features: transactions, schemas, versioning, fast SQL — on one storage layer.
:::

::: source
Armbrust et al. (2021).
:::

::: notes
Armbrust et al. argue that the two-tier architecture (lake + separate warehouse) causes duplicated data, staleness and complexity, and propose the lakehouse. Examples of open table formats: Delta Lake, Apache Iceberg, Apache Hudi. Important for students: the dimensional modelling ideas of the warehouse stay relevant in a lakehouse — only the storage technology changes.
:::

---

# Which Architecture Fits? {.optional}

| Situation | Likely fit |
|---|---|
| Stable, well-defined KPIs from ERP and CRM; many business users | Classic data warehouse |
| Large volumes of raw, varied data for data science and ML | Data lake or lakehouse |
| Both, and the goal is one platform without copying data | Lakehouse |
| Small team, moderate data volume, analytics on a laptop | Analytical database such as DuckDB |

::: source
Own summary based on Armbrust et al. (2021) and Baars and Kemper (2021).
:::

::: notes
Self-study. Architecture decisions depend on data, users, skills and costs, not only on technology trends.
:::

---

# Lab: Explore a Sample Warehouse {.section}

DuckDB and the TPC-H dataset

---

# The Lab Setup

- **DuckDB** is an analytical (OLAP) database that runs inside Python — no server needed
- **TPC-H** is a standard benchmark dataset of a wholesale supplier: orders, line items, customers, parts, suppliers, nations, regions
- DuckDB can generate TPC-H data directly:

```python
import duckdb
con = duckdb.connect("tpch.duckdb")
con.sql("INSTALL tpch; LOAD tpch; CALL dbgen(sf = 0.1)")
con.sql("SHOW TABLES").show()
```

::: source
Raasveldt and Mühleisen (2019); Transaction Processing Performance Council (n.d.).
:::

::: notes
Scale factor 0.1 creates about 600,000 line items — enough to feel analytical queries, small enough for every laptop. The first call downloads the tpch extension, so the room needs internet access. If the download fails, provide the generated file tpch.duckdb on a USB stick or the course platform.
:::

---

# Lab Tasks {.exercise}

Work in pairs. Write your answers in a notebook.

1. **Explore:** list all tables and their columns (`DESCRIBE lineitem`). Which tables hold **facts**, which describe **context**?
2. **Interpret:** what does one row in `lineitem` represent? Which columns are measures?
3. **Query:** compute revenue per **region** and **year**. Revenue = `l_extendedprice * (1 - l_discount)`.
4. **Evaluate:** which region grows fastest? Check the date range of the orders: are all years complete? How realistic do the numbers look?
5. **Reflect:** is TPC-H an Inmon-style or a Kimball-style model? What would you change to make it a star schema?

::: notes
Hints for task 3: join lineitem → orders → customer → nation → region; year = year(o_orderdate). Solution sketch:
SELECT r_name, year(o_orderdate) AS yr, round(sum(l_extendedprice * (1 - l_discount)), 0) AS revenue FROM lineitem JOIN orders ON l_orderkey = o_orderkey JOIN customer ON o_custkey = c_custkey JOIN nation ON c_nationkey = n_nationkey JOIN region ON n_regionkey = r_regionkey GROUP BY ALL ORDER BY r_name, yr;
Task 4 (tested with DuckDB 1.5.6, sf 0.1): revenue is almost flat across all regions and years (about 600–640 million per region and year) because TPC-H is synthetic, uniformly generated data — there is no real growth story. Orders run from 1992-01-01 to 1998-08-02, so 1998 is incomplete and looks like a collapse (about 380 million). Two lessons: check completeness before interpreting a trend, and know whether data is synthetic. Task 5: TPC-H is normalised (closer to a 3NF core); a star schema would have a sales fact with date, customer (incl. nation and region), part and supplier dimensions.
:::

---

# Discussion: What Did You Find?

- Which joins did you need — and how would a star schema simplify them?
- What surprised you in the results?
- What would you need to know about the data **before** reporting these numbers to management?

::: notes
Collect 2–3 answers per question. Lead to the key message: interpreting warehouse data means knowing its model, its definitions and its completeness. This lab is the starting point for portfolio notebook 1 (DWH, OLAP, analytical SQL).
:::

---

# Key Takeaways

- **OLTP** systems run the business; **OLAP** systems analyse it — with different queries, data models and priorities
- A data warehouse is **subject-oriented, integrated, time-variant and non-volatile**
- The reference architecture leads from **sources** via **staging** and **core DWH** to **data marts** and front ends
- **Inmon** integrates first, **Kimball** delivers dimensional marts first; most real warehouses are hybrids
- The **lakehouse** adds warehouse features to the data lake — dimensional thinking stays relevant

---

# Next Session: Dimensional Data and OLAP

- Star and snowflake schema
- Facts, measures, dimensions and hierarchies
- Slowly changing dimensions
- OLAP operations: slice, dice, drill-down, roll-up, pivot

::: callout
**Preparation:** keep your `tpch.duckdb` file — we will turn it into a star schema.
:::

---

# References {.references}

- Armbrust, M., Ghodsi, A., Xin, R., & Zaharia, M. (2021). Lakehouse: A new generation of open platforms that unify data warehousing and advanced analytics. In *Proceedings of the 11th Conference on Innovative Data Systems Research (CIDR)*. https://www.cidrdb.org/cidr2021/papers/cidr2021_paper17.pdf
- Baars, H., & Kemper, H.-G. (2021). *Business Intelligence & Analytics: Grundlagen und praktische Anwendungen* (4th ed.). Springer Vieweg. https://doi.org/10.1007/978-3-8348-2344-1
- Chaudhuri, S., & Dayal, U. (1997). An overview of data warehousing and OLAP technology. *ACM SIGMOD Record, 26*(1), 65–74. https://doi.org/10.1145/248603.248616
- Inmon, W. H. (2005). *Building the data warehouse* (4th ed.). Wiley.
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Raasveldt, M., & Mühleisen, H. (2019). DuckDB: An embeddable analytical database. In *Proceedings of the 2019 International Conference on Management of Data (SIGMOD '19)* (pp. 1981–1984). ACM. https://doi.org/10.1145/3299869.3320212
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 7, 2026, from https://www.tpc.org/tpch/
