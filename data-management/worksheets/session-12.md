---
course: Data Management
session: 12
title: Project Workshop and Catch-Up
subtitle: Mixed practice for Parts A–B — data modelling, normalisation and SQL I–IV on the bike shop and the coworking space
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet is a revision sheet for Parts A and B (sessions 3–11). It mixes all topics: ER modelling, mapping, normalisation, defining tables, queries, joins, aggregation, subqueries, views and transactions. Tasks 1–3 and the exam-style task can be done on paper; for tasks 4–6 you need Jupyter with Python's built-in `sqlite3` module (SQLite 3.39 or newer for `FULL OUTER JOIN` in task 5; check with `sqlite3.sqlite_version`). Tasks 4 and 5 extend the bike shop database by **purchase orders to suppliers**: build the database from [bikeshop-schema.sql](data/bikeshop-schema.sql), [bikeshop-data.sql](data/bikeshop-data.sql) and [bikeshop-data-session09.sql](data/bikeshop-data-session09.sql), add your own tables from task 4, then load [bikeshop-purchasing-session12.sql](data/bikeshop-purchasing-session12.sql). All names in the data are fictional. The terms follow the session slides, which are based on Chen (1976), Staud (2005), Elmasri and Navathe (2016, Chapters 3–7, 9 and 14) and the SQLite documentation (SQLite, n.d.-a, n.d.-b, n.d.-c, n.d.-d).

