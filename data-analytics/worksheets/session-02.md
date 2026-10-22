---
course: Data Analytics
session: 2
title: Data Warehouse Architectures
subtitle: Practice tasks on OLTP and OLAP, the data warehouse definition, the reference architecture and exploring TPC-H in DuckDB
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 2 on your own or in the lab. Tasks 1–3 need only paper and pencil. Tasks 4 and 5 use the TPC-H sample warehouse (Transaction Processing Performance Council, n.d.) in DuckDB (Raasveldt & Mühleisen, 2019) from the session lab (`tpch.duckdb`, scale factor 0.1). If you do not have the file yet, create it with the code from the lab setup slide:

```python
import duckdb
con = duckdb.connect("tpch.duckdb")
con.sql("INSTALL tpch; LOAD tpch; CALL dbgen(sf = 0.1)")
```

Task 6 is a short written recommendation in the style of the portfolio notebooks.

## OLTP or OLAP?

A **hospital** runs several information systems. Decide for each request whether it is a typical **OLTP** or **OLAP** workload, and give a one-line reason.

1. Admit a patient and assign a bed on ward 3.
2. Average length of stay per diagnosis group and quarter over the last five years.
3. Show the current medication plan of patient 4711.
4. Which wards had an occupancy above 95 % on more than 20 days last year?
5. Record a blood test result from the laboratory.
6. Compare the number of emergency admissions on public holidays with normal weekdays.

::: answer lines=6
:::

::: solution
1. **OLTP**: inserts and updates single records in a running process.
2. **OLAP**: aggregates many records over a long history.
3. **OLTP**: reads one business object in its current state.
4. **OLAP**: aggregates occupancy over a year with a condition per ward and day.
5. **OLTP**: a single insert in the operational system.
6. **OLAP**: compares aggregates across a calendar attribute (holiday flag), typical for a date dimension.

Pattern (Chaudhuri & Dayal, 1997): OLTP works on single current records with high throughput; OLAP reads and aggregates many historical records.
:::

## What Makes It a Data Warehouse?

Inmon (2005) defines a data warehouse as **subject-oriented, integrated, time-variant** and **non-volatile**. Each of the following statements describes a system that **violates** one of these characteristics. Name the characteristic and suggest a fix.

1. Every night, the customer table in the warehouse is overwritten with the current state from the CRM system.
2. The marketing mart stores country codes as "DE", the sales mart as "GER" and the finance mart as "276".
3. The warehouse has one table per source application: `sap_tables`, `shop_tables`, `crm_tables`, each copied one to one.
4. Analysts can correct wrong sales figures directly in the warehouse tables with `UPDATE`.

::: answer lines=8
:::

::: solution
1. **Time-variant** (and non-volatile): overwriting loses history; last year's sales can no longer be analysed by the customer's address at that time. Fix: keep history, e.g. with validity dates (slowly changing dimension type 2, session 3).
2. **Integrated**: the same meaning is encoded differently. Fix: map all sources to one agreed code (e.g. ISO 3166 alpha-2) during ETL; a conformed country dimension.
3. **Subject-oriented**: organised by application instead of business subject. Fix: model subjects such as customer, product and sales across all sources.
4. **Non-volatile**: data is changed by users after loading, so reports cannot be reproduced. Fix: correct errors in the source or through a documented correction load; keep the warehouse read-only for analysts.
:::

## Where Do I Find It — and Can I Trust It?

A retail analyst has access to all layers of the reference architecture (staging, core data warehouse, data marts, reports and dashboards). For each request, say **which layer** she should use and **what she must check** before she reports the result.

1. The CFO wants the official revenue figure for the last quarter for the annual report.
2. A data scientist needs every individual web shop order of the last three years, including cancelled ones, for a churn model.
3. A store manager asks why the dashboard shows 3 % lower revenue than his cash register system.
4. A product manager wants to test a new idea: does the weather influence ice-cream sales? Weather data is not yet in the warehouse.

::: answer lines=8
:::

