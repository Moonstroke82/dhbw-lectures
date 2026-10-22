---
course: Data Management
session: 17
title: Data Warehousing
subtitle: DWH concepts · Inmon vs. Kimball · star and snowflake schema · fact and dimension tables · OLAP
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Data Warehousing {.title}

::: notes
Time plan for today (3 h): recap 7 min · today's data 3 min · why a data warehouse: OLTP vs. OLAP, definition 12 min · Inmon vs. Kimball 10 min · mini exercise OLTP or OLAP 8 min · break 10 min · dimensional modelling: facts, dimensions, four steps, grain, star 15 min · dimension and fact tables 8 min · mini exercise fact or dimension 8 min · snowflake, loading the star, conformed dimensions 8 min · OLAP: cube, operations, SQL, reading results 10 min · hands-on: the bike shop star 45 min · team step 12 min · wrap-up 5 min · ~19 min buffer.
Input is about 73 minutes, hands-on, exercises and discussion about 73 minutes. Priorities if time runs short: OLTP vs. OLAP, Inmon's four properties, Inmon vs. Kimball (top-down vs. bottom-up), facts vs. dimensions, the grain, star vs. snowflake, additive vs. non-additive facts and the five OLAP operations are the exam core. Today is an introduction: Data Analytics (semester 5) treats warehouse architectures, slowly changing dimensions, cubes and analytical SQL in depth — do not go deeper than the slides here. The optional slide on slowly changing dimensions is self-study. Shorten the hands-on to questions 1–4 if needed, but keep question 5 (reading the result critically).
How the results were produced: every SQL statement was run with SQLite 3.45.1 on a fresh bikeshop.db built from bikeshop-schema.sql, bikeshop-data.sql, bikeshop-data-session09.sql, bikeshop-etl-session16.sql, the new bikeshop-sales-session17.sql (till receipts of 5–10 October 2026, fictional; daily totals match the till export of session 16) and the new bikeshop-star-session17.sql (the model star). Weather values are those of sessions 15 and 16 (DWD via Bright Sky, saved copy).
:::

---

# Today's Agenda

1. Recap: from a daily pipeline to analysis
2. Why a data warehouse — and what it is
3. Inmon vs. Kimball: two ways to build one
4. Dimensional modelling: facts, dimensions, star and snowflake
5. OLAP: slicing, dicing and drilling through the data
6. Hands-on: a star schema for the bike shop — and for your project

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:07 Today's data (everyone) · 0:10 Why a DWH, Inmon vs. Kimball (input) · 0:32 Mini exercise OLTP or OLAP (pairs) · 0:40 Break · 0:50 Dimensional modelling (input, live drawing on the board) · 1:13 Mini exercise fact or dimension (pairs) · 1:21 Snowflake, loading, conformed dimensions, OLAP (input, live SQL) · 1:39 Hands-on (pairs, each student on their own laptop) · 2:24 Team step (project teams) · 2:36 Wrap-up · buffer.
Live demo: draw the star on the board while explaining the four steps — students should see that the design comes before the SQL. Run the OLAP queries live from the star; the pivot result is the "aha" of the session.
:::

---

# Recap: Where Session 16 Left Us

- A **pipeline** loads the weather, the price lists and the till figures into `bikeshop.db` — every day, idempotently, with a **run log**
- Session 16 ended with a question: do **bad bike days** cost us revenue?
- One join of `till_daily` and `weather_daily` gave a first answer — but only **per day**, only **totals**
- Today: a structure built for **questions** like this one — by day, weather, product group and salesperson

::: callout
**Your preparation:** if the shop wants revenue **per day, per weather type and per product group**, which tables would you build?
:::

::: source
Session 16 of this course; Kimball and Ross (2013, Chapter 1).
:::

::: notes
Collect two or three answers to the preparation question; write them on the board and come back to them after the star schema slide. Typical answers: "one big table with all columns" (close to a star, but with repeated text), "a view joining everything" (works for small data, but every question repeats the joins), "a table per question" (does not scale). Remind: in session 16 the bad bike days (Thu, Fri, Sat) had lower average revenue, but Saturday was the best day of the week — the till totals cannot say which products sold. That needs the receipt lines, which the till delivers today.
:::

---

# Today's Data

| Source | Content | Becomes |
|---|---|---|
| `bikeshop-sales-session17.sql` | **new**: the till's receipts and lines, 5–10 Oct 2026 | `product`, `sale`, `sale_line` |
| `weather_daily` (session 16) | daily weather, Mannheim | weather type per day |
| `employee`, `salesperson` (session 7) | the shop's staff | who sold it |
| `bikeshop-star-session17.sql` | **new**: the model star schema, for checking | `fact_sales`, `dim_…` |

