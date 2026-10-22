---
course: Data Management
session: 7
title: SQL I: Defining Schemas
subtitle: Practice tasks on CREATE, ALTER and DROP, data types and SQLite type affinity, and constraints
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 7 on your own or with your project team. Tasks 1, 2, 3 and 7 can be done on paper; for tasks 4 to 6 you need Jupyter with Python's built-in `sqlite3` module (setup from session 2). Every notebook should start with the cell below: without the `PRAGMA`, SQLite does not check foreign keys (SQLite, n.d.-d). The data types and constraints follow the slides, which are based on Elmasri and Navathe (2016, Chapters 6 and 7) and the SQLite documentation. The complete schema of the bike shop from the session is available as a script: [bikeshop-schema.sql](data/bikeshop-schema.sql). Tasks 3, 4 and 7 continue the food co-op, coworking space and sports club cases from worksheets 5 and 6.

```python
import sqlite3

con = sqlite3.connect("practice.db")   # or ":memory:" for a throw-away database
con.execute("PRAGMA foreign_keys = ON")

def run(sql):
    """Run one statement and show the result or the error message."""
    try:
        print(con.execute(sql).fetchall())
    except sqlite3.Error as e:
        print(type(e).__name__, "-", e)
```

## Business Rules as Constraints

**Part A.** A cinema stores films, screenings, seats, customers and tickets. For each business rule, name the SQL constraint (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `UNIQUE`, `CHECK` or `DEFAULT`) and write the clause as it would appear in the `CREATE TABLE` statement.

1. Each film has a number that identifies it; the database assigns it.
2. Every film must have a title.
3. The age rating of a film is 0, 6, 12, 16 or 18.
4. A seat is identified by the hall number, the row number and the seat number together.
5. Every ticket belongs to an existing screening.
6. A ticket price is never negative.
7. If no discount is given, the discount is 0.
8. An e-mail address belongs to at most one customer account, but customers do not have to give one.

**Part B.** Which part of SQL does each statement belong to: DDL, DML, query, DCL or transaction control?

`CREATE INDEX` · `UPDATE` · `GRANT` · `DROP VIEW` · `SELECT` · `ROLLBACK` · `ALTER TABLE` · `INSERT`

::: answer lines=12
:::

::: solution
Part A (column names may differ):

1. **PRIMARY KEY**: `film_no INTEGER PRIMARY KEY`. In SQLite, exactly `INTEGER PRIMARY KEY` numbers rows automatically (SQLite, n.d.-b).
2. **NOT NULL**: `title TEXT NOT NULL`.
3. **CHECK**: `age_rating INTEGER NOT NULL CHECK (age_rating IN (0, 6, 12, 16, 18))`. Without NOT NULL, a film without a rating would pass, because a CHECK that evaluates to NULL is not violated (SQLite, n.d.-b); accept answers without NOT NULL if the CHECK is correct.
4. **PRIMARY KEY** as a **table constraint**: `PRIMARY KEY (hall_no, row_no, seat_no)` after the last column, with all three columns NOT NULL. Writing PRIMARY KEY after each of the three columns is wrong (a table can only have one primary key).
5. **FOREIGN KEY**: `screening_no INTEGER NOT NULL REFERENCES screening (screening_no)`. NOT NULL because every ticket belongs to a screening.
6. **CHECK**: `price NUMERIC NOT NULL CHECK (price >= 0)`.
7. **DEFAULT**: `discount NUMERIC NOT NULL DEFAULT 0`.
8. **UNIQUE**: `e_mail TEXT UNIQUE`, without NOT NULL. UNIQUE allows several NULLs (tested in SQLite: two rows with NULL are accepted).

All clauses were tested in SQLite; for example, an age rating of 14 gives "CHECK constraint failed: age_rating IN (0, 6, 12, 16, 18)" and a second identical seat gives "UNIQUE constraint failed: seat.hall_no, seat.row_no, seat.seat_no".

Part B: DDL: `CREATE INDEX`, `DROP VIEW`, `ALTER TABLE` · DML: `UPDATE`, `INSERT` · query: `SELECT` · DCL: `GRANT` · transaction control: `ROLLBACK`.
:::

