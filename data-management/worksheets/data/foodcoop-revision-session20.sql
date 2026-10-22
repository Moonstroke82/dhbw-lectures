-- Food co-op: a small order database for the revision worksheet (Data Management, session 20)
--
-- Practice material only. All names, villages and figures are fictional.
-- The food co-op collects its members' weekly orders, buys from regional producers
-- and hands out the goods on a pick-up day (Fridays).
--
--   PRODUCER(producer_no, name, village)
--   PRODUCT(product_no, name, unit, price, producer_no -> PRODUCER)      price = current price
--   MEMBER(member_no, name, e_mail, member_type)
--   PICKUP_ORDER(order_no, member_no -> MEMBER, pickup_date)              one order per member and day
--   ORDER_LINE(order_no -> PICKUP_ORDER, product_no -> PRODUCT, quantity, price_paid)
--
-- Run it in a new, empty database (it drops and recreates its own tables):
--
--   import sqlite3
--   con = sqlite3.connect("foodcoop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   with open("foodcoop-revision-session20.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- or with the SQLite command-line tool:  sqlite3 foodcoop.db < foodcoop-revision-session20.sql
--
-- Row counts afterwards: producer 5, product 11, member 7, pickup_order 10, order_line 24.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_line;
DROP TABLE IF EXISTS pickup_order;
DROP TABLE IF EXISTS member;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS producer;

CREATE TABLE producer (
    producer_no  TEXT NOT NULL PRIMARY KEY,
    name         TEXT NOT NULL,
    village      TEXT
);

CREATE TABLE product (
    product_no   TEXT    NOT NULL PRIMARY KEY,
    name         TEXT    NOT NULL,
    unit         TEXT    NOT NULL,
    price        NUMERIC NOT NULL CHECK (price >= 0),          -- current price
    producer_no  TEXT    NOT NULL REFERENCES producer (producer_no) ON DELETE RESTRICT
);

CREATE TABLE member (
    member_no    TEXT NOT NULL PRIMARY KEY,
    name         TEXT NOT NULL,
    e_mail       TEXT UNIQUE,
    member_type  TEXT NOT NULL CHECK (member_type IN ('regular', 'working'))
);

CREATE TABLE pickup_order (
    order_no     INTEGER PRIMARY KEY,
    member_no    TEXT    NOT NULL REFERENCES member (member_no) ON DELETE RESTRICT,
    pickup_date  TEXT    NOT NULL CHECK (pickup_date IS date(pickup_date)),
    UNIQUE (member_no, pickup_date)                             -- one order per member and pick-up day
);

CREATE TABLE order_line (
    order_no     INTEGER NOT NULL REFERENCES pickup_order (order_no) ON DELETE CASCADE,
    product_no   TEXT    NOT NULL REFERENCES product (product_no) ON DELETE RESTRICT,
    quantity     INTEGER NOT NULL CHECK (quantity > 0),
    price_paid   NUMERIC NOT NULL CHECK (price_paid >= 0),     -- history: the price on the pick-up day
    PRIMARY KEY (order_no, product_no)
);

-- 5 producers; H5 has just joined and has no products yet
INSERT INTO producer (producer_no, name, village) VALUES
    ('H1', 'Hofgut Sonnenberg',        'Schriesheim'),
    ('H2', 'Imkerei Weber',            'Ladenburg'),
    ('H3', 'Käserei am Odenwald',      'Wilhelmsfeld'),
    ('H4', 'Mühle Neckartal',          'Neckargemünd'),
    ('H5', 'Obsthof Kraus',            'Weinheim');

-- 11 products; carrots cost 2.10 until 8 October 2027, 2.20 since then
INSERT INTO product (product_no, name, unit, price, producer_no) VALUES
    ('V01', 'Potatoes',            'kg',           2.40, 'H1'),
    ('V02', 'Carrots',             'kg',           2.20, 'H1'),
    ('V03', 'Hokkaido pumpkin',    'piece',        3.50, 'H1'),
    ('V04', 'Kale',                'bunch',        2.90, 'H1'),
    ('H01', 'Flower honey',        'jar 500 g',    7.80, 'H2'),
    ('H02', 'Forest honey',        'jar 500 g',    8.90, 'H2'),
    ('C01', 'Mountain cheese',     'piece 250 g',  5.60, 'H3'),
    ('C02', 'Fresh goat cheese',   'piece 150 g',  3.90, 'H3'),
    ('C03', 'Soft cheese',         'piece 200 g',  4.50, 'H3'),
    ('F01', 'Spelt flour',         'bag 1 kg',     3.20, 'H4'),
    ('F02', 'Rye flour',           'bag 1 kg',     2.80, 'H4');

-- 7 members; Nora Schmitt has not ordered yet
INSERT INTO member (member_no, name, e_mail, member_type) VALUES
    ('M01', 'Johanna Keller',  'j.keller@example.org',   'working'),
    ('M02', 'Ömer Aydın',      'oemer.aydin@example.com', 'regular'),
    ('M03', 'Lisa Brandt',     'lisa.b@example.net',     'working'),
    ('M04', 'Daniel Roth',     NULL,                     'regular'),
    ('M05', 'Mia Hoffmann',    'mia.h@example.org',      'regular'),
    ('M06', 'Karl Weiß',       'karl.weiss@example.com', 'working'),
    ('M07', 'Nora Schmitt',    'nora.s@example.net',     'regular');

-- 10 orders on two pick-up days; order 10 was opened but has no lines (yet)
INSERT INTO pickup_order (order_no, member_no, pickup_date) VALUES
    (1,  'M01', '2027-10-08'),
    (2,  'M02', '2027-10-08'),
    (3,  'M03', '2027-10-08'),
    (4,  'M04', '2027-10-08'),
    (5,  'M05', '2027-10-08'),
    (6,  'M01', '2027-10-15'),
    (7,  'M02', '2027-10-15'),
    (8,  'M03', '2027-10-15'),
    (9,  'M06', '2027-10-15'),
    (10, 'M05', '2027-10-15');

INSERT INTO order_line (order_no, product_no, quantity, price_paid) VALUES
    (1, 'V01', 3, 2.40), (1, 'V04', 1, 2.90), (1, 'C01', 1, 5.60),
    (2, 'H01', 2, 7.80), (2, 'F01', 1, 3.20),
    (3, 'V02', 2, 2.10), (3, 'V03', 1, 3.50), (3, 'F02', 2, 2.80),
    (4, 'C02', 2, 3.90),
    (5, 'V01', 2, 2.40), (5, 'H02', 1, 8.90),
    (6, 'V01', 2, 2.40), (6, 'C01', 1, 5.60), (6, 'F01', 1, 3.20),
    (7, 'V03', 2, 3.50), (7, 'V02', 1, 2.20),
    (8, 'V02', 1, 2.20), (8, 'H01', 1, 7.80), (8, 'C02', 1, 3.90),
    (9, 'V04', 2, 2.90), (9, 'C02', 1, 3.90), (9, 'F02', 1, 2.80), (9, 'H02', 1, 8.90), (9, 'V01', 4, 2.40);
