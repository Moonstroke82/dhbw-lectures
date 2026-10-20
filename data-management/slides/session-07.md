---
course: Data Management
session: 7
title: SQL I: Defining Schemas
subtitle: CREATE, ALTER, DROP · data types and SQLite type affinity · constraints · the course database in SQLite
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# SQL I: Defining Schemas {.title}

::: notes
Time plan for today (3 h): recap 10 min · SQL and CREATE TABLE 15 min · data types and type affinity 20 min · mini exercise data types 10 min · break 10 min · constraints incl. foreign keys 25 min · ALTER and DROP 10 min · Jupyter walkthrough 5 min · hands-on: build the bike shop database 35 min · team work: project schema in SQL 30 min · wrap-up 5 min · ~5–10 min buffer.
Input is about 75 minutes in total, hands-on about 75 minutes. Live coding works better than reading code from slides: keep a notebook open next to the deck and run each statement as it comes up. If the input runs long, set the optional slides (STRICT tables, the CLI, the 12-step procedure) as self-study and shorten the hands-on to tasks 1–3, but keep at least 25 minutes for the teams.
Every statement on these slides was run with Python's sqlite3 module and the sqlite3 command-line tool (SQLite 3.45.1); the error messages shown are the ones SQLite printed.
:::

---

# Today's Agenda

1. Recap: your normalised schema
2. SQL and the data definition language
3. Data types: standard SQL and SQLite type affinity
4. Constraints: keys, NOT NULL, UNIQUE, CHECK, DEFAULT
5. Changing schemas: ALTER and DROP
6. Hands-on: build the bike shop database in Jupyter
7. Team work: your project schema in SQL

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary, 2–3 teams show one relation of their normalised schema) · 0:10 SQL and CREATE TABLE (input, live coding) · 0:25 Data types and affinity (input, live coding) · 0:45 Mini exercise data types (pairs) · 0:55 Break · 1:05 Constraints (input, live coding) · 1:30 ALTER and DROP (input) · 1:40 Jupyter walkthrough · 1:45 Hands-on bike shop (groups of 3, same groups as sessions 3–6, each student on their own laptop) · 2:20 Team work on project schemas · 2:50 Wrap-up.
:::

---

# Recap: From Schema on Paper to Database

- Your team has a **mapped and normalised** relational schema (sessions 5 and 6)
- Which relation has a **composite primary key**? Which foreign keys may be **NULL**?
- Which **business rules** did you note that the schema cannot show yet (e.g. "a quantity is positive")?

::: callout
Today the schema becomes a real database: every relation becomes a **table**, every key and rule a **constraint** that SQLite enforces.
:::

::: notes
Preparation from session 6: laptop with Python, Jupyter and SQLite working, and the normalised schema. Quickly check that everybody can start Jupyter (session 2 setup slide); pair students whose setup does not work with a neighbour for the live coding. Collect 2–3 business rules on the board and come back to them on the CHECK slide. Reminder: milestone 2 (mapped and normalised schema) is due after today.
:::

---

# SQL and the Data Definition Language {.section}

Describing tables in a language the database understands

---

# SQL: One Language, Several Parts

| Part | Purpose | Statements | Session |
|---|---|---|---|
| **DDL** · data definition | Create and change the schema | `CREATE`, `ALTER`, `DROP` | 7 |
| **DML** · data manipulation | Change the data | `INSERT`, `UPDATE`, `DELETE` | 8 |
| **Queries** | Read the data | `SELECT` | 8–10 |
| **DCL** · data control | Grant and revoke access rights | `GRANT`, `REVOKE` | — |
| **Transaction control** | Group changes into units | `COMMIT`, `ROLLBACK` | 10 |

- SQL is **declarative**: you say *what* you want, the DBMS decides *how*
- SQL is standardised by ANSI and ISO, but every product speaks its own **dialect**

