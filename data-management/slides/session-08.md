---
course: Data Management
session: 8
title: SQL II: Manipulating and Querying Data
subtitle: INSERT, UPDATE, DELETE · SELECT, WHERE, ORDER BY, DISTINCT, LIMIT · NULL and three-valued logic
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# SQL II: Manipulating and Querying Data {.title}

::: notes
Time plan for today (3 h): recap and loading the sample data 10 min · INSERT 10 min · UPDATE and DELETE 15 min · working safely in Python 5 min · mini exercise DML 10 min · break 10 min · SELECT and WHERE 15 min · IN, BETWEEN, LIKE 10 min · NULL and three-valued logic 15 min · ORDER BY, DISTINCT, LIMIT 10 min · hands-on: query the bike shop 40 min · team work: test data and first queries 25 min · wrap-up 5 min · ~5–10 min buffer.
Input is about 70 minutes in total, hands-on about 75 minutes. As in session 7, live coding in a notebook works better than reading code from the slides. If the input runs long, set the optional slides (query parameters, text comparisons) as self-study and shorten the hands-on to questions 1–6, but keep at least 20 minutes for the teams.
Every statement on these slides was run with Python's sqlite3 module (Python 3.13) and the sqlite3 command-line tool (SQLite 3.45.1) on a fresh database built from bikeshop-schema.sql and bikeshop-data.sql; all row counts and error messages are the ones SQLite returned.
:::

---

# Today's Agenda

1. Recap: an empty database
2. Changing data: `INSERT`, `UPDATE`, `DELETE`
3. Querying one table: `SELECT … FROM … WHERE`
4. NULL and three-valued logic
5. Sorting and trimming results: `ORDER BY`, `DISTINCT`, `LIMIT`
6. Hands-on: query the bike shop in Jupyter
7. Team work: test data and first queries for your project

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary, check that bikeshop.db exists; load the sample data together) · 0:10 INSERT (input, live coding) · 0:20 UPDATE and DELETE (input, live coding) · 0:35 Working safely in Python (input) · 0:40 Mini exercise DML (pairs, predict first) · 0:50 Break · 1:00 SELECT and WHERE (input, live coding) · 1:15 IN, BETWEEN, LIKE · 1:25 NULL and three-valued logic (input and short discussion) · 1:40 ORDER BY, DISTINCT, LIMIT · 1:50 Hands-on (groups of 3, same groups as sessions 3–7, each student on their own laptop) · 2:30 Team work on project data · 2:55 Wrap-up.
:::

---

# Recap: An Empty Database

- Last session you created **bikeshop.db** from the course script: nine tables, all constraints, but **no rows**
- Your team's SQL script should run without errors (preparation task)
- Which constraints will reject a row? Which **referential actions** fire when a row is deleted?

::: callout
Today the tables get data: we **insert, change and delete rows** — and then ask questions with `SELECT`.
:::

::: notes
Preparation from session 7: bikeshop.db created from the course script, and the team script running. Quick check by show of hands; students without a working database run the schema script now (it is linked from worksheets 7 and 8). Ask for the three referential actions in the course script (bike → customer SET NULL, repair_job → bike RESTRICT, repair_line and job_mechanic → repair_job CASCADE): today they fire for real. Reminder: milestone 2 was due after session 7; milestone 3 (database and queries) is due after session 12.
:::

---

# Changing Data: INSERT, UPDATE, DELETE {.section}

The data manipulation language (DML)

---

# INSERT: Adding Rows

```sql
INSERT INTO customer (customer_no, name, e_mail, street, postcode, city)
VALUES (101, 'Anna Berger', 'anna.berger@example.org',
        'Lange Rötterstraße 12', '68167', 'Mannheim');

INSERT INTO customer (name, city) VALUES ('Lena Hartmann', 'Mannheim');

INSERT INTO spare_part (part_no, name, list_price) VALUES
    ('P-101', 'Inner tube 28 inch', 6.90),
    ('P-102', 'Tyre 28 x 1.5',     34.90);
```

