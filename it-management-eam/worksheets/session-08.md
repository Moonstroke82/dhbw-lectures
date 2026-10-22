---
course: IT Management and EAM
session: 8
title: IT Security and Business Continuity
subtitle: Practice tasks on protection goals, ISO/IEC 27001, BSI IT-Grundschutz, business continuity management and the business impact analysis
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 8: the protection goals of information security, the information security management system (ISMS) with ISO/IEC 27001 and its Annex A (ISO/IEC, 2022), the IT-Grundschutz method of the BSI with protection requirements and the maximum principle (BSI, 2017a, 2017b), business continuity management with ISO 22301 (ISO, 2019) and BSI-Standard 200-4 (BSI, 2023), and the business impact analysis (BIA) with the recovery parameters MTPD, RTO, RPO and MBCO. Terms and abbreviations follow the session slides; the standards are described in own words. The last core task is in the style of an exam question.

## Which Protection Goal Is at Risk?

For each event, name the protection goal that is **mainly** affected: **confidentiality**, **integrity**, **availability**, or one of the extended goals **authenticity**, **accountability** or **non-repudiation**. Some events affect more than one goal; name the main one and justify it in one line.

- a) A hospital's laboratory system is down for six hours; doctors cannot see blood test results.
- b) An attacker changes the bank details of a supplier in the ERP system; the next payment goes to the attacker.
- c) A sales employee takes a USB stick with the customer list home and loses it on the train.
- d) An e-mail that looks as if it came from the CEO asks accounting to make an urgent transfer.
- e) Five administrators share one admin account; after a wrong configuration change nobody can tell who made it.
- f) A customer claims she never placed an online order worth €4,000, and the shop cannot prove otherwise.
- g) A rounding error in a new software release calculates wrong interest on thousands of loan accounts.
- h) A cloud storage folder with scanned employee ID cards is publicly accessible via a link.

::: answer lines=8
:::

::: hint
Ask: was information **seen** by the wrong people, **changed** or wrong, or **not usable** when needed? The extended goals are about **who**: is the source genuine, can an action be traced to a person, and can that person deny it later?
:::

::: solution
- a) **Availability** — information exists and is correct, but cannot be used when needed.
- b) **Integrity** — data was changed without authorisation (also a sign of weak access control; consequences are financial).
- c) **Confidentiality** — personal and business data may be read by unauthorised people (also a GDPR data breach, session 7).
- d) **Authenticity** — the sender is not genuine (CEO fraud); accept integrity as the wider goal.
- e) **Accountability** — actions cannot be traced to a person because of the shared account.
- f) **Non-repudiation** — the shop cannot prove that the customer performed the action; accept authenticity with reasoning.
- g) **Integrity** — data are incorrect because of a processing error; integrity covers accidental changes too, not only attacks.
- h) **Confidentiality** — unauthorised access is possible even if nobody has opened the link yet.

Marking hint: one point per item for the right goal with a reason; for d) and f), integrity is acceptable only if the student links it to authenticity or proof.
:::

## Inside ISO/IEC 27001

A medium-sized software company prepares for its first ISO/IEC 27001 certification.

1. Assign each activity to the **clause** of ISO/IEC 27001 (4 to 10) where it belongs.
   - a) The board approves the information security policy and names a CISO.
   - b) The company decides that its ISMS covers development and hosting, but not the canteen.
   - c) An internal auditor checks whether the access review procedure is followed.
   - d) All employees complete an awareness training on phishing.
   - e) A nonconformity from the audit is analysed and a corrective action is defined.
   - f) Risks are assessed and a treatment plan is drawn up.
2. Assign each control to its **Annex A theme** (organisational, people, physical, technological): backup of the source code repository · visitor badges at reception · confidentiality agreements for new staff · supplier security requirements in contracts · multi-factor authentication · clear desk rule.
3. The managing director says: "We implement all 93 controls in Annex A, then we are certified." Correct the statement and explain the role of the **statement of applicability**.