::: source
Own example based on the bike shop case; till data fictional. Weather data: Deutscher Wetterdienst via de Maeyer (n.d.), CC BY 4.0.
:::

::: notes
Everyone runs the loading cell now: the five scripts in the order given in the header of bikeshop-sales-session17.sql. Students without the session 16 pipeline are covered: the script adds the seven weather days with INSERT OR IGNORE (rows from their own pipeline are kept). Check: product 18, sale 35, sale_line 54 rows. The daily sums of quantity × unit_price equal the Umsatz column of the session 16 till export (2,840.50 … 5,980.00; 18,866.80 in total) — observed. Do NOT run the star script yet: students design first (hands-on question 2).
:::

---

# Why a Data Warehouse? {.section}

Analysis apart from the operational systems

---

# Two Worlds: OLTP and OLAP

| | Operational (OLTP) | Analytical (OLAP) |
|---|---|---|
| Purpose | **run** the business | **understand** and steer it |
| Bike shop example | the till records receipt 1029 | revenue per product group on rainy days |
| Typical access | read or write **a few rows** | read and **aggregate many rows** |
| Data | current, detailed, changes all the time | **history**, integrated from many sources |
| Design | normalised (session 6): no anomalies | **denormalised**: simple, fast queries |
| Users | staff at the till, the workshop | owner, controlling, analysts |

::: source
Based on Chaudhuri and Dayal (1997) and Kimball and Ross (2013, Chapter 1).
:::

::: notes
OLTP = online transaction processing, OLAP = online analytical processing. Chaudhuri and Dayal (1997) explain why analysis is kept apart from the operational databases: analytical queries scan and aggregate millions of rows and would slow down the till; they need history and data from several systems; and they need a different data model. Kimball and Ross (2013, Chapter 1) open with the same contrast: "different worlds" of data capture and data analysis. Link to session 6: normalisation protects against update anomalies — but a warehouse is mostly read, and loaded by ETL, not by the till, so redundancy is acceptable there (the "when to denormalise" slide of session 6 promised this session).
:::

---

# What Is a Data Warehouse?

::: callout
A data warehouse is a **subject-oriented**, **integrated**, **nonvolatile** and **time-variant** collection of data in support of management's decisions (Inmon, 2005).
:::

| Property | Meaning | Bike shop |
|---|---|---|
| **Subject-oriented** | organised by business subjects, not by applications | sales, repairs, purchasing — not "till app tables" |
| **Integrated** | one format, one key, one meaning across sources | one product number, one date format, one station |
| **Nonvolatile** | loaded and read, not changed by daily work | a receipt line stays as it was sold |
| **Time-variant** | keeps history, every row belongs to a point in time | sales of every day since the start |

::: source
Inmon (2005, Chapter 2); DAMA International (2017, Chapter 11).
:::

::: notes
The definition is from Inmon (2005, Chapter 2, "The Data Warehouse Environment"); it goes back to the early 1990s and is still the most cited one. Do not ask students to learn the sentence by heart — the four properties with an example are the exam core. DAMA International (2017, Chapter 11) treats data warehousing and business intelligence as a knowledge area of its own (the DAMA wheel of session 2). Integrated is where ETL comes in (session 16: schema, format, key and meaning conflicts). Nonvolatile does not mean "never loaded again": new data is added, corrections arrive by the pipeline, but nobody edits the warehouse by hand.
:::

---

# Inmon vs. Kimball {.section}

Two ways to build a data warehouse

---

# Two Architectures

![Two lanes. Inmon, top-down: sources (till, web shop, repairs) go through ETL into one normalised enterprise data warehouse covering all subjects; sales, workshop and purchasing data marts are derived from it and feed BI and reports. Kimball, bottom-up: the same sources go through ETL and staging into dimensional stars for sales, workshop and purchasing that share conformed dimensions (date, product, employee); together they are the data warehouse and feed BI and reports](img/dwh-inmon-kimball.png){width=88%}

::: source
Own illustration based on Inmon (2005), Kimball and Ross (2013, Chapter 1) and Serra (2024, Chapter 8).
:::

::: notes
Inmon: first an enterprise data warehouse with an integrated, normalised model of the whole company; dimensional data marts for departments are derived from it ("top-down"). Kimball: the warehouse is the set of dimensional models (stars), built one business process at a time and integrated by shared, conformed dimensions ("bottom-up"); Kimball and Ross (2013, Chapter 1) describe their architecture and alternatives, including Inmon's hub-and-spoke "Corporate Information Factory". Serra (2024, Chapter 8) presents both methodologies, how to choose and hybrid models. Both use ETL and a staging area — the difference is the layer in the middle.
:::

