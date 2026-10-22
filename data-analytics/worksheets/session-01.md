---
course: Data Analytics
session: 1
title: Introduction to Data Analytics
subtitle: Practice tasks on the development of analytics, the four types of analytics, use-case questions and a first DuckDB query
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 1 on your own or with your project team: how data analysis developed, the four types of analytics, and how to question a use case before any data is touched. Tasks 1–4 need only paper and pencil. Task 5 needs the tool setup from the end of the session 1 slides (Python, Jupyter and DuckDB). Task 6 is a short written assessment in the style of the portfolio notebooks.

## Which Type of Analytics?

Classify each example as **descriptive**, **diagnostic**, **predictive** or **prescriptive** (Delen & Ram, 2018). If an example could be two types, name both and say what would decide it.

| # | Example | Type |
|---|---|---|
| 1 | A hospital dashboard shows the bed occupancy per ward for the last 30 days. | |
| 2 | A public transport operator estimates the number of passengers per line for next Monday. | |
| 3 | An energy supplier analyses why customer complaints doubled in one postcode area. | |
| 4 | An airline system sets ticket prices for each flight to maximise expected revenue. | |
| 5 | A bank flags card transactions that are likely to be fraudulent. | |
| 6 | A retailer compares this year's Christmas sales with last year's, per store. | |
| 7 | A logistics company plans the routes of its delivery vans for tomorrow. | |
| 8 | A streaming service finds that users who cancel watched fewer series in their last month. | |

::: hint
Ask which question the example answers: *What happened? Why did it happen? What will happen? What should we do?* An optimisation or a decision proposal is prescriptive; it usually builds on a prediction.
:::

::: solution
1. **Descriptive**: a report of what happened (occupancy in the past).
2. **Predictive**: a forecast of future demand.
3. **Diagnostic**: looks for the cause of a known change (root-cause analysis, drill-down by postcode, complaint reason, date).
4. **Prescriptive**: dynamic pricing chooses an action (the price) by optimising expected revenue; it builds on predicted demand.
5. **Predictive**: a fraud score estimates the probability that a transaction is fraudulent (a classification). If the system also blocks the card automatically, the decision part is prescriptive; accept "predictive, prescriptive if it acts".
6. **Descriptive**: comparison of past figures; becomes diagnostic only if the analysis asks why stores differ.
7. **Prescriptive**: route optimisation decides what to do.
8. **Diagnostic**: explains cancellations by a pattern in past behaviour. If the finding is turned into a churn model that scores current users, it becomes predictive; accept "diagnostic" or "diagnostic, basis for predictive" with this reasoning.

Marking: one point per correct type; for 5 and 8 the reasoning counts more than the label.
:::

## Eras of Analytics

The session described the development of analytics with Chen et al. (2012) (BI&A 1.0, 2.0, 3.0) and with Davenport (2013) (Analytics 1.0, 2.0, 3.0).

1. Assign each data source to the BI&A stage in which it became important: (a) monthly sales from the ERP system, (b) product reviews on a web shop, (c) GPS positions of a delivery fleet, (d) customer master data from the CRM system, (e) clickstreams of a web shop, (f) vibration sensors in a production machine.
2. A mid-sized manufacturer produces monthly Excel reports from its ERP system. A data team of two people answers ad-hoc questions from management. In which of Davenport's eras is the company? Name **two** concrete steps that would move it towards Analytics 3.0.
3. Why does a later stage not **replace** the earlier one? Give one example from a company you know.

::: answer lines=10
:::

::: solution
1. BI&A 1.0 (structured data from internal systems): (a) ERP sales, (d) CRM master data. BI&A 2.0 (web data): (b) product reviews (text and opinion mining), (e) clickstreams. BI&A 3.0 (mobile and sensor data): (c) GPS positions, (f) machine sensors.
2. **Analytics 1.0**: internal, structured data, descriptive reports, analysts answering questions in the back office. Steps towards 3.0, any two with a concrete example: embed analytics into an operational process (e.g. a demand forecast that feeds production planning automatically); offer analytics as part of the product or service (e.g. machine condition monitoring for customers); make decisions at scale with models instead of single reports; build a data platform and a team that works with the business units rather than for them.
3. The new stages add data types and methods, but the basic needs remain: management still needs reliable figures from integrated internal data, so a data warehouse and reporting (1.0) stay the backbone. Example: a company with predictive maintenance on sensor data still closes its books with ERP-based reporting.
:::

