---
course: Data Management
session: 16
title: ETL and Data Integration
subtitle: Practice tasks on extract–transform–load and ELT, pipeline design, load strategies, scheduling and monitoring
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 16 on your own or with your project team. Tasks 1, 2 and the exam-style task can be done on paper. For the lab tasks you need Jupyter with pandas and openpyxl (`python -m pip install pandas openpyxl`), SQLite 3.38 or newer (check with `sqlite3.sqlite_version` in Python) and these files: the coworking space's invoices [coworking-invoices-session15.xlsx](data/coworking-invoices-session15.xlsx) from worksheet 15 and the new re-export of March [coworking-invoices-2027-03-reexport-session16.csv](data/coworking-invoices-2027-03-reexport-session16.csv), and the saved weather response for Heidelberg [brightsky-heidelberg-2026-09-28.json](data/brightsky-heidelberg-2026-09-28.json). The weather data are real observations of the Deutscher Wetterdienst (DWD), retrieved through the Bright Sky API (de Maeyer, n.d.) and licensed under CC BY 4.0 (Deutscher Wetterdienst, 2024); all other names and data are fictional. The in-class hands-on uses [bikeshop-etl-session16.sql](data/bikeshop-etl-session16.sql) and [bikeshop-till-days-session16.csv](data/bikeshop-till-days-session16.csv) together with the session 15 files. The terms follow the session slides, which are based on Kimball and Ross (2013, Chapters 19–20), Vassiliadis (2009), Rahm and Do (2000), Serra (2024, Chapter 9), Reis and Housley (2022) and the SQLite documentation (SQLite, n.d.-a, n.d.-b, n.d.-c). The results in the solutions were produced with Python 3.13, pandas 3.0.6, openpyxl 3.1.5 and SQLite 3.45.1.

```python
import json
import sqlite3
import pandas as pd
```

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. In ETL, the data is transformed before it is written into the target tables.
2. ELT means that no transformation takes place at all.
3. An incremental extract needs a watermark, for example the date of the last loaded record.
4. A pipeline is idempotent if running it twice with the same input leaves the target in the same state as running it once.
5. `to_sql(..., if_exists="replace")` keeps the primary key and the constraints of the existing table.
6. If one row of a load violates a `CHECK` constraint, the other rows of the same transaction are still stored.
7. A pipeline run that falls back to an old saved copy of the data should still be logged as `ok`, because no error occurred.
8. A freshness check compares the newest date in the target with today's date.

::: answer lines=10
:::

::: solution
1. **True.** Extract, transform (outside the target, e.g. in pandas), then load the clean rows.
2. **False.** ELT changes the **order**: raw data is loaded first and transformed **inside** the target database, e.g. with SQL or views (Serra, 2024, Chapter 9).
3. **True.** The watermark tells the next run where to continue; it can be a date, a running number or a change timestamp.
4. **True.** That is the definition; in our pipeline the upsert on the primary key makes reruns harmless.
5. **False.** `replace` **drops** the table and creates a new one without primary key, `CHECK` or foreign key constraints (observed in session 16). Create the table with constraints once and use an upsert (or delete and insert) instead.
6. **False.** In one transaction it is all or nothing: the whole load is rolled back (atomicity, session 10).
7. **False.** The run should end with a **warning** that says which data was used; otherwise stale data looks current (timeliness).
8. **True.** For example `max(day)` in `weather_daily` compared with yesterday; a gap of more than one day is a warning.

Marking: one point per statement; for false statements, the point requires a correct correction.
:::

## E, T or L? The Food Co-op's Weekly Orders

The food co-op from worksheets 11 and 15 wants a weekly pipeline: every Monday, the order documents of the previous week (JSON, one document per order, as in `foodcoop-orders-session11.json`) are fetched from the ordering app's API and loaded into the co-op's SQLite database with the tables `member`, `customer_order` and `order_item`. The farms also send their new price lists as Excel files.

1. Assign each step to **E**, **T** or **L**, and put the steps into a sensible order:
   a) write the new orders with `INSERT … ON CONFLICT` ·
   b) call the API for the last week, with a timeout ·
   c) turn each `items` array into rows (`json_normalize` with `record_path`) ·
   d) save the API response as a file with the retrieval date ·
   e) replace `"qty"` by `"quantity"` where an app version used the wrong name ·
   f) check that every `member_no` exists in `member` ·
   g) read each farm's Excel price list ·
   h) write a row into the run log
