---
course: IT Management and EAM
session: 15
title: IT Sourcing
subtitle: Make or buy · outsourcing models · offshoring and nearshoring · cloud sourcing (IaaS, PaaS, SaaS) · multi-sourcing · vendor management
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# IT Sourcing {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · what IT sourcing is, dimensions, motives and risks, make or buy 20 min · mini exercise "make or buy?" 10 min · break 10 min · outsourcing models, onshore/nearshore/offshore 15 min · cloud sourcing 20 min · mini exercise "which service model?" 10 min · multi-sourcing, vendor management, sourcing in EAM 20 min · case exercise sourcing decision 40 min · wrap-up 5 min · ~20 min buffer.
Session 14 ended with the question who should run the integration platform of Rhein-Neckar Mobil Group — Group IT, a service provider or a cloud vendor. Today generalises that question: which IT services does an enterprise produce itself, which does it buy, from whom, from where and under which contract — and how does it stay in control? This covers the module content "IT sourcing" and the overarching competence of selecting suitable methods for managing the IT landscape; it links back to IT strategy (session 2), IT organisation (session 3), IT controlling (session 4), SLAs and underpinning contracts (session 6) and compliance (session 7).
Source note for the lecturer: Tiemeyer (2023) has a chapter on cloud computing (chapter 7, by Farwick, Schmidt and Trojer) and a chapter on IT sourcing (chapter 8, by Zsifkovits) with make-or-buy, supplier management and cloud sourcing; chapter numbers checked against the publisher's table of contents, check the text in the library copy before quoting. The cloud definitions follow Mell and Grance (2011, NIST SP 800-145). Outsourcing motives, risks and theories follow the literature review by Dibbern et al. (2004) and the selective sourcing article by Lacity, Willcocks and Feeny (1996); nearshoring follows Carmel and Abbott (2007); multi-sourcing Cohen and Young (2006); the retained organisation Feeny and Willcocks (1998). Make-or-buy matrix, cloud responsibility stack and vendor life cycle are own illustrations; all RNM figures are own examples.
:::

---

# Today's Agenda

1. Recap: what does your company buy from outside?
2. Sourcing decisions: dimensions, motives and risks, make or buy
3. Outsourcing models; onshore, nearshore and offshore
4. Cloud sourcing: IaaS, PaaS, SaaS
5. Multi-sourcing and vendor management
6. Case exercise: a sourcing decision for Rhein-Neckar Mobil Group

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Sourcing decisions, dimensions, make or buy (input) · 0:30 Mini exercise "make or buy?" (pairs) · 0:40 Break · 0:50 Outsourcing models and locations (input) · 1:05 Cloud sourcing (input) · 1:25 Mini exercise "which service model?" (pairs) · 1:35 Multi-sourcing, vendor management, sourcing in EAM (input) · 1:55 Case exercise (groups + plenary) · 2:35 Wrap-up · ~20 min buffer.
If the session runs long: "Offshoring in Practice", "The Retained Organisation" and "Sourcing Pitfalls" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: What Does Your Company Buy from Outside?

You were asked to find out which **IT services** your training company **buys from outside** — and **why** it decided to buy rather than do them itself.

- Which services did you find: **SaaS**, **hosting**, **application support**, **service desk**, **development**?
- Which **reasons** were given: cost, skills, speed, focus — or "we have always done it this way"?
- Did anyone mention a service that was **brought back** in-house?

::: notes
Pairs for 3 min, then collect on the board in three columns: service · provider type (SaaS, hosting/data centre, consultancy/agency, offshore provider) · reason. Typical findings: e-mail and office as SaaS, payroll by an external service provider, SAP hosting and basis operations by a partner, a web agency for the shop, a printer fleet with a managed print contract, sometimes a service desk in another country. Reasons are often a mix of cost, missing skills and "the vendor only offers it as SaaS". Keep the board: the services will be sorted by sourcing dimensions in a few minutes, and the reasons become the make-or-buy criteria. If somebody reports insourcing (backsourcing), ask why — usually quality problems, loss of know-how or a strategic change.
:::

---

# Sourcing Decisions {.section}

What to do ourselves, what to buy — and from whom

---

# What Is IT Sourcing?

::: callout
**IT sourcing** decides **who** provides which IT services and solutions for the enterprise — the own IT department, a group company or external providers — and **under which arrangement**: from buying a SaaS licence to outsourcing a whole IT function.
:::

- **Outsourcing**: an external provider takes over IT services the enterprise used to provide itself, usually with staff, assets or contracts
- **Insourcing** and **backsourcing**: services are provided or brought back in-house
- Sourcing is one **content area of the IT strategy** (session 2) and a decision with long-term effects on cost, skills and the IT landscape

::: source
Own wording based on Dibbern et al. (2004) and Tiemeyer (2023, chapter 8).
:::

