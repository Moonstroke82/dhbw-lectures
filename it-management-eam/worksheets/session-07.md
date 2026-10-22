---
course: IT Management and EAM
session: 7
title: IT Risk and Compliance Management
subtitle: Practice tasks on GRC, the three lines model, GDPR, NIS2 and DORA, the ISO 31000 risk management process and ethics
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 7: governance, risk and compliance (GRC) as an integrated view (Racz et al., 2010), compliance of IT and IT for compliance (Tiemeyer, 2023), the three lines model (The Institute of Internal Auditors, 2020), the main EU requirements for IT (GDPR, NIS2 with the German BSI Act, DORA), the risk management process of ISO 31000 (ISO, 2018) and ethical questions in IT decisions (Mason, 1986). The terms, the 5 × 5 risk matrix and the treatment options follow the session slides. The tasks are practice in applying the rules; they are not legal advice. The last core task is in the style of an exam question.

## Governance, Risk or Compliance?

Assign each activity to **governance**, **risk management** or **compliance**. Then state which **line** of the three lines model (governing body, first, second or third line) typically performs it.

- a) The supervisory board decides how much IT risk the company is willing to take.
- b) The service owner of the HR system reviews every quarter who has access to salary data.
- c) The information security officer checks whether all service owners have done their access reviews.
- d) The data protection officer keeps the record of processing activities up to date.
- e) Internal audit examines whether the change process works as documented and reports to the audit committee.
- f) The IT operations team rates the likelihood and consequence of a failure of the data centre cooling system.
- g) The executive board sets the rule that the CIO reports to the CEO and chairs the IT steering committee.

::: answer lines=8
:::

::: hint
Governance is about **direction and decision rights**, risk management about **uncertain events and their effect on objectives**, compliance about **meeting requirements**. The first line owns the risk; the second line supports, monitors and challenges; the third line is independent.
:::

::: solution
- a) **Governance** (setting the risk appetite is a direction decision; it is also the starting point of risk management) — **governing body**.
- b) **Compliance** (control that implements a requirement, e.g. GDPR Art. 32 and internal access policy) and risk treatment — **first line** (the service owner owns the risk).
- c) **Compliance** monitoring — **second line**.
- d) **Compliance** (GDPR Art. 30) — **second line** (the data protection officer advises and monitors; the business units supply the information).
- e) Independent assurance on compliance and risk management — **third line**.
- f) **Risk management** (risk analysis) — **first line**.
- g) **Governance** (decision rights and structures, session 3) — **governing body** / executive board.

Marking hint: accept a second category where the student explains it (e.g. b) as risk treatment). The line assignment must match the role: the first line never "only checks" others, the third line never runs controls itself.
:::

## Which Rules Apply?