---

# Inmon or Kimball?

| | Inmon | Kimball |
|---|---|---|
| Direction | **top-down**: enterprise model first | **bottom-up**: one business process first |
| Central layer | normalised enterprise DWH (3NF) | dimensional stars with **conformed dimensions** |
| Data marts | derived from the DWH | **are** the DWH |
| First results | later: big upfront design | **sooner**: one star delivers |
| Strength | one integrated, flexible core | easy to understand and query |
| Risk | long project before any report | stars that do not fit together if dimensions are not shared |

- In practice: many **hybrids**, e.g. a normalised core plus stars for reporting
- For the bike shop and your project: **Kimball** — one star per business process

::: source
Based on Inmon (2005), Kimball and Ross (2013, Chapters 1 and 4) and Serra (2024, Chapter 8).
:::

::: notes
Keep it balanced: the debate of the 1990s was heated, today both camps agree on more than they disagree. Serra (2024, Chapter 8) discusses how to choose a methodology and hybrid models. Kimball and Ross (2013, Chapter 4) explain the enterprise data warehouse bus architecture: conformed dimensions are what make a set of stars an integrated warehouse rather than isolated "data silos". Why Kimball for the project: one business process, small team, quick result, easy queries. Data Analytics (semester 5) returns to architectures in depth, including the lakehouse; session 18 gives the overview.
:::

---

# Mini Exercise: OLTP, OLAP — and Inmon's Properties {.exercise}

1. OLTP or OLAP? a) the mechanic closes repair job 512 · b) average repair revenue per month over three years · c) the web shop reserves the last LED light · d) the owner compares rainy and dry Saturdays
2. Which of Inmon's properties does each design **violate**?
   - a) Every night the warehouse table `price` is **overwritten** with today's prices
   - b) The warehouse has one table per **screen** of the till application
   - c) Sales use `2026-10-05`, weather uses `05.10.2026`, and the station is called `MA` in one table and `Mannheim` in the other
3. A team of two must show sales figures to the owner **next month**. Inmon or Kimball?

