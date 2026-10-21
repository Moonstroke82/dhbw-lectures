-- Velo Neckar bike shop: data for the data quality assessment (Data Management, session 13)
--
-- Adds three tables to the bike shop database:
--   webshop_customer  the customer export of the new web shop (20 accounts), loaded as it
--                     arrived: all columns TEXT, no constraints (a "staging" table)
--   postcode_ref      a reference list of the postcodes in the shop's area
--   stock_count       the physical stock count of 2027-04-30 (frame numbers found in the shop)
-- All names, addresses and e-mail addresses are fictional. The errors in the export are
-- intended: today's task is to find and measure them, not to fix them (session 14).
--
-- Run the three bike shop scripts first, then this script:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql", "bikeshop-dq-session13.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- Running this script again deletes and rebuilds the three tables.
-- Row counts afterwards: webshop_customer 20, postcode_ref 12, stock_count 4.

DROP TABLE IF EXISTS webshop_customer;
DROP TABLE IF EXISTS postcode_ref;
DROP TABLE IF EXISTS stock_count;

-- Export of 2027-05-03. customer_no is the customer number in the shop's till system,
-- entered by the staff when a web shop customer also buys in the shop (NULL = not linked).
CREATE TABLE webshop_customer (
    account_id    TEXT,
    name          TEXT,
    e_mail        TEXT,
    postcode      TEXT,
    city          TEXT,
    birth_date    TEXT,
    newsletter    TEXT,
    last_changed  TEXT,
    customer_no   TEXT
);

INSERT INTO webshop_customer VALUES
    ('W01', 'Anna Berger',    'anna.berger@example.org',   '68167',   'Mannheim',     '1988-04-12', 'yes', '2027-01-12', '101'),
    ('W02', 'Jonas Albrecht', 'j.albrecht@example.com',    '69117',   'Heidelberg',   '1979-11-30', 'no',  '2026-09-02', '102'),
    ('W03', 'anna berger',    'ANNA.BERGER@EXAMPLE.ORG',   '68167',   'Mannheim',     '1988-04-12', 'yes', '2025-03-20', NULL),
    ('W04', 'Lukas Brandt',   'lukas.brandt@example.net',  '68526',   'Ladenburg',    '1995-07-08', 'yes', '2027-02-01', '104'),
    ('W05', 'Selin Kaya',     'selin.kaya(at)example.org', '68723',   'Schwetzingen', '2001-02-14', 'yes', '2026-11-15', '105'),
    ('W06', 'Hannah Schulz',  'hannah.schulz@example.com', '68163',   'MANNHEIM',     '1990-09-21', 'no',  '2025-06-30', '107'),
    ('W07', 'Paul Richter',   'p.richter@example.org',     '69115',   'Heidelberg',   '1986-05-02', 'no',  '2026-08-19', '108'),
    ('W08', 'Elif Demir',     'elif.demir@example.net',    '69469',   'Weinheim',     '12.06.1999', 'yes', '2026-12-01', '109'),
    ('W09', 'Clara Neumann',  'clara.neumann@example.com', '69121',   'Heidelberg',   '1975-03-03', 'yes', '2027-03-15', '111'),
    ('W10', 'Noah Fischer',   'noah.fischer@example.org',  '68526',   'Ladenburg',    '1999-08-19', 'no',  '2027-04-02', '112'),
    ('W11', 'Mia Hofmann',    NULL,                        '6811',    'Mannheim',     '1993-05-17', 'no',  '2026-06-10', NULL),
    ('W12', 'Leon Schäfer',   'leon.schaefer@example.com', '69115',   'Mannheim',     '1998-10-02', 'yes', '2027-01-25', NULL),
    ('W13', 'Emma Wolf',      'emma.wolf@example.net',     NULL,      NULL,           '1900-01-01', NULL,  '2023-02-11', NULL),
    ('W14', 'Ben Koch',       'ben.koch@example.org',      '68165',   'Mannheim',     '2031-04-01', 'yes', '2026-03-03', NULL),
    ('W15', 'Lea Zimmermann', 'lea.z@example.com',         '68159',   'Mannheim',     '1987-12-24', '1',   '2022-08-08', NULL),
    ('W16', 'Tobias Krämer',  NULL,                        '68165',   'Mannheim',     '1983-06-30', 'no',  '2026-10-10', '110'),
    ('W17', 'Jonas Albrecht', 'jonas.albrecht@example.com','69117',   'Heidelberg',   '1979-11-30', 'no',  '2023-04-01', NULL),
    ('W18', 'Finn Bauer',     'finn.bauer@example.net',    '69120',   'Heidelberg',   '2000-01-15', 'Y',   '2026-12-20', '199'),
    ('W19', 'Laura Meyer',    'laura.meyer@example.org',   'D-69117', 'Heidelberg',   '1991-02-29', 'no',  '2026-07-07', NULL),
    ('W20', 'Max Weber',      'max.weber@example.com',     '68167',   'Mannheim',     '1996-08-08', 'no',  '2027-04-28', NULL);

-- Reference data: which postcode belongs to which town (the shop's area only)
CREATE TABLE postcode_ref (
    postcode  TEXT PRIMARY KEY,
    city      TEXT NOT NULL
);

INSERT INTO postcode_ref VALUES
    ('68159', 'Mannheim'), ('68161', 'Mannheim'), ('68163', 'Mannheim'),
    ('68165', 'Mannheim'), ('68167', 'Mannheim'),
    ('69115', 'Heidelberg'), ('69117', 'Heidelberg'), ('69120', 'Heidelberg'),
    ('69121', 'Heidelberg'),
    ('68526', 'Ladenburg'), ('68723', 'Schwetzingen'), ('69469', 'Weinheim');

-- Physical stock count on 2027-04-30: the frame numbers of all bikes found in the shop
CREATE TABLE stock_count (
    frame_no    TEXT PRIMARY KEY,
    counted_on  TEXT NOT NULL,
    counted_by  TEXT NOT NULL
);

INSERT INTO stock_count VALUES
    ('GZT884', '2027-04-30', 'Laura Becker'),
    ('TRK311', '2027-04-30', 'Laura Becker'),
    ('GZT886', '2027-04-30', 'Laura Becker'),
    ('CUB204', '2027-04-30', 'Laura Becker');
