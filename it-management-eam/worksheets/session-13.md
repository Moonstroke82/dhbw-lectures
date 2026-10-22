---
course: IT Management and EAM
session: 13
title: Strategic Planning of the IT Landscape
subtitle: Practice tasks on as-is, target and transition landscapes, landscape maps, application portfolio management with the TIME model, gap analysis and roadmaps
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 13: as-is, target and transition landscapes, landscape maps and other views of the landscape (Hanschke, 2023; Keller, 2017), application portfolio management (Riempp & Gieffers-Ankel, 2007; Weill & Vitale, 1999), the TIME model with its two dimensions functional fit and technical fit (SAP LeanIX, n.d.), gap analysis and roadmaps with transition states (The Open Group, 2022). Terms follow the session slides: **functional fit** describes how well an application supports the business (rated by the business owner), **technical fit** how sound its technology is (rated by the IT owner). Paper and pencil are enough; for the maps, a table or a simple drawing tool helps. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) A transition landscape describes the planned state of the landscape at a given date between the as-is and the target.
- b) In the TIME model, an application with high technical fit and low functional fit should be migrated to a new platform.
- c) A landscape map places applications in a matrix of business dimensions such as capabilities and organisation units.
- d) "Eliminate" means that the business function supported by the application is no longer needed.
- e) Application portfolio management decides which new projects are funded; project portfolio management manages the existing applications.
- f) An application that is 20 years old always has low technical fit.

::: answer lines=8
:::

::: hint
Draw the 2 × 2 grid of the TIME model before you answer b) and d). For e), ask: which portfolio manages what exists, and which decides what is changed?
:::

::: solution
- a) **True.**
- b) **False.** High technical fit and low functional fit is **Tolerate**: keep it running with minimal spend. **Migrate** is for high functional fit and low technical fit.
- c) **True.**
- d) **False.** Eliminate retires the **application**; the function may still be needed and is then moved to another application (e.g. revenue sharing at Rhein-Neckar Mobil Group).
- e) **False.** It is the other way round: application portfolio management assesses the **existing** applications and proposes candidates; project portfolio management decides which **changes** (projects) are funded.
- f) **False.** Age is only one hint; an old application can still be vendor-supported, stable, on a standard platform and well maintained — technical fit is rated against defined criteria.

Marking hint: one point per item; for false statements the point requires the correction.
:::

## TIME at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1, 4, 11 and 12), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, has cleaned up its application list (worksheet 11). The business and IT owners have now rated the applications:

| Application | Functional fit | Technical fit | Running cost per year | Remarks |
|---|---|---|---|---|
| Warehouse management system (WMS) | High | Low | €380,000 | 16 years old, own extensions, vendor support ends in two years |
| Route planner | High | High | €60,000 | SaaS, introduced last year |
| Fleet telematics | High | High | €150,000 | Cloud, used by all trucks |
| Old billing system | Low | Low | €90,000 | Replaced by the new billing SaaS; still used for old contracts |
| New billing (SaaS) | High | High | €70,000 | All new contracts since last year |
| Excel macro "diesel cost per tour" | High | Low | — | One dispatcher maintains it; figures go into customer offers |
| Document archive | Low | High | €25,000 | Vendor-supported; scans of delivery notes, rarely searched |

1. Place each application in the **TIME** model and name a concrete **next step** for each.
2. Which **two** applications should the architecture team bring to the IT steering committee first? Use the TIME category **and** cost, risk or timing in your justification.
3. The head of warehouses says: "The WMS is rated 'Migrate' — so we can stop all changes to it right away." Explain why this is wrong.

::: answer lines=16
:::

::: hint
Migrate keeps the function and moves it to a new platform; until the new platform is live, the old application must keep running. Look at support end dates and at who depends on a single person.
:::