2. The board wants to keep **every** raw order document "for questions we do not know yet". Sketch how the pipeline changes if you switch to **ELT**. Which SQLite feature from session 11 does the transformation then use?
3. The order documents contain members' **phone numbers**, which the analysis tables do not need. Does that speak for ETL or for ELT? Give one sentence.

::: answer lines=12
:::

::: solution
1. Order and assignment (other orders with a sound reason are fine): **h** start of the run log (management) → **b** E → **d** E (landing; "load to landing" is also accepted) → **g** E → **c** T → **e** T → **f** T (validation; a foreign key in the database is the second line of defence) → **a** L → **h** finish the run log with status and row counts. Points to check: the raw response is saved **before** any transformation; validation comes **before** the load; the run log has a start and an end.
2. ELT: a table `raw_order(retrieved_at, body)` with one row per API response (or per document), body as JSON text with `CHECK (json_valid(body))`; the transformation becomes SQL — views or `INSERT … SELECT` with `json_each(body, '$.items')` and `->>` (session 11; SQLite, n.d.-a). New questions later only need a new query on the raw table. Price lists from Excel still need Python to be read (or a raw table per sheet).
3. **ETL** (at least for these fields): drop or aggregate personal data before it is loaded — data minimisation (GDPR, session 19). With ELT, the phone numbers would be copied into the analysis database without need, and everyone with access to the raw table could read them.

Marking: 1 has four points (two for a correct order, two for correct E/T/L labels with at most one mistake); 2 and 3 one point each.
:::

## Append, Replace or Upsert? The Car-Sharing Trips

The car-sharing company's reporting database has a table `trip` with three rows:

```sql
CREATE TABLE trip (trip_id TEXT PRIMARY KEY, trip_date TEXT NOT NULL,
                   distance_km REAL CHECK (distance_km >= 0));
-- T-509 | 2027-06-09 | 95.0
-- T-510 | 2027-06-10 |  9.0
-- T-511 | 2027-06-11 | 640.0
```

The next batch from the API has three rows: `T-509, 2027-06-09, 59.0` (the distance was corrected), `T-512, 2027-06-14, 21.0` and the same `T-512` row a second time (sent twice after a retry). The batch is a DataFrame `batch`.

Predict the content of `trip` after each of the following, then check your predictions in SQLite:

1. `batch.to_sql("trip", con, if_exists="append", index=False)`
2. the same, but the table was created **without** a primary key
3. `batch.to_sql("trip", con, if_exists="replace", index=False)`
4. `INSERT … ON CONFLICT (trip_id) DO UPDATE SET trip_date = excluded.trip_date, distance_km = excluded.distance_km` with `executemany`
5. `INSERT OR IGNORE INTO trip …` with `executemany`
6. `INSERT OR REPLACE INTO trip …` gives the same rows as 4. Why can it still be dangerous if another table refers to `trip` with `ON DELETE CASCADE`?

::: hint
Start every case from a fresh table, e.g. with a function that creates the table in `sqlite3.connect(":memory:")` and inserts the three rows. The SQLite page on the ON CONFLICT clause explains `IGNORE` and `REPLACE` (SQLite, n.d.-c).
:::

::: answer lines=14
:::

::: solution
All observed with pandas 3.0.6 and SQLite 3.45.1.

1. Error: pandas raises `DatabaseError` caused by `UNIQUE constraint failed: trip.trip_id`; the table still has the **three old rows** — the batch was one transaction.
2. **6 rows**: T-509 twice (95.0 and 59.0), T-510, T-511 and T-512 twice — duplicates, and nobody knows which distance of T-509 is right.
3. **3 rows**: T-509 (59.0) and T-512 twice; T-510 and T-511 are **gone**, and the new table has no primary key and no `CHECK` (`CREATE TABLE "trip" ("trip_id" TEXT, "trip_date" TEXT, "distance_km" REAL)`).
4. **4 rows**: T-509 **59.0** (updated), T-510, T-511, T-512 once — the second T-512 updated the row the first one inserted. This is the idempotent choice.
5. **4 rows**, but T-509 keeps **95.0**: `IGNORE` skips rows that violate a uniqueness constraint (SQLite, n.d.-c) — new rows arrive, corrections are lost.
6. `REPLACE` **deletes** the old row and inserts a new one (SQLite, n.d.-c). With foreign keys switched on, the delete fires `ON DELETE CASCADE`: in a test with a parent row and two child rows, `INSERT OR REPLACE` on the parent left **0** child rows, while the upsert left them untouched. Use `ON CONFLICT … DO UPDATE` for corrections.

