---
course: Data Management
session: 9
title: SQL III: Joins
subtitle: Practice tasks on inner and outer joins, self joins and join pitfalls
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 9 on your own or with your project team. Task 1 can be done on paper; for all other tasks you need Jupyter with Python's built-in `sqlite3` module. Tasks 3 and 6 use the bike shop database: create it from [bikeshop-schema.sql](data/bikeshop-schema.sql) (session 7), load the sample data from [bikeshop-data.sql](data/bikeshop-data.sql) (session 8) and add the extra rows from [bikeshop-data-session09.sql](data/bikeshop-data-session09.sql) (session 9). Tasks 2, 4 and 5 create small tables of their own; run their scripts in a new `:memory:` database. All names in the data are fictional. The statements follow the session slides, which are based on Elmasri and Navathe (2016, Chapters 6 and 7) and the SQLite documentation (SQLite, n.d.-b). RIGHT and FULL joins need SQLite 3.39.0 or later (SQLite, 2022): check with `SELECT sqlite_version();`.

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

## Join Types on Paper

A language school stores its teachers and courses in two tables. `course.teacher_id` is a foreign key to `teacher`; course C4 has no teacher yet.

::: columns
**teacher**

| teacher_id | name |
|---|---|
| T1 | Leila Ahmadi |
| T2 | Petr Novak |
| T3 | Ana Ferreira |
|||
**course**

| course_id | title | teacher_id |
|---|---|---|
| C1 | English B1 | T1 |
| C2 | Spanish A1 | T1 |
| C3 | German C1 | T2 |
| C4 | French A2 | NULL |
:::

For each query, give the **number of rows** and list the result as pairs (course_id, name). Write NULL where a value is missing.

```sql
-- a
SELECT c.course_id, t.name FROM course c CROSS JOIN teacher t;  -- row count only
-- b
SELECT c.course_id, t.name FROM course c JOIN teacher t
    ON t.teacher_id = c.teacher_id;
-- c
SELECT c.course_id, t.name FROM course c LEFT JOIN teacher t
    ON t.teacher_id = c.teacher_id;
-- d
SELECT c.course_id, t.name FROM course c RIGHT JOIN teacher t
    ON t.teacher_id = c.teacher_id;
-- e
SELECT c.course_id, t.name FROM course c FULL JOIN teacher t
    ON t.teacher_id = c.teacher_id;
-- f
SELECT t.name FROM teacher t LEFT JOIN course c ON c.teacher_id = t.teacher_id
WHERE c.course_id IS NULL;
```

Then answer: **g)** Which of the queries b–e returns the same rows as `FROM teacher t RIGHT JOIN course c ON …`? **h)** Formulate query f as a business question in one sentence.

::: hint
Start with the inner join. An outer join returns the inner join **plus** one extra row for each row of the preserved table that has no partner.
:::

::: answer lines=12
:::

::: solution
All results were checked by running the queries in SQLite 3.45.1 on exactly these tables.

- a) **12** rows (3 teachers × 4 courses): the Cartesian product, no condition.
- b) **3** rows: (C1, Leila Ahmadi), (C2, Leila Ahmadi), (C3, Petr Novak). C4 has no teacher, T3 has no course.
- c) **4** rows: the three from b plus (C4, NULL) — every course is kept.
- d) **4** rows: the three from b plus (NULL, Ana Ferreira) — every teacher is kept.
- e) **5** rows: the three from b plus (C4, NULL) and (NULL, Ana Ferreira).
- f) **1** row: Ana Ferreira.
- g) **c**: `teacher RIGHT JOIN course` keeps every course, exactly like `course LEFT JOIN teacher`; only the column order in `SELECT *` would differ.
- h) "Which teachers do not teach any course (yet)?"

Marking: one point per item a–h. For b–e, the row count and the NULL rows must both be correct; the order of the rows does not matter (there is no ORDER BY).
:::

## Find the Mistakes: Food Co-op Queries

The food co-op from worksheet 8 now also stores its **farms**. Create both tables in a new `:memory:` database with this script:

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

A volunteer wrote one statement for each request. None does what was asked. For each: name the pitfall, explain what goes wrong, write a corrected statement and give the correct result.

