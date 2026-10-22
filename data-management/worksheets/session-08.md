---
course: Data Management
session: 8
title: SQL II: Manipulating and Querying Data
subtitle: Practice tasks on INSERT, UPDATE and DELETE, single-table queries with SELECT, and NULL in WHERE
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 8 on your own or with your project team. Tasks 1, 2 and 6 can be done on paper; for tasks 3, 4, 5 and 7 you need Jupyter with Python's built-in `sqlite3` module. Tasks 3, 4 and 7 use the bike shop database: create it from [bikeshop-schema.sql](data/bikeshop-schema.sql) (session 7) and load the sample data from [bikeshop-data.sql](data/bikeshop-data.sql). All names and addresses in the sample data are fictional. The statements follow the session slides, which are based on Elmasri and Navathe (2016, Chapters 6 and 7) and the SQLite documentation (SQLite, n.d.-a, n.d.-b, n.d.-c). All queries in this worksheet use one table only; combining tables with joins follows in session 9.

```python
import sqlite3

con = sqlite3.connect("bikeshop.db")
con.execute("PRAGMA foreign_keys = ON")
# fresh start: run both scripts again
for script in ["bikeshop-schema.sql", "bikeshop-data.sql"]:
    with open(script, encoding="utf-8") as f:
        con.executescript(f.read())

def run(sql):
    """Run one statement; show the rows, the changed rows or the error."""
    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        print(rows if cur.description else f"{cur.rowcount} row(s) changed")
    except sqlite3.Error as e:
        print(type(e).__name__, "-", e)
```

## TRUE, FALSE or UNKNOWN?

**Part A.** A table `r` has one row with **x = 3**, **y = NULL** and **s = 'Velo'**. Evaluate each condition in SQL's three-valued logic: TRUE, FALSE or UNKNOWN.

| # | Condition | Result |
|---|---|---|
| 1 | `x > 2 AND y > 2` | |
| 2 | `x > 2 OR y > 2` | |
| 3 | `x < 2 AND y > 2` | |
| 4 | `NOT (y = 5)` | |
| 5 | `y IS NULL` | |
| 6 | `y = NULL` | |
| 7 | `x IN (1, 2, NULL)` | |
| 8 | `x NOT IN (1, 2)` | |
| 9 | `x BETWEEN 3 AND 1` | |
| 10 | `s LIKE 'v%'` (in SQLite) | |
| 11 | `s = 'velo'` | |
| 12 | `x <> y OR x = 3` | |

**Part B.** For which of the twelve conditions does `SELECT * FROM r WHERE …` return the row?

**Part C.** A column is declared `y INTEGER CHECK (y > 2)`. Is a row with y = NULL accepted? Compare with your answer to Part B for condition 1 and explain the difference in one sentence.

::: hint
Think of UNKNOWN as "could be true or could be false". If the result of AND or OR is the same in both cases, SQL knows it; otherwise it stays UNKNOWN.
:::

::: answer lines=10
:::

::: solution
Part A (checked in SQLite, which shows TRUE as 1, FALSE as 0 and UNKNOWN as NULL):

1. UNKNOWN (TRUE AND UNKNOWN) · 2. TRUE (TRUE OR UNKNOWN) · 3. FALSE (FALSE AND UNKNOWN) · 4. UNKNOWN (NOT UNKNOWN) · 5. TRUE · 6. UNKNOWN (a comparison with NULL using `=` is never true) · 7. UNKNOWN (3 is not in the list, but the list contains NULL, so SQL cannot rule it out) · 8. TRUE · 9. FALSE (it means x >= 3 AND x <= 1) · 10. TRUE (LIKE ignores case for ASCII letters in SQLite) · 11. FALSE (`=` is case-sensitive) · 12. TRUE (UNKNOWN OR TRUE).

Part B: the row is returned for conditions **2, 5, 8, 10 and 12** — WHERE keeps a row only when the condition is TRUE; FALSE and UNKNOWN rows are dropped (Elmasri & Navathe, 2016, Chapter 7; SQLite, n.d.-c).

