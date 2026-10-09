---
course: Data Analytics
session: 3
title: Dimensional Data and OLAP
subtitle: Star and snowflake schema · facts, dimensions, hierarchies · slowly changing dimensions · OLAP operations
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Dimensional Data and OLAP {.title}

::: notes
Time plan for today (3 h): recap 10 min · reading a dimensional model 25 min · hierarchies 10 min · break 10 min · OLAP cube and operations 30 min · lab 80 min · wrap-up 5 min · ~10 min buffer.
Model design (four steps, slowly changing dimensions) is taught in Data Engineering (W4DSKI_401) — those slides are optional self-study here. If 401 has not covered star schemas yet, spend 10 more minutes on them and shorten the lab.
Students need their tpch.duckdb file from session 2. If someone lost it, the first lab cell recreates it (internet access needed for the extension download).
:::

---

# Today's Agenda

1. Recap: what you found in the TPC-H warehouse
2. Dimensional modelling: facts, measures, dimensions
3. Star and snowflake schema
4. Hierarchies — and why history in dimensions matters
5. The OLAP cube and its operations
6. Lab: build a star schema and answer questions with OLAP operations

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:10 Facts, dimensions, star and snowflake (input + discussion) · 0:35 Hierarchies (input) · 0:45 Break · 0:55 OLAP cube and operations (input + mini exercise) · 1:25 Lab (pairs) · 2:45 Wrap-up · ~10 min buffer.
:::

---

# Recap: TPC-H Is Not a Star

- Revenue per region needed **five joins**: lineitem → orders → customer → nation → region
- TPC-H is **normalised** — built to avoid redundancy, not to make analysis easy
- Today we turn it into a **dimensional model**

::: callout
Dimensional modelling trades a little redundancy for queries that are **simple, fast and understandable** to business users.
:::

::: source
Kimball and Ross (2013).
:::

::: notes
Link back to task 5 of the session 2 lab. Ask a pair to show their join query. Kimball and Ross stress understandability and query performance as the two goals of dimensional modelling.
:::

---

# Dimensional Modelling {.section}

Facts, measures and dimensions

---

# Facts and Dimensions

::: cards
### Fact table
Records the **measurements** of a business process, one row per event at a defined grain. Example: one row per sales line.

### Measures
Numeric, usually **additive** values in the fact table: revenue, quantity, discount.

### Dimension tables
The **context** of the measurements: who, what, where, when. Descriptive attributes used for filtering and grouping.
:::

::: source
Based on Kimball and Ross (2013).
:::

::: notes
Additivity matters: revenue can be summed over all dimensions; an account balance (semi-additive) cannot be summed over time; a unit price or a ratio (non-additive) cannot be summed at all — store its components instead. Ask students for an example of each.
:::

---

# Four Steps of Dimensional Design {.optional}

1. **Select the business process** — e.g. sales, orders, shipments
2. **Declare the grain** — what exactly does one fact row represent?
3. **Identify the dimensions** — who, what, where, when, why, how
4. **Identify the facts** — the numeric measures at that grain

::: callout
The **grain** comes first. Mixing grains in one fact table (e.g. order lines and order totals) leads to double counting.
:::

::: source
Kimball and Ross (2013).
:::

::: notes
Self-study — designing dimensional models is taught in Data Engineering (W4DSKI_401); here students only need to read a model and know its grain. Kimball and Ross call declaring the grain the most important step. Example: grain "one row per order line" allows analysis by product; grain "one row per order" does not. Atomic (finest) grain is the safest choice because it can always be rolled up.
:::

---

# Star Schema

::: columns
**Fact table in the centre**

`fact_sales`
- date_key, customer_key, part_key (foreign keys)
- quantity, revenue (measures)
|||
**Dimensions around it**

- `dim_date`: day to year
- `dim_customer`: segment, nation, region
- `dim_part`: brand, type
:::

::: callout
Each dimension is **one denormalised table**: nation and region sit directly in the customer dimension — one join per dimension.
:::

::: source
Own example based on Kimball and Ross (2013), using TPC-H data (Transaction Processing Performance Council, n.d.).
:::

::: notes
This is exactly the star schema students build in today's lab. Draw it on the whiteboard as a star. Point out the redundancy: "EUROPE" is repeated for every European customer — acceptable because dimension tables are small compared with fact tables (TPC-H sf 0.1: 15,000 customers vs. 600,572 sales lines).
:::

---

# Star vs. Snowflake Schema

| | Star schema | Snowflake schema |
|---|---|---|
| Dimensions | One denormalised table per dimension | Normalised into several tables (e.g. customer → nation → region) |
| Redundancy | Higher | Lower |
| Joins per query | Fewer | More |
| Understandability | High | Lower |
| Typical use | Data marts, BI tools | When dimensions are very large or shared sub-dimensions are needed |

::: source
Based on Kimball and Ross (2013) and Chaudhuri and Dayal (1997).
:::

