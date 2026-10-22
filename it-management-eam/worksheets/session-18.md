---
course: IT Management and EAM
session: 18
title: EAM Tools and Course Synthesis
subtitle: Course-wide revision set (practice only) on IT management, enterprise architecture management and EAM tools
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet is a **mixed revision set for practice**. It is not an exam and contains no exam questions; it uses the question types of the worksheets of sessions 1–17 and of the exam Q&A. It covers the whole course: the fields of action of IT management (Krcmar, 2015), strategy and alignment (Henderson & Venkatraman, 1993), governance (ISACA, 2018), service management (AXELOS, 2019), enterprise architecture management (Hanschke, 2023; The Open Group, 2022, 2023) and the EAM tool SAP LeanIX with its fact sheets, subscriptions and reports (SAP LeanIX, n.d.-a, n.d.-b, n.d.-c, n.d.-d, n.d.-e, n.d.-f). The tasks build on each other: recall first, then application to cases, then one integrated case in the style of an exam question. Paper, pencil and a calculator are enough. Try each task before you look at the hints; compare your answers with fellow students and bring open points to the Q&A.

## True or False? A Walk Through the Course

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) In Krcmar's model, the management of information and communication technology is the top level, because the business needs technology first.
- b) In the strategic alignment model, the "competitive potential" perspective starts from the IT strategy and changes the business strategy.
- c) A problem is the cause, or potential cause, of one or more incidents; a workaround removes the cause permanently.
- d) The recovery time objective (RTO) must not be longer than the maximum tolerable period of disruption (MTPD).
- e) A business capability describes what an enterprise does, independent of organisation units, processes and applications.
- f) In the TIME model, "tolerate" stands for applications with high functional fit and low technical fit.
- g) In the TOGAF ADM, requirements management is a separate phase that runs only once, after Phase H.
- h) In SAP LeanIX, the quality seal of a fact sheet breaks when a user who is neither responsible nor accountable changes its data.

::: answer lines=10
:::

::: hint
For f), draw the TIME portfolio with its two axes. For g), recall the picture of the ADM cycle: where is requirements management drawn?
:::

::: solution
- a) **False.** The **information economy** (information demand, supply and use) is the top level; it drives the information systems, which drive ICT at the bottom.
- b) **True.** The IT strategy (new technology capabilities) leads to a new business strategy and then to organisational changes.
- c) **False.** The first half is true, but a **workaround** only reduces or removes the impact; the permanent fix removes the cause, usually through a change.
- d) **True.** Recovery must happen before the business can no longer tolerate the disruption; in practice the RTO is set clearly below the MTPD.
- e) **True.** A capability says *what* the enterprise must be able to do; processes say *how*, units *who*, applications *with what*.
- f) **False.** "Tolerate" stands for **low functional fit and high technical fit**; high functional and low technical fit is **migrate**.
- g) **False.** Requirements management sits at the **centre** of the ADM and is active **throughout** all phases.
- h) **True.** Changes by other members break the seal ("check needed"); changes to subscriptions, comments, metrics or surveys do not.

Marking hint: one point per item; for false statements the point requires the correction.
:::

## Pairs That Get Mixed Up

Explain the **difference** in each pair in one or two sentences and give an **example** for each side. Use a context of your choice (e.g. your training company, a hospital, a logistics company).

1. IT governance — IT management
2. Utility — warranty
3. SLA — OLA — underpinning contract
4. Recovery time objective (RTO) — recovery point objective (RPO)
5. Business capability — business process
6. Deliverable — artefact (TOGAF)
7. Serving — realisation (ArchiMate)

::: answer lines=16
:::

::: hint
Name the **criterion** of the difference first (who? when? what for?), then the two sides. "Is more detailed" is rarely the right criterion.
:::