::: answer lines=12
:::

::: solution
1. a) **Clause 5** Leadership · b) **Clause 4** Context (scope of the ISMS) · c) **Clause 9** Performance evaluation (internal audit) · d) **Clause 7** Support (awareness and competence) · e) **Clause 10** Improvement · f) **Clause 6** Planning (risk assessment and risk treatment; carrying them out regularly is clause 8 Operation — accept either with reasoning).
2. Backup → **technological** · visitor badges → **physical** · confidentiality agreements → **people** · supplier security requirements → **organisational** · multi-factor authentication → **technological** · clear desk → **physical** (it protects information in the workspace; accept people with reasoning).
3. Certification is not about ticking off all controls. ISO/IEC 27001 requires a working **management system**: scope, leadership, risk assessment and treatment, objectives, competence, audits, management review and improvement (clauses 4–10). Controls are **selected based on the risk assessment**; some may not apply (e.g. secure development if the company does not develop software — not the case here), and further controls may be added. The **statement of applicability** lists every Annex A control, states whether it is applied, justifies inclusion or exclusion and shows whether it is implemented; auditors use it as the link between risks and controls. ISO/IEC 27002 gives guidance on implementing the controls but is not certifiable.
:::

## Protection Requirements in a Dental Practice Group

A group of six dental practices (90 employees) wants to follow the IT-Grundschutz method of the BSI. The structure analysis found these objects:

| Object | Used for |
|---|---|
| Patient management software | Patient records, treatment notes, billing to health insurers |
| Online appointment booking | Patients book appointments on the website |
| Digital X-ray system | Images are taken and stored in each practice |
| Guest Wi-Fi | Internet for patients in the waiting rooms |
| Central server in practice 1 | Hosts the patient management software and the appointment booking |

1. Rate the protection requirements (**normal**, **high**, **very high**) for confidentiality, integrity and availability of the first four objects. Justify each rating with a damage scenario.
2. Derive the protection requirements of the **central server**. Which principle do you apply?
3. The X-ray system runs on six identical local computers, one per practice. Does this change the availability requirement of a single computer? Name the effect.
4. For which objects does the IT-Grundschutz method require an additional **risk analysis** (BSI-Standard 200-3), and why?

::: answer lines=14
:::

::: hint
Damage scenarios include violations of laws and contracts, impaired ability to perform tasks, personal safety, financial consequences and reputation. A system inherits the needs of what runs on it; several systems that can stand in for each other may lower the need of each one.
:::

::: solution
1. Example ratings (consistent justification is what counts):
   - **Patient management software:** C **very high** (health data are special categories under the GDPR, medical confidentiality, severe damage to patients and reputation) · I **high to very high** (wrong treatment notes or allergies can harm patients) · A **high** (practices can work for a few hours with paper, but not for days; billing deadlines).
   - **Online appointment booking:** C **normal to high** (names and contact data; the reason for the visit may reveal health data → high) · I normal · A **normal** (patients can phone).
   - **Digital X-ray system:** C **high** (health data) · I **high** (wrong or mixed-up images → wrong diagnosis) · A **high** (treatments that need X-rays must be postponed).
   - **Guest Wi-Fi:** C normal · I normal · A normal — it must be separated from the practice network, otherwise it inherits risks.
2. **Maximum principle:** the server inherits the highest requirement of the applications it hosts → C very high, I high to very high, A high. Consequence: the server needs strong protection; it might be better to separate the booking system (internet-facing) from the patient data.
3. **Distribution effect:** if one computer fails, the practice can use another practice's system only for appointments there — so the effect is limited. Within one practice there is no stand-in, so availability per practice stays high; if patients can be moved to another practice nearby, the requirement of each single computer can be lowered to normal. Accept either conclusion with this reasoning. (The opposite, the **cumulation effect**, raises the need when many small damages add up.)
4. For all objects with **high or very high** requirements (patient management software, server, X-ray system) and for objects for which no suitable module exists in the Kompendium (e.g. special medical devices). Reason: the standard requirements of the Kompendium are designed for normal protection requirements; higher needs may require additional measures.
:::