::: notes
Kimball and Ross generally advise against snowflaking: the storage saving is small, and usability and performance suffer. Chaudhuri and Dayal describe the snowflake as a refinement where hierarchies are normalised. TPC-H's customer–nation–region chain is a snowflake-like structure.
:::

---

# Hierarchies and Changing Dimensions {.section}

Levels of detail and history

---

# Hierarchies in Dimensions

::: layers
- Year: 1992 … 1998
- Quarter: Q1 … Q4
- Month: January … December
- Day: The grain of the date dimension
:::

- Other examples: **region → nation → customer**, **manufacturer → brand → part**
- Hierarchies define the paths for **drill-down** and **roll-up**

::: source
Own illustration based on Kimball and Ross (2013).
:::

::: notes
A date dimension is one of the most important dimensions; real warehouses add attributes such as weekday, holiday flag, fiscal period. Mention that hierarchies are not always clean (a week can span two months) — a classic source of wrong reports.
:::

---

# Slowly Changing Dimensions {.optional}

A customer moves from Mannheim to Hamburg. What happens to last year's sales by city?

| Type | Technique | Effect on history |
|---|---|---|
| 1 | Overwrite the old value | History is restated: old sales now appear under Hamburg |
| 2 | Add a new row with a new surrogate key and validity dates | History is preserved: old sales stay in Mannheim |
| 3 | Add a column for the previous value | Only one prior value is kept |

::: source
Kimball and Ross (2013).
:::

::: notes
Self-study (design topic of Data Engineering). For analysts the key point: check whether a dimension keeps history before comparing periods. Type 2 is the most common technique when history matters; it needs surrogate keys because the same customer now has several rows. Kimball and Ross describe further types (0, 4–7) — not exam-relevant here. Ask: which type would a tax office need, which a marketing dashboard?
:::

---

# Type 2 in Practice {.optional}

| customer_key | customer_id | city | valid_from | valid_to | current |
|---|---|---|---|---|---|
| 1017 | C-102 | Mannheim | 2021-03-01 | 2025-06-30 | no |
| 2389 | C-102 | Hamburg | 2025-07-01 | 9999-12-31 | yes |

- Facts before July 2025 point to key 1017, later facts to 2389
- Queries on the **current** state filter on `current = yes`

::: source
Own example based on Kimball and Ross (2013).
:::

::: notes
Self-study. The business key (customer_id) stays the same; the surrogate key changes. The far-future end date is a common convention for the open interval.
:::

---

# OLAP {.section}

Analysing data as a cube

---

# The OLAP Cube

- Think of the data as a **cube**: each axis is a dimension, each cell holds measures
- Example: revenue by **region × year × segment**
- Real cubes have many more dimensions — "hypercube"
- The **CUBE** operator in SQL computes the aggregates for all combinations of the grouping columns

::: callout
OLAP lets analysts move through the cube **interactively** — fast enough to follow a train of thought.
:::

::: source
Based on Chaudhuri and Dayal (1997) and Gray et al. (1997).
:::

::: notes
Gray et al. introduced the CUBE operator, which generalises GROUP BY, cross-tabs and subtotals. The SQL syntax (ROLLUP, CUBE, GROUPING SETS) is the topic of session 4. Today: the operations conceptually and with plain GROUP BY.
:::

---

# OLAP Operations

| Operation | What it does | Example |
|---|---|---|
| Roll-up | Aggregate to a higher hierarchy level | Revenue per nation → per region |
| Drill-down | Go to a more detailed level | Revenue per year → per quarter |
| Slice | Fix one dimension to a single value | Only year 1997 |
| Dice | Select a sub-cube with conditions on several dimensions | Asia, 1997, segments Building and Automobile |
| Pivot | Rotate the view: swap rows and columns | Regions as rows, years as columns |

::: source
Based on Chaudhuri and Dayal (1997).
:::

::: notes
In SQL: roll-up/drill-down = fewer/more GROUP BY columns along a hierarchy; slice/dice = WHERE conditions; pivot = presentation (PIVOT statement or the BI tool). Ask students which of these operations they use in Excel pivot tables — they all do.
:::

---

# Mini Exercise: Name the Operation {.exercise}

A sales manager works with a report on revenue by region and year. Which operation is she using?

1. She clicks on "Europe" to see the individual countries
2. She shows only the figures for 2025
3. She switches the report so that years are rows and regions are columns
4. She looks at the total for all regions together
5. She limits the view to Germany and France in Q1 and Q2 for the segment Building

::: notes
Answers: 1 drill-down · 2 slice · 3 pivot · 4 roll-up · 5 dice. Two minutes, plenary.
:::

---

# Lab: Star Schema and OLAP {.section}

DuckDB and the TPC-H data from session 2

---

# Lab Step 1: Build the Star Schema