::: source
Based on Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
SQL goes back to SEQUEL, developed at IBM in the 1970s for the System R prototype of Codd's relational model. Dialects: data types, ALTER TABLE options and some functions differ between SQLite, PostgreSQL, MySQL, Oracle and SQL Server. In this module we write SQL that is as close to the standard as possible and point out where SQLite differs. SQLite has no user management, so DCL does not exist there (session 2: limits of SQLite).
:::

---

# CREATE TABLE: Anatomy

```sql
CREATE TABLE customer (
    customer_no  INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    e_mail       TEXT    UNIQUE,
    street       TEXT,
    postcode     TEXT    CHECK (length(postcode) = 5),
    city         TEXT
);
```

- One line per **column**: name, **data type**, optional **column constraints**
- **Table constraints** (e.g. a composite primary key) follow after the last column
- Relation CUSTOMER(**customer_no**, name, e_mail, street, postcode, city) from session 5 becomes a table

::: source
Based on Elmasri and Navathe (2016, Chapter 6) and SQLite (n.d.-b).
:::

::: notes
Live coding: run the statement in a notebook (`con.execute("""…""")`). Running it a second time gives "table customer already exists" — show `CREATE TABLE IF NOT EXISTS`, which does nothing if the table exists. Naming conventions for this module: table and column names in lower case with underscores, table names in the singular, the same column name for a primary key and the foreign keys that refer to it. SQL keywords are not case-sensitive; writing them in capitals is a convention for readability. Why is the postcode TEXT and not INTEGER? Leading zeros (01067 Dresden) and it is never used for calculations.
:::

---

# Data Types {.section}

Standard SQL and SQLite type affinity

---

# Data Types in Standard SQL

| Kind | Types | Example column |
|---|---|---|
| Whole numbers | `INTEGER`, `SMALLINT` | quantity |
| Exact decimals | `DECIMAL(p, s)`, `NUMERIC(p, s)` | price DECIMAL(8, 2) |
| Approximate numbers | `REAL`, `DOUBLE PRECISION`, `FLOAT` | sensor value |
| Text | `CHAR(n)` fixed, `VARCHAR(n)` variable length | country CHAR(2), name VARCHAR(80) |
| Truth values | `BOOLEAN` | newsletter |
| Date and time | `DATE`, `TIME`, `TIMESTAMP` | job_date |
| Binary data | `BLOB` | photo |

::: callout
A data type is the technical part of a **domain** (session 5): it restricts which values a column can hold.
:::

::: source
Based on Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
DECIMAL(8, 2): eight digits in total, two of them after the decimal point, so up to 999,999.99. Money belongs in exact decimals, never in REAL/FLOAT: binary floating point cannot represent 0.10 exactly. In SQLite, `SELECT 0.1 + 0.2` gives 0.30000000000000004 and `0.1 + 0.2 = 0.3` is false (0). CHAR(n) pads with spaces, VARCHAR(n) does not; in products such as PostgreSQL, VARCHAR(80) rejects longer values. The next slides show that SQLite treats all of this differently.
:::

---

# SQLite: Storage Classes and Type Affinity

- Each **value** has one of five **storage classes**: `NULL`, `INTEGER`, `REAL`, `TEXT`, `BLOB`
- Each **column** has a **type affinity**: the storage class it *prefers*. It follows from the declared type name:

| Rule (applied in this order) | Affinity | Examples |
|---|---|---|
| 1. Name contains "INT" | INTEGER | INTEGER, BIGINT, SMALLINT |
| 2. Contains "CHAR", "CLOB" or "TEXT" | TEXT | TEXT, VARCHAR(80), CHAR(2) |
| 3. Contains "BLOB", or no type given | BLOB | BLOB |
| 4. Contains "REAL", "FLOA" or "DOUB" | REAL | REAL, DOUBLE, FLOAT |
| 5. Anything else | NUMERIC | NUMERIC, DECIMAL(8,2), DATE, BOOLEAN |

::: source
SQLite (n.d.-c).
:::