## The Newspaper That Did Not Appear

The *Kraichgau Tagblatt*, a regional newspaper, produces its daily print edition with an editorial system. The print deadline is **22:30**; the printing plant needs the final pages by then, otherwise the paper does not appear the next day. The BIA set these parameters for the process "produce the daily edition":

| Parameter | Value |
|---|---|
| MTPD | 6 hours (on a production day) |
| RTO of the editorial system | 4 hours |
| RPO of the editorial system | 1 hour |
| MBCO | 16 pages instead of 32, no supplements |

The IT situation: a full backup runs every night at **01:00** to a tape drive. The tapes are kept in a fireproof cabinet **in the server room**. The last restore test, a year ago, took **9 hours**.

On a Tuesday at **18:00**, a burst water pipe floods the server room. Server, tape drive and cabinet are under water.

1. How much data would be lost if the latest tape could be restored? Compare with the RPO.
2. Assuming the tape survived, could the editorial system be running again in time for the print deadline? Compare the restore time with the RTO and the MTPD.
3. Why is the situation in fact even worse? Name the design error.
4. Propose **three** measures that would make the parameters achievable, and one way to reach the **MBCO** on that evening without the editorial system.
5. Which **ISO/IEC 27001 Annex A themes** do your measures belong to?

::: answer lines=14
:::

::: hint
The RPO is measured backwards from the disruption to the last usable copy of the data; the RTO and the MTPD forwards from the disruption.
:::

