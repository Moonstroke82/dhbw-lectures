---
course: IT Management and EAM
session: 16
title: EAM Frameworks I: TOGAF
subtitle: Practice tasks on the purpose of frameworks, the phases of the ADM, the content framework, architecture principles and architecture governance
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 16: kinds of EAM frameworks and their benefits and limits (Keller, 2017; Hanschke, 2023), the TOGAF Architecture Development Method (ADM) with the Preliminary phase, Phases A–H and requirements management (The Open Group, 2022a), the content framework with deliverables, artefacts and building blocks (The Open Group, 2022b), and architecture governance: principles, the architecture board, architecture contracts, compliance reviews, levels of conformance and dispensations (The Open Group, 2022a, 2022b). Terms follow the session slides; the TOGAF Standard is described in own words. Paper and pencil are enough. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) TOGAF is a modelling language with a fixed notation for drawing architecture diagrams.
- b) In each of Phases B, C and D, the architecture team describes a baseline and a target and performs a gap analysis.
- c) Requirements management is done once, at the start of the ADM, before Phase A.
- d) An architecture building block describes what is needed in a vendor-neutral way; a solution building block is a concrete product or service that realises it.
- e) A project rated "compliant" in a TOGAF compliance review has built everything that the specification requires.
- f) A dispensation is a formal, documented and time-limited permission to deviate from the architecture.

::: answer lines=8
:::

::: hint
For c), look at where requirements management sits in the ADM cycle. For e), compare "compliant" with "fully conformant".
:::

::: solution
- a) **False.** TOGAF is mainly a **method framework** (with the ADM, a content framework and a governance part); a modelling language with a fixed notation is ArchiMate (session 17).
- b) **True.**
- c) **False.** Requirements management is **continuous**: it sits in the centre of the cycle and handles requirements that arise or change in every phase.
- d) **True.**
- e) **False.** "Compliant" means that what was built follows the specification, but **not everything** specified was built. Building everything as specified (and nothing extra) is **fully conformant**.
- f) **True.** It is granted by the architecture board and recorded in the repository.

Marking hint: one point per item; for false statements the point requires the correction.
:::

## Phases of the ADM at Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3 and 10–15) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system (HIS) and its own data centre; the group CIO wants to close the four data centres within five years and plans a joint **patient portal**. The CIO uses the ADM for the programme "one group, one HIS". The following activities are listed in random order:

| No. | Activity |
|---|---|
| 1 | The four HIS installations are documented as-is; a target with one HIS of vendor X and one patient master is described |
| 2 | The board of the group sets up an architecture board and approves eight architecture principles |
| 3 | A new requirement from the data protection officer (separate consent for the portal) is recorded and traced to the affected results |
| 4 | Physicians, nursing directors, the works council and the data protection officer are asked about their concerns; the sponsor signs the scope |
| 5 | The migrations of the four hospitals are grouped into work packages and two transition states are defined |
| 6 | The implementation partner's design for hospital A is checked against the principles before go-live |
| 7 | The work packages are put in order with the budget for the next three years |
| 8 | Two years later, a new federal law on digital health records is analysed to decide whether a new cycle is needed |
| 9 | Clinical processes "admit patient" and "transfer patient" are modelled as-is and to-be across the four hospitals |
| 10 | Server, network and cloud options for the single HIS are compared; the target hosting is chosen |

1. Assign each activity to a **phase** (Preliminary, A–H or requirements management).
2. Put the activities that belong to the cycle into the **typical order** of the ADM.
3. Activity 3 arrives while the team is working on Phase D. Explain **why** the ADM does not simply "carry on".

::: answer lines=14
:::

::: hint
One activity is done before the cycle starts, one runs alongside all phases. Phases B, C and D follow the same pattern for different domains.
:::

::: solution
1. 1 → **Phase C** (information systems: application and data architecture). 2 → **Preliminary** (architecture capability, governance, principles). 3 → **Requirements management**. 4 → **Phase A** (stakeholders, concerns, scope, statement of architecture work). 5 → **Phase E** (work packages, transition architectures). 6 → **Phase G** (implementation governance, compliance review). 7 → **Phase F** (migration planning with budget). 8 → **Phase H** (architecture change management). 9 → **Phase B** (business architecture). 10 → **Phase D** (technology architecture).
2. 2 (Preliminary) → 4 (A) → 9 (B) → 1 (C) → 10 (D) → 5 (E) → 7 (F) → 6 (G) → 8 (H); 3 can happen at any time.
3. A new requirement may change results of **earlier phases**: separate consent for the portal affects the business process (B), the data and application architecture (C) and possibly the scope (A). Requirements management assesses the **impact** and decides whether to go back (iteration) or to handle it in the current phase; carrying on would produce a technology architecture for an outdated target.