::: notes
"Most SQL database engines use static, rigid typing" — SQLite uses dynamic typing: the type belongs to the value, not to the column. The column's affinity only says what SQLite *tries* to convert a value into. The rules work on substrings, which leads to surprises: FLOATING POINT contains "INT" and gets INTEGER affinity; STRING matches no rule and gets NUMERIC affinity, so '12' stored in a STRING column becomes the number 12. That is why the course script uses only the five plain names INTEGER, TEXT, REAL, NUMERIC and BLOB. The rule numbers are not exam-relevant; the idea of affinity is.
:::

---

# Type Affinity in Action

```sql
CREATE TABLE demo (a INTEGER, b TEXT, c NUMERIC, e VARCHAR(5), g DATE);
INSERT INTO demo VALUES ('42', 42, '12.50', 'far too long', '2027-04-06');
INSERT INTO demo VALUES ('forty-two', '007', 'cheap', 'ok', 20270406);
SELECT a, typeof(a), c, typeof(c), e, g, typeof(g) FROM demo;
```

| a | typeof(a) | c | typeof(c) | e | g | typeof(g) |
|---|---|---|---|---|---|---|
| 42 | integer | 12.5 | real | far too long | 2027-04-06 | text |
| forty-two | text | cheap | text | ok | 20270406 | integer |

- Text that looks like a number is **converted**; anything else is stored **as it is** — no error
- The length in `VARCHAR(5)` is **ignored**; `DATE` has no special meaning

::: source
Own example based on SQLite (n.d.-c).
:::

::: notes
Live coding: let students predict each typeof before running. The second row shows the risk: a typo or a wrong import puts text into a number column without any warning. In other products (PostgreSQL, SQL Server), both 'forty-two' and the too-long text would be rejected. Consequence: in SQLite, domain constraints that matter must be written as CHECK constraints (next section) or the table declared STRICT (optional slide). Note that b TEXT turned 42 into the text '42', and that '007' in b stays '007' because the column is TEXT.
:::

---

# Dates, Truth Values and Money in SQLite

| Value | SQLite has no … | Store it as … |
|---|---|---|
| Date and time | date type | `TEXT` in ISO 8601 format: '2027-04-06', '2027-04-06 14:30:00' |
| True / false | Boolean storage class | `INTEGER` 0 or 1 (`TRUE` and `FALSE` are just 1 and 0) |
| Money | exact decimal storage | `NUMERIC` with a CHECK — or `INTEGER` cents (1990 = 19.90 €) |

- ISO dates **sort correctly as text** and work with SQLite's date functions: `date('now')`, `date('2027-04-06', '+14 days')`
- `DECIMAL(8, 2)` gets NUMERIC affinity: 19.90 is stored as the floating-point number 19.9, and 19.00 as the integer 19

::: source
Based on SQLite (n.d.-c).
:::

::: notes
'06.04.2027' (German format) sorts wrongly as text and the date functions do not understand it — always convert to ISO when loading data (session 14). Observed in SQLite 3.45.1: '19.90' inserted into a DECIMAL(8,2) column comes back as 19.9 (real) and '19.00' as 19 (integer); trailing zeros are a display question. For the bike shop and the project, NUMERIC prices are good enough; banks and accounting systems use integer cents or a DBMS with a true DECIMAL type.
:::

---

# STRICT Tables {.optional}

```sql
CREATE TABLE price_list (part_no TEXT PRIMARY KEY, price REAL) STRICT;
INSERT INTO price_list VALUES ('P-17', 'cheap');
-- Error: cannot store TEXT value in REAL column price_list.price
```

- Since SQLite 3.37.0, a table declared `STRICT` **enforces** the column types like other DBMS
- Allowed type names: only `INT`, `INTEGER`, `REAL`, `TEXT`, `BLOB` and `ANY` — `DATE` or `NUMERIC` give an error
- Text that is a valid number is still converted: '12.5' is accepted into a REAL column

::: source
SQLite (n.d.-c, n.d.-b).
:::

::: notes
Self-study. STRICT is useful for the design project if teams want type safety, but then dates and money need TEXT/INTEGER/REAL. Check the version first: `sqlite3.sqlite_version` in Python (session 2 setup cell). Errors observed in 3.45.1: `unknown datatype for s2.d: "DATE"` when creating a STRICT table with a DATE column. The course script does not use STRICT, so it also works on older SQLite versions.
:::

