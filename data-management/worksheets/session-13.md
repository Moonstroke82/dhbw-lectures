---
course: Data Management
session: 13
title: Data Quality I
subtitle: Practice tasks on data quality dimensions, business rules, metrics, measurement in SQL, and the causes and costs of poor data
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 13 on your own or with your project team. Tasks 1–3, 5 and the exam-style task can be done on paper (a calculator helps). For task 4 and the optional challenge you need Jupyter with Python's built-in `sqlite3` module and the sports club's merged member list [sportsclub-members-session13.sql](data/sportsclub-members-session13.sql); all names in the data are fictional. The in-class hands-on on the bike shop needs [bikeshop-schema.sql](data/bikeshop-schema.sql), [bikeshop-data.sql](data/bikeshop-data.sql), [bikeshop-data-session09.sql](data/bikeshop-data-session09.sql) and [bikeshop-dq-session13.sql](data/bikeshop-dq-session13.sql). The terms follow the session slides, which are based on Wang and Strong (1996), Pipino et al. (2002), Batini et al. (2009), Haug et al. (2011), the Government Data Quality Hub (2021), DAMA International (2017, Chapter 13) and the SQLite documentation (SQLite, n.d.-a, n.d.-b).

```python
import sqlite3

con = sqlite3.connect(":memory:")
with open("sportsclub-members-session13.sql", encoding="utf-8") as f:
    con.executescript(f.read())

def run(sql, con=con):
    """Run one statement; show the rows, the changed rows or the error."""
    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        print(rows if cur.description else f"{cur.rowcount} row(s) changed")
    except sqlite3.Error as e:
        print(type(e).__name__, "-", e)
```

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. Data quality can be judged from the data alone, without knowing what the data is used for.
2. A date of birth of 1900-01-01 is valid, but probably not accurate.
3. Completeness can always be measured as the share of non-NULL values in a column.
4. Accuracy can usually be checked with a `CHECK` constraint.
5. Wang and Strong (1996) derived their data quality dimensions from a survey of data consumers.
6. A simple-ratio metric of 95 % means that the data is fit for use.
7. Hidden costs of poor data are costs that management is not aware of.
8. The most economical goal for a company is always 100 % data quality.

::: answer lines=10
:::