```python
import duckdb
con = duckdb.connect("tpch.duckdb")
con.sql("""
CREATE OR REPLACE TABLE dim_customer AS
SELECT c_custkey AS customer_key, c_name AS customer,
       c_mktsegment AS segment, n_name AS nation, r_name AS region
FROM customer JOIN nation ON c_nationkey = n_nationkey
              JOIN region ON n_regionkey = r_regionkey;
CREATE OR REPLACE TABLE dim_date AS
SELECT DISTINCT o_orderdate AS date_key, year(o_orderdate) AS year,
       quarter(o_orderdate) AS quarter, month(o_orderdate) AS month
FROM orders;
CREATE OR REPLACE TABLE fact_sales AS
SELECT o_orderdate AS date_key, o_custkey AS customer_key,
       l_partkey AS part_key, l_quantity AS quantity,
       l_extendedprice * (1 - l_discount) AS revenue
FROM lineitem JOIN orders ON l_orderkey = o_orderkey;
""")
```

::: notes
Tested with DuckDB 1.5.6, sf 0.1: fact_sales has 600,572 rows, dim_customer 15,000, dim_date 2,406. If tpch.duckdb is missing, run the setup from session 2 first (INSTALL tpch; LOAD tpch; CALL dbgen(sf = 0.1)). Task 1 below asks students to add dim_part themselves.
The date key is the date itself here for simplicity; real warehouses often use integer keys such as 19970315.
:::

---

# Lab Step 2: Tasks {.exercise}

Work in pairs. Write the queries and your interpretation in a notebook.

1. **Model:** create `dim_part` (part, brand, manufacturer, type). What is the **grain** of `fact_sales`?
2. **Roll-up and drill-down:** revenue per region and year; then drill down into Europe 1997 by nation
3. **Slice and dice:** revenue per segment and quarter for Asia in 1997, segments Building and Automobile only
4. **Pivot:** regions as rows, years 1995–1997 as columns (DuckDB `PIVOT`)
5. **Check:** how many customers have **no** sales? What does that mean for "revenue per customer"?
6. **Reflect:** which changes in `dim_customer` would require a slowly changing dimension?

::: notes
Solution sketches (tested, DuckDB 1.5.6, sf 0.1):
1 CREATE TABLE dim_part AS SELECT p_partkey AS part_key, p_name AS part, p_brand AS brand, p_mfgr AS manufacturer, p_type AS part_type FROM part; grain = one row per order line (lineitem).
2 SELECT region, year, sum(revenue) FROM fact_sales JOIN dim_customer USING (customer_key) JOIN dim_date USING (date_key) GROUP BY ALL ORDER BY ALL; Europe 1997 by nation: Germany is highest (about 129.5 million), all five nations between about 120 and 130 million.
3 add WHERE region = 'ASIA' AND year = 1997 AND segment IN ('BUILDING', 'AUTOMOBILE') and GROUP BY segment, quarter: values about 26–33 million per cell.
4 PIVOT (SELECT region, year, revenue FROM ... WHERE year BETWEEN 1995 AND 1997) ON year USING sum(revenue) GROUP BY region;
5 only 10,000 of 15,000 customers have orders (TPC-H generates a third of customers without orders). Average revenue per customer differs depending on whether you divide by all customers or by active customers — a classic definition question.
6 nation (customer moves), market segment (reclassification), name — discuss type 1 vs. type 2.
:::

---

# Discussion: What Did You Learn?

- How much simpler were the queries compared with session 2?
- Where did you have to **decide on a definition** (e.g. "revenue per customer")?
- Which dimension would you add for the retailer from session 2?

::: notes
Collect answers. Key message: the dimensional model makes queries simpler, but the analyst still has to define measures carefully. The star schema and queries are a good basis for portfolio notebook 1.
:::

---

# Key Takeaways

- Dimensional models separate **facts** (measures at a declared grain) from **dimensions** (context)
- The **star schema** uses one denormalised table per dimension; the **snowflake** normalises them
- **Hierarchies** in dimensions enable drill-down and roll-up
- Check the **grain** of a fact table and whether dimensions keep **history** before you interpret results
- **OLAP operations** — roll-up, drill-down, slice, dice, pivot — map to GROUP BY, WHERE and PIVOT in SQL

---

# Next Session: Analytical SQL

- Window functions: rankings, running totals, moving averages
- `ROLLUP`, `CUBE` and `GROUPING SETS`
- Common table expressions (CTEs)
- Typical analyses: cohorts and funnels

::: callout
**Preparation:** keep your star schema in `tpch.duckdb` — we will query it with analytical SQL.
:::

---

# References {.references}

- Chaudhuri, S., & Dayal, U. (1997). An overview of data warehousing and OLAP technology. *ACM SIGMOD Record, 26*(1), 65–74. https://doi.org/10.1145/248603.248616
- Gray, J., Chaudhuri, S., Bosworth, A., Layman, A., Reichart, D., Venkatrao, M., Pellow, F., & Pirahesh, H. (1997). Data cube: A relational aggregation operator generalizing group-by, cross-tab, and sub-totals. *Data Mining and Knowledge Discovery, 1*(1), 29–53. https://doi.org/10.1023/A:1009726021843
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 9, 2026, from https://www.tpc.org/tpch/
