---
course: IT Management and EAM
session: 11
title: Collecting and Modelling Architecture Information
subtitle: Why and what to collect · meta-models · document analysis, interviews, workshops and tool imports · data quality and maintenance of EA repositories
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# Collecting and Modelling Architecture Information {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · why and what to collect 15 min · meta-models and granularity 20 min · mini exercise "type, element, attribute or relationship?" 10 min · break 10 min · sources and methods 25 min · mini exercise "which method?" 10 min · data quality and maintenance 15 min · case exercise data collection plan 45 min · wrap-up 5 min · ~15 min buffer.
Session 10 ended with the architecture team of Rhein-Neckar Mobil Group starting with transparency: it has no list of applications. Today answers the question "how do we get one — and how do we keep it correct?". This covers the methodological competence of the module (collect information about IT and business processes with suitable methods and model it) and the personal and social competence (working with business units and IT specialists).
Source note for the lecturer: Hanschke (2023) treats the maintenance concept in section 8.3.1, modelling guidelines in 8.3.2, maintenance of the EAM data base in 8.4.1, stakeholder analysis in 7.2 and the right granularity in 5.4.1 (section numbers checked against the table of contents of the 4th edition; check the text in the library copy before quoting). The survey figures come from Roth et al. (2013). The TOGAF Standard describes the architecture repository and the enterprise metamodel in the core concepts document (sections 3.11 and 3.12 of C220); the slides describe the ideas in own words only.
:::

---

# Today's Agenda

1. Recap: where does your company document its applications?
2. Why and what to collect: purpose before data
3. Meta-models: element types, relationships, attributes
4. Sources and methods: documents, interviews, workshops, tool imports
5. Data quality and maintenance of the EA repository
6. Case exercise: plan an EA data collection for Rhein-Neckar Mobil Group

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Why and what to collect (input + discussion) · 0:25 Meta-models and granularity (input) · 0:45 Mini exercise "type, element, attribute or relationship?" (pairs) · 0:55 Break · 1:05 Sources and methods (input) · 1:30 Mini exercise "which method?" (pairs) · 1:40 Data quality and maintenance (input) · 1:55 Case exercise (groups + plenary) · 2:40 Wrap-up · ~15 min buffer.
If the session runs long: "The documentation challenge" and "Meta-models in frameworks and tools" are optional and move to self-study; "The collection as a cycle" can be shown briefly right before the case, since the case tasks follow its steps. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: Where Are Your Applications Documented?

You were asked to find out where your training company documents its applications.

- **Where** is the list: Excel, wiki, CMDB, EAM tool — or nowhere?
- **Who** keeps it up to date, and how often?
- **Would you trust it** for a decision, e.g. which systems to switch off after an acquisition?

::: notes
Pairs for 3 min, then collect on the board: place of documentation · who maintains it · trust (thumbs up, sideways, down). Typical answers: an Excel list from a past project, the CMDB of the ITSM tool (mostly servers, not business applications), a licence list in purchasing, a wiki page per department, an EAM tool such as LeanIX, ADOIT or Alfabet in larger companies. Most lists have no clear owner and are "roughly right". Keep the board: today's three questions follow from it — what should be in such a list (meta-model), where do the data come from (sources and methods), and how do we keep them right (data quality and maintenance).
:::

---

# Why and What to Collect {.section}

Purpose before data

---

# Collect for a Purpose

::: columns
**Start from questions**

- Which **stakeholders** need EA information, and for which **decisions**? (session 10)
- Which **questions** must the repository answer?
- Which **element types, relationships and attributes** follow from these questions?
- Only then: which **sources** and **methods**?
|||
**Typical anti-patterns**

- "Let's document everything first" — the project never ends
- Detail nobody uses, e.g. every server port
- Data collected once for a project, then left to age
- No owner for the data after the collection
:::

::: callout
Collect **as little as possible and as much as needed** to answer the questions of the stakeholders.
:::