## One Domain, Four Questions

A city runs a **bike-sharing system** with 300 stations and 3,000 bikes. For each type of analytics, write **one** business question the operator could ask, and name the **data** you would need to answer it.

| Type | Question | Data needed |
|---|---|---|
| Descriptive | | |
| Diagnostic | | |
| Predictive | | |
| Prescriptive | | |

::: solution
Example answers (accept any consistent set):

| Type | Question | Data needed |
|---|---|---|
| Descriptive | How many rentals were there per station and hour last month? | Rental records (start/end station, time) |
| Diagnostic | Why did rentals at the central station drop in September? | Rentals, weather, construction sites, bike availability, app outages |
| Predictive | How many bikes will be requested at each station tomorrow between 7 and 9 am? | Historical rentals per station and hour, calendar, weather forecast, events |
| Prescriptive | How should the service team redistribute bikes overnight? | Demand forecast, current bike positions, truck capacity, travel times |

Check that the four questions build on each other (the prescriptive question uses the prediction) and that the data is specific (not just "all data").
:::

## Questioning a Use Case

A **water utility** gives a short pitch: "We lose about a fifth of our drinking water through leaks in the pipe network. We have flow and pressure sensors in some districts, a maintenance database and the age and material of every pipe. We want to use AI to find leaks earlier."

Using the five question areas from the session (decision, success, data, constraints, stakeholders), write **two** precise questions per area that you would ask the utility before starting.

::: answer lines=12
:::

::: hint
Good questions can be answered with a fact or a number. "Do you have data?" is weak; "Since when are the pressure sensors installed, and at what interval do they record?" is strong.
:::

::: solution
Example questions (two per area; accept others of similar precision):

- **Decision:** What happens today when a leak is suspected — who decides to send a crew? Should the result rank districts for inspection, or raise alarms in real time?
- **Success:** How is water loss measured today, and by how much should it fall? How many false alarms per week can the maintenance team handle?
- **Data:** Which districts have sensors, since when, and at what time resolution? Are past leaks recorded with location, date found and repair date, so that they can serve as labels?
- **Constraints:** Can the data leave the utility's systems (critical infrastructure, security rules)? Which systems and tools must the solution fit into?
- **Stakeholders:** Who will use the result daily (control room, maintenance crews), and who sponsors the project? Who owns the sensor and maintenance data?

Marking: full marks if each area has two questions that are specific and answerable; deduct for vague questions or for areas left out. Note for students: the same questions apply to the semester-6 partner projects.
:::

## First Steps in DuckDB

An ice-cream shop recorded its monthly revenue (in thousand euros) for the first half of the year: January 120, February 95, March 130, April 150, May 170, June 160.

1. Run the test cell from the session to check your setup.
2. Complete the query below so that it returns the **total**, the **average**, the **best month** and the **growth from January to June** in per cent.

```python
import duckdb
duckdb.sql("""
SELECT sum(revenue) AS total,
       ...
FROM (VALUES (1, 'Jan', 120), (2, 'Feb', 95), (3, 'Mar', 130),
             (4, 'Apr', 150), (5, 'May', 170), (6, 'Jun', 160))
     AS t(m, month, revenue)
""").show()
```

3. Which type of analytics is your query? The owner wants to know how much ice cream to order for July. Why are these six numbers **not enough** for a good forecast?

::: hint
DuckDB has `arg_max(x, y)`, which returns the value of `x` in the row where `y` is largest, and `first(x ORDER BY …)` / `last(x ORDER BY …)`.
:::

::: answer lines=6
:::

::: solution
1. The test cell prints a table with one row, "setup works". If it fails, check the Python installation and `python -m pip install duckdb`.
2. Possible query (tested with DuckDB 1.5):

```sql
SELECT sum(revenue) AS total,
       avg(revenue) AS average,
       arg_max(month, revenue) AS best_month,
       round(100 * (last(revenue ORDER BY m) / first(revenue ORDER BY m) - 1), 1) AS growth_pct
FROM (VALUES ...) AS t(m, month, revenue)
```

