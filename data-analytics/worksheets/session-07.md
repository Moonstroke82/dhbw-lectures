---
course: Data Analytics
session: 7
title: From Business Question to ML Use Case
subtitle: Practice tasks on CRISP-DM, framing, data leakage, cost matrices, baselines, lift and point-in-time features
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 7 on your own or in the lab. Tasks 1–4 need only paper and pencil (and a calculator). Tasks 5 and 6 use Python with DuckDB and `tpch.duckdb`: task 5 the TPC-H base tables `lineitem` and `orders`, task 6 the star schema from session 3 (`fact_sales`, `dim_customer`, `dim_date`), built from the TPC-H data (Transaction Processing Performance Council, n.d.). The optional part of task 6 also needs scikit-learn, which you will use in session 8. Task 7 is a portfolio-style task that prepares portfolio notebook 2. The terms follow the session slides: the six framing questions, cut-off and label window, baselines, leakage (Kaufman et al., 2012), cost matrix, expected value and lift (Provost & Fawcett, 2013).

## CRISP-DM in a Bike-Sharing Project

A city bike-sharing operator wants to know which stations will run **empty within the next two hours**, so that a van can bring bikes in time. Assign each activity to one of the six CRISP-DM phases (Chapman et al., 2000) and give a one-line reason.

1. Interview the dispatchers: how far ahead must they know, and how many van trips per hour are possible?
2. Plot rentals per station and hour; find that 3 % of the stations have gaps in the sensor data.
3. Estimate the cost of a van trip and the lost rentals of an empty station.
4. Join weather data and compute for each station and hour the label "fewer than 2 bikes two hours later".
5. Train a logistic regression and a gradient boosting model and tune them with cross-validation.
6. Compare the models with the rule "empty now at the same hour last week"; dispatchers complain that the many false alarms waste van trips.
7. Build an hourly job that writes the risk list into the dispatch app, and check every month whether the hit rate is stable.
8. Agree with the dispatchers that "empty" means "fewer than 2 bikes" and that the model must beat last week's rule.

After activity 6, to which phase would you go back, and why?

::: answer lines=10
:::

::: solution
1. **Business understanding** — determine business objectives and assess the situation (requirements, resources such as van capacity).
2. **Data understanding** — explore the data and verify data quality.
3. **Business understanding** — assess situation: costs and benefits. (Accept "evaluation" only if the student argues that the values are needed to judge the model; the CRISP-DM guide places costs and benefits in "assess situation".)
4. **Data preparation** — integrate data (join weather) and construct the label and features.
5. **Modelling** — select techniques, build and assess models (tuning is part of modelling).
6. **Evaluation** — evaluate results against the business objectives, here against a baseline and the dispatchers' view.
7. **Deployment** — plan deployment, monitoring and maintenance.
8. **Business understanding** — determine data mining goals and data mining success criteria. (Accept data preparation for the label definition alone, if the reason is given.)

Going back: the evaluation shows that the model does not meet the **business** objective because false alarms are costly. Go back to **business understanding** to quantify the cost of a false alarm and of a missed empty station, then choose a decision threshold that maximises the expected value (as with the cost matrix in session 7). Going back to modelling only (e.g. "tune for precision") is a partial answer: without the costs, nobody knows which precision is good enough.

Marking: one point per activity with a sensible reason, two points for the step back with a business reason.
:::

## Frame It — or Not

For each request, decide first whether it is an **ML task** (which type?), a **query or report**, or a **causal question**. For each ML task, answer the six framing questions from the session: decision, unit, target, prediction point and horizon, features available at that point, success measure.

1. An energy supplier: "Which household customers will switch to another provider when their contract ends?"
2. A hospital: "How many beds will the cardiology ward need each day next week?"
3. An online shop: "Did the new recommendation box increase revenue per visit?"
4. An insurer: "Show the number of claims per region in the last quarter."
5. A pump manufacturer: "Find unusual vibration patterns in the pumps installed at our customers."

::: answer lines=14
:::

::: hint
Start with the decision: who does what differently because of the result? If nothing changes, or if the answer is already in the data, it is not a prediction task.
:::