::: source
Own wording based on Hanschke (2023) and Keller (2017).
:::

::: notes
Hanschke (2023) recommends starting every EAM step with a stakeholder analysis (section 7.2) and building the EA data base in stages, each stage driven by concrete usage scenarios. Keller (2017) makes the same point: the content of the repository follows from the questions it must answer. Example from session 10: the data protection officer asks "where are personal data?" → needed: applications, business objects with a flag "personal data", the relationship "application creates/reads business object", hosting location. A question nobody asks does not need data. Ask: what was the purpose of the list in your training company?
:::

---

# The Documentation Challenge {.optional}

A survey of **140 EA practitioners** on how they document their architecture:

| Finding | Share of respondents |
|---|---|
| Collect data by manual inspection of applications and databases | 76 % |
| Collect data in interviews with stakeholders | 68 % |
| Collect data in modelling workshops | 53 % |
| Name the huge effort of data collection as a challenge | 55 % |
| Name bad data quality as a challenge | 55 % |
| Have some form of automated update of their EA tool | 19 % |

::: source
Roth et al. (2013); rounded.
:::

::: notes
Roth et al. (2013) surveyed 140 practitioners (Wirtschaftsinformatik conference 2013). Further findings: most respondents had no defined process for data collection (ad hoc collection), and time-consuming collection, difficult data acquisition and insufficient actuality of the models were the most frequent documentation problems. Of those who automated, most used file imports (Excel, CSV, XML) rather than live interfaces. The survey is from 2013 and the authors note a possible bias towards automation in the sample; tools have improved since, but the basic picture — collection is mainly manual, costly and fragile — is still what students will meet in practice. Message: EA data collection is a management task, not a side job.
:::

---

# Meta-Models {.section}

Element types, relationships and attributes

---

# What a Meta-Model Is

::: callout
A **meta-model** is the "model of the model": it defines which **element types**, **relationship types** and **attributes** may be used to describe the architecture — and which rules apply to them.
:::

| Level | Example |
|---|---|
| **Meta-model** | Element types *Application* and *Technology component*; relationship type *runs on*; attribute *life cycle status* |
| **Model** (the repository content) | "Car-sharing app runs on the container platform of the cloud provider; status: active" |
| **Reality** | The software and the cloud platform as they actually exist |

::: source
Own wording based on Lankhorst (2017) and The Open Group (2022).
:::

::: notes
Analogy for students who took Data Management: the meta-model is like the ER schema of a database (entity types, relationship types, attributes); the repository content is like the rows in the tables. A repository without a meta-model is like a database without a schema — everyone enters different things. TOGAF, ArchiMate and EAM tools each bring their own meta-model (optional slide after the mini exercise). Lankhorst (2017) stresses that a well-defined meta-model is the precondition for analysing models, e.g. for impact analysis.
:::

---

# A Lean EA Meta-Model

![A lean EA meta-model in four bands: in the business band, an organisation unit performs a business process, which realises a business capability; in the data band, a business object; the organisation unit is owner of the application; in the application band, the application supports the business process, creates or reads business objects and is connected to other applications through an interface that transfers business objects; in the technology band, the application runs on a technology component](img/eam-metamodel.png){width=80%}

::: source
Own illustration based on Hanschke (2023) and The Open Group (2022).
:::

::: notes
This is deliberately small — seven element types and a handful of relationships are enough to answer most first questions: which applications support which processes, who owns them, which data they hold and send, where they run. Hanschke (2023) describes a much larger best-practice enterprise architecture (section 5.4 and 5.6) and recommends starting with a subset. The application is the centre (red) because most EAM initiatives start with the application landscape. Walk through one question with the figure: "Which processes are affected if the cloud platform fails?" → technology component → runs on → application → supports → process. That is impact analysis on the meta-model level. Projects, contracts, risks or capabilities' strategic importance can be added in later stages.
:::

---

# Attributes: The Application Fact Sheet

