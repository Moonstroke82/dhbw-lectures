-- Velo Neckar bike shop: purchase orders to suppliers (Data Management, worksheet 12)
--
-- Fills the tables supplier, purchase_order and purchase_line that you create in
-- worksheet 12, task 4. This script contains only INSERT statements: it loads
-- without error only if your tables have the column names and order used below
-- and allow these rows. All company names are fictional.
--
-- Run the bike shop scripts first, then your CREATE TABLE statements, then this script:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--   con.executescript(my_create_table_statements)      # your solution of task 4
--   with open("bikeshop-purchasing-session12.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- Row counts afterwards: supplier 4, purchase_order 5, purchase_line 10.

PRAGMA foreign_keys = ON;

-- SUPPLIER(supplier_no, name, city); supplier S4 has not received an order yet
INSERT INTO supplier (supplier_no, name, city) VALUES
    ('S1', 'Rad-Großhandel Süd',  'Stuttgart'),
    ('S2', 'E-Motion Parts',      'Köln'),
    ('S3', 'Kette & Co',          'Mannheim'),
    ('S4', 'Licht & Klingel',     'Heidelberg');

-- PURCHASE_ORDER(order_no, order_date, supplier_no -> SUPPLIER)
INSERT INTO purchase_order (order_no, order_date, supplier_no) VALUES
    (701, '2027-01-08', 'S1'),
    (702, '2027-01-15', 'S2'),
    (703, '2027-02-03', 'S1'),
    (704, '2027-02-20', 'S3'),
    (705, '2027-03-05', 'S1');

-- PURCHASE_LINE(order_no -> PURCHASE_ORDER, part_no -> SPARE_PART, quantity, unit_cost)
-- unit_cost is the price Velo Neckar paid per unit in this order (history).
INSERT INTO purchase_line (order_no, part_no, quantity, unit_cost) VALUES
    (701, 'P-101', 20,   3.10),
    (701, 'P-103', 10,   5.80),
    (702, 'P-109',  2, 455.00),
    (703, 'P-101', 30,   2.95),
    (703, 'P-106', 25,   1.60),
    (703, 'P-107', 25,   1.60),
    (704, 'P-104',  5,  12.40),
    (704, 'P-105',  5,  21.00),
    (705, 'P-103', 10,   6.10),
    (705, 'P-108',  3,  31.50);
