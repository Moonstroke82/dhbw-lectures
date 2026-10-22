---
course: IT Management and EAM
session: 15
title: IT Sourcing
subtitle: Practice tasks on sourcing dimensions, make or buy, outsourcing models, nearshoring and offshoring, cloud sourcing, multi-sourcing and vendor management
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 15: the dimensions of a sourcing decision (scope, provider, location, degree, number of providers, delivery model), motives and risks of outsourcing (Dibbern et al., 2004; Lacity et al., 1996), make-or-buy criteria including the core competence tests (Prahalad & Hamel, 1990), outsourcing models, onshore, nearshore and offshore delivery (Carmel & Abbott, 2007), cloud computing and the service models IaaS, PaaS and SaaS (Mell & Grance, 2011), multi-sourcing (Cohen & Young, 2006), the retained organisation (Feeny & Willcocks, 1998) and vendor management over the life cycle (Tiemeyer, 2023). Terms follow the session slides: **selective** sourcing buys specific services from outside, **total** outsourcing hands most of the IT function to one provider; **multi-sourcing** combines several internal and external providers. Paper and pencil are enough; for the calculation in task 4 a calculator helps. The last core task is in the style of an exam question.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

- a) A server rented for three years in a provider's data centre, ordered by ticket and with fixed capacity, is a typical IaaS cloud service.
- b) With SaaS, the provider is responsible for the application; the customer remains responsible for its data and for who has access.
- c) If a company outsources the processing of customer data to a cloud provider, the provider becomes responsible for GDPR compliance instead of the company.
- d) Nearshoring reduces labour cost less than offshoring, but usually also reduces the coordination effort caused by time zones, language and travel.
- e) Multi-sourcing reduces the dependency on a single provider, but the customer has to coordinate the providers end to end.
- f) After a total outsourcing of IT operations, a company no longer needs any IT staff of its own.

::: answer lines=8
:::

::: hint
For a), check the five essential characteristics of cloud computing. For c) and f), ask what can be handed over to a provider and what cannot.
:::

::: solution
- a) **False.** It lacks on-demand self-service and rapid elasticity (Mell & Grance, 2011); it is classic hosting. IaaS means virtual resources ordered by self-service, scaled up and down and billed by use.
- b) **True.**
- c) **False.** The company stays the **controller**; the provider is a **processor** bound by a contract under GDPR Art. 28. The accountability is not outsourced.
- d) **True.** Distance has geographic, temporal, linguistic and cultural dimensions (Carmel & Abbott, 2007); nearshore locations are closer in several of them.
- e) **True.**
- f) **False.** A **retained organisation** is needed to set the strategy, plan the architecture, buy well and monitor the contracts (Feeny & Willcocks, 1998).

Marking hint: one point per item; for false statements the point requires the correction.
:::

## Describing Sourcing Arrangements

Describe each arrangement with the **sourcing dimensions** from the session: **what** (scope), **who** (provider), **where** (location), **how much** (degree), **how many** (providers) and **how delivered** (classic contract or cloud service). Leave a dimension open if the text does not say anything about it.

1. A hospital group (Klinikverbund Oberrhein) moves the servers of its four data centres into **one data centre of a German hosting provider**; the hospitals' IT teams keep running the applications.
2. A tour operator (Bodensee Reisen AG) lets a **call-centre provider in Portugal** answer customer calls in the evenings and at weekends, including bookings in the booking platform.
3. A logistics company (Rheinland Logistik GmbH) uses a **route planner**, **fleet telematics** and a **billing system**, each as a cloud subscription from a different vendor.
4. A bank hands **all IT operations, development and the service desk** to one IT service provider for ten years; 200 employees move to the provider.
5. A group of companies founds an **IT subsidiary** that provides IT services to all group companies and charges them per service.

::: answer lines=14
:::

::: hint
The provider can be external or internal (a group company). A business process with its IT, such as answering customer calls, is more than an IT service.
:::

