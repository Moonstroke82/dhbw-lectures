---
course: IT Management and EAM
session: 13
title: Strategic Planning of the IT Landscape
subtitle: As-is, target and transition landscapes · landscape maps · application portfolio management and the TIME model · roadmaps and transformation planning
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# Strategic Planning of the IT Landscape {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · why plan the landscape, as-is/target/transition 15 min · landscape maps 15 min · mini exercise "read the landscape map" 10 min · break 10 min · application portfolio management and the TIME model 25 min · mini exercise "which TIME category?" 10 min · target landscape, gap analysis and roadmap 20 min · case exercise portfolio assessment 45 min · wrap-up 5 min · ~15 min buffer.
Session 12 built the capability map of Rhein-Neckar Mobil Group and showed which capabilities need investment first. Today puts the applications onto this map (landscape map), assesses them (application portfolio management) and plans the way from the as-is to the target (roadmap). This covers the module content "strategic planning and development of the corporate IT landscape" and the methodological competence of selecting suitable methods for managing and optimising the IT landscape.
Source note for the lecturer: Hanschke (2023) treats strategic IT planning in chapter 3, the best-practice visualisations in section 5.5 (Bebauungsplan-Grafik 5.5.3, Portfolio-Grafik 5.5.4, Lifecycle-Grafik 5.5.7, Masterplan-Grafik 5.5.8, IT-Roadmap-Grafik 5.5.10), application rationalisation in 6.11, IS portfolio management in 6.15, target picture and IT roadmap in 6.16 and IS-Bebauungsplanung in 7.5.5. Keller (2017) treats the management of the application portfolio in 4.3 and 4.5 and strategic landscape planning ("strategische Bebauungsplanung") in 4.7. Section numbers checked against the tables of contents of these editions; check the text in the library copy before quoting. The TIME model is widely attributed to Gartner; the slides cite the publicly available SAP LeanIX documentation, which describes it with the two axes functional fit and technical fit. TOGAF Phases E and F are described in own words only. All maps, ratings and figures are own examples.
:::

---

# Today's Agenda

1. Recap: three applications of your company
2. Why plan the landscape: as-is, target and transition states
3. Landscape maps
4. Application portfolio management and the TIME model
5. From target landscape to roadmap
6. Case exercise: assess the application portfolio of Rhein-Neckar Mobil Group

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Why plan, as-is/target/transition (input) · 0:25 Landscape maps (input) · 0:40 Mini exercise "read the landscape map" (pairs) · 0:50 Break · 1:00 Application portfolio management and TIME (input) · 1:25 Mini exercise "which TIME category?" (pairs) · 1:35 Target landscape, gap analysis, roadmap (input) · 1:55 Case exercise (groups + plenary) · 2:40 Wrap-up · ~15 min buffer.
If the session runs long: "The health grid", "Planning in TOGAF: Phases E and F" and "Pitfalls of landscape planning" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: Three Applications of Your Company

You were asked to find out for three applications of your training company: how **old** is it, how **satisfied** are its users, and is a **replacement** planned?

- Is the **oldest** application also the **worst** one?
- Did you find an application that users **like** but IT wants to **replace** — or the other way round?
- **Who** decides whether an application is replaced, and on which basis?

::: notes
Pairs for 3 min, then collect on the board in a table: application · age · satisfaction · replacement planned (yes/no/unknown). Typical findings: an ERP system of 15–25 years that users find cumbersome but that "runs everything"; a modern SaaS tool that users like; an old custom application that only one person understands; many "unknown" answers on replacement plans. Point out two dimensions hidden in the answers: users judge **how well the application supports their work** (functional fit), IT judges **how sound the technology is** (technical fit) — age is only a hint for the second. Keep the board: these two dimensions are the axes of the TIME model later today. The question "who decides?" leads to governance (session 3) and to the project portfolio (session 4).
:::

---

# Planning the Landscape {.section}

From where we are to where we want to be

---

# Why Plan the IT Landscape?

::: columns
**Without planning**

- Each project adds its own application; little is **retired**
- Landscapes **grow**: more applications, interfaces and licences each year
- Decisions are taken **per project**, not for the whole landscape
- The landscape becomes a **brake** on new business models
|||
**With strategic planning**

- A **target picture** derived from strategy and capabilities
- An **application portfolio** that is assessed regularly
- A **roadmap** that turns the target into a sequence of steps
- Projects are **checked** against the target
:::