::: solution
1. **Criterion: directing vs. executing.** Governance defines decision rights and accountability and evaluates, directs and monitors (e.g. the board decides that IT investments over €500,000 go to the steering committee); management plans, builds and runs within this frame (e.g. the CIO plans the rollout of a new HR system).
2. **Criterion: what the service does vs. how well it performs.** Utility is fitness for purpose — the features (e.g. the e-mail service sends and receives mail with attachments); warranty is fitness for use — availability, capacity, security, continuity (e.g. 99.5 % availability on working days, mailbox of 50 GB).
3. **Criterion: who agrees with whom.** SLA between the service provider and the customer (IT department and sales); OLA between the provider and an internal unit that supports the service (IT department and the internal network team); underpinning contract with an external supplier (hosting provider). The OLA and contract must support the SLA targets.
4. **Criterion: time vs. data.** RTO is the time within which a process or system must be running again after a disruption (e.g. 4 hours for order intake); RPO is the maximum acceptable data loss measured in time (e.g. 15 minutes of orders), which determines the backup or replication interval.
5. **Criterion: what vs. how.** A capability is a stable ability, independent of units and systems (e.g. "customer management"); a process is a sequence of activities with a trigger and a result that uses capabilities (e.g. "handle a customer complaint").
6. **Criterion: agreed work product vs. single description.** A deliverable is a formally agreed and signed-off work product (e.g. the architecture definition document); an artefact is a catalogue, matrix or diagram inside it (e.g. the application–capability matrix).
7. **Criterion: use vs. make real.** Serving: an element provides its functionality to another that uses it — the arrow points to the user (application service "fare calculation" serves the process "sell ticket"); realisation: a concrete element makes an abstract one real (the ticket device software realises "fare calculation").

Marking hint: one point per pair if the criterion and both sides are correct; half a point if only the examples are correct.
:::

## Calculations at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1, 4 and 11–17), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, now runs a **SaaS WMS**, a **customer portal** for shipment tracking, a route planner (SaaS), fleet telematics and a billing SaaS.

1. **Availability.** The SLA for the customer portal promises **99.7 %** availability, measured **24/7** over a **30-day** month. Last month there were two outages of 70 and 80 minutes. Was the target met? What would you add to the SLA?
2. **Interfaces.** Nine applications exchange data. How many interfaces are possible at most with point-to-point connections, and how many connections with an integration platform? What does the platform not remove?
3. **Business case.** A tracking app for customers costs €400,000 once; it saves €150,000 per year in call-centre work and costs €30,000 per year to run. Calculate the simple **payback period** and the **net present value** over five years with the discount factors 0.926 · 0.857 · 0.794 · 0.735 · 0.681 (8 %).

::: answer lines=14
:::

::: hint
Availability = (agreed service time − downtime) ÷ agreed service time × 100 %. With equal net benefits every year, multiply the net benefit by the sum of the discount factors.
:::

::: solution
1. Agreed service time: 30 × 24 h = 720 h = 43,200 min. Allowed downtime: 0.3 % × 43,200 min = **129.6 min**. Actual: 70 + 80 = **150 min** → availability = (43,200 − 150) ÷ 43,200 = **99.65 %** → target **missed**. Add to the SLA: a maximum duration of a single outage, how planned maintenance is counted, measurement method and reporting, and consequences (service credits) — session 6.
2. Point-to-point: n(n−1)/2 = 9 × 8 / 2 = **36** possible interfaces. With a platform: about **9** connections, one per application. The platform does not remove the **mapping and transformation logic**; it concentrates it in one place where it can be monitored and reused — and it becomes a critical central component (session 14).
3. Net benefit: 150,000 − 30,000 = **€120,000 per year**. Payback = 400,000 ÷ 120,000 = **3.33 years**. Sum of discount factors = 3.993; NPV = −400,000 + 120,000 × 3.993 = −400,000 + 479,160 = **about +€79,000** → positive. Comment: only if the call-centre savings are real (staff reassigned or reduced) and owned by a benefit owner (session 4).

Marking hint: two points per part (one for the calculation with formula, one for the interpretation).
:::

## The EAM Tool at Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10–17), a tour operator with 25 travel agencies and a call centre, wants to sell personalised trips online and through an **app by 2030**. It is building a new **booking platform**, uses a SaaS **customer platform** and develops the app with a nearshore partner (worksheets 15–17). The two-person architecture team has just introduced SAP LeanIX and wants to record:

| No. | Item |
|---|---|
| 1 | The new booking platform |
| 2 | The booking system from 2005 that the booking platform replaces |
| 3 | "Trip planning and booking" as something the company must be able to do |
| 4 | The call centre and the travel agencies |
| 5 | The interface through which hotels send prices and availability |
| 6 | Booking and customer as data |
| 7 | The public cloud region in the EU where the booking platform runs, and its provider |
| 8 | The programme "app by 2030" and its goal "60 % of bookings online" |

1. Assign each item to a **fact sheet type** of the SAP LeanIX meta model.
2. Who should be **responsible**, **accountable** and **observer** for the fact sheet of the booking platform? Justify briefly.
3. Which **report** answers each question: (a) "Which applications support trip planning and booking, and which of them are being phased out?" (b) "Which applications should we invest in, and which should we migrate?" (c) "When will the booking system from 2005 be switched off, and how long do old and new run in parallel?"
4. The CEO says: "Now that we have the tool, the architecture is documented." Respond in three sentences.

