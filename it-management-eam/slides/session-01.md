---
course: IT Management and EAM
session: 1
title: Introduction to IT Management
subtitle: Course overview · role of IT · information management models · fields of action
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# Introduction to IT Management {.title}

::: notes
Welcome. Short introduction of yourself, ideally with an example from your own work where IT management decisions mattered.
Time plan for today (3 h): course intro 25 min · warm-up 15 min · role of IT 30 min · break 10 min · information management model 35 min · strategic vs. operational 15 min · case exercise 35 min · wrap-up 5 min · ~10 min buffer.
:::

---

# Today's Agenda

1. Welcome and course overview
2. Warm-up: what does "the IT department" do?
3. The role of IT in the enterprise
4. Information management: a model and its levels
5. Fields of action of IT management
6. Strategic vs. operational IT management
7. Case exercise

::: notes
Time and format guide (not shown to students):
0:00 Welcome and course overview (input) · 0:25 Warm-up (pair discussion) · 0:40 Role of IT (input + discussion) · 1:10 Break · 1:20 Information management model and fields of action (input) · 1:55 Strategic vs. operational (input) · 2:10 Case exercise (groups) · 2:45 Wrap-up · ~10 min buffer.
If the Carr debate runs long, keep it — shorten the fields-of-action overview instead (the table slide is enough) and keep the case exercise.
:::

---

# What You Will Be Able to Do After This Module

- **Distinguish** the fields of action and instruments of strategic and operational IT management
- **Explain and apply** methods for managing IT systems and IT services, e.g. ITIL, IT controlling, IT governance
- **Understand and discuss** the main domains of an enterprise architecture
- **Collect and model** information about a company's IT and business processes
- **Work with** EAM frameworks and tools such as TOGAF, ArchiMate and LeanIX
- **Consider** compliance and ethical requirements in IT decisions

::: source
Based on the module description *IT Management and Enterprise Architecture Management*, DHBW, Digital Business Management.
:::

---

# Course Roadmap: Two Parts

| Part | Sessions | Topics |
|---|---|---|
| A · IT management | 1–9 | Introduction, IT strategy and alignment, governance and organisation, IT controlling, IT service management (ITIL), risk and compliance, security and business continuity, quality management |
| B · Enterprise architecture management | 10–18 | EA foundations, collecting and modelling architecture information, capabilities and transformation, IT landscape planning, application integration, sourcing, TOGAF, ArchiMate, EAM tools |
| Exam Q&A | end | Open questions, exam-style questions |

::: notes
18 sessions plus 1 h exam Q&A. There is no separate buffer block, so optional slides move to self-study if discussions run long.
:::

---

# How We Work and How You Are Assessed

::: columns
**How we work**

- Short input, then discussion and case work
- Every session ends with a **case exercise in exam style**
- Core slides are exam-relevant; slides marked **Optional · Self-study** are not
|||
**Written exam**

- Concepts, models and frameworks
- Applying methods to short cases
- Exam-style questions in every session and in the final Q&A
:::

::: notes
Bring examples from your training companies — the dual study model is ideal for this module. Remind students not to share confidential company information.
:::

---

# Core Literature

| Topic | Book |
|---|---|
| Information management | Krcmar (2015) |
| IT management handbook | Tiemeyer (2023) |
| IT management in the digital age | Urbach and Ahlemann (2019) |
| IT service management | Beims and Ziegenbein |
| Enterprise architecture management | Hanschke; Keller |

Full references at the end of this deck. Further books from the module handbook are added in the sessions where they are used.

::: notes
Editions of Beims/Ziegenbein, Hanschke and Keller are checked and added to the reference list when the sessions on ITSM and EAM are built. Check e-book availability in the DHBW library.
:::

---

# Warm-up: What Does "the IT Department" Do? {.exercise}

**Think – pair – share**

1. **Think:** list everything the IT department of your training company does.
2. **Pair:** compare with your neighbour. Sort the tasks: which keep things running, which change things?
3. **Share:** which task is the most important for the business — and does the business know it?