Marking: one point per case; in 3 the point needs both the lost rows and the lost constraints.
:::

## Lab: An Incremental Invoice Pipeline for the Coworking Space

In worksheet 15 you read all invoice sheets at once. Now the coworking space wants a pipeline that runs **once a month**: each run loads one monthly sheet into a table `invoice`, and every run is logged.

```python
con = sqlite3.connect(":memory:")       # or a file, e.g. "coworking.db"
con.executescript("""
CREATE TABLE etl_run (run_id INTEGER PRIMARY KEY, source TEXT NOT NULL, started_at TEXT NOT NULL,
                      status TEXT, rows_loaded INTEGER, message TEXT);
CREATE TABLE invoice (invoice_no TEXT PRIMARY KEY, member_no TEXT NOT NULL, month TEXT NOT NULL,
                      amount_eur REAL NOT NULL CHECK (amount_eur > 0),
                      paid INTEGER NOT NULL CHECK (paid IN (0, 1)),
                      run_id INTEGER REFERENCES etl_run (run_id));""")
```

1. Write `extract_month(month)` (one sheet, the correct header row, the column names of January for every month), `transform(df, month)` (`paid` as 0/1, a column `month`) and `load()` with an upsert on `invoice_no`. Write a function `run(month)` that logs each run in `etl_run`.
2. Run January, February and March. After each run: number of invoices, total amount, open (unpaid) amount.
3. Run February **again**. What changes in `invoice` and in `etl_run`?
4. Add a check after the load that sets the run status to `warning` if a member has **more than one invoice in the same month**, and a query that finds **gaps** in the invoice numbers. What do they report?
5. In April, the coworking space sends a **re-export of March** ([coworking-invoices-2027-03-reexport-session16.csv](data/coworking-invoices-2027-03-reexport-session16.csv)). Compare it with the March sheet, load it with your pipeline and check the open amount. Is the result right?
6. Change the load for re-exports so that the table matches the newest export of a month exactly. Which totals do you get now?

::: hint
`pd.read_excel(..., sheet_name="2027-02", header=2)` reads one sheet; the February sheet needs `rename` (worksheet 15). `int(s[2:])` turns `"R-2716"` into 2716; `set(range(min, max + 1)) - set(numbers)` lists the gaps. An upsert never deletes anything.
:::

::: answer lines=18
:::

::: solution
All observed with pandas 3.0.6 and SQLite 3.45.1.

```python
REN = {"Invoice": "invoice_no", "Member": "member_no", "Amount (EUR)": "amount_eur", "Paid": "paid"}
UP = """INSERT INTO invoice VALUES (:invoice_no, :member_no, :month, :amount_eur, :paid, :run_id)
ON CONFLICT (invoice_no) DO UPDATE SET member_no = excluded.member_no, month = excluded.month,
  amount_eur = excluded.amount_eur, paid = excluded.paid, run_id = excluded.run_id"""

def extract_month(month):
    return pd.read_excel("coworking-invoices-session15.xlsx", sheet_name=month,
                         header=2).rename(columns=REN)

def transform(df, month):
    out = df[["invoice_no", "member_no", "amount_eur", "paid"]].copy()
    out["month"] = month
    out["paid"] = out["paid"].map({"yes": 1, "no": 0})
    return out

def run(month, df=None, source=None):
    with con:
        run_id = con.execute("INSERT INTO etl_run (source, started_at) VALUES (?, datetime('now'))",
                             (source or f"sheet {month}",)).lastrowid
    df = extract_month(month) if df is None else df
    rows = transform(df, month).assign(run_id=run_id).to_dict("records")
    with con:
        con.executemany(UP, rows)
    twice = con.execute("""SELECT member_no, count(*) FROM invoice WHERE month = ?
                           GROUP BY member_no HAVING count(*) > 1""", (month,)).fetchall()
    with con:
        con.execute("UPDATE etl_run SET status = ?, rows_loaded = ?, message = ? WHERE run_id = ?",
                    ("warning" if twice else "ok", len(rows),
                     f"members invoiced twice: {twice}" if twice else None, run_id))
```

