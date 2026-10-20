---
course: Data Management
session: 1
title: Why Data Matters
subtitle: Practice tasks on the value of data and the key terms Data Management, BI, Business Analytics, Data Science and Big Data
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 1 on your own or in a study group. You need no software, only the slides of session 1. Most tasks have more than one defensible answer: what counts is a clear justification with the terms from the session. Task 7 is in the style of an exam question.

## Terms and Their Key Questions

Complete the table. For each term, write the **key question** it answers and one **example** from your training company or your daily life (not from the slides).

| Term | Key question | Your example |
|---|---|---|
| Data Management | | |
| Business Intelligence | | |
| Business Analytics | | |
| Data Science | | |
| Big Data | | |

::: answer lines=8
:::

::: solution
Key questions (as on the comparison slide; equivalent wording is fine):

- **Data Management:** Is our data available, correct, secure and allowed to be used? It covers plans, policies and practices that deliver, control, protect and enhance the value of data throughout its lifecycle (DAMA International, 2017). Example: a company defines who is responsible for the quality of supplier master data in SAP.
- **Business Intelligence:** What happened, and where do we stand? Example: a monthly dashboard of open orders per sales region.
- **Business Analytics:** Why did it happen, what will happen, what should we do? Example: forecasting the number of support tickets next week to plan staff.
- **Data Science:** What can we learn from data (with scientific methods)? Example: building and testing a model that predicts which customers will cancel their contract.
- **Big Data:** No key question of its own; it **describes the data** (volume, velocity, variety …). Example: the stream of position data from all delivery vans of a parcel service.

Marking hint: an example is correct if it fits the key question. A frequent error is to give a method as example for Big Data ("using AI"); Big Data is a property of data, not a method.
:::

## Which Term Fits?

Assign each situation to the term that fits **best** and give a one-line reason. If two terms fit, name both and explain.

1. A hospital shows the current bed occupancy per ward on a screen in the management office.
2. An insurance company appoints a data owner for customer addresses and defines rules for how addresses must be entered.
3. A public transport company analyses why passenger numbers on one line dropped after the timetable change.
4. A logistics company calculates the best route for each of its 400 vans every morning, taking traffic and delivery windows into account.
5. An online shop processes several thousand click events per second from its website and app.
6. A research team at a car manufacturer tests whether sensor data from engines can predict failures, and publishes the method.
7. A city administration decides which of its datasets may be published as open data.

::: answer lines=8
:::

::: solution
1. **BI / descriptive analytics:** shows what is happening now; no explanation or forecast.
2. **Data Management** (data governance and data quality): responsibilities and rules for data.
3. **Business Analytics, diagnostic level:** asks *why* something happened.
4. **Business Analytics, prescriptive level:** recommends an action (route) by optimisation.
5. **Big Data** (velocity, volume): describes the data stream. What the shop does with it is a separate question.
6. **Data Science** (and predictive analytics): extracting knowledge with a scientific approach and a predictive model.
7. **Data Management** (governance, legal use of data): this is about whether data may be used and shared, not about analysing it.

Accept other answers with a sound reason, e.g. 6 as "predictive analytics" or 1 as "BI with big data" if the student argues with the data volume.
:::

## Four Analytics Questions for One Business

A regional bakery chain with 25 branches throws away too much bread every evening. Formulate **one concrete business question** for each level of business analytics (descriptive, diagnostic, predictive, prescriptive; based on Delen & Ram, 2018), and name the **data** you would need for each.

::: answer lines=10
:::

::: hint
A good business question is specific: it names what is measured, for which unit (branch, product, day) and for which period.
:::

::: solution
Example answer:

- **Descriptive:** How many loaves of each product did each branch throw away per day in the last three months? Data: production quantities, sales from the cash registers, waste records.
- **Diagnostic:** Why does branch 12 throw away more than similar branches? Is it linked to weather, holidays or a nearby competitor? Data: waste and sales per branch, weather data, holiday calendar, location data.
- **Predictive:** How many rolls will branch 12 sell next Saturday? Data: sales history, weather forecast, calendar (holidays, school holidays, local events).
- **Prescriptive:** How many rolls should each branch bake and when, so that waste stays below 5 % and fewer than 2 % of customers find empty shelves? Data: the forecasts above, production costs and capacities, targets for waste and availability.

Marking hint: each level needs a question that really belongs to it (a "why" for diagnostic, a forecast for predictive, a recommended decision for prescriptive) and data that could actually answer it.
:::

## Big Data or Not?

For each case, decide which of the **Vs** (volume, velocity, variety, veracity, variability, value; Laney, 2001; Gandomi & Haider, 2015) are relevant, and whether you would call it Big Data. Justify briefly.

1. A craft brewery stores about 2,000 invoices per year in an Excel file.
2. A municipal utility receives electricity readings every 15 minutes from 300,000 smart meters.
3. A brand agency monitors what people post about its clients on social media: texts, images and short videos in many languages.

::: answer lines=8
:::

::: solution
1. **Not Big Data.** Small volume, low velocity (a few invoices a day), one structured format. An Excel file or a small database is enough.
2. **Big Data**, mainly **volume** and **velocity**: 300,000 × 96 readings ≈ 29 million readings per day, arriving continuously. Variety is low (structured readings); **veracity** matters (faulty or missing meter readings).
3. **Big Data**, mainly **variety** (text, image, video, several languages) and **veracity** (irony, fake accounts, bots), plus velocity at peaks (**variability**, e.g. during a shitstorm). Value density is low: most posts are irrelevant.

