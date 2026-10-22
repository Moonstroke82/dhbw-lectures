---
course: IT Management and EAM
session: 3
title: IT Governance and IT Organisation
subtitle: Practice tasks on governance vs. management, decision rights, COBIT and ISO/IEC 38500, and IT organisation forms
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 3: the difference between IT governance and IT management, the evaluate–direct–monitor cycle, the five key IT decisions and governance archetypes of Weill and Ross (2004), the frameworks ISO/IEC 38500 and COBIT 2019, the role of the CIO, and the organisation of IT. The last core task is in the style of an exam question.

## Governance or Management?

Decide whether each activity is **IT governance** or **IT management**. For governance activities, say whether the governing body **evaluates**, **directs** or **monitors**. For management activities, name the COBIT 2019 management domain (APO, BAI, DSS, MEA).

- a) The supervisory board approves a policy that all customer data stays in the EU
- b) The IT operations team restores a failed database
- c) The board reviews an annual report on IT risks and compliance
- d) A project team tests and rolls out a new HR application
- e) The board assesses whether the current use of IT supports the growth strategy
- f) The IT department sets up the annual IT budget and cost plan
- g) Internal audit checks whether access rights are reviewed as required
- h) The service desk handles 300 user requests per day

::: answer lines=8
:::

::: hint
Governance decides **who decides** and sets direction; management **plans, builds, runs and monitors** within that direction. COBIT's management domains follow the life cycle: Align, Plan and Organise (APO) · Build, Acquire and Implement (BAI) · Deliver, Service and Support (DSS) · Monitor, Evaluate and Assess (MEA).
:::

::: solution
- a) Governance, **direct** (a policy set by the governing body).
- b) Management, **DSS** (managed operations, incidents).
- c) Governance, **monitor**.
- d) Management, **BAI** (projects, solution build, changes).
- e) Governance, **evaluate**.
- f) Management, **APO** (managed budget and costs).
- g) Management, **MEA** (monitoring of conformance). Students who argue that audit reports to the board and therefore supports governance (monitor) have a point; the audit work itself is in MEA.
- h) Management, **DSS** (service requests).
:::

## Evaluate, Direct, Monitor in Practice

The executive board of a hospital group wants to use **generative AI** to write discharge letters. Describe for each of the three governance tasks of ISO/IEC 38500 one concrete activity of the board in this situation.

::: answer lines=6
:::

::: solution
- **Evaluate:** assess benefits (time saved for doctors), risks (wrong medical content, data protection, liability) and the current and future use of AI in the group; ask management for a proposal and a risk assessment.
- **Direct:** set a policy (e.g. AI may draft letters, but a doctor must check and sign each letter; patient data only in approved systems), assign responsibility and approve budget for a pilot.
- **Monitor:** require regular reports on error rates, time saved, data protection incidents and compliance with the policy; adjust the direction if needed.

Marking: one activity per task that is clearly a board activity, not an operational management task such as "configure the AI tool".
:::

## Decision Rights and Archetypes

For each situation, name the **key IT decision** (IT principles, IT architecture, IT infrastructure, business application needs, IT investment and prioritisation) and the **governance archetype** (business monarchy, IT monarchy, feudal, federal, IT duopoly, anarchy).

1. The CIO and the enterprise architects decide that all databases must run on PostgreSQL.
2. Each country subsidiary chooses its own CRM system.
3. The executive board fixes the IT budget for next year without involving IT.
4. The CIO and the head of sales decide together which features the sales app gets.
5. Employees use any cloud storage service they like for project files.
6. Group management and the heads of all business units jointly decide that "IT is a shared service for the whole group".

::: answer lines=8
:::

::: solution
1. IT architecture · **IT monarchy**
2. Business application needs · **feudal**
3. IT investment and prioritisation · **business monarchy**
4. Business application needs · **IT duopoly**
5. Business application needs (or IT infrastructure, if seen as storage infrastructure) · **anarchy**
6. IT principles · **federal**

Marking: one point per line; half a point each for decision and archetype.
:::

## ISO/IEC 38500 and COBIT: True or False?

Decide whether each statement about ISO/IEC 38500 (ISO/IEC, 2024) and COBIT 2019 (ISACA, 2018) is true or false. Correct the false statements.

1. ISO/IEC 38500 is addressed mainly to the governing body of an organisation.
2. COBIT 2019 contains 40 governance and management objectives.
3. COBIT is a standard published by ISO.
4. ISO/IEC 38500 describes detailed processes, roles and metrics for IT operations.
5. In COBIT 2019, the governance domain is called Evaluate, Direct and Monitor (EDM).
6. Using COBIT makes ISO/IEC 38500 unnecessary, because both say the same.

::: answer lines=8
:::

::: solution
1. True.
2. True (EDM 5, APO 14, BAI 11, DSS 6, MEA 4).
3. False: COBIT is a framework published by **ISACA**, an association, not an ISO standard.
4. False: ISO/IEC 38500 is short and **principle-based**; detailed objectives, processes and metrics are in COBIT.
5. True.
6. False: they complement each other. ISO/IEC 38500 says **what** the board should do; COBIT gives detailed guidance on **how** governance and management can be implemented.
:::

