---
course: Data Management
session: 14
title: Data Quality II: Data Cleaning with Python
subtitle: pandas basics · missing values, duplicates, outliers, inconsistent formats · standardisation and validation rules
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Data Quality II: Data Cleaning with Python {.title}

::: notes
Time plan for today (3 h): recap 8 min · loading today's data 4 min · pandas basics 17 min · mini exercise SQL to pandas 8 min · break 10 min · cleaning workflow and missing values 14 min · inconsistent formats 10 min · duplicates 8 min · outliers 9 min · mini exercise which treatment 8 min · validation rules and write-back 10 min · hands-on: clean the web shop export 50 min · team step 12 min · wrap-up 5 min · ~7 min buffer.
Input is about 72 minutes, hands-on, exercises and discussion about 78 minutes. Priorities if time runs short: the cleaning workflow (keep the raw data, standardise before deduplicating, flag instead of silently changing), the treatment options for missing values, duplicates and outliers, and "cleaning moves defects, it does not create correct data" are the exam core. pandas syntax is a tool for the hands-on and the project, not exam syntax — the exam may show short pandas code to read and explain, but does not ask for code from memory. The MCAR/MAR/MNAR slide and the pandas pitfalls slide are optional (self-study). Shorten the hands-on to questions 1–5 if needed, but keep question 7 (scorecard and write-back): it closes the loop to session 13.
Every Python statement on these slides was run with Python 3.13, pandas 3.0.6 and SQLite 3.45.1 on a fresh database built from bikeshop-schema.sql, bikeshop-data.sql, bikeshop-data-session09.sql and bikeshop-dq-session13.sql, plus the new webshop-orders-session14.csv; all results are the ones observed. Students who installed pandas before January 2026 have pandas 2.x: everything works the same, but text columns show the dtype "object" instead of "str" (pandas 3.0 introduced a dedicated string dtype; pandas development team, n.d.-d).
:::

---

# Today's Agenda

1. Recap: measure before you clean
2. pandas basics: DataFrames, selecting and filtering
3. Cleaning step by step: missing values, formats, duplicates, outliers
4. Validation rules in code — and back into the database
5. Hands-on: clean the web shop export in a notebook

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:08 Loading today's data (everyone) · 0:12 pandas basics (input with live demo in Jupyter) · 0:29 Mini exercise SQL to pandas (pairs) · 0:37 Break · 0:47 Cleaning workflow and missing values (input, live demo) · 1:01 Formats, duplicates, outliers (input, live demo) · 1:28 Mini exercise which treatment (pairs) · 1:36 Validation rules and write-back (input, live demo) · 1:46 Hands-on (groups of 3, each student on their own laptop) · 2:36 Team step (project teams) · 2:48 Wrap-up · buffer.
Live demo: run every code slide in a notebook in front of the class instead of only showing the slide; students follow on their own laptops if they like. Breaking and fixing code live is part of the lesson.
:::

---

# Recap: Where Session 13 Left Us

- Data quality is **fitness for use**; dimensions become measurable through **rules** and **metrics**
- The web shop export failed several rules: duplicates, invalid dates, postcodes, codes, an orphan link
- Decision in session 13: **do not merge** the export into `customer` yet
- Today: **clean** it — repeatable, documented, in Python

::: callout
**Your preparation:** pandas installed and tested; your team's five quality rules. Which of your rules could a cleaning step **repair**, and which can only **flag** a problem?
:::

::: source
Wang and Strong (1996); session 13 of this course.
:::

::: notes
Preparation from session 13: hands-on and worksheet 13 done, pandas installed, five team rules. Quick check (2 min): ask for a show of hands — whose `import pandas` worked? Pair students without a working setup with a neighbour for the first part; fix installations during the break (`python -m pip install pandas`). Ask the callout question to two or three teams: a rule like "postcode has five digits" can sometimes be repaired ('D-69117' → '69117'), sometimes not ('6811' — which digit is missing?). That distinction runs through today. Link: the session 13 scorecard (e-mail present 90 %, valid format 94.4 %, postcode 89.5 %, one account per person 90 %) is today's "before" picture.
:::

---

# Loading Today's Data

```python
import sqlite3
import pandas as pd

con = sqlite3.connect("bikeshop.db")      # built in session 13 with the four scripts
raw = pd.read_sql("SELECT * FROM webshop_customer", con)
orders = pd.read_csv("webshop-orders-session14.csv")     # new
```

- **raw**: the 20 web shop accounts from session 13 as a pandas **DataFrame**
- **orders**: 25 web shop orders of March and April 2027 from a CSV file, **as exported**
- `raw` stays **untouched** — every cleaning step works on a **copy**

::: source
Own example based on the bike shop case; all data fictional. McKinney (2022, Chapter 6).
:::

::: notes
Everyone runs this cell now. Students who do not have bikeshop.db from session 13 rebuild it first with the loading cell of session 13 (four scripts). Check: `raw.shape` → (20, 9), `orders.shape` → (25, 5). The CSV is new and fictional; it contains typical export errors on purpose (a decimal comma, an exact duplicate row, a missing amount, a typo outlier, a refund, an unknown account). Reading files in depth (CSV options, Excel, JSON) is the topic of session 15 — today one line of read_csv is enough. read_sql runs any SELECT, so the profiling queries of session 13 still work and return DataFrames.
:::

