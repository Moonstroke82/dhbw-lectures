---
course: IT Management and EAM
session: 16
title: EAM Frameworks I: TOGAF
subtitle: Purpose of frameworks · the TOGAF Architecture Development Method (ADM) · content framework · architecture governance
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# EAM Frameworks I: TOGAF {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · purpose of frameworks, TOGAF at a glance 15 min · the ADM 25 min · mini exercise "which phase?" 10 min · break 10 min · content framework 15 min · mini exercise "deliverable, artefact or building block?" 10 min · architecture governance 20 min · case exercise "walk a case through the ADM" 45 min · wrap-up 5 min · ~15 min buffer.
Sessions 10–15 taught the content of EAM: domains, repository, capabilities, landscape planning, integration, sourcing. Today puts these pieces into one method and one governance model, using the most widely known EAM framework. This covers the module content "EAM frameworks, e.g. TOGAF" and the methodological competence of familiarising oneself with current frameworks of EAM. Session 13 already showed Phases E and F as an optional slide; today they are only placed in the cycle, and the time goes into Preliminary, A–D, G and H.
Source note for the lecturer: the TOGAF Standard, 10th Edition (April 2022) is cited in three Van Haren volumes: Introduction and core concepts (2022a), Architecture development method (2022b; contains the documents Architecture Development Method, ADM Techniques and Applying the ADM) and Content, capability, and governance (2022c; contains Architecture Content and Enterprise Architecture Capability and Governance with the chapters Architecture Governance, Architecture Board, Architecture Contracts and Architecture Compliance). Tables of contents checked against the publisher's sample pages. A "2025 update" of these volumes (with Technical Corrigendum 1) has been published by Van Haren; re-check before the first run in 2028. TOGAF is copyrighted: phase names and work-product names are used as labels; all descriptions are own words and the cycle and governance figures are own illustrations. Hanschke (2023) treats EAM frameworks in section 5.2 and IT and EA governance with roles and decision bodies in chapter 8 (checked against the table of contents). All RNM examples are own examples.
:::

---

# Today's Agenda

1. Recap: how does your company decide on architecture?
2. Why EAM frameworks — and what TOGAF is
3. The Architecture Development Method (ADM)
4. The content framework: deliverables, artefacts, building blocks
5. Architecture governance: principles, board, compliance
6. Case exercise: walk a Rhein-Neckar Mobil Group initiative through the ADM

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Frameworks and TOGAF overview (input) · 0:25 ADM (input) · 0:50 Mini exercise "which phase?" (pairs) · 1:00 Break · 1:10 Content framework (input) · 1:25 Mini exercise "deliverable, artefact or building block?" (pairs) · 1:35 Architecture governance (input) · 1:55 Case exercise (groups + plenary) · 2:40 Wrap-up · ~15 min buffer.
If the session runs long: "ADM Techniques", "The Enterprise Continuum" and "TOGAF in Practice" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: How Does Your Company Decide on Architecture?

You were asked to find out how your training company **decides on architecture** — and to bring one **architecture decision** and **who** took it.

- Is there an **architecture board**, written **architecture principles** or a **framework** such as TOGAF?
- Who took your example decision: a **board**, the **CIO**, a **project**, a **vendor**?
- Was the decision **checked** later — and what happens if a project does not follow it?

::: notes
Pairs for 3 min, then collect on the board in three columns: decision · who decided · how it is enforced. Typical findings: "we use TOGAF" is rare as a whole; more common are an architecture board or design authority that meets every few weeks, a short list of principles ("cloud first", "SAP standard before own development"), a technology radar, and many decisions taken inside projects or by vendors. Enforcement is often weak: "the architect is asked for an opinion". Keep the board: today's three parts map onto it — the method (how architecture work is done), the content (what is produced) and governance (who decides and how it is enforced). Link to session 3: architecture was one of the five IT decision areas of Weill and Ross.
:::

---

# Why Frameworks? {.section}

Method, content and governance for architecture work

---

# What Is an EAM Framework?

::: callout
An **EAM framework** gives an enterprise a **reusable structure** for architecture work: what to describe, how to proceed, which results to produce and who decides.
:::

| Kind of framework | Main question | Examples |
|---|---|---|
| **Method framework** | How do we develop and change the architecture? | TOGAF ADM |
| **Classification framework** | Which descriptions do we need, from which perspective? | Zachman |
| **Modelling language** | How do we draw it consistently? | ArchiMate |
| **Practitioner approach** | How do we run EAM pragmatically? | Hanschke, Keller, tool vendors |