---

# Mini Exercise: Types and Constraints {.exercise}

*Velo Neckar* wants to store its **suppliers**. Write the `CREATE TABLE` statement.

SUPPLIER(**supplier_no**, name, vat_id, country, rating)

- The supplier number is assigned by the database
- Every supplier has a name; the VAT ID is optional but never shared by two suppliers
- The country is a two-letter code (DE, NL, …); if none is given, it is DE
- The rating is a whole number from 1 to 5, or empty if not rated yet

::: notes
About 10 min in pairs, on paper or directly in the notebook. Expected answer (tested):
CREATE TABLE supplier ( supplier_no INTEGER PRIMARY KEY, name TEXT NOT NULL, vat_id TEXT UNIQUE, country TEXT NOT NULL DEFAULT 'DE' CHECK (length(country) = 2), rating INTEGER CHECK (rating BETWEEN 1 AND 5) );
Observed tests: a second supplier with the same VAT ID → "UNIQUE constraint failed: supplier.vat_id"; country 'DEU' → "CHECK constraint failed: length(country) = 2"; rating 6 → "CHECK constraint failed: rating BETWEEN 1 AND 5"; inserting only a name and a VAT ID gives supplier_no 1, country 'DE', rating NULL. This exercise previews the constraint slides — accept constraints written in words if a pair has not used CHECK before. Discuss: a NULL rating passes the CHECK (next section explains why). UNIQUE allows several NULLs.
:::

---

# Constraints {.section}

Integrity rules the database enforces

---

# From Integrity Constraints to SQL

| Integrity constraint (session 5) | SQL constraint | Example |
|---|---|---|
| Key constraint, entity integrity | `PRIMARY KEY` | `job_no INTEGER PRIMARY KEY` |
| Alternate key | `UNIQUE` | `e_mail TEXT UNIQUE` |
| Mandatory attribute | `NOT NULL` | `name TEXT NOT NULL` |
| Domain constraint, business rule | `CHECK` | `CHECK (quantity > 0)` |
| Referential integrity | `FOREIGN KEY … REFERENCES` | `REFERENCES bike (frame_no)` |
| — (a usual value, not a rule) | `DEFAULT` | `DEFAULT CURRENT_DATE` |

- **Column constraint:** written after the column · **Table constraint:** after the last column, needed when a rule involves **several columns**

::: source
Based on Elmasri and Navathe (2016, Chapter 6) and SQLite (n.d.-b).
:::

::: notes
Every violation makes the whole statement fail with an error, and nothing is stored. In Python, the error is raised as sqlite3.IntegrityError, which a program can catch (session 16). DEFAULT is not a constraint in the strict sense, but it is written in the same place. Constraints can be named (`CONSTRAINT positive_qty CHECK (quantity > 0)`), which makes error messages easier to understand in some products.
:::

---

# PRIMARY KEY in SQLite

```sql
CREATE TABLE repair_line (
    job_no         INTEGER NOT NULL REFERENCES repair_job (job_no),
    part_no        TEXT    NOT NULL REFERENCES spare_part (part_no),
    quantity       INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    price_charged  NUMERIC NOT NULL CHECK (price_charged >= 0),
    PRIMARY KEY (job_no, part_no)
);
```

- **Composite key** → table constraint `PRIMARY KEY (job_no, part_no)`
- `INTEGER PRIMARY KEY` (exactly this name) numbers rows **automatically**: 1, 2, 3 …
- **Quirk:** SQLite allows **NULL** in other primary key columns — always add `NOT NULL`

::: source
Based on SQLite (n.d.-b).
:::

