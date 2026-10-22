---
course: Data Management
session: 18
title: Modern Data Architectures
subtitle: Practice tasks on data lakes, schema-on-read, the lakehouse and its layers, data mesh, data fabric, cloud service models and choosing an architecture
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 18 on your own or with your project team. Tasks 1, 2, 5, 6 and the exam-style task can be done on paper. Task 3 needs Jupyter with pandas and the food co-op's two order exports [foodcoop-orders-session11.json](data/foodcoop-orders-session11.json) (May 2027, from session 11) and [foodcoop-orders-2027-06-session18.json](data/foodcoop-orders-2027-06-session18.json) (June 2027, new). Task 4 needs SQLite (in Jupyter with Python's `sqlite3`, or the SQLite command-line tool) and the catalogue [coworking-lake-catalog-session18.sql](data/coworking-lake-catalog-session18.sql). The in-class hands-on on the bike shop uses [bikeshop-lake-catalog-session18.sql](data/bikeshop-lake-catalog-session18.sql) and the two Bright Sky files of session 15, [brightsky-mannheim-2026-10-05.json](data/brightsky-mannheim-2026-10-05.json) and [brightsky-heidelberg-2026-09-28.json](data/brightsky-heidelberg-2026-09-28.json) (weather data of the Deutscher Wetterdienst via de Maeyer, n.d.). All other names and data are fictional. The terms follow the session slides, which are based on Serra (2024), Armbrust et al. (2021), Databricks (n.d.), Dehghani (2020, 2022), Inmon (2016), Mell and Grance (2011) and Reis and Housley (2022). The results in the solutions were produced with Python 3.13, pandas 3.0.6 and SQLite 3.45.1.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. A data lake stores data in its raw, native format and applies a structure when the data is read.
2. Schema-on-read means that the data in a lake has no structure at all.
3. A data swamp is a lake whose files cannot be found, trusted or explained because metadata and ownership are missing.
4. A lakehouse keeps two copies of the data: one in the lake for machine learning and one in a warehouse for BI.
5. In the medallion architecture, the gold layer holds the raw data exactly as it was received.
6. An organisation can introduce a data mesh by buying the right platform product.
7. In a data mesh, the business domain that knows the data best owns it and serves it as a product.
8. A data fabric typically connects data where it is stored, using a metadata catalogue, data virtualisation and access policies.
9. With platform as a service (PaaS), the customer installs and patches the database software.
10. According to NIST, rapid elasticity and measured service are essential characteristics of cloud computing.

::: answer lines=10
:::

::: solution
1. **True.**
2. **False.** The structure is still needed, but it is applied by every reader when the data is read (in the reading code), not enforced when the data is stored.
3. **True.**
4. **False.** The lakehouse keeps **one** copy in open file formats on lake storage and adds warehouse features (transactions, schema enforcement, versions) on top; two copies are the two-tier "lake + warehouse" architecture.
5. **False.** Raw data is in **bronze**; gold holds modelled, aggregated data ready for reports, often a star schema.
6. **False.** Data mesh is an organisational approach (domain ownership, data as a product, self-serve platform, federated governance); a tool can support it but does not create domain ownership.
7. **True.**
8. **True.**
9. **False.** With PaaS the provider runs the platform (database software, patches, often backups); the customer brings data and code. Installing and patching yourself is IaaS.
10. **True.** (The five characteristics: on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service.)

Marking: one point per statement; a false statement needs a correct correction for the point.
:::

## Where Does It Go? The Food Co-op

The food co-op (420 members, two volunteers who know SQL) keeps more and more data. For each item, say whether it belongs in the **bronze**, **silver** or **gold** layer of a small lake — or **outside** the lake — and whether it is read with **schema-on-read** or loaded with **schema-on-write**. Give a one-line reason.

1. Photos of the farmers' delivery notes, taken with a phone
2. The JSON order exports, exactly as the shop software delivers them
3. One table of order lines with harmonised column names and parsed dates
4. Weekly revenue per pickup point for the board meeting
5. The cleaned member table with one row per member
6. Click logs of the co-op's newsletter

Then: should the co-op buy a lakehouse platform? Answer in two sentences.

::: answer lines=10
:::

::: hint
Bronze is "as received, never changed", silver "cleaned and validated", gold "modelled and ready for reports". Ask for each item: has anyone changed it yet, and who will read it?
:::