```python
import sqlite3

con = sqlite3.connect("bikeshop.db")
con.execute("PRAGMA foreign_keys = ON")
# fresh start: run all three scripts again
for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
               "bikeshop-data-session09.sql"]:
    with open(script, encoding="utf-8") as f:
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

## True or False Across Parts A and B

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. A weak entity type is identified by its own partial key alone.
2. An M:N relationship is mapped to a relation of its own; its primary key contains the foreign keys to both participating relations.
3. A relation in 2NF whose primary key consists of a single attribute is automatically in 3NF.
4. The functional dependency A → B means: each value of B belongs to exactly one value of A.
5. In SQLite, a foreign key is checked as soon as the table has a `REFERENCES` clause.
6. `count(*)` and `count(price)` always return the same number.
7. If the subquery returns a NULL, `WHERE x NOT IN (subquery)` is never true.
8. A view stores a copy of the result of its query.
9. A `LEFT JOIN` returns at least as many rows as the left table has.
10. Atomicity means that a committed transaction survives a crash.

::: answer lines=12
:::

::: solution
1. **False.** It is identified by the key of its owner **plus** its partial key (e.g. order 4711, line 2).
2. **True.** Example: JOB_MECHANIC(job_no, employee_no) with the composite primary key. Relationship attributes go into the same relation.
3. **False.** A single-attribute key makes 2NF automatic (there is no "part" of the key), but a non-key attribute may still depend on another non-key attribute (transitive dependency), which violates 3NF.
4. **False.** It is the other way round: each value of A determines exactly one value of B; one B value can belong to many A values.
5. **False.** Foreign key enforcement is off by default and must be switched on for every connection with `PRAGMA foreign_keys = ON` (SQLite, n.d.-d).
6. **False.** `count(*)` counts rows, `count(price)` only the non-NULL prices (bike shop: 15 and 13).
7. **True.** For a value that is not in the list, `NOT IN` is NULL (UNKNOWN), not TRUE, and for a value in the list it is FALSE (SQLite, n.d.-c, Section 8). Use `NOT EXISTS`.
8. **False.** A view is a stored query; every use runs the query again, so it is always up to date. A copy is made with `CREATE TABLE … AS SELECT`.
9. **True.** Every left row appears at least once — with NULLs if it has no partner, several times if it has several partners.
10. **False.** That is **durability**. Atomicity means all or nothing: if one statement of the transaction fails, none of its changes remain.

Marking: one point per statement; for false statements the point requires a correct correction.
:::

## From Case to Tables: Riding Courses

Velo Neckar wants to offer **e-bike riding courses**. Model the following in Chen notation with keys, cardinalities and participation, then map your model to a relational schema. Reuse the existing tables CUSTOMER(**customer_no**, …) and EMPLOYEE(**employee_no**, name).

- A **course type** has a course code, a title, a duration in hours and a list price.
- A course type is offered on several **dates**; it runs at most once per day. For each course date, the start time and the maximum number of participants are stored.
- Each course date is taught by exactly one **instructor**. Instructors are employees with a riding instructor licence (licence number); mechanics and salespeople can also be instructors.
- **Customers book** course dates. For each booking, the price actually paid and whether the customer rents a bike for the course are stored.
- Some course types **require** other course types (e.g. "Mountain e-bike" requires "E-bike basics").

::: hint
Look for one weak entity type, one specialisation, one M:N relationship with attributes and one recursive relationship.
:::

::: answer lines=16
:::

::: solution
**ER model**

- *Course type* (course_code as key, title, duration_h, list_price).
- *Course date*: **weak entity type**, owner *Course type*, partial key course_date (it runs at most once per day); attributes start_time, max_participants. Identifying relationship 1:N with total participation of *Course date*.
- *Instructor* (licence_no) as a **subclass** of *Employee*. Partial (most employees are not instructors) and **overlapping** with *Mechanic* and *Salesperson* (an instructor can also be a mechanic). Accept a separate specialisation of *Employee* by the criterion "has a licence".
- **teaches** between *Instructor* and *Course date*, 1:N; total participation of *Course date* (exactly one instructor), partial of *Instructor*.
- **books** between *Customer* and *Course date*, M:N with attributes price_paid and rental_bike; both participations partial.
- **requires** on *Course type*, recursive M:N with the roles *course* and *prerequisite*, partial on both sides.

**Relational schema**

- COURSE_TYPE(**course_code**, title, duration_h, list_price)
- REQUIRES(**course_code** → COURSE_TYPE, **required_code** → COURSE_TYPE)
- INSTRUCTOR(**employee_no** → EMPLOYEE, licence_no), licence_no UNIQUE
- COURSE_DATE(**course_code** → COURSE_TYPE, **course_date**, start_time, max_participants, *instructor_no* → INSTRUCTOR), instructor_no NOT NULL
- COURSE_BOOKING(**customer_no** → CUSTOMER, **course_code, course_date** → COURSE_DATE, price_paid, rental_bike)

Points to check: the weak entity type gets owner key + partial key as primary key; the 1:N relationship **teaches** becomes a foreign key on the N side (COURSE_DATE); the foreign key of COURSE_BOOKING to COURSE_DATE is **composite**; price_paid is history and belongs to the booking, list_price to the course type (pitfall 2 of session 4).

Marking (8 points): weak entity type with owner and partial key 2 · specialisation with constraints 1 · teaches 1 · books with attributes 1 · requires with roles 1 · relational schema with all keys and foreign keys 2.
:::

## Normalise the Purchase Order List

Until now, Velo Neckar records its purchase orders to suppliers in one spreadsheet:

| order_no | order_date | supplier_no | supplier_name | supplier_city | part_no | part_name | quantity | unit_cost |
|---|---|---|---|---|---|---|---|---|
| 701 | 2027-01-08 | S1 | Rad-Großhandel Süd | Stuttgart | P-101 | Inner tube 28 inch | 20 | 3.10 |
| 701 | 2027-01-08 | S1 | Rad-Großhandel Süd | Stuttgart | P-103 | Brake pads (pair) | 10 | 5.80 |
| 702 | 2027-01-15 | S2 | E-Motion Parts | Köln | P-109 | E-bike battery 500 Wh | 2 | 455.00 |
| 703 | 2027-02-03 | S1 | Rad-Großhandel Süd | Stuttgart | P-101 | Inner tube 28 inch | 30 | 2.95 |
| 703 | 2027-02-03 | S1 | Rad-Großhandel Süd | Stuttgart | P-106 | Brake cable | 25 | 1.60 |
| 703 | 2027-02-03 | S1 | Rad-Großhandel Süd | Stuttgart | P-107 | Gear cable | 25 | 1.60 |
| 704 | 2027-02-20 | S3 | Kette & Co | Mannheim | P-104 | Chain 9-speed | 5 | 12.40 |
| 704 | 2027-02-20 | S3 | Kette & Co | Mannheim | P-105 | Chain 11-speed | 5 | 21.00 |

Each order goes to exactly one supplier; a part appears at most once per order; `unit_cost` is the price Velo Neckar paid per unit in that order.

1. Write down all non-trivial functional dependencies you can justify from the business rules.
2. Determine the primary key.
3. In which normal form is the table? Give the reason.
4. Give one example each of an insertion, an update and a deletion anomaly.
5. Decompose the table into 3NF relations. Which of them already exists in the bike shop database?
6. A colleague wants to drop `unit_cost`, because `spare_part` has a list price. What do you answer?

::: answer lines=14
:::

::: solution
1. order_no → order_date, supplier_no · supplier_no → supplier_name, supplier_city · part_no → part_name · {order_no, part_no} → quantity, unit_cost. (Transitively, order_no → supplier_name, supplier_city.) **Not** part_no → unit_cost: P-101 cost 3.10 in order 701 and 2.95 in order 703.
2. **{order_no, part_no}**: it determines all other attributes, and neither attribute alone does.
3. **1NF**, not 2NF: all values are atomic, but order_date, supplier_no (and the supplier data) depend on order_no alone, and part_name on part_no alone — **partial dependencies** on a part of the key. There are also **transitive** dependencies (order_no → supplier_no → supplier_name).
4. Insertion: a new supplier (e.g. S4) cannot be stored before the first order to it (order_no and part_no would be NULL). Update: if Rad-Großhandel Süd moves, its city must be changed in four rows; forgetting one gives contradicting data. Deletion: deleting order 702 deletes the only information about the supplier E-Motion Parts.
5. SUPPLIER(**supplier_no**, name, city) · PURCHASE_ORDER(**order_no**, order_date, *supplier_no* → SUPPLIER) · PURCHASE_LINE(**order_no** → PURCHASE_ORDER, **part_no** → SPARE_PART, quantity, unit_cost) · SPARE_PART(**part_no**, name, …) **already exists** in the bike shop database; part_name is not stored again.
6. Keep it: `unit_cost` is a **different fact** — the purchase price at the time of the order, depending on (order_no, part_no). The list price is the current selling price. It is history, not redundancy (same as `price_charged` in `repair_line`, session 6).

Marking: 1 point each for items 1–6; item 1 requires the composite determinant of quantity and unit_cost.
:::

## Purchasing in SQL

Create the three tables of task 3 in the bike shop database. Use exactly these names and column orders, so that the data script fits:

- `supplier (supplier_no, name, city)` — supplier numbers are texts such as `'S1'`
- `purchase_order (order_no, order_date, supplier_no)`
- `purchase_line (order_no, part_no, quantity, unit_cost)`

Business rules: every order has a date and a supplier; a supplier with orders must not be deleted; if an order is deleted, its lines go with it; every line refers to an existing spare part; quantities are positive whole numbers, costs are not negative; dates are valid ISO dates.

1. Write the `CREATE TABLE` statements and run them. Then load [bikeshop-purchasing-session12.sql](data/bikeshop-purchasing-session12.sql). Expected row counts: supplier 4, purchase_order 5, purchase_line 10.
2. Predict, then run each statement below **in this order**. Note the result and the constraint that decides it.

| # | Statement |
|---|---|
| a | `INSERT INTO purchase_line VALUES (705, 'P-120', 4, 9.90)` |
| b | `INSERT INTO purchase_order VALUES (706, '2027-02-30', 'S1')` |
| c | `INSERT INTO purchase_line VALUES (701, 'P-101', 5, 3.10)` |
| d | `INSERT INTO supplier (supplier_no, name, city) VALUES ('S5', 'Velo Teile Rhein', NULL)` |
| e | `DELETE FROM supplier WHERE supplier_no = 'S3'` |
| f | `INSERT INTO purchase_line VALUES (705, 'P-110', 0, 2.00)` |
| g | `DELETE FROM purchase_order WHERE order_no = 704` — how many purchase lines are left? |

::: hint
For valid dates, use the pattern from `bikeshop-schema.sql`: `CHECK (job_date IS date(job_date))`. Try `SELECT date('2027-02-30')` to see why it works.
:::

::: answer lines=14
:::

::: solution
Model solution (run in SQLite 3.45.1 after the three bike shop scripts; the data script then loads without error):

```sql
CREATE TABLE supplier (
    supplier_no  TEXT NOT NULL PRIMARY KEY,
    name         TEXT NOT NULL,
    city         TEXT
);
CREATE TABLE purchase_order (
    order_no     INTEGER PRIMARY KEY,
    order_date   TEXT    NOT NULL CHECK (order_date IS date(order_date)),
    supplier_no  TEXT    NOT NULL REFERENCES supplier (supplier_no) ON DELETE RESTRICT
);
CREATE TABLE purchase_line (
    order_no   INTEGER NOT NULL REFERENCES purchase_order (order_no) ON DELETE CASCADE,
    part_no    TEXT    NOT NULL REFERENCES spare_part (part_no),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_cost  NUMERIC NOT NULL CHECK (unit_cost >= 0),
    PRIMARY KEY (order_no, part_no)
);
```

Results observed with this solution:

- a) **FOREIGN KEY constraint failed**: part P-120 does not exist in spare_part.
- b) **CHECK constraint failed: order_date IS date(order_date)**: `date('2027-02-30')` returns `'2027-03-02'`, which is not equal to the input.
- c) **UNIQUE constraint failed: purchase_line.order_no, purchase_line.part_no**: P-101 is already a line of order 701 (primary key).
- d) **Accepted** (1 row): city is optional.
- e) **FOREIGN KEY constraint failed**: order 704 refers to S3 (`ON DELETE RESTRICT`; the default NO ACTION gives the same error here).
- f) **CHECK constraint failed: quantity > 0**.
- g) **Accepted**, 1 order deleted; `ON DELETE CASCADE` removes its two lines: **8** purchase lines are left.

Alternatives: `INTEGER PRIMARY KEY` for supplier_no is wrong here (the numbers are texts). Without `PRAGMA foreign_keys = ON` (observed), a) and e) are accepted and g) does not cascade: **11** lines are left, among them the orphan line for P-120 and two lines of a deleted order — the solution has then not been tested in a connection with foreign keys switched on.
:::

## Lab: Mixed Business Questions

Fresh database: the three bike shop scripts, the model solution of task 4 and the purchasing data script. Predict the number of rows first.

1. Every supplier with the **number of orders** — suppliers without orders too.
2. Every purchase order with date, supplier name and **order value** (quantity × unit cost), highest first.
3. Spare parts that were **never purchased**. Which of them were nevertheless **used** in repairs?
4. A colleague compares purchases and repairs per part:
   `SELECT p.part_no, sum(pl.quantity) AS bought, sum(rl.quantity) AS used FROM spare_part p JOIN purchase_line pl ON pl.part_no = p.part_no JOIN repair_line rl ON rl.part_no = p.part_no GROUP BY p.part_no;`
   Why does it report **100** inner tubes bought? Write a correct query that also shows the average unit cost and the average price charged per part.
5. The **most recent** unit cost of every purchased part (date of the latest order containing it).
6. Create a view `purchase_value` (order_no, order_date, supplier_no, value). Use it to compare **purchases and parts revenue per month**, so that every month with purchases **or** repairs appears.
7. Record a new order 706 to supplier S4 on 2027-04-12 with two lines — 10 × P-110 at 3.20 and 6 × P-111 at 11.50 — in **one transaction**. Test it first with the wrong part number P-113 in the second line.

::: hint
Question 4: what does one row of the join mean when a part has two purchase lines and two repair lines? Aggregate each table on its own level first (session 10).
:::

::: answer lines=20
:::

::: solution
All results observed in SQLite 3.45.1.

1. `SELECT s.supplier_no, s.name, count(o.order_no) AS orders FROM supplier s LEFT JOIN purchase_order o ON o.supplier_no = s.supplier_no GROUP BY s.supplier_no, s.name ORDER BY orders DESC;` → S1 3, S2 1, S3 1, **S4 0**. `count(*)` would give S4 1.
2. purchase_order JOIN supplier JOIN purchase_line, `GROUP BY o.order_no, o.order_date, s.name`, `sum(l.quantity * l.unit_cost)` → 702 (E-Motion Parts) 910 · 703 (Rad-Großhandel Süd) 168.5 · 704 (Kette & Co) 167.0 · 705 (Rad-Großhandel Süd) 155.5 · 701 (Rad-Großhandel Süd) 120.0.
3. `SELECT p.part_no, p.name FROM spare_part p WHERE NOT EXISTS (SELECT 1 FROM purchase_line l WHERE l.part_no = p.part_no);` → P-102 Tyre, P-110 Bell, P-111 LED front light, P-112 Mudguard set (4 rows). Used in repairs: P-102, P-110 and P-111 (add `AND EXISTS (SELECT 1 FROM repair_line r WHERE r.part_no = p.part_no)`) — they were bought before purchasing was recorded, or the data is incomplete (a data quality question for session 13).
4. The join returns one row per **pair** of purchase line and repair line. P-101 has 2 purchase lines (20 + 30) and 2 repair lines, so every purchase quantity is counted twice: 100 instead of 50 (and 4 used instead of 2). Correct: aggregate first, then join:
   `SELECT p.part_no, p.name, b.bought, b.avg_cost, u.used, u.avg_charged FROM spare_part p JOIN (SELECT part_no, sum(quantity) AS bought, round(sum(quantity * unit_cost) / sum(quantity), 2) AS avg_cost FROM purchase_line GROUP BY part_no) b ON b.part_no = p.part_no JOIN (SELECT part_no, sum(quantity) AS used, round(sum(quantity * price_charged) / sum(quantity), 2) AS avg_charged FROM repair_line GROUP BY part_no) u ON u.part_no = p.part_no ORDER BY p.part_no;` → 8 rows, e.g. P-101 50 / 3.01 / 2 / 6.9 · P-103 20 / 5.95 / 6 / 12.0 · P-109 2 / 455.0 / 1 / 649.0. A weighted average (sum of values / sum of quantities) is better than `avg(unit_cost)`; accept `avg()` with a remark.
5. Correlated subquery: `SELECT l.part_no, o.order_date, l.unit_cost FROM purchase_line l JOIN purchase_order o ON o.order_no = l.order_no WHERE o.order_date = (SELECT max(o2.order_date) FROM purchase_line l2 JOIN purchase_order o2 ON o2.order_no = l2.order_no WHERE l2.part_no = l.part_no) ORDER BY l.part_no;` → 8 rows, e.g. P-101 2027-02-03 2.95 · P-103 2027-03-05 6.1 · P-109 2027-01-15 455.
6. `CREATE VIEW purchase_value AS SELECT o.order_no, o.order_date, o.supplier_no, sum(l.quantity * l.unit_cost) AS value FROM purchase_order o JOIN purchase_line l ON l.order_no = o.order_no GROUP BY o.order_no, o.order_date, o.supplier_no;` Then two derived tables per month (purchases from the view, revenue from repair_job JOIN repair_line) combined with `FULL OUTER JOIN … ON r.month = m.month` and `coalesce(m.month, r.month)` → 2027-01: 1030.0 / 28.4 · 2027-02: 335.5 / 76.4 · 2027-03: 155.5 / 733.2 · **2027-04: 0 / 103.4**. With a `LEFT JOIN` from the purchases, April is missing (no purchases in April).
7. `with con:` around the three INSERT statements (order, two lines). With P-113: **FOREIGN KEY constraint failed**, and the whole transaction is rolled back — still 5 orders and 10 lines (observed). With P-111: 6 orders, 12 lines. Without the transaction, the order and the first line would remain as a half-recorded order.

Marking: 1 point per question; question 4 needs both the explanation and a correct query.
:::

## Review a Team's Schema: Student Housing Office

A project team models a student housing office. Houses have rooms (numbered 1, 2, 3 … within each house); tenants sign leases for a room with a start date, an optional end date and the monthly rent agreed in the lease. Their milestone 3 script starts like this:

```sql
CREATE TABLE house  (house_no INTEGER PRIMARY KEY, street TEXT, city TEXT);
CREATE TABLE room   (room_no  INTEGER PRIMARY KEY,
                     house_no INTEGER REFERENCES house (house_no),
                     size_m2  REAL, rent REAL);