::: source
Own compilation based on Keller (2017), Hanschke (2023), Zachman (1987) and The Open Group (2022a).
:::

::: notes
The four kinds overlap; TOGAF is mainly a method framework but also contains a content framework and a governance part. Zachman (1987) is a classification scheme (session 10, optional slide) and ArchiMate a modelling language — both are session 17. The German practitioner books of the module literature describe EAM as a set of instruments and usage scenarios rather than as one fixed method; Hanschke (2023, section 5.2) discusses EAM frameworks as part of the EAM foundations. Exam point: be able to say what kind of question a framework answers — a method does not tell you how to draw a diagram, a modelling language does not tell you who decides.
:::

---

# Benefits and Limits of Frameworks

::: columns
**Benefits**

- **Common language**: terms such as baseline, target, gap, building block
- **Proven method**: steps and results do not have to be invented
- **Completeness**: checklists remind the team of stakeholders and domains
- **Comparability** of work across units and projects
- **Training and certification** create a shared skill base
|||
**Limits**

- **Large and generic**: must be **tailored** to the enterprise
- Risk of **documents for their own sake**
- Says little about **politics**, budgets and people
- Adoption "by the book" is **rare** in practice
- Version and licence questions; the standard evolves
:::

::: callout
A framework is a **toolbox**, not a recipe: take what answers your stakeholders' questions.
:::

::: source
Own wording based on The Open Group (2022a), Hanschke (2023) and Kotusev (2019).
:::

::: notes
The TOGAF Standard itself expects to be adapted: the Preliminary phase includes tailoring the framework to the enterprise. Kotusev (2019) studied the EA artefacts actually used in 27 organisations and argues that practice differs considerably from the textbook view of EA — optional slide later. Link to session 11: "lean" EAM — collect only what a stakeholder question needs. Ask: which of the benefits would help the two-person architecture team of Rhein-Neckar Mobil Group most? (Usually common language with the business and a governance model that gives the team a mandate.)
:::

---

# TOGAF at a Glance

- **TOGAF Standard** of **The Open Group**, a vendor-neutral industry consortium; current: **10th Edition** (2022)
- Free to use internally; widely known through **certification**
- **10th Edition** is modular: a stable **fundamental content** plus **series guides** for specific topics, e.g. business capabilities and value streams (session 12)

::: cards
### ADM
A method for developing and changing the architecture in phases
### Content framework
Which results architecture work produces and how they relate
### Capability and governance
How to set up the architecture function and steer projects
:::

::: source
Own wording based on The Open Group (2022a).
:::

::: notes
The fundamental content consists of documents on the introduction and core concepts, the ADM, ADM techniques, applying the ADM, architecture content, and enterprise architecture capability and governance; the series guides add guidance that changes faster (The Open Group, 2022a, chapter 2 on the documentation set). TOGAF goes back to 1995 and was originally based on a US Department of Defense framework (TAFIM); version 9 (2009) and 9.2 (2018) were widely used before the 10th Edition. Certification is common in consulting and large enterprises; job ads for enterprise architects often ask for it. The three cards are the structure of today's session.
:::

---

# The Architecture Development Method {.section}

A cycle from vision to governed change

---

# The ADM Cycle

![The TOGAF ADM as an own illustration: the preliminary phase in front of the cycle prepares the organisation, sets principles and tailors the framework. The cycle runs clockwise through eight phases around requirements management in the centre: A architecture vision (scope, stakeholders, vision, approval), B business architecture (capabilities, processes, organisation), C information systems architectures (data and applications), D technology architecture (platforms, infrastructure), E opportunities and solutions (work packages, transitions), F migration planning (roadmap, sequence, budget), G implementation governance (compliance reviews, contracts), H architecture change management (monitor changes, new cycle?). Phases A to D are vision and architecture definition, E and F planning the transformation, G and H governing implementation and change. Every phase exchanges requirements with requirements management](img/togaf-adm-cycle.png){width=64%}

::: source
Own illustration based on The Open Group (2022b).
:::

::: notes
Walk around the cycle once, linking each phase to a session: B — capability maps and value streams (session 12); C — data and applications, repository and integration (sessions 10, 11, 14); D — technology, cloud and hosting (sessions 10, 15); E and F — work packages, transition architectures, roadmap (session 13); G — today; H — today. The ADM is a cycle because architecture is never finished: Phase H decides when a new cycle starts. Requirements management sits in the centre because requirements change in every phase and must be managed throughout. The figure is our own drawing; the standard's own figure is copyrighted.
:::

