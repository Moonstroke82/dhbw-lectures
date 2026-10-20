---
course: Data Analytics
session: 6
title: Analytics Portals
subtitle: BI tools · semantic layer · self-service BI · dashboards · embedded analytics · access and governance
program: DHBW Mannheim · Data Science and Artificial Intelligence · Semester 5
---

# Analytics Portals {.title}

::: notes
Time plan for today (3 h): recap 10 min · portals and BI tools 15 min · semantic layer and self-service BI 25 min · exercise 10 min · break 10 min · dashboards and embedded analytics 15 min · access and governance 10 min · lab 80 min · wrap-up 5 min · ~10 min buffer.
Students need tpch.duckdb with the star schema from session 3, their charts from session 5, and Streamlit (`pip install streamlit`; the preparation task was to run `streamlit hello`). Tested with Streamlit 1.66 and DuckDB 1.5.5. Check at the start who could not install Streamlit and pair them with someone who could.
:::

---

# Today's Agenda

1. Recap: from single charts to a dashboard
2. Analytics portals and BI tools
3. Semantic layer and self-service BI
4. Dashboards and embedded analytics
5. Access and governance
6. Lab: a Streamlit dashboard on the warehouse

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:10 Portals and BI tools (input) · 0:25 Semantic layer and self-service (input + discussion) · 0:50 Exercise "who needs what?" (pairs, then plenary) · 1:00 Break · 1:10 Dashboards and embedded analytics (input) · 1:25 Access and governance (input + discussion) · 1:35 Lab (pairs) · 2:55 Wrap-up · buffer is the discussion time in the input parts.
If the governance discussion runs long, keep it and shorten the lab: lab tasks 5 and 6 can be finished at home.
:::

---

# Recap: From Charts to a Dashboard

- Session 5: one chart per question — sorted, honest, with an **action title**
- Your KPI definition sheet: formula, source, time reference, owner
- But managers do not open notebooks: they need **one place** where the right charts are always up to date

::: callout
**Today's question:** how do companies deliver analytics to hundreds of users — consistently, securely and without an analyst in the loop for every request?
:::

::: notes
Ask two pairs to show the chart they want to put on a dashboard today (preparation task from session 5). Ask: if 50 people needed this chart every Monday, how would you deliver it? Collect answers (e-mail with PDF, shared Excel, a BI tool, a web app) — they lead directly to the portal idea.
:::

---

# Analytics Portals {.section}

One entry point to reports, dashboards and analyses

---

# What Is an Analytics Portal?

An **analytics portal** is the single, secured entry point through which users find and use the analytical content of an organisation.

- **Content:** standard reports, dashboards, ad hoc analysis, forecasts and model results
- **Personalised:** each user sees the content and data that fit their role
- **Consistent:** all content uses the same data and the same KPI definitions
- **Channels:** web portal, mobile app, e-mail subscriptions, or embedded in other applications

::: source
Own definition based on Baars and Kemper (2021) and Chaudhuri et al. (2011).
:::

::: notes
Chaudhuri et al. list the front-end applications through which users perform BI tasks: spreadsheets, enterprise portals for searching, performance management applications with visual dashboards, ad hoc query tools and viewers for data mining models. In practice, "portal" today usually means the web front end of a BI platform (e.g. a Power BI workspace or app, a Tableau site) or a company intranet page that bundles them. The module handbook calls the topic "structure and infrastructure of analytics portals".
:::

---

# Layers of an Analytics Portal

::: layers
- Access: portal, mobile app, subscriptions, embedding in other applications
- Analytics services: reports, dashboards, OLAP and ad hoc analysis, notebooks, ML results
- Semantic layer: business terms, metrics, hierarchies, access rules
- Data: data warehouse, data marts, lakehouse
- Sources: ERP, CRM, web shop, external data
:::

**Across all layers:** security, governance, metadata and monitoring

::: source
Own illustration based on Chaudhuri et al. (2011) and Baars and Kemper (2021).
:::