CREATE TABLE tenant (tenant_no INTEGER PRIMARY KEY, name TEXT NOT NULL,
                     e_mail TEXT, rooms TEXT);          -- e.g. '3, 7'
CREATE TABLE lease  (lease_no  INTEGER PRIMARY KEY,
                     tenant_no INTEGER REFERENCES tenant (tenant_no),
                     room_no   INTEGER REFERENCES room (room_no),
                     tenant_name TEXT,
                     start_date TEXT, end_date TEXT, monthly_rent REAL);
```

1. Use the checklist "Schema and Data" from the session slides. Find **at least five** problems and name the concept behind each (key, normal form, constraint, …).
2. The team says `monthly_rent` in `lease` is redundant because `room` has a rent. Do you agree?
3. Write an improved version of `room` and `lease`. Name two statements that the team's version accepts and yours rejects.

::: answer lines=16
:::

::: solution
1. Problems (any five):
   - `room_no` alone as primary key: rooms are numbered **within** a house, so room 1 can exist only once in the whole database (weak entity type, key = house_no + room_no). Observed: inserting room 1 of house 2 fails with "UNIQUE constraint failed: room.room_no".
   - `lease` refers to the room by room_no only; it needs the **composite** foreign key (house_no, room_no).
   - `tenant.rooms` stores a list in one cell (**1NF** violated) and repeats what the leases already say (redundancy).
   - `lease.tenant_name` depends on tenant_no, not on lease_no: **transitive dependency** (3NF violated), update anomaly.
   - No `NOT NULL` on the foreign keys and start_date: a lease without a tenant or room is possible.
   - No date checks: `'01.10.2027'` and an end date before the start date are accepted (both observed with the team's script).
   - No `PRAGMA foreign_keys = ON`, no referential actions chosen; `REAL` for money (session 7 recommends NUMERIC or cents as INTEGER).
2. **No.** `monthly_rent` is the rent **agreed in this lease** (history); `room.rent` is the current list rent. When the room rent rises, old leases must keep their rent — same as `price_charged` vs. `list_price` in the bike shop.
3. Improved version (tested in SQLite 3.45.1 with `PRAGMA foreign_keys = ON`):

```sql
CREATE TABLE room (
    house_no INTEGER NOT NULL REFERENCES house (house_no) ON DELETE RESTRICT,
    room_no  INTEGER NOT NULL,
    size_m2  NUMERIC CHECK (size_m2 > 0),
    rent     NUMERIC NOT NULL CHECK (rent >= 0),
    PRIMARY KEY (house_no, room_no));