::: notes
About 5 min in pairs, 3 min collection. Expected answers:
1 a OLTP (one row changed) · b OLAP (many rows, history, aggregate) · c OLTP (a transaction, ACID of session 10) · d OLAP (aggregate, integrates weather and sales).
2 a time-variant (and nonvolatile): yesterday's prices are lost, so last year's margin cannot be computed any more — keep price rows with a valid-from date (worksheet 16's supplier_price had valid_from). b subject-oriented: organised by application, not by subject (sales, repairs). c integrated: formats and names must be unified in the ETL before loading.
3 Kimball: one star for sales delivers within weeks; an enterprise model first would take too long. Good answers add: share the date and product dimensions so a later workshop star fits.
:::

---

# Dimensional Modelling {.section}

Facts, dimensions and the star schema

---

# Facts and Dimensions

::: cards
### Facts
The **measurements** of a business process: numbers you add up or average. Bike shop: **quantity**, **revenue** of a receipt line.
### Dimensions
The **context** of a fact: who, what, where, when, under which conditions. Bike shop: **date**, **product**, **salesperson**, **weather**.
:::

- Listen for "**by**": "revenue **by** product group **by** weather type" — revenue is the fact, product group and weather type come from dimensions
- Dimension **attributes** are the words in the report headings and filters: `weekday`, `product_group`, `bike_day`
- A **fact table** holds the measurements and the **keys** of its dimensions; **dimension tables** hold the descriptions

::: source
Based on Kimball and Ross (2013, Chapters 1–2).
:::

::: notes
Kimball and Ross (2013, Chapter 1) describe the fact table as the place where the numeric performance measurements of a business process are stored, and dimension tables as the textual context ("who, what, where, when, how and why"). The "by" trick works well in class: take the preparation question and underline the fact and the dimensions. A number is not automatically a fact: list_price is a number, but it describes the product — a dimension attribute (and it is not additive: summing list prices means nothing).
:::

---

# Four Steps of Dimensional Design

| Step | Question | Bike shop till |
|---|---|---|
| 1 **Business process** | which activity do we measure? | selling at the till |
| 2 **Grain** | what is **one row** of the fact table? | **one line on a receipt** |
| 3 **Dimensions** | what describes each row? | date, product, salesperson, weather |
| 4 **Facts** | what do we measure per row? | quantity, revenue |

- The **grain** comes before the dimensions and facts — every later decision must fit it
- Choose the **finest** grain the source offers: totals can always be computed from lines, never the other way round

::: source
Based on Kimball and Ross (2013, Chapter 3).
:::

::: notes
Kimball and Ross (2013, Chapter 3) introduce the four-step dimensional design process with a retail case — very close to our till. Their advice is to declare the grain at the most atomic level the source captures, because atomic data can be rolled up in any direction, while pre-aggregated data limits the questions. Ask: what if we chose "one row per day" (like till_daily)? Then "revenue per product group" is impossible. Typical student mistake: mixing grains in one fact table (a receipt line and a daily total in the same table) — sums double. Business process means an activity (selling, repairing, ordering from suppliers), not a department.
:::

---

# The Star Schema

![Star schema: the fact table fact_sales in the centre with foreign keys date_key, product_key, salesperson_key and weather_key, plus receipt_no, line_no, quantity and revenue; around it four dimension tables: dim_date (date_key, full_date, weekday, day_type, month, quarter, year), dim_product (product_key, product_no, name, product_group, category), dim_salesperson (salesperson_key, employee_no, name) and dim_weather (weather_key, weather_type, bike_day, rule). Grain: one line on a till receipt](img/dwh-star.png){width=78%}

::: source
Own illustration based on Kimball and Ross (2013, Chapters 1–3).
:::

::: notes
This is the model solution of today's hands-on (bikeshop-star-session17.sql). Walk around the star: each dimension is one table, joined to the fact table by one key — every question is "fact table plus the dimensions you need", never a chain of joins. Compare with the operational schema: product, sale, sale_line, salesperson, employee, weather_daily — six tables, chains of joins. receipt_no stays in the fact table without its own dimension: a "degenerate dimension" (Kimball & Ross, 2013, Chapter 3) — useful to count receipts. Weather: one shop, one station — the weather type could also be an attribute of a daily dimension; a small weather dimension makes the hierarchy bike_day > weather_type visible. Come back to the students' preparation answers now.
:::

---

# Dimension Tables

- **Wide and descriptive**: many text attributes, few rows — the labels of every report
- **Denormalised**: `product_group` and `category` repeat in every product row — on purpose
- **Hierarchies** inside one table: product → product group → category; date → month → quarter → year
- **Surrogate key**: a meaningless integer (`product_key`), independent of the till's `product_no`
- A **date dimension** with weekday, day type, month … instead of computing them in every query
- No `NULL` foreign keys in the fact: an **"unknown"** row (`weather_key` 0) instead

::: source
Based on Kimball and Ross (2013, Chapters 2–3).
:::

::: notes
Kimball and Ross (2013, Chapter 3) explain surrogate keys: the warehouse should not depend on the source's keys, which can be reused, changed or collide when two sources are integrated (session 16: the supplier's article number was not our key). They also explain why a date dimension pays off: attributes such as weekday, holiday or fiscal period are hard to compute in SQL and should be stored once. Chapter 2 recommends avoiding null foreign keys in fact tables with a default dimension row. The date key 20261005 is a deliberate exception many teams use: readable and still an integer. The weather dimension holds the business rule of session 15 (rule column) — the threshold is a business decision, now documented.
:::

---

# Fact Tables

| Kind of fact | Can be summed … | Bike shop example |
|---|---|---|
| **Additive** | across **all** dimensions | quantity, revenue |
| **Semi-additive** | across some, **not over time** | bikes in stock at closing time |
| **Non-additive** | **never** — compute from additive parts | unit price, margin %, number of distinct receipts |

- **Transaction** fact table: one row per event (our receipt lines)
- **Periodic snapshot**: one row per period (stock at the end of each day)
- **Accumulating snapshot**: one row per process instance, updated at each milestone (a repair job: received → repaired → collected)

::: source
Based on Kimball and Ross (2013, Chapters 2 and 4).
:::

::: notes
Kimball and Ross (2013, Chapter 2) define additive, semi-additive and non-additive facts; Chapter 4 (inventory) introduces the three fact table types. Stock is the classic semi-additive fact: summing stock over shops is fine, summing it over days is nonsense (use the average or the last value). Non-additive: store the additive parts (revenue and quantity) and compute the ratio after aggregation — the average of percentages is not the percentage of the sums. Number of receipts: observed today, receipts per category 9 + 29 + 6 = 44, but there are only 35 receipts (many contain a bike and a helmet) — a count of distinct values cannot be summed across a dimension. Accumulating snapshot: only mention; not in the hands-on.
:::

