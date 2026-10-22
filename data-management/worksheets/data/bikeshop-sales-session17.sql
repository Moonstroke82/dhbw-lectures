-- Velo Neckar bike shop: till sales of one week (Data Management, session 17)
--
-- The operational (OLTP) side of the till: products, receipts (sale) and receipt
-- lines (sale_line) for Monday 5 to Saturday 10 October 2026, normalised as in
-- sessions 5-7. The daily totals match the till export of session 16
-- (bikeshop-till-days-session16.csv, column Umsatz). All data is fictional.
--
-- It also adds the daily weather of 5-11 October 2026 to weather_daily for everyone
-- who did not finish the session 16 pipeline (INSERT OR IGNORE: rows loaded by
-- your own pipeline are kept). Weather data: Deutscher Wetterdienst via Bright Sky,
-- CC BY 4.0 (values as computed in sessions 15 and 16).
--
-- Run it after the bike shop scripts and the session 16 script:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql", "bikeshop-etl-session16.sql",
--                  "bikeshop-sales-session17.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- Running this script again deletes and rebuilds product, sale and sale_line.
-- Row counts afterwards: product 18, sale 35, sale_line 54, weather_daily at least 7.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS sale_line;
DROP TABLE IF EXISTS sale;
DROP TABLE IF EXISTS product;

-- PRODUCT(product_no, name, product_group, list_price, part_no -> SPARE_PART)
CREATE TABLE product (
    product_no     TEXT    NOT NULL PRIMARY KEY,
    name           TEXT    NOT NULL,
    product_group  TEXT    NOT NULL
                           CHECK (product_group IN ('E-bikes', 'Bikes', 'Parts',
                                                    'Accessories', 'Service')),
    list_price     NUMERIC NOT NULL CHECK (list_price >= 0),
    part_no        TEXT    REFERENCES spare_part (part_no)   -- only for spare parts
);

-- SALE(receipt_no, sale_date, sale_time, employee_no -> SALESPERSON): one receipt
CREATE TABLE sale (
    receipt_no   INTEGER PRIMARY KEY,
    sale_date    TEXT    NOT NULL CHECK (sale_date IS date(sale_date)),
    sale_time    TEXT    NOT NULL,
    employee_no  INTEGER NOT NULL REFERENCES salesperson (employee_no)
);

-- SALE_LINE(receipt_no -> SALE, line_no, product_no -> PRODUCT, quantity, unit_price)
CREATE TABLE sale_line (
    receipt_no  INTEGER NOT NULL REFERENCES sale (receipt_no) ON DELETE CASCADE,
    line_no     INTEGER NOT NULL,
    product_no  TEXT    NOT NULL REFERENCES product (product_no),
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC NOT NULL CHECK (unit_price >= 0),   -- price charged, history
    PRIMARY KEY (receipt_no, line_no)
);

-- 18 products; A-06 (child seat) and P-112 (mudguard set) have not been sold this week
INSERT INTO product (product_no, name, product_group, list_price, part_no) VALUES
    ('E-01',  'Gazelle Ultimate',      'E-bikes',     2499.00, NULL),
    ('E-02',  'KTM Macina Style',      'E-bikes',     3599.00, NULL),
    ('B-01',  'Trek Marlin 7',         'Bikes',       1099.00, NULL),
    ('B-02',  'Cube Touring',          'Bikes',        899.00, NULL),
    ('B-03',  'Cube Kid 200',          'Bikes',        299.00, NULL),
    ('P-101', 'Inner tube 28 inch',    'Parts',          6.90, 'P-101'),
    ('P-102', 'Tyre 28 x 1.5',         'Parts',         34.90, 'P-102'),
    ('P-103', 'Brake pads (pair)',     'Parts',         12.50, 'P-103'),
    ('P-110', 'Bell',                  'Parts',          8.90, 'P-110'),
    ('P-111', 'LED front light',       'Parts',         29.90, 'P-111'),
    ('P-112', 'Mudguard set',          'Parts',         24.90, 'P-112'),
    ('A-01',  'Helmet Urban',          'Accessories',   79.90, NULL),
    ('A-02',  'Folding lock',          'Accessories',   59.90, NULL),
    ('A-03',  'Pannier bag',           'Accessories',   49.90, NULL),
    ('A-04',  'Rain cape',             'Accessories',   39.90, NULL),
    ('A-05',  'Cycling gloves',        'Accessories',   19.90, NULL),
    ('A-06',  'Child seat',            'Accessories',  119.00, NULL),
    ('S-01',  'Bike fitting',          'Service',       49.00, NULL);

