---
course: IT Management and EAM
session: 17
title: EAM Frameworks II: Modelling and Other Frameworks
subtitle: Practice tasks on ArchiMate elements and relationships, layered views, viewpoints, the Zachman framework and the comparison of frameworks
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 17: the ArchiMate modelling language with its layers, aspects, elements, relationships and viewpoints (The Open Group, 2023; Lankhorst, 2017), the Zachman framework with its questions and perspectives (Zachman, 1987; Sowa & Zachman, 1992), and the comparison of TOGAF, ArchiMate, Zachman and practitioner approaches (The Open Group, 2022; Hanschke, 2023). Terms follow the session slides; the standards are described in own words. Paper and pencil are enough: draw ArchiMate elements as labelled boxes with the element type in a corner, as on the slides, and draw relationships with the correct line ends or write their names on the lines. If you prefer a tool, Archi (free and open source) or draw.io (diagrams.net) has ArchiMate shapes. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) ArchiMate is a method that prescribes the phases of architecture work, similar to the TOGAF ADM.
- b) In ArchiMate, a business process is a behaviour element and a business object is a passive structure element.
- c) In a serving relationship, the arrow points to the element that provides the service.
- d) An application component can realise an application service, and that application service can serve a business process.
- e) The Zachman framework classifies architecture descriptions by questions (what, how, where, who, when, why) and by perspectives (for example owner, designer, builder).
- f) The Zachman framework defines a notation and the order in which the cells should be filled.

::: answer lines=8
:::

::: hint
For a) and f), recall the comparison table: which question does each framework answer? For c), ask "who uses whom?".
:::

::: solution
- a) **False.** ArchiMate is a **modelling language** (elements, relationships, notation, viewpoints); it says how to describe architecture, not how to proceed. It complements the TOGAF ADM.
- b) **True.**
- c) **False.** The arrow points to the **user**, i.e. the element that is served.
- d) **True.** This is the typical cross-layer chain: component → realises → application service → serves → business process.
- e) **True.**
- f) **False.** Zachman is a **classification scheme**: it prescribes neither a notation nor a method or order; the columns have no order.

Marking hint: one point per item; for false statements the point requires the correction.
:::

## Element Types at Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3 and 10–16) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system (HIS) and its own data centre; the group plans a joint **patient portal** and the programme "one group, one HIS" (worksheet 16). The architects collect the following items for a first ArchiMate model:

| No. | Item |
|---|---|
| 1 | The patient |
| 2 | "Admit patient" with the steps registration, admission interview and bed allocation |
| 3 | Ward nurse |
| 4 | "Online appointment booking", as patients experience it in the portal |
| 5 | The HIS of hospital A |
| 6 | The electronic patient record (as data in the HIS) |
| 7 | The discharge letter (as a document of the business) |
| 8 | The virtual servers in the data centre of hospital B |
| 9 | The database management system on which the HIS runs |
| 10 | The goal "one HIS for all four hospitals within five years" |
| 11 | "Migrate hospital C to the group HIS" |

For each item, name the **layer** (or motivation), the **aspect** (active structure, behaviour, passive structure) where it applies, and the **ArchiMate element type**.

::: answer lines=12
:::

::: hint
Ask the "sentence" question from the session: who acts (active structure), what is done (behaviour), what is acted upon (passive structure)? A role is a responsibility, an actor a concrete person or unit.
:::

::: solution
1. Business layer, active structure: **business actor** (accept business role "patient" if argued as a responsibility that different persons take on).
2. Business layer, behaviour: **business process** (with three steps that can be modelled as sub-processes linked by triggering).
3. Business layer, active structure: **business role** (the nurse as a person would be an actor).
4. Business layer, behaviour (external): **business service**; accept **application service** if the student models only what the portal application offers — the patient's view makes it a business service realised by a process and served by application services.
5. Application layer, active structure: **application component**.
6. Application layer, passive structure: **data object**.
7. Business layer, passive structure: **business object** (a representation as a file could additionally be an artifact or a representation; not required).
8. Technology layer, active structure: **node** (accept device only if the student argues with physical hardware; virtual servers are nodes).
9. Technology layer, active structure: **system software**.
10. Motivation: **goal**.
11. Implementation and migration: **work package**.

