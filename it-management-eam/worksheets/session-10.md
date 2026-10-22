---
course: IT Management and EAM
session: 10
title: Enterprise Architecture Foundations
subtitle: Practice tasks on EA and EAM, the four architecture domains, operating models, fields of action and stakeholders
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 10, the first session of Part B: the difference between enterprise architecture (EA) and enterprise architecture management (EAM) (Keller, 2017; Ahlemann et al., 2012), the four architecture domains — business, data, application and technology architecture (The Open Group, 2022; Hanschke, 2023) — the operating models of Ross et al. (2006), the fields of action of EAM, and stakeholders, concerns and views (ISO/IEC/IEEE, 2022). Terms follow the session slides; frameworks and standards are described in own words. Paper and pencil are enough. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) A company that has never documented its IT landscape has no enterprise architecture.
- b) A list of all applications with their licence costs is already a complete enterprise architecture.
- c) EAM is the management function that documents, plans and steers the enterprise architecture.
- d) In the TOGAF Standard, the data and the application architecture together are often called the information systems architecture.
- e) A business capability describes *how* a task is carried out, step by step.
- f) A view is always the same for all stakeholders; only the level of detail changes.

::: answer lines=8
:::

::: hint
Remember the three words of the architecture definition: elements, relationships, principles. And remember the difference between a structure and the management of that structure.
:::

::: solution
- a) **False.** Every enterprise *has* an architecture — planned or grown by accident. Without documentation it is just unknown, not absent.
- b) **False.** An architecture also needs the **relationships** (e.g. which process uses which application, which interface carries which data) and the **principles** for design and evolution. A cost list covers only some elements of one domain.
- c) **True.**
- d) **True.** TOGAF and Hanschke (2023) both group data and application architecture as information systems architecture.
- e) **False.** A capability describes *what* an enterprise must be able to do (e.g. "manage fares"); the *how* is described by business processes.
- f) **False.** Different stakeholders have different **concerns**; a **viewpoint** defines which elements and notation answer these concerns, so the board gets, e.g., a capability map and a project manager an interface map.

Marking hint: one point per item; for false statements the point requires the correction.
:::

## The Four Domains at a Municipal Utility

*Stadtwerke Musterstadt* supplies a city of 150,000 inhabitants with electricity, gas, water and public swimming pools. Assign each element to the **business**, **data**, **application** or **technology** architecture.

| # | Element | Domain |
|---|---|---|
| 1 | Process "read meters once a year" | |
| 2 | Billing system (standard software for utilities) | |
| 3 | Smart meter gateways in customers' basements | |
| 4 | Business object "meter reading" | |
| 5 | Customer service centre (organisation unit) | |
| 6 | Customer portal for tariff changes | |
| 7 | Rule "the billing system is the leading system for customer data" | |
| 8 | Virtual servers in the data centre of a regional IT service provider | |
| 9 | Capability "manage the energy grid" | |
| 10 | Interface that transfers meter readings to the billing system | |

Then name **two relationships** between elements of different domains, e.g. "element X supports element Y".

::: answer lines=10
:::

::: solution
1 **Business** (process) · 2 **application** · 3 **technology** (device in the field; accept application for the gateway software with reasoning) · 4 **data** (business object) · 5 **business** (organisation unit) · 6 **application** · 7 **data** (principle on master data and the leading system) · 8 **technology** · 9 **business** (capability) · 10 **application** (interface); the meter readings it carries belong to the data architecture — accept both with reasoning.

Relationships (examples): the smart meter gateways (3) deliver the meter readings (4); the interface (10) transfers the meter readings (4) to the billing system (2); the billing system (2) supports the process "read meters" (1) and billing; the customer portal (6) is used by customers and the customer service centre (5); the billing system (2) runs on the virtual servers (8).

Marking hint: half a point per element, one point per relationship that connects two different domains in the right direction.
:::

## Impact Analysis at Bodensee Reisen AG

