---
course: Data Analytics
session: 10
title: Lab Workshop and Catch-Up
subtitle: Revision of Parts A–B — warehouse and SQL, visualisation and portals, ML use cases and experiments — plus a portfolio-style peer review
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet helps you revise Parts A and B (sessions 2–9) on your own or in the lab. It contains no new content: every task uses terms and methods from the session slides — grain, slowly changing dimensions, window functions, ROLLUP, honest charts, the semantic layer, framing, leakage, baselines, lift, cost matrices, sample size and trust checks. Tasks 1–3 and 5 need only paper and pencil (and a calculator for task 5). Task 4 uses Python with DuckDB and `tpch.duckdb` from session 2 (TPC-H base tables; Transaction Processing Performance Council, n.d.). Task 6 is a portfolio-style review task; task 7 is an optional task for your partner-project team. The companies, people and numbers in tasks 2, 3, 5 and 6 are invented for practice.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. In Kimball's bus architecture, data marts are integrated through shared, conformed dimensions.
2. "Non-volatile" means that no new data is ever added to a data warehouse.
3. With a type 1 slowly changing dimension, last year's sales of a customer who moved stay under the old city.
4. A drill-down from year to quarter adds a column to the `GROUP BY` clause.
5. `GROUP BY ROLLUP (region, segment)` returns a subtotal for each segment across all regions.
6. A pie chart is a good choice to compare five shares that differ by only a few percentage points.
7. Row-level security should be enforced where the data is queried, not only in the dashboard.
8. Fitting a scaler on all rows before cross-validation is a form of leakage.
9. If a model reaches a higher accuracy than the simple rule, it is the better choice for the retention campaign.
10. A sample ratio mismatch can be fixed by reweighting the two groups to 50/50.

::: answer lines=10
:::

::: solution
1. **True.** Conformed dimensions (one customer, one calendar) make marts of different business processes combinable (session 2; Kimball & Ross, 2013).
2. **False.** New data is loaded regularly; "non-volatile" means that loaded data is not changed by daily transactions.
3. **False.** Type 1 overwrites the attribute, so history is restated: last year's sales now appear under the new city. Type 2 keeps them under the old city.
4. **True.** Going to a finer level of the date hierarchy means grouping by one more (finer) column.
5. **False.** ROLLUP follows the column order: (region, segment), (region) and (). Subtotals per segment across regions come from `CUBE` or `GROUPING SETS`.
6. **False.** Angles are read less accurately than positions on a common scale; use a sorted bar chart (session 5).
7. **True.** Rules only in the user interface can be bypassed by anyone with access to the data or the SQL (session 6).
8. **True.** The scaler learns means and variances from the validation rows; put preprocessing into the `Pipeline` so it is fitted inside each fold (session 8).
9. **False.** Accuracy ignores unequal classes and costs; compare by lift and profit at the capacity of the campaign (session 7: the majority baseline had the highest accuracy and found no churner).
10. **False.** An SRM is a symptom of a problem in assignment, logging or filtering; the groups are no longer comparable. Find and fix the cause, then rerun (session 9).

Marking: 1 point per statement (verdict and, for false statements, a correct correction), 10 points.
:::

## Which Method for Which Request?

A chain of fitness studios collects check-ins, memberships, cancellations and class bookings in a data warehouse. For each request, name the **kind of analysis** (query or report, dashboard, classification, clustering, anomaly detection or rule, forecasting, experiment, quasi-experiment), the **session** it belongs to, and **one pitfall** to watch out for.

1. "How many members cancelled in each studio last quarter, compared with the same quarter last year?"
2. "Every studio manager should see check-ins, new members and cancellations each morning — but only for their own studio."
3. "Which members will cancel in the next three months, so that trainers can invite them to a free session?"
4. "Does a welcome call in the first week reduce cancellations of new members?"
5. "Group members by how they use the studio, so we can design class packages."
6. "Find members whose card is used in two studios within one hour."
7. "Since we raised prices in our Berlin studios only, cancellations went up there. Was it the price?"
8. "How many check-ins will each studio have per hour next week, for staff planning?"