---

# pandas Basics {.section}

Tables in Python

---

# DataFrame and Series

::: cards
### DataFrame
A **table**: rows with an **index** (labels) and named **columns**. Each column has **one data type**.
### Series
**One column** of a DataFrame: values plus the index. `raw["city"]` is a Series.
### Vectorised
Operations work on **whole columns** at once — no loops: `raw["city"].str.lower()`
:::

| pandas type | Typical use | Missing value |
|---|---|---|
| `str` (pandas 2: `object`) | text, codes, postcodes | `NaN` |
| `float64`, `Int64` | amounts, counts, keys | `NaN` / `<NA>` |
| `datetime64` | dates, timestamps | `NaT` |
| `boolean` | yes/no flags | `<NA>` |

::: source
Based on McKinney (2022, Chapter 5) and pandas development team (n.d.-a, n.d.-d).
:::

::: notes
A DataFrame is close to a relation of session 5, with two differences: rows have an order and an index label, and duplicates are allowed — there is no primary key. Every column has one dtype; pandas 3.0 stores text as "str" (pandas 2: "object"). Missing values depend on the dtype: NaN for float and str columns, NaT for dates, pd.NA for the nullable types Int64 and boolean (pandas development team, n.d.-a). Capital I in Int64 matters: int64 cannot hold a missing value, Int64 can. Students do not need to learn the table by heart; they need to know that the dtype decides what a missing value looks like and which operations work.
:::

---

# A First Look at the Export

```python
raw.shape                       # (20, 9)
raw.dtypes                      # all 9 columns: str — everything is text
raw.isna().sum()                # e_mail 2, postcode 1, city 1, newsletter 1, customer_no 9
raw["city"].value_counts(dropna=False)
                                # Mannheim 8, Heidelberg 6, Ladenburg 2, Schwetzingen 1,
                                # MANNHEIM 1, Weinheim 1, NaN 1
```

- `info()` and `describe()` give an overview of **all columns** at once
- The same **profile** as in session 13 — now in a few lines of Python
- `value_counts(dropna=False)` shows the **NaN** too — without it, missing values stay invisible

::: source
Own example on the web shop export; McKinney (2022, Chapter 5).
:::

::: notes
All observed (pandas 3.0.6). Compare with the session 13 profile: count(e_mail) = 18 ↔ 2 NaN, GROUP BY city ↔ value_counts. `raw.info()` shows the non-null count and dtype per column in one table; `raw.describe()` on text columns shows count, unique, top and freq — e.g. name: 20 values, 19 unique (Jonas Albrecht twice; "anna berger" and "Anna Berger" count as two). Ask: why are all columns text? → the staging table of session 13 has TEXT columns only; read_sql keeps what SQLite delivers. A numeric column with NULL would come back as float64: `pd.read_sql("SELECT customer_no FROM bike", con)` gives 101.0 and NaN (observed) — a trap when keys become floats.
:::

---

# Selecting and Filtering

```python
raw["e_mail"]                                    # one column → Series
raw[["account_id", "name", "city"]]              # several columns → DataFrame
raw[raw["city"] == "Mannheim"]                   # rows by condition → 8 rows
raw[(raw["city"] == "Heidelberg") & (raw["newsletter"] == "no")]     # → 4 rows
raw.loc[raw["newsletter"] == "yes", ["account_id", "e_mail"]]        # rows and columns
raw.sort_values("last_changed").head(3)          # W15, W13, W17: the oldest changes
```

- A condition gives a **boolean Series** (a **mask**); `raw[mask]` keeps the rows where it is `True`
- Combine masks with `&` (and), `|` (or), `~` (not) — **brackets** around each condition
- `.loc[rows, columns]` selects both — and is the safe way to **change** values

::: source
Own example on the web shop export; McKinney (2022, Chapter 5); pandas development team (n.d.-c).
:::

::: notes
All results observed. The mask idea is the key: a cleaning rule later is just a mask, and "how many rows break the rule" is `(~mask).sum()`. Brackets are needed because & binds more strongly than == in Python; forgetting them gives a TypeError or a confusing result. `and`/`or` do not work on Series (ValueError: The truth value of a Series is ambiguous). .loc with a mask and a column name is also how values are changed: `df.loc[mask, "postcode"] = ...` — see the optional pitfalls slide.
:::

---

# From SQL to pandas

| SQL (sessions 8–10) | pandas |
|---|---|
| `SELECT name, city FROM t` | `t[["name", "city"]]` |
| `WHERE city = 'Mannheim'` | `t[t["city"] == "Mannheim"]` |
| `WHERE e_mail IS NULL` | `t[t["e_mail"].isna()]` |
| `WHERE city IN ('Weinheim', 'Ladenburg')` | `t[t["city"].isin(["Weinheim", "Ladenburg"])]` |
| `ORDER BY last_changed DESC LIMIT 3` | `t.sort_values("last_changed", ascending=False).head(3)` |
| `SELECT city, count(*) … GROUP BY city` | `t.groupby("city").size()` or `t["city"].value_counts()` |
| `SELECT DISTINCT city` | `t["city"].unique()` |
| `LEFT JOIN customer c ON …` | `t.merge(c, how="left", on="customer_no")` |

