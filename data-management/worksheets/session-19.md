---
course: Data Management
session: 19
title: Access to Data: Legal and Organisational Aspects
subtitle: Practice tasks on personal data, legal bases and consent, data subject rights, the Data Act, the Data Governance Act and the AI Act, data licences and data governance roles — teaching material, not legal advice
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 19 on your own or with your project team. **It is teaching material, not legal advice:** the tasks train you to recognise legal and organisational questions about data and to argue with the right concepts; a real case is decided by an organisation's data protection officer or legal department. You do not need to know article numbers by heart — the numbers in the solutions are there so that you can look up the official texts on EUR-Lex. Tasks 1, 2, 4, 5, 6 and the exam-style task can be done on paper. Task 3 needs SQLite (in Jupyter with Python's `sqlite3`, or the SQLite command-line tool) and the coworking script [coworking-privacy-session19.sql](data/coworking-privacy-session19.sql). The in-class hands-on on the bike shop uses [bikeshop-privacy-session19.sql](data/bikeshop-privacy-session19.sql). All names and data are fictional. The terms follow the session slides, which are based on the GDPR (Regulation (EU) 2016/679, 2016), the Data Act (Regulation (EU) 2023/2854, 2023), the Data Governance Act (Regulation (EU) 2022/868, 2022), the AI Act (Regulation (EU) 2024/1689, 2024, as amended by Regulation (EU) 2026/1744, 2026), Khatri and Brown (2010), DAMA International (2017) and DalleMule and Davenport (2017). Dates and the status of laws were checked on 22 October 2026. The results in the solutions were produced with SQLite 3.45.1.

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. Pseudonymised data is no longer personal data, because the names have been replaced by codes.
2. A company that uses a cloud newsletter service remains responsible for the subscribers' data as the controller.
3. Consent is the legal basis that every processing of personal data needs.
4. A pre-ticked box on a sign-up form can be valid consent if the person does not untick it.
5. The GDPR requires the controller to answer a request for access within one month, with an extension possible for complex requests.
6. The Data Act gives the user of a connected product the right to have the product's data shared with a third party of the user's choice.
7. The Data Governance Act obliges public bodies to publish all their data as open data.
8. Under the AI Act, training data of high-risk AI systems must be relevant, sufficiently representative and as free of errors and complete as possible.
9. Data published under CC BY 4.0 may be used commercially if the source is credited, the licence is linked and changes are indicated.
10. The data steward is the business manager who is accountable for a data domain and decides who may use the data.

::: answer lines=10
:::

::: solution
1. **False.** Pseudonymised data is still personal data, because the person can be re-identified with the additional information (the key) that exists somewhere; only anonymous data is outside the GDPR (Art. 4(5), Recital 26).
2. **True.** The newsletter service is a processor; the controller stays responsible and needs a processing contract (Art. 28).
3. **False.** Consent is one of six legal bases (Art. 6(1)); contract, legal obligation, vital interests, public task or legitimate interests can apply instead — and consent should not be used where another basis applies.
4. **False.** Silence, inactivity and pre-ticked boxes are not consent; consent needs a statement or clear affirmative action (Art. 4(11), Recital 32).
5. **True.** (Art. 12(3): within one month; extendable by two further months, with notice and reasons within the first month.)
6. **True.** (Art. 5 Data Act; the data may not be used to develop a competing product, and DMA gatekeepers cannot be such third parties.)
7. **False.** The DGA sets conditions under which public bodies **may** allow re-use of **protected** data (confidential, IP-protected, personal); it creates no obligation to allow re-use (Art. 1). Open data of public bodies is the subject of the Open Data Directive.
8. **True.** (Art. 10(3) AI Act.)
9. **True.**
10. **False.** That is the **data owner**; the data steward does the day-to-day work on definitions, quality rules and fixing errors.

Marking: one point per statement; a false statement needs a correct correction for the point.
:::

## The Sports Club: Personal Data, Legal Basis, Principle

The sports club (about 600 members, run by volunteers) processes the data below. For each item, say (a) whether **personal data** is involved and whether it is a **special category**, (b) the **legal basis** that fits best — or that the processing is not allowed as described — and (c) one **principle** of Art. 5 GDPR the club must watch.

