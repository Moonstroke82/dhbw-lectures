---
course: Data Analytics
session: 3
title: Dimensional Data and OLAP
subtitle: Practice tasks on facts and measures, the four design steps, slowly changing dimensions and OLAP operations on the TPC-H star schema
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 3 on your own or in the lab. Tasks 1–4 need only paper and pencil. Tasks 5 and 6 use the star schema you built from the TPC-H data (Transaction Processing Performance Council, n.d.) in the session lab in `tpch.duckdb` (`fact_sales`, `dim_customer`, `dim_date`, `dim_part`). If it is missing, run the code from the slide "Lab Step 1: Build the Star Schema" first. Task 7 is a design task in the style of the portfolio notebooks.

## Additive or Not?

Classify each measure as **additive**, **semi-additive** or **non-additive** (Kimball & Ross, 2013). For the semi-additive ones, name the dimension over which they must not be summed; for the non-additive ones, say what you would store instead.

| Measure | Type | Note |
|---|---|---|
| Number of tickets sold | | |
| Stock level in a warehouse at the end of each day | | |
| Unit price of a product | | |
| Profit margin in per cent | | |
| Balance of a bank account at month end | | |
| Discount amount in euros | | |
| Temperature measured at a store | | |

::: solution
| Measure | Type | Note |
|---|---|---|
| Number of tickets sold | Additive | Can be summed over all dimensions |
| Stock level at day end | Semi-additive | Not over **time** (use the last value or the average per period); additive over warehouses and products |
| Unit price | Non-additive | Store quantity and revenue; compute the average price as sum(revenue) / sum(quantity) |
| Profit margin % | Non-additive | Store revenue and profit; compute the margin after aggregation |
| Account balance at month end | Semi-additive | Not over **time**; additive over accounts |
| Discount amount € | Additive | |
| Temperature | Non-additive | Report average, minimum, maximum; summing temperatures is meaningless |

Typical mistake: averaging per-row margins instead of computing sum(profit) / sum(revenue) — that weights a small order like a big one.
:::

## Four Steps for a Cinema Chain

A cinema chain with 25 cinemas wants to analyse **ticket sales**. A ticket is sold for one seat in one screening of one film; customers can buy several tickets in one transaction, online or at the box office, with different ticket types (adult, student, child).

Apply the four steps of dimensional design: business process, grain, dimensions, facts. Then sketch the star schema with table names and key attributes.

::: hint
Start with the grain: what is the smallest event the business records? Then ask *who, what, where, when, how* for that event.
:::

::: answer lines=12
:::

::: solution
1. **Business process:** ticket sales.
2. **Grain:** one row per **ticket** (one seat in one screening). Coarser grains (one row per transaction or per screening) would lose ticket type and seat analysis; the atomic grain can always be rolled up.
3. **Dimensions:** `dim_date` (day, weekday, holiday, month, year), `dim_time` or show-time band, `dim_film` (title, genre, age rating, distributor), `dim_cinema` (name, city, region, number of screens), `dim_screen` or screening attributes (hall, 3D/2D) — can also be part of a screening dimension, `dim_ticket_type` (adult, student, child), `dim_channel` (online, box office), optionally `dim_customer` for loyalty-card holders. The transaction number can stay as a **degenerate dimension** in the fact table.
4. **Facts:** ticket price paid, discount, list price, and a count of 1 per row (number of tickets). Occupancy rate is non-additive — compute it from tickets sold and seat capacity (capacity belongs to the screen dimension or a separate screening fact).

Sketch: `fact_ticket_sales(date_key, time_key, film_key, cinema_key, screen_key, ticket_type_key, channel_key, transaction_no, price_paid, discount)` in the centre with the dimensions around it. Accept reasonable variants; the grain must be stated explicitly.
:::

## Name the Operation — and Write the Clause

A hospital controller works with a cube *admissions* with the dimensions **ward** (hierarchy: ward → department → hospital), **date** (day → month → quarter → year) and **diagnosis group**. The starting view shows admissions per department and year. Name the OLAP operation and the SQL part that implements it.

1. She looks only at the year 2025.
2. She expands the surgery department into its wards.
3. She shows the years as columns and the departments as rows.
4. She restricts the view to the cardiology and neurology departments, Q1 and Q2, diagnosis group "stroke".
5. She replaces the departments by one total for the whole hospital.

::: answer lines=6
:::