::: notes
Dibbern et al. (2004) review the literature on information systems outsourcing and structure it along the questions why, what, which (decision process), how (implementation) and with which outcome. In practice "sourcing" is the broader term: every application landscape is already a mix of make and buy — standard software, SaaS, hosting, consultants. Link to session 2: sourcing was one of the content areas of the IT strategy ("what do we do ourselves, what do we buy or outsource?"). Link to session 1: the cloud contract negotiation in the first mini exercise was a sourcing task.
:::

---

# Dimensions of a Sourcing Decision

| Question | Options | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **What?** — scope | Infrastructure, applications, IT processes, business processes | Data centre operation; payroll as a business process |
| **Who?** — provider | Internal IT, group company, external provider | Group IT, an IT subsidiary, the payment provider |
| **Where?** — location | Onshore, nearshore, offshore | Service desk in Mannheim or in Poland |
| **How much?** — degree | Total or selective | Only helpdesk and payroll outsourced |
| **How many?** — providers | Single or multi-sourcing | One provider for all, or several specialists |
| **How delivered?** | Classic service contract or cloud service | Managed hosting vs. SaaS |

::: source
Own compilation based on Dibbern et al. (2004), Lacity et al. (1996) and Tiemeyer (2023, chapter 8).
:::

::: notes
The dimensions help to describe an arrangement precisely — "selective, nearshore, multi-provider outsourcing of application maintenance" says much more than "we outsourced IT". Lacity et al. (1996) contrast total outsourcing (large, long-term contracts for most of the IT function) with selective sourcing (shorter contracts for specific activities), and report that selective sourcing became the typical pattern. Ask the class to sort the preparation findings by the dimensions on the board. Group companies: many German groups run their IT in a subsidiary (an "IT-GmbH") — formally a separate provider, but owned by the group (internal or "captive" sourcing).
:::

---

# Why Outsource — and What Can Go Wrong

::: columns
**Typical motives**

- **Cost**: economies of scale of the provider, variable instead of fixed cost
- **Focus** on core competences and the business
- **Access to skills** and technologies that are scarce on the market
- **Speed and flexibility**: capacity when needed
- **Quality and reliability** through specialised providers
|||
**Typical risks**

- **Hidden costs**: transition, contract management, change requests
- **Loss of know-how** and of control over the landscape
- **Dependency** on a provider; difficult exit (lock-in)
- **Service quality** below expectations; contract cannot capture everything
- **Security, data protection** and compliance at the provider
:::

::: source
Own wording based on Dibbern et al. (2004) and Lacity et al. (1996).
:::

::: notes
Dibbern et al. (2004) summarise motives such as cost reduction, focus on core competences and access to expertise, and theories used to explain sourcing decisions, among them transaction cost economics (outsourcing becomes expensive when a service is highly specific and hard to measure and contract), the resource-based view and agency theory. Lacity et al. (1996) report from their cases that total outsourcing deals often brought hidden costs and unexpected fees and that few were clear successes — one reason why selective sourcing became common. Link to session 4: outsourcing shifts costs from capex to opex and makes them visible per service — but the cost of managing the provider stays in-house.
:::

---

# Make or Buy: The Criteria

- **Strategic importance**: does the activity **differentiate** us from competitors, or is it a **commodity** that every firm needs?
- **Core competence test**: hard to imitate, important for customer value, usable in several markets
- **Specificity**: how specific to our processes is the solution — does a market offering fit?
- **Cost over the life cycle**: build and run vs. price, transition and management of the provider
- **Skills and capacity**: can we build and keep the know-how?
- **Risk and control**: security, availability, dependency, compliance

::: callout
Rule of thumb: **make** what differentiates and cannot be bought; **buy** what is standard and mature on the market — and keep the **control** in-house.
:::

::: source
Own wording based on Prahalad and Hamel (1990), Lacity et al. (1996) and Dibbern et al. (2004).
:::

::: notes
Prahalad and Hamel (1990) describe core competences with three tests: they give access to a wide variety of markets, contribute significantly to the customer benefits of the end product, and are difficult for competitors to imitate. Lacity et al. (1996) assess IT activities by their contribution to business positioning (commodity vs. differentiator) and to business operations (critical vs. useful), and add economic and technical considerations such as the maturity of the technology and how integrated the activity is with other activities. The rule of thumb is a simplification: a commodity can still be critical (payroll must run on time), and "buy" never means giving up architecture and supplier control. Link to session 13: "standard software before own development, except in differentiating capabilities" was one of the architecture principles.
:::

---

# A Make-or-Buy Matrix