*Bodensee Reisen AG* (session 2) is a tour operator with 25 travel agencies and a call centre. Its strategy is to sell personalised trips mainly online and through an app by 2030. The **booking system from 2005** can only be used by travel agents; it runs on servers in the company's own server room. Customer data are kept in the booking system and in a separate newsletter tool. Payments are processed by an external payment service provider.

1. Trace the target use case "**a customer books a personalised trip in the app and pays online**" through the four domains. Name at least one element per domain.
2. The booking system is to be replaced by a cloud-based booking platform. Carry out a short **impact analysis**: which elements in the other domains are affected? Name at least four.
3. Which **data architecture** question must be answered before the app goes live? Justify.

::: answer lines=14
:::

::: hint
Go from top to bottom: process and organisation → business objects → applications and interfaces → infrastructure. Then ask for each element: does it change if the booking system changes?
:::

::: solution
1. **Business:** process "book trip online", capability "sell trips", customers, travel agencies and call centre as channels. **Data:** customer, trip, booking, payment, offer/price. **Application:** app (new), booking system (or its successor), newsletter tool, external payment service. **Technology:** smartphones of customers, own server room (today), cloud platform (future), internet connection, platform of the payment provider.
2. Affected, e.g.: business — processes of travel agents and call centre (new screens, training), roles and responsibilities; data — migration of customer and booking data, new leading system for customers (booking platform vs. newsletter tool), data protection; application — interfaces to the payment service, newsletter tool, accounting and the app must be rebuilt; technology — servers in the server room can be decommissioned, network connection to the cloud, identity management; contracts with the cloud provider (sourcing, session 15).
3. **Which system is the leading (master) system for customer data?** Today customers exist in two places; the app needs one customer account with consistent data. Also acceptable: where are personal data stored and processed (GDPR, cloud provider as processor), and who owns the data quality.
:::

## Operating Models

Ross et al. (2006) distinguish four operating models by the degree of **standardisation** of business processes and **integration** of data across business units.

1. Assign each company to an operating model and justify it:
   - a) A holding company owns a brewery, a software house and a chain of fitness studios. The units share nothing except the finance department of the holding.
   - b) A chain of 300 bakeries runs every shop with the same processes, the same till system and the same recipes. Shops do not need each other's data.
   - c) A bank offers loans, insurance and investment products in separate units with their own processes. All units must see the same customer data to give advice from one source.
   - d) A parcel service runs all depots with identical processes and one central tracking database.
2. What does the operating model mean for the enterprise architecture of company **b)**? Name two consequences.
3. Company **a)** buys a second fitness studio chain and wants to merge both chains. Does its operating model change? Explain.

::: answer lines=12
:::

::: solution
1. a) **Diversification** — low standardisation, low integration: independent units with different businesses. b) **Replication** — high standardisation, low integration: identical processes in every shop, but shops work on their own. c) **Coordination** — high integration (shared customer data), low standardisation (different processes per product). d) **Unification** — high standardisation and high integration.
2. Replication, e.g.: one standard set of applications (till, ordering) rolled out to every shop as a "template"; strong technology standards; central management of master data such as products and prices, but no need for an integrated customer database; new shops can be opened quickly with the template.
3. At group level it stays diversification (brewery, software and fitness remain separate). Within the fitness unit, the merger moves the two chains towards **replication** (same processes in all studios) or **unification** if members can use all studios with one membership and shared data. The EA work happens at the level of the fitness unit: harmonise processes, choose one member management system, migrate data.
:::

## Stakeholders and Views at Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (session 3) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system and its own data centre. The board wants a **joint patient portal** and a **common security level**. A newly appointed group CIO wants to introduce EAM.

1. Name **four stakeholders** of EAM in the group. For each, give one **concern** and one **view** that would answer it.
2. Explain the terms **stakeholder**, **concern**, **viewpoint** and **view** and how they relate to each other.
3. Which **field of action** of EAM should the CIO start with? Justify in two to three sentences.

::: answer lines=14
:::