## Predict the Type Affinity

**Part A.** Use the five affinity rules from the session (in their order) to give the **type affinity** of a column declared with each type name.

| Declared type | Affinity |
|---|---|
| VARCHAR(30) | |
| BIGINT | |
| DECIMAL(6,2) | |
| DATETIME | |
| BOOLEAN | |
| FLOATING POINT | |
| STRING | |
| DOUBLE | |
| CHARACTER(2) | |
| *(no type given)* | |

**Part B.** Predict the stored value and the result of `typeof()` for each cell after these statements. Then check your answers in Jupyter.

```sql
CREATE TABLE contact (a VARCHAR(3), b STRING, c FLOATING POINT, d BOOLEAN);
INSERT INTO contact VALUES ('abcdef', '0621', '2.5', 'yes');
INSERT INTO contact VALUES (42, '12.0', '7', TRUE);
SELECT a, typeof(a), b, typeof(b), c, typeof(c), d, typeof(d) FROM contact;
```

**Part C.** Which of the results could cause a problem for a business? Name one and say how you would prevent it.

::: hint
The rules look for **substrings** in the type name and are applied in order: the first rule that matches wins. A value is converted to a number only if it is text that looks like a number.
:::

::: answer lines=10
:::

::: solution
Part A: VARCHAR(30) TEXT · BIGINT INTEGER · DECIMAL(6,2) NUMERIC · DATETIME NUMERIC · BOOLEAN NUMERIC · FLOATING POINT **INTEGER** (contains "INT", rule 1 comes first) · STRING **NUMERIC** (matches no rule) · DOUBLE REAL · CHARACTER(2) TEXT (contains "CHAR") · no type BLOB. Source: SQLite (n.d.-c).

Part B (observed in SQLite 3.45.1):

| | a | b | c | d |
|---|---|---|---|---|
| Row 1 | 'abcdef', text | 621, integer | 2.5, real | 'yes', text |
| Row 2 | '42', text | 12, integer | 7, integer | 1, integer |

- a: the length 3 is ignored; the number 42 is converted to text because the affinity is TEXT.
- b: STRING has NUMERIC affinity, so '0621' becomes the integer 621 and '12.0' the integer 12.
- c: INTEGER affinity stores 2.5 as a real (it cannot be converted to an integer without loss) and '7' as the integer 7.
- d: 'yes' is not a number and is stored as text; TRUE is the integer 1.

Part C: any one with a sensible prevention, e.g. a phone number or postcode declared as STRING (or INTEGER) loses its **leading zero** (0621 → 621): declare it as TEXT. Or: 'yes' is accepted in a Boolean column: use `INTEGER NOT NULL CHECK (d IN (0, 1))`. Or: VARCHAR(3) does not limit the length: add `CHECK (length(a) <= 3)`. A STRICT table also prevents wrong storage classes (optional slide).
:::

## Find the Mistakes: Food Co-op Script

A team wrote this script for the food co-op from worksheet 5. It runs **without any error message** in SQLite. Find **at least six** mistakes or weaknesses and correct them. Think about the mapping rules from session 5 as well as about SQLite.

```sql
CREATE TABLE member (
    member_no      TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    street         TEXT,
    postcode       INTEGER,
    city           TEXT,
    date_of_birth  TEXT,
    age            INTEGER
);

CREATE TABLE member_phone (
    member_no  TEXT NOT NULL REFERENCES member (member_no),
    phone_no   TEXT NOT NULL,
    PRIMARY KEY (member_no)
);

CREATE TABLE product (
    product_no  INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    unit        TEXT,
    farm_id     INTEGER REFERENCES farm (name)
);

CREATE TABLE farm (
    farm_id  INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    region   TEXT
);

CREATE TABLE rating (
    member_no   TEXT REFERENCES member (member_no),
    product_no  INTEGER REFERENCES product (product_no),
    stars       INTEGER CHECK (stars >= 1 OR stars <= 5),
    comment     TEXT
);
```

::: hint
"No error message" only means the statements are valid SQL. Try inserting a few rows (with foreign keys switched on) and see what happens.
:::

::: answer lines=14
:::

