---
course: Data Analytics
session: 8
title: ML Use-Case Lab
subtitle: Practice tasks on pipelines, time-aware tuning, segmentation, anomaly detection and communicating results — one per track, plus a portfolio-style task
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the content of session 8 on your own or in the lab. Tasks 1, 2 and 6 need only paper and pencil. Tasks 3–5 use Python with DuckDB, pandas and scikit-learn (Pedregosa et al., 2011) and `tpch.duckdb` with the star schema from session 3 (`fact_sales`, `dim_customer`, `dim_part`), built from the TPC-H data (Transaction Processing Performance Council, n.d.); task 5 also uses the base tables `orders` and `lineitem`. There is one practice task per track — **3** churn, **4** segmentation, **5** anomaly detection — each in a different setting from the lab, so you can also try the tracks you did not choose. Task 7 is a portfolio-style task for notebook 2. Use `random_state=42` (or the seed given) wherever randomness is involved, so your numbers match the solutions. The terms follow the slides: pipeline and ColumnTransformer, `step__parameter`, snapshot folds, top-*k* by capacity, planted anomalies, and the five-part result summary.

## Pipeline or Leakage?

Each snippet comes from a churn notebook with a feature table `df` (one row per customer and cut-off), the label `churned` and a column `cutoff`. For each snippet, decide whether it is **correct** or contains a **problem** (leakage, wrong evaluation or a bug). Explain in one or two sentences and give a fix.

```python
# (a)
X_scaled = StandardScaler().fit_transform(df[num])
search = GridSearchCV(LogisticRegression(), {"C": [0.1, 1]},
                      cv=snapshot_folds(df.cutoff))
search.fit(X_scaled, df.churned)

# (b)
pipe = Pipeline([("prep", prep), ("model", LogisticRegression(max_iter=1000))])
search = GridSearchCV(pipe, {"C": [0.1, 1, 10]}, cv=snapshot_folds(df.cutoff))

# (c)
region_rate = df.groupby("region").churned.mean()       # churn rate per region
df["region_churn_rate"] = df.region.map(region_rate)
search.fit(df[num + ["region_churn_rate"]], df.churned)

# (d)
prep = ColumnTransformer([("num", SimpleImputer(strategy="median"), num),
                          ("cat", OneHotEncoder(handle_unknown="ignore"), cat)])
pipe = Pipeline([("prep", prep),
                 ("model", HistGradientBoostingClassifier(random_state=42))])

# (e)
search.fit(train[num + cat], train.churned)
print(search.score(test[num + cat], test.churned))
search2 = GridSearchCV(pipe, {"model__C": [0.003, 0.01, 0.03]},
                       cv=snapshot_folds(train.cutoff))
both = pd.concat([train, test])
search2.fit(both[num + cat], both.churned)
```

::: answer lines=10
:::

::: hint
Ask for each line: which rows does this `fit` (or `mean`) see — only the training rows of the current fold, or also the validation or test rows?
:::

::: solution
- **(a) Problem — preprocessing leakage.** The scaler is fitted on all rows, including the validation snapshots of every fold, so their means and standard deviations leak into training. Fix: put the scaler into a `Pipeline` (or the `ColumnTransformer`) and pass the pipeline to `GridSearchCV`; then it is refitted on the training rows of each fold (scikit-learn developers, n.d.-c). With a scaler the numeric effect is often small — the point is the principle, and it matters a lot for steps such as feature selection.
- **(b) Problem — bug.** Inside a pipeline the parameter must be addressed as `step__parameter`, here `model__C`. `"C"` raises an error (invalid parameter). Fix: `{"model__C": [0.1, 1, 10]}`.
- **(c) Problem — target leakage in training examples.** The churn rate per region is computed from the labels of all rows, including validation and test rows and each row's own label (Kaufman et al., 2012). Fix: compute such target statistics only from earlier snapshots (point-in-time) or inside each training fold — or simply one-hot encode the region and let the model learn its effect.
- **(d) Correct.** Different steps for numeric and categorical columns inside one pipeline; tree-based gradient boosting does not need scaling. (Accept "correct, but `add_indicator=True` would keep the information that the trend was undefined".)
- **(e) Problem — the test set is used for tuning.** After looking at the test score, the second search refines the grid around it and even trains on the test rows. The test score is then no longer an honest estimate (scikit-learn developers, n.d.-b). Fix: tune only with the snapshot folds of the training period; touch the test cut-off once at the end. If you need another round, report it and, ideally, hold out a later cut-off.