::: answer lines=12
:::

::: hint
Ask first: does the request describe the past, predict the future for single members, look for groups or unusual cases, or ask what happens **if we act**?
:::

::: solution
1. **Query or report** (sessions 3–4): roll-up by studio and quarter, `lag(…, 4)` over quarters or a self-join. Pitfall: a different number of members per studio — report the cancellation **rate**, not only counts; the current quarter may be incomplete.
2. **Dashboard with row-level security** (session 6). Pitfall: the filter only in the user interface; define the KPIs once (e.g. "cancellation" = notice received or contract ended?).
3. **Classification** (sessions 7–8): unit member at a cut-off, label = notice in the next 3 months. Pitfalls: leakage (e.g. "cancellation reason", "notice period started" or check-ins after the cut-off as features); compare with a rule such as "no check-in for 4 weeks".
4. **Experiment / A/B test** (session 9): randomise new members (unit member), primary metric cancellation within e.g. 6 months. Pitfalls: the effect appears only months later (plan the duration), peeking, trainers who call "their" members in the control group (interference).
5. **Clustering** (session 8, track B): features such as visit frequency, time of day, class share. Pitfall: judging by one score; the groups must be distinct, stable and usable for packages.
6. **A rule** (session 8, track C: prefer rules for known patterns): the condition can be written as SQL with a window over each card's check-ins (`lag` by time). Pitfall: legitimate cases (a member trains in two nearby studios), so produce a review list, not automatic blocking.
7. **Quasi-experiment: difference-in-differences** (session 9, outlook) with other cities as comparison. Pitfall: parallel trends — a Berlin-specific event (new competitor) would break the assumption; check earlier periods.
8. **Forecasting** (Part C, sessions 11–14): time series per studio and hour with daily and weekly seasonality. Pitfall: holidays and special events; evaluate on later weeks, not random hours.

Marking: 1 point per request (kind of analysis with a fitting pitfall), 8 points. Accept other well-argued answers, e.g. a simple rule plus a dashboard for request 3 if the student explains why a model may not beat the rule.
:::

## Review a Colleague's Report

A colleague has prepared the monthly report of an online bookshop from the shop's data warehouse. The report was produced on **20 October**. Find the problem behind each statement, name the concept from Part A, and propose a fix.

1. "Revenue per customer fell from EUR 52 to EUR 31." — Last month the analyst divided by customers with at least one order; this month by all registered customers.
2. "October is our weakest month this year." — The bar chart compares October with the full months January–September.
3. "Sales in Hamburg are up 40 % compared with last year." — The customer dimension overwrites the city when a customer moves; last year's sales are grouped by the **current** city.
4. "Shipping revenue was EUR 186,000." — The fact table holds one row per **order line**; the shipping fee of each order is stored on every line of that order.
5. "Our five regions differ strongly." — The bar chart's y-axis runs from EUR 95,000 to EUR 105,000.
6. "The average discount across our five regions was 8.2 %." — The analyst averaged the five regional average discount rates.

::: answer lines=12
:::

::: hint
Each statement matches one session 2–6 concept: denominator and KPI definition, incomplete period, slowly changing dimension, grain, truncated axis, non-additive measure.
:::

