---
course: IT Management and EAM
session: 6
title: IT Service Management II — Core Practices
subtitle: Practice tasks on the service desk, incident, problem and change enablement, service level management, SLAs, OLAs and underpinning contracts
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 6: the service desk, incident management with impact, urgency and priority, problem management with workarounds and known errors, change enablement with its three types of change, and service level management with SLAs, OLAs and underpinning contracts (AXELOS, 2019; Beims & Ziegenbein, 2023). The terms and the impact–urgency matrix follow the session slides. A calculator helps for the availability tasks. The last core task is in the style of an exam question.

## Getting the Terms Right

A municipal utility (*Stadtwerke*) runs an online customer portal where customers enter meter readings and download bills. Classify each situation as **incident**, **service request**, **problem**, **known error**, **workaround** or **change**.

- a) A customer cannot log in to the portal; the error message says "server not reachable".
- b) A new employee in customer service asks for access to the billing system.
- c) Since the last release, the portal crashes every time more than 2,000 users are logged in. Nobody knows why yet.
- d) The cause of the crashes has been found (a configuration limit in the application server) and documented; the fix is planned for next week.
- e) Until then, the service desk advises customers to enter meter readings via the mobile app, which uses a different server.
- f) The configuration limit of the application server is increased.
- g) The bill download is very slow, but it works after two minutes.

::: answer lines=8
:::

::: hint
An incident does not have to be a complete outage: a **reduction in quality** of a service also counts. Ask yourself for each item: is it a symptom, a cause, a planned modification, or a normal request?
:::

::: solution
- a) **Incident** (unplanned interruption for this customer)
- b) **Service request** (a normal, pre-defined request; no failure)
- c) **Problem** (the unknown cause of recurring incidents)
- d) **Known error** (the problem has been analysed and documented, but not yet resolved)
- e) **Workaround** (reduces the impact until the permanent fix is available)
- f) **Change** (modification of a component that can affect the service; probably a normal change)
- g) **Incident** (reduction in the quality of the service)
:::

## Prioritising Incidents in a Hospital

The IT department of a hospital uses the impact–urgency matrix from the session (P1 highest to P5 lowest). Its SLA with the hospital management defines these target times:

| Priority | Response | Resolution |
|---|---|---|
| P1 | 10 min | 2 h |
| P2 | 30 min | 4 h |
| P3 | 2 h | 1 working day |
| P4 | 4 h | 3 working days |
| P5 | 1 working day | 5 working days |

For each incident, assess **impact** and **urgency**, derive the **priority** and state the **resolution target**.

1. The patient record system is unavailable in the emergency department; all other wards can still use it.
2. A ward's label printer for blood samples is broken; the ward next door has a working printer on the same floor.
3. The staff roster software shows wrong weekend shifts; the roster for next month must be published in five days.
4. The Wi-Fi for patients and visitors is down in the whole hospital.
5. A senior physician's personal e-mail signature shows the wrong phone number.

::: answer lines=10
:::

::: hint
Ask about safety, revenue and the number of people affected (impact) and about the time by which the business really needs a solution (urgency). A workaround lowers the impact.
:::

::: solution
1. Impact **high** (patient safety, one critical department), urgency **high** → **P1**, resolution within 2 h. Accept impact "medium" (one department) with urgency high → P2 only with a clear argument; patient safety normally makes it P1.
2. Impact **low** (workaround: printer next door), urgency **medium** (samples must still be labelled, the workaround works) → **P4**, 3 working days. Accept P3 if the student argues that walking to the next ward delays urgent samples.
3. Impact **medium** (all staff, but no immediate harm), urgency **medium** (five days) → **P3**, 1 working day.
4. Impact **medium** (many users, but not core hospital processes), urgency **medium** or **low** → **P3** or **P4**. Accept either with reasoning.
5. Impact **low** (one user, cosmetic), urgency **low** → **P5**, 5 working days. The senior position of the user does not change the priority unless the hospital has defined VIP rules.

Marking hint: the justification counts more than the exact priority; impact and urgency must both be named.
:::

## Types of Change in an Online Shop

An online fashion retailer uses change enablement as described in ITIL 4. Classify each change as **standard**, **normal** or **emergency** and suggest a suitable **change authority**.

