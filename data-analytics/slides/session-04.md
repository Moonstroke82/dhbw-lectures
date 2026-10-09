---
course: Data Analytics
session: 4
title: Analytical SQL
subtitle: Window functions · ROLLUP, CUBE and GROUPING SETS · CTEs · rankings, running totals, cohorts and funnels
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Analytical SQL {.title}

::: notes
Time plan for today (3 h): recap 10 min · CTEs 10 min · window functions 35 min · break 10 min · ROLLUP/CUBE/GROUPING SETS 20 min · typical analyses: cohorts and funnels 15 min · lab 70 min · wrap-up 5 min · ~5 min buffer.
Students need tpch.duckdb with the star schema from session 3. Anyone who lost it runs the session 3 lab cells first.
:::

---

# Today's Agenda

1. Recap: OLAP operations in SQL
2. Common table expressions: readable queries
3. Window functions: rankings, running totals, comparisons over time
4. `ROLLUP`, `CUBE` and `GROUPING SETS`: subtotals in one query
5. Typical analyses: cohorts and funnels
6. Lab: analytical SQL on the star schema

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:10 CTEs (input + live demo) · 0:20 Window functions (input + live demo) · 0:55 Break · 1:05 ROLLUP/CUBE (input + demo) · 1:25 Cohorts and funnels (input) · 1:40 Lab (pairs) · 2:50 Wrap-up.
Live-code the examples in DuckDB instead of only showing slides — the result tables make the concepts concrete.
:::

---

# Recap: What GROUP BY Cannot Do

- "Revenue per nation" — easy with `GROUP BY`
- But how do we get…
  - the **top 2 nations per region**?
  - a **running total** of revenue over the year?
  - the change compared with the **previous year**?
  - region totals **and** a grand total in one result?

::: callout
`GROUP BY` collapses rows. Analytical questions often need the detail rows **and** an aggregate next to them.
:::

::: notes
Collect how students would solve these with what they know (subqueries, Excel). Then show that analytical SQL handles all four directly.
:::

---

# Readable Queries {.section}

Common table expressions

---

# Common Table Expressions (CTEs)

- `WITH name AS (…)` defines a named intermediate result
- Several CTEs can build on each other — a query reads **top to bottom** like a recipe
- Easier to test: run each step on its own

```sql
WITH monthly AS (
  SELECT year, month, sum(revenue) AS rev
  FROM fact_sales JOIN dim_date USING (date_key)
  GROUP BY year, month
)
SELECT * FROM monthly WHERE year = 1997 ORDER BY month;
```

::: source
Based on Tanimura (2021).
:::

::: notes
CTEs replace nested subqueries. They do not make a query faster by themselves, but much easier to read and debug. Recursive CTEs exist (hierarchies, e.g. bill of materials) — not needed today.
:::

---

# Window Functions {.section}

Aggregates without collapsing rows

---

# How Window Functions Work

```sql
function(...) OVER (
  PARTITION BY ...   -- groups, like GROUP BY, but rows stay
  ORDER BY ...       -- order within each group
  ROWS BETWEEN ...   -- optional frame, e.g. last 3 rows
)
```

| Type | Examples | Typical question |
|---|---|---|
| Ranking | `rank()`, `dense_rank()`, `row_number()` | Top N per group |
| Aggregate over a window | `sum()`, `avg()` with `OVER` | Running totals, moving averages, share of total |
| Offset | `lag()`, `lead()` | Change vs. previous period |

::: source
Based on Tanimura (2021) and DuckDB Foundation (n.d.).
:::

::: notes
Key idea: the window function computes a value for each row, looking at a "window" of related rows. The result keeps all rows. rank() leaves gaps after ties, dense_rank() does not, row_number() is always unique. DuckDB also supports QUALIFY to filter on window results (not standard SQL, but available in several analytical databases).
:::

---

# Example: Top 2 Nations per Region

```sql
SELECT region, nation, sum(revenue) AS revenue,
       rank() OVER (PARTITION BY region
                    ORDER BY sum(revenue) DESC) AS rnk
FROM fact_sales JOIN dim_customer USING (customer_key)
                JOIN dim_date USING (date_key)
WHERE year = 1997
GROUP BY region, nation
QUALIFY rnk <= 2;
```

