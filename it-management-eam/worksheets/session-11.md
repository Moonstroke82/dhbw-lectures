---
course: IT Management and EAM
session: 11
title: Collecting and Modelling Architecture Information
subtitle: Practice tasks on meta-models, methods for collecting EA data, data quality and the maintenance of EA repositories
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 11: collecting EA information for a purpose, meta-models with element types, relationships and attributes, the granularity of models (Hanschke, 2023), the sources and methods for collecting EA data — document analysis, interviews, questionnaires, workshops and tool imports (Roth et al., 2013; Farwick et al., 2011) — and the data quality and maintenance of EA repositories (Wang & Strong, 1996). Terms follow the session slides; use the lean meta-model from the session (organisation unit, business process, business capability, business object, application, interface, technology component) unless a task says otherwise. Paper and pencil are enough. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) An EA initiative should first document all elements of the enterprise in full detail, so that every later question can be answered.
- b) A meta-model defines which element types, relationship types and attributes may be used in the EA repository.
- c) "The online shop runs on the cloud platform of provider X" is an example of an element type.
- d) Imports from a CMDB deliver up-to-date technical facts, but their names and IDs must be mapped to the applications in the EA repository.
- e) Workshops are the cheapest way to collect the attributes of several hundred applications.
- f) In the view of Wang and Strong (1996), data are of high quality as soon as every value is accurate.

::: answer lines=8
:::

::: hint
Remember the slogan of the session for the scope of a collection, the three levels meta-model – model – reality, and what "beyond accuracy" means.
:::

::: solution
- a) **False.** Collect for a purpose: the questions of the stakeholders decide which element types, relationships and attributes are needed — as little as possible, as much as needed. "Document everything first" leads to projects that never end and to data nobody uses.
- b) **True.**
- c) **False.** It is a **relationship** (*runs on*) between two **elements** of the model; the element types are *Application* and *Technology component*.
- d) **True.**
- e) **False.** Workshops bring many people together and are expensive; they are best for cross-unit relationships and conflicts. Attributes of many known applications are collected more cheaply with a **questionnaire** to the owners (with pre-filled fact sheets) or with **imports**.
- f) **False.** Data quality is **fitness for use**; besides intrinsic quality (accuracy, believability), data must be relevant, timely and complete (contextual), understandable and consistent (representational) and accessible with appropriate security (accessibility).

Marking hint: one point per item; for false statements the point requires the correction.
:::

## Meta-Model, Model or Reality? A Winegrowers' Cooperative

*Weinbau Kaiserstuhl eG* (session 1), a winegrowers' cooperative with 300 members and 60 employees, has started a small EA repository. Its IT consists of an ERP package for orders and accounting, a web shop run by an agency, and sensors in the cellar that monitor fermentation temperatures. A member portal is planned.

1. Classify each item as **element type**, **element**, **attribute (value)** or **relationship**.

| # | Item | Classification |
|---|---|---|
| 1 | Business object | |
| 2 | The web shop | |
| 3 | "The web shop sends orders to the ERP package in a nightly batch" | |
| 4 | Business owner: head of sales | |
| 5 | Technology component | |
| 6 | Process "accept grape deliveries from members" | |
| 7 | Life cycle status "planned" (of the member portal) | |
| 8 | "The ERP package supports the process *invoice customers*" | |

2. Item 3 hides **two** pieces of information that the lean meta-model would store separately. Which ones, and as which kind of model content?
3. Write **two further relationships** for the cooperative that the lean meta-model allows, each between elements of **different** domains.

::: answer lines=12
:::

::: hint
Element types belong to the meta-model and have no concrete name; elements are concrete things with a name; relationships connect two elements; attributes describe one element.
:::

::: solution
1. 1 **element type** · 2 **element** (an application) · 3 **relationship** (via an interface: web shop → ERP package) · 4 **attribute value** of an application; accept "relationship to an organisation unit or role" with reasoning · 5 **element type** · 6 **element** (a business process) · 7 **attribute value** of the element *member portal* · 8 **relationship** (*supports*) between an application and a process.
2. (a) There is an **interface** (an element of type *Interface*) that connects the web shop and the ERP package and **transfers** the business object *order* (relationships). (b) "In a nightly batch" is an **attribute** of the interface (frequency or transfer type). Accept "the business object *order* as an element of the data domain" as one of the two pieces.
3. Examples: the cellar sensors (technology component) deliver data to a cellar monitoring application, or "the monitoring application runs on the sensors' gateway"; the ERP package *creates/reads* the business object *member delivery*; the web shop *runs on* the agency's hosting platform; the sales unit (organisation unit) *performs* the process "sell wine online", which the web shop *supports*; the member portal (application, planned) *reads* the business object *delivery and quality data*.