1. The membership list with name, address, date of birth and bank account for the membership fee
2. Medical certificates that members of the diving department must hand in before training
3. Photos of the summer festival on the club's public website
4. The club passes the names of its tennis players to the regional tennis federation, which requires them for the league
5. The treasurer keeps the fee payments of members who left eight years ago "for statistics"
6. Number of members per department and age group in the annual report

::: answer lines=12
:::

::: hint
First ask: does a contract (the membership) or a legal or association rule already cover it? Consent is the right basis only where the person has a real choice. For the medical certificates, think about which kind of data health data is.
:::

::: solution
1. Personal data, no special category. **Contract** (Art. 6(1)(b)): the membership is a contract; fees need the bank account. Principle: **data minimisation** (date of birth only if needed, e.g. for youth fees) and **storage limitation** (delete after leaving, except what must be kept).
2. Personal data, **special category** (health data, Art. 9). Needs a basis in Art. 6 **and** an exception in Art. 9(2) — typically **explicit consent** (Art. 9(2)(a)) or a legal/safety rule. Principle: **integrity and confidentiality** (only the diving instructor may see the certificates, locked away) and **storage limitation** (only the expiry date needs to be recorded; return or delete the certificate).
3. Personal data (people are recognisable). Small group photos of a public event: **legitimate interests** (Art. 6(1)(f)) are arguable for reporting on club life, close-ups or photos of children need **consent** (Art. 6(1)(a)); accept either with a reason. Principle: **transparency** (inform members at the festival) — and a right to **object**.
4. Personal data. **Contract** (Art. 6(1)(b)) or **legitimate interests**: playing in the league as a club member requires the registration; accept with a reason. Principle: **purpose limitation** (the federation receives only what the league needs).
5. Personal data. **Not allowed** as described: no purpose that needs names; the legal retention for accounting records (in Germany booking vouchers 8 years, books 10 years, § 147 AO; Abgabenordnung, n.d.) is a different purpose. Principle: **storage limitation** — for statistics, keep aggregated numbers and delete the personal data.
6. **No** personal data, if the groups are large enough that no single member can be identified (aggregated). Small groups (e.g. one member over 80 in the diving department) could identify a person — then merge age groups.

Marking: half a point each for (a), (b) and (c) per item (9 points); the legal basis needs a reason where several are possible.
:::

## Lab: Consents, Requests and Re-identification at the Coworking Space

Load [coworking-privacy-session19.sql](data/coworking-privacy-session19.sql) into a database of its own. Use **31 March 2027** as today's date. Until June 2026 new members filled in a paper **welcome pack** in which all consent boxes were **ticked in advance**; since then the web form `web-2026` with unticked boxes is used.

1. Which members may currently appear in **photos** on the website? Write one query. Which members does a naive query "consent given at some point" add — and why must they be left out?
2. Which members may receive the **newsletter**? Member M02 objected to marketing e-mails in February. Does that change your answer?
3. Compute the **deadline** of every request in `cw_request` (one month) and a status column: answered in time, answered late, open in time, open and overdue.
4. Request 4 is an **erasure** request by a former member. Which of her or his data must be deleted, and which may or must be kept? Name the legal reason.
5. The coworking space wants to give a research group a "**pseudonymised**" export without names and e-mails: `member_no` replaced by a random code, plus `birth_year`, `postcode`, `profession` and `plan`. How many members are **unique** by postcode, birth year and profession? What do you conclude?
6. Coarsen the export (first two digits of the postcode, birth decade, no profession). How many members are still unique? Is the export now anonymous?

::: answer lines=18
:::

::: hint
For 1, combine three conditions: a `given` event with the right form, and `NOT EXISTS` a later `withdrawn` event for the same member and purpose. For 3, `date(received_on, '+1 month')` gives the deadline. For 5, group by the three columns and count the groups of size 1: `sum(n = 1)` in an outer query.
:::

::: solution
**1.**
```sql
SELECT g.member_no, m.name, g.event_on
FROM cw_consent g JOIN cw_member m USING (member_no)
WHERE g.purpose = 'photos' AND g.action = 'given' AND g.form = 'web-2026'
  AND NOT EXISTS (SELECT 1 FROM cw_consent w
                  WHERE w.member_no = g.member_no AND w.purpose = 'photos'
                    AND w.action = 'withdrawn' AND w.event_on > g.event_on)
ORDER BY g.member_no;
```