::: solution
1. **False.** Data quality means fitness for use (Wang & Strong, 1996): the same data can be good enough for one task and not for another.
2. **True.** The value has a correct format and range (valid), but it is a typical default or dummy value and very unlikely to be the person's real birth date (accuracy).
3. **False.** Completeness depends on the rule: a NULL can be correct (a bike in stock has no owner; an adult member needs no parent's phone). Some rules are conditional, e.g. "every youth member has a parent's phone".
4. **False.** A `CHECK` constraint tests validity (format, range). Accuracy needs a comparison with reality or a trusted reference, e.g. a stock count or asking the customer.
5. **True.** They grouped the attributes named by data consumers into 15 dimensions in four categories (intrinsic, contextual, representational, accessibility).
6. **False.** Whether 95 % is good enough depends on the threshold the business sets for the use; for payment data it may be far too low, for a newsletter more than enough.
7. **True** (Haug et al., 2011). Example: staff spend hours correcting lists by hand, but nobody records this time as a cost.
8. **False.** The cost of assuring quality keeps rising, so the total cost is usually lowest below 100 % (Haug et al., 2011). The goal is "good enough" for the use.

Marking: one point per statement; for false statements, the point requires a correct correction.
:::

## Which Dimension? The Food Co-op

The food co-op's volunteers have collected complaints about their data. For each problem, name the **dimension** that is violated first (completeness, validity, accuracy, consistency, uniqueness, timeliness), and write **one rule** that would detect it — or say why no rule can.

1. The member list contains Ute Brenner twice: once as "U. Brenner", once with her full name, both with the same phone number.
2. The pick-up list for Tuesday is printed on Monday at noon; orders placed on Monday afternoon are missing.
3. In the product list, the price of honey is stored as "7,50" in some rows and "7.50" in others.
4. A farm's phone number in the list is a correct-looking German number, but it belongs to a hairdresser.
5. Some orders have no pick-up location, so the volunteers do not know where to put the box.
6. The member app stores the pick-up location as "LA", the order spreadsheet as "Ladenburg".
7. An order has the quantity −3.

::: hint
First ask: does the value break a rule about the value itself (format, range), about its relationship to other values or records, or about reality? Then ask whether a computer could check it without leaving the database.
:::

::: answer lines=12
:::

::: solution
Accept a second dimension where the reasoning is sound.

1. **Uniqueness**: one member, two records. Rule: no two members with the same phone number (or the same e-mail address); `GROUP BY phone HAVING count(*) > 1`. Name similarity alone ("U. Brenner") needs a fuzzy comparison.
2. **Timeliness**: the data was correct at noon, but out of date when it was used. Rule: the list must be produced after the order deadline (a process rule), or compare the print time with the newest order time.
3. **Validity** (format), also representational consistency: a price must be a number with a decimal point. Rule: `typeof(price) IN ('integer', 'real')` or `price GLOB '*,*'` finds the comma values. Cause: German number format typed into a text field.
4. **Accuracy**: the value is valid but does not reflect reality. **No rule** in the database can find it; only a comparison with reality (calling the number, checking the farm's website) or a trusted reference.
5. **Completeness**: a value needed for the use is missing. Rule: `pickup IS NOT NULL` for every order (a `NOT NULL` constraint if the schema can be changed).
6. **Consistency** across systems (representation): both values may be correct, but they cannot be joined or compared. Rule: every location code must appear in a reference table of locations with its code and full name.
7. **Validity** (range): a quantity must be positive. Rule: `quantity > 0` (a `CHECK` constraint as in session 7).

Marking: one point per problem for a correct dimension and a fitting rule (or the reasoning why no rule works in 4).
:::

## Metrics by Hand: Car-Sharing Vehicles

The car-sharing company's planning team exported its vehicle list on **2027-04-01**:

| licence_plate | model | drive | mileage_km | last_service | station |
|---|---|---|---|---|---|
| MA-CS 101 | VW ID.3 | electric | 41250 | 2027-03-10 | Hauptbahnhof |
| MA-CS 102 | VW ID.3 | electric | 38900 | 2026-11-02 | Hauptbahnhof |
| MA-CS 103 | Fiat 500e | Electric | NULL | 2027-01-15 | Jungbusch |
| MA-CS 104 | Fiat 500e | electric | 12030 | NULL | Neckarstadt |
| MA-CS 105 | Opel Corsa | petrol | −150 | 2026-09-30 | Lindenhof |
| MA-CS 106 | Opel Corsa | petrol | 55120 | 2025-02-01 | NULL |
| MA-CS 107 | Renault Zoe | electric | 61400 | 2027-02-20 | Hauptbahnhof |
| MA-CS 101 | VW ID.3 | electric | 41250 | 2027-03-10 | Hauptbahnhof |
| MA-CS 108 | Renault Zoe | petrol | 23800 | 2026-12-12 | Jungbusch |
| MA-CS 109 | Toyota Yaris | hybrid | 30500 | 15.01.2027 | Lindenhof |

Allowed values for `drive`: electric, petrol, diesel, hybrid. The Renault Zoe is an electric car only.

1. Compute the **simple ratio** (in %) for each rule. State the numerator and the denominator, and explain your choice of denominator.
   - a) `last_service` is present
   - b) `mileage_km` is not negative
   - c) `last_service` is a valid ISO date
   - d) each licence plate appears once
   - e) `drive` is one of the allowed values (compared exactly, case-sensitive)
2. Find one **consistency** problem and one **completeness** problem that the rules above do not cover.
3. For **service planning**, the team weights the rules a) 0.5, b) 0.3 and d) 0.2. Compute the weighted average and the **min** of the three. Which of the two would you report to the fleet manager, and why?

::: hint
For validity, check only the values that are there — otherwise a missing value counts as a defect twice (once for completeness, once for validity).
:::

::: answer lines=14
:::

