# Data Management — Session Plan (approved 2026-10-01)

20 sessions × 3 h (60-minute hours) = 60 h, including a 1 h exam Q&A in session 20. First run: 2027. Hands-on work uses **SQLite + Jupyter notebooks** (runs on both macOS and Windows).

Assessment: written exam + design project (weighting to be decided). The design project runs through the course: students design and build a small database for a business case, then load, clean and query real data.

Legend for learning-outcome links: **SC** subject competence · **MC** methodological competence · **PSC** personal/social · **OC** overarching (see [MODULE.md](MODULE.md)).

## Part A — Foundations of Data Management

| # | Session | Contents | Hands-on / activity | LO |
|---|---|---|---|---|
| 1 | **Why data matters** | Course overview, exam and project; value of data for organisations and society; definitions and distinctions: Data Management, Data Science, Business Analytics, Business Intelligence, Big Data | Group discussion: data-driven business cases | SC, OC |
| 2 | **Data types and data management fundamentals** | Structured, semi-structured, unstructured data; data lifecycle; overview of data management knowledge areas (DAMA-DMBOK); data, information, knowledge | Classify example datasets; tool setup (Python, Jupyter, SQLite) | SC, MC |
| 3 | **Semantic data modelling I: ER model** | Entities, attributes, relationships, cardinalities; Chen vs. crow's-foot notation | Model a small business case on paper | SC, MC |
| 4 | **Semantic data modelling II** | Weak entities, n:m and recursive relationships, generalisation/specialisation; modelling pitfalls; **design project kickoff** (teams, cases, milestones) | Teams model their project case | MC, PSC |
| 5 | **The relational model** | Relations, tuples, domains, keys (primary, foreign, candidate); integrity constraints; mapping ER → relational schema | Map the project ER model to tables | SC, MC |
| 6 | **Efficient database design: normalisation** | Anomalies; functional dependencies; 1NF, 2NF, 3NF, BCNF; when to denormalise | Normalise a messy spreadsheet | SC, MC |

## Part B — SQL and Databases

| # | Session | Contents | Hands-on / activity | LO |
|---|---|---|---|---|
| 7 | **SQL I: defining schemas** | DDL: `CREATE`, `ALTER`, `DROP`; data types; constraints (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `CHECK`) | Create the course sample database in SQLite | MC |
| 8 | **SQL II: manipulating and querying data** | DML: `INSERT`, `UPDATE`, `DELETE`; `SELECT`, `WHERE`, `ORDER BY`, `DISTINCT`, `LIMIT` | Query exercises in Jupyter | MC |
| 9 | **SQL III: joins** | Inner, left/right/full outer joins; self joins; join pitfalls | Multi-table query exercises | MC |
| 10 | **SQL IV: aggregation and beyond** | `GROUP BY`, `HAVING`, aggregate functions, subqueries, views; indexes, transactions and ACID | Business questions answered with SQL | MC, OC |
| 11 | **NoSQL databases** | Limits of relational systems; CAP theorem and BASE; key-value, document, column-family, graph databases; choosing a data store for a use case | Same case modelled relationally vs. as JSON documents | SC, MC |
| 12 | **Project workshop and catch-up** | Buffer block: catch up on Parts A–B if needed; review of team schemas and SQL; feedback round | Team consultations, extra SQL practice | PSC |

## Part C — Data Quality and Data Access

| # | Session | Contents | Hands-on / activity | LO |
|---|---|---|---|---|
| 13 | **Data quality I** | Definition; data quality dimensions and criteria; measurement methods and metrics; causes and business cost of poor data | Assess the quality of a real dataset | SC, MC, OC |
| 14 | **Data quality II: data cleaning with Python** | pandas basics; missing values, duplicates, outliers, inconsistent formats; standardisation and validation rules | Clean a dataset in a notebook | MC |
| 15 | **Accessing data: files and APIs** | Reading CSV, Excel, JSON; REST APIs and JSON; calling APIs from Python; authentication and rate limits | Fetch data from a public API (open data) | MC |
| 16 | **ETL and data integration** | Extract–transform–load vs. ELT; pipeline design; scheduling and monitoring | Build a small ETL pipeline: API → pandas → SQLite | SC, MC |

## Part D — Data Storage Systems and Access to Data

| # | Session | Contents | Hands-on / activity | LO |
|---|---|---|---|---|
| 17 | **Data warehousing** | DWH concepts (Inmon vs. Kimball); star and snowflake schema; fact and dimension tables; OLAP | Design a star schema for the project case | SC, MC |
| 18 | **Modern data architectures** | Data lake, lakehouse, data mesh, data fabric; cloud data platforms; choosing an architecture | Architecture case comparison | SC, OC |
| 19 | **Access to data: legal and organisational aspects** | GDPR, EU Data Act, Data Governance Act, AI Act (data aspects); data licences and open data; data governance, roles (data owner, data steward, CDO), data strategy | Case discussion: may we use this data? | SC, PSC, OC |
| 20 | **Project presentations and exam Q&A** | Team presentations of design projects (2 h); exam Q&A (1 h) | Presentations, Q&A | PSC |

## Teaching principles (agreed 2026-10-01)

- **Don't squeeze.** Discussion is valuable and should never be cut just to get through the slides.
- **Each 3 h block is planned as roughly:** ~60–75 min input · ~75–90 min hands-on, practice or discussion · ~15–30 min unplanned buffer.
- **Core vs. optional slides.** Every deck marks slides as *core* (exam-relevant, always covered) or *optional* (deep dives that can be skipped or set as self-study). If a session runs long, optional content moves to self-study, not to the next session.
- **1 h exam Q&A** at the end of the course.

## Notes

- Session order puts the design project early (session 4) so teams can apply each technical topic as it is taught.
- Session 12 is deliberately a buffer: no new content, so earlier sessions can overrun without cutting topics.
- Sources for each session (module literature plus primary sources such as Codd 1970, Chen 1976, DAMA-DMBOK) will be checked and cited on the slides when each session is built.
