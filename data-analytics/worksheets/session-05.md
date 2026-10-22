---
course: Data Analytics
session: 5
title: Data Visualisation
subtitle: Practice tasks on chart choice, visual encoding, misleading charts, redesign in matplotlib, KPI definitions and data stories
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 5 on your own or in the lab. Tasks 1–3 need only paper and pencil. Tasks 4–6 use Jupyter with DuckDB, pandas and matplotlib and the star schema from session 3 in `tpch.duckdb` (`fact_sales`, `dim_customer`, `dim_date`), built from the TPC-H data (Transaction Processing Performance Council, n.d.). Start each notebook with:

```python
import duckdb
import matplotlib.pyplot as plt
con = duckdb.connect("tpch.duckdb")
```

Task 7 is a short data story in the style of the portfolio presentations.

## Which Chart for Which Question?

An HR department and an energy supplier want to visualise the following results. Choose a chart type, name the main visual channel it uses, and say what you would **avoid**.

1. Number of employees per department (12 departments, long names)
2. Daily electricity consumption of a city over three years
3. Distribution of employees' commuting distances
4. Share of renewable, gas and coal energy in this year's electricity mix
5. Relationship between training hours and performance rating of 400 employees
6. Sick days per department and month, for a works council that wants to look up exact figures

::: answer lines=8
:::

::: solution
1. **Horizontal bar chart, sorted** (position/length; long labels readable). Avoid: pie chart with 12 slices, vertical bars with rotated labels.
2. **Line chart** (position over time); possibly with a 7-day moving average to show the trend through weekly patterns. Avoid: bars for 1,000+ days, a truncated axis without a label.
3. **Histogram** or box plot (position/length of bins). Avoid: showing only the average — the distribution is probably skewed.
4. With three parts: a **100 % stacked bar** or a sorted bar chart of shares; a pie is acceptable for 2–3 clearly different parts. Avoid: 3D pie, donut with many decimals.
5. **Scatter plot** (position on two axes), with transparency if points overlap. Avoid: two lines on two y-axes, connecting the points with a line.
6. **Table**, optionally as a heatmap with a sequential colour scale (12 departments × 12 months). Avoid: 12 line charts with data labels.

Based on Knaflic (2015, Chapter 2) and the chart-choice table of the session. The channel answers should name position or length for 1–5 (Cleveland & McGill, 1984).
:::

## Critique the Encoding

For each chart, name the **mark** and the **channel** used for the most important attribute (Munzner, 2014), place the channel in the ranking of Cleveland and McGill (1984), and propose a more effective encoding.

1. A map of Germany where each federal state is coloured by its revenue, from light to dark blue.
2. A donut chart with 8 product categories whose shares are between 10 % and 15 %.
3. A bar chart of average delivery time per carrier, where each carrier has its own colour from a rainbow palette.
4. A line chart connecting the revenue of the market segments Automobile, Building, Furniture, Household and Machinery from left to right.

::: answer lines=10
:::

::: solution
1. Mark: area (state shape); channel: **colour lightness/saturation** — the lowest rank. Large states dominate visually regardless of revenue. Better: sorted bar chart or dot plot of revenue per state (position); keep the map only if the geographical pattern is the message.
2. Mark: arc segments; channel: **angle and area** — middle to low rank. Eight similar shares cannot be compared. Better: sorted horizontal bar chart (position on a common scale), labels with the share.
3. Mark: bars; channels: **length** (good) plus **hue** for the carrier. The hue adds no information because the carrier is already on the axis, and a rainbow palette distracts (and is hard to read with colour vision deficiency). Better: one neutral colour, sorted bars, one accent colour for the carrier that matters (e.g. the slowest, or our own).
4. Mark: line; channel: **position**, but the line violates **expressiveness**: a line suggests an order or continuity between the categories, which segments do not have. Better: bar or dot chart of the five segments, sorted by revenue.
:::

## Measure the Distortion

Tufte (2001) defines the **lie factor** as the size of the effect shown in the graphic divided by the size of the effect in the data, where the size of an effect is the relative change (second value / first value − 1).

1. A bar chart compares the number of customer complaints: 50 last year, 55 this year. The y-axis starts at 48. Compute the lie factor.
2. A news chart shows the budget of two cities with circles: 2 billion and 4 billion euros. The designer doubled the **diameter** of the second circle. What effect does a reader see if they read the area, and what is the lie factor?
3. Under which conditions is a y-axis that does not start at zero **acceptable**?

::: answer lines=8
:::

::: hint
In task 1, the effect in the graphic is the ratio of the visible bar heights above the axis start, minus 1.
:::