Marking: 2 points per snippet (1 for the correct verdict, 1 for reason and fix), 10 points in total.
:::

## Which Validation Fits?

For each situation, choose the validation scheme and justify it in one sentence: random (stratified) K-fold, `GroupKFold`, `TimeSeriesSplit`, snapshot folds (train on earlier cut-offs, validate on the next), or "no cross-validation score — something else".

1. A bank predicts loan default from application data. Each customer has exactly one application; the data cover one month.
2. A telecom predicts churn from monthly customer snapshots for 2022–2024 (the same customer appears up to 36 times).
3. A hospital predicts readmission from patient visits; many patients have several visits, and time plays no role in the question.
4. A utility forecasts tomorrow's hourly electricity demand from the past three years.
5. Marketing wants between 3 and 8 customer segments and asks you to tune *k*.
6. An auditor wants an isolation forest for payment records; no payment is labelled as fraud.

::: answer lines=10
:::

::: solution
1. **Stratified K-fold** — rows are independent (one per customer, no time structure); stratification keeps the default rate equal across folds. (Accept a time-based split if the student argues that the model will be used on later months.)
2. **Snapshot folds** (expanding window over cut-offs) — the model predicts the future from the past, and the same customers appear at several cut-offs; random folds would train on later snapshots of the customers being validated. The label window of each training snapshot must end before the validation cut-off.
3. **GroupKFold** with the patient as group — visits of the same patient are not independent; otherwise the model is validated on patients it has already seen.
4. **`TimeSeriesSplit`** (or a rolling forecast origin, sessions 11–14) — autocorrelated series at fixed intervals; always validate on later hours than you train on (scikit-learn developers, n.d.-b).
5. **No cross-validation score** in the supervised sense — compare the silhouette across *k* on the transformed features, check stability (adjusted Rand index between runs on random halves) and judge usability with marketing (scikit-learn developers, n.d.-a).
6. **No labels** — evaluate with planted anomalies of plausible types (precision in the top *k* = audit capacity) and with an expert review of a sample of the top list; compare with a simple rule.

Marking: 1 point per situation with a fitting reason (6 points).
:::

## Track A: A Three-Month Churn Horizon

The head of sales asks: "Six months is too slow. Can we predict who will not order in the next **three** months?" Reuse `FEATURES_SQL` from the slide "Starter A (1/3)" and the pipeline `pipe`, `num`, `cat` and `snapshot_folds` from the slides "Starter A (2/3)" and "Starter A (3/3)".

```python
SQL3 = FEATURES_SQL.replace("$cutoff + INTERVAL 6 MONTH",
                            "$cutoff + INTERVAL 3 MONTH")
cutoffs = [date(1996, 1, 1), date(1996, 4, 1), date(1996, 7, 1),
           date(1996, 10, 1), date(1997, 1, 1), date(1997, 4, 1)]
train = pd.concat([con.execute(SQL3, {"cutoff": c}).df() for c in cutoffs],
                  ignore_index=True)
test = con.execute(SQL3, {"cutoff": date(1997, 7, 1)}).df()
```

1. Report the churn rate per training snapshot and in the test set. Compare with the 6-month definition (34.5 %). What does this mean for the target?
2. Write a scorer for the **top-decile lift** with `make_scorer` and tune `model__C` (0.01, 0.1, 1) and `model__class_weight` (None, "balanced") with `GridSearchCV`, the snapshot folds and **two** metrics (AUC and top-decile lift), refitting on the lift. Which setting wins, and does `class_weight` matter?
3. On the test cut-off, compare the model with the rule "fewest purchase days first" (AUC and top-decile lift).
4. Marketing would use the e-mail voucher from worksheet 7 (TP +1,000, FP −500, break-even probability 33.3 %). How many customers should get it? What is your advice to the head of sales?

::: answer lines=12
:::