Result: **M04, M07, M09, M12, M15** (five members). A naive query adds M01, M02 and M11 (welcome pack with pre-ticked boxes: no valid consent, Recital 32) and M06 and M14 (withdrawn on 2026-12-03 and 2027-03-20; withdrawal must be as easy as giving consent and stops further use, Art. 7(3)). Good answers note that M12 left at the end of February 2027: his consent was not withdrawn, but the space should ask whether a former member still wants to be shown — and photos already published must be removed for M06 and M14.

**2.** The same query for `purpose = 'newsletter'` gives **M05, M06, M07, M15**. M01 and M02 consented only via the welcome pack (no valid consent). M02's objection to marketing (Art. 21(2)–(3)) does not change the result, because M02 has no valid consent anyway; it must be recorded so that she is also excluded from any future marketing.

**3.**
```sql
SELECT request_id, member_no, kind, received_on, answered_on,
       date(received_on, '+1 month') AS deadline,
       CASE WHEN answered_on IS NULL AND date(received_on, '+1 month') < '2027-03-31'
                 THEN 'open, overdue'
            WHEN answered_on IS NULL THEN 'open, in time'
            WHEN answered_on > date(received_on, '+1 month') THEN 'answered late'
            ELSE 'answered in time' END AS status
FROM cw_request ORDER BY request_id;
```

Requests 1, 3 and 5 answered in time; **request 2 (access, M11) answered late** (deadline 2027-02-25, answered 2027-03-02) — unless the space had told her within the first month that it needed an extension (Art. 12(3)); request 4 open, deadline 2027-04-01; request 6 open, deadline 2027-04-10. Accept a deadline rule that counts 30 days if stated.

**4.** Delete (Art. 17(1): no longer needed for the purpose, membership ended): profile and contact data in the booking app, badge scans, photos (consent can no longer be relied on once the person asks for erasure), newsletter data. Keep: **invoices and accounting records** — a legal obligation to retain them (Art. 17(3)(b); in Germany § 147 AO, Abgabenordnung, n.d.) — but only in the accounting system with restricted access, and delete them when the retention period ends. The answer to the member must say what was deleted and what is kept and why.

**5.**
```sql
SELECT sum(n) AS members, sum(n = 1) AS unique_members
FROM (SELECT postcode, birth_year, profession, count(*) AS n
      FROM cw_member GROUP BY postcode, birth_year, profession);
```

16 members in 11 groups; **7 members are unique** (M02, M06, M07, M09, M11, M12, M15). Anyone who knows, e.g., that the psychotherapist born in 1972 lives in 69120 can find M11's bookings. The export is **pseudonymised, not anonymous** — still personal data (Recital 26); it needs a legal basis and safeguards for the research group.

**6.**
```sql
SELECT sum(n) AS members, sum(n = 1) AS unique_members
FROM (SELECT substr(postcode, 1, 2) AS area, (birth_year / 10) * 10 AS decade, count(*) AS n
      FROM cw_member GROUP BY area, decade);
```

Still **3 unique members**: M09 (area 01, 1980s), M06 (area 67, 1970s) and M11 (area 69, 1970s). Not anonymous yet: merge or suppress these groups (e.g. "other area"), or give the research group only aggregates. Even then the `plan` column and the booking times can single people out — anonymisation must consider all columns and what the recipient already knows.

Marking: one point per question; 1 needs both the form condition and the withdrawal; 5 needs the conclusion "pseudonymised, still personal data".
:::

## Which Law, Which Licence? The Food Co-op

The food co-op plans several data projects. For each, name the **EU law(s)** or the **licence** that answer the question, and give the answer in one or two sentences.

1. The co-op's cooling room has a connected compressor. The manufacturer reads its sensor data; the co-op wants the data sent to an independent refrigeration engineer.
2. The co-op wants to show its pickup points on a map built from **OpenStreetMap** data and publish the combined database of pickup points and opening hours on its website.
3. The co-op uses rainfall data of the Deutscher Wetterdienst (CC BY 4.0) in a chart in its member newsletter. Write the attribution line.
4. The city's open data portal publishes market locations under "Datenlizenz Deutschland – Namensnennung – Version 2.0". What must the co-op do when it uses them?
5. A non-profit research institute asks members to donate their shopping data for a nutrition study, through a registered organisation.
6. The co-op wants to move its member database from cloud provider A to provider B. Provider A wants a high exit fee in 2027.

::: answer lines=12
:::