1. See the code. A `map` that meets an unknown value (e.g. `"Yes"`) gives `NaN`, and the `NOT NULL`/`CHECK` on `paid` then stops the load — good.
2. After January: **7** invoices, **1,253 €**, open **189 €**. After February: **15**, **3,677 €**, open **667 €**. After March: **23**, **7,115 €**, open **3,323 €** (the same open amount as in worksheet 15).
3. `invoice` is **unchanged** (23 rows): the eight February invoices are updated with the same values, only their `run_id` becomes 4. `etl_run` has a **fourth** row — the log shows that February was loaded twice.
4. March run: status **warning**, "members invoiced twice: [('M9', 2)]" (R-2723 and R-2724). Gap query: **R-2722** is missing. Both are questions for the office, not errors the pipeline may fix on its own.
5. The re-export has 8 invoices: **R-2721** (M7) and **R-2723** (M9) are now **paid**, **R-2722** appears (M8, 45 €: the gap was a late DAY invoice), and **R-2724 is no longer there** (cancelled). After the upsert: **24** invoices, open **1,945 €** — **wrong**: R-2724 (1,089 €, unpaid) is still in the table with `run_id` 3, and the run still warns about M9. An upsert inserts and updates, but it never **deletes** rows that disappeared from the source.
6. Delete and insert the month in **one transaction**:
   ```python
   with con:
       con.execute("DELETE FROM invoice WHERE month = ?", ("2027-03",))
       con.executemany(UP, transform(reexport, "2027-03").assign(run_id=run_id).to_dict("records"))
   ```
   (inside `run()`, with the `run_id` of the re-export run; `reexport = pd.read_csv(...)` of the new file)
   → **23** invoices, total **6,071 €**, open **856 €** (R-2704 189, R-2709 289, R-2711 189, R-2719 189 — M4 is still the dunning case); March **8** invoices, **2,394 €**. This is idempotent for full extracts of one month. Alternative: keep cancelled invoices with a `status` column instead of deleting them — better for an audit trail, and the usual practice in accounting.

Marking: one point per question; in 5 the point needs the explanation that the upsert does not delete R-2724.
:::

## Lab: ELT for the Sports Club's Weather Data

The sports club wants to keep every weather response it fetches and do the rest in SQL. Work in SQLite (from Python or the command-line tool) with the saved Heidelberg response.

```python
con = sqlite3.connect(":memory:")
con.execute("""CREATE TABLE raw_weather (retrieved_at TEXT NOT NULL, location TEXT NOT NULL,
               body TEXT NOT NULL CHECK (json_valid(body)),
               PRIMARY KEY (retrieved_at, location))""")
body = open("brightsky-heidelberg-2026-09-28.json", encoding="utf-8").read()
```

1. **Load raw**: insert the response with `retrieved_at = '2026-10-21T10:00:00'` and `location = 'pitch'`. Then try to insert the text `<html>502 Bad Gateway</html>` as a body, and the same response a second time with the same `retrieved_at`. What happens, and why is that useful?
2. **Transform in SQL**: create a view `weather_hourly` with one row per hour: `ts`, `day`, `rain_mm`, `temp_c`, `source_id`, and `temp_source_id` — the station that really measured the temperature (`fallback_source_ids` if present, else `source_id`). How many rows does the view have, and which SQL types do the numbers get?
3. **Daily values**: write the query for rain, wet hours, maximum temperature and records per day. Compare with pandas. Which day must the pipeline not load?
4. **Lineage in SQL**: join `weather_hourly` with the `sources` array to count the hours per station that measured (a) the precipitation and (b) the temperature.
5. **Two responses**: insert the same body again with `retrieved_at = '2026-10-22T06:15:00'` (as if the next run had fetched the same week). What happens to the daily rain on 2 October — and how does a view `weather_hourly_latest` fix it?

