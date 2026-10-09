---
course: IT Management and EAM
session: 3
title: IT Governance and IT Organisation
subtitle: Governance vs. management · decision rights · COBIT and ISO/IEC 38500 · the CIO · organising IT
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# IT Governance and IT Organisation {.title}

::: notes
Time plan for today (3 h): recap 10 min · governance vs. management 25 min · decision rights and archetypes 25 min · break 10 min · COBIT and ISO/IEC 38500 25 min · CIO and IT organisation 30 min · case exercise 40 min · wrap-up 5 min · ~10 min buffer.
:::

---

# Today's Agenda

1. Recap: alignment at Kurpfalz Sanitär AG
2. IT governance vs. IT management
3. Who decides what? Decision rights and governance archetypes
4. Frameworks: ISO/IEC 38500 and COBIT
5. The role of the CIO
6. Organising IT: centralised, decentralised, federated · plan–build–run
7. Case exercise: design an IT organisation

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:10 Governance vs. management (input) · 0:35 Decision rights and archetypes (input + discussion) · 1:00 Break · 1:10 ISO/IEC 38500 and COBIT (input) · 1:35 CIO and IT organisation (input) · 2:05 Case exercise (groups) · 2:45 Wrap-up · ~10 min buffer.
:::

---

# Recap: Who Approves IT Projects?

At Kurpfalz Sanitär AG, the CFO alone approved IT projects, and IT and sales hardly talked.

- Who **should** decide on the new platform investment?
- Who decides which **technology standards** apply?
- Who is **accountable** if the platform fails?

::: notes
Bridge from session 2: the alignment problems were partly governance problems — unclear decision rights. Collect answers; most students will say "a committee" — ask who exactly sits on it and who has the final word.
:::

---

# Governance vs. Management {.section}

Who directs — and who executes?

---

# IT Governance: Definition

::: callout
IT governance means "specifying the decision rights and accountability framework to encourage desirable behavior in the use of IT."
:::

- Governance is about **who decides** and **who is accountable** — not about the decisions themselves
- It is part of **corporate governance**: the board is responsible for IT too

::: source
Weill and Ross (2004, p. 8).
:::

::: notes
Weill and Ross's definition is the most cited one. Check the page number against the library copy. Link to session 1: Nolan and McFarlan argued that boards must take responsibility for IT. Emphasise the distinction: governance designs the decision system; management makes and executes the decisions within it.
:::

---

# Evaluate, Direct, Monitor

::: columns
**Governance (governing body)**

- **Evaluate** current and future use of IT
- **Direct** the preparation and implementation of plans and policies
- **Monitor** conformance and performance
|||
**Management**

- Plans, builds, runs and monitors IT activities
- Within the direction set by the governing body
- Reports back to the governing body
:::

::: callout
Governance sets the direction; management steers the daily work within that direction.
:::

::: source
Based on ISO/IEC (2024) and ISACA (2018).
:::

::: notes
The evaluate–direct–monitor (EDM) model comes from ISO/IEC 38500 and is used as the governance domain in COBIT. In COBIT 2019 the management side is split into four domains: Align, Plan and Organise (APO); Build, Acquire and Implement (BAI); Deliver, Service and Support (DSS); Monitor, Evaluate and Assess (MEA).
:::

---

# Decision Rights {.section}

Who decides what?

---

# Five Key IT Decisions

| Decision | Question |
|---|---|
| IT principles | What is the role of IT in the business? |
| IT architecture | Which technical standards and integration requirements apply? |
| IT infrastructure | Which shared IT services are provided centrally? |
| Business application needs | Which applications does the business need? |
| IT investment and prioritisation | How much do we spend, and on what? |

::: source
Based on Weill and Ross (2004).
:::

::: notes
The five decisions are interrelated: principles drive architecture, architecture drives infrastructure, application needs build on infrastructure, and investment ties them together. Ask: at your company, who decides on new business applications?
:::

---

# Governance Archetypes

| Archetype | Who decides? |
|---|---|
| Business monarchy | Senior business executives (e.g. executive board) |
| IT monarchy | IT executives (CIO and IT leaders) |
| Feudal | Business unit heads, each for their own unit |
| Federal | Corporate centre and business units together |
| IT duopoly | IT executives together with one business group |
| Anarchy | Individual users or small groups |