::: notes
Chaudhuri et al. describe a typical BI architecture as data sources → data movement (ETL, complex event processing) → data warehouse servers → mid-tier servers (OLAP, reporting, data mining, enterprise search) → front-end applications. The semantic layer is not a separate box in their figure; we draw it explicitly because modern BI platforms make it a product of its own. Link to session 2: the lower layers are the DWH reference architecture from the analyst's view. Today we work on the upper three layers.
:::

---

# The BI Tool Landscape

| Category | Examples | Strengths | Limits |
|---|---|---|---|
| BI platforms | Power BI, Tableau, Qlik | Self-service, semantic models, sharing, security built in | Licence costs, vendor lock-in |
| Open-source BI | Apache Superset, Metabase | No licence costs, SQL-based | Own operation and security |
| Code-first apps | Streamlit, Dash, Shiny | Full flexibility, Python and ML integration | Everything must be programmed |
| Notebooks | Jupyter | Exploration, documentation | Not for non-technical users |

::: notes
Own compilation; no ranking intended — product names are examples only. Ask: which category does your company use? Most DSKI students know Power BI or Tableau from their company. Selection criteria worth discussing: who builds content (IT vs. business), number and type of users, existing licences, data sources, security requirements, need for ML integration. We use Streamlit in the lab because it is free, runs locally and is Python — the concepts (semantic layer, caching, access rules) transfer to every category.
:::

---

# Semantic Layer and Self-Service BI {.section}

One definition of revenue — for everyone

---

# The Semantic Layer

Three teams report **revenue 1997** for the TPC-H wholesaler — and get three numbers.

- A **semantic layer** maps business terms (revenue, customer, region) to tables, joins and formulas — defined **once**, used by every report and tool
- Users query in business language; the layer generates the SQL
- Idea since the early 1990s: BusinessObjects "universes" let non-technical users query relational databases with business objects
- Today: semantic models in BI platforms, metric layers such as the dbt Semantic Layer

::: source
Cambot and Liautaud (1996); dbt Labs (n.d.); Kimball and Ross (2013).
:::

::: notes
Revenue 1997 (sf 0.1): gross incl. tax by order date 3,212.1 million; net by order date 3,088.6 million; net by ship date 3,095.4 million — all three are defensible, which is exactly the problem (worksheet task 4). The BusinessObjects patent (filed 1991, granted 1996) describes business-vocabulary objects from which the system generates SQL. dbt Labs names consistency, a single source of truth and governed access as the benefits of central metric definitions. Kimball and Ross make the same point for the warehouse itself with conformed dimensions and facts: the same name must mean the same thing everywhere.
:::

---

# What Belongs in a Semantic Layer?

| Element | TPC-H example |
|---|---|
| Business names | `region`, `segment` instead of `r_name`, `c_mktsegment` |
| Joins | fact_sales → dim_customer, dim_date — defined once |
| Metrics with aggregation | net revenue = `sum(revenue)`; active customers = `count(DISTINCT customer_key)` |
| Non-additive metrics | revenue per active customer = sum ÷ distinct count — never average the ratios |
| Hierarchies | region → nation; year → quarter → month |
| Default filters and rules | only complete periods; who may see which region |

::: source
Own example with TPC-H data (Transaction Processing Performance Council, n.d.), based on Kimball and Ross (2013).
:::

::: notes
Distinct counts are the classic trap: active customers 1996: 8,641; 1997: 8,640; but 1996–1997 together only 9,728 — not 17,281. A BI tool that sums a distinct count over years is wrong. The semantic layer must store the formula, not a precomputed number. Link to session 3 (additive, semi-additive, non-additive measures).
:::

---

# Self-Service BI

**Self-service BI** lets business users carry out their own analyses without asking IT or an analyst for every report.

