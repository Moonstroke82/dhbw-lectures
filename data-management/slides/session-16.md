---
course: Data Management
session: 16
title: ETL and Data Integration
subtitle: Extract–transform–load vs. ELT · pipeline design · scheduling and monitoring
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# ETL and Data Integration {.title}

::: notes
Time plan for today (3 h): recap 7 min · today's data 3 min · data integration and ETL 13 min · ETL vs. ELT with the SQLite demo 10 min · mini exercise which step 8 min · break 10 min · pipeline design: principles, extract, transform, price lists 20 min · load and upsert 8 min · mini exercise what if 8 min · scheduling and monitoring 12 min · hands-on: the bike shop pipeline 45 min · team step 12 min · wrap-up 5 min · ~19 min buffer.
Input is about 73 minutes, hands-on, exercises and discussion about 73 minutes. Priorities if time runs short: the three ETL steps with a staging or landing zone, ETL vs. ELT (where the transformation runs), full vs. incremental extraction, replace/append/upsert and idempotent reruns, and the run log with checks are the exam core. Code syntax is a tool, not exam content: the exam may show short code or SQL to read and explain. The optional slide on orchestrators is self-study. Shorten the hands-on to questions 1–5 if needed, but keep question 6 (run it twice and read the run log): it is the heart of today.
How the results were produced: every Python and SQL statement was run with Python 3.13, pandas 3.0.6, requests 2.34.2, openpyxl 3.1.5 and SQLite 3.45.1 on a fresh bikeshop.db built from bikeshop-schema.sql, bikeshop-data.sql, bikeshop-data-session09.sql and the new bikeshop-etl-session16.sql. The authoring environment could not reach api.brightsky.dev (proxy, ProxyError), so every run used the fallback branch with brightsky-mannheim-2026-10-05.json from session 15 — exactly the plan B of session 15. Students calling the live API get the same daily values for 5–11 October; the incremental run on the "Monitoring" slides then loads real days instead of warning. Daily runs are simulated by asking for a few days at a time. The till export bikeshop-till-days-session16.csv is fictional.
:::

---

# Today's Agenda

1. Recap: from one API call to a repeatable process
2. Data integration: extract, transform, load — and ELT
3. Pipeline design: extract, transform and load step by step
4. Scheduling and monitoring: what runs when, and how we notice errors
5. Hands-on: a small pipeline API → pandas → SQLite

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:07 Today's data (everyone) · 0:10 Data integration, ETL, ELT (input with live demo) · 0:33 Mini exercise which step (pairs) · 0:41 Break · 0:51 Pipeline design: extract, transform, load (input, live demo) · 1:19 Mini exercise what if (pairs) · 1:27 Scheduling and monitoring (input, live demo) · 1:39 Hands-on (groups of 3, each student on their own laptop) · 2:24 Team step (project teams) · 2:36 Wrap-up · buffer.
Live demo: run the pipeline functions in a notebook; run the load twice in front of the class and count rows — the "aha" of idempotency works best live. If the network works, call the live API; if not, the fallback is part of the story.
:::

---

# Recap: Where Session 15 Left Us

- We read **CSV**, **Excel** and **JSON** with explicit options and called a **REST API** with `requests`
- Rules: **check the status before you parse**, always a **timeout**, save the **raw response**, plan B with a saved copy
- We ended with `weather_daily` in SQLite — built **once**, by hand, in a notebook
- Today: make it **repeatable**: every day, unattended, without duplicates — and notice when it fails

::: callout
**Your preparation:** your weather notebook with the raw JSON and `weather_daily`; a sample of your team's data source. Which cells would you have to run again **tomorrow** — and in which order?
:::

::: source
Session 15 of this course; Rahm and Do (2000).
:::

