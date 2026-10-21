---
course: IT Management and EAM
session: 12
title: Business Model Transformation and Business–IT Alignment
subtitle: Digital business models · business capabilities and capability maps · heat maps and capability-based planning · value streams · EA as an enabler of transformation
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# Business Model Transformation and Business–IT Alignment {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · business models and digital transformation 20 min · mini exercise "how far does the change go?" 10 min · break 10 min · business capabilities and the capability map 20 min · mini exercise "capability or not?" 10 min · heat maps, capability-based planning and value streams 20 min · EA as an enabler, alignment revisited 10 min · case exercise capability map 45 min · wrap-up 5 min · ~20 min buffer.
Session 11 ended with a first data collection plan for Rhein-Neckar Mobil Group; its lean meta-model already contained the element type *business capability*, but nobody had filled it. Today fills it: the capability map is the business layer that connects the strategy (the new business model of the mobility app) with the application landscape. This session covers the module content "business model transformation, business–IT alignment" and the overarching competence "understand why EAM is needed as a basis for developing digital business models".
Source note for the lecturer: Hanschke (2023) treats business capability management in section 7.4.1 and the procedure for building a capability map in 7.4.2.1; the usage scenario "Business Capability Management & Business Architecture 4 Digitalization" is section 6.14, digital strategy and digital transformation section 6.22 (section numbers checked against the table of contents of the 4th edition; check the text in the library copy before quoting). The TOGAF series guides on business capabilities and value streams are published together in The Open Group (2022), "Business architecture"; the slides describe their ideas in own words only. Osterwalder and Pigneur (2010) published the Business Model Canvas; the slides only name its nine building blocks. All capability maps, ratings and figures are own examples.
:::

---

# Today's Agenda

1. Recap: what must your company be able to do?
2. Business models and digital transformation
3. Business capabilities and the capability map
4. Using the map: heat maps, application mapping, capability-based planning
5. Value streams
6. EA as an enabler of transformation — alignment revisited
7. Case exercise: build a capability map for Rhein-Neckar Mobil Group

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Business models and digital transformation (input) · 0:30 Mini exercise "how far does the change go?" (pairs) · 0:40 Break · 0:50 Capabilities and the capability map (input) · 1:10 Mini exercise "capability or not?" (pairs) · 1:20 Heat maps, application mapping, capability-based planning, value streams (input) · 1:40 EA as an enabler, alignment revisited (input + discussion) · 1:50 Case exercise (groups + plenary) · 2:35 Wrap-up · ~20 min buffer.
If the session runs long: "Four digital business models", "Value streams and processes" and "Limits of capability maps" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: What Must Your Company Be Able to Do?

You were asked to list about ten things your training company **must be able to do** to earn its money — without naming departments or systems.

- Which items on your list are **the same** across very different companies?
- Which items make **your** company special?
- Where did you slip into a **department**, a **process step** or a **system** name?

::: notes
Pairs for 3 min, then collect on the board. Typical lists: manage customers, develop products, purchase materials, produce, sell, deliver, invoice, manage staff, manage finances — plus one or two special items (e.g. "certify medical products", "manage a dealer network"). Typical slips: "sales department" (organisation unit), "enter orders in SAP" (process step plus system), "do the monthly closing" (process). Keep the board: the generic items will become the supporting capabilities, the special ones the core capabilities — and the slips show exactly the difference between capability, unit, process and application that today's session makes precise.
:::

---

# Business Models and Digital Transformation {.section}

What changes when a business model goes digital

---

# What Is a Business Model?

::: callout
A **business model** describes how an enterprise **creates** value for customers, **delivers** it and **captures** a share of it as revenue and profit.
:::

| Building blocks of the Business Model Canvas | Rhein-Neckar Mobil Group today (bus and rail) |
|---|---|
| Customer segments · value propositions | Commuters, pupils, occasional travellers · reliable regional transport |
| Channels · customer relationships | Ticket devices on board, transport association app · mostly anonymous |
| Revenue streams | Ticket sales, subscriptions, revenue share from the association, public contracts |
| Key resources · key activities · key partners | Buses, trains, drivers · operating the timetable · transport association, payment provider |
| Cost structure | Staff, energy, vehicles, maintenance |