::: callout
Strategic landscape planning decides **which applications** the enterprise will use in future, **which it retires** and **in which order** it gets there.
:::

::: source
Own wording based on Hanschke (2023) and Keller (2017).
:::

::: notes
Hanschke (2023) describes strategic IT planning as deriving a target picture ("Ziel-Bild") and an IT roadmap from the business and IT strategy and steering the landscape towards it (chapter 3, sections 6.16 and 7.5). Keller (2017) calls the same task strategic landscape planning ("strategische Bebauungsplanung", section 4.7). Link to session 10: city planning — the zoning plan decides what may be built where; buildings are replaced one by one while the city keeps running. Link to session 12: capability-based planning said where to invest; today says what that means for the applications.
:::

---

# As-Is, Target and Transition Landscapes

| Landscape | Question | Typical content at Rhein-Neckar Mobil Group |
|---|---|---|
| **As-is** (baseline) | What do we have today? | Three ERP systems, customer data in three places, no mobility app |
| **Target** | Where do we want to be in 3–5 years? | One cloud ERP, one leading customer system, mobility app on an API platform |
| **Transition** (planned state) | What will the landscape look like at a given date on the way? | End of year 2: customer master and payment platform live, finance on the cloud ERP |

- The target is a **direction**; it is revised when the strategy changes
- Transitions must be **consistent and operable** — the business has to run with them

::: source
Own wording based on Keller (2017), Hanschke (2023) and The Open Group (2022).
:::

::: notes
TOGAF speaks of baseline, target and transition architectures: a transition architecture shows the enterprise at an architecturally significant state between baseline and target (The Open Group, 2022, Phase E). Practical point: a target that is never reached is normal — by the time the enterprise gets close, the strategy has moved on. That is why transition states with dates matter more for steering than the target itself. Each transition must work on its own: if the mobility app goes live before the payment platform, it needs a temporary interface — and temporary solutions tend to stay. Ask: which date would the CFO want to see — the target or the next transition?
:::

---

# Landscape Maps

![As-is landscape map of Rhein-Neckar Mobil Group: rows are the capabilities customer management, sales and ticketing, payment and revenue management, operations, financial management and human resources management; columns are the business units bus and rail, car sharing and vehicle maintenance. The cells show applications such as the subscription module of the bus and rail ERP, the car-sharing customer database, the ticket device software, the association app, the fare back-end, the payment provider, the car-sharing app, back-end and payment, the dispatching system and the workshop system. The three ERP systems are marked as phase-out planned; payroll is one group-wide external service; the planned mobility account has no application yet](img/eam-landscape-map.png){width=84%}

::: source
Own illustration based on Hanschke (2023); own example.
:::

::: notes
A landscape map ("Bebauungsplan-Grafik", Hanschke 2023, section 5.5.3) places applications in a matrix of two business dimensions — here capabilities × business units; processes, products or locations are also common. A third dimension is shown by colour: here the life cycle status; it could also be the TIME category, the cost or the technical fit. Reading it: redundancy shows as several boxes in one row (financial management: three ERPs); fragmentation as one capability spread over unrelated systems (customer management); gaps as an empty cell where support is needed (mobility account); shared applications as boxes that span columns (payroll). Empty cells in vehicle maintenance are not gaps — the unit has no customers. Tip: the map only shows what is in the repository (session 11); if the data are poor, the map is wrong in a convincing way.
:::

---

# Other Views of the Landscape

| View | Shows | Answers |
|---|---|---|
| **Landscape map** | Applications in a matrix of capabilities, units or processes | Where are redundancies, gaps, fragmentation? |
| **Interface map** | Applications as nodes, interfaces and data flows as lines | What is affected if we replace one application? |
| **Portfolio chart** | Applications in a 2 × 2 grid, e.g. by business value and technical fit | Where do we invest, where do we retire? |
| **Life cycle and roadmap chart** | Applications or projects on a time axis | When does what change, and what depends on what? |

::: callout
The same repository, different **views for different stakeholders** — a board wants the portfolio and roadmap, a project manager the interface map.
:::

::: source
Own compilation based on Hanschke (2023) and Keller (2017).
:::

::: notes
Hanschke (2023, section 5.5) describes a set of best-practice visualisations, among them the landscape map, portfolio, life cycle, masterplan and IT roadmap charts; Keller (2017, section 4.5) describes evaluations of the application portfolio. Link to session 10: stakeholder, concern, viewpoint, view. Interface maps return in session 14 (integration). EAM tools such as LeanIX (session 18) generate these views from the repository; drawing them by hand in PowerPoint is the classic way to make them outdated within weeks.
:::