::: solution
1. Ratios (results checked in SQLite 3.45.1 with the same data):
   - a) completeness: 9 of 10 rows have a date → **90 %** (MA-CS 104 missing). Denominator: all rows, because every vehicle needs a service date.
   - b) validity: 8 of the 9 rows with a mileage → **88.9 %** (MA-CS 105 with −150). Denominator: the 9 non-NULL values; MA-CS 103's missing mileage is a completeness defect.
   - c) validity: 8 of the 9 dates → **88.9 %** ('15.01.2027' for MA-CS 109 is German format, not ISO).
   - d) uniqueness: 9 distinct plates in 10 rows → **90 %** (MA-CS 101 twice, an exact duplicate row).
   - e) validity: 9 of 10 values are in the list → **90 %** ('Electric' for MA-CS 103 fails the exact comparison — a representation problem; with a case-insensitive comparison 100 %). Denominator: all 10 rows (no NULLs).
   Counting the duplicate MA-CS 101 once instead of twice is also acceptable if stated (then e.g. a) is 8/9).
2. Consistency: MA-CS 108, a Renault Zoe with drive "petrol" (contradicts the model; a valid value that is still wrong). Completeness: MA-CS 106 has no station, MA-CS 103 no mileage. Also good: MA-CS 106's last service is more than a year old (2025-02-01) — either the service is overdue or it was not recorded (a question of timeliness or accuracy that only the workshop can answer).
3. Weighted average: 0.5 × 90 + 0.3 × 88.9 + 0.2 × 90 = 45 + 26.67 + 18 = **89.7 %** (with the exact ratio 8/9: 89.67 %). Min: **88.9 %** (mileage validity). The min shows the weakest point and cannot be "rescued" by good values elsewhere — useful when every rule must hold, e.g. a vehicle with a wrong mileage may miss its service interval. The weighted average is better for following a trend over time. Either answer with a reason is correct; the best answers report both, or the min plus the list of failing vehicles.

Marking: part 1 five points (one per ratio with a sound denominator), part 2 one point, part 3 two points.
:::

## Lab: The Sports Club's Member List

Run the set-up cell from the introduction. The football and the tennis department kept separate spreadsheets; a volunteer has merged them into `member_list`. The club rules: `member_type` is `adult` or `youth` (under 18 on the reference date **2027-06-01**); every **youth** member needs a `parent_phone`; `department` must exist in the table `department`. Predict each result before you run the query.

1. **Profile** the table: number of rows and of distinct member numbers, non-NULL values per column, the values of `member_type` and `department` with their frequencies, min and max of `joined_on`. List what looks suspicious.
2. **Completeness**: the share of members with an e-mail address, and the share of members **under 18** (by birth date) who have a parent's phone. Why is a NULL in `parent_phone` not always a defect?
3. **Validity**: the share of rows whose department is in the reference table, whose `joined_on` is a valid ISO date not after 2027-06-01, and whose `member_type` is exactly `adult` or `youth`.
4. **Uniqueness**: which member numbers are used more than once? Which persons (name and birth date) appear more than once — and is that necessarily an error?
5. **Consistency**: members whose `member_type` does not fit their age, and members who joined **before they were born**. Look closely at the second result.
6. **Fit for use**: the city pays the club a grant per youth member. How many youth members does the club have? Give the numbers the different interpretations of the data lead to, and decide which one you would report.

::: hint
`date('2027-06-01', '-18 years')` gives the cut-off date: members born after it are under 18 (SQLite, n.d.-a). `x IS date(x)` is true for a valid ISO date — and also for NULL. A comparison is 1 or 0 in SQLite, so `sum(condition)` counts the rows where it holds.
:::

::: answer lines=18
:::

::: solution
All statements were run with Python 3.13 and SQLite 3.45.1 on exactly this file; results as observed.