::: solution
1. Examples (concern → view):
   - **Board of the group:** what do we need to invest for the portal and the common security level? → roadmap with costs and milestones; capability map with heat map.
   - **Medical directors / heads of departments:** will my clinical processes still work if the information system changes? → process-to-application map for their department.
   - **CISO / data protection officer:** where are patient data, and which systems are critical? → data flow of patient data across systems and locations, incl. external processors; criticality map.
   - **IT heads of the four hospitals:** which systems and data centres will be kept? → application landscape map with life cycle status; infrastructure map of the four data centres.
   - **Project manager of the patient portal:** which systems must the portal connect to? → interface map of the four information systems.
2. A **stakeholder** is a person, group or organisation with interests in the architecture. These interests are **concerns** (e.g. cost, security, availability). A **viewpoint** defines how to look at the architecture to answer certain concerns — which elements, relationships and notation. A **view** is the result of applying a viewpoint to the actual architecture, e.g. today's interface map. One repository of architecture information can produce many views.
3. **Transparency** first: nobody has an overview of the four landscapes, so neither the portal nor a common security level can be planned. Start with an inventory of applications, interfaces, data centres and their criticality — it also feeds the security programme (protection requirements, session 8). Accept "strategic planning" if the student argues that the board's goals need a target architecture early, as long as an inventory is part of the first step.
:::

## Exam-Style Task: Enterprise Architecture at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–9), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers. Orders received by 14:00 are delivered the same day from the central warehouse. The platform is hosted by an external provider and extended by an in-house team of six developers; orders are passed to a 20-year-old, heavily customised **ERP system** in the company's own server room. Sixty field sales representatives use tablets with an ordering app that is also connected to the ERP system.

The board plans to **acquire a smaller wholesaler** in the Saarland that has its own ERP system and web shop. The CIO says: "We don't even know all our own interfaces. Before we buy another company, we need enterprise architecture management."

**Tasks:**

1. Define **enterprise architecture** and distinguish it from **enterprise architecture management**. (3 points)
2. Name the **four architecture domains** and give one element from the case for each. (4 points)
3. Trace the process "**an installer orders on the platform for same-day delivery**" through the four domains and name **two dependencies** that are a risk for the process. (4 points)
4. Explain **two goals** of EAM that are especially relevant for the planned acquisition. (3 points)
5. Recommend **three fields of action** of EAM for the next twelve months and justify each in one sentence. (3 points)
6. Name **three stakeholders** of EAM at Kurpfalz Sanitär AG with one concern and one suitable view each. (3 points)

::: answer lines=28
:::

::: solution
Marking guide (20 points):

**1. EA and EAM (3 points)**

- EA (1.5 points): the fundamental structure of the enterprise — its elements (strategy, processes, data, applications, technology), their relationships and the principles for its design and evolution; it covers as-is, target and the path between them. Every company has one, documented or not.
- EAM (1.5 points): the management function that documents, plans and steers the EA — sets principles and standards, plans a target architecture and roadmap, and checks that projects follow them; links business strategy and IT implementation.

**2. Domains (4 points, 1 per domain: name 0.5, case element 0.5)**

- **Business:** process order handling, same-day delivery, field sales, central warehouse, installers as customers.
- **Data:** order, article, price, customer (installer), stock level.
- **Application:** online order platform, ERP system, ordering app for the tablets, interfaces between them.
- **Technology:** servers in the own server room, platform of the hosting provider, tablets, network connection between the hosting provider and the server room.

**3. Trace and dependencies (4 points)**

- Trace (2 points; at least one element per domain in the right order): installer places order (business, sales process) → order, article, price, stock data (data) → online order platform passes the order via an interface to the ERP system, which creates pick lists for the warehouse (application) → hosting provider's platform, network connection, server room with the ERP (technology).
- Two dependencies (2 points, 1 each), e.g.: the platform depends on the ERP interface — if it blocks, orders time out (session 6); the whole process depends on the single ERP in the own server room (single point of failure, session 8); the hosting provider's availability and support hours; correct prices depend on the price data in the ERP (price error, session 9); the old customised ERP depends on a few experts.

