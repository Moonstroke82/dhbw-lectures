---
course: IT Management and EAM
session: 5
title: IT Service Management I — ITIL 4
subtitle: Practice tasks on service concepts, the four dimensions, the service value chain, guiding principles and practices
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 5: services and value, outputs and outcomes, utility and warranty, service relationships, the four dimensions of service management, the service value system with its value chain and value streams, the seven guiding principles and the practices of ITIL 4 (AXELOS, 2019; see also Beims & Ziegenbein, 2023). The terms follow the session slides. The last core task is in the style of an exam question.

## Service Vocabulary

A university's IT centre offers a **video conferencing service** to all faculties. Classify each item with one of the terms: **output** · **outcome** · **utility** · **warranty** · **cost removed** · **risk removed** · **cost imposed** · **risk imposed**.

- a) Lecturers can hold online lectures for up to 500 students
- b) A meeting link is created automatically for every timetabled course
- c) Students who are ill can still follow the lecture
- d) The service is available 99.8 % of the time during the semester
- e) Faculties no longer need to buy and maintain their own conferencing licences
- f) Faculties pay an annual fee per lecturer to the IT centre
- g) Recordings are stored encrypted on servers in the EU
- h) Faculties depend on the IT centre's choice of tool and its release dates

::: answer lines=8
:::

::: hint
An **output** is what an activity delivers; an **outcome** is the result a stakeholder achieves with it. **Utility** is what the service does (fit for purpose); **warranty** is how well it does it (fit for use).
:::

::: solution
- a) **Utility** (a function that supports the outcome; the capacity of 500 participants is also a warranty aspect, accept with reasoning)
- b) **Output** (a deliverable the service produces)
- c) **Outcome** (the result for the students, enabled by the service)
- d) **Warranty** (availability)
- e) **Cost removed**
- f) **Cost imposed**
- g) **Warranty** (security); also **risk removed** (data protection risk is managed by the provider), accept either with reasoning
- h) **Risk imposed** (dependency on the provider)
:::

## Describing a Service

A logistics company's IT department provides a **mobile scanner service** to its warehouses: handheld scanners, the scanning app, Wi-Fi in the warehouse, a replacement pool and a support hotline.

1. Name the **customer**, the **users** and the **sponsor** of the service.
2. What does the **service offering** contain? Sort the elements into goods, access to resources and service actions.
3. Formulate two **utility** statements and two measurable **warranty** statements.
4. Explain why ITIL 4 says that value is **co-created**, using this example.

::: answer lines=12
:::

::: solution
1. Customer: head of warehouse operations (defines requirements, responsible for the outcomes). Users: warehouse staff. Sponsor: managing director or head of logistics who approves the budget (the head of warehouse operations can also be the sponsor; one person can hold several roles).
2. Goods: none in the narrow sense, unless scanners are handed over into the ownership of the warehouses (then goods); spare batteries could be goods. Access to resources: scanners from the pool, the scanning app, Wi-Fi, back-end systems. Service actions: replacing broken scanners, hotline support, installing app updates.
3. Utility: scan incoming and outgoing goods and book them directly in the warehouse system; show the storage location for each item. Warranty: 98 % of scanners ready at the start of each shift; broken scanner replaced within 30 minutes; Wi-Fi coverage in 100 % of the storage area; app response time below 1 second.
4. The IT department provides scanners, app and support, but value only arises when warehouse staff use them correctly in their processes (scan at the right point, report defects). Provider and consumer both contribute; poor use or unclear processes destroy value even if the technology works.
:::

## The Four Dimensions

The administration of a large city introduced a new IT service management tool. Six months later the project is seen as a failure. Read the findings and assign each to the **dimension** of service management that was neglected. Then propose one measure for each dimension.

1. Service desk staff were not trained and keep using e-mail and Excel lists.
2. The external company that provides second-level support for the school network was not connected to the tool.
3. The tool was configured with the vendor's standard workflow, which does not match how requests are approved in the city.
4. Nobody decided who owns the tool and who may change its configuration.
5. Data from the old ticket system was not migrated, so the history of recurring problems is lost.

