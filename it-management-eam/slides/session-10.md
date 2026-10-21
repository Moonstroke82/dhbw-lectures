---
course: IT Management and EAM
session: 10
title: Enterprise Architecture Foundations
subtitle: What enterprise architecture is and why it matters · business, data, application and technology architecture · fields of action and stakeholders of EAM
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# Enterprise Architecture Foundations {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · what EA is, EA vs. EAM 15 min · why EA matters, operating models 15 min · mini exercise "symptom and goal" 10 min · break 10 min · the four domains incl. trace figure 25 min · mini exercise "which domain?" 10 min · fields of action and stakeholders of EAM 20 min · case exercise EA domains 45 min · wrap-up 5 min · ~15 min buffer.
This is the first session of Part B (enterprise architecture management, sessions 10–18). Start with a two-minute bridge: Part A asked how IT is steered (strategy, governance, controlling, services, risk, security, quality); Part B asks how the business and its IT are structured as a whole and how this structure is changed on purpose.
Copyright note for the lecturer: the TOGAF Standard and ISO/IEC/IEEE 42010 are copyrighted. The slides describe their ideas in own words; the domain names are used as labels only, no definitions are copied. Status checked in October 2026: the TOGAF Standard, 10th Edition (April 2022) and ISO/IEC/IEEE 42010:2022 are current; re-check before the first run in 2028. The German module literature (Hanschke 2023, Keller 2017) is cited without page numbers; check chapters in the library copies before quoting.
:::

---

# Today's Agenda

1. Recap: the five most important applications of your company
2. What is enterprise architecture — and what is EAM?
3. Why EA matters: goals and the operating model
4. The four domains: business, data, application, technology
5. Fields of action and stakeholders of EAM
6. Case exercise: EA domains at Rhein-Neckar Mobil Group

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 What EA is, EA vs. EAM (input) · 0:25 Why EA matters, operating models (input + discussion) · 0:40 Mini exercise "symptom and goal" (pairs) · 0:50 Break · 1:00 The four domains and the trace example (input) · 1:25 Mini exercise "which domain?" (pairs) · 1:35 Fields of action and stakeholders (input) · 1:55 Case exercise (groups + plenary) · 2:40 Wrap-up · ~15 min buffer.
If the session runs long: "Stages of architecture maturity", "Other ways to cut the domains" and "A short history: Zachman" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: Your Five Most Important Applications

You were asked to list the five most important applications of your training company.

- **Which business processes** does each application support?
- **Which data** does it hold — and which other applications need these data?
- **Who** could give you the complete list of all applications? Does such a list exist?

::: notes
Pairs for 3 min, then collect on the board in three columns: application · processes · data. Typical answers: SAP S/4HANA or another ERP (finance, purchasing, sales), Salesforce or another CRM (sales, service), Microsoft 365 (everything), a manufacturing execution or warehouse system, an HR system, a ticket tool. Question 3 is the key: most students do not know who has the complete list; some mention a CMDB, an Excel list, an EAM tool (LeanIX, Alfabet, ADOIT) or "the architect". Keep the board: the three columns are already three of today's four domains (business, application, data) — technology is missing, which is typical for business users. Question 3 also leads to session 11 (collecting EA data).
:::

---

# What Is Enterprise Architecture? {.section}

Architecture, enterprise architecture and EAM

---

# An Analogy: Building and City Planning

::: columns
**A building**

- An architect designs one building for its owner
- Plans show different **views** for different trades: floor plan, wiring, plumbing
- Building rules and standards apply
|||
**A city**

- City planning designs how many buildings, roads and supply networks fit together over decades
- A **zoning plan** sets what may be built where
- Buildings are replaced one by one while the city keeps running
:::

::: callout
A **solution architect** designs one building; an **enterprise architect** works like a city planner for the whole landscape of business and IT.
:::

::: source
Own illustration based on Hanschke (2023) and Keller (2017).
:::