::: solution
Mistakes (1 point each for a tutor; the observed behaviour comes from running the script with foreign keys on):

1. **member_no can be NULL**: in SQLite, a TEXT PRIMARY KEY accepts NULL (SQLite, n.d.-b; two members with member_no NULL were accepted). Fix: `member_no TEXT NOT NULL PRIMARY KEY`.
2. **postcode INTEGER**: '01067' is stored as 1067; the leading zero is lost. Fix: `postcode TEXT CHECK (length(postcode) = 5)`.
3. **age** is a derived attribute and must not be stored (session 5 mapping rule; session 4 pitfall). Fix: drop the column; calculate the age from date_of_birth.
4. **member_phone key**: `PRIMARY KEY (member_no)` allows only one phone number per member; the second number fails with "UNIQUE constraint failed: member_phone.member_no". A multi-valued attribute needs both columns in the key: `PRIMARY KEY (member_no, phone_no)`.
5. **product.farm_id references farm (name)**, which is not a key. The CREATE works, but every insert into product fails with "foreign key mismatch - "product" referencing "farm"". Fix: `REFERENCES farm (farm_id)`.
6. **product.farm_id may be NULL**, but every product comes from exactly one farm: add `NOT NULL`.
7. **rating has no primary key**: a member can rate the same product several times. Fix: `PRIMARY KEY (member_no, product_no)` and NOT NULL on both columns.
8. **CHECK with OR** is always true for a number (every number is ≥ 1 or ≤ 5): with foreign keys off, ratings with 9 and −3 stars were accepted. Fix: `CHECK (stars BETWEEN 1 AND 5)`, plus NOT NULL.
9. Also accept: farm is created **after** product, which refers to it (SQLite accepts the CREATE, but inserts into product fail until farm exists, and many other DBMS reject the CREATE itself); no referential actions (e.g. `ON DELETE CASCADE` for ratings and phone numbers of a deleted member); no format check for date_of_birth (e.g. `CHECK (date_of_birth IS date(date_of_birth))`); the locker table from worksheet 5 is missing.

The corrected script was tested: all corrected constraints reject the faulty rows and accept valid ones.
:::

## Lab: Integrity Constraints in the Coworking Space

Worksheet 5 asked on paper which operations on the coworking database are accepted. Now test this in SQLite. The relations are:

- PLAN(**plan_code**, monthly_fee)
- MEMBER(**member_no**, name, *plan_code* → PLAN), *plan_code* may be NULL
- BOOKING(**desk_no, booking_date**, *member_no* → MEMBER), *member_no* NOT NULL

1. Create a **naive** version of the three tables with only data types, primary keys and `REFERENCES` clauses — no NOT NULL, no CHECK, no referential actions — in a connection **without** `PRAGMA foreign_keys = ON`. Insert the data below and run the seven operations, one after the other. Write down which ones are accepted.
2. Repeat with a new database and `PRAGMA foreign_keys = ON`. What changes?
3. Write a **complete** version with all constraints that the business rules need. Use `ON DELETE RESTRICT` for both foreign keys. Repeat the test. Which operations are rejected now, and with which error message?
4. Compare with your paper answers from worksheet 5. Where does SQLite behave differently from the relational model, and why?

```sql
INSERT INTO plan VALUES ('FLEX', 99), ('FIX', 249);
INSERT INTO member VALUES ('M1', 'Jonas Weber', 'FLEX'),
                          ('M2', 'Sara Öztürk', 'FIX'),
                          ('M3', 'Tim Lang', NULL);
INSERT INTO booking VALUES ('D4', '2027-05-03', 'M1'), ('D7', '2027-05-03', 'M2');
```

| # | Operation |
|---|---|
| 1 | `INSERT INTO member VALUES ('M4', 'Eva Kim', 'PRO')` |
| 2 | `INSERT INTO booking VALUES ('D4', '2027-05-03', 'M3')` |
| 3 | `INSERT INTO booking VALUES (NULL, '2027-05-04', 'M2')` |
| 4 | `UPDATE plan SET monthly_fee = 'ninety-nine' WHERE plan_code = 'FLEX'` |
| 5 | `INSERT INTO member VALUES ('M5', 'Ali Demir', NULL)` |
| 6 | `DELETE FROM member WHERE member_no = 'M1'` |
| 7 | `DELETE FROM plan WHERE plan_code = 'FLEX'` |

