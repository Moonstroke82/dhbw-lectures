---
course: Data Management
session: 10
title: SQL IV: Aggregation and Beyond
subtitle: Practice tasks on aggregate functions, GROUP BY and HAVING, subqueries, views, indexes and transactions
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 10 on your own or with your project team. Task 1 can be done on paper; for all other tasks you need Jupyter with Python's built-in `sqlite3` module. Tasks 4 and 5 and the optional challenge use the bike shop database: build it from [bikeshop-schema.sql](data/bikeshop-schema.sql), [bikeshop-data.sql](data/bikeshop-data.sql) and [bikeshop-data-session09.sql](data/bikeshop-data-session09.sql), as in session 9. Tasks 2, 3 and 6 create small tables of their own; run their scripts in a new `:memory:` database. All names in the data are fictional. The statements follow the session slides, which are based on Elmasri and Navathe (2016, Chapters 7, 17 and 20), Haerder and Reuter (1983) and the SQLite documentation (SQLite, n.d.-a, n.d.-b, n.d.-c).

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

## Aggregates and NULL on Paper

The coworking space from earlier worksheets now records how many hours a desk was used. `hours` is NULL while the member has not checked out yet.

| booking_no | member_no | desk_no | booking_date | hours |
|---|---|---|---|---|
| 1 | M1 | D4 | 2027-05-03 | 8 |
| 2 | M2 | D7 | 2027-05-03 | 4 |
| 3 | M1 | D4 | 2027-05-04 | NULL |
| 4 | M3 | D2 | 2027-05-04 | 6 |
| 5 | M2 | D7 | 2027-05-05 | 4 |
| 6 | M1 | D2 | 2027-05-05 | NULL |

Without running them, write down the result of each query.

```sql
-- a
SELECT count(*), count(hours), count(DISTINCT member_no) FROM booking;
-- b
SELECT sum(hours), avg(hours), min(hours), max(hours) FROM booking;
-- c
SELECT sum(hours) / count(*) FROM booking;
-- d
SELECT member_no, count(*), sum(hours) FROM booking GROUP BY member_no;
-- e
SELECT sum(hours), count(*), avg(hours) FROM booking WHERE desk_no = 'D9';
-- f
SELECT avg(coalesce(hours, 0)) FROM booking;
```

Then answer: **g)** The manager asks for "the average length of a booking". Which of the results b, c and f would you report, and what would you add to it?

::: hint
`count(*)` counts rows, every other aggregate skips NULL. In SQLite, dividing an integer by an integer gives an integer.
:::

::: answer lines=12
:::

::: solution
All results were checked by running the queries in SQLite 3.45.1 on exactly this table (`hours` declared NUMERIC).

- a) **6, 4, 3**: six rows, four known hours, three different members.
- b) **22, 5.5, 4, 8**: sum, average, minimum and maximum of the four known values; the two NULLs are ignored, so the average is 22 / 4.
- c) **3**: 22 / 6 with integer division (3.67 cut off). It divides by **all** rows, including the two without hours, and is therefore neither the average of the known values nor exact.
- d) M1: 3 bookings, 8 hours · M2: 2, 8 · M3: 1, 6. M1's two open bookings count in `count(*)` but not in the sum.
- e) **NULL, 0, NULL**: no row matches; `count` gives 0, `sum` and `avg` give NULL (`total(hours)` would give 0.0).
- f) **3.666…**: NULL is treated as 0 hours, so the open bookings pull the average down.
- g) Report **5.5 hours** (b) as "average length of the **completed** bookings" and add "4 of 6 bookings; 2 still open". f would be correct only if an open booking really meant 0 hours, which is false; c is wrong for both reasons.

Marking: one point per item a–g; for b, c, e and f the point requires the correct treatment of NULL or of integer division.
:::

## GROUP BY and HAVING: The Food Co-op

Use the food co-op tables from worksheet 9 (farm and product). Create them again in a new `:memory:` database with this script:

