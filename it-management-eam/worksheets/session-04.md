---
course: IT Management and EAM
session: 4
title: IT Controlling
subtitle: Practice tasks on IT costs, chargeback, portfolio decisions, business cases and the IT balanced scorecard
program: DHBW · Digital Business Management (Business IT) · Semester 4
---

This worksheet lets you practise the concepts of session 4: views on IT costs, chargeback models, IT project portfolio management, business cases and the IT balanced scorecard. Some tasks need simple calculations; a calculator is enough. The last core task is in the style of an exam question.

## Classifying IT Costs

Classify each cost item (Krcmar, 2015) by **cost type** (personnel, hardware, software and licences, external services, cloud), as **run** or **change**, and as **capex** or **opex**.

- a) Salaries of the service desk team
- b) New servers bought to replace old ones in the own data centre
- c) Monthly subscription fee for the cloud CRM
- d) External consultants who migrate data in the ERP replacement project
- e) Perpetual licences for a new CAD software, bought this year
- f) Electricity and cooling for the data centre

::: answer lines=6
:::

::: hint
Capex = investments that are capitalised and depreciated over several years. Opex = expenses in the year they occur. A replacement keeps things running; a project changes them.
:::

::: solution
- a) Personnel · run · opex
- b) Hardware · run (replacement keeps the existing service running; "change" is accepted if the student argues it is a modernisation project) · capex
- c) Cloud (or software and licences) · run · opex
- d) External services · change · opex (in some companies capitalised as part of the new system; accept with this reasoning)
- e) Software and licences · change (new software) · capex
- f) Usually counted as infrastructure or facility costs; run · opex. Students may say "none of the listed types": a good answer notes that data centre energy is often hidden in facility budgets and therefore missing in IT cost transparency.
:::

## Which Chargeback Model?

Recommend a chargeback model (no chargeback, allocation, chargeback by service, profit centre) for each situation and give one reason.

1. A small company with 80 employees and one IT administrator.
2. A group in which business units complain that "IT is too expensive" but use far more storage than they need.
3. A large IT subsidiary that wants to sell its data centre services to other companies.
4. A company that needs a quick and simple way to show business units their share of IT costs, without measuring usage.

Then explain what Ross et al. (1999) found about when chargeback actually influences business managers' IT decisions.

::: answer lines=10
:::

::: solution
1. **No chargeback** (cost centre): the effort of measuring and pricing services is higher than the benefit.
2. **Chargeback by service** (e.g. price per GB): makes usage visible and creates cost awareness, which reduces wasteful demand.
3. **Profit centre**: market logic, prices must be competitive with external providers.
4. **Allocation** (e.g. by headcount): simple and cheap, but weak link to actual use.

Ross et al. (1999): in only four of the ten organisations they studied did chargeback actually influence business managers' IT decisions. In those firms chargeback was used to build communication and a shared understanding of IT costs and benefits between IT and the business. The technical model matters less than how it is used.
:::

## Payback, NPV and ROI

An insurance company considers an AI solution that reads and classifies incoming customer mail.

- One-off costs: 600 k€ (licences, implementation, training)
- Running costs: 80 k€ per year
- Benefits: the work of 4 full-time clerks can be moved to other tasks; one full-time clerk costs 60 k€ per year
- Period: 5 years; discount rate 8 %

1. Calculate the annual net benefit and the simple **payback period**.
2. Calculate the **net present value** (NPV) over 5 years. Use the discount factors 0.926 · 0.857 · 0.794 · 0.735 · 0.681 for years 1–5.
3. Calculate the simple **ROI** over 5 years: (sum of net benefits − investment) / investment.
4. The head of the clerks says that realistically only 3 clerks can be moved. Recalculate payback and NPV. What do you learn?

::: answer lines=12
:::

::: hint
NPV = − investment + Σ (net benefit in year t × discount factor of year t). With the same net benefit every year, you can multiply it by the sum of the discount factors.
:::