---

# Preliminary Phase and Phase A

| Phase | Purpose in own words | Typical results |
|---|---|---|
| **Preliminary** | Prepare the enterprise for architecture work: scope of the architecture function, roles, **principles**, governance, **tailoring** of the framework, tools | Organisational model for EA, tailored framework, architecture principles |
| **A: Architecture vision** | Start one cycle: clarify the **trigger**, goals and constraints, **stakeholders** and their concerns, **scope**; sketch the target at a high level; get **approval** | Architecture vision, statement of architecture work, communications plan |

::: callout
Phase A ends with an **agreed mandate**: what will be architected, why, by whom, by when — before anyone draws detailed models.
:::

::: source
Own wording based on The Open Group (2022b).
:::

::: notes
The Preliminary phase is done once when the architecture function is set up and revisited when it changes — at RNM, the two-person team reporting to the CIO, the principles of session 13 and an architecture board would be its results. A cycle is started by a request for architecture work, e.g. from the board or a programme. In Phase A, stakeholder analysis is the key technique (session 10: stakeholders, concerns, views); business transformation readiness (can the organisation absorb the change?) and risks are assessed. The statement of architecture work is a kind of project charter for the architecture work, signed by the sponsor. Exam point: be able to say why Phase A comes before B–D — without scope and stakeholders, the architecture work has no limits and no customer.
:::

---

# Phases B, C and D: Defining the Architecture

| Phase | Domain | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **B: Business architecture** | Capabilities, value streams, processes, organisation | Capability "mobility account" needed, value stream "plan and take a trip" (session 12) |
| **C: Information systems architectures** | Data architecture and application architecture | One leading customer master; mobility app on the API platform (sessions 13–14) |
| **D: Technology architecture** | Platforms, infrastructure, hosting | Container platform in an EU cloud region; data centre 1 retired (session 15) |

- Each phase follows the same pattern: describe the **baseline**, describe the **target**, perform a **gap analysis**, propose **roadmap components**, check the **impact** on other domains, review with **stakeholders**

::: source
Own wording based on The Open Group (2022b); own examples.
:::

::: notes
The four domains of session 10 appear here as phases; TOGAF groups data and application as "information systems architectures" in one phase, and the order of data and application within Phase C can be chosen. The repeated pattern is the core idea to remember: baseline – target – gaps – roadmap components. Gap analysis is the technique of session 13 (new, replace, consolidate, retire, keep). The results of B–D are collected in an architecture definition document, and the requirements that projects must meet in an architecture requirements specification. Practical point: in many enterprises B–D are not done in full for every cycle; the team describes only what the initiative changes, reusing the repository (session 11) for the rest.
:::

---

# Phases E to H: From Plan to Governed Change

| Phase | Purpose in own words | Typical results |
|---|---|---|
| **E: Opportunities and solutions** | Group gaps into **work packages**, decide build or buy, define **transition architectures** (session 13) | Candidate roadmap, transitions |
| **F: Migration planning** | Sequence and fund the work packages with portfolio and budget (sessions 4, 13) | Architecture roadmap, implementation and migration plan |
| **G: Implementation governance** | Make sure projects **build what was architected**: architecture contracts, **compliance reviews** | Architecture contracts, compliance assessments |
| **H: Architecture change management** | Monitor business and technology changes; decide whether a change needs a **new cycle** | Change requests, new request for architecture work |

::: source
Own wording based on The Open Group (2022b).
:::

::: notes
E and F were covered in session 13 (optional slide) — only recall that the build-or-buy decisions of session 15 are taken here for each work package. Spend the time on G and H. Phase G: the architects do not build the solution; they guide and check the projects that do. Phase H: TOGAF distinguishes changes that can be handled by normal change management (simplification), changes that may need partial re-architecting (incremental) and changes that require a new pass through the ADM (re-architecting). Example: a new fare zone is a small change; a new law requiring real-time passenger data for all operators may need a new cycle. Link to session 6: change enablement for IT services vs. architecture change management for the architecture.
:::

---

# Using the ADM: Iteration, Scope and Requirements

::: columns
**Iterate and scope**

- The ADM is **iterative**: across the whole cycle and between phases, e.g. back from C to B
- Different **levels**: a long-term **strategic** architecture for the enterprise, **segment** architectures for a unit or programme, **capability** architectures for one change
- **Scope** each cycle by breadth, depth, time and domains
|||
**Manage requirements**