::: notes
Timing guide: 15 min — think 3, pair 5, share 7.
Collect answers on the whiteboard in two columns: "run" (service desk, operations, licences, security patches) and "change" (projects, new applications, digitalisation, data platforms). Keep the list — it is reused in the case exercise.
:::

---

# The Role of IT in the Enterprise {.section}

Commodity or strategic asset?

---

# Does IT Matter?

::: columns
**"IT doesn't matter" (Carr, 2003)**

- IT has become a widely available **commodity**, like electricity
- Scarcity, not ubiquity, creates competitive advantage
- Therefore: spend less, follow rather than lead, focus on risks
|||
**Counter-arguments**

- Advantage comes from **how** IT is used in processes and business models, not from the technology itself
- Digital business models (platforms, data-based services) depend on IT
- IT management capabilities differ strongly between firms
:::

::: source
Carr (2003); counter-arguments: own summary, see also Urbach and Ahlemann (2019).
:::

::: notes
Carr's article triggered a large debate. Ask: who is right for your training company? Most will say "both": infrastructure is a commodity, but the use of data and applications can differentiate. This leads to the strategic grid on the next slide. Urbach and Ahlemann argue that the IT department increasingly co-designs the business instead of only serving it.
:::

---

# The Strategic Impact Grid

| | **Low need for new IT** | **High need for new IT** |
|---|---|---|
| **High need for reliable IT** | **Factory:** operations depend on IT, but few new initiatives | **Strategic:** IT is critical for both today's operations and future strategy |
| **Low need for reliable IT** | **Support:** IT supports administration; low strategic impact | **Turnaround:** new IT will change the business; today's operations depend little on IT |

::: source
Adapted from Nolan and McFarlan (2005).
:::

::: notes
The grid helps to decide how much management and board attention IT needs. Examples: a bank or airline is usually "strategic"; a steel plant with automated production may be "factory"; a traditional law firm "support"; a retailer starting e-commerce "turnaround". Ask students to place their training company and justify it. The position can change over time.
:::

---

# Information Management {.section}

A model of what has to be managed

---

# Why "Information" Management?

- Information is a **production factor** and a resource that has to be planned, provided and used economically
- Information is created and used by **information systems** (people, tasks, technology)
- Information systems run on **information and communication technology (ICT)**
- **Information management** plans, steers and controls all three — as a management task

::: source
Based on Krcmar (2015).
:::

::: notes
In German literature, "Informationsmanagement" is the broader term; "IT management" is often used synonymously in practice. In this course we use "IT management" for the management of IT in the enterprise, and Krcmar's model as the structure behind it.
:::

---

# Krcmar's Model of Information Management

::: layers
- Management of the information economy: Information demand, supply and use — what information does the business need?
- Management of information systems: Applications, data, processes and their life cycle
- Management of ICT: Infrastructure: storage, processing, communication, technology bundles
:::

::: callout
Across all three levels: **management tasks of information management**, e.g. IT strategy, IT governance, IT organisation and processes, IT personnel, IT controlling.
:::

::: source
Adapted from Krcmar (2015).
:::

::: notes
Read top-down: business demand for information drives the information systems, which drive the technology. The cross-level management tasks are covered in sessions 2–9 of this course. Check the exact naming of the cross-level tasks and the figure page in the library copy before quoting in written material.
:::

---

# Fields of Action of IT Management

| Field of action | Typical questions | Session |
|---|---|---|
| IT strategy and alignment | Which IT do we need to reach our business goals? | 2 |
| IT governance and organisation | Who decides about IT? How is IT organised? | 3 |
| IT controlling | What does IT cost, and what value does it create? | 4 |
| IT service management | How do we deliver reliable IT services? | 5–6 |
| IT risk and compliance | Which rules apply, and which risks do we accept? | 7 |
| IT security and business continuity | How do we protect information and keep operating? | 8 |
| IT quality management | How good are our IT services and software? | 9 |
| Enterprise architecture management | How do business and IT fit together, today and in the future? | 10–18 |

::: source
Own compilation based on the module description, Krcmar (2015) and Tiemeyer (2023).
:::

::: notes
This is the map for the whole course. Do not explain each field now. Point out that the fields are connected: e.g. IT strategy sets goals that IT controlling measures and EAM implements in the landscape.
:::