1. `SELECT count(*), count(DISTINCT member_no), count(e_mail), count(parent_phone), min(joined_on), max(joined_on) FROM member_list;` → 16 rows, **15** member numbers, 10 e-mails, 6 parent phones, min **'01.05.2016'**, max **'2027-08-15'**. `GROUP BY member_type` → adult 8, youth 6, **Youth** 1, **A** 1. `GROUP BY department` → Football 9, Tennis 6, **Footbal** 1. Suspicious: one member number too few, four type codes for two types, a misspelt department, a German date (it sorts as the "smallest" text) and a joining date in the future.
2. E-mail: `round(100.0 * count(e_mail) / count(*), 1)` → **62.5 %** (10 of 16). Parent phone: `… WHERE birth_date > date('2027-06-01', '-18 years')` → 8 members under 18, 6 with a phone → **75 %**; missing for M104 Lena Vogt and M107 Jonas Klein. Adults need no parent's phone, so their NULLs are correct: the rule is **conditional**, and the denominator is the youth members only.
3. Department: `LEFT JOIN department d ON d.name = m.department` → **93.8 %** (15/16; M105 'Footbal'). Joining date: `sum(joined_on IS date(joined_on) AND joined_on <= '2027-06-01')` → **87.5 %** (14/16; M109 '01.05.2016', M115 2027-08-15 in the future). Member type: `sum(member_type IN ('adult', 'youth'))` → **87.5 %** (14/16; M106 'Youth', M109 'A').
4. `GROUP BY member_no HAVING count(*) > 1` → **M108** for Eva Brandt and Nils Brandt: two people share one key — a uniqueness defect of the identifier (93.8 %), probably both departments numbered independently, or a family membership typed in twice. `GROUP BY name, birth_date HAVING count(*) > 1` → **Lena Vogt**, M104 (Tennis) and M112 (Football). Not necessarily an error: a member may play in two departments. But the list stores one row per member **and** department with two member numbers — a design problem (an M:N relationship squeezed into one table, session 6). The club must decide whether she is one member with two department memberships.
5. Type vs. age: `WHERE (birth_date > date('2027-06-01', '-18 years')) <> (lower(member_type) = 'youth')` → **M107 Jonas Klein**, born 2012-02-17, marked adult (15/16 = 93.8 %). He is also the second youth without a parent's phone — the wrong type hid him from a check on `member_type`. Joined before birth: `WHERE joined_on < birth_date` → M111 Tim Sommer (joined 1994-06-01, born 1995-01-20) **and** M109 Ida Krüger — but M109 is a **false alarm**: '01.05.2016' < '1969-10-10' as text. Check validity first (`AND joined_on IS date(joined_on)` leaves only M111).
6. `member_type = 'youth'` → **6**; `lower(member_type) = 'youth'` → **7** (adds M106); by birth date → **8 rows**, but Lena Vogt twice → **7 persons** (adds M107, removes the duplicate). Report the number based on **birth date, counting persons once (7)**, because the grant depends on age, not on a code typed by a volunteer; document the two corrections (M107's type, Lena Vogt's duplicate) and fix them at the source.

Marking: one point per question; for 5 the point requires spotting the false alarm, for 6 a justified choice.
:::

## Causes and Costs: The Coworking Space

The coworking space has opened a second location. Since then, members complain, and the manager asks you to analyse the situation. What is known:

- Bookings are entered at reception in a **spreadsheet** at the new location and in the **booking app** at the old one; once a month an intern copies the spreadsheet into the app database.
- Some members have **two member numbers**, one per location; the monthly invoice then comes twice.
- Reception staff spend about **two hours a week** looking up members in both systems and correcting invoices before they are sent.
- The utilisation report for the new location is **one month late**, so the manager decided to rent additional desks based on last quarter's numbers.
- Desk numbers at the new location are free text ("D 4", "D4", "Desk 4").

1. Name **four causes** of poor data quality in this case and assign each to a type of cause from the session (data entry, missing rules, integration, data decay, processes and organisation, migration).
2. Classify **four costs** in the matrix of Haug et al. (2011): direct or hidden, operational or strategic. Justify one hidden cost.
3. Propose **three measures** that fix the problem **at the source** rather than downstream, and name the dimension each one improves.

::: answer lines=16
:::

::: solution
1. Causes (any four):
   - Two systems for one business, copied monthly → **integration** (and timeliness: data arrives late).
   - Free-text desk numbers and spreadsheet input → **missing rules** (no list of valid values) and **data entry**.
   - Two member numbers per person → **integration** / missing rules (no common key, no duplicate check).
   - Monthly manual copying by an intern, nobody responsible for the member data → **processes and organisation**.
   - Copying from a spreadsheet into the app is a small **migration** each month, with format problems.
2. Costs (examples):
   - Double invoices to members → **direct, operational** (visible: complaints, corrections, possibly refunds).
   - Two hours a week of reception time for checking and correcting → **hidden, operational**: nobody books it as a data quality cost; it looks like normal reception work (the "hidden data factory", Redman, 2016).
   - Renting extra desks based on outdated utilisation numbers → **hidden** or **direct, strategic** (a long-term decision on poor data; hidden as long as nobody links the wrong decision to the data).
   - Members' annoyance and lost trust, cancelled memberships → **hidden, strategic**.
   The justification of a hidden cost must say that management is not aware of it as a cost of poor data.