::: notes
The city planning analogy is common in the German EAM literature: the term "Bebauungsplan" (zoning plan) for the application landscape plan comes from city planning, and Keller (2017) calls the planning of the future landscape "strategische Bebauungsplanung". Ask: what happens in a city without planning? Roads end nowhere, every house has its own water supply, nobody knows where the cables are — exactly the symptoms of an unmanaged IT landscape (several ERP systems, many interfaces, unknown dependencies). Limit of the analogy: an enterprise changes much faster than a city.
:::

---

# Architecture and Enterprise

::: callout
**Architecture** describes the fundamental structure of a system: its **elements**, their **relationships** to each other and to the environment, and the **principles** that guide its design and evolution.
:::

- An **enterprise** is any organisation or group of organisations with common goals: a company, a division, a public authority, a group with its partners
- **Enterprise architecture (EA)** applies this idea to the whole enterprise: strategy, organisation, processes, information, applications and technology — and how they fit together
- Architecture covers the **as-is** state, the intended **target** state and the **path** between them

::: source
Own wording based on ISO/IEC/IEEE (2022) and The Open Group (2022).
:::

::: notes
ISO/IEC/IEEE 42010 is the international standard for architecture descriptions; TOGAF refers to it and adds its own, more practical reading: the structure of components, their relationships and the principles and guidelines governing their design and evolution over time. Three words to stress: elements, relationships, principles. A list of applications is not yet an architecture; the relationships (which process uses which application, which interface carries which data) and the rules (e.g. "one master system per business object") make it one. The enterprise need not be a legal entity: Rhein-Neckar Mobil Group with its three units is one enterprise; so is the group with the regional transport association, if they plan together.
:::

---

# EA and EAM

::: columns
**Enterprise architecture (EA)**

- The **structure** itself: what exists and how it fits together
- Every enterprise **has** an architecture — planned or grown by accident
- Documented in models, maps and lists
|||
**Enterprise architecture management (EAM)**

- The **management function** that documents, plans and steers the EA
- Sets **principles** and standards, plans a **target architecture** and roadmap, and checks that projects follow them
- Links business strategy and IT implementation
:::

::: callout
EAM is not the drawing of diagrams. It is the continual process of **making architecture decisions transparent and steering change** towards the target.
:::

::: source
Own wording based on Keller (2017), Ahlemann et al. (2012) and Hanschke (2023).
:::

::: notes
Keller (2017) distinguishes enterprise architecture as a structure (the noun) and as a management activity. Ahlemann et al. (2012) describe EAM as a management practice that establishes, maintains and uses principles, guidelines and governance to drive the architecture towards the strategy. Exam point: be able to distinguish EA (the structure and its description) from EAM (the management function). Link to session 3: architecture was one of the five key IT decisions of Weill and Ross — EAM is the function that prepares and enforces these decisions; an architecture board is a governance body.
:::

---

# Why EA Matters {.section}

Goals of EAM and the operating model

---

# Typical Symptoms Without EA

| Symptom | EAM goal |
|---|---|
| IT does not know which processes depend on which applications | **Business–IT alignment**, transparency |
| Three systems for the same task, each with licences and staff | **IT cost** reduction, **less heterogeneity** |
| A new digital product takes years because data are scattered | **Time-to-market** |
| After an acquisition, nobody knows which systems to keep | Managing **mergers** |
| An auditor asks where personal data are stored — weeks of searching | **Compliance**, security, risk |
| Contracts and sourcing are decided per project | Consistent **sourcing** strategy |

::: source
Own examples; goals based on Keller (2017) and Hanschke (2023).
:::

::: notes
Keller (2017) lists typical goals for EAM, among them business–IT alignment, IT cost management and business earning power, sourcing, time-to-market, customer satisfaction, reducing heterogeneity, managing mergers, and compliance, security and risk. Ask students which symptoms they know from their training companies — there are always some. Make clear that EAM is a means to an end: an EA initiative that cannot name the problem it solves loses support quickly (a classic failure: the "ivory tower" architecture team).
:::

---

# EA as a Foundation for Execution

::: columns
**The idea**

- Strategy changes often; the **foundation** of processes, data and systems that executes it changes slowly
- EA should define which processes are **standardised** and which data are **integrated** across the enterprise
- This choice is the **operating model**
|||
**Four operating models**