::: solution
1. **Reports or the finance data mart**: the agreed KPI. Check the definition (net or gross, after returns, which date) and that the quarter is closed and completely loaded.
2. **Core data warehouse**: integrated, historised and detailed. Check whether cancelled orders are kept or filtered out in the core layer, and how far back the history goes.
3. Compare **mart/dashboard** definitions with the **source** (via staging or core): typical causes are returns or discounts treated differently, a different date (order vs. payment date), late-loaded data or store assignments. The layers table of the session: marts are "already aggregated or filtered — check the definitions".
4. The weather data is **not** in the warehouse, so she combines core or mart sales data with an external source in her own analysis environment (sandbox, notebook, or lakehouse). Check the granularity (daily, per store location) and that the join keys (date, region) match. If the analysis proves useful, the weather data should be loaded properly into the warehouse.
:::

## Explore the TPC-H Warehouse

Open `tpch.duckdb` in a Jupyter notebook.

1. Count the rows of all eight tables. Which tables are large and which are small? What does that tell you about facts and context?
2. How many line items does an order have on average, and what are the minimum and maximum? Write the query.
3. `orders` has a column `o_totalprice`. Check with a query whether it equals the sum of its line items, and find out which formula matches: `l_extendedprice * (1 - l_discount)` or `l_extendedprice * (1 - l_discount) * (1 + l_tax)`.
4. Why would summing `o_totalprice` after joining `orders` with `lineitem` give a wrong total? Show it with numbers.

::: hint
For task 2, first count line items per `l_orderkey` in a subquery, then aggregate the counts. For task 3, aggregate `lineitem` per order in a CTE and join it to `orders`; compare with a tolerance (rounding), e.g. `abs(a - b) < 1`.
:::

::: answer lines=10
:::

::: solution
Expected results (DuckDB 1.5, sf 0.1):

1. lineitem 600,572 · orders 150,000 · partsupp 80,000 · part 20,000 · customer 15,000 · supplier 1,000 · nation 25 · region 5. The large tables (lineitem, orders) record business events — they hold the facts (measures such as quantity, price, discount). The small tables describe context (who, what, where).
2. On average 4.0 line items per order (minimum 1, maximum 7):

```sql
SELECT avg(n), min(n), max(n)
FROM (SELECT l_orderkey, count(*) AS n FROM lineitem GROUP BY l_orderkey);
```

3. `o_totalprice` matches the **gross** formula including tax, up to rounding (differences of a few cents per order):

```sql
WITH l AS (
  SELECT l_orderkey, sum(l_extendedprice * (1 - l_discount) * (1 + l_tax)) AS s
  FROM lineitem GROUP BY l_orderkey)
SELECT count(*) AS orders, count(*) FILTER (WHERE abs(s - o_totalprice) < 1) AS matching
FROM l JOIN orders ON l_orderkey = o_orderkey;
```

All 150,000 orders match. Totals: sum of `o_totalprice` 21,356.6 million; net revenue `sum(l_extendedprice * (1 - l_discount))` 20,535.1 million. Two legitimate "revenue" figures differ by 4 % — exactly the definition problem from the session.

4. After the join, each order appears once **per line item**, so its `o_totalprice` is counted about four times: the sum becomes 106,851.4 million instead of 21,356.6 million. The two tables have different **grains** (order vs. order line); measures must be summed at their own grain. This prepares the grain discussion of session 3.
:::

## How Complete Is the Data?

Before you report numbers, check what the data covers.

1. Find the first and last **order date** and the first and last **ship date**. What do you notice?
2. Compute net revenue per year once by **order year** and once by **ship year**. Which years differ most, and why?
3. `l_returnflag` marks returned line items with `R` (the other values are `A` and `N`). How much of the net revenue comes from **returned** line items? What does this mean for a KPI called "revenue"?
4. Write two sentences you would add as a warning under a chart of "revenue per year" from this warehouse.

::: answer lines=10
:::

::: solution
Expected results (DuckDB 1.5, sf 0.1):

1. Orders: 1992-01-01 to 1998-08-02. Ship dates: 1992-01-03 to 1998-12-01. Line items are shipped up to about four months after the order, so the ship dates run later than the order dates.
2. Net revenue in million:

| Year | By order year | By ship year |
|---|---|---|
| 1992 | 3,124.6 | 2,615.4 |
| 1993–1997 | 3,064–3,151 | 3,057–3,143 |
| 1998 | 1,859.3 | 2,366.8 |

The edges differ most: by ship year, 1992 is lower (orders from late 1991 do not exist, so early 1992 has few shipments) and 1998 is higher (orders from mid-1998 are shipped until December). Query: `SELECT year(l_shipdate), sum(l_extendedprice * (1 - l_discount)) FROM lineitem GROUP BY ALL ORDER BY ALL;` and the same by `year(o_orderdate)` with a join to `orders`.