::: answer lines=10
:::

::: solution
1. **Organisations and people** (skills, culture). Measure: training, champions in each team, management makes the tool mandatory and explains why.
2. **Partners and suppliers**. Measure: integrate the supplier via an interface or give it access; include tool use in the contract.
3. **Value streams and processes**. Measure: map the city's request and approval value streams first, then configure the tool to support them (with simplification).
4. **Organisations and people** (roles and responsibilities, governance). Measure: appoint a tool owner and a change process for the configuration.
5. **Information and technology**. Measure: migrate or archive historical data so that problem management can use it.

Key insight: the project only looked at technology; ITIL's principle "think and work holistically" asks for all four dimensions to be considered.
:::

## Guiding Principles

Name the guiding principle that is **applied** or **violated** in each situation and justify your answer.

1. An IT department introduces a new incident process for all 20 locations at once, without a pilot.
2. Before designing a new service catalogue, the team analyses which entries of the old catalogue users actually request.
3. A bank automates its account-opening workflow, including five manual checks that nobody can explain.
4. IT and the HR department set up a shared board that shows the status of all onboarding requests.
5. A service team measures the success of its new laptop service by asking users whether they can work better, not only by counting delivered devices.
6. The approval of a standard software installation needs signatures from three managers.

::: answer lines=8
:::

::: solution
1. **Progress iteratively with feedback** (violated): no pilot, no feedback before full roll-out.
2. **Start where you are** (applied): existing data and services are assessed before designing something new.
3. **Optimise and automate** (violated): automation before optimisation; also **keep it simple and practical** (violated).
4. **Collaborate and promote visibility** (applied).
5. **Focus on value** (applied): outcomes for users instead of outputs.
6. **Keep it simple and practical** (violated): steps that add no value. **Optimise and automate** is also accepted.

Several principles may apply; accept well-justified alternatives.
:::

## Mapping a Value Stream

At an insurance company, new employees often wait several days for a working laptop and system access. The value stream "**new employee is ready to work on day one**" consists of the following steps (in random order). Put them in a sensible order and map each step to a **value chain activity** (plan, improve, engage, design and transition, obtain/build, deliver and support).

- a) The laptop is configured with the standard image and the required applications
- b) The hiring manager submits an onboarding request via the portal
- c) On day one, the service desk hands over the laptop and explains the login
- d) IT analyses why 30 % of onboardings were late last quarter
- e) A laptop is taken from stock or ordered from the supplier
- f) User accounts and access rights for the role are created
- g) A week after the start, the manager confirms that the employee can work and gives feedback

Where do you expect waiting times, and which guiding principle would help to remove them?

::: answer lines=12
:::

::: hint
Some activities appear more than once in a value stream, and not every value stream uses all six activities in the same order.
:::

::: solution
Sensible order and mapping (alternatives possible):

1. b) Request via portal → **engage**
2. e) Laptop from stock or supplier → **obtain/build**
3. a) Configuration with standard image → **obtain/build** (or design and transition, if the student sees it as preparing the transition into use)
4. f) Accounts and access rights → **obtain/build** or **deliver and support** (accept both with reasoning)
5. c) Handover and login explanation → **deliver and support** (also design and transition: the service is transitioned into use)
6. g) Manager confirms and gives feedback → **engage**
7. d) Analysis of late onboardings → **improve**

Waiting times: between the request and the laptop order (late request, approvals, supplier delivery), and between account creation steps handled by different teams. Helpful principles: **optimise and automate** (trigger account creation automatically from the HR system after optimising the approval steps), **collaborate and promote visibility** (HR and IT share the onboarding status), **keep it simple and practical** (standard role packages instead of individual approvals).
:::

## Exam-Style Task: Mobile Sales at Kurpfalz Sanitär AG

*Kurpfalz Sanitär AG* (session 2) is building its online platform for installers. As a first step, the IT department offers a **mobile sales service** to the 60 field sales representatives: tablets with a product catalogue, live stock levels, an ordering app that is connected to the ERP system, and a support hotline. The head of sales asked for the service; the CFO approved the budget.