1. A new employee in the warehouse gets a user account with the standard warehouse role.
2. The payment module is replaced by a new payment provider before Black Friday.
3. Attackers are actively exploiting a vulnerability in the shop software; the vendor has just released a patch.
4. The product images on the start page are exchanged for the summer campaign using the content management system.
5. The database server is moved to a new cloud region.

Then explain in two or three sentences why it is useful to turn frequent normal changes into standard changes, and what must be in place before you do so.

::: answer lines=10
:::

::: solution
1. **Standard** change: low risk, documented procedure, pre-authorised; no individual approval needed (the procedure itself was authorised once, e.g. by the IT service manager).
2. **Normal** change: high risk and high business impact; authority e.g. a change board with the head of e-commerce, IT operations and security, or management for very high risk. Timing before Black Friday must be planned in the change schedule (or deliberately avoided).
3. **Emergency** change: must be done as soon as possible; fast-track authority, e.g. emergency change authority (head of IT operations and the security officer); test as far as possible, document and review afterwards.
4. Usually **not a change to the IT service** at all, but content work by the business (standard work in the CMS). If the student treats it as a change, **standard** change is correct.
5. **Normal** change: assessment of risk, migration plan and fallback; authority e.g. a change board including the cloud/infrastructure team.

Turning frequent normal changes into standard changes speeds up delivery and frees the change authority for risky changes (guiding principles "keep it simple and practical" and "optimise and automate"). Before that, the change must be well understood and low risk, with a documented and tested procedure, and its past success rate should be high; the pre-authorisation should be reviewed regularly.
:::

## Agreements That Must Fit Together

A logistics company's IT department provides the **warehouse management service** to the logistics business unit. Read the agreements and answer the questions.

- **SLA** with the logistics unit: service hours Mon–Sat 6:00–22:00; availability 99.5 % per month (26 operating days) in service hours; P1 incidents resolved within 2 h.
- **Agreement A** with the company's internal database team: support Mon–Fri 8:00–17:00; P1 response within 1 h.
- **Agreement B** with the cloud provider hosting the system: availability 99.9 % per month on a 24/7 basis.
- **Agreement C** with the vendor of the handheld scanners: replacement of broken devices within 3 working days.

1. Which of the agreements A–C is an **OLA**, which an **underpinning contract**? Explain the difference.
2. Calculate the **maximum downtime per month** allowed by the SLA.
3. Check for each agreement A–C whether it **underpins** the SLA. Where is there a gap, and how could the IT department close it?
4. Last month the system was down for 5 hours on a Saturday afternoon. Calculate the availability. Was the SLA target met?

::: answer lines=14
:::

::: hint
Underpinning means: the internal or external partner's promise must be at least as good as what the SLA promises, **in the same hours**. Check the time bases.
:::

::: solution
1. **A is an OLA** (agreement with an internal team of the same organisation). **B and C are underpinning contracts** (contracts with external suppliers). OLAs are internal agreements, usually not legal contracts; UCs are legally binding contracts.
2. Service time: 16 h × 26 days = **416 h**. Maximum downtime: 0.5 % × 416 h = **2.08 h ≈ 125 minutes** per month.
3. Gaps:
   - **A (OLA) does not underpin the SLA**: database support only Mon–Fri 8:00–17:00, but the service runs Mon–Sat 6:00–22:00; a P1 incident on Saturday or at 20:00 gets no database support, and a 1 h response leaves little time for a 2 h resolution. Remedy: on-call duty for the database team in service hours, faster response for P1.
   - **B (UC) underpins** the availability: 99.9 % on 24/7 is about 43.8 min downtime per month (0.1 % of 730 h), which is less than the 125 min allowed. But a single outage could fall entirely into service hours, so it uses up part of the SLA budget; other causes (application, network) must stay below the rest. Accept "underpins, with remaining risk".
   - **C (UC) does not underpin** a fast restoration if scanner failures count against the SLA: 3 working days. Remedy: spare pool of scanners in each warehouse, or renegotiate the contract. Students may argue that a single broken scanner is not a P1 incident; accept with reasoning.
4. Availability = (416 − 5) ÷ 416 × 100 % = **98.8 %** (exactly 98.80 %). Target 99.5 % **missed** (5 h > 2.08 h). The SLA report should show this, and the review should look at the cause (problem management) and the consequences agreed in the SLA.
:::