::: hint
For operation 4, try `SELECT 'ninety-nine' >= 0` first. In SQLite, a text value compared with a number is always the greater one, so a simple `CHECK (monthly_fee >= 0)` is not enough. The function `typeof()` helps.
:::

::: answer lines=14
:::

::: solution
`UPDATE` and `DELETE` are a preview of session 8; their meaning is clear from the text. Observed in SQLite 3.45.1:

| # | Naive, no PRAGMA | Naive, with PRAGMA | Complete |
|---|---|---|---|
| 1 | accepted | rejected: FOREIGN KEY constraint failed | rejected: FOREIGN KEY constraint failed |
| 2 | rejected: UNIQUE constraint failed: booking.desk_no, booking.booking_date | same | same |
| 3 | accepted | accepted | rejected: NOT NULL constraint failed: booking.desk_no |
| 4 | accepted | accepted | rejected: CHECK constraint failed |
| 5 | accepted | accepted | accepted |
| 6 | accepted (booking of M1 is left orphaned) | rejected: FOREIGN KEY constraint failed | rejected: FOREIGN KEY constraint failed |
| 7 | accepted (M1 was already deleted; nothing refers to FLEX any more) | rejected: FOREIGN KEY constraint failed | rejected: FOREIGN KEY constraint failed |

Complete version (tested):

```sql
CREATE TABLE plan (
    plan_code    TEXT    NOT NULL PRIMARY KEY,
    monthly_fee  NUMERIC NOT NULL
                 CHECK (typeof(monthly_fee) IN ('integer', 'real')
                        AND monthly_fee >= 0)
);
CREATE TABLE member (
    member_no  TEXT NOT NULL PRIMARY KEY,
    name       TEXT NOT NULL,
    plan_code  TEXT REFERENCES plan (plan_code) ON DELETE RESTRICT
);
CREATE TABLE booking (
    desk_no       TEXT NOT NULL,
    booking_date  TEXT NOT NULL CHECK (booking_date IS date(booking_date)),
    member_no     TEXT NOT NULL REFERENCES member (member_no) ON DELETE RESTRICT,
    PRIMARY KEY (desk_no, booking_date)
);
```

Differences from the relational model (task 4):

- **Entity integrity** (operation 3): SQLite allows NULL in a primary key column that is not INTEGER PRIMARY KEY. Fix: NOT NULL on every key column.
- **Domain constraint** (operation 4): type affinity stores 'ninety-nine' as text in a NUMERIC column. `CHECK (monthly_fee >= 0)` alone does **not** help, because `'ninety-nine' >= 0` is true (1) in SQLite; the `typeof()` test is needed (or a STRICT table). A text such as '99.50' is still accepted, because it is converted to the number 99.5 before the check.
- **Referential integrity** (operations 1, 6, 7): only checked with `PRAGMA foreign_keys = ON`.
- Operation 7 depends on operation 6: with foreign keys on, M1 still exists and refers to FLEX, so deleting FLEX is rejected.
:::

## Referential Actions in a Dental Practice

The dental practice from worksheet 5 implemented its schema like this (foreign keys are switched on):

```sql
CREATE TABLE patient (patient_no TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE dentist (dentist_no TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE treatment (
    code         TEXT    NOT NULL PRIMARY KEY,
    description  TEXT    NOT NULL,
    fee          NUMERIC NOT NULL CHECK (fee >= 0)
);
CREATE TABLE appointment (
    appointment_no  INTEGER PRIMARY KEY,
    start_time      TEXT NOT NULL,
    patient_no      TEXT NOT NULL REFERENCES patient (patient_no) ON DELETE CASCADE,
    dentist_no      TEXT REFERENCES dentist (dentist_no) ON DELETE SET NULL
);
CREATE TABLE performed (
    appointment_no  INTEGER NOT NULL
                    REFERENCES appointment (appointment_no) ON DELETE CASCADE,
    code            TEXT    NOT NULL REFERENCES treatment (code),
    quantity        INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    PRIMARY KEY (appointment_no, code)
);
```