Decide for each organisation whether the **GDPR**, **NIS2** (in Germany the BSI Act, BSIG) and **DORA** apply. For NIS2, state the category (essential/*besonders wichtig* or important/*wichtig*) where it applies. Justify each decision in one line.

| Organisation | Employees | Activity |
|---|---|---|
| A | 2,000 | Insurance company with an online customer portal |
| B | 1,500 | Operator of a regional airport |
| C | 600 | Manufacturer of frozen food, sells to supermarkets |
| D | 40 | Start-up with a health app that records users' blood pressure |
| E | 15 | Provider of DNS services for business customers |
| F | 120 | Crypto exchange (crypto-asset service provider) |

::: answer lines=12
:::

::: hint
Three questions for NIS2: Is the sector listed (Annex I or Annex II)? Is the entity at least medium-sized, or is it one of the few types in scope regardless of size? Is there a sector-specific law that takes precedence? Remember: almost every organisation processes personal data.
:::

::: solution
- **A Insurance company:** GDPR yes (customer and employee data). DORA **yes** (insurance undertakings are financial entities). NIS2: insurance is not one of the NIS2 sectors; DORA covers ICT risk management, incident reporting and testing anyway.
- **B Airport operator:** GDPR yes. NIS2 **yes**: transport sector (air), Annex I; large (≥ 250 employees) → **essential** (*besonders wichtige Einrichtung*); probably also an operator of a critical facility (KRITIS). DORA no.
- **C Frozen food manufacturer:** GDPR yes. NIS2 **yes**: production, processing and distribution of food is an Annex II sector; at least medium-sized → **important** (*wichtige Einrichtung*), because Annex II entities are important regardless of whether they are medium or large. DORA no.
- **D Health app start-up:** GDPR **yes**, and health data are special categories of personal data (Art. 9), which requires an explicit legal basis, strong security and usually a data protection impact assessment (Art. 35). NIS2 no: below the size threshold (fewer than 50 employees; accept "unless turnover and balance sheet exceed €10 million"). DORA no.
- **E DNS provider:** GDPR yes (customer contacts). NIS2 **yes, regardless of size**: DNS service providers belong to digital infrastructure (Annex I) and are **essential** entities even when small. DORA no (unless it is a critical ICT provider for financial entities, which is unlikely at this size).
- **F Crypto exchange:** GDPR yes. DORA **yes** (crypto-asset service providers are financial entities). NIS2 not as a sector; DORA applies as the financial-sector law.

Marking hint: 1 point per organisation if all three laws are decided correctly with a reason; the NIS2 category is needed for B, C and E.
:::

## Ransomware at the Food Manufacturer: Who Must Be Told by When?

Organisation C from the previous task (an **important entity** under the BSIG) is hit by ransomware. The timeline:

- **Friday 22:00:** the IT on-call team notices that the production planning system and the HR database are encrypted. The attackers claim to have copied employee data, including bank details.
- **Saturday 10:00:** production is stopped; deliveries to supermarkets are delayed.
- The CIO wants to "first fix the systems and inform management on Monday".

1. Which **reports** must the company make under the BSIG (NIS2) and under the GDPR? State the **recipient** and the **latest deadline** for each, starting from Friday 22:00.
2. When must the employees be informed, and why?
3. Comment on the CIO's plan. Who must be involved, and which governance duty does the plan ignore?
4. Which ITIL practice from session 6 should be extended so that this works next time, and how?

::: answer lines=14
:::

::: hint
NIS2 and the BSIG have a three-step reporting duty for significant incidents. The GDPR has its own 72-hour rule for personal data breaches. The deadlines run from the moment the company becomes aware of the incident.
:::

::: solution
1. **BSIG / NIS2** (significant incident: production stopped, deliveries affected) to the **BSI**: early warning within **24 h** → by **Saturday 22:00**; incident notification with a first assessment within **72 h** → by **Monday 22:00**; final report within **one month** after the incident notification (progress reports if requested). **GDPR** (personal data breach: employee data copied) to the **data protection supervisory authority** of the federal state: without undue delay and where feasible within **72 h** → by **Monday 22:00** (Art. 33). The breach must also be documented internally.
2. Employees must be informed **without undue delay** because the breach is likely to result in a **high risk** to them (bank details, risk of fraud and phishing) (GDPR Art. 34). Practically: as soon as the facts are clear enough, with advice on what to do (watch accounts, beware of phishing).
3. The plan misses the 24-hour deadline and ignores the duty of management: under § 38 BSIG (Art. 20 NIS2) **management** must implement and oversee the risk management measures and is liable — it must be informed at once, not on Monday. Also involve the information security officer, the data protection officer, legal, communications and possibly the police and the cyber insurer. Restoring systems is incident management; reporting and decisions (e.g. about ransom, communication with customers) are management tasks.
4. **Incident management** (with the major incident procedure): add a classification step "significant incident / personal data breach?", a checklist with reporting deadlines, named roles (who reports to the BSI and to the authority), contact details and templates; test it in an exercise. Accept also **information security management** or the service desk with a justified answer.

Marking hint: deadlines must be given as concrete times; "within 72 hours" without the correct starting point gets half credit.
:::

## A Risk Register for an Online Furniture Shop

An online furniture retailer (450 employees) uses the 5 × 5 matrix from the session: risk level = likelihood × consequence, each from 1 to 5. Its **risk criteria**: low 1–4 (accept), medium 5–9 (treat if cost-effective), high 10–16 (must be treated), very high 20–25 (must be treated immediately, board informed).

| No. | Risk | Likelihood | Consequence |
|---|---|---|---|
| 1 | The shop is unavailable during the Black Friday weekend because of an overload | 3 | 5 |
| 2 | An employee's laptop with unencrypted customer data is stolen | 3 | 3 |
| 3 | The payment provider changes its interface and orders fail for a day | 2 | 3 |
| 4 | Attackers take over admin accounts of the shop system because there is no multi-factor authentication | 4 | 5 |
| 5 | A small supplier of product photos goes out of business | 2 | 1 |

1. Calculate the **risk level** of each risk, classify it and **rank** the risks.
2. For each risk, choose a **treatment option** (avoid, reduce, share, accept) and name a concrete measure.
3. For risk 4, estimate the **residual risk** after your measure. Who should decide whether it can be accepted?
4. The CFO suggests: "We buy a cyber insurance policy, then all cyber risks are treated." Assess this statement.

::: answer lines=16
:::

::: solution
1. Levels: risk 1 = 15 (high), risk 2 = 9 (medium), risk 3 = 6 (medium), risk 4 = **20 (very high)**, risk 5 = 2 (low). Ranking: 4 > 1 > 2 > 3 > 5.
2. Treatments (examples):
   - Risk 4: **reduce** immediately: multi-factor authentication for all admin accounts, separate admin accounts, monitoring of logins; inform the board.
   - Risk 1: **reduce**: load tests before Black Friday, scalable cloud capacity, queueing page; possibly **share** part of the financial loss via insurance.
   - Risk 2: **reduce**: hard-disk encryption on all laptops, no customer data on local devices. (Also reduces GDPR breach consequences: encrypted data on a stolen laptop usually do not require informing customers.)
   - Risk 3: **reduce**: contract clause on advance notice of interface changes, test environment, monitoring of failed payments; or **accept** with a monitored workaround.
   - Risk 5: **accept** (low risk; other photo suppliers exist).
3. With MFA and monitoring, likelihood drops to about 2 (rare to unlikely), consequence stays 5 → residual risk about 10 (high, but much lower) or 5 if the student argues likelihood 1. Further measures (privileged access management, logging) may be needed to reach the risk appetite. The **risk owner** in the first line (e.g. the head of e-commerce or the service owner of the shop) decides about acceptance within the risk appetite set by the governing body; for high residual risks, management must sign off. The IT administrator does not accept risks.
4. Insurance only **shares the financial consequence** of some events; it does not prevent the incident, does not restore the shop, does not remove legal duties (GDPR, reputation) and usually requires minimum security measures (e.g. MFA, backups) as a condition. Insurance is one treatment option among others, usually combined with risk reduction.
:::

## Monitoring in the Call Centre: Legal, but Right?

The customer service centre of a telecoms provider (300 agents) plans a new "productivity analytics" tool. It records every keystroke and every pause, analyses the agents' voice in all calls for "emotional tone", and shows a daily ranking of all agents on a screen in the office. The vendor says the tool is "GDPR-ready".

1. Analyse the plan with Mason's four issues (**privacy, accuracy, property, accessibility**). Name at least one concrete concern for each.
2. Why does "the tool is GDPR-ready" not settle the question? Distinguish the legal from the ethical question.
3. Propose a version of the plan that still helps to improve service quality but that you would find acceptable. Who should be involved in the decision?

::: answer lines=12
:::

::: solution
1. **Privacy:** continuous, complete monitoring of behaviour and emotions; agents cannot control what is revealed about them. **Accuracy:** is "emotional tone" measured correctly (accents, illness, difficult customers)? Who is accountable for wrong scores that affect careers? **Property:** who owns the voice and behaviour data — can the company reuse them, e.g. to train AI models, or sell insights? **Accessibility:** who may see the data and rankings — colleagues on the screen, managers, HR? Do agents get access to their own data?
2. A tool cannot be "GDPR-compliant" by itself; compliance depends on how it is used (purpose, lawful basis, proportionality, transparency, data protection impact assessment for systematic monitoring of employees). In Germany, employee monitoring is also limited by employment law and requires the works council's co-determination. Even if a lawful version exists, the ethical question remains: is total monitoring fair and respectful, does it damage trust and motivation, does it create pressure that harms health? Legal is a minimum, not proof that something is right.
3. Acceptable version (example): aggregated team-level statistics instead of individual rankings; no keystroke logging; emotional analysis only on a voluntary basis for training or not at all; individual feedback only to the agent and the coach; clear deletion periods; transparency about what is measured. Involve the works council, the data protection officer (DPIA), HR, agents' representatives and the service owner. Accept other well-reasoned proposals.
:::

## Exam-Style Task: Compliance at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2, 5 and 6), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, runs an **online order platform** for its 4,000 installer customers, most of them small trades businesses and sole traders. The platform is hosted by an external provider. Recent events:

- A sales employee sent an Excel list with names, e-mail addresses, phone numbers and annual order volumes of all installers to a wrong external e-mail address. He noticed it the next morning and told nobody.
- A hospital group, one of the largest customers, demands that Kurpfalz Sanitär sign a new contract with **information security clauses** "because of NIS2".
- Sales management wants the platform to **automatically refuse same-day delivery** to installers whose payment score, calculated by an algorithm from past payment delays, is below a threshold.
- There is no risk register; IT risks are discussed "when something happens".

**Tasks:**

1. Explain the difference between **compliance of IT** and **IT for compliance**, with one example from the case for each. (3 points)
2. Assess whether the **GDPR**, **NIS2** (BSIG) and **DORA** apply to Kurpfalz Sanitär AG. Explain why the hospital group demands security clauses. (4 points)
3. What must the company do now about the wrongly sent e-mail? Name the steps, the deadline and the recipient. (3 points)
4. Introduce risk management based on **ISO 31000**: describe the steps of the process and rate **two** IT risks of the case with likelihood × consequence and a treatment option. (5 points)
5. Assign three concrete tasks to the **three lines** at Kurpfalz Sanitär AG. (3 points)
6. Discuss the automated delivery refusal from an **ethical** point of view. (2 points)

::: answer lines=26
:::

::: solution
Marking guide (20 points):

**1. Compliance of IT vs. IT for compliance (3 points)**

- Compliance of IT: IT systems and processes themselves must meet requirements (1 point), e.g. the order platform must protect installers' personal data with appropriate security measures and access rights; e-mail must not leak customer lists (0.5 points).
- IT for compliance: IT supports the company in meeting requirements (1 point), e.g. a data loss prevention filter that blocks customer lists in external e-mails, a GRC tool or risk register, an archive for invoices (0.5 points).

**2. Applicability (4 points)**

- GDPR **applies** (1 point): installers are often sole traders, and contact persons of businesses are natural persons — names, e-mail addresses, phone numbers and order volumes are personal data; employees' data too.
- NIS2/BSIG **does not apply directly** (1 point): wholesale of bathroom fittings is not one of the sectors in Annex I or II, although the company is large. Accept "check carefully, e.g. if the company also manufactures listed products" as an addition.
- DORA **does not apply** (0.5 points): not a financial entity.
- Hospital group (1.5 points): hospitals are in scope of NIS2 (health sector) and must manage **supply chain security** (Art. 21 NIS2, § 30 BSIG); they pass requirements on to suppliers through contracts. So NIS2 affects Kurpfalz Sanitär **indirectly** as a supplier.

**3. Wrongly sent e-mail (3 points)**

- It is a **personal data breach** (1 point); the employee should have reported it at once — internal reporting channel to IT security / data protection officer.
- Assess the risk to the installers and **notify the data protection supervisory authority** without undue delay and **within 72 hours** of becoming aware (Art. 33), unless the breach is unlikely to result in a risk; the clock started when the company became aware — at the latest the next morning (1 point).
- Further steps (1 point, any two): ask the recipient to delete the e-mail and confirm; document the breach; inform installers if there is a high risk (Art. 34), e.g. risk of targeted phishing; lessons learned: training, DLP filter, restricted exports.

**4. ISO 31000 (5 points)**

- Process (2 points): scope, context and criteria → risk assessment (identification, analysis, evaluation) → risk treatment; throughout: communication and consultation, monitoring and review, recording and reporting. 1 point for the core steps in the right order, 1 point for the accompanying activities or the role of criteria and the risk register.
- Two risks rated (1.5 points each: 0.5 rating with justification, 0.5 level, 0.5 treatment), examples:
  - Data leak via e-mail or exports: likely (4) × major (4) = 16 (high) → reduce: DLP filter, export rights, training.
  - Outage of the externally hosted platform: possible (3) × major (4) = 12 (high) → reduce and share: SLA and underpinning contract with the hosting provider (session 6), redundancy; insurance for the financial loss.
  - Ransomware on ERP and platform: possible (3) × severe (5) = 15 → reduce: backups, MFA, segmentation.
  - Losing the hospital group's contract because security requirements are not met: possible (3) × serious (3) = 9 → reduce: implement the required measures, e.g. along ISO/IEC 27001 (session 8).
- Ratings may differ; points require a consistent justification.

**5. Three lines (3 points, 1 per line)**

- First line: service owner of the order platform and sales management own the risks, implement controls (access rights, export restrictions, reporting of incidents), maintain the risk register entries.
- Second line: data protection officer, information security officer or compliance function define requirements, monitor (e.g. check that breaches are reported), train staff, challenge risk ratings.
- Third line: internal audit (or, without an internal audit function, an external auditor) audits the compliance and risk management processes and reports to the executive and supervisory board.

**6. Ethics (2 points)**

- Concerns (1 point, any two): **accuracy** — is the payment score correct, are past delays caused by Kurpfalz Sanitär's own invoicing errors? **Fairness / accessibility** — small installers are excluded from same-day delivery without explanation; no way to object; **privacy** — profiling of sole traders. For sole traders, a decision based solely on automated processing with significant effects may also be restricted by the GDPR (Art. 22); accept as an extra argument.
- Proposal (1 point): human review of borderline cases, transparency about the criteria, a chance to explain or object, regular checks of the algorithm's accuracy; or use the score only as a warning for the sales team instead of an automatic refusal.
:::

## Optional Challenge: One Control, Many Rules {.optional}

A GRC team wants to build **one control catalogue** instead of separate lists for each law. For each control, name the **requirements** it helps to meet (GDPR, NIS2/BSIG, DORA — articles or sections where you know them) and the **ITIL practice** (sessions 5–6) or role that would typically operate it.

| Control | Requirements | ITIL practice / role |
|---|---|---|
| Multi-factor authentication for remote and admin access | | |
| Incident classification with reporting deadlines | | |
| Deletion concept with fixed retention periods | | |
| Security clauses and audit rights in contracts with IT suppliers | | |
| Regular restore tests of backups | | |

Then explain in three or four sentences why an integrated control catalogue is cheaper and more effective than separate compliance projects per law.

::: answer lines=12
:::

::: solution
- **MFA:** GDPR Art. 32 (security of processing); NIS2 Art. 21 / § 30 BSIG (MFA is named explicitly); DORA ICT risk management (access control). Practice: information security management; identity and access management in IT operations.
- **Incident classification with deadlines:** GDPR Art. 33/34 (72 h); NIS2 Art. 23 / § 32 BSIG (24 h, 72 h, one month); DORA incident management and reporting pillar. Practice: incident management (major incident procedure), service desk; roles: information security officer, data protection officer.
- **Deletion concept:** GDPR Art. 5 (storage limitation, data minimisation) and Art. 17 (right to erasure); retention duties from commercial and tax law set minimum periods. Practice: information security management / data management; role: data protection officer with application owners.
- **Supplier security clauses:** NIS2 Art. 21 / § 30 BSIG (supply chain security); DORA ICT third-party risk (contract requirements, register of information); GDPR Art. 28 (processor agreements). Practice: supplier management (session 15), relationship management.
- **Restore tests:** NIS2 Art. 21 / § 30 BSIG (business continuity, backup management); DORA resilience testing; GDPR Art. 32 (ability to restore availability). Practice: service continuity management, infrastructure and platform management (session 8).

Integrated catalogue: one control is designed, operated and tested once and the evidence is reused for several laws and audits; fewer duplicate projects and audit requests; the risk register and the control catalogue give management one overall picture; changes in a law only require updating the mapping, not a new project. This is the core idea of integrated GRC (Racz et al., 2010).
:::

## References {.references}

- Directive (EU) 2022/2555 of the European Parliament and of the Council of 14 December 2022 on measures for a high common level of cybersecurity across the Union (NIS 2 Directive). (2022). *Official Journal of the European Union*, L 333, 80–152. http://data.europa.eu/eli/dir/2022/2555/oj
- Gesetz zur Umsetzung der NIS-2-Richtlinie und zur Regelung wesentlicher Grundzüge des Informationssicherheitsmanagements in der Bundesverwaltung vom 2. Dezember 2025. (2025). *Bundesgesetzblatt*, 2025 I, Nr. 301.
- ISO. (2018). *Risk management — Guidelines* (ISO Standard No. 31000:2018). International Organization for Standardization.
- Mason, R. O. (1986). Four ethical issues of the information age. *MIS Quarterly, 10*(1), 5–12.
- Racz, N., Weippl, E., & Seufert, A. (2010). A frame of reference for research of integrated governance, risk and compliance (GRC). In B. De Decker & I. Schaumüller-Bichl (Eds.), *Communications and multimedia security* (Lecture Notes in Computer Science, Vol. 6109, pp. 106–117). Springer. https://doi.org/10.1007/978-3-642-13241-4_11
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1–88. http://data.europa.eu/eli/reg/2016/679/oj
- Regulation (EU) 2022/2554 of the European Parliament and of the Council of 14 December 2022 on digital operational resilience for the financial sector (DORA). (2022). *Official Journal of the European Union*, L 333, 1–79. http://data.europa.eu/eli/reg/2022/2554/oj
- The Institute of Internal Auditors. (2020). *The IIA's three lines model: An update of the three lines of defense*. The Institute of Internal Auditors.
- Tiemeyer, E. (Ed.). (2023). *Handbuch IT-Management: Konzepte, Methoden, Lösungen und Arbeitshilfen für die Praxis* (8th ed.). Hanser.

The tasks are training material, not legal advice.
