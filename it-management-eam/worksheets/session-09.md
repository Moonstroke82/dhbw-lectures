---
course: IT Management and EAM
session: 9
title: IT Quality Management
subtitle: Practice tasks on approaches to quality, service quality, ISO 9000 and ISO 9001, ISO/IEC 25010 and CMMI
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 9: Garvin's (1984) five approaches to quality, the service quality dimensions of SERVQUAL (Parasuraman et al., 1988), the seven quality management principles of ISO 9000 (ISO, 2026a) and the quality management system requirements of ISO 9001 (ISO, 2026b) with their clauses 4–10, the product quality model of ISO/IEC 25010:2023 (ISO/IEC, 2023), and the CMMI maturity levels (CMMI Institute, n.d.). Terms follow the session slides; the standards are described in own words. The last core task is in the style of an exam question.

## Five Views on One Laptop

A university buys 800 new laptops for its staff. Different people comment on the purchase. For each statement, name the **approach to quality** (Garvin, 1984) it reflects — transcendent, product-based, user-based, manufacturing-based or value-based — and justify it in one line.

- a) Purchasing: "Model B is €150 cheaper and almost as good. That is the better quality."
- b) Lecturer: "I need a laptop that is light enough to carry between buildings and lasts a whole day of teaching."
- c) IT department: "The vendor's delivery matched our specification exactly: same image, same BIOS settings, no deviations."
- d) Student assistant: "Model A just feels like a premium device."
- e) Tech blog: "Model A has 32 GB of RAM and a faster processor, so it is the higher-quality laptop."
- f) IT department, six months later: "Only 0.5 % of the devices came back with hardware defects — the agreed maximum was 2 %."

::: answer lines=7
:::

::: hint
Ask what the person compares quality *with*: an ideal they cannot define, a measurable attribute, their own needs, a specification, or the price.
:::

::: solution
- a) **Value-based** — quality is judged relative to the price.
- b) **User-based** — quality is fitness for this user's needs (weight, battery life in teaching).
- c) **Manufacturing-based** — conformance to the specification.
- d) **Transcendent** — excellence that is recognised but not defined.
- e) **Product-based** — more of a measurable attribute means higher quality.
- f) **Manufacturing-based** — conformance to an agreed requirement (defect rate within the limit); accept product-based if the student argues with reliability as a measurable attribute.

Marking hint: one point per item for the approach with a reason. Point out that the same purchase is judged "good" or "bad" depending on the view — the core idea of Garvin's article.
:::

## Service Quality at the Service Desk

The IT service desk of an insurance company met all SLA targets last quarter: 96 % of calls answered within 60 seconds, 82 % of incidents resolved at first contact. Still, a user survey shows low satisfaction. Comments include:

1. "They always say the ticket is solved, but the problem comes back a week later."
2. "Nobody calls back when they promised to."
3. "The agent clearly did not understand our claims software and just read from a script."
4. "When I said I had a customer appointment in ten minutes, nobody cared."
5. "The self-service portal looks like it is from 2005 and the remote support tool keeps crashing."

**Tasks:**

1. Assign each comment to the **SERVQUAL dimension** it mainly addresses: reliability, responsiveness, assurance, empathy, tangibles.
2. Explain with the **gap** idea why users can be unhappy although all SLA targets are met.
3. Propose **two indicators** that would make the problem visible in the monthly report.

::: answer lines=10
:::

::: solution
1. 1 **Reliability** — the promised result (a solved problem) is not delivered dependably; 2 **reliability** (a promise is broken) or **responsiveness** — accept either with reasoning; 3 **assurance** — lack of competence that creates trust; 4 **empathy** — no individual attention to the user's situation; 5 **tangibles** — tools and equipment.
2. Users compare what they **expect** with what they **perceive**. The SLA measures technical outputs (speed of answering, tickets closed), not whether the problem is really solved or how users are treated. Perception falls short of expectation → negative gap, although the SLA report is green (watermelon effect, session 6).
3. E.g. reopen rate of tickets within 14 days; share of promised call-backs made on time; user satisfaction score per closed ticket (short survey); repeat contacts for the same problem; results of a regular survey per SERVQUAL dimension.
:::

## Principles and Clauses in a Hosting Company

*Neckar Cloud GmbH* (120 employees) hosts business applications for medium-sized companies and wants to be certified to ISO 9001.