```sql
CREATE TABLE farm (
    farm_id  INTEGER PRIMARY KEY,
    name     TEXT    NOT NULL,
    village  TEXT
);
CREATE TABLE product (
    product_no  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    category    TEXT,
    price       NUMERIC CHECK (price >= 0),
    farm_id     INTEGER REFERENCES farm (farm_id),
    organic     INTEGER CHECK (organic IN (0, 1))       -- NULL: not known yet
);
INSERT INTO farm (farm_id, name, village) VALUES
    (1, 'Hofgut Neckarblick',   'Ladenburg'),
    (2, 'Obsthof Bergstraße',   'Weinheim'),
    (3, 'Ziegenhof Odenwald',   'Wilhelmsfeld'),
    (4, 'Gärtnerei Sonnenfeld', 'Edingen'),
    (5, 'Imkerei Kraichgau',    'Sinsheim');
INSERT INTO product (product_no, name, category, price, farm_id, organic) VALUES
    (1,  'Potatoes',    'vegetables', 2.80, 1,    1),
    (2,  'Carrots',     'vegetables', 1.90, 1,    1),
    (3,  'Apple juice', 'drinks',     3.50, 2,    0),
    (4,  'Apples',      'fruit',      2.40, 2,    NULL),
    (5,  'Goat cheese', 'dairy',      6.90, 3,    1),
    (6,  'Milk',        'dairy',      1.30, 3,    0),
    (7,  'Honey',       NULL,         7.50, NULL, 1),
    (8,  'Pumpkin',     'vegetables', NULL, 1,    1),
    (9,  'Pears',       'fruit',      2.90, 2,    1),
    (10, 'Yoghurt',     'dairy',      1.10, 3,    NULL),
    (11, 'Onions',      'vegetables', 1.50, 4,    0);
```

Write one query for each request and give the result.

1. Number of products **per category**, largest category first. What happens to Honey?
2. Per category: number of products, number of products **with a price**, cheapest and most expensive price.
3. Per farm (with its name): number of priced products and average price, rounded to two decimals — only farms with **at least two** priced products.
4. **All five** farms with their number of products and their number of **organic** products, farms without products too.
5. Categories whose **cheapest** product costs less than 2 €. Then explain how this differs from `SELECT category, count(*) FROM product WHERE price < 2 GROUP BY category;`.

::: hint
For request 4: which column do you count after a LEFT JOIN? For the organic products, `sum(p.organic = 1)` counts the rows where the comparison is true, because SQLite stores TRUE as 1.
:::

::: answer lines=14
:::

::: solution
All queries were run in SQLite 3.45.1 on exactly these tables; results as observed.

1. `SELECT category, count(*) AS products FROM product GROUP BY category ORDER BY products DESC;` → vegetables 4, dairy 3, fruit 2, drinks 1, **NULL 1**. Honey has no category: all NULLs form **one group** of their own.
2. `SELECT category, count(*), count(price), min(price), max(price) FROM product GROUP BY category;` → NULL 1/1/7.5/7.5 · dairy 3/3/1.1/6.9 · drinks 1/1/3.5/3.5 · fruit 2/2/2.4/2.9 · vegetables **4/3**/1.5/2.8 (Pumpkin has no price).
3. `SELECT f.name, count(p.price) AS priced, round(avg(p.price), 2) AS avg_price FROM farm f JOIN product p ON p.farm_id = f.farm_id GROUP BY f.farm_id, f.name HAVING count(p.price) >= 2 ORDER BY avg_price DESC;` → Ziegenhof Odenwald 3 / 3.1, Obsthof Bergstraße 3 / 2.93, Hofgut Neckarblick **2** / 2.35. With `count(*)` instead of `count(p.price)`, Hofgut Neckarblick would show 3 products, but the average is over 2 prices; the request asks for priced products.
4. `SELECT f.name, count(p.product_no) AS products, sum(p.organic = 1) AS organic FROM farm f LEFT JOIN product p ON p.farm_id = f.farm_id GROUP BY f.farm_id, f.name;` → Hofgut Neckarblick 3 / 3, Obsthof Bergstraße 3 / 1, Ziegenhof Odenwald 3 / 1, Gärtnerei Sonnenfeld 1 / 0, Imkerei Kraichgau **0 / NULL**. `count(*)` would give Imkerei Kraichgau 1 product (the row added by the outer join). For a 0 instead of NULL: `count(CASE WHEN p.organic = 1 THEN 1 END)` or `coalesce(sum(…), 0)`; accept any of these. Apples and Yoghurt (organic unknown) are correctly not counted as organic.
5. `SELECT category, min(price) FROM product GROUP BY category HAVING min(price) < 2;` → dairy 1.1, vegetables 1.5. The second query filters **rows** before grouping and counts the cheap products per category: dairy 2, vegetables 2. It returns the same categories here, but answers a different question ("how many cheap products per category") and could not express conditions such as "average price below 2 €", which need HAVING.