::: callout
The window function runs **after** `GROUP BY`: first revenue per nation, then the ranking within each region.
:::

::: source
Own example based on TPC-H data (Transaction Processing Performance Council, n.d.).
:::

::: notes
Result (DuckDB 1.5.6, sf 0.1): e.g. Europe — Germany 129.5 million (rank 1), Romania 124.7 million (rank 2); Middle East — Iran 140.9 million is the highest of all. Without QUALIFY, wrap the query in a CTE and filter WHERE rnk <= 2.
:::

---

# Example: Running Total and Moving Average

```sql
WITH monthly AS (
  SELECT month, sum(revenue) AS rev
  FROM fact_sales JOIN dim_date USING (date_key)
  WHERE year = 1997 GROUP BY month
)
SELECT month, rev,
       sum(rev) OVER (ORDER BY month) AS running_total,
       avg(rev) OVER (ORDER BY month
         ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS moving_avg_3m
FROM monthly ORDER BY month;
```

::: source
Own example based on TPC-H data (Transaction Processing Performance Council, n.d.).
:::

::: notes
Result: monthly revenue in 1997 is between about 246 and 271 million; the running total reaches about 3,089 million in December. The 3-month moving average smooths the curve — a first link to time series (sessions 11–14). Ask: why are the first two moving-average values based on fewer months?
:::

---

# Example: Change vs. Previous Year

```sql
WITH yearly AS (
  SELECT region, year, sum(revenue) AS rev
  FROM fact_sales JOIN dim_customer USING (customer_key)
                  JOIN dim_date USING (date_key)
  WHERE year < 1998 GROUP BY region, year
)
SELECT region, year, rev,
       rev / lag(rev) OVER (PARTITION BY region ORDER BY year) - 1
         AS growth
FROM yearly ORDER BY region, year;
```

::: source
Own example based on TPC-H data (Transaction Processing Performance Council, n.d.).
:::

::: notes
1998 is excluded because it is incomplete (orders end in August 1998, see session 2). Europe: growth between about −3 % and +4 % per year — synthetic data without a real trend. The first year per region has no previous value (NULL): discuss how to show this in a report.
:::

---

# Subtotals in One Query {.section}

ROLLUP, CUBE and GROUPING SETS

---

# ROLLUP, CUBE and GROUPING SETS

| Clause | Groups computed for `(region, segment)` | Use |
|---|---|---|
| `GROUP BY ROLLUP (region, segment)` | (region, segment), (region), () | Subtotals along a hierarchy |
| `GROUP BY CUBE (region, segment)` | All combinations: (region, segment), (region), (segment), () | All subtotals — the OLAP cube |
| `GROUP BY GROUPING SETS ((region), (segment))` | Exactly the listed groups | Selected subtotals |

- Subtotal rows show `NULL` in the rolled-up columns; `grouping()` tells real NULLs from subtotals

::: source
Based on Gray et al. (1997) and Tanimura (2021).
:::

::: notes
Gray et al. introduced the CUBE operator (session 3). Example (1997, Europe and Asia): ROLLUP returns 10 detail rows, 2 region subtotals and 1 grand total = 13 rows (grand total about 1,219.5 million). CUBE over all 5 regions and 5 segments returns 25 + 5 + 5 + 1 = 36 rows.
:::

---

# Typical Analyses {.section}

Cohorts and funnels

---

# Cohort Analysis

- A **cohort** is a group of customers who started in the same period, e.g. first order in 1993
- Track how many of them are **still active** in later periods → retention
- Built with CTEs: first period per customer, activity per period, then a join

| Cohort (first order) | Customers | Active 1 year later | Active 2 years later |
|---|---|---|---|
| 1992 | 8,717 | 87.3 % | 87.7 % |
| 1993 | 1,029 | 81.6 % | 81.8 % |
| 1994 | 208 | 81.7 % | 80.3 % |

::: source
Own analysis of TPC-H data (Transaction Processing Performance Council, n.d.); method based on Tanimura (2021).
:::