- Always give the **column list**: the statement then still works if columns are added
- Omitted columns get their **DEFAULT**, otherwise **NULL**; `INTEGER PRIMARY KEY` gets the next number
- One statement can insert **several rows**; `INSERT INTO … SELECT …` copies rows from a query

::: source
Based on SQLite (n.d.-b) and Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
Observed: the second statement gives Lena Hartmann customer_no 113 (the largest number was 112), e_mail, street and postcode NULL. Without a column list, the values must match all columns in table order: `INSERT INTO customer VALUES (114, 'Max Roth')` fails with "table customer has 6 columns but 2 values were supplied". `INSERT INTO repair_job (frame_no) VALUES ('GZT884')` gives job 513 with today's date (DEFAULT CURRENT_DATE, UTC). Text values in single quotes; double quotes are for identifiers in standard SQL. INSERT … SELECT appeared in session 7's table rebuild.
:::

---

# Loading the Sample Data

```python
import sqlite3

con = sqlite3.connect("bikeshop.db")
con.execute("PRAGMA foreign_keys = ON")
for script in ["bikeshop-schema.sql", "bikeshop-data.sql"]:
    with open(script, encoding="utf-8") as f:
        con.executescript(f.read())
```

| Table | Rows | Table | Rows | Table | Rows |
|---|---|---|---|---|---|
| customer | 12 | spare_part | 11 | employee | 7 |
| bike | 15 | repair_job | 12 | mechanic | 4 |
| job_mechanic | 14 | repair_line | 16 | salesperson | 2 |

- **bikeshop-data.sql** (linked from worksheet 8) inserts fictional data in an order that respects the foreign keys
- Running the schema script first gives a clean start: it drops and recreates all tables

::: source
Own example based on the bike shop case from sessions 3–7.
:::

::: notes
Everyone runs this cell now. Running only the data script a second time fails with "UNIQUE constraint failed" at the first duplicate key, because the rows already exist — run both scripts again. The data has deliberate gaps for today's NULL slides: 3 customers without e-mail, 1 customer with only a name, 4 bikes in stock (customer_no NULL), 2 bikes with unknown price, 2 repair jobs without description. Command-line alternative: `sqlite3 bikeshop.db < bikeshop-data.sql` (tested).
:::

---

# INSERT and Constraints

```sql
INSERT INTO customer (customer_no, name) VALUES (101, 'Max Roth');
-- UNIQUE constraint failed: customer.customer_no

INSERT INTO spare_part (part_no, name, list_price) VALUES
    ('P-112', 'Saddle', 49.90),
    ('P-113', 'Pedals', -5);
-- CHECK constraint failed: list_price >= 0
```

- Every constraint from session 7 is checked **for every new row**
- A statement is **atomic**: if one row fails, **no row** of the statement is stored — the saddle is not inserted either
- Order matters: insert **referenced** rows first (customer before bike, bike before repair job)

::: source
Based on SQLite (n.d.-b).
:::

::: notes
Observed: after the failed two-row insert, spare_part still has 11 rows. The error message names the constraint, which helps when loading data from files (session 16). INSERT OR IGNORE / INSERT OR REPLACE and the upsert clause (ON CONFLICT … DO UPDATE) exist in SQLite but are not part of this session; REPLACE deletes the old row first, which can fire ON DELETE actions. Mention only if asked.
:::

---

# UPDATE: Changing Rows

```sql
UPDATE bike
SET    customer_no = 106, price = 2399
WHERE  frame_no = 'GZT884';                 -- 1 row: a stock bike is sold

UPDATE spare_part
SET    list_price = round(list_price * 1.05, 2)
WHERE  list_price < 10;                     -- 4 rows: +5 % on small parts
```

- `SET` names the columns and their new values; expressions may use the **old values** of the row
- `WHERE` decides **which rows** change — **no WHERE means every row**
- Constraints are checked again: `SET customer_no = 999` fails with "FOREIGN KEY constraint failed"