::: hint
`json_each(r.body, '$.weather') AS j` gives one row per record; `j.value ->> 'precipitation'` extracts a value, and `j.value -> 'fallback_source_ids' ->> 'temperature'` goes one level deeper (SQLite, n.d.-a). Use `substr(ts, 1, 10)` for the local day — `date()` converts to UTC. `row_number() OVER (PARTITION BY location, ts ORDER BY retrieved_at DESC)` numbers the copies of an hour, newest first.
:::

::: answer lines=18
:::

::: solution
All observed with SQLite 3.45.1.

```sql
CREATE VIEW weather_hourly AS
SELECT r.location, r.retrieved_at,
       j.value ->> 'timestamp'                 AS ts,
       substr(j.value ->> 'timestamp', 1, 10)  AS day,
       j.value ->> 'precipitation'             AS rain_mm,
       j.value ->> 'temperature'               AS temp_c,
       j.value ->> 'source_id'                 AS source_id,
       coalesce(j.value -> 'fallback_source_ids' ->> 'temperature',
                j.value ->> 'source_id')       AS temp_source_id
FROM raw_weather AS r, json_each(r.body, '$.weather') AS j;
```

1. The first insert works. The HTML text fails with `CHECK constraint failed: json_valid(body)`; the second insert of the same key fails with `UNIQUE constraint failed: raw_weather.retrieved_at, raw_weather.location`. Useful: an error page from a proxy or a server can never be stored as "data", and the same retrieval cannot be stored twice by accident.
2. **169** rows (28 September 00:00 to 5 October 00:00). `->>` returns SQL values: `rain_mm` and `temp_c` are **real**, `source_id` and `temp_source_id` **integer** — no type conversion needed.
3. ```sql
   SELECT day, round(sum(rain_mm), 1) AS rain_mm, sum(rain_mm > 0) AS wet_hours,
          max(temp_c) AS t_max, count(*) AS records
   FROM weather_hourly GROUP BY day ORDER BY day;
   ```
   Rain 0.0, 0.0, 0.0, **1.1** (1 Oct, 4 wet hours), **2.4** (2 Oct, 4 wet hours), 0.0, **0.2** (4 Oct, 1 wet hour) and 0.0 for 5 October; t_max of the seven full days from 29.8 °C (30 Sep) down to 22.3 °C (2 Oct). Pandas gives the same sums per day. **5 October** has only **1** record (the included `last_date`) — a volume check must reject it. With `date(ts)` instead of `substr`, the days shift to UTC: 27 September appears with 2 records and 4 October has 23.
4. ```sql
   SELECT s.value ->> 'station_name' AS station, count(*) AS hours
   FROM weather_hourly AS h JOIN raw_weather AS r ON r.retrieved_at = h.retrieved_at,
        json_each(r.body, '$.sources') AS s
   WHERE s.value ->> 'id' = h.temp_source_id      -- or h.source_id for (a)
   GROUP BY station;
   ```
   (a) Precipitation (`source_id`): **Heidelberg-Kurpfalzhof 169**. (b) Temperature: **Mannheim 169** — the same lineage finding as in worksheet 15, now in SQL.
5. The view has **338** rows for 169 distinct hours, and the rain on 2 October doubles to **4.8 mm** with 48 records: the ELT transformation must deal with overlapping raw responses. Fix:
   ```sql
   CREATE VIEW weather_hourly_latest AS
   SELECT location, retrieved_at, ts, day, rain_mm, temp_c, source_id, temp_source_id
   FROM (SELECT h.*, row_number() OVER (PARTITION BY location, ts
                                         ORDER BY retrieved_at DESC) AS rn
         FROM weather_hourly AS h)
   WHERE rn = 1;
   ```
   → 169 rows, all from the retrieval of 22 October; 2 October again 2.4 mm with 24 records. The newest retrieval wins, which also takes over DWD corrections — the ELT version of an upsert.

Marking: one point per question; in 3 the point needs the rejected day, in 5 the point needs both the doubled value and a working fix (a `GROUP BY ts` with `max(retrieved_at)` and a join is also correct).
:::