---

# Mini Exercise: Read the Landscape Map {.exercise}

Use the landscape map of *Rhein-Neckar Mobil Group* to answer:

1. Find one **redundancy**, one **fragmented** capability and one **gap**.
2. Why are the empty cells in **vehicle maintenance** not a problem?
3. The **payment provider** fails. Which capabilities and units are affected — and what can the map **not** tell you?
4. Which **colour lens** would you choose for the CFO, and which for the CISO?

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 redundancy: three ERP systems for financial management (also two payment paths: payment provider and car-sharing payment); fragmentation: customer management (ERP subscriptions and car-sharing customer database, plus the association app outside the group); gap: mobility account / mobility app. 2 The unit has no end customers and sells no tickets — no need for support; a gap is an empty cell where the business needs support. 3 Payment and revenue management in bus and rail (on-board card payments); the map does not show interfaces and dependencies (does the car-sharing payment use the same provider? does the fare back-end need the provider for settlement?), nor criticality or recovery times — that needs the interface map and the BIA (session 8). 4 CFO: running cost per application or number of applications per capability (redundancy = cost); CISO: protection requirements or technical fit/vendor support status (unsupported software = risk). Lesson: a map answers some questions well and others not at all.
:::

---

# Application Portfolio Management {.section}

Assessing applications to decide what to do with them

---

# What Is Application Portfolio Management?

::: callout
**Application portfolio management (APM)** regularly assesses all applications of the enterprise by their **business value**, **technical state**, **cost** and **risk** — and derives a strategy for each: invest, keep, migrate or retire.
:::

- Treats applications like a **portfolio of investments**, not one by one
- Typical goals: **rationalisation** (fewer, simpler applications), lower **running cost**, less **risk** from outdated technology, room for **innovation**
- Differs from the **project portfolio** (session 4): APM manages what **exists**, project portfolio management decides what is **changed**

::: source
Own wording based on Riempp and Gieffers-Ankel (2007), Keller (2017) and Hanschke (2023).
:::

::: notes
Riempp and Gieffers-Ankel (2007) describe application portfolio management as a decision-oriented view of enterprise architecture: the portfolio of applications is assessed along business and technical dimensions to support decisions about investment and retirement. Keller (2017, section 4.3) and Hanschke (2023, sections 6.11 and 6.15) describe the same instrument for the German context ("Anwendungsportfolio", "IS-Portfoliomanagement"). The two portfolios are linked: APM produces candidates (migrate the fare back-end), the project portfolio (session 4) decides whether and when a project is funded. Typical figure from practice: a large share of the IT budget goes into running existing applications — APM is where "run" money is freed for "change".
:::

---

# Assessing an Application: Two Dimensions

::: columns
**Functional fit — business value**

- How well does it support the **processes and capabilities**?
- Importance of the supported **capabilities** (heat map, session 12)
- **User satisfaction**, number of users
- Fit with **future** requirements, e.g. the mobility app
- Rated by the **business owner**
|||
**Technical fit — technical state**

- **Age** and maintainability, vendor support status
- Fit with **technology standards** and target platforms
- Stability, security, performance (session 9)
- **Know-how**: how many people can still change it?
- Rated by the **IT owner**
:::

::: callout
Ratings need **defined criteria and scales** — otherwise each owner rates their own application "high".
:::

::: source
Own wording based on Weill and Vitale (1999), SAP LeanIX (n.d.) and Hanschke (2023).
:::

::: notes
Weill and Vitale (1999) had senior managers rate each application on importance, investment, technical quality, use and management value, and plotted technical quality against management value. EAM tools such as SAP LeanIX use functional fit and technical fit as attributes of the application fact sheet (session 11). Practical tips: use a four-point scale (no neutral middle); write down what "high" means for each criterion (e.g. technical fit "high" = vendor-supported version, on a standard platform, at least two people can maintain it); let business and IT owners rate separately and discuss differences. Link to the preparation task: age and satisfaction are only two of the criteria — an old system can be technically sound, a new one can be poorly integrated.
:::

---

# The TIME Model

