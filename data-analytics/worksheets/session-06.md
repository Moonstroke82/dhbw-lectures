---
course: Data Analytics
session: 6
title: Analytics Portals
subtitle: Practice tasks on portal layers, self-service BI, dashboard design, a mini semantic layer, Streamlit and access control
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

This worksheet lets you practise the concepts of session 6 on your own or in the lab. Tasks 1–3 need only paper and pencil. Tasks 4–6 use Python with DuckDB and Streamlit and the star schema from session 3 in `tpch.duckdb` (`fact_sales`, `dim_customer`, `dim_date`), built from the TPC-H data (Transaction Processing Performance Council, n.d.). Tasks 5 and 6 start from the starter app on the slides "Starter App (1/2)" and "Starter App (2/2)": save it as `app.py` next to `tpch.duckdb` and run it with `streamlit run app.py`. Remember to close any notebook connection to `tpch.duckdb` (`con.close()`) before you start the app. Task 7 is a dashboard task in the style of the group case study.

## Layers of a Portal

A regional public transport company builds an analytics portal. Assign each element to a layer — **sources, data, semantic layer, analytics services, access** — or to the **cross-cutting** concerns (security, governance, metadata, monitoring). Give a one-line reason.

1. Ticket sales from the vending machines and the mobile app
2. A definition "punctuality = share of departures less than 3 minutes late", used by all reports
3. A dashboard of today's delays per line for the control centre
4. A star schema with a fact table of departures and dimensions line, stop, date and time
5. A delay widget inside the company's passenger app
6. A log of who opened which report
7. A hierarchy line → route → network
8. A forecast of passenger numbers for next week, shown as a chart in the portal

::: answer lines=8
:::

::: solution
1. **Sources** — operational systems that produce the data.
2. **Semantic layer** — a metric defined once in business terms (alternatively: governance, because the definition is also a documented KPI; accept with reason).
3. **Analytics services** (dashboard), delivered through the access layer; an operational dashboard in the sense of Few (2013).
4. **Data** — the dimensional model in the warehouse or data mart.
5. **Access** — embedded analytics in another application (Microsoft, n.d.-a).
6. **Cross-cutting** — monitoring/governance (usage and access logging).
7. **Semantic layer** — hierarchies for drill-down and roll-up are defined there (the underlying attributes live in the line dimension of the data layer; accept "data" if the student says so).
8. **Analytics services** — ML results are content of the portal like reports and dashboards.

Marking: one point per correct assignment with a sensible reason; accept justified alternatives as noted. Layers as on the session slide (own illustration based on Chaudhuri et al., 2011, and Baars & Kemper, 2021).
:::

## Self-Service Levels and Guard Rails

In a hospital group, the following people work with data. For each person, name the **self-service level** after Alpar and Schulz (2016), one **risk**, and one **guard rail** that limits it.

1. A ward manager opens the bed-occupancy report and filters it by her ward and week.
2. A controller builds a new report of overtime per department from the certified HR data model.
3. A physician loads a CSV export from a medical device and joins it with patient admissions in a BI tool.
4. A quality manager copies the monthly infection report into a spreadsheet, adds his own corrections and e-mails it to the board.

::: answer lines=10
:::

::: hint
The three levels differ in what the user creates: nothing new (only filters), new analyses on prepared data, or new data sources.
:::

::: solution
1. **Usage of information.** Risk: low — at most misreading a filtered view (e.g. a partial week). Guard rail: visible filters and data freshness on the report; row-level security so she sees only her wards if required.
2. **Creation of information.** Risk: wrong aggregation or a new "overtime" definition that competes with HR's. Guard rail: metrics taken from the semantic layer, review before the report is shared or certified.
3. **Creation of information resources.** Risks: data quality of the export, wrong join keys, and above all **data protection** (health data are a special category of personal data). Guard rails: a sandbox for personal analysis, approval by data protection and the data owner before sharing, pseudonymised data, training.
4. Technically level 1 or 2 inside the tool, but the **manual correction outside** the governed portal creates a shadow version of the truth ("spreadmart"). Risk: the board sees numbers that nobody can trace and that differ from the portal. Guard rail: corrections go back to the source or the data owner; the board report is published from the certified data set, with a named owner.

