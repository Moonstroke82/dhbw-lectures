---
course: IT Management and EAM
session: 18
title: EAM Tools and Course Synthesis
subtitle: The EAM tool landscape · SAP LeanIX walkthrough · how IT management and EAM fit together · exam Q&A
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# EAM Tools and Course Synthesis {.title}

::: notes
Time plan for today (3 h block + 1 h exam Q&A): recap of the preparation task 10 min · from spreadsheet to tool and what tools do 10 min · tool landscape and selection 10 min · SAP LeanIX walkthrough (meta model, fact sheets, data quality, reports) 35 min · break 10 min · hands-on tool walkthrough 45 min · course synthesis 15 min · synthesis exercise 30 min · wrap-up 5 min · ~10 min buffer. Then, after a short break: exam Q&A 60 min (question types and approach 15 min · worked practice examples 20 min · students' own questions 20 min · close 5 min).
This is the last session. It covers the module content "EAM tools, e.g. LeanIX", closes Part B and connects it with Part A (overarching competence: choose suitable methods for modelling, managing and optimising the IT landscape). The exam Q&A shows question **types** and worked **practice** examples only. Never present any slide or example as an actual exam question, and do not hint at exam content beyond "all core slides are relevant".
Source note for the lecturer: the SAP LeanIX part is based only on the official product documentation at docs-eam.leanix.net (pages on the overview, meta model, fact sheets, fact sheet subscription, quality seal, reports, matrix report, roadmap report and general modeling guidelines; all retrieved 22 October 2026). Product features change often — re-check the pages before the first run in 2028, in particular the meta model version (v4 at the time of writing) and the names of the reports. No product screenshots are used: the two tool figures are own schematic drawings. LeanIX became part of SAP in November 2023 (SAP news release); the product is now called SAP LeanIX. Hanschke (2023) states that her book covers tool support only at the margin and refers to market studies for tool comparisons; the tool landscape slide is therefore an own overview without a ranking. If a demo or trial workspace is available (e.g. through the SAP university programme), use it for the hands-on part; otherwise use the paper version of the walkthrough (printed fact sheet templates), which works just as well for the learning goals.
:::

---

# Today's Agenda

1. Recap: EAM tools in your company and your revision questions
2. EAM tools: what they do and how to choose one
3. SAP LeanIX walkthrough: meta model, fact sheets, data quality, reports
4. Hands-on: the on-demand bus pilot of Rhein-Neckar Mobil Group in the tool
5. Course synthesis: how IT management and EAM fit together
6. Exam Q&A: question types, worked practice examples, your questions

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (plenary) · 0:10 From spreadsheet to tool, functions (input) · 0:20 Tool landscape and selection (input + discussion) · 0:30 SAP LeanIX walkthrough (input with demo or figures) · 1:05 Break · 1:15 Hands-on walkthrough (pairs + plenary) · 2:00 Course synthesis (input) · 2:15 Synthesis exercise (groups + plenary) · 2:45 Wrap-up · ~10 min buffer · 3:00 Break · 3:10 Exam Q&A (input + plenary) · 4:10 End.
If the session runs long: "Limits of EAM Tools" and "Modelling Guidelines in the Tool" are optional and move to self-study. Keep the hands-on walkthrough and the Q&A; shorten the synthesis exercise to two lenses if needed. The worksheet for today is a course-wide revision set with full solutions for self-study.
:::

---

# Recap: EAM Tools and Your Questions

You were asked to find out whether your training company uses an **EAM tool** and to bring **three revision questions** about sessions 1–17.

- Which **tool** do you use — or is it Excel, a wiki, a CMDB, Visio?
- **What for**: application list, landscape maps, roadmaps, compliance?
- **Who** maintains the data, and do people **trust** it?
- Your questions: which **topics** come up most often?

::: notes
First 5 min: show of hands per tool category (dedicated EAM tool · modelling tool · CMDB/ITSM tool · spreadsheet/wiki · nothing known). Typical findings: larger companies use SAP LeanIX, Alfabet, ADOIT, Bizzdesign or Ardoq; many medium-sized companies still use Excel plus a CMDB; trust is low when nobody owns the data (session 11). Next 5 min: collect the revision questions on a flipchart or board, cluster them by session and keep the list for the Q&A at the end. Tell students that questions will be answered in the Q&A, not now.
:::

---

# EAM Tools {.section}

From the spreadsheet to a shared repository

---

# From Spreadsheet to EAM Tool

::: columns
**Spreadsheets and drawings**

- One **list per person**; versions in e-mails
- **Relationships** (application – capability – interface) hard to keep
- Every picture **drawn by hand** and outdated quickly
- No **owners**, no history, no access rights
|||
**What a tool adds**

- One **repository** with a **meta-model** (session 11)
- Relations are **data**: views and analyses are **generated**
- **Owners**, workflows and quality checks keep data current
- **Imports** and **interfaces** from CMDB, cloud and project tools
:::

::: callout
A tool does not create an EA practice — it makes an existing practice **scalable**: more data, more users, less manual drawing.
:::

::: source
Own wording based on Hanschke (2023), Farwick et al. (2011) and Roth et al. (2013).
:::

::: notes
Link to the running case: Rhein-Neckar Mobil Group has about 180 applications and 240 software contracts, and a retiring colleague keeps the Excel list (session 11). With two architects, the team cannot draw landscape maps by hand for every question. Roth et al. (2013) surveyed EA practitioners and found that organisations struggle to document the EA and keep it current; Farwick et al. (2011) explain why manual maintenance of large models is slow and costly and what automated maintenance requires (reliable source systems, mapping, conflict rules). Hanschke (2023) recommends starting EAM with clear questions and lean data, then choosing a tool — not the other way round.
:::

---

# What EAM Tools Do

::: cards
### Repository and meta-model
Store elements, attributes and relations in a configurable meta-model
### Data collection
Imports, interfaces to CMDB, cloud and project tools; surveys to owners
### Data quality and collaboration
Owners, notifications, quality checks, comments, history
### Analysis and visualisation
Generated reports and diagrams: landscape maps, matrices, portfolios
### Planning
Target states, roadmaps, initiatives and their impact on the landscape
### Governance support
Standards, life cycles, risks and compliance evidence in one place
:::

::: source
Own compilation based on Hanschke (2023), Farwick et al. (2011) and SAP LeanIX (n.d.-i).
:::

::: notes
Map each card to the course: repository and meta-model (session 11), data collection methods (session 11), data quality and maintenance concept (session 11), views for stakeholders (sessions 10 and 17), landscape planning and TIME (session 13), integration view (session 14), architecture governance (session 16). The point for students: the functions of a tool are the fields of action of EAM made concrete — nothing in the tool is new; it supports what they already know.
:::

---

# The EAM Tool Landscape

| Kind of tool | Typical strength | Examples (no ranking) |
|---|---|---|
| **Dedicated EAM suites**, often SaaS | Predefined meta-model, quick start, reports for management | SAP LeanIX, Ardoq, Alfabet |
| **Modelling-centred EA tools** | ArchiMate models, detailed views, analyses (session 17) | Bizzdesign, ADOIT, MEGA HOPEX |
| **Free modelling tools** | ArchiMate drawing at no licence cost | Archi |
| **Neighbouring tools** used for EA data | Technical inventory or process models | CMDB in the ITSM tool, process modelling tools |
| **Office tools** | Available everywhere, no training | Spreadsheets, wikis, drawing tools |

::: source
Own overview; product names are examples, not a market study or recommendation.
:::

::: notes
The categories overlap: many EAM suites support ArchiMate today, and many modelling tools offer dashboards. Market overviews exist (e.g. analyst reports), but they change every year and are often behind paywalls; we deliberately do not rank products. Ask: which category is your training company's tool in? Point out the neighbouring tools: a CMDB (session 6) knows servers and installed software, but not capabilities or business owners — EAM tools usually import from it rather than replace it. Archi is a free, open-source ArchiMate modelling tool that students can use for the worksheet tasks of session 17.
:::

---

# Choosing an EAM Tool

::: columns
**Questions before the tool**

- Which **stakeholder questions** must it answer (session 10)?
- Which **meta-model** do we need — can the tool's default fit (session 11)?
- Who **maintains** the data, and how much effort is realistic?
- Which **sources** must be connected (CMDB, cloud, project portfolio)?
|||
**Criteria for the tool**

- **Fit** of meta-model and reports; configurability
- **Usability** for business owners, not only for architects
- **Integration**: imports, APIs, ArchiMate exchange
- **Sourcing** aspects: SaaS or on-premises, data location, cost, exit (session 15)
:::

::: callout
Start with the **questions**, then the **data**, then the **tool** — a tool chosen first decides your meta-model for you.
:::

::: source
Own compilation based on Hanschke (2023) and Farwick et al. (2011).
:::

::: notes
This is a make-or-buy and vendor selection decision like in session 15: functional fit, total cost (licences per user, configuration, data collection effort — usually the largest cost), skills, risks (lock-in, data protection for personal data of owners), exit strategy (can we export the repository?). Most EAM tools are offered as SaaS, so the cloud sourcing questions of session 15 apply (location, sub-processors, contract). A useful method: run a proof of concept with the organisation's own data for two or three real questions (e.g. "which applications support ticketing and reach end of support before 2029?").
:::

---

# SAP LeanIX Walkthrough {.section}

Fact sheets, relations and reports

---

# SAP LeanIX at a Glance

- A **SaaS** tool for enterprise architecture management, with the **application** as its central entity
- Base product: **application portfolio management**; add-ons for **architecture and roadmap planning** and **technology risk and compliance**
- **Fact sheets** store the data of each architecture object; the **meta model** defines how they relate
- **Inventory** to manage fact sheets; **reports** and **diagrams** to visualise; **surveys**, **subscriptions** and comments to collaborate; **integrations** to collect data

::: source
Own wording based on SAP LeanIX (n.d.-i, n.d.-e).
:::

::: notes
If a demo workspace is available, show the start page, the inventory and one application fact sheet now (max. 5 min), then switch back to the slides; otherwise describe the parts with the following slides. Name the session links: inventory = the EA repository (session 11), reports = views for stakeholders (sessions 10 and 17), application portfolio management = TIME and roadmap (session 13). Stress: we use SAP LeanIX as an example because it is named in the module description; the concepts transfer to other tools.
:::

---

# The Meta Model: Twelve Fact Sheet Types

![Own schematic drawing of the twelve fact sheet types of the SAP LeanIX meta model version 4 in four layers. Strategy and transformation: objective, initiative, platform. Business architecture: organization, business capability, business context. Application and data architecture: interface, application, data object. Technical architecture: provider, IT component, tech category. The application in the centre supports business capabilities, is used or owned by organizations, is used in business contexts, provides or consumes interfaces, creates or reads data objects and runs on or uses IT components; IT components are offered by providers and belong to tech categories; objectives are realised by initiatives that affect the landscape; platforms group capabilities, applications or technologies. Simplified selection of relations](img/eamtool-metamodel.png){width=74%}

::: source
Own illustration based on SAP LeanIX (n.d.-e); simplified selection of relations.
:::

::: notes
The documentation groups the twelve types into four layers and stresses that the layers are a way to think about the model, not labels in the product. Compare with the lean meta-model of session 11: organisation unit, capability, process, business object, application, interface, technology component — almost the same, plus strategy and transformation types (objective, initiative, platform) and providers. Compare with ArchiMate (session 17): business capability ≈ capability, application ≈ application component, IT component ≈ node or system software, interface ≈ application interface plus flow, data object ≈ data object, initiative ≈ work package. Business context covers things such as processes, value streams or customer journeys (session 12). Older workspaces use meta model v3 with other types (e.g. user group, project, process); the documentation recommends staying close to the standard model, especially for organisations with low EA maturity.
:::

---

# Anatomy of a Fact Sheet

| Part | What it shows | Link to the course |
|---|---|---|
| **Header** | Name, type, completeness in %, quality seal, subscribe | Data quality (session 11) |
| **Body** | Sections with attributes: description, life cycle, criticality, functional and technical fit | Application fact sheet (11), TIME (13) |
| **Relations** | Related fact sheets, e.g. capabilities, organisations, interfaces, IT components | Meta-model (11), impact analysis (10) |
| **Tabs** | Subscriptions, comments, metrics and surveys, change history | Maintenance concept (11) |
| **Type and subtype** | Template per type; subtypes, e.g. business application, deployment, microservice | Granularity (11) |

::: source
Own compilation based on SAP LeanIX (n.d.-b, n.d.-j).
:::

::: notes
The documentation calls a fact sheet a single-page repository for the essential details of one object. Walk through the application "Fare back-end" of Rhein-Neckar Mobil Group as if it were a fact sheet: subtype business application; life cycle active, phase-out planned; functional fit high, technical fit low (→ migrate, session 13); relations to the capability "payment and revenue management", the organisation "bus and rail", interfaces to the ticket device software and the ERP, IT component "server in data centre 1". Ask: which attribute groups of the session 11 fact sheet are here, and which values come from other sessions? (Criticality from the BIA, session 8; cost from IT controlling, session 4.)
:::

---

# Who Keeps the Data Right?

::: columns
**Subscriptions: roles per fact sheet**

- **Responsible**: keeps the fact sheet up to date; several possible
- **Accountable**: overall accountability, usually the business side; only one
- **Observer**: informed about changes, can take part in surveys
|||
**Quality seal: is the data confirmed?**

- **Approved** by a responsible or accountable subscriber
- **Breaks** when someone else changes the data — "check needed"
- Can **expire** after a set period, e.g. three months
- Plus a **completeness** score per fact sheet
:::

::: callout
Tools turn the **maintenance concept** of session 11 into daily routine: owners, triggers and quality checks.
:::

::: source
Own wording based on SAP LeanIX (n.d.-a, n.d.-f, n.d.-i).
:::

::: notes
Link to session 11: a maintenance concept needs owners, update triggers and quality KPIs. Here the owner roles are subscriptions, the triggers are seal breaks and expiry periods, and the KPIs are completeness and the share of approved fact sheets. The accountable role must be switched on by an administrator; admins can also enable optional seal states such as draft and rejected. Ask: who should be responsible and who accountable for the fare back-end fact sheet at Rhein-Neckar Mobil Group? (Responsible: IT owner in Group IT; accountable: business owner, e.g. head of revenue management.) Link to session 3: this is a RACI-like assignment of decision rights for data.
:::

---

# Reports: One Repository, Many Views

![Own schematic drawing of four report types fed by one repository of fact sheets and relations, with example data of Rhein-Neckar Mobil Group. Landscape report: capabilities sales and ticketing, payment and revenue, operations with the applications that support them, fare back-end and revenue sharing database marked for phase-out. Matrix report: capabilities as rows and business units bus and rail, car sharing, maintenance as columns, with the applications in the cells. Portfolio report: functional fit against technical fit with the TIME quadrants; car-sharing app invest, fare back-end migrate, workshop system tolerate, old intranet eliminate. Roadmap report: life-cycle bars for fare back-end, new fare platform and ERP bus and rail from 2027 to 2030. Not product screenshots](img/eamtool-reports.png){width=70%}

::: source
Own illustration based on SAP LeanIX (n.d.-g, n.d.-d, n.d.-h); own example data.
:::

::: notes
The key idea: reports are generated from the fact sheets and their relations; nobody draws them by hand. Each report can be filtered and coloured by a "view" (e.g. life cycle, business criticality, functional fit) — like the heat maps of session 12. The matrix report correlates three fact sheet types: applications in the cells, related types on both axes. The roadmap report places applications, IT components or initiatives on a timeline using their life-cycle dates. The documentation also lists cost reports, circle maps and world maps; diagrams (free-form, e.g. data flows) complement the reports. Ask: which of the session 13 views is which report here? (Landscape map → landscape or matrix report; TIME → portfolio report; roadmap → roadmap report.)
:::

---

# Which Report Answers Which Question?

| Stakeholder question | Report | Coloured by (view) |
|---|---|---|
| Which applications support "payment and revenue management"? | Landscape | Life cycle |
| Which units use which applications for the same capability — where is redundancy? | Matrix | Business criticality |
| Which applications should we invest in, migrate, tolerate or eliminate? | Portfolio | Functional and technical fit |
| When will which application be replaced, and what overlaps? | Roadmap | Life cycle |
| What do the applications of a capability cost per year? | Cost report | Running cost |

::: source
Own compilation based on SAP LeanIX (n.d.-g, n.d.-d, n.d.-h); own example questions.
:::

::: notes
Exam relevance: not the product names, but the principle — a stakeholder concern (session 10, ISO/IEC/IEEE 42010) determines the viewpoint, and the tool generates the view. Ask students for a question from their own company and which report would answer it. Typical answer quality issue: the report is only as good as the relations behind it — if nobody linked applications to capabilities, the landscape report is empty.
:::

---

# Modelling Guidelines in the Tool {.optional}

- **Start small**: use the default meta-model and fields before adding new ones — every addition must be maintained
- **Think backwards**: decide which reports you need, then which data
- **Low granularity first**; hierarchies of about **two to three levels** with roughly **five to ten items** per level
- **Few tags**, used for temporary statuses rather than permanent structure
- **Write down** modelling decisions so that similar things are modelled alike

::: source
Own wording based on SAP LeanIX (n.d.-c) and Hanschke (2023).
:::

::: notes
Self-study. The vendor's own guidelines repeat the lessons of session 11: collect for a purpose, keep the meta-model lean, fix granularity in modelling guidelines (Hanschke, 2023, recommends binding modelling guidelines as part of the EAM rule set). The two-to-three-level rule matches the capability map of session 12 (level 1 and level 2, sometimes level 3).
:::

---

# Hands-on: The On-Demand Bus Pilot in the Tool {.exercise}

**Case:** *Rhein-Neckar Mobil Group* prepares its **on-demand bus pilot** in two rural districts from 2028 (sessions 16 and 17). The two architects want to record it in their EAM tool. They collected:

| | |
|---|---|
| a | The SaaS **on-demand platform** (booking, routing, driver tablets) |
| b | The capability **on-demand trip management** |
| c | The **integration platform** and its **booking API** to the customer master |
| d | The vendor of the on-demand platform; the **EU cloud region** it runs in |
| e | The **phone booking team** and the unit **bus and rail** |
| f | The goal **pilot in operation from 2028** and the project **integrate the on-demand platform** |
| g | **Trip requests** and **vehicle positions** as data |

::: notes
Pairs. If a demo workspace exists, pairs create the fact sheets there; otherwise they use printed fact sheet templates (one A4 page per fact sheet: header with name, type, subtype, completeness, seal; body with life cycle, fit, criticality; relations; subscriptions). Read the case together (2 min); tasks on the next slide. The case deliberately reuses the model of session 17 so that students can compare ArchiMate elements with fact sheet types.
:::

---

# Hands-on: Your Tasks {.exercise}

1. Assign each item a–g to a **fact sheet type** of the meta model.
2. Fill the fact sheet of the **on-demand platform**: subtype, life cycle with dates, functional and technical fit, criticality, **four relations**.
3. Assign **responsible**, **accountable** and **observer** for this fact sheet. When should its quality seal be checked again?
4. The district councils ask: "Which applications does the pilot use, and when are they live?" The works council asks: "Where are vehicle positions stored?" Which **report** or **diagram** answers each question?
5. Which information from the case is **missing** to answer both questions reliably?

::: notes
About 30 min pair work + 15 min plenary. Expected answers (several defensible):
1 a application (subtype business application); b business capability; c application (integration platform; accept IT component if argued as middleware product) and interface (booking API); d provider (vendor) and IT component (cloud service of the EU region); e organization (both; the phone booking team as a sub-unit or user group of bus and rail); f objective (goal) and initiative (project); g data object (trip request, vehicle position).
2 Subtype business application; life cycle: plan until 2027, phase-in early 2028, active from the pilot start (end date open or pilot end); functional fit: not yet rated or "expected high"; technical fit: to be assessed (SaaS, EU region); criticality: medium during the pilot (phone booking as fallback), later high; relations: supports "on-demand trip management", used by "bus and rail" and the phone booking team, provides/consumes the booking API via the integration platform, creates "trip request" and "vehicle position", runs on the IT component "EU cloud region" offered by the vendor, affected by the initiative "integrate the on-demand platform".
3 Responsible: IT owner of the pilot (e.g. product owner in Group IT); accountable: business owner (head of the on-demand pilot in bus and rail); observers: data protection officer, architects, perhaps the works council liaison. Re-check: at go-live, after the pilot evaluation and at the latest after a fixed period (e.g. three months), or when the integration changes.
4 District councils: roadmap report filtered on the initiative or the capability (applications with life-cycle dates); works council: a data-flow diagram or the data object fact sheet "vehicle position" with its relations to applications and the IT component/region — complemented by the processing record under GDPR (session 7), which the tool does not replace.
5 Missing: life-cycle dates, which applications store vehicle positions and for how long, owners, the hosting location details of the driver tablets' data, retention rules. Lesson: the tool answers questions only if someone maintained the relations — and some questions (purpose, retention) belong to data protection documentation.
:::

---

# Limits of EAM Tools {.optional}

- **Tool ≠ EAM**: without questions, owners and decisions, a tool is an expensive list
- **Garbage in, garbage out**: reports look precise even when the data is old
- **Over-modelling**: every new field and type must be maintained by someone
- **Adoption**: business owners must find it useful, or they stop updating
- **Lock-in and cost**: licences per user, export options, contract exit (session 15)

::: source
Own wording based on Roth et al. (2013) and Hanschke (2023).
:::

::: notes
Self-study. Roth et al. (2013) report that practitioners struggle with documenting the EA and keeping it current, even with frameworks in place. A tool helps with the "how" of maintenance, not with the "why". Good practice: publish a few reports that management really uses (e.g. the TIME portfolio in the yearly IT planning, session 4) — use creates the pressure that keeps data current.
:::

---

# Course Synthesis {.section}

How IT management and EAM fit together

---

# How It All Fits Together

![Own illustration of the course as one system. At the top: strategy and alignment (sessions 2 and 12) and governance (IT governance, COBIT, ISO/IEC 38500 in session 3; architecture governance in session 16). In the middle, plan, build and run: plan with EA foundations, landscape planning, TIME, roadmap and the TOGAF ADM (sessions 10, 13 and 16); build and change with project portfolio and business cases, integration and sourcing (sessions 4, 14 and 15); run with service management, ITIL 4, incident, problem, change and SLA (sessions 5 and 6); feedback from run to plan: incidents, costs, risks, technical fit. Across plan, build and run: IT controlling (session 4). Below: risk and compliance (7), security and continuity (8), quality (9). At the base: the shared information base of EA repository and meta-model (11), ArchiMate views (17), EAM tools such as SAP LeanIX (18) and the CMDB (6)](img/course-synthesis.png){width=74%}

::: source
Own illustration based on Krcmar (2015), Ahlemann et al. (2012) and Hanschke (2023).
:::

::: notes
Read the figure top-down. Strategy and governance direct (session 1: strategic IT management; session 3: evaluate – direct – monitor). Plan – build – run (session 3) is the operating logic: EAM plans the landscape, the portfolio and projects build it, service management runs it — and feedback from operations (incidents, problems, costs, technical fit) flows back into planning. IT controlling measures across the whole chain. Risk, compliance, security and quality are not separate silos but requirements on every step. The shared information base is what makes the parts work together: the BIA needs the dependencies from the repository (session 8), APM needs costs from controlling (session 4), change enablement updates the CMDB (session 6). Krcmar (2015) is the frame of session 1: management of the information economy, information systems and ICT, plus cross-level management tasks; Ahlemann et al. (2012) for embedding EAM into planning, projects and operations.
:::

---

# One Decision Through the Whole Course

**Decision:** replace the 14-year-old **fare back-end** of Rhein-Neckar Mobil Group (session 13: *migrate*)

| Lens | Question | Session |
|---|---|---|
| Strategy and alignment | Does it enable the mobility app and the strategy? | 2, 12 |
| Governance | Who decides — steering committee, architecture board? | 3, 16 |
| Controlling | Business case, NPV, run vs. change cost | 4 |
| Architecture | TIME, target landscape, roadmap, ArchiMate views | 13, 16, 17 |
| Integration and sourcing | APIs instead of nightly files; build, buy or SaaS? | 14, 15 |
| Service, risk, security, quality | Change, SLA; GDPR; BIA, RTO; ISO/IEC 25010 | 5–9 |

::: source
Own example; the instruments are cited in the decks of the sessions named.
:::

::: notes
Walk through the rows with the class, asking for one concrete statement per lens: alignment — the fare back-end blocks the mobility app (technology transformation perspective); governance — investment decision by the IT steering committee, architecture compliance review by the architecture board; controlling — business case with NPV and owned benefits, run cost of two specialists; architecture — migrate, transition states, gap; integration — event-based sales data instead of the nightly file to the ERP; sourcing — standard fare software as SaaS vs. own development (strategic importance of tariffs); service — normal change with CAB-like review, new SLA with the fare platform vendor (underpinning contract); risk and compliance — payment data, GDPR, NIS2 as transport operator; security — BIA: RTO for ticket sales, store-and-forward on the devices; quality — measurable quality requirements for the new system. This is the type of thinking an integrated case question expects: choosing the instruments that fit the problem.
:::

---

# Recurring Ideas Across the Course

- **Direct vs. execute**: governance decides who decides; management decides and delivers (3, 16)
- **Cycles everywhere**: PDCA (9), evaluate – direct – monitor (3), ISO 31000 (7), the ADM (16), continual improvement (5)
- **Tailor, don't copy**: ITIL, COBIT, TOGAF and tools are toolboxes
- **For a purpose**: collect data and draw views for stakeholder questions (10, 11, 17)
- **Value, not technology**: services, capabilities and business cases speak the language of the business (4, 5, 12)
- **People and ethics**: owners, works council, data protection — EAM is communication (7, 11)

::: source
Own summary of the course.
:::

::: notes
Ask students to add one idea of their own. These patterns help in the exam: if a question asks to "assess" or "recommend", these ideas are often the basis of a good justification (e.g. "tailor TOGAF to a two-person team", "collect only what answers the board's question").
:::

---

# Exercise: Trace One Decision {.exercise}

**Decision:** *Rhein-Neckar Mobil Group* wants to **retire data centre 1 within three years** (session 15) and move its applications to the cloud or the second data centre.

Each group takes **two lenses** and answers:

1. Which **instrument** from the course do you use, and **why**?
2. What **information** do you need — and where in the **EAM tool** would you find it?
3. Which **risk** or **conflict** do you see with another lens?

Lenses: strategy and alignment · governance · controlling · landscape planning · integration · sourcing · service management · risk and compliance · security and continuity · quality

::: notes
Groups of 4–5, 20 min work + 10 min plenary; assign lenses so that every lens is covered once. Expected answers (examples): strategy — does the move support the strategy (cost, resilience, mobility platform)? alignment perspective technology transformation. Governance — steering committee decides the investment, architecture board the principles (cloud first? EU region), CIO accountable. Controlling — business case: one-off migration cost vs. saved data centre cost; run vs. change; chargeback changes from fixed costs to consumption. Landscape planning — TIME for each application in data centre 1 (rehost, replatform, replace, retire), roadmap with transition states; tool: roadmap report and fact sheets with IT component "data centre 1". Integration — which interfaces depend on co-location (nightly files, shared databases); tool: interface fact sheets. Sourcing — IaaS, PaaS or SaaS per application; vendor management, exit clauses; data location. Service management — changes (normal changes in waves), SLAs and OLAs with the cloud provider (underpinning contracts). Risk and compliance — NIS2 duties, GDPR for passenger data, DORA does not apply (not a financial entity). Security and continuity — BIA: RTO/RPO of ticketing and dispatching; new continuity solutions in the cloud; ISMS scope changes. Quality — performance efficiency and reliability requirements (ISO/IEC 25010) for migrated systems. Conflicts: cost vs. resilience; speed vs. works council (monitoring tools in the cloud); controlling wants fixed budgets, cloud costs vary. Lesson: the tool provides the data (which applications run where, who owns them, which interfaces), the instruments provide the method.
:::

---

# Exam Q&A {.section}

Question types, how to approach them, and your questions

---

# Practice Question Types

| Type | Typical operator | A good answer … |
|---|---|---|
| **Recall** | Name, list, define | is precise and complete; uses the course terms |
| **Explain and distinguish** | Explain, distinguish, compare | names the criterion of the difference and gives an example for each side |
| **Apply to a case** | Apply, classify, draw, model | uses facts from the case text, not generic examples |
| **Calculate** | Calculate, determine | shows the formula, the steps and the unit, then interprets the result |
| **Assess and recommend** | Assess, evaluate, recommend, justify | takes a position, weighs arguments, refers to the case, states one limit |

::: callout
These are **practice** question types used in the worksheets. They are not taken from any exam.
:::

::: notes
Exam format details (duration, permitted aids, number of tasks) are announced by the lecturer and the examination office; MODULE.md still lists them as an open question — fill in the official information here before the first run in 2028. Point out the worksheets: every worksheet of the course contains an exam-style practice task with a marking guide, and today's worksheet is a mixed revision set. Do not make statements such as "this will be in the exam".
:::

---

# How to Approach a Case Question

1. **Read the operator**: "name" asks for a list, "assess" for a judgement with reasons
2. **Mark the case facts** that matter: numbers, deadlines, problems, stakeholders
3. **Choose the concept** from the course that fits — and name it
4. **Apply** it with the case facts; one fact per argument
5. **Conclude**: answer the question that was asked, then check the **points** — roughly one argument per point

::: callout
Common mistakes: listing theory without the case · answering a different question · no justification for a recommendation · drawings without labels or legend
:::

::: notes
Show the structure "claim – reason – case fact" on the board: "The fare back-end belongs in *migrate* (claim), because it is business-critical but technically weak (reason): it is 14 years old and only two developers know it (case fact)." Discuss time management in general terms: read all tasks first, start with what you know, keep the points in mind. Drawings (capability map, TIME portfolio, ArchiMate view, landscape map): label axes and elements, add a short legend, keep it readable.
:::

---

# Worked Practice Example 1: Explain and Distinguish

*Practice example — not from an exam.*

::: callout
A municipal utility runs water, energy and public swimming pools. Its new CIO says: "The architecture board decides which projects we fund." Explain the difference between **IT governance** and **IT management**, and assess the CIO's statement. (4 points)
:::

- What does **each term** mean — with one example from the utility?
- Which **body** should decide on project funding, and which on architecture compliance?
- What is your **assessment**?

::: source
Practice example based on sessions 3 and 16.
:::

::: notes
Let pairs write an answer in 5 min, then show the model answer and the marking logic. Model answer: IT governance defines decision rights, accountability and the evaluate – direct – monitor cycle for IT, set by the board and top management (1 point; e.g. the supervisory board of the utility sets that IT investments above a threshold go to the steering committee). IT management makes and executes decisions within this frame — plan, build, run (1 point; e.g. the CIO plans the smart meter rollout). Assessment (2 points): the statement mixes up bodies — project funding is a portfolio and investment decision of the IT steering committee or board-level investment committee (sessions 3 and 4); the architecture board reviews compliance with principles and standards and can recommend or block designs, grant dispensations, but does not fund projects (session 16). Better: the architecture board gives an architecture assessment as input to the steering committee's funding decision. Marking: one point per correct definition with example, two points for a reasoned assessment that names the correct body for each decision.
:::

---

# Worked Practice Example 2: Apply and Recommend

*Practice example — not from an exam.*

::: callout
A regional bakery chain (40 shops) uses a 15-year-old checkout system: cashiers like it, but the vendor ends support next year and it cannot accept mobile payments. A cloud checkout is offered at €1,200 per shop and year. Classify the system using the **TIME** model and recommend a **sourcing** option. Justify with two arguments each. (6 points)
:::

::: notes
Pairs 8 min, then model answer. TIME (3 points): functional fit medium to high today (cashiers like it, core function of every shop) but falling (no mobile payments); technical fit low (old, vendor support ends) → **migrate** (keep the function, move to a new platform); 1 point for the category, 1 point per dimension with a case fact. Accept "eliminate" only if the student argues that the function moves to a new application and names this. Sourcing (3 points): recommendation SaaS cloud checkout (buy, standard function, not differentiating for a bakery, no own IT skills, vendor handles updates and payment standards); cost: 40 × €1,200 = €48,000 per year — compare with current licence and maintenance costs and one-off migration (1 point for showing the calculation and that it needs a comparison); one risk or limit: dependence on internet connectivity → offline mode required in the contract, data location, exit clause (1 point). Marking: 1 point per correct, case-based argument; the recommendation without justification earns no point. Possible variant for discussion: what changes if the bakery wants to use checkout data for its own loyalty app? (integration via API; data access in the contract.)
:::

---

# Worked Practice Example 3: Calculate and Interpret

*Practice example — not from an exam.*

::: callout
An online pharmacy promises 99.8 % availability for its shop, measured 24/7 over a 30-day month. Last month the shop was down for 50 minutes. Its 12 applications are connected point-to-point with up to one interface per pair.
:::

1. Was the target met? (2 points)
2. How many interfaces are possible at most, and how many connections would an integration platform need? (2 points)

::: notes
Model answer. 1: agreed service time 30 × 24 h = 720 h = 43,200 min; allowed downtime 0.2 % × 43,200 min = 86.4 min; actual 50 min → availability (43,200 − 50) ÷ 43,200 = 99.88 % → target met (1 point for the calculation with formula, 1 point for the interpretation, e.g. "met, but one outage of 90 minutes would already break it — agree a maximum single outage", session 6). 2: n(n−1)/2 = 12 × 11 / 2 = 66 possible interfaces; with a hub about 12 connections, one per application (1 point each); interpretation: the mapping logic does not disappear, it is concentrated and visible (session 14). Calculation tips: always write the formula first, then the numbers, then the unit — partial points for the method even if a number is wrong.
:::

---

# Your Questions

We go through the questions you brought, clustered by topic.

- Which **concepts** are still unclear?
- Which **differences** do you mix up?
- Which **case tasks** from the worksheets would you like to discuss?

::: callout
All **core slides** of sessions 1–18 are relevant for your revision; slides marked **optional** are self-study.
:::

::: notes
Use the clustered question list from the recap. Prioritise questions asked by several students. For each, answer briefly and point to the session and worksheet task where it is practised. Typical clusters from experience with such modules: incident vs. problem; SLA vs. OLA vs. underpinning contract; RTO vs. RPO vs. MTPD; governance vs. management; capability vs. process; TIME dimensions; TOGAF phases; ArchiMate serving direction. Do not answer questions of the type "will X be in the exam?" beyond the callout. If time remains, let students work on worksheet 18 task 6 in pairs.
:::

---

# Key Takeaways

- **EAM tools** store the architecture in a repository with a **meta-model** and generate **views** for stakeholders; they make an EA practice scalable but do not replace it
- **SAP LeanIX** organises the architecture in **fact sheets** of twelve types in four layers, kept current with **subscriptions** and a **quality seal**, and visualised in **reports**
- Choose a tool after the **questions** and the **data**, and treat it as a **sourcing** decision
- **IT management** and **EAM** form one system: strategy and governance direct, **plan – build – run** delivers, controlling, risk, security and quality accompany, a shared information base connects
- In the exam, **apply** concepts to the case and **justify** your answers

---

# After the Course: Preparing for the Exam

- Revise the **key takeaways** of all 18 sessions and the **core slides**
- Work through the **exam-style tasks** of the worksheets **before** you look at the solutions
- Use **worksheet 18** as a mixed revision set across the course
- Explain concepts to each other with **cases from your training company**

::: callout
Thank you for your contributions and your examples from practice throughout the course.
:::

::: notes
There is no next session. Close the course: thank the students, ask for feedback on the course (format of the case exercises, worksheets, depth of the EAM part, tool walkthrough) and note it in STATUS.md for the next run. Remind them that the worksheets and their solutions are practice material and that the exam is not published anywhere in the course material.
:::

---

# References {.references}

- Ahlemann, F., Stettiner, E., Messerschmidt, M., & Legner, C. (Eds.). (2012). *Strategic enterprise architecture management: Challenges, best practices, and future developments*. Springer. https://doi.org/10.1007/978-3-642-24223-6
- Farwick, M., Agreiter, B., Breu, R., Ryll, S., Voges, K., & Hanschke, I. (2011). Requirements for automated enterprise architecture model maintenance: A requirements analysis based on a literature review and an exploratory survey. In *Proceedings of the 13th International Conference on Enterprise Information Systems (ICEIS 2011)* (Vol. 4, pp. 325–337). SciTePress. https://doi.org/10.5220/0003429203250337
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Krcmar, H. (2015). *Informationsmanagement* (6th ed.). Springer Gabler. https://doi.org/10.1007/978-3-662-45863-1
- Roth, S., Hauder, M., Farwick, M., Breu, R., & Matthes, F. (2013). Enterprise architecture documentation: Current practices and future directions. In *Proceedings of the 11th International Conference on Wirtschaftsinformatik (WI 2013)* (pp. 911–925). https://aisel.aisnet.org/wi2013/58
- SAP LeanIX. (n.d.-a). *Fact sheet subscription*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/fact-sheet-subscription
- SAP LeanIX. (n.d.-b). *Fact sheets*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/factsheets
- SAP LeanIX. (n.d.-c). *General modeling guidelines*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/general-modeling-guidelines
- SAP LeanIX. (n.d.-d). *Matrix report*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/matrix-report
- SAP LeanIX. (n.d.-e). *Meta model*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/data-model
- SAP LeanIX. (n.d.-f). *Quality seal*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/quality-seal
- SAP LeanIX. (n.d.-g). *Reports*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/reports
- SAP LeanIX. (n.d.-h). *Roadmap report*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/roadmap-report
- SAP LeanIX. (n.d.-i). *SAP LeanIX overview*. Retrieved October 22, 2026, from https://docs-eam.leanix.net
- SAP LeanIX. (n.d.-j). [TIME framework in SAP LeanIX enterprise architecture management]. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/time

SAP and LeanIX are trademarks of SAP SE. Product names are used for identification only. Diagrams in this deck are own schematic illustrations, not product screenshots.