::: source
Definition based on Teece (2010); building blocks from Osterwalder and Pigneur (2010); own example.
:::

::: notes
Teece (2010) describes the business model as the design of the mechanisms by which a firm creates, delivers and captures value — and stresses that the business model is not the same as the strategy: strategy decides how to compete, the business model is the logic of how the firm makes money. Osterwalder and Pigneur's canvas has nine building blocks (customer segments, value propositions, channels, customer relationships, revenue streams, key resources, key activities, key partnerships, cost structure); here paired to save space. Ask: which building blocks would change with the joint mobility app? (Channels: own app; relationships: from anonymous to a customer account; value proposition: one app for all modes; revenue streams: possibly new pricing; partners: car sharing integrated, maybe other mobility providers.) That is the case at the end of the session.
:::

---

# Digitisation, Digitalisation, Digital Transformation

| Term | What changes | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **Digitisation** | Information from analogue to digital | Paper timetables become PDF files |
| **Digitalisation** | Processes use digital technology | Ticket devices upload sales every 15 minutes instead of drivers handing in paper lists |
| **Digital transformation** | The **value proposition** and the **business model** change | One app and one account for bus, rail, car sharing and partner services |

::: callout
Digital transformation is a **process** in which digital technologies trigger **significant changes** to an organisation — in strategy, structure, processes and culture.
:::

::: source
Own wording and examples based on Vial (2019).
:::

::: notes
Vial (2019) reviewed the research literature on digital transformation and proposed a definition: a process that aims to improve an entity by triggering significant changes to its properties through combinations of information, computing, communication and connectivity technologies. He also points out the "building blocks": digital technologies disrupt customer behaviour and competition, firms respond with digital business strategies, use digital technologies to change value creation paths, and must manage structural changes and organisational barriers. The three-step distinction (digitisation/digitalisation/transformation) is common in practice and literature; the terms are not used consistently, so in the exam students should explain what they mean rather than rely on the word alone. Link to session 1: the strategic impact grid — the more IT changes the business model, the more strategic the role of IT.
:::

---

# Four Digital Business Models {.optional}