Current data:

| Table | Rows |
|---|---|
| patient | (P1, Mara Lenz) · (P2, Can Aydin) |
| dentist | (D1, Dr. Haas) · (D2, Dr. Okafor) |
| treatment | (T01, Check-up, 30) · (T02, Filling, 80) |
| appointment | (1, 2027-03-01 09:00, P1, D1) · (2, 2027-03-08 10:30, P1, D2) · (3, 2027-03-09 14:00, P2, D1) |
| performed | (1, T01, 1) · (1, T02, 2) · (3, T01, 1) |

1. The statements below are run **one after the other**. For each, say whether it succeeds and which rows change in which tables.
2. How many rows does each table contain at the end?
3. Is `ON DELETE CASCADE` from patient to appointment a good choice for a dental practice? Suggest a better option and justify it.

| # | Statement |
|---|---|
| a | `DELETE FROM treatment WHERE code = 'T02'` |
| b | `DELETE FROM dentist WHERE dentist_no = 'D1'` |
| c | `DELETE FROM patient WHERE patient_no = 'P1'` |
| d | `DELETE FROM treatment WHERE code = 'T02'` |
| e | `INSERT INTO performed (appointment_no, code) VALUES (3, 'T02')` |

::: answer lines=12
:::

::: solution
Observed in SQLite with foreign keys on:

1. 
  - a **Rejected** ("FOREIGN KEY constraint failed"): performed (1, T02) refers to T02, and the foreign key has no action clause (NO ACTION).
  - b **Succeeds**: D1 is deleted; appointments 1 and 3 get dentist_no NULL (SET NULL).
  - c **Succeeds**: P1 is deleted; appointments 1 and 2 are deleted (CASCADE), and through them the performed rows (1, T01) and (1, T02) (a second CASCADE: actions can form a chain).
  - d **Succeeds** now: no row refers to T02 any more.
  - e **Rejected** ("FOREIGN KEY constraint failed"): treatment T02 no longer exists.
2. patient 1 (P2) · dentist 1 (D2) · treatment 1 (T01) · appointment 1 (number 3, dentist NULL) · performed 1 ((3, T01, 1)).
3. No. Deleting a patient silently deletes the medical and billing history; medical records have to be kept for years. Better: **RESTRICT** (or no action clause), so patients with appointments cannot be deleted, plus a status column (e.g. `active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1))`) to mark former patients. CASCADE from appointment to performed is fine: performed rows do not exist without their appointment (like a weak entity type). SET NULL for a dentist who leaves is defensible, but RESTRICT plus an inactive flag would also keep the information who treated the patient.
:::

## Changing a Schema: Car-Sharing Vehicles

The car-sharing company from worksheets 4 and 5 already has data in this table:

```sql
CREATE TABLE vehicle (
    licence_plate  TEXT    NOT NULL PRIMARY KEY,
    model          TEXT    NOT NULL,
    location       TEXT,
    mileage        INTEGER CHECK (mileage >= 0)
);
INSERT INTO vehicle VALUES ('MA-CS 101', 'VW ID.3', 'Mannheim Hbf', 18250),
                           ('MA-CS 102', 'Opel Corsa', 'Quadrate', 40310);
```

**Part A.** For each change request, write the `ALTER TABLE` statement, or explain why SQLite's `ALTER TABLE` cannot do it and what you would do instead. Test your statements in Jupyter.

1. Store the colour of a vehicle (optional).
2. Store whether a vehicle is active (mandatory, 0 or 1); all existing vehicles are active.
3. Rename the column location to station.
4. Store the vehicle identification number (VIN), which must be unique.
5. Store the registration date; new vehicles should get today's date automatically.
6. Store the mileage with decimals (REAL instead of INTEGER).

**Part B.** Write the statements for the table rebuild needed for request 6, keeping the data.

::: hint
Run each failing statement and read the error message: it says exactly which restriction of ADD COLUMN applies.
:::

::: answer lines=14
:::

::: solution
Part A (observed in SQLite 3.45.1):