---

# Mini Exercise: Fact or Dimension? {.exercise}

The workshop wants a star for **repair jobs** (session 8 data: `repair_job`, `repair_line`, `bike`, `customer`, `spare_part`, `job_mechanic`).

1. Name the business process and a suitable **grain**
2. Fact or dimension attribute? `quantity` · `price_charged` × `quantity` · `job_date` · `brand` · `qualification` of the mechanic · customer `city` · `list_price` · `name` of the part
3. Additive, semi-additive or non-additive? revenue · discount in % · number of open jobs at the end of each month
4. Repair line 508/P-110 has `price_charged` 0. Fact row or not?

::: notes
About 5 min in pairs, 3 min collection. Expected answers:
1 Process: repairing bikes (workshop). Grain: one spare part on one repair job (a repair_line row) — the finest available. One row per job is possible but loses the parts. Good students notice: jobs without lines (506, 512) then have no fact row.
2 Facts: quantity, revenue (price_charged × quantity). Dimension attributes: job_date (→ date dimension), brand (bike dimension), qualification (mechanic dimension), city (customer or bike dimension), list_price and part name (product dimension). Mechanics are M:N with jobs (session 4) — they do not fit the line grain directly; a separate fact table or a bridge table is needed (worksheet 17).
3 Revenue additive; discount % non-additive (store list value and revenue, compute the % after summing); open jobs at month end semi-additive (a periodic snapshot).
4 Yes: a free bell is a sale with revenue 0 — dropping it would lose quantity and make the free items invisible. Zero is a value, not a missing value (session 13).
:::

---

# Star or Snowflake?

![The same schema as a snowflake: dim_product keeps product_key, product_no and name and gets a foreign key group_key to a new table dim_product_group with group_key, product_group and category; date, salesperson and weather stay as in the star. One more join for every question by product group or category](img/dwh-snowflake.png){width=92%}

- **Star**: one denormalised table per dimension — fewer joins, easier to read, values repeat
- **Snowflake**: dimensions **normalised** into several tables — stored once, but more joins

::: source
Own illustration based on Kimball and Ross (2013, Chapter 3), Chaudhuri and Dayal (1997) and Elmasri and Navathe (2016, Chapter 29).
:::

::: notes
Chaudhuri and Dayal (1997) describe the snowflake schema as a refinement of the star where the dimensional hierarchy is represented explicitly by normalising the dimension tables, which eases maintenance; denormalised dimensions are easier to browse. Elmasri and Navathe (2016, Chapter 29) show star, snowflake and the fact constellation (several fact tables sharing dimensions). Kimball and Ross (2013, Chapter 3, "Resisting Normalization Urges") advise against snowflaking: dimension tables are small, the storage saving is tiny, and queries and users suffer. Exam: be able to draw both and name one advantage of each.
:::

---

# Loading the Star with SQL

```sql
INSERT INTO fact_sales (date_key, product_key, salesperson_key, weather_key,
                        receipt_no, line_no, quantity, revenue)
SELECT CAST(strftime('%Y%m%d', s.sale_date) AS INTEGER),          -- 20261005
       p.product_key, sp.salesperson_key,
       CASE WHEN w.day IS NULL  THEN 0                             -- unknown
            WHEN w.rain_mm >= 5 THEN 4  WHEN w.rain_mm >= 1 THEN 3 -- heavy, light rain
            WHEN w.t_max < 15   THEN 2  ELSE 1 END,                -- dry and cool, warm
       l.receipt_no, l.line_no, l.quantity, round(l.quantity * l.unit_price, 2)
FROM sale_line AS l
JOIN sale            AS s  ON s.receipt_no  = l.receipt_no
JOIN dim_product     AS p  ON p.product_no  = l.product_no        -- surrogate key lookup
JOIN dim_salesperson AS sp ON sp.employee_no = s.employee_no
LEFT JOIN weather_daily AS w ON w.day = s.sale_date AND w.station = 'Mannheim';
```

- Dimensions first, then the fact table: **look up** the surrogate keys by the natural keys
- **54** fact rows, revenue **18,866.80** — the same as the till's daily totals

::: source
Own example; based on Kimball and Ross (2013, Chapters 3 and 19).
:::

