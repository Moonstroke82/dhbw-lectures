-- Velo Neckar bike shop: target tables for the ETL pipeline (Data Management, session 16)
--
-- Creates the tables that the session 16 pipeline loads into:
--   raw_weather     landing table: one row per API response, the JSON body unchanged (ELT)
--   weather_daily   target table: one row per day and station, loaded by the pipeline
--   supplier_price  target table: the integrated price lists of suppliers S1 and S2
--   etl_run         run log: one row per pipeline run (monitoring)
-- and the supplier table of worksheet 12 if it does not exist yet (with S1 to S4).
--
-- Run it after the bike shop scripts (spare_part must exist):
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql", "bikeshop-etl-session16.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- Running this script again empties the four session 16 tables (not supplier).
-- If you want the purchase orders of worksheet 12 as well, load
-- bikeshop-purchasing-session12.sql BEFORE this script.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS supplier_price;
DROP TABLE IF EXISTS weather_daily;
DROP TABLE IF EXISTS raw_weather;
DROP TABLE IF EXISTS etl_run;

-- SUPPLIER as in worksheet 12, task 4 (kept if it already exists)
CREATE TABLE IF NOT EXISTS supplier (
    supplier_no  TEXT NOT NULL PRIMARY KEY,
    name         TEXT NOT NULL,
    city         TEXT
);
INSERT OR IGNORE INTO supplier (supplier_no, name, city) VALUES
    ('S1', 'Rad-Großhandel Süd',  'Stuttgart'),
    ('S2', 'E-Motion Parts',      'Köln'),
    ('S3', 'Kette & Co',          'Mannheim'),
    ('S4', 'Licht & Klingel',     'Heidelberg');

-- ETL_RUN: what ran when, from which source, with which result
CREATE TABLE etl_run (
    run_id          INTEGER PRIMARY KEY,
    pipeline        TEXT    NOT NULL,                 -- e.g. 'weather', 'prices'
    started_at      TEXT    NOT NULL,                 -- ISO timestamp, local time
    finished_at     TEXT,
    status          TEXT    NOT NULL DEFAULT 'running'
                            CHECK (status IN ('running', 'ok', 'warning', 'failed')),
    source          TEXT,                             -- 'api', 'saved copy', file name
    rows_extracted  INTEGER,
    rows_loaded     INTEGER,
    rows_rejected   INTEGER,
    message         TEXT
);

-- RAW_WEATHER: landing zone for ELT, the response body as it arrived
CREATE TABLE raw_weather (
    retrieved_at  TEXT NOT NULL,                      -- when we called the API
    location      TEXT NOT NULL,                      -- e.g. 'shop'
    params        TEXT NOT NULL,                      -- the query parameters as JSON
    body          TEXT NOT NULL CHECK (json_valid(body)),
    PRIMARY KEY (retrieved_at, location)
);

-- WEATHER_DAILY: one row per station and day (local time)
CREATE TABLE weather_daily (
    station      TEXT    NOT NULL,                    -- DWD station name
    day          TEXT    NOT NULL CHECK (day IS date(day)),
    rain_mm      REAL    NOT NULL CHECK (rain_mm >= 0),
    wet_hours    INTEGER NOT NULL CHECK (wet_hours BETWEEN 0 AND 25),
    t_max        REAL,
    sunshine_h   REAL    CHECK (sunshine_h BETWEEN 0 AND 25),
    records      INTEGER NOT NULL,                    -- hourly records behind the row
    run_id       INTEGER REFERENCES etl_run (run_id), -- lineage: which run wrote the row
    PRIMARY KEY (station, day)
);

-- SUPPLIER_PRICE: one row per supplier article, both price lists in one schema
CREATE TABLE supplier_price (
    supplier_no   TEXT    NOT NULL REFERENCES supplier (supplier_no),
    item_no       TEXT    NOT NULL,                   -- the supplier's article number, as text
    description   TEXT    NOT NULL,
    part_no       TEXT    REFERENCES spare_part (part_no),   -- NULL: not stocked by us
    price_eur     REAL    CHECK (price_eur > 0),      -- NULL: price on request
    pack_size     INTEGER NOT NULL CHECK (pack_size > 0),
    valid_from    TEXT    NOT NULL CHECK (valid_from IS date(valid_from)),
    run_id        INTEGER REFERENCES etl_run (run_id),
    PRIMARY KEY (supplier_no, item_no)
);