Marking hint: half a point per item in part 1; one point each for parts 2 and 3 items with a correct direction and element types from two different domains.
:::

## Choose the Method at Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10), a tour operator with 25 travel agencies and a call centre, wants to replace its **booking system from 2005** and to sell personalised trips through an app. The new enterprise architect has no repository yet. For each information need, name the **source and method** you would use first and **one way to cross-check** the result. Justify briefly.

1. All software contracts and their annual cost
2. Which applications the travel agencies use besides the booking system (e.g. local tools, spreadsheets)
3. All interfaces of the booking system, incl. the data they transfer
4. Life cycle status and business owner of the roughly 60 applications on a first draft list
5. Which applications and processes are involved when a customer complains about a trip — across call centre, agencies and accounting
6. Which servers in the own server room host which applications

::: answer lines=14
:::

::: hint
Start with what already exists (documents and systems), then ask people to confirm and complete. Relationships across several units are a typical workshop topic.
:::

::: solution
1. **Document analysis / import** of the contract and licence list (purchasing) and the cost accounting (IT controlling); cross-check with the owners or the invoices in accounting — contracts can exist for software that is no longer used.
2. **Interviews** with a sample of agency managers (or a short **questionnaire** to all 25 agencies); cross-check with software asset/licence management or the CMDB of installed software on agency PCs. Local tools are rarely in any document, so people are the main source.
3. **Interview or small workshop** with the IT owner and the developers or vendor of the booking system, prepared with the system documentation; cross-check with network monitoring or the interface configuration — documents are often outdated for an old system.
4. **Questionnaire** to the owners with a pre-filled fact sheet; cross-check by sampling a few answers in interviews or against the CMDB and contract list. A questionnaire is cheap per element for attributes of known applications.
5. **Workshop** with process owners and staff from call centre, agencies and accounting, walking through the complaint process step by step; cross-check against the ticket or CRM tool data. Cross-unit relationships and conflicts become visible in a workshop.
6. **Tool import** from the CMDB or a network/server inventory, mapped to applications in a short session with the server administrator; cross-check with the operating handbook.

Marking hint: one point per need for a suitable source/method with a justification; half a point extra for a sensible cross-check (max. 6 points). Other combinations are acceptable if justified.
:::

## Data Quality Detective at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1 and 4), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, has merged three Excel lists into a first application list. Here is an extract:

| ID | Name | Business owner | Life cycle | Hosting | Supported process |
|---|---|---|---|---|---|
| A-01 | WMS Lagerverwaltung | Head of warehouses | active | Data centre Köln | Warehouse operations |
| A-02 | Warehouse Management System | M. Weber | Active | DC Cologne | Warehousing |
| A-03 | Route planner | | active | | |
| A-04 | Fleet telematics | Head of fleet | active | Cloud (provider) | Fleet management |
| A-05 | Old billing system | Head of finance | active | Data centre Köln | Invoicing |
| A-06 | New billing (SaaS) | Head of finance | active | Cloud (provider) | Invoicing |
| A-07 | Excel macro "diesel cost per tour" | | | Laptop of a dispatcher | |
| A-08 | SAP | CFO | active | Data centre Köln | Finance, purchasing, HR, sales |

1. Find **at least six** data quality problems. For each, name the **category and dimension** (Wang & Strong, 1996) and propose a **fix**.
2. Which **two rules** (modelling guidelines or maintenance concept) would prevent most of these problems in future?

::: answer lines=16
:::

::: hint
Look for duplicates, empty fields, different spellings and value lists, rows that cannot both be true at the same time, and entries that are much coarser or finer than the others.
:::