::: source
Based on pandas development team (n.d.-c).
:::

::: notes
The pandas documentation has a full "Comparison with SQL" page (pandas development team, n.d.-c) — recommend it for the project. Differences worth one sentence each: groupby drops NaN groups by default (use dropna=False to see them, unlike SQL where NULL forms a group); merge needs the key columns to have the same dtype (str '101' does not match int 101 — another reason for cleaning dtypes); pandas keeps the row order unless you sort. When to use which: SQL in the database for large data and shared business logic (views), pandas for exploration, cleaning and steps that are awkward in SQL (parsing dates in several formats, regular expressions, statistics).
:::

---

# Mini Exercise: From SQL to pandas {.exercise}

Write the pandas expression and predict the result on `raw`.

1. `SELECT count(*) FROM webshop_customer WHERE customer_no IS NULL`
2. `SELECT account_id, name FROM webshop_customer WHERE postcode IS NULL OR city IS NULL`
3. `SELECT newsletter, count(*) FROM webshop_customer GROUP BY newsletter`
4. `SELECT account_id FROM webshop_customer WHERE e_mail LIKE '%(at)%'`
5. Which of your answers would change if `raw["city"]` were written in **capitals** everywhere?

::: notes
About 5 min in pairs, 3 min collection. Expected answers (all observed):
1 `raw["customer_no"].isna().sum()` → 9.
2 `raw.loc[raw["postcode"].isna() | raw["city"].isna(), ["account_id", "name"]]` → W13 Emma Wolf (one row: both are missing in the same record).
3 `raw["newsletter"].value_counts(dropna=False)` → no 9, yes 8, NaN 1, '1' 1, 'Y' 1. Without dropna=False the NaN row is missing — like `count(newsletter)` vs. `count(*)`. `raw.groupby("newsletter").size()` also drops NaN by default.
4 `raw[raw["e_mail"].str.contains("(at)", regex=False, na=False)]["account_id"]` → W05. Without regex=False, "(at)" is a regular expression group that matches any "at" anywhere: on this data only W05 contains "at", so the result happens to be the same, but pandas shows a UserWarning (observed) — on other data (e.g. "kate@…", "matthias@…") it would not be. Without na=False, the NaN e-mails give missing values in the mask.
5 None of them: no question uses city values. Good students notice that question 2 tests NULL only, not the spelling.
:::

---

# Cleaning Step by Step {.section}

Repair what can be repaired — flag the rest

---

# A Cleaning Workflow

::: layers
- 1 Profile: find the problems and their patterns (session 13)
- 2 Standardise: one spelling, one format, one data type per column
- 3 Validate: apply the rules; mark every value that breaks one
- 4 Treat: missing values, duplicates, outliers — repair, set to missing, or flag for a person
- 5 Verify and load: measure again, then write to the target table
:::

- Keep the **raw data** unchanged; clean in a **script**, so every step can be **repeated**
- Every change is **logged**: which record, which value, which rule, which decision

::: source
Own illustration based on Rahm and Do (2000) and DAMA International (2017, Chapter 13).
:::

::: notes
Rahm and Do (2000) describe the phases data analysis, definition of transformation workflow and mapping rules, verification, transformation, and backflow of cleaned data to the sources; within the transformation they name validation and correction, standardisation and duplicate elimination. Our five steps simplify this for the hands-on. Why a script and not Excel: the next export arrives next month with the same problems; a notebook or script cleans it again in seconds and documents what was done (this becomes the "T" in ETL, session 16). Backflow (Rahm and Do) matters for the cost argument of session 13: if the error is only fixed in the copy, the source produces it again next month — tell the web shop team about W05's "(at)".
:::

---

# Missing Values: Find Them

```python
raw.isna().sum()                               # explicit NaN per column
raw.isna().mean().round(3)                     # as a share: e_mail 0.10, customer_no 0.45
(raw["birth_date"] == "1900-01-01").sum()      # 1 hidden missing value (W13)
```

- **Explicit** missing values: `NaN`, `NaT`, `<NA>`, `None` — `isna()` finds them all
- **Hidden** missing values: default values and placeholders that look like data: `1900-01-01`, `""`, `"n/a"`, `"-"`, `0`, `99999`
- Hidden values must be **turned into** real missing values first — otherwise `count`, `mean` and `isna()` are wrong
- Never test with `== NaN`: `NaN == NaN` is `False` — use `isna()`

::: source
Own example on the web shop export; pandas development team (n.d.-a); McKinney (2022, Chapter 7).
:::

::: notes
Observed: e_mail 2, postcode 1, city 1, newsletter 1, customer_no 9; birth_date 0 explicit but 1 hidden. `raw["e_mail"] == None` finds 0 rows (observed) although there are 2 NaN: comparison does not find missing values (pandas development team, n.d.-a; same idea as `= NULL` in SQL, session 8). Hidden missing values come from forms that require a value ("1900-01-01" as a default date, "-" in a mandatory field) and from exports that write empty strings. pd.read_csv converts some placeholders to NaN automatically (e.g. empty fields, "NA", "n/a"); others such as "-" or "unknown" need `na_values=[...]` (session 15).
:::