| # | Request | Statement |
|---|---|---|
| a | Each product with the name of its farm | `SELECT p.name, f.name FROM product p, farm f;` |
| b | The farms that supply vegetables | `SELECT f.name FROM farm f JOIN product p ON p.farm_id = f.farm_id WHERE p.category = 'vegetables';` |
| c | All farms with their organic products, farms without organic products too | `SELECT f.name, p.name FROM farm f LEFT JOIN product p ON p.farm_id = f.farm_id WHERE p.organic = 1;` |
| d | All products with the village they come from | `SELECT name, village FROM product p LEFT JOIN farm f ON f.farm_id = p.farm_id;` |
| e | Farms that do not supply any product | `SELECT f.name FROM farm f LEFT JOIN product p ON p.farm_id = f.farm_id WHERE p.organic IS NULL;` |
| f | Each product with the name of its farm (second attempt) | `SELECT p.name, f.name FROM product p JOIN farm f ON f.farm_id = p.product_no;` |
| g | Each product with the name of its farm (third attempt) | `SELECT * FROM product NATURAL JOIN farm;` |

::: hint
Run each statement and look at the number of rows first. For g, list the column names the two tables have in common.
:::

::: answer lines=18
:::

::: solution
All wrong and corrected statements were run in SQLite 3.45.1 (Python sqlite3 and the sqlite3 command-line tool); results as observed.

- a) **Missing join condition**: the result is the Cartesian product, 11 × 5 = **55** rows. Fix: `SELECT p.name AS product, f.name AS farm FROM product p JOIN farm f ON f.farm_id = p.farm_id;` → **10** rows; Honey is missing because its farm_id is NULL. If Honey should be listed too, use `LEFT JOIN` (11 rows, farm NULL). Accept both with this explanation; the `AS` names are good practice (both columns are otherwise called `name`).
- b) **Duplicates from 1:N**: Hofgut Neckarblick supplies three vegetables (potatoes, carrots, pumpkin) and appears three times (4 rows). Fix: `SELECT DISTINCT f.name …` → Hofgut Neckarblick, Gärtnerei Sonnenfeld.
- c) **Outer join filtered in WHERE**: for farms without an organic product, `p.organic` is NULL in the added row (or 0), so the WHERE removes them; the result has only 5 rows and no farm without organic products. Fix: move the condition into ON: `… LEFT JOIN product p ON p.farm_id = f.farm_id AND p.organic = 1;` → 7 rows: Hofgut Neckarblick with Potatoes, Carrots, Pumpkin; Obsthof Bergstraße with Pears; Ziegenhof Odenwald with Goat cheese; Gärtnerei Sonnenfeld and Imkerei Kraichgau with NULL.
- d) **Ambiguous column name**: SQLite reports "ambiguous column name: name" — both tables have a column `name`. Fix: `SELECT p.name, f.village FROM product p LEFT JOIN farm f ON f.farm_id = p.farm_id;` → 11 rows, Honey with village NULL.
- e) **NULL meaning two things after an outer join**: `p.organic IS NULL` is also true for real products whose organic status is unknown (Apples, Yoghurt). Wrong result: Obsthof Bergstraße, Ziegenhof Odenwald, Imkerei Kraichgau. Fix: test the partner's primary key, `WHERE p.product_no IS NULL` → only **Imkerei Kraichgau**.
- f) **Wrong join column**: the farm number is compared with the **product** number. The query runs and returns 5 plausible-looking but wrong pairs (e.g. Carrots – Obsthof Bergstraße). Fix: `ON f.farm_id = p.farm_id` (as in a).
- g) **NATURAL JOIN on all common names**: the tables share `farm_id` **and** `name`, so SQLite compares product names with farm names as well → **0** rows. Fix: `JOIN farm USING (farm_id)` or, better, `JOIN … ON f.farm_id = p.farm_id` with qualified columns (10 rows).

Marking: one point per item for naming the pitfall with explanation and correction together (7 points).
:::

## Lab: Business Questions Across Tables

Answer each question with **one** query on the bike shop database (all three scripts, fresh start). Before running a query, predict the number of rows. Write down which join type you use and why.