CREATE TABLE lease (
    lease_no     INTEGER PRIMARY KEY,
    tenant_no    INTEGER NOT NULL REFERENCES tenant (tenant_no) ON DELETE RESTRICT,
    house_no     INTEGER NOT NULL,
    room_no      INTEGER NOT NULL,
    start_date   TEXT    NOT NULL CHECK (start_date IS date(start_date)),
    end_date     TEXT    CHECK (end_date IS date(end_date)),
    monthly_rent NUMERIC NOT NULL CHECK (monthly_rent >= 0),
    FOREIGN KEY (house_no, room_no) REFERENCES room (house_no, room_no) ON DELETE RESTRICT,
    CHECK (end_date IS NULL OR end_date > start_date));
```

   Plus: drop `tenant.rooms` and `lease.tenant_name`; `e_mail` UNIQUE. Observed with this version: room 1 of house 2 is accepted; a lease for room 3 of house 1 (does not exist) fails with "FOREIGN KEY constraint failed"; start date `'01.10.2027'` fails with "CHECK constraint failed: start_date IS date(start_date)"; end date 2027-03-31 for a start on 2027-10-01 fails with "CHECK constraint failed: end_date IS NULL OR end_date > start_date"; an open-ended lease (end_date NULL) is accepted.

Marking: 5 points for five problems with the concept, 1 point for item 2, 2 points for item 3 (composite key and composite foreign key are required).
:::

## Exam-Style Task: Meeting Rooms in the Coworking Space

This task is in the style of an exam question covering Parts A and B. The coworking space from worksheets 5, 7 and 10 now rents out **meeting rooms**. Each room has a room code, a name, a capacity and an hourly rate. Members (member number, name, optional plan) book a room for a date, a start time and a number of whole hours (1 to 10). The rate actually paid per hour is stored, because members on the FIX plan get a discount. A room cannot be booked twice with the same start time on the same day.

1. Draw an ER model (Chen notation) for *Plan*, *Member*, *Room* and the room bookings, with keys, cardinalities and participation. (4 points)
2. Map your model to a relational schema; mark primary and foreign keys. (3 points)
3. The manager keeps the list ROOM_BOOKING_LIST(room_code, room_name, booking_date, start_time, member_no, member_name, hours, rate_paid) with the key (room_code, booking_date, start_time). In which normal form is it? Justify with the functional dependencies and decompose it into 3NF. (3 points)
4. Write the `CREATE TABLE` statement for the room bookings with all constraints the rules above need. Name one business rule your table cannot enforce. (4 points)
5. With the data below, write a query for (a) the **revenue per room** (hours × rate paid), rooms without bookings with 0, highest first, and (b) the **members without a room booking**. Give both results. (4 points)
6. Explain the result or error of each query, and correct it. (2 points)
   - `SELECT r.name, count(*) AS bookings FROM room r LEFT JOIN room_booking b ON b.room_code = r.room_code GROUP BY r.room_code, r.name;`
   - `SELECT member_no, sum(hours) FROM room_booking WHERE sum(hours) > 3 GROUP BY member_no;`

::: columns
**member**

| member_no | name | plan_code |
|---|---|---|
| M1 | Jonas Weber | FLEX |
| M2 | Sara Öztürk | FIX |
| M3 | Tim Lang | NULL |
| M4 | Lena Graf | FLEX |
|||
**room**

| room_code | name | capacity | hourly_rate |
|---|---|---|---|
| R1 | Neckar | 6 | 25 |
| R2 | Rhein | 12 | 40 |
| R3 | Quiet box | 2 | 10 |
:::

**room_booking**

| room_code | booking_date | start_time | member_no | hours | rate_paid |
|---|---|---|---|---|---|
| R1 | 2027-06-01 | 09:00 | M1 | 2 | 25 |
| R1 | 2027-06-01 | 14:00 | M2 | 3 | 20 |
| R2 | 2027-06-02 | 10:00 | M2 | 4 | 40 |
| R1 | 2027-06-08 | 09:00 | M1 | 1 | 25 |
| R2 | 2027-06-09 | 13:00 | M3 | 2 | 40 |


::: answer lines=28
:::

::: solution
All SQL was run in SQLite 3.45.1 on exactly these tables (plan: FLEX 99, FIX 249); results as observed.

1. *Plan* (plan_code, monthly_fee) 1:N **has** *Member* (member_no, name), partial on both sides (a member may have no plan). *Room* (room_code, name, capacity, hourly_rate). The booking is best modelled as a **weak entity type** *Room booking* with owner *Room* and partial key (booking_date, start_time), attributes hours and rate_paid, plus a 1:N relationship **makes** from *Member* (each booking has exactly one member: total participation of the booking). Alternative accepted: M:N **books** between *Member* and *Room* with attributes booking_date, start_time, hours, rate_paid — if the answer notes that one member can book the same room several times, so date and time must be part of the key.
2. PLAN(**plan_code**, monthly_fee) · MEMBER(**member_no**, name, *plan_code* → PLAN) · ROOM(**room_code**, name, capacity, hourly_rate) · ROOM_BOOKING(**room_code** → ROOM, **booking_date, start_time**, *member_no* → MEMBER, hours, rate_paid), member_no NOT NULL.
3. FDs: (room_code, booking_date, start_time) → member_no, hours, rate_paid · room_code → room_name · member_no → member_name. room_name depends on **part** of the key → not 2NF, so the list is in **1NF**. member_name depends on the non-key attribute member_no → transitive (would also violate 3NF). Decomposition: ROOM(room_code, room_name), MEMBER(member_no, member_name), ROOM_BOOKING(room_code, booking_date, start_time, member_no, hours, rate_paid) — matches item 2.
4. Model solution:

```sql
CREATE TABLE room_booking (
    room_code    TEXT    NOT NULL REFERENCES room (room_code) ON DELETE RESTRICT,
    booking_date TEXT    NOT NULL CHECK (booking_date IS date(booking_date)),
    start_time   TEXT    NOT NULL CHECK (start_time GLOB '[0-2][0-9]:[0-5][0-9]'),
    member_no    TEXT    NOT NULL REFERENCES member (member_no) ON DELETE RESTRICT,
    hours        INTEGER NOT NULL CHECK (hours BETWEEN 1 AND 10),
    rate_paid    NUMERIC NOT NULL CHECK (rate_paid >= 0),
    PRIMARY KEY (room_code, booking_date, start_time)
);
```

   Observed: a second booking of R1 on 2027-06-01 at 09:00 fails with "UNIQUE constraint failed: room_booking.room_code, room_booking.booking_date, room_booking.start_time"; the date 2027-06-31 fails the date CHECK; a booking of R1 on 2027-06-01 at 10:00 is accepted, although R1 is booked from 09:00 for 2 hours. Not enforceable with these constraints: **overlapping** bookings (R1 from 09:00 for 2 hours and another booking at 10:00 have different keys), or that the number of participants fits the capacity. Accept other correct rules (e.g. rate_paid at most hourly_rate).
5. (a) `SELECT r.room_code, r.name, coalesce(sum(b.hours * b.rate_paid), 0) AS revenue FROM room r LEFT JOIN room_booking b ON b.room_code = r.room_code GROUP BY r.room_code, r.name ORDER BY revenue DESC;` → R2 Rhein **240**, R1 Neckar **135**, R3 Quiet box **0**.
   (b) `SELECT m.member_no, m.name FROM member m WHERE NOT EXISTS (SELECT 1 FROM room_booking b WHERE b.member_no = m.member_no);` → **M4 Lena Graf**. `NOT IN` is also correct here, because member_no in room_booking is NOT NULL.
6. First query: Quiet box gets **1** instead of 0 — `count(*)` counts the row the outer join adds with NULLs. Fix: `count(b.member_no)` (any NOT NULL column of room_booking) → Neckar 3, Rhein 2, Quiet box 0. Second query: error **misuse of aggregate: sum()** — WHERE filters rows before grouping and cannot use aggregates. Fix: `GROUP BY member_no HAVING sum(hours) > 3` → M2 7.

Marking guide (20 points):

- Item 1: entity types with keys 1 · booking as weak entity (or M:N with date and time in the key) 2 · cardinalities and participation 1
- Item 2: all relations with primary keys 1 · foreign keys incl. NOT NULL member_no 1 · composite primary key of the booking 1
- Item 3: FDs 1 · normal form with reason 1 · decomposition 1
- Item 4: composite primary key 1 · foreign keys 1 · CHECKs for date, hours and rate 1 · one rule that cannot be enforced 1
- Item 5: (a) LEFT JOIN with coalesce or total 1, result 1 · (b) query 1, result 1
- Item 6: one point per query (explanation and fix)
:::

## References {.references}

- Chen, P. P.-S. (1976). The entity-relationship model—Toward a unified view of data. *ACM Transactions on Database Systems, 1*(1), 9–36. https://doi.org/10.1145/320434.320440
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- SQLite. (n.d.-a). *Pragma statements supported by SQLite*. Retrieved October 21, 2026, from https://www.sqlite.org/pragma.html
- SQLite. (n.d.-b). *SELECT*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_select.html
- SQLite. (n.d.-c). *SQL language expressions*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_expr.html
- SQLite. (n.d.-d). *SQLite foreign key support*. Retrieved October 21, 2026, from https://www.sqlite.org/foreignkeys.html
- Staud, J. L. (2005). *Datenmodellierung und Datenbankentwurf: Ein Vergleich aktueller Methoden*. Springer. https://doi.org/10.1007/b137949
