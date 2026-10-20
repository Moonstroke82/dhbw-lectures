---
course: Data Analytics
session: 4
title: Analytical SQL
subtitle: Practice tasks on window functions, ROLLUP and CUBE, CTEs, period comparisons, concentration and funnel analysis
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 4 on your own or in the lab. Tasks 1 and 2 need only paper and pencil. Tasks 3–6 use the star schema from session 3 in `tpch.duckdb` (`fact_sales`, `dim_customer`, `dim_date`, `dim_part`), built from the TPC-H data (Transaction Processing Performance Council, n.d.). Task 7 is an analysis in the style of portfolio notebook 1. Write every query as CTEs that you can run step by step (Tanimura, 2021).

## Ranking Functions by Hand

Seven sales representatives have the following revenue (thousand euros). Fill in the three ranking columns for `ORDER BY revenue DESC`.

| Representative | Revenue | `rank()` | `dense_rank()` | `row_number()` |
|---|---|---|---|---|
| Ahmed | 90 | | | |
| Berg | 80 | | | |
| Costa | 80 | | | |
| Dietz | 70 | | | |
| Eke | 60 | | | |
| Fischer | 60 | | | |
| Gruber | 50 | | | |

Then answer (DuckDB Foundation, n.d., describes the functions): management wants "the top 3 representatives" for a bonus. Which function would you use, and what do you have to agree with management first?

::: answer lines=4
:::

::: solution
| Representative | Revenue | `rank()` | `dense_rank()` | `row_number()` |
|---|---|---|---|---|
| Ahmed | 90 | 1 | 1 | 1 |
| Berg | 80 | 2 | 2 | 2 or 3 |
| Costa | 80 | 2 | 2 | 3 or 2 |
| Dietz | 70 | 4 | 3 | 4 |
| Eke | 60 | 5 | 4 | 5 or 6 |
| Fischer | 60 | 5 | 4 | 6 or 5 |
| Gruber | 50 | 7 | 5 | 7 |

`row_number()` breaks ties arbitrarily unless the `ORDER BY` has a tie-breaker. For "top 3": `rank() <= 3` gives Ahmed, Berg, Costa (3 people); `dense_rank() <= 3` gives four people (incl. Dietz); `row_number() <= 3` gives three, but which of Berg and Costa is third is arbitrary. Management must decide **how ties are treated** — a definition question, not a SQL question.
:::

## Predict the Result

Without running the queries, predict the number of result rows (the operators go back to Gray et al., 1997). TPC-H has 5 regions, 5 market segments, 5 manufacturers and 25 brands; each brand belongs to exactly one manufacturer. All combinations occur in the data.

1. `GROUP BY ROLLUP (manufacturer, brand)`
2. `GROUP BY CUBE (region, segment)`
3. `GROUP BY GROUPING SETS ((manufacturer), (segment))`
4. `GROUP BY CUBE (manufacturer, brand)` — and why is this query partly redundant?
5. A 3-month moving average with `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` over 12 months: how many values are based on fewer than three months?

::: answer lines=6
:::

::: solution
1. 25 (manufacturer, brand) + 5 (manufacturer) + 1 (total) = **31** rows.
2. 25 + 5 + 5 + 1 = **36** rows (as in the session).
3. 5 + 5 = **10** rows; no grand total.
4. 25 + 5 + 25 (brand alone) + 1 = **56** rows. The 25 "brand alone" rows repeat the 25 (manufacturer, brand) rows with the same values, because brand determines manufacturer (a hierarchy). For hierarchies, `ROLLUP` is the right operator; `CUBE` is for independent dimensions.
5. **Two** (months 1 and 2). They should be marked or left empty in a report.
:::

## Top Brands per Manufacturer

Find the **three brands** with the highest net revenue in **1996** for **each manufacturer**. Use `rank()` and `QUALIFY`.

1. Write the query. Note: in DuckDB, `QUALIFY` cannot be combined with `GROUP BY ALL` — name the grouping columns explicitly.
2. Which manufacturer has the strongest single brand? How large is the gap between rank 1 and rank 3 within each manufacturer?
3. Rewrite the query without `QUALIFY`, using a CTE and `WHERE`.

::: answer lines=10
:::

::: solution
```sql
SELECT manufacturer, brand, sum(revenue) / 1e6 AS rev_m,
       rank() OVER (PARTITION BY manufacturer ORDER BY sum(revenue) DESC) AS rnk
FROM fact_sales JOIN dim_part USING (part_key) JOIN dim_date USING (date_key)
WHERE year = 1996
GROUP BY manufacturer, brand
QUALIFY rnk <= 3
ORDER BY manufacturer, rnk;
```

Expected result (million, DuckDB 1.5, sf 0.1):

| Manufacturer | Rank 1 | Rank 2 | Rank 3 |
|---|---|---|---|
| Manufacturer#1 | Brand#14 134.32 | Brand#13 131.15 | Brand#12 127.72 |
| Manufacturer#2 | Brand#21 129.23 | Brand#25 127.62 | Brand#24 121.16 |
| Manufacturer#3 | Brand#34 128.26 | Brand#33 125.31 | Brand#32 122.99 |
| Manufacturer#4 | Brand#41 127.88 | Brand#42 125.54 | Brand#43 123.18 |
| Manufacturer#5 | Brand#53 130.94 | Brand#54 130.61 | Brand#52 121.34 |