1. Repair jobs in **March 2027** with date, brand and model of the bike and the **owner's name** — all March jobs.
2. All parts used on the bikes of **Anna Berger**: job number, date, part name, quantity and price charged. Then extend the query so that her repair jobs **without** repair lines also appear.
3. Repair lines in which the **price charged differs from the current list price**, with the part name and both prices.
4. All spare parts with a list price of at least 20 €, and the repair jobs in which they were used — parts that were never used too.
5. Repair jobs for which the shop **cannot send an e-mail** when the bike is ready. Explain the two different reasons that occur.
6. Repair jobs in March 2027 with the name of each mechanic who worked on it **and** the name of that mechanic's supervisor.
7. Employees who are **neither** mechanic **nor** salesperson.

::: hint
For question 7, think about which column you test for NULL: Laura Becker is a salesperson, but her sales target is not known.
:::

::: answer lines=16
:::

::: solution
All queries were run on a fresh database built from the three course scripts; results as observed in Python sqlite3 and the sqlite3 command-line tool.

1. `SELECT j.job_no, j.job_date, b.brand, b.model, c.name AS owner FROM repair_job j JOIN bike b ON b.frame_no = j.frame_no LEFT JOIN customer c ON c.customer_no = b.customer_no WHERE j.job_date BETWEEN '2027-03-01' AND '2027-03-31' ORDER BY j.job_date;` → 5 rows: 506 Scott Paul Richter, 507 KTM Macina Style **NULL**, 508 Gazelle Lukas Brandt, 509 Brompton Elif Demir, 510 Canyon Selin Kaya. With an inner join to customer, job 507 (stock bike KTM530) is missing (4 rows). The join to bike can stay inner: every job has a bike (frame_no NOT NULL).
2. customer → bike → repair_job → repair_line → spare_part with `WHERE c.name = 'Anna Berger'` → 1 row: 501, 2027-01-12, Inner tube 28 inch, 1, 6.9. With `LEFT JOIN repair_line … LEFT JOIN spare_part …` → 2 rows: job 512 appears with NULL part, quantity and price (no parts used yet). Both LEFT JOINs are needed: an inner join to spare_part after the LEFT JOIN would remove job 512 again.
3. `SELECT l.job_no, p.name, p.list_price, l.price_charged FROM repair_line l JOIN spare_part p ON p.part_no = l.part_no WHERE l.price_charged <> p.list_price;` → 2 rows: 503 Brake pads (pair) 12.5 / 11, 508 Bell 8.9 / 0. This is the history from session 4: price_charged keeps the price at the time of the repair.
4. `SELECT p.part_no, p.name, p.list_price, l.job_no FROM spare_part p LEFT JOIN repair_line l ON l.part_no = p.part_no WHERE p.list_price >= 20 ORDER BY p.part_no;` → 7 rows: P-102 (510), P-104 (505), P-105 (511), P-108 (511), P-109 (507), P-111 (509), P-112 (NULL). The price condition is on the **preserved** table, so it belongs in WHERE; in ON it would not filter the parts (all 12 parts would appear).
5. `SELECT j.job_no, b.frame_no, c.name, c.e_mail FROM repair_job j JOIN bike b ON b.frame_no = j.frame_no LEFT JOIN customer c ON c.customer_no = b.customer_no WHERE c.e_mail IS NULL;` → 3 rows: 503 (Mira Okonkwo, no e-mail address), 507 (stock bike, **no customer at all**), 511 (Tobias Krämer, no e-mail address). Here the double meaning of NULL is wanted: both cases need a phone call. To tell them apart, also select `c.customer_no` (NULL only for 507).
6. repair_job → job_mechanic → mechanic → employee (mechanic's name), `LEFT JOIN employee s ON s.employee_no = m.supervisor_no` → 5 rows: 506 Jan Hoffmann / Katrin Vogel, 507 Sophie Lindner / Katrin Vogel, 508 Jan Hoffmann / Katrin Vogel, 509 Deniz Arslan / Katrin Vogel, 510 Jan Hoffmann / Katrin Vogel. The LEFT JOIN is not needed for March (Katrin worked on no March job), but it is the safe choice: with an inner join, any job of Katrin's would vanish.
7. `SELECT e.employee_no, e.name FROM employee e LEFT JOIN mechanic m ON m.employee_no = e.employee_no LEFT JOIN salesperson s ON s.employee_no = e.employee_no WHERE m.employee_no IS NULL AND s.employee_no IS NULL;` → 1 row: 7 Ben Weber. Testing `s.sales_target IS NULL` instead wrongly adds Laura Becker (2 rows).
:::

## Self Joins: The Sports Club Mentors

The sports club from worksheets 7 and 8 stores who mentors whom in the member table itself (`mentor_no REFERENCES member (member_no)`). Create the table in a new `:memory:` database:

```sql
CREATE TABLE member (
    member_no     TEXT PRIMARY KEY,
    name          TEXT NOT NULL,
    date_of_birth TEXT,
    joining_date  TEXT NOT NULL DEFAULT CURRENT_DATE,
    member_type   TEXT CHECK (member_type IN ('adult', 'youth')),
    mentor_no     TEXT REFERENCES member (member_no) ON DELETE SET NULL
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
```

1. List every member who has a mentor, with the **mentor's name**. Then change the query so that **all** members appear.
2. List each member together with their mentor **and the mentor's mentor**.
3. Which members do **not** mentor anybody?
4. Find all **pairs of members who joined in the same year**. Each pair should appear once. (Hint: `substr(joining_date, 1, 4)` returns the year.) How many rows do you get if you leave out the condition that prevents duplicates, and how many without any extra condition at all? Explain the numbers.

::: answer lines=14
:::

::: solution
All queries were run in SQLite 3.45.1 on exactly this table; results as observed.

1. `SELECT m.member_no, m.name, t.name AS mentor FROM member m JOIN member t ON t.member_no = m.mentor_no;` → 4 rows: M02 – Sabine Keller, M03 – Omar Haddad, M05 – Sabine Keller, M07 – Omar Haddad. With `LEFT JOIN` → 8 rows; M01, M04, M06, M08 with mentor NULL. The alias `t` plays the role *mentor*, `m` the role *mentee*; `AS mentor` avoids two result columns called `name`.
2. `SELECT m.name, t.name AS mentor, tt.name AS mentors_mentor FROM member m JOIN member t ON t.member_no = m.mentor_no JOIN member tt ON tt.member_no = t.mentor_no;` → 2 rows: Lea Hofmann – Omar Haddad – Sabine Keller, Tom Berg – Omar Haddad – Sabine Keller. Three aliases of the same table. (With LEFT JOINs, all 8 members appear; accept either if the version is stated.)
3. Anti-join on the mentor role: `SELECT t.member_no, t.name FROM member t LEFT JOIN member m ON m.mentor_no = t.member_no WHERE m.member_no IS NULL;` → 6 rows: M03, M04, M05, M06, M07, M08. Only M01 and M02 are mentors. A common mistake is `WHERE t.mentor_no IS NULL`, which answers a different question (members **without** a mentor).
4. `SELECT a.name, b.name, substr(a.joining_date, 1, 4) AS year FROM member a JOIN member b ON substr(a.joining_date, 1, 4) = substr(b.joining_date, 1, 4) AND a.member_no < b.member_no;` → 1 row: Ida Yilmaz – Tom Berg, 2027. With `a.member_no <> b.member_no` instead of `<`: 2 rows (the same pair in both orders). Without any extra condition: 10 rows — every member is paired with themselves (8) plus the pair in both orders (2).

Marking: parts 1 and 4 two points each (inner and outer version; query and explanation of the counts), parts 2 and 3 one point each.
:::

## Exam-Style Task: Car-Sharing Bookings

This task is in the style of an exam question. The car-sharing company from worksheet 8 stores its vehicles (table from worksheet 8, task 2: licence_plate, model, station, mileage, fuel, last_service), its customers and their bookings. `booking.customer_no` and `booking.licence_plate` are foreign keys, both NOT NULL; `km` is NULL while a trip has not been billed yet.

::: columns
**customer**

| customer_no | name |
|---|---|
| 1 | Aylin Şahin |
| 2 | Moritz Lang |
| 3 | Greta Huber |
| 4 | David Osei |

**vehicle** (extract)

| licence_plate | model | fuel |
|---|---|---|
| MA-CS 101 | VW ID.3 | electric |
| MA-CS 102 | Opel Corsa | petrol |
| MA-CS 103 | VW ID.3 | electric |
| MA-CS 104 | Fiat 500e | electric |
| MA-CS 105 | Skoda Octavia | diesel |
| MA-CS 106 | Opel Corsa | petrol |
| MA-CS 107 | Renault Zoe | electric |
| MA-CS 108 | Skoda Octavia | diesel |
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

1. Write a query that lists booking number, start date, customer name and vehicle model of all bookings in **February 2027**, in date order. Give the result. (2 points)
2. Write a query that finds the vehicles that have **never been booked**. Give the result. (2 points)
3. The station manager wants **all vehicles, with their bookings from March 2027 if any**, and writes:
   `SELECT v.licence_plate, b.booking_no FROM vehicle v LEFT JOIN booking b ON b.licence_plate = v.licence_plate WHERE b.start_date >= '2027-03-01';`
   How many rows does she get, and why is the result not what she wanted? Correct the query and give the number of rows of the correct result. (2 points)
4. A colleague lists the customers who have booked an **electric** vehicle by joining customer, booking and vehicle with `WHERE v.fuel = 'electric'`. He gets 5 rows for 3 customers. Explain why and correct the query. (2 points)
5. How many rows does `SELECT * FROM customer, booking;` return, and why? Another query, `SELECT c.name FROM customer c LEFT JOIN booking b ON b.customer_no = c.customer_no WHERE b.km IS NULL;`, is meant to find customers without bookings. Give its result and correct it. (2 points)

::: answer lines=24
:::

::: solution
All statements were run in SQLite 3.45.1 on these tables (the full vehicle table from worksheet 8); results as observed.

1. `SELECT b.booking_no, b.start_date, c.name, v.model FROM booking b JOIN customer c ON c.customer_no = b.customer_no JOIN vehicle v ON v.licence_plate = b.licence_plate WHERE b.start_date BETWEEN '2027-02-01' AND '2027-02-28' ORDER BY b.start_date;` → 4 rows: 2 (2027-02-03, Aylin Şahin, VW ID.3), 3 (2027-02-10, Moritz Lang, Fiat 500e), 4 (2027-02-14, Aylin Şahin, Renault Zoe), 5 (2027-02-20, Greta Huber, Opel Corsa). Inner joins are correct: every booking has a customer and a vehicle (NOT NULL foreign keys).
2. `SELECT v.licence_plate, v.model FROM vehicle v LEFT JOIN booking b ON b.licence_plate = v.licence_plate WHERE b.booking_no IS NULL;` → MA-CS 106 (Opel Corsa), MA-CS 108 (Skoda Octavia).
3. She gets **2** rows (MA-CS 101 with booking 6, MA-CS 105 with booking 7). For vehicles without a March booking, the outer join adds a row with `b.start_date` NULL; the WHERE condition is UNKNOWN for it and removes the row again, so the LEFT JOIN behaves like an inner join. Correction: put the condition into ON: `… LEFT JOIN booking b ON b.licence_plate = v.licence_plate AND b.start_date >= '2027-03-01';` → **8** rows, one per vehicle, six of them with booking_no NULL.
4. A join returns one row per matching **booking**: Aylin Şahin has three bookings of electric vehicles (2, 4, 6), Moritz Lang one (3), Greta Huber one (1) → 5 rows. The question asks for customers, so: `SELECT DISTINCT c.name FROM customer c JOIN booking b ON b.customer_no = c.customer_no JOIN vehicle v ON v.licence_plate = b.licence_plate WHERE v.fuel = 'electric';` → Aylin Şahin, Greta Huber, Moritz Lang.
5. **28** rows: without a join condition the result is the Cartesian product, 4 customers × 7 bookings. The second query returns **Aylin Şahin and David Osei**: `b.km IS NULL` is true both for the row added because David has no booking **and** for Aylin's real booking 4, which is not billed yet. Correction: test the partner's primary key, `WHERE b.booking_no IS NULL` → David Osei only.

Marking guide (10 points):

- Part 1: 1 point for both join conditions, 1 point for the date filter, ORDER BY and the correct result. A missing join condition gives 0 for the first point.
- Part 2: 1 point for LEFT JOIN (in the correct direction), 1 point for testing a NOT NULL column of booking and the correct result. `NOT IN` with a subquery is also accepted if correct (session 10).
- Part 3: 1 point for "2 rows" with the explanation (UNKNOWN in WHERE removes the added rows), 1 point for the corrected query with 8 rows.
- Part 4: 1 point for the explanation (one row per booking, 1:N), 1 point for DISTINCT and the result.
- Part 5: 1 point for 28 with "Cartesian product", 1 point for the two names, the reason and the correction.
- Common mistakes: ambiguous `name` or `customer_no` without table prefix (−½ point once); condition on the optional table in WHERE; `= NULL` instead of `IS NULL`; RIGHT JOIN with the tables in the wrong order.
:::

## Optional Challenge: Orphans Without Foreign Keys {.optional}

In session 8 (worksheet 8, task 3b) you saw that `ON DELETE SET NULL` from bike to customer makes "in stock" and "owner deleted" look the same. Now see what happens when foreign keys are **not** enforced — as in many spreadsheets, CSV imports and databases where someone forgot `PRAGMA foreign_keys = ON`.

1. Start from fresh data. Run `con.execute("PRAGMA foreign_keys = OFF")`, then `DELETE FROM customer WHERE customer_no = 108`. What happens to bike SCO640?
2. How many rows does `bike JOIN customer` return now, and which bike is missing compared with before the deletion?
3. Write a query that finds all **orphans**: bikes that refer to a customer who does not exist. Make sure the stock bikes are **not** in the result.
4. Run `PRAGMA foreign_key_check;` and compare its output with your query.
5. Switch foreign keys on again, reload the data and repeat the deletion. What does your orphan query return now? Which of the two situations is better for the business, and what would be better than both?

::: answer lines=12
:::

::: solution
All steps were run in Python sqlite3 and the sqlite3 command-line tool (SQLite 3.45.1); results as observed.

1. The DELETE succeeds (1 row). With foreign keys off, no referential action fires: SCO640 keeps `customer_no = 108`, which now points to no customer — an **orphan** (a violation of referential integrity, session 5).
2. **10** rows instead of 11: SCO640 silently disappears from every inner join with customer, and so does repair job 506 from "jobs with owner" lists. No error, no warning.
3. `SELECT b.frame_no, b.customer_no FROM bike b LEFT JOIN customer c ON c.customer_no = b.customer_no WHERE b.customer_no IS NOT NULL AND c.customer_no IS NULL;` → 1 row: SCO640, 108. Without `b.customer_no IS NOT NULL`, the four stock bikes would be listed too (5 rows), because their customer columns are also NULL after the outer join.
4. `PRAGMA foreign_key_check;` returns one row: table `bike`, rowid 10, parent `customer`, foreign key index 0 — the same bike (SQLite, n.d.-a). The LEFT JOIN query works for any pair of tables, also without declared foreign keys, e.g. after importing CSV files (session 16).
5. With foreign keys on, ON DELETE SET NULL sets SCO640's customer_no to NULL: the orphan query returns **no rows**, and SCO640 is now one of 5 bikes with customer_no NULL (SQLite, n.d.-c). Without foreign keys, the database is inconsistent, but the old customer number is still visible; with SET NULL, it is consistent, but the information "this bike belonged to someone" is lost. Better than both (as in worksheet 8): `ON DELETE RESTRICT` plus anonymising the customer, or a separate status column for bikes ('stock', 'sold', 'external'), so that NULL has only one meaning. Checking for orphans with a LEFT JOIN is a standard data quality test (session 13).
:::

## References {.references}

- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- SQLite. (n.d.-a). *Pragma statements supported by SQLite*. Retrieved October 21, 2026, from https://www.sqlite.org/pragma.html
- SQLite. (n.d.-b). *SELECT*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_select.html
- SQLite. (n.d.-c). *SQLite foreign key support*. Retrieved October 21, 2026, from https://www.sqlite.org/foreignkeys.html
- SQLite. (2022). *SQLite release 3.39.0 on 2022-06-25*. Retrieved October 21, 2026, from https://www.sqlite.org/releaselog/3_39_0.html