1. `ALTER TABLE vehicle ADD COLUMN colour TEXT;` works; existing rows get NULL.
2. `ALTER TABLE vehicle ADD COLUMN active INTEGER NOT NULL DEFAULT 1 CHECK (active IN (0, 1));` works. Without the DEFAULT the error is "Cannot add a NOT NULL column with default value NULL", because the existing rows would violate NOT NULL.
3. `ALTER TABLE vehicle RENAME COLUMN location TO station;` works.
4. `ADD COLUMN vin TEXT UNIQUE` fails: "Cannot add a UNIQUE column". Options: rebuild the table with `vin TEXT UNIQUE`, or add the column without UNIQUE and create a unique index (`CREATE UNIQUE INDEX vehicle_vin ON vehicle (vin);`, indexes follow in session 10). Both were tested; the index then rejects a duplicate VIN with "UNIQUE constraint failed: vehicle.vin".
5. `ADD COLUMN registered_on TEXT DEFAULT CURRENT_DATE` fails: "Cannot add a column with non-constant default". Options: rebuild the table with the DEFAULT, or add the column without a default and fill the existing rows with `UPDATE` (session 8) — but then new rows do not get today's date automatically, so only the rebuild meets the request fully.
6. Not possible: SQLite's ALTER TABLE cannot change a data type (`ALTER COLUMN … TYPE` gives a syntax error). Rebuild the table (Part B). Other DBMS, e.g. PostgreSQL, have `ALTER TABLE … ALTER COLUMN … TYPE`.

Part B (tested on the original table; mileage then shows as 18250.0, real):

```sql
CREATE TABLE new_vehicle (
    licence_plate  TEXT NOT NULL PRIMARY KEY,
    model          TEXT NOT NULL,
    location       TEXT,
    mileage        REAL CHECK (mileage >= 0)
);
INSERT INTO new_vehicle SELECT licence_plate, model, location, mileage FROM vehicle;
DROP TABLE vehicle;
ALTER TABLE new_vehicle RENAME TO vehicle;
```

Full marks also for a rebuild that includes the changes from Part A. If other tables refer to vehicle, foreign keys should be switched off during the rebuild and checked afterwards with `PRAGMA foreign_key_check` (SQLite, n.d.-a). In a project at this stage, editing the schema script and rebuilding the whole database is often simpler.
:::

## Exam-Style Task: The Sports Club in SQL

This task is in the style of an exam question. Implement the normalised schema of the sports club from worksheets 5 and 6 in SQLite:

- MEMBER(**member_no**, name, date_of_birth, joining_date, member_type, *mentor_no* → MEMBER)
- YOUTH_MEMBER(**member_no**, parent_phone), *member_no* → MEMBER
- DEPARTMENT(**dept_name**, monthly_fee, *head_no* → MEMBER)
- MEMBERSHIP(**member_no, dept_name**, joined_on), *member_no* → MEMBER, *dept_name* → DEPARTMENT
- TEAM(**dept_name, team_no**, *coach_no* → MEMBER), *dept_name* → DEPARTMENT

Business rules:

- member_type is either 'adult' or 'youth'; nobody mentors themselves; parent_phone is mandatory for youth members.
- If no date is given, joining_date and joined_on are today's date. The monthly fee is positive; team numbers are positive whole numbers. Every team has exactly one coach.
- When a member is deleted, their memberships and youth member data are deleted too; their mentees keep their membership but have no mentor; a department they head has no head until a new one is chosen. A member who still coaches a team cannot be deleted.
- When a department is closed, its teams and memberships are deleted.
- A member coaches at most two teams.

1. Write the `CREATE TABLE` statements for all five tables in a valid order, with suitable data types and all constraints that can be expressed in `CREATE TABLE`. (7 points)
2. Name **two** business rules that your statements cannot enforce. How could they be enforced? (2 points)
3. A colleague runs your script in a new notebook and is surprised that a team with coach 'M-99', who does not exist, is accepted. Explain the cause and the fix. (1 point)

::: answer lines=24
:::

::: solution
1. Model answer (tested in SQLite; all rules were checked with test rows):

