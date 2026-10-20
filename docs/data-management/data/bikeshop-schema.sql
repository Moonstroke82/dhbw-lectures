-- Velo Neckar bike shop: course sample database (Data Management, sessions 5-7)
--
-- The normalised relational schema from sessions 5 and 6, implemented in SQLite.
-- Run it from Jupyter:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   with open("bikeshop-schema.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- or with the SQLite command-line tool:  sqlite3 bikeshop.db < bikeshop-schema.sql
--
-- Running the script again deletes all tables (and their data) and creates them anew.
-- Sample data: bikeshop-data.sql (session 8).

PRAGMA foreign_keys = ON;

-- Drop in reverse order of creation: tables that refer to others go first.
DROP TABLE IF EXISTS job_mechanic;
DROP TABLE IF EXISTS repair_line;
DROP TABLE IF EXISTS repair_job;
DROP TABLE IF EXISTS salesperson;
DROP TABLE IF EXISTS mechanic;
DROP TABLE IF EXISTS employee;
DROP TABLE IF EXISTS spare_part;
DROP TABLE IF EXISTS bike;
DROP TABLE IF EXISTS customer;

-- CUSTOMER(customer_no, name, e_mail, street, postcode, city)
CREATE TABLE customer (
    customer_no  INTEGER PRIMARY KEY,               -- alias for the rowid: numbered automatically
    name         TEXT    NOT NULL,
    e_mail       TEXT    UNIQUE,                    -- optional, but never shared
    street       TEXT,
    postcode     TEXT    CHECK (length(postcode) = 5),
    city         TEXT
);

-- BIKE(frame_no, brand, model, price, customer_no -> CUSTOMER); customer_no may be NULL (bike in stock)
CREATE TABLE bike (
    frame_no     TEXT    NOT NULL PRIMARY KEY,
    brand        TEXT    NOT NULL,
    model        TEXT    NOT NULL,
    price        NUMERIC CHECK (price >= 0),
    customer_no  INTEGER REFERENCES customer (customer_no)
                         ON DELETE SET NULL
);

-- REPAIR_JOB(job_no, job_date, description, frame_no -> BIKE); every job concerns exactly one bike
CREATE TABLE repair_job (
    job_no       INTEGER PRIMARY KEY,
    job_date     TEXT    NOT NULL DEFAULT CURRENT_DATE
                         CHECK (job_date IS date(job_date)),  -- a valid date as YYYY-MM-DD
    description  TEXT,
    frame_no     TEXT    NOT NULL REFERENCES bike (frame_no)
                         ON DELETE RESTRICT                    -- keep the repair history
);

-- SPARE_PART(part_no, name, list_price)
CREATE TABLE spare_part (
    part_no      TEXT    NOT NULL PRIMARY KEY,
    name         TEXT    NOT NULL,
    list_price   NUMERIC NOT NULL CHECK (list_price >= 0)
);

-- REPAIR_LINE(job_no -> REPAIR_JOB, part_no -> SPARE_PART, quantity, price_charged)
CREATE TABLE repair_line (
    job_no         INTEGER NOT NULL REFERENCES repair_job (job_no) ON DELETE CASCADE,
    part_no        TEXT    NOT NULL REFERENCES spare_part (part_no),
    quantity       INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    price_charged  NUMERIC NOT NULL CHECK (price_charged >= 0),   -- history: not the list price
    PRIMARY KEY (job_no, part_no)
);

-- Specialisation, option A: EMPLOYEE with subclasses MECHANIC and SALESPERSON
CREATE TABLE employee (
    employee_no  INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL
);

CREATE TABLE mechanic (
    employee_no    INTEGER PRIMARY KEY REFERENCES employee (employee_no) ON DELETE CASCADE,
    qualification  TEXT,
    supervisor_no  INTEGER REFERENCES mechanic (employee_no) ON DELETE SET NULL,  -- recursive 1:N
    CHECK (supervisor_no <> employee_no)                        -- nobody supervises themselves
);

CREATE TABLE salesperson (
    employee_no   INTEGER PRIMARY KEY REFERENCES employee (employee_no) ON DELETE CASCADE,
    sales_target  NUMERIC CHECK (sales_target >= 0)
);

-- JOB_MECHANIC(job_no -> REPAIR_JOB, employee_no -> MECHANIC): mechanic works on repair job (M:N)
CREATE TABLE job_mechanic (
    job_no       INTEGER NOT NULL REFERENCES repair_job (job_no) ON DELETE CASCADE,
    employee_no  INTEGER NOT NULL REFERENCES mechanic (employee_no),
    PRIMARY KEY (job_no, employee_no)
);