::: solution
1. Last backup at 01:00, disruption at 18:00 → **17 hours** of data lost (the whole day's editorial work). Required RPO: 1 hour → missed by far.
2. Restore takes 9 hours → system running at about **03:00** (plus time to get replacement hardware). RTO 4 h (22:00) and MTPD 6 h (24:00) are both exceeded, and so is the print deadline of 22:30 → the paper does not appear. Even the RTO itself leaves only 30 minutes of margin before the deadline; a good BIA would also check this.
3. The backup copies are stored **in the same room** as the system they protect: one event (water, fire, ransomware on connected media) destroys original and backup together. There is no off-site or offline copy, and the restore has not been tested for a year.
4. Measures (any three, with reference to the parameters): replication of the editorial database to a second site or cloud at least every hour (RPO ≤ 1 h); off-site and offline backup copies (e.g. 3-2-1 rule); a standby system or cloud environment that can be started within the RTO; regular restore tests with measured times; moving the server room out of reach of water pipes, water sensors. MBCO on the evening: emergency workflow — editors write in a cloud office tool or from home, the layout team builds a reduced 16-page edition from templates and sends PDF pages directly to the printing plant; agreement with the printing plant about a later deadline as part of the continuity plan.
5. Replication, backup and restore tests → **technological** (backup, redundancy); off-site storage and protection against water → **physical** (protecting equipment against environmental threats); continuity plan and emergency workflow → **organisational** (ICT readiness for business continuity, incident management).
:::

## A Business Impact Analysis in Contract Logistics

*Odenwald Logistik GmbH* (600 employees) stores and ships goods for industrial customers. Its largest customer is a pharmaceutical wholesaler; the contract requires that orders are shipped within 24 hours, with high penalties otherwise. All warehouse processes run on one **warehouse management system (WMS)**; invoicing and payroll run on the ERP system.

The BIA workshop rated the impact of an outage of each process over time. The company's criterion: an impact of **high** or **very high** is **unacceptable**.

| Process | 4 hours | 1 day | 3 days | 1 week |
|---|---|---|---|---|
| P1 Goods receipt | low | medium | high | very high |
| P2 Picking and shipping for the pharma customer | medium | high | very high | very high |
| P3 Invoicing customers | low | low | low | medium |
| P4 Payroll (outage in the week before pay day) | low | low | medium | high |
| P5 Shipment tracking portal for customers | low | medium | medium | high |

1. Determine the **MTPD** of each process (use the first point in time at which the impact becomes unacceptable).
2. Rank the processes and name the **time-critical** ones.
3. Propose an **RTO** for P1 and P2 and explain why it must be shorter than the MTPD.
4. P1, P2 and P5 all depend on the WMS. Which RTO must the **WMS** meet? Explain the rule.
5. Propose a sensible **MBCO** for P2 and a continuity solution that achieves it.

::: answer lines=14
:::

::: solution
1. MTPD: P1 **3 days** · P2 **1 day** · P3 **more than 1 week** (no unacceptable impact in the period analysed) · P4 **1 week** · P5 **1 week**. Accept a refined statement such as "P2: between 4 hours and 1 day" if the student explains it.
2. Ranking by MTPD: P2 (1 day) > P1 (3 days) > P4 and P5 (1 week) > P3. Time-critical: **P2** clearly, **P1** also (both need recovery within days); P4 is only critical in the week before pay day — a good point for discussion (the time of the year or month matters).
3. Example: P2 RTO **8–12 hours**, P1 RTO **1 day**. The RTO must be shorter than the MTPD because recovery takes time to organise, the emergency solution may not work at once, and a backlog builds up during the outage that must be worked off before the impact becomes unacceptable (safety margin).
4. The WMS must meet the **shortest RTO** of the processes that depend on it, i.e. the RTO of P2 (8–12 h). A resource inherits the strictest requirement of the processes it supports — the same idea as the maximum principle for protection requirements.
5. MBCO for P2, e.g.: all orders of the pharma customer marked "urgent" are shipped within 24 hours; other customers' orders may wait. Continuity solution: paper-based or spreadsheet-based picking with printed pick lists exported every hour from the WMS (or a read-only replica); a standby WMS instance in a second data centre or the cloud; agreement with the customer on an emergency procedure. Accept other solutions that would actually achieve the MBCO within the RTO.
:::

## Exam-Style Task: Security and Continuity at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–7), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers. Orders received by 14:00 are delivered the same day from the central warehouse. The platform is hosted by an external provider (99 % availability per month, 24/7; support Mon–Fri 8:00–16:00); orders are passed to the ERP system in the company's own server room. After a data leak and a hospital group's demand for security clauses (session 7), the board decides to build an ISMS and business continuity management.

Current situation:

- The ERP system is backed up every night at 2:00 to a storage device in the same server room. Nobody has ever restored the whole system.
- There is no plan for what to do if the platform or the ERP system fails; the IT manager says, "We would fix it."
- The warehouse needs the ERP system to print pick lists and delivery notes.

**Tasks:**

1. Explain the three classic **protection goals** and give one example from the case for each. (3 points)
2. Recommend whether Kurpfalz Sanitär should build its ISMS on **ISO/IEC 27001** directly or on **BSI IT-Grundschutz**. Justify with two arguments and name three first steps. (4 points)
3. Carry out a short **BIA** for the processes "order intake via the platform" and "same-day picking and delivery": describe the impact over time and set **MTPD, RTO, RPO** and **MBCO** for each. (6 points)
4. Assess the current backup and the hosting contract against your parameters. (4 points)
5. Propose two **continuity solutions** and one **exercise**. Who must approve the BIA results and the solutions? (3 points)

::: answer lines=28
:::

::: solution
Marking guide (20 points):

**1. Protection goals (3 points, 1 per goal: definition 0.5, case example 0.5)**

- **Confidentiality:** only authorised people can access information — e.g. installer customer lists and order volumes (the data leak from session 7).
- **Integrity:** information is correct and complete, changes are authorised — e.g. prices and order quantities in the platform and the ERP system; wrong delivery addresses.
- **Availability:** information and systems can be used when needed — e.g. the platform and the ERP system before the 14:00 order deadline.

**2. ISO/IEC 27001 or IT-Grundschutz (4 points)**

- Recommendation with two arguments (2 points). Both are acceptable:
  - **ISO/IEC 27001** directly: internationally known certificate that customers (the hospital group) recognise; risk-based and flexible for a private company; less detailed documentation effort than the full Grundschutz modelling.
  - **IT-Grundschutz:** free and very concrete requirements, helpful for a company without security experience; also leads to an ISO/IEC 27001 certificate (on the basis of IT-Grundschutz); basic protection allows a quick start. Note that Grundschutz++ is replacing the Kompendium — accept this as an argument for waiting or for ISO.
- Three first steps (2 points, 0.5 each, max. 2): management commitment and security policy (clause 5 / BSI 200-1); appoint a CISO / information security officer; define the scope (e.g. platform, ERP, warehouse); inventory of information, applications and systems (structure analysis); risk assessment or protection requirements assessment; quick wins such as off-site backup and MFA.

**3. BIA (6 points, 3 per process: impact over time 1, MTPD and RTO 1, RPO and MBCO 1)**

- **Order intake via the platform:** daily turnover about €1.3 million (€320 m ÷ about 250 working days), 70 % via the platform → about €0.9 million per day. 1 h: some orders delayed, installers phone sales; 4 h before 14:00: same-day promise broken, installers buy from competitors; 1 day: about €0.9 m revenue at risk, reputation damage with installers; 1 week: loss of customers, contractual problems with large customers. Example parameters: **MTPD 4–8 hours** on a working day · **RTO 2 hours** · **RPO close to 0 / max. 15 minutes** (lost orders are lost revenue and angry customers) · **MBCO**: installers can order by phone or e-mail with sales staff entering orders, or a reduced platform without live stock levels.
- **Same-day picking and delivery:** depends on ERP (pick lists, delivery notes). 1 h: delay can be caught up; 4 h: afternoon tours cannot leave, same-day promise broken; 1 day: backlog, lost customers; 1 week: severe. Example: **MTPD 4 hours** in the morning (before the tours) · **RTO 1–2 hours** · **RPO 1 hour or less** (orders and stock data) · **MBCO**: delivery of all orders received until 12:00, with manually printed pick lists.
- Parameters may differ; points require RTO < MTPD, an RPO that fits the data, and an MBCO that is a concrete minimum level.

**4. Assessment of backup and hosting (4 points)**

- Nightly ERP backup → data loss of up to **24 hours** (failure just before 2:00) — does not meet an RPO of 1 hour or less (1 point).
- Backup in the **same server room**: fire, water or ransomware can destroy system and backup together; restore never tested → restore time unknown, RTO cannot be promised (1 point).
- Hosting: 99 % per month on 24/7 allows about **7.3 hours** of downtime per month (1 % of about 730 h), possibly in one block during order time — does not meet an RTO of 2 hours (1 point).
- Support only Mon–Fri 8:00–16:00: no support early in the morning or on Saturdays, the response is too slow for the MTPD of order intake (1 point). Conclusion: renegotiate the underpinning contract (session 6) or build redundancy.

**5. Continuity solutions, exercise, approval (3 points)**

- Two solutions (1 point, 0.5 each), e.g.: hourly replication or frequent incremental backups of the ERP system to a second site or cloud, plus an offline copy; standby ERP or platform environment; emergency order intake by phone and e-mail with a prepared form; manual pick lists from a regularly exported order file; new hosting contract with higher availability and 24/7 support.
- One exercise (1 point): e.g. full restore test of the ERP system with measured time; tabletop exercise "platform down at 10:00 on a Monday" with sales, warehouse and IT; switch-over test to the standby environment.
- Approval (1 point): **top management / the board** approves the BIA results, the recovery parameters and the budget for the solutions (it decides which residual risk is acceptable); process owners (sales, warehouse) provide the business view. Not the IT manager alone — "we would fix it" is no plan.
:::

## Optional Challenge: A Municipal Utility Prepares for NIS2 {.optional}

*Stadtwerke Bergstraße* (a municipal utility for electricity, gas and drinking water, 420 employees) is an essential entity under NIS2 (session 7). The managing director asks you:

1. Map these NIS2 risk-management measures (Directive (EU) 2022/2555, Art. 21(2)) to the instrument from session 8 that best covers them: **ISMS (ISO/IEC 27001 or IT-Grundschutz)**, **Annex A control theme**, or **BCM (ISO 22301 or BSI-Standard 200-4)**:
   - a) policies on risk analysis and information system security
   - b) business continuity, such as backup management and disaster recovery, and crisis management
   - c) supply chain security
   - d) human resources security, access control and asset management
   - e) use of multi-factor authentication
