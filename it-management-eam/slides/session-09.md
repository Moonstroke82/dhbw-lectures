---
course: IT Management and EAM
session: 9
title: IT Quality Management
subtitle: Quality concepts · ISO 9000 and ISO 9001 in IT · software quality with ISO/IEC 25010 · maturity models and CMMI
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# IT Quality Management {.title}

::: notes
Time plan for today (3 h): recap and preparation task 10 min · quality concepts and service quality 20 min · mini exercise "whose quality?" 10 min · ISO 9000 principles and ISO 9001 20 min · break 10 min · software quality with ISO/IEC 25010 15 min · mini exercise quality characteristics 10 min · maturity models and CMMI 15 min · how the instruments fit together 5 min · case exercise quality assessment 45 min · wrap-up and outlook to Part B 5 min · ~15 min buffer.
Copyright note for the lecturer: ISO 9000, ISO 9001, ISO/IEC 25010 and the CMMI model are copyrighted. The slides describe their structure and ideas in own words; the names of principles, clauses, characteristics and levels are used as labels only, no definitions are copied.
Status checked in October 2026: ISO 9001:2026 (6th edition) was published on 16 September 2026 and replaces ISO 9001:2015 incl. Amendment 1:2024 (climate action); the accreditation transition period had not yet been confirmed by the IAF (about three years is expected). ISO 9000:2026 (5th edition, May 2026) replaced ISO 9000:2015; the seven principles keep their names. ISO/IEC 25010:2023 (2nd edition, November 2023) is current; quality in use moved to ISO/IEC 25019:2023. CMMI V3.0 (ISACA/CMMI Institute, April 2023) is the current model version. Re-check all four before the first run in 2028.
This is the last session of Part A. Sessions 5 (ITIL continual improvement) and 6 (SLAs) are linked, not repeated.
:::

---

# Today's Agenda

1. Recap: software that annoys you
2. What is quality? Five approaches and service quality
3. Quality management with ISO 9000 and ISO 9001
4. Software and product quality with ISO/IEC 25010
5. Maturity models: CMMI
6. Case exercise: quality assessment of the on-board ticketing service

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Quality concepts, service quality (input) · 0:30 Mini exercise "whose quality?" (pairs) · 0:40 ISO 9000 principles, ISO 9001 (input) · 1:00 Break · 1:10 ISO/IEC 25010 (input) · 1:25 Mini exercise quality characteristics (pairs) · 1:35 Maturity models, CMMI, overview (input) · 1:55 Case exercise (groups + plenary) · 2:40 Wrap-up and outlook to Part B · ~15 min buffer.
If the session runs long: "Garvin's eight dimensions", "What is new in ISO 9001:2026" and "From product quality to quality in use" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: Software That Annoys You

You were asked to think of a piece of software at work that annoys you.

- **What exactly** is wrong: it crashes, it is slow, you cannot find the function, the data are wrong?
- **Who** would see a quality problem — you, the IT department, the vendor, the controller?
- **How would you measure** it, so that somebody has to act?

::: notes
Pairs for 3 min, then collect 6–8 complaints on the board in a loose cluster. Typical answers: ERP screens with too many fields, slow time recording tool, frequent crashes after updates, unclear error messages, VPN disconnects, data that must be entered twice. Keep the board: later today the complaints are sorted into the ISO/IEC 25010 characteristics, and question 2 leads straight to Garvin's approaches — the user, the developer and the controller look at the same software with different ideas of quality. Question 3 is the bridge to measurable quality requirements and to the SLA metrics of session 6.
:::

---

# What Is Quality? {.section}

Approaches, dimensions and service quality

---

# Five Approaches to Quality

| Approach | Quality means … | IT example |
|---|---|---|
| **Transcendent** | Innate excellence that you recognise when you see it, but cannot define exactly | "This app just feels right" |
| **Product-based** | More of a measurable attribute | More features, faster response time, more storage |
| **User-based** | Fitness for the needs of the user — in the eye of the beholder | Drivers can sell a ticket in under 10 seconds |
| **Manufacturing-based** | Conformance to requirements and specifications | Release passes all tests; no deviation from the specification |
| **Value-based** | Performance or conformance at an acceptable price | A 99.5 % service for the price of a 99.5 % service |

::: source
Own wording based on Garvin (1984).
:::