![Make-or-buy matrix with two axes: contribution to competitive position from commodity to differentiator, and maturity of market offerings from low to high. Make (differentiator, low maturity): develop and run in-house, e.g. fare and journey logic of the mobility app. Buy and differentiate (differentiator, high maturity): standard product or platform with own extensions, keep control, e.g. customer master on a CRM platform with own app on top. Standardise first (commodity, low maturity): question the requirement, then buy or share, e.g. special fare macros in Excel. Buy or outsource (commodity, high maturity): SaaS, managed service, selective outsourcing, e.g. payroll, e-mail and office, helpdesk tool, finance ERP](img/sourcing-make-or-buy.png){width=66%}

::: source
Own illustration based on Lacity et al. (1996) and Prahalad and Hamel (1990); own example.
:::

::: notes
The matrix combines two of the criteria. Read it with the RNM examples: the journey and fare logic of the mobility app is what makes the app different and no product offers it for the regional tariff → make (or at least own the product and the code). The customer master is important for the strategy, but CRM and customer identity platforms are mature → buy and differentiate: buy the platform, build the differentiating parts on top. Payroll, office, helpdesk and finance ERP are commodities with mature markets → buy or outsource. Bottom left is a warning sign: a commodity for which no product fits usually means the requirement is too special — standardise the process first (the fare macros of session 13). The matrix is an own teaching tool, not a standard model.
:::

---

# Mini Exercise: Make or Buy? {.exercise}

*Rhein-Neckar Mobil Group* reviews six IT activities. Place each in the **make-or-buy matrix** and name **one criterion** that decides it.

1. E-mail, calendar and office software for 3,200 employees
2. The **pricing logic** for combined bus, rail, car-sharing and e-bike trips in the mobility app
3. Repair of broken **ticket devices**
4. Operation of the servers in **data centre 1**
5. **Timetable planning** for buses and regional trains
6. A **fraud check** for app payments

::: notes
Pairs, 5 min + 5 min discussion. Expected answers (several defensible): 1 buy/outsource — commodity, mature SaaS market; check data location and the works council (session 11). 2 make — differentiating, no product knows the combination of the regional tariff, partners and best-price rules; keep the know-how in-house (two developers of the fare back-end are a warning). 3 buy — the manufacturer repairs under an underpinning contract already (session 6); commodity, needs the manufacturer's parts. 4 buy/outsource — infrastructure is a commodity; colocation, hosting or IaaS when data centre 1 is retired (roadmap, session 13); criterion cost and skills. 5 buy and differentiate or tolerate — vendor standard already in use (session 13), specialised market. 6 buy — fraud detection needs data and know-how of many merchants; typically a service of the payment provider; keep the decision rules and the data protection review in-house. Lesson: the same company makes and buys at the same time.
:::

---

# Outsourcing Models and Locations {.section}

Who provides the service — and from where

---

# Outsourcing Models

| Model | What the provider takes over | Example |
|---|---|---|
| **Infrastructure outsourcing** | Data centre, servers, network, workplaces | Hosting of the fare back-end |
| **Application management** | Maintenance and further development of applications | Support for the dispatching system |
| **Managed services** | A defined IT service with SLAs, often per user or device | Managed workplace, managed security monitoring |
| **Business process outsourcing** | A whole business process including its IT | Payroll for all units |
| **Internal options** | Shared service centre or IT subsidiary of the group | Group IT as an internal provider |

::: callout
**Selective** sourcing combines several models for specific services; **total** outsourcing hands most of the IT function to one provider.
:::

::: source
Own compilation based on Tiemeyer (2023, chapter 8) and Lacity et al. (1996).
:::

::: notes
The models differ in what is handed over and in how the provider is steered: infrastructure outsourcing is often measured by availability and capacity, application management by response and fix times and release quality, BPO by business results (payslips on time and correct). Outsourcing an existing function often includes the transfer of staff and assets to the provider — in Germany, this can be a transfer of undertaking with legal consequences for the employment contracts, so legal and the works council are involved early. Internal options: a shared service centre bundles IT services for several units (Group IT at RNM after the federated organisation of session 3); an IT subsidiary can also sell to third parties.
:::

---

# Onshore, Nearshore, Offshore

| Location | Seen from Germany, e.g. | Strengths | Challenges |
|---|---|---|---|
| **Onshore** | Germany | Same language, law, time zone; easy to meet | Highest labour cost, scarce skills |
| **Nearshore** | Poland, Czechia, Portugal | Lower cost, little time difference, EU law, short travel | Cost advantage smaller than offshore |
| **Offshore** | India, Vietnam | Large talent pool, lowest labour cost | Time zones, language and culture, data transfers outside the EU |

::: callout
Distance has several dimensions — **geographic, temporal, linguistic, cultural** — and each costs coordination effort.
:::

::: source
Own wording based on Carmel and Abbott (2007); own examples.
:::