::: columns
![TIME model as a 2 by 2 portfolio with technical fit on the horizontal axis and functional fit on the vertical axis: Migrate for high functional and low technical fit, Invest for high functional and high technical fit, Eliminate for low functional and low technical fit, Tolerate for low functional and high technical fit. Example applications of Rhein-Neckar Mobil Group: car-sharing app and ticket device software in Invest, fare back-end and ERP bus and rail in Migrate, workshop system in Tolerate, revenue sharing database and old intranet in Eliminate](img/eam-time-model.png){width=88%}
|||
- **Invest**: develop further
- **Migrate**: keep the function, new platform
- **Tolerate**: keep with minimal spend
- **Eliminate**: retire or consolidate
- The quadrant suggests a **direction**, not a decision
:::

::: source
Own illustration based on SAP LeanIX (n.d.) and Weill and Vitale (1999); own example ratings.
:::

::: notes
TIME stands for tolerate, invest, migrate, eliminate. The model is widely attributed to Gartner; we use the description in the SAP LeanIX documentation, which classifies applications by functional fit and technical fit. Walk through the quadrants: Invest — valuable and technically sound, develop further (car-sharing app). Migrate — valuable but technically weak: keep the function, move it to a new platform (fare back-end: a 14-year-old own development that only two developers know; ERP bus and rail → cloud ERP). Tolerate — technically fine but of limited business value: keep it running with minimal spend, no new features (workshop system). Eliminate — neither: retire or consolidate into another application (revenue sharing database, old intranet). Important: "eliminate" retires the application, not necessarily the function — revenue sharing is still needed and moves to another application.
:::

---

# From Quadrant to Decision

| Category | Typical action | What it needs on the roadmap |
|---|---|---|
| **Invest** | Develop further; candidate for reuse across units | Budget for new features; architecture principles |
| **Migrate** | Move the function to a new platform or standard software | Replacement project, data migration, interfaces |
| **Tolerate** | Keep running, no new features, minimal spend | Review date; watch support and cost |
| **Eliminate** | Retire, move users and data to another application | Decommissioning plan, archiving, contract end |

- Before acting, add **cost**, **risk** and **dependencies**: a cheap "eliminate" candidate with ten interfaces is not cheap to retire
- **Contract end dates** and vendor support often set the **timing**

::: source
Own wording based on SAP LeanIX (n.d.), Hanschke (2023) and Keller (2017).
:::

::: notes
The TIME category is an input to a decision, not the decision itself. Typical third and fourth lenses: running cost per year (bubble size in a portfolio chart), risk (protection requirements, vendor support ending), number of interfaces (dependencies — session 14), number of users. Decommissioning is a project of its own: archiving data with retention periods (GDPR deletion vs. retention duties under commercial and tax law), terminating contracts, informing users, switching off interfaces. Many landscapes grow because nobody budgets for switching off. Link to session 4: the business case for one cloud ERP was exactly a "migrate" decision with costs and benefits.
:::

---

# The Health Grid {.optional}

- An early research study of an applications portfolio: managers of a manufacturing business unit rated each application on **five attributes**: importance, investment, technical quality, use, management value
- Plotting **technical quality** against **management value** gave a "health grid" that made the state of the portfolio visible and **discussable**
- Findings: most applications **needed attention**; investment in an application was **not related** to its management value

::: callout
The same idea as TIME: two dimensions make a portfolio **comparable** — and the ratings start the **discussion**, they do not end it.
:::

::: source
Own summary based on Weill and Vitale (1999).
:::

::: notes
Self-study. Weill and Vitale (1999) studied the most profitable business unit of a large process manufacturer with 18 systems; senior managers rated them, and the authors discuss strengths and weaknesses of the grid and the changes the firm made afterwards. The finding that investment and management value were not related is a classic argument for APM: money flows to applications by habit, not by value. Exam point: be able to name the two dimensions and why a portfolio view is better than single decisions.
:::

---

# Mini Exercise: Which TIME Category? {.exercise}

Classify each application of *Rhein-Neckar Mobil Group* with the **TIME** model and name the **next step**.