::: solution
1. WMS: **Migrate** — high business value, weak technology; next step: start a replacement project (standard WMS or new version) with data migration and interfaces. Route planner: **Invest** — develop further, e.g. connect it to fleet telematics. Fleet telematics: **Invest**. Old billing: **Eliminate** — migrate or archive the old contracts, terminate the licence, switch off. New billing: **Invest** — the target system for all billing. Excel macro: **Migrate** — high value (feeds customer offers), poor technology (one person, no controls); move the calculation into the route planner, billing or a controlled tool. Document archive: **Tolerate** — keep cheaply, review at contract end; possibly move the archive into another system later.
2. E.g. the **WMS** (highest cost, vendor support ends in two years — a replacement takes time, so the decision is urgent; warehouse operations are a core capability) and the **old billing system** (eliminate saves €90,000 per year quickly; the only blocker is the old contracts). Also accept the **Excel macro** instead of old billing with the argument of **risk**: wrong diesel costs in customer offers, single person dependency.
3. Migrate means the **function** moves to a new platform; until the new WMS is live, the old one runs the warehouses and must stay operable — security patches, legal changes and urgent fixes are still needed. The category says "no major new features, plan the replacement", not "freeze". Changes should be limited to what is necessary and coordinated with the replacement project, so that nothing is built twice.

Marking hint: half a point per application for the category and half a point for a sensible next step (7 points); two points for part 2 (one per application with a justification beyond the quadrant); two points for part 3.
:::

## Reading a Landscape Map at Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3, 10, 11 and 12) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system (HIS) and its own data centre. The group CIO has drawn a first landscape map (extract):

| Capability | Hospital A | Hospital B | Hospital C | Hospital D |
|---|---|---|---|---|
| Patient management | HIS vendor X | HIS vendor X | HIS vendor Y | HIS vendor Z |
| Appointment and capacity management | HIS vendor X | Paper calendar | Scheduling SaaS | HIS vendor Z |
| Clinical documentation | HIS vendor X | HIS vendor X | HIS vendor Y | Own development (2004) |
| Billing | Billing module of ERP | Billing module of ERP | Billing module of ERP | Billing module of ERP |
| Patient portal (planned) | — | — | — | — |

1. Name one **redundancy**, one **gap** and one application that is already **shared** across the group. Explain what each means for the planned patient portal.
2. Hospitals A and B use the same HIS vendor X. Name **two questions** you must answer before treating them as "one application".
3. Which **colour lens** would you add for the group CFO and which for the CISO? Justify briefly.
4. Name **two questions** about the planned patient portal that this landscape map **cannot** answer, and the **view** that would answer them.

::: answer lines=16
:::

::: hint
Redundancy: several applications for the same capability. Gap: an empty or paper-based cell where support is needed. A map shows "what supports what", not "what is connected to what".
:::

::: solution
1. Redundancy: **patient management and clinical documentation** with three HIS products (X, Y, Z) plus an own development — the portal would need interfaces to all of them. Gap: **appointment and capacity management in hospital B** (paper calendar) and the **patient portal** itself (planned, no application) — online appointments cannot work for hospital B. Shared: **the ERP billing module** for all four hospitals — invoices could be offered in the portal from one source.
2. E.g.: Is it **one installation** (one instance, one database, one operator) or two separate installations of the same product? Are the **versions and configurations** (catalogues, workflows) the same? Do they have the same **owner and life cycle** (granularity rule, session 11)? Can patient data be shared between the hospitals legally and technically?
3. CFO: **running cost per year** or number of applications per capability — redundant HIS installations and data centres are the cost driver. CISO: **technical fit / vendor support status** or **protection requirements** — an own development from 2004 in clinical documentation holds highly sensitive health data. Accept other lenses with a justification (e.g. criticality from the BIA for the CISO).
4. E.g.: Which **interfaces** exist between the HIS products and to the ERP, and can they deliver data to a portal? → **interface map**. Where are the **patient data** stored and which is the **leading system** for the patient? → **data flow view** / data architecture. When will which HIS be replaced? → **roadmap / life cycle chart**. Which applications are **technically outdated**? → **portfolio chart** (TIME).