::: solution
1. Data effect: 55 / 50 − 1 = 0.10 (10 %). Visible heights: 55 − 48 = 7 and 50 − 48 = 2, graphic effect 7 / 2 − 1 = 2.5 (250 %). Lie factor = 2.5 / 0.10 = **25**. Tufte considers values between about 0.95 and 1.05 acceptable; 25 is a severe distortion.
2. Doubling the diameter quadruples the area: area ratio 4, so the graphic effect is 4 − 1 = 3 (300 %); data effect 4 / 2 − 1 = 1 (100 %). Lie factor = **3**. Fix: scale the area (diameter × √2), or better use bars.
3. For **line charts and dot plots**, where the reader judges position and change, not length: a narrower range is acceptable and often necessary (e.g. body temperature, exchange rates), as long as the axis is clearly labelled. For **bar charts**, the axis must start at zero because the reader compares lengths (Knaflic, 2015).
:::

## Redesign a Bad Chart

A colleague produced this chart of revenue 1997 per nation:

```python
import numpy as np
df = con.sql("""
  SELECT nation, sum(revenue) AS revenue
  FROM fact_sales JOIN dim_customer USING (customer_key)
                  JOIN dim_date USING (date_key)
  WHERE year = 1997 GROUP BY nation
""").df()
plt.figure(figsize=(8, 8))
plt.pie(df["revenue"], labels=df["nation"], shadow=True, explode=[0.05] * 25,
        colors=plt.cm.rainbow(np.linspace(0, 1, 25)))
plt.title("NATION REVENUE")
plt.show()
```

1. Run it and list **at least four** problems, using the terms from the session.
2. Redesign the chart in matplotlib so that the **highest and lowest nations** and the spread between them are visible at a glance. Use an **action title**.
3. Is the spread between nations large or small? Give the numbers.

::: answer lines=10
:::

::: solution
1. Problems: 25 slices of nearly equal angle (angle and area are read inaccurately; all shares are 3.7–4.6 %); a rainbow palette for categories (25 hues cannot be distinguished, no meaning, problematic for colour vision deficiency); shadow and exploded slices (chartjunk, lower data-ink ratio); unsorted order; no values or units; the title states the topic, not the message; the query has no `ORDER BY`, so the order is arbitrary.
2. Example redesign:

```python
df = df.sort_values("revenue")
df["revenue_m"] = df["revenue"] / 1e6
colours = ["#B8C0C5"] * len(df)
colours[0] = colours[-1] = "#E2001A"          # lowest and highest nation
fig, ax = plt.subplots(figsize=(8, 7))
ax.barh(df["nation"], df["revenue_m"], color=colours)
ax.axvline(df["revenue_m"].mean(), color="#5C6971", linewidth=1, linestyle="--")
ax.set_xlabel("Revenue 1997 (million)")
ax.set_title("All 25 nations generate between 113 and 141 million revenue",
             loc="left")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
```

Accept other good designs, e.g. a dot plot starting near the minimum (position, so a non-zero axis is allowed if labelled), or bars of the deviation from the average.

3. Small: Iran 140.9 million (4.56 %) is highest, Saudi Arabia 112.8 million (3.65 %) lowest — a spread of about 28 million or 25 % between the extremes, while most nations lie between about 116 and 132 million. The pie hides even this ranking; the sorted bar chart shows it immediately.
:::

## An Honest Comparison Over Time

Management asks: "How is 1998 going compared with previous years?"

1. Compute net revenue per year 1992–1998 and plot it as a bar chart. Why is this chart misleading?
2. Compute **year-to-date** revenue (January to July) for 1996, 1997 and 1998, and the growth of 1998 vs. 1997.
3. Plot monthly revenue for January to July of 1997 and 1998 as a line chart with two lines. Give it an action title that the data supports.

::: answer lines=10
:::

::: solution
1. Revenue per year (million): 1992 3,124.6 · 1993 3,063.8 · 1994 3,150.7 · 1995 3,144.2 · 1996 3,103.8 · 1997 3,088.6 · **1998 1,859.3**. Orders end on 1998-08-02, so 1998 contains seven months and two days: the bar suggests a collapse that does not exist (incomplete period, as on the session slide).
2. Year-to-date January–July:

```sql
SELECT year, sum(revenue) / 1e6 AS ytd_m
FROM fact_sales JOIN dim_date USING (date_key)
WHERE month <= 7 AND year >= 1996
GROUP BY year ORDER BY year;
```

1996 1,797.2 · 1997 1,817.1 · 1998 1,841.6 million → 1998 vs. 1997: **+1.3 %** (1997 vs. 1996: +1.1 %).

3. Monthly 1998 (Jan–Jul): 269.3, 238.2, 267.6, 271.3, 271.2, 250.8, 273.1; 1997: 257.2, 246.4, 256.3, 254.7, 264.5, 267.4, 270.5 million. Code sketch: query year, month, sum(revenue) for `month <= 7 AND year IN (1997, 1998)`, then `df.pivot(index="month", columns="year", values="rev_m").plot(ax=ax)`. Honest title, e.g.: "1998 is on track: revenue January–July is 1.3 % above 1997". Not acceptable: "Revenue falls in 1998" or a title that interprets single-month differences (February 1998 is lower, June 1998 is lower) as a trend. Both lines should share one y-axis; a narrower y-range is acceptable for a line chart if labelled.
:::