Based on Alpar and Schulz (2016) and Passlick et al. (2023). Award points for level (1), risk (1) and guard rail (1) per person; for person 4, credit any answer that identifies the uncontrolled copy as the main problem.
:::

## Critique a Dashboard Design

An energy supplier specifies a dashboard for its **network control room**:

- 14 tiles in two columns; users scroll to see the lower half
- Each tile shows a gauge with the current value of one measure, e.g. "load North: 412 MW"
- Every tile has its own colour scheme; red and green mark "bad" and "good"
- Data are refreshed once a day at 6 a.m.
- The title is "Network Dashboard"; there is no information on data age

1. Which **role** (strategic, analytical, operational) should this dashboard play? What follows for its update frequency?
2. Name **at least five** design problems, using the terms from the session.
3. Sketch an improved layout in words: what goes where, and with which displays?

::: answer lines=12
:::

::: solution
1. **Operational**: a control room monitors processes that change quickly. It needs near real-time data (minutes, not a daily load) and alerts; a daily refresh makes it useless for its purpose (Few, 2013).
2. Problems (any five): exceeds **one screen** (scrolling loses the overview) · **no context** — "412 MW" without capacity, threshold or normal range · **gauges** use much space for one number and encode by angle (session 5) · **inconsistent displays** — a different colour scheme per tile · **red/green only** is a problem for colour vision deficiency · **no data freshness** shown, so users cannot know the data are up to 24 hours old · topic title instead of a message or purpose · all 14 measures equally prominent, nothing **highlighted**.
3. Example: top row — status line with data time stamp and active alerts; main area — one small-multiple line chart per network region with load over the last 24 hours, a shaded band for capacity and a marked threshold; values outside the band highlighted with one accent colour plus an icon or label (not only colour); right column — sorted list of the regions closest to capacity; details (individual stations) on click, not on the overview. Everything fits one screen.
:::

## A Mini Semantic Layer

The sales, finance and logistics teams of the TPC-H wholesaler each report "revenue 1997":

- Finance: gross order value incl. tax, `sum(o_totalprice)` of orders placed in 1997
- Sales: net revenue `sum(revenue)` in `fact_sales` by **order** date (the star schema)
- Logistics: net revenue `sum(l_extendedprice * (1 - l_discount))` of line items **shipped** in 1997

1. Compute the three numbers in DuckDB.
2. Compute the number of **active customers** (customers with at least one sale) for 1996, for 1997, and for 1996 and 1997 together. What does the result mean for a BI tool that sums this measure?
3. Build a mini semantic layer in Python: a dictionary of metrics (`net_revenue`, `quantity`, `active_customers`, `revenue_per_customer`), a dictionary of dimensions (`year`, `quarter`, `month`, `region`, `nation`, `segment`) and a function `metric_sql(metrics, by, where)` that returns the SQL and the parameter list. Use it to compute net revenue and revenue per active customer by region for 1997.

::: answer lines=12
:::

::: hint
The function only needs to join the strings: a SELECT list from the dimension and metric dictionaries, one fixed FROM clause with the joins, `WHERE dim = ?` conditions with a parameter list, and `GROUP BY ALL` if there are dimensions.
:::

::: solution
1. Results (DuckDB 1.5.5, sf 0.1), revenue 1997 in million: finance (gross, order date) **3,212.1** · sales (net, order date) **3,088.6** · logistics (net, ship date) **3,095.4**. Gross is about 4 % higher because it includes tax; ship date differs because orders placed at the end of 1996 are shipped in 1997 and orders from late 1997 in 1998. All three are legitimate — the semantic layer must give each a distinct name (e.g. `gross_order_value`, `net_revenue`, `net_revenue_shipped`) so that "revenue" is unambiguous.

```sql
SELECT sum(o_totalprice) FROM orders WHERE year(o_orderdate) = 1997;
SELECT sum(revenue) FROM fact_sales JOIN dim_date USING (date_key) WHERE year = 1997;
SELECT sum(l_extendedprice * (1 - l_discount)) FROM lineitem
WHERE year(l_shipdate) = 1997;
```

2. 1996: **8,641**; 1997: **8,640**; 1996 and 1997 together: **9,728** (not 17,281). Distinct counts are **non-additive** across the dimension in which the same customer can appear several times (here: time). A BI tool that sums the yearly values overstates the customers by 7,553. The semantic layer must store the formula `count(DISTINCT customer_key)` and compute it at the requested grain. (Across regions it happens to be additive, because each customer belongs to exactly one region: 1,715 + 1,712 + 1,720 + 1,735 + 1,758 = 8,640.)