::: notes
Garvin (1984) collected these five definitions from philosophy, economics, marketing and operations management. His key argument: each department in a company tends to use a different approach — marketing the user-based view, engineering the product-based view, production the manufacturing-based view, controlling the value-based view — and quality problems often come from these different views clashing. Transfer to IT: users judge an application by fitness for their work, developers by conformance to the specification, the CFO by cost per user. A good quality manager can switch between the views. Exam point: be able to name the five approaches and assign a statement to one of them.
:::

---

# Garvin's Eight Dimensions of Quality {.optional}

| Dimension | Ticket device example |
|---|---|
| **Performance** | Time to sell a ticket |
| **Features** | Contactless card, app ticket check |
| **Reliability** | Failures per 1,000 operating hours |
| **Conformance** | Fares match the approved tariff |
| **Durability** | Years of use before replacement |
| **Serviceability** | Time and effort to swap or repair a device |
| **Aesthetics** | Look and feel of the screen |
| **Perceived quality** | Reputation of the manufacturer |

::: source
Own examples based on Garvin (1984).
:::

::: notes
Self-study. Garvin proposed the eight dimensions to make quality usable for strategy: a firm does not have to excel on all eight, but can choose the dimensions on which it competes. Several dimensions reappear in ISO/IEC 25010 (performance → performance efficiency, reliability, serviceability ≈ maintainability) — a good bridge to the software section.
:::

---

# Quality of IT Services

::: columns
**Five dimensions of service quality (SERVQUAL)**

- **Reliability:** the promised service is delivered dependably and accurately
- **Responsiveness:** willingness to help and to react promptly
- **Assurance:** competence and courtesy that create trust
- **Empathy:** individual attention to the customer
- **Tangibles:** facilities, equipment, appearance
|||
**Quality as a gap**

- Customers compare what they **expected** with what they **perceive**
- Perceived quality = perception − expectation
- An SLA can be met while the gap is negative — the watermelon effect from session 6
- So service quality needs **user surveys** as well as technical metrics
:::

::: source
Own wording based on Parasuraman et al. (1988).
:::

::: notes
SERVQUAL comes from services marketing (banks, retail, repair services), not from IT, but it is widely used for IT services and service desks. The original instrument asks customers 22 pairs of questions (expectation and perception) on the five dimensions. Only mention the instrument; students need the five dimensions and the gap idea. Link without repeating session 6: SLA targets measure reliability and responsiveness well; assurance and empathy (e.g. how the service desk treats users) need surveys. In ITIL terms, the warranty of session 5 covers mainly reliability and responsiveness.
:::

---

# Quality Management: The Vocabulary

::: callout
**Quality management** covers all coordinated activities to direct and control an organisation with regard to quality: setting a **quality policy** and **quality objectives**, and achieving them through quality **planning**, **assurance**, **control** and **improvement**.
:::

| Activity | Focus | IT example |
|---|---|---|
| Quality planning | Set objectives and the processes and resources to reach them | Define acceptance criteria for a release |
| Quality assurance | Build confidence that requirements will be met (prevention) | Code reviews, test strategy, process audits |
| Quality control | Check that requirements are met (detection) | Running test cases, checking fares before go-live |
| Quality improvement | Increase the ability to meet requirements | Root cause analysis, process changes |

::: source
Own wording based on ISO (2026a) and Tiemeyer (2023).
:::

::: notes
The structure follows the terms in ISO 9000; the wording is our own. Classic exam point: quality assurance (prevention, process-oriented) vs. quality control (detection, product-oriented) — testing is control, a test strategy and reviews are assurance. Tiemeyer (2023) describes quality management for IT systems and for requirements and projects as part of IT management; quality in IT projects is covered there too. Link: quality improvement and problem management (session 6) work with the same root cause techniques.
:::

---

# Mini Exercise: Whose Quality? {.exercise}

The **car-sharing app** of *Rhein-Neckar Mobil Group* has a new release. Which of Garvin's **approaches** does each person take — and which **SERVQUAL dimension** do the last two statements address?