- Requirements arise and change in **every phase**
- **Requirements management** stores, prioritises and traces them
- Changed requirements are checked for their **impact** on the current phase and on earlier results
:::

::: callout
One enterprise runs **many ADM cycles** at different levels at the same time.
:::

::: source
Own wording based on The Open Group (2022b).
:::

::: notes
The volume "Applying the ADM" (contained in The Open Group, 2022b) describes iteration and how the ADM is used across the architecture landscape at different levels of detail. At RNM: a strategic architecture for the group (target landscape of session 13, revised yearly), a segment architecture for "customer and mobility" (the mobility app programme), and capability architectures for single changes such as the payment platform. Each runs its own cycle, and the strategic one sets the frame for the others. Requirements management is not a phase that runs once: think of it as the backlog of the architecture work, with traceability from stakeholder concern to architecture element. Ask: which level did the case exercise of session 13 work on? (Segment: customer management and customer service.)
:::

---

# Mini Exercise: Which Phase? {.exercise}

Assign each activity at *Rhein-Neckar Mobil Group* to a **phase of the ADM** (Preliminary, A–H or requirements management).

1. The CIO decides that the architecture team writes **principles** and that an **architecture board** meets monthly
2. The team lists **who is affected** by the mobility app and what each stakeholder worries about
3. Interfaces of the fare back-end are documented **as-is** and **to-be**; the missing event stream is noted
4. The work packages "customer master", "API platform" and "payment platform" are **sequenced** with the budget
5. The app project's design is **checked** against the API-first principle before go-live
6. A new **EU law** on multimodal travel information is analysed for its impact on the target
7. The district council wants **usage reports**; the request is recorded and traced to the affected phases

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 Preliminary (architecture capability, principles, governance). 2 Phase A (stakeholders and concerns; stakeholder analysis). 3 Phase C (application and data architecture: baseline, target, gap); accept D if the student argues about the integration platform as technology. 4 Phase F (migration planning; E grouped them, F sequences and funds). 5 Phase G (implementation governance, compliance review). 6 Phase H (architecture change management: is this a change that needs a new cycle?); accept "requirements management" as well, because it creates new requirements. 7 Requirements management (a new requirement during the cycle); it may lead back to A or B. Lesson: the phases are a structure for thinking, not a strict sequence of calendar months — several can run at the same time.
:::

---

# ADM Techniques {.optional}

| Technique | Used for | Session link |
|---|---|---|
| **Architecture principles** | Rules that guide all architecture decisions | 13, today |
| **Stakeholder management** | Finding stakeholders, concerns and suitable views | 10 |
| **Gap analysis** | Comparing baseline and target | 13 |
| **Migration planning techniques** | Sequencing work packages by value, cost, risk | 13 |
| **Business transformation readiness** | Can the organisation absorb the change? | 12 |
| **Risk management** | Risks of the transformation, before and after measures | 7 |
| **Architecture alternatives and trade-offs** | Comparing options transparently | 15 |

::: source
Own compilation based on The Open Group (2022b).
:::

::: notes
Self-study. The ADM Techniques document (contained in The Open Group, 2022b) also covers architecture patterns and interoperability requirements. Most of these techniques were already taught in earlier sessions without the TOGAF label — that is the point of the slide: TOGAF collects good practice, it does not invent a separate world. Exam point: name two techniques and the phase in which they are typically used (e.g. stakeholder management in A, gap analysis in B–D, migration planning in E and F).
:::

---

# The Content Framework {.section}

What architecture work produces

---

# Deliverables, Artefacts and Building Blocks

| Term | Meaning in own words | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **Deliverable** | A formally **agreed and signed-off** work product, often defined in a contract | Statement of architecture work for the mobility app; architecture roadmap |
| **Artefact** | A single **view** of the architecture: a **catalogue** (list), **matrix** (relationships) or **diagram** | Application catalogue; application–capability matrix; interface diagram |
| **Building block** | A **reusable component** of business, IT or architecture capability | "Customer identity service"; the chosen identity product |

::: callout
**Architecture building blocks** describe **what** is needed (requirements, capability); **solution building blocks** describe **how** it is realised (a product, a package, a service).
:::

::: source
Own wording based on The Open Group (2022c); own examples.
:::