Part C: yes, the row is accepted (tested). A CHECK constraint is violated only when its condition is **FALSE**, so UNKNOWN passes; WHERE is the opposite and keeps only TRUE rows. To forbid NULL, add NOT NULL. One point per correct line in Part A is a reasonable marking scale; Part C must name the difference FALSE vs. TRUE.
:::

## Predict the Result: Car-Sharing Vehicles

The car-sharing company from earlier worksheets stores its vehicles in this table (NULL means unknown):

| licence_plate | model | station | mileage | fuel | last_service |
|---|---|---|---|---|---|
| MA-CS 101 | VW ID.3 | Mannheim Hbf | 18250 | electric | 2027-01-15 |
| MA-CS 102 | Opel Corsa | Quadrate | 40310 | petrol | 2026-11-02 |
| MA-CS 103 | VW ID.3 | Neckarstadt | NULL | electric | NULL |
| MA-CS 104 | Fiat 500e | Mannheim Hbf | 9120 | electric | 2027-02-20 |
| MA-CS 105 | Skoda Octavia | Lindenhof | 65400 | diesel | 2026-09-30 |
| MA-CS 106 | Opel Corsa | NULL | 52000 | petrol | 2027-02-01 |
| MA-CS 107 | Renault Zoe | Neckarstadt | 31800 | electric | NULL |
| MA-CS 108 | Skoda Octavia | Mannheim Hbf | NULL | diesel | 2026-12-12 |

Without running them, write down the result of each query (rows, or the number for `count(*)`).

```sql
-- a
SELECT licence_plate FROM vehicle
WHERE station = 'Mannheim Hbf' AND mileage < 20000;
-- b
SELECT DISTINCT model FROM vehicle WHERE fuel <> 'electric';
-- c
SELECT licence_plate FROM vehicle WHERE mileage > 30000 OR fuel = 'electric';
-- d
SELECT licence_plate, mileage FROM vehicle ORDER BY mileage DESC LIMIT 3;
-- e
SELECT count(*) FROM vehicle WHERE station NOT IN ('Quadrate', 'Lindenhof');
-- f
SELECT licence_plate FROM vehicle
WHERE last_service < '2027-01-01' OR last_service IS NULL;
-- g
SELECT licence_plate, mileage FROM vehicle ORDER BY mileage LIMIT 2;
```

::: answer lines=12
:::

::: solution
All results were checked by running the queries in SQLite on exactly this table.

- a: MA-CS 101, MA-CS 104. MA-CS 108 is at Mannheim Hbf, but its mileage is unknown, so `mileage < 20000` is UNKNOWN.
- b: Opel Corsa, Skoda Octavia — two rows: DISTINCT removes the duplicate models.
- c: seven rows, MA-CS 101 to MA-CS 107. MA-CS 103 qualifies because it is electric (UNKNOWN OR TRUE = TRUE); MA-CS 108 is missing (UNKNOWN OR FALSE = UNKNOWN).
- d: MA-CS 105 (65400), MA-CS 106 (52000), MA-CS 102 (40310). In descending order, SQLite puts NULL last.
- e: 5. The three vehicles at Mannheim Hbf and the two at Neckarstadt; MA-CS 106 (station NULL) is not counted.
- f: MA-CS 102, 103, 105, 107, 108 — five rows. ISO dates compare correctly as text.
- g: MA-CS 103 and MA-CS 108, both with mileage NULL: in ascending order, SQLite sorts NULL **first** (SQLite, n.d.-b). Students who answered MA-CS 104 and MA-CS 101 forgot the NULLs; to get them, add `WHERE mileage IS NOT NULL` or `ORDER BY mileage NULLS LAST`.

Marking: one point per query; for c, e and g the point requires the correct treatment of NULL.
:::

## Business Events in the Bike Shop

Start from the fresh sample data. Write **one SQL statement** for each business event, run them in this order, and note what SQLite reports (number of changed rows, or the error).

1. A new customer, Jana Wolf (jana.wolf@example.com, Friedrichsring 4, 68161 Mannheim), registers. The database assigns her number.
2. She buys the stock bike TRK311 at a special price of 999 €.
3. The list price of brake pads (P-103) rises by 1.00 €.
4. Repair job 512 gets the description "Rear brake rubs".
5. Customer 106 asks for his data to be deleted.
6. Customer 108 asks for his data to be deleted.
7. The e-bike battery P-109 is no longer sold and should be removed from the parts list.