::: answer lines=16
:::

::: hint
The meta model has four layers: strategy and transformation, business, application and data, technical. The application is the central type that links business and IT.
:::

::: solution
1. 1 **Application**; 2 **Application** (with life cycle "phase-out"); 3 **Business capability**; 4 **Organization** (two units, or one organization with sub-units); 5 **Interface** (between the hotel systems and the booking platform; accept application for the external hotel systems at the other end); 6 **Data object** (booking, customer); 7 **IT component** (the cloud service / region) and **provider** (the cloud provider); 8 **Initiative** (programme) and **objective** (goal).
2. Responsible: the IT owner or product owner of the booking platform (maintains the data, e.g. life cycle, technical fit); accountable: the business owner, e.g. the head of sales or e-commerce (overall accountability, only one person); observers: the architects, the data protection officer or the nearshore partner's lead (informed of changes). Justification: data is maintained by those who know it, accountability lies with the business that decides on the application.
3. (a) **Landscape report** grouped by business capability, coloured by life cycle (accept matrix report with organisations as second axis). (b) **Portfolio report** with functional fit and technical fit (TIME). (c) **Roadmap report** with the life-cycle dates of the two applications.
4. E.g.: "The tool only stores and visualises what people enter and keep up to date. We still need owners, a maintenance concept with update triggers and quality checks (subscriptions, quality seal), and clear questions that the data must answer. Documentation is a means for decisions such as the roadmap to 2030, not a goal in itself."

Marking hint: four points for part 1 (half a point per item), one and a half points for part 2, one and a half points for part 3, one point for part 4.
:::

## Which Instrument? Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3 and 10–17) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system (HIS) and its own data centre; one hospital suffered a ransomware attack last year. The group plans a joint **patient portal** and the programme "one group, one HIS". The new group CIO lists the following problems.

For each problem, name the **instrument or framework** from the course that you would use, the **session** it comes from, and **why** it fits. Name a different instrument for each problem.

1. Nobody knows which applications the four hospitals run, who owns them and on which servers they run.
2. Each hospital decides on IT investments itself; the group board wants clear decision rights.
3. The board asks whether the joint patient portal pays off.
4. After the ransomware attack, the board wants to know which processes must be restored first and how fast.
5. Users complain that the incident handling of the four service desks is slow and inconsistent.
6. The CIO wants to decide which of the four HIS should become the group HIS.
7. The portal must exchange appointments and findings with four HIS and the billing ERP without building a web of interfaces.

::: answer lines=16
:::

::: hint
Ask for each problem: which **question** does it raise (who decides? what is it worth? what is critical? what do we have?) — then pick the instrument that answers exactly this question.
:::

::: solution
Example answers (accept other instruments with a convincing reason):

1. **EA data collection and repository with a lean meta-model and application fact sheets** (session 11), ideally in an **EAM tool** (session 18): document analysis, imports from the CMDBs, interviews with owners; the meta-model links application, owner and technology component.
2. **IT governance**: decision rights for the key IT decisions, archetypes, evaluate – direct – monitor; **COBIT** or **ISO/IEC 38500** as framework (session 3) — e.g. a group IT steering committee for investments above a threshold.
3. **Business case** with NPV and payback, owned benefits and a sensitivity analysis; **project portfolio management** (session 4).
4. **Business impact analysis** with MTPD, RTO, RPO and MBCO in business continuity management (ISO 22301, BSI-Standard 200-4; session 8).
5. **ITIL 4 incident management and service desk** with a common priority scheme (impact × urgency), one tool and SLAs (sessions 5 and 6); problem management for recurring causes.
6. **Application portfolio management with TIME** (functional and technical fit), a **target landscape** and **roadmap** (session 13); for the whole programme the **TOGAF ADM** with architecture principles and an architecture board (session 16).
7. **Enterprise application integration** with an **integration platform** (hub, API management or events) instead of point-to-point (session 14).

Marking hint: one point per problem (half for a suitable instrument, half for the reason); deduct half a point if the same instrument is used twice.
:::

## Exam-Style Practice Task: One Year After the Acquisition at Kurpfalz Sanitär AG

*This is a practice task in exam style. It is not an exam question.*

*Kurpfalz Sanitär AG* (sessions 2 and 5–17), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers; orders received by 14:00 are delivered the same day from the central warehouse. A year ago it acquired a smaller **wholesaler in the Saarland**; the platform is to become a **marketplace** for manufacturers and other wholesalers (worksheets 12–17). The current situation:

| Topic | Situation |
|---|---|
| Strategy | The board wants third-party sellers on the platform within 18 months; marketplace commission should become a new revenue stream |
| Applications | 20-year-old customised Kurpfalz ERP in the own server room (two people know the customisations); externally hosted order platform with six in-house developers; Saarland cloud ERP (6 years old); Saarland warehouse system maintained by one developer; nightly files to carriers |
| Architecture | Two architects; architecture principles and an architecture board have been set up; the application list is still a spreadsheet with about 90 entries; no common notation |
| Operations | Service desk of two people, office hours only; the platform's hosting contract guarantees 99 % availability per month and support Mon–Fri 8:00–16:00 |
| Customers and rules | A large hospital group requires evidence of information security from its suppliers; an ISMS is being built |

**Tasks:**

1. Which **alignment perspective** of the strategic alignment model fits the marketplace plan? Justify with the case. (2 points)
2. Who should **decide** on the marketplace investment, and what is the role of the **architecture board** in this decision? (3 points)
3. Classify the **Kurpfalz ERP** and the **Saarland cloud ERP** with the **TIME** model and outline a **roadmap** with two transition states for the ERP landscape. (4 points)
4. Recommend an **integration approach** for connecting the third-party sellers and justify it with two arguments. (3 points)
5. Should Kurpfalz **build** the marketplace functions itself or **buy** them as **SaaS**? Give a recommendation with two criteria. (3 points)
6. Assess whether today's **service desk** and **hosting contract** fit the marketplace. Propose two concrete **SLA** targets and one **RTO** for order intake. (4 points)
7. The architects want to replace the spreadsheet with an **EAM tool**. Name **three requirements** for the tool and **two steps** to take before buying it. (3 points)
8. Explain how the instruments of tasks 2, 3 and 6 **work together** in one sentence each — what does each need from the others? (2 points)

::: answer lines=40
:::

::: solution
Marking guide (24 points):

**1. Alignment perspective (2 points)**

- **Competitive potential** (1): the platform and its technology (the IT strategy) open a new business model — marketplace commissions — and change the business strategy. Accept **technology transformation** if argued: the business strategy (marketplace) requires a new IT strategy and infrastructure.
- Case reference (1): new revenue stream, third-party sellers, the platform as the basis.

**2. Decision and architecture board (3 points)**

- Decision on the investment (1.5): the **IT steering committee** (CEO, CFO, CIO, head of sales) or the board on its proposal, based on a **business case** and portfolio priorities (sessions 3 and 4); the CEO or head of sales as accountable business owner.
- Architecture board (1.5): reviews the solution against the **architecture principles** (e.g. "interfaces only via the integration platform"), gives an architecture assessment as input, later carries out **compliance reviews** and grants **dispensations** — it does not decide on funding (session 16).

**3. TIME and roadmap (4 points)**

- Kurpfalz ERP (1): functional fit high (runs order processing, warehouse, finance) but technical fit low (20 years, heavy customisation, two experts) → **migrate**.
- Saarland cloud ERP (1): standard cloud ERP, little customisation → technical fit high; functional fit to be checked for the larger business → **invest** (as target platform) or **tolerate** if not chosen as the target; justification required.
- Roadmap (2): e.g. transition 1 — integration platform, finance of both companies on the cloud ERP, Kurpfalz ERP keeps order and warehouse; transition 2 — order processing and warehouse moved, Saarland warehouse system replaced or integrated; target — one cloud ERP, Kurpfalz ERP retired. One point for two plausible transition states, one point for a dependency or order factor (e.g. marketplace deadline, skills risk of the two experts, peak season).

**4. Integration (3 points)**

- Recommendation (1): **API management** on the integration platform: a documented seller API (product data, stock, orders) plus **events** for order and shipping status; accept iPaaS with a reason.
- Two arguments (2): many external partners → one standard interface instead of point-to-point per seller; security and access control (API keys, throttling) for the hospital group's security requirements; loose coupling — the ERP migration does not affect the sellers; monitoring.

**5. Build or buy (3 points)**

- Recommendation (1): e.g. **buy** marketplace standard functions (seller onboarding, commission billing) as **SaaS** and **build** only the differentiating parts (installer experience, same-day logistics) with the six in-house developers. Accept "build" if justified by strategic importance and existing skills.
- Two criteria (2): strategic importance and specificity; market maturity of marketplace software; time to market (18 months); skills and capacity of six developers; life-cycle cost; risk and exit.

**6. Service desk, hosting, SLA, RTO (4 points)**