```sql
CREATE TABLE member (
    member_no      TEXT NOT NULL PRIMARY KEY,
    name           TEXT NOT NULL,
    date_of_birth  TEXT NOT NULL,
    joining_date   TEXT NOT NULL DEFAULT CURRENT_DATE,
    member_type    TEXT NOT NULL CHECK (member_type IN ('adult', 'youth')),
    mentor_no      TEXT REFERENCES member (member_no) ON DELETE SET NULL,
    CHECK (mentor_no <> member_no)
);
CREATE TABLE youth_member (
    member_no     TEXT NOT NULL PRIMARY KEY
                  REFERENCES member (member_no) ON DELETE CASCADE,
    parent_phone  TEXT NOT NULL
);
CREATE TABLE department (
    dept_name    TEXT    NOT NULL PRIMARY KEY,
    monthly_fee  NUMERIC NOT NULL CHECK (monthly_fee > 0),
    head_no      TEXT    REFERENCES member (member_no) ON DELETE SET NULL
);
CREATE TABLE membership (
    member_no  TEXT NOT NULL
               REFERENCES member (member_no) ON DELETE CASCADE,
    dept_name  TEXT NOT NULL
               REFERENCES department (dept_name) ON DELETE CASCADE,
    joined_on  TEXT NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (member_no, dept_name)
);
CREATE TABLE team (
    dept_name  TEXT    NOT NULL
               REFERENCES department (dept_name) ON DELETE CASCADE,
    team_no    INTEGER NOT NULL CHECK (team_no > 0),
    coach_no   TEXT    NOT NULL
               REFERENCES member (member_no) ON DELETE RESTRICT,
    PRIMARY KEY (dept_name, team_no)
);
```

Marking guide (10 points; the first six lines are part 1):

- member: key NOT NULL, CHECK on member_type, DEFAULT for joining_date: 1 point; recursive foreign key mentor_no with ON DELETE SET NULL and the CHECK against self-mentoring: 1 point
- youth_member: primary key that is also a foreign key, ON DELETE CASCADE, parent_phone NOT NULL: 1 point
- department: CHECK on the fee, head_no nullable with ON DELETE SET NULL: 1 point
- membership: composite primary key as table constraint, both foreign keys with CASCADE, DEFAULT for joined_on: 1 point
- team: composite primary key, CHECK on team_no, coach_no NOT NULL with ON DELETE RESTRICT (no action clause is also accepted): 1 point
- Valid order (member before the tables that refer to it) and sensible data types (dates as TEXT, fee as NUMERIC, no INTEGER for codes with letters): 1 point
- Deduct nothing for a missing date format CHECK; give no point for a table whose primary key is missing.

2. Any two (1 point each, half a point without a way to enforce it):
  - **At most two teams per coach**: a CHECK only sees one row (tested: a third team with the same coach was accepted). Enforce with a trigger or in the application before inserting.
  - **Youth member data only for members of type 'youth'** (and every youth member has a row in youth_member): this involves two tables. Enforce with a trigger or application logic, or change the mapping (pure option C: parent_phone in member with `CHECK (member_type = 'youth' OR parent_phone IS NULL)`).
  - Also accept: joined_on not before the member's joining_date (two tables).
3. SQLite checks foreign keys only after `PRAGMA foreign_keys = ON`, and the setting is per connection and lost in every new connection. Fix: run `con.execute("PRAGMA foreign_keys = ON")` directly after connecting, before any other statement; check existing data with `PRAGMA foreign_key_check`. (1 point)

Common mistakes: PRIMARY KEY written after both columns of a composite key instead of as a table constraint; `CHECK (monthly_fee >= 0)` (the fee must be positive); ON DELETE CASCADE from member to team (would delete teams when a coach leaves); forgetting NOT NULL on TEXT key columns.
:::

## References {.references}

- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- SQLite. (n.d.-a). *ALTER TABLE*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_altertable.html
- SQLite. (n.d.-b). *CREATE TABLE*. Retrieved October 20, 2026, from https://www.sqlite.org/lang_createtable.html
- SQLite. (n.d.-c). *Datatypes in SQLite*. Retrieved October 20, 2026, from https://www.sqlite.org/datatype3.html
- SQLite. (n.d.-d). *SQLite foreign key support*. Retrieved October 20, 2026, from https://www.sqlite.org/foreignkeys.html