::: source
Based on SQLite (n.d.-f) and Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
Observed: the second statement changes P-101, P-106, P-107 and P-110 to 7.25, 4.73, 4.73 and 9.35. Without round(), 6.90 × 1.05 gives 7.245000000000001 — binary floating point again (session 7). All expressions in SET are evaluated before any assignment: `SET a = b, b = a` swaps two values. A WHERE that matches no row is not an error: "0 rows changed". `UPDATE bike SET price = 0.9 * price` (no WHERE) changed all 15 bikes — the typical accident. A WHERE on the primary key changes at most one row.
:::

---

# DELETE: Removing Rows

```sql
DELETE FROM repair_job WHERE job_no = 511;
-- 1 row; its 3 repair lines and 2 mechanic assignments go too (CASCADE)

DELETE FROM customer WHERE customer_no = 101;
-- 1 row; bike WAX123 stays, customer_no becomes NULL (SET NULL)

DELETE FROM bike WHERE frame_no = 'WAX123';
-- FOREIGN KEY constraint failed: repair jobs refer to it (RESTRICT)
```

- `DELETE` removes **whole rows**; to empty one value, use `UPDATE … SET column = NULL`
- **No WHERE deletes every row** of the table; the table itself stays (unlike `DROP TABLE`)
- With foreign keys on, the **referential actions** from session 7 fire

::: source
Based on SQLite (n.d.-a, n.d.-e).
:::

::: notes
Observed counts after deleting job 511: repair_line 16 → 13, job_mechanic 14 → 12. A surprising case for discussion: `DELETE FROM employee WHERE employee_no = 3` fails, although mechanic → employee is ON DELETE CASCADE: the cascade would delete mechanic 3, but job_mechanic still refers to mechanic 3 without an action clause, so the whole statement is rejected. Employee 7 (no subclass, no jobs) can be deleted. Rows for which the WHERE condition is false **or NULL** are kept (SQLite, n.d.-a) — the next section explains why that matters.
:::

---

# Working Safely: SELECT First, Then Change

```python
con.execute("SELECT * FROM bike WHERE customer_no IS NULL").fetchall()  # 4 rows
cur = con.execute("UPDATE bike SET price = price - 100 WHERE customer_no IS NULL")
print(cur.rowcount)        # 4 – as expected?
con.commit()               # make it permanent ...
# con.rollback()           # ... or undo everything since the last commit
```

- Run the **same WHERE** as a `SELECT` before every `UPDATE` or `DELETE`
- Python's sqlite3 opens a **transaction** before a change: nothing is saved until `con.commit()`
- `cur.rowcount` tells how many rows a change affected

::: source
Own example; transactions follow in session 10.
:::

::: notes
Observed: rowcount 4; a second connection saw the old data until commit (in our test, a DELETE in one connection was not visible to another before commit). rollback() undid a DELETE completely. Forgetting commit is the most common reason for "my changes are gone" after restarting the kernel; executescript() commits pending changes before it runs. In the sqlite3 command-line tool and in DB Browser the behaviour differs: the CLI saves each statement immediately unless you type BEGIN. ACID and transactions in detail: session 10.
:::

---

# Mini Exercise: Predict the Changes {.exercise}

Start from the fresh sample data. Run the statements **one after the other**. Which succeed, how many rows change, and what happens in other tables?

```sql
INSERT INTO spare_part (part_no, name) VALUES ('P-112', 'Saddle');
UPDATE spare_part SET list_price = 4.90 WHERE name LIKE '%cable';
DELETE FROM spare_part WHERE part_no = 'P-107';
DELETE FROM repair_job WHERE job_no = 504;
DELETE FROM spare_part WHERE part_no = 'P-107';
UPDATE mechanic SET supervisor_no = 3 WHERE employee_no = 3;
```

