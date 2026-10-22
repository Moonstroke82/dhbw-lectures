---
course: Data Analytics
session: 15
title: Big Data Analytics with Spark
subtitle: Practice tasks on Spark jobs and shuffles, Spark SQL and DataFrames, evaluating price estimates and choosing a tool — plus a portfolio-style analysis of the new-build premium
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 15 on your own or in the lab. Tasks 1–5 need only paper, pencil and a calculator. Task 6 uses PySpark (Zaharia et al., 2016) with Java 17 or later, as set up for the session, on the HM Land Registry Price Paid Data (HM Land Registry, n.d.-a). Contains HM Land Registry data © Crown copyright and database right 2021. This data is licensed under the Open Government Licence v3.0.

The terms follow the slides: **transformation** (lazy, defines a new DataFrame) and **action** (starts a job); **narrow** and **wide** transformations, where a wide one needs a **shuffle**; **partition pruning** (only the needed folders of a partitioned Parquet dataset are read); an MLlib **Pipeline** of Estimators and Transformers (Apache Software Foundation, n.d.-b). For price estimates, APE = |estimate − actual| / actual, **MdAPE** = median of the APEs, and "within ±20 %" = share of estimates with APE ≤ 0.2.

## True or False?

Decide whether each statement is true or false and give a one-sentence reason.

1. `df.filter(...).groupBy(...).agg(...)` reads the data as soon as the line has run.
2. A query written in Spark SQL usually runs slower than the same query written with the DataFrame API.
3. `groupBy` causes a shuffle, `filter` does not.
4. In local mode, Spark runs the driver and the executor in one JVM on your computer.
5. On one laptop, Spark is always faster than DuckDB because it uses all cores.
6. An MLlib `Pipeline` is fitted on the training data; the resulting `PipelineModel` applies the same encoding to the test data.

::: answer lines=8
:::

::: solution
1. **False.** Transformations are lazy: Spark only records the plan; data is read when an action such as `count()` or `show()` runs (Apache Software Foundation, n.d.-a).
2. **False.** SQL and the DataFrame API are translated into the same plan by the Catalyst optimiser and run on the same engine (Armbrust et al., 2015).
3. **True.** `groupBy` must bring all rows with the same key into one partition (wide, shuffle); `filter` works on each partition separately (narrow).
4. **True.** `local[*]` runs everything in one JVM with one worker thread per core — no cluster needed.
5. **False.** Both use all cores; Spark adds planning, JVM and shuffle overhead that pays off only beyond one machine. In the session, DuckDB was about 6–40 times faster on the same queries (McSherry et al., 2015, on single-machine baselines).
6. **True.** Fitting replaces every Estimator by its fitted Transformer; `transform()` then uses the indexes and encodings learned from the training data (Apache Software Foundation, n.d.-b).

Marking: 1 point per statement with a correct reason (6 points); no point for a correct verdict without reason.
:::

## Follow a Spark Job

A bike-sharing company stores its trips as Parquet, partitioned by month (folders `month=2025-01`, `month=2025-02`, …). `stations` is a small table with 800 stations.

```python
trips = spark.read.parquet("trips")                                   # (1)
long = trips.filter(F.col("duration_s") > 3600)                       # (2)
per_station = long.groupBy("start_station").count()                   # (3)
report = per_station.join(stations, "start_station")                  # (4)
report.write.parquet("out/long_trips")                                # (5)
members = (trips.filter(F.col("month") == "2025-07")
                .select("member_type").distinct().count())            # (6)
```

1. Mark each numbered line as transformation or action, and each transformation as narrow or wide.
2. When is the data read from disk? How often is `trips` read in total?
3. Why does line (4) probably **not** cause a shuffle of `per_station` and `stations` — and what would change if `stations` had 50 million rows?
4. Which folders does line (6) read, and why? What would happen if the filter were on `start_time` instead of `month`?
5. A colleague adds `trips.cache()` after line (1). Is this a good idea here?

::: answer lines=12
:::

::: hint
Look for the lines that return a result or write a file. For question 3, think about the smaller table: what is cheaper — moving 800 rows to every executor, or moving millions of rows between partitions?
:::