| Level | Users can … | TPC-H example |
|---|---|---|
| Usage of information | Open prepared reports, set filters and parameters | Choose region and year on the sales dashboard |
| Creation of information | Build their own reports and analyses on prepared data | Build a new chart from the certified sales model |
| Creation of information resources | Add and combine new data sources themselves | Join a purchased market data file to the sales data |

::: source
Based on Alpar and Schulz (2016) and Passlick et al. (2023).
:::

::: notes
Alpar and Schulz distinguish the three levels along two dimensions, self-reliance of the user and system support. Passlick et al. build a taxonomy of self-service BI and analytics application scenarios on this work. The higher the level, the more freedom — and the more governance is needed. Ask: which level does your company support? Most say level 1 for everyone and level 2 for "power users".
:::

---

# Self-Service: Benefits and Risks

::: columns
**Benefits**

- Faster answers, fewer requests in the IT backlog
- Business knowledge goes directly into the analysis
- Analysts can focus on harder questions
|||
**Risks**

- Competing numbers for the same KPI
- "Shadow" spreadsheets and unmanaged copies of data
- Wrong joins and aggregations by untrained users
- Data protection and security gaps
:::

::: callout
Self-service needs **guard rails**: certified data sets, a semantic layer, training, and a path from personal sandbox to shared, reviewed content.
:::

::: source
Own compilation based on Alpar and Schulz (2016) and Passlick et al. (2023).
:::

::: notes
The guard rails are the practical answer to the tension between flexibility and control. Typical pattern in BI platforms: personal workspace → shared workspace → certified/endorsed content, with a review step before promotion. Ask the students for an example of competing numbers from their company.
:::

---

# Exercise: Who Needs What? {.exercise}

The TPC-H wholesaler plans an analytics portal. For each user group, propose the content, the self-service level and the data access.

1. Chief executive officer
2. Sales manager for Europe
3. Controller
4. Data analyst in the BI team
5. Retail customers who buy from the wholesaler

::: notes
Expected answers: 1 strategic dashboard (revenue, growth, on-time delivery vs. target, by region), usage of information, all regions, aggregated · 2 operational/analytical dashboard with drill-down to nation and customer, usage of information (maybe creation), only Europe (row-level security) · 3 detailed reports and tables, export to Excel, creation of information on the certified model, all regions · 4 full SQL access to the warehouse, creation of information resources, all data incl. new sources, but publishes to others only via review · 5 embedded analytics in the customer portal: own orders, delivery status, spend per month — usage of information, strictly only their own customer rows. Point out that group 5 is outside the company: authentication, multi-tenancy and data protection become critical.
:::

---

# Dashboards and Embedded Analytics {.section}

Showing what matters — where people work

---

# Dashboards

A **dashboard** shows the most important information for a goal on **one screen**, so it can be monitored at a glance.

| Role | Purpose | Typical design |
|---|---|---|
| Strategic | Overview of business health for executives | Few KPIs, comparisons to target and previous period, low update frequency |
| Analytical | Understand causes and patterns | More detail, filters, drill-down |
| Operational | Monitor processes that change quickly | Near real-time data, alerts, simple displays |

::: source
Based on Few (2013).
:::

::: notes
Paraphrase of Few's definition: a visual display of the most important information needed to achieve one or more objectives, arranged on a single screen so it can be monitored at a glance. Few classifies dashboards by the role they play (strategic, analytical, operational) and stresses that the role has the greatest effect on visual design. Ask: which role does the dashboard you will build in the lab play? (Mostly analytical: filters by region and year.)
:::

---

# Dashboard Design Rules

- **One screen:** if users must scroll, the overview is lost
- **Context for every number:** target, previous period or benchmark
- **Most important first:** top left, largest; details below or on click
- **Consistent displays:** same chart type and colour for the same kind of data
- **Visible filters and data freshness:** "Data as of 2 August 1998, complete years only"
- **Avoid clutter:** no gauges, 3D or decoration that hides the data

::: source
Based on Few (2013) and Knaflic (2015).
:::