2. Strongest brand: Brand#14 (Manufacturer#1, 134.3 million). Gaps between rank 1 and rank 3 are small, about 4.7 to 9.6 million (4–7 %); Manufacturer#5's top two brands are almost equal (130.9 vs. 130.6). In synthetic data, rankings of nearly equal values are fragile — a small change can swap them.

3. Without `QUALIFY`:

```sql
WITH ranked AS (
  SELECT manufacturer, brand, sum(revenue) AS rev,
         rank() OVER (PARTITION BY manufacturer ORDER BY sum(revenue) DESC) AS rnk
  FROM fact_sales JOIN dim_part USING (part_key) JOIN dim_date USING (date_key)
  WHERE year = 1996
  GROUP BY manufacturer, brand)
SELECT * FROM ranked WHERE rnk <= 3 ORDER BY manufacturer, rnk;
```
:::

## Find and Fix the Bug

An analyst wants the growth of each market segment in 1997 compared with 1996 and writes:

```sql
WITH yearly AS (
  SELECT segment, year, sum(revenue) AS rev
  FROM fact_sales JOIN dim_customer USING (customer_key)
                  JOIN dim_date USING (date_key)
  GROUP BY ALL)
SELECT segment, year, rev / lag(rev) OVER (PARTITION BY segment ORDER BY year) - 1 AS growth
FROM yearly
WHERE year = 1997;
```

1. What does the query return, and why?
2. Fix it and report the growth rate of each segment.
3. Which segment would you name in a management summary — and would you call it "growth"?

::: answer lines=8
:::

::: solution
1. Five rows with `growth = NULL`. `WHERE` is evaluated **before** the window function, so only the 1997 rows are left when `lag()` runs, and there is no previous row. (The same trap as in lab task 3.)
2. Filter in an outer query:

```sql
WITH yearly AS (...),
growth AS (
  SELECT segment, year,
         rev / lag(rev) OVER (PARTITION BY segment ORDER BY year) - 1 AS growth
  FROM yearly)
SELECT * FROM growth WHERE year = 1997 ORDER BY growth DESC;
```