## Choosing an Organisation Form

Recommend an IT organisation form (centralised, decentralised or federated; Brown & Magill, 1994) for each company and justify it with two arguments.

- a) *Hohenlohe Holding*: owns a food producer, a chemicals trader and a real estate company. The businesses share nothing except the owner.
- b) *Pfalz Direktbank*: one bank, one product range, strict regulatory requirements.
- c) *Schwarzwald Medizintechnik*: five plants in four countries with the same products; each plant has its own production systems, but the group wants one ERP and one security standard.

Then assign these teams of the bank to **plan**, **build** or **run** (Krcmar, 2015): enterprise architecture, service desk, app development team, demand management, data centre operations, test and release team.

::: answer lines=10
:::

::: solution
- a) **Decentralised**: no synergies between the businesses, different requirements; business proximity matters more than scale. A small central function for minimum security standards is a good addition.
- b) **Centralised**: one business, economies of scale, standards and control; regulators require tight control of IT risks.
- c) **Federated**: central ERP, security and architecture standards (scale, control), local production systems close to the plants.

Plan–build–run: enterprise architecture **plan** · service desk **run** · app development team **build** · demand management **plan** · data centre operations **run** · test and release team **build**.
:::

## Exam-Style Task: Klinikverbund Oberrhein

*Klinikverbund Oberrhein* is a group of four hospitals that merged two years ago. Each hospital still has its own IT team, its own hospital information system and its own data centre. Each hospital director decides on IT purchases. A ransomware attack on one hospital last year stopped admissions for three days. The board wants a joint patient portal and a common security level. There is no CIO; the IT teams report to the commercial directors of the hospitals.

1. Distinguish IT governance from IT management. (2 points)
2. Recommend an IT organisation form for the group and justify it with two advantages and one disadvantage you need to manage. (4 points)
3. Which governance archetype would you choose for **IT architecture**, **IT investment** and **business application needs**? Justify briefly. (3 points)
4. Where should a group CIO report? (1 point)
5. Propose one governance body: who sits on it and what does it decide? (2 points)

::: answer lines=18
:::

::: solution
Marking guide (12 points):

**1. Governance vs. management (2 points)**

- Governance: specifies decision rights and accountability; evaluates, directs and monitors; done by the governing body (1 point).
- Management: plans, builds, runs and monitors IT within the direction set by governance (1 point).

**2. Organisation form (4 points)**

- **Federated** or **centralised** (1 point). Federated is the expected answer: central infrastructure, security and architecture; hospital-specific applications close to the clinics. Centralised is accepted with a convincing argument (one group, similar processes, security risk).
- Two advantages linked to the case (1 point each): common security level after the ransomware attack, economies of scale (one data centre), basis for the joint patient portal, consistent data.
- One disadvantage to manage (1 point): distance from local clinical needs, slower decisions, coordination effort, resistance of hospital directors.

**3. Archetypes (3 points, 1 each)**

- IT architecture: **IT monarchy** (group CIO and architects set standards, including security).
- IT investment: **business monarchy** (board) with CIO input, or **federal** (board and hospital directors together).
- Business application needs: **federal** or **IT duopoly** (CIO with clinical and administrative leaders).

**4. Reporting line (1 point)**

- To the **board** (CEO or chief executive of the group), given the strategic importance of security and the patient portal; not to a single hospital's commercial director.

**5. Governance body (2 points)**

- e.g. **IT steering committee**: board member, hospital directors, medical director, CIO, data protection officer; decides on IT priorities, budget and the portal programme. Or a **security board**: CIO, CISO, medical representatives; decides on security standards and monitors their implementation.
- 1 point for members, 1 point for decisions.
:::

## Optional Challenge: CIO and CDO {.optional}

A retail company has a CIO who reports to the CFO. The new CEO wants to appoint a Chief Digital Officer (CDO) for e-commerce and data. Describe two risks of having both roles and two ways to manage them.

::: answer lines=6
:::

::: solution
Risks: two competing digital agendas and budgets; unclear responsibility for platforms, data and security; the CIO is pushed into a pure "run" and cost role, which demotivates IT staff; duplicate teams and shadow IT in the CDO's area.

Ways to manage: clear split of responsibilities (e.g. CDO for digital products and customer experience, CIO for platforms, infrastructure and security), joint governance body and a shared roadmap, both report to the CEO, shared KPIs; alternatively merge the roles after a transition phase.
:::

## References {.references}

- Brown, C. V., & Magill, S. L. (1994). Alignment of the IS functions with the enterprise: Toward a model of antecedents. *MIS Quarterly, 18*(4), 371–403. https://doi.org/10.2307/249521
- ISACA. (2018). *COBIT 2019 framework: Introduction and methodology*. ISACA.
- ISO/IEC. (2024). *Information technology — Governance of IT for the organization* (ISO/IEC Standard No. 38500:2024). International Organization for Standardization.
- Krcmar, H. (2015). *Informationsmanagement* (6th ed.). Springer Gabler. https://doi.org/10.1007/978-3-662-45863-1
- Weill, P., & Ross, J. W. (2004). *IT governance: How top performers manage IT decision rights for superior results*. Harvard Business School Press.