## From Vague Promises to Good Service Levels

The draft SLA for a university's **e-learning platform** contains these statements. For each one, explain what is wrong and rewrite it as a measurable, business-based target.

1. "The platform is available as much as possible."
2. "Problems are fixed quickly."
3. "Server CPU load stays below 70 %."
4. "IT does everything to make lecturers happy."

Then explain the **watermelon effect** with an example from this e-learning platform and suggest one measure that would reveal it.

::: answer lines=12
:::

::: solution
1. Not measurable, no time base. Better: "The platform is available 99.5 % during the lecture period, Mon–Sat 7:00–22:00, measured per month; planned maintenance only on Sundays and announced 5 days in advance."
2. "Quickly" is undefined, no distinction between response and resolution or priority. Better: "P1 incidents (platform unusable for all users): response within 15 min, service restored within 2 h in service hours; P3: resolution within 1 working day."
3. A technical, internal metric that means nothing to the customer (it could go into an OLA or internal monitoring). Better, business-based: "95 % of page loads and file uploads complete within 3 seconds during the exam period."
4. Not measurable, and it promises everything without obligations on the customer side. Better: "Lecturer satisfaction with the platform is measured each semester; target average of at least 4 on a 5-point scale" and add the customer's responsibilities, e.g. course rooms requested two weeks before the semester starts.

Watermelon effect: all SLA metrics are green (e.g. server availability 99.9 %), but students cannot hand in assignments because uploads time out shortly before deadlines — the users' experience is red. Measures: outcome-based metrics such as the share of successful uploads, end-to-end response time measured from the user's side, user satisfaction surveys, analysis of complaints and tickets.
:::

## Exam-Style Task: Order Platform at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5) now runs an **online order platform** for its 4,000 installer customers. The platform is operated by the company's IT department; it runs on servers of an external hosting provider, and orders are passed to the ERP system, which is run by the internal ERP team. Sales management, the internal customer, is unhappy: "The platform keeps failing and nobody tells us anything."

In the last four weeks, the IT department recorded the following:

- On four Tuesday afternoons in a row, the platform became so slow that orders timed out for about 45 minutes. Each time, the service desk received over 100 calls; the ERP team cleared the queue of the order interface, and the platform worked normally again.
- One installer reported that the price of a single article was shown incorrectly.
- There is no SLA. The hosting contract guarantees 99 % availability per month (24/7) and support on working days 8:00–16:00.

**Tasks:**

1. Distinguish **incident** and **problem** using this case. What should incident management and problem management each do? (4 points)
2. Assess the **priority** of the Tuesday failure and of the price error using **impact** and **urgency**. (3 points)
3. Problem management finds the cause: a weekly price import into the ERP system blocks the order interface. Explain the terms **known error** and **workaround** for this case, and name the **type of change** for the permanent fix with a justification. (3 points)
4. Propose the core content of an **SLA** between the IT department and sales management: four elements with concrete, measurable targets where applicable. (4 points)
5. Which **OLA** and which **underpinning contract** are relevant here? Assess whether the existing hosting contract underpins your SLA. (4 points)

::: answer lines=24
:::

::: solution
Marking guide (18 points):

**1. Incident vs. problem (4 points)**

- Incident: unplanned interruption or quality reduction of a service, here orders time out on Tuesday afternoons (each occurrence is an incident; the price error is also an incident) (1 point).
- Problem: the (unknown) cause of one or more incidents, here the cause of the recurring Tuesday failures (1 point).
- Incident management: restore service as fast as possible, e.g. clear the interface queue, inform installers and sales, link calls to one ticket (1 point).
- Problem management: identify the problem from the recurring pattern, analyse the root cause, document the workaround and known error, initiate a permanent fix via change enablement (1 point).

**2. Priorities (3 points)**

- Tuesday failure: impact high (all installers, revenue, reputation; a severe quality reduction counts as an incident), urgency high (orders in the afternoon still count for same-day delivery or are lost to competitors) → P1 or P2 with justification (1.5 points; 0.5 for the priority, 1 for naming impact and urgency with case reference).
- Price error: impact low (one article; however possibly wrong invoices — medium accepted), urgency medium → P3 or P4 with justification (1.5 points). Points also for noting that the price error might hint at the same import job (bonus thinking, no extra point).