::: notes
A deliverable usually contains several artefacts: the architecture definition document contains catalogues, matrices and diagrams for each domain. Artefacts are what an EAM tool generates from the repository (session 11: views; session 18: LeanIX reports). Building blocks: "customer identity service with single sign-on and consent management" is an architecture building block — vendor-neutral; "product X from vendor Y in the EU cloud" is a solution building block that fulfils it. The distinction matters for sourcing (session 15): the architecture defines the ABB, the tender chooses the SBB. Note the British spelling "artefact" in the slides; the standard uses "artifact".
:::

---

# The Architecture Repository

- TOGAF expects a **repository** that holds all architecture work products, structured by a **metamodel** (session 11)
- Typical areas, in own words:
  - the **metamodel** and the tailored framework
  - the **architecture landscape**: baseline, target and transition descriptions at strategic, segment and capability level
  - **standards** and **reference models** the enterprise has adopted
  - **requirements** and the **governance records**: decisions, contracts, compliance assessments, dispensations

::: callout
At Rhein-Neckar Mobil Group, the EA tool is the repository: one source for views, reviews and decisions.
:::

::: source
Own wording based on The Open Group (2022a, 2022c).
:::

::: notes
Session 11 introduced the repository and the meta-model from the data collection side; today adds what TOGAF puts into it beyond the landscape: standards, reference models and governance records. The core concepts document describes the repository and the enterprise metamodel (session 11: sections 3.11 and 3.12 of the core concepts); the Architecture Content document details the content framework and the repository. The component names differ slightly between TOGAF versions — check the library copy before quoting them. Practical point: governance records are the part most often missing — two years later nobody knows why the board allowed an exception.
:::

---

# The Enterprise Continuum {.optional}

- A way to **classify reusable assets** from **generic** to **specific**
- From **foundation** architectures (valid for almost any enterprise) via **common systems** and **industry** architectures to **organisation-specific** architectures
- The same idea applies to **solutions**: from generic products to the enterprise's own implementation
- Purpose: **reuse** instead of inventing — e.g. start from an industry reference model for public transport, then adapt it

::: source
Own wording based on The Open Group (2022c).
:::

::: notes
Self-study. Example: a generic capability reference model shipped with an EAM tool (foundation/common), an industry data model for public transport such as standard formats for timetable data (industry), and RNM's own capability map (organisation-specific). Link to session 12: the capability map was built by renaming a reference model into the company's language — that is moving along the continuum. Exam point: understand the direction "generic → specific" and the purpose "reuse".
:::

---

# Mini Exercise: Deliverable, Artefact or Building Block? {.exercise}

Classify each item from the architecture work at *Rhein-Neckar Mobil Group*. For building blocks, say whether it is an **architecture** or a **solution** building block.

1. A table listing all **applications** with owner, life cycle status and hosting
2. The signed **architecture roadmap** for the mobility programme
3. "A **payment service** for all units that supports cards, app wallets and refunds"
4. The **payment platform of provider P**, contracted for five years
5. A diagram showing which **applications** exchange **customer data**
6. The **statement of architecture work** for the on-demand bus pilot
7. A grid of **capabilities** against **applications** with ticks in the cells

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 artefact (catalogue). 2 deliverable (formally agreed, signed). 3 architecture building block (vendor-neutral, what is needed). 4 solution building block (concrete product and contract). 5 artefact (diagram; an interface or data-flow diagram). 6 deliverable (signed by the sponsor at the end of Phase A). 7 artefact (matrix). Lesson: deliverables are about agreement, artefacts about views, building blocks about reusable components; one deliverable contains many artefacts, and artefacts describe building blocks.
:::

---

# Architecture Governance {.section}

Who decides, and how decisions are enforced

---

# What Is Architecture Governance?

::: callout
**Architecture governance** is the way an enterprise **steers and controls** its architectures: it sets the rules, decides on proposals and exceptions, and **checks compliance** — with clear responsibilities and records.
:::

- Part of **IT governance** (session 3): architecture is one of the key IT decisions
- Main elements in TOGAF:
  - **architecture principles** and standards
  - an **architecture board** with a mandate
  - **architecture contracts** with projects and partners
  - **compliance reviews** and **dispensations**
  - a **record** of decisions in the repository

::: source
Own wording based on The Open Group (2022c) and Hanschke (2023).
:::