| | **Value chain** (own products and processes) | **Ecosystem** (own and partners' offers) |
|---|---|---|
| **Deep knowledge of end customers** | **Omnichannel**: one customer experience across all channels | **Ecosystem driver**: a platform that the customer starts from, with offers of many partners |
| **Little knowledge of end customers** | **Supplier**: sells through others, e.g. through an intermediary's app | **Modular producer**: a plug-and-play product or service used in many ecosystems |

- Today, bus and rail tickets are sold largely through the **association's app**: a supplier position
- The mobility app moves the group towards **omnichannel**; opening it to partners would move it towards **ecosystem driver**

::: source
Own wording based on Weill and Woerner (2018).
:::

::: notes
Self-study. Weill and Woerner (2018) classify digital business models along two dimensions: how much a firm knows about its end customers, and whether it operates in its own value chain or in an ecosystem of partners. They argue that digital competition pushes firms to know more about their end customers and to decide which role to play in ecosystems. Examples (in own words): a manufacturer selling through retailers is a supplier; a bank with a seamless customer experience across branch, web and app is omnichannel; a payment service integrated into many shops is a modular producer; a platform where customers find offers of many providers is an ecosystem driver. For the mobility app: the group would collect customer accounts for the first time — a strategic asset and a GDPR topic (session 7).
:::

---

# Digital Business Strategy and Alignment

::: columns
**Session 2: alignment**

- Business strategy and IT strategy must **fit**, vertically and horizontally
- Four perspectives; in two of them, **IT drives** the business strategy (competitive potential, service level)
|||
**Digital business: fusion**

- In digital business models, IT **is part of the product**: the app *is* the customer channel
- Business and IT strategy merge into one **digital business strategy**
- The question shifts from "does IT support the strategy?" to "**what can we do differently** with digital technology?"
:::

::: callout
EAM provides the **shared picture** that both sides need for this: what the enterprise can do today, and what it must be able to do tomorrow.
:::

::: source
Own wording based on Henderson and Venkatraman (1993) and Bharadwaj et al. (2013).
:::

::: notes
Bharadwaj et al. (2013) argue that the traditional view of IT strategy as a functional strategy aligned with, but subordinate to, the business strategy no longer fits digital business; they call for a fusion of the two into a digital business strategy. Henderson and Venkatraman's competitive potential perspective (session 2) already described IT shaping the business strategy. The mobility app is a typical example: the business model (one account, one payment) can only be defined together with the architecture (customer master data, interfaces, payment). The bridge between the two is the business architecture — capabilities and value streams — which is the rest of today's session.
:::

---

# Mini Exercise: How Far Does the Change Go? {.exercise}

Is each change at *Rhein-Neckar Mobil Group* **digitisation**, **digitalisation** or **digital transformation**? Which **canvas building blocks** change?

1. Driver duty rosters are no longer printed but shown in a staff app.
2. Sensor data from the buses predict when brakes need repair; breakdowns fall by 20 %.
3. The mobility app offers one monthly fee for buses, trains and 10 hours of car sharing.
4. Customers can rent e-bikes from a city partner in the mobility app; the group earns a commission.
5. Scanned vehicle maintenance records are stored as PDF files in the archive.

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 digitalisation of a process (rostering), with digitisation as a precondition; no building block changes, except perhaps key activities. 2 digitalisation (predictive maintenance improves a key activity and the cost structure); it becomes a business model change only if the group sold the prediction as a service to other operators. 3 digital transformation: new value proposition and revenue stream (bundle price), new customer relationship (account), channel (own app). 4 digital transformation towards an ecosystem: key partners, new revenue stream (commission), value proposition widened — Weill and Woerner's ecosystem driver. 5 digitisation. Lesson: the same technology (an app, sensors) can serve digitalisation or transformation; what counts is whether the value proposition and the way money is earned change.
:::

---

# Business Capabilities {.section}

What the enterprise must be able to do

---

# What Is a Business Capability?

::: callout
A **business capability** is an ability of the enterprise to **achieve a specific purpose** — it describes **what** the enterprise does, not **how**, **where** or **by whom**.
:::

::: columns
**Properties**

- **Stable**: changes far less often than processes, organisation or systems
- **Realised** by people, processes, information and technology
- **Named** with a business object and an activity, e.g. *fare management*, *customer management*
|||
**Why it matters for EA**

- A **common language** for business and IT, independent of the org chart
- The anchor to map **processes, units, applications and projects** to
- The level at which the board can discuss **investment**
:::

::: source
Own wording based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
The Open Group's guide to business capabilities stresses that a capability is the "what", not the "how, why or where"; capabilities can exist today or be needed for a future strategy; they are realised by a combination of people, processes, information and resources; and they are named with a noun–verb pattern (business object + activity) that the business recognises. Hanschke (2023) describes capability maps as the core of the business architecture and as the bridge between strategy and IT landscape (sections 7.4.1, 6.14). Example of stability: the group has had to manage fares for decades — paper tickets, ticket machines, devices, app — the capability is the same, its realisation changed many times. In session 10 the capability was only a term; in session 11's lean meta-model a process realises a capability.
:::

---

# Capability, Process, Unit, Application

| Element | Answers | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **Business capability** | *What* must we be able to do? | Fare management |
| **Business process** | *How*, in which steps? | Introduce a new fare zone: decide, configure, test, roll out to devices |
| **Organisation unit** | *Who* is responsible? | Sales and fares department of the bus and rail unit |
| **Application** | *With which software*? | Fare back-end, ticket device software |

- One capability is supported by **several** processes, units and applications — and vice versa
- **Test**: if a reorganisation or a new system would rename it, it is not a capability

::: source
Own wording and examples based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
This is the most important distinction of the session and a typical exam question. The Open Group's guide warns against copying the organisation chart into the capability map: organisations change often, the capability map should not. Ask students to check their preparation lists with the test: "sales department" fails, "sell products" or "sales management" passes; "enter orders in SAP" fails twice (process step and system). Link to the meta-model of session 11: *organisation unit performs process*, *process realises capability*, *application supports process* — so applications can be mapped to capabilities via the processes or directly.
:::

---

# The Capability Map

![Level-1 business capability map of Rhein-Neckar Mobil Group in three tiers: strategic capabilities strategy and business development, network and timetable planning, partner management, risk and compliance management; core capabilities customer management, product and fare management, sales and ticketing, vehicle sharing management, fleet maintenance, customer service, payment and revenue management, transport operations; supporting capabilities financial management, procurement, human resources management, IT and information management. Transport operations is broken down into four level-2 capabilities: duty and vehicle scheduling, dispatching and operations control, passenger information, incident handling in operations](img/eam-capability-map.png){width=92%}

::: source
Own illustration based on Hanschke (2023) and The Open Group (2022); own example.
:::

::: notes
Walk through: the map fits on one page — that is its strength. Three tiers are a common grouping: strategic (steering the enterprise), core (customer-facing, where the enterprise earns its money and differentiates), supporting (needed by every enterprise). Level 1 has typically 10–30 capabilities, each broken down into level 2 (and sometimes level 3); The Open Group's guide speaks of 20 to 30 top-level capabilities for a starter map and of three to six levels in a full decomposition — for most decisions two levels are enough. Ask: which capabilities are the same as those of Kurpfalz Sanitär (session 2)? The supporting tier is almost identical; the core tier is where the businesses differ. Note "vehicle sharing management" rather than "car-sharing unit" — the capability survives a reorganisation.
:::

---

# Building a Capability Map

1. **Collect input**: business model and strategy, existing reference maps for the industry, process maps, the organisation chart — as a checklist, not as a template
2. **Draft level 1** with a small team: top-down from the business model, bottom-up from processes and lists like your preparation task
3. **Detail level 2** for the capabilities that matter for the current decisions
4. **Review in workshops** with business owners: names, gaps, overlaps
5. **Define rules**: naming, levels, one owner per capability; publish the map as the common reference

::: callout
A capability map is **never finished** — but it should be **good enough after a few weeks**, not a few years.
:::

::: source
Own wording based on Hanschke (2023) and The Open Group (2022).
:::

::: notes
Hanschke (2023) describes the procedure for creating a capability map in section 7.4.2.1; The Open Group's guide lists the business model, the organisation structure and strategic and financial plans as typical inputs and recommends combining top-down and bottom-up. Practical tips: start with a reference model for the industry if one exists (many EAM tools ship generic reference maps), but rename everything into the company's language; a map with more than about 30 level-1 boxes is too detailed for the board; avoid "other" boxes. Link to session 11: workshops are the method of choice for cross-unit maps; the prepared draft is corrected, not drawn from scratch. Each capability gets a business owner — the person who can rate it in a heat map.
:::

---

# Mini Exercise: Capability or Not? {.exercise}

Is each item a **business capability**? If not, say **what it is** and suggest a capability name.

::: columns
1. Customer management
2. Car-sharing unit
3. Unlock a car
4. Fare back-end
5. Revenue sharing with the transport association
|||
6. Sell ticket on board
7. Post on social media every day
8. Vehicle maintenance
9. Driver recruitment
:::

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 capability; 2 organisation unit → "vehicle sharing management"; 3 process step (or a function of the app) → part of "vehicle sharing management"; 4 application → it supports "product and fare management" and "payment and revenue management"; 5 capability if phrased as an ability, e.g. "revenue sharing" as a level-2 capability under "payment and revenue management" — the session 10 figure showed it as a process; good discussion: the same words can name a process ("share revenue with the association each month") or a capability ("revenue sharing"), the test is what vs. how; 6 process (or a value stream stage) → capability "sales and ticketing"; 7 activity, too specific → capability "marketing management" (missing on our map — good catch); 8 ambiguous: it is also the name of a unit — fine as a capability ("fleet maintenance"), but make sure it is not just copied from the org chart; 9 level-2 capability under "human resources management". Lesson: names alone do not decide — the what/how test does.
:::

---

# Using the Capability Map {.section}

Heat maps, application mapping and capability-based planning

---

# Heat Maps: One Map, Many Lenses

![The level-1 capability map of Rhein-Neckar Mobil Group as a heat map with the lens IT support today: customer management and customer service are weak; partner management, risk and compliance management, sales and ticketing, fleet maintenance, payment and revenue management, financial management and procurement are partial or redundant; the other capabilities are good](img/eam-capability-heatmap.png){width=86%}

- Other lenses: **strategic importance**, **maturity gap**, **cost**, **number of applications**, **risk**, **planned investment**

::: source
Own illustration based on Hanschke (2023) and The Open Group (2022); own example ratings.
:::

::: notes
A heat map colours the same map by one attribute — here the IT support today, rated by the architecture team together with the capability owners. Reading it: customer management is weak because customer data sit in three places (car-sharing database, ERP subscriptions, association app — session 10); customer service is split per unit; financial management and procurement are "redundant" because three ERP systems do the same job. The power comes from combining two lenses: a capability with high strategic importance and weak IT support is an investment candidate; low importance and high cost is a candidate for standardisation or outsourcing (session 15). The Open Group's guide describes heat maps with traffic-light scales and lenses such as maturity, performance, cost and strategic contribution. Warning: ratings are judgements — document who rated and on which basis, otherwise the heat map becomes a political tool.
:::

---

# Mapping Applications to Capabilities

| Capability | Applications today | Finding |
|---|---|---|
| Customer management | Car-sharing customer database, subscription module in the bus and rail ERP, transport association app | **Fragmented**: no group-wide customer |
| Financial management | Three ERP systems | **Redundant**: candidate for the one cloud ERP |
| Vehicle sharing management | Car-sharing app and back-end | **Good**, cloud-based, modern |
| Mobility account (new) | — | **Gap**: needed for the mobility app |

- Shows **redundancy**, **gaps** and **fragmentation** at a glance
- The basis for the **landscape maps** and the **application portfolio** of session 13

::: source
Own example based on Hanschke (2023).
:::

::: notes
Hanschke (2023) uses capabilities (or business domains) as one axis of the landscape map ("Bebauungsplan"); session 13 builds such maps. The table form is enough for today. Key insight: the same table answers different stakeholders — the CFO sees redundancy (cost), the CEO sees the gap for the strategic project, the CIO sees where to consolidate. "Mobility account" is a capability the group does not have yet; The Open Group's guide suggests marking such wanted-but-missing capabilities in a separate colour. Note the link to the data architecture: "fragmented customer management" is the same problem as "no leading system for the business object customer" (session 10).
:::

---

# Capability-Based Planning

::: layers
- Strategy: Goals and business model, e.g. one app and one account for all mobility services by 2028
- Capabilities: Which capabilities must be built, improved or consolidated? Target maturity per capability
- Initiatives: Projects and changes per capability: processes, organisation, data, applications, technology
- Roadmap: Sequence, dependencies, budget; reviewed in the project portfolio
:::

::: callout
Investments are discussed **per capability**, not per system: "we improve customer management" instead of "we buy a CRM".
:::

::: source
Own illustration based on The Open Group (2022) and Hanschke (2023).
:::

::: notes
Capability-based planning links strategic goals with investments: each initiative must name the capabilities it improves and how much. The Open Group's guide describes capabilities as the link between strategy and the portfolio of initiatives; Hanschke (2023) lists capability-based planning as a usage scenario of EAM. Benefits: the board can compare investments across units; duplicate projects for the same capability become visible; IT projects are justified with a business outcome. Link to session 4: the IT project portfolio and business cases; link to session 13: target landscape and roadmap; link to session 2: this is "strategy execution" and "technology transformation" made concrete.
:::

---

# Value Streams {.section}

How the enterprise delivers value to a stakeholder

---

# Value Streams

![Value stream subscribe to a monthly ticket with the stakeholder customer and the value of travelling all month with one ticket. Five stages: apply for a subscription, check and conclude contract, issue ticket, collect monthly payments, change or cancel. Enabling capabilities below each stage: customer management and sales and ticketing; customer management and product and fare management; sales and ticketing; payment and revenue management; customer service and customer management. Customer management enables three stages and is marked as critical](img/eam-value-stream.png){width=90%}

- A **value stream** is the end-to-end sequence of **stages** that delivers a result of value to a **stakeholder**
- Cross-mapping stages to capabilities shows which capabilities are **critical** for the customer experience

::: source
Own illustration based on The Open Group (2022); own example.
:::

::: notes
The Open Group's guide to value streams describes a value stream as an end-to-end set of value-adding stages that produces an outcome for a stakeholder (customer, end user, partner); each stage is enabled by one or more capabilities. The cross-mapping explains why capabilities matter: customer management enables three of five stages of this value stream — combined with the heat map ("weak"), it is the most urgent capability for any customer-facing change. Capabilities that appear in no important value stream are candidates for standardisation. Value streams and capabilities are developed together: the value stream gives the stakeholder context, the capability map the structure.
:::

---

# Value Streams and Processes {.optional}

| | **Value stream** | **Business process** |
|---|---|---|
| Perspective | The **stakeholder's** view of value received | The **enterprise's** view of work done |
| Granularity | A few stages, end to end | Detailed steps, roles, rules, systems |
| Stability | Stable, like capabilities | Changes with organisation and systems |
| Use | Strategy, capability prioritisation, customer journey | Process design, automation, controls |

::: source
Own comparison based on The Open Group (2022).
:::

::: notes
Self-study. A value stream stage such as "check and conclude contract" may be realised by several processes (credit check, data entry, contract dispatch) in different units. Link to session 5: ITIL 4 also uses "value streams" — combinations of value chain activities that create a service outcome; the idea is the same (end-to-end view of value), the scope differs (service management vs. whole enterprise). The term is also used in lean management (value stream mapping) with a more process-oriented meaning — students should say which meaning they use.
:::

---

# EA as an Enabler of Transformation {.section}

From the business model to the landscape

---

# From Business Model to IT Landscape

::: layers
- Strategy and business model: New value proposition, channels, partners, revenue streams — e.g. one app and one account for all mobility services
- Business architecture: Capabilities to build or improve, value streams to redesign — e.g. customer management, a new mobility account
- Data and application architecture: A leading system for each business object, applications and interfaces — e.g. one customer master, APIs to car sharing and the association
- Technology architecture: Platforms and hosting — e.g. cloud platform, API gateway, connection to the data centres
:::

::: source
Own illustration based on The Open Group (2022) and Ross et al. (2006).
:::

::: notes
The layers repeat the four domains of session 10 (with data and applications combined), and today's addition sits on top: the business model and the capabilities. EA enables transformation by making the chain traceable in both directions — top-down (which capabilities, data and applications does the new business model need?) and bottom-up (which new business models do our platforms make possible — e.g. the car-sharing platform's API gateway could also serve partners). Ross et al. (2006): the operating model decides what must be shared — the mobility app needs at least coordination (shared customer and payment data across units).
:::