::: solution
1. **Bronze**, schema-on-read: unstructured files, stored as they are; the delivered quantities can later be typed into a silver table. Keep them with farm, date and owner in a catalogue.
2. **Bronze**, schema-on-read: raw and unchanged, so that silver can be rebuilt if the cleaning code has a bug or the export format changes (as in task 3).
3. **Silver**, schema-on-write: cleaned, typed and validated — a table with a fixed schema (or a database table with constraints).
4. **Gold**, schema-on-write: aggregated and ready for the report; it can be a view or a small fact table on the silver data.
5. **Silver**, schema-on-write: cleaned master data. Accept gold if the student argues it is the member dimension of a star (session 17).
6. **Bronze**, schema-on-read — or **outside** the lake if there is no purpose: click logs are personal data (session 19), and storing them "just in case" turns into a swamp. Accept both with the purpose argument.

Lakehouse platform: **no**. Two volunteers and a few MB of data do not need a platform with a transaction log and cluster compute; a folder with bronze files, a catalogue and an SQLite database (silver and gold as tables or views) follow the same layer idea at almost no cost. Revisit only if volumes, users or use cases (e.g. machine learning) grow.

Marking: one point per item (zone and reason; schema-on-read/write must fit), two points for the lakehouse answer with a reason from the case.
:::

## Lab: Schema-on-Read with Two Order Exports

The co-op's shop software was updated in June 2027. The May orders are in the old format ([foodcoop-orders-session11.json](data/foodcoop-orders-session11.json)), the June orders in the new one ([foodcoop-orders-2027-06-session18.json](data/foodcoop-orders-2027-06-session18.json)). Both files sit unchanged in the bronze layer.

1. Open both files in a text editor. List **four** differences in structure, field names or formats.
2. Read the order **lines** of both files with `pd.json_normalize` (use `record_path` and `meta`), and concatenate the two results without any changes. How many rows and columns do you get — and why so many columns?
3. Build one **silver** table with the columns `order_id`, `order_date` (a date), `member_no`, `pickup`, `product`, `unit_price`, `quantity`, `unit`, `paid` (True/False). Watch out for one May line that uses a different field name for the quantity.
4. Compute the revenue (`unit_price × quantity`) of **paid** orders per month, and per month and pickup point.
5. Which orders of the two files appear in **none** of your rows? Is that a problem for task 4?
6. Write down **three** rules that the co-op's pipeline should check every time a new export arrives, so that the next format change is noticed **loudly**.

::: answer lines=18
:::

::: hint
The May file is a list of orders; the June file is an object whose orders are under the key `"orders"`. Nested fields such as the member number in May need a list in `meta`: `["member", "member_no"]`. Parse the two date formats separately with `format=` before you concatenate.
:::

::: solution
**1.** Any four, e.g.: the top level is a list (May) vs. an object with `export` and `orders` (June); `order_no` 1, 2, … vs. `order_id` "2027-06-0001"; `date` ISO `2027-05-04` vs. `order_date` German `01.06.2027`; `member` nested object with name vs. `member_no` only; `pickup` vs. `pickup_point`; `items` vs. `lines`; `price` vs. `unit_price`; new field `unit`; `paid` true/false vs. `status` "paid"/"cancelled"; May has an optional `note`; one May line uses `qty` instead of `quantity`.

**2.**
```python
import json
import pandas as pd

with open("foodcoop-orders-session11.json", encoding="utf-8") as f:
    may = json.load(f)
with open("foodcoop-orders-2027-06-session18.json", encoding="utf-8") as f:
    june = json.load(f)

m = pd.json_normalize(may, record_path="items",
                      meta=["order_no", "date", "pickup", "paid", ["member", "member_no"]])
j = pd.json_normalize(june["orders"], record_path="lines",
                      meta=["order_id", "order_date", "member_no", "pickup_point", "status"])
naive = pd.concat([m, j], ignore_index=True)
naive.shape          # (25, 17)
```

May gives (15, 10), June (10, 10); together **25 rows and 17 columns**: pandas puts fields with different names into different columns and fills the gaps with NaN (`price` and `unit_price`, `date` and `order_date` …). No error, no warning — schema-on-read leaves the harmonisation to the reader.