::: notes
About 10 min in pairs: predict on paper first, then run. LIKE is introduced properly after the break — here '%cable' means "ends with cable". Expected answers (all observed):
1 Fails: "NOT NULL constraint failed: spare_part.list_price" (no default).
2 Succeeds, 2 rows (P-106 Brake cable, P-107 Gear cable), both 4.9.
3 Fails: "FOREIGN KEY constraint failed" — repair line (504, P-107) refers to it.
4 Succeeds, 1 row; CASCADE removes its 2 repair lines (16 → 14) and 2 mechanic assignments (14 → 12).
5 Succeeds now: no repair line refers to P-107 any more.
6 Fails: "CHECK constraint failed: supervisor_no <> employee_no".
Point out that statement 3 and 5 are identical but give different results: the outcome of DML depends on the current data.
:::

---

# Querying One Table {.section}

SELECT, FROM, WHERE

---

# SELECT: Anatomy of a Query

```sql
SELECT   part_no, name, round(list_price * 1.19, 2) AS gross_price
FROM     spare_part
WHERE    list_price < 10
ORDER BY gross_price DESC;
```

| part_no | name | gross_price |
|---|---|---|
| P-110 | Bell | 10.59 |
| P-101 | Inner tube 28 inch | 8.21 |
| P-106 | Brake cable | 5.35 |
| P-107 | Gear cable | 5.35 |

- **Written** order: SELECT – FROM – WHERE – ORDER BY – LIMIT
- **Logical** order: FROM (which table) → WHERE (which rows) → SELECT (which columns) → ORDER BY → LIMIT
- `SELECT *` returns all columns; `AS` gives a result column a name

::: source
Based on Elmasri and Navathe (2016, Chapter 6) and SQLite (n.d.-c).
:::

::: notes
In relational algebra terms: WHERE is a selection (rows), the SELECT list a projection (columns) — Codd's operations from session 5. The result of a query is again a table (without a name), which is why queries can be nested later (session 10). The logical order explains why the alias gross_price works in ORDER BY but should not be used in WHERE (not standard SQL; SQLite happens to accept it). `SELECT *` is fine for exploring, but in programs list the columns. 19 % is the standard German VAT rate.
:::

---

# WHERE: Comparisons and Logical Operators

```sql
SELECT frame_no, brand, model, price
FROM   bike
WHERE  price >= 2000 AND customer_no IS NULL;    -- 3 rows: expensive bikes in stock
```

| Operators | Meaning |
|---|---|
| `=`, `<>` (or `!=`), `<`, `<=`, `>`, `>=` | comparison |
| `AND`, `OR`, `NOT` | combine conditions |

- `AND` binds **more strongly** than `OR` — use **parentheses**:
  - `brand = 'Cube' OR brand = 'Trek' AND price < 1000` → 6 rows (all Cubes)
  - `(brand = 'Cube' OR brand = 'Trek') AND price < 1000` → 4 rows
- Text in single quotes, compared **case-sensitively** with `=`: `'Cube' = 'cube'` is false

::: source
Based on Elmasri and Navathe (2016, Chapter 6) and SQLite (n.d.-d).
:::

::: notes
Observed: the 3 rows are GZT884 and GZT886 (Gazelle Ultimate, 2499) and KTM530 (3599). Without parentheses SQLite reads `brand = 'Cube' OR (brand = 'Trek' AND price < 1000)`: all four Cubes including the 3299 Stereo Hybrid, plus TRK310 and TRK312. Ask students to say the business question in words before writing the condition. Dates stored as ISO text compare correctly with <, >: `job_date >= '2027-03-01'` gives the 7 jobs from March on (session 7: ISO dates sort as text).
:::

---

# IN, BETWEEN and LIKE