::: notes
Carmel and Abbott (2007) analysed how the term "nearshore" is used and found that it mostly means sourcing work to a lower-wage country that is relatively close in distance or time zone; they distinguish geographic, temporal, linguistic and cultural distance and argue that distance still matters — the right location depends on the task: frequent face-to-face workshops favour geographic closeness, real-time collaboration favours time-zone overlap. The countries are common examples, not recommendations. Data protection: transfers of personal data to countries outside the EU/EEA need a legal basis under Chapter V GDPR (e.g. an adequacy decision or standard contractual clauses) — a point for every offshore contract that involves customer data.
:::

---

# Offshoring in Practice {.optional}

- **Suitable**: well-specified, stable, documented tasks — testing, maintenance of standard applications, 24/7 monitoring
- **Less suitable**: tasks that need close contact with users, fast feedback or deep business knowledge — early product discovery, workshops
- **Hidden costs**: knowledge transfer, travel, specifications, coordination, staff turnover at the provider
- **Follow the sun**: teams in several time zones can work around the clock — but every hand-over must be organised

::: source
Own wording based on Carmel and Abbott (2007) and Dibbern et al. (2004).
:::

::: notes
Self-study. A wage difference of 60 % does not mean savings of 60 %: transition, coordination and rework eat part of it, and a large share of the cost of a project is coordination and specification. Mixed models are common: product owner and architect onshore, development team nearshore, regression testing and monitoring offshore. Exam point: argue the location with the characteristics of the task, not only with the hourly rate.
:::

---

# Cloud Sourcing {.section}

Buying IT as a service

---

# What Is Cloud Computing?

::: columns
**Five essential characteristics**

- **On-demand self-service**: resources are ordered without human interaction
- **Broad network access** from many devices
- **Resource pooling**: the provider serves many customers from shared resources
- **Rapid elasticity**: capacity scales up and down
- **Measured service**: use is metered and billed
|||
**Deployment models**

- **Public cloud**: open to the general public, run by a provider
- **Private cloud**: for one organisation only
- **Community cloud**: for a group with shared concerns, e.g. public authorities
- **Hybrid cloud**: a combination, e.g. own data centre plus public cloud
:::

::: source
Own wording based on Mell and Grance (2011).
:::

::: notes
Mell and Grance (2011) give the widely used NIST definition: cloud computing is a model for convenient, on-demand network access to a shared pool of configurable computing resources that can be rapidly provisioned and released with minimal management effort or provider interaction; it has five essential characteristics, three service models and four deployment models. Use the characteristics as a test: a server rented for three years in a provider's data centre with a ticket-based ordering process is hosting, not cloud — no self-service, no elasticity. Many firms run a multi-cloud landscape (several public cloud providers) in addition to hybrid setups.
:::

---

# IaaS, PaaS, SaaS: Who Manages What?

![Comparison of on-premises operation, IaaS, PaaS and SaaS in seven layers from network and data centre at the bottom to data and access rights at the top. On-premises: the customer manages all layers. IaaS: the provider manages network and data centre, servers and storage, and virtualisation; the customer manages operating system, runtime and middleware, application, data and access rights. PaaS: the provider also manages operating system and runtime and middleware; the customer manages the application, data and access rights. SaaS: the provider manages everything up to the application; data and access rights stay with the customer in every model](img/sourcing-cloud-responsibility.png){width=78%}

::: source
Own illustration based on Mell and Grance (2011); simplified.
:::

::: notes
NIST defines the three service models by what the consumer controls: with IaaS, the consumer controls operating systems, storage and deployed applications but not the underlying infrastructure; with PaaS, the consumer deploys own applications using the provider's programming languages, libraries, services and tools; with SaaS, the consumer uses the provider's application and at most changes user-specific settings. RNM examples: IaaS — virtual servers for the fare back-end when data centre 1 is retired; PaaS — a managed database or container platform for the mobility app, an iPaaS for integration (session 14); SaaS — helpdesk tool, cloud ERP, office. The top row matters most for compliance: whoever the provider is, the enterprise remains the controller for personal data and decides who has access. The figure is a simplification; real services sit between the categories.
:::

---

# Cloud Sourcing: Opportunities and Risks

::: columns
**Opportunities**

- **Opex instead of capex**; pay for use (session 4)
- **Speed**: environments in minutes, not weeks
- **Elasticity** for peaks, e.g. app launch, events
- **Modern services**: analytics, AI, managed databases
- **Security operations** by large specialised providers
|||
**Risks and questions**

- **Lock-in**: proprietary services, data formats, egress fees
- **Cost control**: bills grow with use; nobody switches off test systems
- **Data location** and access by third countries
- **Shared responsibility** misunderstood, e.g. open storage buckets
- **Skills**: cloud architecture and cost management
:::

::: callout
The EU **Data Act** obliges providers of data processing services to make **switching** possible; from 12 January 2027 they may not charge switching fees.
:::

::: source
Own compilation based on Mell and Grance (2011) and Tiemeyer (2023, chapter 7); Regulation (EU) 2023/2854, Art. 23 and 29.
:::