Marking: one point per request; for 4 the point requires that all five farms appear with 0 products for Imkerei Kraichgau.
:::

## Find the Mistakes: Sports Club Fees

The sports club from earlier worksheets stores its members (with mentors, as in worksheet 9), department memberships and fee payments. Create the tables in a new `:memory:` database:

```sql
CREATE TABLE member (
    member_no     TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    date_of_birth TEXT,
    joining_date  TEXT NOT NULL DEFAULT CURRENT_DATE,
    member_type   TEXT CHECK (member_type IN ('adult', 'youth')),
    mentor_no     TEXT REFERENCES member (member_no) ON DELETE SET NULL
);
CREATE TABLE department_member (
    member_no   TEXT NOT NULL REFERENCES member (member_no),
    department  TEXT NOT NULL,
    joined_on   TEXT,
    PRIMARY KEY (member_no, department)
);
CREATE TABLE payment (
    payment_no  INTEGER PRIMARY KEY,
    member_no   TEXT    NOT NULL REFERENCES member (member_no),
    paid_on     TEXT    NOT NULL,
    amount      NUMERIC NOT NULL CHECK (amount > 0)
);
INSERT INTO member VALUES
    ('M01', 'Sabine Keller', '1975-04-12', '2010-03-01', 'adult', NULL),
    ('M02', 'Omar Haddad',   '1988-09-30', '2015-06-15', 'adult', 'M01'),
    ('M03', 'Lea Hofmann',   '2011-02-14', '2026-09-01', 'youth', 'M02'),
    ('M04', 'Finn Schäfer',  '2012-07-08', '2025-01-10', 'youth', NULL),
    ('M05', 'Sven Maier',    '2008-11-23', '2020-05-01', 'youth', 'M01'),
    ('M06', 'Ida Yilmaz',    '1995-01-05', '2027-01-15', 'adult', NULL),
    ('M07', 'Tom Berg',      '2013-03-19', '2027-02-01', 'youth', 'M02'),
    ('M08', 'Nina Graf',     '1969-12-02', '2018-10-01', 'adult', NULL);
INSERT INTO department_member VALUES
    ('M01', 'football', '2010-03-01'), ('M01', 'tennis', '2016-04-01'),
    ('M02', 'football', '2015-06-15'), ('M03', 'football', '2026-09-01'),
    ('M05', 'tennis',   '2020-05-01'), ('M07', 'football', '2027-02-01'),
    ('M08', 'tennis',   '2018-10-01'), ('M08', 'football', '2019-03-01');
INSERT INTO payment (payment_no, member_no, paid_on, amount) VALUES
    (1, 'M01', '2027-01-10', 120), (2, 'M02', '2027-01-12', 120),
    (3, 'M03', '2027-01-15',  60), (4, 'M05', '2027-01-20',  60),
    (5, 'M01', '2027-02-01',  35), (6, 'M08', '2027-01-05', 120),
    (7, 'M02', '2027-03-01',  35), (8, 'M07', '2027-02-03',  60);
```

The club's treasurer wrote one statement for each request. None does what was asked. For each: run it, describe what goes wrong, write a corrected statement and give the correct result.

| # | Request | Statement |
|---|---|---|
| a | Number of members per member type | `SELECT member_type, count(*) FROM member;` |
| b | Members who paid more than 100 € in total | `SELECT member_no, sum(amount) FROM payment WHERE sum(amount) > 100 GROUP BY member_no;` |
| c | Number of payments per member, members without payments too | `SELECT m.name, count(*) FROM member m LEFT JOIN payment p ON p.member_no = m.member_no GROUP BY m.member_no, m.name;` |
| d | Per member: total paid and number of departments | `SELECT m.name, sum(p.amount), count(d.department) FROM member m JOIN payment p ON p.member_no = m.member_no JOIN department_member d ON d.member_no = m.member_no GROUP BY m.member_no, m.name;` |
| e | Members who are nobody's mentor | `SELECT name FROM member WHERE member_no NOT IN (SELECT mentor_no FROM member);` |
| f | Average total amount per **paying** member | `SELECT avg(amount) FROM payment;` |