::: hint
`make_scorer(f, response_method="predict_proba")` passes the predicted probabilities to `f(y_true, y_score)`. With a dictionary of metrics, `GridSearchCV(..., scoring={"auc": "roc_auc", "lift10": lift10}, refit="lift10")` reports both and refits on the lift.
:::

::: solution
Code (tested with DuckDB 1.5.5, scikit-learn 1.9.1):

```python
from sklearn.metrics import make_scorer, roc_auc_score

def top_decile_lift(y_true, y_score):
    k = len(y_true) // 10
    top = np.argsort(-y_score, kind="stable")[:k]
    return np.asarray(y_true)[top].mean() / np.mean(y_true)

lift10 = make_scorer(top_decile_lift, response_method="predict_proba")
grid = {"model__C": [0.01, 0.1, 1], "model__class_weight": [None, "balanced"]}
search = GridSearchCV(pipe, grid, cv=snapshot_folds(train.cutoff),
                      scoring={"auc": "roc_auc", "lift10": lift10},
                      refit="lift10")
search.fit(train[num + cat], train.churned)
p = search.predict_proba(test[num + cat])[:, 1]
# rule: fewest purchase days first, ties broken by longer recency
rule = -test.purchase_days.values + 1e-6 * test.recency_days.values
for s in [p, rule]:
    print(roc_auc_score(test.churned, s),
          top_decile_lift(test.churned.values, s))
```

1. Churn rate per snapshot **57.4–58.5 %** (1996-01-01: 58.0 %, 1996-04-01: 58.0 %, 1996-07-01: 57.7 %, 1996-10-01: 57.4 %, 1997-01-01: 58.5 %, 1997-04-01: 57.6 %); test **57.6 %** (10,000 customers). With 3 months, most customers "churn" — an active customer bought on about 12 days in the five and a half years before mid-1997, so three months without an order is normal behaviour, not a loss. The target no longer measures what sales means by churn.
2. Five snapshot folds. Mean validation AUC 0.597 for every setting; top-decile lift between 1.172 and 1.180. Best: `C = 0.01`, `class_weight = "balanced"` (lift 1.180) — but `None` gives 1.180 as well (1.1796 vs. 1.1799): the difference is noise. `class_weight` changes the **probabilities** (with "balanced", the mean predicted probability is 0.484 instead of close to the base rate 0.576), not the **ranking** — and lift and AUC depend only on the ranking.
3. Test: model AUC **0.598**, lift **1.18**; rule AUC **0.598**, lift **1.18**. The model again reproduces the rule.
4. Break-even 33.3 % is far **below** the base rate 57.6 %, so even a random customer has a positive expected value. Cumulative profit by the model's ranking: top 1,000: 518,500 · top 5,000: 2,402,000 · all 10,000: **3,638,500** (the maximum, 3,640,500, is at 9,978 customers — practically everybody). Advice: with a 3-month horizon, no model is needed for the voucher — send it to all active customers, or better, keep the 6-month definition, which separates real losses from normal pauses. The horizon is a business decision (session 7 framing), not a tuning parameter.

Marking (10 points): base rates and interpretation 2; scorer and multi-metric search 3; `class_weight` explained (ranking vs. probabilities) 2; test comparison 1; decision with cost argument 2.
:::

## Track B: Segments by What Customers Buy

In the lab, segments were built from **how** customers buy (recency, frequency, basket size, promo share). Marketing now wants segments by **what** they buy: the share of each customer's revenue per part family (the first word of `part_type`: ECONOMY, LARGE, MEDIUM, PROMO, SMALL, STANDARD) before 1 July 1997.

```python
mix = con.sql("""
  PIVOT (SELECT f.customer_key, f.revenue,
                split_part(p.part_type, ' ', 1) AS family
         FROM fact_sales f JOIN dim_part p USING (part_key)
         WHERE f.date_key < DATE '1997-07-01')
  ON family USING sum(revenue)
  GROUP BY customer_key ORDER BY customer_key""").df().fillna(0)
fam = [c for c in mix.columns if c != "customer_key"]
shares = mix[fam].div(mix[fam].sum(axis=1), axis=0)
```