1. **Staff app** for duty rosters: one year old, cloud, drivers love it, planned for more functions
2. **Document archive** for scanned maintenance records: ten years old, vendor-supported, rarely used, no new requirements
3. **Excel macro** that calculates special fares: maintained by one person in sales, used every month
4. **Lost-property database**: 15 years old, Access, two users, the function is also offered by the new customer service tool
5. **Parking garage booking**: a pilot built by a student for the mobility app, no owner, used by 40 customers

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 Invest — high functional and technical fit; next step: budget for new functions, make it the standard staff app. 2 Tolerate — technically fine, low business value; keep running cheaply, review at contract end, consider moving the archive into the document management of the cloud ERP. 3 Migrate — high business value (used for real fares every month), poor technical fit (one person, Excel, no controls — also a compliance risk, session 7); next step: move the logic into the fare back-end or its successor. 4 Eliminate — low value, poor technology, function exists elsewhere; next step: migrate data, retire. 5 Debatable: functional fit potentially high for the partner strategy (session 12), technical fit low (no owner, pilot quality) → Migrate if the board wants partner parking (rebuild properly on the API platform), Eliminate if not; first step: assign an owner and decide. Lesson: the category depends on the ratings, and the ratings depend on the strategy.
:::

---

# From Target to Roadmap {.section}

Target landscape, gap analysis and transformation planning

---

# Deriving the Target Landscape

::: columns
**Inputs**

- Strategy and business model (session 12)
- Capability map and heat map: where to invest
- TIME results of the application portfolio
- **Architecture principles** and technology standards
|||
**Example principles at Rhein-Neckar Mobil Group**

- One **leading system** per business object, e.g. customer, fare
- **Standard software** before own development, except in differentiating capabilities
- **API first**: new applications offer their functions via the API platform
- **Cloud first** for new applications, data stored in the EU
:::

::: callout
The target landscape is the **landscape map of the future**: it shows which application supports which capability — and which applications are gone.
:::

::: source
Own wording based on Hanschke (2023), Keller (2017) and The Open Group (2022).
:::

::: notes
Hanschke (2023) describes the target picture together with guard rails ("Leitplanken", sections 3.4 and 3.5) — principles and standards that the target must follow; Keller (2017, section 4.7) describes how a target landscape is worked out. Principles are the link to IT governance (session 3: IT principles as one of the five key decisions). A good principle has a rationale and implications, and it can be checked in a project review (session 16). The principles here are own examples; "cloud first" must be reconciled with the BCM requirements of the ticketing service (session 8) — on-board devices still need to work offline.
:::

---

# Gap Analysis: From As-Is to Target

| Gap type | Example at Rhein-Neckar Mobil Group | Leads to |
|---|---|---|
| **New** — needed, does not exist | Mobility account, API platform | Build or buy project |
| **Replace** — function stays, application changes | Three ERPs → one cloud ERP; fare back-end → new fare and revenue platform | Migration project |
| **Consolidate** — several become one | Customer data from three places into one customer master | Data migration, interfaces |
| **Retire** — function no longer needed or moved | Revenue sharing database, old intranet | Decommissioning |
| **Keep** — unchanged | Ticket device software, dispatching system | No project, regular review |

::: source
Own wording based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
Gap analysis compares baseline and target element by element; TOGAF uses it in each architecture domain and consolidates the gaps in Phase E into work packages. The table is the bridge from the landscape maps to projects: each gap becomes a candidate work package with costs, benefits and dependencies. Check the whole chain for each gap: business (process changes, training), data (migration, leading system), application, technology (hosting) — the four domains of session 10. A frequent omission: the "retire" row — without a decommissioning project, the old system keeps running "just in case".
:::

---

# The Roadmap

![Landscape roadmap of Rhein-Neckar Mobil Group over three years in half-year steps: four states as-is, transition 1, transition 2 and target; four swimlanes. Customer and mobility app: customer master and consent, then mobility app release 1 as the red milestone, then partner offers. Integration and technology: API platform, later retire data centre 1. Payment and revenue: payment platform for all units, then new revenue sharing. ERP: cloud ERP for finance, then cloud ERP for maintenance. Arrows show that the mobility app depends on the customer master, the API platform and the payment platform](img/eam-roadmap.png){width=90%}

::: source
Own illustration based on Hanschke (2023) and The Open Group (2022); own example.
:::

::: notes
A roadmap shows initiatives on a time axis, grouped into swimlanes, with the landscape states they produce (Hanschke's IT roadmap and masterplan charts, section 5.5; TOGAF's architecture roadmap with transition architectures). Read the dependencies: the mobility app cannot start release 1 before the customer master, the API platform and the payment platform exist — that is why they come first, although the board only "sees" the app. Each transition is a state the group can operate: after transition 1, finance runs on the cloud ERP while maintenance still uses its old ERP — an interim interface is needed. Ask: what happens to the roadmap if the cloud ERP project is six months late?
:::