::: solution
1. **KPI definition / denominator** (sessions 3, 5, 6): two different definitions of "customer" make the months incomparable. Fix: define the KPI once (e.g. revenue per **active** customer) in the semantic layer and use it every month.
2. **Incomplete period** (sessions 2, 5): October has only 19 or 20 days of data. Fix: compare complete months, show October to date against the same days of September or of last October, or mark it as partial.
3. **Slowly changing dimension type 1** (session 3): overwriting the city restates history, so customers who moved to Hamburg take their old sales with them. Fix: type 2 (new row with validity dates) to report sales by the city at the time of the order — or state clearly that the report uses current cities.
4. **Mixed grain / double counting** (session 3): the order-level fee is repeated on every line, so the sum counts it once per line (with about four lines per order, roughly four times too much). Fix: an order-level fact table for fees, or allocate the fee to the lines (e.g. divide by the number of lines).
5. **Truncated axis** (session 5): differences of a few percent look huge. Fix: bars start at zero (or use dots on a shorter axis and say so); write the actual differences in the title.
6. **Non-additive measure / average of ratios** (session 6): small regions count as much as large ones. Fix: total discount amount ÷ total gross revenue across all regions (a weighted average), defined once.

Marking: 2 points per statement (problem and concept 1, fix 1), 12 points.
:::

## Average Order Value in TPC-H

Management of the TPC-H wholesaler asks for the **average order value** (net revenue per order) per region and year, with a row for all regions and the change against the previous year.

1. A colleague runs `SELECT avg(revenue) FROM fact_sales JOIN dim_date USING (date_key) WHERE year = 1997` and reports **34,152**. Why is this not the average order value?
2. Can you count orders in `fact_sales`? Compare `count(*)` of `orders` for all years with the number of distinct `(customer_key, date_key)` pairs in `fact_sales`, and explain the difference. What is missing in the star schema?
3. Write one query on the base tables (`orders`, `lineitem`, `customer`, `nation`, `region`) for the complete years 1992–1997: number of orders and average order value per region and year, a row "ALL REGIONS" per year using `ROLLUP`, and the growth against the previous year with `lag()`.
4. Finance reports an average order value of about **141,600** for 1997, computed as `avg(o_totalprice)`. Explain the difference to your result.
5. Write a two-sentence interpretation for management.

::: answer lines=14
:::

::: hint
Compute the revenue of each **order** in a first CTE, then aggregate the orders. For the "ALL REGIONS" row, compute the average as sum ÷ count over all orders — not as the average of the five regional averages. Look up how TPC-H defines `o_totalprice` (it includes something that net revenue does not).
:::

::: solution
Code (tested with DuckDB 1.5.5, sf 0.1):

```sql
WITH order_rev AS (                       -- grain: one row per order
  SELECT o_orderkey, r_name AS region, year(o_orderdate) AS year,
         sum(l_extendedprice * (1 - l_discount)) AS revenue
  FROM orders JOIN lineitem ON l_orderkey = o_orderkey
              JOIN customer ON o_custkey = c_custkey
              JOIN nation ON c_nationkey = n_nationkey
              JOIN region ON n_regionkey = r_regionkey
  WHERE o_orderdate < DATE '1998-01-01'
  GROUP BY ALL),
aov AS (
  SELECT coalesce(region, 'ALL REGIONS') AS region, year,
         count(*) AS orders, sum(revenue) / count(*) AS aov
  FROM order_rev GROUP BY ROLLUP (year, region))
SELECT region, year, orders, round(aov, 0) AS aov,
       round(100 * (aov / lag(aov) OVER (PARTITION BY region ORDER BY year) - 1), 2)
         AS growth_pct
FROM aov WHERE year IS NOT NULL           -- drop the grand total over all years
ORDER BY region, year;
```