---

# Missing Values: Drop, Fill or Flag?

| Option | pandas | When it fits | Risk |
|---|---|---|---|
| **Drop** rows | `dropna(subset=["e_mail"])` | the row is useless for **this use** | lose information; biased results |
| **Fill** with a value | `fillna(...)` | a **known** default: quantity 1, country DE | invents data |
| **Fill** from another source | `fillna(other)`, `merge` | a trusted **reference**: postcode → city | the source may be wrong, too |
| **Flag** and keep | `df["e_mail_missing"] = df["e_mail"].isna()` | most cases in **master data** | someone must follow up |

- Bike prices (session 10): mean of the 13 known prices **2,191.31 €**; with `fillna(0)` **1,899.13 €** — a missing price is **not a free bike**
- Decide **per use**: the newsletter drops W11 and W16; the invoice must **ask** them

::: source
Based on McKinney (2022, Chapter 7) and DAMA International (2017, Chapter 13); own example on the bike shop data.
:::

::: notes
Observed: `b = pd.read_sql("SELECT price FROM bike", con)`; `b["price"].mean()` → 2191.31 (pandas skips NaN like SQL's avg); `b["price"].fillna(0).mean()` → 1899.13. Filling with the mean or median is common in statistics and machine learning, but in master data (customers, products) it invents values that look real — never fill a birth date with the average age. The rule of thumb for business data: repair only with a trusted rule or reference, otherwise keep the gap visible and flag it. Cleaning does not create information: W11 and W16 have no e-mail, and no pandas function can find it — only asking the customer can.
:::

---

# Why Is It Missing? {.optional}

| Mechanism | Meaning | Web shop example |
|---|---|---|
| **MCAR**: missing completely at random | missingness has nothing to do with the data | a server error lost some fields |
| **MAR**: missing at random | depends on **other, observed** values | customers who registered in the till never gave an e-mail |
| **MNAR**: missing not at random | depends on the **missing value itself** | older customers leave the birth date empty more often |

- Only under MCAR does dropping rows leave the remaining data **unbiased**
- Ask **why** values are missing before you drop or fill them

::: source
Based on Rubin (1976); own examples.
:::

::: notes
Self-study. Rubin (1976) defined the conditions under which the process that causes missing data can be ignored; the labels MCAR, MAR and MNAR go back to his work. Business example: if the customers without e-mail are mostly older till customers (MAR), an e-mail survey only reaches younger ones — the result is biased even though no value was "wrong". Not exam content; useful for students who will do data science (session 18 and the DSKI-style projects).
:::

---

# Inconsistent Formats: Text and Codes

```python
df = raw.copy()
for col in ["name", "e_mail", "postcode", "city"]:
    df[col] = df[col].str.strip()                        # spaces at the ends
df["name"]   = df["name"].str.title()                    # 'anna berger' → 'Anna Berger'
df["city"]   = df["city"].str.title()                    # 'MANNHEIM' → 'Mannheim': 5 cities
df["e_mail"] = df["e_mail"].str.lower().str.replace("(at)", "@", regex=False)

codes = {"yes": True, "y": True, "1": True, "no": False}
df["newsletter"] = df["newsletter"].str.lower().map(codes).astype("boolean")
                                                         # True 10, False 9, <NA> 1
```

- **Standardise** = one agreed representation per value: case, spaces, codes, units
- `map` with a **dictionary** documents the decision; unmapped values become **missing**, not silently wrong

::: source
Own example on the web shop export; McKinney (2022, Chapter 7).
:::

::: notes
All observed. city: 6 distinct values before, 5 after title(). The newsletter mapping is a business decision, not a technical one: we assume the web shop team confirmed that 'Y' and '1' come from an old app version and mean consent (session 13 left this open; the legal side is session 19). Without 'y' and '1' in the dictionary, map gives NaN for W15 and W18 (observed: True 8, False 9, NaN 3) — better than guessing. str.title() has limits: 'Mcdonald', 'Van Der Berg'; for names, lower-case comparison keys are often safer than changing the stored name. Repairing '(at)' is safe here because the till system has the same address (session 13: W05); in general, a repair rule should be confirmed on a few records.
:::

---

# Inconsistent Formats: Dates and Postcodes

```python
iso = pd.to_datetime(df["birth_date"], format="%Y-%m-%d", errors="coerce")
ger = pd.to_datetime(df["birth_date"], format="%d.%m.%Y", errors="coerce")
bd  = iso.fillna(ger)                       # W08 '12.06.1999' → 1999-06-12; W19 → NaT
df["birth_date"] = bd.where(bd.between("1910-01-01", "2027-05-03"))   # W13, W14 → NaT

df["postcode"] = df["postcode"].str.removeprefix("D-")          # 'D-69117' → '69117'
ok = df["postcode"].str.fullmatch(r"\d{5}", na=False)           # W11 '6811', W13 NaN
df["postcode"] = df["postcode"].where(ok)
```

- `errors="coerce"`: what cannot be parsed becomes `NaT` — **look** at these rows before moving on
- `1991-02-29` (W19) does not exist: pandas → `NaT`; SQLite's `date()` gave `1991-03-01`
- Postcodes are **text**, not numbers: `01067` (Dresden) would lose its leading zero

::: source
Own example on the web shop export; pandas development team (n.d.-b); McKinney (2022, Chapter 7).
:::

::: notes
All observed. An explicit format makes parsing strict: '%Y-%m-%d' fails for '12.06.1999' and for the impossible date '1991-02-29'. Avoid format="mixed" or dayfirst=True on unknown data: the documentation warns that dayfirst is not strict (pandas development team, n.d.-b) — '01.02.2027' could become 1 February or 2 January. Our rule: try the formats we know, in order, and inspect what is left. `where(cond)` keeps values where cond is True and sets the rest to missing. Plausibility range 1910 to the export date as in session 13. '6811' cannot be repaired (which digit is missing?) — set to missing and flag; the postcode reference list could suggest the city, but not the postcode. Session 13 link: SQLite date('1991-02-29') returns '1991-03-01' (observed) — it normalises instead of rejecting, so the SQL check needed `birth_date IS NOT date(birth_date)`.
:::

---

# Duplicates: Standardise First, Then Compare

```python
raw.duplicated(subset=["name", "birth_date"]).sum()     # 1: only Jonas Albrecht
df.duplicated(subset=["name", "birth_date"]).sum()      # 2: + Anna Berger (now title case)
df[df.duplicated(subset=["name", "birth_date"], keep=False)]    # W01, W02, W03, W17
```

- **Exact duplicates**: the same row twice, e.g. an order exported twice → `drop_duplicates()`
- **Same entity, different records**: one person, two accounts — needs a **matching key**
- Standardise **before** matching: `'anna berger'` and `'Anna Berger'` only match after `title()`
- Spelling variants (`'Müller'` / `'Mueller'`) need **fuzzy matching** — and a person to confirm

::: source
Own example on the web shop export; Rahm and Do (2000); McKinney (2022, Chapter 7).
:::

::: notes
Observed: 1 duplicate in raw, 2 after standardising. keep=False marks all copies, so you can look at both records before deciding. The matching key (name + birth date) is a business choice: e-mail alone finds only Anna (Jonas used two addresses); name alone would merge two different people with a common name. Rahm and Do (2000) list duplicate elimination as a step of its own, typically after standardisation, because matching on unstandardised values misses duplicates. Record linkage and fuzzy matching (similarity measures for names and addresses) are beyond this course; tools exist, but they still need thresholds and human review.
:::

---

# Duplicates: Which Record Survives?

```python
df = df.sort_values("last_changed")
older = df.duplicated(subset=["name", "birth_date"], keep="last")
df.loc[older, "account_id"].tolist()          # ['W17', 'W03']
clean = df[~older]                            # 18 accounts

moved = {"W03": "W01", "W17": "W02"}          # old account → surviving account
orders["account_id"] = orders["account_id"].replace(moved)    # O-2004, O-2012
```

- **Survivorship rule**: here the most recently changed record wins (W01, W02)
- Check what the other record **knows**: W17 has a second e-mail address for Jonas Albrecht
- Records that **refer** to the removed one must be **re-pointed** — or they become orphans

::: source
Own example on the web shop export and orders; McKinney (2022, Chapter 7).
:::

::: notes
Observed: W17 (2023-04-01) and W03 (2025-03-20) are the older copies; W01 and W02 survive and are also the accounts linked to the till system (customer_no 101 and 102). Other survivorship rules: the record with the most filled fields, the one linked to the master system, or field by field (`combine_first` fills gaps of one record from another). Session 9 link: deleting W03 without re-pointing O-2004 would create an orphan order — exactly what a foreign key with ON DELETE RESTRICT would have prevented. Ask: is it right to drop jonas.albrecht@example.com? → it may be his current private address; keep it in the log or ask him.
:::

---

# Outliers: Rule or Statistics?

```python
orders["amount_eur"] = pd.to_numeric(orders["amount_eur"].str.replace(",", "."))
orders = orders.drop_duplicates()                          # O-2015 was exported twice
x = orders["amount_eur"]
q1, q3 = x.quantile([0.25, 0.75])                          # 23.70 and 94.00
fence = q3 + 1.5 * (q3 - q1)                               # 199.45
orders[x > fence]                                          # O-2003, O-2008, O-2015
orders[~x.between(0.01, 5899)]                             # O-2008 12,990.00, O-2021 −34.90
```

- **Rule-based**: a business limit — no order above the most expensive product, no negative amount
- **Statistical**: unusual compared with the other values, e.g. Tukey's fences at **1.5 × IQR**
- An outlier is a **question**, not an error: two of the three statistical outliers are **real bikes**

::: source
Own example on the web shop orders; Tukey (1977); McKinney (2022, Chapter 7).
:::

::: notes
All observed: before fixing the comma, to_numeric fails on '64,50' (with errors="coerce" it silently becomes NaN — check first). After removing the duplicate: 24 orders, 23 amounts, Q1 23.70, Q3 94.00, IQR 70.30, upper fence 199.45, lower fence negative. Tukey (1977) introduced fences at 1.5 times the spread between the hinges in exploratory data analysis; pandas computes quartiles by linear interpolation, which can differ slightly from Tukey's hinges — not exam-relevant. McKinney (2022, Chapter 7) shows the simpler rule "absolute value above a threshold". O-2003 (899 €) and O-2015 (3,599 €, an e-bike) are real bike orders; O-2008 12,990 € is above the most expensive bike — probably 129.90 typed without the decimal point; O-2021 −34.90 € is a refund booked as an order. Treatment: never "correct" 12,990 to 129.90 without asking; flag it, and keep refunds in their own table or with a type column.
:::

---

# One Outlier Can Move the Mean

![Order amounts on a logarithmic axis: most orders lie between 7.90 and 149 euros inside the upper fence of 199.45 euros; three orders lie above it (899, 3,599 and 12,990 euros); only 12,990 euros is above the business limit of 5,899 euros; the median is 52.40 euros, the mean 803.96 euros](img/cleaning-outliers.png){width=92%}

::: source
Own illustration based on Tukey (1977); fictional web shop orders (webshop-orders-session14.csv).
:::

::: notes
The median (52.40 €) describes a typical order; the mean (803.96 €) is pulled up by three orders. Revenue in March 2027 with the typo: 18,063.29 € (observed, after removing the duplicate) — a report to the shop owner would overstate March by about 12,860 € if O-2008 really is 129.90 €. The log axis is needed because the values span four orders of magnitude; the refund (−34.90 €) cannot be shown on a log axis. Ask: what would the business rule miss? → a 1,000 € typo for a 100 € helmet is below the limit — plausibility rules per product would find it (the order lines, which this export does not have).
:::

---

# Mini Exercise: Which Treatment? {.exercise}

Choose **drop**, **fill**, **repair**, **flag** or **ask** — and say why.

1. A customer's postcode is `'69 117'`
2. 30 % of the product records have no weight; shipping costs depend on it
3. An order appears twice in the export: same order number, same values
4. A car-sharing trip of **2,140 km** in one day
5. The country field is empty for all customers of the German web shop
6. A member's date of birth is `1900-01-01`
7. Two customer records "Müller GmbH" and "Mueller GmbH" with the same VAT number

::: notes
About 5 min in pairs, 3 min collection. Expected answers (other answers with a sound reason are fine):
1 Repair: remove the space (a safe standardisation rule), then validate against the reference list.
2 Flag and ask: the weight cannot be invented; fill only from a trusted source (supplier data). Do not drop the products — they are still sold.
3 Drop the exact duplicate (keep one).
4 Flag and ask: physically possible only with ~90 km/h for 24 h; probably a typo in the odometer — a statistical outlier and above a plausibility rule. Do not delete the trip: it may have to be invoiced.
5 Fill with 'DE': a known default for this source (document the rule) — but check that the shop really only delivers in Germany.
6 Set to missing (hidden missing value) and flag; never fill with an average.
7 Merge after confirmation: the VAT number is a strong matching key; choose a surviving record and re-point invoices and orders.
:::

---

# Validation Rules {.section}

Measure again — then enforce

---

# Validation Rules in Code

```python
rules = {
    "e-mail present":        clean["e_mail"].notna(),
    "postcode has 5 digits": clean["postcode"].str.fullmatch(r"\d{5}", na=False),
    "birth date plausible":  clean["birth_date"].between("1910-01-01", "2027-05-03"),
    "newsletter known":      clean["newsletter"].notna(),
}
report = pd.DataFrame({
    "pass_pct": {r: round(100 * m.mean(), 1) for r, m in rules.items()},
    "failing":  {r: ", ".join(clean.loc[~m, "account_id"]) for r, m in rules.items()}})
```

| rule | pass_pct | failing |
|---|---|---|
| e-mail present | 88.9 | W11, W16 |
| postcode has 5 digits | 88.9 | W11, W13 |
| birth date plausible | 83.3 | W13, W14, W19 |
| newsletter known | 94.4 | W13 |

::: source
Own example on the cleaned web shop export; metrics based on Pipino et al. (2002).
:::

::: notes
All observed on the 18 cleaned accounts. Each rule is a mask; mean() of a boolean mask is the simple ratio of session 13 (Pipino et al., 2002), and `~mask` lists the failing records — the work list for the person who follows up. Writing the rules as a dictionary makes them a reusable, documented rule set: the same cell can run on next month's export (monitoring, session 16). NaT in `between` gives False, so missing birth dates count as failing here — a choice: this rule measures "usable birth date", i.e. completeness and validity together. Name the denominator explicitly in a report.
:::

---

# Before and After: Cleaning Moves Defects

| Rule | Raw export (20 rows) | Cleaned (18 rows) |
|---|---|---|
| one account per person | 90.0 % | **100.0 %** |
| e-mail valid format (of present) | 94.4 % | **100.0 %** |
| postcode valid (of present) | 89.5 % | **100.0 %** |
| birth date valid (of all) | 80.0 % | 83.3 % |
| e-mail present | 90.0 % | **88.9 %** ↓ |
| postcode present | 95.0 % | **88.9 %** ↓ |

- Setting invalid values to missing turns a **validity** defect into a **completeness** defect — honest, but not better data
- Fewer rows change the **denominator**: removing duplicates lowered "e-mail present"
- Cleaning **cannot create** correct data — W11's postcode and W16's e-mail need the **customer**

::: source
Own example on the web shop export; metrics based on Pipino et al. (2002).
:::

::: notes
All observed. Raw values match session 13 (e-mail valid 17/18 with the same pattern as LIKE '%_@_%._%', postcode 17/19, birth date 16/20, uniqueness 18/20). Cleaned: e-mail present 16/18 (W11, W16; both removed duplicates had an e-mail, so the share fell), postcode present 16/18 (W11 set to missing, W13 was missing), birth date 15/18 (W13 default, W14 future, W19 impossible). The key message for the exam: a scorecard after cleaning must be read together with the list of changes; "100 % valid" can simply mean "all invalid values were deleted". This is why the log and the flags matter.
:::

---

# Validate in pandas, Enforce in the Database

```python
con.execute("""CREATE TABLE webshop_account (
    account_id   TEXT PRIMARY KEY,
    e_mail       TEXT CHECK (e_mail LIKE '%_@_%._%'),
    postcode     TEXT CHECK (length(postcode) = 5),
    newsletter   INTEGER CHECK (newsletter IN (0, 1)),
    customer_no  INTEGER REFERENCES customer (customer_no),
    ...)""")
out = clean.assign(birth_date=clean["birth_date"].dt.strftime("%Y-%m-%d"), ...)
out.to_sql("webshop_account", con, if_exists="append", index=False)
# DatabaseError … caused by IntegrityError: FOREIGN KEY constraint failed — 0 rows stored
```

- W18 points to customer **199**, which does not exist — the database **rejects** the whole load
- Create the table **with constraints** first, then `append`: `to_sql` alone creates a table **without** any
- Dates go into SQLite as **ISO text** (session 7)

::: source
Own example on the web shop export; McKinney (2022, Chapter 6); SQLite (n.d.).
:::

::: notes
Observed with pandas 3.0.6 and PRAGMA foreign_keys = ON: pandas raises pandas.errors.DatabaseError "Execution failed" with the cause sqlite3.IntegrityError: FOREIGN KEY constraint failed; afterwards count(*) is 0 — the insert ran as one transaction (session 10: atomicity). pandas 2.x may show the IntegrityError directly. The full statement has nine columns (name TEXT NOT NULL, city, birth_date, last_changed TEXT NOT NULL as well); the slide shows the constraints only. Decision for W18: set customer_no to missing and flag the account for the shop staff — then 18 rows load (observed). Booleans are stored as 0/1 (observed typeof integer). Without the explicit CREATE TABLE, `to_sql(..., if_exists="replace")` creates columns without keys or constraints — fine for a scratch table, wrong for the target table. Two lines of defence: pandas rules measure and report, constraints guarantee (session 7; SQLite, n.d. on foreign keys).
:::

---

# pandas Pitfalls {.optional}

| Pitfall | What happens | Instead |
|---|---|---|
| `df[df["a"] > 1]["b"] = 0` | changes a **copy**, not `df` (pandas 3) | `df.loc[df["a"] > 1, "b"] = 0` |
| `df["x"] == np.nan` | always `False` | `df["x"].isna()` |
| integer key with a missing value | becomes **float**: `101.0` | `.astype("Int64")` |
| `and`, `or` with Series | `ValueError: … ambiguous` | `&`, `\|` and brackets |
| `str.contains("(at)")` | `(at)` is a **regular expression** | `regex=False` |
| `pd.to_numeric(..., errors="coerce")` | bad values vanish **silently** | count the new NaN first |

::: source
Based on pandas development team (n.d.-a, n.d.-d) and McKinney (2022, Chapters 5 and 7).
:::

::: notes
Self-study. Chained assignment: since pandas 3.0 every indexing result behaves as a copy (Copy-on-Write); the first line does nothing to df (pandas development team, n.d.-d); pandas 3.0.6 prints a ChainedAssignmentError warning (observed). In pandas 2.x the same line gave a SettingWithCopyWarning and sometimes did change df. The float keys trap is the one that breaks merges most often: '101' (str), 101 (int) and 101.0 (float) do not match each other. For the project: check `dtypes` after every load.
:::

---

# Exercise: Clean the Web Shop Export {.exercise}

New notebook, `raw` and `orders` loaded. Predict first, then run. Keep `raw` unchanged.

1. **First look**: shape, dtypes, missing values per column, frequencies of `city` and `newsletter`
2. **Standardise** names, e-mails, cities and newsletter codes. How many cities remain?
3. **Dates and postcodes**: parse, check range and format. Which accounts end up with a missing value — and why?
4. **Duplicates**: which persons have two accounts? Keep one, build the mapping, re-point the orders
5. **Orders**: fix the amounts, remove exact duplicates, find outliers by **rule** and by **IQR**, find orders of **unknown** accounts
6. **Newsletter**: how many people may receive it now? Compare with session 13
7. **Scorecard and load**: before/after report; write the accounts into a table **with constraints**. What is rejected, and what do you decide?

::: source
Own example on the web shop export and orders; McKinney (2022, Chapters 5–7).
:::

::: notes
About 45 min + 5 min comparison. Expected answers (all observed with pandas 3.0.6):
1 (20, 9), all str; NaN: e_mail 2, postcode 1, city 1, newsletter 1, customer_no 9; city 6 values (MANNHEIM extra) + NaN; newsletter no 9, yes 8, '1', 'Y', NaN. Orders (25, 5), amount_eur is str (because of '64,50').
2 strip + title/lower: 5 cities; W05's e-mail repaired; W03's name and e-mail now match W01. Newsletter with the mapping: True 10, False 9, <NA> 1 (W13).
3 W19 postcode repaired ('D-69117' → '69117'); W11 '6811' → missing (cannot be repaired), W13 was missing. Birth dates: W08 parsed with the German format; W19 1991-02-29 → NaT (impossible), W13 1900-01-01 → missing (default value), W14 2031-04-01 → missing (future). 17 of 20 usable.
4 Anna Berger (W01, W03) and Jonas Albrecht (W02, W17); keep the newer W01 and W02 → 18 accounts. Mapping W03 → W01, W17 → W02; orders O-2004 and O-2012 re-pointed. W17's e-mail jonas.albrecht@example.com is lost unless logged.
5 '64,50' → 64.5; O-2015 twice → 24 orders; O-2017 has no amount (flag, ask). IQR fence 199.45 → O-2003 (899), O-2008 (12,990), O-2015 (3,599); rule 0.01–5,899 → O-2008 and O-2021 (−34.90, a refund). Unknown account: O-2024 → W21 (not in the export; a new account after the export date, or an error). payment 'PayPal' vs 'paypal' (lower()).
6 newsletter True and e-mail present: 9 people (W01, W04, W05, W08, W09, W12, W14, W15, W18). Session 13: 8 people with Y and 1 counted as yes — W05 is new because her e-mail was repaired. W14 has an implausible birth date but may still receive the newsletter: fitness for use.
7 See the before/after slide. Load: FOREIGN KEY constraint failed because of W18 (customer 199), nothing stored. Decide: set customer_no to missing and flag W18 for the shop staff → 18 rows load. Good groups also store the change log (account, column, old value, new value, rule) as a table.
:::

---

# Team Work: A Cleaning Plan for Your Project Data {.exercise}

Use the five quality rules from session 13.

1. For each rule: what can be **repaired** automatically, what must be **set to missing** or **flagged**, and who must be **asked**?
2. Which **standardisations** does your data need: codes, case, date and number formats, units?
3. What is your **matching key** for duplicates, and which record **survives**?
4. Which rules become **constraints** in your schema, and which stay **checks** in the notebook?

::: callout
Your cleaning plan and notebook are part of **milestone 4** (data loading and quality, after session 16).
:::

::: notes
About 12 min. Teams without their data yet: plan with the kind of data they expect; sessions 15 and 16 bring the data in. Walk around and ask: which of your cleaning steps changes data, and how do you document it? Where would the error be fixed at the source? A good team answer names a survivorship rule and keeps a log. The exact milestone 4 deliverables are in the project brief.
:::

---

# Key Takeaways

- **pandas** holds a table as a DataFrame; masks select rows, and a **rule** is just a mask
- A cleaning workflow: **profile → standardise → validate → treat → verify and load** — in a script, on a **copy** of the raw data
- Missing values, duplicates and outliers each need a **decision**: drop, fill, repair, flag or ask
- **Standardise before matching**; when removing duplicates, **re-point** what refers to them
- Cleaning **moves** defects, it does not create correct data — **validate** in code, **enforce** with constraints, fix at the **source**

---

# Next Session: Accessing Data — Files and APIs

- Reading **CSV**, **Excel** and **JSON** with pandas: options that prevent cleaning work
- **REST APIs** and JSON: requests, responses, status codes
- Calling an API from Python; **authentication** and **rate limits**
- Hands-on: fetch data from a public **open data** API

::: callout
**Preparation:** finish the hands-on questions and worksheet 14; check that `import requests` works in Jupyter (`pip install requests` if not); find one open data source your team could use.
:::

---

# References {.references}

- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- pandas development team. (n.d.-a). *Working with missing data*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/user_guide/missing_data.html
- pandas development team. (n.d.-b). *pandas.to_datetime*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
- pandas development team. (n.d.-c). *Comparison with SQL*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_sql.html
- pandas development team. (n.d.-d). *What's new in 3.0.0 (January 21, 2026)*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/whatsnew/v3.0.0.html
- Pipino, L. L., Lee, Y. W., & Wang, R. Y. (2002). Data quality assessment. *Communications of the ACM, 45*(4), 211–218. https://doi.org/10.1145/505248.506010
- Rahm, E., & Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.
- Rubin, D. B. (1976). Inference and missing data. *Biometrika, 63*(3), 581–592. https://doi.org/10.1093/biomet/63.3.581
- SQLite. (n.d.). *SQLite foreign key support*. Retrieved October 21, 2026, from https://www.sqlite.org/foreignkeys.html
- Tukey, J. W. (1977). *Exploratory data analysis*. Addison-Wesley.
- Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33. https://doi.org/10.1080/07421222.1996.11518099