::: notes
Chapter VI of the Data Act (Art. 23–31, "switching between data processing services") requires providers to remove commercial, technical, contractual and organisational obstacles to switching to another provider or back on-premises; Art. 29 allows only reduced, cost-based switching charges until 12 January 2027 and none after that date. This does not remove technical lock-in: an application built on proprietary PaaS services still has to be rebuilt elsewhere. Cost control in the cloud is a discipline of its own (often called FinOps): tagging resources by application and owner, budgets and alerts, regular clean-up — the link to IT controlling (session 4) and to the EA repository (which application causes which cloud cost, session 11). Tiemeyer (2023, chapter 7) also discusses cloud strategy and migration options; the details are not exam content.
:::

---

# Sourcing and Compliance

| Requirement | Source | What it means for a sourcing contract |
|---|---|---|
| **Processor agreement** | GDPR Art. 28 | Provider processes personal data only on instruction, with security measures and audit rights |
| **Transfers outside the EU** | GDPR Chapter V | Legal basis, e.g. adequacy decision or standard contractual clauses |
| **Supply chain security** | NIS2 Art. 21 | Essential and important entities assess and manage the security of their suppliers |
| **ICT third-party risk** | DORA Art. 28–30 | Financial entities: register of contracts, exit strategies, mandatory contract clauses |

::: callout
You can outsource the **service**, but not the **accountability**.
:::

::: source
Regulation (EU) 2016/679; Directive (EU) 2022/2555; Regulation (EU) 2022/2554.
:::

::: notes
Link to session 7. GDPR: the enterprise stays the controller; the provider is a processor bound by a contract under Art. 28; data transfers to third countries follow Chapter V (Art. 44 ff.). NIS2: RNM is an essential entity because of the regional trains (session 7), so it must include supply chain security, i.e. the security of its direct suppliers and service providers, in its risk management measures (Art. 21; in Germany § 30 BSIG). DORA does not apply to RNM, but to its payment provider — which therefore asks for DORA clauses in its own contracts. The callout is the key message for the exam: responsibility towards customers, authorities and auditors remains with the enterprise. Link to session 8: ISO/IEC 27001 Annex A has controls for supplier relationships and for the use of cloud services.
:::

---

# Mini Exercise: Which Service Model? {.exercise}

Decide for each need of *Rhein-Neckar Mobil Group* whether you would choose **IaaS**, **PaaS**, **SaaS** — or **no cloud** — and say what stays **with the group**.

1. A new **customer service** tool for all three units
2. The **fare back-end** must leave data centre 1 before it is replaced
3. The **mobility app** back-end that the group develops itself
4. The **ticket device** software on 400 buses
5. A **data analytics** platform for passenger numbers and revenue

::: notes
Pairs, 5 min + 5 min discussion. Expected answers (several defensible): 1 SaaS — commodity, mature market; the helpdesk SaaS already exists and can be extended (session 13); stays with RNM: configuration, customer data, access rights, processor agreement. 2 IaaS ("rehost") — the old system cannot be rebuilt for PaaS; quick move of virtual servers; RNM keeps operating system patches, application, backups unless bought as a managed service; alternative: colocation or managed hosting. 3 PaaS (container platform, managed database, API management) — the group writes the differentiating code, the provider runs the platform; stays: code, data, security configuration, cost control. 4 No cloud for the device software itself: it must run offline on the bus (session 8); the back-end it uploads to can be in the cloud. 5 PaaS or SaaS analytics service — elastic, modern tools; stays: data model, data quality, data protection (passenger data, location data), who may see revenue. Lesson: the service model follows the make-or-buy decision — the more you build yourself, the further down the stack you buy.
:::

---

# Multi-Sourcing and Vendor Management {.section}

Steering many providers

---

# Multi-Sourcing

::: columns
**What it is**

- Services are bought from **several** internal and external providers, each chosen for what it does best
- Typical today: a few SaaS vendors, one or two cloud platforms, a hosting partner, application specialists, the own IT
- Replaces large single-provider deals in many enterprises
|||
**What it needs**

- **Service integration**: someone must make the providers work together end to end
- Clear **interfaces** between providers: incidents, changes, data
- An **architecture** that keeps the landscape coherent
- **Governance** of contracts and performance across providers
:::

::: callout
Multi-sourcing reduces dependency on one provider — but moves the **integration effort** to the customer.
:::

::: source
Own wording based on Cohen and Young (2006) and AXELOS (2019).
:::