::: notes
Few lists common dashboard design mistakes, e.g. exceeding one screen, too little context, excessive detail, poorly chosen measures, inappropriate or needlessly varied display media, poor layout, failing to highlight what matters, clutter and misuse of colour. Most map directly to session 5. The freshness line matters in practice: many support tickets are "the number is wrong" when the data is simply from yesterday's load.
:::

---

# Embedded Analytics

**Embedded analytics** puts reports and dashboards **inside the applications** where people already work — CRM, web shop, customer portal — instead of a separate BI tool.

| Scenario | Users | Authentication | Example |
|---|---|---|---|
| For your organisation | Employees | Company login of each user | Sales figures in the CRM |
| For your customers | External users | The application's own login | Spend report in a supplier portal |

- Challenges: one tenant must never see another tenant's data, licences and capacity, performance under load

::: source
Microsoft (n.d.-a); Chaudhuri et al. (2011).
:::

::: notes
Microsoft distinguishes "embed for your organization" (user owns data: users sign in with their own account and need a licence) and "embed for your customers" (app owns data: the application authenticates with a service account and handles its own users). The two scenarios are general, not Power BI-specific. Chaudhuri et al. mention CRM applications with built-in analytics. Link to the exercise: group 5 needs the second scenario.
:::

---

# Access and Governance {.section}

Who may see what — and who is responsible

---

# Access Control

- **Authentication:** who is the user? (login, single sign-on)
- **Authorisation:** what may this user see and do?
- **Role-based access:** rights are given to roles (viewer, author, admin), users get roles
- **Row-level security:** filter rows per role, e.g. the Europe role sees only `region = 'EUROPE'`
- **Object-level security:** hide whole tables or columns, e.g. customer names

::: callout
Enforce access rules **where the data is queried**, not only in the user interface — and check what admins and authors can see.
:::

::: source
Microsoft (n.d.-b); Streamlit (n.d.-b).
:::

::: notes
Power BI row-level security defines roles with DAX filter expressions; it restricts viewers but not workspace admins, members or contributors. Streamlit's built-in login (st.login, OpenID Connect) only authenticates — the app must implement authorisation itself (worksheet task 6). Hiding a region in a dropdown is not security if another chart or a download button still shows all regions. Aggregates can leak too: "Europe is 19.9 % of total revenue" reveals the company total.
:::

---

# Governance of a Portal

- **Ownership:** every dashboard and data set has an owner
- **Certified content:** reviewed data sets and dashboards are marked as trusted
- **Definitions:** KPIs documented once — in the semantic layer and a glossary
- **Freshness and lineage:** where does a number come from, and how old is it?
- **Lifecycle:** monitor usage, archive what nobody opens
- **Data protection:** personal data only where needed, with access logged

::: notes
Own compilation. Connect to the KPI definition sheet from session 5 and to the semantic layer: governance is mostly about making definitions and responsibilities explicit. Ask: how many dashboards does your company have, and how many are actually used? Students often report hundreds of reports with a handful in daily use.
:::

---

# Lab: A Streamlit Dashboard {.section}

From the star schema to a small analytics portal

---

# Streamlit in Five Minutes

- An app is a **Python script**; `streamlit run app.py` opens it in the browser
- On every interaction the script **reruns from top to bottom**; widgets return the current value
- `@st.cache_resource` keeps **one shared object**, e.g. the database connection
- `@st.cache_data` caches **query results**; `ttl` sets when they expire
- Open DuckDB with `read_only=True`; a notebook with a write connection to the same file **blocks** the app — close it first

::: source
Streamlit (n.d.-a); DuckDB Foundation (n.d.).
:::

::: notes
The rerun model is the main mental shift for students used to notebooks: there is no "cell state"; everything not cached is recomputed. Streamlit recommends caching database queries. DuckDB documents that a single connection is thread-safe (queries are serialised) and that read-only mode is required when several processes access the same file. Tested: a notebook holding a read-write connection makes the app fail with "Could not set lock on file"; con.close() in the notebook fixes it.
:::

---