---

# What EAM Contributes to a Transformation

| Phase | EAM contribution | Session |
|---|---|---|
| Strategy development | Capability map, heat maps: where are we strong, where are gaps? | 12 |
| Target picture | Target capabilities, target landscape, architecture principles | 12, 13 |
| Planning | Roadmap, impact analysis, sourcing options, integration design | 13–15 |
| Implementation | Architecture reviews of projects; standards; governance | 16 |
| Monitoring | Progress per capability; update of the as-is | 11, 18 |

::: callout
EAM turns a business model idea into a **sequence of changes** that the enterprise can actually carry out — and shows **what it costs** and **what it touches**.
:::

::: source
Own summary based on Hanschke (2023) and Ahlemann et al. (2012).
:::

::: notes
Hanschke (2023) describes digital strategy and digital transformation as a usage scenario of EAM (section 6.22); Ahlemann et al. (2012) emphasise that EAM creates value only when it is embedded in strategic planning and in the project life cycle. The table is also the map of the rest of Part B. Typical failure without EAM: the app project builds its own customer database — a fourth one — because nobody saw that customer management was already fragmented. Ask: who in your training company would produce the capability map — strategy department, enterprise architects, business process management?
:::

---

# Limits of Capability Maps {.optional}

- **Abstract**: a map of 20 boxes says little until it is linked to processes, applications and investments
- **Subjective ratings**: heat maps can be bent to support a decision already taken
- **Effort**: maps drawn once for a strategy workshop and never maintained age quickly
- **Language**: business units may see it as "IT's map" if they are not involved in naming