1. Assign each practice to the **quality management principle** of ISO 9000 it mainly reflects (customer focus, leadership, engagement of people, process approach, improvement, evidence-based decision making, relationship management):
   - a) The decision to buy new storage is based on six months of capacity and incident data.
   - b) Twice a year, the account managers hold service reviews with each customer.
   - c) The data centre provider and the network carrier are evaluated yearly and invited to a joint planning workshop.
   - d) Monitoring, incident, change and release are documented as linked processes with clear hand-overs.
   - e) Teams may stop a release if they see a quality risk, without asking the managing director.
2. During the first internal audit, the auditor records these findings. For each one, name the **ISO 9001 clause** (4–10) it concerns and say what the company must do.
   - f) Customer complaints are collected in an e-mail folder, but nobody analyses them.
   - g) The same backup error has occurred four times; each time it was fixed, but the cause was never investigated.
   - h) Nobody can say which services and locations the QMS covers.
   - i) Two new administrators started work without any training on the change process.

::: answer lines=12
:::

::: solution
1. a) **Evidence-based decision making** · b) **customer focus** (accept relationship management with reasoning) · c) **relationship management** · d) **process approach** · e) **engagement of people** (empowerment); accept leadership if the student argues that management created the conditions.
2. f) **Clause 9** Performance evaluation — customer satisfaction must be monitored and analysed; complaints are an important source; results go into the management review. g) **Clause 10** Improvement — nonconformity and **corrective action**: analyse the root cause, take action so that the error does not recur, and check the effectiveness (in IT, problem management does this — session 6). h) **Clause 4** Context — the **scope** of the QMS must be determined and documented. i) **Clause 7** Support — competence and awareness: train people, keep evidence of competence.

Marking hint: one point for each correct principle in part 1; in part 2, half a point for the clause and half for a sensible action.
:::

## From Wishes to Quality Requirements

A city wants a new **online appointment service** for its citizens' office (passports, registrations). The project team has collected these wishes:

- a) "Citizens must find a free appointment quickly."
- b) "Older people and people with disabilities must be able to use it."
- c) "Citizens' data must be safe."
- d) "It must not crash when the booking window opens on Monday at 8:00."
- e) "It must work with the city's existing scheduling system."
- f) "Later we want to add other offices without starting from scratch."

**Tasks:**

1. Assign each wish to an **ISO/IEC 25010:2023 characteristic** and a sub-characteristic.
2. Rewrite **three** wishes as **measurable quality requirements** (with a target value and how it is checked).
3. Which two characteristics were **renamed** in the 2023 edition, and which one was **added**? Would the added one matter for this system?

::: answer lines=12
:::

::: hint
A measurable requirement names a measure, a target value and the condition or method of measurement, e.g. "95 % of … within … seconds, measured by …".
:::

::: solution
1. a) **Performance efficiency** (time behaviour) or **interaction capability** (operability, appropriateness recognisability) — accept both with reasoning; b) **interaction capability** (inclusivity, user assistance); c) **security** (confidentiality, integrity); d) **reliability** (availability, fault tolerance) or **flexibility** (scalability) / **performance efficiency** (capacity); e) **compatibility** (interoperability); f) **maintainability** (modularity, modifiability) or **flexibility** (adaptability).
2. Examples: a) "A citizen finds and books a free appointment in at most 3 steps; in a usability test, 90 % of test persons do this within 2 minutes." b) "The service meets the accessibility requirements applicable to public websites (e.g. WCAG level AA), checked by an accessibility test before go-live." d) "With 3,000 simultaneous users, 95 % of pages load within 2 seconds and no bookings are lost; checked by a load test." c) "Personal data are transmitted encrypted; access to booking data is logged; a penetration test before go-live finds no critical vulnerabilities." Points require a measure, a target value and a check.
3. **Usability → interaction capability**, **portability → flexibility**; **safety** was added. Safety concerns harm to people or the environment; for an appointment service it is hardly relevant (low hazard), unlike, e.g., the car-sharing app that lets cars drive. Accept "little relevance" with reasoning.
:::

## Maturity of a Software House

*Odenwald Software GmbH* (45 developers) builds apps for regional banks. A bank wants to know how mature its development processes are. Interviews show:

- Each project manager plans in their own way; some use Jira, others Excel.
- Requirements are agreed with the customer in writing for each project and changes are tracked.
- Project status and effort are reported monthly and compared with the plan.
- There is no company-wide standard process; good practices from one project are not passed on.
- Nobody collects data on defect rates or delivery accuracy across projects.

**Tasks:**