::: notes
All observed. This is the T and L of session 16, now as ELT inside SQLite: the operational tables are the source, the star is the target. Kimball and Ross (2013, Chapter 19) name the surrogate key pipeline as an ETL subsystem: replace natural keys by surrogate keys while loading facts. The LEFT JOIN on the weather plus the CASE … THEN 0 keeps a sale even when the weather is missing — the unknown row. Reconciliation: sum of revenue per day = till_daily.revenue for all six days — the "does the warehouse agree with the source?" check that every load should run (session 16, checks). PRAGMA foreign_key_check returns no rows. In a real pipeline this load would be an upsert per day (session 16).
:::

---

# Conformed Dimensions and the Bus Matrix

| Business process | Date | Product | Employee | Weather | Bike | Supplier |
|---|---|---|---|---|---|---|
| Till sales | ✓ | ✓ | ✓ | ✓ | | |
| Repairs | ✓ | ✓ (parts) | ✓ (mechanic) | | ✓ | |
| Purchasing | ✓ | ✓ (parts) | | | | ✓ |

- A **conformed dimension** means the same in every star: same keys, same attributes, same values
- Then stars can be **combined** ("drill across"): parts sold at the till **and** used in the workshop
- The **bus matrix** is the plan of a Kimball warehouse: one row per process, one column per dimension

::: source
Based on Kimball and Ross (2013, Chapter 4).
:::

::: notes
Kimball and Ross (2013, Chapter 4) introduce the enterprise data warehouse bus architecture and the bus matrix: rows are business processes, columns are dimensions, a mark says which dimension is used where. It is a planning tool for the bottom-up approach — this is how Kimball answers Inmon's integration argument. Example of a non-conformed dimension: the till calls the inner tube product A-17, the workshop P-101 — then "parts sold and used" cannot be compared. In our data the till uses the workshop's part numbers on purpose (product.part_no). Worksheet 17 builds the repair star and drills across.
:::

---

# Slowly Changing Dimensions {.optional}

The rain cape moves from **Accessories** to a new group **Clothing** on 1 November. What happens to October's report?

| Type | What the load does | October report afterwards |
|---|---|---|
| **Type 1** | overwrite the attribute | shows **Clothing** — history rewritten |
| **Type 2** | add a **new row** with a new surrogate key, valid from 1 Nov | shows **Accessories** — history kept |

::: source
Based on Kimball and Ross (2013, Chapter 2).
:::

::: notes
Self-study. Kimball and Ross (2013, Chapter 2) list the techniques for slowly changing dimension attributes, from type 0 (keep the original) to hybrid types; types 1 and 2 are the most common. Type 2 is why surrogate keys matter: the product A-04 then has two rows (two product_keys) with the same product_no. Data Analytics (semester 5) treats this in depth; in this course it is enough to know that dimension changes need a decision.
:::

---

# OLAP {.section}

Questions in many dimensions

---

# The Data Cube

![A data cube with three dimensions: weather type (dry and warm, dry and cool, light rain, heavy rain), product group (E-bikes, Bikes, Parts, Accessories, Service) and salesperson (Marco, Laura). One cell is the revenue of one product group, weather type and salesperson. The slice weather type = heavy rain is highlighted](img/dwh-cube.png){width=70%}

- The star schema stores the data; OLAP tools and SQL show it as a **cube** of measures by dimensions

::: source
Own illustration based on Chaudhuri and Dayal (1997) and Elmasri and Navathe (2016, Chapter 29).
:::

::: notes
Chaudhuri and Dayal (1997) describe the multidimensional view: measures in a cube whose axes are the dimensions, each dimension with a hierarchy. The cube is a way of thinking, not necessarily a storage format: ROLAP tools compute it from star schemas with SQL, MOLAP tools store it in special structures (mention only; Data Analytics, semester 5). Three dimensions fit on a slide; real cubes have more (date is the fourth here). Most cells of a real cube are empty (sparse): e.g. no Service on bad days in our week.
:::

---

# OLAP Operations

| Operation | What it does | Bike shop example |
|---|---|---|
| **Roll-up** | aggregate along a hierarchy, less detail | product → product group → **category** |
| **Drill-down** | the reverse, more detail | category Bikes → E-bikes, Bikes → models |
| **Slice** | fix **one** dimension to one value | only `weather_type = 'heavy rain'` |
| **Dice** | select a sub-cube on **several** dimensions | parts and accessories, Mon–Fri, all weather types |
| **Pivot** | rotate: swap rows and columns | product groups as rows, good/bad days as columns |

- In SQL: roll-up and drill-down change the **`GROUP BY`**, slice and dice add **`WHERE`**, pivot turns values into **columns**

::: source
Based on Chaudhuri and Dayal (1997) and Elmasri and Navathe (2016, Chapter 29).
:::