::: solution
1. What: **infrastructure** (servers, data centre operation); who: **external** hosting provider; where: **onshore**; how much: **selective** (applications stay in-house); how many: one provider for this service; how: classic **hosting / infrastructure outsourcing** (accept colocation or managed hosting).
2. What: a **business process** (customer service and booking) including the use of IT — **business process outsourcing** of part of the call centre; who: external; where: **nearshore** (Portugal); how much: selective (evenings and weekends only); how: classic service contract with access to the booking platform. Note: the provider processes customer data — processor agreement, EU location avoids a third-country transfer.
3. What: **applications**; who: three external vendors; where: open (depends on the vendors' data centres); how much: selective; how many: **multi-sourcing**; how: **cloud (SaaS)**.
4. What: infrastructure, applications and IT processes — almost the whole IT function; who: external; where: open; how much: **total outsourcing**; how many: **single sourcing**; how: classic long-term contract, including a **transfer of staff**. For a bank, DORA requirements for ICT third-party contracts apply (register, exit strategy, contract clauses).
5. What: IT services in general; who: **internal / captive** provider (group company); where: open; how much: depends on the scope given to it; how: internal service contracts with **chargeback** (session 4). The subsidiary can later also buy from external providers or sell to third parties.

Marking hint: two points per arrangement (full points for at least four correct dimensions with a plausible reading of the text), 10 points in total.
:::

## Cloud Service Models at Klinikverbund Oberrhein

*Klinikverbund Oberrhein* (sessions 3 and 10–14) is a group of four hospitals that merged two years ago. Each hospital still has its own hospital information system (HIS) and its own data centre; one hospital suffered a ransomware attack last year (worksheet 3). The group CIO wants to close the four data centres within five years and looks at cloud offerings for these needs:

| No. | Need |
|---|---|
| 1 | The planned **patient portal**, developed by an agency for the group |
| 2 | Hospital D's **own clinical documentation** system from 2004, which must keep running until the HIS of vendor X replaces it (worksheet 14) |
| 3 | **E-mail, calendar and office** software for all staff |
| 4 | A **duty-roster** tool for nurses and doctors, offered by several vendors |
| 5 | **Backups** of all hospital systems in a second location |

1. Choose a **service model** (IaaS, PaaS, SaaS) — or **no cloud** — for each need and justify your choice in one sentence.
2. For needs **1** and **2**, say who installs **security updates** for the operating system and who decides **which employees** may see patient data.
3. Name **two requirements** from law or regulation that the group must address in its contracts with cloud providers, and **one question** about data location.

::: answer lines=16
:::

::: hint
The more the group builds or keeps itself, the further down the stack it buys. Health data are a special category of personal data, and hospitals are essential entities under NIS2.
:::

::: solution
1. Need 1 **PaaS** — the agency develops custom code for the group; container platform, managed database and API management are bought, the platform is run by the provider (accept IaaS with reasoning, or SaaS if a standard portal product is chosen). Need 2 **IaaS** (rehost of the virtual servers) — an old system cannot be rebuilt for a platform shortly before it is retired; accept "stay in a remaining data centre until replacement" with a risk argument. Need 3 **SaaS** — commodity, mature market. Need 4 **SaaS** — standard function, several vendors. Need 5 **IaaS** (cloud storage) or a backup service (SaaS-like managed backup) — accept either; must include an offline or immutable copy because of ransomware (session 8).
2. Need 1 (PaaS): operating system updates are installed by the **provider**; the group (or the agency on its behalf) keeps the application up to date. Need 2 (IaaS): the **group** (or a contracted operator) installs operating system updates — the provider only runs the virtualisation and hardware. In both cases the **group decides about access** to patient data (data and access rights stay with the customer in every model).
3. Requirements, e.g.: **GDPR Art. 28** processor agreement; health data are a special category (Art. 9) — strong security measures, possibly a data protection impact assessment; **NIS2** supply chain security — hospitals must assess and manage the security of their suppliers; national rules for patient data and professional secrecy (accept as an additional point without details). Data location question, e.g.: are the data stored and processed **only in the EU** — and can a provider from a third country be forced to hand them over (Chapter V GDPR, transfers)? Where are backups and support staff located?

Marking hint: five points for part 1 (one per need with justification), two points for part 2, three points for part 3.
:::

## Make or Buy for a Warehouse System at Rheinland Logistik

*Rheinland Logistik GmbH* (sessions 1, 4 and 11–14), a logistics company with 1,800 employees, 25 warehouses and 300 trucks, must decide about its **warehouse management system (WMS)**: 16 years old, many own extensions, running cost €380,000 per year, **vendor support ends in two years** (worksheet 13). A pharma customer requires that urgent orders are shipped within 24 hours (worksheet 8). Two options are on the table:

| | Option A: new version, own extensions rebuilt in-house | Option B: standard WMS as SaaS |
|---|---|---|
| One-off cost (project, migration, interfaces, training) | €900,000 | €600,000 |
| Running cost per year | €400,000 (licences, servers, own team) | €300,000 subscription + €40,000 for vendor management |
| Fit with today's processes | 100 % (own extensions) | About 85 %; some processes must change |
| Who knows the system | Own team of three | Vendor; own team configures |

1. Calculate the **total cost** of both options over **five years** (without discounting).
2. Apply **three make-or-buy criteria** from the session to the WMS. Is warehouse management a **differentiator** or a **commodity** for Rheinland Logistik?
3. Recommend an option. Name **two risks** of your option and one countermeasure each.
4. The CFO says: "Option B is €600,000 cheaper — decision made." Which **costs or effects** are missing from the table?

::: answer lines=18
:::

::: hint
For part 2, look at what makes the company win customers — and whether the extensions are really unique. For part 4, think about the whole vendor management life cycle.
:::

::: solution
1. Option A: €900,000 + 5 × €400,000 = **€2,900,000**. Option B: €600,000 + 5 × (€300,000 + €40,000) = **€2,300,000**. Difference €600,000 in favour of B.
2. E.g.: **strategic importance** — warehouse management is a core process, but WMS functions (stock, picking, shipping) are mostly a **commodity**; the differentiator is reliable service for customers such as the pharma customer, which a good standard WMS can support. **Market maturity** — high; many standard WMS products and SaaS offerings exist. **Specificity** — 85 % fit; check whether the missing 15 % are real differentiators (e.g. the 24-hour pharma rule) or habits. **Skills and risk** — three people know the old system; vendor support ends in two years. **Cost** — B is cheaper over five years. Accept "differentiator" if the student argues that special processes for key customers are the company's competitive edge and cannot be bought.
3. E.g. **Option B**: cheaper, mature market, removes the know-how risk, vendor carries the development. Risks: processes do not fit (pharma 24-hour rule) → requirement in the tender and fit-gap workshops, change processes before go-live; **dependency and lock-in** → exit clause, data export in a usable format, notice periods (Data Act switching rights); **availability** of a cloud service for 25 warehouses → SLA with availability and recovery times derived from the BIA, offline/fallback picking lists (session 8). Option A is acceptable with the argument that the extensions are a real differentiator and the team can be strengthened; risks then: know-how in three people, higher cost.
4. E.g.: **transition costs** beyond the project (parallel operation, productivity loss in warehouses); **exit costs** at the end of the SaaS contract; **price increases** (indexation) of the subscription; the **cost of process changes** for the 15 % gap; **retained staff** time for steering the vendor (partly included); **interfaces** to fleet telematics, billing and customer portal (session 14); the **value** side — e.g. faster new functions, better reliability; **discounting** (the one-off costs come first); what happens to the three employees of the own team (works council).

Marking hint: two points for part 1, three points for part 2, three points for part 3, two points for part 4.
:::

## Where Should the App Be Built? Bodensee Reisen AG

*Bodensee Reisen AG* (sessions 2 and 10–14), a tour operator with 25 travel agencies and a call centre, wants to sell personalised trips online and through an **app by 2030**; it is building a new booking platform and a customer platform (SaaS) (worksheets 13 and 14). The company has two web developers of its own. For the app it receives three offers:

| | Agency in Konstanz | Nearshore provider in Czechia | Offshore provider in India |
|---|---|---|---|
| Day rate per developer | €950 | €620 | €330 |
| Time difference to Germany | None | None | 3.5 to 4.5 hours |
| Travel | Local | About one day | Long-haul flight |
| Experience with travel booking | Little | Good | Very good |

1. Explain **three dimensions of distance** and use them to compare the offers.
2. The app needs a few weeks of **discovery** with travel agents and customers, then **feature development**, then **regression testing** for every release. Which location suits which kind of work? Justify.
3. The developers will need **test data** from the customer platform. What must the company check if the offshore provider gets access to real customer data?
4. Recommend a **sourcing set-up** for the app and say which roles must stay **in-house**.

::: answer lines=16
:::

::: hint
The cheapest day rate is not the cheapest project. Think about which tasks need close contact with users and which are well specified.
:::

::: solution
1. **Geographic** distance (travel time: local, one day, long-haul); **temporal** distance (time zones: none for Konstanz and Czechia, several hours for India — less overlap for meetings and quick questions); **linguistic** and **cultural** distance (German-speaking agency; English-speaking work in Czechia and India, different business cultures) (Carmel & Abbott, 2007). The day rates fall with distance, while coordination effort rises.
2. **Discovery**: onshore — agency or in-house — close to agents and customers, workshops on site, fast feedback. **Feature development**: nearshore — good domain experience, same time zone, travel possible for joint planning; also acceptable onshore if the budget allows. **Regression testing**: offshore is suitable — well specified, repeatable tasks; time difference can even help (tests run overnight from the German point of view). Accept other assignments with consistent reasoning.
3. Customer data in India means a **transfer to a third country** (GDPR Chapter V): legal basis such as standard contractual clauses (India has no general adequacy decision — accept "check whether an adequacy decision exists"); **processor agreement** (Art. 28); security measures and access control; better: use **anonymised or synthetic test data** so that no personal data leave the EU.
4. E.g.: **product owner** and **architect** in-house (vision, priorities, architecture fit with booking and customer platform, API first), the two own developers work in the core team; feature team **nearshore** (Czechia) with regular joint sprints; **offshore** regression testing with synthetic data; a clear contract with deliverables, quality criteria and code ownership (source code and documentation belong to Bodensee Reisen, exit and hand-over). In-house roles: product ownership, architecture, vendor management, data protection and security responsibility.

Marking hint: two points for part 1, three points for part 2, two points for part 3, three points for part 4.
:::

## Exam-Style Task: Sourcing Strategy at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (sessions 2 and 5–14), a wholesaler of bathroom fittings with 850 employees and €320 million turnover, sells about 70 % of its goods via its **online order platform** to 4,000 installers; orders received by 14:00 are delivered the same day from the central warehouse. It is **acquiring a smaller wholesaler in the Saarland** and wants to open the platform as a **marketplace** for manufacturers and other wholesalers (worksheets 12–14). A large hospital group, one of its customers, asks its suppliers for evidence of information security (worksheet 7). Today's sourcing:

| Service | Today |
|---|---|
| Kurpfalz ERP | 20 years old, heavily customised, own server room; two people know the customisations |
| Online order platform | Hosted by an external provider; developed by six in-house developers |
| Saarland ERP | Standard cloud ERP (SaaS), 6 years old, little customisation |
| Saarland warehouse system | Own development, maintained by one developer |
| Integration | No platform yet; the architecture team proposes an integration platform (worksheet 14) |
| Service desk | Two employees, office hours only |

The board asks the CIO for a **sourcing strategy** for the next three years.

**Tasks:**

1. Explain **make or buy** and name **four criteria** for the decision. (4 points)
2. Recommend a sourcing decision for **four** of the services in the table (make, buy as SaaS/PaaS/IaaS, outsource as a managed service, or retire) and justify each with **one criterion**. (6 points)
3. Explain the difference between **IaaS, PaaS and SaaS** using the **online order platform** as an example: what would Kurpfalz still manage in each model? (3 points)
4. Your strategy leads to **multi-sourcing**. Name **two risks** of multi-sourcing for the same-day delivery promise and **two roles or capabilities** the retained IT organisation must have. (4 points)
5. Name **three elements** of the contract for the most critical service and **one compliance requirement** that results from the hospital group's request. (3 points)

::: answer lines=30
:::

::: solution
Marking guide (20 points):

**1. Make or buy (4 points)**

- Explanation (1 point): **make** — the enterprise develops and runs a solution or service itself; **buy** — it acquires standard software, a cloud service or a service from a provider; in between, buy a platform and build differentiating parts on top.
- Four criteria (3 points, 0.75 each, rounded), e.g.: **strategic importance** (differentiator vs. commodity, core competence tests); **specificity** and fit of market offerings; **market maturity**; **life-cycle cost** incl. transition and vendor management; **skills and capacity**; **risk and control** (availability, security, dependency, compliance).

**2. Four sourcing decisions (6 points, 1.5 each: decision 0.5, justification 1)**

- **Kurpfalz ERP**: **buy** — move to the **Saarland cloud ERP (SaaS)** or another standard ERP; ERP is a commodity with a mature market; know-how risk (two people), own server room. Accept a new standard ERP for both with reasoning.
- **Online order platform**: **make** (keep development in-house) — it is the differentiator for installers and the basis of the marketplace; buy the platform underneath (**PaaS**, or keep managed hosting/IaaS) to free developers from operations.
- **Saarland ERP**: **keep/invest as SaaS** — standard, little customisation; candidate target ERP.
- **Saarland warehouse system**: **retire** (move warehouse functions into the target ERP or a standard WMS) or **buy** a standard WMS — single developer, commodity function; accept "tolerate for the transition, then retire".
- **Integration platform**: **buy as iPaaS or managed service** — no skills in-house, speed for the acquisition and marketplace; keep integration architecture and principles in-house.
- **Service desk**: **outsource selectively** as a managed service for extended hours (e.g. from 6:00 to 22:00 for installers and warehouse) or keep first level in-house with an external partner for out-of-hours; criterion: availability for same-day delivery, commodity service; accept keeping it in-house with reasoning (close contact with installers).

**3. IaaS, PaaS, SaaS for the platform (3 points, 1 each)**

- **IaaS**: the provider runs data centre, servers, storage and virtualisation; Kurpfalz manages operating systems, middleware, databases, the platform software, data and access.
- **PaaS**: the provider also runs operating system, runtime and databases (e.g. container platform, managed database); Kurpfalz develops and runs the platform code and manages data and access.
- **SaaS**: Kurpfalz would use a standard e-commerce/marketplace product run by the vendor and only configure it; it keeps data and access rights — but loses the own development that differentiates the platform.

**4. Multi-sourcing (4 points)**

- Two risks (2 points, 1 each), e.g.: **unclear responsibility** when an order does not reach the warehouse (platform, iPaaS, ERP vendor, hosting provider each point to the others); **interfaces between providers** become a single point of failure for orders before 14:00; **inconsistent SLAs** — the end-to-end target is not underpinned; **vendor lock-in** in several places; more **contracts to manage** with a small IT team.
- Two retained roles or capabilities (2 points, 1 each), e.g.: **architecture planning** (target landscape, integration principles); **service integration** — end-to-end incident and change management across providers; **vendor/contract management** (informed buying, contract monitoring); **service owner** for "order to delivery" with an end-to-end SLA; security officer for supplier security.

**5. Contract and compliance (3 points)**

- Three contract elements (2 points), for the most critical service (e.g. the target ERP SaaS or the platform hosting): **SLAs** with availability during order hours and recovery times derived from the BIA (session 8); **security measures and incident reporting**; **audit rights**; **data location in the EU** and **processor agreement**; **price model and change process**; **exit** with data return and hand-over support.
- Compliance requirement (1 point): the hospital group falls under **NIS2** and must manage **supply chain security**; Kurpfalz must therefore show its own security level and that of its providers — e.g. security clauses and evidence (ISO/IEC 27001 certificates or audit reports) from its cloud and hosting providers. Also accept GDPR Art. 28 processor agreements for installer data.
:::

## Optional Challenge: One Provider for Everything? {.optional}

*Weinbau Kaiserstuhl eG* (sessions 1 and 11–14), a winegrowers' cooperative with 300 members and 60 employees, has no IT staff of its own. It uses an ERP package for orders and accounting, a web shop run by an agency, cellar sensors and plans a member portal; an iPaaS was proposed to connect shop, ERP and portal (worksheet 14). A regional IT service provider offers to take over **all IT** — workplaces, ERP operation, web shop, sensors and portal — for a fixed monthly fee.

1. Give **two arguments for** and **two arguments against** the single-provider offer compared with multi-sourcing (agency, ERP vendor, iPaaS, sensor supplier).
2. Even with one provider, which **retained capabilities** does the cooperative need? Who could take them on in an organisation without IT staff?
3. Name **three points** that the contract must settle so that the cooperative can **leave** the provider later.

::: answer lines=14
:::

::: solution
1. For: **one contact** and one contract for a small organisation without IT staff — no coordination between providers; **end-to-end responsibility** (no finger-pointing); predictable fixed fee; regional provider is close and speaks the language of the business. Against: **dependency** on one small provider (what if it fails or is sold?); the provider may be weak in some areas (e.g. web shop or IoT sensors) compared with specialists; less **negotiating power** at renewal; the fixed fee may hide poor value; know-how about the web shop moves away from the agency.
2. Retained capabilities: **IT strategy and priorities** linked to the business goals (30 % online), **informed buying** and **contract monitoring** (are the service levels met, is the price fair?), **data protection** responsibility for member and customer data, a basic **architecture overview** (which systems, which data, which interfaces). Who: a member of the management board as IT owner, supported by an office employee as coordinator and, if needed, an independent IT consultant for tenders and reviews.
3. E.g.: **return of all data** (ERP, shop, member data, sensor data) in documented, usable formats; **documentation** of configurations, interfaces and passwords/accounts in the cooperative's name; **ownership** of domains, licences and source code of the shop and portal; **hand-over support** by the provider for a defined period at agreed prices; **notice periods** that allow a re-tender.

Marking hint: four points for part 1, three points for part 2, three points for part 3.
:::

## References {.references}

- Carmel, E., & Abbott, P. (2007). Why "nearshore" means that distance matters. *Communications of the ACM, 50*(10), 40–46. https://doi.org/10.1145/1290958.1290959
- Cohen, L., & Young, A. (2006). *Multisourcing: Moving beyond outsourcing to achieve growth and agility*. Harvard Business School Press.
- Dibbern, J., Goles, T., Hirschheim, R., & Jayatilaka, B. (2004). Information systems outsourcing: A survey and analysis of the literature. *The DATA BASE for Advances in Information Systems, 35*(4), 6–102. https://doi.org/10.1145/1035233.1035236
- Directive (EU) 2022/2555 of the European Parliament and of the Council of 14 December 2022 on measures for a high common level of cybersecurity across the Union (NIS 2 Directive). (2022). *Official Journal of the European Union*, L 333, 80–152. http://data.europa.eu/eli/dir/2022/2555/oj
- Feeny, D. F., & Willcocks, L. P. (1998). Core IS capabilities for exploiting information technology. *Sloan Management Review, 39*(3), 9–21.
- Lacity, M. C., Willcocks, L. P., & Feeny, D. F. (1996). The value of selective IT sourcing. *Sloan Management Review, 37*(3), 13–25.
- Mell, P., & Grance, T. (2011). *The NIST definition of cloud computing* (NIST Special Publication 800-145). National Institute of Standards and Technology. https://doi.org/10.6028/NIST.SP.800-145
- Prahalad, C. K., & Hamel, G. (1990). The core competence of the corporation. *Harvard Business Review, 68*(3), 79–91.
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1–88. http://data.europa.eu/eli/reg/2016/679/oj
- Regulation (EU) 2022/2554 of the European Parliament and of the Council of 14 December 2022 on digital operational resilience for the financial sector (DORA). (2022). *Official Journal of the European Union*, L 333, 1–79. http://data.europa.eu/eli/reg/2022/2554/oj
- Regulation (EU) 2023/2854 of the European Parliament and of the Council of 13 December 2023 on harmonised rules on fair access to and use of data and amending Regulation (EU) 2017/2394 and Directive (EU) 2020/1828 (Data Act). (2023). *Official Journal of the European Union*, L, 2023/2854. http://data.europa.eu/eli/reg/2023/2854/oj
- Tiemeyer, E. (Ed.). (2023). *Handbuch IT-Management: Konzepte, Methoden, Lösungen und Arbeitshilfen für die Praxis* (8th ed.). Hanser.

Company names and figures in the tasks are fictitious training examples.