## Exam-Style Task: A Nightly Pipeline for the Car-Sharing Company

This task is in the style of an exam question.

The car-sharing company wants its reporting database to contain all trips up to yesterday. A trainee built this job and scheduled it with cron at **00:05** every night:

```python
def nightly():
    yesterday = date.today() - timedelta(days=1)
    trips = get_all_trips(yesterday)            # all pages from the partner API, a list of dicts
    df = pd.DataFrame(trips)
    df = df[df["distance_km"] >= 0]
    df.to_sql("trip", con, if_exists="append", index=False)
    print("done")
```

The trips are also corrected by the service team for up to three days after the trip (e.g. a wrong odometer reading). The table `trip` has the primary key `trip_id`.

1. Mark the extract, transform and load parts of the job. Is it ETL or ELT? (1 point)
2. The job fails one night at the `to_sql` line, and the operator starts it again by hand. Then cron starts it again the next night, as planned. What happens in each case? (2 points)
3. Explain two problems caused by the schedule and by the extraction of "yesterday only". (2 points)
4. Name **three** checks the job should perform, each with the dimension it measures and what the job should do when it fails. (3 points)
5. Describe an improved design: extract, landing, load strategy, logging. (2 points)

::: answer lines=20
:::

::: solution
Marking guide (10 points).

1. (1 point) E: `get_all_trips(yesterday)`; T: building the DataFrame and the filter `distance_km >= 0`; L: `to_sql(..., if_exists="append")`. ETL — the transformation runs in pandas before the load. The point needs the labels and the ETL answer.
2. (2 points) Manual rerun: the failed `to_sql` stored nothing (one transaction), so the rerun appends the day once and works — but only because the first attempt failed completely. Had any trips of that day been stored before (e.g. a second manual start after a success), `append` fails with `UNIQUE constraint failed` on the primary key, and without a primary key it would store **duplicates** — the job is not idempotent — 1 point. Next night: cron extracts only the new "yesterday"; if the manual rerun had not happened, the failed day would never be loaded, and nobody would notice, because the job only prints "done" and logs nothing — 1 point.
3. (2 points, 1 per problem) **Corrections** within three days are never loaded: the job only extracts yesterday and only appends. **Late or still running trips**: at 00:05 trips that end after midnight or are booked late are not yet complete; and "yesterday" depends on the time zone of the server and of the API. Also accepted: the job does not notice when the API returns nothing (an empty day looks like "no trips").
4. (3 points, 1 per check with dimension and action; any three) **Volume/completeness**: number of trips compared with the API's `total` or with the usual range per weekday — stop and warn if it differs. **Validity**: `distance_km >= 0`, plausible duration — reject and **log** the rows instead of silently dropping them (a negative distance is a typo to report to the service team, not to hide). **Uniqueness**: `trip_id` unique in the batch — the primary key enforces it. **Freshness/timeliness**: newest `trip_date` in the table = yesterday — warn otherwise. **Schema**: expected fields present in the API response — stop. **Referential integrity**: every `member_no` and `plate` exists — the foreign keys refuse, the run is logged as failed.
5. (2 points: 1 for incremental extract with overlap plus idempotent load, 1 for landing and run log) Example: run at 06:00; extract **from the watermark minus three days** to yesterday (overlap for corrections), all pages, with timeout and status check; save the raw response with the retrieval time (landing); transform and validate, write rejected rows to a reject table; load with an **upsert** on `trip_id` in **one transaction**; log every run in `etl_run` (start, end, status, rows read/loaded/rejected, source, message) and alert on `failed` and `warning`; rerunning any day is then harmless.
:::

## Optional Challenge: A Script for the Scheduler {.optional}

Turn the weather pipeline of the session into a script `weather_pipeline.py` that a scheduler can run:

- it takes the first and the last day as command-line arguments and **checks** them before calling anything,
- it accepts a day only if it has as many hourly records as the **local day has hours** — 24 on most days, 25 on 25 October 2026 and 23 on 28 March 2027,
- it logs every run in `etl_run` and ends with exit code 0 on success (also with warnings) and 1 on failure,
- and write the crontab line that runs it every day at 06:15 for yesterday (hint: a small wrapper or `date -d yesterday +%F` on Linux).