::: notes
TOGAF places architecture governance in a hierarchy of governance: corporate, technology/IT and architecture governance, and it emphasises characteristics such as discipline, transparency, independence, accountability, responsibility and fairness (The Open Group, 2022c, chapter on architecture governance; own summary). Hanschke (2023, chapter 8) describes IT and EA governance with roles, decision areas and bodies, and the EAM rule set. Link to session 3: COBIT and ISO/IEC 38500 govern IT as a whole; architecture governance is the part that keeps the landscape coherent. Link to session 10: EAM must be embedded in planning, projects and operations (Ahlemann et al., 2012) — governance is the mechanism.
:::

---

# Architecture Principles

| Part | Content | Example: "API first" at Rhein-Neckar Mobil Group |
|---|---|---|
| **Name** | Short and memorable | API first |
| **Statement** | The rule, clearly worded | New applications offer their functions and data via the group API platform |
| **Rationale** | Why the rule helps the business | Partners and the mobility app reuse functions; fewer point-to-point interfaces |
| **Implications** | What follows: costs, tasks, changes | Every project budgets for APIs; the platform needs an owner and SLAs; legacy systems get adapters |

- Good principles are **understandable**, **robust**, **complete**, **consistent** and **stable** — and few: typically 10–20

::: source
Own wording based on The Open Group (2022b) and Hanschke (2023); own example.
:::

::: notes
The ADM Techniques document recommends a format with name, statement, rationale and implications and lists the quality criteria shown on the slide (The Open Group, 2022b; own wording). Hanschke (2023, section 3.5.1) treats principles as part of the guard rails ("Leitplanken") of strategic IT planning (session 13). The implications are the part most often missing — and the part that makes a principle bite: "API first" costs money in every project. Principles can conflict ("cloud first" vs. offline operation of ticket devices, session 8); the board decides which principle wins in a case. The number 10–20 is a rule of thumb from practice, not a requirement of the standard.
:::

---

# The Architecture Board and Architecture Contracts

::: columns
**Architecture board**

- A small **cross-functional** body: CIO or chief architect, business and IT representatives
- Keeps architectures **consistent**, decides on **standards** and **reuse**
- Reviews projects, decides on **exceptions (dispensations)**, resolves **conflicts**
- Needs a **mandate** from top management — otherwise it only advises
|||
**Architecture contracts**

- Joint **agreements** between the architecture function and those who build or use a solution
- Define the **architecture to be delivered**, quality and standards, and how **compliance** is checked
- Examples: statement of architecture work with the sponsor; contract with an implementation partner
:::

::: source
Own wording based on The Open Group (2022c).
:::

::: notes
The Content, capability, and governance volume has separate chapters on the architecture board, architecture contracts and architecture compliance. At RNM: an architecture board chaired by the CIO with the two architects, the heads of IT operations and security, and a representative of each unit; it meets monthly and reports to the IT steering committee (session 3). The board must not become a bottleneck: lightweight reviews for small projects, full reviews only for projects with a large architecture impact. Contracts are particularly important with external partners (session 15): the sourcing contract can refer to the architecture contract (standards, interfaces via the integration platform, data location in the EU).
:::

---

# Compliance Reviews and Dispensations

![Own illustration of an architecture compliance review: a project solution design, for example the booking platform for on-demand buses, and the architecture principles, standards, target architecture and reference models are inputs to a compliance review with checklists by domain in which the level of conformance is assessed. The architecture board decides with four possible outcomes: approve and build under an architecture contract; approve with a dispensation, a time-limited exception with conditions that is logged; rework, that is change the design and review again; or change the architecture through a change request in Phase H. Every decision, dispensation and contract is recorded in the repository](img/togaf-governance-flow.png){width=80%}

::: source
Own illustration based on The Open Group (2022c); own example.
:::

::: notes
Reviews happen at defined points of the project life cycle, e.g. after the solution concept, before the vendor contract is signed, before go-live (session 10: embedding EAM in the project life cycle). A dispensation is a formal, documented and time-limited permission to deviate — e.g. the on-demand vendor stores data in a non-EU region for six months until its EU region is available, with a data protection review and a deadline. The fourth outcome matters: sometimes the project is right and the standard is outdated — then the architecture changes via Phase H. TOGAF provides checklists per domain for such reviews; own checklists derived from the principles are enough in practice.
:::

---

# Levels of Conformance

| Level | Meaning in own words |
|---|---|
| **Irrelevant** | The solution has nothing in common with the specification |
| **Consistent** | Some specified features are built as specified, some are missing, and extra features exist |
| **Compliant** | What is built follows the specification, but not everything specified is built; nothing extra |
| **Conformant** | Everything specified is built as specified, but there are extra features outside the specification |
| **Fully conformant** | Everything specified is built as specified, nothing extra |
| **Non-conformant** | Something specified is built **against** the specification |