::: solution
1. Benefits 4 × 60 = 240 k€; net benefit 240 − 80 = **160 k€ per year**. Payback = 600 / 160 = **3.75 years**.
2. Sum of discount factors = 3.993. NPV = −600 + 160 × 3.993 = −600 + 638.9 = **about +39 k€**. Positive, but small.
3. ROI = (5 × 160 − 600) / 600 = 200 / 600 = **33 %** over 5 years (not per year).
4. Benefits 180 k€; net benefit 100 k€. Payback = 600 / 100 = **6 years** (longer than the period). NPV = −600 + 100 × 3.993 = **about −201 k€**.

Lesson: the result depends heavily on one assumption (how many clerks are really freed, and whether the company actually reduces cost or reassigns staff). Business cases need evidence and an owner for each benefit (Ward et al., 2008), and a sensitivity analysis for the key assumptions.
:::

## Portfolio Decision with a Scoring Model

The IT steering committee of a regional energy supplier has a budget of **2.0 m€** for new projects. It scores proposals from 1 (poor) to 5 (very good) with these weights: strategic fit 40 %, value 30 %, risk 20 % (5 = low risk), urgency 10 %.

| Project | Cost | Strategic fit | Value | Risk | Urgency |
|---|---|---|---|---|---|
| A · Customer app relaunch | 1.2 m€ | 5 | 4 | 2 | 3 |
| B · Data warehouse modernisation | 0.8 m€ | 4 | 3 | 4 | 2 |
| C · E-mail archiving required by law | 0.3 m€ | 2 | 1 | 5 | 5 |
| D · Process automation in accounting | 0.5 m€ | 3 | 4 | 3 | 2 |

1. Calculate the weighted score of each project and rank them.
2. Which projects would you select within the budget if you followed the ranking strictly?
3. Is that a good portfolio? Discuss one problem and propose your final selection.

::: answer lines=10
:::

::: solution
1. A: 0.4·5 + 0.3·4 + 0.2·2 + 0.1·3 = 2.0 + 1.2 + 0.4 + 0.3 = **3.9** · B: 1.6 + 0.9 + 0.8 + 0.2 = **3.5** · C: 0.8 + 0.3 + 1.0 + 0.5 = **2.6** · D: 1.2 + 1.2 + 0.6 + 0.2 = **3.2**. Ranking: A, B, D, C.
2. A (1.2) + B (0.8) = 2.0 m€; budget used up, C and D are rejected.
3. Problem: C is **required by law**. Mandatory projects should not compete in the scoring; they are taken first (or financed from a separate compliance budget). Final selection: C (0.3), then A (1.2), then the next project that fits the remaining 0.5 m€, which is D (0.5) → total 2.0 m€. B is postponed. Further discussion points: A is the riskiest project; a portfolio view (McFarlan, 1981) checks whether the overall risk is acceptable. Scores are judgements; the weights themselves are a strategic decision.
:::

## The IT Balanced Scorecard

1. Assign each KPI to a perspective of the IT balanced scorecard: business contribution, user orientation, operational excellence or future orientation (Kaplan & Norton, 1992; De Haes et al., 2020).
   - a) Share of incidents solved within the agreed time
   - b) IT costs as a percentage of revenue
   - c) User satisfaction score in the annual survey
   - d) Training days per IT employee
   - e) Share of IT projects whose business benefits were confirmed after go-live
   - f) Share of the IT budget spent on innovation
2. Build a **cause-and-effect chain** using four of these KPIs, one from each perspective.
3. A CIO proposes "number of tickets closed per month" as the main KPI of the service desk. Explain why this is a poor KPI and suggest a better one.

::: answer lines=10
:::

::: solution
1. a) operational excellence · b) business contribution · c) user orientation · d) future orientation · e) business contribution · f) future orientation (business contribution is accepted if argued as a strategic budget split)
2. Example: more training days per IT employee (future) → more incidents solved in time (operational excellence) → higher user satisfaction (user orientation) → more projects with confirmed benefits / lower IT cost per revenue (business contribution).
3. It measures activity, not value: it rewards closing tickets quickly (even without solving the problem) and splitting tickets; more tickets can also mean worse IT. Better: share of incidents solved within the agreed time, first-contact resolution rate, user satisfaction after ticket closure, or lost working hours due to IT incidents.
:::