Marking hint: three points for part 1 (one per finding with its meaning for the portal); two points for part 2; two points for part 3; two points for part 4.
:::

## Gap Analysis and Roadmap at Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10–12), a tour operator with 25 travel agencies and a call centre, wants to sell personalised trips mainly online and through an app by 2030. The architecture team has described the as-is and the target for selected capabilities:

| Capability | As-is | Target |
|---|---|---|
| Customer management | Booking system (2005), newsletter tool, Excel lists in agencies | One customer platform (SaaS) as the leading system for customers and consents |
| Booking and reservation | Booking system (2005), only for travel agents | New booking platform with self-service for customers, agents and the app |
| Trip design and personalisation | — | Personalisation module on the customer platform |
| Payment management | External payment service provider | External payment service provider |
| Supplier and contract management | Booking system, two spreadsheets | Supplier module of the new booking platform |

1. List all **gaps** between as-is and target and classify each as **new, replace, consolidate, retire** or **keep**.
2. A first draft roadmap reads: *Year 1: personalisation module and app. Year 2: customer platform. Year 3: new booking platform, then switch off the booking system.* Find **two** problems with this sequence.
3. Propose a better roadmap with **two transition states** (what runs at the end of each). Name the **dependency** that sets your order.
4. Why must each transition state be **operable** on its own? Give one example from your roadmap.

::: answer lines=18
:::

::: hint
Personalisation needs one view of the customer; the app needs a booking platform that customers can use. Look for things that the draft builds on foundations that do not exist yet.
:::

::: solution
1. Customer management: **consolidate** (booking system, newsletter tool and Excel lists into one customer platform; also accept "new" for the platform itself) and **retire** the newsletter tool and Excel lists. Booking and reservation: **replace** (booking system → new booking platform). Trip design and personalisation: **new**. Payment management: **keep**. Supplier and contract management: **replace/consolidate** (booking system and spreadsheets → supplier module). The old booking system: **retire** once booking and supplier data have moved.
2. Problems, e.g.: (a) personalisation and the app in year 1 have **no foundation** — no leading customer system and no self-service booking; the app could only show the agents' booking system or would build its own customer data (a fourth store); (b) the customer platform comes **after** the module that needs it; (c) the booking system is switched off only at the very end, so all interfaces to the old system have to be built in years 1–2 and thrown away; (d) everything big lands in year 3 — high risk and change load for the agencies before 2030.
3. E.g. **transition 1** (end of year 1): customer platform live as the leading system; customer data from booking system, newsletter tool and Excel lists migrated; consent process in agencies and online; newsletter tool retired. **Transition 2** (end of year 2): new booking platform live for agents and customers on the web, supplier module in use, old booking system retired. **Target** (year 3): app and personalisation module on top of customer and booking platforms. Dependency: **one customer view and a self-service booking platform before personalisation and the app**. Also accept booking platform first if the student argues that customer data are migrated together with the booking data.
4. The business must run at every transition: travel agents must be able to book every day, and the call centre must see the customer. Example: at transition 1 the old booking system still takes bookings but must read customers from the new customer platform — an interim interface is needed and must be planned, tested and later switched off.

Marking hint: three points for part 1 (half a point per correctly classified gap); two points for part 2; three points for part 3 (two transition states with content, one dependency); two points for part 4.
:::

## Exam-Style Task: Landscape Planning at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–12), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers; orders received by 14:00 are delivered the same day from the central warehouse. The board plans to **acquire a smaller wholesaler in the Saarland** and to open the platform as a **marketplace** for manufacturers and other wholesalers (worksheet 12). The acquisition is expected to close in a few months; the CIO must present an integration plan for the IT landscape. The architecture team has collected these facts:

| Application | Company | Facts |
|---|---|---|
| ERP system | Kurpfalz | 20 years old, heavily customised, own server room; two people know the customisations; runs order processing, warehouse, finance |
| Online order platform | Kurpfalz | Hosted externally, extended by six in-house developers; installers like it |
| Tablet ordering app | Kurpfalz | Used by 60 field sales representatives; connected to the ERP |
| ERP system | Saarland | 6 years old standard cloud ERP, little customisation; runs order processing and finance |
| Web shop | Saarland | Standard shop software, few users; installers prefer phone orders |
| Warehouse system | Saarland | Own development, one developer, works reliably |

**Tasks:**

1. Explain the difference between an **as-is**, a **target** and a **transition** landscape, using the integration of the two companies as an example. (3 points)
2. Draw a simple **landscape map** for the merged company with at least **four capabilities** and the two companies as columns. Mark one **redundancy** and one capability where a **gap** appears with the marketplace. (4 points)
3. Explain the **TIME** model with its two dimensions and classify **four** of the applications. Justify each classification. (6 points)
4. Formulate **two architecture principles** for the target landscape and use them to decide which **ERP** should be the target system. Name one argument against your choice. (3 points)
5. Sketch a **roadmap** with two **transition states** and name **two factors** that determine the order of the steps. (4 points)

::: answer lines=30
:::

::: solution
Marking guide (20 points):

**1. As-is, target, transition (3 points, 1 each)**

- **As-is:** the landscape today — two ERPs, the platform and the web shop, two warehouse solutions, side by side after the closing.
- **Target:** the intended landscape in 3–5 years, derived from strategy and capabilities — e.g. one ERP, the platform (as marketplace) as the single sales channel for installers of both companies, one warehouse solution.
- **Transition:** a planned, operable state at a given date on the way — e.g. "end of year 1: Saarland installers order on the platform, the web shop is switched off, both ERPs still run with an interface".

**2. Landscape map (4 points)**

- Matrix with at least four capabilities (rows) × Kurpfalz / Saarland (columns), applications in the cells (2 points), e.g.: order management — platform, tablet app, ERP / web shop, phone orders, ERP; warehouse and delivery management — ERP / warehouse system; financial management — ERP / cloud ERP; field sales management — tablet app / —; partner (seller) management — — / —.
- Redundancy marked (1 point): e.g. two ERPs for financial management and order processing; platform and web shop for online orders.
- Gap marked (1 point): e.g. **seller/partner management** and **commission settlement** for the marketplace — no application in either company.

**3. TIME (6 points)**

- Model (2 points): two dimensions **functional fit** (business value, rated by the business owner) and **technical fit** (technical state, rated by the IT owner); four categories: **Invest** (high/high), **Migrate** (high functional, low technical), **Tolerate** (low functional, high technical), **Eliminate** (low/low).
- Four classifications with justification (4 points, 1 each), e.g.: Kurpfalz ERP — **Migrate** (runs the core processes, but 20 years old, heavily customised, two people know it); online order platform — **Invest** (core of the marketplace strategy, liked by installers, actively developed); tablet app — **Invest** or **Tolerate** (used daily by field sales; accept either with reasoning); Saarland ERP — **Invest** or **Tolerate** (modern standard software; its value depends on the target decision in task 4); Saarland web shop — **Eliminate** (few users, function covered by the platform); Saarland warehouse system — **Tolerate** or **Migrate** (works, but own development with a single developer — risk; accept either with reasoning).

**4. Principles and ERP decision (3 points)**

- Two principles (1 point), e.g.: standard software before own development and customisation; one leading system per business object; cloud first; API first for the marketplace.
- Decision (1 point): e.g. the **Saarland cloud ERP** as the target system for the merged company — standard, little customisation, cloud, modern; the Kurpfalz ERP is a Migrate candidate anyway. Also accept a **new** ERP for both with the argument that the Saarland ERP may not scale to the larger company.
- Argument against (1 point): e.g. the Saarland ERP is sized for a smaller company; Kurpfalz's same-day delivery processes and customisations may not be covered; the larger company would have to adapt more processes; contract and licence model must be checked; migration effort and risk for the core company.

**5. Roadmap (4 points)**

