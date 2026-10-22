---
course: Data Management
session: 14
title: Data Quality II: Data Cleaning with Python
subtitle: Practice tasks on pandas basics, missing values, duplicates, outliers, inconsistent formats and validation rules
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 14 on your own or with your project team. Tasks 1, 3 and the exam-style task can be done on paper; for task 2 a notebook helps but is not required. For tasks 4 and 5 you need Jupyter with pandas and the car-sharing company's trip export [carsharing-trips-session14.csv](data/carsharing-trips-session14.csv); the optional challenge uses the sports club's member list from worksheet 13, [sportsclub-members-session13.sql](data/sportsclub-members-session13.sql). All names and data are fictional. The in-class hands-on on the bike shop needs the four scripts of session 13 and [webshop-orders-session14.csv](data/webshop-orders-session14.csv). The terms follow the session slides, which are based on Rahm and Do (2000), McKinney (2022, Chapters 5–7), the pandas documentation (pandas development team, n.d.-a, n.d.-b), Tukey (1977) and Pipino et al. (2002). The results in the solutions were produced with pandas 3.0.6; with pandas 2.x, text columns show the dtype `object` instead of `str`, everything else is the same.

```python
import sqlite3
import pandas as pd

trips = pd.read_csv("carsharing-trips-session14.csv")
STATIONS = ["Hauptbahnhof", "Jungbusch", "Neckarstadt", "Lindenhof"]
MEMBERS = [f"C{i:03d}" for i in range(1, 13)]     # C001 … C012
```

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. `df["x"] == np.nan` finds the missing values in column `x`.
2. `drop_duplicates()` without arguments removes only rows that are identical in every column.
3. A value outside Tukey's fences is an error and should be deleted.
4. Setting an invalid postcode to missing raises the validity ratio and lowers the completeness ratio.
5. Duplicates should be searched for **before** the text columns are standardised, so that no information is lost.
6. `pd.to_datetime(..., errors="coerce")` turns values it cannot parse into `NaT`.
7. Filling missing prices with 0 is a neutral choice that does not change the average price.
8. The raw export should be overwritten with the cleaned data, so that there are not two versions.

::: answer lines=10
:::

::: solution
1. **False.** `NaN == NaN` is `False`, so the comparison never finds a missing value; use `df["x"].isna()` (pandas development team, n.d.-a).
2. **True.** Without `subset`, all columns are compared, and the first copy is kept (`keep="first"`). Records of the same entity with small differences (e.g. 'anna berger' and 'Anna Berger') are not removed.
3. **False.** An outlier is unusual compared with the other values, not necessarily wrong — a real e-bike order or a weekend rental can lie outside the fences. Flag it and check it with a business rule or a person.
4. **True.** The invalid value leaves the denominator of the validity ratio and becomes a completeness defect — the data is not better, the defect has only moved.
5. **False.** Standardise first: 'anna berger' and 'Anna Berger' only match after the names have one format. Information is protected by keeping the raw data and a log, not by the order of the steps.
6. **True.** Check those rows afterwards: `errors="coerce"` hides parsing problems if you do not look at the new `NaT` values.
7. **False.** A 0 is counted as a real price and pulls the mean down (bike shop: 2,191.31 € → 1,899.13 €); `mean()` skips missing values on its own.
8. **False.** Keep the raw data unchanged and clean a copy with a script, so that every step can be repeated, checked and corrected.

Marking: one point per statement; for false statements, the point requires a correct correction.
:::

## Read and Write pandas: The Coworking Space's Desk Bookings

The coworking space keeps its desk bookings in a DataFrame `b` (`NaN` = missing value):

| booking_id | member_no | desk | day | hours | plan |
|---|---|---|---|---|---|
| B1 | M1 | D4 | 2027-03-01 | 8 | FLEX |
| B2 | M2 | D 4 | 2027-03-01 | 4 | FIX |
| B3 | M3 | Desk 7 | 2027-03-02 | NaN | FLEX |
| B4 | M1 | D4 | 2027-03-02 | 8 | flex |
| B5 | M4 | D12 | 2027-03-02 | 80 | DAY |
| B6 | M2 | D4 | 2027-03-03 | 6 | FIX |
| B7 | M5 | NaN | 2027-03-03 | 3 | DAY |
| B8 | M1 | D4 | 2027-03-01 | 8 | FLEX |