---

# Sequencing the Transformation

::: columns
**What sets the order**

- **Dependencies**: platforms and master data before the applications that use them
- **Strategic deadlines**, e.g. the mobility app
- **Risk**: end of vendor support, know-how of a single person
- **Contract ends** and licence renewals
- **Capacity**: people and budget, change load on the business units
|||
**Good practice**

- Plan **transition states** that can be operated, not only projects
- Deliver **visible value** early to keep support
- Feed the roadmap into the **project portfolio** and the budget (session 4)
- **Review** the roadmap regularly against strategy and progress
:::

::: source
Own wording based on Hanschke (2023), Keller (2017) and The Open Group (2022).
:::

::: notes
TOGAF lists factors for prioritising and sequencing work packages in Phases E and F, among them dependencies, business value, risk and the capacity of the organisation to absorb change. In practice the "capacity of the business" is the most underestimated factor: the bus and rail unit cannot change its ERP, its fares platform and its customer processes in the same half-year. A roadmap that is not in the budget is a wish list — the link to the IT steering committee (session 3) and the project portfolio (session 4) makes it binding. Typical review rhythm: yearly with the strategy and budget cycle, plus updates when major projects change.
:::

---

# Planning in TOGAF: Phases E and F {.optional}

| Phase | Purpose in own words | Typical results |
|---|---|---|
| **E: Opportunities and solutions** | Consolidate the gaps of all domains, group them into **work packages**, identify **transition architectures** | Candidate roadmap, transition architectures |
| **F: Migration planning** | Prioritise and sequence the work packages with cost, value and risk; agree with portfolio and budget | Architecture roadmap, implementation and migration plan |

::: source
Own wording based on The Open Group (2022).
:::

::: notes
Self-study; the ADM as a whole follows in session 16. Phase E is the first phase that is concerned with implementation; Phase F turns the candidate roadmap into an implementation and migration plan that is coordinated with the enterprise's other management frameworks (portfolio, budget, operations). The names of the phases and work products are given as labels; the descriptions are own words.
:::

---

# Pitfalls of Landscape Planning {.optional}

- **Ratings as politics**: owners rate their own applications high; document criteria and raters
- **Target without path**: a beautiful target picture without transitions, budget or owners
- **Forgetting the retirement**: new systems are added, old ones keep running
- **Planning in IT only**: the business units do not recognise their roadmap
- **Out of date**: maps and roadmaps that are drawn once and never reviewed

::: source
Own wording based on Hanschke (2023) and Keller (2017).
:::

::: notes
Self-study. Countermeasures: rating workshops with business and IT owners, a target picture with transition states and named initiatives in the project portfolio, decommissioning as part of every replacement project (and its business case), roadmaps built with the capability owners, and a review in the yearly planning cycle with views generated from the repository (session 11 maintenance concept). Exam point: name strengths and limits of an instrument, not just describe it.
:::

---

# Case Exercise: Assess the Application Portfolio {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–12): 3,200 employees, €410 million turnover; about 180 applications. The mobility app needs **customer management** and **customer service** across all units.

| Application | Unit | Age, technology | Users | Notes |
|---|---|---|---|---|
| Passenger information system | Bus and rail | 12 years, own development | Satisfied | Cannot deliver real-time data the app needs; one developer |
| Dispatching system | Bus and rail | 9 years, vendor standard | Satisfied | Vendor support until 2031 |
| Customer database | Car sharing | 4 years, cloud | Very satisfied | Holds car-sharing customers only |
| Complaint database | Bus and rail | 10 years, Access | Dissatisfied | No interface; data on a file server |
| Helpdesk tool (SaaS) | Car sharing | 3 years, cloud | Satisfied | Licences for 15 agents; could serve more |
| Timetable planning tool | Bus and rail | 7 years, vendor standard | Satisfied | Used by 12 planners; no link to the app |