Then answer:

- **a)** Do the repair lines that contain P-103 change in step 3? Why is that intended?
- **b)** Which bikes are "in stock" (customer_no NULL) after step 7? What is wrong with this result, and what does it say about the `ON DELETE SET NULL` decision in the schema?

::: hint
Use a column list in the INSERT and leave out customer_no. Before each UPDATE and DELETE, run the same WHERE clause as a SELECT.
:::

::: answer lines=14
:::

::: solution
Statements and observed results (Python sqlite3 and the sqlite3 command-line tool):

```sql
-- 1: 1 row, customer_no 113
INSERT INTO customer (name, e_mail, street, postcode, city)
VALUES ('Jana Wolf', 'jana.wolf@example.com', 'Friedrichsring 4',
        '68161', 'Mannheim');
-- 2: 1 row
UPDATE bike SET customer_no = 113, price = 999 WHERE frame_no = 'TRK311';
-- 3: 1 row, new list price 13.5
UPDATE spare_part SET list_price = list_price + 1 WHERE part_no = 'P-103';
-- 4: 1 row
UPDATE repair_job SET description = 'Rear brake rubs' WHERE job_no = 512;
-- 5 and 6: 1 row each
DELETE FROM customer WHERE customer_no = 106;
DELETE FROM customer WHERE customer_no = 108;
-- 7: FOREIGN KEY constraint failed (repair line 507 uses P-109)
DELETE FROM spare_part WHERE part_no = 'P-109';
```

- Step 2 uses the number from step 1 (113); looking it up with `SELECT customer_no FROM customer WHERE name = 'Jana Wolf'` is better than guessing. Using the name instead of the number in the bike table is wrong: the foreign key is customer_no.
- Step 6 succeeds: bike SCO640 gets customer_no NULL (ON DELETE SET NULL), and repair job 506 for that bike stays.
- Step 7 fails because repair_line refers to spare_part without an action clause. Options: keep the part and mark it as discontinued (e.g. a new column `active`), or accept that history prevents deletion.

a) No: the repair lines keep 12.50 and 11.00 (observed). price_charged stores the price **at the time of the repair** (pitfall "missing history", session 4); changing the list price must not change past invoices.

b) GZT884, KTM530, SCO640 and GZT886 (observed). SCO640 is **not** in stock — it was bought elsewhere and belongs to the deleted customer. ON DELETE SET NULL mixes two meanings of NULL: "not sold yet" and "owner deleted". Better options: ON DELETE RESTRICT for customers with bikes, a separate status column for bikes (e.g. 'stock', 'sold', 'external'), or anonymising the customer (overwrite name and contact data with an UPDATE) instead of deleting the row — which also keeps the repair history. Session 19 returns to deletion requests under the GDPR.

Marking: one point per correct statement (7), one point each for a) and b).
:::

## Lab: Business Questions on the Bike Shop

Answer each question with **one** `SELECT` on **one** table of the bike shop database (fresh sample data). Before running a query, predict the number of rows.

1. Number and name of all customers from Mannheim, sorted by name.
2. Spare parts whose name contains "chain" or "cassette".
3. Repair lines in which more than one unit of a part was used.
4. For repair job 502: part number, quantity, unit price and the **line total** (quantity × unit price) as a column named `line_total`, largest total first.
5. Mechanics who have no supervisor.
6. All days on which at least one repair job was started — each day once, latest first.
7. Bikes whose frame number is TRK31 followed by exactly one more character.
8. Name and postcode of customers in the 69… postcode area who have no e-mail address.
9. Repair jobs that are annual services **or** have no description yet, latest first.

::: answer lines=14
:::

::: solution
All queries were run on a fresh database built from the two course scripts; results as observed.