::: hint
For d, run the query without `GROUP BY` and the aggregates and look at Sabine Keller's rows. For e, look at the list the subquery returns.
:::

::: answer lines=18
:::

::: solution
All wrong and corrected statements were run in SQLite 3.45.1; results as observed.

- a) **Missing GROUP BY / bare column**: SQLite returns **one** row, ('adult', 8): the count of all members with a member type taken from some row. Most other DBMS reject the query. Fix: `… FROM member GROUP BY member_type;` → adult 4, youth 4.
- b) **Aggregate in WHERE**: error "misuse of aggregate: sum()". WHERE filters rows before any sum exists. Fix: `SELECT member_no, sum(amount) AS total FROM payment GROUP BY member_no HAVING sum(amount) > 100;` → M01 155, M02 155, M08 120.
- c) **count(\*) after a LEFT JOIN**: Finn Schäfer and Ida Yilmaz have no payment but get **1**, because count(\*) counts the row added by the outer join. Fix: `count(p.payment_no)` → Sabine Keller 2, Omar Haddad 2, Lea Hofmann 1, Finn Schäfer **0**, Sven Maier 1, Ida Yilmaz **0**, Tom Berg 1, Nina Graf 1.
- d) **Two independent 1:N paths multiply** (the "doubled revenue"): Sabine Keller has 2 payments × 2 departments = 4 rows, so she shows 310 € and 4 departments instead of 155 € and 2; Nina Graf 240 € instead of 120 €. Also, the inner joins drop members without payments. Fix: aggregate each path on its own, e.g. with scalar subqueries: `SELECT m.name, (SELECT total(p.amount) FROM payment p WHERE p.member_no = m.member_no) AS paid, (SELECT count(*) FROM department_member d WHERE d.member_no = m.member_no) AS departments FROM member m;` → Sabine Keller 155 / 2, Omar Haddad 155 / 1, Lea Hofmann 60 / 1, Finn Schäfer 0 / 0, Sven Maier 60 / 1, Ida Yilmaz 0 / 0, Tom Berg 60 / 1, Nina Graf 120 / 2. Derived tables (aggregate in FROM, then LEFT JOIN) are also correct.
- e) **NOT IN with NULL in the list**: the subquery returns the mentor_no of every member, including NULLs, so NOT IN is never TRUE → **0 rows**. Fix: `WHERE member_no NOT IN (SELECT mentor_no FROM member WHERE mentor_no IS NOT NULL)` or, better, `SELECT m.name FROM member m WHERE NOT EXISTS (SELECT 1 FROM member t WHERE t.mentor_no = m.member_no);` → 6 rows: Lea Hofmann, Finn Schäfer, Sven Maier, Ida Yilmaz, Tom Berg, Nina Graf.
- f) **Wrong granularity**: avg(amount) is the average **payment** (610 / 8 payments = 76.25). The request asks for the average **total per paying member**: `SELECT avg(total) FROM (SELECT member_no, sum(amount) AS total FROM payment GROUP BY member_no);` → 610 / 6 = **101.67**. (By coincidence, 610 / 8 members is also 76.25 — the club happens to have 8 payments and 8 members; this does not make the original query right.)

Marking: one point per item for the explanation and the correction with the correct result together (6 points).
:::

## Lab: Subqueries and Views on the Bike Shop

Answer each question with **one** statement on the bike shop database (all three scripts, fresh start). Predict the number of rows first.