::: solution
1. **Classification (churn).** Decision: retention offer by the sales team before the notice period. Unit: one contract (or customer) whose contract ends in the horizon. Target: notice of cancellation received in the window before contract end. Prediction point: e.g. 4 months before contract end (before the notice period); horizon: until the notice deadline. Features before that point: tariff, recent price changes, consumption, payment problems, complaints, contact history, contract age. Success: lift in the top of the ranking and profit of the retention campaign vs. a simple rule (e.g. "price increase received").
2. **Forecasting (regression over time).** Decision: staff and bed planning for next week. Unit: ward-day. Target: occupied beds per day (or admissions and length of stay). Prediction point: e.g. Friday for the following Monday–Sunday; horizon 3–9 days. Features: past occupancy, weekday, holidays, planned (elective) admissions, season, flu wave indicators — all known on Friday. Success: forecast error (MAE) vs. a seasonal naive forecast "same day last week" (sessions 11–14) and the cost of too few vs. too many staffed beds.
3. **Causal question** — not a prediction task. A model that predicts revenue from "saw the box" would confuse correlation with causation (e.g. active users see the box more often). Answer with an A/B test or, if impossible, a careful causal analysis (session 9).
4. **Query or report** — descriptive analytics on the warehouse (a GROUP BY or a dashboard tile), no ML.
5. **Anomaly detection** (unsupervised; supervised classification only if failures are labelled). Decision: send a technician or call the customer. Unit: pump and time window (e.g. pump-hour). "Target": no label; score of unusualness. Prediction point: continuously, after each window. Features: vibration statistics in the window, operating mode, temperature, pump type, age, recent maintenance. Success: share of alerts that engineers confirm (precision of the top alerts), failures detected in advance, and the number of alerts the service team can handle.

Marking: one point for the correct type per request; for 1, 2 and 5 up to two further points for a consistent framing (the prediction point and features must fit together). Accept other reasonable horizons and units.
:::

## Spot the Leakage

An online fashion retailer wants to predict **at checkout** whether an order will be returned. If the risk is high, the shop shows size advice before the order is placed. A data scientist proposes these features. Classify each one as **legitimate**, **leakage** or **depends** (explain on what), and name the type of leakage from the session.

| # | Feature |
|---|---|
| a | Customer's return rate over their orders in the previous 12 months |
| b | Number of different sizes of the same article in the basket |
| c | Refund amount |
| d | Delivery time in days |
| e | Payment method chosen at checkout |
| f | "Return label printed" flag |
| g | Return rate of the article's category, computed once over the whole data set (2023–2025) and used for training and testing |
| h | Customer contacted customer service after delivery |

::: answer lines=10
:::

::: hint
For every feature, ask: at the moment of checkout, does this value already exist — and does it have exactly the value that the model sees in training?
:::

::: solution
- a **Legitimate** if computed only from orders **before** the current order (point-in-time). Leakage if the "12 months" include later orders or the current order's own return.
- b **Legitimate** — known in the basket; a strong signal (customers order two sizes and return one).
- c **Leakage** (feature from the future, even caused by the target): a refund exists only after a return.
- d **Depends on the prediction point.** At checkout the delivery time is unknown → leakage. It would be legitimate for a model that predicts returns after delivery (a different decision, e.g. warehouse planning). The *promised* delivery time shown at checkout is legitimate.
- e **Legitimate** — chosen at checkout. (Discuss fairness: payment method can be a proxy for income.)
- f **Leakage** — a step of the return process itself, caused by the target.
- g **Leakage in training examples**: the category return rate includes the returns of the test period (and of each training row itself). Compute it only from orders before each order, or at least only from the training period (Kaufman et al., 2012, call the avoidance principle learn–predict separation).
- h **Leakage** — happens after delivery; contacts are often about the return itself.

Marking: one point per feature with a correct reason; for d and g, the reason (prediction point; computed over the test period) is required for the point.
:::

## Cost Matrix: Checking Insurance Claims

An insurer receives 10,000 claims per quarter; 500 of them are fraudulent. Investigating a claim costs **300**. An investigation of a fraudulent claim saves on average **4,000** (the payment that is not made). Without a model, no claim is investigated. Two models are offered:

| | Claims flagged | Fraudulent among flagged |
|---|---|---|
| Model A | 800 | 300 |
| Model B | 2,000 | 450 |

1. Set up the cost matrix (value of TP, FP, FN, TN relative to investigating nothing).
2. For "investigate nothing", "investigate all", model A and model B: compute accuracy, precision, recall, lift of the flagged group, and the expected profit per quarter.
3. Which model would you choose? What changes if the investigation team can handle at most **1,000** claims per quarter?
4. Customer service reports that every investigated honest customer costs another 400 in complaints and lost goodwill. Recompute the profit of A and B. Which probability of fraud must a claim have before an investigation pays off — before and after this change?