::: solution
1. **Slice**: `WHERE year = 2025`.
2. **Drill-down**: add `ward` to `GROUP BY` (along the ward hierarchy), with `WHERE department = 'Surgery'`.
3. **Pivot**: DuckDB `PIVOT … ON year USING sum(admissions)`, or the pivot function of the BI tool — a change of presentation, not of the data.
4. **Dice**: `WHERE department IN ('Cardiology', 'Neurology') AND quarter IN (1, 2) AND diagnosis_group = 'Stroke'`.
5. **Roll-up**: remove `department` from `GROUP BY` (aggregate to the hospital level).

Source: operations as in Chaudhuri and Dayal (1997).
:::

## Slowly Changing Dimensions

An online shop has a customer dimension with the attributes **e-mail address**, **date of birth**, **city**, **customer segment** (assigned by marketing) and **tax ID** (for business customers).

1. For each attribute, choose SCD **type 1** or **type 2** and justify your choice in one line.
2. Customer C-311 (surrogate key 507) lives in Mannheim since 2022-04-01 and is in segment "Standard". On 2026-03-15 she moves to Heidelberg. On 2026-09-01 marketing reclassifies her as "Premium". Write down all rows of the customer dimension for C-311 after both changes, with the columns `customer_key, customer_id, city, segment, valid_from, valid_to, current`.
3. Which surrogate key does a sale on 2026-05-10 point to?

::: answer lines=10
:::

::: solution
1. Suggested choices (accept others with a business justification):
   - **E-mail**: type 1 — a correction or update; history is not needed for analysis.
   - **Date of birth**: type 1 — changes are corrections of errors, not real changes.
   - **City**: type 2 — sales should stay in the region where they happened (regional analysis).
   - **Segment**: type 2 if marketing wants to evaluate campaigns by the segment at purchase time; type 1 if only the current segment matters. Both acceptable with reasoning.
   - **Tax ID**: type 1 — usually a correction; type 2 if legal reporting needs the historical value.
2. With type 2 for city and segment:

| customer_key | customer_id | city | segment | valid_from | valid_to | current |
|---|---|---|---|---|---|---|
| 507 | C-311 | Mannheim | Standard | 2022-04-01 | 2026-03-14 | no |
| new, e.g. 1288 | C-311 | Heidelberg | Standard | 2026-03-15 | 2026-08-31 | no |
| new, e.g. 1530 | C-311 | Heidelberg | Premium | 2026-09-01 | 9999-12-31 | yes |

Each change adds a row with a new surrogate key; the business key C-311 stays. Accept `valid_to` equal to the next `valid_from` if the convention (exclusive end date) is stated.
3. The sale on 2026-05-10 falls into the second row (Heidelberg, Standard), so it points to that row's surrogate key (1288 in the example).
:::

## Add a Supplier Dimension

Extend the TPC-H star schema so that you can analyse **where products come from**.

1. Create `dim_supplier` with supplier key, supplier name, supplier nation and supplier region (join `supplier`, `nation`, `region`).
2. The current `fact_sales` has no supplier key. Recreate it as `fact_sales_supp` with the additional column `l_suppkey AS supplier_key`.
3. Compute net revenue 1997 with **customer regions as rows** and **supplier regions as columns** (`PIVOT`).
4. What share of revenue 1997 is bought from suppliers in the **same region** as the customer? Which supplier region delivers the most, and why could that be? Check the number of suppliers per region.

::: hint
In the fact table, `nation` and `region` would appear twice (customer and supplier). Give the supplier attributes different names (`supplier_nation`, `supplier_region`) so that both can be used in one query.
:::

::: answer lines=10
:::

::: solution
```sql
CREATE OR REPLACE TABLE dim_supplier AS
SELECT s_suppkey AS supplier_key, s_name AS supplier,
       n_name AS supplier_nation, r_name AS supplier_region
FROM supplier JOIN nation ON s_nationkey = n_nationkey
              JOIN region ON n_regionkey = r_regionkey;

CREATE OR REPLACE TABLE fact_sales_supp AS
SELECT o_orderdate AS date_key, o_custkey AS customer_key,
       l_partkey AS part_key, l_suppkey AS supplier_key,
       l_quantity AS quantity, l_extendedprice * (1 - l_discount) AS revenue
FROM lineitem JOIN orders ON l_orderkey = o_orderkey;

PIVOT (SELECT c.region AS customer_region, s.supplier_region, f.revenue / 1e6 AS rev
       FROM fact_sales_supp f JOIN dim_customer c USING (customer_key)
       JOIN dim_supplier s USING (supplier_key) JOIN dim_date d USING (date_key)
       WHERE d.year = 1997)
ON supplier_region USING round(sum(rev), 1) GROUP BY customer_region;
```