**3.**
```python
m2 = pd.DataFrame({
    "order_id": m["order_no"].astype(str),
    "order_date": pd.to_datetime(m["date"], format="%Y-%m-%d"),
    "member_no": m["member.member_no"],
    "pickup": m["pickup"],
    "product": m["product"],
    "unit_price": m["price"],
    "quantity": m["quantity"].fillna(m["qty"]),      # order 6: honey with "qty"
    "unit": pd.NA,                                    # not in the old format
    "paid": m["paid"],
})
j2 = pd.DataFrame({
    "order_id": j["order_id"],
    "order_date": pd.to_datetime(j["order_date"], format="%d.%m.%Y"),
    "member_no": j["member_no"],
    "pickup": j["pickup_point"],
    "product": j["product"],
    "unit_price": j["unit_price"],
    "quantity": j["quantity"],
    "unit": j["unit"],
    "paid": j["status"].eq("paid"),
})
lines = pd.concat([m2, j2], ignore_index=True)    # shape (25, 9)
```

Accept other ways (renaming with `rename`, a mapping dictionary). The unit is unknown for May — `NA` is honest; inventing "kg" would be a guess.

**4.**
```python
lines["revenue"] = lines["unit_price"] * lines["quantity"]
paid = lines[lines["paid"]]
month = paid["order_date"].dt.to_period("M")
paid.groupby(month)["revenue"].sum().round(2)
paid.groupby([month, "pickup"])["revenue"].sum().round(2)
```

Paid revenue: **May 88.40**, **June 70.10**. Per pickup point: May Edingen 38.10, Ladenburg 50.30; June Edingen 20.20, Ladenburg 49.90. Without the paid filter: May 93.70 (order 3 is not paid), June 91.10 (order 2027-06-0004, apple juice 21.00, is cancelled). Without `fillna(m["qty"])` the honey line of order 6 (15.00) would be lost silently.

**5.** May order **5** has an empty `items` list (note "Cancelled by member"), so `record_path` produces no row for it — the same effect as the inner join of `json_each` in session 11. For revenue this is harmless (no lines, no revenue), but a count of orders from the lines table would show 7 instead of 8 May orders. Count orders from the order level, not from the lines.

**6.** Any three, e.g.: the expected keys are present in every record (`order_date`, `lines`, `quantity`, …) — otherwise stop and log; every date parses with the expected format; `quantity` > 0 and `unit_price` > 0 and not missing; `status` only takes known values; the number of orders and the revenue total roughly match the shop's own monthly summary; an unknown new field is reported in the run log (session 16).

Marking: one point per question; 3 needs the qty/quantity case and both date formats.
:::

## Lab: Computational Governance for the Coworking Lake

The coworking space keeps a catalogue of its data lake. Load [coworking-lake-catalog-session18.sql](data/coworking-lake-catalog-session18.sql) into a database of its own. The management has agreed four **global rules**:

| Rule | Text |
|---|---|
| R1 | Every dataset has an **owner** and a **purpose**. |
| R2 | Personal data that is **not pseudonymised** must have the access level **restricted**. |
| R3 | No dataset is kept beyond its **retention date**. |
| R4 | Every **gold** dataset was updated within the last **30 days**. |

1. How many datasets and how many MB are in each zone? Where is most of the volume?
2. Write **one query per rule** that lists the datasets that violate it. Use **31 March 2027** as today's date.
3. Combine the four checks into one query with one row per violating dataset and one column per rule (1 = violated).
4. Which datasets with personal data have **no retention date** at all? Why does your R3 query not find them — and should it?
5. "Computational" governance means the platform runs these checks automatically. Name **two** moments at which the checks should run, and what should happen when one fails.

::: answer lines=16
:::

::: hint
A condition such as `retention_until < '2027-03-31'` is unknown (NULL) when `retention_until` is NULL — session 8's three-valued logic. For R4, `date('2027-03-31', '-30 days')` gives the cut-off date. In the combined query, a comparison returns 1 or 0 in SQLite; wrap a possibly NULL comparison in `coalesce(…, 0)`.
:::

::: solution
**1.**
```sql
SELECT zone, count(*) AS datasets, round(sum(size_mb), 1) AS mb
FROM lake_dataset GROUP BY zone ORDER BY min(dataset_id);
```

bronze 8 datasets 2,704.8 MB · silver 4 datasets 6.2 MB · gold 4 datasets 21.1 MB. Almost all volume is raw data in bronze (CCTV snapshots 1,450 MB, Wi-Fi sessions 880 MB, badge scans 310 MB).

