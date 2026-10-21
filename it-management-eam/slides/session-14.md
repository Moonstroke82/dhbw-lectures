---
course: IT Management and EAM
session: 14
title: Enterprise Application Integration
subtitle: Integrated information processing · integration styles and patterns · point-to-point vs. middleware · ESB, APIs, event-driven integration and iPaaS
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

# Enterprise Application Integration {.title}

::: notes
Time plan for today (3 h): recap of the preparation task 10 min · why integrate, integrated information processing, what EAI is 15 min · integration styles 10 min · break 10 min · point-to-point vs. middleware, integration patterns 20 min · mini exercise "count and choose" 10 min · ESB, APIs, events, iPaaS, integration in EAM 25 min · mini exercise "which integration approach?" 10 min · case exercise integration architecture 45 min · wrap-up 5 min · ~20 min buffer.
Session 13 planned the landscape of Rhein-Neckar Mobil Group and put an "API platform" on the roadmap; its landscape map deliberately left out the interfaces. Today is about the lines between the boxes: how applications exchange data and functions, and how an enterprise designs this as an integration architecture. This covers the module content "integrated information processing — Enterprise Application Integration (EAI)" and the methodological competence of selecting suitable methods for managing the IT landscape.
Source note for the lecturer: "integrated information processing" (integrierte Informationsverarbeitung) follows Mertens (2013), section 1.1, which describes the integration dimensions object, direction, reach, degree of automation and timing (checked in the publisher's sample of the 18th edition; only the objects are explained in the text, the other dimensions appear in figure 1.1/1). The four integration styles and the pattern names come from Hohpe and Woolf (2004) — the book appeared in October 2003 with copyright 2004; APA uses the copyright year. The ESB follows Chappell (2004), REST Fielding (2000), iPaaS the BISE catchword article by Ebert et al. (2017). Hanschke (2023) describes the information flow chart ("Informationsfluss-Grafik") in section 5.5.5. All diagrams and RNM interface figures are own examples; product names are not needed for the exam.
:::

---

# Today's Agenda

1. Recap: how do your applications exchange data?
2. Integrated information processing and EAI
3. Integration styles
4. Point-to-point vs. middleware; integration patterns
5. ESB, APIs, event-driven integration and iPaaS
6. Case exercise: design an integration architecture for Rhein-Neckar Mobil Group

::: notes
Time and format guide (not shown to students):
0:00 Recap of preparation task (pairs + plenary) · 0:10 Why integrate, integrated information processing, EAI (input) · 0:25 Integration styles (input) · 0:35 Break · 0:45 Point-to-point vs. middleware, patterns (input) · 1:05 Mini exercise "count and choose" (pairs) · 1:15 ESB, APIs, events, iPaaS, integration in EAM (input) · 1:40 Mini exercise "which integration approach?" (pairs) · 1:50 Case exercise (groups + plenary) · 2:35 Wrap-up · ~20 min buffer.
If the session runs long: "Canonical Data Model", "Choosing a Style: The Criteria" and "Integration Anti-Patterns" are optional and move to self-study. Keep the case exercise; it is the session's exam-style exercise.
:::

---

# Recap: How Do Your Applications Exchange Data?

You were asked to follow one **business process** of your training company and find out which **applications** exchange data along it — and **how**.

- How many **applications** did the process touch?
- Where did you find **file transfer**, a **direct interface**, **middleware** — or **manual re-entry**?
- What happens when one of these connections **fails**? Who notices first?

::: notes
Pairs for 3 min, then collect on the board: process · applications · type of connection. Typical findings: order-to-cash touches a shop, an ERP, a warehouse system, a payment provider and a carrier portal; there is at least one nightly CSV file, one "the interface team" nobody can explain, and one Excel sheet that somebody copies by hand. Ask who owns an interface — the sender, the receiver or nobody? Mark every manual step as a "media break" (Medienbruch): it is where data are retyped, delayed and corrupted. Keep the board: today's styles (file, shared database, call, message) can be matched to the findings later.
:::

---

# Integrated Information Processing {.section}

Why applications must work together

---

# Why Integrate?

::: columns
**Islands of applications**

- Data are **re-entered** by hand — media breaks, typing errors
- The same customer exists in **several systems**, in different versions
- Information arrives **late**, e.g. revenue figures once a month
- Processes stop at **system borders**
|||
**Integrated information processing**

- Data are captured **once** and used by every application that needs them
- **Leading systems** keep the master data; others receive copies or ask
- Processes run **across** applications, units and partners
- New offers combine existing **functions**, e.g. the mobility app
:::

::: callout
Example: a passenger cancels a subscription in the app — the customer account, the ERP subscription module, the fare back-end and the payment provider must all know it.
:::

::: source
Own wording based on Mertens (2013).
:::

::: notes
Mertens (2013) describes integrated information processing as the goal of linking data, functions and processes so that information captured once serves the whole enterprise. Link to session 10: the data architecture rule "one leading system per business object, everything else gets copies via interfaces" — today is about the "via interfaces". Link to session 12: the mobility app is a new business model built almost entirely from existing functions (customer, fare, car sharing, partners). Ask: in the subscription example, what goes wrong if one of the four applications does not learn about the cancellation? (Ticket stays valid, money is still collected — a complaint and a GDPR question.)
:::

---

# Dimensions of Integration

| Dimension | Forms | Example at Rhein-Neckar Mobil Group |
|---|---|---|
| **Object** | Data, functions, processes, methods, programs | Customer data shared; "check fare" called by the app |
| **Direction** | Horizontal (along the value chain), vertical (operations → planning and control) | Ticket sale → revenue sharing; sales → management reporting |
| **Reach** | Within an area, across functions and processes, enterprise-wide, between companies | Bus and rail only; group-wide account; partner offers |
| **Degree of automation** | Full or partial automation | Revenue posting automatic; complaint routed to a person |
| **Timing** | Batch or real time | Nightly file vs. live seat availability |

::: source
Own wording based on Mertens (2013, section 1.1).
:::

::: notes
Mertens (2013, section 1.1) structures the forms of integrated information processing in these dimensions. Data integration means data are logically combined, either by automatic transfer between applications or by a shared database; function integration links functions; process integration links activities into a continuous flow. Exam point: use the dimensions to describe an integration need precisely — "horizontal, inter-company, real-time data integration with the e-bike partner" says much more than "we need an interface". The partners come from session 12 (e-bike city partner, parking garages, long-distance operator).
:::

---

# What Is Enterprise Application Integration?

::: callout
**Enterprise Application Integration (EAI)** connects the applications of an enterprise — and of its partners — through a **planned integration architecture** and **middleware**, so that they share data and functions without re-entry and without each pair needing its own interface.
:::

- Became a topic around **2000**: ERP and best-of-breed systems, e-commerce, supply chains — linked by a growing number of point-to-point interfaces
- Today's drivers: **apps and digital channels**, **SaaS** in many units, **partner ecosystems**, **mergers**
- The **operating model** sets how much integration is needed: coordination and unification need shared data

::: source
Own wording based on Ebert et al. (2017), Hohpe and Woolf (2004) and Ross et al. (2006).
:::

::: notes
Ebert et al. (2017) describe how IT departments began to speak of EAI around 2000 because standalone applications were linked through many point-to-point interfaces, which made landscapes complex and slowed down new needs such as marketplaces and supply chain management. Link to session 10: Ross et al. (2006) — the operating model sets the degree of data integration across units. RNM moves from diversification towards coordination: shared customer and payment data across units — that is an integration requirement. EAI is not a product; it is an architecture task supported by middleware products.
:::

---

# Four Integration Styles

| Style | How it works | Example | Watch out |
|---|---|---|---|
| **File transfer** | One application writes a file, another reads it | Nightly CSV from fare back-end to ERP | Late data, format changes break it |
| **Shared database** | Applications read and write the same database | Ticket devices and back-end on one database | Tight coupling, one schema for all |
| **Remote procedure invocation** | One application calls a function of another and waits | App asks the fare back-end for a price | Both must be up at the same time |
| **Messaging** | Applications exchange messages via a messaging system | Sales sent as messages to revenue sharing | Middleware needed, harder to test |

::: source
Own wording based on Hohpe and Woolf (2004).
:::

::: notes
Hohpe and Woolf (2004, chapter 2) describe these four styles and compare them; the rest of their book develops patterns for messaging. Today's API calls are a modern form of remote procedure invocation (request–reply over HTTP). Ask the class to match their preparation findings to the styles: the nightly CSV is file transfer; "the warehouse system reads the ERP tables directly" is a shared database (often an undocumented one); the shop calling the payment provider is remote invocation. File transfer is not "wrong": it is simple and robust and still fine for large, non-urgent data such as monthly reports — the question is whether the data timeliness fits the business need.
:::

---

# Choosing a Style: The Criteria {.optional}

- **Coupling**: can each application change without breaking the others?
- **Timeliness**: how fresh must the data be at the receiver?
- **Data or function**: is data shared, or is behaviour of another application used?
- **Asynchronicity**: may the sender continue while the receiver is down?
- **Data format**: do sender and receiver agree on a format, or is translation needed?
- **Effort and technology**: how much integration code and specialised middleware?

::: callout
No style is best in general — the criteria are weighed **per integration need**.
:::

::: source
Own wording based on Hohpe and Woolf (2004).
:::

::: notes
Self-study. Hohpe and Woolf (2004) introduce the styles with these decision criteria. Example: ticket device sales — timeliness of minutes, must work when the mobile network fails (asynchronous, store and forward) → messaging or file upload in batches; app price check — the customer waits, needs an answer now → synchronous call. Exam point: justify a style with two or three criteria rather than naming technologies.
:::

---

# Integration Architectures {.section}

From point-to-point to middleware

---

# Point-to-Point vs. Integration Platform

![Comparison of two integration architectures for six applications of Rhein-Neckar Mobil Group (fare back-end, ERP bus and rail, car-sharing back-end, customer database, payment provider, passenger information). Left: point-to-point, every pair of applications has its own interface, 15 interfaces. Right: an integration platform in the middle, each application has one connection to it, 6 connections](img/eai-p2p-vs-hub.png){width=88%}

::: source
Own illustration based on Hohpe and Woolf (2004); own example.
:::

::: notes
With n applications and an interface between every pair, there are n(n−1)/2 interfaces: 6 → 15, 20 → 190, 180 → 16,110. Real landscapes are not fully meshed, but they grow in this direction because each project adds "just one more interface". With a hub, each application connects once (n connections) and the platform handles routing and translation. Careful: "6 connections" does not mean less logic — the mappings still exist, they are now in one place where they can be seen, monitored and reused. The figure also shows the price: the platform is a central component that must be highly available (link to BCM, session 8).
:::

---

# Point-to-Point vs. Middleware

| Aspect | Point-to-point | Middleware (hub, bus, platform) |
|---|---|---|
| Start | Quick and cheap for the first interfaces | Investment in platform, skills and operation |
| Growth | Up to n(n−1)/2 interfaces | About one connection per application |
| Change | Replacing an application touches all its interfaces | Change the connection to the platform |
| Transparency | Interfaces hidden in applications | Interfaces visible, monitored in one place |
| Risk | Many small failure points | Central component: must be highly available |

::: callout
Point-to-point is fine for a **few, stable** interfaces; middleware pays off when the number of applications and **changes** grows.
:::

::: source
Own compilation based on Hohpe and Woolf (2004), Chappell (2004) and Ebert et al. (2017).
:::

::: notes
Middleware: software between applications that takes over transport, routing, transformation and monitoring. Historical forms: message-oriented middleware (queues), integration brokers ("EAI hub", hub-and-spoke), then the ESB. Link to session 13: replacing the ERP bus and rail ("migrate") is much cheaper if its interfaces run via a platform — the other applications do not notice the change. That is the main business argument for middleware: it makes the landscape changeable. Counter-argument from practice: a central platform team can become a bottleneck if every interface waits for it.
:::

---

# Integration Patterns

Patterns give integration problems a **common vocabulary**:

| Pattern | Problem it solves |
|---|---|
| **Point-to-point channel** | A message must be processed by exactly one receiver |
| **Publish-subscribe channel** | An event must reach every interested receiver |
| **Message translator** | Sender and receiver use different data formats |
| **Content-based router** | The receiver depends on the content, e.g. unit or region |
| **Idempotent receiver** | A message may arrive twice and must not be booked twice |
| **Dead letter channel** | Messages that cannot be delivered must not get lost |

::: source
Own wording based on Hohpe and Woolf (2004).
:::

::: notes
Hohpe and Woolf (2004) collect 65 patterns in categories such as channels, message construction, routing, transformation and endpoints; the names are now used in many integration products. The point here is not to memorise patterns but to see that integration has recurring problems with known solutions. Examples at RNM: content-based router — a complaint goes to the bus and rail or the car-sharing team; idempotent receiver — the ticket device resends a sale after a network loss, revenue sharing must not count it twice; dead letter channel — a sale with an unknown fare code is parked for checking, not dropped. Note the two meanings of "point-to-point": a point-to-point channel is a messaging pattern, point-to-point integration an architecture.
:::

---

# Canonical Data Model {.optional}

- Without a common format, each pair of applications needs its own **translation**
- A **canonical data model** defines one shared format for a business object, e.g. "customer" or "ticket sale"
- Each application translates only **to and from** this format
- Links to the **data architecture**: leading system and business object definitions (session 10)

::: callout
Trade-off: fewer translations — but agreeing on one "customer" for all units takes **governance** and time.
:::

::: source
Own wording based on Hohpe and Woolf (2004).
:::

::: notes
Self-study. Hohpe and Woolf (2004) describe the canonical data model as a pattern that reduces the number of translations when many applications exchange the same kind of data. In practice the hard part is not technical: bus and rail see a "customer" as a subscription holder, car sharing as a verified driver with a licence. A canonical model needs a business object owner (session 11 meta-model) and a change process. A common compromise: canonical models only for the most important business objects (customer, ticket sale, payment), point formats elsewhere.
:::

---

# Mini Exercise: Count and Choose {.exercise}

*Rhein-Neckar Mobil Group* wants to connect **eight** applications for the mobility app: customer database, fare back-end, car-sharing back-end, payment platform, passenger information, helpdesk SaaS, and the APIs of the e-bike partner and the parking garages.

1. How many interfaces would a **full point-to-point** mesh need? How many connections with a **hub**?
2. Choose an **integration style** for: (a) monthly revenue report to the transport association, (b) price check while the customer waits in the app, (c) "car returned" to billing, the app and the damage check.
3. The e-bike partner changes its data format. What happens in each architecture?

::: notes
Pairs, 5 min + 5 min discussion. Expected answers: 1 8 × 7 / 2 = 28 interfaces vs. 8 connections (not all pairs need an interface — accept "up to 28"). 2 (a) file transfer is acceptable: large, monthly, not urgent, the association may require a file format (accept messaging with reasoning); (b) remote procedure invocation / synchronous API call: the customer waits for the answer; (c) messaging with a publish-subscribe channel: one event, several receivers, the car-sharing back-end does not need to know them. 3 Point-to-point: every application that talks to the e-bike partner must change its own interface (up to seven changes, each tested separately); hub: one message translator on the platform is adapted — the other applications do not notice. Lesson: the cost of point-to-point is in the changes, not in the first build.
:::

---

# Integration Approaches Today {.section}

ESB, APIs, events and iPaaS

---

# Enterprise Service Bus (ESB)

::: columns
**What it is**

- Middleware that connects applications as **services** over a shared bus
- Core functions: **routing**, **transformation**, **protocol mediation**, reliable messaging, often **orchestration** of process steps
- Builds on messaging and open standards
- Typical in **service-oriented architectures** (SOA)
|||
**Experience from practice**

- Gives **one place** to see and govern interfaces
- Risk of a **central bottleneck**: one team, one product, every change waits
- Business logic creeps **into the bus** — it becomes a hidden application
- Today often replaced or complemented by **APIs and events**
:::

::: source
Own wording based on Chappell (2004) and Hohpe and Woolf (2004).
:::

::: notes
Chappell (2004) describes the ESB as a highly distributed, event-driven service-oriented architecture that combines message-oriented middleware, web services, content-based routing and data transformation on the basis of open standards, and discusses how it differs from centralised hub-and-spoke integration brokers. In practice, many ESB programmes of the 2000s ended as large central platforms; the pattern "smart endpoints, dumb pipes" in microservice architectures is a reaction to logic in the middleware. The exam asks for the idea and the trade-off, not for products.
:::

---

# APIs and API Management

- An **API** (application programming interface) offers functions and data of an application through a defined, documented **contract**
- Web APIs often follow **REST**: resources addressed by URLs, standard operations, stateless requests
- **Request–reply**: the caller waits for the answer — good for queries and immediate decisions
- **API management**: a gateway for security and load control, versioning, a developer portal, usage monitoring
- APIs open the enterprise to **partners** and **apps**: the basis of platform business models

::: callout
**API first** (principle from session 13): new applications offer their functions via the API platform, so the next app or partner can reuse them.
:::

::: source
Own wording based on Fielding (2000) and Hohpe and Woolf (2004).
:::

::: notes
Fielding (2000, chapter 5) defined REST as an architectural style for the web, derived by adding constraints such as client–server, statelessness, caching, a uniform interface and layering. In business terms, an API is a product with consumers: it needs an owner, a version policy and service levels (session 6 — an SLA for an API). The car-sharing unit already runs an API gateway (session 6: the Monday-morning incident) — a starting point for the group API platform on the roadmap. Partners of session 12 (e-bike, parking garages, long-distance operator) are connected via APIs in both directions.
:::

---

# Event-Driven Integration

![Event-driven integration at Rhein-Neckar Mobil Group: ticket devices on 400 buses upload sales to the fare back-end; the fare back-end publishes the event ticket sold to an event broker, which acts as a publish-subscribe channel; subscribers are revenue sharing for the report to the transport association, the cloud ERP for the daily revenue posting, the mobility app for the ticket in the customer account, and reporting and analytics](img/eai-event-driven.png){width=88%}

::: source
Own illustration based on Hohpe and Woolf (2004); own example.
:::

::: notes
An event is a fact that has happened ("ticket sold", "car returned", "customer moved"). The publisher sends it once to an event broker; every interested application subscribes. Advantages: loose coupling — the fare back-end does not know or wait for its subscribers; new subscribers (e.g. a fraud check) are added without changing the publisher; data flow in near real time instead of a nightly file. Prices: eventual consistency — for a short time the ERP and the app may show different figures; duplicates and order of events must be handled (idempotent receiver); tracing a business transaction across many events needs good monitoring. Today's event brokers (streaming platforms) also store events for replay.
:::

---

# Synchronous or Asynchronous?

| | Synchronous (request–reply, API call) | Asynchronous (messaging, events) |
|---|---|---|
| Caller | Waits for the answer | Continues after sending |
| Availability | Both sides must be up | Receiver can be down for a while |
| Coupling | Tighter: caller knows the receiver | Looser: sender may not know receivers |
| Good for | Queries, checks, decisions while a user waits | Notifications, data distribution, high volumes |
| Example | App asks for the price of a trip | Ticket devices send sales after a network gap |

::: callout
Most landscapes need **both**: APIs for questions, events for facts.
:::

::: source
Own wording based on Hohpe and Woolf (2004).
:::

::: notes
Hohpe and Woolf (2004) list asynchronicity as one of the decision criteria for integration styles: synchronous calls fail if the remote application or the network is down. Link to BCM (session 8): the ticket devices store sales locally and forward them later — that is asynchronous by design and is why bus ticketing keeps running when the mobile network fails. A chain of synchronous calls (app → API platform → fare back-end → payment platform) is only as available as its weakest link: 99.5 % × 99.5 % × 99.5 % ≈ 98.5 %.
:::

---

# Integration Platform as a Service (iPaaS)

- A **cloud service** for building, running and monitoring integrations — the integration platform is rented, not operated
- Ready-made **connectors** for common SaaS and ERP products, graphic **mapping** tools
- Fits landscapes with many **SaaS** applications and **hybrid** cloud and on-premises systems
- Can enable **business units** to build simple integrations themselves

::: callout
Questions to ask: data **location** and protection, **lock-in** to the provider, cost per connection or message volume, who **governs** integrations built outside IT.
:::

::: source
Own wording based on Ebert et al. (2017); questions: own compilation.
:::

::: notes
Ebert et al. (2017) start from the history of EAI — many point-to-point interfaces, then expensive middleware that required changes on both sides — and describe iPaaS as cloud-based application integration. The questions in the callout are an own compilation. At RNM: the helpdesk SaaS, the cloud ERP for finance and the payroll service are all cloud services; connecting them with ready connectors is faster than building on-premises interfaces. Link to session 15 (IT sourcing): iPaaS is a sourcing decision for the integration platform itself. Link to session 7: integrations built by business units without IT governance are a form of shadow IT — data leave the controlled landscape.
:::

---

# Comparing the Approaches

| Approach | Best for | Watch out |
|---|---|---|
| **Point-to-point** | Few, stable interfaces | Growth, hidden dependencies |
| **ESB / integration broker** | Many internal applications, central governance | Bottleneck, logic in the bus |
| **APIs** | Apps, partners, reuse of functions, request–reply | Availability chains, versioning |
| **Events** | Facts for many receivers, near real time, loose coupling | Eventual consistency, monitoring |
| **iPaaS** | Many SaaS, hybrid landscapes, speed | Lock-in, data location, governance |

::: callout
An integration architecture **combines** approaches and defines **which one is used for what**.
:::

::: source
Own compilation based on Hohpe and Woolf (2004), Chappell (2004) and Ebert et al. (2017).
:::

::: notes
This table is the core of the exam: be able to recommend an approach for a given integration need with two arguments, and name its main risk. Students often see the approaches as generations where the newest wins; stress that a landscape keeps several of them for years — RNM will keep the nightly file to the association while it builds the API platform. Ask: which approach would you choose for the merger of two companies with two ERPs? (Typically a hub or iPaaS with translators during the transition, then fewer interfaces once one ERP is retired.)
:::

---

# Integration in Enterprise Architecture Management

- **Interfaces in the repository**: each with sender, receiver, business object, style, frequency and **owner** (session 11)
- **Information flow chart**: applications as nodes, data flows as arrows — for impact analysis
- **Integration principles**, e.g. API first, events for facts, no new shared databases, one leading system per business object
- **Integration platform** as part of the target landscape and **roadmap** (session 13)
- **Project reviews** check new interfaces against the principles (session 16)

::: source
Own wording based on Hanschke (2023, section 5.5.5) and Hohpe and Woolf (2004).
:::

::: notes
Hanschke (2023, section 5.5.5) describes the information flow chart ("Informationsfluss-Grafik") as one of the best-practice visualisations of EAM: it shows which applications exchange which information. Interface data are the hardest part of the repository to keep current (session 11): integration platforms and API gateways can deliver them automatically for everything that runs through them — one more argument for middleware. Interfaces count in application portfolio management too (session 13): an "eliminate" candidate with ten interfaces is not cheap to retire.
:::

---

# Integration Anti-Patterns {.optional}

- **Integration by database**: other applications read and write tables directly — no one can change the schema
- **Logic in the middleware**: business rules hidden in mappings and routes — a "shadow application"
- **Chains of synchronous calls**: one slow system blocks the whole process
- **Unowned interfaces**: nobody feels responsible when data are wrong
- **One more interface**: each project adds its own, nobody retires any

::: source
Own wording based on Hohpe and Woolf (2004) and Chappell (2004).
:::

::: notes
Self-study. Countermeasures: APIs or events instead of direct table access; keep business rules in the owning application, use the platform for transport and translation; asynchronous integration where the user does not wait, timeouts and fallbacks otherwise; an owner for every interface in the repository; decommissioning of interfaces as part of every replacement project. Exam point: name a risk of an integration design and a countermeasure.
:::

---

# Mini Exercise: Which Integration Approach? {.exercise}

Recommend an approach (point-to-point, ESB/broker, API, events, iPaaS) and give **one reason**:

1. The new helpdesk SaaS must receive customer data from the customer database and send case data to the cloud ERP.
2. The parking garage operator wants to show free spaces in the mobility app.
3. A change of a customer's address must reach five applications.
4. A small interface between the workshop system and a spare-parts supplier, unchanged for ten years.
5. A conductor checks in the app whether a passenger's ticket is valid.

::: notes
Pairs, 5 min + 5 min discussion. Expected answers (several defensible): 1 iPaaS — two cloud services, ready connectors, quick (accept API platform with reasoning). 2 API — partner offers a query interface, the app asks when the customer looks (request–reply); accept events if the operator pushes changes. 3 Events — one fact, many receivers, publisher does not need to know them (accept ESB/broker with publish-subscribe). 4 Point-to-point — few, stable, not worth moving; document it in the repository and keep it until the workshop system is replaced (it is a "tolerate" application, session 13). 5 API — synchronous check, the conductor waits; needs high availability and an offline fallback (e.g. signed ticket stored on the phone). Lesson: the need decides the approach.
:::

---

# Case Exercise: Integration Architecture for the Mobility App {.exercise}

**Case:** *Rhein-Neckar Mobil Group* (sessions 3–13): 3,200 employees, €410 million turnover, about 180 applications. The **mobility app** is planned for 2028: one account, journey planning, bus and rail tickets, car sharing, partner offers, one payment.

- Ticket devices upload sales every 15 minutes to the **fare back-end** (14 years old, two developers)
- The fare back-end sends a **nightly file** to the ERP bus and rail; revenue reports go to the transport association **monthly**
- Customer data are copied **by hand** between the ERP subscription module and the car-sharing customer database
- The car-sharing unit runs an **API gateway** for its app; the helpdesk and finance ERP are **cloud services**
- Partners: e-bike city partner, parking garages, long-distance operator — each with its own API
- No list of interfaces; the architecture team estimates "a few hundred", mostly point-to-point

::: notes
Read the case together (2 min). Hints if asked: the roadmap of session 13 has the API platform in the first year, the customer master and the payment platform before the app release; the two-person architecture team (session 10) cannot run an integration platform alone — Group IT operations would run it; budget for the platform is not yet approved. Tasks on the next slide.
:::

---

# Case Exercise: Your Tasks {.exercise}

1. List **five integration needs** of the mobility app. For each, describe it with the **dimensions** (object, direction, reach, timing) and choose an **integration style**.
2. Explain to the CFO why extending the **point-to-point** approach is not an option.
3. Draw a **target integration architecture**: which **middleware components** (API platform, event broker, iPaaS, others) connect which applications?
4. Formulate **three integration principles** and one **governance measure**.
5. How do you integrate the **fare back-end** without rebuilding it first? Name one **risk** and one **dependency** on the roadmap.

::: notes
Groups of 4–5, about 30 min + 15 min discussion. This is the session's exam-style exercise. Expected answers (several defensible):
1 E.g. log in with one account → customer master: data, horizontal, enterprise-wide, real time, synchronous API; buy a bus and rail ticket → fare back-end and payment platform: function and process, real time, API; book a car → car-sharing back-end via its gateway: function, API; show partner offers (e-bikes, parking) → partner APIs: inter-company, real time, API; ticket sold → revenue sharing, ERP, app account: data, horizontal and vertical, near real time, events; support case → helpdesk SaaS with customer data: iPaaS or API; journey planning with real-time data → passenger information: API (gap: today's system cannot deliver real time, session 13).
2 With n applications up to n(n−1)/2 interfaces — even 20 applications around the app give up to 190; each change (e.g. migrating the ERP, a new partner) touches many interfaces; no overview, no monitoring; the app would depend on many hidden connections; cost is in maintenance and changes, not the first build. Business framing: time-to-market for partners, risk, cost of the ERP migration.
3 E.g. API platform with gateway (extend the car-sharing gateway) for app, partners and internal functions; event broker for facts (ticket sold, car returned, customer changed); iPaaS or connectors for the SaaS services (helpdesk, cloud ERP, payroll); legacy adapter for the fare back-end; nightly or monthly files kept where timeliness is not needed (association report). Customer master as the leading system behind the account APIs.
4 Principles: API first; events for facts that several applications need; no new direct database access between applications; one leading system per business object; every interface has an owner and is documented in the repository. Governance: interfaces checked in project quality gates; integration platform team with service levels; interface data imported from the platform into the EA repository.
5 Wrap the fare back-end with an API facade or adapter on the platform: the app talks to the API, the adapter translates to the old system; sales become events published by an adapter that reads the existing upload. Later the back-end is migrated behind the same API (session 13: "migrate") without changing the app. Risk: two developers, load on an old system when the app adds traffic, offline capability of ticket devices must be kept. Dependency: API platform before app release; customer master and payment platform before ticket sales in the app.
:::

---

# Key Takeaways

- **Integrated information processing** links data, functions and processes so that information captured once serves the whole enterprise; integration can be described by object, direction, reach, automation and timing
- Four **integration styles**: file transfer, shared database, remote procedure invocation, messaging — chosen by coupling, timeliness and availability needs
- **Point-to-point** grows towards n(n−1)/2 interfaces; **middleware** centralises routing, translation and monitoring — at the price of a central component
- Today's landscapes combine an **ESB or broker**, **APIs** for requests, **events** for facts and **iPaaS** for cloud services — governed by integration principles in EAM

---

# Next Session: IT Sourcing

- Make or buy; outsourcing models
- Offshoring and nearshoring
- Cloud sourcing: IaaS, PaaS, SaaS; multi-sourcing
- Vendor management

::: callout
**Preparation:** find out which IT services your training company **buys from outside** — e.g. SaaS, hosting, application support — and ask **why** it decided to buy rather than to do them itself.
:::

::: notes
The SaaS services and the iPaaS question of today lead into sourcing: who runs the integration platform — Group IT, a service provider or a cloud vendor?
:::

---

# References {.references}

- Chappell, D. A. (2004). *Enterprise service bus*. O'Reilly Media.
- Ebert, N., Weber, K., & Koruna, S. (2017). Integration platform as a service. *Business & Information Systems Engineering, 59*(5), 375–379. https://doi.org/10.1007/s12599-017-0486-0
- Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* [Doctoral dissertation, University of California, Irvine].
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Hohpe, G., & Woolf, B. (2004). *Enterprise integration patterns: Designing, building, and deploying messaging solutions*. Addison-Wesley.
- Mertens, P. (2013). *Integrierte Informationsverarbeitung 1: Operative Systeme in der Industrie* (18th ed.). Springer Gabler.
- Ross, J. W., Weill, P., & Robertson, D. C. (2006). *Enterprise architecture as strategy: Creating a foundation for business execution*. Harvard Business School Press.

Diagrams in this deck are own illustrations. Integration patterns and frameworks are described in own words.