::: solution
1. (1) transformation (reads only metadata); (2) narrow; (3) wide (shuffle by `start_station`); (4) join — see question 3; (5) **action** (write); (6) `filter` and `select` narrow, `distinct` wide, `count()` **action**.
2. Only when an action runs: in (5), the rows needed for lines (2)–(4) are read; in (6), `trips` is read again (only the July folder). So `trips` is scanned twice, once in full and once for one month.
3. `stations` is far below the default broadcast threshold of 10 MB (`spark.sql.autoBroadcastJoinThreshold`), so Spark sends a copy of it to every executor and joins locally: a **broadcast join** without shuffling the large side (Apache Software Foundation, n.d.-c). With 50 million rows, both sides would be shuffled by the join key (sort-merge or shuffle hash join) — much more expensive. In `explain()`, look for `BroadcastHashJoin` vs. `SortMergeJoin`.
4. Only `month=2025-07`: the filter is on the partition column, so Spark prunes all other folders (`PartitionFilters` in the plan). A filter on `start_time` cannot prune folders; Spark reads all months, although Parquet statistics may still skip some row groups.
5. Not useful: `trips` is used twice, but the two uses read different subsets (all months vs. one month), and the full table may not fit in memory. Caching pays off when the **same** intermediate result is reused several times and fits in memory — e.g. `long` if several reports were built on it.

Marking (10 points): 1 all lines classified (3); 2 when and how often (2); 3 broadcast join with reason and the large-table case (2); 4 pruning and the `start_time` case (2); 5 judgement with reason (1).
:::

## Translate Between SQL and DataFrames

A parcel delivery company has a table `shipments` (one row per parcel) with the columns `depot`, `region`, `ship_date`, `weight_kg`, `delivered_on_time` (1/0) and `cost_eur`.

1. Write the following DataFrame code as a Spark SQL query on the view `shipments`:

```python
(shipments.filter(F.year("ship_date") == 2025)
  .groupBy("region", "depot")
  .agg(F.count("*").alias("parcels"),
       F.avg("delivered_on_time").alias("on_time_rate"),
       F.median("cost_eur").alias("median_cost"))
  .filter(F.col("parcels") >= 1000)
  .orderBy(F.desc("on_time_rate")))
```

2. Write the following query with the DataFrame API. *Hint:* use `Window` from `pyspark.sql.window`.

```sql
WITH d AS (
  SELECT region, depot, avg(delivered_on_time) AS on_time_rate
  FROM shipments WHERE year(ship_date) = 2025
  GROUP BY region, depot)
SELECT *, rank() OVER (PARTITION BY region ORDER BY on_time_rate DESC) AS rnk
FROM d
```

3. The query of question 2 is meant to give the **best two depots per region**. Complete it in SQL. Why can you not simply add `WHERE rnk <= 2` to the outer query as written?
4. Which of the three steps (filter, aggregation, window) cause a shuffle?

::: answer lines=14
:::

::: solution
1. SQL:

```sql
SELECT region, depot, count(*) AS parcels,
       avg(delivered_on_time) AS on_time_rate, median(cost_eur) AS median_cost
FROM shipments
WHERE year(ship_date) = 2025
GROUP BY region, depot
HAVING count(*) >= 1000
ORDER BY on_time_rate DESC
```

The filter after the aggregation becomes `HAVING`.

2. DataFrame API:

```python
from pyspark.sql.window import Window
d = (shipments.filter(F.year("ship_date") == 2025)
       .groupBy("region", "depot")
       .agg(F.avg("delivered_on_time").alias("on_time_rate")))
w = Window.partitionBy("region").orderBy(F.desc("on_time_rate"))
ranked = d.withColumn("rnk", F.rank().over(w))
```

3. The `WHERE` clause of a query is evaluated before the window functions of the same query's `SELECT`, so `rnk` does not exist there. Wrap the query: `SELECT * FROM (… the query of question 2 …) WHERE rnk <= 2`, or in the DataFrame API `ranked.filter("rnk <= 2")`. (DuckDB offers `QUALIFY rnk <= 2`, as in session 4.) With `rank()`, ties can return more than two depots per region; use `row_number()` if exactly two are needed.
4. The filter is narrow (no shuffle). The aggregation shuffles by (region, depot). The window shuffles by region (`PARTITION BY region`) — after the aggregation only one row per depot is left, so this shuffle is small.

Marking (10 points): 1 correct SQL incl. HAVING (3); 2 correct DataFrame code with window (3); 3 outer query or filter with reason, ties mentioned (3); 4 shuffles (1).
:::

## Are the Price Estimates Good Enough?

A property portal compares two price estimators on eight sales (in thousand £): the **baseline** (median price of the same postcode district and property type last year) and a **model** trained with MLlib.

| Sale | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Actual price | 250 | 180 | 420 | 310 | 95 | 600 | 230 | 275 |
| Baseline | 240 | 210 | 380 | 300 | 130 | 520 | 235 | 260 |
| Model | 262 | 200 | 350 | 335 | 120 | 640 | 200 | 280 |