1. Explain the ITIL 4 understanding of a **service** and distinguish **output** and **outcome** with one example each from the case. (3 points)
2. Name the **customer**, the **users** and the **sponsor** of the mobile sales service. (2 points)
3. Formulate one **utility** and one measurable **warranty** statement for the service. (2 points)
4. Describe the value stream "**a new sales representative is fully equipped and can take orders**" in at least four steps and map each step to a **value chain activity**. (3 points)
5. Choose one **guiding principle** and explain how it should be applied when the service is introduced. (2 points)

::: answer lines=18
:::

::: solution
Marking guide (12 points):

**1. Service, output and outcome (3 points)**

- A service enables value co-creation by helping customers achieve the outcomes they want, without them having to manage specific costs and risks (1 point; own words are fine, "value co-creation" or "without managing costs and risks" must be present).
- Output, e.g. configured tablet, ordering app, daily stock data (1 point).
- Outcome, e.g. sales reps take orders at the installer's site and can promise delivery dates; more orders and fewer order errors (1 point).

**2. Roles (2 points)**

- Customer: head of sales (0.5) · users: field sales representatives (0.5) · sponsor: CFO (0.5) · correct explanation of at least one role (0.5).

**3. Utility and warranty (2 points)**

- Utility, e.g. show live stock levels and place orders directly in the ERP system (1 point).
- Warranty with a measure, e.g. app available 99.5 % between 7:00 and 20:00 on working days; broken tablet replaced within one working day; stock data at most 15 minutes old (1 point; no points without a measure).

**4. Value stream (3 points)**

- At least four sensible steps (1 point) and correct mapping (2 points), e.g.: head of sales requests equipment for the new rep → **engage**; tablet taken from stock and configured, accounts created → **obtain/build**; tablet handed over and the rep trained → **design and transition** or **deliver and support**; hotline supports the rep in the first weeks → **deliver and support**; feedback collected and the onboarding improved → **engage** and **improve**. Half a point per wrong mapping deducted.

**5. Guiding principle (2 points)**

- Principle named (0.5) and applied to the case with a concrete action (1.5), e.g. **progress iteratively with feedback**: pilot with five sales reps, collect feedback before rolling out to all 60; **focus on value**: measure success by orders taken on site, not by tablets delivered; **think and work holistically**: train sales reps, connect the ERP, agree support with the tablet supplier; **start where you are**: reuse the existing ERP product data and web shop catalogue.
:::

## Optional Challenge: Practices {.optional}

Assign each activity to an ITIL 4 **practice** and to its **group** (general management, service management, technical management).

1. A user cannot print; the service desk restores the service with a workaround.
2. Analysts look for the root cause of the printer failures that happen every Monday.
3. A planned update of the firewall rules is assessed and authorised before it is carried out.
4. IT and the HR department agree on the availability and response times of the HR system.
5. The contract with the cloud provider is reviewed and renegotiated.
6. A new version of the ordering app is moved into the production environment.
7. The list of all IT services that users can order is updated in the portal.
8. A security policy for mobile devices is written and enforced.

::: answer lines=8
:::

::: solution
1. Incident management · service management (the service desk practice is also involved)
2. Problem management · service management
3. Change enablement · service management
4. Service level management · service management
5. Supplier management · general management
6. Deployment management · technical management (release management is also accepted; it is a service management practice not shown on the slide)
7. Service catalogue management · service management
8. Information security management · general management

Session 6 covers incident, problem, change enablement, service level management and the service desk in detail.
:::

## References {.references}

- AXELOS. (2019). *ITIL Foundation: ITIL 4 edition*. TSO.
- Beims, M., & Ziegenbein, M. (2023). *IT-Service-Management in der Praxis mit ITIL®: Zusammenarbeit systematisieren und relevante Ergebnisse erzielen* (6th ed.). Hanser.

ITIL® is a registered trademark of PeopleCert group.