::: notes
Definitions as in Chaudhuri and Dayal (1997): roll-up increases the level of aggregation along a hierarchy, drill-down decreases it; slice and dice are selection and projection; pivot re-orients the multidimensional view. Elmasri and Navathe (2016, Chapter 29) give the same operations with figures. Observed numbers for the examples: category totals Bikes 16,491.00, Parts and accessories 2,081.80, Service 294.00; drill-down Bikes → E-bikes 12,196.00 and Bikes 4,295.00. SQL databases such as PostgreSQL offer GROUP BY ROLLUP and CUBE for subtotals; SQLite 3.45 does not (observed: "no such function: rollup") — not needed today.
:::

---

# OLAP in SQL: A Pivot by Bike Day

```sql
SELECT p.product_group,
       round(sum(CASE WHEN w.bike_day = 'good' THEN f.revenue ELSE 0 END), 2) AS good_days,
       round(sum(CASE WHEN w.bike_day = 'bad'  THEN f.revenue ELSE 0 END), 2) AS bad_days,
       round(sum(f.revenue), 2)                                                AS total
FROM fact_sales AS f
JOIN dim_product AS p ON p.product_key = f.product_key
JOIN dim_weather AS w ON w.weather_key = f.weather_key
GROUP BY p.product_group
ORDER BY total DESC;
```

| product_group | good_days | bad_days | total |
|---|---|---|---|
| E-bikes | 8,597.00 | 3,599.00 | 12,196.00 |
| Bikes | 299.00 | 3,996.00 | 4,295.00 |
| Accessories | 958.10 | 588.80 | 1,546.90 |
| Parts | 228.30 | 306.60 | 534.90 |
| Service | 294.00 | 0.00 | 294.00 |

::: source
Own example; based on Kimball and Ross (2013, Chapter 3).
:::

::: notes
All observed. The pattern of every star query: fact table, join the dimensions you need, filter with WHERE (slice/dice), group by dimension attributes (roll-up/drill-down), and CASE inside sum to turn values into columns (pivot) — the conditional aggregation of session 10. Three good days (Mon–Wed) and three bad days (Thu–Sat). Ask before showing the result: what do you expect? Many expect "bad days: less of everything". Then let them read the table — next slide.
:::

---

# Reading the Result Carefully

- Bad days: **8,490.40** revenue on 3 days, good days **10,376.40** on 3 days — 2,830.13 vs. 3,458.80 per day
- But **bikes** sold better on bad days — because the "bad" days include **Saturday**, the best shopping day
- Rain capes: 5 of 9 sold on bad days, **none** on the heavy-rain Thursday
- **One week** cannot separate weather and weekday: we need months of data — which is what the warehouse collects every day

::: callout
A star schema makes questions **easy to ask**. It does not make the answers **true**: check the grain, the additivity and what else differs between the groups.
:::

::: source
Own example (fictional till data); weather data: Deutscher Wetterdienst via de Maeyer (n.d.).
:::

::: notes
All observed: per weather type, dry and warm 3 days 10,376.40, dry and cool (Fri) 1,530.00, light rain (Sat) 5,980.00, heavy rain (Thu) 980.40. Average revenue per receipt: good days 546.13 (19 receipts), bad days 530.65 (16 receipts) — almost the same; the difference is the number of customers. Saturday's light rain (1.6 mm) did not keep customers away. This is confounding — a second dimension (day type) explains the effect: dice by day_type = 'Mon-Fri' and the comparison becomes fairer (worksheet). Links: session 13 (data quality: fitness for use) and the overarching competence of the module — reflect critically whether the data is suitable for the business question.
:::

---

# Exercise: The Bike Shop Star {.exercise}

Load `bikeshop-sales-session17.sql`. Predict first, then run.

1. **Check the source**: revenue per day from `sale_line` — does it match the till export of session 16?
2. **Design** (paper, before opening the model): the four steps for the till, then draw your star
3. **Build**: run `bikeshop-star-session17.sql`. Compare it with your design. Why `weather_key` 0? Why `product_key` and not `product_no`?
4. **OLAP**: write one query each for roll-up, drill-down, slice, dice and pivot
5. **Read**: do bad bike days cost revenue? Compare **Mon–Fri** only. What would you tell the owner?
6. **Snowflake**: move `product_group` and `category` into `dim_product_group`. What changes in your queries?

::: source
Own example; till data fictional; weather data: Deutscher Wetterdienst via de Maeyer (n.d.), CC BY 4.0.
:::