::: notes
The quirk is a historical bug that SQLite keeps for backward compatibility. Observed: with `code TEXT PRIMARY KEY`, two rows with code NULL were both accepted. With `code TEXT NOT NULL PRIMARY KEY`: "NOT NULL constraint failed". INTEGER PRIMARY KEY is an alias for SQLite's internal rowid: inserting without a value (or NULL) gives max + 1 — after inserting 10 explicitly, the next automatic value is 11. INT PRIMARY KEY is **not** an alias: inserting without a value stores NULL. A non-number in an INTEGER PRIMARY KEY column gives "datatype mismatch". This is the surrogate key from session 5's optional slide.
:::

---

# NOT NULL, UNIQUE, CHECK and DEFAULT

```sql
CREATE TABLE repair_job (
    job_no       INTEGER PRIMARY KEY,
    job_date     TEXT    NOT NULL DEFAULT CURRENT_DATE
                         CHECK (job_date IS date(job_date)),
    description  TEXT,
    frame_no     TEXT    NOT NULL REFERENCES bike (frame_no)
);
```

- A row inserted **without** a job_date gets today's date (UTC) as 'YYYY-MM-DD'
- `job_date IS date(job_date)` accepts only **valid ISO dates**: '2027-02-30' and '06.04.2027' are rejected
- A CHECK fails only if the condition is **false** — a result of **NULL passes**

::: source
Based on SQLite (n.d.-b).
:::

::: notes
Why `IS` and not `=`? date('06.04.2027') returns NULL because SQLite does not understand the format. With `CHECK (job_date = date(job_date))`, the comparison gives NULL and the CHECK **passes** — observed when testing the course script, which is why it uses IS (IS compares with NULL as a normal value). date('2027-02-30') returns '2027-03-02', so the value differs and the CHECK fails. Observed error: "CHECK constraint failed: job_date IS date(job_date)". Back to the business rules from the recap: which ones can be CHECKs? Rules about a single row (quantity > 0, end after start) can; rules across rows or tables ("a mechanic supervises at most 3 apprentices") cannot — those need triggers or application logic.
:::

---

# FOREIGN KEY and Referential Actions

```sql
CREATE TABLE bike (
    frame_no     TEXT    NOT NULL PRIMARY KEY,
    brand        TEXT    NOT NULL,
    model        TEXT    NOT NULL,
    price        NUMERIC CHECK (price >= 0),
    customer_no  INTEGER REFERENCES customer (customer_no)
                         ON DELETE SET NULL
);
```

| Clause | Effect when a customer is deleted |
|---|---|
| no clause (`NO ACTION`) or `RESTRICT` | Delete rejected while bikes refer to the customer |
| `ON DELETE CASCADE` | The customer's bikes are deleted too |
| `ON DELETE SET NULL` | bike.customer_no becomes NULL |

::: source
Based on SQLite (n.d.-d) and Elmasri and Navathe (2016, Chapter 6).
:::

::: notes
The referential actions from session 5, now as syntax. ON UPDATE works the same way for changes of the referenced key. A composite foreign key is written as a table constraint: FOREIGN KEY (job_no, part_no) REFERENCES … (…). The referenced columns must be the primary key or UNIQUE. In the course script: bike → customer SET NULL (bike stays, owner unknown), repair_job → bike RESTRICT (keep the history), repair_line and job_mechanic → repair_job CASCADE (weak entity type / M:N rows belong to the job). The difference between NO ACTION and RESTRICT only matters for deferred constraints and inside transactions — not exam-relevant.
:::

---

# Switch Them On: PRAGMA foreign_keys