## Exam-Style Task: Route Planning at Rheinland Logistik

*Rheinland Logistik GmbH* (session 1) considers a cloud-based **route optimisation** service for its 300 trucks.

- One-off costs: 850 k€ (implementation, integration with the warehouse system, driver training)
- Running costs: 250 k€ per year (subscription)
- Fuel costs today: 3.0 m€ per year; the vendor promises 10 % savings from year 1
- The old planning tool is switched off: saves 60 k€ per year from year 1
- Less overtime for dispatchers and drivers: 150 k€ per year from year 2

1. Calculate the annual net benefits for years 1–5 and the simple **payback period**. (4 points)
2. Name two benefits that are not in the figures and classify them following Ward et al. (2008) (financial, quantifiable, measurable, observable). (2 points)
3. Name one risk and one critical assumption behind the figures. (2 points)
4. Who should be the **benefit owner**? Propose two KPIs to track after go-live and assign each to a perspective of the IT balanced scorecard. (4 points)

::: answer lines=18
:::

::: solution
Marking guide (12 points):

**1. Net benefits and payback (4 points)**

- Year 1: fuel 300 + old tool 60 − subscription 250 = **110 k€** (1 point)
- Years 2–5: 110 + 150 = **260 k€** per year (1 point)
- Cumulative: 110 · 370 · 630 · 890 → the 850 k€ are reached in **year 4** (1 point)
- Payback ≈ 3 + (850 − 630) / 260 = 3 + 0.85 ≈ **3.8 years** (1 point). "During year 4" without the decimal: full points if the cumulative values are shown.

**2. Non-financial benefits (2 points, 1 each with correct class)**

- e.g. lower CO₂ emissions (measurable), more reliable delivery times for customers (quantifiable or measurable), less stress for dispatchers (observable), better data for pricing tenders (observable).

**3. Risk and assumption (2 points)**

- Risk: integration with the warehouse system is delayed; drivers ignore the suggested routes; vendor raises the subscription price.
- Assumption: the 10 % fuel saving is realistic for this fleet (vendor promise, no evidence); fuel prices stay at today's level; overtime is actually reduced and not just shifted.

**4. Benefit owner and KPIs (4 points)**

- Benefit owner: head of transport operations or managing director of logistics, **not** the CIO, because the business must change how routes are planned and driven (2 points; 1 point if "business" without a role).
- Two KPIs with perspective (1 point each), e.g. fuel cost per 100 km (business contribution), on-time delivery rate (user orientation, as the "user" is the dispatching business), availability of the route service (operational excellence), share of drivers trained (future orientation).
:::

## References {.references}

- De Haes, S., Van Grembergen, W., Joshi, A., & Huygh, T. (2020). *Enterprise governance of information technology: Achieving alignment and value in digital organizations* (3rd ed.). Springer. https://doi.org/10.1007/978-3-030-25918-1
- Kaplan, R. S., & Norton, D. P. (1992). The balanced scorecard—Measures that drive performance. *Harvard Business Review, 70*(1), 71–79.
- Krcmar, H. (2015). *Informationsmanagement* (6th ed.). Springer Gabler. https://doi.org/10.1007/978-3-662-45863-1
- McFarlan, F. W. (1981). Portfolio approach to information systems. *Harvard Business Review, 59*(5), 142–150.
- Ross, J. W., Vitale, M. R., & Beath, C. M. (1999). The untapped potential of IT chargeback. *MIS Quarterly, 23*(2), 215–237. https://doi.org/10.2307/249752
- Ward, J., Daniel, E., & Peppard, J. (2008). Building better business cases for IT investments. *MIS Quarterly Executive, 7*(1), 1–15.