::: answer lines=14
:::

::: hint
Lift = precision of the flagged group ÷ overall fraud rate. For the break-even probability, set the expected value of investigating a claim with fraud probability *p* to zero.
:::

::: solution
1. TP (fraud, investigated): 4,000 − 300 = **+3,700** · FP (honest, investigated): **−300** · FN (fraud, not investigated): **0** · TN: **0**. FN is 0 because "not investigating" is the reference; the 4,000 lost is an opportunity cost that also occurs without a model.

2. (Fraud rate 5 %.)

| Policy | TP | FP | Accuracy | Precision | Recall | Lift | Profit |
|---|---|---|---|---|---|---|---|
| Investigate nothing | 0 | 0 | 95.0 % | — | 0 % | — | 0 |
| Investigate all | 500 | 9,500 | 5.0 % | 5.0 % | 100 % | 1.0 | −1,000,000 |
| Model A | 300 | 500 | 93.0 % | 37.5 % | 60 % | 7.5 | 960,000 |
| Model B | 450 | 1,550 | 84.0 % | 22.5 % | 90 % | 4.5 | 1,200,000 |

Profit A = 300 × 3,700 − 500 × 300 = 960,000; B = 450 × 3,700 − 1,550 × 300 = 1,200,000. "Investigate nothing" has the **highest accuracy** and zero value — accuracy is the wrong yardstick here (Provost & Fawcett, 2013).

3. Without a capacity limit, **B** (higher profit, because a found fraud is worth 12 times the cost of an investigation). With a limit of 1,000 investigations, B's 2,000 flags cannot all be checked; A (800 flags) fits. If B delivers a score, the insurer could investigate only B's top 1,000 — whether that beats A cannot be computed from the table; it needs B's lift at the top 10 %. Good answers say this explicitly.

4. FP now costs 300 + 400 = 700. Profit A = 300 × 3,700 − 500 × 700 = **760,000**; B = 450 × 3,700 − 1,550 × 700 = **580,000** → now **A** is better. Break-even: *p* × 3,700 = (1 − *p*) × cost(FP), so *p* = cost(FP) / (cost(FP) + 3,700): before **300 / 4,000 = 7.5 %**, after **700 / 4,400 ≈ 15.9 %**. The decision threshold follows from the cost matrix, not from the model (Elkan, 2001).

Marking: cost matrix 2 points; table 4 points (accept rounding); choice with capacity argument 2 points; recomputation and break-even 2 points.
:::

## Late Deliveries in TPC-H

The wholesaler wants to warn customers **when the order is placed** if an order line will probably arrive after the committed date. In TPC-H, a line is late if `l_receiptdate > l_commitdate`. Use the base tables `lineitem` and `orders` (the star schema has no delivery dates).

1. What share of the order lines is late? What is the accuracy of the baseline "always late"?
2. Compute the late share by **commit lead time** (`l_commitdate - o_orderdate`) in 15-day groups, and by ship mode and order priority. Which of these features carry signal?
3. Evaluate the rule "late if the commit lead time is below 60 days": accuracy, precision, recall. Compare with the baseline. Is the rule useless?
4. A colleague adds the feature "days from order to shipping" (`l_shipdate - o_orderdate`) and is excited about the result. Compute the late share by this feature in 30-day groups and explain the problem.
5. Should the unit be the **order line** or the **order**? Compute the share of orders with at least one late line and discuss.

::: answer lines=14
:::

::: hint
A boolean can be cast to an integer, `(l_receiptdate > l_commitdate)::INT`, so `avg()` of it is a share. Integer division `// 15 * 15` puts values into groups of 15.
:::

::: solution
Results (DuckDB 1.5.5, sf 0.1):

```sql
SELECT count(*) AS lines,
       avg((l_receiptdate > l_commitdate)::INT) AS late_share
FROM lineitem;

SELECT (l_commitdate - o_orderdate) // 15 * 15 AS lead_days_from,
       count(*) AS lines,
       round(avg((l_receiptdate > l_commitdate)::INT), 3) AS late_share
FROM lineitem JOIN orders ON l_orderkey = o_orderkey
GROUP BY ALL ORDER BY ALL;
```