1. For each brand, the **most expensive** bike: brand, frame number, model, price. Use a **correlated subquery**. Then compare your result with `SELECT brand, frame_no, model, max(price) FROM bike GROUP BY brand;` — what differs, and why should you not rely on the second query?
2. Customers who do **not** own a Gazelle. First try `NOT IN` with a subquery on bike, then `NOT EXISTS`. Explain the difference in the results.
3. Create a view **part_usage** with one row per spare part: part number, name, list price, number of repair lines it appears in, units used and revenue (0 for parts never used). Use the view to list (a) the parts never used and (b) the parts used in 3 or more units.
4. The repair jobs whose parts revenue is **above the average job revenue**. State which average you use and give its value.
5. The mechanic(s) with the **most** repair jobs. Write it so that **all** mechanics would be returned if two shared the first place.

::: hint
Question 5 needs a subquery on a grouped result: first the number of jobs per mechanic, then the maximum of these numbers. `ORDER BY … LIMIT 1` returns exactly one row even when there is a tie.
:::

::: answer lines=16
:::

::: solution
All statements were run on a fresh database built from the three course scripts (SQLite 3.45.1); results as observed.

1. `SELECT b.brand, b.frame_no, b.model, b.price FROM bike b WHERE b.price = (SELECT max(b2.price) FROM bike b2 WHERE b2.brand = b.brand) ORDER BY b.brand;` → 6 rows: Brompton BRO860 1749, Cube CUB202 3299, Gazelle GZT885 2799, KTM KTM530 3599, Riese & Müller RIE420 5899, Trek TRK311 1099. Canyon and Scott are missing: their only bike has price NULL, so the comparison is UNKNOWN. The GROUP BY query returns 8 rows with the same bikes plus Canyon and Scott (max NULL). Its frame_no and model are **bare columns**: SQLite happens to take them from the row with the maximum (a documented special case for a single min/max), but other DBMS reject the query, and with two aggregates in the list the values could come from any row (SQLite, n.d.-b).
2. `SELECT name FROM customer WHERE customer_no NOT IN (SELECT customer_no FROM bike WHERE brand = 'Gazelle');` → **0 rows**: two Gazelles are in stock, so the list contains NULL. `SELECT c.name FROM customer c WHERE NOT EXISTS (SELECT 1 FROM bike b WHERE b.customer_no = c.customer_no AND b.brand = 'Gazelle');` → **11 rows**: everybody except Lukas Brandt (GZT885). NOT EXISTS only asks whether a matching row exists and is not affected by NULL.
3. `CREATE VIEW part_usage AS SELECT p.part_no, p.name, p.list_price, count(l.job_no) AS times_used, coalesce(sum(l.quantity), 0) AS units, coalesce(sum(l.quantity * l.price_charged), 0) AS revenue FROM spare_part p LEFT JOIN repair_line l ON l.part_no = p.part_no GROUP BY p.part_no, p.name, p.list_price;` → 12 rows. (a) `SELECT part_no, name FROM part_usage WHERE times_used = 0;` → P-112 Mudguard set. (b) `… WHERE units >= 3` → P-103 Brake pads (pair) 6, P-106 Brake cable 3. Note P-110 Bell: used once, revenue 0 (given away). Without LEFT JOIN and coalesce, P-112 would be missing or show NULL.
4. Average over the **10 jobs with repair lines**: `SELECT job_no, revenue FROM (SELECT job_no, sum(quantity * price_charged) AS revenue FROM repair_line GROUP BY job_no) WHERE revenue > (SELECT avg(revenue) FROM (SELECT sum(quantity * price_charged) AS revenue FROM repair_line GROUP BY job_no));` → average **94.14**; jobs 507 (649) and 511 (103.4). Averaging over all 12 jobs (jobs 506 and 512 with 0, e.g. with the view `job_revenue` from the slides) gives 78.45 and the same two jobs. Either is correct if stated; the average per **repair line** (58.84) is not what was asked.
5. `SELECT e.name, count(*) AS jobs FROM job_mechanic jm JOIN employee e ON e.employee_no = jm.employee_no GROUP BY jm.employee_no, e.name HAVING count(*) = (SELECT max(n) FROM (SELECT count(*) AS n FROM job_mechanic GROUP BY employee_no));` → Deniz Arslan, 5. `ORDER BY jobs DESC LIMIT 1` gives the same here, but hides a tie.

Marking: two points each for questions 1, 2 and 4 (query and explanation), one point each for 3 and 5.
:::