Marking hint: half a point per item if layer and element type are correct (5.5 points); the aspect is part of the reasoning.
:::

## Relationships and Errors at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1, 4 and 11–16), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, replaces its warehouse management system with a **SaaS WMS** (worksheet 16). Drivers use **scanners** to confirm deliveries; customers track shipments in the **customer portal**.

**Part A.** Name the ArchiMate relationship, including its direction, for each statement:

1. The SaaS WMS makes the application service "stock information" available.
2. The application service "stock information" supports the business process "plan picking".
3. The role "picker" carries out the process "pick order".
4. The process "pick order" changes the business object "picking list".
5. "Pick order" is followed by "pack shipment".
6. The customer portal consists of a tracking module and a document module.
7. The driver app sends delivery confirmations to the billing system.

**Part B.** A junior architect drew the following model. Find **four errors** and correct them.

- The business process "deliver shipment" has a **serving** arrow pointing to the application service "delivery confirmation".
- The application component "driver app" is connected to the business role "driver" with an **association** labelled "is used by".
- The business object "delivery note" is drawn with an **assignment** to the process "deliver shipment".
- The application component "SaaS WMS" is drawn as a **business actor**, because "it does the work".
- The device "scanner" is assigned to the application component "driver app".

::: answer lines=14
:::

::: hint
Write each relationship as a sentence with the element names. If the sentence sounds odd ("the delivery note performs the delivery"), the relationship is wrong.
:::

::: solution
**Part A**

1. **Realisation** from the application component "SaaS WMS" to the application service "stock information".
2. **Serving** from the application service to the business process (arrow points to the process).
3. **Assignment** from the business role "picker" to the process "pick order".
4. **Access** (write) from the process to the business object; the arrow points to the object.
5. **Triggering** from "pick order" to "pack shipment".
6. **Composition** from the customer portal to its modules (accept aggregation with a reason, e.g. modules reused in other applications).
7. **Flow** from the driver app to the billing system (accept triggering only if the student argues that the confirmation starts the billing).

**Part B** (four errors)

- The serving direction is reversed: the **application service "delivery confirmation" serves the process** "deliver shipment" — the arrow points to the process (the user).
- Association is too weak: the driver app **serves** the driver via an application service (e.g. "delivery confirmation") or an application interface; a direct link from component to role is not the usual way to show use.
- A business object cannot be assigned: the process **accesses** (reads or writes) the delivery note.
- A software system is not a business actor: the SaaS WMS is an **application component**; if the point is that work is automated, an application process or function realises the behaviour.
- Not an error: the last item is **correct** — a device can be assigned to the software that runs on it. No point is given for "correcting" it.

Marking hint: half a point per relationship in Part A (3.5 points), one point per correctly identified and corrected error in Part B (4 points).
:::

## A Layered View at Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10–16), a tour operator with 25 travel agencies and a call centre, sells trips through its agencies, the call centre and online; it is building a new **booking platform** and uses a SaaS **customer platform** (worksheets 15 and 16). The following description of the process "book a trip" comes from an interview:

> A customer asks a travel agent for a trip. The agent searches offers in the booking platform, which gets prices and availability from the hotels' and airlines' systems via the **integration platform**. When the customer agrees, the agent books the trip; the booking platform reads the customer data from the customer platform and writes the booking. The customer receives a booking confirmation by e-mail. The booking platform runs in a public cloud region in the EU; the customer platform is a SaaS offering; the agencies work on standard PCs.

1. Draw a **layered view** (business, application, technology) with at least **four elements per layer** and at least **one** of each relationship type: serving, realisation, assignment, access and triggering.
2. Write **three sentences** that read your model from the technology layer up to the customer.
3. Which element would change if the call centre also booked trips, and which would stay the same? What does this tell you about services?