1. Compute the APE of each estimate (in %, one decimal).
2. Compute for both estimators the MdAPE, the **mean** APE, and the number of estimates within ±10 % and within ±20 %.
3. Which estimator is better? Why do MdAPE and mean APE disagree?
4. The portal shows a range of ±20 % around the estimate. What would you tell the product manager — and what would you check on a much larger test set?

::: answer lines=12
:::

::: hint
For eight values, the median is the mean of the 4th and 5th value after sorting.
:::

::: solution
1. APE in %:

| Sale | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Baseline | 4.0 | 16.7 | 9.5 | 3.2 | 36.8 | 13.3 | 2.2 | 5.5 |
| Model | 4.8 | 11.1 | 16.7 | 8.1 | 26.3 | 6.7 | 13.0 | 1.8 |

2. Baseline: sorted 2.2, 3.2, 4.0, **5.5, 9.5**, 13.3, 16.7, 36.8 → MdAPE (5.5 + 9.5) / 2 = **7.5 %**; mean APE **11.4 %**; within ±10 %: **5**; within ±20 %: **7**. Model: sorted 1.8, 4.8, 6.7, **8.1, 11.1**, 13.0, 16.7, 26.3 → MdAPE **9.6 %**; mean APE **11.1 %**; within ±10 %: **4**; within ±20 %: **7**.
3. On the typical sale (MdAPE, within ±10 %) the baseline is better; on the mean APE the model is slightly better, because the mean is dominated by the one cheap property (sale 5), where the baseline is 37 % off. The median is robust to such single cases, the mean is not. With eight sales neither difference is meaningful — this is a calculation exercise, not evidence.
4. Both estimators put 7 of 8 sales inside a ±20 % range here, but in the session's test on 763,740 sales only about 52–54 % were within ±20 % — a ±20 % range would be wrong for almost half of the listings. Tell the product manager that the range must be wider or the estimate should be shown only where it is reliable. On the large test set, check the error **by segment** (property type, price band, region, new build), the share within ±20 % per segment, and the bias (do estimates systematically run high or low?). Keep the baseline unless the model is better on the decision-relevant measure (Provost & Fawcett, 2013).

Marking (10 points): 1 sixteen APEs (3); 2 MdAPE, mean and counts for both (3); 3 judgement and the median/mean argument (2); 4 recommendation with checks by segment (2).
:::

## Which Tool, and Why?

1. In the session, the 2024 yearly file (931,453 rows, 16 columns, 162 MB CSV) needed **232 MB** of memory after `pandas.read_csv` (pandas 3.0.6). Estimate the memory needed to load the complete file (31.6 million rows) into pandas in the same way. Would it work on a laptop with 16 GB of RAM?
2. Give two ways to analyse the complete file on that laptop **without** a cluster.
3. For each case, choose a tool (DuckDB or pandas on one machine, or Spark) and name the deciding requirement:
  - a) A start-up stores 300 GB of app events per day in cloud object storage and must compute daily KPIs for two years of history.
  - b) A data analyst explores 50 million rows of web shop orders in a Parquet file on her laptop to prepare a dashboard.
  - c) A retailer's data platform team already runs all pipelines on a Spark cluster in a lakehouse and asks you to add a weekly demand feature table.
  - d) A student team wants to show a big data framework in its case study on the Price Paid Data.

::: answer lines=12
:::

::: solution
1. 232 MB / 931,453 rows ≈ 249 bytes per row; × 31.6 million ≈ **7.9 GB**, before any copies made by joins or groupings. On a 16 GB laptop this is borderline: the operating system and other programs need memory, and operations often create temporary copies — likely to fail or swap.
2. (a) DuckDB: query the CSV or, better, a Parquet copy directly with SQL; it reads only the needed columns and can spill to disk (Raasveldt & Mühleisen, 2019). (b) Spark in local mode with a Parquet copy partitioned by year. Also accepted: pandas with only the needed columns (`usecols`), suitable dtypes and chunks, or reading the yearly files one by one.
3. a. **Spark** (or another distributed engine): about 200 TB for two years, in cloud storage — beyond one machine. b. **DuckDB** (or pandas with Parquet): 50 million rows fit on one machine; interactive exploration is faster without a cluster. c. **Spark**: the platform and the data are already there; consistency with the team's pipelines and governance decides, not the data size. d. **Spark is defensible** if the goal is to demonstrate a framework — but the group should measure against DuckDB and state honestly that one machine would be enough for 31.6 million rows (McSherry et al., 2015).

Marking (10 points): 1 estimate with calculation and judgement (3); 2 two valid ways (2); 3 four cases with tool and deciding requirement (4); honest remark on case d (1).
:::