::: solution
1. **Data Act** (Chapter II): the co-op is the user of a connected product; it can ask the data holder (manufacturer) to make the data available to a third party of its choice, the engineer (Art. 5), without charge to the user; the engineer may not use it to build a competing compressor. Note: if the manufacturer were a micro or small enterprise, the obligations would not apply (Art. 7(1)).
2. **ODbL 1.0** (OpenStreetMap): credit OpenStreetMap and state the licence; because the co-op publishes a **derived database** built on OSM data, it must be shared under the same licence (share-alike). Using only a rendered map image with attribution is a simpler alternative (OpenStreetMap Foundation, n.d.).
3. E.g. "Data: Deutscher Wetterdienst, CC BY 4.0 (link to the licence); monthly totals computed by the food co-op." — source, licence with link, and an indication of changes (Creative Commons, n.d.; Deutscher Wetterdienst, 2024).
4. A source note with the name of the provider (the city), the licence name "dl-de/by-2-0" with a link to the licence text, and a link to the dataset; if the co-op changes the data, the note must say that it was changed. Commercial and non-commercial use are allowed (GovData, n.d.).
5. **Data Governance Act** (data altruism: voluntary sharing for general-interest purposes such as research, through a recognised data altruism organisation) **and GDPR** (shopping data relates to members; consent is the usual basis). Accept "GDPR consent" alone for half the credit.
6. **Data Act** (Chapter VI, switching between data processing services): from 12 January 2027 providers may no longer charge for switching (Art. 29); before that only at cost. Also check the contract and the GDPR processing contract with provider B.

Marking: one point per item (law/licence plus a correct consequence).
:::

## Data Governance at the Coworking Space

The coworking space has grown to three locations and 25 staff. Data problems pile up: nobody knows who may approve a new data export, the booking app's member records contain duplicates, the IT service provider asks who decides on backup periods, and marketing wants to analyse badge scans to plan events.

1. Assign the roles **data owner**, **data steward**, **data custodian** and **data user** for the member data. Who in the coworking space could hold each role?
2. Which of the five **decision domains** (data principles, data quality, metadata, data access, data lifecycle) do the four problems above belong to?
3. Marketing's badge-scan idea: is it data **offence** or **defence**? Which legal questions must the data owner answer before saying yes?
4. Does the coworking space need a **chief data officer**? Give a reason, and say who should take over the CDO's tasks if not.
5. The managing director wants to appoint the head of marketing as **data protection officer**. Give one argument against it.

::: answer lines=14
:::

::: solution
1. **Owner**: the head of community/member services (business, accountable for member data: decides who may use it and what quality is needed). **Steward**: a community manager who knows the booking app — defines fields, sets quality rules, cleans duplicates, answers questions. **Custodian**: the IT service provider (runs, secures and backs up the booking app and the lake). **Users**: front desk, finance, marketing — use the data under the rules. Accept other people if the role meaning is right (owner = accountable business role; steward = day-to-day; custodian = IT).
2. Approving exports → **data access**; duplicates → **data quality**; backup periods → **data lifecycle** (and access/security); badge-scan analysis for a new purpose → **data principles** (which uses of data are acceptable) and **data access**. (Khatri & Brown, 2010.)
3. **Offence** (creating value: better events). Legal questions: is the new purpose compatible with the original purpose of the badge scans (building security; Art. 5(1)(b), 6(4))? Which legal basis applies — legitimate interests with a balancing test, or consent? Can the analysis use aggregated or anonymised data (counts per hour) instead of personal data (minimisation)? How long are the scans kept (storage limitation; worksheet 18: retention date)? Are members informed (transparency)?
4. A dedicated CDO is usually not justified for 25 staff; the tasks (data strategy, governance council, priorities) can be held by the managing director or a member of the management team as part of their role, with a small governance meeting of the data owners. Accept "yes" if the student argues with data as the core of the business model (e.g. selling occupancy analytics) — the decision depends on the strategy.
5. The DPO must not have a conflict of interests and must be able to monitor independently (GDPR Art. 38(3) and (6)): the head of marketing decides on marketing uses of personal data and would have to monitor her or his own decisions. (Whether a DPO is required at all: in Germany from 20 persons regularly processing personal data automatically, § 38 BDSG — likely here; Bundesdatenschutzgesetz, n.d.)

Marking: one point per question; 1 needs four correct role descriptions.
:::

## Exam-Style Task: Data at the Car-Sharing Company

This task is in the style of an exam question. Teaching material, not legal advice.