| Attribute group | Examples for the element type *Application* |
|---|---|
| **Identification** | Unique ID, name, short description, aliases |
| **Responsibility** | Business owner, IT owner (technical responsibility) |
| **Life cycle** | Planned · in development · active · phase-out · retired, with dates |
| **Business value** | Supported processes and capabilities, number of users, criticality |
| **Technical state** | Technology stack, hosting, standard software or own development, vendor |
| **Cost and contracts** | Running cost per year, licence and support contracts |
| **Risk and compliance** | Protection requirements (session 8), personal data yes/no |

::: source
Own compilation based on Hanschke (2023) and Keller (2017).
:::

::: notes
EAM tools often call the record of one element a "fact sheet" (session 18). Each attribute needs a definition and a permitted value list (e.g. criticality: low/medium/high/very high — taken from the BIA of session 8, not invented again). Ask for each attribute: which question does it answer, and who can give a reliable value? Example: "running cost" sounds simple, but only IT controlling (session 4) can give it — and only if the cost accounting uses the same application names. Two owners per application is common practice: the business owner decides about functions and demand, the IT owner about operations and technology.
:::

---

# Granularity: What Is One Application?

::: columns
**The problem**

- Is SAP S/4HANA one application — or finance, purchasing and sales as three?
- Is the car-sharing app one application — or 25 microservices?
- Is Excel with a fare calculation macro an application?
|||
**Modelling guidelines decide**

- Model at the level at which **decisions** are made: owner, budget, life cycle
- **As coarse as possible, as fine as necessary** for the questions
- Write the rules down and apply them everywhere — otherwise lists are not comparable
:::

::: source
Own wording based on Hanschke (2023).
:::

::: notes
Hanschke (2023) discusses the right granularity (section 5.4.1) and recommends documenting modelling guidelines as part of the EAM rule set (section 8.3.2). Typical rules: an application is a software system that is perceived as a unit by the business, has an owner and its own life cycle; large standard packages are split into modules only if the modules have different owners or life cycles; microservices are documented by the development team in its own tools, not in the EA repository; end-user tools (Excel macros, Access databases) are recorded only if they are business-critical. Without such rules one unit reports 3 applications and another 40 for the same kind of landscape — and the "180 applications" of Rhein-Neckar Mobil Group are not a number anyone can compare.
:::

---

# Mini Exercise: Type, Element, Attribute or Relationship? {.exercise}

Classify each item from the EA repository of *Rhein-Neckar Mobil Group* as **element type**, **element**, **attribute (value)** or **relationship**.