For 1–3, write the pandas expression and give the result. For 4–6, give the result and explain it.

1. The number of bookings without a desk.
2. The booking IDs with more than 10 hours.
3. The number of bookings per plan, as `value_counts()` shows it — and after `str.upper()`.
4. `b.groupby("member_no")["hours"].sum()` — what does it return for M3, and why is that misleading?
5. `b["desk"].str.replace(r"\D", "", regex=True)` removes every character that is not a digit. How many different desks are there before and after this step?
6. `b["hours"].mean()` and `b["hours"].fillna(0).mean()`. Which one is right, and is either of them a good description of a typical booking?

::: hint
`\D` in a regular expression means "not a digit". `sum()` and `mean()` skip missing values; `groupby` keeps a group even if all its values are missing.
:::

::: answer lines=14
:::

::: solution
All results were checked with pandas 3.0.6 on exactly this table.

1. `b["desk"].isna().sum()` → **1** (B7). Also correct: `len(b[b["desk"].isna()])`.
2. `b.loc[b["hours"] > 10, "booking_id"]` → **B5** (80 hours in one day — an outlier and almost certainly a typo; a plausibility rule "at most 24 hours per day" finds it). B3 with NaN is not returned: a comparison with NaN is `False`.
3. `b["plan"].value_counts()` → FLEX 3, FIX 2, DAY 2, flex 1; with `b["plan"].str.upper().value_counts()` → FLEX 4, FIX 2, DAY 2.
4. M3 → **0.0**: the sum of no values is 0, so a missing value turns into "zero hours". A report "M3 used 0 hours" is wrong — the hours are unknown. Use `min_count=1` (`sum(min_count=1)` gives NaN) or report the missing value separately.
5. Before: 4 desk values ('D4', 'D 4', 'Desk 7', 'D12'; `nunique()` ignores NaN). After: **3** ('4', '7', '12'). Standardising reveals a **consistency problem**: on 2027-03-01, desk 4 is booked by M1 (B1, B8) and by M2 (B2) — a double booking that the raw spelling hid. B8 is also an exact copy of B1 apart from the booking ID (same member, desk and day): a duplicate to remove after checking.
6. `mean()` → **16.71** (7 known values), `fillna(0).mean()` → **14.63** (8 values, one invented 0). The first is right in the sense that it does not invent data, but neither is typical: B5's 80 hours pull the mean up; the **median** is **8.0**. Clean B5 and the duplicate B8 first, then describe.

Marking: one point per question; in 4 and 6 the point requires the explanation.
:::

## Which Treatment? The Sports Club

For each problem in the sports club's data, choose **drop**, **fill**, **repair**, **flag** or **ask** (combinations are allowed), and justify your choice in one or two sentences.

1. Phone numbers are stored as `'0621 1234 102'`, `'06211234102'` and `'+49 621 1234102'`.
2. The fitness log shows a member weighing **720 kg**.
3. The department of one member is `'Footbal'`.
4. A youth member has no parent's phone number; the club rules require one.
5. The monthly fee is empty for all **honorary members**; by the club statutes, honorary members pay no fee.
6. The same person appears in the tennis and the football list with two different member numbers.
7. A training session lists **31 participants** for a team of 18 players.

::: answer lines=12
:::

::: solution
Other answers with a sound reason are fine.

1. **Repair** (standardise): remove spaces, convert to one format (e.g. E.164 `+496211234102`) with a documented rule. No information is lost.
2. **Flag and ask**: probably 72.0 kg with a missing decimal point, but the value must not be changed without confirmation. Rule-based outlier (a plausibility range, e.g. 30–250 kg).
3. **Repair** with a mapping to the reference list of departments (`replace({"Footbal": "Football"})`); afterwards validate against the list.
4. **Flag and ask**: the number cannot be invented or filled from anywhere unless another record of the same person has it (then fill from that trusted source). Safety-relevant: follow up quickly.
5. **Fill with 0**: here the missing value has a known meaning set by a rule (the statutes); document the rule. Contrast: a missing bike price is not 0.
6. **Ask, then merge**: confirm it is one person, choose a surviving member number, and re-point the department memberships of the other number. Dropping one record would lose a department membership.
7. **Flag and ask**: an outlier compared with the team size, but it may be real (guest players, a joint training). Do not delete — attendance may matter for insurance or grants.