::: solution
1. Possible findings (any six):
   - **A-01 and A-02 are duplicates** (same WMS under a German and an English name) — intrinsic: accuracy; representational: consistency. Fix: merge into one element, keep the other name as an alias.
   - **Owner as a person's name (M. Weber) vs. a role** — representational: consistency; also more personal data than needed. Fix: record roles or organisation units, not names.
   - **"active" vs. "Active", "Data centre Köln" vs. "DC Cologne"**, "Warehouse operations" vs. "Warehousing" — representational: consistency, interpretability. Fix: value lists for life cycle, hosting and processes.
   - **A-03 has no owner, no hosting and no process** — contextual: completeness. Fix: mandatory fields; ask the dispatch unit; until then flag as incomplete. (Also an orphan: an application without a supported process.)
   - **A-05 and A-06 are both "active" for invoicing** — intrinsic: accuracy or contextual: timeliness; probably the old system is in phase-out. Fix: check with the head of finance and update the life cycle status with dates.
   - **A-07 (Excel macro)**: granularity much finer than the rest, no owner, no status — representational: consistency, contextual: appropriate amount/relevancy. Fix: modelling guideline on end-user tools — record only if business-critical, then with owner and status; otherwise remove.
   - **A-08 "SAP"** for four processes: granularity much coarser than the rest — representational: consistency, contextual: relevancy (an ERP decision for one module cannot be analysed). Fix: split into modules only if they have different owners or life cycles; otherwise keep one element but record all supported processes as separate relationships.
   - **No source and no review date** in the list — contextual: timeliness/believability cannot be judged. Fix: add "source" and "last reviewed".
2. Rules, e.g.: (a) **modelling guidelines** with a definition of "application", granularity rules (modules, end-user tools), naming rules and value lists for all attributes; (b) a **maintenance concept** with a responsible owner (role) per application, mandatory fields, a review cycle and quality checks for duplicates, orphans and empty fields, reported as KPIs.

Marking hint: one point per problem with a correct category/dimension and a sensible fix (max. 6 points); one point per rule.
:::

## A Lean Meta-Model for Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3 and 10) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system and its own data centre. The board wants a **joint patient portal** and a **common security level**. The new group CIO wants a repository that answers three questions:

- Q1: Which applications in the four hospitals hold or exchange **patient data**, and where are they hosted?
- Q2: Which applications are **critical** for admissions and emergency care, and which infrastructure do they depend on?
- Q3: Which systems must the **patient portal** connect to?

1. Derive a **lean meta-model** from the three questions: name the element types and the relationship types you need, and say which question each one serves.
2. Name **six attributes** of the element type *Application* and the question each serves.
3. Formulate **two granularity rules** for this group (think of the hospital information systems with many modules and of medical devices with software).
4. Which element types or attributes would you deliberately **leave out** for now? Name two and justify.

::: answer lines=16
:::

::: hint
Go from each question to the elements and relationships needed to answer it: Q1 needs data and hosting, Q2 needs processes and dependencies, Q3 needs interfaces.
:::

::: solution
1. Element types and relationships, e.g.:
   - *Application* (all questions); *Business object* with "patient data" (Q1); relationship application **creates/reads** business object (Q1); *Interface* that **connects** applications and **transfers** business objects (Q1, Q3).
   - *Technology component* (data centre, server platform, network) and relationship application **runs on** technology component (Q1 hosting, Q2 dependencies).
   - *Business process* (admission, emergency care) and relationship application **supports** process (Q2); *Organisation unit* (hospital, department) **performs** process and **is owner of** application (Q1–Q3, to know whom to ask and which hospital).
2. Attributes, e.g.: ID and name (all); hospital/organisation unit (Q1); business and IT owner (all — who confirms data); **personal data / patient data yes/no** (Q1); **hosting location** (Q1, if not modelled as a relationship); **criticality** or protection requirements from the BIA (Q2); **life cycle status** (Q3 — do not connect the portal to a system in phase-out); **interface technology / API available** (Q3); vendor (Q3).
3. Rules, e.g.: (a) each hospital information system is one application per hospital; modules are recorded separately only if they have their own owner or life cycle (e.g. a laboratory system from another vendor); (b) medical devices are not applications; only the software that stores or exchanges patient data with other systems (e.g. the imaging archive) is recorded, devices are grouped as technology components per type and location; (c) one naming scheme: "<system> – <hospital>".
4. E.g. *business capabilities* (not needed for the three questions; add when strategic planning starts); detailed server data (CPU, RAM — the CMDB holds them); costs per application (useful later for consolidation, but not needed for Q1–Q3 and hard to collect); every individual interface field. Justification: as little as possible, as much as needed — every extra attribute must be collected and maintained by someone.