| | **Low standardisation** | **High standardisation** |
|---|---|---|
| **High integration** | Coordination | Unification |
| **Low integration** | Diversification | Replication |
:::

::: source
Own illustration based on Ross et al. (2006).
:::

::: notes
Ross, Weill and Robertson (2006) argue that the enterprise architecture should follow from the operating model, not from individual projects. Integration = units share data (e.g. one customer view); standardisation = units do the same processes in the same way. Examples: diversification — a conglomerate with independent units; coordination — a bank with one customer view across different products; replication — a franchise or hotel chain where each site works the same way; unification — an airline or a company with one global ERP and shared data. Ask: which operating model does Rhein-Neckar Mobil Group have today (three units, three ERPs, own IT: close to diversification), and which does the joint mobility app require (shared customer and ticket data: coordination)? This is part of today's case.
:::

---

# Stages of Architecture Maturity {.optional}

::: layers
- 4 · Business modularity: Reusable, loosely coupled process and data modules that can be combined quickly
- 3 · Optimised core: Enterprise-wide processes and shared data as a digitised core
- 2 · Standardised technology: Fewer technology platforms, shared infrastructure, lower IT cost
- 1 · Business silos: Each unit optimises its own applications; little sharing
:::

::: source
Own wording based on Ross et al. (2006).
:::

::: notes
Self-study. Ross et al. (2006) found that companies move through these stages one at a time; skipping a stage rarely works because each stage builds the learning for the next. Benefits shift from local flexibility (stage 1) to lower IT cost (2), to better operational efficiency (3), to strategic agility (4). Link to session 2 (alignment maturity): another five-or-four-level model, but here the object is the architecture. Rhein-Neckar Mobil Group is between stage 1 and 2: the federated IT (session 3) has started to share infrastructure.
:::

---

# Mini Exercise: Symptom and Goal {.exercise}

*Rhein-Neckar Mobil Group* (sessions 3–9). Which **EAM goal** does each symptom point to — and which **earlier session** dealt with a similar problem?

1. The three ERP systems cost 1.8 m€ per year to run.
2. The joint mobility app is late because bus, rail and car-sharing customers are stored in different systems.
3. When the payment provider failed, it took hours to find out which processes were affected.
4. The data protection officer cannot say in which systems car-sharing customer data are stored.
5. Each project chooses its own database and cloud provider.

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 IT cost, reducing heterogeneity — session 4 (business case for one cloud ERP); 2 time-to-market, business–IT alignment, integration of data — session 2 (alignment) and session 3 (joint app as a governance topic); 3 transparency of dependencies for risk and continuity — session 8 (BIA needs resources and dependencies); 4 compliance — session 7 (GDPR, records of processing); 5 reducing heterogeneity, technology standards — session 3 (architecture as a key IT decision, IT monarchy). Message: EA information is the common basis for many Part A instruments.
:::

---

# The Domains of Enterprise Architecture {.section}

Business, data, application and technology architecture

---

# Four Architecture Domains

::: layers
- Business architecture: Strategy, capabilities, business processes, organisation, products — what the enterprise does and how
- Data architecture: Business objects and data entities, their structure, ownership, master data and data flows
- Application architecture: Applications, their functions and interfaces — the application landscape
- Technology architecture: Infrastructure and platforms: devices, networks, servers, data centres, cloud services
:::

::: callout
Each domain **supports** the one above it — changes in one domain have effects in the others.
:::

::: source
Own wording based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
TOGAF names these four domains as the commonly accepted subsets of an enterprise architecture (often abbreviated BDAT). Data and application architecture are often combined as information systems architecture (in TOGAF and in Hanschke). Read the layers top-down for the logic of alignment (business demand → data → applications → technology), bottom-up for support. Krcmar's model from session 1 has a similar layering: information economy, information systems, ICT. Cross-cutting topics such as security, compliance and cost run through all four domains.
:::

---

# Business Architecture

::: columns
**Typical elements**