Expected result: total 825, average 137.5, best month May (170), growth January to June 33.3 %. Alternatives such as a subquery with `ORDER BY revenue DESC LIMIT 1` are fine.

3. **Descriptive** analytics. Six months cannot separate **trend** from **seasonality**: ice cream sales rise towards summer every year, so the "growth" of 33 % is probably mostly seasonal. A forecast for July needs at least one previous year (ideally several), and possibly drivers such as weather and holidays. Link: time series forecasting, sessions 11–14.
:::

## Portfolio-Style Task: Is Analytics the Answer?

The portfolio notebooks end with a short written assessment of whether a method suits the use case. Practise this format.

A sales manager of a wholesaler asks the data team for "an AI model that predicts which customers will order next month", so that the sales team can call them. The company has 400 business customers; most of them order on fixed weekly or monthly schedules agreed in their contracts. Orders are stored in the ERP system.

Write a short assessment (about 150–200 words): Is a predictive model the right approach? What would you suggest instead or first? What would change your recommendation? (Background: the critical-perspective slide of session 1 and Provost & Fawcett, 2013.)

::: answer lines=12
:::

::: solution
Marking guide (10 points):

- **Understands the business situation** (2 points): 400 customers is a small population, and most orders follow contractual schedules, so future orders are largely **known**, not uncertain.
- **Recommends a simpler first step** (3 points): a descriptive report or list from the ERP system — customers whose next scheduled order is due, plus customers who deviate from their usual pattern (e.g. no order for longer than their usual interval). This is cheap, transparent and probably good enough. A rule-based baseline should come before any model.
- **Names conditions for a model** (2 points): a predictive model becomes worthwhile if many customers order irregularly, if the customer base is much larger, or if the goal changes to detecting churn risk early (a customer who reduces orders).
- **Mentions success measurement or usage** (2 points): e.g. how will we know the calls help (more orders, less churn)? Who acts on the list? The critical-perspective slide: analytics fails when nobody acts on the result.
- **Clarity and length** (1 point): coherent argument, within the word limit.

Sample answer: "A predictive model is not the right first step. With 400 customers and mostly contractual order schedules, the next orders are largely known. A simple ERP report that lists customers whose next order is due, and customers whose last order is overdue compared with their usual interval, answers the manager's need transparently and within days. If the analysis shows that a large share of customers orders irregularly, or if the goal shifts to spotting customers who are about to leave, a churn model on order history becomes worthwhile; it must then beat the simple rule as a baseline. In both cases we should agree how the sales team uses the list and measure whether the calls lead to more orders."
:::

## Optional Challenge: Find a Public Dataset {.optional}

The group case study uses a public dataset. Find **one** public dataset on a portal such as the EU or German open data portals, Kaggle, or the UCI Machine Learning Repository that interests you. Note: name and source, size (rows, columns, time span), which of the four types of analytics it supports, and one question you could answer with it.

::: answer lines=6
:::

::: solution
Any dataset with a correct description is acceptable. Check that: the source is a real, public URL; the size is stated; the analytics types are plausible (e.g. a dataset without a time dimension cannot support a time series forecast; a dataset without an outcome variable cannot support supervised prediction); the question is answerable with the columns described. Good candidates for the case study have a time dimension and several thousand rows or more.
:::

## References {.references}

- Chen, H., Chiang, R. H. L., & Storey, V. C. (2012). Business intelligence and analytics: From big data to big impact. *MIS Quarterly, 36*(4), 1165–1188. https://doi.org/10.2307/41703503
- Davenport, T. H. (2013). Analytics 3.0. *Harvard Business Review, 91*(12), 64–72.
- Delen, D., & Ram, S. (2018). Research challenges and opportunities in business analytics. *Journal of Business Analytics, 1*(1), 2–12. https://doi.org/10.1080/2573234X.2018.1507324
- Provost, F., & Fawcett, T. (2013). Data science and its relationship to big data and data-driven decision making. *Big Data, 1*(1), 51–59. https://doi.org/10.1089/big.2013.1508