## Portfolio-Style Task: Is There a New-Build Premium?

A mortgage bank asks: *"How much more do buyers pay for a new-build home in England and Wales — and is the premium the same for all property types and regions?"* Answer with a short PySpark notebook on the Price Paid Data. This task is practice in the style of the case study, not part of a portfolio component.

- **Data:** the yearly files 2018–2025 (download the missing years as in the lab starter) or the complete file; category A only. First check the new-build share per year from 2018 to 2025 and choose the analysis year with a reason.
- **Raw premium:** median price of new builds divided by the median of established homes, minus 1 — overall and per property type.
- **Per county and type:** the same premium for every county × property type with at least 100 new and 100 established sales; summarise the distribution per type and name the extremes.
- **Controlled premium:** an MLlib pipeline (`StringIndexer`, `OneHotEncoder`, `VectorAssembler`, `LinearRegression`) for the log price with a new-build indicator, property type, tenure, postcode district and month; translate the coefficient of the indicator into a percentage. Repeat per property type.
- **Memo:** answer first, evidence, limits, next step — at most eight sentences.

::: answer lines=8
:::

::: hint
`F.median(F.when(F.col("new_build") == "Y", F.col("price")))` gives the median of new builds within a `groupBy`. A coefficient *b* on the log scale means a premium of exp(*b*) − 1. The first entry of the `coefficients` vector belongs to the first input of the `VectorAssembler`.
:::

::: solution
Code (tested with PySpark 4.2.0 and OpenJDK 21; `p` = the Parquet data of the lab starter):

```python
import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, OneHotEncoder, VectorAssembler
from pyspark.ml.regression import LinearRegression

a = p.filter("category = 'A'")
(a.filter("year BETWEEN 2018 AND 2025").groupBy("year")
  .agg(F.round(F.avg((F.col("new_build") == "Y").cast("int")) * 100, 1).alias("pct_new"))
  .orderBy("year").show())

s = a.filter("year = 2022 AND ptype IN ('D', 'S', 'T', 'F')")
new_med = F.median(F.when(F.col("new_build") == "Y", F.col("price")))
old_med = F.median(F.when(F.col("new_build") == "N", F.col("price")))
s.agg((new_med / old_med - 1).alias("premium")).show()
s.groupBy("ptype").agg((new_med / old_med - 1).alias("premium")).show()

g = (s.groupBy("county", "ptype")
      .agg(new_med.alias("med_new"), old_med.alias("med_old"),
           F.sum((F.col("new_build") == "Y").cast("int")).alias("n_new"),
           F.sum((F.col("new_build") == "N").cast("int")).alias("n_old"))
      .filter("n_new >= 100 AND n_old >= 100")
      .withColumn("premium", F.col("med_new") / F.col("med_old") - 1))
g.groupBy("ptype").agg(F.count("*"), F.median("premium"), F.min("premium"), F.max("premium")).show()

d = (s.filter("postcode IS NOT NULL")
       .withColumn("outcode", F.split("postcode", " ")[0])
       .withColumn("month", F.month("date")).withColumn("log_price", F.log("price"))
       .withColumn("is_new", (F.col("new_build") == "Y").cast("double")))
cats = ["ptype", "tenure", "outcode"]
pipe = Pipeline(stages=[
    StringIndexer(inputCols=cats, outputCols=[c + "_i" for c in cats], handleInvalid="keep"),
    OneHotEncoder(inputCols=[c + "_i" for c in cats], outputCols=[c + "_v" for c in cats]),
    VectorAssembler(inputCols=["is_new", "month"] + [c + "_v" for c in cats], outputCol="features"),
    LinearRegression(labelCol="log_price")])
b = pipe.fit(d).stages[-1].coefficients[0]
print(np.exp(b) - 1)                                       # controlled premium, all types
for t in ["D", "S", "T", "F"]:
    print(t, np.exp(pipe.fit(d.filter(F.col("ptype") == t)).stages[-1].coefficients[0]) - 1)
```

**Choice of year:** new-build share 12.9 % (2018), 13.5 %, 13.1 %, 11.0 % (2021), 12.7 % (2022), 11.3 %, 9.5 % (2024), 6.2 % (2025). New builds are registered late, so 2024 and 2025 are still incomplete for them; 2022 is the latest year that looks complete (909,941 sales).

**Results for 2022:**