1. Build a pipeline `StandardScaler` → `KMeans(n_init=10, random_state=42)` and compute the silhouette for *k* = 2 … 6.
2. **Null baseline:** shuffle each column independently (`rng = np.random.default_rng(42)`; `shares.apply(lambda col: rng.permutation(col.values))`) and compute the silhouettes again. What does the comparison tell you?
3. Profile the clusters for *k* = 3 (mean shares and size).
4. Check stability: ARI between the fit with `random_state=42` and fits with `random_state` 1–5, and between the full fit and fits on five random halves (use the same `rng`).
5. What do you tell marketing?

::: answer lines=12
:::

::: hint
The shuffled data keep every column's distribution but destroy any relationship between the columns. If real clusters existed, the real data should score clearly better than the shuffled data.
:::

::: solution
Code (tested with DuckDB 1.5.5, scikit-learn 1.9.1):

```python
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score

def sil(X, k, seed=42):
    km = KMeans(n_clusters=k, n_init=10, random_state=seed)
    pipe = Pipeline([("scale", StandardScaler()), ("kmeans", km)])
    lab = pipe.fit_predict(X)
    return silhouette_score(pipe[:-1].transform(X), lab), lab

rng = np.random.default_rng(42)
shuffled = shares.apply(lambda col: rng.permutation(col.values))
for k in range(2, 7):
    print(k, round(sil(shares, k)[0], 3), round(sil(shuffled, k)[0], 3))
_, lab = sil(shares, 3)
print(shares.assign(cluster=lab).groupby("cluster").mean().round(3))
print([adjusted_rand_score(lab, sil(shares, 3, seed=s)[1])
       for s in range(1, 6)])
for i in range(5):
    idx = rng.choice(len(shares), len(shares) // 2, replace=False)
    km = KMeans(n_clusters=3, n_init=10, random_state=42)
    half = Pipeline([("scale", StandardScaler()), ("kmeans", km)])
    half.fit(shares.iloc[idx])
    print(adjusted_rand_score(lab, half.predict(shares)))
```

1. and 2. 10,000 customers; each family has a mean share of about 16–17 %.

| *k* | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Silhouette, real data | 0.124 | 0.124 | 0.131 | 0.141 | 0.148 |
| Silhouette, shuffled columns | 0.112 | 0.104 | 0.109 | 0.112 | 0.119 |

The real data score only slightly above data **without any structure** (all silhouettes far below the 0.19–0.22 of the lab features). k-means always returns *k* groups — the null baseline shows that there is hardly any structure to find. The rising silhouette with *k* is no argument for large *k*.

3. *k* = 3: cluster 0 (3,093 customers) STANDARD share 23.9 % (others 13.9–16.4 %); cluster 1 (3,123) PROMO share 24.2 %; cluster 2 (3,784) "the rest": ECONOMY and MEDIUM about 19.5 %, PROMO and STANDARD about 12.5 %. Shares add up to 1, so a high share of one family forces lower shares elsewhere — the clusters are "one family a bit above average".

4. ARI against other seeds: 0.238, 0.265, 0.963, 0.238, 0.680; against random halves: 0.241, 0.386, 0.333, 0.770, 0.006. **Unstable:** with another start or half of the data, many customers change their segment (compare the lab segments: ARI at least 0.93).

5. Advice: there are no robust "what they buy" segments in this data (TPC-H assigns parts to orders at random). Do not build offers on them. If marketing wants product-based offers, use a simple rule instead (e.g. "customers with a PROMO share above 25 %"), which is transparent and reproducible, and test the offer (session 9). A stable but meaningless segmentation would be just as bad: always check structure (null baseline), stability and usefulness (Provost & Fawcett, 2013; scikit-learn developers, n.d.-a).

Marking (10 points): silhouettes 2; null baseline and its interpretation 3; profile 1; stability numbers and interpretation 2; recommendation 2.
:::

## Track C: Unusual Orders

The audit team now checks whole **orders** instead of order lines and can review **120 orders** of 1997. Build the order features from the base tables and plant three kinds of known anomalies in a copy:

```python
orders = con.sql("""
  SELECT o_orderkey,
         count(*)                      AS n_lines,
         sum(l_quantity)::DOUBLE       AS total_qty,
         max(l_shipdate) - o_orderdate AS ship_days,
         o_totalprice / sum(l_extendedprice * (1 - l_discount) * (1 + l_tax))
                                       AS total_ratio
  FROM orders JOIN lineitem ON l_orderkey = o_orderkey
  WHERE year(o_orderdate) = 1997
  GROUP BY o_orderkey, o_orderdate, o_totalprice
  ORDER BY o_orderkey""").df()

rng = np.random.default_rng(42)          # plant 120 known anomalies in a copy
aud = orders.copy(); aud["kind"] = "normal"
idx = rng.choice(len(aud), 120, replace=False)
a, b, c = idx[:40], idx[40:80], idx[80:]
aud.loc[a, "total_ratio"] = rng.uniform(1.1, 1.3, 40)    # header total wrong
aud.loc[b, "n_lines"] = 7                                # many lines ...
aud.loc[b, "total_qty"] = rng.integers(7, 21, 40).astype(float)  # tiny qty
aud.loc[c, "ship_days"] = rng.integers(150, 251, 40)     # very late shipping
aud.loc[a, "kind"] = "header"
aud.loc[b, "kind"] = "joint"
aud.loc[c, "kind"] = "late"
```

1. Describe the normal orders: ranges of the four features. Which value does `total_ratio` have for normal orders, and why?
2. With all four features, compare the z rule (largest absolute z-score) and an isolation forest with default settings (`n_estimators=200, random_state=42`) on the top 120. How many orders does `contamination="auto"` flag?
3. Two anomaly types can be described exactly. Write a **rule** for each and count its hits and false alarms.
4. On the orders that the rules do not flag, compare the z rule with isolation forests on `n_lines`, `total_qty`, `ship_days` (`max_samples` 256, 1024, 4096), top 40 each. Why does the z rule find none of the joint anomalies?
5. Propose an audit procedure for the 120 orders.

::: answer lines=14
:::

::: hint
TPC-H stores the order total in the order header. Compare the largest normal `ship_days` with the planted values — and look at the z-scores of a joint anomaly feature by feature.
:::

::: solution
Results (tested with DuckDB 1.5.5, scikit-learn 1.9.1; precision = share of planted anomalies in the top *k*):

```python
from sklearn.ensemble import IsolationForest
feats4 = ["n_lines", "total_qty", "ship_days", "total_ratio"]
feats3 = ["n_lines", "total_qty", "ship_days"]

def top(df, score, k):
    t = df.loc[score.nlargest(k).index]
    return (t.kind != "normal").mean(), t.kind.value_counts().to_dict()

z4 = ((aud[feats4] - aud[feats4].mean()) / aud[feats4].std()).abs().max(axis=1)
iso4 = IsolationForest(n_estimators=200, random_state=42).fit(aud[feats4])
s4 = pd.Series(-iso4.score_samples(aud[feats4]), index=aud.index)
print(top(aud, z4, 120), top(aud, s4, 120))
print((iso4.predict(aud[feats4]) == -1).sum())         # flagged with "auto"

hdr = (aud.total_ratio - 1).abs() > 0.001   # header total must match the lines
late = aud.ship_days > 121                   # beyond the normal maximum
rest = aud[~hdr & ~late]
z3 = ((rest[feats3] - rest[feats3].mean()) / rest[feats3].std())
z3 = z3.abs().max(axis=1)
print(top(rest, z3, 40))
for ms in [256, 1024, 4096]:
    iso = IsolationForest(n_estimators=200, max_samples=ms, random_state=42)
    iso.fit(rest[feats3])
    s = pd.Series(-iso.score_samples(rest[feats3]), index=rest.index)
    print(ms, top(rest, s, 40))
```

