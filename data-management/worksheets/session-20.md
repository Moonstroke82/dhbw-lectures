---
course: Data Management
session: 20
title: Course Revision
subtitle: A mixed revision set across Parts A–D — modelling, normalisation, SQL, data quality, pipelines, warehousing and access to data. Practice material, not from an exam
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet is a **revision set for the whole course** (sessions 1–19). **All tasks are practice tasks written for this course — they are not taken from any exam** and say nothing about what an exam will contain. The exam format and permitted aids are announced by the examination office. Tasks rise in difficulty: task 1 checks concepts across all parts, tasks 2–5 each revise one or two parts on a new case, and task 6 is a mixed exam-style practice task with a marking guide. Tasks 1, 2, 5 and 6 can be done on paper. Task 3 needs SQLite (in Jupyter with Python's `sqlite3`, or the SQLite command-line tool) and the script [foodcoop-revision-session20.sql](data/foodcoop-revision-session20.sql); task 4 needs pandas. All names and data are fictional. The terms follow the session slides, which are based on Chen (1976), Elmasri and Navathe (2016), Pipino et al. (2002), the Government Data Quality Hub (2021), McKinney (2022), Kimball and Ross (2013), Serra (2024) and the GDPR (Regulation (EU) 2016/679, 2016). The results in the solutions were produced with SQLite 3.45.1 and pandas 3.0.6. Legal questions are teaching material, not legal advice.

```python
import sqlite3

con = sqlite3.connect("foodcoop.db")
con.execute("PRAGMA foreign_keys = ON")
with open("foodcoop-revision-session20.sql", encoding="utf-8") as f:
    con.executescript(f.read())

def run(sql, con=con):
    """Run one statement; show the rows, the changed rows or the error."""
    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        print(rows if cur.description else f"{cur.rowcount} row(s) changed")
    except sqlite3.Error as e:
        print(type(e).__name__, "-", e)
```

## True or False Across the Course

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. Business intelligence and Big Data are two methods for analysing data.
2. In a 1:N relationship, the foreign key is placed in the relation on the N side.
3. A relation whose primary key is a single attribute is automatically in 3NF.
4. `WHERE e_mail = NULL` returns all rows without an e-mail address.
5. A view stores a copy of its result and must be refreshed after every change.
6. In the CAP theorem, the C means the same as the C in ACID.
7. A value can be valid and still not be accurate.
8. `pd.read_csv("members.csv")` always reads postcodes such as `06108` correctly.
9. A load is idempotent if running it twice leaves the target table in the same state as running it once.
10. The grain of a fact table should be decided after the facts have been chosen.
11. A data lake applies the structure of the data when it is read, not when it is stored.
12. Pseudonymised customer data is outside the scope of the GDPR.

::: answer lines=12
:::

::: solution
1. **False.** Business intelligence describes and reports what happened; Big Data describes **properties** of data (volume, velocity, variety …), not a method (session 1).
2. **True.** Example: `bike.customer_no` refers to the customer (session 5).
3. **False.** A single-attribute key makes 2NF automatic, but a non-key attribute can still depend on another non-key attribute (transitive dependency), which violates 3NF (session 6).
4. **False.** Every comparison with NULL is UNKNOWN, and WHERE keeps only TRUE rows: the query returns no rows. Use `IS NULL` (session 8).
5. **False.** A view is a stored **query**; it runs again on every use and is always current (session 10).
6. **False.** CAP's C (consistency) means that all nodes return the latest written value; ACID's C means that a transaction moves the database from one valid state to another, respecting the constraints (session 11).
7. **True.** `1900-01-01` is a valid date but almost certainly not a true birth date; validity is checked by rules, accuracy needs a comparison with reality (session 13).
8. **False.** Without `dtype=str` (or `dtype={"postcode": str}`), pandas infers an integer column and the leading zero is lost: `6108` (sessions 14–15).
9. **True.** That is what an upsert on a key achieves; append is not idempotent (session 16).
10. **False.** The grain comes **before** the dimensions and facts: business process → grain → dimensions → facts (Kimball & Ross, 2013; session 17).
11. **True.** Schema-on-read; a data warehouse applies schema-on-write (session 18).
12. **False.** Pseudonymised data is still personal data, because re-identification is possible with the additional information; only anonymous data is outside the GDPR (session 19).

Marking: one point per statement; a false statement needs a correct correction for the point.
:::

## Part A: From Case to Tables — The Food Co-op

The food co-op from earlier worksheets wants a proper database. The rules:

- **Members** have a member number, a name and an optional e-mail address. Every member is either a **regular** member or a **working** member; working members also have a weekly number of hours and a task area.
- **Producers** have a number, a name and a village. Every **product** (product number, name, unit, current price) comes from exactly one producer; a producer can have no products yet.
- A member places **at most one order per pick-up day**. An order contains several products; for each product the quantity and the **price paid** on that day are stored.
- New members get an experienced working member as their **buddy**; a working member can look after several new members.

1. Draw an ER model in Chen notation with keys, cardinalities and participation.
2. Map your model to a relational schema. Mark primary keys and foreign keys.
3. The co-op also keeps a **shift list** SHIFT_LIST(shift_date, task_area, area_lead, member_no, member_name, hours) with the key (shift_date, task_area, member_no). Each task area has exactly one lead. Name the functional dependencies, the normal form and a 3NF decomposition.

::: hint
Look for one specialisation, one M:N relationship with attributes, one recursive relationship and a business rule that becomes a `UNIQUE` constraint.
:::

::: answer lines=18
:::

::: solution
**1. ER model**

- *Member* (member_no as key, name, e_mail) with the specialisation into *Regular member* and *Working member* (weekly_hours, task_area): **disjoint and total** ("either … or").
- *Producer* (producer_no, name, village) 1:N **supplies** *Product* (product_no, name, unit, price): total participation of *Product* (exactly one producer), partial of *Producer* (no products yet is possible).
- *Order* (order_no, pickup_date): *Member* 1:N **places** *Order*, total participation of *Order*. The rule "at most one order per member and pick-up day" is a business rule (key alternative: *Order* as a weak entity type of *Member* with partial key pickup_date — accept both with a reason).
- *Order* M:N **contains** *Product* with the attributes quantity and price_paid (or a weak entity type *Order line*, owner *Order*).
- **is buddy of**: recursive 1:N on *Member* with the roles *buddy* and *new member*; strictly the buddy side belongs to *Working member*. Partial on both sides.

**2. Relational schema** (option A for the specialisation)

- MEMBER(**member_no**, name, e_mail, member_type, *buddy_no* → WORKING_MEMBER)
- WORKING_MEMBER(**member_no** → MEMBER, weekly_hours, task_area)
- PRODUCER(**producer_no**, name, village)
- PRODUCT(**product_no**, name, unit, price, *producer_no* → PRODUCER), producer_no NOT NULL
- PICKUP_ORDER(**order_no**, *member_no* → MEMBER, pickup_date), UNIQUE (member_no, pickup_date)
- ORDER_LINE(**order_no** → PICKUP_ORDER, **product_no** → PRODUCT, quantity, price_paid)

Accept option B (one table per subclass only) or option C (one table with a type column, as in the data script of task 3), if the answer names the trade-off. price_paid is history, not a copy of the current price.

**3. Shift list**

- FDs: task_area → area_lead · member_no → member_name · (shift_date, task_area, member_no) → hours.
- **1NF**: area_lead and member_name depend on **part** of the key (partial dependencies), so the list is not in 2NF.
- 3NF: TASK_AREA(**task_area**, area_lead) · MEMBER(**member_no**, member_name) — already exists · SHIFT(**shift_date, task_area** → TASK_AREA, **member_no** → MEMBER, hours). If area_lead is itself a member, it becomes a foreign key to MEMBER.

Marking (10 points): specialisation with constraints 1 · supplies with participation 1 · orders and the one-per-day rule 2 · contains with attributes 1 · recursive buddy relationship with roles 1 · relational schema with keys and foreign keys 2 · shift list: FDs and normal form 1, decomposition 1.
:::

## Part B: SQL Lab — The Food Co-op's Orders

Load [foodcoop-revision-session20.sql](data/foodcoop-revision-session20.sql) into a new database (code above). Expected row counts: producer 5, product 11, member 7, pickup_order 10, order_line 24. **Predict the number of rows first**, then run each query.

1. Every producer with its **number of products** — producers without products too.
2. Create a view `order_value(order_no, pickup_date, member_no, value)` with value = sum of quantity × price paid; orders without lines with 0. Use it for the **revenue** and the **average order value** per pick-up day. Order 10 has no lines: should it count in the average?
3. Members who did **not** order on 2027-10-15. Does Mia Hoffmann (order 10) belong in the result?
4. **Revenue per producer**, only producers with more than 30 euros, highest first.
5. Order lines where the **price paid differs** from the current price, and products that were **never ordered**. Why must `price_paid` stay in `order_line`?
6. A colleague wants the number of products and the units sold per producer:
   `SELECT h.name, count(p.product_no) AS products, sum(l.quantity) AS units FROM producer h JOIN product p ON p.producer_no = h.producer_no JOIN order_line l ON l.product_no = p.product_no GROUP BY h.producer_no, h.name;`
   Why does Hofgut Sonnenberg get 11 products? What else is wrong? Write a correct query.
7. Predict, then run these statements **in this order**. Note the result and the constraint that decides it.

| # | Statement |
|---|---|
| a | `INSERT INTO pickup_order VALUES (11, 'M01', '2027-10-15')` |
| b | `INSERT INTO order_line VALUES (10, 'C03', 0, 4.50)` |
| c | `DELETE FROM product WHERE product_no = 'V02'` |
| d | `DELETE FROM product WHERE product_no = 'C03'` |
| e | `DELETE FROM pickup_order WHERE order_no = 9` — how many order lines are left? |
| f | `INSERT INTO pickup_order VALUES (12, 'M07', '2027-10-32')` |
| g | In **one transaction**: order 11 for M07 on 2027-10-15 with the lines 2 × F01 at 3.20 and 1 × V05 at 2.90 — then the same with V04 instead of V05 |

::: hint
Question 1: what does `count(*)` count for a producer without products? Question 6: what does one row of the join mean — and which table is aggregated on which level?
:::

::: answer lines=22
:::

::: solution
All results observed in SQLite 3.45.1 on a fresh database.

1. `SELECT h.producer_no, h.name, count(p.product_no) AS products FROM producer h LEFT JOIN product p ON p.producer_no = h.producer_no GROUP BY h.producer_no, h.name;` → H1 4, H2 2, H3 3, H4 2, **H5 0**. With `count(*)`, H5 gets 1.
2. `CREATE VIEW order_value AS SELECT o.order_no, o.pickup_date, o.member_no, coalesce(sum(l.quantity * l.price_paid), 0) AS value FROM pickup_order o LEFT JOIN order_line l ON l.order_no = o.order_no GROUP BY o.order_no, o.pickup_date, o.member_no;` Then `SELECT pickup_date, count(*), round(sum(value), 2), round(avg(value), 2) FROM order_value GROUP BY pickup_date;` → 2027-10-08: 5 orders, **69.3**, average **13.86** · 2027-10-15: 5 orders, **67.7**, average **13.54**. Without order 10 (`WHERE value > 0`): 4 orders, average **16.93**. Order 10 is an empty order (opened, nothing ordered): as an "average basket" it should not count; as "orders opened" it should. The answer depends on the business question — say which one you answer.
3. `SELECT m.member_no, m.name FROM member m WHERE NOT EXISTS (SELECT 1 FROM pickup_order o WHERE o.member_no = m.member_no AND o.pickup_date = '2027-10-15');` → **M04 Daniel Roth, M07 Nora Schmitt**. If "ordered" means "has at least one order line", join `order_line` inside the subquery → M04, **M05 Mia Hoffmann**, M07. Both are correct with the definition stated.
4. `SELECT h.name, round(sum(l.quantity * l.price_paid), 2) AS revenue FROM producer h JOIN product p ON p.producer_no = h.producer_no JOIN order_line l ON l.product_no = p.product_no GROUP BY h.producer_no, h.name HAVING sum(l.quantity * l.price_paid) > 30 ORDER BY revenue DESC;` → **Hofgut Sonnenberg 54.2, Imkerei Weber 41.2** (the others: Käserei am Odenwald 26.8, Mühle Neckartal 14.8).
5. product JOIN order_line JOIN pickup_order `WHERE l.price_paid <> p.price` → **V02 Carrots**, paid 2.10 on 2027-10-08, current price 2.20. `NOT EXISTS` on order_line → **C03 Soft cheese**. price_paid is a different fact — the price on the pick-up day, depending on (order_no, product_no). Without it, the old orders would change their value when the price changes (history, session 4 pitfall 2; session 6).
6. One row of the join is one **order line** with its product: Hofgut Sonnenberg has 11 order lines of its 4 products, so `count(p.product_no)` counts lines. The inner joins also drop Obsthof Kraus (no products) and would drop a product without orders (C03 is missing from the count of Käserei am Odenwald: 5 lines instead of 3 products). Correct: `SELECT h.name, count(DISTINCT p.product_no) AS products, coalesce(sum(l.quantity), 0) AS units FROM producer h LEFT JOIN product p ON p.producer_no = h.producer_no LEFT JOIN order_line l ON l.product_no = p.product_no GROUP BY h.producer_no, h.name;` → Hofgut Sonnenberg 4 / 21, Imkerei Weber 2 / 5, Käserei am Odenwald 3 / 6, Mühle Neckartal 2 / 5, Obsthof Kraus 0 / 0. Aggregating each table on its own level first is also correct.
7. a) **UNIQUE constraint failed: pickup_order.member_no, pickup_order.pickup_date** — M01 already has order 6 on that day. b) **CHECK constraint failed: quantity > 0**. c) **FOREIGN KEY constraint failed** — carrots appear in order lines (`ON DELETE RESTRICT`). d) **Accepted**, 1 row — C03 was never ordered. e) **Accepted**, 1 order; `ON DELETE CASCADE` removes its 5 lines: **19** order lines left. f) **CHECK constraint failed: pickup_date IS date(pickup_date)**. g) With `with con:` around the three INSERTs: V05 does not exist → **FOREIGN KEY constraint failed**, the whole transaction is rolled back — still 9 orders and 19 lines. With V04: 10 orders, 21 lines. Without the transaction, order 11 and its first line would remain as a half-recorded order.