3. Returned line items account for 5,071.8 of 20,535.1 million, about 24.7 % (`SELECT l_returnflag, sum(...) FROM lineitem GROUP BY ALL`). A "revenue" KPI must state whether returns are included; a net-after-returns definition would be about a quarter lower. (High return rates are a property of the synthetic data, not of real wholesale.)

4. Example: "1998 contains orders only until 2 August, so the 1998 value is not comparable with earlier years. Revenue is net of discounts, by order date, including returned items." Accept any warning that covers completeness and the definition.
:::

## Portfolio-Style Task: Recommend an Architecture

A regional **chain of 40 fitness studios** wants to analyse memberships, check-ins and course bookings. Data comes from a membership system (SQL database), a check-in system (one CSV export per studio and day), and a booking app (JSON events via an API, about 2 million events per year). There are two business analysts who know SQL and Excel, and no data engineers. Management wants a monthly KPI report and, later, a churn prediction.

Write a recommendation (about 200 words) for an analytical architecture. Use the concepts from the session: layers, Inmon vs. Kimball (Inmon, 2005; Kimball & Ross, 2013), data lake, lakehouse, or an analytical database such as DuckDB. Justify your choice and name one risk.

::: answer lines=14
:::

::: solution
Marking guide (10 points):

- **Analyses the situation** (2 points): small to moderate volume (millions of rows, not billions), three heterogeneous sources incl. semi-structured JSON, few technical staff, two different uses (stable KPIs and later ML).
- **Coherent architecture** (3 points): e.g. a small layered warehouse: raw files and API events land in a staging area (a folder or object storage), are transformed with SQL into an integrated core, and served as a **dimensional mart** (Kimball-style star: fact check-in, fact booking, fact membership; dimensions member, studio, date, course). Technology: an analytical database such as DuckDB or a managed cloud warehouse is sufficient; a full lakehouse platform is not necessary at this size but acceptable if justified (JSON events, ML later).
- **Justifies Inmon vs. Kimball** (2 points): Kimball's bottom-up approach delivers the KPI report quickly, conformed dimensions (member, studio, date) keep marts integrated; a full Inmon enterprise model is too heavy for two analysts.
- **Connects to the later churn model** (1 point): the core/mart layer keeps member history at detailed grain (time-variant), so features for churn can be built later.
- **Names a realistic risk** (1 point): e.g. no data engineers to maintain ETL; inconsistent member IDs across systems; changing CSV formats; personal data (GDPR) of members.
- **Clarity** (1 point).

Reject answers that only name a tool without layers or justification, or that propose a big data cluster without reference to the data volume.
:::

## Optional Challenge: Count the Joins {.optional}

Write a query on the **normalised** TPC-H tables that returns net revenue 1997 per **supplier nation** and **customer nation** (e.g. how much German customers bought from Chinese suppliers). How many joins do you need, and why does `nation` appear twice?

::: answer lines=6
:::

::: solution
```sql
SELECT sn.n_name AS supplier_nation, cn.n_name AS customer_nation,
       sum(l_extendedprice * (1 - l_discount)) AS revenue
FROM lineitem
JOIN orders   ON l_orderkey = o_orderkey
JOIN customer ON o_custkey = c_custkey
JOIN nation cn ON c_nationkey = cn.n_nationkey
JOIN supplier ON l_suppkey = s_suppkey
JOIN nation sn ON s_nationkey = sn.n_nationkey
WHERE year(o_orderdate) = 1997
GROUP BY ALL;
```

Five joins; 625 nation pairs. `nation` appears twice in two different **roles** (customer nation and supplier nation), so it needs two aliases. In a star schema, this becomes two dimensions (or one role-playing dimension used twice) — a preview of session 3.
:::

## References {.references}

- Chaudhuri, S., & Dayal, U. (1997). An overview of data warehousing and OLAP technology. *ACM SIGMOD Record, 26*(1), 65–74. https://doi.org/10.1145/248603.248616
- Inmon, W. H. (2005). *Building the data warehouse* (4th ed.). Wiley.
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Raasveldt, M., & Mühleisen, H. (2019). DuckDB: An embeddable analytical database. In *Proceedings of the 2019 International Conference on Management of Data (SIGMOD '19)* (pp. 1981–1984). ACM. https://doi.org/10.1145/3299869.3320212
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