::: notes
Read the case together (2 min). Hints if asked: the vehicle maintenance unit handles customer complaints about car damage by e-mail; the transport association app remains the association's (partner) application; running costs per year (own example figures): passenger information 140 k€, dispatching 210 k€, customer database 90 k€, complaint database 10 k€ plus an estimated 0.5 FTE of manual work, helpdesk 30 k€, timetable planning 120 k€. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. Rate each application on **functional fit** and **technical fit** (high/low) with a short reason, and place it in the **TIME** model.
2. Draw the **as-is** landscape map for the capabilities **customer management** and **customer service** across the three units. Mark one **redundancy** and one **gap**.
3. Formulate two **architecture principles** and draw the **target** landscape for these two capabilities.
4. List the **gaps** between as-is and target (new, replace, consolidate, retire, keep).
5. Sketch a **roadmap** with two **transition states**. Which **dependency** sets the order, and which **risk** would you watch?

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 Passenger information: functional high (needed every day, more so for the app), technical low (own development, one developer, no real-time) → Migrate. Dispatching: high/high → Invest or Tolerate (accept both; it works, vendor-supported, not central to the app) — "Invest" if real-time data for the app should come from dispatching. Customer database: functional high for car sharing and potential group customer master, technical high → Invest. Complaint database: low/low → Eliminate (move to helpdesk tool). Helpdesk SaaS: high/high → Invest (extend to all units). Timetable planning: functional high, technical high → Tolerate or Invest; not urgent for the app — accept "Tolerate" with the argument "keep running, no investment now".
2 Customer management: bus and rail → ERP subscription module; car sharing → customer database; maintenance → none (no end customers); association app outside. Customer service: bus and rail → complaint database; car sharing → helpdesk SaaS; maintenance → e-mail. Redundancy: two (three with e-mail) customer service solutions; two customer stores. Gap: no group-wide customer account/mobility account; no customer service across units.
3 Principles: one leading system per business object (customer); standard software/SaaS for non-differentiating capabilities; API first; data in the EU. Target: one customer master (e.g. built on the car-sharing customer database or a new CRM/customer identity platform — accept either with reasoning) for all units and the mobility app; one helpdesk for all units, connected to the customer master; real-time passenger information as a service on the API platform.
4 New: group customer master/mobility account, real-time passenger information interface; replace: passenger information system; consolidate: customer data from ERP subscriptions and car-sharing database; customer service into the helpdesk; retire: complaint database (and later the ERP subscription module); keep: dispatching, timetable planning.
5 E.g. transition 1 (first year): helpdesk for all units (quick win, cheap SaaS licence expansion), complaint database retired, customer master designed and car-sharing customers migrated; transition 2: bus and rail subscriptions migrated, mobility app on customer master, new passenger information. Dependency: customer master before the app and before migrating subscriptions; risk: the single developer of the passenger information system, data protection and works council (session 7, 11) for the customer master, change load in bus and rail during the cloud ERP project.
:::

---

# Key Takeaways

- Strategic landscape planning moves the enterprise from the **as-is** via operable **transition** states towards a **target** landscape derived from strategy and capabilities
- **Landscape maps** show applications against capabilities and units and reveal **redundancy, fragmentation and gaps**
- **Application portfolio management** assesses applications by **functional and technical fit** — plus cost and risk; the **TIME** model suggests invest, tolerate, migrate or eliminate
- **Gap analysis** turns the target into work packages; a **roadmap** sequences them by dependencies, deadlines, risk and capacity and feeds the project portfolio

---

# Next Session: Enterprise Application Integration

- Integrated information processing: why applications must exchange data
- Point-to-point vs. middleware; integration patterns
- ESB, APIs, event-driven integration, iPaaS

::: callout
**Preparation:** pick one business process of your training company and find out which **applications** exchange data along it — and **how**: file transfer, direct interface, middleware or manual re-entry?
:::

::: notes
The preparation task leads into the interface view that today's landscape map left out. The roadmap's "API platform" swimlane is the topic of session 14.
:::

---

# References {.references}

- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Riempp, G., & Gieffers-Ankel, S. (2007). Application portfolio management: A decision-oriented view of enterprise architecture. *Information Systems and e-Business Management, 5*(4), 359–378. https://doi.org/10.1007/s10257-007-0052-2
- SAP LeanIX. (n.d.). [TIME framework in SAP LeanIX enterprise architecture management]. Retrieved October 21, 2026, from https://docs-eam.leanix.net/docs/time
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Architecture development method*. Van Haren Publishing.
- Weill, P., & Vitale, M. (1999). Assessing the health of an information systems applications portfolio: An example from process manufacturing. *MIS Quarterly, 23*(4), 601–624. https://doi.org/10.2307/249491

TOGAF® is a registered trademark of The Open Group. SAP and LeanIX are trademarks of SAP SE. Diagrams in this deck are own illustrations. Frameworks are described in own words.