Test it with a correct range, a range that includes the incomplete day 12 October, and an invalid date such as `2026-10-1x`.

::: hint
`pd.Timestamp(day, tz="Europe/Berlin") + pd.DateOffset(days=1)` is the next local midnight; `+ pd.Timedelta(days=1)` adds exactly 24 hours, which is wrong on these two days. `sys.exit(main(...))` passes the exit code to the scheduler. `dt.date.fromisoformat()` rejects invalid dates.
:::

::: answer lines=12
:::

::: solution
One possible solution, using `extract`, `transform`, `load`, `start_run` and `finish_run` from the session (tested on the saved Mannheim copy):

```python
import datetime as dt, sqlite3, sys
import pandas as pd
from pipeline import extract, transform, load, start_run, finish_run

def expected_hours(day, tz="Europe/Berlin"):
    start = pd.Timestamp(day, tz=tz)
    return int((start + pd.DateOffset(days=1) - start) / pd.Timedelta(hours=1))

def main(first, last, db="bikeshop.db"):
    con = sqlite3.connect(db)
    con.execute("PRAGMA foreign_keys = ON")
    run_id = start_run(con, "weather")
    try:
        if dt.date.fromisoformat(first) > dt.date.fromisoformat(last):   # check the parameters
            raise ValueError(f"first {first} is after last {last}")
        data, source = extract(first, last)
        daily = transform(data, first, last)
        ok = daily["records"] == daily["day"].map(expected_hours)
        n = load(con, daily[ok], run_id)
        bad = daily.loc[~ok, "day"].tolist()
        finish_run(con, run_id, "warning" if bad else "ok", source, len(data["weather"]),
                   n, len(bad), f"incomplete days: {bad}" if bad else None)
        return 0
    except Exception as e:
        finish_run(con, run_id, "failed", message=f"{type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
```

Observed: `expected_hours` gives 24 for 2026-10-24, **25** for 2026-10-25, **23** for 2027-03-28. `python weather_pipeline.py 2026-10-05 2026-10-11` → exit code 0, status ok, 7 rows; `2026-10-10 2026-10-12` → exit 0, status warning, 2 loaded, 1 rejected ("incomplete days: ['2026-10-12']"); `2026-10-10 2026-10-1x` → exit **1**, status failed, "ValueError: Invalid isoformat string: '2026-10-1x'". Without the parameter check, that last call ran **without** any error: the string comparison in the filter happened to accept the days 10–12 — an invalid parameter that produces plausible output is the worst case.

Crontab line (Linux; five time fields minute, hour, day of month, month, weekday — The Open Group, 2018):

```text
15 6 * * * cd /home/velo/etl && python weather_pipeline.py $(date -d yesterday +\%F) $(date -d yesterday +\%F) >> etl.log 2>&1
```

In a crontab, `%` must be escaped as `\%`. On Windows, create a daily task in the Task Scheduler that runs a small batch file with the same call. Points to check in other solutions: the parameters are validated, the expected hours come from the calendar (not a constant 24), failures end with a non-zero exit code **and** a log entry.
:::

## References {.references}

- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Deutscher Wetterdienst. (2024). *Terms of use for data on the CDC-OpenData area*. https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Rahm, E., & Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.
- Reis, J., & Housley, M. (2022). *Fundamentals of data engineering: Plan and build robust data systems*. O'Reilly Media.
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
- SQLite. (n.d.-a). *JSON functions and operators*. Retrieved October 22, 2026, from https://www.sqlite.org/json1.html
- SQLite. (n.d.-b). *UPSERT*. Retrieved October 22, 2026, from https://www.sqlite.org/lang_upsert.html
- SQLite. (n.d.-c). *The ON CONFLICT clause*. Retrieved October 22, 2026, from https://www.sqlite.org/lang_conflict.html
- The Open Group. (2018). *crontab — schedule periodic background work*. The Open Group Base Specifications Issue 7, 2018 edition (IEEE Std 1003.1-2017). https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html
- Vassiliadis, P. (2009). A survey of extract–transform–load technology. *International Journal of Data Warehousing and Mining, 5*(3), 1–27. https://doi.org/10.4018/jdwm.2009070101