3. Measures at the source (any three):
   - Use the booking app at both locations, no spreadsheet → consistency, timeliness.
   - One member number per person, with a duplicate check (e.g. by e-mail) when a member registers → uniqueness.
   - Desk numbers chosen from a list of valid desks (a reference table, a foreign key) → validity, consistency.
   - Name a person responsible for member data (a data owner or steward, session 19) and measure the duplicate rate monthly → all dimensions, monitoring.
   Correcting invoices by hand before sending is a downstream fix and does not count.

Marking: part 1 two points (four causes, half a point each), part 2 two points (four costs, half a point each, justification required for full marks), part 3 two points.
:::

## Exam-Style Task: The Coworking Space's Member List

This task is in the style of an exam question. The coworking space wants to send all monthly invoices **by e-mail** from now on. The plan codes are FLEX, FIX and DAY. Extract of the member list:

| member_no | name | e_mail | plan_code | start_date |
|---|---|---|---|---|
| M1 | Jonas Weber | jonas.weber@example.com | FLEX | 2026-01-15 |
| M2 | Sara Öztürk | sara.oeztuerk@example.org | FIX | 2026-03-01 |
| M3 | Tim Lang | NULL | NULL | 2026-04-10 |
| M4 | Nora Haas | nora.haas@example | FLEX | 2026-05-02 |
| M5 | Jonas Weber | jonas.weber@example.com | FLEX | 2026-01-15 |
| M6 | Ali Kaya | ali.kaya@example.net | FIXX | 2026-07-01 |
| M7 | Julia Roth | julia.roth@example.org | FIX | 2027-13-01 |
| M8 | Ben Graf | ben.graf@example.com | DAY | 2026-09-20 |

1. Define data quality and explain, with this list, why the same data can be fit for one use and not for another. (2 points)
2. Identify **four different** data quality problems in the list. Name the record, the problem and the dimension. (4 points)
3. Compute the **completeness** of `e_mail` and the **validity** of `plan_code` as simple ratios. State numerator and denominator. (2 points)
4. All e-mail addresses except M4's have a valid format. Can the coworking space conclude that the invoices will reach the right people? Explain how this could be measured. (1 point)
5. Name a likely **cause** of the problem with M1 and M5 and one **measure at the source**. (1 point)

::: answer lines=20
:::

::: solution
Marking guide (10 points):

1. (2 points) Data quality is the fitness of data for use by its data consumers (Wang & Strong, 1996) — 1 point. Example from the list — 1 point: for e-mail invoicing, M3's missing e-mail and M4's broken address are critical; for counting members per plan or planning desks, the e-mail does not matter, but the plan codes (M3, M6) do.
2. (4 points, one per problem with record, problem and correct dimension; any four):
   - M3: no e-mail and no plan → **completeness**
   - M4: 'nora.haas@example' has no domain ending → **validity** (format)
   - M1 and M5: the same person twice → **uniqueness** (double invoice)
   - M6: 'FIXX' is not a plan code → **validity** (domain; also consistency with the plan list)
   - M7: '2027-13-01' — there is no month 13 → **validity**