# Starter App (1/2): Connection and Filters

```python
import duckdb
import streamlit as st

st.set_page_config(page_title="TPC-H Sales", layout="wide")

@st.cache_resource                     # one connection for all users
def get_con():
    return duckdb.connect("tpch.duckdb", read_only=True)

@st.cache_data(ttl=3600)               # cache query results for one hour
def query(sql, params=()):
    return get_con().execute(sql, list(params)).df()

BASE = """FROM fact_sales JOIN dim_customer USING (customer_key)
                     JOIN dim_date USING (date_key)"""
st.title("Sales Dashboard")
regions = query("SELECT DISTINCT region FROM dim_customer ORDER BY region")
region = st.sidebar.selectbox("Region", regions["region"])
year = st.sidebar.selectbox("Year", range(1993, 1998), index=4)  # complete years
```

::: notes
Save both parts as one file app.py next to tpch.duckdb and run `streamlit run app.py`. Point out: parameters with ? (no string concatenation of user input into SQL); the year list stops at 1997 because 1998 is incomplete (session 5) and starts at 1993 so that every year has a previous year for the comparison.
:::

---

# Starter App (2/2): KPI Tiles and Chart

```python
kpi = query(f"""SELECT year, sum(revenue) / 1e6 AS revenue_m,
                       count(DISTINCT customer_key) AS customers
                {BASE} WHERE region = ? AND year IN (?, ?)
                GROUP BY year ORDER BY year""", (region, year - 1, year))
prev, cur = kpi.iloc[0], kpi.iloc[1]
growth = cur.revenue_m / prev.revenue_m - 1

c1, c2 = st.columns(2)
c1.metric("Revenue (million)", f"{cur.revenue_m:,.1f}",
          f"{growth:+.1%} vs. {year - 1}")
c2.metric("Active customers", f"{int(cur.customers):,}")

monthly = query(f"""SELECT month, sum(revenue) / 1e6 AS revenue_m
                    {BASE} WHERE region = ? AND year = ?
                    GROUP BY month ORDER BY month""", (region, year))
st.subheader(f"Monthly revenue {year}: {region.title()}")
st.bar_chart(monthly, x="month", y="revenue_m",
             x_label="Month", y_label="Revenue (million)")
```