::: answer lines=18
:::

::: hint
Start with the customer and the business service the customer gets. Then ask which process realises it, which application services serve the process, which components realise these services and where the components run.
:::

::: solution
1. Example model (accept other consistent models):
   - **Business:** actor "Customer"; business service "Trip booking" serves the customer; business process "Book a trip" realises the service, with steps "Search offers" → (triggering) "Agree on trip" → "Book trip" → "Send confirmation"; role "Travel agent" assigned to the process; business objects "Booking" (written by "Book trip") and "Booking confirmation".
   - **Application:** application services "Offer search", "Booking management" and "Customer data" serve the process steps; application components "Booking platform" (realises offer search and booking management), "Customer platform" (realises customer data), "Integration platform", partner systems of hotels and airlines (as external application components); data objects "Offer", "Booking", "Customer"; booking management writes "Booking", reads "Customer"; flows from the partner systems via the integration platform to the booking platform.
   - **Technology:** node "EU public cloud region" assigned to the booking platform; node "SaaS provider's platform" assigned to the customer platform (or left out as outside the company); device "Agency PC" with system software "Web browser"; communication network "Internet / company network"; technology service "Cloud hosting" serving the booking platform.
2. E.g.: "The booking platform runs on a node in an EU cloud region. The booking platform realises the application service 'booking management', which serves the business process 'book a trip'. The travel agent performs this process, which realises the business service 'trip booking' used by the customer."
3. A new role "Call centre agent" is assigned to the process (or a second process variant for the phone channel) and maybe a business interface "Telephone" is added. The business service "Trip booking", the application services and the components **stay the same**. Services decouple the layers: the way a service is delivered or used can change without changing what is offered.

Marking hint: six points for part 1 (two per layer, of which one for correct relationships), two points for part 2, two points for part 3.
:::

## Zachman at Weinbau Kaiserstuhl eG

*Weinbau Kaiserstuhl eG* (sessions 1 and 11–16), a winegrowers' cooperative with 300 members and 60 employees, has no IT staff of its own; it uses an ERP package, a web shop run by an agency and cellar sensors and plans a **member portal** (worksheet 16). For the board, the managing director collected the following documents:

| No. | Document |
|---|---|
| 1 | The cooperative's statute with its purpose and the board's five-year goals, incl. "30 % of wine sold online" |
| 2 | A list of the most important business things: members, vineyard plots, grape deliveries, wines, orders |
| 3 | The process description "accept grape delivery at harvest" |
| 4 | The agency's database schema of the web shop |
| 5 | The harvest calendar and the dates of the monthly member payouts |
| 6 | The network plan of the winery with the cellar sensors and the router |
| 7 | A table of who in the office is responsible for which tasks |

1. Place each document in the **Zachman grid** (question and perspective).
2. Which **questions** or **perspectives** are poorly covered for the planned member portal? Name two gaps and what should be described.
3. The board member who attended a TOGAF training (worksheet 16) asks whether the cooperative should fill all 36 cells. Answer in three sentences.

::: answer lines=14
:::

::: solution
1. 1 → **why / planner** (scope: purpose and high-level goals). 2 → **what / planner** (list of important things; accept owner). 3 → **how / owner** (business process model). 4 → **what / builder** (physical data design in a database technology; accept designer if argued as a logical schema). 5 → **when / owner** (business events and cycles). 6 → **where / builder** (technology network). 7 → **who / owner** (responsibilities in the business).
2. E.g.: **why / owner** for the portal — what members should gain and which rules apply (data protection, what members may see); **what / designer** — which data the portal needs (member, deliveries, quality values, payouts) and where they come from; **who / designer** — which roles may see what in the portal (access rights); **where / designer–builder** — where the portal runs and how it connects to the ERP. Accept any two gaps with a reasoned description.
3. No: the framework is a checklist, not a method, and filling all cells would cost far more than the value for a landscape of four or five systems. The cooperative should describe only the cells that support a decision, e.g. the member portal's goals, data and access rights. The grid helps to see what is missing before signing a contract with the agency or provider.