::: notes
About 40 min + 5 min comparison. Expected answers (all observed):
1 2026-10-05 2,840.50 · 10-06 3,125.00 · 10-07 4,410.90 · 10-08 980.40 · 10-09 1,530.00 · 10-10 5,980.00 — equal to the till export (Umsatz); receipts per day 5, 7, 7, 4, 5, 7.
2 Process: selling at the till; grain: receipt line; dimensions date, product, salesperson, weather; facts quantity, revenue. Accept designs with weather attributes in a daily dimension, and with a customer dimension marked "not available (walk-ins)".
3 dim_date 31, dim_product 18, dim_salesperson 2, dim_weather 5, fact_sales 54 rows. Key 0 = unknown weather (no NULL foreign key; e.g. a day the pipeline missed). Surrogate key: independent of the till's numbering, allows history (type 2), integer joins.
4 e.g. roll-up: revenue per category (Bikes 16,491.00 · Parts and accessories 2,081.80 · Service 294.00); drill-down: Bikes → product (KTM Macina Style 2 × = 7,198.00, Gazelle Ultimate 4,998.00, Trek Marlin 7 2,198.00, Cube Touring 1,798.00, Cube Kid 200 299.00); slice: bike_day = 'bad' by product group (Bikes 3,996.00, E-bikes 3,599.00, Accessories 588.80, Parts 306.60); dice: parts and accessories, Mon–Fri, by weather type (dry and warm 1,186.40 · dry and cool 431.00 · heavy rain 81.40); pivot: the slide's query, or weekday × category.
5 All days: bad 2,830.13 vs. good 3,458.80 per day. Mon–Fri only: good days 3,458.80 per day vs. Thursday 980.40 and Friday 1,530.00 — on weekdays the bad days look clearly worse. Advice: a hint, not a proof — one week, two bad weekdays; collect data for months, compare like with like (weekday with weekday).
6 CREATE TABLE dim_product_group (group_key INTEGER PRIMARY KEY, product_group TEXT UNIQUE, category TEXT); fill it with SELECT DISTINCT; give dim_product a group_key. Every query by group or category needs one more JOIN; results are identical (check the category totals).
:::

---

# Team Work: Your Star for Milestone 5 {.exercise}

1. Which **business process** of your case matters most for analysis?
2. Declare the **grain**: what is one row of your fact table?
3. Which **dimensions** describe it — and which attributes and hierarchies do they have?
4. Which **facts** — additive or not?
5. Draw the **star**. Which dimension could a second star share with it?

::: callout
Milestone 5 (star schema): a star schema for your project case — business process, grain, dimension and fact tables with keys — and three analytical questions it answers.
:::

::: notes
About 12 min. Teams draw on paper or in draw.io; walk around and ask: what is one row? (The most common error is a vague grain such as "sales".) Can your dimension attributes be read in a report heading? Is there a date dimension? Which facts must not be summed? Teams with a small or unusual case: one fact table with three or four dimensions is enough. Milestone 5 is due after today; the exact deliverables are in the project brief. Teams may build the star in SQLite from their milestone 4 tables — optional, but a strong basis for the final presentation.
:::

---

# Key Takeaways

- A **data warehouse** separates analysis from operations: **subject-oriented, integrated, nonvolatile, time-variant** (Inmon)
- **Inmon** builds a normalised enterprise DWH **top-down**; **Kimball** builds dimensional stars **bottom-up**, joined by **conformed dimensions**
- Dimensional design in **four steps**: business process, **grain**, dimensions, facts
- **Star**: one fact table with keys and measures, denormalised dimension tables; **snowflake**: normalised dimensions, more joins
- Facts are **additive**, **semi-additive** or **non-additive** — sum only what may be summed
- **OLAP**: roll-up, drill-down, slice, dice, pivot — in SQL: `GROUP BY`, `WHERE`, `CASE`

::: source
Inmon (2005); Kimball and Ross (2013).
:::

---

# Next Session: Modern Data Architectures

- Beyond the warehouse: **data lake** and **lakehouse**
- **Data mesh** and **data fabric**: architecture as an organisational question
- **Cloud** data platforms
- Choosing an architecture: case comparison

::: callout
**Preparation:** finish the hands-on and worksheet 17; submit milestone 5. Think: the shop wants to keep **photos of damaged bikes** and the **raw API responses** for later. Would you put them into the star schema — and if not, where?
:::

---

# References {.references}

- Chaudhuri, S., & Dayal, U. (1997). An overview of data warehousing and OLAP technology. *ACM SIGMOD Record, 26*(1), 65–74. https://doi.org/10.1145/248603.248616
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Inmon, W. H. (2005). *Building the data warehouse* (4th ed.). Wiley.
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
