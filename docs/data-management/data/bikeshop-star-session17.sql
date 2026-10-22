-- Velo Neckar bike shop: a star schema for till sales (Data Management, session 17)
--
-- The model solution of the session 17 hands-on: one fact table and four dimension
-- tables, built and filled with SQL from the operational tables (ELT inside SQLite).
-- Design your own star first, then compare it with this one.
--
--   fact_sales       grain: one line on a till receipt
--   dim_date         one row per calendar day of October 2026
--   dim_product      one row per product, with product group and category
--   dim_salesperson  one row per salesperson
--   dim_weather      one row per weather type (banded from weather_daily)
--
-- Run it after bikeshop-sales-session17.sql (needs product, sale, sale_line,
-- salesperson, employee and weather_daily):
--
--   with open("bikeshop-star-session17.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- Running this script again deletes and rebuilds the five star tables.
-- Row counts afterwards: dim_date 31, dim_product 18, dim_salesperson 2,
-- dim_weather 5, fact_sales 54.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_salesperson;
DROP TABLE IF EXISTS dim_weather;

-- DIM_DATE: one row per day; the key is the date as a number (20261005)
CREATE TABLE dim_date (
    date_key     INTEGER PRIMARY KEY,
    full_date    TEXT    NOT NULL UNIQUE CHECK (full_date IS date(full_date)),
    weekday      TEXT    NOT NULL,                    -- 'Monday' ... 'Sunday'
    day_type     TEXT    NOT NULL CHECK (day_type IN ('Mon-Fri', 'Saturday', 'Sunday')),
    month        INTEGER NOT NULL,
    month_name   TEXT    NOT NULL,
    quarter      INTEGER NOT NULL,
    year         INTEGER NOT NULL
);

-- DIM_PRODUCT: surrogate key plus the product number of the till (natural key)
CREATE TABLE dim_product (
    product_key    INTEGER PRIMARY KEY,
    product_no     TEXT    NOT NULL UNIQUE,
    name           TEXT    NOT NULL,
    product_group  TEXT    NOT NULL,
    category       TEXT    NOT NULL                   -- hierarchy: category > group > product
);

-- DIM_SALESPERSON
CREATE TABLE dim_salesperson (
    salesperson_key  INTEGER PRIMARY KEY,
    employee_no      INTEGER NOT NULL UNIQUE,
    name             TEXT    NOT NULL
);

-- DIM_WEATHER: weather types; bike_day groups them (hierarchy: bike_day > weather_type)
CREATE TABLE dim_weather (
    weather_key   INTEGER PRIMARY KEY,
    weather_type  TEXT    NOT NULL UNIQUE,
    bike_day      TEXT    NOT NULL CHECK (bike_day IN ('good', 'bad', 'unknown')),
    rule          TEXT    NOT NULL
);

-- FACT_SALES: one row per receipt line; four foreign keys, two measures
CREATE TABLE fact_sales (
    date_key         INTEGER NOT NULL REFERENCES dim_date (date_key),
    product_key      INTEGER NOT NULL REFERENCES dim_product (product_key),
    salesperson_key  INTEGER NOT NULL REFERENCES dim_salesperson (salesperson_key),
    weather_key      INTEGER NOT NULL REFERENCES dim_weather (weather_key),
    receipt_no       INTEGER NOT NULL,                -- degenerate dimension
    line_no          INTEGER NOT NULL,
    quantity         INTEGER NOT NULL CHECK (quantity > 0),     -- additive
    revenue          NUMERIC NOT NULL CHECK (revenue >= 0),     -- additive: quantity x price
    PRIMARY KEY (receipt_no, line_no)
);

-- Fill dim_date with every day of October 2026
WITH RECURSIVE days (d) AS (
    SELECT '2026-10-01'
    UNION ALL
    SELECT date(d, '+1 day') FROM days WHERE d < '2026-10-31'
)
INSERT INTO dim_date (date_key, full_date, weekday, day_type, month, month_name, quarter, year)
SELECT CAST(strftime('%Y%m%d', d) AS INTEGER),
       d,
       CASE strftime('%w', d) WHEN '0' THEN 'Sunday'   WHEN '1' THEN 'Monday'
                              WHEN '2' THEN 'Tuesday'  WHEN '3' THEN 'Wednesday'
                              WHEN '4' THEN 'Thursday' WHEN '5' THEN 'Friday'
                              ELSE 'Saturday' END,
       CASE strftime('%w', d) WHEN '0' THEN 'Sunday' WHEN '6' THEN 'Saturday'
                              ELSE 'Mon-Fri' END,
       CAST(strftime('%m', d) AS INTEGER),
       'October',
       (CAST(strftime('%m', d) AS INTEGER) + 2) / 3,
       CAST(strftime('%Y', d) AS INTEGER)
FROM days;

-- Fill dim_product: the category is derived from the product group
INSERT INTO dim_product (product_no, name, product_group, category)
SELECT product_no, name, product_group,
       CASE WHEN product_group IN ('E-bikes', 'Bikes')       THEN 'Bikes'
            WHEN product_group IN ('Parts', 'Accessories')   THEN 'Parts and accessories'
            ELSE 'Service' END
FROM product
ORDER BY product_no;

INSERT INTO dim_salesperson (employee_no, name)
SELECT s.employee_no, e.name
FROM salesperson AS s JOIN employee AS e ON e.employee_no = s.employee_no
ORDER BY s.employee_no;

-- Weather types (the rule of session 15: a bad bike day has at least 1 mm or below 15 °C)
INSERT INTO dim_weather (weather_key, weather_type, bike_day, rule) VALUES
    (0, 'unknown',      'unknown', 'no weather data for the day'),
    (1, 'dry and warm', 'good',    'rain < 1 mm and t_max >= 15 °C'),
    (2, 'dry and cool', 'bad',     'rain < 1 mm and t_max < 15 °C'),
    (3, 'light rain',   'bad',     '1 mm <= rain < 5 mm'),
    (4, 'heavy rain',   'bad',     'rain >= 5 mm');

-- Fill the fact table: look up the surrogate keys, classify the day's weather
INSERT INTO fact_sales (date_key, product_key, salesperson_key, weather_key,
                        receipt_no, line_no, quantity, revenue)
SELECT CAST(strftime('%Y%m%d', s.sale_date) AS INTEGER),
       p.product_key,
       sp.salesperson_key,
       CASE WHEN w.day IS NULL     THEN 0
            WHEN w.rain_mm >= 5    THEN 4
            WHEN w.rain_mm >= 1    THEN 3
            WHEN w.t_max < 15      THEN 2
            ELSE 1 END,
       l.receipt_no, l.line_no, l.quantity,
       round(l.quantity * l.unit_price, 2)
FROM sale_line AS l
JOIN sale            AS s  ON s.receipt_no = l.receipt_no
JOIN dim_product     AS p  ON p.product_no = l.product_no
JOIN dim_salesperson AS sp ON sp.employee_no = s.employee_no
LEFT JOIN weather_daily AS w ON w.day = s.sale_date AND w.station = 'Mannheim';