-- 35 receipts; salespeople 5 (Marco Esposito) and 6 (Laura Becker); closed on Sundays
INSERT INTO sale (receipt_no, sale_date, sale_time, employee_no) VALUES
    (1001, '2026-10-05', '10:12', 5), (1002, '2026-10-05', '11:40', 6),
    (1003, '2026-10-05', '14:05', 5), (1004, '2026-10-05', '16:30', 6),
    (1005, '2026-10-05', '17:55', 5),
    (1006, '2026-10-06', '09:48', 5), (1007, '2026-10-06', '10:31', 6),
    (1008, '2026-10-06', '12:15', 6), (1009, '2026-10-06', '13:50', 5),
    (1010, '2026-10-06', '15:20', 6), (1011, '2026-10-06', '16:45', 5),
    (1012, '2026-10-06', '18:10', 6),
    (1013, '2026-10-07', '10:05', 5), (1014, '2026-10-07', '11:22', 6),
    (1015, '2026-10-07', '12:40', 5), (1016, '2026-10-07', '14:18', 6),
    (1017, '2026-10-07', '15:33', 5), (1018, '2026-10-07', '16:50', 6),
    (1019, '2026-10-07', '18:02', 5),
    (1020, '2026-10-08', '11:15', 6), (1021, '2026-10-08', '13:40', 5),
    (1022, '2026-10-08', '15:05', 6), (1023, '2026-10-08', '17:30', 5),
    (1024, '2026-10-09', '10:20', 5), (1025, '2026-10-09', '12:45', 6),
    (1026, '2026-10-09', '14:10', 6), (1027, '2026-10-09', '16:00', 5),
    (1028, '2026-10-09', '17:25', 6),
    (1029, '2026-10-10', '09:35', 5), (1030, '2026-10-10', '10:50', 6),
    (1031, '2026-10-10', '11:30', 5), (1032, '2026-10-10', '12:05', 6),
    (1033, '2026-10-10', '13:20', 5), (1034, '2026-10-10', '14:40', 6),
    (1035, '2026-10-10', '15:55', 5);

-- 54 receipt lines; unit_price = price charged on the day (here the list price)
INSERT INTO sale_line (receipt_no, line_no, product_no, quantity, unit_price) VALUES
    (1001, 1, 'E-01',  1, 2499.00), (1001, 2, 'S-01',  1,   49.00),
    (1002, 1, 'A-03',  2,   49.90),
    (1003, 1, 'A-04',  1,   39.90), (1003, 2, 'A-05',  1,   19.90),
    (1004, 1, 'S-01',  1,   49.00),
    (1005, 1, 'S-01',  1,   49.00), (1005, 2, 'P-102', 1,   34.90),
    (1006, 1, 'E-01',  1, 2499.00), (1006, 2, 'A-01',  1,   79.90),
    (1006, 3, 'A-02',  1,   59.90), (1006, 4, 'S-01',  1,   49.00),
    (1007, 1, 'A-04',  2,   39.90),
    (1008, 1, 'A-02',  1,   59.90), (1008, 2, 'A-05',  1,   19.90),
    (1009, 1, 'S-01',  1,   49.00),
    (1010, 1, 'A-03',  2,   49.90),
    (1011, 1, 'A-03',  1,   49.90), (1011, 2, 'P-111', 1,   29.90),
    (1012, 1, 'S-01',  1,   49.00),
    (1013, 1, 'E-02',  1, 3599.00), (1013, 2, 'A-01',  1,   79.90),
    (1014, 1, 'B-03',  1,  299.00), (1014, 2, 'A-01',  1,   79.90),
    (1014, 3, 'P-110', 1,    8.90),
    (1015, 1, 'P-111', 2,   29.90),
    (1016, 1, 'P-102', 2,   34.90),
    (1017, 1, 'A-04',  1,   39.90), (1017, 2, 'A-03',  1,   49.90),
    (1018, 1, 'P-103', 2,   12.50),
    (1019, 1, 'A-03',  2,   49.90),
    (1020, 1, 'B-02',  1,  899.00),
    (1021, 1, 'P-101', 2,    6.90),
    (1022, 1, 'P-110', 2,    8.90), (1022, 2, 'A-05',  1,   19.90),
    (1023, 1, 'P-111', 1,   29.90),
    (1024, 1, 'B-01',  1, 1099.00), (1024, 2, 'A-02',  1,   59.90),
    (1024, 3, 'A-01',  1,   79.90),
    (1025, 1, 'P-102', 1,   34.90), (1025, 2, 'P-101', 1,    6.90),
    (1026, 1, 'A-03',  2,   49.90),
    (1027, 1, 'P-111', 1,   29.90),
    (1028, 1, 'A-04',  3,   39.90),
    (1029, 1, 'E-02',  1, 3599.00),
    (1030, 1, 'B-01',  1, 1099.00), (1030, 2, 'A-01',  1,   79.90),
    (1031, 1, 'B-02',  1,  899.00), (1031, 2, 'P-110', 1,    8.90),
    (1032, 1, 'A-04',  2,   39.90),
    (1033, 1, 'P-102', 2,   34.90),
    (1034, 1, 'P-102', 1,   34.90), (1034, 2, 'A-03',  1,   49.90),
    (1035, 1, 'P-111', 2,   29.90);

-- Daily weather in Mannheim, 5-11 October 2026 (as loaded by the session 16 pipeline)
INSERT OR IGNORE INTO weather_daily
    (station, day, rain_mm, wet_hours, t_max, sunshine_h, records, run_id) VALUES
    ('Mannheim', '2026-10-05',  0.0,  0, 23.8, 10.7, 24, NULL),
    ('Mannheim', '2026-10-06',  0.0,  0, 24.3, 10.6, 24, NULL),
    ('Mannheim', '2026-10-07',  0.0,  0, 24.0,  9.4, 24, NULL),
    ('Mannheim', '2026-10-08', 11.9, 10, 18.0,  0.4, 24, NULL),
    ('Mannheim', '2026-10-09',  0.9,  2, 12.6,  0.6, 24, NULL),
    ('Mannheim', '2026-10-10',  1.6,  5, 17.8,  6.0, 24, NULL),
    ('Mannheim', '2026-10-11',  0.2,  2, 15.5,  4.0, 24, NULL);