- Business strategy, goals and drivers
- **Business capabilities**: what the enterprise must be able to do (e.g. "manage fares")
- **Business processes** and value streams
- Organisation units, roles, locations
- Products and services, customers, partners
|||
**Questions it answers**

- What does the enterprise do, for whom and with whom?
- Which capabilities are critical for the strategy?
- Who is responsible for which process?
- Where does the business need to change?
:::

::: source
Own summary based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
Business architecture is the starting point; without it, EA becomes IT documentation only. Business capabilities are introduced here only as a term — session 12 builds a capability map. Difference to remember: a capability says *what* an enterprise can do (stable over years), a process says *how* it is done (changes more often). Link to session 5: ITIL value streams are one way of describing how value is created; EA uses the same term.
:::

---

# Data Architecture

::: columns
**Typical elements**

- **Business objects**: customer, ticket, fare, vehicle, invoice
- Logical data models and data entities
- **Master data** and the **leading system** for each object
- **Data ownership** and data quality rules
- **Data flows** between applications
|||
**Questions it answers**

- Which data does the business need, and where are they created?
- Which system holds the "golden record" of a customer?
- Who is responsible for the quality of the data?
- Where are personal data stored and processed?
:::

::: source
Own summary based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
For Business IT students who took Data Management in semester 2: the data architecture is the enterprise-wide view, not the database design of one application. Key idea: one leading (master) system per business object, everything else gets copies via interfaces. Without this rule, three ERP systems each believe they hold the "true" customer. GDPR (session 7) needs the data architecture: records of processing activities, deletion concepts, data transfers to processors.
:::

---

# Application Architecture

::: columns
**Typical elements**

- **Applications** (information systems) and their functions
- **Interfaces** between applications and to partners
- Standard software vs. custom development, SaaS
- Life cycle status: planned, active, phase-out
- Owners and users of each application
|||
**Questions it answers**

- Which applications support which processes and capabilities?
- Where do we have redundant applications?
- What happens elsewhere if an application is replaced?
- Which applications are at the end of their life?
:::

::: source
Own summary based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
The application landscape is the heart of most EAM initiatives in practice — EAM tools such as LeanIX (session 18) start with application fact sheets. The "what happens elsewhere if …" question is impact analysis, one of the main uses of EA information. Application portfolio management (e.g. the TIME model) follows in session 13, integration (interfaces, middleware, APIs) in session 14.
:::

---

# Technology Architecture

::: columns
**Typical elements**

- Hardware and devices, networks
- Servers, data centres, operating systems
- Platforms: databases, middleware, container platforms
- **Cloud services** (IaaS, PaaS) and their providers
- **Technology standards**: approved products and versions
|||
**Questions it answers**

- On which infrastructure do our applications run?
- Which technologies are we using — and which should we stop using?
- Where are single points of failure?
- Which providers do we depend on?
:::

::: source
Own summary based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
Hanschke (2023) separates technical architecture (technologies and standards used to build applications) from the operations infrastructure architecture (the actual servers, networks and locations); TOGAF puts both into technology architecture. Technology standards (a "technology radar" or standards catalogue) are a classic EAM instrument: they reduce heterogeneity and cost. Link to session 8: single points of failure and provider dependencies are BCM questions; link to session 15: sourcing and cloud.
:::

---

# One Process Through Four Domains