1. Estimate the **CMMI maturity level** and justify it with evidence from the interviews.
2. Name **three** steps that would bring the company to the **next level**.
3. Explain the difference between a **maturity level** and a **capability level**.
4. The bank asks: "If you reach level 3, will your apps have fewer bugs?" Give a balanced answer.

::: answer lines=12
:::

::: solution
1. **Level 2 (managed):** projects are planned, requirements are agreed and changes tracked, status is measured and compared with the plan — but only at project level, each in its own way. Level 3 is not reached because there are no organisation-wide standard processes; level 4 would need quantitative data across projects. Accept level 1–2 if the student argues that planning differs widely between projects.
2. Towards **level 3 (defined):** define an organisation-wide standard development process with tailoring rules; common tools and templates (one planning tool); a process group or quality manager who maintains the process and collects lessons learned; training for project managers in the standard process; organisation-wide reviews and peer reviews.
3. A **maturity level** rates the organisation (or unit) as a whole on one scale and requires a defined set of practice areas at once (staged view). A **capability level** rates a single process or practice area (continuous view), so a company can be strong in one area and weak in another.
4. Not automatically: CMMI rates how capable and repeatable the processes are, not the product itself. Defined processes, reviews and lessons learned usually reduce defects and make delivery more predictable, but product quality must still be specified and tested (e.g. with ISO/IEC 25010 characteristics and acceptance criteria). A level can also be reached "on paper" without real improvement.
:::

## Exam-Style Task: Quality Management at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–8), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers. Since its launch, the platform has been extended every two weeks by an in-house team of six developers. The company is ISO 9001 certified for logistics and sales, but **IT is not part of the scope**. Last month's findings:

- The platform met its SLA availability target (99.5 %) every month this year.
- An installer survey gives the platform 2.8 of 5 points. Comments: "Search does not find articles by manufacturer number", "On the tablet on the building site the order button is hidden", "Since the last update, the shopping cart is sometimes empty after login."
- A release in May showed net prices instead of gross prices to private customers for one day; the error was fixed, nobody analysed why it happened.
- Each developer tests their own changes; there is no common definition of done; some features are delivered without any written requirements.
- A large hospital group (session 7) now asks all suppliers for evidence of a quality management system that **covers IT**.

**Tasks:**

1. Explain **two** of Garvin's approaches to quality and show how they explain why the platform can be "green" in the SLA report and still be rated 2.8 by installers. (4 points)
2. Assign the three installer comments and the price error to **ISO/IEC 25010** characteristics. (4 points)
3. Formulate **two** measurable quality requirements for the platform. (2 points)
4. Estimate the **CMMI maturity level** of the platform development and propose two steps to the next level. (3 points)
5. The board considers extending the **ISO 9001** scope to IT. Explain what this would require, using **three** clauses of ISO 9001, and how the price error would have to be handled. (5 points)
6. Name **two quality management principles** of ISO 9000 that the IT department violates at the moment, with evidence. (2 points)

::: answer lines=28
:::

::: solution
Marking guide (20 points):

**1. Approaches to quality (4 points)**

- Two approaches explained correctly (1 point each), e.g. **manufacturing-based**: quality = conformance to requirements or specifications; **user-based**: quality = fitness for the needs of the user; also accept product-based or value-based if explained.
- Application (2 points): the SLA report takes a manufacturing-based view — it checks conformance to an agreed target (availability 99.5 %), which is met. The installers take a user-based view — they judge whether they can find articles and order quickly on the building site; availability says nothing about search, usability or lost carts. Both views are legitimate; the SLA covers only part of quality (watermelon effect, session 6).

**2. ISO/IEC 25010 (4 points, 1 per item)**

- Search does not find articles by manufacturer number → **functional suitability** (functional completeness or appropriateness).
- Order button hidden on the tablet → **interaction capability** (operability, appropriateness recognisability); accept flexibility (adaptability to another device) with reasoning.
- Cart empty after login since the update → **reliability** (faultlessness) or **functional suitability** (correctness); accept either with reasoning.
- Net instead of gross prices → **functional suitability** (functional correctness).

**3. Measurable quality requirements (2 points, 1 each: measure + target + check)**

- E.g. "A search by manufacturer number returns the article as the first hit in 99 % of test cases (automated test with 500 numbers)." · "All order functions can be used on screens from 8 inches without scrolling sideways; checked in a usability test on three tablet models." · "After login, the cart content is kept in 100 % of sessions; checked by automated regression tests in every release." · "Prices for private customers are shown including VAT; automated test before every release."

