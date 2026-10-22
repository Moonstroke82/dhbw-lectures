-- Velo Neckar bike shop: the catalogue of a small data lake (Data Management, session 18)
--
-- The shop has started to keep files in a folder-based data lake with three zones
-- (bronze = raw, as received; silver = cleaned; gold = ready for reports). This
-- script does NOT contain the files themselves, only the catalogue that describes them:
--   lake_file     one row per file in the lake (path, zone, source, format, size,
--                 date received, owner, description, personal data, licence, checksum)
--   lake_lineage  which file was built from which other file (target <- source)
-- All names, sizes and checksums are fictional. The weather files are the real
-- Bright Sky files of session 15 (DWD data, CC BY 4.0).
--
-- It does not depend on the other bike shop tables. Load it into bikeshop.db or
-- into a database of its own:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   with open("bikeshop-lake-catalog-session18.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- Running this script again deletes and rebuilds both tables.
-- Row counts afterwards: lake_file 24, lake_lineage 14.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS lake_lineage;
DROP TABLE IF EXISTS lake_file;

CREATE TABLE lake_file (
    file_id        INTEGER PRIMARY KEY,
    path           TEXT    NOT NULL UNIQUE,
    zone           TEXT    NOT NULL CHECK (zone IN ('bronze', 'silver', 'gold')),
    source         TEXT    NOT NULL,                    -- system or person it came from
    format         TEXT    NOT NULL,                    -- json, csv, xlsx, jpg, pdf, parquet ...
    size_kb        INTEGER NOT NULL CHECK (size_kb > 0),
    received_on    TEXT    NOT NULL CHECK (received_on IS date(received_on)),
    owner          TEXT,                                -- who is responsible (NULL = nobody known)
    description    TEXT,                                -- what is in it (NULL = not documented)
    personal_data  TEXT    NOT NULL CHECK (personal_data IN ('yes', 'no', 'unknown')),
    licence        TEXT,                                -- terms of use, if any
    checksum       TEXT    NOT NULL                     -- shortened content hash
);

CREATE TABLE lake_lineage (
    target_id  INTEGER NOT NULL REFERENCES lake_file (file_id),
    source_id  INTEGER NOT NULL REFERENCES lake_file (file_id),
    PRIMARY KEY (target_id, source_id)
);

INSERT INTO lake_file VALUES
-- bronze: raw files, exactly as they arrived
( 1, 'bronze/brightsky/mannheim/2026-10-05.json',       'bronze', 'Bright Sky API', 'json',      36, '2026-10-12', 'Laura Becker', 'hourly weather, station Mannheim, 5-11 Oct 2026', 'no', 'CC BY 4.0', 'a91f03c2'),
( 2, 'bronze/brightsky/heidelberg/2026-09-28.json',     'bronze', 'Bright Sky API', 'json',      61, '2026-10-05', 'Laura Becker', 'hourly weather, station Heidelberg, 28 Sep-4 Oct 2026', 'no', 'CC BY 4.0', '5c2e8d10'),
( 3, 'bronze/suppliers/s1/pricelist-2027.csv',          'bronze', 'supplier S1',    'csv',        1, '2026-10-01', 'Katrin Vogel', 'price list S1, cp1252, semicolon', 'no', 'supplier terms', '0d44b7e9'),
( 4, 'bronze/suppliers/s2/pricelist-2027.xlsx',         'bronze', 'supplier S2',    'xlsx',       6, '2026-10-01', 'Katrin Vogel', 'price list S2, Excel with title rows', 'no', 'supplier terms', '7e1a6f35'),
( 5, 'bronze/till/till-days-2026-10.csv',               'bronze', 'till',           'csv',        1, '2026-10-11', 'Laura Becker', 'daily till figures, 5-10 Oct 2026', 'no', NULL, 'c3b90a47'),
( 6, 'bronze/till/receipts-2026-10.csv',                'bronze', 'till',           'csv',        9, '2026-10-11', 'Laura Becker', 'receipt lines, 5-10 Oct 2026', 'no', NULL, '91d2e6aa'),
( 7, 'bronze/webshop/accounts-export-2026-09.csv',      'bronze', 'web shop',       'csv',        3, '2026-09-30', 'Laura Becker', 'customer accounts export (session 13)', 'yes', NULL, 'e8f4c120'),
( 8, 'bronze/webshop/clickstream/2026-10-05.jsonl',     'bronze', 'web shop',       'jsonl',   5200, '2026-10-06', NULL,           'page views with IP address', 'yes', NULL, '2b7d9e03'),
( 9, 'bronze/webshop/clickstream/2026-10-06.jsonl',     'bronze', 'web shop',       'jsonl',   4900, '2026-10-07', NULL,           NULL, 'yes', NULL, 'f6a0c5d8'),
(10, 'bronze/workshop/photos/2027-02-02_RIE420_01.jpg', 'bronze', 'workshop tablet','jpg',     2400, '2027-02-02', 'Katrin Vogel', 'damage photo, repair job 504', 'unknown', NULL, '4c88e1f7'),
(11, 'bronze/workshop/photos/2027-02-02_RIE420_02.jpg', 'bronze', 'workshop tablet','jpg',     2650, '2027-02-02', 'Katrin Vogel', 'damage photo, repair job 504', 'unknown', NULL, 'b03f7a92'),
(12, 'bronze/workshop/photos/IMG_0412.jpg',             'bronze', 'workshop tablet','jpg',     3100, '2027-02-14', NULL,           NULL, 'unknown', NULL, '6e2d0b5c'),
(13, 'bronze/scans/supplier-invoices/inv-S2-4471.pdf',  'bronze', 'scanner',        'pdf',      180, '2026-10-20', 'Katrin Vogel', 'scanned invoice of supplier S2', 'no', NULL, '8a5c3e61'),
(14, 'bronze/misc/old_stuff.zip',                       'bronze', 'unknown',        'zip',    48000, '2026-10-15', NULL,           NULL, 'unknown', NULL, 'd17b4f08'),
(15, 'bronze/misc/pricelist-2027 (1).csv',              'bronze', 'unknown',        'csv',        1, '2026-10-02', NULL,           NULL, 'unknown', NULL, '0d44b7e9'),
-- silver: cleaned and integrated tables
(16, 'silver/weather_daily.parquet',                    'silver', 'pipeline',       'parquet',    4, '2026-10-12', 'Laura Becker', 'one row per station and day', 'no', 'CC BY 4.0', '3f9e2a71'),
(17, 'silver/supplier_price.parquet',                   'silver', 'pipeline',       'parquet',    3, '2026-10-01', 'Katrin Vogel', 'both price lists in one schema', 'no', 'supplier terms', 'aa04d6c9'),
(18, 'silver/till_daily.parquet',                       'silver', 'pipeline',       'parquet',    2, '2026-10-11', 'Laura Becker', 'daily till figures, typed', 'no', NULL, '5d71b8e2'),
(19, 'silver/sale_line.parquet',                        'silver', 'pipeline',       'parquet',    6, '2026-10-11', 'Laura Becker', 'receipt lines, typed and checked', 'no', NULL, 'c0e93f14'),
(20, 'silver/webshop_accounts.parquet',                 'silver', 'pipeline',       'parquet',    2, '2026-10-01', 'Laura Becker', 'accounts, cleaned (session 14)', 'yes', NULL, '7b26a0dd'),
-- gold: ready for reports and analysis
(21, 'gold/fact_sales.parquet',                         'gold',   'pipeline',       'parquet',    5, '2026-10-12', 'Laura Becker', 'star schema fact table, grain receipt line', 'no', NULL, '19c4e7b0'),
(22, 'gold/dim_product.parquet',                        'gold',   'pipeline',       'parquet',    2, '2026-10-12', 'Laura Becker', 'product dimension', 'no', NULL, 'e5a8d233'),
(23, 'gold/dim_weather_day.parquet',                    'gold',   'pipeline',       'parquet',    1, '2026-10-12', 'Laura Becker', 'weather type per day', 'no', 'CC BY 4.0', '2d0f61c8'),
(24, 'gold/report_revenue_by_weather.csv',              'gold',   'analyst',        'csv',        1, '2026-10-13', 'Laura Becker', 'revenue per product group, good and bad bike days', 'no', NULL, '8f3b5a07');

INSERT INTO lake_lineage (target_id, source_id) VALUES
(16, 1),
(17, 3), (17, 4),
(18, 5),
(19, 6),
(20, 7),
(21, 19), (21, 23),
(22, 17), (22, 19),
(23, 16),
(24, 21), (24, 22), (24, 23);