::: notes
Cohen and Young (2006) describe multisourcing as the disciplined provisioning and blending of business and IT services from the optimal set of internal and external providers. The practical problem: when the mobility app fails, is it the app team, the API platform, the cloud provider or the payment provider? Without end-to-end incident management and agreed hand-overs, each provider proves its own SLA was met while the customer service is down. The role that coordinates many providers is often called service integration (in practice also SIAM, service integration and management); it can be kept in-house or bought from one lead provider. Link to sessions 5 and 6: the service value chain runs across several organisations; the SLA can only promise what the OLAs and underpinning contracts allow.
:::

---

# The Vendor Management Life Cycle

![Vendor management life cycle with six phases arranged in a circle: 1 sourcing strategy (what to buy, which model), 2 selection (requirements, tender, evaluation), 3 contract (services, SLAs, prices, audit and exit clauses), 4 transition (hand-over of staff, data, knowledge), 5 operation and steering (SLA reviews, changes, relationship), 6 renewal or exit (re-tender, insource, switch provider), then back to the sourcing strategy. In the centre: the retained organisation steers the provider: owner, architecture, contracts](img/sourcing-vendor-lifecycle.png){width=70%}

::: source
Own illustration based on Tiemeyer (2023, chapter 8) and AXELOS (2019).
:::

::: notes
Tiemeyer (2023, section 8.6) treats supplier management with its phases, supplier classification and supplier relationship management; ITIL 4 has a supplier management practice in the group of general management practices (AXELOS, 2019; session 5). The phases here are an own compilation. Emphasise the two phases most often underestimated: transition (knowledge leaves with the staff who move or leave; the first months after a transition typically show quality problems) and exit (if the exit is not planned in the contract, the provider has all the negotiating power at renewal). Selection typically uses a requirements catalogue, a tender (request for proposal) and a weighted scoring of offers — the same scoring logic as the project portfolio in session 4.
:::

---

# What a Sourcing Contract Must Settle

| Element | Content | Link |
|---|---|---|
| **Service description and SLAs** | Scope, service levels, measurement, reporting, service credits | Session 6 |
| **Prices and changes** | Price model, indexation, how changes are ordered and priced | Session 4 |
| **Security and data protection** | Measures, processor agreement, certificates, incident reporting | Sessions 7 and 8 |
| **Audit and information rights** | Customer and auditors may check the provider | Session 7 |
| **Steering bodies** | Regular service reviews, escalation path, named roles | Session 3 |
| **Exit** | Data return and formats, support during hand-over, notice periods | Data Act |

::: source
Own compilation based on Tiemeyer (2023, chapter 8), AXELOS (2019) and Regulation (EU) 2022/2554, Art. 30.
:::

::: notes
For financial entities, DORA Art. 30 makes many of these elements mandatory for ICT service contracts — e.g. a description of services and locations, service levels, cooperation with authorities, termination rights and exit strategies; other sectors use the list as good practice. Underpinning contracts from session 6 are exactly such contracts: the 4-hour replacement target for ticket devices needed a spare pool because the manufacturer's contract only guaranteed next-working-day repair. Ask: which of these elements was missing when a company in your experience changed a provider? (Usually exit: data come back as unreadable exports.)
:::

---

# The Retained Organisation {.optional}

Even after outsourcing, the enterprise needs a small, strong **retained IT function**. Its core capabilities include:

- **Leadership** and **business systems thinking**: link IT to the business strategy
- **Architecture planning**: keep the landscape coherent across providers
- **Informed buying**: know the market, choose sourcing options, run tenders
- **Contract facilitation** and **contract monitoring**: make contracts work, hold providers to them
- **Vendor development**: grow the value of a relationship over time

::: source
Own wording based on Feeny and Willcocks (1998).
:::

::: notes
Self-study. Feeny and Willcocks (1998) describe nine core IS capabilities that an enterprise must keep in-house to exploit IT, even when most delivery is outsourced; the slide groups some of them. The two-person architecture team of RNM (session 10) is part of the retained organisation: it cannot run platforms, but it must decide which platforms the providers run. Typical mistake: outsourcing the people who understood the old system and then having nobody left who can judge the provider's proposals. Exam point: "outsourcing" never means "no IT department".
:::

---

# Sourcing in Enterprise Architecture Management

- **Transparency**: the EA repository records for each application its **provider**, **hosting**, **contract end** and **sourcing model** (session 11)
- **Impact analysis**: which capabilities depend on a provider — what if it fails or is acquired? (sessions 8 and 10)
- **Portfolio and roadmap**: contract ends and end of vendor support set the **timing** of TIME decisions (session 13)
- **Sourcing principles**, e.g. SaaS for non-differentiating capabilities, data stored in the EU, no new single-provider dependency for critical services
- **Integration**: every external service needs interfaces — via the integration platform (session 14)

::: source
Own wording based on Hanschke (2023) and Keller (2017).
:::