::: notes
Tested with Streamlit 1.66, DuckDB 1.5.5, sf 0.1 (also with Streamlit's AppTest). Default view Africa 1997: revenue 602.4 million, −3.9 % vs. 1996, 1,715 active customers. Europe 1997: 615.2 (−0.2 %), 1,735; Middle East 1997: 640.4 (+3.0 %), 1,758. The metric tile colours the delta green or red automatically — discuss whether −0.2 % deserves a red signal (session 5: context and targets).
:::

---

# Lab Tasks {.exercise}

Work in pairs. Start from the starter app and extend it step by step.

1. **Run:** start the app, change the filters, and explain what happens on each rerun
2. **Trend:** add a line chart of yearly revenue 1993–1997 for the selected region
3. **Detail:** add a table of the top 10 customers of the selected region and year
4. **Your chart:** add your best chart from session 5 with its action title
5. **Semantic layer:** create a view `sales` in DuckDB with business column names and use it in all queries
6. **Governance:** write down who may use this dashboard, which data they may see, and how you would enforce it

::: notes
Expected results (DuckDB 1.5.5, sf 0.1): 1 every widget change reruns the whole script; cached queries return immediately · 2 e.g. Asia: 1993 617.8, 1994 642.0, 1995 639.3, 1996 622.9, 1997 604.3 million; st.line_chart(df, x="year", y="revenue_m") — tell students to treat year as a category or format the axis, and not to read a trend into ±3 % · 3 Asia 1997: top customer Customer#000008425 (Japan, Automobile) with 1.598 million; st.dataframe(df, hide_index=True) · 4 any chart; in Streamlit use st.pyplot(fig) for matplotlib · 5 in the notebook (write connection): CREATE VIEW sales AS SELECT d.year, d.quarter, d.month, c.region, c.nation, c.segment, c.customer, f.customer_key, f.quantity, f.revenue AS net_revenue FROM fact_sales f JOIN dim_customer c USING (customer_key) JOIN dim_date d USING (date_key); then con.close() before restarting the app. A view gives business names and joins, but metrics still live in each query — worksheet task 4 adds a metric layer · 6 e.g. regional sales managers only their region, enforced in the query function, not only in the dropdown. The app feeds into the group case study (dashboard option).
:::

---

# Key Takeaways

- An **analytics portal** is the secured single entry point to reports, dashboards and analyses
- A **semantic layer** defines business terms, joins and metrics **once** — the cure for competing numbers
- **Self-service BI** ranges from using to creating information and information resources — more freedom needs more guard rails
- **Dashboards** show what matters on one screen, with context; **embedded analytics** brings them into everyday applications
- **Access and governance:** authenticate, authorise where the data is queried, and give every KPI and dashboard an owner

---

# Next Session: From Business Question to ML Use Case

- Short recap of ML methods and the analytics process (CRISP-DM)
- Framing a business problem as an ML task
- Features from the warehouse, baselines and data leakage
- Judging a model by business cost

::: callout
**Preparation:** think of one decision at the TPC-H wholesaler that a prediction could improve — which customers, orders or products would it be about?
:::

---

# References {.references}

- Alpar, P., & Schulz, M. (2016). Self-service business intelligence. *Business & Information Systems Engineering, 58*(2), 151–155. https://doi.org/10.1007/s12599-016-0424-6
- Baars, H., & Kemper, H.-G. (2021). *Business Intelligence & Analytics – Grundlagen und praktische Anwendungen: Ansätze der IT-basierten Entscheidungsunterstützung* (4th ed.). Springer Vieweg. https://doi.org/10.1007/978-3-8348-2344-1
- Cambot, J.-M., & Liautaud, B. (1996). *Relational database access system using semantically dynamic objects* (U.S. Patent No. 5,555,403). U.S. Patent and Trademark Office. https://patents.google.com/patent/US5555403
- Chaudhuri, S., Dayal, U., & Narasayya, V. (2011). An overview of business intelligence technology. *Communications of the ACM, 54*(8), 88–98. https://doi.org/10.1145/1978542.1978562
- dbt Labs. (n.d.). *dbt Semantic Layer*. Retrieved October 20, 2026, from https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl
- DuckDB Foundation. (n.d.). *Python DB API*. Retrieved October 20, 2026, from https://duckdb.org/docs/current/clients/python/dbapi.html
- Few, S. (2013). *Information dashboard design: Displaying data for at-a-glance monitoring* (2nd ed.). Analytics Press.
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Knaflic, C. N. (2015). *Storytelling with data: A data visualization guide for business professionals*. Wiley.
- Microsoft. (n.d.-a). *What is Power BI embedded analytics?* Retrieved October 20, 2026, from https://learn.microsoft.com/en-us/power-bi/developer/embedded/embedded-analytics-power-bi
- Microsoft. (n.d.-b). *Row-level security (RLS) with Power BI*. Retrieved October 20, 2026, from https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security
- Passlick, J., Grützner, L., Schulz, M., & Breitner, M. H. (2023). Self-service business intelligence and analytics application scenarios: A taxonomy for differentiation. *Information Systems and e-Business Management, 21*(1), 159–191. https://doi.org/10.1007/s10257-022-00574-3
- Streamlit. (n.d.-a). *Caching overview*. Retrieved October 20, 2026, from https://docs.streamlit.io/develop/concepts/architecture/caching
- Streamlit. (n.d.-b). *User authentication and information*. Retrieved October 20, 2026, from https://docs.streamlit.io/develop/concepts/connections/authentication
- Transaction Processing Performance Council. (n.d.). *TPC-H*. Retrieved October 20, 2026, from https://www.tpc.org/tpch/