![Ticket sale at Rhein-Neckar Mobil Group traced through four domains: the business processes sell ticket on board, share revenue with the transport association and settle card payments use the data objects fare, ticket sale and card payment; these are handled by the ticket device software, the fare back-end and the external payment provider, which run on ticket devices and the mobile network, servers in the Group IT data centre and the provider's platform](img/ea-domains-trace.png){width=88%}

::: source
Own illustration based on The Open Group (2022); own example.
:::

::: notes
Walk through the figure from top to bottom, then ask "what if" questions — this is impact analysis: (1) The fare back-end is moved to the cloud: which processes are affected? All three, because ticket sales feed revenue sharing and payment settlement. (2) The mobile network fails: what still works? Device software keeps fares locally; sales are stored and uploaded later (session 8 BIA). (3) A new fare zone is introduced: which elements change? Business (fare decision), data (fare table), application (device software, back-end), possibly none in technology. Dashed boxes: external partner — the EA must also show what the enterprise does not own.
:::

---

# Other Ways to Cut the Domains {.optional}

| Source | Domains |
|---|---|
| TOGAF | Business · data · application · technology (data + application = information systems) |
| Hanschke | Business · information systems · technical · operations infrastructure |
| ArchiMate (session 17) | Strategy · business · application · technology · physical · implementation and migration |
| Zachman (1987) | Not layers, but a matrix: perspectives (owner, designer, builder …) × questions (what, how, where, who, when, why) |

The names differ, the idea is the same: separate concerns, but **keep the relationships** between them.

::: source
Own comparison based on The Open Group (2022), Hanschke (2023), Lankhorst (2017) and Zachman (1987).
:::

::: notes
Self-study. Students will see different layer models in the literature and in their training companies; none is "wrong". The ArchiMate layers are only named here; session 17 models them. Zachman's 1987 article in the IBM Systems Journal is often called the beginning of EA as a discipline; his framework is a classification scheme rather than a method. Session 17 compares frameworks.
:::

---

# Mini Exercise: Which Domain? {.exercise}

Assign each element of *Rhein-Neckar Mobil Group* to the **business, data, application** or **technology** architecture.

::: columns
1. Capability "manage fares"
2. Customer master data of the car-sharing app
3. The car-sharing app
4. Mobile data connection of the buses
5. Vehicle maintenance unit
|||
6. Interface from the fare back-end to the revenue sharing report
7. API gateway of the car-sharing platform
8. Process "unlock a car"
9. Rule "personal data are stored only in the EU"
:::

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 business (capability); 2 data (business object, master data); 3 application; 4 technology; 5 business (organisation unit); 6 application (interface) — the data it carries (sales, revenue) belong to the data architecture; accept both with reasoning; 7 technology (platform component) or application (it exposes the app's functions) — a good discussion point, both defensible; 8 business (process); 9 a principle that cuts across domains — mainly data (where personal data may be stored) and technology (choice of cloud regions). Lesson: the borders are not sharp, but the relationships matter more than the box.
:::

---

# EAM: Fields of Action and Stakeholders {.section}

What EAM does and for whom

---

# Fields of Action of EAM

::: cards
### Transparency
Document the landscape: processes, applications, interfaces, technologies and their relationships.
### Strategic planning
Derive a target architecture and roadmap from the strategy; manage the application portfolio.
### Steering projects
Assess demands and projects against the target; architecture guidance and reviews.
### Standards and principles
Set architecture principles and technology standards; reduce heterogeneity.
### Risk, compliance, operations
Provide dependencies for security, BCM, data protection and audits.
### Transformation
Support business transformation, digital business models, mergers and sourcing.
:::

::: source
Own grouping based on Hanschke (2023) and Ahlemann et al. (2012).
:::

::: notes
Hanschke (2023) describes more than twenty usage scenarios of EAM (e.g. transparency over the landscape, compliance, data protection and security, reliable operations, sourcing, technology standardisation, application rationalisation, demand management, capability-based planning, target picture and IT roadmap, project portfolio management, IT controlling, digital transformation). The six cards are our grouping. Ahlemann et al. (2012) stress that EAM only works when it is embedded in strategic planning, in the project life cycle and in operations — next slide. Most of the Part B sessions map onto a card: session 11 transparency, 12 transformation and capabilities, 13 strategic planning, 14 integration, 15 sourcing, 16–18 frameworks and tools.
:::

---

# EAM in the Management Cycle

| Where EAM is embedded | What EAM contributes | Link to Part A |
|---|---|---|
| **Strategic planning** | Target architecture, roadmap, input to IT strategy and the project portfolio | IT strategy (2), portfolio management (4) |
| **Project life cycle** | Architecture requirements at project start, reviews at quality gates, update of the as-is | Governance bodies (3), change enablement (6) |
| **Operations and monitoring** | Dependencies for incidents, BIA and audits; architecture KPIs | Service management (5–6), risk and BCM (7–8) |

::: callout
EAM works when it is **part of decisions** that are taken anyway — not as a separate documentation exercise.
:::

::: source
Own summary based on Ahlemann et al. (2012).
:::

::: notes
Ahlemann et al. (2012) devote one chapter each to embedding EAM into strategic planning, into the project life cycle and into operation and monitoring. The practical consequence: an architecture board that reviews projects (architecture governance, session 16 with TOGAF), a rule that new applications are recorded in the EA repository before go-live, and an EA input to the yearly IT planning and budget (session 4). Ask: in your training company, at which point does an architect see a new project — before the business case, or after go-live?
:::

---

# EAM Stakeholders and Their Concerns

| Stakeholder | Typical concern |
|---|---|
| Board, CEO | Does IT support the strategy? Where should we invest? |
| CIO, IT management | Cost, complexity, roadmap, standards |
| Heads of business units, process owners | Which applications support my processes? When does my demand get delivered? |
| Project managers, solution architects | Which standards and interfaces must my project follow? |
| IT operations, service owners | Dependencies, life cycles, capacity |
| CISO, data protection officer, auditors | Where are critical and personal data? Which risks exist? |
| Controller, purchasing | Cost per application, licences, contracts |

::: source
Own compilation based on Ahlemann et al. (2012) and Hanschke (2023).
:::

::: notes
Hanschke (2023) recommends a stakeholder analysis at the start of every EAM initiative: who has which concerns, who must contribute data, who must be convinced. Ahlemann et al. (2012) discuss the "EAM agenda for the CxO": EAM gets support only if it answers top management's questions. The enterprise architects themselves are a stakeholder group too; in many companies they sit in the CIO's office or in a strategy unit. Note the personal and social competence of the module: EAM is mainly communication with business units and IT specialists.
:::

---

# Views for Stakeholders

- A **stakeholder** has **concerns** — interests in the architecture
- A **viewpoint** defines how to look at the architecture for certain concerns: which elements, which notation
- A **view** applies a viewpoint to the actual architecture

| Stakeholder | Concern | Suitable view |
|---|---|---|
| Board | Where do we invest? | Capability map with heat map of strategic importance |
| Data protection officer | Where are personal data? | Data flow diagram of personal data across applications |
| Project manager | What does my project touch? | Interface map of the affected applications |

::: source
Own wording based on ISO/IEC/IEEE (2022) and Lankhorst (2017).
:::

::: notes
The terms come from ISO/IEC/IEEE 42010; TOGAF and ArchiMate use them too. Lankhorst (2017) stresses that an architecture model is only useful if it is communicated in views that the audience understands — the board does not want an interface diagram. Message: one repository, many views. Visualisations (landscape maps, capability maps, interface maps) follow in sessions 11–13 and in the tool session 18.
:::

---

# Case Exercise: EA Domains at Rhein-Neckar Mobil Group {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–9): 3,200 employees, €410 million turnover, three business units, federated IT. The CEO wants a **joint mobility app by 2028**: one customer account and one payment for bus, regional train and car sharing.

- **Bus and rail:** 400 buses and regional trains; on-board ticketing service with ticket devices, fare back-end and external payment provider; app tickets come from the regional transport association's app
- **Car sharing:** 120,000 customers; own app with its own customer database and API gateway, hosted by a cloud provider
- **Vehicle maintenance:** workshop system on its own ERP
- **Group:** three ERP systems, two data centres; a new architecture team of two people reports to the CIO and has no list of applications

::: notes
Read the case together (2 min). Hints if asked: the bus and rail unit stores customer data only for subscriptions (in its ERP); the transport association's app sells single and day tickets and sends the sales data monthly; there are about 180 applications in the group according to a first guess of the CIO (own example figure). Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. List elements of the **four domains** from the case that matter for the mobility app — at least three per domain.
2. Trace the use case "**a customer buys a day ticket and books a car in one app**" through the four domains. Where are the gaps?
3. Which **operating model** does the group have today, and which does the mobility app require?
4. Which **fields of action of EAM** should the new architecture team start with? Justify two.
5. Name four **stakeholders**, their **concerns** and one **view** you would prepare for each.

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 Business: capabilities customer management, ticket sales, car-sharing booking, payment, revenue sharing; processes sell ticket, book and unlock a car; units bus and rail, car sharing, maintenance; partner transport association. Data: customer (three places: car-sharing database, ERP subscriptions, association app), ticket, fare, booking, vehicle, payment. Application: car-sharing app, mobility app (planned), fare back-end, three ERPs, association app, payment provider service. Technology: cloud platform of car sharing, API gateway, two data centres, ticket devices, mobile network.
2 Customer logs in (business: customer management) → one customer account (data: customer — gap: no leading system, three customer stores) → mobility app (application: new) calls the association's ticket sales and the car-sharing booking (gap: interfaces, the association app has no API known yet; sales data only monthly) → one payment (gap: two payment paths) → technology: cloud and data centres must be connected (gap: hosting and network, security). Main gaps: customer master data, interfaces, payment, ownership.
3 Today close to diversification (low integration, low standardisation — own systems per unit; accept "business silos"); the app requires at least coordination: shared customer and payment data across units, while the units keep their own processes. Unification is not needed.
4 Transparency first (no application list — basis for everything, session 11); strategic planning: target architecture and roadmap for the app (session 13); standards and principles: e.g. one leading customer system, API-first; steering projects: the app project must be reviewed against the target. Accept compliance (customer data, GDPR) with reasoning.
5 E.g. CEO — will the app be ready by 2028, what does it cost? → roadmap with milestones; head of car sharing — will my customers be migrated without loss? → data flow of customer data; data protection officer — where are customer data and who processes them? → data flow diagram of personal data incl. processors; app project manager — which systems and interfaces do I need? → interface map; CIO — what happens to the three ERPs? → application landscape map with life cycle status.
:::

---

# Key Takeaways

- **Architecture** = elements, relationships and principles; **EA** applies this to the whole enterprise; **EAM** is the management function that documents, plans and steers it
- EA serves goals such as **alignment, lower cost and heterogeneity, time-to-market, compliance**; the **operating model** sets how much standardisation and integration it must deliver
- Four **domains**: business, data, application, technology — each supports the one above, and the relationships between them enable impact analysis
- EAM works when it is **embedded** in strategic planning, projects and operations and serves its **stakeholders** with suitable views

---

# Next Session: Collecting and Modelling Architecture Information

- Sources and methods for collecting EA data: documents, interviews, workshops, tool imports
- Data quality of EA repositories
- Meta-models: which elements and relationships to collect

::: callout
**Preparation:** find out where your training company documents its applications (Excel list, CMDB, wiki, EAM tool?) — and who keeps the list up to date.
:::

::: notes
The preparation task continues today's recap question "who has the complete list?". Session 11 plans the data collection for the case, which is the first field of action the architecture team needs.
:::

---

# References {.references}

- Ahlemann, F., Stettiner, E., Messerschmidt, M., & Legner, C. (Eds.). (2012). *Strategic enterprise architecture management: Challenges, best practices, and future developments*. Springer. https://doi.org/10.1007/978-3-642-24223-6
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- ISO/IEC/IEEE. (2022). *Software, systems and enterprise — Architecture description* (ISO/IEC/IEEE Standard No. 42010:2022). International Organization for Standardization.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Lankhorst, M. (2017). *Enterprise architecture at work: Modelling, communication and analysis* (4th ed.). Springer. https://doi.org/10.1007/978-3-662-53933-0
- Ross, J. W., Weill, P., & Robertson, D. C. (2006). *Enterprise architecture as strategy: Creating a foundation for business execution*. Harvard Business School Press.
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.
- Zachman, J. A. (1987). A framework for information systems architecture. *IBM Systems Journal, 26*(3), 276–292. https://doi.org/10.1147/sj.263.0276

TOGAF® and ArchiMate® are registered trademarks of The Open Group. Diagrams in this deck are own illustrations. Standards are described in own words.