## Indexes and Transactions in the Bike Shop

Work on a fresh bike shop database.

1. Run `EXPLAIN QUERY PLAN` for each query and note whether SQLite **scans** or **searches**, and with which index:
   - `SELECT * FROM repair_line WHERE job_no = 511;`
   - `SELECT * FROM repair_line WHERE part_no = 'P-103';`
   - `SELECT * FROM customer WHERE e_mail = 'anna.berger@example.org';`
   - `SELECT * FROM customer WHERE city = 'Heidelberg';`

   Explain why the first two differ although both columns are part of the primary key of repair_line. Then create an index that helps the second query and check the plan again.
2. The shop wants spare part names to be unique. Create a suitable index and try `INSERT INTO spare_part VALUES ('P-113', 'Bell', 9.90);`. What happens? Why would a unique index on `customer (city)` be a bad idea — and what happens if you try to create it?
3. A new repair job consists of three statements: the job, one repair line and the mechanic assignment. Run them in Python inside **one** `with con:` block, using mechanic number **9** (who does not exist), and check afterwards whether job 513 exists. Repeat without the `with` block, calling `con.commit()` after each statement. Compare the two outcomes.
4. Name the ACID property that each situation is about:
   a) After the shop's laptop crashed, the sale confirmed one second before the crash is still in the database.
   b) The bookkeeping connection, which is reading this month's revenue, does not see a repair job that the counter is just entering.
   c) A repair line for job 513 is never stored without the job itself.
   d) The DBMS rejects a repair line whose quantity is 0.

```sql
INSERT INTO repair_job (job_no, job_date, description, frame_no)
       VALUES (513, '2027-04-12', 'New tyre, front', 'BRO860');
INSERT INTO repair_line (job_no, part_no, quantity, price_charged)
       VALUES (513, 'P-102', 1, 34.90);
INSERT INTO job_mechanic (job_no, employee_no) VALUES (513, 9);
```

::: hint
An index on several columns is sorted by the first column, then by the second — like a phone book sorted by surname, then first name.
:::

::: answer lines=16
:::

::: solution
All steps were run in SQLite 3.45.1 (Python sqlite3); plans and messages as observed (the EXPLAIN QUERY PLAN format may differ in other SQLite versions; SQLite, n.d.-d).

1. `SEARCH repair_line USING INDEX sqlite_autoindex_repair_line_1 (job_no=?)` · `SCAN repair_line` · `SEARCH customer USING INDEX sqlite_autoindex_customer_1 (e_mail=?)` · `SCAN customer`. The primary key (job_no, part_no) has an automatic index sorted by job_no **first**; it helps for job_no, but not for part_no alone (like a phone book for first names). The UNIQUE constraint on e_mail created an index; city has none. After `CREATE INDEX idx_line_part ON repair_line (part_no);` the plan is `SEARCH repair_line USING INDEX idx_line_part (part_no=?)`.
2. `CREATE UNIQUE INDEX idx_part_name ON spare_part (name);` → the insert fails with "UNIQUE constraint failed: spare_part.name" (P-110 is already called Bell). A unique index on city would forbid two customers in the same city, which is not a business rule; creating it fails at once with "UNIQUE constraint failed: customer.city", because the data already has duplicates. Indexes for speed should be plain (non-unique) indexes.
3. With `with con:` the third statement fails ("FOREIGN KEY constraint failed"), the whole transaction is rolled back: job 513 and its repair line do **not** exist (count 0). With a commit after each statement, the job and the line are stored and only the assignment fails: job 513 exists **without a mechanic** — the database is half updated (a job without mechanic now looks like job 512, which is simply not assigned yet). This is atomicity.
4. a) **Durability**, b) **Isolation**, c) **Atomicity**, d) **Consistency** (the CHECK constraint `quantity > 0` keeps the database in a valid state).

Marking: part 1 three points (plans, explanation of the composite key, new index), part 2 two points, part 3 two points, part 4 one point for all four correct.
:::

## Exam-Style Task: Car-Sharing Figures

This task is in the style of an exam question. The car-sharing company from worksheets 8 and 9 stores customers, vehicles and bookings. `booking.customer_no` and `booking.licence_plate` are NOT NULL foreign keys; `km` is NULL while a trip has not been billed yet.