::: columns
1. Application
2. The car-sharing app
3. Life cycle status "phase-out"
4. "The fare back-end runs on the servers in data centre 2"
|||
5. Interface
6. Process "sell ticket on board"
7. Criticality "very high"
8. "The head of car sharing is the business owner of the car-sharing app"
:::

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 element type (meta-model level); 2 element (an instance of *Application*); 3 attribute value of an application; 4 relationship (*runs on*) between two elements; 5 element type; 6 element (instance of *Business process*); 7 attribute value; 8 can be modelled as an attribute "business owner" of the application (a person's name) or as a relationship between the application and an organisation unit or role — good discussion point. Lesson: the meta-model decides; modelling the owner as a relationship to a role or unit survives reorganisations and staff changes better than a name in a text field, and it avoids storing more personal data than needed.
:::

---

# Meta-Models in Frameworks and Tools {.optional}

| Where | What it offers |
|---|---|
| **TOGAF Standard** | An enterprise metamodel as part of its content framework, with core entities across business, data, application and technology, to be tailored to the enterprise |
| **ArchiMate** (session 17) | A modelling language with a fixed meta-model and a standard notation for elements and relationships |
| **EAM tools** (session 18) | A predefined, configurable meta-model with fact sheet types, attributes and reports |
| **Own meta-model** | Often derived from one of the above and tailored to the questions of the stakeholders |

::: source
Own summary based on The Open Group (2022) and Lankhorst (2017).
:::

::: notes
Self-study. The TOGAF core concepts describe the content framework and the enterprise metamodel and explicitly expect tailoring. Lankhorst (2017) explains why ArchiMate uses one integrated meta-model across layers: only then can relationships between business, application and technology be analysed. In practice most companies take the default meta-model of their EAM tool and switch off what they do not need — "lean" again. Warning sign: a meta-model with 60 element types and nobody to maintain them.
:::

---

# Sources and Methods {.section}

Documents, people and systems

---

# Three Kinds of Sources

::: cards
### Documents
Application lists, contracts and licence lists, operating handbooks, project documents, records of processing (GDPR), BIA results, network diagrams, organisation charts.
### People
Business and IT owners, process owners, developers and operators, purchasing and controlling — reached through **interviews**, **questionnaires** and **workshops**.
### Systems
CMDB and ITSM tool, software asset and licence management, cloud provider inventories, project portfolio tool, integration platform and API gateway, network monitoring.
:::

::: callout
Start with **what already exists** — then ask people to **confirm and complete**, instead of asking them to start from a blank page.
:::

::: source
Own compilation based on Hanschke (2023) and Roth et al. (2013).
:::

::: notes
Many Part A instruments have already produced EA data: the GDPR records of processing (session 7), the BIA with its resources and dependencies (session 8), the service catalogue and CMDB (sessions 5–6), the project portfolio and cost accounting (session 4). An EA team that reuses them saves effort and earns goodwill, because units are not asked the same questions twice. Pre-filled lists also give better answers: people correct a wrong entry more easily than they recall a complete list.
:::

---

# Document Analysis

::: columns
**Strengths**

- Cheap and fast; no one's time needed
- Gives a first structure and a list of names to work with
- Good for formal facts: contracts, licences, costs, dates
|||
**Weaknesses**

- Documents are often **outdated** or contradict each other
- Different **granularity** and names in every document
- Shows what was planned or bought — not always what runs
:::

::: callout
Treat results from documents as **hypotheses** to be confirmed by the owners.
:::

::: source
Own wording based on Hanschke (2023) and Keller (2017).
:::

::: notes
Practical tips: keep a source column for every entry ("from licence list, 2026-03"), so that later conflicts can be traced; create a first draft of the application list from two or three documents and mark contradictions. Typical traps: a licence list contains software that was bought but never deployed; a project document describes the target design, not what was finally built. Link to research methods (bachelor thesis): document analysis is a recognised qualitative method; the same rules of source criticism apply.
:::

---

# Interviews and Questionnaires

::: columns
**Interviews**

- **Semi-structured**: an interview guide with fixed topics, room for follow-up
- Good for **relationships, context and problems**: who uses what, why, what hurts
- Prepare with the pre-filled list; send the summary back for **confirmation**
- Costly: one owner at a time
|||
**Questionnaires**

- Reach **many owners** with the same questions
- Good for **attributes** of known elements: users, life cycle, cost, criticality
- Need clear definitions and value lists, otherwise answers differ
- Low response rates without management backing
:::

::: source
Own wording based on Hanschke (2023) and Roth et al. (2013).
:::

::: notes
An interview with an application owner typically takes 60 to 90 minutes; plan it with the pre-filled fact sheet. Good interview questions are concrete: "Which other systems send data to your application, and which data?" rather than "Describe your interfaces." Questionnaires (often a form in the EAM tool or a spreadsheet) work for attributes but rarely for relationships. Typical combination: questionnaire to all owners for attributes, interviews with the owners of the critical applications for interfaces and problems. Roth et al. (2013) found interviews in about two thirds and questionnaires in about a third of the organisations surveyed.
:::

---

# Workshops

- Bring **several roles** together: business owner, IT owner, process owner, developers, operations
- Good for **cross-unit relationships**: process-to-application maps, interface maps, capability maps (session 12)
- **Conflicts and gaps** become visible at once — and can be resolved together
- Build **shared understanding** and acceptance of the results
- Need preparation, a moderator and a visual method: whiteboard, sticky notes, a prepared draft map

::: callout
A workshop works best when the participants **correct a prepared draft** instead of drawing from scratch.
:::

::: source
Own wording based on Hanschke (2023) and Roth et al. (2013).
:::

::: notes
Roth et al. (2013) report modelling workshops in about half of the organisations. Workshop formats that work: walk through one business process from start to end and ask at each step "which application, which data, which interface?"; or start with a printed landscape map and let participants add arrows. Moderation tips: one person moderates, one documents; agree the modelling rules (granularity) at the start; take photos and send a clean version within a few days. Workshops are expensive (many people at once), so they are used for the important processes, not for all 180 applications.
:::

---

# Tool Imports and Automated Collection

| System | What it can deliver | Limits |
|---|---|---|
| CMDB / ITSM tool | Servers, installed software, services, incidents | Technical view; names differ from business names |
| Software asset and licence management | Installed and licensed products, versions | Says nothing about business use |
| Cloud provider inventories | Cloud resources, regions, cost | Resources must be mapped to applications |
| Project portfolio tool | Planned changes to applications | Often only project names, not affected elements |
| Integration platform, API gateway | Real interfaces and data flows | Covers only interfaces that run through it |

::: callout
Imports are **up to date and cheap to repeat**, but deliver a **technical view**: someone must map IDs and names to the meta-model.
:::

::: source
Own compilation based on Farwick et al. (2011) and Roth et al. (2013).
:::

::: notes
Farwick et al. (2011) analysed the requirements for automated maintenance of EA models: the models become large, so manual maintenance is slow and costly; automation needs reliable source systems, a mapping to the EA meta-model and rules for conflicts between sources. In practice, the main effort is reconciliation: the CMDB knows "srv-dc2-047" and "S4P", the business knows "SAP finance". A good start is one mapping table (CMDB ID ↔ application ID) maintained by the EA team. Automation in general: Roth et al. (2013) found few organisations with automated updates, mostly via file imports; research proposed monitoring tools, service bus data and project portfolio tools as sources. Business elements (capabilities, processes, owners) still need people — automation helps for technical facts, not for meaning and responsibility. Link to session 6: a well-maintained CMDB from change enablement is the best partner of the EA repository; each has its own level of detail.
:::

---

# Comparing the Methods

| Method | Best for | Effort | Main risk |
|---|---|---|---|
| Document analysis | First draft, formal facts | Low | Outdated, inconsistent |
| Interviews | Relationships, context, problems | High per element | Subjective, depends on memory |
| Questionnaires | Attributes of many known elements | Low per element | Low response, misunderstood fields |
| Workshops | Cross-unit maps, conflicts | High, many people | Dominant voices, poor preparation |
| Tool imports | Technical facts, frequent updates | High once, low later | Technical view, mapping needed |

::: callout
No method is enough on its own: **combine** them and **cross-check** the results.
:::

::: source
Own comparison based on Hanschke (2023), Roth et al. (2013) and Farwick et al. (2011).
:::

::: notes
Exam point: for a given information need, choose a suitable method and justify it — e.g. interfaces of the critical ticketing applications: workshop with business and IT owners, checked against the integration platform; costs: import from IT controlling; life cycle status: questionnaire to owners. Triangulation (comparing two sources) is the best quality check during collection: if the CMDB and the owner disagree about where an application runs, one of them is wrong.
:::

---

# Collecting Is Working with People

::: columns
**Win the owners**

- Explain **what's in it for them**: views they need, fewer duplicate requests
- Ask for **little**, pre-fill what you can
- Give results **back** quickly
- Get **management backing** for the collection
|||
**Respect rules and people**

- Store only the **personal data** needed (GDPR, session 7): roles rather than names where possible
- Involve the **works council** if the repository could show who uses which system
- Protect **sensitive** content: vulnerabilities, critical dependencies
- Report problems **without blaming** the people who name them
:::

::: source
Own wording based on Hanschke (2023) and Ahlemann et al. (2012).
:::

::: notes
This slide covers the personal and social competence of the module. Owners have other jobs; a collection that feels like an audit gets defensive or minimal answers. Ahlemann et al. (2012) stress that EAM needs support from top management and visible benefits for the business to be accepted. In Germany, the works council has a co-determination right when technical systems are suitable to monitor the behaviour or performance of employees (Works Constitution Act, section 87(1) no. 6); an EAM tool with user names and usage figures may fall under this — involve the works council early rather than late. Security: a complete map of critical systems and their weaknesses is valuable to attackers too — restrict access (accessibility and access security, next section).
:::

---

# Mini Exercise: Which Method? {.exercise}

The architecture team of *Rhein-Neckar Mobil Group* needs the following information. Which **source and method** would you use first — and how would you **check** the result?

1. Running cost per year of each application
2. All interfaces of the fare back-end
3. Which applications the vehicle maintenance unit uses
4. Life cycle status and business owner of about 180 applications
5. Which cloud resources the car-sharing unit runs
6. Which applications support the process "handle customer complaints" across all three units

::: notes
Pairs, 5 min + 5 min discussion. Expected answers (several defensible): 1 import/document from IT controlling (cost accounting, session 4), check against contracts in purchasing; 2 interview or small workshop with the IT owner and developers of the fare back-end, check against the integration platform or network monitoring and the BIA dependencies (session 8); 3 interview with the head of maintenance and the unit's IT contact, check against licence list and CMDB; 4 questionnaire to the owners with a pre-filled list from the licence list and CMDB, check by sampling and by comparing with the CMDB; 5 import from the cloud provider's inventory, mapped to applications in a short interview with the car-sharing IT; 6 workshop with the process owners and service desk staff of all three units — cross-unit relationships are a workshop topic. Lesson: start with existing data, use people to confirm and to supply relationships.
:::

---

# Data Quality and Maintenance {.section}

Keeping the EA repository trustworthy

---

# Data Quality of EA Repositories

| Category | Dimensions | EA example |
|---|---|---|
| **Intrinsic** | Accuracy, believability, objectivity, reputation | The recorded owner is really responsible; the hosting location is correct |
| **Contextual** | Value-added, relevancy, timeliness, completeness, appropriate amount | All applications of all units are recorded; status updated after go-live |
| **Representational** | Interpretability, ease of understanding, consistency, conciseness | Same granularity and naming rules in all units |
| **Accessibility** | Accessibility, access security | Owners can find and update their data; vulnerabilities only visible to security |

::: callout
Data quality is **fitness for use**: data are good if they are good enough for the decisions they support.
:::

::: source
Own examples; categories and dimensions based on Wang and Strong (1996).
:::

::: notes
Wang and Strong (1996) derived these four categories from a survey of data consumers: quality is judged by the user, not only by the correctness of a value — hence "beyond accuracy". Typical EA quality problems: duplicates (the same application under three names), orphans (an application with no supported process, an interface with no data), outdated life cycle status, empty mandatory attributes, inconsistent granularity. Roth et al. (2013) found bad data quality named as a challenge by more than half of the practitioners. Link to session 9: a repository nobody trusts is not used — a quality problem in Garvin's user-based sense.
:::

---

# Keeping the Repository Alive: The Maintenance Concept

::: columns
**Who and when**

- A **data owner** for each element type or attribute, e.g. the application owner for "life cycle", controlling for "cost"
- **Event triggers**: project quality gates, go-live, change enablement, new contract
- **Regular reviews**, e.g. every six months per owner
|||
**How and how well**

- Simple **forms** in the tool; **imports** where systems know better
- **Quality checks**: mandatory fields, orphans, duplicates
- **Quality KPIs**, e.g. share of applications with an owner, share reviewed in the last six months
- Report KPIs to the CIO; escalate if owners do not respond
:::

::: source
Own wording based on Hanschke (2023) and Ahlemann et al. (2012).
:::

::: notes
Hanschke (2023) calls this a maintenance concept ("Pflegekonzept", section 8.3.1) and treats the maintenance of the EAM data base as one of the EAM processes (section 8.4.1). The strongest trigger is embedding: a project cannot pass its quality gate, or a change cannot be closed, until the repository is updated (link to session 10: EAM embedded in the project life cycle; session 6: change enablement). Ahlemann et al. (2012) emphasise this integration into existing processes. Quality KPIs are themselves a small IT balanced scorecard topic (session 4). Ask: which trigger would work in your training company?
:::

---

# The Collection as a Cycle

![Seven steps of an EA data collection: 1 purpose and questions, 2 meta-model and granularity, 3 sources and data owners, 4 collect, existing data first, 5 consolidate and check quality, 6 publish views and use them, 7 maintain continuously; a feedback arrow leads from step 7 back to step 1 with the label new questions and changes in the landscape](img/eam-collection-steps.png){width=95%}

- Steps 1–2 decide **what** to collect, steps 3–5 **how**, steps 6–7 make sure the data are **used and kept current**
- Each new stakeholder question starts a new, smaller round — the repository grows in **stages**

::: source
Own illustration based on Hanschke (2023) and Roth et al. (2013).
:::

::: notes
This figure is the structure of today's case exercise. Hanschke (2023) recommends introducing EAM in stages ("Ausbaustufen", section 7.3), each with a design, a pilot and anchoring in the organisation. Step 6 is often forgotten: if no one uses the views, no one has a reason to maintain the data, and quality decays — the cycle breaks. Roth et al. (2013) found that most organisations had no defined process for data collection; this figure is such a process in its simplest form.
:::

---

# Case Exercise: Plan an EA Data Collection {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–10): 3,200 employees, €410 million turnover, three units. The new two-person **architecture team** must deliver, within six months, an application landscape that supports the **joint mobility app** and the decision on **one cloud ERP**. The CIO guesses about **180 applications**.

- **Group IT:** a CMDB for the servers in its two data centres; the BIA of the on-board ticketing service (session 8)
- **Bus and rail:** an Excel list of applications kept by one colleague who retires next year
- **Car sharing:** a wiki page per microservice; all systems run at a cloud provider
- **Purchasing:** a list of about 240 software contracts; **data protection officer:** records of processing activities
- The **works council** asks whether the EA tool will show which employees use which application

::: notes
Read the case together (2 min). Hints if asked: vehicle maintenance has no list at all; the business units fear extra work and say "IT should know this"; the CIO will support the collection in the management meeting if the team explains the benefit; the figures (240 contracts, six months) are own example figures. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. Name the **purpose** of the collection: three **questions** the repository must answer, and the stakeholders behind them.
2. Sketch a **lean meta-model**: element types, relationships and five attributes for *Application*. State one **granularity rule**.
3. For each existing **source**: what can it deliver, and what is its main weakness? Which **methods** close the gaps?
4. How do you win the **owners** — and how do you answer the **works council**?
5. Define two **quality checks** or KPIs and two **triggers** that keep the data current.

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 E.g. CEO/app project: which applications and interfaces hold customer, ticket and payment data across the units? CIO/CFO: which applications depend on the three ERPs, and what do they cost? DPO/CISO: where are personal data, which applications are critical? Also accepted: which applications are near the end of their life.
2 Element types: application, interface, business object, business process (or capability), organisation unit, technology component (hosting); relationships as in the lean meta-model. Application attributes: ID, name, business owner, IT owner, life cycle status, criticality (from BIA), hosting, cost, personal data yes/no, ERP dependency. Granularity rule: e.g. "an application has its own owner and life cycle; microservices of the car-sharing platform are grouped into one application per product"; ERP modules only if they have different owners.
3 CMDB: technical facts on servers in Group IT data centres; misses cloud systems and business names → mapping workshop with Group IT. Excel list of bus and rail: good first draft; knowledge risk (retirement) → interview the colleague early and transfer ownership. Wiki of car sharing: detailed but too fine-grained → group into applications with the car-sharing IT, import cloud inventory. Contract list: shows what is bought, incl. SaaS; not what is used → confirm with owners. Records of processing: applications with personal data and processors → reuse for data flags. BIA: dependencies and criticality of the ticketing service → reuse. Gaps: vehicle maintenance (no list) → interview; interfaces across units → workshop for the mobility-app processes; attributes of all applications → questionnaire with pre-filled fact sheets.
4 Owners: management backing by the CIO, explain the benefit (views for their own decisions, fewer duplicate requests), pre-fill and ask little, give results back. Works council: inform early; the repository stores applications and roles, not individual usage; if user numbers are needed, only aggregated; agree access rules, possibly a works agreement.
5 Checks/KPIs: share of applications with business and IT owner; share reviewed in the last six months; number of orphans (applications without a process) and duplicates; share of mandatory fields filled. Triggers: go-live and decommissioning at project quality gates; change enablement; new or terminated contracts in purchasing; half-yearly review by the owners.
:::

---

# Key Takeaways

- Collect EA information **for a purpose**: stakeholder questions decide what goes into the repository — as little as possible, as much as needed
- A **meta-model** defines element types, relationships and attributes; **modelling guidelines** fix the granularity
- **Documents, people and systems** are the sources; document analysis, interviews, questionnaires, workshops and tool imports each have strengths — **combine and cross-check** them
- **Data quality** is fitness for use; a **maintenance concept** with owners, triggers and quality KPIs keeps the repository alive

---

# Next Session: Business Model Transformation and Business–IT Alignment

- Digital business models
- Business capability maps and value streams
- EA as an enabler of transformation

::: callout
**Preparation:** list about ten things your training company **must be able to do** to earn its money (e.g. "manage customer contracts") — without naming any department or system.
:::

::: notes
The preparation task is a first, intuitive capability list for session 12. The "without departments or systems" rule already hints at the difference between capabilities, organisation units and applications — the capability map will become the business layer of today's meta-model.
:::

---

# References {.references}

- Ahlemann, F., Stettiner, E., Messerschmidt, M., & Legner, C. (Eds.). (2012). *Strategic enterprise architecture management: Challenges, best practices, and future developments*. Springer. https://doi.org/10.1007/978-3-642-24223-6
- Farwick, M., Agreiter, B., Breu, R., Ryll, S., Voges, K., & Hanschke, I. (2011). Requirements for automated enterprise architecture model maintenance: A requirements analysis based on a literature review and an exploratory survey. In *Proceedings of the 13th International Conference on Enterprise Information Systems (ICEIS 2011)* (Vol. 4, pp. 325–337). SciTePress. https://doi.org/10.5220/0003429203250337
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Lankhorst, M. (2017). *Enterprise architecture at work: Modelling, communication and analysis* (4th ed.). Springer. https://doi.org/10.1007/978-3-662-53933-0
- Roth, S., Hauder, M., Farwick, M., Breu, R., & Matthes, F. (2013). Enterprise architecture documentation: Current practices and future directions. In *Proceedings of the 11th International Conference on Wirtschaftsinformatik (WI 2013)* (pp. 911–925). https://aisel.aisnet.org/wi2013/58
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.
- Wang, R. Y., & Strong, D. M. (1996). Beyond accuracy: What data quality means to data consumers. *Journal of Management Information Systems, 12*(4), 5–33.

TOGAF® and ArchiMate® are registered trademarks of The Open Group. Diagrams in this deck are own illustrations. Standards are described in own words.
