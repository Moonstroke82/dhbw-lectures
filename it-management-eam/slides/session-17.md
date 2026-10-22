---
course: IT Management and EAM
session: 17
title: EAM Frameworks II: Modelling and Other Frameworks
subtitle: The ArchiMate modelling language · the Zachman framework · comparing and combining frameworks
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# EAM Frameworks II: Modelling and Other Frameworks {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · why a modelling language 10 min · ArchiMate framework and elements 20 min · relationships 15 min · mini exercise "read the model" 10 min · break 10 min · views, viewpoints and good practice 10 min · Zachman framework 10 min · mini exercise "which cell?" 10 min · comparing and combining frameworks 10 min · case exercise "model the on-demand bus pilot in ArchiMate" 45 min · wrap-up 5 min · ~15 min buffer.
Session 16 introduced TOGAF as a method framework; today adds the two other kinds of frameworks named on its first content slide: a modelling language (ArchiMate) and a classification framework (Zachman), and closes with a comparison. This covers the module content "EAM frameworks" and the methodological competence of modelling a company's IT and business processes. The running case is the on-demand bus pilot that was walked through the ADM in session 16.
Source note for the lecturer: ArchiMate is cited from the ArchiMate 3.2 Specification (The Open Group Standard of 2022, published as a book by Van Haren in January 2023, document C226; chapters checked against the publisher's sample: 5 relationships, 7–10 strategy, business, application and technology layers, 11 cross-layer relationships, 12 implementation and migration, 13 viewpoints, appendix C example viewpoints). The relationship categories were checked against the online 3.1 specification (association is a dependency relationship since 3.1; value stream added in 3.1). ArchiMate is copyrighted: element and relationship names are used as labels, descriptions are own words, all figures are own drawings in a simplified notation. Zachman is cited from the two IBM Systems Journal articles (1987; Sowa & Zachman, 1992). The current version 3.0 of the Zachman Framework is published by Zachman International with changed row and column names; it is not cited here — re-check before the first run in 2028. Hanschke (2023) has no ArchiMate chapter; it treats EAM frameworks in section 5.2 and modelling guidelines in section 8.3.2 (checked against the table of contents). All RNM examples are own examples.
:::

---

# Today's Agenda

1. Recap: your architecture diagram
2. Why a modelling language?
3. ArchiMate: layers, elements, relationships
4. Views, viewpoints and good modelling practice
5. The Zachman framework
6. Comparing and combining frameworks
7. Case exercise: model the on-demand bus pilot of Rhein-Neckar Mobil Group in ArchiMate

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Why a modelling language (input) · 0:20 ArchiMate framework and elements (input) · 0:40 Relationships (input) · 0:55 Mini exercise "read the model" (pairs) · 1:05 Break · 1:15 Views, viewpoints and good practice (input) · 1:25 Zachman (input) · 1:35 Mini exercise "which cell?" (pairs) · 1:45 Comparing and combining frameworks (input + discussion) · 1:55 Case exercise (groups + plenary) · 2:40 Wrap-up · ~15 min buffer.
If the session runs long: "ArchiMate and the TOGAF ADM", "Common Modelling Mistakes" and "Zachman: Versions and Use Today" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise. Bring A3 paper and sticky notes for the case exercise; groups with laptops may use a free modelling tool (e.g. Archi, an open-source ArchiMate tool, or draw.io with its ArchiMate shapes).
:::

---

# Recap: Your Architecture Diagram

You were asked to bring one **architecture diagram** from your training company and to note its **symbols** and whether a reader outside IT would understand it.

- Which **symbols** does it use: boxes, cylinders, clouds, arrows, colours? Is there a **legend**?
- What does an **arrow** mean in your diagram: data flow, call, dependency, "belongs to"?
- Which **domains** does it show: business, data, application, technology (session 10)?
- Would the **board** or the **works council** understand it?

::: notes
Pairs for 3 min: swap diagrams and let the partner explain the other diagram without help — then the owner says what was misread. Collect on the board: symbols used · meaning of arrows · domains · audience. Typical findings: PowerPoint or Visio boxes with vendor logos; arrows mean different things in the same diagram; no legend; mainly application and technology, rarely business; diagrams made for one project and never updated. Some students bring UML, BPMN or network diagrams; a few may know ArchiMate (often from Bizzdesign, ADOIT, Archi or LeanIX exports). Keep the board — the next slide turns these findings into the case for a common language. Remind students not to show confidential diagrams to the plenary.
:::

---

# Why a Modelling Language? {.section}

From boxes and lines to a shared language

---

# The Problem with Boxes and Lines

::: columns
**Informal diagrams**

- Every author invents **own symbols**
- An arrow may mean **data flow**, **call**, **dependency** or **"is part of"**
- Business, application and technology are **mixed** or missing
- Diagrams cannot be **checked**, **combined** or **analysed**
|||
**A modelling language adds**

- A defined set of **element types** with fixed meaning
- Defined **relationships** with rules for what may connect to what
- A **notation** that readers learn once
- One **meta-model** across domains: models from different teams **fit together**
:::

::: callout
A shared language makes architecture models **understandable**, **consistent** and **analysable** — e.g. "which processes are affected if this server fails?"
:::

::: source
Own wording based on Lankhorst (2017) and The Open Group (2023).
:::

::: notes
Lankhorst (2017) argues that enterprise architecture needs an integrated language across domains: domain-specific languages such as BPMN for processes, UML for software or network diagrams for infrastructure each cover one domain well, but they do not describe the relationships between domains. Link to session 11: the meta-model of the repository defines what can be stored; ArchiMate is such a meta-model plus a notation. The analysis example is the impact analysis of session 10 — with a consistent model, it becomes a query instead of a meeting.
:::

---

# ArchiMate at a Glance

- An **open standard** of **The Open Group** for modelling enterprise architectures; current version **3.2** (2022)
- Developed from a Dutch research and practice project led by **Lankhorst**; an Open Group standard since 2009
- **Complements TOGAF**: TOGAF says how to proceed, ArchiMate how to **describe** the results
- **Supported by many EAM tools**; models can be exchanged in a standard file format

::: cards
### Few concepts
A small set of element types that covers business, applications and technology
### Relationships across layers
Shows how technology supports applications and applications support the business
### Views for stakeholders
Viewpoints select what each audience needs to see
:::

::: source
Own wording based on The Open Group (2023) and Lankhorst (2017).
:::

::: notes
The ArchiMate 3.2 Specification was published in 2022 as an Open Group standard and as a book in January 2023. The language goes back to a project in the Netherlands in the early 2000s in which research institutes and companies developed an enterprise modelling language; Lankhorst (2017) describes the project and the design choices. The designers deliberately kept the language small: it does not replace detailed languages such as BPMN for processes or UML for software design — it connects them at the architecture level. Exchange format: the Open Group publishes a model exchange file format, so models can move between tools. Exam point: be able to state the purpose of ArchiMate and how it relates to TOGAF.
:::

---

# ArchiMate: Layers, Elements, Relationships {.section}

The core of the language

---

# The ArchiMate Framework: Layers and Aspects

![Own illustration of the ArchiMate framework as a grid. Rows are layers: strategy with capability, value stream, resource and course of action; business with business object, contract and product as passive structure, business process, function, service and event as behaviour, business actor, role and interface as active structure; application with data object, application process, function and service, application component and interface; technology and physical with artifact and material, technology process and service, node, device, system software, network and equipment; implementation and migration with work package, deliverable, implementation event, plateau and gap. A motivation column spans all layers with stakeholder, driver, assessment, goal, outcome, principle, requirement, constraint, meaning and value. Lower layers serve and realise upper layers. In each row, an active structure element performs behaviour that accesses passive structure](img/archimate-framework.png){width=72%}

::: source
Own illustration based on The Open Group (2023); selection of elements.
:::

::: notes
Two dimensions to explain. Layers: business, application and technology are the core, extended by strategy above, implementation and migration below, and motivation as a separate set of elements; physical elements (equipment, facility, distribution network, material) extend the technology layer for things such as buses and depots. Aspects: active structure (who or what acts: actor, component, node), behaviour (what is done: process, function, service), passive structure (what is acted upon: business object, data object, artifact). The analogy from natural language helps: subject (active) – verb (behaviour) – object (passive): "the bus driver sells a ticket". The colours are a convention used by most tools, not part of the standard. Link to session 10: the four EA domains map onto the layers — data sits as passive structure in the business layer (business object) and the application layer (data object).
:::

---

# Core Elements in Each Layer

| Aspect | Business layer | Application layer | Technology layer |
|---|---|---|---|
| **Active structure** | Business actor, business role | Application component | Node, device, system software, communication network |
| **Behaviour (internal)** | Business process, business function | Application function, application process | Technology function, technology process |
| **Behaviour (external)** | Business service | Application service | Technology service |
| **Interface** | Business interface | Application interface | Technology interface |
| **Passive structure** | Business object | Data object | Artifact |

- The same **pattern** repeats in each layer — learn it once, use it three times

::: source
Own compilation based on The Open Group (2023).
:::

::: notes
Examples at RNM for each cell: actor "Passenger", role "Bus driver"; component "Fare back-end"; node "Server in the Group IT data centre", device "On-board ticket device", system software "Database management system"; process "Sell ticket on board", function "Fare management"; application function "Calculate fare"; service "Ticket sale on board", application service "Fare calculation"; interface: the ticket device screen (business interface to the passenger), the API of the fare back-end (application interface); business object "Ticket", data object "Sale record", artifact "Installation package of the ticket device software". Process vs function: a process has a sequence and a result ("sell ticket on board"), a function groups behaviour by skills or resources without a sequence ("fare management") — similar to the capability discussion of session 12. An actor is a concrete person or organisation unit; a role is a responsibility that actors take on.
:::

---

# Services: The Key Concept

::: columns
**External view: the service**

- A service is **behaviour offered to the environment**: what the user gets
- Named from the **user's perspective**: "Ticket sale on board", "Fare calculation"
- Users do not care **how** it is realised
|||
**Internal view: the realisation**

- **Processes** or **functions** realise the service
- **Active structure** performs them
- Can be **changed** without changing the service, e.g. a new ticket device
:::

::: callout
Layers are linked by services: **technology serves applications, applications serve the business** — each layer uses the services of the layer below.
:::

::: source
Own wording based on The Open Group (2023) and Lankhorst (2017).
:::

::: notes
Service orientation is the organising principle of ArchiMate, and Lankhorst (2017) explains it as the way to keep layers loosely coupled. Link to session 5: an ITIL service is also defined by the value for the consumer, not by the technology — the ArchiMate service is the architecture view of the same idea. Link to session 14: an API makes an application service available through an application interface. Typical student error: naming services after systems ("SAP service") instead of after what the user gets ("Post revenue").
:::

---

# Strategy, Motivation and Migration Elements

| Group | Main elements | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **Strategy** | Capability, value stream, resource, course of action | Capability "on-demand trip management"; value stream "plan and take a trip" (session 12) |
| **Motivation** | Stakeholder, driver, assessment, goal, outcome, principle, requirement, constraint | Driver "rural mobility without a car"; goal "pilot running from 2028"; principle "API first"; requirement "usage reports for the districts" |
| **Migration** | Implementation and migration elements: work package, deliverable, plateau, gap | Work package "integrate the on-demand platform"; plateau "pilot with phone booking" (session 13: transitions) |

- These groups connect the model to **strategy** (session 12), **principles** (session 16) and **roadmaps** (session 13)

::: source
Own compilation based on The Open Group (2023); own examples.
:::

::: notes
Motivation elements answer "why": stakeholders have drivers, assessments of drivers lead to goals, goals are made concrete by outcomes, principles and requirements, and core elements realise requirements. Implementation and migration elements answer "how do we get there": plateaus are stable states (baseline, transition, target — session 13), a gap is the difference between two plateaus (session 16: gap analysis in Phases B–D), work packages realise deliverables that realise the target elements. This is what makes ArchiMate fit the TOGAF ADM: motivation for the Preliminary phase, Phase A and requirements management; the core layers for B–D; implementation and migration for E–F.
:::

---

# Relationships

![Own illustration of the eleven ArchiMate relationships in simplified notation. Structural relationships: composition (filled diamond at the whole; the part cannot exist alone), aggregation (hollow diamond; the part can belong to several wholes), assignment (dot at the source, arrowhead at the target; who or what performs the behaviour) and realisation (dashed line with hollow triangle; something concrete makes something abstract real). Dependency relationships: serving (solid line with open arrowhead pointing to the user), access (dotted line; behaviour reads or writes a passive element, arrow towards the object means write), influence (dashed line with open arrowhead; affects a motivation element, plus or minus) and association (plain line; any other relation, may be directed). Dynamic relationships: triggering (solid line with filled arrowhead; causes the next behaviour) and flow (dashed line with filled arrowhead; passes something on). Other: specialisation (solid line with hollow triangle; is a kind of)](img/archimate-relationships.png){width=70%}

::: source
Own illustration based on The Open Group (2023).
:::

::: notes
Go through the four groups. Structural relationships build things up (composition, aggregation), say who does what (assignment) and connect abstract and concrete (realisation: a process realises a service, an application component realises an application service, a work package realises a deliverable). Dependency relationships say who uses what (serving, access) and how motivation elements affect each other (influence). Dynamic relationships describe time order (triggering) and transfer (flow) between behaviour elements. The specification defines which relationship is allowed between which pair of elements and rules for deriving indirect relationships — students do not need to learn the tables; they need to choose the right relationship for typical cases. The drawing is simplified; the standard notation has finer details (e.g. the size of the arrowheads).
:::

---

# Reading Relationships Correctly

| Relationship | Read as | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **Serving** | A *serves* B — arrow points to the **user** | Application service "Fare calculation" serves process "Sell ticket on board" |
| **Realisation** | A *realises* B — concrete → abstract | Ticket device software realises "Fare calculation" |
| **Assignment** | A *performs* or *is responsible for* B | Role "Bus driver" is assigned to "Sell ticket on board" |
| **Access** | Behaviour *reads* or *writes* an object | "Sell ticket on board" writes the business object "Ticket" |
| **Triggering / flow** | A *starts* B / A *passes something to* B | "Receive payment" triggers "Issue ticket"; device software passes sale data to the fare back-end |
| **Composition** | A *consists of* B | The fare back-end consists of a tariff module and a sales module |

::: source
Own wording based on The Open Group (2023); own examples.
:::

::: notes
The two most frequent errors: (1) serving drawn in the wrong direction — ask "who uses whom?"; the arrow points to the one who is served (the user), not to the provider. (2) Association used for everything — it carries almost no meaning; use it only when nothing else fits. Tip for the exam and the case: write the relationship as a sentence with the element names ("the payment provider realises card payment authorisation") — if the sentence sounds wrong, the relationship is probably wrong. Flow between application components (as in the example view) is common practice to show data exchange between applications at the architecture level.
:::

---

# Example: A Layered View of the On-Board Ticket Sale

![Own illustration in simplified ArchiMate notation of the on-board ticket sale at Rhein-Neckar Mobil Group. Business layer: the business service ticket sale on board serves the business actor passenger; the business process sell ticket on board realises this service; the business role bus driver is assigned to the process; the process writes the business object ticket. Application layer: the application services fare calculation and card payment authorisation serve the business process; the ticket device software realises fare calculation; the external payment provider realises card payment authorisation; the ticket device software passes sale data to the fare back-end in a flow; the fare back-end writes the data object sale record. Technology layer: the on-board ticket device is assigned to the ticket device software, a server in the Group IT data centre is assigned to the fare back-end, and the mobile network connects the ticket devices with the data centre](img/archimate-ticketing-view.png){width=62%}

::: source
Own illustration based on The Open Group (2023); own example.
:::

::: notes
This is the trace example of session 10 (ticket sale through four domains) drawn in ArchiMate. Read it bottom-up with the class: the device runs the ticket device software, which realises the fare calculation service, which serves the sales process, which the bus driver performs and which realises the service the passenger uses. Ask: what happens to the business if the mobile network fails? (Nothing at first — sales are stored on the device and uploaded later, session 8 and 14; the model shows the dependency, the store-and-forward design is a detail outside this view.) Ask: what changes in the model if the fare back-end is replaced (session 13 roadmap)? Only the component and its node; services and business layer stay — the value of service orientation.
:::

---

# Mini Exercise: Read the Model {.exercise}

Name the **ArchiMate relationship** (and its **direction**) for each statement at *Rhein-Neckar Mobil Group*.

1. The car-sharing app offers the service "unlock a car" to customers
2. The **dispatcher** role is responsible for the process "plan vehicle deployment"
3. The process "handle complaint" **reads** the customer data
4. "Receive payment" is followed by "issue ticket"
5. The cloud ERP makes the application service "post revenue" available
6. The principle "API first" contributes to the goal "partners reuse our functions"
7. Electric buses and diesel buses are **kinds of** bus
8. The mobility app **consists of** a booking module and an account module

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 the application service "Unlock a car" **serves** the customer (business actor) or the customer's process; the app (component) **realises** the service — full marks for naming realisation + serving. 2 **Assignment** from the business role "Dispatcher" to the process. 3 **Access** (read): in the notation the arrow points from the object to the process. 4 **Triggering** from "Receive payment" to "Issue ticket" (both business processes or events). 5 **Realisation** from the application component "Cloud ERP" to the application service. 6 **Influence** (positive, "+") from the principle to the goal. 7 **Specialisation** from "Electric bus" and "Diesel bus" to "Bus" (physical equipment or node). 8 **Composition** from the mobility app to its modules (application components); aggregation is acceptable if students argue that a module could be reused in other apps. Lesson: almost every statement in a case text maps to a relationship — reading cases this way is the core skill for the case exercise.
:::

---

# Views, Viewpoints and Good Practice {.section}

One model, many pictures

---

# Viewpoints: Which Picture for Whom?

| Example viewpoint | Shows | Typical audience |
|---|---|---|
| **Layered** | Business, application and technology in one picture | Architects, programme managers |
| **Application cooperation** | Applications and their data flows | IT managers, integration team (session 14) |
| **Technology usage** | Which applications run on which infrastructure | IT operations, security (sessions 8, 15) |
| **Motivation** | Stakeholders, goals, principles, requirements | Management, architecture board (session 16) |
| **Capability map** | Capabilities and their properties | Business management (session 12) |
| **Migration** | Plateaus, gaps and work packages | Steering committee, portfolio (session 13) |

::: source
Own compilation based on The Open Group (2023), ISO/IEC/IEEE (2022) and Lankhorst (2017).
:::

::: notes
Session 10 introduced the terms from ISO/IEC/IEEE 42010: stakeholders have concerns; a viewpoint defines the conventions for a kind of view; a view shows the architecture from one viewpoint. ArchiMate offers example viewpoints (appendix C of the specification) and expects organisations to define their own. The names in the table are partly own short names. The key point: the model is stored once in the repository (session 11), and each view is a selection for one audience — the board gets a capability map with colours, not the layered view with 40 boxes. EAM tools such as LeanIX generate many of these views as reports (session 18).
:::

---

# Good Modelling Practice

- **Start from a question**: who will read the view, and what should they decide?
- **One viewpoint per diagram**; keep it readable — rather two small views than one large one
- **Name elements consistently**: processes as verb + noun, services from the user's view, components by their business name
- Use the **right relationship**; avoid association as a default
- **Model in the repository**, not in a drawing tool: views are generated from one model
- Keep **levels of detail** apart: architecture, not every screen or database table
- Add a **legend** for non-architects and **date** every view

::: source
Own wording based on Lankhorst (2017) and Hanschke (2023).
:::

::: notes
Hanschke (2023, section 8.3.2) recommends binding modelling guidelines as part of the EAM rule set, and section 5.5 presents best-practice visualisations — her book focuses on visualisations such as landscape maps rather than on ArchiMate. Lankhorst (2017) treats communication of models to stakeholders as a central task: a correct model nobody understands has no effect. Practical rule of thumb from projects (not from the standard): if a view needs more than about 20 elements, split it. Link to the recap: compare these rules with the diagrams students brought.
:::

---

# ArchiMate and the TOGAF ADM {.optional}

| ADM phase (session 16) | ArchiMate elements typically used |
|---|---|
| **Preliminary, A** | Stakeholder, driver, goal, principle; capability (high level) |
| **Requirements management** | Requirement, constraint, and their realisation by core elements |
| **B: Business** | Capability, value stream, actor, role, process, business service, business object |
| **C: Information systems** | Application component, application service, interface, data object |
| **D: Technology** | Node, device, system software, network, technology service |
| **E, F: Planning** | Plateau, gap, work package, deliverable |

::: source
Own compilation based on The Open Group (2022, 2023).
:::

::: notes
Self-study. Both standards are maintained by The Open Group and are designed to be used together; the mapping is approximate — each phase can use any element if the stakeholders need it. The point for the exam: TOGAF produces artefacts (catalogues, matrices, diagrams, session 16); ArchiMate is a language in which many of the diagrams can be drawn.
:::

---

# Common Modelling Mistakes {.optional}

| Mistake | Better |
|---|---|
| Serving arrow points to the **provider** | The arrow points to the **user** |
| A **system** named as a service ("SAP service") | Service named after what the user gets ("Post revenue") |
| **Process** used for a permanent area of work | **Function** (or capability) for "fare management"; process for "sell ticket" |
| **Actor** and **role** mixed up | Actor = who (person, unit); role = responsibility ("bus driver") |
| **Association** everywhere | A specific relationship that carries meaning |
| One view with **everything** | Several views, each for one audience |

::: source
Own compilation based on The Open Group (2023) and Lankhorst (2017).
:::

::: notes
Self-study; also a checklist for marking the case exercise and for the worksheet. The process–function distinction is often debated; accept a reasoned answer. Capability vs. function: a capability (session 12) is what the enterprise can do, independent of organisation; a business function groups behaviour within the organisation.
:::

---

# The Zachman Framework {.section}

A classification scheme for architecture descriptions

---

# The Zachman Framework

![Own illustration of the Zachman framework as a grid of six columns and six rows. Columns are the questions what (things, data), how (processes), where (locations), who (people, roles), when (events, timing) and why (goals, rules). Rows are the perspectives planner (scope), owner (business model), designer (system model), builder (technology model), subcontractor (detailed parts) and the functioning enterprise. Example cells for the on-demand bus pilot of Rhein-Neckar Mobil Group: planner–what: list of business things such as trips, vehicles, fares; planner–where: two pilot districts; owner–how: process book an on-demand trip; owner–who: dispatcher, driver, phone booking team; owner–why: goal rural access without a car; designer–what: logical data model with trip request and vehicle position; designer–when: booking cut-off and service hours; builder–where: SaaS in an EU cloud region and mobile network](img/zachman-grid.png){width=74%}

::: source
Own illustration based on Zachman (1987) and Sowa and Zachman (1992); own example.
:::

::: notes
Zachman (1987) used the analogy of building architecture and manufacturing: the owner, the designer and the builder of a building need different descriptions of the same thing. The 1987 article described three columns (data, function, network); Sowa and Zachman (1992) extended the framework to six columns (people, time, motivation) and named the perspectives. Each cell is one kind of description; the rows are different perspectives, not more detail of the same model — the builder's model is not a refined owner's model but a different model with its own constraints. Rules from the 1992 article in own words: each cell is unique, the columns have no order, and each row is complete in itself. The functioning enterprise (bottom) is the real thing, not a description. Link to session 10: Zachman's article is often called the starting point of EA as a discipline.
:::

---

# Using Zachman: Strengths and Limits

::: columns
**Strengths**

- **Completeness check**: which questions and perspectives are not yet described?
- **Neutral**: no method, notation or tool prescribed — works with any of them
- Makes clear that **different stakeholders** need **different models**
- Simple to explain with **six questions**
|||
**Limits**

- **No method**: says nothing about how or in which order to produce the cells
- **No relationships** between cells defined; no notation
- Filling **all 36 cells** is rarely worth the effort
- Row and column names changed over the **versions**
:::

::: callout
Zachman tells you **what** to describe; TOGAF tells you **how to proceed**; ArchiMate tells you **how to draw** it.
:::

::: source
Own wording based on Zachman (1987) and Sowa and Zachman (1992).
:::

::: notes
In practice, Zachman is used as a thinking tool and a checklist rather than as the structure of a repository: e.g. "our application landscape describes what and how at the designer level, but nobody has described why (goals, rules) or when (events, timing)". Session 16 already sorted Zachman as a classification framework, in contrast to the method framework TOGAF. Exam point: name the two dimensions and state one strength and one limit.
:::

---

# Mini Exercise: Which Cell? {.exercise}

Place each description from *Rhein-Neckar Mobil Group* in the **Zachman grid**: which **question** (column) and which **perspective** (row)?

1. The board's list of **goals** for the mobility app
2. The **logical data model** of the customer account
3. The **source code** of the fare calculation
4. The process model **"handle complaint"**
5. The **organisation chart** of the customer service centre with its roles
6. The **dates** of the yearly timetable change
7. The **server and network plan** of the Group IT data centre

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 why / planner (scope) — accept owner if the goals are already detailed business goals. 2 what / designer (system model). 3 how / subcontractor (detailed parts). 4 how / owner (business model). 5 who / owner (business model). 6 when / owner (business events and cycles) — accept planner if argued as a list of key events. 7 where / builder (technology model). Lesson: the row is decided by the audience and level of abstraction, the column by the question answered. Ask: which column is usually the emptiest in practice? (Often when and why.)
:::

---

# Zachman: Versions and Use Today {.optional}

- **1987**: first article in the *IBM Systems Journal* — three columns (data, function, network) and perspectives taken from building and manufacturing
- **1992**: extension with **Sowa** to six columns and a formal set of rules
- Later versions, published by **Zachman International**, renamed rows and columns; the framework is called an **ontology** of enterprise descriptions
- Today: rarely used as a full method; often used as a **checklist** and to explain **perspectives**

::: source
Own wording based on Zachman (1987) and Sowa and Zachman (1992).
:::

::: notes
Self-study. Students who search the web will find the current version 3.0 with different labels (e.g. "executive perspective", "business management perspective" instead of planner and owner). The idea is the same; the exam uses the labels from the slides. The later versions are proprietary; the slides only use the published 1987 and 1992 articles.
:::

---

# Comparing Frameworks {.section}

Which framework for which purpose?

---

# Comparing TOGAF, ArchiMate and Zachman

| | TOGAF | ArchiMate | Zachman | Practitioner approaches |
|---|---|---|---|---|
| **Kind** | Method framework | Modelling language | Classification framework | Instruments and practices |
| **Main question** | How do we develop and govern architecture? | How do we describe it consistently? | Which descriptions are needed? | How do we run EAM pragmatically? |
| **Provides** | ADM, content framework, governance | Elements, relationships, notation, viewpoints | Grid of questions × perspectives | Visualisations, usage scenarios, governance rules |
| **Strength** | Complete process, common terms | Cross-layer analysis, tool support | Completeness check, neutrality | Fast start, close to practice |
| **Limit** | Large, needs tailoring | Learning effort, no method | No method, no notation | Less standardised |

::: source
Own compilation based on The Open Group (2022, 2023), Zachman (1987), Hanschke (2023) and Keller (2017).
:::

::: notes
Practitioner approaches: Hanschke (2023) and Keller (2017) from the module literature, and the default meta-models of EAM tools (session 18). Discuss with the class: these are not competitors — each answers a different question. Exam point: the table is the core of today's comparison; students should be able to explain the kind and the main question of each framework and give one strength and one limit, ideally applied to a case.
:::

---

# Choosing and Combining Frameworks

::: columns
**A typical combination**

- **TOGAF ADM**, tailored, as the **method** for larger changes
- **ArchiMate** as the **language** for the diagrams in the repository
- **Zachman** as a **checklist**: have we described all questions for all audiences?
- The **EAM tool's meta-model** as the practical basis (session 18)
|||
**Questions for choosing**

- What is the **purpose**: transformation, documentation, governance?
- How **large** and how **mature** is the EAM function?
- Who are the **stakeholders**, and what can they read?
- Which **tools** and **skills** exist?
- What do **partners** and **regulators** expect?
:::

::: source
Own wording based on Hanschke (2023), Lankhorst (2017) and The Open Group (2022).
:::

::: notes
Apply to the two-person team of RNM: tailored TOGAF ideas (principles, Phase A for larger initiatives, board, compliance reviews — session 16), ArchiMate for a few standard views in the EA tool (layered view for projects, application cooperation for integration), a capability map for management; Zachman only as a mental checklist. For a small organisation such as the winegrowers' cooperative of the worksheets: no formal framework, a simple application list and principles. Kotusev (2019, session 16) is a reminder that practice uses a limited set of artefacts that support decisions — choose frameworks by the decisions they support.
:::

---

# Case Exercise: Model the On-Demand Bus Pilot {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–16) plans an **on-demand bus pilot** in two rural districts from 2028 (session 16): 20 minibuses, booked in the **mobility app** or **by phone**.

- An **on-demand platform** (SaaS, EU region) handles booking, routing and the **driver tablets**
- The platform is connected via the **integration platform** to the **customer master**, the **payment platform** and the **dispatching system**
- A **phone booking team** enters bookings for passengers without the app
- The districts co-fund the pilot and want **monthly usage reports**; the **works council** watches driver tracking
- Principle **"API first"** (session 16); the pilot starts with **phone booking and the vendor's app** before the mobility app is ready

::: notes
Read the case together (2 min). Groups of 4–5 work on A3 paper (or a tool). Remind them of the simplified notation: labelled boxes with the element type in the corner are fine; relationships must be drawn with the correct line ends or labelled with their names. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. **Business layer:** model the business actor(s) and roles, the business service, the process "book and take an on-demand trip" with **three steps** and **triggering**, and one business object.
2. **Application layer:** model the application components and services that **serve** the process, the **data objects** and the **flows** via the integration platform.
3. **Technology layer:** model where the platform runs and the **driver tablet**.
4. **Motivation and migration:** model the districts as **stakeholder** with a **goal** and a **requirement**, the principle "API first", and **two plateaus** with the **gap** between them.
5. **Viewpoints:** which view would you show the **district council** and which the **works council**? What would you leave out?

::: notes
About 30 min group work + 15 min plenary (two groups present, the others compare). This is the session's exam-style exercise. Expected answers (several defensible; check element types and relationship directions):
1 Business: actor "Passenger" served by business service "On-demand trip"; process "Book and take an on-demand trip" realises the service, composed of steps "Request trip" → (triggering) "Confirm pick-up time" → "Pick up and drop off passenger" → "Pay fare"; roles "Phone booking agent", "Dispatcher", "Minibus driver" assigned to steps; business objects "Trip booking", "Ticket"; actors "District council", "Phone booking team".
2 Application: components "On-demand platform" (realises application services "Trip booking" and "Route optimisation"), "Mobility app" (later) and the "vendor app" (pilot), "Integration platform", "Customer master", "Payment platform", "Dispatching system"; application services serve the process steps (trip booking serves "Request trip", route optimisation serves "Confirm pick-up time"); data objects "Trip request", "Vehicle position", "Customer", "Usage report"; flows: on-demand platform → integration platform → customer master / payment platform / dispatching system (or flows labelled with the data); no direct flow bypassing the integration platform (API first). Application interface "Booking API" of the platform is a good addition.
3 Technology: node "SaaS platform of the vendor (EU cloud region)" assigned to the on-demand platform; device "Driver tablet" with system software "Driver app" or with the application component "Driver app" assigned; communication network "Mobile network"; optional: "Mobile device management" as technology service serving the tablets.
4 Motivation: stakeholder "District councils" — driver "Rural mobility without a car" — goal "Pilot in operation from 2028" or "Better rural access" — requirement "Monthly usage reports" realised by the application service "Usage reporting"; principle "API first" influences or realises the requirement "Integration only via the integration platform"; stakeholder "Works council" with requirement "No individual performance monitoring of drivers" (constraint). Migration: plateau 1 "Pilot with phone booking and vendor app", plateau 2 "Booking in the mobility app with one customer account"; gap: mobility app integration, customer master link, single sign-on, payment platform; work packages realise plateau 2.
5 District council: a simple view of the service, the goal and the usage report (motivation view plus the business service) — no technology. Works council: a view of driver tablet, the data collected (vehicle position, trip data), who accesses it and for what purpose (technology usage plus data objects and access) — leave out payment and fare details. Lesson: one model, different views — and the model shows exactly which data the works council asks about.
:::

---

# Key Takeaways

- A **modelling language** gives architecture diagrams a fixed meaning, so they can be understood, combined and analysed
- **ArchiMate** structures the enterprise in **layers** (strategy, business, application, technology, implementation and migration) and **aspects** (active structure, behaviour, passive structure), plus **motivation**
- **Services** link the layers; **relationships** such as serving, realisation, assignment, access, triggering and flow carry the meaning
- **Viewpoints** select what each stakeholder needs from one model
- **Zachman** classifies descriptions by **six questions** × **perspectives** — a completeness check, not a method
- TOGAF, ArchiMate and Zachman answer **different questions** and are best **combined** and tailored

---

# Next Session: EAM Tools and Course Synthesis

- The **EAM tool landscape**: what tools do, and how to choose one
- **SAP LeanIX** walkthrough: fact sheets, relations, reports
- **Synthesis**: how IT management (Part A) and EAM (Part B) fit together
- **Exam Q&A**: question types and worked practice examples

::: callout
**Preparation:** find out whether your training company uses an **EAM tool** (e.g. LeanIX, Alfabet, ADOIT, Bizzdesign) and what it is used for. Bring **three questions** about topics from sessions 1–17 that you would like to revise.
:::

::: notes
The preparation task connects today's modelling (repository, meta-model, views) to the tools of session 18 — many of them support ArchiMate or generate similar views from fact sheets. The questions feed the exam Q&A (1 h in session 18); collect them at the start of session 18 or ask students to post them beforehand. Remind students that the Q&A covers question types and practice examples, not the actual exam.
:::

---

# References {.references}

- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- ISO/IEC/IEEE. (2022). *Software, systems and enterprise — Architecture description* (ISO/IEC/IEEE Standard No. 42010:2022). International Organization for Standardization.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Kotusev, S. (2019). Enterprise architecture and enterprise architecture artifacts: Questioning the old concept in light of new findings. *Journal of Information Technology, 34*(2), 102–128. https://doi.org/10.1177/0268396218816273
- Lankhorst, M. (2017). *Enterprise architecture at work: Modelling, communication and analysis* (4th ed.). Springer. https://doi.org/10.1007/978-3-662-53933-0
- Sowa, J. F., & Zachman, J. A. (1992). Extending and formalizing the framework for information systems architecture. *IBM Systems Journal, 31*(3), 590–616. https://doi.org/10.1147/sj.313.0590
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Introduction and core concepts* (Document No. C220). Van Haren Publishing.
- The Open Group. (2023). *ArchiMate 3.2 specification* (Document No. C226). Van Haren Publishing.
- Zachman, J. A. (1987). A framework for information systems architecture. *IBM Systems Journal, 26*(3), 276–292. https://doi.org/10.1147/sj.263.0276

TOGAF®, ArchiMate® and The Open Group® are registered trademarks of The Open Group. Zachman Framework is a trademark of Zachman International. Diagrams in this deck are own illustrations. Frameworks are described in own words.