1. 600,572 lines, **63.2 %** late (379,809 lines). Baseline "always late": accuracy **63.2 %**. (Synthetic data: TPC-H draws the dates at random, so the late share is unrealistically high — session 5 worksheet: on-time rate 36.8 %.)
2. Commit lead time 30–44 days: 82.4 % late · 45–59: 69.8 % · 60–74: 57.5 % · 75–89: 44.9 % · 90: 38.8 % → **strong signal** (a later committed date is easier to meet). Ship mode (63.1–63.6 %) and priority (63.1–63.4 %) → **no signal** in TPC-H. In real data, ship mode and priority would be expected to matter — an example of why synthetic data limits what a model can show.
3. Rule (lead < 60 days → late):

```sql
WITH t AS (
  SELECT (l_receiptdate > l_commitdate)::INT AS late,
         (l_commitdate - o_orderdate < 60)::INT AS rule_late
  FROM lineitem JOIN orders ON l_orderkey = o_orderkey)
SELECT avg(late) AS acc_always_late,
       avg((late = rule_late)::INT) AS acc_rule,
       sum(late * rule_late) / sum(rule_late) AS precision_rule,
       sum(late * rule_late) / sum(late) AS recall_rule,
       sum((1 - late) * (1 - rule_late)) / sum(1 - late) AS on_time_found
FROM t;
```

Accuracy **62.4 %** (below the baseline!), precision **76.1 %**, recall **59.2 %**; it also identifies 67.9 % of the on-time lines. The rule is **not useless**: "always late" warns every customer, which makes the warning meaningless; the rule separates high-risk lines (76 % late) from lower-risk lines (51 % late). Whether it is worth it depends on the cost of a warning vs. a missed late delivery — accuracy cannot decide this.
4. Ship days 0–29: 8.5 % late · 30–59: 49.1 % · 60–89: 91.1 % · 90 and more: 100 %. **Leakage**: the shipping date is not known when the order is placed (it lies in the future of the prediction point). A model with this feature looks excellent but cannot be used for the decision. It would be legitimate only for a different prediction point (e.g. a warning at shipping time — a different, later decision).
5. **150,000** orders, **91.7 %** have at least one late line. At order level, "late" is almost always true, so the target is useless for warnings; the customer also experiences delays per delivery, i.e. per line or per shipment. The order line is the better unit here; an order-level view could use "share of late lines" instead. The unit determines the target and the base rate — choose it from the decision.

Marking: 1 (1 point), 2 (2 points), 3 (3 points: numbers and the argument that accuracy is misleading), 4 (2 points: leakage with reason), 5 (2 points).
:::

## A Second Cut-off and a Cheaper Campaign

In the session, the cut-off was 1 July 1997 and the campaign was a sales call (TP +2,500, FP −2,000). Now marketing proposes an **e-mail voucher** for the first half of 1997: it costs 500 per customer, 10 % of the contacted churners stay, and a kept customer is worth 15,000.

1. Write a Python function `features(cutoff)` that builds the churn feature table of the session for any cut-off date (6-month label window), with **one** SQL string and a parameter instead of hard-coded dates. Build the table for the cut-off **1 January 1997**. How many customers and churners are there?
2. Set up the cost matrix of the voucher campaign and compute the break-even churn probability.
3. Compute the lift table with cumulative profit for two scores: fewest purchase days first, and longest recency first. Which score is better, and how many customers should receive the voucher?
4. Compare with the call campaign of the session: why does sending the voucher to **everybody** make a profit here, while calling everybody loses money?

::: answer lines=14
:::

::: hint
DuckDB supports named parameters: write `$cutoff` in the SQL and pass `{"cutoff": date(1997, 1, 1)}` to `con.execute()`. Date arithmetic: `$cutoff + INTERVAL 6 MONTH`.
:::

::: solution
1. Example (tested with DuckDB 1.5.5, sf 0.1):