::: columns
**customer**

| customer_no | name |
|---|---|
| 1 | Aylin Şahin |
| 2 | Moritz Lang |
| 3 | Greta Huber |
| 4 | David Osei |

**vehicle** (extract)

| licence_plate | model |
|---|---|
| MA-CS 101 | VW ID.3 |
| MA-CS 102 | Opel Corsa |
| MA-CS 103 | VW ID.3 |
| MA-CS 104 | Fiat 500e |
| MA-CS 105 | Skoda Octavia |
| MA-CS 106 | Opel Corsa |
| MA-CS 107 | Renault Zoe |
| MA-CS 108 | Skoda Octavia |
|||
**booking**

| booking_no | customer_no | licence_plate | start_date | km |
|---|---|---|---|---|
| 1 | 3 | MA-CS 103 | 2027-01-28 | 35 |
| 2 | 1 | MA-CS 101 | 2027-02-03 | 12 |
| 3 | 2 | MA-CS 104 | 2027-02-10 | 48 |
| 4 | 1 | MA-CS 107 | 2027-02-14 | NULL |
| 5 | 3 | MA-CS 102 | 2027-02-20 | 110 |
| 6 | 1 | MA-CS 101 | 2027-03-02 | 23 |
| 7 | 2 | MA-CS 105 | 2027-03-05 | 260 |
:::

1. Write a query that lists **every customer** with the number of bookings and the total km driven, customers without bookings with 0 bookings and 0 km. Give the result. (2 points)
2. Write a query that lists the vehicle **models** that were booked **at least twice**, with the number of bookings. Give the result. (2 points)
3. Write a query that lists the bookings whose km are **above the average km** of all billed bookings. Give the average and the result. (2 points)
4. `SELECT count(*), count(km), sum(km), avg(km), sum(km) / count(*) FROM booking;` returns 7, 6, 488, 81.33 and 69. Explain each of the five numbers in one short sentence and say which number is the correct "average trip length". (2 points)
5. At the end of a trip, the system runs two statements: it writes the km into the booking and adds them to the vehicle's mileage. Explain, with the correct ACID property, what can go wrong if the server crashes between the two statements, and how the developer prevents it. (2 points)

::: answer lines=24
:::

::: solution
All statements were run in SQLite 3.45.1 on these tables (the full vehicle table from worksheet 8); results as observed.