**2.**
```sql
-- R1
SELECT dataset_id, path FROM lake_dataset WHERE owner IS NULL OR purpose IS NULL;
-- R2
SELECT dataset_id, path, access_level FROM lake_dataset
WHERE personal_data = 1 AND pseudonymised = 0 AND access_level <> 'restricted';
-- R3
SELECT dataset_id, path, retention_until FROM lake_dataset
WHERE retention_until < '2027-03-31';
-- R4
SELECT dataset_id, path, last_updated FROM lake_dataset
WHERE zone = 'gold' AND last_updated < date('2027-03-31', '-30 days');
```

R1: 4 (Wi-Fi sessions), 16 (churn features). R2: 2 (booking app exports), 4 (Wi-Fi sessions), 7 (event sign-ups), 14 (dim_member) — all "internal". R3: 1 (badge scans, 2027-01-31), 6 (CCTV snapshots, 2027-02-28), 7 (event sign-ups, 2027-03-15). R4: 16 (churn features, last updated 2026-11-02, 149 days ago). Dataset 15 (updated 2027-03-01, exactly 30 days ago) does **not** violate R4 — accept it as a violation only if the student states that they read "within 30 days" as "fewer than 30 days".

**3.**
```sql
SELECT dataset_id, path,
       (owner IS NULL OR purpose IS NULL)                                     AS r1,
       (personal_data = 1 AND pseudonymised = 0 AND access_level <> 'restricted') AS r2,
       coalesce(retention_until < '2027-03-31', 0)                            AS r3,
       (zone = 'gold' AND last_updated < date('2027-03-31', '-30 days'))      AS r4
FROM lake_dataset
WHERE r1 + r2 + r3 + r4 > 0;
```

Seven datasets: 1 (R3) · 2 (R2) · 4 (R1, R2) · 6 (R3) · 7 (R2, R3) · 14 (R2) · 16 (R1, R4). Without `coalesce`, the rows with a NULL retention date get NULL in r3, the sum becomes NULL, and datasets 4 and 16 disappear from the result although they violate R1 (and R2 or R4).

**4.** Datasets **4** (Wi-Fi sessions) and **16** (churn features) contain personal data and have no retention date. The R3 query cannot find them: the comparison with NULL is unknown, not true. It should: a fifth rule "personal data must have a retention date" (or R3 extended with `OR (personal_data = 1 AND retention_until IS NULL)`) closes the gap — storage limitation is a GDPR principle (session 19). Note also that datasets 1 and 6 are still being filled (last update 30/31 March) although their retention date has passed — a rolling retention period per file (e.g. delete scans older than 60 days) fits better than one date per dataset.

**5.** For example: (a) **before publishing** a new or changed dataset to silver or gold — block the publication until owner, purpose, access level and retention date are set; (b) **every night** over the whole catalogue — report violations to the owner, escalate to the data governance board after a deadline, automatically restrict access (R2) or delete expired data (R3) where the rule allows it. Good answers mention that the rules are agreed **centrally** but each **domain** fixes its own datasets (federated).

Marking: one point each for 1, 4 and 5; two points for 2 (half a point per rule); one point for 3 (needs the NULL handling).
:::

## Data Mesh at the Car-Sharing Company

The car-sharing company has grown: 1,800 cars in eight cities. Five departments work with data — **fleet and maintenance**, **bookings and trips**, **billing and payments**, **customer service** and **marketing** — and each has one or two analysts. A central data team of three people runs the warehouse and has a backlog of eleven weeks.

1. Name **four** domains and for each **one data product** it could own, with one consumer of that product.
2. Write a short **product description** for the data product "trips per station and hour": owner, content and grain, update frequency, two quality figures, access and personal data.
3. Formulate **two global rules** of federated governance and say how the platform can **enforce** them automatically.
4. Marketing wants "trips per customer segment and city". Which data products must be combined, and what must the domains agree on first so that this works?
5. Name **two** risks of the mesh for this company, and **one** situation in which you would advise against a mesh.
6. A colleague says: "Let's build a data fabric instead." Explain the difference in two sentences.

::: answer lines=16
:::

::: solution
**1.** For example: fleet and maintenance — "vehicle status per day" (battery, mileage, damage) → used by bookings (which cars can be rented). Bookings and trips — "trips per station and hour" → used by fleet (where to relocate cars) and marketing. Billing and payments — "revenue per trip" → used by finance and marketing. Customer service — "complaints per vehicle and category" → used by fleet. Marketing — "customer segments" → used by bookings and customer service. Any four plausible pairs.