```python
con = sqlite3.connect("bikeshop.db")
con.execute("PRAGMA foreign_keys = ON")    # right after connecting!
con.execute("INSERT INTO bike VALUES ('GZT884', 'Gazelle', 'Ultimate', 2499, 999)")
# sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

- In SQLite, foreign key enforcement is **off by default** and must be switched on **for every connection**
- Without the PRAGMA, the insert above **succeeds** — a bike for the non-existent customer 999
- Inside an open transaction, the PRAGMA has **no effect** (and no error)
- `PRAGMA foreign_key_check` lists rows that violate a foreign key

::: source
SQLite (n.d.-d).
:::

::: notes
The most common SQLite mistake in student projects. Observed without the PRAGMA: the insert succeeds; `PRAGMA foreign_key_check` then returns ('bike', 1, 'customer', 0) — table, rowid, referenced table, number of the foreign key. Observed in Python: after an INSERT (Python opens a transaction automatically), `PRAGMA foreign_keys = ON` is silently ignored and `PRAGMA foreign_keys` still returns 0; after `con.commit()` it works. So: put the PRAGMA in the first cell, directly after connect. The setting is not stored in the database file: a new connection (or a restarted notebook kernel) starts with foreign keys off again. Other DBMS enforce foreign keys always.
:::

---

# Changing Schemas: ALTER and DROP {.section}

Schemas evolve — carefully

---

# ALTER TABLE

```sql
ALTER TABLE customer ADD COLUMN phone TEXT;
ALTER TABLE customer ADD COLUMN newsletter INTEGER NOT NULL DEFAULT 0
    CHECK (newsletter IN (0, 1));
ALTER TABLE customer RENAME COLUMN e_mail TO email;
ALTER TABLE customer DROP COLUMN phone;
ALTER TABLE spare_part RENAME TO part;
```

- SQLite supports four forms: `ADD COLUMN`, `RENAME COLUMN`, `DROP COLUMN`, `RENAME TO`
- `ADD COLUMN` restrictions: no PRIMARY KEY or UNIQUE; NOT NULL needs a **default**; no `CURRENT_DATE` default
- **Not** possible in SQLite: change a data type, add a constraint to an existing column — other DBMS offer `ALTER COLUMN`, `ADD CONSTRAINT`

::: source
SQLite (n.d.-a); Elmasri and Navathe (2016, Chapter 7).
:::

::: notes
Observed errors (SQLite 3.45.1): ADD COLUMN … UNIQUE → "Cannot add a UNIQUE column"; ADD COLUMN birth_year INTEGER NOT NULL → "Cannot add a NOT NULL column with default value NULL" (existing rows would violate it); DEFAULT CURRENT_DATE → "Cannot add a column with non-constant default"; DROP COLUMN email (UNIQUE) → "cannot drop UNIQUE column"; DROP COLUMN customer_no → "cannot drop PRIMARY KEY column"; ALTER COLUMN … → syntax error. RENAME TO also updates foreign keys in other tables: repair_line now REFERENCES "part". Very recent SQLite versions (3.53.0, 2026) add a form of ALTER COLUMN for NOT NULL — not used in this module. Other products: ALTER TABLE … ALTER COLUMN … TYPE, ADD CONSTRAINT (Elmasri and Navathe, Chapter 7).
:::

---

# Bigger Changes: Rebuild the Table {.optional}

For changes ALTER TABLE cannot do, the SQLite documentation describes a **rebuild**:

1. Switch foreign keys off and start a transaction
2. `CREATE TABLE new_bike (…)` with the new definition
3. `INSERT INTO new_bike SELECT … FROM bike` to copy the data
4. `DROP TABLE bike`, then `ALTER TABLE new_bike RENAME TO bike`
5. Recreate indexes, triggers and views; run `PRAGMA foreign_key_check`; commit; switch foreign keys on

::: callout
In an early project, the simplest rebuild is often: fix the **script**, drop all tables and run it again.
:::

::: source
Based on SQLite (n.d.-a).
:::

::: notes
Self-study. The documentation lists twelve steps; this is a shortened version. It warns against renaming the old table first and creating the new one under the original name, because that can break references. For the design project: keep the whole schema in one .sql script under version control (or at least in the team folder) and rebuild the database from it — that is why the course script starts with DROP TABLE IF EXISTS. Once real data is loaded (milestone 4), migrations need more care.
:::

---

# DROP TABLE

```sql
DROP TABLE IF EXISTS job_mechanic;   -- no error if the table does not exist
DROP TABLE bike;
-- sqlite3.IntegrityError: FOREIGN KEY constraint failed
```

- `DROP TABLE` deletes the table **and all its data** — there is no undo
- With foreign keys on, SQLite first deletes all rows, so **referential actions fire**: dropping customer sets bike.customer_no to NULL; dropping bike fails while repair jobs refer to it (RESTRICT)
- Drop in **reverse order** of creation: tables with foreign keys first

::: source
SQLite (n.d.-d); Elmasri and Navathe (2016, Chapter 7).
:::

::: notes
Observed: with one customer, one bike and one repair job, `DROP TABLE customer` succeeded and set the bike's customer_no to NULL (ON DELETE SET NULL); `DROP TABLE bike` then failed because repair_job refers to it with ON DELETE RESTRICT; the bike table and its row stayed. After a parent table is gone, inserts into the child fail with "no such table: main.customer". Standard SQL has DROP TABLE … CASCADE / RESTRICT, which drops or protects dependent objects; SQLite does not support these keywords. Also: DROP INDEX, DROP VIEW (session 10).
:::

---

# Hands-On: The Course Database {.section}

The bike shop in SQLite

---

# The Bike Shop Schema as a Script

- All tables of the normalised *Velo Neckar* schema in one file: **bikeshop-schema.sql** (linked from worksheet 7 on the course page)
- Nine tables: customer, bike, repair_job, spare_part, repair_line, employee, mechanic, salesperson, job_mechanic

```python
import sqlite3