Marking hint: five points for part 1 (half a point per activity), two points for part 2, two points for part 3.
:::

## Deliverable, Artefact or Building Block at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1, 4 and 11–15), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, must replace its **warehouse management system (WMS)** because vendor support ends in two years (worksheet 15). The architecture team produces the following items:

1. The **statement of architecture work** for the WMS replacement, signed by the COO
2. A **list of all warehouses** with their WMS version, interfaces and site manager
3. "A **warehouse management service** that supports picking, stock, shipping and the 24-hour rule for pharma orders"
4. The **SaaS WMS of vendor W**, chosen in the tender
5. A **matrix** that shows which warehouse processes are supported by which applications
6. A **diagram** of the data flows between WMS, route planner, fleet telematics, billing and customer portal
7. The **architecture roadmap** with two transition states, approved by the IT steering committee
8. The group's **integration platform**, which every new application must use

For each item, decide whether it is a **deliverable**, an **artefact** (catalogue, matrix or diagram) or a **building block** (architecture or solution). Then explain in two sentences why the distinction between **architecture** and **solution** building blocks helps in the tender for the new WMS.

::: answer lines=12
:::

::: solution
1. **Deliverable** (formally agreed and signed). 2. **Artefact — catalogue**. 3. **Architecture building block** (what is needed, vendor-neutral). 4. **Solution building block** (concrete product). 5. **Artefact — matrix**. 6. **Artefact — diagram**. 7. **Deliverable** (approved roadmap). 8. **Solution building block** (an existing, reusable component); accept "building block" without the type if the student notes that the integration capability itself would be the architecture building block.

Tender: the architecture building block becomes the **requirements** of the tender (functions, the pharma rule, interfaces via the integration platform, data in the EU) without favouring a product; offers (solution building blocks) are then compared against the same requirements, and the chosen one can be checked for **conformance** later.

Marking hint: four points for the classification (half a point per item), two points for the explanation.
:::

## Writing Architecture Principles at Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10–15), a tour operator with 25 travel agencies and a call centre, wants to sell personalised trips online and through an **app by 2030**. It is building a new booking platform and a customer platform (SaaS); the app will be developed with a nearshore partner (worksheet 15). The new architect drafted these principles:

- P1: "We use modern technology."
- P2: "Customer data are kept in the customer platform only. Other applications read them via its interface and do not store their own copies."
- P3: "All applications are developed in-house so that we keep control."
- P4: "Standard software as a service is preferred for capabilities that do not differentiate us."

1. Assess each draft with the **quality criteria** for principles from the session. Which would you keep, rewrite or delete?
2. Write **one principle in full** with **name**, **statement**, **rationale** and **implications** for Bodensee Reisen AG.
3. P3 and P4 contradict each other. Who should resolve such a conflict, and how should the result be documented?

::: answer lines=16
:::

::: hint
Ask of each draft: could two architects disagree about whether a project follows it? Does it say why, and what it costs?
:::

::: solution
1. **P1**: delete or rewrite — not understandable or checkable ("modern" means anything), no rationale; could be rewritten as a technology standard (e.g. "supported versions only"). **P2**: keep — clear, checkable in a project review, supports the customer platform strategy; add rationale (one view of the customer, GDPR) and implications (interfaces, migration of copies). **P3**: delete or rewrite — not robust and not consistent with the sourcing strategy (SaaS customer platform, nearshore partner) and with P4; a rewritten version could be "differentiating capabilities are under own product ownership". **P4**: keep and complete — clear direction; add rationale and implications and define what "differentiate" means (e.g. via the capability map).
2. Example: **Name**: One leading system for customer data. **Statement**: Customer data are created and changed only in the customer platform; other applications use them via its interface and keep no own copies. **Rationale**: customers see the same data in agency, call centre, web and app; personalised offers need one complete customer view; fewer copies reduce data protection risk and effort for deletion requests. **Implications**: the booking platform and the app must use the interface; existing copies (e.g. in the old booking system and the newsletter tool) are migrated and removed; the customer platform needs an owner, an SLA and an exit plan; projects budget for integration.
3. The **architecture board** (or the body with the architecture mandate, e.g. CIO with the IT steering committee) decides which principle applies, normally by rewriting one of them so that they no longer conflict. The decision is **recorded** in the repository (governance records) and the principle set is updated; individual project exceptions are handled as **dispensations**.

Marking hint: four points for part 1 (one per draft), four points for part 2 (one per part), two points for part 3.
:::

## Compliance Review at Rheinland Logistik

The architecture board of *Rheinland Logistik GmbH* specified three requirements for every new application: **(S1)** interfaces only via the integration platform, **(S2)** single sign-on with the company directory, **(S3)** data stored in the EU. Three project designs are reviewed:

| Project | Design |
|---|---|
| New WMS (SaaS) | Uses the integration platform and single sign-on; data in an EU region; also offers a direct file export to the pharma customer that the board did not specify |
| Driver app | Uses single sign-on and stores data in the EU; sends deliveries directly to billing because "the platform is too slow" |
| Warehouse sensor pilot | Uses the integration platform and stores data in the EU; single sign-on is planned for the second release |

1. Determine the **level of conformance** of each design and justify it.
2. Recommend a **board decision** for each project (approve, approve with dispensation, rework, or change the architecture). State any **conditions**.
3. The driver app team argues that the platform really is too slow for real-time deliveries. What should the board consider before deciding?

::: answer lines=14
:::

::: hint
Check for each design: is anything built against the specification? Is anything missing? Is anything extra?
:::

::: solution
1. **New WMS: conformant** — all three requirements are met as specified, plus an extra feature (direct file export) outside the specification. **Driver app: non-conformant** — the direct interface to billing contradicts S1. **Sensor pilot: compliant** — what is built follows the specification, but S2 is not yet built; nothing extra.
2. WMS: **approve**; ask whether the extra export should go via the platform too (it is an interface) — accept "approve with the condition to move the export to the platform" or a dispensation for the export. Driver app: **rework** (send events via the platform) or **dispensation** with a deadline and a plan to migrate if real-time cannot be achieved yet. Sensor pilot: **approve with condition** (single sign-on in release 2, before more users) — or a time-limited dispensation for S2; it is a pilot.
3. Whether the problem is real (measurements, SLA of the platform), whether the **standard** must change — e.g. event-based integration on the platform for real-time needs (session 14) — which would be a change to the architecture via **Phase H**, the **risks** of a point-to-point exception (more interfaces, no monitoring, problems when billing is replaced), and that any exception is **time-limited and recorded**.

Marking hint: three points for part 1, three points for part 2, two points for part 3.
:::

## Exam-Style Task: Integrating the Saarland Wholesaler with the ADM at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–15), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers; orders received by 14:00 are delivered the same day from the central warehouse. The acquisition of a smaller **wholesaler in the Saarland** has closed; the platform is to become a **marketplace** for manufacturers and other wholesalers (worksheets 12–15). Known facts:

| Topic | Today |
|---|---|
| Kurpfalz | 20-year-old, heavily customised ERP in its own server room (two people know the customisations); externally hosted order platform with six in-house developers; tablet ordering app for 60 field sales representatives |
| Saarland | Standard cloud ERP (SaaS), 6 years old; own web shop; warehouse system maintained by one developer |
| Architecture | Two architects report to the CIO; an integration platform has been proposed (worksheet 14); no architecture principles or board yet |
| Governance | The IT steering committee (CEO, CFO, CIO, head of sales) decides on budgets; a large hospital group customer requires evidence of information security |

The CEO asks the CIO to use the TOGAF ADM for the integration programme "one company, one landscape".

**Tasks:**

1. Explain what an **EAM framework** is and name **two benefits** and **one limit** of using TOGAF for this programme. (3 points)
2. Describe what Kurpfalz Sanitär must do in the **Preliminary phase** and in **Phase A**: name two results of each and **three stakeholders** with one concern each. (5 points)
3. For **Phases B, C and D**, name one **baseline** element, one **target** element and the resulting **gap** each. (6 points)
4. Draft **two architecture principles** for the programme, one of them with **statement, rationale and implications**. (3 points)
5. The Saarland warehouse system must stay for 18 months, although it violates the planned principle "interfaces only via the integration platform". Explain how architecture governance should handle this case, using the terms **compliance review**, **architecture board** and **dispensation**. (3 points)

::: answer lines=32
:::

::: solution
Marking guide (20 points):

**1. Framework, benefits, limit (3 points)**

- Explanation (1 point): a reusable structure for architecture work — method (how to proceed), content (what to produce) and governance (who decides); TOGAF is mainly a method framework with content and governance parts.
- Two benefits (1 point, 0.5 each), e.g.: a proven sequence of steps for a complex merger; common language (baseline, target, gap) for two IT teams; completeness — all domains and stakeholders considered; governance elements give the small architecture team a mandate.
- One limit (1 point), e.g.: large and generic, must be tailored to a two-person team; risk of producing documents instead of results under time pressure; says little about politics and the people side of a merger.

**2. Preliminary and Phase A (5 points)**

- Preliminary, two results (1 point): e.g. mandate and role of the architecture team, architecture principles, an architecture board or decision path, tailored (lean) framework, repository/tool.
- Phase A, two results (1 point): e.g. architecture vision for "one company, one landscape", scope (both companies, all domains; marketplace in or out), stakeholder map, statement of architecture work signed by the CEO as sponsor, communications plan.
- Three stakeholders with concerns (3 points, 1 each), e.g.: CEO — integration on time without disrupting same-day delivery; CFO — one finance system, cost of the programme, synergies; head of sales and field sales — installers keep ordering seamlessly, tablet app works; Saarland managing director and staff — what happens to their systems and jobs; works council — staff changes; IT operations — two ERPs and server room; hospital group (customer) — information security evidence; installers — one platform, one price list.