## Define and Compute a KPI

The wholesaler wants a KPI for delivery reliability: **on-time delivery rate**, the share of line items received by the committed date (`l_receiptdate <= l_commitdate`).

1. Fill in a KPI definition sheet: formula, source and grain, time reference, filters, comparison, owner and frequency, and whether it is a leading or lagging indicator.
2. Compute the KPI overall, per ship mode for orders from 1997, and per year — once by **order year** and once by **ship year**.
3. What do you notice? Which time reference would you choose, and what target would you propose?

::: answer lines=12
:::

::: solution
1. Example definition sheet (Parmenter, 2015; KPI design slide):

| Field | Example |
|---|---|
| Formula | count of line items with `l_receiptdate <= l_commitdate` / count of line items, in % |
| Source and grain | `lineitem` (with `orders` for the order date), one row per order line |
| Time reference | Ship date (the period in which logistics delivers) — or order date, but stated |
| Filters | Only line items already received at the reporting date; complete periods only |
| Comparison | Previous period, same period last year, target |
| Owner, frequency | Head of logistics; weekly or monthly |
| Type | Lagging for logistics performance; leading for customer satisfaction and churn |

Alternative unit: per order (an order is on time only if all lines are) — must be decided and written down.

2. Expected results (DuckDB 1.5, sf 0.1):
   - Overall: **36.8 %** (`SELECT avg(CASE WHEN l_receiptdate <= l_commitdate THEN 1 ELSE 0 END) FROM lineitem`).
   - Per ship mode, orders 1997: between 36.0 % (RAIL) and 37.0 % (AIR, MAIL).
   - By order year: 36.4–37.1 % in every year (1992–1998).
   - By ship year: 1992 40.8 %, 1993–1997 36.6–37.2 %, 1998 32.1 %.
3. The KPI is very low (about two thirds of line items arrive late) and flat across years and ship modes — characteristic of synthetic data, but in a real company it would call for action. The time reference changes the result at the edges: by ship year, 1992 and 1998 differ because the first and last years of the data contain a selected mix of line items (1992: only items from the first orders; 1998: many items from orders placed months earlier, with longer average delays). Always check edge periods before reporting a KPI trend. Recommendation: report by ship or receipt period, but only for completed periods. A target should be based on the business need and a benchmark, not set arbitrarily, e.g. raise the rate step by step towards a contractual service level; a good answer explains how the target was derived.
:::

## Portfolio-Style Task: A One-Slide Data Story

Create **one slide** (or one notebook cell with a chart and text) that answers a question for the management of the TPC-H wholesaler, using one result from sessions 2–5. It must contain:

- an **action title** that states the finding in one sentence,
- **one** chart designed with the principles of the session (chart choice, one accent colour, no clutter, honest axes),
- three sentences: context, finding, recommendation or next step,
- one line on data limitations.

::: answer lines=12
:::

::: solution
Marking guide (10 points):

- **Action title** (2 points): a full sentence with a finding, consistent with the data (e.g. "Revenue is stable across regions and years — the 1998 dip is an artefact of incomplete data"). Topic-only titles ("Revenue by region") score 0.
- **Chart choice** (2 points): fits the question (comparison → bars, time → line, share → stacked bar, concentration → cumulative line or sorted bars).
- **Design** (2 points): sorted where meaningful, units and labels, one accent colour on the message, no 3D, no unnecessary legend or gridlines.
- **Honesty** (2 points): zero baseline for bars, complete periods or marked partial periods, no dual axis, correct denominator.
- **Story and limitation** (2 points): context, finding and recommendation are connected (beginning, middle, end — Knaflic, 2015); the limitation names something real (synthetic data, incomplete 1998, revenue definition incl. returns).

Typical good submissions: the honest year comparison (task 5), the nation spread (task 4), revenue concentration (worksheet 4), on-time delivery (task 6) with a recommendation to set a target.
:::

## References {.references}

- Cleveland, W. S., & McGill, R. (1984). Graphical perception: Theory, experimentation, and application to the development of graphical methods. *Journal of the American Statistical Association, 79*(387), 531–554.
- Knaflic, C. N. (2015). *Storytelling with data: A data visualization guide for business professionals*. Wiley.
- Munzner, T. (2014). *Visualization analysis and design*. CRC Press.
- Parmenter, D. (2015). *Key performance indicators: Developing, implementing, and using winning KPIs* (3rd ed.). Wiley.
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
- Tufte, E. R. (2001). *The visual display of quantitative information* (2nd ed.). Graphics Press.