Marking: one point per case for a fitting treatment with a reason.
:::

## Lab: Clean the Car-Sharing Trips

Run the set-up cell from the introduction. The car-sharing company exported the trips of June 2027 from its booking system. Plates have the format `MA-CS 101` (one space); valid stations are in `STATIONS`, valid member numbers in `MEMBERS`. Work on a copy `t = trips.copy()` and predict each result before you run it.

1. **First look**: shape, dtypes, missing values per column, the frequencies of `station`, the number of different `plate` values. Why is `distance_km` a `float64` column but `duration_min` an `int64` column?
2. **Standardise** `station` (spaces, case, the abbreviation `Hbf`) and `plate` (case, one space). How many stations and plates remain?
3. **Exact duplicates**: find and remove them. What would have happened to the total distance of June without this step?
4. **Dates**: parse `trip_date` with the formats you find. Which trips have a date that cannot be repaired?
5. **Missing and impossible values**: trips without a distance, trips with a duration of 0 or less, trips of unknown members.
6. **Outliers**: compute Tukey's fences (1.5 × IQR) for `distance_km` and for `duration_min`. Then check the plausibility rule "average speed at most 130 km/h". Which trips are outliers by which method, and which of them are probably **errors**?

::: hint
`str.replace(r"^MA-CS\s*", "MA-CS ", regex=True)` puts exactly one space after the prefix. The average speed is `distance_km / (duration_min / 60)`. `x.quantile([0.25, 0.75])` returns both quartiles.
:::

::: answer lines=18
:::

::: solution
All results observed with pandas 3.0.6 on exactly this file.

