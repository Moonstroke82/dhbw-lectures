---
course: Data Management
session: 17
title: Data Warehousing
subtitle: Practice tasks on data warehouse concepts, Inmon vs. Kimball, dimensional modelling, star and snowflake schemas and OLAP
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 17 on your own or with your project team. Tasks 1–3 and the exam-style task can be done on paper. For the lab tasks you need SQLite (in Jupyter with Python's `sqlite3`, or the SQLite command-line tool) and the bike shop database of the session: run [bikeshop-schema.sql](data/bikeshop-schema.sql), [bikeshop-data.sql](data/bikeshop-data.sql), [bikeshop-data-session09.sql](data/bikeshop-data-session09.sql), [bikeshop-etl-session16.sql](data/bikeshop-etl-session16.sql), [bikeshop-sales-session17.sql](data/bikeshop-sales-session17.sql) and the model star [bikeshop-star-session17.sql](data/bikeshop-star-session17.sql) in this order. The till data are fictional; the weather values are real observations of the Deutscher Wetterdienst, retrieved through the Bright Sky API (de Maeyer, n.d.). All other names and data are fictional. The terms follow the session slides, which are based on Inmon (2005), Kimball and Ross (2013), Chaudhuri and Dayal (1997), Elmasri and Navathe (2016, Chapter 29) and Serra (2024, Chapter 8). The results in the solutions were produced with SQLite 3.45.1.

```python
import sqlite3
con = sqlite3.connect("bikeshop.db")
con.execute("PRAGMA foreign_keys = ON")
for script in ["bikeshop-schema.sql", "bikeshop-data.sql", "bikeshop-data-session09.sql",
               "bikeshop-etl-session16.sql", "bikeshop-sales-session17.sql",
               "bikeshop-star-session17.sql"]:
    with open(script, encoding="utf-8") as f:
        con.executescript(f.read())
```

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. A data warehouse is usually designed in third normal form so that analysts can update data without anomalies.
2. "Time-variant" means that the warehouse keeps history: every row belongs to a point or period in time.
3. In Kimball's approach, the data warehouse is the set of dimensional stars that share conformed dimensions.
4. The grain of a fact table should be decided after the facts have been chosen.
5. A snowflake schema needs fewer joins than a star schema.
6. A surrogate key is a meaningless integer key of a dimension table that does not depend on the keys of the source systems.
7. The number of items in stock at the end of each day may be summed over several days.
8. A slice fixes one dimension to a single value; a dice selects values on several dimensions.

::: answer lines=10
:::

::: solution
1. **False.** A warehouse is mainly read and loaded by ETL, not updated by users; dimensional models are deliberately denormalised for simple, fast queries (Inmon's enterprise layer is normalised, but nobody "updates" it by hand either).
2. **True.**
3. **True.** The conformed dimensions (the bus architecture) are what integrates the stars.
4. **False.** The grain is declared **before** dimensions and facts (step 2 of 4); dimensions and facts must fit the grain.
5. **False.** A snowflake normalises the dimensions, so it needs **more** joins.
6. **True.**
7. **False.** Stock is a **semi-additive** fact: it may be summed across products or shops, but not over time — use the last value or the average.
8. **True.**

Marking: one point per statement; a false statement needs a correct correction for the point.
:::

## Inmon or Kimball? The Food Co-op

The food co-op (420 members, two volunteers who know SQL) wants to analyse its weekly orders: which products sell in which season, and which members order regularly. Later it may also analyse deliveries from farmers and volunteer shifts.

1. Assign each statement to **Inmon**, **Kimball** or **both**:
   a) Start with an integrated, normalised data model of the whole organisation.
   b) Data is extracted from the sources, transformed and loaded through a staging area.
   c) Build the first star for one business process; add the next process later.
   d) Departments get data marts that are derived from the central warehouse.
   e) Shared dimensions such as date and member make the stars fit together.
   f) The warehouse keeps history and integrates data from several sources.