| Condition | Short for | Bike shop result |
|---|---|---|
| `brand IN ('Gazelle', 'KTM')` | `brand = 'Gazelle' OR brand = 'KTM'` | 4 bikes |
| `price BETWEEN 1000 AND 2500` | `price >= 1000 AND price <= 2500` | 5 bikes |
| `e_mail LIKE '%@example.org'` | pattern: ends with "@example.org" | 4 customers |
| `description LIKE '%puncture%'` | pattern: contains "puncture" | jobs 501, 510 |

- `BETWEEN` **includes** both bounds; the smaller bound comes first
- In `LIKE`, `%` stands for **any number** of characters, `_` for **exactly one**
- `NOT IN`, `NOT BETWEEN`, `NOT LIKE` negate the condition

::: source
Based on SQLite (n.d.-d) and Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
Observed: BETWEEN 1000 AND 2500 includes the two Gazelle Ultimate at 2499 and excludes nothing at the bound; `BETWEEN 2500 AND 1000` returns 0 rows (it means price >= 2500 AND price <= 1000). The LIKE on description finds "Puncture, rear wheel" although the pattern is lower case: in SQLite, LIKE ignores case for ASCII letters (optional slide on text comparisons). LIKE '_a%' means "second letter is a". For a literal % or _, SQLite offers ESCAPE: `LIKE '50!%' ESCAPE '!'`. Date ranges: `job_date BETWEEN '2027-03-01' AND '2027-03-31'` works for ISO dates without time.
:::

---

# Text Comparisons in SQLite {.optional}

| Expression | Result | Why |
|---|---|---|
| `'Cube' = 'cube'` | false (0) | `=` is case-sensitive |
| `'a' LIKE 'A'` | true (1) | `LIKE` ignores case — for ASCII letters only |
| `'ü' LIKE 'Ü'` | false (0) | umlauts are not ASCII |
| `brand LIKE 'riese%'` | 1 bike | finds "Riese & Müller" |
| `brand LIKE '%MÜLLER'` | 0 bikes | "ü" ≠ "Ü" for LIKE |

- Other DBMS differ: in PostgreSQL, `LIKE` is case-sensitive and `ILIKE` is not
- For reliable searches, store text in a **consistent form** (data cleaning, session 14)

::: source
Based on SQLite (n.d.-d).
:::

::: notes
Self-study. SQLite: "SQLite only understands upper/lower case for ASCII characters by default." All five results observed in SQLite 3.45.1. A common workaround is `lower(brand) = 'cube'`, which also only lowers ASCII letters in SQLite without the ICU extension. Relevance for the project: imported customer names, cities and product names often vary in case and spelling.
:::

---

# NULL and Three-Valued Logic {.section}

Why some rows go missing

---

# A Comparison with NULL Is Unknown

```sql
SELECT count(*) FROM customer WHERE e_mail = NULL;      -- 0
SELECT count(*) FROM customer WHERE e_mail IS NULL;     -- 3
SELECT count(*) FROM bike WHERE price < 1000;           -- 4
SELECT count(*) FROM bike WHERE price >= 1000;          -- 9
SELECT count(*) FROM bike WHERE price < 1000
                             OR price >= 1000;          -- 13, not 15!
```

- NULL means **unknown or missing** — so `NULL = NULL`, `NULL < 1000` are neither true nor false but **UNKNOWN**
- **WHERE keeps a row only if the condition is TRUE**; FALSE and UNKNOWN rows are dropped
- Test for NULL with **`IS NULL`** and **`IS NOT NULL`** — never with `= NULL`

::: source
Based on Elmasri and Navathe (2016, Chapter 7) and SQLite (n.d.-c, n.d.-d).
:::

::: notes
Core, exam-relevant. The two bikes with unknown price (SCO640, CAN750) are in neither group, so the "complete" condition returns 13 of 15. SQLite shows UNKNOWN as NULL (None in Python): `SELECT NULL = NULL` returns NULL, `SELECT NULL IS NULL` returns 1. `e_mail <> 'x'` returns only the 9 customers with an e-mail address. Elmasri and Navathe discuss three meanings of NULL: unknown value, value exists but is withheld, attribute does not apply. Back to session 7: a CHECK fails only when its condition is FALSE, so UNKNOWN passes — WHERE is the opposite: only TRUE passes.
:::

