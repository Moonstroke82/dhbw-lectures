-- Velo Neckar bike shop: sample data (Data Management, session 8)
--
-- Fills the empty tables created by bikeshop-schema.sql (session 7).
-- All names, addresses and e-mail addresses are fictional.
-- Run the schema script first, then this script:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- or with the SQLite command-line tool:
--   sqlite3 bikeshop.db < bikeshop-schema.sql
--   sqlite3 bikeshop.db < bikeshop-data.sql
--
-- Rows are inserted in an order that respects the foreign keys:
-- referenced tables (customer, spare_part, employee) first.
-- Running the data script twice fails with "UNIQUE constraint failed":
-- run the schema script again to start from empty tables.

PRAGMA foreign_keys = ON;

-- 12 customers; some have no e-mail address or an incomplete address (NULL)
INSERT INTO customer (customer_no, name, e_mail, street, postcode, city) VALUES
    (101, 'Anna Berger',     'anna.berger@example.org',   'Lange Rötterstraße 12',     '68167', 'Mannheim'),
    (102, 'Jonas Albrecht',  'j.albrecht@example.com',    'Hauptstraße 88',            '69117', 'Heidelberg'),
    (103, 'Mira Okonkwo',    NULL,                        'Bergheimer Straße 5',       '69115', 'Heidelberg'),
    (104, 'Lukas Brandt',    'lukas.brandt@example.net',  'Weinheimer Straße 21',      '68526', 'Ladenburg'),
    (105, 'Selin Kaya',      'selin.kaya@example.org',    'Karl-Theodor-Straße 9',     '68723', 'Schwetzingen'),
    (106, 'Felix Wagner',    NULL,                        NULL,                        NULL,    NULL),
    (107, 'Hannah Schulz',   'hannah.schulz@example.com', 'Neckarauer Straße 140',     '68163', 'Mannheim'),
    (108, 'Paul Richter',    'p.richter@example.org',     'Rohrbacher Straße 61',      '69115', 'Heidelberg'),
    (109, 'Elif Demir',      'elif.demir@example.net',    NULL,                        '69469', 'Weinheim'),
    (110, 'Tobias Krämer',   NULL,                        'Seckenheimer Straße 30',    '68165', 'Mannheim'),
    (111, 'Clara Neumann',   'clara.neumann@example.com', 'Dossenheimer Landstraße 7', '69121', 'Heidelberg'),
    (112, 'Noah Fischer',    'noah.f@example.org',        'Hauptstraße 5',             '68526', 'Ladenburg');

-- 15 bikes; customer_no NULL = still in stock; price NULL = bought elsewhere, price unknown
INSERT INTO bike (frame_no, brand, model, price, customer_no) VALUES
    ('WAX123', 'Cube',           'Kathmandu',     1899, 101),
    ('GZT884', 'Gazelle',        'Ultimate',      2499, NULL),
    ('CUB201', 'Cube',           'Touring',        899, 102),
    ('CUB202', 'Cube',           'Stereo Hybrid', 3299, 107),
    ('TRK310', 'Trek',           'FX 3',           949, 103),
    ('TRK311', 'Trek',           'Marlin 7',      1099, NULL),
    ('RIE420', 'Riese & Müller', 'Charger4',      5899, 111),
    ('GZT885', 'Gazelle',        'Medeo T9',      2799, 104),
    ('KTM530', 'KTM',            'Macina Style',  3599, NULL),
    ('SCO640', 'Scott',          'Addict 30',     NULL, 108),
    ('CAN750', 'Canyon',         'Grail 6',       NULL, 105),
    ('TRK312', 'Trek',           'Domane AL 2',    999, 110),
    ('CUB203', 'Cube',           'Kid 200',        299, 112),
    ('BRO860', 'Brompton',       'C Line',        1749, 109),
    ('GZT886', 'Gazelle',        'Ultimate',      2499, NULL);

