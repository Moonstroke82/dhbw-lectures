---
course: IT Management and EAM
session: 14
title: Enterprise Application Integration
subtitle: Practice tasks on integrated information processing, integration styles, point-to-point vs. middleware, ESB, APIs, event-driven integration and iPaaS
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 14: integrated information processing and its dimensions (Mertens, 2013), the four integration styles file transfer, shared database, remote procedure invocation and messaging, and integration patterns (Hohpe & Woolf, 2004), point-to-point integration vs. middleware, the enterprise service bus (Chappell, 2004), APIs (Fielding, 2000), event-driven integration and integration platform as a service (Ebert et al., 2017), and the place of integration in EAM (Hanschke, 2023). Terms follow the session slides: **synchronous** integration means the caller waits for the answer (request–reply), **asynchronous** integration means the sender continues after sending (messaging, events). Paper and pencil are enough; for the architecture sketches, boxes and arrows are sufficient. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) With ten applications and an interface between every pair, a point-to-point landscape has 45 interfaces.
- b) In a publish-subscribe channel, the publisher must know every subscriber in order to send the message to it.
- c) File transfer is an outdated integration style and should always be replaced by APIs.
- d) A synchronous API call fails if the called application is not available at that moment.
- e) An integration platform removes the need to translate between data formats.
- f) Vertical integration links operational systems with planning and control systems, e.g. sales data feeding management reporting.

::: answer lines=8
:::

::: hint
For a), use n(n−1)/2. For c) and e), ask what the style or the platform is good for — and what still has to be done somewhere.
:::

::: solution
- a) **True.** 10 × 9 / 2 = 45.
- b) **False.** The publisher sends the message once to the channel (event broker); the subscribers register with the channel. The publisher does not need to know them — that is the loose coupling of event-driven integration.
- c) **False.** File transfer is simple and robust and still suitable for large data volumes where timeliness is not critical, e.g. a monthly report; the style is chosen per integration need.
- d) **True.** The caller waits for the answer; if the receiver or the network is down, the call fails (unless the caller has a fallback).
- e) **False.** The translations still exist, but they are done in one place (message translator on the platform) instead of in every application; a canonical data model can reduce their number.
- f) **True.**

Marking hint: one point per item; for false statements the point requires the correction.
:::

## Styles and Dimensions at Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10–13), a tour operator with 25 travel agencies and a call centre, is building a new booking platform and a customer platform (SaaS) and wants to sell personalised trips online and through an app by 2030 (worksheet 13). The IT team has listed the following data exchanges:

| No. | Data exchange |
|---|---|
| 1 | Every night, the booking system writes all new bookings into a file that the accounting system imports the next morning. |
| 2 | The newsletter tool reads customer addresses directly from the tables of the booking system's database. |
| 3 | While a customer books online, the booking platform asks the hotel partner's system whether a room is still free and waits for the answer. |
| 4 | When a booking is cancelled, a message is sent that the customer platform, accounting and the hotel partner each receive. |
| 5 | The call centre types bookings made by phone into the booking system from a paper form. |
| 6 | Once a month, revenue per destination is summarised for the management dashboard. |

1. Assign each exchange to one of the four **integration styles** — or say why none applies.
2. Describe exchanges **3**, **4** and **6** with the **dimensions** object, direction, reach and timing.
3. For which **two** exchanges would you recommend a change first? Justify with one criterion each (e.g. coupling, timeliness, availability).

::: answer lines=16
:::

::: hint
Shared database means that several applications work on the same tables. A person typing from paper is not an integration style — what is it?
:::