1. `trips.shape` → (21, 7); `trip_id`, `plate`, `member_no`, `station`, `trip_date` are `str`, `duration_min` is `int64`, `distance_km` is `float64`; `isna().sum()` → only `distance_km` 2. `value_counts()` of station → Hauptbahnhof 6, Jungbusch 4, Neckarstadt 3, Lindenhof 3, Hbf 2, ' jungbusch' 1, LINDENHOF 1, 'Neckarstadt ' 1 — **8 spellings** of 4 stations. `nunique()` of plate → **11** spellings of 9 cars ('MA-CS104', 'ma-cs 106'). `distance_km` has missing values, and `NaN` is a float, so the whole column becomes float; `duration_min` has none and stays integer.
2. `t["station"] = t["station"].str.strip().str.title().replace({"Hbf": "Hauptbahnhof"})` → **4** stations; `t["plate"] = t["plate"].str.upper().str.replace(r"^MA-CS\s*", "MA-CS ", regex=True)` → **9** plates. (Order matters: `title()` before the mapping, otherwise 'HBF' variants would be missed in future exports.)
3. `t.duplicated().sum()` → 1: **T-511** appears twice (same ID, same values). `t = t.drop_duplicates()` → 20 trips. Total distance: 5,720 km with the duplicate, **5,080 km** without — the weekend trip's 640 km would have been counted twice.
4. `iso = pd.to_datetime(t["trip_date"], format="%Y-%m-%d", errors="coerce")`, `ger = pd.to_datetime(t["trip_date"], format="%d.%m.%Y", errors="coerce")`, `t["trip_date"] = iso.fillna(ger)` → T-507 and T-519 parsed from the German format; **T-517** ('2027-06-31') stays `NaT` — June has 30 days; flag it and ask (the booking system's log has the real date).
5. Missing distance: **T-506, T-515** (flag; the odometer readings could fill it). Duration ≤ 0: **T-508** (0 minutes, 0 km — probably a cancelled booking; check with the business whether to keep it as a cancellation) and **T-514** (−15 minutes — invalid, probably start and end swapped). Unknown member: **T-513** with C015 (an orphan; ask, or check whether the member list is outdated).
6. Distance: Q1 8.0, Q3 23.5, IQR 15.5, upper fence 46.75 → **T-503** (4,120 km), **T-509** (95 km), **T-511** (640 km), **T-519** (58 km). Duration: Q1 30, Q3 80, IQR 50, upper fence 155 → **T-509** (180 min), **T-511** (2,880 min). Speed rule → only **T-503** (2,602 km/h in 95 minutes). Errors: only T-503 is impossible (probably 41.2 km or an odometer typo — ask). T-511 is a weekend rental (48 h, 640 km, 13 km/h on average), T-509 and T-519 are plausible longer trips. Lower fences are negative and find nothing; the negative duration of T-514 is found by the rule, not by statistics. Effect: without T-503, the distance of June is 960 km instead of 5,080 km.

Marking: one point per question; for 6 the point requires the distinction between statistical outliers and errors.
:::

## Lab: Validation Rules and Loading

Continue with the cleaned trips `t` from the previous task (20 trips, before treating the problems of questions 4–6).

1. Write the rules as a dictionary of boolean masks — at least: station in the list, trip date valid, member known, distance present, duration positive, average speed at most 130 km/h — and build a report with the pass rate in % and the failing trip IDs.
2. Run the same rules on the **raw** export (`trips`). Which rates changed through standardisation, and which did not change at all? Why?
3. Create a SQLite table `trip` with a primary key and `CHECK` constraints for the station list and a positive duration. Try to load all 20 cleaned trips with `to_sql(..., if_exists="append")`. What happens?
4. Load only the trips that pass **all** rules into `trip`, and the others into a table `trip_review`. How many rows land where? Is it right to keep T-506 out of `trip`?

::: hint
`pd.concat(rules, axis=1).all(axis=1)` gives one mask that is `True` where every rule holds. Dates must be written as ISO text: `t["trip_date"].dt.strftime("%Y-%m-%d")`. A rule about the speed should not fail for trips without a distance — they are already caught by another rule.
:::

::: answer lines=16
:::

::: solution
Run with pandas 3.0.6 and SQLite 3.45.1; results as observed.

```python
d, k = t["duration_min"], t["distance_km"]
rules = {
    "station in list":        t["station"].isin(STATIONS),
    "trip date valid":        t["trip_date"].notna(),
    "member known":           t["member_no"].isin(MEMBERS),
    "distance present":       k.notna(),
    "duration positive":      d > 0,
    "speed at most 130 km/h": (k / (d / 60)).le(130) | k.isna() | (d <= 0),
}
report = pd.DataFrame({
    "pass_pct": {r: round(100 * m.mean(), 1) for r, m in rules.items()},
    "failing":  {r: ", ".join(t.loc[~m, "trip_id"]) for r, m in rules.items()}})
```

1. Cleaned (20 trips): station 100.0 · trip date 95.0 (T-517) · member 95.0 (T-513) · distance 90.0 (T-506, T-515) · duration 90.0 (T-508, T-514) · speed 95.0 (T-503).
2. Raw (21 rows; trip date checked as ISO text): station **76.2** (T-504, T-505, T-507, T-509, T-512), trip date **85.7** (T-507, T-517, T-519), member 95.2, distance 90.5, duration 90.5, speed 95.2. Standardisation repaired the station spellings and the German dates. Member, distance, duration and speed did not improve — their problems cannot be repaired by reformatting; they need a decision or a person. The small differences (95.2 → 95.0) come only from the removed duplicate (21 → 20 rows): a different denominator.
3. pandas raises `DatabaseError: Execution failed` caused by `sqlite3.IntegrityError: CHECK constraint failed: duration_min > 0`; afterwards the table has **0 rows** — the insert runs as one transaction and is rolled back.
4. `ok = pd.concat(rules, axis=1).all(axis=1)` → **13** trips into `trip`, **7** into `trip_review` (T-503, T-506, T-508, T-513, T-514, T-515, T-517). T-511 (the weekend rental) is loaded: it breaks no rule. T-506: the trip happened and must be invoiced; only the distance is missing. Keeping it out of `trip` is a defensible choice for a "clean" table, but the better design is often to load it with `distance_km` NULL (the `CHECK (distance_km >= 0)` allows NULL) and a flag, so that reports do not miss a real trip. Either answer with this reasoning is correct.

Marking: 1 two points, 2 one point, 3 one point, 4 two points (numbers one point, reasoning about T-506 one point).
:::

## Exam-Style Task: The Food Co-op's Orders

This task is in the style of an exam question. The food co-op loaded its weekly orders into a DataFrame `orders` (`NaN` = missing value):

| order_no | member | product | quantity | pickup | order_date |
|---|---|---|---|---|---|
| F01 | Ute Brenner | Honey | 2 | Ladenburg | 2027-05-04 |
| F02 | ute brenner␣ | Honey | 2 | Ladenburg | 2027-05-04 |
| F03 | Jan Ott | Potatoes | 5 | LA | 2027-05-04 |
| F04 | Mira Sander | Eggs | 120 | Schriesheim | 2027-05-05 |
| F05 | Jan Ott | Apples | NaN | Ladenburg | 2027-05-05 |
| F06 | Paul Kern | Potatoes | 3 | NaN | 05.05.2027 |
| F07 | Mira Sander | Eggs | −6 | Schriesheim | 2027-05-06 |
| F08 | Lisa Wolf | Apples | 2 | Schriesheim | 2027-05-06 |

(␣ = a space at the end of the name.)

```python
orders.isna().sum()                                                  # (a)
orders["member"].nunique()                                           # (b)
orders["member"].str.strip().str.title().nunique()                   # (c)
orders.loc[~orders["quantity"].between(1, 50), "order_no"]           # (d)
pd.to_datetime(orders["order_date"], format="%Y-%m-%d",
               errors="coerce").isna().sum()                         # (e)
```

1. Give the results of (a) to (e). What does the difference between (b) and (c) tell you? (3 points)
2. Name **four different** data quality problems in the table. For each, give the record, the dimension and a suitable treatment (repair, fill, drop, flag or ask). (4 points)
3. Explain why F05 appears in the result of (d). Is that what the rule should do? (1 point)
4. The co-op wants to order eggs from the farm and computes `orders.loc[orders["product"] == "Eggs", "quantity"].sum()`, which gives **114**. Explain why this number must not be sent to the farm and what the co-op should do instead. (2 points)

::: answer lines=20
:::

::: solution
Marking guide (10 points). All results checked with pandas 3.0.6 on exactly this table.

1. (3 points; half a point each for (a)–(e), half a point for the interpretation)
   - (a) order_no 0, member 0, product 0, **quantity 1**, **pickup 1**, order_date 0.
   - (b) **6** different member values; (c) **5** after removing spaces and unifying case.
   - (d) **F04, F05, F07**.
   - (e) **1** (F06's German date).
   - (b) vs. (c): 'Ute Brenner' and 'ute brenner ' are the same person written in two ways — a representation problem that also hides a possible duplicate.
2. (4 points; one per problem with record, dimension and a fitting treatment; any four):
   - F01/F02: the same order twice (same member, product, quantity and date) → **uniqueness**; ask Ute Brenner, then drop one (do not drop without asking: she may really want four jars).
   - F03: 'LA' instead of 'Ladenburg' → **consistency** (representation); repair with a mapping to the list of pick-up locations.
   - F04: 120 eggs → **accuracy/plausibility** (an outlier, probably 12); flag and ask.
   - F05: no quantity → **completeness**; ask Jan Ott (do not fill with a guess).
   - F06: no pick-up location → **completeness**; ask, or fill only if Paul Kern always picks up at the same place (a trusted rule). Its date '05.05.2027' → **validity** (format); repair by parsing the German format.
   - F07: −6 eggs → **validity** (range); flag — possibly a cancellation booked as a negative order; ask.
3. (1 point) `between(1, 50)` is `False` for NaN, so `~` makes it `True`: the missing quantity is reported as "outside the range". Useful as a work list (F05 needs attention), but it mixes a completeness defect with a validity defect; a clean rule set checks `notna()` separately and applies the range only to existing values.
4. (2 points) 114 = 120 + (−6): it includes the implausible 120 (probably 12) and the negative −6, and ignores that F04 and F07 may be an order and its correction (1 point). The co-op must not change the numbers silently: flag F04 and F07, ask Mira Sander, then sum the confirmed quantities — e.g. 12 − 6 = 6 if F07 cancels part of F04, or 12 + 6 = 18 if both are orders; report the open questions with the number (1 point).

Deduct no points for a different but sound dimension where a problem fits two (e.g. F01/F02 as consistency).
:::

## Optional Challenge: A Reusable Cleaning Function for the Sports Club {.optional}

Load the sports club's member list from worksheet 13 into pandas (`pd.read_sql("SELECT * FROM member_list", con)` after running the script). Write a function `clean_members(raw)` that returns the cleaned DataFrame **and** a change log (one row per changed value: member number, column, old value, new value, rule). It should

- standardise `member_type` ('Youth' → 'youth', 'A' → 'adult') and repair the department 'Footbal',
- parse `joined_on` (two formats) and set dates in the future (after 2027-06-01) or before the birth date to missing,
- set `member_type` from the age on 2027-06-01 (under 18 → youth).

Then answer: how many youth **rows** and how many youth **persons** are there? Which youth members still have no parent's phone, and could one of the gaps be filled from another record? Check that `raw` was not changed.

::: hint
`raw.copy()` at the start of the function protects the input. For the log, compare old and new values per column; remember that `NaN == NaN` is `False`. `birth > pd.Timestamp("2027-06-01") - pd.DateOffset(years=18)` marks members under 18.
:::

::: answer lines=12
:::

::: solution
One possible solution (run with pandas 3.0.6):

```python
REF = pd.Timestamp("2027-06-01")

def clean_members(raw):
    df, log = raw.copy(), []
    def change(col, new, rule):
        old = df[col]
        diff = ~((old == new) | (old.isna() & new.isna()))
        for i in df.index[diff]:
            log.append({"member_no": df.at[i, "member_no"], "column": col,
                        "old": old[i], "new": new[i], "rule": rule})
        df[col] = new
    change("member_type", df["member_type"].str.lower().replace({"a": "adult"}), "type code")
    change("department", df["department"].replace({"Footbal": "Football"}), "department list")
    j = pd.to_datetime(df["joined_on"], format="%Y-%m-%d", errors="coerce").fillna(
        pd.to_datetime(df["joined_on"], format="%d.%m.%Y", errors="coerce"))
    birth = pd.to_datetime(df["birth_date"], format="%Y-%m-%d")
    bad = (j > REF) | (j < birth)
    change("joined_on", j.where(~bad).dt.strftime("%Y-%m-%d"), "joined date")
    youth = birth > REF - pd.DateOffset(years=18)
    change("member_type", youth.map({True: "youth", False: "adult"}), "type from age")
    return df, pd.DataFrame(log)
```

Observed log (7 changes): M106 type 'Youth' → 'youth'; M109 type 'A' → 'adult'; M105 department 'Footbal' → 'Football'; M109 joined_on '01.05.2016' → '2016-05-01'; M111 joined_on 1994-06-01 → missing (before birth); M115 joined_on 2027-08-15 → missing (future); M107 type 'adult' → 'youth' (born 2012).

- Youth: **8 rows**, **7 persons** (Lena Vogt appears as M104 and M112) — the same 7 as the grant answer of worksheet 13, now produced by a repeatable function.
- Without parent's phone: M104 Lena Vogt and M107 Jonas Klein. Lena's gap can be filled from her other record M112 ('0621 1234 112') — a trusted source, because it is the same person (after the club confirms the duplicate). Jonas Klein must be asked.
- `raw` is unchanged (`raw.equals(...)` with a fresh `read_sql` → `True`), because the function works on a copy.

Other designs (e.g. a log built with `compare()`) are fine if they work and the log is complete.
:::

## References {.references}

- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- pandas development team. (n.d.-a). *Working with missing data*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/user_guide/missing_data.html
- pandas development team. (n.d.-b). *pandas.to_datetime*. pandas 3.0.6 documentation. Retrieved October 21, 2026, from https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html
- Pipino, L. L., Lee, Y. W., & Wang, R. Y. (2002). Data quality assessment. *Communications of the ACM, 45*(4), 211–218. https://doi.org/10.1145/505248.506010
- Rahm, E., & Do, H. H. (2000). Data cleaning: Problems and current approaches. *IEEE Data Engineering Bulletin, 23*(4), 3–13.
- Tukey, J. W. (1977). *Exploratory data analysis*. Addison-Wesley.