1. `SELECT c.name, count(b.booking_no) AS bookings, coalesce(sum(b.km), 0) AS km FROM customer c LEFT JOIN booking b ON b.customer_no = c.customer_no GROUP BY c.customer_no, c.name ORDER BY km DESC;` → Moritz Lang 2 / 308, Greta Huber 2 / 145, Aylin Şahin 3 / 35, David Osei 0 / 0. (Aylin's 35 km are from two billed bookings; booking 4 has no km yet.)
2. `SELECT v.model, count(*) AS bookings FROM booking b JOIN vehicle v ON v.licence_plate = b.licence_plate GROUP BY v.model HAVING count(*) >= 2;` → VW ID.3, 3 (bookings 1, 2 and 6 on two different ID.3 cars).
3. `SELECT booking_no, km FROM booking WHERE km > (SELECT avg(km) FROM booking);` → average **81.33** km (488 / 6); bookings 7 (260) and 5 (110).
4. count(\*) = 7: number of bookings (rows). count(km) = 6: bookings with known km; booking 4 is not billed. sum(km) = 488: total of the known km. avg(km) = 81.33: 488 / 6, the average of the billed trips. sum(km) / count(\*) = 69: 488 / 7 with integer division — divides by an unbilled trip and cuts off the decimals. Correct average trip length: **81.33 km** (of the billed trips).
5. **Atomicity** (all or nothing) is violated: after a crash between the statements, the booking shows the km but the vehicle's mileage was not increased (or the other way round), so the data contradict each other — wrong service intervals and billing later. Prevention: put both statements in **one transaction** (`BEGIN … COMMIT`, or `with con:` in Python); after a crash the DBMS rolls back the unfinished transaction on restart, and once committed, both changes are durable.

Marking guide (10 points):

- Part 1: 1 point for LEFT JOIN with `count(b.booking_no)` (not `count(*)`), 1 point for GROUP BY with 0 km for David Osei (coalesce) and the correct result.
- Part 2: 1 point for join and GROUP BY model, 1 point for HAVING (not WHERE) and the result.
- Part 3: 1 point for the scalar subquery, 1 point for 81.33 and the two bookings.
- Part 4: 1 point for correct explanations of count(\*) vs. count(km) and sum, 1 point for avg vs. integer division and the right choice.
- Part 5: 1 point for atomicity with the inconsistent state, 1 point for the transaction as the solution. Mentioning consistency or durability in addition is fine; naming only isolation gives 0 for the first point.
- Common mistakes: `WHERE count(*) >= 2` (misuse of aggregate); bare `model` without GROUP BY; `km > avg(km)` without subquery; `= NULL`.
:::

## Optional Challenge: A Fair Revenue Share per Mechanic {.optional}

In the session's hands-on question 6, the parts revenue per mechanic added up to 1095.80 €, although the shop's parts revenue is only 941.40 €, because jobs with two mechanics were counted twice.

1. Show the problem: compute the sum of `revenue` over `job_revenue JOIN job_mechanic` and explain the difference to 941.40 € with the job numbers involved. (Create the view `job_revenue` from the slides first.)
2. Write a query that gives each mechanic a **share** of each job's revenue: the revenue divided by the number of mechanics on that job. All five mechanics should appear.
3. Check that the shares add up to 941.40 €. Which job's revenue is still missing from the mechanics' figures, and why does the total still match?
4. Is an equal split a good business rule? Suggest a better basis and say which column the schema would need.

::: answer lines=12
:::

::: solution
All queries were run on a fresh database built from the three course scripts plus the view `job_revenue` from the slides (SQLite 3.45.1); results as observed.

1. `SELECT sum(r.revenue) FROM job_revenue r JOIN job_mechanic jm ON jm.job_no = r.job_no;` → 1095.8. Jobs 502 (21.5), 504 (29.5) and 511 (103.4) have two mechanics each, so their revenue (154.40 €) is counted twice: 941.40 + 154.40 = 1095.80.
2. `SELECT e.name, count(jm.job_no) AS jobs, round(total(r.revenue * 1.0 / (SELECT count(*) FROM job_mechanic x WHERE x.job_no = jm.job_no)), 2) AS revenue_share FROM mechanic m JOIN employee e ON e.employee_no = m.employee_no LEFT JOIN job_mechanic jm ON jm.employee_no = m.employee_no LEFT JOIN job_revenue r ON r.job_no = jm.job_no GROUP BY m.employee_no, e.name ORDER BY revenue_share DESC;` → Sophie Lindner 663.75, Deniz Arslan 135.4, Katrin Vogel 77.2, Jan Hoffmann 65.05, Tim Krause 0.0. The `* 1.0` protects against integer division for whole-euro revenues; total() gives 0.0 instead of NULL for Tim Krause.
3. 663.75 + 135.40 + 77.20 + 65.05 = **941.40**. Job 512 has no mechanic, but also no revenue (0), so nothing is lost; a job **with** revenue but without mechanic would be missing from the mechanics' total — check with `NOT EXISTS` (returns job 512 with revenue 0).
4. An equal split ignores how much each mechanic worked. Better: hours worked per mechanic and job — a new attribute `hours` in `job_mechanic` (the relationship M:N carries it, as in session 4), and then revenue × hours / total hours of the job. Any reasoned basis is acceptable.
:::

## References {.references}

- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Haerder, T., & Reuter, A. (1983). Principles of transaction-oriented database recovery. *ACM Computing Surveys, 15*(4), 287–317. https://doi.org/10.1145/289.291
- SQLite. (n.d.-a). *Built-in aggregate functions*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_aggfunc.html
- SQLite. (n.d.-b). *SELECT*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_select.html
- SQLite. (n.d.-c). *SQL language expressions*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_expr.html
- SQLite. (n.d.-d). *EXPLAIN QUERY PLAN*. Retrieved October 21, 2026, from https://www.sqlite.org/eqp.html