Marking hint: three and a half points for part 1 (half a point per document), two points for part 2, one point for part 3.
:::

## Exam-Style Task: Modelling the Order Landscape of Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–16), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers; orders received by 14:00 are delivered the same day from the central warehouse. The acquisition of a wholesaler in the **Saarland** has closed; the platform is to become a **marketplace** for manufacturers and other wholesalers (worksheets 12–16). Known facts:

| Topic | Today |
|---|---|
| Order process | An installer orders on the platform; the order is checked (credit limit, stock), picked and packed in the central warehouse and handed to a carrier; the installer receives a shipping notice |
| Applications | Externally hosted order platform (six in-house developers); 20-year-old customised ERP in the own server room, with stock and credit limits; tablet ordering app for 60 field sales representatives; a proposed integration platform; nightly files to carriers |
| Architecture | Two architects report to the CIO; architecture principles and an architecture board were proposed in the ADM work (worksheet 16) |
| Documentation | A spreadsheet of applications, network plans of the server room and a few process descriptions; no common notation |

**Tasks:**

1. Explain what **ArchiMate** is and how it relates to the **TOGAF ADM**. (2 points)
2. Draw a **layered ArchiMate view** of the order process "order to same-day delivery" with the business, application and technology layer. Use at least **three business process steps** with **triggering**, one **business role**, one **business object**, two **application components** with the **application services** that serve the process, and the **nodes** on which the components run. (8 points)
3. Explain **two relationships** from your view in one sentence each, stating the direction. (2 points)
4. Model the marketplace plan with **motivation** and **migration** elements: one **stakeholder** with a **goal**, one **requirement**, and **two plateaus** with the **gap** between them. (3 points)
5. Place three of the existing documents in the **Zachman grid** and name one **question** that is not described at all. (2 points)
6. The CIO asks which frameworks the two-person team should use. Recommend a **combination** and justify it. (3 points)

::: answer lines=34
:::

::: solution
Marking guide (20 points):

**1. ArchiMate and TOGAF (2 points)**

- ArchiMate is an open **modelling language** of The Open Group with defined elements, relationships, notation and viewpoints for describing enterprise architectures across layers (1 point).
- TOGAF ADM is a **method** (how to proceed); ArchiMate is the **language** for the models and diagrams produced in its phases, e.g. business, application and technology views in Phases B–D and plateaus and work packages in E–F (1 point).

**2. Layered view (8 points)**

- **Business layer (3 points)**: actor "Installer" served by business service "Same-day delivery" (or "Order handling") (0.5); process steps "Receive order" → "Check order" → "Pick and pack" → "Hand over to carrier" (and "Send shipping notice") connected by triggering (1); role assigned, e.g. "Warehouse picker" to "Pick and pack" or "Order clerk" to "Check order" (0.5); business object "Order" or "Shipping notice" accessed by a step (0.5); process realises the business service (0.5).
- **Application layer (3 points)**: components "Order platform" and "ERP" (and optionally "Integration platform", "Carrier systems") (1); application services that serve the steps, e.g. "Order entry" (realised by the platform) serves "Receive order", "Credit and stock check" and "Picking list" (realised by the ERP) serve "Check order" and "Pick and pack" (1); correct realisation and serving directions (0.5); data object "Order" with access, or a flow from platform to ERP (0.5).
- **Technology layer (2 points)**: node "External hosting" assigned to the order platform and node "Server in own server room" assigned to the ERP (1); correct assignment direction and a sensible addition, e.g. communication network between the two or system software "Database" (1).
- Deduct half a point per reversed serving arrow (maximum one point). Accept labelled boxes with the element type instead of the exact symbols.

**3. Two relationships explained (2 points, 1 each)**

