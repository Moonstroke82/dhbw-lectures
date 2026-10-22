-- Coworking space: the catalogue of its data lake (Data Management, worksheet 18)
--
-- The coworking space keeps its data in a lake with three zones (bronze = raw,
-- silver = cleaned, gold = ready for reports and analysis). This script contains only
-- the catalogue: one row per dataset, with owner, purpose, personal data, access level,
-- retention date and the date of the last update. All names and values are fictional.
--
--   lake_dataset   one row per dataset in the lake
--
-- Load it into a database of its own:
--
--   import sqlite3
--   con = sqlite3.connect("coworking-lake.db")
--   with open("coworking-lake-catalog-session18.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- Running this script again deletes and rebuilds the table. Row count afterwards: 16.

DROP TABLE IF EXISTS lake_dataset;

CREATE TABLE lake_dataset (
    dataset_id      INTEGER PRIMARY KEY,
    path            TEXT    NOT NULL UNIQUE,
    zone            TEXT    NOT NULL CHECK (zone IN ('bronze', 'silver', 'gold')),
    source          TEXT    NOT NULL,
    format          TEXT    NOT NULL,
    size_mb         REAL    NOT NULL CHECK (size_mb > 0),
    owner           TEXT,                                 -- responsible person or team
    purpose         TEXT,                                 -- why the data is kept
    personal_data   INTEGER NOT NULL CHECK (personal_data IN (0, 1)),
    pseudonymised   INTEGER NOT NULL CHECK (pseudonymised IN (0, 1)),  -- names replaced by codes
    access_level    TEXT    NOT NULL CHECK (access_level IN ('public', 'internal', 'restricted')),
    retention_until TEXT    CHECK (retention_until IS date(retention_until)),  -- delete after
    last_updated    TEXT    NOT NULL CHECK (last_updated IS date(last_updated))
);

INSERT INTO lake_dataset VALUES
( 1, 'bronze/door/badge-scans/',          'bronze', 'door system',   'json',    310.0, 'Facility',  'building security',          1, 0, 'restricted', '2027-01-31', '2027-03-30'),
( 2, 'bronze/booking-app/exports/',       'bronze', 'booking app',   'csv',      42.5, 'Community', 'bookings and billing',       1, 0, 'internal',   '2028-12-31', '2027-03-31'),
( 3, 'bronze/finance/invoices/',          'bronze', 'accounting',    'xlsx',      6.8, 'Finance',   'invoices, tax records',      1, 0, 'restricted', '2037-12-31', '2027-03-31'),
( 4, 'bronze/network/wifi-sessions/',     'bronze', 'Wi-Fi router',  'log',     880.0, NULL,        NULL,                         1, 0, 'internal',   NULL,         '2027-03-31'),
( 5, 'bronze/facility/energy-meter/',     'bronze', 'smart meter',   'csv',      12.0, 'Facility',  'energy costs per floor',     0, 0, 'internal',   NULL,         '2027-03-31'),
( 6, 'bronze/facility/cctv-snapshots/',   'bronze', 'camera',        'jpg',    1450.0, 'Facility',  'building security',          1, 0, 'restricted', '2027-02-28', '2027-03-31'),
( 7, 'bronze/community/event-signups/',   'bronze', 'web form',      'csv',       0.4, 'Community', 'event planning',             1, 0, 'internal',   '2027-03-15', '2027-02-20'),
( 8, 'bronze/external/brightsky/',        'bronze', 'Bright Sky API','json',      3.1, 'Data team', 'weather vs. occupancy',      0, 0, 'public',     NULL,         '2027-03-31'),
( 9, 'silver/members.parquet',            'silver', 'pipeline',      'parquet',   0.2, 'Community', 'member master data',         1, 0, 'restricted', '2028-12-31', '2027-03-31'),
(10, 'silver/bookings.parquet',           'silver', 'pipeline',      'parquet',   4.6, 'Community', 'bookings and billing',       1, 1, 'internal',   '2028-12-31', '2027-03-31'),
(11, 'silver/invoices.parquet',           'silver', 'pipeline',      'parquet',   1.1, 'Finance',   'invoices, tax records',      1, 0, 'restricted', '2037-12-31', '2027-03-31'),
(12, 'silver/energy_daily.parquet',       'silver', 'pipeline',      'parquet',   0.3, 'Facility',  'energy costs per floor',     0, 0, 'internal',   NULL,         '2027-03-31'),
(13, 'gold/fact_booking.parquet',         'gold',   'pipeline',      'parquet',   2.9, 'Data team', 'occupancy and revenue reports', 1, 1, 'internal', '2028-12-31', '2027-03-30'),
(14, 'gold/dim_member.parquet',           'gold',   'pipeline',      'parquet',   0.1, 'Data team', 'occupancy and revenue reports', 1, 0, 'internal', '2028-12-31', '2027-03-30'),
(15, 'gold/occupancy_by_floor.csv',       'gold',   'analyst',       'csv',       0.1, 'Data team', 'monthly management report',  0, 0, 'internal',   NULL,         '2027-03-01'),
(16, 'gold/churn_features.parquet',       'gold',   'data scientist','parquet',  18.0, NULL,        'churn prediction trial',     1, 1, 'internal',   NULL,         '2026-11-02');