Expected result (DuckDB 1.5, sf 0.1): BUILDING +2.3 % · MACHINERY −0.3 % · FURNITURE −1.4 % · HOUSEHOLD −1.5 % · AUTOMOBILE −1.6 %. (DuckDB's `QUALIFY year = 1997` is an alternative.)

3. Building is the only segment with a positive change, but all changes are within ±2.5 % in uniformly generated synthetic data. A careful summary says "revenue was stable in all segments (−1.6 % to +2.3 %)" rather than presenting Building as a growth segment; without a measure of normal year-to-year variation, such differences should not be interpreted.
:::

## Funnel With Messy Data

A newsletter sign-up has four steps: `landing` (visit the landing page) → `form` (fill in the form) → `confirm` (confirm the e-mail) → `first_open` (open the first newsletter). Create the event table:

```sql
CREATE OR REPLACE TABLE nl_events AS
SELECT * FROM (VALUES
 (1,'landing'),(1,'form'),(1,'confirm'),(2,'landing'),(3,'landing'),(3,'form'),
 (4,'landing'),(4,'form'),(4,'confirm'),(4,'first_open'),(5,'landing'),
 (6,'landing'),(6,'form'),(6,'confirm'),(6,'first_open'),(7,'landing'),(7,'form'),
 (8,'landing'),(8,'form'),(8,'confirm'),(9,'landing'),(10,'landing'),(10,'form'),
 (10,'confirm'),(10,'first_open'),(11,'landing'),(12,'landing'),(12,'form'),
 (13,'confirm')) AS t(user_id, step);
```

1. Count the distinct users per step and compute the conversion from the previous step (`lag()`) and from the first step (`first_value()`).
2. User 13 has a `confirm` event but no `landing` or `form`. How does this affect your result? Compute a **strict** funnel that counts a user in a step only if they also reached all previous steps.
3. Where is the biggest drop, and what would you investigate next?

::: hint
Map the step names to numbers with `CASE` so that `ORDER BY` follows the process, not the alphabet. For the strict funnel, compute each user's highest step and check that the number of distinct steps equals that highest step number.
:::

::: answer lines=10
:::

::: solution
1. Simple funnel:

```sql
WITH s AS (
  SELECT CASE step WHEN 'landing' THEN 1 WHEN 'form' THEN 2
                   WHEN 'confirm' THEN 3 ELSE 4 END AS step_no,
         step, count(DISTINCT user_id) AS users
  FROM nl_events GROUP BY step)
SELECT step_no, step, users,
       users / lag(users) OVER (ORDER BY step_no) AS conv_prev,
       users / first_value(users) OVER (ORDER BY step_no) AS conv_total
FROM s ORDER BY step_no;
```

Result: landing 12 · form 8 (66.7 %) · confirm **6** (75.0 %) · first_open 3 (50.0 %); overall 25.0 %. (In DuckDB, `/` between integers returns a decimal number; in other databases, cast to `DOUBLE` first.)

2. User 13 inflates the confirm step: 6 instead of 5 users. A strict funnel gives landing 12 · form 8 (66.7 %) · confirm 5 (62.5 %) · first_open 3 (60.0 %); overall 25.0 %. One strict solution: per user, collect the step numbers, keep only users whose steps form an unbroken sequence from 1 (e.g. `count(DISTINCT step_no) = max(step_no)` and `min(step_no) = 1`), then count users with `max_step >= k` for each step k. Any correct approach is fine. Events without a previous step usually indicate tracking problems (e.g. a user who signed up via another page, or a lost event); they must be explained, not silently counted.

```sql
WITH e AS (
  SELECT user_id, CASE step WHEN 'landing' THEN 1 WHEN 'form' THEN 2
                            WHEN 'confirm' THEN 3 ELSE 4 END AS step_no
  FROM nl_events),
u AS (
  SELECT user_id, max(step_no) AS max_step FROM e GROUP BY user_id
  HAVING count(DISTINCT step_no) = max(step_no) AND min(step_no) = 1)
SELECT k AS step_no, count(*) FILTER (WHERE max_step >= k) AS users
FROM u, range(1, 5) AS r(k) GROUP BY k ORDER BY k;
```
3. In the strict funnel, the largest relative drop is form → confirm (37.5 % of users who filled in the form never confirm), closely followed by landing → form (33.3 %). With the messy data, the confirm step looked like the *best* step (75 %) — the data problem changed the conclusion. Next: check the confirmation e-mail (delivery delay, spam folder, unclear wording) and the form, then test a change with an A/B test (session 9). The funnel shows *where* users leave, not *why*. With 12 users, all rates are very uncertain.
:::

## Portfolio-Style Task: Is Revenue Concentrated?

A typical question in portfolio notebook 1: **"Do a few customers generate most of our revenue, and has that changed over time?"** Answer it with analytical SQL and write a short interpretation.

1. For 1997, compute each active customer's revenue, the **cumulative share** of revenue when customers are sorted by revenue (descending), and find: the share of customers that generates 50 % of revenue, and the revenue share of the top 20 % of customers.
2. For each year 1993–1997, compute the revenue share of the **top 100 customers**.
3. Write an interpretation of about 100–150 words, including one warning about the data.

::: answer lines=14
:::

::: solution
Marking guide (10 points):

- **Cumulative share query** (3 points), e.g.

```sql
WITH c AS (
  SELECT customer_key, sum(revenue) AS rev
  FROM fact_sales JOIN dim_date USING (date_key)
  WHERE year = 1997 GROUP BY customer_key),
r AS (
  SELECT rev,
         sum(rev) OVER (ORDER BY rev DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
           / sum(rev) OVER () AS cum_share,
         row_number() OVER (ORDER BY rev DESC) AS rn,
         count(*) OVER () AS n
  FROM c)
SELECT n, min(rn) FILTER (WHERE cum_share >= 0.5) / n AS cust_share_for_50,
       max(cum_share) FILTER (WHERE rn <= 0.2 * n) AS top20_rev_share
FROM r GROUP BY n;
```

Expected (DuckDB 1.5, sf 0.1): 8,640 active customers in 1997; **25.8 %** of customers (2,226) generate 50 % of revenue; the top 20 % generate **41.7 %**; 80 % of revenue needs 54.4 % of customers. Note the explicit frame `ROWS BETWEEN …`: with the default frame, customers with equal revenue would be summed together.

- **Top 100 per year** (2 points): `row_number() OVER (PARTITION BY year ORDER BY rev DESC)` in a CTE, then `sum(rev) FILTER (WHERE rn <= 100) / sum(rev)` per year. Expected: 1993 4.01 % · 1994 3.97 % · 1995 4.04 % · 1996 4.04 % · 1997 3.90 %.
- **Interpretation** (3 points): revenue is only moderately concentrated — far from the "80/20 rule" (the top 20 % have about 42 %, not 80 %); the top 100 customers (about 1.2 % of active customers) generate about 4 % of revenue, stable over five years. So there is no strong dependence on a few key accounts.
- **Warning** (1 point): TPC-H is synthetic, uniformly generated data — real B2B customer bases are usually much more concentrated; also, the base matters (8,640 active customers in 1997, not all 15,000 customers).
- **Clarity** (1 point).
:::

## References {.references}

- DuckDB Foundation. (n.d.). *Window functions*. DuckDB documentation. Retrieved October 20, 2026, from https://duckdb.org/docs/current/sql/functions/window_functions.html
- Gray, J., Chaudhuri, S., Bosworth, A., Layman, A., Reichart, D., Venkatrao, M., Pellow, F., & Pirahesh, H. (1997). Data cube: A relational aggregation operator generalizing group-by, cross-tab, and sub-totals. *Data Mining and Knowledge Discovery, 1*(1), 29–53. https://doi.org/10.1023/A:1009726021843
- Tanimura, C. (2021). *SQL for data analysis: Advanced techniques for transforming data into insights*. O'Reilly Media.
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