::: source
Own wording based on Hanschke (2023) and The Open Group (2022).
:::

::: notes
Self-study. Countermeasures: link capabilities to the repository (session 11 meta-model), document the rating criteria and raters, assign capability owners and review the map yearly with the strategy process, build the map in workshops with the business. Exam point: be able to name strengths and limits of an instrument, not just describe it.
:::

---

# Case Exercise: A Capability Map for the Mobility App {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–11): 3,200 employees, €410 million turnover; units bus and rail, car sharing (120,000 customers), vehicle maintenance. The architecture team now has a first application list of about 180 applications (session 11).

- The **joint mobility app** is to offer one account and one payment for bus, regional train and car sharing
- The board also discusses opening the app to **partners**: e-bikes of a city partner, parking garages, the long-distance train operator
- Bus and rail tickets are sold on board and through the **transport association's app**; customer data are held in three places
- Three ERP systems; card payments via an external payment provider; car sharing has its own app and API gateway at a cloud provider

::: notes
Read the case together (2 min). Hints if asked: the CEO's goal is "the mobility platform of the region"; the transport association is a partner, not a competitor, but it owns its app and its customers; the works council and the data protection officer must be involved in any customer account (session 7). The partners and their roles are own example facts. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. Which **building blocks** of the business model change with the mobility app — and which with the partner platform? Name the digital business model **today** and **in the target**.
2. Build a **level-1 capability map** (strategic, core, supporting; 12–20 capabilities). Add **level 2** for two core capabilities that the app needs most.
3. Draw a **value stream** "travel with the mobility app" with 4–6 stages and the enabling capabilities.
4. Create a **heat map** with the lens "importance for the mobility app" and compare it with today's IT support. Which **three capabilities** need investment first?
5. Which **applications** support these three capabilities today? Name one **redundancy**, one **gap** and one next step for the architecture team.

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 Mobility app: value proposition (one account, one payment, all modes), channels (own app instead of the association's app for some sales), customer relationships (from anonymous to registered accounts), revenue streams (possibly bundles or best-price billing), key activities (app operation, customer data management). Partner platform: key partners (city, parking, long-distance operator), revenue streams (commissions), value proposition (door to door). Digital business model: today supplier for bus and rail tickets (association app), omnichannel-like in car sharing; target omnichannel, with partners ecosystem driver (Weill and Woerner, optional slide).
2 E.g. strategic: strategy and business development, network and timetable planning, partner management, risk and compliance management; core: customer management, product and fare management, sales and ticketing, vehicle sharing management, transport operations, fleet maintenance, customer service, payment and revenue management, partner integration or mobility platform management (new); supporting: financial management, procurement, HR management, IT and information management, marketing management. Level 2, e.g. customer management: customer registration and identification, customer account management, consent and privacy management, customer data analytics; payment and revenue management: payment processing, billing and best-price calculation, revenue sharing, receivables management. Check names with the what/how test and that no unit or system names appear.
3 E.g. register/log in → plan journey → buy ticket or book vehicle → travel (check-in, unlock) → pay and settle → get support; capabilities: customer management (register, pay, support), network and timetable planning / passenger information (plan), sales and ticketing, vehicle sharing management (book, unlock), transport operations (travel), payment and revenue management (pay; revenue sharing with association and partners), customer service, partner integration.
4 Highest importance and weak today: customer management, payment and revenue management, partner integration (new, does not exist) — also accept customer service or sales and ticketing with reasoning.
5 Customer management: car-sharing customer database, ERP subscription module, association app → fragmented (redundancy); payment: payment provider for on-board cards and a separate payment path in the car-sharing app → two paths (redundancy); partner integration: no application, the API gateway of car sharing as a possible base → gap. Next steps: define a leading system for the customer (target data architecture), a target landscape and roadmap (session 13), an integration design via APIs (session 14), sourcing options for a mobility platform (session 15), present the heat map to the board for capability-based investment decisions.
:::

---

# Key Takeaways

- A **business model** describes how an enterprise creates, delivers and captures value; **digital transformation** changes it — not just the processes
- In digital business, business and IT strategy **merge**; EAM gives both sides a shared picture
- A **business capability** says **what** the enterprise must be able to do — stable, independent of units, processes and systems; the **capability map** shows them in levels and tiers
- **Heat maps**, application mapping and **value streams** turn the map into a planning tool: capability-based planning links strategy, investments and the IT landscape

---

# Next Session: Strategic Planning of the IT Landscape

- As-is and to-be landscapes; landscape maps
- Application portfolio management, e.g. the TIME model
- Roadmaps and transformation planning

::: callout
**Preparation:** pick three applications of your training company and find out for each: how **old** is it, how **satisfied** are its users, and is a **replacement** planned?
:::

::: notes
The preparation task prepares the application portfolio assessment of session 13 (business value and technical fitness). Today's capability map becomes one axis of the landscape map next time.
:::

---

# References {.references}

- Ahlemann, F., Stettiner, E., Messerschmidt, M., & Legner, C. (Eds.). (2012). *Strategic enterprise architecture management: Challenges, best practices, and future developments*. Springer. https://doi.org/10.1007/978-3-642-24223-6
- Bharadwaj, A., El Sawy, O. A., Pavlou, P. A., & Venkatraman, N. (2013). Digital business strategy: Toward a next generation of insights. *MIS Quarterly, 37*(2), 471–482.
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Henderson, J. C., & Venkatraman, N. (1993). Strategic alignment: Leveraging information technology for transforming organizations. *IBM Systems Journal, 32*(1), 4–16.
- Osterwalder, A., & Pigneur, Y. (2010). *Business model generation: A handbook for visionaries, game changers, and challengers*. Wiley.
- Ross, J. W., Weill, P., & Robertson, D. C. (2006). *Enterprise architecture as strategy: Creating a foundation for business execution*. Harvard Business School Press.
- Teece, D. J. (2010). Business models, business strategy and innovation. *Long Range Planning, 43*(2–3), 172–194. https://doi.org/10.1016/j.lrp.2009.07.003
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Business architecture*. Van Haren Publishing.
- Vial, G. (2019). Understanding digital transformation: A review and a research agenda. *Journal of Strategic Information Systems, 28*(2), 118–144.
- Weill, P., & Woerner, S. L. (2018). *What's your digital business model? Six questions to help you build the next-generation enterprise*. Harvard Business Review Press.

TOGAF® is a registered trademark of The Open Group. Diagrams in this deck are own illustrations. Standards and frameworks are described in own words.