::: notes
Keller (2017) lists sourcing among the goals that EAM supports, and Hanschke (2023) describes sourcing as one of the usage scenarios of EAM (session 10). In practice the EA repository is where the sourcing view comes together: "which of our 180 applications run at provider X?" is a question the board asks after every provider incident or acquisition news — and one that often takes days to answer without a repository. The capability map of session 12 is a good basis for sourcing decisions: differentiating capabilities are candidates for make, commodity capabilities for buy.
:::

---

# Sourcing Pitfalls {.optional}

- **Outsourcing a mess**: unclear processes and undocumented systems become more expensive, not cheaper
- **Price only**: the cheapest offer wins, transition and management costs are forgotten
- **No exit plan**: data, know-how and tools stay with the provider
- **Too few people retained** to steer the providers
- **Shadow sourcing**: business units buy SaaS without IT, security or purchasing

::: source
Own wording based on Lacity et al. (1996), Dibbern et al. (2004) and Feeny and Willcocks (1998).
:::

::: notes
Self-study. Countermeasures: stabilise and document before outsourcing; evaluate offers on total cost over the contract term plus transition and retained organisation; agree exit clauses and data formats in the contract; define the retained capabilities before the deal; a SaaS approval process with a light check of data protection, security and integration (link to shadow IT, session 7, and to the iPaaS governance question in session 14).
:::

---

# Case Exercise: A Sourcing Decision for Rhein-Neckar Mobil Group {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–14): 3,200 employees, €410 million turnover, about 180 applications; mobility app planned for 2028.

- **Group IT** runs two data centres; data centre 1 must be **retired** within three years (roadmap, session 13)
- The **fare back-end** (14 years, two developers) must be **replaced**; a vendor offers a fare management **SaaS** used by other transport companies
- The **integration platform** (session 14) is approved — but nobody at Group IT knows the technology
- The car-sharing app team (**six developers**) is fully booked; an agency offers a **nearshore** team in Poland, an Indian provider an **offshore** team at a lower day rate
- Payroll, helpdesk tool and finance ERP are already **external**; the **works council** must be involved in staff questions

::: notes
Read the case together (2 min). Hints if asked: RNM is an essential entity under NIS2 (session 7) and processes location and payment data (GDPR); the BIA of the ticketing service (session 8) requires the fare back-end to be back within a few hours; the two-person architecture team reports to the CIO (session 10); budget for staff increases is limited. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. Make or buy: decide for **data centre 1**, the **fare back-end successor**, the **integration platform** and the **mobility app** development. Justify each with **two criteria**.
2. For your "buy" decisions, choose the **service model** (IaaS, PaaS, SaaS, managed service) and say what stays **in-house**.
3. App development: compare **in-house**, **nearshore** and **offshore**. What do you recommend, and for which tasks?
4. Your decisions create **multi-sourcing**. Which **retained roles** does Group IT need, and how are the providers coordinated?
5. Name **four contract elements** and two **compliance requirements** for the most critical contract, and plan the **exit**.

::: notes
Groups of 4–5, about 30 min + 10 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 Data centre 1: buy — infrastructure is a commodity; cost and skills (no investment in an old data centre), roadmap deadline. Fare back-end successor: buy and differentiate — a mature SaaS used by other transport companies fits the standard part (fares of the association, sales, revenue sharing), the regional tariff is shared with the association; keep the differentiating best-price logic of the app in-house or on top; criteria: know-how risk (two developers), maturity of the market, but criticality (BIA) — needs strong SLAs. Accept make with the argument that fare logic differentiates the mobility app, if the student addresses the know-how risk. Integration platform: buy as iPaaS/managed platform or buy the product with a partner for operation in the first years — no skills in-house, speed; but keep integration architecture and principles in-house. Mobility app: make (product ownership, architecture, core code in-house) with external capacity — differentiating, fast feedback with users.
2 Data centre 1 → IaaS (rehost) or managed hosting/colocation; in-house: application operation, patching unless bought, backups and recovery tests. Fare SaaS → SaaS; in-house: fare data, configuration, access rights, interfaces, revenue reconciliation. Integration → iPaaS (PaaS) or managed service; in-house: integration principles, interface ownership, repository data. App → PaaS (container platform, managed databases, API management); in-house: code, data, security configuration, cost control.
3 In-house: product owner, architect, core developers — close to users and business, but capacity limit. Nearshore (Poland): EU law (no third-country transfer), little time difference, short travel, workshops possible — good for feature development alongside the in-house team. Offshore (India): lowest rate, large talent pool, but time difference, coordination and a GDPR third-country transfer if personal data are accessed — suitable for well-specified tasks such as test automation, not for discovery. Recommendation e.g.: in-house core plus nearshore team; offshore only for testing with anonymised data.
4 Providers: hosting/IaaS provider, fare SaaS vendor, integration platform provider or partner, nearshore agency, plus existing payroll, helpdesk and ERP vendors. Retained roles: CIO and sourcing/vendor manager, architecture team (target landscape, principles), service owners per service, contract and licence management, security officer for supplier security, a service integration function for end-to-end incident and change management across providers. Coordination: joint service reviews, one incident process with agreed hand-overs, provider OLAs/UCs aligned with the SLAs to the units, interfaces via the integration platform.
5 Most critical: fare SaaS (ticket sales and revenue). Contract elements: SLAs aligned with the BIA (availability, recovery time, support hours 4:30–0:30), price model and indexation, security measures and incident reporting, audit rights, data location in the EU, change process, exit with data return in a usable format and support. Compliance: GDPR Art. 28 processor agreement; NIS2 supply chain security (RNM is essential); also check the payment provider's DORA requirements. Exit: keep a copy of fare and sales data, documented interfaces via the integration platform (only the adapter changes), notice periods aligned with the roadmap, re-tender before contract end. Works council: involve when staff tasks change or data centre staff move.
:::