**3. Known error, workaround, change type (3 points)**

- Known error: the problem is analysed and its root cause (the price import blocking the interface) is documented, but not yet resolved (1 point).
- Workaround: clearing the interface queue as soon as the slowdown starts, or temporarily starting the import manually in the evening until the fix is in place (1 point).
- Permanent fix, e.g. moving the import to the night or decoupling it: **normal change** — it needs assessment (does the night import conflict with other jobs? risk for prices) and authorisation by the change authority (1 point; 0.5 if type is right but the justification is missing). Emergency change only accepted if the student argues with very high ongoing damage; standard change not accepted (not yet a well-known, pre-authorised procedure).

**4. SLA content (4 points)** — 1 point per element with a concrete target, max. 4:

- Service description and scope: online ordering for installers, incl. price and stock display; excluded: ERP functions not used by the platform.
- Service hours and support hours, e.g. platform 24/7, support Mon–Sat 6:00–20:00.
- Availability, e.g. 99.5 % per month in the main order time Mon–Fri 6:00–18:00; maximum length of a single outage.
- Response and resolution times per priority, e.g. P1 response 15 min, resolution 2 h.
- Communication and reporting: information to sales within 30 min of a P1 incident; monthly report; quarterly review (addresses "nobody tells us anything").
- Responsibilities of sales management, e.g. report errors via the service desk, announce campaigns in advance.
- Statements without measurable targets (e.g. "high availability") get no point.

**5. OLA, UC and underpinning (4 points)**

- OLA with the internal ERP team, e.g. support for the order interface in the platform's support hours, P1 response time (1 point).
- Underpinning contract with the external hosting provider (1 point).
- Assessment (2 points): 99 % per month on 24/7 allows about 7.3 h downtime per month (1 % of about 730 h) and support only on working days 8:00–16:00. This does **not** underpin an SLA of e.g. 99.5 % with support from 6:00 and on Saturdays: renegotiate the contract (higher availability, extended support hours) or build redundancy. 1 point for the calculation or a correct comparison of the figures, 1 point for the conclusion with a measure.
:::

## Optional Challenge: Change Enablement in a DevOps Team {.optional}

The development team of a car-sharing app releases small updates several times a day. The company's change policy still requires every change to be approved by a change advisory board that meets on Tuesdays. The team has started to label every release as an "emergency change" to get around the board.

1. What risks does this situation create for the company?
2. Redesign the change enablement for this team: which changes should be standard, normal and emergency, who should be the change authority, and which controls replace the weekly board?
3. Which guiding principles from session 5 support your design?

::: answer lines=12
:::

::: solution
1. Risks: the emergency change category loses its meaning (real emergencies are not recognised); changes are not properly assessed or documented, so audits fail and failures are harder to trace; conflicts between the team and IT operations; the board becomes a formality.
2. Design (several solutions possible): small, low-risk releases that pass the automated pipeline (tests, security scans, peer review) become **standard changes**, pre-authorised once for the pipeline; changes with higher risk (e.g. payment, data model, interfaces to other teams) are **normal changes** authorised by the product owner and the platform lead, or by a board for cross-team changes; **emergency changes** only for incidents and security issues, with review afterwards. Controls: automated tests, peer review (four-eyes principle), deployment logs as evidence, feature toggles and automatic rollback, monitoring after deployment, regular review of failed changes.
3. **Keep it simple and practical** (no board for low-risk changes), **optimise and automate** (controls in the pipeline after optimising the process), **progress iteratively with feedback** (small releases, monitoring), **collaborate and promote visibility** (change schedule and logs visible to operations and audit), **focus on value** (fast delivery of useful features with controlled risk).
:::

## References {.references}

- AXELOS. (2019). *ITIL Foundation: ITIL 4 edition*. TSO.
- Beims, M., & Ziegenbein, M. (2023). *IT-Service-Management in der Praxis mit ITIL®: Zusammenarbeit systematisieren und relevante Ergebnisse erzielen* (6th ed.). Hanser.

ITIL® is a registered trademark of PeopleCert group.