---

# Strategic vs. Operational IT Management

::: columns
**Strategic IT management**

- Long-term (several years)
- Direction: IT strategy, target architecture, sourcing, investment portfolio
- Question: *are we doing the right things?*
- Decided with top management
|||
**Operational IT management**

- Short- to mid-term (months, weeks, days)
- Delivery: running services, projects, incidents, budgets
- Question: *are we doing things right?*
- Done by IT units and service owners
:::

::: callout
Both levels must be linked: strategy without operations stays on paper; operations without strategy optimise the wrong things.
:::

::: source
Own illustration based on Krcmar (2015) and Tiemeyer (2023).
:::

::: notes
Link to the warm-up: "change" tasks are often driven by strategic IT management, "run" tasks by operational IT management. Many IT organisations describe this as plan–build–run (session 3).
:::

---

# The IT Department of the Future {.optional}

- IT is no longer only a **service provider** for the business but a **co-designer** of products, processes and business models
- Digital competences spread into the business units; the boundary between "business" and "IT" blurs
- IT management needs both: **reliable operations** and **fast innovation**

::: source
Based on Urbach and Ahlemann (2019).
:::

::: notes
Self-study. Urbach and Ahlemann develop a vision of how IT management should look in about ten years. Good background for session 3 (IT organisation) and session 12 (business model transformation).
:::

---

# Case Exercise: Mapping IT Tasks {.exercise}

**Case:** *Rheinland Logistik GmbH* — 1,800 employees, 25 warehouses. The CIO lists these tasks for next year:

1. Introduce a new warehouse management system in all sites
2. Negotiate a new contract with the cloud provider
3. Reduce the number of open service desk tickets
4. Prepare for a cyber-security audit required by a major customer
5. Decide whether IT should report to the CFO or to the CEO
6. Calculate the IT costs per warehouse
7. Draw up a map of all applications and their interfaces

**Tasks:** assign each task to a field of action. Is it strategic or operational? Place the company in the strategic impact grid and justify your choice.

::: notes
Groups of 4–5, about 25 min work + 10 min discussion.
Expected mapping (several answers defensible): 1 EAM / project portfolio, strategic decision + operational project · 2 IT sourcing (session 15) / controlling · 3 IT service management, operational · 4 IT security and compliance · 5 IT governance and organisation, strategic · 6 IT controlling · 7 EAM (landscape documentation).
Grid: a logistics company with automated warehouses is at least "factory"; with the new WMS and data-based services possibly "strategic". This is the typical exam question format: short case + assignment + justification.
:::

---

# Key Takeaways

- Whether IT matters strategically depends on **how a company uses it** — the strategic impact grid helps to assess this
- **Information management** covers three levels: information economy, information systems and ICT, plus cross-level management tasks
- IT management has distinct **fields of action** — from strategy and governance to service, security and architecture management
- **Strategic** IT management sets the direction, **operational** IT management delivers — both must be linked

---

# Next Session: IT Strategy and Business–IT Alignment

- What is an IT strategy, and how is it derived from the business strategy?
- The strategic alignment model
- Measuring alignment maturity

::: callout
**Preparation:** find out whether your training company has a published business strategy or vision. What does it say about IT or digitalisation?
:::

---

# References {.references}

- Carr, N. G. (2003). IT doesn't matter. *Harvard Business Review, 81*(5), 41–49.
- Krcmar, H. (2015). *Informationsmanagement* (6th ed.). Springer Gabler. https://doi.org/10.1007/978-3-662-45863-1
- Nolan, R. L., & McFarlan, F. W. (2005). Information technology and the board of directors. *Harvard Business Review, 83*(10), 96–106.
- Tiemeyer, E. (Ed.). (2023). *Handbuch IT-Management: Konzepte, Methoden, Lösungen und Arbeitshilfen für die Praxis* (8th ed.). Hanser.
- Urbach, N., & Ahlemann, F. (2019). *IT management in the digital age: A roadmap for the IT department of the future*. Springer. https://doi.org/10.1007/978-3-319-96187-3