::: solution
1. 1 **file transfer**; 2 **shared database** (the newsletter tool works directly on the booking system's tables); 3 **remote procedure invocation** (synchronous request–reply, today typically an API call); 4 **messaging** (one message, several receivers — a publish-subscribe channel); 5 **no integration** — manual re-entry, a media break; 6 depends on the implementation: typically **file transfer** or a database extract into the dashboard; accept "not yet defined" with a sensible proposal.
2. Exchange 3: object **data and function** (availability check), direction **horizontal** (along the booking process), reach **inter-company** (hotel partner), timing **real time**. Exchange 4: object **data/process** (the cancellation triggers follow-up activities), direction **horizontal** (customer, accounting, partner), reach **enterprise-wide and inter-company**, timing **near real time**. Exchange 6: object **data**, direction **vertical** (operational bookings → management dashboard), reach **enterprise-wide**, timing **batch**.
3. E.g. exchange **2** — tight **coupling**: the new booking platform will replace the booking system, and the newsletter tool will stop working; also a data protection risk (direct access to all customer data). Exchange **5** — media break: typing errors, delay, no data for personalisation; the call centre should book directly in the booking platform. Also accept exchange 1 with the argument of **timeliness** (accounting sees bookings one day late) if the student explains why this matters for the business.

Marking hint: three points for part 1 (half a point per exchange), three points for part 2 (one per exchange with all four dimensions), two points for part 3.
:::

## Counting Interfaces at Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3 and 10–13) is a group of four hospitals. Each hospital has its own hospital information system (HIS); billing runs in one shared ERP. The planned **patient portal** must receive appointments and findings from all four HIS and invoices from the ERP; the four HIS must also exchange patient data with each other when patients are transferred, and each HIS sends billing data to the ERP.

1. Count the interfaces needed in a **point-to-point** architecture for these requirements. Then count the connections with an **integration platform**.
2. Hospital D will replace its own development with HIS vendor X in two years. Which interfaces must change in each architecture?
3. The group CIO is worried that the integration platform becomes a **single point of failure** for patient care. Is the worry justified? Name **two measures**.

::: answer lines=14
:::

::: hint
Count only the interfaces the requirements ask for: HIS–HIS pairs, HIS–ERP, HIS–portal, ERP–portal. Applications in the hub architecture: four HIS, ERP, portal.
:::

::: solution
1. Point-to-point: HIS–HIS pairs 4 × 3 / 2 = **6**; HIS–ERP **4**; HIS–portal **4**; ERP–portal **1** → **15 interfaces** (6 applications, here all pairs are needed: 6 × 5 / 2 = 15). Integration platform: one connection per application → **6 connections** (four HIS, ERP, portal).
2. Point-to-point: all interfaces of hospital D's system must be rebuilt — to the three other HIS, to the ERP and to the portal: **5 interfaces**, each tested with another partner. Platform: only **hospital D's connection** (adapter and translation) to the platform changes; the other applications keep their connections. If a canonical data model for patients is used, only the translation of the new system to the canonical model is needed.
3. Justified: if the platform fails, transfers, portal and billing data stop for all hospitals at once. Measures, e.g.: **high-availability operation** (redundant installation, second data centre or cloud region, session 8); **asynchronous messaging with guaranteed delivery**, so messages are stored and delivered after an outage; **fallback procedures** for clinical processes (e.g. transfer documents on paper or as PDF); **monitoring and an SLA** for the platform with recovery times derived from the BIA; keep life-critical clinical processes **independent** of the platform where possible.

Marking hint: two points for part 1 (one per count with the calculation), two points for part 2, two points for part 3 (justification and two measures).
:::

## From Batch File to Events at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1, 4 and 11–13), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, uses a route planner (SaaS), fleet telematics (cloud) and a new billing SaaS (worksheet 13). Today, the drivers' scanners record each delivery; once a night, the fleet telematics system writes all completed deliveries into a file that billing imports. Customers complain that they see deliveries in the customer portal only the next day, and invoices are sent late.

The architecture team proposes an **event** "delivery completed" published to an event broker.

1. Name **four subscribers** of the event and what each does with it.
2. Explain **two advantages** of the event-driven design compared with the nightly file and compared with **direct API calls** from fleet telematics to each receiver.
3. A driver's scanner loses network coverage and later resends three deliveries. Which **problem** can occur in billing, and which **integration pattern** solves it?
4. The CFO asks: "Will billing and the customer portal always show the same figures now?" Answer in two sentences.

::: answer lines=16
:::

::: hint
Think about who needs to know that a delivery is done: the customer, accounting, planning, analytics. For part 4, remember what "eventual consistency" means.
:::

::: solution
1. E.g. **billing** — creates the invoice item at once; **customer portal** — shows the delivery and proof of delivery; **route planner** — updates the remaining tour and plans the next day; **analytics / reporting** — delivery times, punctuality per customer; **warehouse management** — closes the shipment or triggers returns handling. Any four with a sensible use.
2. Compared with the nightly file: **timeliness** (near real time instead of next day) — customers see deliveries, invoices go out earlier, which improves cash flow. Compared with direct API calls: **loose coupling** — fleet telematics publishes once and does not need to know or wait for the receivers; new receivers are added without changing the publisher; a receiver that is down receives the event later instead of making the call fail.
3. **Duplicates**: the same delivery could be invoiced twice. Pattern: **idempotent receiver** — billing recognises already processed events (e.g. by delivery ID) and ignores repeats. Also accept a short description of de-duplication by a unique message ID.
4. Not at every moment: each subscriber processes the event independently, so for a short time one system may already show a delivery the other has not processed yet (eventual consistency). After all events have been processed, the figures agree; monitoring and reconciliation reports catch events that fail.

Marking hint: two points for part 1 (half a point per subscriber), two points for part 2, two points for part 3 (problem and pattern), two points for part 4.
:::

## Exam-Style Task: Integration Architecture at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–13), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers; orders received by 14:00 are delivered the same day from the central warehouse. The company is **acquiring a smaller wholesaler in the Saarland** and wants to open the platform as a **marketplace** for manufacturers and other wholesalers (worksheets 12 and 13). Today's integration:

| Connection | Today |
|---|---|
| Online order platform → Kurpfalz ERP | Direct calls to the ERP database every few minutes; built by the platform team |
| Tablet ordering app → Kurpfalz ERP | Own interface, 60 field sales representatives |
| Kurpfalz ERP → carriers | Nightly files with shipments |
| Saarland cloud ERP ↔ Saarland warehouse system | Own interface, maintained by the warehouse system's only developer |
| Saarland web shop → Saarland cloud ERP | Standard connector of the shop software |
| Manufacturers (planned marketplace sellers) | No connection; product data arrive as Excel lists by e-mail |

During a transition period of about two years, both ERPs will run in parallel; Saarland installers should order on the online order platform from the first year.

**Tasks:**

1. Explain the difference between **point-to-point** integration and integration via **middleware**. Use two arguments to show why the acquisition makes the question urgent for Kurpfalz Sanitär. (4 points)
2. Name the **integration style** of three of today's connections and assess **one weakness** of each. (3 points)
3. Design a **target integration architecture** for the transition period: which **components** (e.g. API platform, event broker, iPaaS) connect which applications? Show how an order of a Saarland installer on the online order platform reaches the **Saarland ERP**. (6 points)
4. Recommend an approach for the **marketplace sellers** (product data, orders, stock levels) and justify it with two criteria. (3 points)
5. Formulate **two integration principles** and name **two risks** of your architecture with one countermeasure each. (4 points)

::: answer lines=30
:::

::: solution
Marking guide (20 points):

**1. Point-to-point vs. middleware (4 points)**

- Point-to-point: each pair of applications has its own interface, up to n(n−1)/2; logic, translation and monitoring sit in each interface (1 point).
- Middleware: applications connect once to a platform (hub, bus, API platform, broker, iPaaS) that handles routing, translation and monitoring; about one connection per application, but a central component that must be highly available (1 point).
- Two arguments for urgency (2 points, 1 each), e.g.: the acquisition **doubles** the number of applications — with point-to-point, the platform, the tablet app and the carriers would each need interfaces to two ERPs; the Kurpfalz ERP will be replaced later (Migrate, worksheet 13), so every direct interface to it is built twice; the marketplace adds many external partners; nobody has an overview of the interfaces — risk for same-day delivery.

**2. Styles and weaknesses (3 points, 1 per connection with style and weakness)**

- Platform → Kurpfalz ERP: **shared database** (direct database access) — tight coupling, every ERP change or migration breaks the platform; performance load on the ERP database.
- Tablet app → ERP: **remote procedure invocation** (own interface; accept "point-to-point API") — only works with the Kurpfalz ERP, must be rebuilt for the target ERP.
- ERP → carriers: **file transfer** — data arrive late; acceptable for nightly shipment lists, but no live tracking.
- Saarland ERP ↔ warehouse system: point-to-point own interface (remote invocation or file — accept either with reasoning) — single developer, knowledge risk.
- Web shop → cloud ERP: point-to-point via standard connector — fine technically, but the web shop is to be retired.
- Manufacturers: **no integration** — manual re-entry from Excel, media break, errors in product data.

**3. Target integration architecture for the transition (6 points)**

- Components named and placed (3 points), e.g.: **API platform** with gateway in front of order, price, stock and customer functions — used by the online order platform, the tablet app and later the marketplace sellers; **event broker** for facts such as "order placed", "shipment created", "stock changed"; **iPaaS or connectors** for the Saarland cloud ERP and other SaaS; **adapters** for the Kurpfalz ERP (replacing the direct database access) and the Saarland warehouse system; file transfer kept for carriers where they cannot do more.
- Order flow of a Saarland installer (2 points): installer orders on the platform → the platform calls the order API on the API platform → a **content-based router** decides by customer or warehouse that the order belongs to the Saarland company → a **message translator** converts it into the format of the Saarland cloud ERP → the order is passed to the cloud ERP via its connector/API → confirmation back to the platform (synchronous) or as an event "order accepted" (asynchronous).
- Benefit for the later ERP migration explained (1 point): when the Kurpfalz ERP is replaced, only its adapter changes; platform, tablet app and sellers keep their APIs.

**4. Marketplace sellers (3 points)**

- Recommendation (1 point): **APIs** with API management (seller portal, authentication, documentation) for product data, orders and stock; **events** (e.g. "order placed for seller X") to notify sellers; accept iPaaS or a file upload for small sellers as an additional option with reasoning.
- Two criteria (2 points, 1 each), e.g.: **many external partners** with different systems — a documented contract is needed, not individual interfaces; **timeliness** — stock levels must be current for the same-day promise; **security** — external access via a gateway with authentication and load control; **coupling** — sellers can change their systems without affecting Kurpfalz.

**5. Principles and risks (4 points)**

- Two principles (2 points, 1 each), e.g.: API first for all functions used by more than one application or by partners; no direct database access between applications; events for facts needed by several applications; one leading system per business object (customer, article, order); every interface has an owner and is documented in the EA repository.
- Two risks with countermeasures (2 points, 1 each), e.g.: platform as **single point of failure** for same-day delivery → high availability, asynchronous buffering, monitoring with SLA; **skills** — nobody at Kurpfalz knows the platform → training, external partner, start with few interfaces; **eventual consistency** of stock between two ERPs → reconciliation and clear leading system for stock; **cost and lock-in** of iPaaS → check exit options and data location; **single developer** of the Saarland warehouse system → document the interface early, move it onto the platform.
:::

## Optional Challenge: iPaaS for a Small Cooperative {.optional}

*Weinbau Kaiserstuhl eG* (sessions 1 and 11–13), a winegrowers' cooperative with 300 members and 60 employees, uses an ERP package for orders and accounting, a web shop run by an agency, cellar sensors that monitor fermentation temperatures, and plans a member portal (worksheet 13). Orders from the web shop are typed into the ERP every morning by an office worker. The agency offers to connect shop, ERP and the planned member portal with an **iPaaS** subscription.

1. Explain what an iPaaS is and why it might suit a company of this size better than an own integration server.
2. Name **three questions** the managing director should clarify with the agency before signing.
3. Would you integrate the **cellar sensors** via the same iPaaS? Argue briefly.

::: answer lines=14
:::

::: solution
1. An iPaaS is an integration platform rented as a **cloud service**: integrations are built with ready-made **connectors** and mapping tools and run and are monitored by the provider. For a cooperative without own IT staff, there is no server to operate, no middleware skills to build up, and standard connectors for common shop and ERP products shorten the project; cost scales with use. It removes the daily media break (manual re-entry of web shop orders).
2. E.g.: **Where are the data processed** and stored (EU, GDPR, data processing agreement for customer and member data)? **Who owns and documents** the integrations — what happens if the agency contract ends (lock-in, exit, export of mappings)? **Cost model** (per connection, per message, per year) and how it grows? **Who monitors** failures and is told when an order does not arrive (service levels)? Does a **connector** exist for the ERP package?
3. Probably not at first: the sensors serve a different purpose (monitoring fermentation, real time, local alarms) and must keep working if the internet connection fails; their data are not needed by shop or ERP. Integrate them only if a business need arises (e.g. quality data in the member portal) — then a batch export would suffice. Accept "yes" with the argument of one platform for everything if the student addresses offline operation and alarms.

Marking hint: two points for part 1, three points for part 2 (one per question), two points for part 3.
:::

## References {.references}

- Chappell, D. A. (2004). *Enterprise service bus*. O'Reilly Media.
- Ebert, N., Weber, K., & Koruna, S. (2017). Integration platform as a service. *Business & Information Systems Engineering, 59*(5), 375–379. https://doi.org/10.1007/s12599-017-0486-0
- Fielding, R. T. (2000). *Architectural styles and the design of network-based software architectures* [Doctoral dissertation, University of California, Irvine].
- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Hohpe, G., & Woolf, B. (2004). *Enterprise integration patterns: Designing, building, and deploying messaging solutions*. Addison-Wesley.
- Mertens, P. (2013). *Integrierte Informationsverarbeitung 1: Operative Systeme in der Industrie* (18th ed.). Springer Gabler.

Company names and figures in the tasks are fictitious training examples.