---

# Three-Valued Logic: Truth Tables

| AND | TRUE | FALSE | UNKNOWN |
|---|---|---|---|
| **TRUE** | TRUE | FALSE | UNKNOWN |
| **FALSE** | FALSE | FALSE | FALSE |
| **UNKNOWN** | UNKNOWN | FALSE | UNKNOWN |

| OR | TRUE | FALSE | UNKNOWN |
|---|---|---|---|
| **TRUE** | TRUE | TRUE | TRUE |
| **FALSE** | TRUE | FALSE | UNKNOWN |
| **UNKNOWN** | TRUE | UNKNOWN | UNKNOWN |

- `NOT UNKNOWN` is UNKNOWN: `NOT (price < 1000)` also misses the two bikes without a price (9 rows)
- Rule of thumb: UNKNOWN AND FALSE is FALSE, UNKNOWN OR TRUE is TRUE — everything else with UNKNOWN stays UNKNOWN

::: source
Adapted from Elmasri and Navathe (2016, Chapter 7).
:::

::: notes
Observed in SQLite: `SELECT NULL AND 0` → 0, `NULL OR 1` → 1, `NULL AND 1` → NULL, `NULL OR 0` → NULL, `NOT NULL` → NULL. Think of UNKNOWN as "could be true or false": if the result is the same either way, SQL knows it. Ask: how do we write "bikes under 1,000 € or with unknown price"? → `price < 1000 OR price IS NULL` (6 rows). This is the hands-on question 8.
:::

---

# The NOT IN Trap

```sql
SELECT count(*) FROM bike WHERE customer_no NOT IN (101, 102);        -- 9
SELECT count(*) FROM bike WHERE frame_no NOT IN ('WAX123', NULL);     -- 0
```

- The first query misses the **4 stock bikes**: `NULL NOT IN (101, 102)` is UNKNOWN
- If the list contains a NULL, `NOT IN` is **never TRUE**: `x NOT IN ('WAX123', NULL)` means `x <> 'WAX123' AND x <> NULL`
- Danger in practice: a list from a subquery (session 10) that contains a NULL silently returns **no rows**

::: callout
Whenever a column can be NULL, ask: **what should happen with the unknown rows?** Then write `IS NULL` or `IS NOT NULL` explicitly.
:::

::: source
Based on SQLite (n.d.-d) and Elmasri and Navathe (2016, Chapter 7).
:::

::: notes
15 bikes: 2 belong to customers 101 or 102, 4 have customer_no NULL → 9. Correct for "all bikes not owned by 101 or 102, including stock": `customer_no NOT IN (101, 102) OR customer_no IS NULL` (13). Second query: for every frame number, `x <> NULL` is UNKNOWN, so the AND is at best UNKNOWN — observed 0 rows. `IN` with a NULL in the list still finds the matching values (observed: `customer_no IN (101, 102, NULL)` → 2). Exam-relevant pattern.
:::

---

# Sorting and Trimming Results {.section}

ORDER BY, DISTINCT, LIMIT

---

# ORDER BY

```sql
SELECT frame_no, brand, price FROM bike ORDER BY brand, price DESC;
```

| frame_no | brand | price |
|---|---|---|
| BRO860 | Brompton | 1749 |
| CAN750 | Canyon | NULL |
| CUB202 | Cube | 3299 |
| WAX123 | Cube | 1899 |
| … | … | … |

- `ASC` (default) or `DESC` **per column**; further columns break ties
- Without ORDER BY, the order of the rows is **undefined** — never rely on it
- SQLite sorts **NULL first** in ascending order (last in descending); `NULLS LAST` / `NULLS FIRST` change this