- E.g.: "The application service 'credit and stock check' **serves** the process step 'check order' — the arrow points to the step, which uses the service." "The ERP **realises** 'credit and stock check' — the concrete component makes the service real." "The role 'warehouse picker' is **assigned** to 'pick and pack' — it performs the step."

**4. Motivation and migration (3 points)**

- Stakeholder and goal (1): e.g. stakeholder "CEO" or "Manufacturers" — goal "Platform opened as marketplace" or "Higher turnover through third-party sellers".
- Requirement (1): e.g. "Sellers upload product data via an interface", "Commission billing per seller", "Same-day delivery remains for own goods"; ideally realised by an application service (e.g. "Seller onboarding").
- Plateaus and gap (1): e.g. plateau "Today: own online shop, two ERPs" → plateau "Marketplace with seller interface and one ERP"; gap: seller management, product data interface, commission billing, integration platform, ERP consolidation.

**5. Zachman (2 points)**

- Placement (1, any three correct): spreadsheet of applications → what or how / designer (accept builder); network plans of the server room → where / builder; process descriptions → how / owner.
- Missing question (1): e.g. **why** (goals, principles: only proposed, not described), **when** (events such as the 14:00 cut-off, nightly carrier files) or **who** (responsibilities for applications and data).

**6. Framework recommendation (3 points)**

- A combination with reasons (2): e.g. **tailored TOGAF** — Phase A, principles, architecture board and compliance reviews for the integration programme; **ArchiMate** — a few standard views (layered view for projects, application cooperation for integration, migration view for the roadmap) in an EA tool or repository; **Zachman** as a checklist for missing descriptions.
- Fit to the situation (1): only two architects → lean, few viewpoints, no complete documentation; the programme needs a common language for two companies' IT teams; the business (CEO, sales) needs simple views such as capability or migration views rather than full ArchiMate diagrams.
:::

## Optional Challenge: Viewpoints for the Patient Portal {.optional}

*Klinikverbund Oberrhein* designs the joint **patient portal**: patients book appointments, see findings and pay invoices; the portal reads data from the four HIS and the shared billing ERP via an integration platform (worksheet 14). Three stakeholders want to see the architecture: the **board of the group**, the **data protection officer** and the **IT operations team**.

1. For each stakeholder, name the **concern**, a suitable **viewpoint** and **three element types** that the view shows.
2. Which element types would you deliberately **leave out** of the board's view, and why?

::: answer lines=10
:::

::: solution
1. E.g.: **Board** — concern: benefits, cost, timeline; viewpoint: motivation and migration (or capability map) — elements: goal, outcome, plateau, work package (and capability). **Data protection officer** — concern: which personal data flow where and who can access them; viewpoint: application cooperation with data objects (or an information structure view) — elements: application component, data object, flow and access relationships, business role (who accesses). **IT operations** — concern: where the portal runs, dependencies, availability; viewpoint: technology usage — elements: node, system software, communication network, technology service, application component.
2. Technology details (nodes, networks, system software) and individual data objects or interfaces: they do not support the board's decisions and make the view hard to read. One model, many views: the details remain in the repository for those who need them.

Marking hint: one point per stakeholder (three points), one point for part 2.
:::

## References {.references}

- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Lankhorst, M. (2017). *Enterprise architecture at work: Modelling, communication and analysis* (4th ed.). Springer. https://doi.org/10.1007/978-3-662-53933-0
- Sowa, J. F., & Zachman, J. A. (1992). Extending and formalizing the framework for information systems architecture. *IBM Systems Journal, 31*(3), 590–616. https://doi.org/10.1147/sj.313.0590
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.
- The Open Group. (2023). *ArchiMate 3.2 specification* (Document No. C226). Van Haren Publishing.
- Zachman, J. A. (1987). A framework for information systems architecture. *IBM Systems Journal, 26*(3), 276–292. https://doi.org/10.1147/sj.263.0276

Company names and figures in the tasks are fictitious training examples. TOGAF® and ArchiMate® are registered trademarks of The Open Group.