Marking: one point per question; questions 2, 3 and 6 need the explanation as well as the query.
:::

## Part C: Measure, Clean, Load — The Sports Club

The sports club's office exports its member list. Rules agreed with the board: birth date filled, an ISO date and not before 1920 · postcode exactly five digits · e-mail filled with one `@` and no spaces · department one of Football, Tennis, Swimming · one row per person (name + birth date).

```python
import io
import pandas as pd

raw = """member_no,name,birth_date,postcode,e_mail,department
S01,Paul Meier,2004-03-12,69115,paul.meier@example.org,Football
S02,Eva Lorenz,12.05.1998,68163,,Tennis
S03,Jan Wolf,2011-09-30,6911,jan.wolf@example.net,Football
S04,Paul Meier,2004-03-12,69115,p.meier@example.org,football
S05,Ida Kühn,,68526,ida.kuehn@example.com,Swimming
S06,Tom Berg,1890-01-01,68723,tom.berg@example.org,Tennis
S07,Lea Graf,2009-07-14,69469,lea graf@example.com,Handball
S08,Max Roth,2001-11-02,68165,max.roth@example.org,Swimming
"""
df = pd.read_csv(io.StringIO(raw), dtype=str)
departments = ["Football", "Tennis", "Swimming"]
```

1. By hand: calculate the **completeness** and **validity** of the birth date and the e-mail address, the validity of the postcode and the department, and the **uniqueness** (simple ratio, validity measured on the filled values). Name the defective rows.
2. Predict the five printed numbers, then run the code:
   ```python
   print(df["birth_date"].isna().sum())
   born = pd.to_datetime(df["birth_date"], format="%Y-%m-%d", errors="coerce")
   print(born.isna().sum())
   print((born < "1920-01-01").sum())
   df["department"] = df["department"].str.strip().str.capitalize()
   print(df["department"].isin(departments).sum())
   print(df.duplicated(subset=["name", "birth_date"]).sum())
   ```