1. Developer: "All 412 test cases passed, so the release has high quality."
2. Customer: "I just want to open the car in five seconds, even in an underground car park."
3. Product manager: "Our competitor's app has 30 features; ours needs at least as many."
4. Controller: "The new release cost €200,000 more than the old one, but bookings only rose by 1 %."
5. Customer review: "The app is somehow great — I can't say why."
6. Customer: "When the car would not open, the hotline answered at once and the agent knew exactly what to do."

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 manufacturing-based (conformance to specification); 2 user-based (fitness for the user's need and situation); 3 product-based (more of an attribute); 4 value-based (quality relative to cost); 5 transcendent; 6 user-based view of the service; SERVQUAL responsiveness (answered at once) and assurance (competence). Discussion: statements 1 and 2 can both be true at the same time — tests did not cover the underground car park (no mobile network). That is why quality needs more than one view.
:::

---

# Quality Management Systems {.section}

ISO 9000 and ISO 9001 in IT

---

# Seven Quality Management Principles

::: cards
### Customer focus
Meet and try to exceed customer needs.
### Leadership
Leaders set direction and conditions for quality.
### Engagement of people
Competent, empowered people at all levels.
### Process approach
Manage activities as interrelated processes in a system.
### Improvement
Ongoing improvement as a permanent objective.
### Evidence-based decision making
Decide on the basis of data and analysis.
### Relationship management
Manage relationships with suppliers and partners.
:::

::: source
Own wording based on ISO (2026a).
:::

::: notes
The seven principles are described in ISO 9000 (fundamentals and vocabulary); ISO 9001 is built on them. The 2026 edition of ISO 9000 keeps the seven principle names; the wording of the explanations was revised. Ask students to give one IT example per principle: customer focus → service level reviews with business units; process approach → incident, change and release as linked processes; evidence-based → decisions based on incident trends; relationship management → suppliers and underpinning contracts (session 6). Students should know the names and be able to explain them — not the full text.
:::

---

# ISO 9001: Structure and PDCA

![Clauses of ISO 9001 in the plan-do-check-act cycle: context of the organisation (4) as input, leadership (5) in the centre, planning (6) as plan, support (7) and operation (8) as do, performance evaluation (9) as check, improvement (10) as act; results are conforming services and products and satisfied customers](img/pdca-iso9001.png){width=78%}

ISO 9001 sets **requirements** for a quality management system (QMS); it is **certifiable**. It uses the same clause structure 4–10 as ISO/IEC 27001 and ISO 22301 (session 8) and asks for **risk-based thinking**.

::: source
Own illustration based on ISO (2015, 2026b).
:::

::: notes
ISO 9001 does not prescribe how good a product or service must be — it requires a system that reliably delivers what customers and regulations require and that improves. The PDCA cycle (plan–do–check–act, popularised by Deming) runs at system level and within each process. Link to session 5: ITIL's continual improvement model is a more detailed improvement cycle of the same kind ("Where are we now?" = check; "Take action" = do) — do not repeat it, just point out the family resemblance. Same harmonised structure as the ISMS and BCMS of session 8: many companies run one integrated management system with shared document control, internal audits and management review.
:::

---

# ISO 9001 in an IT Organisation

| Clause | What it means for an IT department or IT service provider |
|---|---|
| 4 Context | Scope, e.g. "development and operation of IT services for the group"; interested parties |
| 5 Leadership | Quality policy, roles, customer focus of IT management |
| 6 Planning | Risks and opportunities, measurable quality objectives (e.g. first-time-right changes) |
| 7 Support | Competence, monitoring tools, knowledge management, documented information |
| 8 Operation | Requirements, design and development of software, control of external suppliers, release and service delivery, nonconforming outputs |
| 9 Performance evaluation | Customer satisfaction, internal audits, management review |
| 10 Improvement | Nonconformity and **corrective action**, continual improvement |

::: source
Own summary based on ISO (2015, 2026b).
:::

::: notes
Point out: a requirement that cannot apply (e.g. design and development for a pure operations provider) can be declared not applicable with a justification, as long as this does not affect conformity of the services. Corrective action is the key concept: find the cause of a nonconformity and stop it from happening again — the same logic as problem management (session 6). Typical evidence an auditor asks for in IT: change records, test reports, incident trends, supplier evaluations, results of user surveys, minutes of the management review. ISO/IEC 20000-1 (session 5, optional slide) is the service management counterpart; an IT provider can hold both certificates.
:::

---

# What Is New in ISO 9001:2026 {.optional}

- **ISO 9001:2015** (5th edition) with **Amendment 1:2024**: organisations must consider whether **climate change** is a relevant issue
- **ISO 9001:2026** (6th edition, September 2026) replaces both
  - Integrates the climate amendment
  - More weight on **leadership, quality culture and ethical behaviour**
  - Clearer handling of **risks and opportunities**
  - Latest harmonised structure for management system standards
- Certified organisations get a **transition period** to move to the new edition

::: source
ISO (2024, 2026b, 2026c).
:::

::: notes
Self-study; status as of October 2026. The ISO press release of 16 September 2026 lists the focus on leadership, quality culture and ethics, risks and opportunities, and a new explanation of the intent of the requirements. The length of the transition period is set by the International Accreditation Forum (IAF); about three years is expected, as for earlier revisions — check before 2028. The 2024 climate amendment was made to all management system standards at the same time, also ISO/IEC 27001 and ISO 22301 (session 8).
:::

---

# ISO 9001 in IT: Benefits and Criticism

::: columns
**Benefits**

- Required or expected by many customers and in public tenders
- Clear processes, roles and documented responsibilities
- Systematic handling of errors via corrective action
- Common structure with ISO/IEC 27001 and ISO/IEC 20000-1
|||
**Criticism**

- Risk of "paper quality": documents for the auditor instead of better services
- A certificate shows a working system, **not** a good product
- Can feel bureaucratic for agile teams — unless the QMS uses agile practices as its processes
:::

::: source
Own assessment based on ISO (2026b).
:::

::: notes
Discussion question: "Our supplier is ISO 9001 certified, so its software is good" — true or false? False: the certificate says the supplier has a working QMS and handles nonconformities; it does not judge the product's quality characteristics. That is the bridge to product quality models (next section). Agile and ISO 9001 are compatible: sprint reviews and retrospectives are evidence for clauses 9 and 10, definition of done for clause 8.
:::

---

# Software and Product Quality {.section}

ISO/IEC 25010

---

# ISO/IEC 25010:2023 — Product Quality Model

| Characteristic | Sub-characteristics (selection) |
|---|---|
| **Functional suitability** | Completeness, correctness, appropriateness |
| **Performance efficiency** | Time behaviour, resource utilisation, capacity |
| **Compatibility** | Co-existence, interoperability |
| **Interaction capability** | Learnability, operability, user error protection, inclusivity, user assistance |
| **Reliability** | Faultlessness, availability, fault tolerance, recoverability |
| **Security** | Confidentiality, integrity, non-repudiation, accountability, authenticity, resistance |
| **Maintainability** | Modularity, reusability, analysability, modifiability, testability |
| **Flexibility** | Adaptability, scalability, installability, replaceability |
| **Safety** | Operational constraint, risk identification, fail safe, hazard warning, safe integration |

::: source
Own summary based on ISO/IEC (2023a).
:::

::: notes
Nine characteristics with sub-characteristics; the model is used to specify quality requirements, to design tests and to evaluate products — from software to whole ICT systems. Changes from the 2011 edition (exam-relevant in short): usability became **interaction capability**, portability became **flexibility**, **safety** was added as a ninth characteristic; new sub-characteristics include inclusivity, self-descriptiveness, resistance and scalability; maturity was replaced by faultlessness and user interface aesthetics by user engagement. The security sub-characteristics are the protection goals of session 8 again. Selection on the slide: interaction capability also has appropriateness recognisability, user engagement and self-descriptiveness.
:::

---

# From Product Quality to Quality in Use {.optional}

::: columns
**Product quality (ISO/IEC 25010)**

- Properties of the product itself
- Can be tested before go-live: code, tests, load tests, reviews
- Seen by developers and testers
|||
**Quality in use (ISO/IEC 25019)**

- Effect of the product on its users and stakeholders in a real **context of use**
- Three characteristics: **beneficialness**, **freedom from risk**, **acceptability**
- Seen by users, customers, society
:::

::: source
Own summary based on ISO/IEC (2023a, 2023b).
:::

::: notes
Self-study. Until 2023, ISO/IEC 25010 contained both models; the 2023 revision moved quality in use into the new ISO/IEC 25019. Link to Garvin: product quality ≈ product-based and manufacturing-based view, quality in use ≈ user-based view. Good product quality is a precondition for quality in use, but not a guarantee — the ticket device can pass all tests and still be hard to use in a dark bus at 5:00.
:::

---

# Making Quality Requirements Measurable

| Vague wish | Characteristic | Measurable requirement |
|---|---|---|
| "The device must be fast" | Performance efficiency (time behaviour) | 95 % of card payments complete within 3 seconds |
| "Easy to use for new drivers" | Interaction capability (learnability) | A new driver sells all standard fares after a 30-minute briefing |
| "It must not break down" | Reliability (fault tolerance) | Without mobile network, cash sales continue and data are stored for 48 hours |
| "Fare changes must be easy" | Maintainability (modifiability) | A new fare can be configured and tested within 2 days without a software release |

::: callout
Quality requirements become **testable** acceptance criteria — and some of them become **service level targets** in the SLA (session 6).
:::

::: source
Own examples based on ISO/IEC (2023a).
:::

::: notes
Pattern: characteristic → measure → target value → measuring method. ISO/IEC 25023 (in the same SQuaRE series) proposes measures for each characteristic — only mention that it exists. Non-functional requirements are a typical weak point in IT projects: they are forgotten in requirements, so tests and SLAs cannot check them. Link without repeating session 6: availability and resolution times are SLA material; learnability and modifiability are usually acceptance criteria in the project.
:::

---

# Mini Exercise: Name the Characteristic {.exercise}

Assign each complaint about the *Rhein-Neckar Mobil* **car-sharing app** to an ISO/IEC 25010 **characteristic** (and sub-characteristic, if you can).

1. "The app does not work with the car's new keyless system of manufacturer X."
2. "Since the update, the app drains my battery in two hours."
3. "Blind users cannot book a car, the screen reader reads nothing."
4. "Every small change takes the vendor three months."
5. "The app shows 'Car unlocked' while the car is still locked."
6. "On New Year's Eve, with 5,000 bookings at once, the system collapsed."
7. "The app lets me start driving while the car's warning light says the brakes are faulty."

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 compatibility (interoperability); 2 performance efficiency (resource utilisation); 3 interaction capability (inclusivity; in the 2011 model accessibility); 4 maintainability (modifiability, possibly analysability or modularity); 5 functional suitability (functional correctness) — some will say reliability; correctness of a function is the better fit; 6 flexibility (scalability) or performance efficiency (capacity) — both acceptable with reasoning; 7 safety (hazard warning, operational constraint). Then sort the complaints from the recap board in the same way.
:::

---

# Maturity Models {.section}

How capable are our processes?

---

# The Idea of Maturity Models

- A maturity model describes **typical stages** an organisation passes through on the way to mature, capable processes
- It serves to **assess** the as-is state, **compare** with others and plan the **next improvement steps**
- Two ways of looking at it:
  - **Maturity levels:** the whole organisation or unit is rated on one scale (staged)
  - **Capability levels:** each process or practice area is rated separately (continuous)
- Examples: alignment maturity (session 2), **CMMI** for development and services

::: source
Own summary based on CMMI Institute (n.d.) and Lear (2023).
:::

::: notes
Do not repeat Luftman's model from session 2 — just point out that it follows the same logic of five levels. COBIT 2019 (session 3) also rates its processes on a capability scale derived from CMMI; mention only if students ask. Criticism to mention briefly: maturity is not a goal in itself; a level is a snapshot; organisations may optimise for the appraisal instead of performance.
:::

---

# CMMI Maturity Levels

::: layers
- 5 · Optimising: Focus on continuous improvement; stable yet flexible, adapts to change
- 4 · Quantitatively managed: Data-driven; processes are measured and controlled with quantitative objectives
- 3 · Defined: Organisation-wide standard processes; proactive rather than reactive
- 2 · Managed: Projects and work are planned, performed, measured and controlled
- 1 · Initial: Work gets done, but unpredictably and often late or over budget
- 0 · Incomplete: Ad hoc; work may or may not be completed
:::

::: source
Own wording based on CMMI Institute (n.d.).
:::

::: notes
CMMI (Capability Maturity Model Integration) goes back to the Capability Maturity Model for software of the Software Engineering Institute at Carnegie Mellon University (1991); since 2016 it belongs to ISACA through the CMMI Institute. The CMMI Institute today lists a level 0 (incomplete); older literature shows five levels 1–5 — accept both. The typical jump is from 1 to 2 (project discipline) and from 2 to 3 (organisation-wide standards); levels 2 and 3 are the ones most companies aim for. Ask: on which level is the software development of your training company?
:::

---

# CMMI V3.0 in a Nutshell

::: columns
**The model**

- Current version **V3.0** (April 2023), published by **ISACA** / CMMI Institute
- Best practices in **practice areas**, grouped into capability areas
- **One integrated model** with domains for development, services, suppliers — and since V3.0 also data, people, safety, security and virtual work
|||
**Appraisals**

- Lead appraisers rate an organisation against selected domains
- Result: a **maturity level** (or capability levels per practice area)
- Used by customers to select suppliers, especially in software development and the public sector
:::

::: source
Own summary based on Lear (2023) and CMMI Institute (n.d.).
:::

::: notes
V2.0 (2018) merged the earlier separate models for development, services and acquisition into one model; V3.0 added new domains (e.g. data management, people management, safety, security, virtual work). Do not go into practice area names; students should know: who publishes CMMI, the current version, the six levels and the difference between maturity and capability levels. CMMI V2.0 and V3.0 also stress performance: practices should improve measurable business performance, not only produce documents. ISO/IEC 33000 (formerly SPICE) is the international standard family for process assessment — mention only if students know it from automotive (Automotive SPICE).
:::

---

# How the Instruments Fit Together

| Instrument | Question it answers | Link |
|---|---|---|
| Garvin, SERVQUAL | What does quality mean — for whom? | Users, customers, controllers |
| ISO 9001 | Do we have a working system that delivers quality and improves? | Certifiable QMS; same structure as ISO/IEC 27001 |
| ISO/IEC 25010 | Which properties must our software or system have? | Requirements, tests, acceptance |
| CMMI | How capable are our development and service processes? | Supplier selection, improvement roadmap |
| SLA (session 6) | Which service levels have we agreed? | Measured and reported monthly |
| ITIL continual improvement (session 5) | How do we improve step by step? | Improvement cycle like PDCA |

::: source
Own overview.
:::

::: notes
This is the integrating slide for Part A: quality management connects service management (5–6), risk and security (7–8) and controlling (4: quality KPIs in the IT balanced scorecard). Exam type: "Which instrument would you use for problem X, and why?" — the answer should name the question the instrument answers, not only its name.
:::

---

# Case Exercise: Quality of the On-Board Ticketing Service {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–8), **on-board ticketing service**. The monthly SLA report is green: back-end availability **99.8 %** (target 99.5 %), **98.6 %** of devices working at shift start (target 98 %). Yet:

- Driver survey: satisfaction **2.1 of 5**; "a card payment takes up to 8 seconds, the queue at the front door grows"
- The screen can hardly be read in direct sunlight; new drivers need two shifts to learn the menus
- After the **March fare change**, 30 buses charged the old fares for two days; nobody noticed until passengers complained
- Device software: **3 of 12 releases** last year were rolled back; tests are done manually by one developer; there is no written release process
- The regional transport association announces that from 2028 it expects operators to prove a **quality management system**

::: notes
Read the case together (2 min). Hints if asked: the device software is developed by a small in-house team of four at Group IT; the hardware comes from the manufacturer (session 6); passengers' complaints about ticketing rose from 40 to 140 per month. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. Which of Garvin's **approaches** do the SLA report, the drivers and the transport association take? Why can the service be "green" and still poor?
2. Classify the findings with **ISO/IEC 25010** characteristics (device software) and **SERVQUAL** dimensions (service).
3. Turn two findings into **measurable quality requirements**.
4. Estimate the **CMMI maturity level** of the device software development and propose two steps to the next level.
5. How would an **ISO 9001**-based QMS have handled the fare error? Name the clauses and the steps.
6. Propose a **quality dashboard** with four indicators that goes beyond the SLA.

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 SLA report: manufacturing-based (conformance to agreed targets); drivers: user-based (fitness for their work at the front door); transport association: manufacturing-based (correct fares, proof of a system) and indirectly value-based. Green but poor: the SLA measures availability, not speed, usability or correctness of fares → watermelon effect (session 6).
2 25010: payment time → performance efficiency (time behaviour); sunlight → interaction capability (operability; accept user engagement); learning time → interaction capability (learnability); wrong fares → functional suitability (correctness); rollbacks → reliability (faultlessness) and maintainability (testability). SERVQUAL: reliability (wrong fares, rollbacks), responsiveness (slow payment, nobody noticed), tangibles (screen), assurance (drivers lose trust).
3 E.g. 95 % of card payments within 3 seconds, measured on the device; new drivers sell all standard fares after a 30-minute briefing; after every fare change, 100 % of devices confirm the new fare version within 4 hours, checked automatically.
4 Level 1 (initial): work gets done, but unpredictably; no written release process, manual tests by one person, frequent rollbacks. To level 2: plan and track releases, define a release and change process with approvals (session 6 change enablement), requirements and acceptance criteria per release, version control and configuration management, test plans and a second reviewer; measure rollback rate. Level 3 would need organisation-wide standards.
5 Clause 8: nonconforming output — stop and correct (push the correct fares, decide on refunds); clause 10: nonconformity and corrective action — root cause analysis (why did 30 devices not receive the update? why no check?), action (automatic confirmation of fare versions, test on a sample of buses), check effectiveness; clause 9: monitor complaints, internal audit of the fare change process, management review; clause 6: risk of wrong fares as a planned risk. Link to problem management (session 6).
6 E.g. payment time (95th percentile), driver satisfaction (quarterly survey), passenger complaints about ticketing per 100,000 trips, rollback rate of releases, share of devices with the correct fare version, plus the SLA availability metrics.
:::

---

# Key Takeaways

- **Quality** depends on the view: transcendent, product-, user-, manufacturing- or value-based (Garvin); service quality is the gap between expectation and perception
- **ISO 9000** describes seven quality management principles; **ISO 9001** (now 2026 edition) sets certifiable requirements for a QMS in the PDCA structure 4–10
- **ISO/IEC 25010:2023** describes product quality in nine characteristics — incl. interaction capability, flexibility and safety
- **CMMI V3.0** rates process maturity on levels 0–5; most organisations aim for levels 2–3
- Quality needs measurable requirements and indicators beyond SLA compliance

---

# Next Session: Enterprise Architecture Foundations

::: callout
**End of Part A — IT management.** From session 10 we move to **Part B — enterprise architecture management**: from managing IT functions to designing how business and IT fit together as a whole.
:::

- What enterprise architecture is and why it matters
- The main domains: business, data, application and technology architecture
- Fields of action and stakeholders of EAM

**Preparation:** list the five most important applications of your training company. Which business processes does each one support — and who would know the complete list?

::: notes
Briefly look back at Part A (sessions 1–9) on the course overview from session 1: strategy and alignment, governance, controlling, service management, risk, security and quality. In Part B, these instruments come back: EA information supports the BIA (session 8), application portfolio management builds on IT controlling (session 4), and sourcing links to supplier management and underpinning contracts (session 6). The preparation task leads into EA domains and EA data collection (sessions 10–11).
:::

---

# References {.references}

- CMMI Institute. (n.d.). *Maturity levels*. ISACA. Retrieved October 21, 2026, from https://cmmiinstitute.com/learning/appraisals/levels
- Garvin, D. A. (1984). What does "product quality" really mean? *Sloan Management Review, 26*(1), 25–43.
- ISO. (2015). *Quality management systems — Requirements* (ISO Standard No. 9001:2015). International Organization for Standardization.
- ISO. (2024). *Quality management systems — Requirements — Amendment 1: Climate action changes* (ISO 9001:2015/Amd 1:2024). International Organization for Standardization.
- ISO. (2026a). *Quality management — Fundamentals and vocabulary* (ISO Standard No. 9000:2026). International Organization for Standardization.
- ISO. (2026b). *Quality management systems — Requirements* (ISO Standard No. 9001:2026). International Organization for Standardization.
- ISO. (2026c, September 16). *ISO launches update to world's most widely used quality management standard for a new era of business*. https://www.iso.org/news/2026/09/ISO9001-2026
- ISO/IEC. (2023a). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model* (ISO/IEC Standard No. 25010:2023). International Organization for Standardization.
- ISO/IEC. (2023b). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Quality-in-use model* (ISO/IEC Standard No. 25019:2023). International Organization for Standardization.
- Lear, R. (2023, April 10). *CMMI updates take performance improvements to the next level*. ISACA Now Blog. https://www.isaca.org/resources/news-and-trends/isaca-now-blog/2023/cmmi-updates-take-performance-improvements-to-the-next-level
- Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. *Journal of Retailing, 64*(1), 12–40.
- Tiemeyer, E. (Ed.). (2023). *Handbuch IT-Management: Konzepte, Methoden, Lösungen und Arbeitshilfen für die Praxis* (8th ed.). Hanser.

CMMI® is a registered trademark of ISACA. Diagrams in this deck are own illustrations. Standards are described in own words.