1. **Wrong grain.** `fact_sales` has one row per **order line**, so the query returns the average line revenue. An order has about 4.0 lines on average, so the average order value is about four times higher (136,168 in 1997).
2. `orders` has **150,000** rows; `fact_sales` has **149,469** distinct (customer, date) pairs. 531 orders are "lost" because some customers placed several orders on the same day. The star schema has **no order number**: Kimball and Ross (2013) would keep it in the fact table as a **degenerate dimension** (a key without its own dimension table) to allow counting orders and order-level measures.
3. Result (excerpt): ALL REGIONS 1992 **137,292** (22,759 orders), 1993 136,700 (−0.43 %), 1994 137,237 (+0.39 %), 1995 137,249 (+0.01 %), 1996 136,642 (−0.44 %), 1997 **136,168** (−0.35 %). Regions in 1997 between 134,965 (Europe, −1.38 %) and 137,694 (Middle East, +0.10 %); all yearly changes per region between −2.10 % (Europe 1993) and +1.73 % (Europe 1994). The "ALL REGIONS" row is computed over all orders; the average of the five regional averages would differ only slightly here (1997: 136,155 instead of 136,168), because the regions have similar numbers of orders — with unequal regions the difference can be large.
4. `o_totalprice` is the **gross** order total including **tax**: in TPC-H it equals the sum of `l_extendedprice * (1 - l_discount) * (1 + l_tax)` (checked: differences below 0.11 per order). The average tax rate is about 4.0 %, so the average order total in 1997 is **141,616**, 4.0 % above the net value. Neither number is wrong — they are different definitions; the KPI sheet must say which one is meant (session 5).
5. Example: "The average net order value is stable at about 136,000–137,000 in every region and year; changes of up to ±2 % are no trend. Note that finance reports order totals including tax (about 4 % higher), so always state which definition a figure uses." Strong answers also mention that TPC-H is synthetic, which explains the flat values.

Marking (10 points): grain (2); order count and degenerate dimension (2); correct query with ROLLUP and lag (3); tax explanation (2); interpretation with a definition warning (1).
:::

## Late Invoices: From Model to Experiment

A B2B wholesaler sends about **10,000 invoices** per month. A model ranks open invoices by the risk of being paid late. The accounts team could call customers a few days before the due date. Assumptions: a call costs **EUR 8**; a late invoice costs **EUR 60** (dunning, interest, follow-up work); a call prevents late payment in **25 %** of the invoices that would otherwise be late.

The model was tested on a later month (1,000 invoices per decile, ranked by score):

| Decile | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Late rate | 72 % | 58 % | 47 % | 38 % | 30 % | 24 % | 18 % | 13 % | 9 % | 6 % |

1. Set up the **cost matrix** for calling an invoice (late / not late). Above which late probability *p* does a call pay off?
2. Compute the **overall late rate**, the cumulative **lift** and the cumulative **profit** for calling the top 10 %, 20 % and 30 %. How many invoices should be called each month?
3. The head of accounts says: "The top decile has a lift above 2 — so the calls work." Why does the lift table not show that?
4. Design a test that shows whether the calls work: what is randomised, which **unit**, which **primary metric**? With a late rate of **65 %** in the top 20 % and a minimum effect of **10 percentage points**, how many invoices per group are needed (rule of thumb n ≈ 16σ²/δ²)? How long must the test run, and what limits the duration?

::: answer lines=14
:::

::: hint
TP: called and would have been late; FP: called and would have paid on time anyway. The value of a TP is the expected saving minus the cost of the call. For the lift, divide the late rate of the called group by the overall late rate.
:::

::: solution
1. Called and late (TP): 0.25 × 60 − 8 = **+EUR 7**; called and on time (FP): **−EUR 8**; not called: 0. Expected value of a call: *p* × 7 − (1 − *p*) × 8 > 0 ⇔ 15*p* > 8 ⇔ ***p* > 53.3 %** (same logic as the cost matrix of session 7).
2. Overall late rate = mean of the deciles = **31.5 %**.

| Called | Late rate of the called group | Cumulative lift | Cumulative profit |
|---|---|---|---|
| Top 10 % (1,000) | 72.0 % | **2.29** | 720 × 7 − 280 × 8 = **EUR 2,800** |
| Top 20 % (2,000) | 65.0 % | **2.06** | + 580 × 7 − 420 × 8 = **EUR 3,500** |
| Top 30 % (3,000) | 59.0 % | **1.87** | − 950 → **EUR 2,550** |