::: notes
Tested with DuckDB 1.5.6, sf 0.1. Interpretation exercise: almost all customers start in 1992 and retention hardly drops — unrealistic, because TPC-H generates orders uniformly. Real cohorts usually show a strong drop after the first period. Cohort analysis is a core method in e-commerce, subscriptions and SaaS.
:::

---

# Funnel Analysis

- A **funnel** follows users through the steps of a process: visit → product view → cart → checkout → purchase
- Key figures: number of users per step and **conversion rate** from step to step
- In SQL: count distinct users per step (conditional aggregation), then compare with `lag()`

::: callout
The biggest drop between two steps shows where to look first — but the funnel tells you **where** users leave, not **why**.
:::

::: source
Based on Tanimura (2021).
:::

::: notes
TPC-H has no event data, so the lab uses a tiny generated event table for funnels (see lab task 5). The "why" question leads to experiments (session 9): A/B tests check whether a change at the leaking step actually helps.
:::

---

# Lab: Analytical SQL {.section}

Star schema from session 3

---

# Lab Tasks {.exercise}

Work in pairs. Write queries and a short interpretation in your notebook.

1. **Ranking:** the top 3 **customers** per **market segment** by revenue in 1997
2. **Share:** each region's share of total revenue per year (window `sum() OVER (PARTITION BY year)`)
3. **Comparison:** monthly revenue 1997 vs. the same month in 1996 (`lag(…, 12)` or a self-join)
4. **Subtotals:** revenue by region and segment with all subtotals (`CUBE`); mark subtotal rows with `grouping()`
5. **Funnel:** create the small event table from the course notebook and compute conversion per step
6. **Interpret:** which result would you show to management, and with which warning?

::: notes
Hints: 2 — sum(revenue) / sum(sum(revenue)) OVER (PARTITION BY year) after GROUP BY region, year; shares are close to 20 % each (uniform synthetic data). 3 — monthly CTE with year and month, lag(rev, 12) OVER (ORDER BY year, month), and filter on 1997 only in an outer query: a WHERE year = 1997 in the same query runs before the window function, so lag() would return only NULLs (a classic mistake worth showing). Watch out for missing months. Tested: January 1997 257.2 million vs. 258.5 million in January 1996. 4 — 36 rows for 1997.
Funnel event table for task 5 (paste into the notebook):
CREATE TABLE events AS SELECT * FROM (VALUES (1,'visit'),(1,'view'),(1,'cart'),(1,'purchase'),(2,'visit'),(2,'view'),(3,'visit'),(3,'view'),(3,'cart'),(4,'visit'),(5,'visit'),(5,'view'),(5,'cart'),(5,'purchase')) t(user_id, step);
Expected: visit 5, view 4, cart 3, purchase 2 users. Task 6: e.g. TPC-H is synthetic and 1998 is incomplete — never report trends without checking completeness. This lab is part of portfolio notebook 1.
:::

---

# Key Takeaways

- **CTEs** make multi-step analytical queries readable and testable
- **Window functions** compute rankings, running totals, shares and period comparisons without collapsing rows
- **ROLLUP**, **CUBE** and **GROUPING SETS** produce subtotals and grand totals in one query
- **Cohorts** show retention over time; **funnels** show where users drop out of a process
- Always check **completeness and meaning** of the data before interpreting a result

---

# Next Session: Data Visualisation

- Choosing the right chart for the question
- Perception and visual encoding
- Misleading charts — and how to spot them
- Storytelling with data and KPI design

::: callout
**Preparation:** bring one chart from your company or the news that you find good — or misleading.
:::

---

# References {.references}

- DuckDB Foundation. (n.d.). *Window functions*. DuckDB documentation. Retrieved October 9, 2026, from https://duckdb.org/docs/sql/functions/window_functions
- Gray, J., Chaudhuri, S., Bosworth, A., Layman, A., Reichart, D., Venkatrao, M., Pellow, F., & Pirahesh, H. (1997). Data cube: A relational aggregation operator generalizing group-by, cross-tab, and sub-totals. *Data Mining and Knowledge Discovery, 1*(1), 29–53. https://doi.org/10.1023/A:1009726021843
- Tanimura, C. (2021). *SQL for data analysis: Advanced techniques for transforming data into insights*. O'Reilly Media.
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 9, 2026, from https://www.tpc.org/tpch/