::: source
Based on Weill and Ross (2004).
:::

::: notes
Weill and Ross found that firms use different archetypes for different decisions — e.g. IT monarchy for architecture, duopoly for application needs. They also report that top-performing firms tend to centralise decisions when they aim at profit and decentralise more when they aim at growth. Ask: which archetype fits Kurpfalz Sanitär (CFO decides investments → business monarchy)?
:::

---

# Governance Mechanisms {.optional}

| Type | Examples |
|---|---|
| Decision-making structures | IT steering committee, architecture board, executive committee |
| Alignment processes | IT investment approval, portfolio management, service level agreements, chargeback |
| Communication approaches | CIO office, announcements, IT portals, web of relationship managers |

::: source
Based on Weill and Ross (2004).
:::

::: notes
Self-study. Decision rights only work if mechanisms put them into practice. Portfolio management and chargeback are the topic of session 4 (IT controlling).
:::

---

# Frameworks {.section}

ISO/IEC 38500 and COBIT

---

# ISO/IEC 38500 and COBIT

::: cards
### ISO/IEC 38500
International standard for the **governance of IT for the organisation**. Short and principle-based; addressed to the **governing body** (board). Current edition: 2024.

### COBIT 2019
Framework by ISACA for the **governance and management of enterprise information and technology**. Detailed: **40 governance and management objectives** in five domains, with processes, roles and metrics.
:::

::: callout
ISO/IEC 38500 says **what** the board should do; COBIT gives **detailed guidance on how** governance and management can be implemented.
:::

::: source
ISO/IEC (2024); ISACA (2018).
:::

::: notes
COBIT 2019 domains: EDM (5 objectives), APO (14), BAI (11), DSS (6), MEA (4) = 40. COBIT is widely used by auditors (ISACA is the association of IT auditors) — students will meet it in audits and in the IT risk and compliance session (7). Before teaching (first run 2028), check whether a newer COBIT version has been released (see STATUS open items).
:::

---

# COBIT in a Nutshell {.optional}

- **Governance domain:** Evaluate, Direct and Monitor (EDM)
- **Management domains:**
  - Align, Plan and Organise (APO) — e.g. managed strategy, managed budget and costs
  - Build, Acquire and Implement (BAI) — e.g. managed projects, managed changes
  - Deliver, Service and Support (DSS) — e.g. managed operations, managed incidents
  - Monitor, Evaluate and Assess (MEA) — e.g. managed performance and conformance monitoring
- A **design factor** approach tailors the governance system to the enterprise

::: source
ISACA (2018).
:::

::: notes
Self-study. The domain names reflect the lifecycle plan → build → run → monitor that we see again in the organisation of the IT department.
:::

---

# The CIO and the IT Organisation {.section}

Roles and structures

---

# The Role of the CIO

- The **Chief Information Officer** leads IT and is responsible for the IT strategy, IT governance and IT operations
- Typical tensions:
  - **Cost manager** vs. **innovation driver**
  - Reporting to the **CFO** vs. the **CEO**
- Newer roles share the field: **CDO** (chief digital or data officer), **CISO** (security)

::: callout
Where the CIO reports — and whether the CIO sits on the executive board — signals how strategically a company sees IT.
:::

::: source
Based on Krcmar (2015) and Urbach and Ahlemann (2019).
:::

::: notes
Ask students: to whom does the CIO report in their company? Typical answers vary: CFO in cost-focused firms, CEO or executive board member in firms where IT is part of the product. The CDO role often emerged when the CIO was seen as running "only" internal IT.
:::

---

# Centralised, Decentralised, Federated

| | Centralised | Decentralised | Federated |
|---|---|---|---|
| IT decisions and resources | In one corporate IT unit | In the business units | Shared: central infrastructure and standards, local applications |
| Strengths | Economies of scale, standards, control | Closeness to the business, speed, flexibility | Combines scale and business proximity |
| Weaknesses | Distance from business needs, slow | Duplication, inconsistent systems, higher costs | Complex coordination, unclear boundaries |

::: source
Based on Brown and Magill (1994) and Weill and Ross (2004).
:::

