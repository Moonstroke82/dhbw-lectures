---
course: Data Management
session: 15
title: Accessing Data: Files and APIs
subtitle: Practice tasks on reading CSV, Excel and JSON, REST APIs and status codes, calling APIs from Python, authentication and rate limits
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 15 on your own or with your project team. Tasks 1 and 4 and the exam-style task can be done on paper. For the lab tasks you need Jupyter with pandas, requests and openpyxl (`python -m pip install pandas requests openpyxl`) and these files: the coworking space's member export [coworking-members-session15.csv](data/coworking-members-session15.csv) and invoices [coworking-invoices-session15.xlsx](data/coworking-invoices-session15.xlsx), the food co-op's orders from worksheet 11 [foodcoop-orders-session11.json](data/foodcoop-orders-session11.json), and the saved weather response for Heidelberg [brightsky-heidelberg-2026-09-28.json](data/brightsky-heidelberg-2026-09-28.json). The weather data are real observations of the Deutscher Wetterdienst (DWD), retrieved through the Bright Sky API (de Maeyer, n.d.) on 21 October 2026 and trimmed to nine fields per record; they are licensed under CC BY 4.0 (Deutscher Wetterdienst, 2024). All other names and data are fictional. The in-class hands-on uses [brightsky-mannheim-2026-10-05.json](data/brightsky-mannheim-2026-10-05.json) and the supplier price lists [bikeshop-pricelist-s1-session15.csv](data/bikeshop-pricelist-s1-session15.csv) and [bikeshop-pricelist-s2-session15.xlsx](data/bikeshop-pricelist-s2-session15.xlsx). The terms follow the session slides, which are based on McKinney (2022, Chapter 6), the pandas documentation (pandas development team, n.d.), the Requests documentation (Requests, n.d.), Fielding (2000), RFC 9110 (Fielding et al., 2022) and RFC 6585 (Nottingham & Fielding, 2012). The results in the solutions were produced with Python 3.13, pandas 3.0.6, requests 2.34.2 and openpyxl 3.1.5; with pandas 2.x, text columns show the dtype `object` instead of `str`.

```python
import json
import pandas as pd
import requests
```

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. `pd.read_csv` detects the separator and the decimal mark of a file automatically.
2. Reading a column of postcodes or article numbers with `dtype=str` keeps leading zeros such as `01067`.
3. A status code **404** means that the server has a problem; trying again a few minutes later usually helps.
4. In REST, a `GET` request reads a resource without changing it.
5. If no `timeout` is given, `requests.get` gives up after 30 seconds.
6. `r.json()` raises an error whenever the server answers with a 4xx or 5xx status code.
7. An API key should be stored in an environment variable or a local file that is not committed — not in the notebook.
8. Data published as open data may be used without naming the source.

::: answer lines=10
:::

::: solution
1. **False.** Without arguments, `read_csv` assumes `,` as separator and `.` as decimal mark; a German export needs `sep=";"` and `decimal=","` (`sep=None` lets pandas guess the separator, but nothing guesses the decimal mark).
2. **True.** As text the value stays `'01067'`; read as a number it becomes 1067 (or 1067.0 if the column has missing values).
3. **False.** 404 is a client error (4xx): the resource or endpoint does not exist — fix the URL or the ID. Retrying later helps with 5xx errors and with 429.
4. **True.** GET is the method for reading; it does not change data and can be repeated (Fielding et al., 2022).
5. **False.** Without `timeout`, requests do not time out at all (Requests, n.d.); a hanging server makes the script wait indefinitely.
6. **False.** `r.json()` parses any JSON body, including error messages such as `{"detail": "Not Found"}`. Check `r.status_code` or call `r.raise_for_status()` first.
7. **True.** Keys are secrets; a key in a notebook ends up in shared folders and repositories.
8. **False.** Open data comes with a licence; CC BY 4.0, for example, requires naming the source, linking the licence and indicating changes (Creative Commons, n.d.).

Marking: one point per statement; for false statements, the point requires a correct correction.
:::