Marking hint: parts 1 and 2 two points each for a consistent selection linked to the questions; one point per rule in part 3; one point for part 4 with a justification (max. 8 points).
:::

## Exam-Style Task: EA Data Collection at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–10), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers. The platform is hosted by an external provider and extended by an in-house team of six developers; orders are passed to a 20-year-old, heavily customised **ERP system** in the company's own server room. Sixty field sales representatives use tablets with an ordering app that is also connected to the ERP system.

The board plans to **acquire a smaller wholesaler** in the Saarland that has its own ERP system and web shop. The CIO has been asked to present, within four months, an overview of both landscapes as a basis for the **integration decision**. Existing material: a contract list in purchasing, the CMDB of the IT operations team (servers in the own server room only), a wiki of the development team, and the GDPR records of processing activities. Nothing is known yet about the Saarland company's IT.

**Tasks:**

1. Name **three questions** the EA repository must answer for the integration decision and the **stakeholder** behind each. (3 points)
2. Explain what a **meta-model** is. Name **five element types** and **three relationship types** you need, and give one **granularity rule**. (5 points)
3. Choose a **source and method** for each of the following and name one **weakness** of your choice: (a) the applications of the Saarland wholesaler, (b) the interfaces between the order platform, the tablet app and the ERP system, (c) the running cost and contracts of the applications of both companies. (6 points)
4. Name **two data quality dimensions** that are at risk in this collection, each with an example from the case, and **two measures** that keep the repository current after the integration decision. (4 points)
5. Name **two aspects** of dealing with **people** that the CIO must consider when collecting data at the acquired company. (2 points)

::: answer lines=30
:::

::: solution
Marking guide (20 points):

**1. Questions and stakeholders (3 points, 1 each: question + stakeholder)**

- Board / CFO: which systems of the two companies do the same job (two ERPs, platform and web shop), and what does each cost? → keep or retire.
- Head of sales: which applications support order taking by installers and field sales, and what changes for them during the integration?
- CIO / development team: which interfaces connect the platform, the tablet app and the ERP — what must be rebuilt if the installers of the acquired company order on the platform?
- Data protection officer / CISO: where are customer data of both companies, and which processors are involved?
- Also accept: which applications are near the end of their life (the 20-year-old ERP), which are critical for same-day delivery.

**2. Meta-model (5 points)**

- Definition (1 point): the "model of the model" — it defines the element types, relationship types and attributes (and their rules) that may be used to describe the architecture; like a database schema for the repository.
- Five element types (2 points, 0.4 each): e.g. organisation unit (incl. company), business process, business object, application, interface, technology component; also accept business capability, contract.
- Three relationship types (1 point): e.g. application *supports* process; application *runs on* technology component; interface *connects* applications and *transfers* business objects; organisation unit *is owner of* application; application *creates/reads* business object.
- Granularity rule (1 point): e.g. an application has its own owner and life cycle; the ERP systems are each one application, modules only if they have different owners or life cycles; the platform's microservices or components are grouped into one application; end-user tools only if business-critical.

**3. Sources and methods (6 points, 2 per item: 1 for a suitable source/method, 1 for a relevant weakness)**

- (a) Saarland applications: nothing documented is known → **interviews** with the IT contact and the key users of the acquired company, ideally prepared with a short **questionnaire** or template (pre-structured fact sheet); their contract or licence list as a document if available. Weakness: subjective and depends on memory; possible incompleteness; the people may be reluctant (see task 5); before closing, access to information may be limited.
- (b) Interfaces: **workshop** or interviews with the six developers and the ERP team, prepared with the development wiki; cross-check with the interface configuration, logs or the hosting provider. Weakness: wiki outdated or incomplete — the CIO admits the interfaces are not known; workshops need preparation and people's time.
- (c) Cost and contracts: **document analysis / import** of the purchasing contract list and IT cost accounting for Kurpfalz; for the Saarland company the corresponding lists via the due diligence data. Weakness: contracts show what was bought, not what is used; names differ from the application names, so a mapping is needed.
- Accept other justified combinations (e.g. CMDB import for hosting facts with the weakness "only servers in the own server room, not the externally hosted platform").