| Property type | Share new | Raw premium | Median of county premiums (cells) | Controlled premium (regression) |
|---|---|---|---|---|
| Detached | 19.8 % | −8.6 % | −2.7 % (74) | −5.6 % |
| Semi-detached | 11.5 % | +6.3 % | +7.2 % (60) | +8.5 % |
| Terraced | 4.9 % | +18.4 % | +22.8 % (46) | +22.5 % |
| Flat | 16.1 % | +54.7 % | +28.0 % (44) | +36.8 % |
| **All types** | — | **+21.4 %** | — | **+10.4 %** |

- 224 county × type cells have at least 100 new and 100 established sales. Extremes: flats in Dorset +91.6 % (£344,950 vs. £180,000), Cambridgeshire +75.7 % and West Midlands +75.4 %; detached houses in Surrey −28.6 % and Buckinghamshire −28.5 %.
- Regression on 909,859 sales: coefficient of the new-build indicator 0.099 → **+10.4 %**, R² 0.72.
- The raw premium of 21 % halves when location and type are held constant: new builds are sold in different places and as different types than the average home. A single "premium" hides opposite effects by type: new detached houses sell **below** established ones, new flats far above.

Example memo: "Controlling for location, property type, tenure and month, new-build homes sold for about 10 % more than established homes in 2022; the raw comparison (21 %) overstates the premium because new builds are a different mix. The premium depends strongly on the type: about +37 % for flats and +23 % for terraced houses, but −6 % for detached houses, and it varies widely between counties. We used 2022 because recent years are incomplete for new builds. Limits: no floor area, plot size or condition in the data — new detached houses are probably smaller than established ones, so part of the 'discount' is size, not newness; one year only; medians and a linear model on the log scale. Next step: add floor area from energy performance certificates and repeat for several years."

Marking guide (30 points; training only):

- **Data and choice of year** (6 points): category A filter (1); new-build share per year computed (2); late registration recognised and a complete year chosen with a reason (3).
- **Raw and per-cell premiums** (8 points): correct medians and premium overall and by type (3); county × type cells with minimum counts (3); distribution and extremes reported (2).
- **Controlled premium** (8 points): working pipeline with sensible features (4); coefficient correctly converted to a percentage (2); per-type models or an interaction (2).
- **Interpretation** (5 points): composition effect explained (2); opposite effects by type (1); limits — missing size variables, one year (2).
- **Memo** (3 points): answer first (1); evidence and limits (1); next step (1).

A strong submission notices that the overall premium is a mix of very different type-specific effects and does not present the regression coefficient as a causal "value of newness".
:::

## References {.references}

- Apache Software Foundation. (n.d.-a). *RDD programming guide* (Spark 4.2.0 documentation). Retrieved October 22, 2026, from https://spark.apache.org/docs/latest/rdd-programming-guide.html
- Apache Software Foundation. (n.d.-b). *ML pipelines* (Spark 4.2.0 documentation). Retrieved October 22, 2026, from https://spark.apache.org/docs/latest/ml-pipeline.html
- Apache Software Foundation. (n.d.-c). *Performance tuning* (Spark 4.2.0 documentation, Spark SQL guide). Retrieved October 22, 2026, from https://spark.apache.org/docs/latest/sql-performance-tuning.html
- Armbrust, M., Xin, R. S., Lian, C., Huai, Y., Liu, D., Bradley, J. K., Meng, X., Kaftan, T., Franklin, M. J., Ghodsi, A., & Zaharia, M. (2015). Spark SQL: Relational data processing in Spark. In *Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data*. ACM. https://doi.org/10.1145/2723372.2742797
- HM Land Registry. (n.d.-a). *Price Paid Data* [Data set]. GOV.UK. Retrieved October 22, 2026, from https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads
- McSherry, F., Isard, M., & Murray, D. G. (2015). Scalability! But at what COST? In *15th Workshop on Hot Topics in Operating Systems (HotOS XV)*. USENIX Association. https://www.usenix.org/conference/hotos15/workshop-program/presentation/mcsherry
- Provost, F., & Fawcett, T. (2013). *Data science for business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.
- Raasveldt, M., & Mühleisen, H. (2019). DuckDB: An embeddable analytical database. In *Proceedings of the 2019 International Conference on Management of Data (SIGMOD '19)* (pp. 1981–1984). ACM. https://doi.org/10.1145/3299869.3320212
- Zaharia, M., Xin, R. S., Wendell, P., Das, T., Armbrust, M., Dave, A., Meng, X., Rosen, J., Venkataraman, S., Franklin, M. J., Ghodsi, A., Gonzalez, J., Shenker, S., & Stoica, I. (2016). Apache Spark: A unified engine for big data processing. *Communications of the ACM, 59*(11), 56–65. https://doi.org/10.1145/2934664