::: source
Based on SQLite (n.d.-c) and Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
Observed: 15 rows; the four Cubes are sorted by price descending within the brand. `ORDER BY price` puts SCO640 and CAN750 (NULL) first; `ORDER BY price DESC` puts them last. Other DBMS differ: PostgreSQL and Oracle treat NULL as larger than all values (last in ascending order). Today's results often appear in insertion order, but this is an accident of the implementation and can change, e.g. when an index is added (session 10). ORDER BY 2 (column number) works but is hard to read.
:::

---

# DISTINCT and LIMIT

```sql
SELECT DISTINCT brand FROM bike;                  -- 8 brands, not 15 rows
SELECT DISTINCT city FROM customer;               -- 6 rows, one of them NULL

SELECT frame_no, brand, model, price
FROM   bike
ORDER BY price DESC
LIMIT 3;                                          -- the three most expensive bikes
```

- `DISTINCT` removes **duplicate rows** of the result — it applies to **all** selected columns: `DISTINCT brand, model` gives 14 rows
- For DISTINCT, NULLs count as **equal**: one NULL row
- `LIMIT n` returns at most n rows; `LIMIT n OFFSET m` skips m rows first. Use it **with ORDER BY**, otherwise "the first 3" is undefined

::: source
Based on SQLite (n.d.-c) and Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
Observed: 8 brands; 14 brand–model pairs (two Gazelle Ultimate); 6 cities including NULL (Felix Wagner). The top 3 are RIE420 (5899), KTM530 (3599), CUB202 (3299). Ties: `LIMIT 3 OFFSET 3` returns GZT885, GZT884, GZT886 — GZT884 and GZT886 both cost 2499, so which one comes first is not defined; for paging add a tie-breaker (`ORDER BY price DESC, frame_no`). SQL relations are sets (session 5), but SQL results are multisets: duplicates stay unless DISTINCT removes them. LIMIT is not standard SQL; the standard has FETCH FIRST n ROWS ONLY (PostgreSQL, Oracle), SQL Server uses TOP. SQLite also accepts `LIMIT m, n` with the offset first — avoid it.
:::

---

# Query Parameters in Python {.optional}

```python
city = input("City: ")                         # e.g. Heidelberg
rows = con.execute(
    "SELECT name FROM customer WHERE city = ? ORDER BY name",
    (city,)
).fetchall()
# [('Clara Neumann',), ('Jonas Albrecht',), ('Mira Okonkwo',), ('Paul Richter',)]
```

- Never build SQL by **pasting user input** into the string (f-strings, `+`): this allows **SQL injection**
- The `?` placeholder passes the value **separately**; the DBMS treats it as data, never as SQL
- Placeholders work for values in `INSERT`, `UPDATE`, `DELETE` and `WHERE` — not for table or column names

::: source
Own example.
:::

::: notes
Self-study, relevant from session 15 (APIs) and 16 (ETL) on. Observed result for 'Heidelberg': the four names shown. Example of the danger: with an f-string, the input `x' OR '1'='1` turns the condition into one that is always true. For many rows: `con.executemany("INSERT INTO spare_part VALUES (?, ?, ?)", list_of_tuples)`.
:::

---

# Hands-On: Query the Bike Shop {.section}

Business questions in SQL

---

# Exercise: Query the Bike Shop {.exercise}

Write **one query** per question on the fresh sample data. Predict the number of rows first.

1. All Gazelle bikes, most expensive first
2. Name and city of customers **without** an e-mail address
3. Spare parts with a list price from 10 to 40 €, cheapest first
4. Repair jobs in **March 2027**, in date order
5. The cities our customers live in — each city once, alphabetically, no empty entries
6. The **three cheapest bikes in stock**
7. Repair jobs whose description mentions a **chain**
8. Bikes under 1,000 € **or** with an unknown price