**4. Data quality and maintenance (4 points)**

- Two dimensions with example (2 points, 1 each): **completeness** (the externally hosted platform and the Saarland systems are not in the CMDB; unknown interfaces); **consistency** (different names and granularity in contract list, wiki and CMDB, two companies with different naming); **accuracy/believability** (wiki and old ERP documentation may be wrong); **timeliness** (data collected in four months may be outdated by the time integration starts); **access security** (sensitive data on critical systems and weaknesses of the acquired company).
- Two measures (2 points, 1 each): an owner (role) per application with a regular review; update triggers at project quality gates, go-live and decommissioning in the integration project and in change enablement; quality checks and KPIs (share of applications with owner, share reviewed in the last six months, orphans, duplicates); imports from CMDB and contract list repeated regularly; modelling guidelines for both companies.

**5. People (2 points, 1 each)**

- Employees of the acquired company may fear for their jobs or systems → explain the purpose openly, ask for little, give results back, involve their management.
- Works council and data protection: the repository stores roles, not usage by named employees; inform the works council early; store only the personal data needed (GDPR).
- Confidentiality: information about the acquired company's IT is sensitive (and, before the acquisition is completed, may only be used within the agreed due diligence process) → restrict access.
- Do not blame people for weaknesses they report; otherwise answers become defensive.
:::

## Optional Challenge: An Interview Guide for an Application Owner {.optional}

You are preparing an interview with the business owner of the **fleet telematics** application at *Rheinland Logistik GmbH* (task 4).

1. Write a **semi-structured interview guide** with four topic blocks and two questions per block. The answers should fill the fact sheet of the application and its relationships in the lean meta-model.
2. What do you prepare and send **before** the interview, and what do you do **after** it? Name two points each.
3. During the interview, the owner says: "The telematics data would also show us which drivers drive badly. We could put that into the EA tool too." How do you react?

::: answer lines=14
:::

::: solution
1. Example guide:
   - **Purpose and use:** Which processes does fleet telematics support? Which units and roughly how many users work with it?
   - **Data and interfaces:** Which data does it create (positions, mileage, fuel, driving times)? Which other systems receive or send data (route planner, billing, workshop system), and how often?
   - **Technology and operations:** Where does it run (provider, region), who operates it, which support contract exists? What happens to the business if it fails for a day (criticality)?
   - **Life cycle and plans:** Since when is it in use, and is a replacement or extension planned? What are the main problems today?
   Questions should be open but concrete ("which systems receive data?" rather than "describe the architecture").
2. Before: send the pre-filled fact sheet from the existing list (A-04) and the purpose of the collection; agree the date and who else should join (e.g. the IT owner). After: write a short summary and send it back for **confirmation**; enter the data with the source and date in the repository; note open points and conflicts with other sources.
3. Thank the owner, but do not record driver behaviour in the EA repository: it is personal data about employees that the repository does not need for its purpose (data minimisation under the GDPR), and a system that monitors the behaviour or performance of employees is a matter for the works council. Record only that the application processes **personal data of drivers** (attribute "personal data: yes", business object "driving data") — this is exactly what the data protection officer needs to know.

Marking hint: one point per block with two suitable questions, one point each for before and after, two points for part 3 with both the data minimisation and the works council argument.
:::

## References {.references}

- Farwick, M., Agreiter, B., Breu, R., Ryll, S., Voges, K., & Hanschke, I. (2011). Requirements for automated enterprise architecture model maintenance: A requirements analysis based on a literature review and an exploratory survey. In *Proceedings of the 13th International Conference on Enterprise Information Systems (ICEIS 2011)* (Vol. 4, pp. 325–337). SciTePress. https://doi.org/10.5220/0003429203250337
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Roth, S., Hauder, M., Farwick, M., Breu, R., & Matthes, F. (2013). Enterprise architecture documentation: Current practices and future directions. In *Proceedings of the 11th International Conference on Wirtschaftsinformatik (WI 2013)* (pp. 911–925). https://aisel.aisnet.org/wi2013/58
- Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33.

Company names and figures in the tasks are fictitious training examples.