2. Recommend one approach for the co-op and give **two** reasons.
3. Which **two** dimensions should the later "deliveries" star share with the "orders" star, and what goes wrong if the two stars use different member or product numbers?

::: answer lines=12
:::

::: solution
1. a) Inmon · b) both (ETL and staging are part of both architectures) · c) Kimball · d) Inmon · e) Kimball (conformed dimensions, bus architecture) · f) both (Inmon's definition, and every Kimball warehouse keeps history).
2. **Kimball**: (1) a small team with limited time gets a usable result quickly with one "orders" star; (2) dimensional models are easy for volunteers to query and understand; (3) the co-op has few sources, so an enterprise model up front would be heavy for little gain. Any two reasons with the case.
3. **Date** and **product** (deliveries from farmers are about products and days; members do not deliver — "farmer" is a new dimension). With different product numbers the stars cannot be combined: "ordered vs. delivered per product and week" is impossible, or needs a mapping table — the stars become isolated silos. Accept "member" only if the student explains that members also deliver (e.g. member farmers).

Marking: 1 has three points (half a point per statement), 2 and 3 two points each.
:::

## Facts, Dimensions and Grain: The Car-Sharing Company

The car-sharing company wants a star schema for its **trips**. The trip export has these columns:

| Column | Example |
|---|---|
| `trip_id` | T-501 |
| `plate`, `vehicle_model`, `fuel_type` | MA-CS 101, VW ID.3, electric |
| `member_no`, `tariff` | C001, student |
| `station`, `district` | Hauptbahnhof, Innenstadt |
| `trip_date`, `start_time` | 2027-06-01, 08:15 |
| `duration_min`, `distance_km` | 45, 18 |
| `price_eur` | 14.40 |
| `price_per_km` | 0.80 |
| `battery_end_pct` | 62 |

1. Name the business process and the grain of the fact table.
2. Sort the columns into **facts**, **dimension attributes** (say which dimension) and a **degenerate dimension**.
3. Classify each fact as additive, semi-additive or non-additive.
4. Name one **hierarchy** in a dimension and one question that rolls up along it.
5. The company also wants "number of cars available at each station at 06:00 every day". Does this belong in the trip fact table? If not, what kind of fact table is it?

::: answer lines=14
:::

::: hint
Ask for every number: does a sum over trips, over stations and over days make sense? `price_per_km` and `battery_end_pct` are numbers — but are they measurements you add up?
:::

::: solution
1. Business process: renting cars (trips). Grain: **one trip** (one row per `trip_id`).
2. **Facts**: `duration_min`, `distance_km`, `price_eur` (and, if stored, `battery_end_pct` — see 3). **Dimension attributes**: vehicle dimension (`plate`, `vehicle_model`, `fuel_type`); member dimension (`member_no`, `tariff`); station dimension (`station`, `district`); date dimension (`trip_date` plus derived weekday, month …); `start_time` in a time-of-day dimension or as an attribute of the fact (accept both). `price_per_km` is a tariff attribute (member/tariff dimension) — or a derived, non-additive value. **Degenerate dimension**: `trip_id` (an identifier without its own dimension table).
3. `duration_min`, `distance_km`, `price_eur`: **additive**. `price_per_km`: **non-additive** (compute as sum of price / sum of km after aggregation). `battery_end_pct`: **non-additive** (a percentage state after the trip; averaging is possible, summing is not) — some students call it semi-additive because it is a state: accept with the argument that summing over trips makes no sense.
4. Station → district (→ city): "revenue per district". Date → month → quarter → year: "kilometres per quarter". Vehicle → model → fuel type: "trips of electric cars".
5. No: it is not a trip, it is a **state** measured once a day per station — a different grain. It is a **periodic snapshot** fact table (one row per station and day), and "available cars" is **semi-additive** (sum over stations, not over days). It can share the date and station dimensions with the trip star.

Marking: one point per question; in 2 at most two misclassifications.
:::

## Lab: OLAP on the Bike Shop Star

Use the star of the session (`fact_sales` with `dim_date`, `dim_product`, `dim_salesperson`, `dim_weather`). Write one query per question, run it, and name the **OLAP operation** it performs (roll-up, drill-down, slice, dice, pivot).

1. Revenue per weekday — then roll it up to the **day type** (Mon–Fri, Saturday).
2. Start from revenue per product group; then show the **products** of the group *Accessories* with quantity and revenue.
3. Revenue and number of receipts per salesperson on **dry and warm** days only.
4. Quantity and revenue of **accessories** on **bad bike days**, per salesperson.
5. A table with one row per **salesperson** and one column per **category** (Bikes, Parts and accessories, Service) plus a total.
6. The average revenue per receipt for the whole week. Then compute the average per day and take the average of the six daily values. Why do the two numbers differ — and which one is right?

::: answer lines=18
:::

::: hint
Every query has the same shape: `FROM fact_sales` joined with the dimensions you need, `WHERE` for slices and dices, `GROUP BY` the dimension attributes. For the pivot, use `sum(CASE WHEN … THEN revenue ELSE 0 END)`. Count receipts with `count(DISTINCT receipt_no)`.
:::

::: solution
Results observed with the model star (bikeshop-star-session17.sql).

**1.** Roll-up (date hierarchy weekday → day type).
```sql
SELECT d.day_type, round(sum(f.revenue), 2) AS revenue
FROM fact_sales AS f JOIN dim_date AS d ON d.date_key = f.date_key
GROUP BY d.day_type;
```

Per weekday: Mon 2,840.50 · Tue 3,125.00 · Wed 4,410.90 · Thu 980.40 · Fri 1,530.00 · Sat 5,980.00. Rolled up: **Mon–Fri 12,886.80**, **Saturday 5,980.00**. Sunday does not appear: no sales (closed), not missing data.

**2.** Drill-down (product group → product):
```sql
SELECT p.name, sum(f.quantity) AS qty, round(sum(f.revenue), 2) AS revenue
FROM fact_sales AS f JOIN dim_product AS p ON p.product_key = f.product_key
WHERE p.product_group = 'Accessories'
GROUP BY p.name ORDER BY revenue DESC;
```

Pannier bag 11 / 548.90 · Helmet Urban 5 / 399.50 · Rain cape 9 / 359.10 · Folding lock 3 / 179.70 · Cycling gloves 3 / 59.70 (sum 1,546.90 = the Accessories total). The child seat (A-06) does not appear: in `dim_product`, never sold. (The `WHERE` makes it a drill-down into one group; strictly, fixing the group is also a slice — accept both names with this reasoning.)

**3.** Slice (weather type fixed to one value):
```sql
SELECT s.name, round(sum(f.revenue), 2) AS revenue, count(DISTINCT f.receipt_no) AS receipts
FROM fact_sales AS f
JOIN dim_salesperson AS s ON s.salesperson_key = f.salesperson_key
JOIN dim_weather     AS w ON w.weather_key = f.weather_key
WHERE w.weather_type = 'dry and warm'
GROUP BY s.name;
```

Laura Becker 939.80 (9 receipts) · Marco Esposito 9,436.60 (10 receipts).

**4.** Dice (conditions on product and weather):
```sql
SELECT s.name, sum(f.quantity) AS qty, round(sum(f.revenue), 2) AS revenue
FROM fact_sales AS f
JOIN dim_salesperson AS s ON s.salesperson_key = f.salesperson_key
JOIN dim_weather     AS w ON w.weather_key = f.weather_key
JOIN dim_product     AS p ON p.product_key = f.product_key
WHERE p.product_group = 'Accessories' AND w.bike_day = 'bad'
GROUP BY s.name;
```

Laura Becker 10 / 449.00 · Marco Esposito 2 / 139.80.

**5.** Pivot:
```sql
SELECT s.name,
       round(sum(CASE WHEN p.category = 'Bikes' THEN f.revenue ELSE 0 END), 2) AS bikes,
       round(sum(CASE WHEN p.category = 'Parts and accessories' THEN f.revenue ELSE 0 END), 2)
           AS parts_acc,
       round(sum(CASE WHEN p.category = 'Service' THEN f.revenue ELSE 0 END), 2) AS service,
       round(sum(f.revenue), 2) AS total
FROM fact_sales AS f
JOIN dim_salesperson AS s ON s.salesperson_key = f.salesperson_key
JOIN dim_product     AS p ON p.product_key = f.product_key
GROUP BY s.name;
```

| name | bikes | parts_acc | service | total |
|---|---|---|---|---|
| Laura Becker | 2,297.00 | 1,086.30 | 98.00 | 3,481.30 |
| Marco Esposito | 14,194.00 | 995.50 | 196.00 | 15,385.50 |

**6.** Week: `sum(revenue) / count(DISTINCT receipt_no)` = 18,866.80 / 35 = **539.05**. Average of the daily averages (568.10, 446.43, 630.13, 245.10, 306.00, 854.29) = **508.34**. They differ because every day gets the same weight, although the days have different numbers of receipts (4 to 7). The average per receipt is **non-additive**: compute it from the additive parts (revenue and receipt count) at the level you report — 539.05 is right for "average receipt this week".

Marking: one point per question; each point needs a working query (or the correct result) and the correct operation.
:::

## Lab: A Second Star for the Workshop

The workshop wants to analyse repairs (data of session 8: `repair_job`, `repair_line`, `bike`, `customer`, `spare_part`). The new star should **share** dimensions with the sales star.

1. Do the four design steps. Use the grain "one spare part on one repair job".
2. Which dimensions of the sales star can be **conformed** (reused)? What has to be added to them so that every repair line finds its dimension row? Check with SQL.
3. Create `dim_bike` (brand, model, the customer's city) and `fact_repair_line` with `quantity`, `revenue` (`quantity × price_charged`) and `list_value` (`quantity × list_price`), and load them.
4. Revenue, discount (`list_value − revenue`) and number of jobs per month. Why does the fact table show fewer jobs than `repair_job` has?
5. **Drill across**: one result with, per spare part, the quantity sold at the till and the quantity used in the workshop.

::: answer lines=18
:::

::: hint
`dim_date` of the session covers only October 2026; the repair jobs are from January to April 2027. Compare `SELECT part_no FROM spare_part` with `SELECT product_no FROM dim_product`. For 5, aggregate each fact table on its own first (two subqueries or `WITH`), then join the results on `product_key` — never join two fact tables row by row.
:::

::: solution

**1.** Process: repairing bikes. Grain: one `repair_line` row (a part on a job). Dimensions: date (`job_date`), product (the part), bike (brand, model, customer city); `job_no` as degenerate dimension. Facts: quantity, revenue, list value (all additive). Mechanics are M:N with jobs and do not fit this grain (see the optional challenge).

**2.** **dim_date** and **dim_product** can be conformed. dim_date must be extended to January–April 2027 (151 rows afterwards: 31 + 120). dim_product lacks the six spare parts the till does not sell: P-104, P-105, P-106, P-107, P-108, P-109 (check: `SELECT part_no FROM spare_part WHERE part_no NOT IN (SELECT product_no FROM dim_product)`); they are added with product group Parts (24 rows afterwards). Extending, not copying, is the point: the same table serves both stars.
```sql
WITH RECURSIVE days (d) AS (
    SELECT '2027-01-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2027-04-30')
INSERT INTO dim_date (date_key, full_date, weekday, day_type, month, month_name, quarter, year)
SELECT CAST(strftime('%Y%m%d', d) AS INTEGER), d,
       CASE strftime('%w', d) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday' ELSE 'Saturday' END,
       CASE strftime('%w', d) WHEN '0' THEN 'Sunday' WHEN '6' THEN 'Saturday' ELSE 'Mon-Fri' END,
       CAST(strftime('%m', d) AS INTEGER),
       CASE strftime('%m', d) WHEN '01' THEN 'January' WHEN '02' THEN 'February'
            WHEN '03' THEN 'March' ELSE 'April' END,
       (CAST(strftime('%m', d) AS INTEGER) + 2) / 3, CAST(strftime('%Y', d) AS INTEGER)
FROM days;

INSERT INTO dim_product (product_no, name, product_group, category)
SELECT part_no, name, 'Parts', 'Parts and accessories'
FROM spare_part WHERE part_no NOT IN (SELECT product_no FROM dim_product);
```

**3.** Dimension and fact table:
```sql
CREATE TABLE dim_bike (
    bike_key INTEGER PRIMARY KEY, frame_no TEXT NOT NULL UNIQUE,
    brand TEXT NOT NULL, model TEXT NOT NULL, customer_city TEXT);
INSERT INTO dim_bike (frame_no, brand, model, customer_city)
SELECT b.frame_no, b.brand, b.model, coalesce(c.city, 'unknown')
FROM bike AS b LEFT JOIN customer AS c ON c.customer_no = b.customer_no ORDER BY b.frame_no;

CREATE TABLE fact_repair_line (
    date_key INTEGER NOT NULL REFERENCES dim_date (date_key),
    product_key INTEGER NOT NULL REFERENCES dim_product (product_key),
    bike_key INTEGER NOT NULL REFERENCES dim_bike (bike_key),
    job_no INTEGER NOT NULL,
    quantity INTEGER NOT NULL, revenue NUMERIC NOT NULL, list_value NUMERIC NOT NULL,
    PRIMARY KEY (job_no, product_key));
INSERT INTO fact_repair_line
SELECT CAST(strftime('%Y%m%d', j.job_date) AS INTEGER), p.product_key, b.bike_key, l.job_no,
       l.quantity, round(l.quantity * l.price_charged, 2), round(l.quantity * sp.list_price, 2)
FROM repair_line AS l
JOIN repair_job  AS j  ON j.job_no = l.job_no
JOIN spare_part  AS sp ON sp.part_no = l.part_no
JOIN dim_product AS p  ON p.product_no = l.part_no
JOIN dim_bike    AS b  ON b.frame_no = j.frame_no;
```

dim_bike 15 rows, fact_repair_line **16** rows (= repair_line), `PRAGMA foreign_key_check` returns nothing. Without the new parts of step 2, the `JOIN dim_product` silently drops the lines with P-104 … P-109; without the new dates, the insert fails with `FOREIGN KEY constraint failed`. Always compare row counts with the source.

**4.** Query:
```sql
SELECT d.month_name, round(sum(f.revenue), 2) AS revenue,
       round(sum(f.list_value - f.revenue), 2) AS discount,
       count(DISTINCT f.job_no) AS jobs
FROM fact_repair_line AS f JOIN dim_date AS d ON d.date_key = f.date_key
GROUP BY d.month ORDER BY d.month;
```

January 28.40 / 0.00 / 2 · February 76.40 / 3.00 / 3 · March 733.20 / 8.90 / 4 · April 103.40 / 0.00 / 1 (total 941.40). Discounts: job 503 brake pads 2 × 1.50; job 508 the free bell 8.90. Only **10** of 12 jobs appear: jobs 506 and 512 have no repair lines — at this grain a job without parts has no fact row. If the workshop wants to count all jobs, it needs a second fact table at the grain "one repair job" (e.g. an accumulating snapshot).

**5.** Query:
```sql
WITH till AS (SELECT product_key, sum(quantity) AS qty FROM fact_sales GROUP BY product_key),
     shop AS (SELECT product_key, sum(quantity) AS qty FROM fact_repair_line GROUP BY product_key)
SELECT p.product_no, p.name, coalesce(t.qty, 0) AS till_qty, coalesce(s.qty, 0) AS workshop_qty
FROM dim_product AS p
LEFT JOIN till AS t ON t.product_key = p.product_key
LEFT JOIN shop AS s ON s.product_key = p.product_key
WHERE p.product_group = 'Parts' ORDER BY p.product_no;
```

P-101 3/2 · P-102 7/1 · P-103 2/6 · P-104 0/1 · P-105 0/1 · P-106 0/3 · P-107 0/1 · P-108 0/1 · P-109 0/1 · P-110 4/1 · P-111 7/1 · P-112 0/0. Note that the periods differ (till: October 2026, workshop: January–April 2027) — a fair comparison would filter both on the same months. Joining the two fact tables directly on `product_key` would multiply rows (every till line with every workshop line of the same part).

Marking: one point per question; 2 needs both the date extension and the six missing parts.
:::

## Exam-Style Task: A Star Schema for the Coworking Space

This task is in the style of an exam question.

The coworking space rents **desks and rooms by the hour**. Every booking records: booking number, member (member number, name, plan FLEX/FIX/DAY/TEAM, postcode), workspace (workspace number, type "open desk", "fixed desk" or "meeting room", floor, number of seats), date, start time, booked hours and the price charged. The management wants to answer: *How many hours are booked per workspace type, per weekday and per plan? Which floors earn the most? How full are the meeting rooms in each month?*

1. Name the business process and declare the grain of the fact table. (2 points)
2. Draw a star schema: the fact table and **three** dimension tables with primary keys, foreign keys and their most important attributes. Mark one hierarchy. (4 points)
3. Classify these measures as additive, semi-additive or non-additive and say how to handle each in a report: booked hours · price charged · occupancy rate of a room in % · number of members with an active contract at the end of the month. (2 points)
4. A colleague proposes to move `type` and `floor` into separate tables. Name the resulting schema type, one advantage and one disadvantage. Would you do it? (1 point)
5. Write an SQL query on your star for "booked hours per workspace type and plan in March 2027" and name the OLAP operations it contains. (1 point)

::: answer lines=24
:::

::: solution
Marking guide (10 points).

**1.** (2 points) Business process: **booking workspaces** (renting desks and rooms) — 1 point. Grain: **one booking** (one row per booking number) — 1 point. "Per member and month" or "per day" is a coarser grain and loses the weekday and workspace questions: 0 points for the grain.

**2.** (4 points) Fact table `fact_booking(date_key FK, member_key FK, workspace_key FK, booking_no [degenerate], start_time, hours, price_eur)` — 1 point for keys and facts. `dim_date(date_key PK, full_date, weekday, month, quarter, year)` — 1 point. `dim_member(member_key PK, member_no, name, plan, postcode)` and `dim_workspace(workspace_key PK, workspace_no, type, floor, seats)` — 1 point for both with surrogate keys. One hierarchy marked, e.g. date → month → quarter → year or workspace → floor — 1 point. A time-of-day dimension is accepted as a fourth dimension. Deduct the point for keys if facts are put into dimensions (e.g. hours in `dim_member`).

**3.** (2 points; half a point each) Booked hours: **additive** — sum. Price charged: **additive** — sum. Occupancy rate: **non-additive** — compute from additive parts after aggregation (booked hours / available hours), never sum or average the percentages. Active members at month end: **semi-additive** — a state (periodic snapshot): sum over plans, but over months take the last value or the average.

**4.** (1 point) **Snowflake schema**. Advantage: no repeated type and floor values, a hierarchy stored explicitly, easier maintenance of the floor data. Disadvantage: more joins, harder to read for users. Recommendation with reason, e.g. "no: the workspace dimension is small, the saving is tiny, a star is easier to query". The point needs the name and both arguments.

**5.** (1 point)
```sql
SELECT w.type, m.plan, sum(f.hours) AS booked_hours
FROM fact_booking AS f
JOIN dim_date      AS d ON d.date_key = f.date_key
JOIN dim_workspace AS w ON w.workspace_key = f.workspace_key
JOIN dim_member    AS m ON m.member_key = f.member_key
WHERE d.year = 2027 AND d.month = 3
GROUP BY w.type, m.plan;
```

Operations: **slice** on the date (March 2027) and **roll-up** to workspace type and plan (from single bookings / workspaces). "Dice" is accepted if the student filters on more than one dimension. Half a point for the query, half for the operations.
:::

## Optional Challenge: Which Mechanic Earned the Revenue? {.optional}

Build on the workshop star of the lab task. The management wants repair revenue **per mechanic**. A job can have several mechanics (`job_mechanic`, M:N).

1. Join `fact_repair_line` with `job_mechanic` and `employee` and sum the revenue per mechanic. Compare the sum over all mechanics with the total revenue of `fact_repair_line`. What went wrong?
2. Build a **bridge table** `bridge_job_mechanic(job_no, employee_no, weight)` in which the weights of each job add up to 1 (equal shares), and compute the revenue per mechanic again. Check the total.
3. Name one business reason why equal shares might be unfair, and one alternative.

::: hint
For the weight, divide 1.0 by the number of mechanics of the same job: a correlated subquery `(SELECT count(*) FROM job_mechanic AS x WHERE x.job_no = jm.job_no)` or a window function `count(*) OVER (PARTITION BY job_no)` works.
:::

::: answer lines=12
:::

::: solution

**1.** Naive join: Sophie Lindner 678.50 · Deniz Arslan 187.10 · Katrin Vogel 154.40 · Jan Hoffmann 75.80; sum **1,095.80**, but the fact table has only **941.40**. Jobs 502, 504 and 511 have two mechanics each, so their revenue (21.50 + 29.50 + 103.40 = 154.40) is counted twice — the M:N relationship multiplies fact rows (the join pitfall of session 9). Katrin Vogel's 154.40 is exactly this: she is the second mechanic on all three jobs.

**2.** Bridge table and query:
```sql
CREATE TABLE bridge_job_mechanic AS
SELECT jm.job_no, jm.employee_no,
       1.0 / (SELECT count(*) FROM job_mechanic AS x WHERE x.job_no = jm.job_no) AS weight
FROM job_mechanic AS jm;

SELECT e.name, round(sum(f.revenue * b.weight), 2) AS revenue
FROM fact_repair_line AS f
JOIN bridge_job_mechanic AS b ON b.job_no = f.job_no
JOIN employee            AS e ON e.employee_no = b.employee_no
GROUP BY e.name ORDER BY revenue DESC;
```

Sophie Lindner 663.75 · Deniz Arslan 135.40 · Katrin Vogel 77.20 · Jan Hoffmann 65.05; total **941.40** — equal to the fact table. Jobs 506 and 512 have no lines; job 512 also has no mechanic yet — neither changes the total.

**3.** Equal shares ignore who did how much: the master (Katrin Vogel) may only have checked the apprentice's work, or one mechanic worked three hours and the other ten minutes. Alternative: weights from recorded working hours per mechanic and job, or a separate fact table "work hours per mechanic and job" at its own grain. Kimball and Ross (2013, Chapter 2) describe bridge tables for such multivalued dimensions.
:::

## References {.references}

- Chaudhuri, S., & Dayal, U. (1997). An overview of data warehousing and OLAP technology. *ACM SIGMOD Record, 26*(1), 65–74. https://doi.org/10.1145/248603.248616
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Inmon, W. H. (2005). *Building the data warehouse* (4th ed.). Wiley.
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