::: notes
Groups of 3, about 35 min + 5 min comparison. Expected answers (all observed):
1 `SELECT frame_no, model, price FROM bike WHERE brand = 'Gazelle' ORDER BY price DESC;` → 3 rows: GZT885 2799, GZT884 2499, GZT886 2499.
2 `SELECT name, city FROM customer WHERE e_mail IS NULL;` → 3: Mira Okonkwo (Heidelberg), Felix Wagner (NULL), Tobias Krämer (Mannheim). `= NULL` gives 0 rows.
3 `… WHERE list_price BETWEEN 10 AND 40 ORDER BY list_price;` → 5: P-103 12.5, P-104 24.9, P-111 29.9, P-102 34.9, P-105 39.9.
4 `… WHERE job_date BETWEEN '2027-03-01' AND '2027-03-31' ORDER BY job_date;` → 5: 506–510 (LIKE '2027-03%' also works).
5 `SELECT DISTINCT city FROM customer WHERE city IS NOT NULL ORDER BY city;` → 5: Heidelberg, Ladenburg, Mannheim, Schwetzingen, Weinheim.
6 `… WHERE customer_no IS NULL ORDER BY price LIMIT 3;` → TRK311 1099, GZT884 2499, GZT886 2499.
7 `… WHERE description LIKE '%chain%';` → 505, 511 (case-insensitive).
8 `… WHERE price < 1000 OR price IS NULL;` → 6: CUB201, TRK310, SCO640, CAN750, TRK312, CUB203.
Extra for fast groups: which repair jobs are *not* annual services? `description <> 'Annual service'` gives 7 jobs and misses 506 and 512 (NULL) — add `OR description IS NULL` for 9.
:::

---

# Team Work: Test Data and First Queries {.exercise}

1. Write a **data script** for your project database: 5–15 realistic (fictional) rows per table, inserted in foreign-key order
2. Include **NULLs** where your schema allows them, and at least one case for every referential action
3. Formulate **five business questions** your client would ask and answer each with a single-table `SELECT`
4. Write one `UPDATE` and one `DELETE` that a user of your system would really run — check them with a `SELECT` first

::: callout
Data script and queries are part of **milestone 3** (database and queries, after session 12). Use fictional names only — no real customers or classmates.
:::

::: notes
About 25 min. Walk around and check: PRAGMA foreign_keys on? Insert order correct? Does any query compare with = NULL? ORDER BY wherever the order matters? Questions that need two tables (e.g. "customers and their bikes") are welcome but are answered next session with joins — let teams note them. Remind teams that real personal data must not be used in the project (session 19: GDPR); generated or invented data is fine.
:::

---

# Key Takeaways

- **DML** changes data: `INSERT` adds rows, `UPDATE` changes them, `DELETE` removes them — always with a **WHERE** that you have tested as a SELECT
- Constraints and **referential actions** apply to every change; a failing statement changes **nothing**
- A query: `SELECT` columns `FROM` table `WHERE` condition `ORDER BY` … `LIMIT` …
- Comparisons with NULL are **UNKNOWN**; WHERE keeps only **TRUE** rows — use `IS NULL` / `IS NOT NULL`
- Without `ORDER BY`, row order is undefined; `DISTINCT` removes duplicate result rows

---

# Next Session: SQL III — Joins

- Combining tables: inner joins, left/right/full outer joins
- Self joins (e.g. mechanic and supervisor)
- Join pitfalls: missing and duplicated rows
- Hands-on: multi-table queries on the bike shop

::: callout
**Preparation:** load the sample data into **bikeshop.db** and finish the hands-on questions; bring your team's data script.
:::

---

# References {.references}

- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- SQLite. (n.d.-a). *DELETE*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_delete.html
- SQLite. (n.d.-b). *INSERT*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_insert.html
- SQLite. (n.d.-c). *SELECT*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_select.html
- SQLite. (n.d.-d). *SQL language expressions*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_expr.html
- SQLite. (n.d.-e). *SQLite foreign key support*. Retrieved October 20, 2026, from https://www.sqlite.org/foreignkeys.html
- SQLite. (n.d.-f). *UPDATE*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_update.html