1. `SELECT customer_no, name FROM customer WHERE city = 'Mannheim' ORDER BY name;` → 3 rows: 101 Anna Berger, 107 Hannah Schulz, 110 Tobias Krämer. Note that the name column holds first and last name together, so the list is sorted by **first** name; sorting by surname would need a separate column (atomic attributes, session 6).
2. `SELECT part_no, name, list_price FROM spare_part WHERE name LIKE '%chain%' OR name LIKE '%cassette%';` → 3: P-104, P-105, P-108. LIKE ignores case, so "Chain" is found.
3. `SELECT job_no, part_no, quantity, price_charged FROM repair_line WHERE quantity > 1;` → 3: (502, P-106, 2), (503, P-103, 2), (504, P-103, 2).
4. `SELECT part_no, quantity, price_charged, quantity * price_charged AS line_total FROM repair_line WHERE job_no = 502 ORDER BY line_total DESC;` → P-103 (1 × 12.5 = 12.5), P-106 (2 × 4.5 = 9.0). Adding up the lines of a job needs aggregation (session 10).
5. `SELECT employee_no, qualification FROM mechanic WHERE supervisor_no IS NULL;` → 1 row: employee 1, master. `= NULL` gives no row. The mechanic's name is in the employee table — combining both needs a join (session 9).
6. `SELECT DISTINCT job_date FROM repair_job ORDER BY job_date DESC;` → 11 days from 2027-04-07 to 2027-01-12 (12 jobs, two on 2027-02-02).
7. `SELECT frame_no, brand, model FROM bike WHERE frame_no LIKE 'TRK31_';` → 3: TRK310, TRK311, TRK312.
8. `SELECT name, postcode FROM customer WHERE postcode LIKE '69%' AND e_mail IS NULL;` → 1: Mira Okonkwo, 69115. Postcodes are TEXT, so LIKE works and leading zeros would be kept.
9. `SELECT job_no, frame_no, job_date FROM repair_job WHERE description = 'Annual service' OR description IS NULL ORDER BY job_date DESC;` → 5: 512, 508, 506, 504, 502.
:::

## Find the Mistakes: Food Co-op Queries

The food co-op from earlier worksheets keeps its products in one table. Create it in a new notebook (or `:memory:` database) with this script:

```sql
CREATE TABLE product (
    product_no  INTEGER PRIMARY KEY,
    name        TEXT    NOT NULL,
    category    TEXT,
    price       NUMERIC CHECK (price >= 0),
    farm_id     INTEGER,
    organic     INTEGER CHECK (organic IN (0, 1))       -- NULL: not known yet
);
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

A volunteer wrote one statement for each request. Every statement runs without an error message, but none does what was asked. Explain each mistake, write a corrected statement and give the correct result.

| # | Request | Statement |
|---|---|---|
| a | Products that are not organic, or whose status is not known yet | `SELECT product_no FROM product WHERE organic = 0 OR organic = NULL;` |
| b | Organic vegetables and organic fruit | `SELECT product_no FROM product WHERE category = 'vegetables' OR category = 'fruit' AND organic = 1;` |
| c | Products that cost from 2 to 3 € | `SELECT name, price FROM product WHERE price BETWEEN 3 AND 2;` |
| d | The two cheapest products | `SELECT name, price FROM product LIMIT 2;` |
| e | A list of all categories | `SELECT DISTINCT category, name FROM product;` |
| f | Products that do not come from farm 1 or 2, including those with an unknown farm | `SELECT product_no FROM product WHERE farm_id NOT IN (1, 2);` |
| g | Raise the price of all dairy products by 10 % | `UPDATE product SET price = price * 1.1;` |

::: hint
For d, there are two mistakes: think about the order **and** about the product without a price.
:::

::: answer lines=16
:::

::: solution
All wrong and corrected statements were run in SQLite on this table; results as observed.

- a) `organic = NULL` is never TRUE, so the unknown products are missing (wrong result: 3, 6, 11). Fix: `WHERE organic = 0 OR organic IS NULL` → 3, 4, 6, 10, 11.
- b) AND binds more strongly than OR: the statement means "all vegetables, or organic fruit" and includes the non-organic onions (wrong: 1, 2, 8, 9, 11). Fix: `WHERE (category = 'vegetables' OR category = 'fruit') AND organic = 1`, or `WHERE category IN ('vegetables', 'fruit') AND organic = 1` → 1, 2, 8, 9.
- c) BETWEEN needs the smaller bound first; `BETWEEN 3 AND 2` means price >= 3 AND price <= 2 and returns no row. Fix: `BETWEEN 2 AND 3` → Potatoes 2.8, Apples 2.4, Pears 2.9.
- d) Without ORDER BY, "the first two" are undefined (here: Potatoes and Carrots). Adding only `ORDER BY price` returns Pumpkin (NULL) first, because SQLite sorts NULL first. Fix: `SELECT name, price FROM product WHERE price IS NOT NULL ORDER BY price LIMIT 2;` → Yoghurt 1.1, Milk 1.3. (Ties at the second place would need a tie-breaker; there are none here.)
- e) DISTINCT applies to the whole row: every (category, name) pair is different, so all 11 rows are returned. Fix: `SELECT DISTINCT category FROM product WHERE category IS NOT NULL ORDER BY category;` → dairy, drinks, fruit, vegetables. Without the WHERE, a fifth row NULL (Honey) appears; accept either if explained.
- f) `NULL NOT IN (1, 2)` is UNKNOWN, so Honey (farm unknown) is missing (wrong: 5, 6, 10, 11). Fix: `WHERE farm_id NOT IN (1, 2) OR farm_id IS NULL` → 5, 6, 7, 10, 11.
- g) Without WHERE, every product gets 10 % more. Fix: `UPDATE product SET price = round(price * 1.1, 2) WHERE category = 'dairy';` → 3 rows: Goat cheese 7.59, Milk 1.43, Yoghurt 1.21. Check first with `SELECT … WHERE category = 'dairy'`; in Python, `con.rollback()` undoes the wrong UPDATE if it has not been committed yet.

Marking: one point per item for explanation and correction together.
:::

## Exam-Style Task: The Sports Club Members

This task is in the style of an exam question. The sports club from worksheet 7 stores its members in this table (schema as in worksheet 7, with `mentor_no REFERENCES member (member_no) ON DELETE SET NULL` and `joining_date … DEFAULT CURRENT_DATE`):

| member_no | name | date_of_birth | joining_date | member_type | mentor_no |
|---|---|---|---|---|---|
| M01 | Sabine Keller | 1975-04-12 | 2010-03-01 | adult | NULL |
| M02 | Omar Haddad | 1988-09-30 | 2015-06-15 | adult | M01 |
| M03 | Lea Hofmann | 2011-02-14 | 2026-09-01 | youth | M02 |
| M04 | Finn Schäfer | 2012-07-08 | 2025-01-10 | youth | NULL |
| M05 | Sven Maier | 2008-11-23 | 2020-05-01 | youth | M01 |
| M06 | Ida Yilmaz | 1995-01-05 | 2027-01-15 | adult | NULL |
| M07 | Tom Berg | 2013-03-19 | 2027-02-01 | youth | M02 |
| M08 | Nina Graf | 1969-12-02 | 2018-10-01 | adult | NULL |

1. Write a query that lists number, name and joining date of all **youth members who joined in 2026 or later**, sorted by name. Give the result. (2 points)
2. Write a query that lists the **three members without a mentor who joined most recently**. Give the result. (2 points)
3. A colleague wants to know how many members are **not** mentored by M01 and writes `SELECT count(*) FROM member WHERE mentor_no <> 'M01';`. What result does she get, what result did she expect, and why do they differ? Correct the query. (2 points)
4. Write the statements for two changes: M05 turns 18 and becomes an **adult** member; a new youth member **M09**, Jana Brück, born 2014-05-30, joins on 2027-03-01 with mentor M06. (2 points)
5. M02 leaves the club. Write the statement, describe its effect on other rows of the table, and give the result of your query from part 2 afterwards (after the changes from part 4). (2 points)

::: answer lines=24
:::

::: solution
All statements were run in SQLite on this table, in the order of the parts; results as observed.

1. `SELECT member_no, name, joining_date FROM member WHERE member_type = 'youth' AND joining_date >= '2026-01-01' ORDER BY name;` → M03 Lea Hofmann (2026-09-01), M07 Tom Berg (2027-02-01). Also accept `joining_date BETWEEN '2026-01-01' AND '2099-12-31'` or `(joining_date LIKE '2026%' OR joining_date LIKE '2027%')` with the parentheses.
2. `SELECT member_no, name, joining_date FROM member WHERE mentor_no IS NULL ORDER BY joining_date DESC LIMIT 3;` → M06 (2027-01-15), M04 (2025-01-10), M08 (2018-10-01).
3. She gets **2** (M03 and M07, mentored by M02). She expected **6** (all members except M02 and M05). For the four members without a mentor, `NULL <> 'M01'` is UNKNOWN, and WHERE drops these rows. Correction: `WHERE mentor_no <> 'M01' OR mentor_no IS NULL` → 6. (`WHERE mentor_no IS NOT 'M01'` also gives 6 in SQLite; accept it.)
4. `UPDATE member SET member_type = 'adult' WHERE member_no = 'M05';` (1 row) and
   `INSERT INTO member (member_no, name, date_of_birth, joining_date, member_type, mentor_no) VALUES ('M09', 'Jana Brück', '2014-05-30', '2027-03-01', 'youth', 'M06');`
   In the full schema of worksheet 7, M05's row in youth_member would also have to be deleted, and M09 needs a youth_member row with a parent phone number; mention earns no extra point but is a good sign.
5. `DELETE FROM member WHERE member_no = 'M02';` (1 row). Because of `ON DELETE SET NULL`, M03 and M07 lose their mentor (mentor_no becomes NULL); they stay members. The query from part 2 now returns M07 (2027-02-01), M06 (2027-01-15), M03 (2026-09-01) — M09 has mentor M06 and does not appear.

Marking guide (10 points):

- Parts 1 and 2: 1 point for a correct WHERE (including `IS NULL` in part 2), 1 point for ORDER BY / LIMIT and the correct result. A missing ORDER BY in part 2 costs the second point; `= NULL` costs the first.
- Part 3: 1 point for the two numbers and the explanation with UNKNOWN; 1 point for the corrected query.
- Part 4: 1 point per statement. An INSERT without a column list is accepted if the values are in the correct column order; WHERE missing in the UPDATE gives 0 for that statement.
- Part 5: 1 point for the DELETE and the SET NULL effect; 1 point for the new result.
- Common mistakes: `mentor_no = NULL`; LIMIT without ORDER BY; dates compared in German format ('01.01.2026'); text values in double quotes.
:::

## Optional Challenge: Paging Through the Bike List {.optional}

The bike shop's web shop shows the bikes **five per page**, cheapest first, bikes with unknown price at the end.

1. Write the query for **page 2** and give its result.
2. A first version used `ORDER BY price LIMIT 5 OFFSET 5`. Which two problems does it have? Think about NULL and about bikes with the same price.
3. Write a Python function `bike_page(page, size=5)` that returns the rows of a page. Pass the numbers with `?` placeholders instead of building the SQL string yourself.

::: answer lines=12
:::

::: solution
1. `SELECT frame_no, brand, price FROM bike ORDER BY price NULLS LAST, frame_no LIMIT 5 OFFSET 5;` → BRO860 (1749), WAX123 (1899), GZT884 (2499), GZT886 (2499), GZT885 (2799) (observed). Page 3 then ends with CAN750 and SCO640 (price NULL).
2. (a) SQLite sorts NULL **first** in ascending order, so the two bikes without a price fill the start of page 1 (observed: page 2 of the first version starts with TRK312 instead of BRO860). (b) Without a tie-breaker, the order of GZT884 and GZT886 (both 2499) is undefined; if it changes between two page requests, a bike can appear twice or not at all. A unique last sort column (the primary key frame_no) makes the order deterministic (SQLite, n.d.-b).
3. Tested version:

```python
def bike_page(page, size=5):
    sql = """SELECT frame_no, brand, model, price FROM bike
             ORDER BY price NULLS LAST, frame_no
             LIMIT ? OFFSET ?"""
    return con.execute(sql, (size, (page - 1) * size)).fetchall()

bike_page(2)   # same five rows as in part 1
```

Placeholders work for values such as LIMIT and OFFSET, but not for table or column names. Building the string with f-strings from user input allows SQL injection.
:::

## References {.references}

- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- SQLite. (n.d.-a). *INSERT*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_insert.html
- SQLite. (n.d.-b). *SELECT*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_select.html
- SQLite. (n.d.-c). *SQL language expressions*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_expr.html