1. 22,682 orders in 1997. `n_lines` 1–7, `total_qty` 1–303, `ship_days` 1–121, `total_ratio` 0.99998–1.0: the order total in the header **equals** the sum of the line amounts (with discount and tax) up to rounding — TPC-H computes it that way. This is a business rule, not a statistical pattern.
2. z rule: **53.3 %** (40 header, 24 late, 0 joint). Isolation forest with defaults: **2.5 %** (2 joint, 1 late) — practically useless here. `contamination="auto"` flags **4,252** orders. Possible reasons to discuss: the near-constant `total_ratio` with rounding noise and the small default subsamples (256 orders per tree contain on average about one planted anomaly). Lesson: defaults are not a method; check the detector with known cases.
3. Rule "|total_ratio − 1| > 0.001": **40 hits, 0 false alarms**. Rule "ship_days > 121" (the largest value seen in normal orders): **40 hits, 0 false alarms**. If you can describe an anomaly exactly, a rule is cheaper, explainable and better.
4. Remaining orders: 22,602 (40 joint anomalies). Top 40 — z rule **0 %** (0 joint); isolation forest `max_samples=256`: **25 %** (10 joint); 1,024: **55 %** (22 joint); 4,096: **42.5 %** (17 joint). A joint anomaly has 7 lines (z = 1.5) and a total quantity of 7–20 (z ≈ −1.4 to −1.6): each value alone is normal, only the **combination** is unusual — no normal 7-line order has a total quantity below 56. The z rule looks at one feature at a time; the forest isolates the combination (Liu et al., 2008). Tuning `max_samples` on planted anomalies optimises for the anomalies you imagined — report it as a limitation.
5. Procedure: (1) data-validation rules first (header total, ship days beyond the known maximum) — 80 orders with certainty; (2) fill the remaining 40 review slots with the top of an isolation forest on the remaining orders, each listed with its feature values as the reason; (3) let auditors label what they find and use these labels to evaluate and improve the detector over time (with labels, the problem becomes supervised). Expected hits with this procedure: 80 + 22 = 102 of 120 (85 %), compared with 64 (53.3 %) for the z rule alone.

Marking (10 points): 1 (1 point); 2 (2); 3 rules with counts (2); 4 numbers and the explanation of joint anomalies (3); 5 procedure (2).
:::

## Rewrite the Summary

A pair hands in this result summary for the anomaly track of the lab (numbers from the session slides). List at least **five** problems and rewrite the summary in the five-part structure from the session (answer first, evidence against the baseline, meaning for the decision, limits, next step), in at most 120 words.

> "We used a state-of-the-art isolation forest (Liu et al., 2008) on all 90,435 order lines of 1997. It detected 37,444 anomalies, which shows that data quality is a big problem. After hyperparameter tuning (max_samples = 4096), the model is 93.3 % accurate. The z-score rule reached 97.8 %, but z-scores are only a statistical trick and not machine learning. We recommend deploying the isolation forest."

::: answer lines=12
:::

::: solution
Problems (one point each, up to 5):

- **37,444 "anomalies"** are just the lines flagged by the default `contamination="auto"` threshold, not a finding about data quality; the number to report is the result in the top *k* = audit capacity (180).
- **"93.3 % accurate"** is the share of planted anomalies among the top 180 (precision at the audit capacity), not accuracy. Accuracy on 90,435 lines with 180 anomalies would be high for any detector.
- The evaluation uses **planted** anomalies of three self-made types; the forest was **tuned on them** (max_samples) — the result is optimistic and only valid for these types.
- The **baseline is better** (97.8 % vs. 93.3 %) and is dismissed for not being "machine learning" — the decision must follow the evidence, not the method label.
- **No meaning for the decision:** how many lines go to the auditors, what is found, what does it cost?
- **Answer is buried** at the end; no limits, no next step; "state-of-the-art" adds nothing.

Example rewrite (about 100 words):

"Use a z-score rule on quantity and price ratio to choose the 180 order lines the audit team reviews each year. On 1997 data with 180 planted errors, the rule put 176 of them in its top 180 (97.8 %); the best isolation forest reached 93.3 % and only after tuning on the same planted errors (48.3 % with default settings). Auditors would review the same workload with fewer false alarms. Limits: only three self-made error types were tested; real errors may combine several features, where a forest can help. Next step: auditors label the reviewed lines, and we re-evaluate both methods on real findings."

Marking: 5 points for problems, 5 points for the rewrite (1 per part of the structure, with numbers stated correctly).
:::

## Portfolio-Style Task: Notebook 2 End to End

Complete portfolio notebook 2 for **one** track — on the TPC-H warehouse or on a public dataset of comparable depth. Build on worksheet 7, task 7 (framing, feature table, baseline, leakage audit, cost assumptions) and add:

- a scikit-learn **pipeline** that contains all preprocessing steps,
- **tuning** with `GridSearchCV` or `RandomizedSearchCV` and a validation design that fits your data (snapshot folds for churn; stability checks for segments; planted anomalies or expert review for anomaly detection),
- an **evaluation** on a later period or held-out data, against the baseline, with a business metric (lift and profit, usable and stable segments, hits in the top *k*),
- an **interpretation** (permutation importance, profiles or a review list) in business terms,
- a **result summary** in the five-part structure and a **suitability assessment** (is ML worth it here?),
- reproducibility: runs top to bottom on a fresh `tpch.duckdb`, prints library versions, fixes every `random_state`.

::: answer lines=8
:::

::: solution
Marking guide (30 points; follows the suggested rubric on the slides — training only, the official brief and rubric of the portfolio are published separately):

- **Business framing and success criteria** (4 points): decision and owner; business and data mining success criteria separated; six framing questions answered consistently (worksheet 7, task 7). "Predict churn with high accuracy" scores at most 1.
- **Data preparation and point-in-time correctness** (6 points): features only from data before each cut-off or snapshot date; label only from the label window; complete label windows (not the incomplete 1998); NULL vs. 0 decided deliberately (e.g. `revenue_trend` NULL plus missing indicator); sanity checks reported (rows, base rate, ranges); leakage audit table.
- **Baseline, pipeline and validation design** (8 points): a baseline that fits the track (rule, existing segments, z-score or domain rule) with its result (2); one pipeline with all preprocessing — no fitting on all data before the split (2); tuning with sensible parameter ranges and `step__parameter` names (2); a validation design that fits the data — snapshot folds or another time-aware split for churn; silhouette with a null baseline and stability for segments; planted anomalies and/or expert review for anomaly detection — and the test period used only once (2).
- **Evaluation and interpretation** (6 points): business metric on the test period or held-out data compared with the baseline (e.g. top-decile lift and profit at the capacity; segment profiles with sizes and revenue shares; hits in the top *k* by type); interpretation in business terms with its limits (importances describe the model; segments named and checked with later behaviour; review list with reasons).
- **Suitability assessment and communication** (4 points): five-part summary with the answer first and correct numbers; honest verdict, e.g. "on TPC-H the rule is enough" (session 8: test AUC rule 0.627 vs. tuned logistic regression 0.627 and gradient boosting 0.625) or "no robust product segments" (task 4); limits (synthetic data, one test period, planted anomalies) and a next step.
- **Reproducibility and code quality** (2 points): runs top to bottom; versions printed; fixed `random_state`; short code cells with Markdown explanations.

Typical strong submission (churn): five snapshots as in the lab, logistic regression and gradient boosting tuned with snapshot folds, comparison with the purchase-days rule by top-20 % profit (257,000 rule, 248,000 LR, 266,000 HGB — within noise), permutation importance showing that purchase days carry almost all the signal (AUC drop about 0.12), and the recommendation to use the rule. A negative result shown convincingly scores as well as a positive one.
:::

## References {.references}

- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data, 6*(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation forest. In *2008 Eighth IEEE International Conference on Data Mining* (pp. 413–422). IEEE. https://doi.org/10.1109/ICDM.2008.17
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*(85), 2825–2830. https://jmlr.org/papers/v12/pedregosa11a.html
- Provost, F., & Fawcett, T. (2013). *Data science for business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.
- scikit-learn developers. (n.d.-a). *Clustering* (scikit-learn 1.9.1 documentation, Section 2.3). Retrieved October 20, 2026, from https://scikit-learn.org/stable/modules/clustering.html
- scikit-learn developers. (n.d.-b). *Cross-validation: Evaluating estimator performance* (scikit-learn 1.9.1 documentation, Section 3.1). Retrieved October 20, 2026, from https://scikit-learn.org/stable/modules/cross_validation.html
- scikit-learn developers. (n.d.-c). *Pipelines and composite estimators* (scikit-learn 1.9.1 documentation, Section 8.1). Retrieved October 20, 2026, from https://scikit-learn.org/stable/modules/compose.html
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