con = sqlite3.connect("bikeshop.db")
con.execute("PRAGMA foreign_keys = ON")
with open("bikeshop-schema.sql", encoding="utf-8") as f:
    con.executescript(f.read())

for row in con.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
    print(row[0])
```

::: source
Own example based on the bike shop case from sessions 3–6.
:::

::: notes
5 min walkthrough before the hands-on. The script and the notebook must be in the same folder (or give the full path). `executescript` runs several statements separated by semicolons; `execute` runs only one. The output lists the nine table names. Further checks: `PRAGMA table_info(bike)` shows columns, types, NOT NULL and primary key flags; `SELECT sql FROM sqlite_master WHERE name = 'bike'` shows the CREATE statement. Command-line alternative (optional): `sqlite3 bikeshop.db < bikeshop-schema.sql` — tested; note that a new sqlite3 session again starts with `PRAGMA foreign_keys` = 0. DB Browser for SQLite (session 2) shows the same structure graphically.
:::

---

# Exercise: Build the Bike Shop Database {.exercise}

1. Create **bikeshop.db** from the script and check that all nine tables exist
2. **Predict**, then run: which statements fail, and why? What is in bike afterwards?

```sql
INSERT INTO customer (customer_no, name) VALUES (101, 'Anna Berger');
INSERT INTO bike VALUES ('WAX123', 'Cube', 'Kathmandu', 1899.00, 101);
INSERT INTO repair_job (job_no, frame_no) VALUES (501, 'WAX123');
INSERT INTO repair_job (job_no, frame_no) VALUES (502, 'XYZ999');
INSERT INTO bike VALUES ('GZT884', 'Gazelle', 'Ultimate', -10, NULL);
DELETE FROM customer WHERE customer_no = 101;
```

3. Add the **rental part** from session 6: BIKE_CATEGORY, RENTAL_BIKE, RENTAL, RENTAL_LINE
4. Restart the kernel and repeat statement 4 **without** the PRAGMA. What happens?

::: notes
Groups of 3, each on their own laptop, about 30 min + 5 min comparison. INSERT and DELETE are a preview of session 8 — the syntax is self-explanatory.
Expected answers (all observed): 1 nine table names. 2 Statements 1–3 succeed; job 501 gets today's date as job_date (DEFAULT). Statement 4: "FOREIGN KEY constraint failed" (no bike XYZ999). Statement 5: "CHECK constraint failed: price >= 0". Statement 6 succeeds; bike WAX123 remains with customer_no NULL (ON DELETE SET NULL); price shows as 1899 (NUMERIC affinity stores 1899.00 as an integer).
3 Tested solution: bike_category (category TEXT NOT NULL PRIMARY KEY, day_rate NUMERIC NOT NULL CHECK (day_rate > 0)) · rental_bike (frame_no TEXT NOT NULL PRIMARY KEY, category TEXT NOT NULL REFERENCES bike_category (category)) · rental (rental_no INTEGER PRIMARY KEY, rental_date TEXT NOT NULL DEFAULT CURRENT_DATE, days INTEGER NOT NULL CHECK (days >= 1), customer_no INTEGER NOT NULL REFERENCES customer (customer_no), employee_no INTEGER REFERENCES salesperson (employee_no)) · rental_line (rental_no INTEGER NOT NULL REFERENCES rental (rental_no) ON DELETE CASCADE, frame_no TEXT NOT NULL REFERENCES rental_bike (frame_no), rate_charged NUMERIC NOT NULL CHECK (rate_charged >= 0), PRIMARY KEY (rental_no, frame_no)). Create them in this order (referenced tables first). Observed: a rental bike with category 'mountain' fails (FK); deleting a customer with a rental fails (NO ACTION); deleting a rental deletes its lines (CASCADE).
4 After a restart the connection has foreign keys off: the repair job for XYZ999 is accepted, and `PRAGMA foreign_key_check` lists it. Delete it again and add the PRAGMA.
:::

---

# Team Work: Your Project Schema in SQL {.exercise}

1. Write a **.sql script** with one `CREATE TABLE` per relation of your normalised schema, in an order that respects the foreign keys
2. Choose **data types** deliberately (dates as ISO text, money as NUMERIC or cents)
3. Add **constraints**: primary and foreign keys with referential actions, NOT NULL, UNIQUE, and at least three **CHECK** constraints from your business rules
4. Run the script from Jupyter with foreign keys on, insert two test rows per table, and try to break each constraint once

::: callout
**Milestone 2** (mapped and normalised relational schema) is **due after this session**. The SQL script is the starting point for **milestone 3** (database and queries, after session 12).
:::

::: notes
About 30 min. Walk around and check: PRAGMA foreign_keys in the first cell? INTEGER PRIMARY KEY or NOT NULL on every key? Composite keys as table constraints? Foreign key columns with the same type as the referenced key? Business rules as CHECKs where possible, the rest documented. Typical problems: a foreign key referencing a column that is neither primary key nor UNIQUE (observed: the CREATE works, but every insert into the child table fails with "foreign key mismatch", naming both tables); a table created before the table it refers to (the CREATE works, but inserts fail with "no such table" until the parent exists); names with spaces or umlauts. Milestone 2 hand-in: the relational schema in text notation with keys marked, the FDs checked and any denormalisation justified; the SQL script is welcome but only required for milestone 3.
:::

---

# Key Takeaways

- **DDL** defines the schema: `CREATE TABLE`, `ALTER TABLE`, `DROP TABLE`
- Standard SQL has **static types**; SQLite uses **type affinity** — values keep their own storage class, unless the table is STRICT
- Constraints turn the integrity rules into SQL: **PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK**, plus **DEFAULT**
- SQLite enforces foreign keys only after **`PRAGMA foreign_keys = ON`** — on every connection
- ALTER TABLE in SQLite is limited; keep the schema in a **script** you can rerun

---

# Next Session: SQL II — Manipulating and Querying Data

- Inserting, changing and deleting data: `INSERT`, `UPDATE`, `DELETE`
- Querying one table: `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `LIMIT`
- Hands-on: load sample data into the bike shop database and query it in Jupyter

::: callout
**Preparation:** have **bikeshop.db** created from the course script, and your team's SQL script running without errors.
:::

---

# References {.references}

- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- SQLite. (n.d.-a). *ALTER TABLE*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_altertable.html
- SQLite. (n.d.-b). *CREATE TABLE*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_createtable.html
- SQLite. (n.d.-c). *Datatypes in SQLite*. Retrieved October 20, 2026, from https://www.sqlite.org/datatype3.html
- SQLite. (n.d.-d). *SQLite foreign key support*. Retrieved October 20, 2026, from https://www.sqlite.org/foreignkeys.html