::: notes
Brown and Magill studied which factors (e.g. corporate strategy, structure, IT maturity) lead firms towards centralised, decentralised or shared (hybrid) IS structures. Most large companies today are federated. Link to archetypes: centralised ≈ IT monarchy for many decisions; federated ≈ federal archetype.
:::

---

# Plan–Build–Run

::: layers
- Plan: IT strategy, enterprise architecture, demand management, portfolio planning
- Build: Projects and solution development, integration, testing, release
- Run: Operations, service desk, incident and problem management, infrastructure
:::

- Organising IT along the **lifecycle** of IT services instead of along technologies
- Often combined with **business relationship managers** who link IT and business units

::: source
Own illustration based on Krcmar (2015) and Tiemeyer (2023).
:::

::: notes
Plan–build–run structures replaced the older technology-oriented structure (e.g. "mainframe", "network", "SAP team"). Critique: hand-overs between build and run create friction — one motivation for DevOps and product-oriented IT, which Urbach and Ahlemann discuss as the IT organisation of the future. Verify the chapter references in Krcmar and Tiemeyer before using them in written material.
:::

---

# Case Exercise: Design an IT Organisation {.exercise}

**Case:** *Rhein-Neckar Mobil Group* runs three business units: bus and rail services, a car-sharing app, and vehicle maintenance. Each unit has built its own IT; there are three ERP systems, two data centres and no common security standard. The new CEO wants a joint mobility app by 2028.

**Tasks:**
1. Which **organisation form** (centralised, decentralised, federated) do you recommend? Justify.
2. For each of the **five key IT decisions**, name the **archetype** you would choose.
3. Which **governance bodies** (committees, boards) would you set up?
4. Where should the **CIO** report, and should there also be a CDO?

::: notes
Groups of 4–5, about 30 min + 10 min discussion. Expected answers (several defensible): 1 federated — central infrastructure, security and architecture standards, joint app platform; business-unit-specific applications stay close to the units. 2 IT principles: business monarchy or duopoly · architecture: IT monarchy · infrastructure: IT monarchy · application needs: federal or duopoly · investment: business monarchy with CIO input. 3 IT steering committee (CEO, unit heads, CIO), architecture board, security board. 4 CIO reports to the CEO, given the strategic role of the app; a CDO is optional — if created, clarify the boundary with the CIO to avoid two competing digital agendas.
:::

---

# Key Takeaways

- **IT governance** defines decision rights and accountability; **IT management** makes and executes decisions
- Governance follows the cycle **evaluate – direct – monitor**
- Five key IT decisions can be assigned to different **archetypes**, from business monarchy to anarchy
- **ISO/IEC 38500** sets principles for the board; **COBIT** gives detailed governance and management objectives
- IT can be organised **centralised, decentralised or federated**, and along **plan–build–run**

---

# Next Session: IT Controlling

- IT cost and performance accounting
- IT budgeting and chargeback
- IT project portfolio management
- Business cases, IT KPIs and the IT balanced scorecard

::: callout
**Preparation:** find out how your training company finances IT — central budget, or do business units pay for IT services?
:::

---

# References {.references}

- Brown, C. V., & Magill, S. L. (1994). Alignment of the IS functions with the enterprise: Toward a model of antecedents. *MIS Quarterly, 18*(4), 371–403. https://doi.org/10.2307/249521
- ISACA. (2018). *COBIT 2019 framework: Introduction and methodology*. ISACA.
- ISO/IEC. (2024). *Information technology — Governance of IT for the organization* (ISO/IEC Standard No. 38500:2024). International Organization for Standardization.
- Krcmar, H. (2015). *Informationsmanagement* (6th ed.). Springer Gabler. https://doi.org/10.1007/978-3-662-45863-1
- Tiemeyer, E. (Ed.). (2023). *Handbuch IT-Management: Konzepte, Methoden, Lösungen und Arbeitshilfen für die Praxis* (8th ed.). Hanser.
- Urbach, N., & Ahlemann, F. (2019). *IT management in the digital age: A roadmap for the IT department of the future*. Springer. https://doi.org/10.1007/978-3-319-96187-3
- Weill, P., & Ross, J. W. (2004). *IT governance: How top performers manage IT decision rights for superior results*. Harvard Business School Press.