```python
from datetime import date
import duckdb

con = duckdb.connect("tpch.duckdb", read_only=True)

FEATURES_SQL = """
WITH hist AS (
  SELECT customer_key,
         $cutoff - max(date_key)  AS recency_days,
         count(DISTINCT date_key) AS purchase_days,
         coalesce(sum(revenue) FILTER (
             date_key >= $cutoff - INTERVAL 12 MONTH), 0) AS revenue_12m,
         $cutoff - min(date_key)  AS tenure_days
  FROM fact_sales WHERE date_key < $cutoff
  GROUP BY customer_key),
future AS (
  SELECT DISTINCT customer_key FROM fact_sales
  WHERE date_key >= $cutoff AND date_key < $cutoff + INTERVAL 6 MONTH)
SELECT h.*, c.segment, c.region,
       (future.customer_key IS NULL)::INT AS churned
FROM hist h JOIN dim_customer c USING (customer_key)
LEFT JOIN future USING (customer_key)
ORDER BY customer_key
"""

def features(cutoff):
    return con.execute(FEATURES_SQL, {"cutoff": cutoff}).df()

train = features(date(1997, 1, 1))
print(len(train), train.churned.sum(), round(train.churned.mean(), 4))
```

**10,000** customers, **3,469** churners (**34.7 %**). One SQL string for all cut-offs guarantees that training and test features are built with the **same definitions** — and makes point-in-time correctness testable in one place.

2. TP: 0.10 × 15,000 − 500 = **+1,000** · FP: **−500** · FN, TN: 0. Break-even: *p* × 1,000 = (1 − *p*) × 500 → *p* = 500 / 1,500 = **33.3 %**.

3. Lift query as on the slide "Lift Table in SQL", on the new table (here registered as `cf`, e.g. `con.register("cf", train)`), with `sum(1000 * c - 500 * (n - c))` and the overall churn rate of 34.69 %:

| Top % | Purchase days: decile churn rate | cum. lift | cum. profit | Recency: decile churn rate | cum. lift | cum. profit |
|---|---|---|---|---|---|---|
| 10 % | 48.2 % | 1.39 | 223,000 | 45.2 % | 1.30 | 178,000 |
| 20 % | 45.7 % | 1.35 | 408,500 | 38.5 % | 1.21 | 255,500 |
| 30 % | 46.4 % | 1.35 | 604,500 | 37.3 % | 1.16 | 315,000 |
| 40 % | 41.3 % | 1.31 | 724,000 | 36.6 % | 1.14 | 364,000 |
| 50 % | 39.1 % | 1.27 | **810,500** | 33.6 % | 1.10 | 368,000 |
| 60 % | 31.0 % | 1.21 | 775,500 | 32.0 % | 1.07 | 348,000 |
| 100 % | 21.1 % | 1.00 | 203,500 | 30.0 % | 1.00 | 203,500 |

Ranking by purchase days (ties broken by recency, then customer key) is clearly better. Best policy: voucher to the **top 50 %** (5,000 customers), profit **810,500** — after decile 5, the decile churn rate (31.0 %) falls below the break-even 33.3 %.

4. With the voucher, break-even (33.3 %) is **below** the base rate (34.7 %), so even a random customer has a positive expected value: 0.347 × 1,000 − 0.653 × 500 > 0 (total 203,500). With the call (break-even 44.4 %), the base rate is far below break-even, so calling everybody loses 4,493,000. The cheaper the action, the more customers it pays to target, and the less a model is worth over "everybody" (Provost & Fawcett, 2013). Note that 10,000 customers in each table are the same people at different times; a fair comparison of models uses a time-based split (optional part).

Marking: function with a parameter and no copied SQL per cut-off (3 points), cost matrix and break-even (2), lift tables and policy (3), explanation (2).
:::

### Optional: A First Model with a Time-Based Split {.optional}

Train a logistic regression on the cut-off 1 January 1997 and test it on the cut-off 1 July 1997 (features: recency, purchase days, revenue 12 months, tenure, segment, region). Compare its AUC and accuracy with the majority baseline and with the score "fewest purchase days" alone. Then add the leaky feature "purchase days in 1997" to the test set as a score of its own and compute its AUC.

::: answer lines=6
:::

::: solution
```python
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

test = features(date(1997, 7, 1))
cols = ["recency_days", "purchase_days", "revenue_12m", "tenure_days",
        "segment", "region"]
X_train = pd.get_dummies(train[cols], columns=["segment", "region"], dtype=float)
X_test = pd.get_dummies(test[cols], columns=["segment", "region"], dtype=float)

dummy = DummyClassifier(strategy="most_frequent").fit(X_train, train.churned)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_train, train.churned)
p = model.predict_proba(X_test)[:, 1]
print(accuracy_score(test.churned, dummy.predict(X_test)),
      accuracy_score(test.churned, model.predict(X_test)),
      roc_auc_score(test.churned, p),
      roc_auc_score(test.churned, -test.purchase_days))

leak = con.execute("""SELECT customer_key, count(DISTINCT date_key)
                      FILTER (year(date_key) = 1997) AS pd_1997
                      FROM fact_sales GROUP BY customer_key""").df()
t2 = test.merge(leak, on="customer_key")
print(roc_auc_score(t2.churned, -t2.pd_1997))
```