3. Decide a **treatment** (repair, set to missing, drop, flag, ask) for S02, S03, S04, S06 and S07, with a reason.
4. Which **two** of the rules would you also enforce with a `CHECK` or `UNIQUE` constraint in the club's database — and why is that better than cleaning every export?
5. Why does `dtype=str` matter here? What happens to S03's postcode without it?

::: answer lines=16
:::

::: solution
1. Ratios (computed with pandas 3.0.6):
   - Birth date: completeness 1 − 1/8 = **87.5 %** (S05 missing); validity on 7 filled values 1 − 2/7 = **71.4 %** (S02 German format, S06 before 1920).
   - E-mail: completeness 1 − 1/8 = **87.5 %** (S02 missing); validity 1 − 1/7 = **85.7 %** (S07 contains a space).
   - Postcode: validity 1 − 1/8 = **87.5 %** (S03 has four digits).
   - Department: validity 1 − 2/8 = **75 %** (S04 lower case, S07 Handball is not a department).
   - Uniqueness: 1 − 1/8 = **87.5 %** (S01 and S04: same name and birth date — one person, two rows).
2. **1** (missing birth date) · **2** (S05 missing plus S02 not parsable, coerced to NaT) · **1** (S06) · **7** (after standardising, only Handball remains invalid) · **1** (S04 is a duplicate of S01; `keep="first"` marks only the second row).
3. S02: **repair** the date to 1998-05-12 — a format defect, the value is recoverable; ask for the e-mail. S03: **ask** (or set to missing and flag) — a missing digit cannot be guessed; the street and city could help. S04: duplicate — **merge** with S01, keep one member number and re-point everything that refers to S04; ask which e-mail address is current. S06: **flag and ask** — 1890 is almost certainly a default or typing error; do not invent a date. S07: **ask** — fix the e-mail (likely lea.graf@…) and the department; Handball might be a new department the board has to decide on (a reference list question).
4. For example `CHECK (birth_date IS date(birth_date) AND birth_date >= '1920-01-01')`, `CHECK (length(postcode) = 5)`, `CHECK (department IN (…))` or a foreign key to a department table, `UNIQUE (name, birth_date)` (weak: two different people can share both). Constraints **prevent** the defect at the source; cleaning only moves the defect in each copy, every month again (session 14, fix at the source).
5. Without `dtype=str`, pandas reads postcode as an **integer** column (observed: int64). S03 stays 6911 (no information lost here), but a postcode such as 06108 would become 6108 — the leading zero is lost and a valid value turns invalid. Codes and identifiers are text, not numbers.