**4. EAM goals for the acquisition (3 points; 1.5 per goal: name 0.5, link to the case 1)**

- **Managing mergers:** decide which systems to keep (two ERPs, two web shops), plan the integration and migration on the basis of a known landscape.
- **Reducing heterogeneity / IT cost:** avoid running two of everything; harmonise technologies and contracts.
- **Business–IT alignment / transparency:** know which processes depend on which systems before changing them; the CIO admits that the own interfaces are unknown.
- Also accept time-to-market (installers of the acquired company should order on the platform quickly) or compliance (customer data of both companies, GDPR) with a case link.

**5. Fields of action (3 points, 1 each with justification)**

- **Transparency:** inventory of applications, interfaces and data flows of both companies — basis for every decision.
- **Strategic planning:** target architecture for the merged company (one ERP? one platform?) and a roadmap; the 20-year-old ERP needs a plan.
- **Standards and principles:** e.g. one leading system per business object, approved technologies for the developers.
- **Steering projects:** the integration project is reviewed against the target.
- **Risk, compliance, operations:** dependencies for BCM and security (sessions 7–8).
- **Transformation:** support of the acquisition as a business transformation.

**6. Stakeholders (3 points, 1 each: stakeholder + concern + view)**

- **Board:** what does the integration cost and how long does it take? → roadmap with milestones and costs; overview of both landscapes.
- **Head of sales:** will installers and field sales be able to order without disruption? → process-to-application map for order handling.
- **Head of logistics/warehouse:** will same-day delivery still work? → dependency map of the order process down to the ERP and server room.
- **Development team / platform owner:** which interfaces and standards must we use? → interface map, technology standards list.
- **Data protection officer / CISO:** where are customer data of both companies? → data flow diagram of personal data.
:::

## Optional Challenge: What Part A Needs from EA {.optional}

Many instruments of Part A (sessions 1–9) depend on enterprise architecture information. For each instrument, name the **EA information** it needs and the **domain(s)** it comes from.

1. A **business impact analysis** (session 8) for the process "pay salaries"
2. The **records of processing activities** under the GDPR (session 7)
3. A **business case** for replacing three CRM systems with one (session 4)
4. The **service catalogue** and an **SLA** for an IT service (sessions 5–6)
5. An **ISO 9001** scope statement for an IT department (session 9)

::: answer lines=10
:::

::: solution
1. Resources and dependencies of the process: which applications (payroll, HR system), which data (salary data, bank data), which interfaces (bank transfer), which infrastructure and providers — all four domains; the BIA uses the application and technology dependencies to set recovery priorities.
2. Which applications process which categories of personal data, for which processes and purposes, where the data are stored and to whom they are transferred (processors, third countries) — business (purposes, processes), data (categories of personal data, data flows), application and technology (systems, locations, providers).
3. The three CRM systems with their costs, users, functions and interfaces; the processes and units that depend on them; the data to be migrated — application (portfolio, redundancy), business (users, processes), data (customer data, migration).
4. Which applications and infrastructure a service consists of and which business processes use it — application and technology (service components), business (customers, processes); needed to set realistic targets and underpinning contracts.
5. Which services, locations, processes and systems are within scope — business (processes, locations, organisation units) and application/technology (systems used to deliver the services).

Marking hint: one point per instrument for sensible information and the matching domain(s). Message: EA information is shared infrastructure for IT management — collected once, used many times.
:::

## References {.references}

- Ahlemann, F., Stettiner, E., Messerschmidt, M., & Legner, C. (Eds.). (2012). *Strategic enterprise architecture management: Challenges, best practices, and future developments*. Springer. https://doi.org/10.1007/978-3-642-24223-6
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- ISO/IEC/IEEE. (2022). *Software, systems and enterprise — Architecture description* (ISO/IEC/IEEE Standard No. 42010:2022). International Organization for Standardization.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Ross, J. W., Weill, P., & Robertson, D. C. (2006). *Enterprise architecture as strategy: Creating a foundation for business execution*. Harvard Business School Press.
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.

Company names and figures in the tasks are fictitious training examples.