The car-sharing company (1,800 cars in eight cities) collects from every car the **GPS position** every 30 seconds during a trip, **battery and engine data**, and **error codes**. Customers register in an app with name, address, date of birth, driving licence number and payment data. The company wants to:

- (A) send customers **offers** for weekend trips by e-mail,
- (B) give the **car manufacturer's** independent competitor, a repair network, access to the error codes of its own cars,
- (C) publish an **open data** set "trips per station and hour" for the city,
- (D) train an AI model that **decides automatically** which customers get a lower deposit, based on their driving behaviour.

1. Name **three** kinds of personal data in the case and explain why the GPS positions are personal data although they contain no name. (2 points)
2. Give the **legal basis** for (A) and two conditions that the company's sign-up form must meet. (2 points)
3. Which law gives the company, as the **user** of the connected cars, a right in (B)? Name the right and **one** limit. (2 points)
4. For (C): what must the company do so that the published data is not personal data, and which **licence** would you recommend? Give a reason. (2 points)
5. For (D): explain why the AI Act's **data governance** requirements may apply, and name **two** of them. (1 point)
6. Name the **data owner** and the **data steward** you would appoint for the trip data, with one task each. (1 point)

::: answer lines=24
:::

::: solution
Marking guide (10 points).

**1.** (2 points; one for three kinds, one for the explanation) E.g. name, address, date of birth, driving licence number, payment data, GPS positions of trips, driving behaviour derived from engine data. GPS positions are **personal data** because each trip is linked to a booking and thereby to an identified customer (indirect identification via the booking or customer number); even without the booking, movement patterns (home, workplace) make a person **identifiable** (Art. 4(1), Recital 26).