3. Example solution:

```python
METRICS = {
    "net_revenue": "sum(f.revenue)",
    "quantity": "sum(f.quantity)",
    "active_customers": "count(DISTINCT f.customer_key)",
    "revenue_per_customer": "sum(f.revenue) / count(DISTINCT f.customer_key)",
}
DIMENSIONS = {"year": "d.year", "quarter": "d.quarter", "month": "d.month",
              "region": "c.region", "nation": "c.nation", "segment": "c.segment"}
JOINS = """FROM fact_sales f
JOIN dim_customer c USING (customer_key)
JOIN dim_date d USING (date_key)"""

def metric_sql(metrics, by=(), where=None):
    cols = [f"{DIMENSIONS[b]} AS {b}" for b in by]
    cols += [f"{METRICS[m]} AS {m}" for m in metrics]
    sql, params = f"SELECT {', '.join(cols)}\n{JOINS}", []
    if where:
        sql += "\nWHERE " + " AND ".join(f"{DIMENSIONS[k]} = ?" for k in where)
        params = list(where.values())
    if by:
        sql += "\nGROUP BY ALL ORDER BY ALL"
    return sql, params

sql, params = metric_sql(["net_revenue", "revenue_per_customer"],
                         by=["region"], where={"year": 1997})
con.execute(sql, params).df()
```

Result 1997 (net revenue in million; revenue per active customer): Africa 602.4; 351,260 · America 626.2; 365,786 · Asia 604.3; 351,364 · Europe 615.2; 354,566 · Middle East 640.4; 364,286. Total: 3,088.6 million and 357,473 per active customer (8,640 customers). Dividing by all 15,000 customers instead would give 205,905 — a further definition that must be fixed in the layer.

Marking: the function must only accept names from the dictionaries (this is what makes the layer governed: users cannot write their own formula) and must use `?` parameters for filter values. Ratios must be computed from sums and counts at the requested grain, never by averaging precomputed ratios. Compare with the idea of business objects that generate SQL (Cambot & Liautaud, 1996) and with central metric definitions in tools such as the dbt Semantic Layer (dbt Labs, n.d.).
:::

## Extend the Starter App

Extend the starter app from the session:

1. Add a **multiselect** in the sidebar for the market segments (default: all five). All queries must respect it. If no segment is selected, show a warning and stop the script.
2. Add a third KPI tile **revenue per active customer**.
3. Add a horizontal bar chart of the **top 5 nations** of the selected region, year and segments, sorted by revenue.
4. Check your app: what does it show for **Asia, 1997, segments Building and Machinery**?
5. Explain what happens when the user changes the segment selection: which code runs again, and which results come from the cache?

::: answer lines=12
:::

::: hint
A Python list can be passed as one parameter: `list_contains(?, segment)` is true if the segment is in the list. `st.stop()` ends the current run of the script.
:::