## Lab: Read the Coworking Space's Files Right

The coworking space exports its member list from an old booking tool and keeps its invoices in an Excel workbook with one sheet per month. Open both files in a text editor or Excel first and look at them. Predict each result before you run it.

**Member list (CSV)**

1. Run `pd.read_csv("coworking-members-session15.csv")`. What happens? Then try `sep=";"`. Why is the result still wrong? Look at the first line of the file.
2. Read the file with `sep=";", skiprows=1`. Give the `dtypes`. Which columns have the wrong type, and what has already been lost?
3. Write the call that reads all columns with the right type (fees as numbers, dates as dates, codes as text). How many fees are missing, and what is the sum of the monthly fees? Is the missing fee of **M3** the same kind of "missing" as the missing postcode of **M4**?

**Invoices (Excel)**

4. Run `pd.read_excel("coworking-invoices-session15.xlsx")`. Which sheet did pandas read, and what became the header?
5. Read **all** sheets with the correct header row into one DataFrame with a column `month`. How many rows and columns do you get — and why are there more columns than you expected? Fix it.
6. Check the invoices: total per month, open (unpaid) amount, and anything that looks wrong. Compare the amounts with the members' monthly fees.

::: hint
`header` counts rows from 0. `sheet_name=None` returns a dictionary `{sheet name: DataFrame}`; `pd.concat(sheets, names=["month", "row"])` stacks them and keeps the sheet name in the index — `reset_index(level="month")` turns it into a column. A dictionary in `rename(columns=...)` aligns different column names.
:::

::: answer lines=18
:::

::: solution
All results observed with pandas 3.0.6 on exactly these files.

1. `ParserError: Error tokenizing data. C error: Expected 1 fields in line 3, saw 2`. With `sep=";"`: shape (9, 2) with the columns `'sep='` and `'Unnamed: 1'` — pandas took the first line `sep=;` as the header. That line is an Excel hint ("the separator is ;"), not data.
2. `member_no` str, `name` str, `plan` str, **`monthly_fee` str** (decimal comma, `1.089,00`), **`start_date` str**, **`badge_no` int64** (`0007` → 7: leading zeros lost), **`postcode` float64** (68159.0; `01067` → 1067.0 because one value is missing). Missing: `monthly_fee` 2 (`n/a` is a default missing-value marker), `postcode` 1.
3. ```python
   m = pd.read_csv("coworking-members-session15.csv", sep=";", skiprows=1,
                   decimal=",", thousands=".", dtype={"badge_no": str, "postcode": str},
                   parse_dates=["start_date"], date_format="%d.%m.%Y")
   ```
   `monthly_fee` float64 (1,089.0 for M9), `start_date` datetime64, `badge_no` and `postcode` str with leading zeros. 2 fees missing (M3, M8); sum **2,334.00 €** from 6 members. No: M3 and M8 are on the DAY plan and pay per day — "not applicable", a known meaning that may be filled with 0 **for "fixed monthly revenue"** with a documented rule. M4's postcode is **unknown** — a completeness gap; ask the member. `n/a` hides the difference; a separate value (e.g. `"DAY"` → no fee) or `keep_default_na=False` plus a rule keeps it visible. The file is UTF-8 with a byte order mark (`Öztürk` reads correctly with the default encoding).
4. Only the **first** sheet, `2027-01`; the title "Invoices January 2027" became the header (shape (9, 4), columns `'Invoices January 2027'`, `'Unnamed: 1'` …).
5. ```python
   sheets = pd.read_excel("coworking-invoices-session15.xlsx", sheet_name=None, header=2)
   inv = pd.concat(sheets, names=["month", "row"]).reset_index(level="month").reset_index(drop=True)
   ```
   → (23, **9**): the February sheet uses the headers `Invoice`, `Member`, `Amount (EUR)`, `Paid`; concat puts them in their own columns, with `NaN` for the other months (8 and 15 missing values). Fix: rename before concatenating:
   ```python
   ren = {"Invoice": "invoice_no", "Member": "member_no", "Amount (EUR)": "amount_eur", "Paid": "paid"}
   sheets = {k: v.rename(columns=ren) for k, v in sheets.items()}
   ```
   → (23, 5).