::: source
Own wording based on The Open Group (2022c).
:::

::: notes
The levels make the review result precise: "compliant" in TOGAF does not mean "fully conformant" — a frequent exam trap. Example for the API-first principle and the on-demand booking platform: it offers the specified booking API but not the cancellation API, and no extra interfaces → compliant; it offers both and an extra direct database export for the district council → conformant; it offers both and nothing else → fully conformant; it bypasses the API platform with a direct interface to the payment provider → non-conformant: rework or dispensation. Do not ask students to memorise the exact wording; ask them to apply the levels to a case.
:::

---

# TOGAF in Practice {.optional}

- In practice, enterprises use **parts** of TOGAF: vocabulary, phases as a checklist, principles format, governance elements
- An empirical study of **27 organisations** found **24 types of artefacts** that are actually used — many of them not part of the classic textbook view
- The study questions the idea of EA as **layers** plus **as-is, to-be and roadmap**, and calls for a view based on what practitioners really use
- Practitioner literature recommends starting **lean** and embedding EAM into existing processes (sessions 10–11)

::: source
Own summary based on Kotusev (2019), Hanschke (2023) and Ahlemann et al. (2012).
:::

::: notes
Self-study. Kotusev (2019) is a critical voice in EA research; his case studies show EA practice organised around a set of artefacts used in decision processes rather than around complete layered models. This does not make TOGAF useless — it explains why "implementing TOGAF" as a whole rarely works and why tailoring is part of the standard itself. Exam point: argue strengths and limits of a framework with examples.
:::

---

# Case Exercise: An On-Demand Bus Service for Rhein-Neckar Mobil Group {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–15): 3,200 employees, €410 million turnover, about 180 applications; a two-person architecture team reports to the CIO.

- The board wants an **on-demand bus pilot** in two rural districts: 20 minibuses, **booked in the mobility app** or by phone, from 2028; the districts co-fund it and want **usage reports**
- Vendors offer an **on-demand platform** as SaaS: booking, routing, driver tablets
- The **dispatching system** (vendor support until 2031) does not know on-demand trips; **fares** come from the fare back-end, which is being replaced
- **Principles** exist (session 13); the **integration platform** is approved (sessions 14–15); the **works council** watches driver tracking