3. (2 points) Completeness of e_mail: 7 of 8 rows have a value → **87.5 %** (denominator: all members, because every member gets an invoice) — 1 point. Validity of plan_code: 6 of the 7 non-NULL codes are FLEX, FIX or DAY → **85.7 %** (denominator: the 7 existing codes; M3's NULL is a completeness defect) — 1 point. 7/8 = 87.5 % for plan validity with NULL counted as invalid is accepted if the choice is explained.
4. (1 point) No: a valid format is **validity**, not **accuracy**. An address may be valid but belong to someone else or no longer be used (data decay). Measure it by comparison with reality: send a confirmation e-mail with a link and count the confirmed addresses, or count bounced e-mails.
5. (1 point) Cause: e.g. the member registered twice (at two locations, or once online and once at reception) and the system does not check for an existing e-mail address — data entry / missing rule / integration. Measure at the source: a `UNIQUE` constraint or a duplicate check on the e-mail address at registration, one member number per person.

Deduct no points for a different but correct dimension where the problem fits two (e.g. M6 as consistency).
:::

## Optional Challenge: A Quality View for the Club {.optional}

Build a **view** `dq_member` on the sports club's `member_list` that returns one row per rule with the columns `rule`, `dimension` and `pct` — at least five rules from the lab task, from at least four dimensions. Then:

1. Correct the department of M105 with an `UPDATE` and query the view again. What changes, and why do you not need to rebuild the view?
2. Write a query that returns the **weakest** rule. Which one is it, and what would you do first?

::: hint
Combine one `SELECT … FROM member_list` per rule with `UNION ALL`. A conditional rule gets its own `WHERE`. Views run their query every time they are used (session 10).
:::

::: answer lines=12
:::

::: solution
Run on a fresh copy of the file in SQLite 3.45.1; results as observed.

```sql
CREATE VIEW dq_member AS
SELECT 'e-mail present' AS rule, 'completeness' AS dimension,
       round(100.0 * count(e_mail) / count(*), 1) AS pct FROM member_list
UNION ALL
SELECT 'parent phone for youth', 'completeness',
       round(100.0 * count(parent_phone) / count(*), 1)
FROM member_list WHERE birth_date > date('2027-06-01', '-18 years')
UNION ALL
SELECT 'department in list', 'validity',
       round(100.0 * sum(department IN (SELECT name FROM department)) / count(*), 1) FROM member_list
UNION ALL
SELECT 'joined_on valid date', 'validity',
       round(100.0 * sum(joined_on IS date(joined_on) AND joined_on <= '2027-06-01') / count(*), 1) FROM member_list
UNION ALL
SELECT 'member_no unique', 'uniqueness',
       round(100.0 * count(DISTINCT member_no) / count(*), 1) FROM member_list
UNION ALL
SELECT 'type fits age', 'consistency',
       round(100.0 * sum((birth_date > date('2027-06-01', '-18 years'))
                         = (lower(member_type) = 'youth')) / count(*), 1) FROM member_list;
```

`SELECT * FROM dq_member;` → e-mail present 62.5 · parent phone for youth 75.0 · department in list 93.8 · joined_on valid date 87.5 · member_no unique 93.8 · type fits age 93.8.

1. `UPDATE member_list SET department = 'Football' WHERE department = 'Footbal';` → 1 row; "department in list" is now **100.0**. A view stores only the query, not the result, so it always shows the current data — this is how a simple monitoring of data quality works (the scorecard is re-run, e.g. every month).
2. `SELECT rule, pct FROM dq_member ORDER BY pct LIMIT 1;` (or `min(pct)`) → **e-mail present, 62.5**. Whether to act first depends on the use: for an e-mail newsletter it is the most important gap; for safety and youth grants, the parent phone (75 %) and the type check matter more. The lowest number is not automatically the most important problem.

Other rules are fine if they work and are explained.
:::

## References {.references}

- Batini, C., Cappiello, C., Francalanci, C., & Maurino, A. (2009). Methodologies for data quality assessment and improvement. *ACM Computing Surveys, 41*(3), 1–52. https://doi.org/10.1145/1541880.1541883
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Government Data Quality Hub. (2021, June 24). *Meet the data quality dimensions*. GOV.UK. https://www.gov.uk/government/news/meet-the-data-quality-dimensions
- Haug, A., Zachariassen, F., & van Liempd, D. (2011). The costs of poor data quality. *Journal of Industrial Engineering and Management, 4*(2), 168–193. https://doi.org/10.3926/jiem.2011.v4n2.p168-193
- Pipino, L. L., Lee, Y. W., & Wang, R. Y. (2002). Data quality assessment. *Communications of the ACM, 45*(4), 211–218. https://doi.org/10.1145/505248.506010
- Redman, T. C. (2016, September 22). Bad data costs the U.S. $3 trillion per year. *Harvard Business Review*. https://hbr.org/2016/09/bad-data-costs-the-u-s-3-trillion-per-year
- SQLite. (n.d.-a). *Date and time functions*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_datefunc.html
- SQLite. (n.d.-b). *SQL language expressions*. Retrieved October 21, 2026, from https://www.sqlite.org/lang_expr.html
- Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33. https://doi.org/10.1080/07421222.1996.11518099