6. Totals: 2027-01 **1,253**, 2027-02 **2,424**, 2027-03 **3,438** (amounts are int64: all whole euros). Open: **3,323 €** in 7 invoices (M2 289, M4 567, M7 289, M9 2,178); M4 has not paid in any month — a dunning case. Findings: **M9 invoiced twice** in March (R-2723 and R-2724, 1,089 € each) — a uniqueness problem, ask before cancelling one; invoice number **R-2722 is missing** (cancelled or lost?); **M7's January invoice is 177 €** instead of 289 € — plausible pro rata for a start on 13 January (19 of 31 days: 289 × 19/31 ≈ 177.1); M3 and M8 (DAY) have varying amounts by design; M8 has no March invoice (no usage, or forgotten?). A merge with the member list (`inv.merge(m, on="member_no", how="left", indicator=True)`) finds no unknown member.

Marking: one point per question; in 3 the point requires the distinction between "not applicable" and "unknown".
:::

## From Documents to Tables: The Food Co-op's Orders

In worksheet 11 you queried the food co-op's order documents with SQL. Now load them into pandas.

1. Load the file with `json.load` and turn it into **one row per order** with `pd.json_normalize`. Which columns come from nested objects, and which column exists only because of a single document?
2. Build **one row per item**, with order number, pick-up location, paid flag and the member's name copied into each row. How many rows do you get? Which order is missing, and why?
3. Compute the revenue per farm. Check your result against worksheet 11 — what must you fix first?
4. Which **types** do the copied columns `order_no` and `paid` get, and why does that matter for the next step (joins, SQLite)?

::: answer lines=12
:::

::: solution
Observed with pandas 3.0.6.

```python
with open("foodcoop-orders-session11.json", encoding="utf-8") as f:
    orders = json.load(f)
o = pd.json_normalize(orders)
items = pd.json_normalize(orders, record_path="items",
                          meta=["order_no", "pickup", "paid", ["member", "name"]])
items["quantity"] = items["quantity"].fillna(items["qty"])
items["revenue"] = items["price"] * items["quantity"]
items.groupby("farm")["revenue"].sum()
```

1. `o` has shape (8, 9): `member.member_no`, `member.name` and `member.phone` come from the nested object `member`; `items` stays a column of lists. `member.phone` exists only because order 7 (Lotte Hahn) has a phone number — 7 of 8 values are `NaN`. `note` exists only in orders 3 and 5. Schema-on-read (session 11): the columns come from the data, not from a schema.
2. **15** rows, columns `product`, `farm`, `price`, `quantity`, **`qty`**, `order_no`, `pickup`, `paid`, `member.name`. Order **5** is missing: its `items` array is empty (cancelled), so it produces no row — like an inner join.
3. Without fixing: Imkerei Kraichgau **7.5**, because order 6 has `"qty": 2` instead of `"quantity"` and its revenue is `NaN`, which `sum()` skips. After `fillna(items["qty"])`: Ziegenhof Odenwald 27.7, Obsthof Bergstraße 24.8, **Imkerei Kraichgau 22.5**, Hofgut Neckarblick 17.2, Gärtnerei Sonnenfeld 1.5; total **93.7** — the same as the corrected SQL in worksheet 11.
4. Both come back as **object** (not int64 and bool). A merge on `order_no` with an int64 column fails or matches nothing, and `paid` must be converted (`astype(bool)`) before writing 0/1 into SQLite. Convert meta columns right after normalising.

Marking: one point per question.
:::

## Read the API Documentation: The Car-Sharing Partner API