Results (scikit-learn 1.9.1): majority baseline accuracy **0.655**, model accuracy **0.653** (lower!), model AUC **0.627**, purchase-days score alone AUC **0.626**; leaky feature AUC **0.856**. Interpretation: the model adds nothing over a one-line rule on this synthetic data — a legitimate and important finding for the suitability assessment. The leaky feature's AUC is "too good to be true" (Kaufman et al., 2012). Session 8 continues from here with pipelines and tuning.
:::

## Portfolio-Style Task: An ML Use-Case Brief

Prepare the first part of portfolio notebook 2. Choose **one** use case — churn prediction, customer segmentation or anomaly detection — on the TPC-H warehouse or on a public dataset of your choice. Hand in a notebook section (or a two-page brief plus SQL) with:

- the business objective and the data mining goal, each with a **success criterion** (CRISP-DM),
- answers to the **six framing questions**,
- a **point-in-time feature table** (SQL or pandas) with a documented cut-off and label window, and sanity checks (rows, base rate, NULLs, value ranges),
- a **baseline** (majority class, a simple rule, or for clustering and anomaly detection a simple non-ML alternative) with its result,
- a **leakage audit**: a table of all features with "known at prediction time? yes/no, why",
- a **cost matrix** or value assumptions with their source, and the resulting decision rule (break-even probability or capacity),
- a short **suitability assessment**: is ML worth it here, and what would you check next?

::: answer lines=10
:::

::: solution
Marking guide (20 points):

- **Business objective and data mining goal** (3 points): concrete decision and owner; business success criterion (e.g. profit of the campaign, fewer lost customers) separated from the technical one (e.g. top-20 % lift above a stated value). Generic "predict churn with high accuracy" scores at most 1.
- **Framing** (3 points): all six questions answered consistently — unit, target and prediction point fit together; the target is computable from the data (e.g. "no purchase in the 6 months after the cut-off"); for clustering, the "target" is replaced by a usage criterion (can marketing name and use the groups?).
- **Feature table** (4 points): runs on a fresh `tpch.duckdb` (or the stated dataset); features only from data before the cut-off; label only from the label window; complete label window (not the incomplete 1998); NULLs handled deliberately (0 vs. undefined); checks reported, e.g. for the session's definition: 10,000 customers, base rate 34.5 % (cut-off 1997-07-01) or 34.7 % (1997-01-01).
- **Baseline** (3 points): baseline result reported with an appropriate metric (lift, precision/recall, profit — not accuracy alone); for segmentation e.g. the existing market segments, for anomaly detection e.g. a z-score rule.
- **Leakage audit** (3 points): every feature listed with a reason; at least one plausible leakage risk identified and avoided (e.g. features over the label window, status fields, statistics computed on all data before the split).
- **Business value** (2 points): cost matrix with stated assumptions and their source; break-even probability or capacity-based policy derived correctly.
- **Suitability** (2 points): honest conclusion (a simple rule may be enough on TPC-H), limitations (synthetic data, one cut-off), next steps for session 8 (time-based validation, model comparison against the baseline).

Typical good submission: the churn case with cut-offs 1997-01-01 (training) and 1997-07-01 (test), an added trend feature, the purchase-days rule as baseline (top-decile lift 1.35 at the July cut-off), the "purchase days in 1997" leak named and excluded, and a voucher or call campaign with break-even 33.3 % or 44.4 %. This is training material for portfolio notebook 2; the official brief and rubric of the portfolio are published separately.
:::

## References {.references}

- Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C., & Wirth, R. (2000). *CRISP-DM 1.0: Step-by-step data mining guide*. SPSS.
- Elkan, C. (2001). The foundations of cost-sensitive learning. In B. Nebel (Ed.), *Proceedings of the Seventeenth International Joint Conference on Artificial Intelligence (IJCAI 2001)* (pp. 973–978). Morgan Kaufmann.
- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data, 6*(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Provost, F., & Fawcett, T. (2013). *Data science for business: What you need to know about data mining and data-analytic thinking*. O'Reilly Media.
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