**4. CMMI (3 points)**

- Estimate (1 point): **level 1 (initial)** — work gets done, but unpredictably; no common definition of done, own tests only, features without written requirements. Level 2 is not reached because requirements and work are not managed consistently even at project level.
- Two steps to level 2 (2 points, 1 each): written requirements and acceptance criteria for each feature, with change tracking; release planning and tracking against the plan; a common definition of done incl. peer review and independent or automated testing; configuration and version management; measuring defects and rollbacks per release.

**5. ISO 9001 for IT (5 points)**

- Three clauses with meaning for IT (3 points, 1 each), e.g.: **clause 4** — extend the scope to development and operation of the platform; **clause 6** — risks (e.g. wrong prices) and measurable quality objectives for IT; **clause 7** — competence, documented information (definition of done, test procedures); **clause 8** — requirements, design and development, control of external providers (hosting), release; **clause 9** — customer satisfaction (installer survey), internal audit of IT, management review; **clause 10** — nonconformity and corrective action.
- Price error (2 points): it is a **nonconforming output** — it was corrected (clause 8), but ISO 9001 also requires **corrective action** (clause 10): analyse the root cause (why did the release pass without a price test?), take action against recurrence (automated price tests, review rule), check effectiveness, record it; customers who were affected may need information or refunds. "Fixed and forgotten" does not meet the standard.

**6. Principles (2 points, 1 each: principle + evidence)**

- **Customer focus** — installer needs (search by manufacturer number, building-site tablets) are not reflected in requirements; satisfaction 2.8.
- **Evidence-based decision making** — survey results and error causes are not analysed.
- **Improvement** — the price error was fixed but not analysed; no lessons learned.
- **Process approach** — no common development and test process; each developer works their own way.
- Accept leadership (IT excluded from the QMS by management) with reasoning.
:::

## Optional Challenge: One Management System Instead of Four {.optional}

A medium-sized IT service provider holds certificates for **ISO 9001**, **ISO/IEC 27001** (session 8) and **ISO/IEC 20000-1** (session 5), and prepares for **ISO 22301** (session 8). Each certificate has its own manager, its own document set and its own internal audit.

1. Which common structure of these standards makes an **integrated management system** possible? Name four elements that could be shared.
2. Name two **risks** of integration.
3. The CEO asks whether a CMMI appraisal could replace the ISO 9001 certificate. Answer in three sentences.

::: answer lines=10
:::

::: solution
1. All four follow the **harmonised structure** of ISO management system standards with clauses 4–10 (context, leadership, planning, support, operation, performance evaluation, improvement). Shareable elements, e.g.: one context analysis and register of interested parties; common document control and documented information; one risk management process (ISO 31000 as a basis, session 7); combined internal audits; one management review; one process for nonconformities and corrective actions; common competence and training management.
2. Risks: specific requirements get lost in a general system (e.g. the statement of applicability of ISO/IEC 27001, the BIA of ISO 22301); one combined audit becomes too large or too shallow; responsibilities become unclear when one person owns everything; a problem in one area can endanger all certificates at the same time.
3. No: CMMI and ISO 9001 answer different questions. ISO 9001 is an international, certifiable standard for a whole quality management system that customers and tenders often require; CMMI is a model for rating the maturity of development and service processes by an appraisal, not a certification against an ISO standard. Both can complement each other — CMMI practices can help to meet ISO 9001 requirements for development, and the ISO 9001 system can use CMMI as an improvement roadmap.
:::

## References {.references}

- CMMI Institute. (n.d.). *Maturity levels*. ISACA. Retrieved October 21, 2026, from https://cmmiinstitute.com/learning/appraisals/levels
- Garvin, D. A. (1984). What does "product quality" really mean? *Sloan Management Review, 26*(1), 25–43.
- ISO. (2026a). *Quality management — Fundamentals and vocabulary* (ISO Standard No. 9000:2026). International Organization for Standardization.
- ISO. (2026b). *Quality management systems — Requirements* (ISO Standard No. 9001:2026). International Organization for Standardization.
- ISO/IEC. (2023). *Systems and software engineering — Systems and software Quality Requirements and Evaluation (SQuaRE) — Product quality model* (ISO/IEC Standard No. 25010:2023). International Organization for Standardization.
- Parasuraman, A., Zeithaml, V. A., & Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. *Journal of Retailing, 64*(1), 12–40.

Company names and figures in the tasks are fictitious training examples.