**3. Phases B, C, D (6 points, 2 per phase: baseline/target 1, gap 1)**

- **B (business)**: baseline — two companies with separate order, warehouse and finance processes; target — one order-to-delivery process, marketplace capabilities (seller management, commission billing); gap — harmonise processes, new capabilities for the marketplace, new roles.
- **C (data and applications)**: baseline — two ERPs, Saarland web shop, direct database access from platform to Kurpfalz ERP, one-developer warehouse system; target — one ERP (e.g. the Saarland cloud ERP), one order platform for all installers, one leading system for customer, product and price data, interfaces via the integration platform; gap — ERP migration, retire the web shop, data migration and consolidation of product and customer data, new adapters.
- **D (technology)**: baseline — own server room, external hosting of the platform, no integration platform; target — SaaS ERP and platform in EU cloud/hosting, integration platform (iPaaS), server room retired; gap — introduce the integration platform, migrate hosting, decommission the server room, security measures for the customer evidence.
- Accept other consistent elements; a gap must follow from baseline and target.

**4. Two principles (3 points)**

- Two relevant principles named (1 point), e.g.: one leading system per business object; interfaces only via the integration platform; standard software/SaaS for non-differentiating capabilities; own development only for the marketplace platform; data stored in the EU.
- One in full (2 points): statement (0.5), rationale (0.75), implications (0.75), e.g. **Interfaces only via the integration platform** — statement: applications exchange data only via the integration platform; rationale: the ERP migration only changes one adapter, interfaces are monitored, same-day delivery risk is lower; implications: the platform must be introduced first, direct database access of the order platform is replaced, every project budgets for adapters, the platform needs an owner and SLA.

**5. Governance for the warehouse system (3 points, 1 per term used correctly)**

- **Compliance review**: the integration design for the warehouse system is checked against the principles; result: non-conformant (direct interface).
- **Architecture board**: (to be set up in the Preliminary phase, e.g. CIO, architects, heads of operations and sales) decides — not the project alone; it weighs the risk (one developer, same-day delivery) against the short remaining life.
- **Dispensation**: time-limited exception for 18 months with conditions — document the interface, no new interfaces to the system, monitoring, a retirement date in the roadmap (Phase F) — recorded in the repository; reviewed when the period ends. Also accept "rework" (adapter on the integration platform) if justified with the one-developer risk.
:::

## Optional Challenge: TOGAF for a Cooperative? {.optional}

*Weinbau Kaiserstuhl eG* (sessions 1 and 11–15), a winegrowers' cooperative with 300 members and 60 employees, has no IT staff of its own. It uses an ERP package, a web shop run by an agency, cellar sensors and plans a member portal; it is considering one regional IT service provider for everything (worksheet 15). A board member who attended a TOGAF training wants to "introduce TOGAF".

1. Give **two arguments** why introducing TOGAF as a whole would not suit the cooperative.
2. Propose a **tailored, lean** use of TOGAF ideas: which **three elements** would you keep, and what would they look like at the cooperative?
3. Who could act as the **architecture board** in an organisation without IT staff?

::: answer lines=12
:::

::: solution
1. E.g.: TOGAF is large and generic — the effort for deliverables, repository and governance would exceed the size of the landscape (four or five systems); there are no architects to run it; the main decisions are sourcing and contract decisions with few providers; certification and training costs are out of proportion.
2. E.g.: (a) a short list of **architecture principles** (data stays in the EU, standard software and SaaS before custom development, every system has an owner, data exports in usable formats); (b) a simple **Phase A** for each larger change, e.g. the member portal: goal, stakeholders (members, office, agency, provider), scope, approval by the board; (c) a light **compliance check** before signing contracts: does the offer meet the principles? Also accept a simple application catalogue as the "repository", or gap analysis for the member portal.
3. The managing board or one board member as IT owner, together with the office coordinator; if needed, an independent consultant for larger decisions. It meets as part of regular board meetings and records decisions in the minutes.

Marking hint: two points for part 1, three points for part 2, one point for part 3.
:::

## References {.references}

- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- The Open Group. (2022a). *The TOGAF Standard, 10th Edition: Architecture development method*. Van Haren Publishing.
- The Open Group. (2022b). *The TOGAF Standard, 10th Edition: Content, capability, and governance*. Van Haren Publishing.

Company names and figures in the tasks are fictitious training examples. TOGAF® is a registered trademark of The Open Group.