Expected result (million, DuckDB 1.5, sf 0.1): `dim_supplier` has 1,000 rows. Asia is the largest column for every customer region (about 135–143 million per cell), Africa the smallest (about 109–114). Example row Europe: Africa 110.2, America 117.6, Asia 142.6, Europe 127.4, Middle East 117.4.

Same-region share: about **20.2 %** — no more than one would expect if suppliers were chosen at random (5 regions). Asia delivers most because it has the most suppliers (225 of 1,000; Africa only 179). Lesson: before interpreting a "strong supply region", normalise by the number of suppliers — a typical case of a missing denominator (session 5). In real data, the same-region share would usually be much higher.
:::

## Drill Down and Roll Up

Use `fact_sales`, `dim_customer` and `dim_date`.

1. Compute net revenue of the segment **MACHINERY** in **1996**.
2. Drill down into the four quarters, then into the months of the strongest quarter.
3. Check that rolling the quarters up again gives exactly the yearly figure. Why is that guaranteed here, and when would it fail (think of a measure from task 1)?

::: answer lines=8
:::

::: solution
Expected results (million, DuckDB 1.5, sf 0.1):

1. MACHINERY 1996: **638.9**.
2. Quarters: Q1 159.9 · Q2 156.4 · Q3 157.7 · Q4 **164.9** (strongest). Months of Q4: October 52.0 · November 57.1 · December 55.9.

```sql
SELECT quarter, month, sum(revenue) / 1e6 AS rev_m
FROM fact_sales JOIN dim_customer USING (customer_key) JOIN dim_date USING (date_key)
WHERE year = 1996 AND segment = 'MACHINERY'
GROUP BY ROLLUP (quarter, month) ORDER BY ALL;
```

(Students may use separate GROUP BY queries; `ROLLUP` is the topic of session 4.)

3. 159.9 + 156.4 + 157.7 + 164.9 = 638.9. It works because revenue is **additive** and the date hierarchy is clean (each day belongs to exactly one month and quarter). It fails for semi-additive or non-additive measures (e.g. a stock level or an average price summed over quarters), and for hierarchies that do not nest cleanly (weeks spanning two months or years).
:::

## Portfolio-Style Task: Design a Star Schema for Taxi Trips

The New York City Taxi and Limousine Commission publishes trip records as open data (NYC Taxi and Limousine Commission, n.d.). Each record contains pick-up and drop-off date and time, pick-up and drop-off zone (about 260 zones, each belonging to a borough), passenger count, trip distance, fare amount, tip amount, total amount, payment type and the vendor (taxi company).

Design a star schema for analysing taxi trips. Your answer should contain: the grain, the fact table with its measures (state additivity), all dimensions with their main attributes and hierarchies, one slowly changing dimension issue, and three business questions with the OLAP operation each needs.

::: answer lines=16
:::

::: solution
Marking guide (12 points):

- **Grain** (2 points): one row per trip. Stated explicitly.
- **Fact table and measures** (2 points): `fact_trip` with trip_distance, fare_amount, tip_amount, total_amount, passenger_count, trip_duration (derived), all additive except passenger count (additive but often averaged) — and the note that ratios such as tip percentage are computed after aggregation.
- **Dimensions** (3 points): `dim_date` (day → month → quarter → year, weekday, holiday), `dim_time` (hour, time band), `dim_zone` used **twice** as a role-playing dimension (pick-up zone and drop-off zone; zone → borough), `dim_payment_type`, `dim_vendor`. Deduct one point if pick-up and drop-off are not separated.
- **Hierarchies** (1 point): at least date and zone → borough.
- **SCD issue** (2 points): e.g. zone boundaries or zone-to-borough assignments change; vendors are renamed or merge; payment types are recoded — with type 1 or type 2 and a reason.
- **Business questions with operations** (2 points): e.g. "Average tip share per borough and month" (roll-up from zone to borough); "Trips from Manhattan to the airports on weekday mornings in 2025" (dice); "From borough to zones in Brooklyn" (drill-down); "Revenue per payment type, years as columns" (pivot).

Accept dimensional designs that differ in detail if the grain is consistent and each dimension answers who, what, where, when or how.
:::

## References {.references}

- Chaudhuri, S., & Dayal, U. (1997). An overview of data warehousing and OLAP technology. *ACM SIGMOD Record, 26*(1), 65–74. https://doi.org/10.1145/248603.248616
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- NYC Taxi and Limousine Commission. (n.d.). *TLC trip record data*. Retrieved October 20, 2026, from https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