**2.** Example: **Owner:** bookings and trips domain, product owner named. **Content and grain:** number of trip starts and trip minutes per station and hour (one row per station and hour). **Update:** daily by 06:00 for the previous day. **Quality figures:** completeness (share of trips with a station, e.g. ≥ 99 %), timeliness (delivered on time on ≥ 98 % of days), reconciliation with billing (trip count per day equal). **Access:** internal, no personal data (aggregated; no member numbers). Optional: schema with column types, documentation link, version and deprecation notice.

**3.** Examples: (a) "Every data product has an owner, a description and a schema" — the platform refuses to publish a product without these catalogue fields. (b) "Personal data is pseudonymised before it leaves its domain" — the platform masks columns tagged as personal data automatically. (c) "All products use the shared station and date keys" — a schema check in the publishing pipeline. Any two with an automatic mechanism.

**4.** Trips (bookings and trips) and customer segments (marketing), possibly revenue (billing). The domains must agree on a **shared customer key** (and segment definitions) and a **shared city/station key** — the conformed dimensions of session 17. Without them, the products cannot be joined, or every consumer builds their own mapping.

**5.** Risks: duplicated effort and cost (every domain builds pipelines); one or two analysts per department may lack data engineering skills; inconsistent definitions across domains ("trip" with or without cancelled bookings); long organisational change. Advise against: few domains or no data skills in the domains, a small company, or when the central team's backlog can be solved more cheaply (e.g. more staff, a self-service BI tool).

**6.** A data mesh is mainly **organisational**: ownership moves to the domains, which serve data as products. A data fabric is mainly **technical**: a metadata-driven layer (catalogue, virtualisation, access policies) connects data where it is, usually run centrally — the two can be combined.

Marking: one point per question; 2 needs owner, grain and at least one quality figure.
:::

## Cloud Service Models

1. Classify each offering as **IaaS**, **PaaS** or **SaaS** and give a reason:
   a) A virtual server; the coworking space installs Ubuntu and PostgreSQL itself.
   b) A managed PostgreSQL service with automatic updates and backups.
   c) An online accounting application in the browser.
   d) A cloud data warehouse service: you create tables and load data, and pay per query.
   e) A storage service where the sports club keeps files ("buckets").
   f) An online form tool for the sports club's event registrations.
2. In a) and b): who installs the security updates of the database software?
3. The warehouse in d) adds computing power automatically at the end of each month and charges by the amount of data scanned. Which **two** NIST characteristics does this show?
4. Name **two** risks of moving the food co-op's member data to a cloud service — and one question to ask the provider before signing.

::: answer lines=12
:::

::: solution
1. a) **IaaS** — infrastructure only; operating system and database are run by the customer. b) **PaaS** — the provider runs the database platform; the customer brings schema and data. c) **SaaS** — a complete application. d) **PaaS** — a managed data platform; the customer still designs tables and writes SQL (some providers call it SaaS; accept with this reason). e) **IaaS** (storage infrastructure); accept PaaS if the student argues that the storage service is managed. f) **SaaS**.
2. a) The **customer** (the coworking space). b) The **provider**.
3. **Rapid elasticity** (capacity grows and shrinks with demand) and **measured service** (usage is metered and billed).
4. Risks, e.g.: data stored outside the EU or accessible by foreign authorities (GDPR, session 19); lock-in (data and skills tied to one provider, hard to move); unclear or rising costs; dependence on the network and the provider's availability. Question, e.g.: "Where (in which country) are the data and backups stored?", "Can we export all data in an open format at any time?", "Is there a data processing agreement?"

Marking: half a point per offering in 1 (3 points), one point each for 2–4 (4 needs two risks and a question).
:::

## Exam-Style Task: An Architecture for a Sports Federation

This task is in the style of an exam question.

A regional sports federation supports **140 member clubs**. Its office has two IT staff, one of them part-time; the clubs are run by volunteers. The federation holds:

- each club's **annual membership report** (Excel, one file per club, fixed template)
- **grant applications** of the clubs (PDF, with scanned receipts)
- **course bookings** for coach education (the database of a web application)
- **new:** occupancy **sensor readings** from 30 sports halls, one value per hall every minute (JSON)