Marking: 1 point per sub-task, item 1 needs numerator and denominator for every ratio.
:::

## Part D: Pipeline, Star and Rules — The Coworking Space

The coworking space's door system records every **badge scan** (scan_id, member_no, door, timestamp). Every night the system exports the scans of the previous day as a CSV file; sometimes a day is **exported again** with corrections. The management wants to analyse **attendance per day, weekday, plan and floor** — and the sales team wants to use the scans to send upgrade offers to members who come in more often than their plan includes.

1. Describe the pipeline in three steps (E, T, L). Which **load strategy** do you choose for re-exported days — append, replace or upsert — and on which key? What does "idempotent" mean here?
2. Name **three checks** the pipeline should log after every run, with an example threshold.
3. Design a **star schema**: business process, grain, at least three dimensions and two facts. Which measure is **not additive**?
4. The IT team suggests a cloud **data lake** for the scans. Argue for or against with two criteria.
5. **Access to data** (not legal advice): are the scans personal data? Who is the controller? May the sales team use them for upgrade offers? Name one **principle** and one **role** (data owner, data steward, custodian) that matters.

::: answer lines=18
:::

::: solution
1. **E**: read the nightly CSV (set separator, encoding and types explicitly), keep the raw file. **T**: parse timestamps, map doors to floors, drop test badges, derive check-in/check-out pairs or presence per day. **L**: **upsert** on **scan_id** (primary key) in one transaction — a re-exported day replaces its corrected rows and adds missing ones without duplicates. Append would duplicate the day; replacing the whole table loses history. Idempotent: running the load for the same file twice gives the same table as running it once.
2. Freshness (latest scan not older than one day), volume (number of scans within e.g. ±50 % of the same weekday's average; 0 scans on a workday is an alarm), schema (expected columns and types), validity (every member_no exists in the member table; no timestamps in the future). Each run writes a row to a run log; someone has to read it.
3. Process: attendance (badge scans). Grain: **one member present on one day** (or one scan — then attendance must be derived in the query). Dimensions: date (weekday, month), member (plan, membership start), floor/door, optionally time of day. Facts: hours present (additive), number of scans (additive), number of visits. **Not additive**: occupancy rate in % per floor and day, and "number of distinct members" (cannot be summed over days — semi-/non-additive); compute them from the base facts.
4. **Against** (the stronger case here): the data is small, structured and from one source — a relational database or a small warehouse (even SQLite) meets the need; a lake adds cost and needs a catalogue to avoid a swamp. **For** would need e.g. many unstructured sources (camera data, sensor streams) or ML use cases. Choose the simplest architecture that fits (session 18).
5. Yes: scans relate to identified members — **personal data**; the coworking space is the **controller**. Using them for upgrade offers is a **new purpose**: purpose limitation — check compatibility, inform the members, and for e-mail advertising consent may be needed; aggregated attendance per plan is less intrusive (data minimisation). Storage limitation: define a deletion period for raw scans. Role: the community or member manager as **data owner** decides about use; a **data steward** maintains definitions (what counts as a visit) and quality rules; IT as **custodian** runs the door system.

Marking: 2 points each for items 1–5 (10 points).
:::

## Exam-Style Practice Task: The Car-Sharing Company

*Practice, not from an exam.* This task mixes all parts of the course in the form and length of an exam-style task. The car-sharing company has **stations** (station code, name, city), **vehicles** (licence plate, model; each vehicle belongs to exactly one home station), **customers** (customer number, name) and **trips** (trip number, vehicle, customer, start time, end time, kilometres, price).

1. Write the `CREATE TABLE` statement for `trip` with all constraints the description needs, plus a rule that the end time is after the start time and the kilometres are not negative. (4 points)
2. With the data below, write a query for (a) the **number of trips, kilometres and revenue per station** — stations without trips with 0 — highest revenue first, and (b) the **customers without a trip**. Give both results. (5 points)
3. Explain the error and correct the query: `SELECT customer_no, sum(price) FROM trip WHERE sum(price) > 20 GROUP BY customer_no;` Give the corrected result. (2 points)
4. The trips are loaded every night from the booking system. Which **extraction** (full or incremental) and which **load** strategy do you recommend? Name one check for the run log. (3 points)
5. For a star schema on trips: state the **grain**, two dimensions and two facts. (3 points)
6. The trips will also store **GPS tracks**, and the app shows them on an **OpenStreetMap** map. Name one GDPR principle that applies to the tracks and one licence obligation of the map data. (3 points)

::: columns
**station**

| station_code | name | city |
|---|---|---|
| S1 | Bismarckplatz | Heidelberg |
| S2 | Hauptbahnhof | Mannheim |
| S3 | Schloss | Schwetzingen |

**customer**

| customer_no | name |
|---|---|
| C1 | Aylin Demir |
| C2 | Ben Schäfer |
| C3 | Clara Vogt |
| C4 | David Nowak |
|||
**vehicle**

| plate | model | station_code |
|---|---|---|
| HD-CS 101 | ID.3 | S1 |
| HD-CS 102 | Zoe | S1 |
| MA-CS 201 | ID.3 | S2 |
| MA-CS 202 | 500e | S2 |
| HD-CS 301 | Zoe | S3 |
:::

**trip**

| trip_no | plate | customer_no | start_time | end_time | km | price |
|---|---|---|---|---|---|---|
| 1 | HD-CS 101 | C1 | 2027-06-01 08:10 | 2027-06-01 09:05 | 18 | 9.50 |
| 2 | HD-CS 101 | C2 | 2027-06-01 17:30 | 2027-06-01 19:00 | 42 | 16.00 |
| 3 | HD-CS 102 | C1 | 2027-06-02 07:45 | 2027-06-02 08:20 | 11 | 6.20 |
| 4 | MA-CS 201 | C3 | 2027-06-02 12:00 | 2027-06-02 15:30 | 95 | 31.50 |
| 5 | MA-CS 202 | C2 | 2027-06-03 09:00 | 2027-06-03 09:40 | 14 | 7.10 |
| 6 | HD-CS 102 | C3 | 2027-06-03 18:15 | 2027-06-03 18:50 | 9 | 5.40 |

::: answer lines=26
:::

::: solution
All SQL was run in SQLite 3.45.1 on exactly these tables; results as observed.

1. Model solution:

```sql
CREATE TABLE trip (
    trip_no      INTEGER PRIMARY KEY,
    plate        TEXT    NOT NULL
                 REFERENCES vehicle (plate) ON DELETE RESTRICT,
    customer_no  TEXT    NOT NULL
                 REFERENCES customer (customer_no) ON DELETE RESTRICT,
    start_time   TEXT    NOT NULL,
    end_time     TEXT    NOT NULL,
    km           INTEGER NOT NULL CHECK (km >= 0),
    price        NUMERIC NOT NULL CHECK (price >= 0),
    CHECK (end_time > start_time)
);
```

   Observed: a trip ending at 09:30 after a start at 10:00 fails with "CHECK constraint failed: end_time > start_time"; a trip for plate HD-CS 999 fails with "FOREIGN KEY constraint failed" (with `PRAGMA foreign_keys = ON`). The text comparison works because the times are in ISO format (`YYYY-MM-DD HH:MM`).

2. (a) `SELECT s.station_code, s.name, count(t.trip_no) AS trips, coalesce(sum(t.km), 0) AS km, coalesce(sum(t.price), 0) AS revenue FROM station s LEFT JOIN vehicle v ON v.station_code = s.station_code LEFT JOIN trip t ON t.plate = v.plate GROUP BY s.station_code, s.name ORDER BY revenue DESC;` → **S2 Hauptbahnhof 2 trips, 109 km, 38.6** · **S1 Bismarckplatz 4, 80, 37.1** · **S3 Schloss 0, 0, 0**. With `count(*)`, S3 gets 1.
   (b) `SELECT c.customer_no, c.name FROM customer c WHERE NOT EXISTS (SELECT 1 FROM trip t WHERE t.customer_no = c.customer_no);` → **C4 David Nowak**.
3. Error **misuse of aggregate: sum()**: WHERE filters rows before grouping and cannot use aggregates. Fix: `SELECT customer_no, sum(price) FROM trip GROUP BY customer_no HAVING sum(price) > 20;` → **C2 23.1, C3 36.9**.
4. **Incremental** extraction with a watermark (e.g. trips with end_time or a change timestamp after the last successful run) — full extraction grows every night. **Upsert** on trip_no in one transaction, so that corrected trips replace old rows and a rerun creates no duplicates (idempotent). Check: number of trips per night within an expected range, or freshness (latest end_time not older than one day), or no trips with unknown plate.
5. Grain: **one trip**. Dimensions: date (start date, weekday), vehicle (model, home station, city), customer (or customer segment), time of day. Facts: km, price, duration in minutes (all additive); revenue per km is a ratio — compute it from the sums (here 75.7 € / 189 km ≈ 0.401 € per km observed; the average of the per-trip ratios is 0.422, which over-weights short trips).
6. GDPR: GPS tracks linked to a customer are personal data (location) — **data minimisation** (store only what the purpose needs, e.g. start and end station) or **storage limitation** (delete tracks after a defined period); purpose and legal basis must be clear. OpenStreetMap data is under the **ODbL**: credit OpenStreetMap, and share a **derived database** under the same licence if it is distributed (share-alike). (Teaching material, not legal advice.)

Marking guide (20 points):

- Item 1: primary key and NOT NULL foreign keys 2 · CHECKs for km/price 1 · CHECK end after start 1
- Item 2: (a) LEFT JOINs over vehicle 1, count of a trip column and coalesce 1, result 1 · (b) query 1, result 1
- Item 3: cause 1 · fix with result 1
- Item 4: incremental with watermark 1 · upsert / idempotent 1 · one check 1
- Item 5: grain 1 · dimensions 1 · facts 1
- Item 6: principle applied to GPS tracks 2 · licence obligation 1
:::

## Optional Challenge: Trace One Question Through the Course {.optional}

The owner of Velo Neckar asks: **"Do we sell fewer accessories on rainy Saturdays — and may we show the result with the weather data in a public blog post?"** List the steps from the raw data to the published answer. For each step, name the **session**, the **concept** and **one thing that can go wrong**.

::: answer lines=14
:::

::: solution
A good answer has at least six steps in a sensible order, for example:

1. **Business question and data** (sessions 1–2): which data is needed — till receipts (structured), weather (semi-structured JSON). Risk: a vague question ("rainy" undefined).
2. **Model and schema** (3–7): product, sale, sale_line with keys and constraints. Risk: product group stored as free text in each line (update anomaly).
3. **Query** (8–10): accessories revenue per day with `GROUP BY` and a join to the weather. Risk: summing after joining two 1:N paths (doubled revenue).
4. **Quality** (13–14): missing or duplicate receipts, wrong product groups. Risk: valid but inaccurate data (a sale booked on the wrong day).
5. **Access** (15): weather from the Bright Sky API (DWD data). Risk: not checking the status code, no timeout, no saved raw response.
6. **Integration** (16): ETL into daily weather and sales tables, upsert, run log. Risk: a failed night load nobody notices.
7. **Warehouse** (17): star with fact_sales and dim_date (day type), dim_product (group), dim_weather. Risk: wrong grain or summing a non-additive measure.
8. **Architecture** (18): a small relational warehouse is enough; a lake only with a catalogue. Risk: files without owner or licence.
9. **Rules** (19): the result is aggregated (no personal data), but the weather data is **CC BY 4.0** — the blog post needs the attribution line. Risk: attribution lost along the lineage.

Marking: one point per correct step with session and concept, up to 8; one point for a realistic risk in at least four steps.
:::

## References {.references}

- Chen, P. P.-S. (1976). The entity-relationship model—Toward a unified view of data. *ACM Transactions on Database Systems, 1*(1), 9–36. https://doi.org/10.1145/320434.320440
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Government Data Quality Hub. (2021, June 24). *Meet the data quality dimensions*. GOV.UK. https://www.gov.uk/government/news/meet-the-data-quality-dimensions
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- Pipino, L. L., Lee, Y. W., & Wang, R. Y. (2002). Data quality assessment. *Communications of the ACM, 45*(4), 211–218. https://doi.org/10.1145/505248.506010
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1. http://data.europa.eu/eli/reg/2016/679/oj
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