::: notes
Quick check (2 min): who has the session 15 notebook and weather_daily? Students without it start today from the saved copy — no disadvantage. Ask the callout question to two or three students: typical answers "all of them, from the top", "the API call and then the to_sql" — and what happens to weather_daily when to_sql runs again with if_exists="append"? (duplicates; today's load slides). Link: session 14 named the cleaning steps the "T" of ETL; session 15 was the "E"; today we add the "L" and the glue.
:::

---

# Today's Data

| Source | Content | Becomes |
|---|---|---|
| Bright Sky API or `brightsky-mannheim-2026-10-05.json` | hourly weather, Mannheim, 5–11 Oct 2026 | `weather_daily` |
| `bikeshop-pricelist-s1-session15.csv` | price list of S1, German CSV | `supplier_price` |
| `bikeshop-pricelist-s2-session15.xlsx` | price list of S2, Excel | `supplier_price` |
| `bikeshop-till-days-session16.csv` | **new**: daily figures from the till | `till_daily` |
| `bikeshop-etl-session16.sql` | **new**: target tables and run log | `bikeshop.db` |

::: source
Own example based on the bike shop case; supplier and till data fictional. Weather data: Deutscher Wetterdienst via de Maeyer (n.d.), CC BY 4.0.
:::

::: notes
Everyone runs the loading cell now: the three bike shop scripts plus bikeshop-etl-session16.sql (it creates supplier if it does not exist yet, raw_weather, weather_daily, supplier_price and etl_run). Students who did worksheet 12 and have the purchase orders load bikeshop-purchasing-session12.sql before the new script. The till export has six rows (Monday 5 to Saturday 10 October): walk-in customers, test rides, repair intakes and revenue — the shop is closed on Sundays. Check: `SELECT name FROM sqlite_master WHERE type = 'table'` lists 14 tables.
:::

---

# Data Integration {.section}

From many sources to one place

---

# Why Data Integration?

- The bike shop's data lives in **many systems**: till, web shop, suppliers' price lists, weather service
- Questions **across** them need the data **in one place**, in **one format**: "Do rainy days cost us test rides?"
- **Data integration**: moving and combining data between systems so it can be used together

| Problem | Bike shop example |
|---|---|
| **Schema** differs | `Preis netto` vs. `Price EUR`; `Gültig ab` vs. `Available from` |
| **Formats** differ | `05.10.2026` vs. `2026-10-05`; `3,05` vs. `3.05` |
| **Keys** differ | supplier article `004711` vs. our part `P-101` |
| **Meaning** differs | price per piece or per pack? local time or UTC? |

::: source
Based on DAMA International (2017, Chapter 8) and Rahm and Do (2000).
:::

::: notes
DAMA-DMBOK (DAMA International, 2017, Chapter 8) treats data integration and interoperability as a knowledge area of its own (session 1: the DAMA wheel); ETL is its classic technique. Rahm and Do (2000) separate single-source from multi-source problems and schema-level from instance-level problems: naming conflicts (same thing, different names) and structural conflicts are schema-level; duplicates and contradicting values across sources are instance-level. Meaning is the hardest: S2's LED light costs 14.50 with a pack of 5 — per piece or per pack? The data cannot tell; only the supplier can. Ask: which of these problems did we already meet in sessions 13–15? (formats, codes as text, time zones.)
:::

---

# Extract, Transform, Load

::: cards
### Extract
Read the data from the **sources**: API calls, files, database queries. Keep it **unchanged** in a landing or staging area.
### Transform
Make it fit the target: **parse**, **clean**, map **columns and keys**, **aggregate**, **validate** (sessions 14–15).
### Load
Write it into the **target tables** — with constraints, in **one transaction**, without duplicates.
:::

- **ETL** is the classic way to fill a **data warehouse** (session 17) — and any shared database
- Most of the work is in the **T**, most of the **risk** in the E and the L

::: source
Based on Kimball and Ross (2013, Chapters 19–20), Vassiliadis (2009) and Rahm and Do (2000).
:::

::: notes
Vassiliadis (2009) surveys ETL technology: ETL processes extract the relevant data from the sources, transport it to a special-purpose area where it is processed, and load the cleansed, transformed data into the warehouse. Rahm and Do (2000) describe the same: cleaning happens in a separate staging area before loading. Kimball and Ross (2013, Chapter 19) organise an ETL system into many subsystems — extracting, cleaning and conforming, delivering, and managing (scheduling, monitoring, error handling); Chapter 20 is the step-by-step development process. "Most risk in E and L": the source can change or disappear (session 15), a load can create duplicates or half-written tables. Staging vs. landing: names vary; today "landing" = raw files as they arrived, "staging" = tables in between.
:::

---

# The Bike Shop Pipeline

![The bike shop pipeline: five sources (Bright Sky API, saved copy, price list S1, price list S2, till export) feed step 1 extract; raw files land unchanged with their retrieval time; step 2 transform parses, maps columns and keys, aggregates and validates, sending rejected rows to a log; step 3 load upserts in one transaction into weather_daily, supplier_price and till_daily in bikeshop.db; a scheduler starts the run daily, and a run log etl_run records status, rows and source](img/etl-pipeline.png){width=90%}

::: source
Own illustration based on Kimball and Ross (2013, Chapters 19–20) and Rahm and Do (2000).
:::

::: notes
This is today's target picture; the hands-on builds it. Walk through left to right: the landing zone is the "save the raw response" of session 15 — if the transformation has a bug, we repeat it on the stored raw data instead of calling the API again (and the source may have changed in between). Rejected rows are not thrown away silently: they are counted and logged. The scheduler and the run log are the "managing" part that turns a notebook into a process. The time 06:15 is an example: after the night, when yesterday is complete.
:::

---

# ETL or ELT: Where Does the Transformation Run?

![Two lanes. ETL: source, extract with Python, transform with pandas outside the database, load only clean rows, target tables inside the database. ELT: source, extract, load the raw data unchanged into the database, transform there with SQL, target tables and views — load, transform and target are inside the database](img/etl-vs-elt.png){width=80%}

| | ETL | ELT |
|---|---|---|
| Transform in | a tool or script **outside** (pandas) | the **target database** (SQL) |
| Target receives | clean, conformed rows | **raw** data first |
| Fits | small targets, sensitive raw data, complex cleaning | powerful cloud warehouses, data lakes, "keep everything" |

::: source
Own illustration based on Serra (2024, Chapter 9) and Reis and Housley (2022, Chapter 7).
:::

::: notes
Serra (2024, Chapter 9) explains that ETL was the most common way to fill relational data warehouses, and that ELT became popular with data lakes and scalable cloud platforms, where loading raw data first is cheap and the database does the heavy lifting. Reis and Housley (2022, Chapter 7) discuss ETL versus ELT as a batch ingestion choice. Trade-offs: ELT keeps the raw history inside the platform (re-transform any time, new questions later) and uses SQL that many analysts know; but raw data — possibly personal data — sits in the target, and the database must be strong enough. ETL keeps the target clean and small. In practice most pipelines are a mix. Exam: be able to say where the T runs and name one advantage of each.
:::

---

# ELT in SQLite: Raw JSON In, SQL Out

```python
con.execute("INSERT INTO raw_weather VALUES (?, ?, ?, ?)",
            ("2026-10-21T10:00:00", "shop", json.dumps(params), body))   # body: the JSON text
```

```sql
SELECT substr(j.value ->> 'timestamp', 1, 10)      AS day,
       round(sum(j.value ->> 'precipitation'), 1) AS rain_mm,
       max(j.value ->> 'temperature')             AS t_max,
       count(*)                                   AS records
FROM raw_weather AS r, json_each(r.body, '$.weather') AS j
GROUP BY day;          -- 2026-10-08 | 11.9 | 18.0 | 24  … the same as pandas
```

- The **raw response** is stored once; the **T** is a query — or a **view** — that can be changed and rerun
- Trap: `date('2026-10-05T00:00:00+02:00')` gives **2026-10-04** — SQLite converts to **UTC**

::: source
Own example; SQLite (n.d.-a); weather data: Deutscher Wetterdienst via de Maeyer (n.d.).
:::

::: notes
All observed on the saved copy (body 35,948 characters, json_array_length 169). json_each (session 11) turns the weather array into rows; ->> extracts SQL values (SQLite 3.38 or newer; SQLite, n.d.-a). The query returns the same daily values as pandas in session 15: 0.0, 0.0, 0.0, 11.9, 0.9, 1.6, 0.2 mm, plus 2026-10-12 with 1 record. With date() instead of substr(), the days shift (observed): 2026-10-04 appears with 2 records, 8 October has 11.8 mm and 9 wet hours, 11 October only 23 records — date() treats "+02:00" as a time zone and returns the UTC date. A silent, plausible-looking error: exactly why every pipeline needs checks (records per day). The CHECK (json_valid(body)) on raw_weather rejects a body that is not JSON (e.g. an HTML error page).
:::

---

# Mini Exercise: ETL, ELT — Which Step? {.exercise}

1. Assign each activity to **E**, **T** or **L**: reading the S2 Excel sheet · renaming `Preis netto` to `price_eur` · `INSERT … ON CONFLICT` · converting `05.10.2026` to `2026-10-05` · saving the API response as a file · summing hourly rain per day
2. The web shop team wants to keep **every** raw order export for later questions nobody knows yet. ETL or ELT?
3. The till export contains customers' **names and e-mail addresses**, but the target only needs daily totals. ETL or ELT — and why?
4. Where does the transformation run in the SQL query on the previous slide?

::: notes
About 5 min in pairs, 3 min collection. Expected answers:
1 E: reading the Excel sheet, saving the API response (part of extraction: the landing zone). T: renaming the column, converting the date, summing per day. L: INSERT … ON CONFLICT. Saving the raw file is sometimes called "load to landing" — accept it with that reasoning; that is ELT thinking.
2 ELT (or at least: load raw first): keep the raw exports in the database or a data lake and transform later; questions nobody knows yet need the unchanged data. Cost: storage and a governance question — who may see raw data?
3 ETL: aggregate (and drop the personal data) before loading — data minimisation (GDPR, session 19). Loading names and e-mails raw into the analysis database just to sum them would spread personal data without need.
4 Inside the database (SQLite): ELT. The pandas version of session 15 is ETL.
:::

---

# Pipeline Design {.section}

From notebook cells to a process that runs every day

---

# Five Design Rules for a Pipeline

| Rule | Why | In our pipeline |
|---|---|---|
| **Steps as functions** | testable, rerunnable, schedulable | `extract()`, `transform()`, `load()` |
| **Raw stays raw** | repeat the T without asking the source again | `raw/weather_…json` |
| **Idempotent** | a rerun gives the **same** result, no duplicates | upsert on the primary key |
| **All or nothing** | no half-loaded tables | one transaction per load |
| **Every run leaves a trace** | notice errors, prove lineage | `etl_run`, `run_id` per row |

- Parameters (dates, location, file names) **in**, results **out** — no hidden notebook state
- Secrets and settings **outside** the code (session 15)

::: source
Based on Kimball and Ross (2013, Chapters 19–20), Reis and Housley (2022, Chapter 2) and Python Software Foundation (n.d.).
:::

::: notes
Idempotent: running the same operation twice has the same effect as running it once — the most important property of a pipeline, because pipelines are rerun all the time: after a failure, after a fix, by a second scheduler entry by mistake. Reis and Housley (2022, Chapter 2) list orchestration, DataOps and software engineering as "undercurrents" of the data engineering lifecycle: a pipeline is software and deserves tests, version control and monitoring. Notebook state: a notebook that only works when the cells run in a certain order, with variables left over from yesterday, is not a pipeline. A script `python weather_pipeline.py 2026-10-08 2026-10-11` is. The `with con:` block commits or rolls back (Python Software Foundation, n.d.; session 10).
:::

---

# Extract: Full or Incremental?

| | Full (snapshot) | Incremental (differential) |
|---|---|---|
| What | **everything**, every run | only what is **new or changed** since the last run |
| Needs | nothing | a **watermark**: last loaded date, ID or change time |
| Fits | small sources: two price lists | growing sources: weather, orders, trips |
| Risk | slow, heavy for the source | missed **corrections** and late data |

```python
last_loaded = con.execute("SELECT max(day) FROM weather_daily "
                          "WHERE station = 'Mannheim'").fetchone()[0]     # '2026-10-11'
first = last_loaded                                       # overlap: reload the last day
last = (dt.date.today() - dt.timedelta(days=1)).isoformat()                # yesterday
```

::: source
Based on Reis and Housley (2022, Chapter 7) and Kimball and Ross (2013, Chapter 19); own example.
:::

::: notes
Reis and Housley (2022, Chapter 7) discuss snapshot versus differential extraction. The watermark is read from the target itself, so the pipeline needs no extra state file. The overlap of one day is deliberate: recent observations can still be corrected (session 15: "stability"), and with an upsert reloading a day is harmless. Other watermarks: the highest order number, a "last_changed" timestamp (the web shop export of session 13 had one), or change data capture from a database log (Reis & Housley, 2022, Chapter 7) — beyond this course. Price lists come complete every quarter: a full extract is simpler and correct.
:::

---

# Extract and Transform: The Weather

```python
def extract(first, last):
    params = {**SHOP, "date": first, "last_date": f"{last}T23:00", "tz": "Europe/Berlin"}
    try:
        r = requests.get(URL, params=params, timeout=10); r.raise_for_status()
        data, source = r.json(), "api"
    except requests.RequestException:
        data, source = json.loads(Path(SAVED).read_text(encoding="utf-8")), "saved copy"
    Path(f"raw/weather_{first}_{last}_{stamp()}.json").write_text(json.dumps(data))
    return data, source

def transform(data, first, last):           # parse, filter, map, aggregate (session 15)
    w = pd.DataFrame(data["weather"])
    w["timestamp"] = pd.to_datetime(w["timestamp"], utc=True).dt.tz_convert("Europe/Berlin")
    w["day"] = w["timestamp"].dt.strftime("%Y-%m-%d")
    w = w[w["day"].between(first, last)]
    w["station"] = w["source_id"].map({s["id"]: s["station_name"] for s in data["sources"]})
    return w.groupby(["station", "day"], as_index=False).agg(…)   # rain_mm, wet_hours, …
```

::: source
Own example based on session 15; Requests (n.d.); McKinney (2022, Chapters 6 and 10).
:::

::: notes
Shortened on the slide (stamp() returns the current time as text; the agg is the one of session 15 plus sunshine_h and records). Observed for 5–8 October: four rows Mannheim with rain 0.0, 0.0, 0.0, 11.9 mm, t_max 23.8, 24.3, 24.0, 18.0, sunshine 10.7, 10.6, 9.4, 0.4 h, 24 records each. Three design points: (1) last_date with T23:00 avoids the extra midnight record; (2) the filter on first..last makes the transform correct even when the saved copy covers more days; (3) the station name comes from the response, not from our assumption — lineage. utc=True plus tz_convert is safe across the change to winter time (25 October 2026). The day is stored as ISO text for SQLite (session 7).
:::

---

# Integrating Two Price Lists: Map the Schema

| Target `supplier_price` | S1 (CSV) | S2 (Excel) |
|---|---|---|
| `supplier_no` | — (constant `'S1'`) | — (constant `'S2'`) |
| `item_no` | `Artikel-Nr.` (text: `004711`) | `Item no` |
| `description` | `Bezeichnung` (German) | `Description` (English) |
| `part_no` → `spare_part` | `Ihre Teile-Nr.` | `Your part no` |
| `price_eur` | `Preis netto` (`3,05`) | `Price EUR` (`on request`) |
| `pack_size` | `VPE` | `Pack` |
| `valid_from` | `Gültig ab` (`01.04.2027`) | `Available from` (Excel date) |
| — | `Lagerbestand` (dropped) | — |

- One **target schema**, one **mapping per source** — the mapping is documentation, too
- The supplier's article number is **not** our key: `part_no` links to `spare_part`, if the shop stocks the item

::: source
Own example (fictional supplier price lists); based on Rahm and Do (2000) and DAMA International (2017, Chapter 8).
:::

::: notes
The mapping table is the core of data integration and a good format for the project documentation. Decisions hidden in it: the composite key (supplier_no, item_no) — two suppliers may use the same article number; descriptions stay in the supplier's language (translation would be a new source of errors); Lagerbestand is dropped because S2 has no stock column and stock is not needed for price comparison — a conscious decision, write it down. Is valid_from the same concept as "available from"? Not quite: one is a price validity date, the other an availability date — a semantic conflict (Rahm & Do, 2000) that the team must accept or ask about.
:::

---

# Integrating Two Price Lists: The Code

```python
MAP_S1 = {"Artikel-Nr.": "item_no", "Bezeichnung": "description", "Ihre Teile-Nr.": "part_no",
          "Preis netto": "price_eur", "VPE": "pack_size", "Gültig ab": "valid_from"}
MAP_S2 = {"Item no": "item_no", "Description": "description", "Your part no": "part_no",
          "Price EUR": "price_eur", "Pack": "pack_size", "Available from": "valid_from"}
p = pd.concat([s1.rename(columns=MAP_S1).assign(supplier_no="S1"),
               s2.rename(columns=MAP_S2).assign(supplier_no="S2")])[COLS]
p["price_eur"] = pd.to_numeric(p["price_eur"], errors="coerce")    # 'on request' → NaN
p["valid_from"] = p["valid_from"].dt.strftime("%Y-%m-%d")
```

- **13** articles: 8 from S1, 5 from S2 — **9** linked to a spare part, **4** not stocked
- EM-D28 has **no price** ("on request") — loaded as `NULL`, not as 0
- Now one query compares: battery P-109 — list price **649.00**, S2 **449.00**: margin **30.8 %**

::: source
Own example (fictional supplier price lists); McKinney (2022, Chapters 6 and 8); pandas development team (n.d.).
:::

::: notes
s1 and s2 are read exactly as in session 15 (read_csv with sep, encoding, decimal, thousands, dtype, na_values, parse_dates; read_excel with header=3, nrows=5). All observed: shape (13, 7); part_no missing for 099017 Werkstattkoffer, EM-625, EM-CH4, EM-D28; NaN in pandas arrives as NULL in SQLite (observed typeof null) — the FK on part_no accepts NULL. Margin query (spare_part JOIN supplier_price): lowest margins P-109 30.8 %, P-108 44.2 %, P-105 46.4 %; highest P-110 bell 64.0 %. Spare parts without any supplier price: P-102, P-104, P-112 — the next purchasing task. Without the column mapping, concat would produce 13 columns with NaN blocks (worksheet 15 had this with the coworking invoices).
:::

---

# Load: Replace, Append or Upsert?

| Strategy | What it does | Rerun of 8–11 Oct after 5–8 Oct |
|---|---|---|
| `to_sql(…, if_exists="replace")` | drops the table, creates a **new one** | constraints **gone**; only the last run's rows |
| `to_sql(…, if_exists="append")` | adds all rows | with a PK: **UNIQUE constraint failed**, 0 rows; without: **duplicates** |
| **Upsert** `INSERT … ON CONFLICT DO UPDATE` | inserts new keys, **updates** existing ones | **7** rows; 8 Oct updated |

- Upsert needs a **primary key** (or `UNIQUE`) that says when two rows are **the same thing**
- Full extracts of small tables: delete and insert in **one transaction** is also idempotent

::: source
Based on SQLite (n.d.-b), pandas development team (n.d.) and Kimball and Ross (2013, Chapter 19); own example.
:::

::: notes
All observed. replace: `to_sql(..., if_exists="replace")` dropped weather_daily and created a table without primary key, CHECK constraints and foreign key (CREATE TABLE "weather_daily" ("station" TEXT, "day" TEXT, …)); a following append then doubled the rows (4 → 8 with duplicates). append with the PK: pandas raised DatabaseError "Execution failed" caused by IntegrityError UNIQUE constraint failed: weather_daily.station, weather_daily.day, and nothing was stored (one transaction; session 14 saw the same with a foreign key). pandas 3 also offers if_exists="delete_rows" (keeps the table, deletes all rows, then inserts; pandas development team, n.d.) — idempotent for full extracts. Ask: which strategy fits the price lists? (upsert or delete+insert per supplier — but think about articles that disappear from a list: upsert keeps them.)
:::

---

# Upsert: Run It Twice, Get the Same Table

```python
UPSERT = """
INSERT INTO weather_daily (station, day, rain_mm, wet_hours, t_max, sunshine_h, records, run_id)
VALUES (:station, :day, :rain_mm, :wet_hours, :t_max, :sunshine_h, :records, :run_id)
ON CONFLICT (station, day) DO UPDATE SET
    rain_mm = excluded.rain_mm, wet_hours = excluded.wet_hours, t_max = excluded.t_max,
    sunshine_h = excluded.sunshine_h, records = excluded.records, run_id = excluded.run_id"""

def load(con, daily, run_id):
    rows = daily.assign(run_id=run_id).to_dict("records")
    with con:                                    # one transaction: all rows or none
        con.executemany(UPSERT, rows)
    return len(rows)
```

| Run | Days asked | Rows in `weather_daily` afterwards |
|---|---|---|
| 1 | 5–8 Oct | 4 |
| 2 | 8–11 Oct | **7** (8 Oct updated, not doubled) |
| 3 | 8–11 Oct again | **7** — idempotent |

::: source
Based on SQLite (n.d.-b) and Python Software Foundation (n.d.); own example.
:::

::: notes
All observed. `excluded.` refers to the row that would have been inserted (SQLite, n.d.-b); UPSERT exists since SQLite 3.24. Named placeholders (:station) take the values from the dictionaries of to_dict("records") — pandas returns plain Python numbers there, which sqlite3 can bind. After run 3, the days 8–11 October carry run_id 3: the row says which run wrote it last (lineage). With real data a rerun can change values (DWD corrections) — the upsert takes the newest. A refinement: `DO UPDATE … WHERE excluded.rain_mm IS NOT weather_daily.rain_mm` only touches changed rows (SQLite, n.d.-b shows a WHERE on DO UPDATE).
:::

---

# Mini Exercise: What If …? {.exercise}

For each case: what happens in **our** pipeline — and is that what we want?

1. The scheduler starts the pipeline **twice** at 06:15 by mistake
2. The load fails on the **third** of four rows (a `CHECK` violation)
3. The API is down for **three days**; the saved copy covers only 5–11 October
4. Supplier S1 renames `Preis netto` to `Nettopreis` in the next price list
5. On **25 October 2026** (summer time ends) the day has **25** hourly records

::: notes
About 5 min in pairs, 3 min collection. Expected answers (our pipeline as on the slides):
1 Both runs upsert the same keys: same rows, last run_id wins — idempotent, no harm (two entries in etl_run show it).
2 One transaction: the whole load is rolled back, 0 rows from this run (observed with rain_mm = −1 in the third row: IntegrityError CHECK constraint failed: rain_mm >= 0, table unchanged); the exception goes up, the run is logged as failed — wanted: no half-loaded table. Fix the data or the rule, rerun.
3 Each run falls back to the saved copy: days after 11 October are missing → our validation reports "days missing" (next slides). Wanted? Only if somebody reads the warning; the incremental watermark then catches up when the API is back.
4 Observed: no error at all. rename ignores the unknown name, and after concat the column price_eur exists anyway (from S2), so all 8 S1 prices become NaN → loaded as NULL, which our schema reads as "price on request". A silent, wrong load — not wanted. A schema check before the transform (expected columns present in each source) must stop the run (next slides).
5 Our check "records == 24" would reject a correct day; 29 March has 23 records. The rule must use the expected number of hours of the local day (worksheet 16 challenge). Good students mention that UTC days would avoid the problem — but the shop works in local days.
:::

---

# Scheduling and Monitoring {.section}

What runs when — and how we notice errors

---

# Scheduling: Who Starts the Pipeline?

| Option | How | Fits |
|---|---|---|
| **By hand** | run the notebook or script | one-off loads, development |
| **cron** (Linux, macOS) | `15 6 * * * python /etl/weather_pipeline.py` | one script, one machine |
| **Windows Task Scheduler** | a task with a daily trigger | the same on Windows |
| **Orchestrator** (e.g. Airflow) | tasks with **dependencies**, retries, history | many pipelines that depend on each other |

- **Time-based** (every day at 06:15) or **event-based** (when a new price list arrives)
- **Dependencies**: `supplier_price` before the margin report; weather and till before the join
- Schedule **after** the source is complete: yesterday's weather, not today's

::: source
Based on The Open Group (2018), Apache Software Foundation (n.d.) and Reis and Housley (2022, Chapter 2).
:::

::: notes
The crontab line has five time fields — minute, hour, day of month, month, day of week — followed by the command (The Open Group, 2018): "15 6 * * *" means 06:15 every day. A scheduled job needs a script, not a notebook: absolute paths, no interactive input, output into a log file. Orchestration is one of the undercurrents of Reis and Housley (2022, Chapter 2): a tool that knows the tasks, their order and their state. In Airflow, a DAG (directed acyclic graph) collects tasks "organized with dependencies and relationships" and says how often to run (Apache Software Foundation, n.d.). For the project, by hand or one scheduled script is enough. Event-based: a file arriving in a folder, a webhook (session 15).
:::

---

# Monitoring: Every Run Leaves a Trace

```python
run_id = start_run(con, "weather")             # INSERT INTO etl_run … status 'running'
try:
    data, source = extract(first, last)
    good, bad, problems = validate(transform(data, first, last), first, last)
    n = load(con, good, run_id)
    finish_run(con, run_id, "warning" if problems else "ok", source, …, "; ".join(problems))
except Exception as e:
    finish_run(con, run_id, "failed", message=f"{type(e).__name__}: {e}"); raise
```

| run | status | source | loaded | rejected | message |
|---|---|---|---|---|---|
| 3 | ok | saved copy | 4 | 0 | |
| 4 | **warning** | saved copy | 1 | 1 | days missing: 2026-10-13 … 2026-10-21; incomplete days not loaded: 2026-10-12 |
| 5 | **failed** | | | | FileNotFoundError: … `missing.json` |

::: source
Own example; based on Kimball and Ross (2013, Chapter 19) and Reis and Housley (2022, Chapter 2).
:::

::: notes
All observed. Run 4 is the incremental run of the "Extract" slide on 22 October 2026 (watermark 2026-10-11, last = yesterday 2026-10-21): the API was not reachable, the saved copy ends on 12 October 00:00 → 11 October reloaded (overlap), 12 October rejected (1 of 24 records), 13–21 October missing. Without the run log, the table would simply look "fine" — the stale fallback would be invisible (timeliness, session 13). Run 5 was provoked by pointing the fallback to a file that does not exist: the run is logged as failed and the error still goes up, so the scheduler shows it too. "failed" must never look like "ok": a pipeline that swallows errors is worse than one that crashes. Live API users see run 4 as "ok" with 11 days.
:::

---

# Checks That Catch Problems

| Check | Question | Bike shop example | If it fails |
|---|---|---|---|
| **Freshness** | is the newest data recent enough? | `max(day)` = 11 Oct, today 22 Oct | warn |
| **Volume** | as many rows as expected? | 24 records per day; 13 price list rows | reject the day / stop |
| **Schema** | are all expected columns there? | `Preis netto` still in S1's file | stop |
| **Validity** | do values pass the rules? | `rain_mm >= 0`, valid dates | reject the row |
| **Integrity** | keys unique, references exist? | PK, FK `part_no` → `spare_part` | the database refuses |

- **Stop** when the whole batch is suspicious; **reject and log** single bad rows; **warn** and load when it is usable
- Somebody must **read** the result: a daily look at `etl_run`, or an e-mail on `failed`

::: source
Based on Kimball and Ross (2013, Chapter 19), DAMA International (2017, Chapter 13) and Wang and Strong (1996).
:::

::: notes
Freshness observed: `SELECT max(day), julianday('2026-10-22') - julianday(max(day)) FROM weather_daily` → 2026-10-11, 11 days. These are the data quality dimensions of session 13 (timeliness, completeness, validity, consistency; Wang & Strong, 1996) turned into automatic checks that run with every load — monitoring is measurement on a schedule (DAMA International, 2017, Chapter 13). Kimball and Ross (2013, Chapter 19) place quality checks, and structures that record quality errors, inside the ETL system itself. The integrity line is the "two lines of defence" of session 14: pandas checks report, constraints guarantee. Who reads the log is an organisational question (data steward, session 19). Alerting tools are beyond the course; `SELECT * FROM etl_run WHERE status <> 'ok'` every morning is a start.
:::

---

# Orchestrators and DAGs {.optional}

- A **DAG** (directed acyclic graph): tasks as nodes, **dependencies** as arrows, no cycles
- The orchestrator starts tasks **in order**, **retries** failed ones, keeps the **history**, shows the state
- Bike shop as a DAG: `extract_weather → load_weather` and `extract_till → load_till`, then `weather_vs_till_report`
- Examples: Apache Airflow, Dagster, Prefect; transformations inside the database are often managed with dbt

::: source
Based on Apache Software Foundation (n.d.) and Reis and Housley (2022, Chapter 2).
:::

::: notes
Self-study. Airflow defines a DAG as the collection of tasks organised with dependencies and relationships; the DAG also says how often to run and how often tasks are retried (Apache Software Foundation, n.d.). Tools are named without endorsement; none is needed for the course. Why a DAG and not one long script: independent branches can run in parallel, and after a failure only the failed task and its successors are rerun. dbt is a common tool for the ELT pattern: SQL SELECT statements become managed tables and views — the same idea as the SQL on the ELT slide.
:::

---

# Exercise: The Bike Shop Pipeline {.exercise}

New notebook (or script). Load `bikeshop-etl-session16.sql`. Predict first, then run.

1. **Functions**: turn your session 15 code into `extract(first, last)` and `transform(data, first, last)`; check the result for 5–8 October
2. **Load**: write `load()` with the upsert. Load 5–8, then 8–11 October. How many rows — and why not 8?
3. **ELT**: store the raw response in `raw_weather` and compute the daily values with SQL. Same result? Try `date()` instead of `substr()`
4. **Price lists**: map S1 and S2 to `supplier_price` and load them. Which parts have no supplier price? Which supplier price is the cheapest per part?
5. **Till**: load the till export as `till_daily` (ISO dates!) and join it with `weather_daily`. Compare test rides on "bad bike days" (session 15) with the other days
6. **Run log**: wrap everything in `run_weather()` with `etl_run`. Run it twice, run it incrementally, provoke a failure — then read `etl_run`

::: source
Own example; API: de Maeyer (n.d.); data: Deutscher Wetterdienst, CC BY 4.0; supplier and till data fictional.
:::

::: notes
About 40 min + 5 min comparison. Expected answers (all observed on the saved copy):
1 Four rows Mannheim, 24 records each; rain 0.0, 0.0, 0.0, 11.9; t_max 23.8, 24.3, 24.0, 18.0.
2 4, then 7: 8 October exists already and is updated (upsert on station, day). With append: UNIQUE constraint failed, 0 rows from that run.
3 Same daily values; date() shifts to UTC days (2026-10-04 with 2 records, 8 Oct 11.8 mm, 11 Oct 23 records). raw_weather keeps the response with retrieval time and parameters.
4 13 rows, 9 linked; spare parts without a supplier price: P-102 tyre, P-104 chain 9-speed, P-112 mudguard set. Each linked part has exactly one supplier in these two lists (S1 or S2), so "cheapest" is trivial today — the query (GROUP BY part_no with min(price_eur)) matters when S3 sends a list. Margins from 30.8 % (P-109) to 64.0 % (P-110). Good groups notice pack sizes (P-111 pack of 5 — price per piece?).
5 read_csv(sep=";", decimal=",", thousands=".", parse_dates=["Datum"], date_format="%d.%m.%Y"), rename, strftime("%Y-%m-%d"). LEFT JOIN from weather_daily: Sunday 11 October has no till row (closed — not missing data). Bad bike days (≥ 1 mm or < 15 °C) Thu, Fri, Sat: on average 30.7 walk-ins, 3.7 test rides, 2,830.13 € revenue vs. 41.0, 7.0, 3,458.80 € on the three dry days. But Saturday (1.6 mm) was the best day of the week: the weekday matters more than 1.6 mm of rain — one week proves nothing; we need months of data, which is why the pipeline runs daily. This question leads to session 17 (facts and dimensions such as date and weather).
6 etl_run as on the monitoring slide: two ok runs with the same row count; incremental run → warning with missing days (or ok with the live API); failure → status failed with the message. Good groups also log the price list run.
:::

---

# Team Work: Your Pipeline for Milestone 4 {.exercise}

1. Draw your pipeline: **sources**, landing, transformation steps, **target tables**, run log
2. ETL or ELT — where does each transformation run, and why?
3. Full or **incremental**? What is your **watermark**, and what makes a rerun **idempotent**?
4. Which **three checks** run with every load, and what happens when one fails?
5. How often should it run — and who notices a failure?

::: callout
Milestone 4 (data loading and quality): your data **loaded with Python** into your project database, with cleaning steps, checks and a short pipeline description.
:::

::: notes
About 12 min. Teams draw on paper or in draw.io; walk around and ask: what happens if you run your notebook twice? Which key decides that two rows are the same? A good answer names a primary key for the upsert, a landing folder for raw files and one check per quality dimension from session 13. Milestone 4 is due after today; the exact deliverables are in the project brief. Teams whose data is a one-off download: full extract plus delete-and-insert is fine — say so explicitly.
:::

---

# Key Takeaways

- **Data integration** brings data from many sources into one place and one format — schema, formats, keys and meaning must be **mapped**
- **ETL** transforms **before** loading; **ELT** loads **raw** data and transforms **inside** the database
- A pipeline is **functions**, **raw data kept**, **parameters** — not notebook state
- Extract **full** or **incremental** (watermark); load **idempotently** (upsert on a key) in **one transaction**
- **Schedule** it, **log** every run, **check** freshness, volume, schema and validity — and make sure someone reads the result

---

# Next Session: Data Warehousing

- Why a **data warehouse**: analysis apart from the operational systems
- **Inmon** vs. **Kimball**
- **Star** and **snowflake** schema: **fact** and **dimension** tables
- **OLAP**: slicing and dicing
- Hands-on: a star schema for the project case

::: callout
**Preparation:** finish the hands-on and worksheet 16; keep `bikeshop.db` with `weather_daily` and `till_daily`. Think: if the shop wants revenue **per day, per weather type and per product group**, which tables would you build?
:::

---

# References {.references}

- Apache Software Foundation. (n.d.). *DAGs*. Apache Airflow 2.11.2 documentation. Retrieved October 22, 2026, from https://airflow.apache.org/docs/apache-airflow/2.11.2/core-concepts/dags.html
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- pandas development team. (n.d.). *pandas.DataFrame.to_sql*. pandas 3.0.6 documentation. Retrieved October 22, 2026, from https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html
- Python Software Foundation. (n.d.). *sqlite3 — DB-API 2.0 interface for SQLite databases*. Retrieved October 22, 2026, from https://docs.python.org/3/library/sqlite3.html
- Rahm, E., & Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.
- Reis, J., & Housley, M. (2022). *Fundamentals of data engineering: Plan and build robust data systems*. O'Reilly Media.

---

# References (continued) {.references}

- Requests. (n.d.). *Quickstart*. Requests 2.34.2 documentation. Retrieved October 21, 2026, from https://requests.readthedocs.io/en/latest/user/quickstart/
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
- SQLite. (n.d.-a). *JSON functions and operators*. Retrieved October 22, 2026, from https://www.sqlite.org/json1.html
- SQLite. (n.d.-b). *UPSERT*. Retrieved October 22, 2026, from https://www.sqlite.org/lang_upsert.html
- The Open Group. (2018). *crontab — schedule periodic background work*. The Open Group Base Specifications Issue 7, 2018 edition (IEEE Std 1003.1-2017). https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html
- Vassiliadis, P. (2009). A survey of extract–transform–load technology. *International Journal of Data Warehousing and Mining, 5*(3), 1–27. https://doi.org/10.4018/jdwm.2009070101
- Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33. https://doi.org/10.1080/07421222.1996.11518099