- Assessment (2): two people in office hours and support only Mon–Fri 8:00–16:00 do not fit a marketplace with external sellers and orders until 14:00 and later; 99 % per month allows over 7 hours of downtime — too much; the hosting contract does not underpin a higher SLA.
- SLA targets (1): e.g. availability 99.8 % 24/7 per month with a maximum single outage of 60 minutes; incident response for priority 1 within 30 minutes, 7:00–20:00 Mon–Sat; resolution targets per priority; reporting monthly.
- RTO (1): e.g. **2 hours** for order intake during business days (justified with the 14:00 cut-off and same-day delivery), with a fallback (orders by phone or e-mail) and an MTPD of about half a day; accept other values with a reason.

**7. EAM tool (3 points)**

- Three requirements (1.5): meta-model that covers applications, capabilities, interfaces, IT components and data (configurable); import from the spreadsheet and the CMDB, API; owner roles and quality checks; reports for landscape, TIME portfolio and roadmap; SaaS with EU data location and export for exit; usable for business owners.
- Two steps before buying (1.5): define stakeholder questions and the lean meta-model; clean the spreadsheet (granularity rules, owners); clarify who maintains the data; proof of concept with own data; sourcing and contract check (session 15).

**8. Interplay (2 points)**

- E.g.: governance decides with the business case and the architecture assessment, which needs the **TIME** and **roadmap** information from the repository; landscape planning needs the **criticality and RTO** from the BIA and the **service data** (incidents, costs) from operations; service and continuity management need the **dependencies** from the repository to set SLAs and recovery priorities. Two plausible links with what is exchanged, one point each.
:::

## Optional Challenge: Your Own Course Map {.optional}

Draw a **concept map** of the course on one A4 page: place at least **twelve** instruments or frameworks from sessions 1–18 (e.g. strategic alignment model, COBIT, IT balanced scorecard, ITIL service value chain, SLA, ISO 31000, BIA, ISO/IEC 25010, capability map, TIME, TOGAF ADM, ArchiMate, EAM tool) and connect them with **labelled arrows** that say what one gives to the other. Then mark the three connections you find hardest to explain and bring them to the Q&A.

::: answer lines=8
:::

::: solution
There is no single correct map. Good maps (one point each, up to four points):

- connect **strategy** to **planning** (e.g. "business strategy → strategic alignment model → IT strategy → capability map → target landscape");
- connect **planning** to **delivery** (e.g. "TIME → roadmap → project portfolio → business case → change enablement");
- connect **operations** back to **planning** (e.g. "incidents and problems → technical fit in TIME"; "IT costs from IT controlling → application fact sheet");
- connect **risk, security and quality** to the landscape (e.g. "BIA → criticality attribute in the repository"; "ISO/IEC 25010 → quality requirements in the business case");
- use **labelled** arrows that say what is passed on, not only "relates to".

Typical gaps: governance missing (who decides?), the information base missing (where do the data come from?), no feedback from operations to planning.
:::

## References {.references}

- AXELOS. (2019). *ITIL Foundation: ITIL 4 edition*. TSO.
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Henderson, J. C., & Venkatraman, N. (1993). Strategic alignment: Leveraging information technology for transforming organizations. *IBM Systems Journal, 32*(1), 4–16.
- ISACA. (2018). *COBIT 2019 framework: Introduction and methodology*. ISACA.
- Krcmar, H. (2015). *Informationsmanagement* (6th ed.). Springer Gabler. https://doi.org/10.1007/978-3-662-45863-1
- SAP LeanIX. (n.d.-a). *Fact sheet subscription*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/fact-sheet-subscription
- SAP LeanIX. (n.d.-b). *Fact sheets*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/factsheets
- SAP LeanIX. (n.d.-c). *Meta model*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/data-model
- SAP LeanIX. (n.d.-d). *Quality seal*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/quality-seal
- SAP LeanIX. (n.d.-e). *Reports*. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/reports
- SAP LeanIX. (n.d.-f). [TIME framework in SAP LeanIX enterprise architecture management]. Retrieved October 22, 2026, from https://docs-eam.leanix.net/docs/time
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.
- The Open Group. (2023). *ArchiMate 3.2 specification* (Document No. C226). Van Haren Publishing.

Company names and figures in the tasks are fictitious training examples. This worksheet is practice material only; it is not an exam and does not contain exam questions. SAP and LeanIX are trademarks of SAP SE; TOGAF® and ArchiMate® are registered trademarks of The Open Group; ITIL® is a registered trademark of PeopleCert; COBIT® is a registered trademark of ISACA.