- Two transition states with content (2 points), e.g.: **transition 1** — Saarland installers order on the platform (interface to the Saarland ERP), web shop retired, both ERPs run; finance consolidated reporting. **Transition 2** — Kurpfalz moved to the target ERP, interfaces of platform and tablet app switched, warehouse solution decided; then marketplace functions (seller management, commissions).
- Two factors (2 points, 1 each): **dependencies** (ERP and interfaces before marketplace functions; the platform must handle both companies' products and prices); **risk** (two people know the Kurpfalz ERP, one developer for the Saarland warehouse system); **business deadlines** (closing date, marketplace launch); **capacity and change load** (same-day delivery must not be disrupted; six developers are needed for the marketplace too); **contract ends** and licence renewals.
:::

## Optional Challenge: Rating Criteria for a Small Portfolio {.optional}

*Weinbau Kaiserstuhl eG* (sessions 1, 11 and 12), a winegrowers' cooperative with 300 members and 60 employees, has a small portfolio: an ERP package for orders and accounting, a web shop run by an agency, cellar sensors that monitor fermentation temperatures, and a planned member portal. The managing director wants to "do the TIME thing" at the next board meeting.

1. Define **three criteria** each for functional fit and technical fit that suit a company of this size, with a short description of what "high" means for one criterion on each side.
2. Who should rate which dimension? Name **two measures** that keep the ratings from becoming "politics".
3. Is a full application portfolio management process worth it for a portfolio of four applications? Argue for a **lean** variant.

::: answer lines=14
:::

::: solution
1. Functional fit, e.g.: **support of the online sales goal** (session 12: 30 % online) — "high" means the application directly supports online sales without manual work; **user satisfaction** of shop staff, cellar master and office; **coverage of required functions** (e.g. subscriptions, member services). Technical fit, e.g.: **vendor or agency support** — "high" means a supported version with a support contract and security updates; **integration** (does the web shop pass orders to the ERP automatically?); **security and data protection** (customer data, hosting in the EU); **dependence on single persons**.
2. Functional fit: the **business users** — managing director for sales, cellar master for the sensors, office for the ERP; technical fit: the **IT service provider or agency** and whoever looks after IT internally. Measures: written criteria and a four-point scale before rating; separate rating by business and IT, then discussion of differences; document who rated and why; review once a year with the budget.
3. With four applications a formal process with a tool would cost more than it saves. A lean variant: one table with the four applications, the two fits, cost, contract end and owner; one rating meeting a year before the budget; TIME as a discussion aid for the board (e.g. "Invest" in web shop and member portal, "Tolerate" for the sensors). The value lies in the conversation and the decision, not in the method.

Marking hint: three points for part 1 (criteria on both sides and one clear "high" definition each), two points for part 2, two points for part 3.
:::

## References {.references}

- Hanschke, I. (2023). *Strategisches Management der IT-Landschaft: Ein praktischer Leitfaden für das Enterprise Architecture Management* (4th ed.). Hanser.
- Keller, W. (2017). *IT-Unternehmensarchitektur: Von der Geschäftsstrategie zur optimalen IT-Unterstützung* (3rd ed.). dpunkt.verlag.
- Riempp, G., & Gieffers-Ankel, S. (2007). Application portfolio management: A decision-oriented view of enterprise architecture. *Information Systems and e-Business Management, 5*(4), 359–378. https://doi.org/10.1007/s10257-007-0052-2
- SAP LeanIX. (n.d.). [TIME framework in SAP LeanIX enterprise architecture management]. Retrieved October 21, 2026, from https://docs-eam.leanix.net/docs/time
- The Open Group. (2022). *The TOGAF Standard, 10th Edition: Architecture development method*. Van Haren Publishing.
- Weill, P., & Vitale, M. (1999). Assessing the health of an information systems applications portfolio: An example from process manufacturing. *MIS Quarterly, 23*(4), 601–624. https://doi.org/10.2307/249491

Company names and figures in the tasks are fictitious training examples.