2. The utility has no ISMS yet. Its IT team proposes to start with Grundschutz++ "because it is the future". Discuss the proposal.
3. Why should the utility not run the ISMS and the BCM as two separate projects?

::: answer lines=12
:::

::: solution
1. a) **ISMS** core: security policy (leadership), risk assessment and treatment (ISO/IEC 27001 clauses 5–6; BSI 200-1 to 200-3). b) **BCM**: BIA, continuity strategies, plans and exercises (ISO 22301 clause 8, BSI-Standard 200-4), supported by Annex A controls on backup, redundancy and ICT readiness for business continuity. c) Annex A **organisational** controls on supplier relationships; ISMS risk assessment of suppliers. d) Annex A **people** controls (screening, training) and **organisational/technological** controls (asset inventory, access rights). e) Annex A **technological** controls (secure authentication); also a Kompendium requirement.
2. Arguments for: Grundschutz++ is certifiable from 2027, machine-readable requirements support tools and automation, and it avoids a later migration from the classic Kompendium. Arguments against or cautions: early experience is limited, tools and consultants are still adapting; NIS2 duties apply now, so waiting is not an option. A sensible answer: start now with the elements that are the same in all approaches (policy, roles, scope, inventory, protection requirements, BIA, quick wins) and decide on ISO/IEC 27001 native, classic IT-Grundschutz or Grundschutz++ based on current BSI guidance; utilities may also be operators of critical facilities with sector-specific requirements, which must be checked.
3. Both systems share the same management structure (harmonised clauses 4–10), the same inventory of processes and resources, the same risk view (availability ratings feed the BIA), the same roles (top management, process owners) and the same audits and management reviews. Running them together avoids duplicate work and contradictions (e.g. backup requirements that differ between ISMS and BCM), and gives management one overall picture, as in integrated GRC (session 7).
:::

## References {.references}

- Bundesamt für Sicherheit in der Informationstechnik. (2017a). *BSI-Standard 200-1: Managementsysteme für Informationssicherheit (ISMS)* (Version 1.0). BSI.
- Bundesamt für Sicherheit in der Informationstechnik. (2017b). *BSI-Standard 200-2: IT-Grundschutz-Methodik* (Version 1.0). BSI.
- Bundesamt für Sicherheit in der Informationstechnik. (2023). *BSI-Standard 200-4: Business Continuity Management*. BSI.
- Directive (EU) 2022/2555 of the European Parliament and of the Council of 14 December 2022 on measures for a high common level of cybersecurity across the Union (NIS 2 Directive). (2022). *Official Journal of the European Union*, L 333, 80–152. http://data.europa.eu/eli/dir/2022/2555/oj
- ISO. (2019). *Security and resilience — Business continuity management systems — Requirements* (ISO Standard No. 22301:2019). International Organization for Standardization.
- ISO/IEC. (2022). *Information security, cybersecurity and privacy protection — Information security management systems — Requirements* (ISO/IEC Standard No. 27001:2022). International Organization for Standardization.

Company names and figures in the tasks are fictitious training examples.