---

# Key Takeaways

- **IT sourcing** decides who provides which IT services under which arrangement — along the dimensions scope, provider, location, degree, number of providers and delivery model
- **Make or buy** depends on strategic importance, specificity, market maturity, life-cycle cost, skills and risk: make what differentiates, buy what is standard — and keep control
- **Cloud sourcing** (IaaS, PaaS, SaaS) shifts responsibility layer by layer to the provider; data, access and **accountability** stay with the enterprise
- **Multi-sourcing** needs service integration, a capable **retained organisation** and **vendor management** over the whole life cycle — including the exit

---

# Next Session: EAM Frameworks I — TOGAF

- Purpose of EAM frameworks
- The TOGAF Architecture Development Method (ADM)
- Content framework and architecture governance

::: callout
**Preparation:** find out how your training company **decides on architecture**: is there an architecture board, written architecture principles or a framework such as TOGAF? Bring one example of an architecture decision and **who** took it.
:::

::: notes
Many students will find "no framework, but a few principles and an architecture board" — that is a good starting point: TOGAF is a toolbox, not something enterprises implement as a whole. Today's sourcing decisions reappear in TOGAF Phases E and F (opportunities and solutions, migration planning), where build-or-buy decisions are made for work packages.
:::

---

# References {.references}

- AXELOS. (2019). *ITIL Foundation: ITIL 4 edition*. TSO.
- Carmel, E., & Abbott, P. (2007). Why "nearshore" means that distance matters. *Communications of the ACM, 50*(10), 40–46. https://doi.org/10.1145/1290958.1290959
- Cohen, L., & Young, A. (2006). *Multisourcing: Moving beyond outsourcing to achieve growth and agility*. Harvard Business School Press.
- Dibbern, J., Goles, T., Hirschheim, R., & Jayatilaka, B. (2004). Information systems outsourcing: A survey and analysis of the literature. *The DATA BASE for Advances in Information Systems, 35*(4), 6–102. https://doi.org/10.1145/1035233.1035236
- Directive (EU) 2022/2555 of the European Parliament and of the Council of 14 December 2022 on measures for a high common level of cybersecurity across the Union (NIS 2 Directive). (2022). *Official Journal of the European Union*, L 333, 80–152. http://data.europa.eu/eli/dir/2022/2555/oj
- Feeny, D. F., & Willcocks, L. P. (1998). Core IS capabilities for exploiting information technology. *Sloan Management Review, 39*(3), 9–21.
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Lacity, M. C., Willcocks, L. P., & Feeny, D. F. (1996). The value of selective IT sourcing. *Sloan Management Review, 37*(3), 13–25.
- Mell, P., & Grance, T. (2011). *The NIST definition of cloud computing* (NIST Special Publication 800-145). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-145
- Prahalad, C. K., & Hamel, G. (1990). The core competence of the corporation. *Harvard Business Review, 68*(3), 79–91.
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1–88. http://data.europa.eu/eli/reg/2016/679/oj
- Regulation (EU) 2022/2554 of the European Parliament and of the Council of 14 December 2022 on digital operational resilience for the financial sector (DORA). (2022). *Official Journal of the European Union*, L 333, 1–79. http://data.europa.eu/eli/reg/2022/2554/oj
- Regulation (EU) 2023/2854 of the European Parliament and of the Council of 13 December 2023 on harmonised rules on fair access to and use of data and amending Regulation (EU) 2017/2394 and Directive (EU) 2020/1828 (Data Act). (2023). *Official Journal of the European Union*, L, 2023/2854. http://data.europa.eu/eli/reg/2023/2854/oj
- Tiemeyer, E. (Ed.). (2023). *Handbuch IT-Management: Konzepte, Methoden, Lösungen und Arbeitshilfen für die Praxis* (8th ed.). Hanser.

TOGAF® is a registered trademark of The Open Group. ITIL® is a registered trademark of PeopleCert group. Diagrams in this deck are own illustrations. Frameworks are described in own words.