::: solution
Changes to the starter app (tested with Streamlit 1.66 and DuckDB 1.5.5, also with Streamlit's `AppTest`):

```python
segments = query("SELECT DISTINCT segment FROM dim_customer ORDER BY segment")
segments = segments["segment"].tolist()
chosen = st.sidebar.multiselect("Segments", segments, default=segments)
if not chosen:
    st.warning("Select at least one segment.")
    st.stop()

FILTER = "WHERE region = ? AND list_contains(?, segment)"
kpi = query(f"""SELECT year, sum(revenue) / 1e6 AS revenue_m,
                       count(DISTINCT customer_key) AS customers
                {BASE} {FILTER} AND year IN (?, ?)
                GROUP BY year ORDER BY year""", (region, chosen, year - 1, year))
prev, cur = kpi.iloc[0], kpi.iloc[1]
c1, c2, c3 = st.columns(3)
c1.metric("Revenue (million)", f"{cur.revenue_m:,.1f}",
          f"{cur.revenue_m / prev.revenue_m - 1:+.1%} vs. {year - 1}")
c2.metric("Active customers", f"{int(cur.customers):,}")
c3.metric("Revenue per active customer",
          f"{cur.revenue_m * 1e6 / cur.customers:,.0f}")

nations = query(f"""SELECT nation, sum(revenue) / 1e6 AS revenue_m
                    {BASE} {FILTER} AND year = ?
                    GROUP BY nation ORDER BY revenue_m DESC LIMIT 5""",
                (region, chosen, year))
st.subheader(f"Top nations {year}")
st.bar_chart(nations, x="nation", y="revenue_m", horizontal=True,
             sort="-revenue_m")
```

The monthly chart from the starter app gets the same `FILTER`. Accept `segment IN (...)` built from placeholders (`", ".join("?" * len(chosen))`) as an alternative; do **not** accept segment names pasted into the SQL string.

4. Asia, 1997, Building and Machinery: revenue **247.5** million, **−2.5 %** vs. 1996 (253.7 million), **703** active customers, **351,996** revenue per active customer. Top nations: Indonesia 56.6, India 54.6, Vietnam 47.0, China 45.3, Japan 43.9 million (Asia has exactly five nations, so the "top 5" shows all of them — a good moment to check whether a top-N chart makes sense for the selected region).

5. Every widget change **reruns the whole script from top to bottom**. `get_con()` returns the cached connection (`st.cache_resource`). `query()` is called again, but the calls whose SQL and parameters are unchanged (the region and segment lists) come from the `st.cache_data` cache; the KPI, monthly and nation queries have new parameters, so DuckDB runs them and their results are cached for one hour (`ttl=3600`). Because cached results are shared by all users, a second user with the same selection gets them immediately (Streamlit, n.d.-a).
:::

## Who Sees Which Region?

The wholesaler wants regional sales managers to use the dashboard: Lena may see only Europe, Omar only Asia and the Middle East, the controller all regions.

1. Add a dictionary `USERS` that maps each user to the allowed regions, and a demo user selector in the sidebar. The region selector may offer only the allowed regions. Make sure the queries cannot return other regions even if the selector code changes later.
2. Which revenue 1997 does Omar see for each of his regions, and what would a tile "revenue of my regions" show?
3. In a real deployment, the demo selector is replaced by `st.login()` with the company's identity provider. Why does that alone not solve the problem?
4. A colleague proposes a tile "Your share of total company revenue". Why is this a problem for Lena?
5. Compare your solution with row-level security in a BI platform such as Power BI. What is different?

::: answer lines=12
:::

::: solution
1. Example:

```python
USERS = {"lena": ["EUROPE"], "omar": ["ASIA", "MIDDLE EAST"],
         "controller": ["AFRICA", "AMERICA", "ASIA", "EUROPE", "MIDDLE EAST"]}
user = st.sidebar.selectbox("User (demo login)", list(USERS))
allowed = USERS[user]
region = st.sidebar.selectbox("Region", allowed)
if region not in allowed:      # enforce, do not only hide
    st.stop()
```

Better still: enforce it in the data access itself, e.g. a function `secure_query(sql, params, allowed)` that always adds `AND list_contains(?, region)` with the user's allowed regions, so that every chart, table and download is filtered — also ones added later.

2. Omar: Asia **604.3** million, Middle East **640.4** million; "my regions" **1,244.8** million (computed from the unrounded values). Lena sees only Europe: 615.2 million.
3. `st.login()` (OpenID Connect) only **authenticates** — it tells the app who the user is. **Authorisation** — what this user may see — must still be implemented by the app, e.g. by mapping `st.user.email` to allowed regions (Streamlit, n.d.-b). The mapping itself must be maintained and owned (governance).
4. The share reveals data she is not allowed to see: from Europe's revenue (615.2 million) and the share (19.9 %) she can compute the company total (3,088.6 million) and thus the revenue of all other regions combined. Aggregates over restricted data are also restricted data.
5. In a BI platform, roles with filter expressions (e.g. `[Region] = "EUROPE"`) are defined once in the **semantic model**, members are assigned in the service, and every report on the model is filtered automatically; dynamic rules can use the user's login name (Microsoft, n.d.-b). The Streamlit solution is application code that each developer must apply correctly. Common to both: rules must be tested ("view as role"), and in Power BI they do not restrict workspace admins, members and contributors who can edit the model — so the authors' access must be controlled too.
:::

## Portfolio-Style Task: A Dashboard for One Stakeholder

Build a small Streamlit dashboard on the TPC-H warehouse for **one** stakeholder of the wholesaler (e.g. the head of logistics, a regional sales manager or the CFO). Submit `app.py`, a short `README.md` and one page of design notes with:

- the stakeholder, their decision and **three questions** the dashboard answers,
- the **role** of the dashboard (strategic, analytical or operational),
- **definitions** of all metrics used, kept in one place in the code (a mini semantic layer),
- 3–5 tiles or charts on one screen, with context (previous period or target) and data freshness,
- an **access rule**: who may see which data, and where in the code it is enforced,
- caching and run instructions.

::: answer lines=10
:::

::: solution
Marking guide (20 points):

- **Stakeholder and questions** (3 points): a concrete person and decision; three questions that the tiles actually answer. Generic "overview of everything" scores at most 1.
- **Dashboard role and fit** (2 points): role named and consistent with the design (e.g. strategic → few KPIs with comparisons; analytical → filters and drill-down).
- **Metric definitions** (4 points): all metrics defined once (dictionary, SQL views or a module), with clear names for variants (e.g. net vs. gross, order vs. ship date); non-additive metrics computed correctly (distinct counts, ratios from sums); complete periods only or partial periods marked.
- **Design** (4 points): fits one screen; every number has context; chart choice and honest axes as in session 5; one accent colour; action titles or captions; data freshness shown (orders end on 1998-08-02).
- **Access and governance** (3 points): rule stated and enforced in the query function, not only in a widget; owner of the dashboard named; no leakage through totals or shares.
- **Technical quality** (3 points): app runs with `streamlit run app.py` on a fresh `tpch.duckdb`; read-only connection cached with `st.cache_resource`; queries cached with `st.cache_data`; `?` parameters instead of string concatenation; README explains setup.
- **Reflection** (1 point): one limitation (synthetic data, no real users, no real-time data) and one next step.

Typical good submissions: a logistics dashboard with on-time delivery rate by ship mode and month (worksheet 5, task 6: about 36.8 % overall) and a target line; a regional sales dashboard as in tasks 5 and 6 with row-level filtering; a CFO dashboard with year-to-date revenue vs. previous year (worksheet 5, task 5). The dashboard can be reused in the group case study.
:::

## References {.references}

- Alpar, P., & Schulz, M. (2016). Self-service business intelligence. *Business & Information Systems Engineering, 58*(2), 151–155. https://doi.org/10.1007/s12599-016-0424-6
- Baars, H., & Kemper, H.-G. (2021). *Business Intelligence & Analytics – Grundlagen und praktische Anwendungen: Ansätze der IT-basierten Entscheidungsunterstützung* (4th ed.). Springer Vieweg. https://doi.org/10.1007/978-3-8348-2344-1
- Cambot, J.-M., & Liautaud, B. (1996). *Relational database access system using semantically dynamic objects* (U.S. Patent No. 5,555,403). U.S. Patent and Trademark Office. https://patents.google.com/patent/US5555403
- Chaudhuri, S., Dayal, U., & Narasayya, V. (2011). An overview of business intelligence technology. *Communications of the ACM, 54*(8), 88–98. https://doi.org/10.1145/1978542.1978562
- dbt Labs. (n.d.). *dbt Semantic Layer*. Retrieved October 20, 2026, from https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl
- Few, S. (2013). *Information dashboard design: Displaying data for at-a-glance monitoring* (2nd ed.). Analytics Press.
- Microsoft. (n.d.-a). *What is Power BI embedded analytics?* Retrieved October 20, 2026, from https://learn.microsoft.com/en-us/power-bi/developer/embedded/embedded-analytics-power-bi
- Microsoft. (n.d.-b). *Row-level security (RLS) with Power BI*. Retrieved October 20, 2026, from https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security
- Passlick, J., Grützner, L., Schulz, M., & Breitner, M. H. (2023). Self-service business intelligence and analytics application scenarios: A taxonomy for differentiation. *Information Systems and e-Business Management, 21*(1), 159–191. https://doi.org/10.1007/s10257-022-00574-3
- Streamlit. (n.d.-a). *Caching overview*. Retrieved October 20, 2026, from https://docs.streamlit.io/develop/concepts/architecture/caching
- Streamlit. (n.d.-b). *User authentication and information*. Retrieved October 20, 2026, from https://docs.streamlit.io/develop/concepts/connections/authentication
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