Call the **top 20 %, about 2,000 invoices** per month: decile 2 (58 %) is still above the 53.3 % threshold, decile 3 (47 %) is below. Calling everyone would cost EUR 32,750 per month.

3. The lift shows that the model finds invoices that **will be** late — a prediction. Whether a call **changes** the outcome is a causal question; the 25 % prevention rate is an assumption, not a result. Customers with high risk might pay late anyway (or be annoyed by the call). Only a comparison of called and not-called invoices with the same risk shows the effect (session 9; Kohavi et al., 2020).
4. **Randomise within the top 20 %**: half of the eligible invoices are called, the other half are not (holdout). Unit: preferably the **customer** (all invoices of a customer in the same group, because the call talks to the customer and affects their other invoices); primary metric: share of invoices paid late; guardrails: complaints, payment volume, customer churn. Rule of thumb: 16 × 0.65 × 0.35 / 0.10² = **364** per group (statsmodels with Cohen's h: 375). With about 1,000 eligible invoices per group and month, the sample size is reached within the first month. The duration is limited by the **outcome**: an invoice can be judged only after its due date (plus a tolerance), so the results come in only some weeks after the last call. Run at least one full billing month to cover all customers' payment cycles, and analyse once. Good answers also note the cost of the holdout (expected profit lost on uncalled invoices) and that a minimum effect of 10 pp lies below the break-even reduction (EUR 8 / EUR 60 = 13.3 pp), so the test can also show that calls do **not** pay off.

Marking (12 points): 1 cost matrix and threshold (3); 2 overall rate, lift and profit, decision (4); 3 prediction vs. causal effect (2); 4 design with unit and metric (1), sample size (1), duration and its limit (1).
:::

## Portfolio-Style Task: Review a Notebook

A pair hands in the following summary of their **notebook 2** (ML use case, fictional). Review it like in the peer feedback round of session 10: use the notebook 2 checklist and the suggested rubric from session 8.

> **Churn prediction for a mobile phone provider (public dataset, 7,000 customers, monthly snapshots from January 2023 to June 2024; 8 % churn).**
>
> We dropped rows with missing values (11 % of the customers) and standardised all numeric columns. Then we split the data randomly into 80 % training and 20 % test data. Features: tenure, monthly charges, contract type, number of support calls, data volume and `contract_end_reason`. We tuned a gradient boosting model with `GridSearchCV` (5-fold) and chose the parameters with the best **test** accuracy. Result: **accuracy 96 %**. The most important feature is `contract_end_reason` (importance 0.71, computed on the training data). **Recommendation:** deploy the model, because it is very accurate.

1. Find at least **six** problems. For each, name the concept from sessions 7–8 and the consequence for the result.
2. Write the feedback in the format **two strengths, three suggestions, one question**. The suggestions must be the three most important ones, each with a concrete next step.
3. Rewrite the **recommendation** in the five-part structure from session 8 — as far as you can without new results (use placeholders such as "[lift]" where a number is missing).

::: answer lines=16
:::

::: hint
Check in this order: point-in-time correctness (which features are known at the prediction point?), the split and preprocessing, the baseline, the metric, how the test set was used, and what the recommendation says about value and limits.
:::

::: solution
1. Problems (any six, 1 point each, up to 6):
   - **Leakage — feature caused by the target:** `contract_end_reason` is filled only when a contract ends, i.e. after the churn decision (Kaufman et al., 2012). It explains the high importance and accuracy; the model cannot be used in production.
   - **Random split of time-ordered snapshots:** the same customer appears in several months in training and test; training rows "see" the test period. Validate on a **later** period (e.g. train up to December 2023, test on 2024).
   - **Preprocessing outside the pipeline:** standardising all rows before the split leaks statistics of the test rows; for gradient boosting scaling is not even needed. Put imputing and scaling into the `Pipeline`.
   - **Dropping missing values** (11 %) without checking whether they are random: if, for example, new customers lack data, the model is evaluated on a biased population. Impute with a missing indicator instead, and report the effect.
   - **Tuning on the test set:** choosing parameters by test accuracy turns the test set into a validation set; the reported score is optimistic. Use the cross-validation score for tuning and the test period **once**.
   - **No baseline and the wrong metric:** with 8 % churn, "nobody churns" already reaches **92 %** accuracy; 96 % is not impressive. Compare with a majority baseline and a simple rule (e.g. many support calls or a monthly contract) by lift, precision at capacity and profit.
   - **Importance on training data:** compute permutation importance on held-out data; importances of a leaky model mainly show the leak.
   - **No decision and no business evaluation:** who would be contacted, how many, what does a contact cost, and what is a kept customer worth? "Very accurate" is no reason to deploy.
2. Example feedback (4 points: strengths specific 1, three suggestions with the most important issues and concrete steps 2, a real question 1):
   - *Strengths:* a public dataset with monthly snapshots is a good basis for a time-aware design; tuning with cross-validation in a grid is set up correctly in principle.
   - *Suggestions:* (1) Remove `contract_end_reason` and check every feature against the prediction point — write a short leakage audit. (2) Replace the random split by a split in time (train on snapshots up to a cut-off, test on later months), with imputing and scaling inside a pipeline and tuning by cross-validation on the training period only. (3) Add a majority baseline and a simple rule, and evaluate by lift and profit for a realistic number of contacts.
   - *Question:* which decision should the model support — who calls whom, and how many customers can be contacted per month?
3. Example (4 points: answer first 1, evidence against a baseline 1, decision and limits 1, next step 1): "**Do not deploy yet.** After removing the leaky feature, the model must show that it beats the rule 'monthly contract and at least three support calls' on a later period: top-decile lift [lift] vs. [lift of the rule], profit [EUR] for [n] contacts per month. If the gain is small, use the rule. Limits: one public dataset, 18 months, costs and the effect of a contact are assumptions. Next step: a time-based validation and, if the model is used, a randomised holdout to measure whether contacts reduce churn."

Marking guide (14 points; training only — the portfolio brief and rubric are published separately): problems 6, feedback 4, rewritten recommendation 4. A strong answer puts the leak first: as long as `contract_end_reason` is in the model, all other numbers are meaningless.
:::

## Optional Team Task: First Findings for Your Partner Project {.optional}

Prepare a one-page **first-findings brief** for your semester-6 partner project, following the project brief structure from session 1: business goal and success criteria; stakeholders and their needs; as-is process; data inventory (sources, volume, quality, access); open questions, risks and next steps. Add one line per Part A–B method you could apply first and why.

Keep the brief inside your team: it may contain confidential information from the partner company. Do not upload it to public repositories or share it outside the course.

::: answer lines=10
:::

::: solution
No model answer — the projects differ. Checklist for the lecturer or a team member reviewing the brief:

- The **decision** the project should support is named, with an owner, and success can be measured.
- Stakeholders are named by **role** (not only by name), with what they need from the result.
- The as-is process fits on one page and shows where data is created.
- The data inventory states for each source: system, owner, volume, time span, known quality problems, and the **access status** (requested, granted, open).
- Risks include at least one data risk (definitions, missing history, access delays) and one organisational risk (availability of contacts, unclear goal).
- The first method is realistic: usually a descriptive result (data inventory, KPI definition, dashboard prototype) before a model; causal questions name a comparison group.
- No confidential information appears outside the team's private workspace.
:::

## References {.references}

- Kaufman, S., Rosset, S., Perlich, C., & Stitelman, O. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data, 6*(4), Article 15. https://doi.org/10.1145/2382577.2382579
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy online controlled experiments: A practical guide to A/B testing*. Cambridge University Press. https://doi.org/10.1017/9781108653985
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 21, 2026, from https://www.tpc.org/tpch/