The car-sharing company offers its partners (e.g. the city's mobility office) an API. Extract of the documentation:

| | |
|---|---|
| Base URL | `https://api.carshare.example/v2` |
| Endpoint | `GET /trips?from=YYYY-MM-DD&to=YYYY-MM-DD&page=N&per_page=N` |
| Paging | `per_page` 1–100, default 25; the response has `data`, `page`, `total` and `next` (the URL of the next page, or `null`) |
| Authentication | header `X-API-Key: <your key>`; one key per partner |
| Rate limit | 60 requests per minute per key; above that **429** with `Retry-After` in seconds |
| Errors | 400 invalid parameters · 401 missing or invalid key · 403 key not allowed for this endpoint · 503 maintenance |

1. Write the request (URL and header) for all trips of **June 2027** with the largest page size.
2. The first response says `"total": 2340`. How many requests do you need with `per_page=100` — and with the default? Can either loop hit the rate limit?
3. What should a client do on **401**, **403**, **429** and **503**? Which of them make sense to retry automatically?
4. After the loop, how do you check that you really received **all** trips?
5. Name two pieces of information that are **not** in this extract, but that you would need before building a pipeline on this API.

::: answer lines=14
:::

::: solution
1. `GET https://api.carshare.example/v2/trips?from=2027-06-01&to=2027-06-30&page=1&per_page=100` with the header `X-API-Key: <key>`. In Python: `requests.get(BASE + "/trips", params={"from": "2027-06-01", "to": "2027-06-30", "page": 1, "per_page": 100}, headers={"X-API-Key": key}, timeout=10)`. Whether `to` is inclusive is not stated — check it (see 5).
2. 2,340 / 100 → **24** requests (23 full pages, the last with 40 trips). Default 25 → 2,340 / 25 = 93.6 → **94** requests. With 24 requests the limit of 60 per minute is not reached; 94 requests sent as fast as possible **can** exceed it — after 60 requests the API answers 429; wait `Retry-After` seconds or pause about one second between requests. Using the largest page size is the polite choice.
3. **401**: check the key (typo, expired, not sent in the header) — do not retry unchanged. **403**: the key is valid but has no right for this endpoint — ask the provider for access; no retry. **429**: wait as long as `Retry-After` says, then retry the same request — automatic. **503**: maintenance — retry later with a growing pause and a maximum number of attempts — automatic. Only 429 and 5xx are worth retrying (Fielding et al., 2022; Nottingham & Fielding, 2012).
4. Compare the number of collected trips with `total` (2,340) and check that the last response had `"next": null`; also check that `trip_id` is unique (a page fetched twice after a retry would create duplicates). If the data changes during the download, `total` can differ — then repeat or fetch by smaller date ranges.
5. Any two, e.g.: the **fields and units** of a trip record (distance in km? times in which time zone?); whether `to` is **inclusive**; the **licence or terms of use** (may the city publish the data?); whether **personal data** (member numbers) is included (GDPR, session 19); how long data is available and how corrections are delivered; versioning (what happens when v3 comes).

Marking: one point per question; in 2 both numbers and the rate-limit reasoning are needed.
:::

## Lab: Rain at Training? The Sports Club and the Bright Sky API

The sports club from worksheets 13 and 14 trains outdoors in Heidelberg on **Tuesdays and Thursdays from 18:00 to 20:00**. The board wants to know whether training was affected by rain in the week of 28 September 2026 — and whether the weather data is good enough to decide in future.

1. **Call**: request `https://api.brightsky.dev/weather` for lat 49.41, lon 8.69 from 2026-09-28 to 2026-10-05 in German local time. If the API is not reachable, load the saved copy. How many records do you get, and how many **sources** are listed? Give their names and distances.
2. **Table**: build a DataFrame with `pd.json_normalize(data["weather"])`. Which columns appear because of the nested field `fallback_source_ids`, and why does `fallback_source_ids.condition` have the type `float64`?
3. **Lineage**: from which station do the **temperature**, the **precipitation** and the **condition** values come? What does this mean for a statement like "it was 28.8 °C in Heidelberg"?
4. **Training**: precipitation is the amount over the **previous** hour. Which records describe the training sessions? Was there rain during training on Tuesday 29 September and Thursday 1 October?
5. **Consistency**: count the hours in which `condition` and `precipitation > 0` disagree. How many of them have a `condition` taken from **another** station?
6. **Fitness for use**: write three sentences for the board — is this data good enough to decide whether training takes place, and what would you change?

::: hint
`pd.DataFrame(data["sources"])` shows the stations. `w["timestamp"].dt.dayofweek` is 0 for Monday; `dt.hour` gives the hour. The training from 18:00 to 20:00 is covered by the records at 19:00 and 20:00.
:::

::: answer lines=18
:::

::: solution
Results on the saved copy (live data identical in these fields; the live response has about 20 fields per record).

1. Call: `params = {"lat": 49.41, "lon": 8.69, "date": "2026-09-28", "last_date": "2026-10-05", "tz": "Europe/Berlin"}`. **169** records (28 September 00:00 to 5 October 00:00; `last_date` is included). **3** sources: Heidelberg-Kurpfalzhof (6,417 m), Neckargemünd-Kleingemünd (8,472 m), Mannheim (14,339 m).
2. Shape (169, 15). New columns: `fallback_source_ids.cloud_cover`, `.sunshine`, `.temperature`, `.wind_speed`, `.relative_humidity` (in every record) and `fallback_source_ids.condition` (only in 12 records). For the other 157 records the value is missing, and an integer column with `NaN` becomes `float64` (234403.0) — the same trap as integer keys with NULL in session 14.
3. All 169 records have `source_id` 128157 (Heidelberg-Kurpfalzhof) — but that station delivers only the **precipitation** (and the condition in most hours). **Temperature**, sunshine, wind, humidity and cloud cover come from **Mannheim** in all 169 records; the **condition** comes from Neckargemünd in 8 and from Mannheim in 4 records. "28.8 °C in Heidelberg" is really "28.8 °C measured in Mannheim, 14 km away" — fine for training decisions, wrong for a statement about the Heidelberg microclimate. Lineage belongs in every report.
4. Records 19:00 and 20:00 on Tuesday 29 September: 0.0 mm, 0.0 mm (dry, 24.9 °C and 25.3 °C). Thursday 1 October: 19:00 **0.0 mm**, 20:00 **0.5 mm** with condition 'rain' — it rained in the second training hour (19:00–20:00). The week's rain was 1.1 mm on 1 October, 2.4 mm on 2 October and 0.2 mm on 4 October; the Saturday 3 October was dry and sunny.
5. **9** hours disagree: 6 hours with precipitation > 0 but 'dry' (0.1–0.4 mm), 3 hours 'rain' with 0.0 mm. **8** of the 9 have a condition from Neckargemünd (7) or Mannheim (1) — precipitation and condition were measured at different places. Only 2 October 05:00 disagrees with no fallback.
6. Example: "The rain values come from a DWD station 6 km from our pitch and are suitable to document past training conditions; temperature and wind come from Mannheim. For a decision **before** training we need a forecast, not observations — Bright Sky also offers forecasts, which are less certain. We will use precipitation > 0 (not the condition field) as our rain rule, note the station and the licence (DWD, CC BY 4.0) in every report, and re-check after a month whether the decisions matched what coaches saw on the pitch."

Marking: one point per question; 3 and 5 need the link between the result and the station.
:::

## Exam-Style Task: A Script for the Car-Sharing API

This task is in the style of an exam question. It uses the car-sharing partner API from task 4. A trainee wrote this script for the city's mobility office:

```python
import requests
import pandas as pd

KEY = "a81f3c09e2b74d55"                                                    # line 4
url = ("https://api.carshare.example/v2/trips"
       "?from=2027-06-01&to=2027-06-30&key=" + KEY)                         # line 6
r = requests.get(url)                                                        # line 7
trips = pd.DataFrame(r.json()["data"])                                       # line 8
trips.to_csv("trips_june.csv")                                               # line 9
print(len(trips), "trips in June")                                           # line 10
```

1. Name the parts of the **request** in lines 6–7 and the parts of the **response** that the script uses or ignores. (2 points)
2. The API accepts the key in this call. The script prints `25 trips in June`, although the API reports `"total": 2340`. Explain the result. (1 point)
3. Name **four further** problems of the script and explain the risk of each. (4 points)
4. One day the key has expired. What happens in line 8 — and why is that worse than an error in line 7? (1 point)
5. Sketch an improved version (code or numbered steps). (2 points)

::: answer lines=22
:::

::: solution
Marking guide (10 points).

1. (2 points) Request: method **GET**; base URL `https://api.carshare.example/v2`, endpoint `/trips`, **query parameters** `from`, `to` (and `key`); no headers set — 1 point. Response: the script uses only the **body** (JSON, key `data`); it ignores the **status code** and the **headers** (e.g. `Retry-After`) and the paging fields `total` and `next` — 1 point.
2. (1 point) Only the **first page** was fetched: without `per_page`, the API returns the default of **25** records per page; the remaining 2,315 trips are on 93 further pages (`next`). The script never follows `next`.
3. (4 points, one per problem with risk; any four):
   - **Key in the code** (line 4) — the script will be shared or committed; anyone with the file can use the partner's access. Use an environment variable.
   - **Key in the URL** instead of the documented header — URLs end up in logs, browser histories and error messages (`raise_for_status` prints the URL); the documentation asks for `X-API-Key`.
   - **No timeout** (line 7) — if the API hangs, the script waits forever, e.g. in a nightly job.
   - **No status check** — an error body is parsed as if it were data (see 4).
   - **Query string glued by hand** — no encoding of special characters, easy to break; use `params`.
   - **Raw response not saved** — no way to check or repeat the cleaning without calling the API again.
   - `to_csv` writes the **index** as an extra unnamed column (use `index=False`); no retrieval date in the file name — the next run overwrites it silently.
   - No check of completeness (`len(trips)` vs. `total`) and no handling of **429** if paging is added.
4. (1 point) The API answers **401** with an error body such as `{"error": "invalid or missing API key"}`; `requests.get` does **not** raise, so line 8 fails with **`KeyError: 'data'`** — a confusing message far away from the cause. Worse still, if the error body happened to contain `data`, wrong data would silently be written. With `r.raise_for_status()` after line 7 the script stops with "401 Client Error: Unauthorized" at the right place.
5. (2 points; 1 point for paging with status check, 1 point for key handling, timeout and saving the raw data)
   ```python
   import os, json, time
   key = os.environ["CARSHARE_API_KEY"]
   params = {"from": "2027-06-01", "to": "2027-06-30", "per_page": 100, "page": 1}
   rows, url = [], "https://api.carshare.example/v2/trips"
   while url:
       r = requests.get(url, params=params, headers={"X-API-Key": key}, timeout=10)
       if r.status_code == 429:
           time.sleep(int(r.headers.get("Retry-After", "60"))); continue
       r.raise_for_status()
       body = r.json(); rows += body["data"]
       url, params = body["next"], None          # 'next' already contains the parameters
   assert len(rows) == body["total"]
   with open("trips-raw-2027-06.json", "w", encoding="utf-8") as f:
       json.dump(rows, f)
   pd.DataFrame(rows).to_csv("trips_2027-06.csv", index=False)
   ```
   Equivalent numbered steps earn full points if they contain paging until `next` is null, a status check, the key from the environment in the header, a timeout, and saving the raw data.

Whether `next` is a full URL or a path is not in the documentation extract; accept either assumption if stated.
:::

## Optional Challenge: A Weather Function with a Cache {.optional}

Write a function `get_weather(lat, lon, first, last, cache_dir="cache")` that

- calls Bright Sky for the days `first` to `last` (inclusive, German local time) with a timeout,
- retries up to three times after a timeout, a connection error, a 429 or a 5xx, with a growing pause,
- saves every successful response in the cache folder under a file name built from the parameters,
- uses the cached file if the API cannot be reached — and raises a clear error if there is none,
- returns a DataFrame with **local** timestamps, without the extra record after `last`, and tells the caller whether the data came from the API or the cache.

Test it with the Heidelberg week (copy the saved response into the cache under the right name and switch off your network, or use a wrong host name).

::: hint
`pd.to_datetime(..., utc=True).dt.tz_convert("Europe/Berlin")` also works for weeks across the change from summer to winter time. `DataFrame.attrs` is a dictionary for metadata such as the origin of the data.
:::

::: answer lines=12
:::

::: solution
One possible solution (tested with the network blocked; the cache file for the Heidelberg week was used):

```python
import time
from pathlib import Path

URL = "https://api.brightsky.dev/weather"

def get_weather(lat, lon, first, last, cache_dir="cache", retries=3):
    path = Path(cache_dir) / f"weather_{lat}_{lon}_{first}_{last}.json"
    params = {"lat": lat, "lon": lon, "date": first,
              "last_date": f"{last}T23:00", "tz": "Europe/Berlin"}
    data, origin = None, "api"
    for attempt in range(retries):
        try:
            r = requests.get(URL, params=params, timeout=10)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(int(r.headers.get("Retry-After", 2 ** attempt)))
                continue
            r.raise_for_status()                       # other 4xx: stop, the request is wrong
            data = r.json()
            path.parent.mkdir(exist_ok=True)
            path.write_text(json.dumps(data), encoding="utf-8")
            break
        except (requests.ConnectionError, requests.Timeout):
            time.sleep(2 ** attempt)
    if data is None:
        if not path.exists():
            raise RuntimeError(f"API not available and no cached copy {path}")
        data, origin = json.loads(path.read_text(encoding="utf-8")), "cache"
    w = pd.json_normalize(data["weather"])
    w["timestamp"] = pd.to_datetime(w["timestamp"], utc=True).dt.tz_convert("Europe/Berlin")
    w = w[w["timestamp"].dt.date <= pd.Timestamp(last).date()]
    w.attrs["origin"] = origin
    return w
```

Observed: with the saved response copied to `cache/weather_49.41_8.69_2026-09-28_2026-10-04.json`, `get_weather(49.41, 8.69, "2026-09-28", "2026-10-04")` returned (168, 15) — the extra record of 5 October dropped — with timestamps from 2026-09-28 00:00 to 2026-10-04 23:00 (`datetime64[us, Europe/Berlin]`) and `attrs == {"origin": "cache"}` after about 8 seconds of retries (1 + 2 + 4 s). For the Mannheim week without a cache file it raised `RuntimeError: API not available and no cached copy cache/weather_49.49_8.47_2026-10-05_2026-10-11.json`. Points to check in other solutions: other 4xx errors are **not** retried; the pause grows; the cache is written only after a successful call; the origin is visible to the caller. A real cache would also store the retrieval time, because recent observations can still be corrected.
:::

## References {.references}

- Creative Commons. (n.d.). *Attribution 4.0 International (CC BY 4.0)*. Retrieved October 21, 2026, from https://creativecommons.org/licenses/by/4.0/
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* (Version 2.2.12) [API documentation]. Retrieved October 21, 2026, from https://brightsky.dev/docs/
- Deutscher Wetterdienst. (2024). *Terms of use for data on the CDC-OpenData area*. https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf
- Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* [Doctoral dissertation, University of California, Irvine]. https://ics.uci.edu/~fielding/pubs/dissertation/top.htm
- Fielding, R., Nottingham, M., & Reschke, J. (Eds.). (2022). *HTTP semantics* (RFC 9110). RFC Editor. https://doi.org/10.17487/RFC9110
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- Nottingham, M., & Fielding, R. (2012). *Additional HTTP status codes* (RFC 6585). RFC Editor. https://doi.org/10.17487/RFC6585
- pandas development team. (n.d.). *IO tools (text, CSV, HDF5, …)*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/user_guide/io.html
- Requests. (n.d.). *Quickstart*. Requests 2.34.2 documentation. Retrieved October 21, 2026, from https://requests.readthedocs.io/en/latest/user/quickstart/