-- 11 spare parts
INSERT INTO spare_part (part_no, name, list_price) VALUES
    ('P-101', 'Inner tube 28 inch',   6.90),
    ('P-102', 'Tyre 28 x 1.5',       34.90),
    ('P-103', 'Brake pads (pair)',   12.50),
    ('P-104', 'Chain 9-speed',       24.90),
    ('P-105', 'Chain 11-speed',      39.90),
    ('P-106', 'Brake cable',          4.50),
    ('P-107', 'Gear cable',           4.50),
    ('P-108', 'Cassette 11-speed',   59.00),
    ('P-109', 'E-bike battery 500 Wh', 649.00),
    ('P-110', 'Bell',                 8.90),
    ('P-111', 'LED front light',     29.90);

-- 7 employees: 4 mechanics, 2 salespeople, 1 in neither subclass (bookkeeping)
INSERT INTO employee (employee_no, name) VALUES
    (1, 'Katrin Vogel'),
    (2, 'Deniz Arslan'),
    (3, 'Jan Hoffmann'),
    (4, 'Sophie Lindner'),
    (5, 'Marco Esposito'),
    (6, 'Laura Becker'),
    (7, 'Ben Weber');

-- The supervisor (1) is inserted before the mechanics she supervises.
INSERT INTO mechanic (employee_no, qualification, supervisor_no) VALUES
    (1, 'master',            NULL),
    (2, 'journeyman',        1),
    (3, 'apprentice',        1),
    (4, 'e-bike technician', 1);

INSERT INTO salesperson (employee_no, sales_target) VALUES
    (5, 250000),
    (6, NULL);

-- 12 repair jobs in 2027; jobs 506 and 512 have no description yet
INSERT INTO repair_job (job_no, job_date, description, frame_no) VALUES
    (501, '2027-01-12', 'Puncture, rear wheel',      'WAX123'),
    (502, '2027-01-19', 'Annual service',            'CUB201'),
    (503, '2027-02-02', 'Brakes squeal',             'TRK310'),
    (504, '2027-02-02', 'Annual service',            'RIE420'),
    (505, '2027-02-16', 'Gears skip, replace chain', 'CUB202'),
    (506, '2027-03-01', NULL,                        'SCO640'),
    (507, '2027-03-03', 'Battery does not charge',   'KTM530'),
    (508, '2027-03-10', 'Annual service',            'GZT885'),
    (509, '2027-03-15', 'Front light broken',        'BRO860'),
    (510, '2027-03-22', 'Puncture, front wheel',     'CAN750'),
    (511, '2027-04-06', 'Chain and cassette worn',   'TRK312'),
    (512, '2027-04-07', NULL,                        'WAX123');

-- 16 repair lines; price_charged is the unit price actually charged (history)
INSERT INTO repair_line (job_no, part_no, quantity, price_charged) VALUES
    (501, 'P-101', 1,   6.90),
    (502, 'P-103', 1,  12.50),
    (502, 'P-106', 2,   4.50),
    (503, 'P-103', 2,  11.00),
    (504, 'P-103', 2,  12.50),
    (504, 'P-107', 1,   4.50),
    (505, 'P-104', 1,  24.90),
    (507, 'P-109', 1, 649.00),
    (508, 'P-103', 1,  12.50),
    (508, 'P-110', 1,   0),
    (509, 'P-111', 1,  29.90),
    (510, 'P-101', 1,   6.90),
    (510, 'P-102', 1,  34.90),
    (511, 'P-105', 1,  39.90),
    (511, 'P-108', 1,  59.00),
    (511, 'P-106', 1,   4.50);

-- 14 assignments of mechanics to repair jobs (M:N); job 512 is not assigned yet
INSERT INTO job_mechanic (job_no, employee_no) VALUES
    (501, 2), (502, 3), (502, 1), (503, 2), (504, 4), (504, 1), (505, 2),
    (506, 3), (507, 4), (508, 3), (509, 2), (510, 3), (511, 2), (511, 1);