Marking hint: the classification is less important than the justification with the right Vs. Students should not call case 1 Big Data just because it is "a lot of data for a small company".
:::

## Case Analysis: When Does Data Create Value?

A car dealer group with six workshops wants to use its workshop data (vehicle, mileage, repairs, customer contact data) to send customers **personalised service reminders**, e.g. "Your brake pads will probably need replacing in about two months."

1. Which of the four ways in which data creates value (session 1) does this idea address? There can be more than one.
2. Data only creates value if it is available, fit for purpose, understood, allowed to be used and protected. For each of the five conditions, describe **one concrete risk** in this case.

::: answer lines=12
:::

::: solution
1. Mainly **new products and services** (a data-based service for customers) and **better decisions** (planning workshop capacity). Possibly **efficient operations** (better utilisation of the workshops). Compliance and risk does not fit as the main goal.
2. Example risks (one per condition is enough):
  - **Available:** each workshop runs its own system or keeps paper records, so the data cannot be brought together.
  - **Fit for purpose:** mileage was entered incorrectly or not at all; customers have sold their car, so the reminder reaches the wrong person.
  - **Understood:** "repair date" means the order date in one workshop and the completion date in another; nobody knows exactly what a column means.
  - **Allowed to be used:** customers gave their contact data for the repair, not for advertising. Sending reminders needs a legal basis or consent (session 19).
  - **Protected:** a list of customers and their cars leaks, or too many employees can access it.
:::

## Read a Claim Critically

A business magazine headline says: **"Study proves: data analytics makes every company 6 % more productive."** It refers to the study by Brynjolfsson et al. (2011) from session 1. Name **three problems** with this headline and rewrite it so that it is correct.

::: answer lines=8
:::

::: solution
Problems (any three):

- **"Proves":** the study shows a statistical **association**, not proof of a causal effect for every case.
- **"Every company":** the sample consisted of 179 large, publicly traded US firms; small firms, other countries or industries are not covered.
- **"Data analytics":** the study measured **data-driven decision making** in organisations, not the use of a particular analytics tool.
- **"6 %":** the study reports an effect of about 5–6 % in output and productivity, beyond what the firms' other investments and IT use would lead us to expect; the headline drops this condition.
- A single study is not a settled finding.

Possible correct headline: "Study of 179 large US firms: companies that decide based on data are about 5–6 % more productive than expected from their IT investment."
:::

## Exam-Style Task: BI, Data Science and Data Management

This task is in the style of an exam question.

1. Define **Business Intelligence** and **Data Science**, and explain **two differences** between them.
2. Explain why **Data Management** is a prerequisite for both. Use one example.

::: answer lines=14
:::

::: solution
Model answer:

1. **Business Intelligence** comprises techniques, technologies, systems and practices that analyse critical business data so that a company understands its business and market better and can make timely decisions (Chen et al., 2012). **Data Science** is the set of fundamental principles that guide the extraction of knowledge from data (Provost & Fawcett, 2013). Differences, for example:
  - **Key question:** BI asks what happened and where we stand; data science asks what we can learn from data, often what will happen.
  - **Methods:** BI uses reports, dashboards and OLAP on a data warehouse; data science uses statistics, machine learning and experiments.
  - **Data:** classic BI works mainly with structured internal data; data science often also uses semi-structured and unstructured or external data.
2. Both build on data that is available, correct, understood, allowed to be used and protected, and data management provides exactly this ("garbage in, garbage out"). Example: if customer master data contains duplicates, the BI report shows too many customers, and a churn model learns from wrong data.

Marking guide (8 points):

- Definition of BI with its decision-support purpose: 2 points
- Definition of data science as extracting knowledge from data: 2 points
- Two correct differences, 1 point each: 2 points
- Data management as a prerequisite, with a convincing example: 2 points (1 for the argument, 1 for the example)

Exact wording of the definitions is not required; the core idea must be clear.
:::

## References {.references}

- Brynjolfsson, E., Hitt, L. M., & Kim, H. H. (2011). *Strength in numbers: How does data-driven decisionmaking affect firm performance?* SSRN. https://doi.org/10.2139/ssrn.1819486
- Chen, H., Chiang, R. H. L., & Storey, V. C. (2012). Business intelligence and analytics: From big data to big impact. *MIS Quarterly, 36*(4), 1165–1188. https://doi.org/10.2307/41703503
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Delen, D., & Ram, S. (2018). Research challenges and opportunities in business analytics. *Journal of Business Analytics, 1*(1), 2–12. https://doi.org/10.1080/2573234X.2018.1507324
- Gandomi, A., & Haider, M. (2015). Beyond the hype: Big data concepts, methods, and analytics. *International Journal of Information Management, 35*(2), 137–144. https://doi.org/10.1016/j.ijinfomgt.2014.10.007
- Laney, D. (2001). *3D data management: Controlling data volume, velocity, and variety* (Application Delivery Strategies, File 949). META Group.
- Provost, F., & Fawcett, T. (2013). Data science and its relationship to big data and data-driven decision making. *Big Data, 1*(1), 51–59. https://doi.org/10.1089/big.2013.1508