The board wants dashboards on membership trends and course bookings, and a pilot that predicts the demand for sports halls.

1. Classify the four data sources as structured, semi-structured or unstructured, and say for each whether you would load it into a **warehouse** or keep it in a **lake** (or both). (2 points)
2. Recommend an architecture for the federation and give **three** reasons from the case. (3 points)
3. A consultant proposes a **data mesh** with the 140 clubs as domains. Give **two** reasons against it, and name **one** idea of the data mesh that the federation should adopt anyway. (2 points)
4. Describe what the **bronze**, **silver** and **gold** layers contain for the hall sensor data. (2 points)
5. Name **two** risks of running the solution on a cloud platform. (1 point)

::: answer lines=24
:::

::: solution
Marking guide (10 points).

**1.** (2 points; half a point per source, classification and place must both fit) Membership reports: **structured** (fixed template) → load into the **warehouse** (raw files kept in the lake's bronze layer). Grant applications: **unstructured** (PDF, scans) → **lake**; amounts and dates may be extracted into the warehouse. Course bookings: **structured** (database) → **warehouse**. Sensor readings: **semi-structured** (JSON), high frequency → **lake** (raw), aggregates per hall and hour into the warehouse or gold layer.

**2.** (3 points; one per reason from the case, the recommendation must match the reasons) A good answer: a **small lakehouse** (or a lake plus a small warehouse) on a managed cloud platform (PaaS), with bronze/silver/gold layers. Reasons: mixed data types (Excel, PDF, JSON) need lake storage; dashboards need modelled, trusted tables (gold, a star for membership and bookings); the prediction pilot needs the raw sensor detail — one copy for BI and ML; a team of 1.5 people cannot operate servers, so managed services fit. Also accepted: a **warehouse plus a simple lake folder** if the student argues that the sensor pilot is small and skills are limited. Not accepted without strong reasons: a data mesh or a large self-built platform. One point is lost if the reasons do not refer to the case.

**3.** (2 points) Against (one point for two reasons): clubs are volunteer organisations without data skills or staff to own data products; 140 small "domains" would multiply effort; the federation is the only consumer that needs the integrated view; a central office with two IT staff is not a bottleneck that a mesh would remove. Adopt anyway (one point): **data as a product** — e.g. the annual report template as a documented product with an owner, a schema and quality checks (completeness, deadline); or federated governance rules such as "every report uses the federation's club number".

**4.** (2 points) **Bronze:** the JSON readings as received, per hall and day, unchanged (with hall, time of receipt). **Silver:** typed and validated readings — one row per hall and minute, duplicates removed, impossible values (negative occupancy, more people than capacity) flagged, time zone fixed. **Gold:** aggregates for the dashboard and the model — occupancy per hall, weekday and hour (a fact table with date, time and hall dimensions) and the features of the prediction pilot. Half a point for bronze, one for silver (at least two cleaning steps), half for gold.

**5.** (1 point; half a point per risk) E.g. personal data of members and coaches stored outside the EU or without a data processing agreement; running costs rising with data volume and careless queries; lock-in to one provider; dependence on the network; nobody in the small team with cloud skills.
:::

## References {.references}

- Armbrust, M., Ghodsi, A., Xin, R., & Zaharia, M. (2021). Lakehouse: A new generation of open platforms that unify data warehousing and advanced analytics. In *CIDR 2021: Conference on Innovative Data Systems Research*. https://vldb.org/cidrdb/2021/lakehouse-a-new-generation-of-open-platforms-that-unify-data-warehousing-and-advanced-analytics.html
- Databricks. (n.d.). *What is the medallion lakehouse architecture?* Databricks documentation. Retrieved October 22, 2026, from https://docs.databricks.com/aws/en/lakehouse/medallion.html
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Dehghani, Z. (2020, December 3). *Data mesh principles and logical architecture*. martinfowler.com. https://martinfowler.com/articles/data-mesh-principles.html
- Dehghani, Z. (2022). *Data mesh: Delivering data-driven value at scale*. O'Reilly Media.
- Inmon, B. (2016). *Data lake architecture: Designing the data lake and avoiding the garbage dump*. Technics Publications.
- Mell, P., & Grance, T. (2011). *The NIST definition of cloud computing* (NIST Special Publication 800-145). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-145
- Reis, J., & Housley, M. (2022). *Fundamentals of data engineering: Plan and build robust data systems*. O'Reilly Media.
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