::: notes
Read the case together (2 min). Hints if asked: RNM is an essential entity under NIS2 (session 7); location data of passengers and drivers are personal data (GDPR); the mobility app depends on the customer master, the API platform and the payment platform (roadmap, session 13); there is no architecture board yet — the CIO decides architecture questions alone. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. **Preliminary and A:** what must be in place before the cycle starts? Name **three stakeholders** with one concern each and write a **two-sentence vision** with the **scope**.
2. **B, C, D:** for each phase, name one **baseline** element, one **target** element and the resulting **gap**.
3. **E and F:** define three **work packages**, decide **build or buy** for the platform, and name the **dependency** that sets the order.
4. **G:** list **four checks** for the compliance review of the vendor's solution. The vendor's data are stored outside the EU until next year: what can the board decide?
5. **H:** two changes happen after go-live. Which needs a **new ADM cycle**, and why?

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Changes for task 5 (give them when groups reach task 5): (a) the vendor releases a new version of its driver tablet app; (b) the state government decides that on-demand services will become part of regular public transport in all rural districts from 2030. Expected answers (several defensible):
1 Preliminary: the architecture function and its mandate, principles (exist), an architecture board or at least a defined decision path, tailoring (lean: only the deliverables needed), the repository as source. Stakeholders: board/CEO (pilot on time, cost), district councils (service level, usage reports, funding), drivers and works council (tablets, tracking, performance monitoring), passengers (easy booking, reliability, data protection), dispatching team (one view of all vehicles), data protection officer (location data), IT operations (SaaS integration). Vision e.g.: "From 2028, passengers in the two pilot districts can book a minibus in the mobility app or by phone and travel on one ticket with bus and rail. Scope: booking, dispatching of the minibuses, fares and payment, reporting to the districts; out of scope: the regular bus timetable and other districts." Result: statement of architecture work signed by the sponsor.
2 B: baseline — scheduled services only, no on-demand booking; target — capability "on-demand trip management" and value stream "book and take an on-demand trip" with phone and app channels; gap — new capability, new process for phone booking, new roles. C: baseline — dispatching system for scheduled services, fare back-end, app in planning; target — on-demand platform (booking, routing) integrated via the integration platform with the customer master, payment platform, fare logic and dispatching; reporting data for the districts; gap — new application, new interfaces, new data objects (trip request, vehicle position), data protection concept. D: baseline — own data centres, no driver tablets; target — SaaS in an EU region, driver tablets with mobile device management, mobile network coverage in rural areas; gap — tablets and MDM, network check, SaaS connectivity.
3 Work packages e.g.: WP1 on-demand platform (buy SaaS — commodity routing and booking market is mature; differentiation is the integrated offer in the app, not the routing algorithm), WP2 integration (APIs to customer master, payment, fares, dispatching via the integration platform), WP3 tablets and MDM for 20 minibuses, WP4 reporting for the districts, WP5 organisation (phone booking, driver training, works agreement). Dependency: app booking needs the customer master, API platform and payment platform of the mobility roadmap — the pilot may start with phone booking and the vendor's own app as a transition architecture.
4 Checks: data location and processor agreement (GDPR), security and NIS2 supply-chain requirements, API-first (integration only via the integration platform, no direct database access), one leading customer system (no second customer master in the vendor platform), SLA and availability matching the service hours, exit and data return (session 15), works council agreement on tracking data. Data outside the EU: options — rework (choose another vendor or wait), dispensation with conditions (time-limited until the EU region is available, data protection impact assessment, legal basis for transfer, pseudonymisation, deadline and review), or no go-live with real customer data until compliant. Accept a reasoned decision; a dispensation must be time-limited, documented and approved by the board, not by the project.
5 (a) New tablet app version: normal change management (simplification/incremental change) — check compatibility, no new cycle. (b) State decision: changes the business context and the scale — re-architecting change: new request for architecture work, new cycle starting with Phase A (vision for on-demand in all districts, new stakeholders, scale, sourcing). Also accept "requirements management records it first", if the student says it leads to a new cycle.
:::

---

# Key Takeaways

- **EAM frameworks** give architecture work a reusable structure — method, content and governance — and must be **tailored**
- The **TOGAF ADM** runs from the **Preliminary** phase and the **architecture vision** (A) via business, information systems and technology architecture (B–D) to planning (E–F) and **governed implementation and change** (G–H), with **requirements management** at the centre
- The **content framework** distinguishes **deliverables** (agreed), **artefacts** (catalogues, matrices, diagrams) and **building blocks** (architecture vs. solution)
- **Architecture governance** works through **principles**, an **architecture board**, **contracts**, **compliance reviews** and recorded **dispensations**

---

# Next Session: EAM Frameworks II — Modelling and Other Frameworks

- The **ArchiMate** modelling language: layers, elements, relationships
- The **Zachman** framework
- Comparing frameworks: which one for which purpose?

::: callout
**Preparation:** take one architecture diagram from your training company (or draw one from memory) and note which **symbols** it uses and whether a reader outside IT would understand it. Remove anything confidential.
:::

::: notes
The preparation task leads to the question of a common notation: today's artefacts (catalogues, matrices, diagrams) need a consistent language to be understood across teams — that is ArchiMate. The case of today (on-demand bus) can be modelled in ArchiMate next time.
:::

---

# References {.references}

- Ahlemann, F., Stettiner, E., Messerschmidt, M., & Legner, C. (Eds.). (2012). *Strategic enterprise architecture management: Challenges, best practices, and future developments*. Springer. https://doi.org/10.1007/978-3-642-24223-6
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Kotusev, S. (2019). Enterprise architecture and enterprise architecture artifacts: Questioning the old concept in light of new findings. *Journal of Information Technology, 34*(2), 102–128. https://doi.org/10.1177/0268396218816273
- The Open Group. (2022a). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.
- The Open Group. (2022b). *The TOGAF Standard, 10th Edition: Architecture development method*. Van Haren Publishing.
- The Open Group. (2022c). *The TOGAF Standard, 10th Edition: Content, capability, and governance*. Van Haren Publishing.
- Zachman, J. A. (1987). A framework for information systems architecture. *IBM Systems Journal, 26*(3), 276–292. https://doi.org/10.1147/sj.263.0276

TOGAF® and ArchiMate® are registered trademarks of The Open Group. Diagrams in this deck are own illustrations. Frameworks are described in own words.