**2.** (2 points) **Consent** (Art. 6(1)(a)) — e-mail advertising generally needs prior consent (in Germany § 7 UWG, Gesetz gegen den unlauteren Wettbewerb, n.d., with a narrow exception for existing customers and the company's own similar services if they were told they can object). One point for consent with a reason. One point for two conditions: an **unticked** box / clear affirmative action (no pre-ticked box); **specific** and separate from accepting the terms of use (not a condition for renting); **informed** (who, what, how often, right to withdraw); withdrawal **as easy** as giving consent (unsubscribe link); the company can **prove** it (consent log, e.g. double opt-in).

**3.** (2 points) The **Data Act**: the user of a connected product can access the product data and have it made available to a **third party** of its choice (Art. 4–5), free of charge for the user, in a machine-readable format (one point). One limit (one point), e.g.: the repair network may not use the data to develop a **competing product** (a car); **trade secrets** of the manufacturer are protected; a DMA **gatekeeper** cannot be the third party; **micro and small** manufacturers are exempt; personal data in the error codes (linked to trips and customers) still needs a GDPR legal basis.

**4.** (2 points) Make it **anonymous**: aggregate trips per station and hour, drop customer and car identifiers, suppress or merge cells with very few trips (e.g. fewer than five) so that no single trip or person can be singled out; check re-identification with other data (Recital 26). One point for anonymisation with at least two concrete measures. Licence (one point): **CC BY 4.0** (re-use with attribution; the format of high-value datasets) or **CC0** (no conditions, easiest re-use, e.g. in other open datasets); a share-alike licence (ODbL) is possible if the company wants derived databases to stay open. The reason must fit the choice.

**5.** (1 point) Deciding about customers' deposits based on their behaviour is close to **creditworthiness/credit scoring**, a high-risk use case in Annex III of the AI Act (accept the argument "may be high-risk, check Annex III"); then Art. 10 applies (from 2 December 2027 for Annex III systems). Requirements (any two, half a point each): documented data governance (origin and purpose of the data, preparation such as cleaning and labelling); examination for **bias** and measures against it (e.g. drivers in rural areas or older drivers disadvantaged); data **relevant** and **sufficiently representative**; as **free of errors** and **complete** as possible; data gaps identified. A good answer also mentions that the GDPR applies in parallel (automated decisions, Art. 22).

**6.** (1 point; half for each role with a task) **Owner**: head of operations or fleet (business) — decides who may use the trip data and for what (e.g. approves the open data release in C), sets quality requirements. **Steward**: a data analyst in operations — maintains definitions ("trip", "station"), quality checks (missing GPS points), the catalogue entry with licence and retention, answers users' questions.
:::

## Data Act beyond Connected Products {.optional}

The Data Act does not only concern connected products. Read the questions and answer each in one or two sentences.

1. A large supplier imposes a clause on the bike shop: "The supplier may use all sales data the shop enters into the ordering portal for any purpose, and the shop waives all claims." Which chapter of the Data Act is relevant, and what could be the consequence?
2. During a flood, the city asks the bike shop for the number of cargo bikes it can rent out. Under which conditions may a public body ask for data under the Data Act?
3. Why does the Data Act's chapter on switching between cloud services matter for a data architecture decision (session 18)?

::: answer lines=8
:::

::: solution
1. **Chapter IV** (unfair contractual terms between enterprises, Art. 13): a term on data access and use unilaterally imposed on another enterprise is not binding if it is unfair — e.g. one that grossly deviates from good commercial practice; the clause could be void. It applies to contracts concluded after 12 September 2025, and from 12 September 2027 to older long-term contracts.
2. **Chapter V** (Art. 14–22): a public body may request data in an **exceptional need**, e.g. to respond to a public emergency such as a flood; the request must describe the data, explain the purpose and show why the need is exceptional (Art. 17); in an emergency, non-personal data is requested first, and micro and small enterprises are exempt from non-emergency requests.
3. **Chapter VI** (Art. 23–31) reduces **lock-in**: providers must remove obstacles to switching, offer data export, and may no longer charge switching fees from 12 January 2027 (Art. 29). The legal option to switch lowers the risk of choosing a cloud platform, but technical portability (open formats, session 18) still matters.

Marking: one point per question.
:::

## References {.references}

- Abgabenordnung. (n.d.). *§ 147 Ordnungsvorschriften für die Aufbewahrung von Unterlagen*. Gesetze im Internet. Retrieved October 22, 2026, from https://www.gesetze-im-internet.de/ao_1977/__147.html
- Bundesdatenschutzgesetz. (n.d.). *§ 38 Datenschutzbeauftragte nichtöffentlicher Stellen*. Gesetze im Internet. Retrieved October 22, 2026, from https://www.gesetze-im-internet.de/bdsg_2018/__38.html
- Creative Commons. (n.d.). *Attribution 4.0 International (CC BY 4.0)*. Retrieved October 22, 2026, from https://creativecommons.org/licenses/by/4.0/
- DalleMule, L., & Davenport, T. H. (2017). What's your data strategy? *Harvard Business Review, 95*(3), 112–122.
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Deutscher Wetterdienst. (2024). *Terms of use for data on the CDC-OpenData area*. https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf
- Gesetz gegen den unlauteren Wettbewerb. (n.d.). *§ 7 Unzumutbare Belästigungen*. Gesetze im Internet. Retrieved October 22, 2026, from https://www.gesetze-im-internet.de/uwg_2004/__7.html
- GovData. (n.d.). *Datenlizenz Deutschland – Namensnennung – Version 2.0* [Data licence Germany – attribution – version 2.0]. https://www.govdata.de/dl-de/by-2-0
- Khatri, V., & Brown, C. V. (2010). Designing data governance. *Communications of the ACM, 53*(1), 148–152. https://doi.org/10.1145/1629175.1629210
- OpenStreetMap Foundation. (n.d.). *Copyright and License*. Retrieved October 22, 2026, from https://www.openstreetmap.org/copyright
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1. http://data.europa.eu/eli/reg/2016/679/oj
- Regulation (EU) 2022/868 of the European Parliament and of the Council of 30 May 2022 on European data governance and amending Regulation (EU) 2018/1724 (Data Governance Act). (2022). *Official Journal of the European Union*, L 152, 1. http://data.europa.eu/eli/reg/2022/868/oj
- Regulation (EU) 2023/2854 of the European Parliament and of the Council of 13 December 2023 on harmonised rules on fair access to and use of data and amending Regulation (EU) 2017/2394 and Directive (EU) 2020/1828 (Data Act). (2023). *Official Journal of the European Union*, L, 2023/2854. http://data.europa.eu/eli/reg/2023/2854/oj
- Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence … (Artificial Intelligence Act). (2024). *Official Journal of the European Union*, L, 2024/1689. http://data.europa.eu/eli/reg/2024/1689/oj
- Regulation (EU) 2026/1744 of the European Parliament and of the Council of 8 July 2026 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 on simplifying the implementation of harmonised AI rules (Digital Omnibus on AI). (2026). *Official Journal of the European Union*, L, 2026/1744. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744
