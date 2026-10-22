---
course: Data Management
session: 19
title: Access to Data: Legal and Organisational Aspects
subtitle: GDPR · Data Act · Data Governance Act · AI Act · data licences and open data · data governance and roles — teaching material, not legal advice
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Access to Data: Legal and Organisational Aspects {.title}

::: notes
Time plan for today (3 h): recap 6 min · today's data and the "not legal advice" note 4 min · the legal map 4 min · GDPR: personal data, roles 8 min · principles and legal bases 10 min · consent and the newsletter case 6 min · mini exercise legal basis 7 min · break 10 min · rights and accountability 8 min · Data Act 7 min · Data Governance Act 4 min · AI Act 6 min · mini exercise which law 7 min · licences and open data 7 min · data governance, roles, strategy 9 min · hands-on part 1: consent log, record of processing, licences 20 min · hands-on part 2: case discussion "may we use this data?" 28 min · team step 12 min · wrap-up 5 min · ~12 min buffer.
Input is about 79 minutes, hands-on, exercises and discussion about 74 minutes. Priorities if time runs short: personal data (incl. pseudonymised vs. anonymous), controller vs. processor, the six principles plus accountability, the six legal bases, valid consent, the main data subject rights, which EU law regulates what (GDPR, Data Act, DGA, AI Act with Art. 10), CC BY vs. CC0 vs. share-alike, and the roles data owner, data steward, data custodian and CDO are the exam core. Exam questions ask for concepts and their application to a case, never for article numbers by heart; the numbers on the slides are there so students can look things up. There are no optional slides today; the Data Act beyond connected products (contract terms, public sector access, cloud switching) is in the notes of the Data Act slide and in worksheet 19.
This session is teaching material, not legal advice — say so at the start and when students ask about their own employer's case: "ask your company's data protection officer or legal department". You are not expected to answer legal questions beyond the slides.
How the content was checked: every regulation number, article number and application date on the slides was checked on 22 October 2026 against the texts on EUR-Lex (GDPR consolidated text, DGA, Data Act, AI Act, Regulation (EU) 2026/1744, Directive 96/9/EC, Directive (EU) 2019/1024, Implementing Regulation (EU) 2023/138, Commission proposal COM(2025) 837), the Commission's AI Act Service Desk (timeline and article pages, consolidated version of 27 July 2026), the Commission's Data Act pages and, where the EUR-Lex page could not be read in full, a reproduction of the Official Journal text (Data Act Art. 4–7 and 50; GDPR Art. 83 and 99). German law (BDSG, UWG, AO) was checked on gesetze-im-internet.de. Laws change: check the AI Act timeline and the status of the Digital Omnibus proposal before each run of the course.
How the results were produced: every SQL statement was run with SQLite 3.45.1 on a fresh bikeshop.db built from bikeshop-schema.sql, bikeshop-data.sql, bikeshop-data-session09.sql, bikeshop-dq-session13.sql, the new bikeshop-privacy-session19.sql (consent texts, consent log, draft record of processing activities; fictional) and bikeshop-lake-catalog-session18.sql.
:::

---

# Today's Agenda

1. Recap: may the shop keep the clickstream?
2. A map of the EU data laws
3. The GDPR: personal data, principles, legal bases, consent, rights
4. Data Act, Data Governance Act and AI Act: what they mean for data work
5. Data licences and open data
6. Data governance: roles and strategy
7. Hands-on: may we use this data?

::: notes
Time and format guide (not shown to students):
0:00 Recap (plenary) · 0:06 Today's data, not legal advice (everyone) · 0:10 Legal map, GDPR basics (input, questions to the room) · 0:38 Mini exercise legal basis (pairs) · 0:45 Break · 0:55 Rights and accountability, Data Act, DGA, AI Act (input) · 1:20 Mini exercise which law (pairs) · 1:27 Licences, governance (input) · 1:43 Hands-on part 1 (pairs, each student on their own laptop) · 2:03 Hands-on part 2 (groups of 4, one case per group, short presentations) · 2:31 Team step (project teams) · 2:43 Wrap-up · buffer.
Live demo: after the consent slide, run the consent query against bikeshop-privacy-session19.sql and compare with session 14's nine newsletter recipients. The drop from 9 to 5 people is the aha of the session: a cleaning decision in session 14 ("Y and 1 mean yes") was a legal question in disguise.
:::

---

# Recap: Where Session 18 Left Us

- The shop's **lake** holds files nobody can explain — and some contain **personal data**: accounts, clickstream with **IP addresses**, damage photos
- The catalogue had a column `personal_data` — but no **purpose**, no **legal basis**, no **deletion date**
- The preparation question: may the shop keep the clickstream with IP addresses — and for **how long**?
- Today: the **rules** for using data — and **who** in an organisation makes sure they are kept

::: callout
**Your answer?** Only if there is a **purpose** and a **legal basis**, and only as long as the purpose needs it. "We might need it later" is neither.
:::

::: source
Session 18 of this course; Regulation (EU) 2016/679 (2016, Art. 5).
:::

::: notes
Collect two or three answers. Typical answers: "yes, it is our data" (the data is about visitors — ownership is not the question, the GDPR is), "IP addresses are not personal" (they can be: online identifiers, Recital 30 — see the personal data slide), "keep it forever, storage is cheap" (storage limitation, Art. 5(1)(e)), "delete the IP, keep the rest" (good instinct: data minimisation; whether the rest is then anonymous depends on what else is in the file). Keep the answers on the board; the principles slide sorts them. Remind: in session 18 the clickstream files had no owner and no description — a governance problem before it is a legal one.
:::

---

# Before We Start: Not Legal Advice

::: callout
This session is **teaching material, not legal advice**. It explains the main ideas of EU data law so that you can recognise **when to ask** — the answer for a real case comes from your organisation's **data protection officer** or **legal department**.
:::

- Laws are cited by **regulation and article number** so that you can **look them up** on EUR-Lex — you do not need to learn numbers by heart
- Article contents are **paraphrased**, not quoted; the official text is binding
- Laws **change**: dates and the status of proposals were checked on **22 October 2026**

::: source
EUR-Lex (Publications Office of the European Union) for all EU texts; gesetze-im-internet.de for German law.
:::

::: notes
Say this explicitly and come back to it whenever a student asks "is this allowed at my company?". The exam asks for concepts and their application to a case (e.g. "which legal basis fits?"), not for article numbers. The German examples (BDSG, UWG, AO) are national law on top of the EU rules; other Member States have their own.
:::

---

# Today's Data

| Source | Content | Used for |
|---|---|---|
| `webshop_customer` (session 13) | 20 web shop accounts, newsletter column `yes`/`no`/`Y`/`1` | the consent case |
| `bikeshop-privacy-session19.sql` | **new**: 3 consent texts, 20 consent events, draft record of 9 processing activities | consent check, gaps in the record |
| `bikeshop-lake-catalog-session18.sql` | 24 lake files with licence and personal data | licences through the lineage |
| six data cases | **new**: on the exercise slide | may we use this data? |

::: source
Own example based on the bike shop case; all names and events fictional.
:::

::: notes
Everyone loads the new script into the bikeshop.db that already contains webshop_customer (session 13); the lake catalogue of session 18 can go into the same file. Check after loading: consent_text 3, consent_event 20, processing_activity 9. The legal bases in processing_activity are examples for discussion — say so; the hands-on asks students to criticise them.
:::

---

# The Legal Map {.section}

Which law regulates which data?

---

# Four EU Laws for Data — at a Glance

| Law | Number | Applies since | Regulates |
|---|---|---|---|
| **GDPR** | Regulation (EU) 2016/679 | 25 May 2018 | processing of **personal data** |
| **Data Governance Act** | Regulation (EU) 2022/868 | 24 Sep 2023 | re-use of protected **public-sector data**, data **intermediaries**, data **altruism** |
| **Data Act** | Regulation (EU) 2023/2854 | 12 Sep 2025 | access to data of **connected products**, B2B contract terms, **cloud switching** |
| **AI Act** | Regulation (EU) 2024/1689 | in stages, 2025–2028 | **AI systems** by risk, incl. **data governance** for high-risk AI |

- The GDPR protects **people**; the others mainly open up **data** — the GDPR still applies whenever personal data is involved

::: source
Regulation (EU) 2016/679 (2016, Art. 99); Regulation (EU) 2022/868 (2022, Art. 38); Regulation (EU) 2023/2854 (2023, Art. 50); European Commission (n.d.-b).
:::

::: notes
All four are regulations: they apply directly in every Member State, without national transposition (unlike directives such as the Open Data Directive). The DGA and the Data Act are part of the European strategy for data of 2020 (session 1: data spaces, single market for data). The AI Act dates follow on its own slide. Pending change: the Commission's Digital Omnibus proposal of 19 November 2025 (COM(2025) 837) would amend the GDPR and the Data Act and repeal the DGA and the Open Data Directive, moving their content into the Data Act. Status checked 22 October 2026: still a proposal, the Council's negotiating position was under discussion in Coreper in October 2026, no trilogue, not adopted (European Commission, 2025). Mention it in one sentence; do not teach the proposal. The AI part of the omnibus was adopted separately (Regulation (EU) 2026/1744).
:::

---

# The GDPR {.section}

Personal data, principles, legal bases, consent, rights

---

# What Is Personal Data?

- **Personal data**: any information relating to an **identified or identifiable** natural person — directly (name) or indirectly (customer number, location, **online identifier**)
- **Pseudonymised** data is still personal data: the key to re-identify exists somewhere
- **Anonymous** data is outside the GDPR — but only if nobody can re-identify a person with means **reasonably likely** to be used
- **Special categories** (health, religion, ethnic origin, biometrics …) are banned by default; exceptions are narrow

| Bike shop data | Personal? |
|---|---|
| frame number of a customer's bike in a repair job | **yes** — linked to the customer |
| clickstream with IP addresses | **yes**, in general — online identifiers |
| revenue per product group and day | **no** — aggregated, no person |

::: source
Regulation (EU) 2016/679 (2016, Art. 4(1), 4(5), Art. 9(1), Recitals 26 and 30).
:::

::: notes
Recital 30 names IP addresses and cookie identifiers as online identifiers that can be used to identify people when combined with other information. Whether a specific IP address is personal data for a specific shop depends on whether the shop can, by reasonable means, link it to a person — the safe working assumption is "yes". Recital 26: for identifiability, consider cost, time and available technology. Link to session 18: the catalogue's "unknown" for photos is honest — a damage photo can show a face or a licence plate. Link to session 16: aggregation before loading (ETL) turned personal data into non-personal data. Ask: is a sales figure "revenue of salesperson Laura Becker on 6 October" personal? → yes, it relates to an identified employee.
:::

---

# Who Is Who?

| Role | Meaning | Bike shop example |
|---|---|---|
| **Data subject** | the person the data is about | customer, web shop visitor, employee |
| **Controller** | decides **purposes and means** of processing | Velo Neckar |
| **Processor** | processes **on behalf of** the controller | newsletter service, web shop hosting, payroll office |
| **Recipient** | anyone the data is disclosed to | parcel service, tax adviser |

- A processor needs a **contract** with the controller (what, how long, which safeguards)
- A **data protection officer** is required for public bodies and for core activities with large-scale monitoring or special categories; in Germany also from **20 persons** regularly processing personal data automatically

::: source
Regulation (EU) 2016/679 (2016, Art. 4(7), 4(8), Art. 28, Art. 37); Bundesdatenschutzgesetz (n.d.).
:::

::: notes
The controller stays responsible for what its processors do — "the cloud provider handles GDPR" is a classic misconception. Art. 28(3) lists what the contract must cover (subject matter, duration, nature and purpose, type of data, categories of data subjects, obligations and rights of the controller). Velo Neckar has seven employees: no DPO duty from the German 20-person threshold of § 38 BDSG (unless its core activity were large-scale monitoring, Art. 37(1)) — but the obligations of the GDPR apply anyway. Session 18's cloud slide: where the provider stores the data matters (transfers outside the EU need an adequacy decision or safeguards such as standard data protection clauses, Art. 44–46) — one sentence, no details.
:::

---

# Six Principles — and Accountability

| Principle | In one line | Bike shop example |
|---|---|---|
| **Lawfulness, fairness, transparency** | a legal basis; people know what happens | privacy notice in the web shop |
| **Purpose limitation** | collected for a stated purpose, not reused for incompatible ones | repair phone number not used for advertising calls |
| **Data minimisation** | only what the purpose needs | no birth date for a newsletter |
| **Accuracy** | correct and up to date | the data quality of sessions 13–14 |
| **Storage limitation** | kept no longer than needed | clickstream deleted after a defined period |
| **Integrity and confidentiality** | appropriate security | access rights, encryption, backups |

- **Accountability**: the controller must comply **and be able to show it**

::: source
Regulation (EU) 2016/679 (2016, Art. 5).
:::

::: notes
Art. 5(1)(a)–(f) plus Art. 5(2) accountability. Link back to the course: accuracy is literally the data quality dimension of session 13; storage limitation is a deletion date in the catalogue (worksheet 18, rule R3); integrity and confidentiality is data security (DAMA knowledge area of session 1). Further processing for archiving, research or statistics is not considered incompatible (Art. 5(1)(b)); other new purposes need a compatibility check (Art. 6(4)). Sort the recap answers from the board into the rows: "keep forever" → storage limitation; "delete the IP" → minimisation.
:::

---

# Six Legal Bases

Processing is lawful only if **at least one** applies:

| Basis | When | Bike shop example |
|---|---|---|
| (a) **Consent** | the person agreed for a specific purpose | newsletter |
| (b) **Contract** | needed to perform a contract with the person | address for delivering a web shop order |
| (c) **Legal obligation** | the law requires it | keeping invoices for the tax office |
| (d) **Vital interests** | to protect someone's life | rarely relevant for a shop |
| (e) **Public task** | public bodies' tasks | not for a shop |
| (f) **Legitimate interests** | a real interest that the person's rights do not override | video camera against theft — with limits |

- Consent is **not** the default: if a contract or a law covers the processing, use that basis

::: source
Regulation (EU) 2016/679 (2016, Art. 6(1), Recital 47).
:::

::: notes
Art. 6(1)(a)–(f). Legitimate interests need a balancing test: the interest of the shop against the reasonable expectations of the person (Recital 47, which also mentions fraud prevention and direct marketing as possible legitimate interests). Public authorities cannot use (f) for their tasks. Common misconception: "we always need consent" — no; asking for consent where a contract applies is misleading, because the person cannot really refuse. For e-mail advertising, Germany adds § 7 UWG on top: in general prior express consent, with a narrow exception for existing customers (own similar products, the customer was told they can object at any time) — that is unfair competition law, not the GDPR.
:::

---

# Valid Consent

Consent must be:

- **freely given** — a real choice, no detriment for saying no
- **specific** — for a stated purpose
- **informed** — who, what, why, and that it can be withdrawn
- **unambiguous** — a statement or a **clear affirmative action**; silence, inactivity or a **pre-ticked box** are not consent

And the controller must:

- be able to **demonstrate** that the person consented
- make **withdrawal** as easy as giving consent — and stop when it happens

::: source
Regulation (EU) 2016/679 (2016, Art. 4(11), Art. 7(1)–(3), Recitals 32 and 42).
:::

::: notes
Art. 4(11) defines consent; Art. 7 sets the conditions: demonstrate (7(1)), clearly distinguishable request in plain language (7(2)), withdrawal at any time and as easy as giving it (7(3)); Recital 32 excludes silence, pre-ticked boxes and inactivity. Double opt-in (confirmation link by e-mail) is not written in the GDPR; it is a common way to prove that the e-mail address belongs to the person who signed up — the shop's own rule in today's data. Consent of children for online services: Art. 8 (16 years, Member States may lower it to 13) — not needed today.
:::

---

# Back to Session 14: "Y" and "1"

![A chain of three checks for each newsletter consent in the shop's log. Start: 11 accounts with a consent given. Check 1, was the box ticked by the person? No for W03, W15 and W18 from the old app APP-1, whose box was pre-ticked, which is no consent according to Recital 32. Check 2, was the sign-up confirmed by the e-mail link? No for W08, the shop's proof of consent under Article 7(1). Check 3, not withdrawn since then? No for W02 and W09, who unsubscribed; withdrawal stops consent under Article 7(3). Result: valid consent for W01, W04, W05, W12 and W14 — five people may receive the newsletter, compared with nine people from the export's newsletter column in session 14](img/legal-consent-check.png){width=92%}

- Session 14 mapped `Y` and `1` to **yes** — a data cleaning rule that was really a **legal** decision

::: source
Own illustration based on Regulation (EU) 2016/679 (2016, Art. 7, Recital 32); data from bikeshop-privacy-session19.sql.
:::

::: notes
All observed (SQLite 3.45.1). Live demo, query:
SELECT g.account_id FROM consent_event g JOIN consent_text t ON t.text_version = g.text_version WHERE g.action = 'given' AND t.pre_ticked = 0 AND (t.double_opt_in = 0 OR EXISTS (SELECT 1 FROM consent_event c WHERE c.account_id = g.account_id AND c.action = 'confirmed' AND c.event_at > g.event_at)) AND NOT EXISTS (SELECT 1 FROM consent_event w WHERE w.account_id = g.account_id AND w.action = 'withdrawn' AND w.event_at > g.event_at) → W01, W04, W05, W12, W14.
The export says yes, Y or 1 for W01, W03, W04, W05, W08, W09, W12, W14, W15, W18; W03 (Anna Berger's old account) and the two old-app codes come from the pre-ticked APP-1 form; W09 unsubscribed on 20 April 2027 but the export of 3 May still says yes — the export is out of sync with the log (a consistency problem, session 13). Session 14's nine people included W08, W09, W15 and W18. Lesson: the consent log, not a yes/no column, is the evidence (accountability). What can the shop do for W15 and W18? Ask for consent again at the next log-in or visit in the shop with a correct form; do not simply e-mail them advertising.
:::

---

# Mini Exercise: Which Legal Basis? {.exercise}

Which legal basis fits best — or is the processing not allowed as described?

1. The web shop stores the delivery address of an order
2. The shop keeps invoices for the tax office
3. The workshop sends an SMS when a repaired bike is ready
4. The shop sends a monthly newsletter to all customers in the till system
5. A camera at the entrance records to deter theft
6. The shop sells its customer list to a fitness studio "because it has a legitimate interest in revenue"

::: notes
About 5 min in pairs, 2 min collection. Expected answers (teaching material, not legal advice): 1 contract (b). 2 legal obligation (c) — § 147 AO in Germany (booking vouchers 8 years, books 10 years). 3 contract (b): informing the customer about the job is part of the repair contract. 4 not allowed as described: needs consent (a) for e-mail advertising; in Germany a narrow existing-customer exception exists in § 7(3) UWG (own similar products, address obtained in a sale, customer informed of the right to object) — "all customers in the till" without consent or these conditions is not covered. 5 legitimate interests (f), with limits: clear signs, short storage (the draft record says 72 hours), no cameras in staff rooms; national rules and DPA guidance apply. 6 not allowed: the customers' interests clearly override; customers do not expect this (Recital 47), new incompatible purpose (Art. 5(1)(b), 6(4)); would need consent. Typical mistake: "consent for everything".
:::

---

# Rights of Data Subjects

| Right | The person can … | Article |
|---|---|---|
| **Information** | learn at collection who processes what, why, how long | 13 |
| **Access** | get confirmation and a **copy** of their data | 15 |
| **Rectification** | have wrong data corrected | 16 |
| **Erasure** | have data deleted, e.g. when no longer needed or consent withdrawn | 17 |
| **Restriction** | have processing paused while a dispute is checked | 18 |
| **Portability** | get data they provided in a machine-readable format (consent or contract) | 20 |
| **Objection** | object, e.g. to **direct marketing** — then it must stop | 21 |

- Answer **within one month** (extendable in complex cases)

::: source
Regulation (EU) 2016/679 (2016, Art. 12(3), Art. 13, 15–18, 20, 21).
:::

::: notes
Data management view: every right is a query or an update. Access = find all rows about one person across all systems (sessions 13–14: duplicates such as W01/W03 make this hard — data quality is a precondition). Erasure = delete in all copies, including the lake and backups, or document why the data must be kept (e.g. invoices, legal obligation). Portability ties to session 15: CSV or JSON export. Art. 22 (automated decisions) exists too; mention only if asked.
:::

---

# Accountability in Practice

- **Record of processing activities**: what, why, legal basis, recipients, deletion periods, security — per activity
- **Data protection by design and by default**: privacy built into systems; by default only the data needed
- **Security** appropriate to the risk: pseudonymisation, encryption, confidentiality, availability, tested regularly
- **Data breach**: notify the supervisory authority without undue delay, where feasible **within 72 hours**; inform the people affected if the risk is high
- **Impact assessment** before high-risk processing, e.g. large-scale monitoring
- **Fines** up to EUR 20 million or 4 % of worldwide annual turnover, whichever is higher

::: source
Regulation (EU) 2016/679 (2016, Art. 25, 30, 32–35, 83); European Commission (n.d.-c).
:::

::: notes
Art. 30(5) exempts organisations with fewer than 250 employees from the record — but not if the processing is not occasional, risky, or involves special categories; a shop processing customer data every day is usually not exempt, and the record is good practice anyway. Today's hands-on uses the shop's draft record. Link: the record is a catalogue (session 18) for processing activities; data protection by default is data minimisation in the schema (session 7: do not add a birth_date column "just in case"). The 72-hour rule is Art. 33(1); informing data subjects Art. 34. Fines: Art. 83(5) for breaches of principles, legal bases, consent and data subject rights; lower cap (EUR 10 million or 2 %) in Art. 83(4).
:::

---

# The EU Data Strategy Laws {.section}

Data Act, Data Governance Act, AI Act

---

# Data Act: Who Gets the Data of a Connected Product?

- **Connected products** (e-bikes, cars, machines, smart meters) produce data — so far the **manufacturer** usually kept it
- New products must be **designed** so that users can access their data (for products placed on the market after **12 Sep 2026**)
- The **user** can get the data **free of charge** and in a machine-readable format — or have it sent to a **third party** of their choice, e.g. an independent repair shop
- Limits: the data may not be used to build a **competing product**; **trade secrets** are protected; large online **gatekeepers** cannot receive it this way
- **Micro and small** manufacturers are exempt from these obligations
- Personal data in the product data: the **GDPR** still applies

::: source
Regulation (EU) 2023/2854 (2023, Art. 3–7, Art. 50); European Commission (n.d.-a).
:::

::: notes
Session 1's discussion question comes back here: "Should a car manufacturer have to share the data your car produces with you and with independent repair shops?" — this is Chapter II of the Data Act. Article references (paraphrased): Art. 3(1) access by design (applies to products placed on the market after 12 September 2026, Art. 50); Art. 4(1) user access, free of charge, without undue delay; Art. 5(1) sharing with a third party at the user's request; Art. 5(3) and 6(2)(d) DMA gatekeepers excluded; Art. 4(10) and 6(2)(e) no competing product; Art. 4(6)–(9) and the corresponding paragraphs of Art. 5 protect trade secrets; Art. 7(1) micro and small enterprises exempt. For Velo Neckar: an e-bike owner could ask the motor manufacturer to share the e-bike's diagnostic data with the shop — a new business opportunity for independent workshops. Beyond devices (mention in one or two sentences, worksheet 19 has a task): Chapter IV unfair contractual terms between businesses (Art. 13; contracts after 12 September 2025, older long-term contracts from 12 September 2027, Art. 50); Chapter V access for public bodies in an exceptional need such as a public emergency (Art. 14–22; non-personal data first, micro and small enterprises exempt from non-emergency requests); Chapter VI switching between cloud services (Art. 23–31; switching charges at cost until 12 January 2027, none afterwards, Art. 29) — the legal answer to the lock-in risk of session 18; Chapter VII safeguards against unlawful foreign government access to non-personal data (Art. 32).
:::

---

# Data Governance Act

Applies since **24 Sep 2023**. Four building blocks for **trusted data sharing**:

::: cards
### Re-use of protected public data
Public bodies may allow re-use of data protected by confidentiality, IP rights or data protection — with safeguards such as anonymisation or secure processing environments.
### Data intermediation services
Neutral data marketplaces and data-sharing services: notification to an authority, a separate legal entity, no use of the data for their own purposes.
### Data altruism
People and companies can donate data for the general interest, e.g. research, through registered not-for-profit organisations.
### European Data Innovation Board
An expert group that advises the Commission on standards and practices for data sharing.
:::

::: source
Regulation (EU) 2022/868 (2022, Art. 1–3, 10–12, 38); European Commission (n.d.-a).
:::

::: notes
Art. 3(1) lists the protected categories: commercial confidentiality, statistical confidentiality, third-party IP rights, personal data outside the Open Data Directive. Art. 12(a): the intermediary may not use the data for other purposes and must provide the service through a separate legal person. Art. 2(16) defines data altruism. The DGA creates no obligation for public bodies to allow re-use (Art. 1). For students: the DGA matters when your employer wants to use a data marketplace or research data from a public body. Pending: the Digital Omnibus proposal (COM(2025) 837) would repeal the DGA and move its content into the Data Act — not adopted as of 22 October 2026.
:::

---

# AI Act: Where Data Management Comes In

- **Risk-based**: prohibited practices · **high-risk** systems (e.g. hiring, credit scoring) · transparency duties · minimal risk
- High-risk AI: training, validation and test data need **data governance** — origin and purpose of data, preparation (labelling, cleaning), assumptions, examination for **bias**, data gaps
- The data must be **relevant**, sufficiently **representative**, as **free of errors** and **complete** as possible
- General-purpose AI models: a **copyright policy** and a public **summary of training content**
- Prohibited, e.g.: building face databases by **untargeted scraping** of the internet or CCTV

| Stage | Date |
|---|---|
| prohibitions, AI literacy | 2 Feb 2025 |
| general-purpose AI models | 2 Aug 2025 |
| most rules, transparency | 2 Aug 2026 |
| high-risk (Annex III) / in products (Annex I) | 2 Dec 2027 / 2 Aug 2028 |

::: source
Regulation (EU) 2024/1689 (2024, Art. 5(1)(e), 10, 53, 113), as amended by Regulation (EU) 2026/1744 (2026); European Commission (n.d.-b).
:::

::: notes
Art. 10 is a data quality and data governance article: its list (design choices, collection and origin, preparation such as annotation, labelling and cleaning, assumptions, availability and suitability, bias examination and mitigation, data gaps; Art. 10(2)(a)–(h)) reads like sessions 13–16 of this course. Art. 10(3): relevant, sufficiently representative, to the best extent possible free of errors and complete; 10(4): fit the setting where the system is used. Since the Digital Omnibus on AI (Regulation (EU) 2026/1744, in force since 27 July 2026): Art. 10(5) on special categories for bias detection moved into a new Art. 4a; Art. 4 (AI literacy) now requires measures to support AI literacy; the high-risk dates moved from 2 August 2026 to 2 December 2027 (Annex III) and 2 August 2028 (Annex I). Check the Commission's AI Act Service Desk timeline before teaching — further changes are possible. Data Analytics (semester 5) covers machine learning; today only the data side.
:::

---

# Mini Exercise: Which Law? {.exercise}

Which law (GDPR, Data Act, DGA, AI Act — or several) answers each question? Not legal advice.

1. A customer asks the shop for a copy of all data it holds about her
2. An e-bike owner wants the motor's diagnostic data sent to Velo Neckar
3. A start-up builds a marketplace where shops trade anonymised sales data
4. A bank trains a credit-scoring model on past loan data
5. The city wants the shop's sales data during a flood emergency
6. The shop wants to leave its cloud provider without paying exit fees

::: notes
About 5 min in pairs, 2 min collection. Expected answers: 1 GDPR, right of access (Art. 15). 2 Data Act, user's right to share with a third party (Art. 5) — plus GDPR, because the data relates to the owner. 3 DGA, data intermediation service (Chapter III) — and the question whether the data is really anonymous (GDPR, Recital 26). 4 AI Act: credit scoring is a high-risk use case in Annex III, so Art. 10 data governance applies (from 2 December 2027); plus GDPR for the personal loan data. 5 Data Act, Chapter V (exceptional need); non-personal data first. 6 Data Act, Chapter VI (switching; charges end on 12 January 2027). Good answers name several laws: the GDPR applies in parallel whenever personal data is involved.
:::

---

# Licences and Open Data {.section}

Who may use data — and under which conditions?

---

# Data Licences

| Licence | You may … | You must … |
|---|---|---|
| **CC0** | do anything | nothing (attribution welcome) |
| **CC BY 4.0** | use, change, also commercially | **name the source**, link the licence, **say what you changed** |
| **Datenlizenz Deutschland – Namensnennung 2.0** | use, change, also commercially | source note with provider, licence, link; mark changes |
| **ODbL 1.0** (e.g. OpenStreetMap) | use, change, also commercially | credit, and share **derived databases** under the **same licence** (share-alike) |
| **Terms of use** (supplier, API) | what the contract allows | read them — often **no publication**, no resale |

- No licence stated ≠ free to use: databases can be protected by a **database right** for 15 years

::: source
Creative Commons (n.d.); GovData (n.d.); OpenStreetMap Foundation (n.d.); Directive 96/9/EC (1996, Art. 7 and 10).
:::

::: notes
CC BY 4.0 deed: credit, link to the licence, indicate changes, no suggestion of endorsement, no additional restrictions; the licence does not cover privacy rights — open data can still contain personal data, and then the GDPR applies. DL-DE BY 2.0 (licence of many German public bodies): source note with provider name, licence name and a link to the dataset, and changes must be marked. ODbL share-alike: if you build on OpenStreetMap data and distribute the result, you may do so only under the same licence — a reason to check before mixing it into a product. Database right (Directive 96/9/EC, Art. 7): protects the maker's substantial investment in obtaining, verifying or presenting the contents against extraction or re-use of the whole or a substantial part; 15 years (Art. 10). Scraping a website's database is therefore not automatically allowed even if the facts themselves are not protected.
:::

---

# Open Data — and the Weather in Our Pipeline

- **Open Data Directive** (EU) 2019/1024: public bodies should make their data re-usable, ideally **open by default** and machine-readable
- **High-value datasets** (Implementing Regulation (EU) 2023/138): six categories — geospatial, earth observation, **meteorological**, statistics, companies, mobility — free of charge, via **APIs**, under **CC BY 4.0** or a less restrictive licence
- The DWD's open weather data is published under **CC BY 4.0** — hence the line under every chart since session 15:

::: callout
*Data: Deutscher Wetterdienst, via Bright Sky, CC BY 4.0; daily totals computed by Velo Neckar.*
:::

- Attribution travels **through the lineage**: every table and report built from the weather data needs it

::: source
Directive (EU) 2019/1024 (2019); Implementing Regulation (EU) 2023/138 (2023, Annex, Section 3); Deutscher Wetterdienst (2024); de Maeyer (n.d.).
:::

::: notes
Directive (EU) 2019/1024 is a recast of the earlier directive on the re-use of public sector information; as a directive it is transposed into national law. Implementing Regulation (EU) 2023/138: Annex Section 3.2(a) requires meteorological high-value datasets under CC BY 4.0 or an equivalent or less restrictive open licence; Art. 4 sets the general licence rule (CC0 or CC BY 4.0 or equivalent). The DWD terms of use (status May 2024) state that CC BY 4.0 applies; Bright Sky says the DWD's terms apply to data retrieved through it. Hands-on question 5 traces the licence through the session 18 lineage: fact_sales and the revenue report are built from dim_weather_day, but their catalogue entries have no licence — the attribution would get lost.
:::

---

# Data Governance {.section}

Who decides, who is responsible, who does the work?

---

# What Is Data Governance?

- **Data governance**: exercising **authority and control** over the management of data — decision rights and accountability
- It decides **who** may decide **what** about data; data management **carries out** the decisions
- Typical decision areas:
  - **Data principles**: data as an asset, its uses
  - **Data quality**: what "good enough" means (session 13)
  - **Metadata**: definitions, catalogue (session 18)
  - **Data access**: who may see and use what — and on which legal basis
  - **Data lifecycle**: from creation to deletion

::: source
Abraham et al. (2019); Khatri and Brown (2010); DAMA International (2017, Chapter 3).
:::

::: notes
Abraham et al. (2019) define data governance as exercising authority and control over the management of data, to increase its value and reduce cost and risk; their framework is based on a review of 145 publications. Khatri and Brown (2010) name the five decision domains used on the slide (data principles, data quality, metadata, data access, data lifecycle) and ask for each domain who holds the decision rights. DAMA International (2017, Chapter 3) places data governance at the centre of its wheel (session 1): governance is the "what and who", the other knowledge areas the "how". Compliance with the laws of today is one goal of governance; value creation is the other.
:::

---

# Roles in Data Governance

::: layers
- Chief data officer (CDO): owns the data strategy at board level; leads data governance and data management
- Data governance council: owners and IT agree on policies, standards and priorities; settle conflicts
- Data owner: a business manager accountable for a data domain — decides who may use it, for what, and how good it must be
- Data steward: does the day-to-day work — definitions, quality rules, fixing errors, answering questions
- Data custodian: IT — runs, secures and backs up the systems that hold the data
- Data users: use the data according to the rules
:::

- Velo Neckar: owner = **CDO** and **council** in one person; Katrin Vogel **owner** of workshop data; Laura Becker **steward** of the web shop and sales data

::: source
Own illustration based on Khatri and Brown (2010), DAMA International (2017, Chapters 3 and 16) and Lee et al. (2014).
:::

::: notes
Role names vary between companies and books: DAMA International (2017, Chapter 16) describes data management roles and how organisations set them up; Khatri and Brown (2010) list data owner/trustee, data custodian, data steward, data producer, data consumer and an enterprise data council. The key distinction for the exam: the owner is accountable (business), the steward does the work (business, close to the data), the custodian runs the technology (IT). Link to session 16: who reads the ETL run log? → the steward. Link to session 18: data mesh moves ownership into domains with federated governance. In a small shop, one person holds several roles — the roles still exist. Also: the data protection officer is not a governance role in this sense — the DPO advises and monitors, receives no instructions on these tasks and must not have a conflict of interests (GDPR Art. 38(3) and (6), Art. 39) — so not the person who decides on the processing.
:::

---

# Data Strategy: Defence and Offence

| | Defence | Offence |
|---|---|---|
| Goal | minimise **risk**: compliance, privacy, security, quality | **create value**: analytics, new products, customer insight |
| Typical tools | single source of truth, controls, governance | flexible analysis, multiple versions of the truth |
| Bike shop | consent log, record of processing, deletion rules | weather vs. revenue analysis, e-bike diagnostics as a service |

- A **data strategy** sets the balance — regulated industries lean to defence, retail and marketing to offence
- The **CDO** role grew from both sides: inward or outward collaboration, traditional or big data, service or strategy

::: source
DalleMule and Davenport (2017); Lee et al. (2014).
:::

::: notes
DalleMule and Davenport (2017) describe data defence (compliance, governance, quality, security; a single source of truth) and data offence (analytics and insight to increase profit; multiple versions of the truth derived from it) and argue that each company must find its own balance, which can shift over time. Lee et al. (2014) describe the CDO role along three dimensions — collaboration direction (inward/outward), data space (traditional data/big data) and value impact (service/strategy). Today's session covered mainly defence; sessions 13–18 built the tools for both. Exam: explain defence vs. offence with one example each.
:::

---

# Exercise: Consent, Record and Licences {.exercise}

Load `bikeshop-privacy-session19.sql` (and the session 13 and 18 scripts). Predict first, then run. Not legal advice.

1. **Consent**: which accounts have a valid newsletter consent today? Use the three checks of the figure
2. **Out of sync**: which accounts does the export mark `yes`, `Y` or `1` without valid consent — and why?
3. **Record gaps**: which processing activities of personal data lack a purpose, legal basis, deletion period or owner?
4. **Critique**: which entries in the record are doubtful or do not belong there? Which need special care (Art. 9)?
5. **Licences**: which silver and gold files are built from **CC BY 4.0** data (`lake_lineage`)? Which of them lack the licence in the catalogue?
6. **Clickstream**: write a purpose, a legal basis and a deletion rule for activity 5 — or argue for deleting the data

::: notes
About 18 min + 2 min comparison. Expected answers (all observed; SQLite 3.45.1):
1 W01, W04, W05, W12, W14 (query on the consent slide). 2 W03 (pre-ticked APP-1; duplicate of W01, who has a valid consent), W08 (not confirmed), W09 (withdrawn 2027-04-20, export of 2027-05-03 still yes), W15 and W18 (pre-ticked APP-1).
3 `WHERE personal_data = 1 AND (purpose IS NULL OR legal_basis IS NULL OR retention IS NULL OR owner IS NULL)` → 2 repair jobs (no retention), 5 clickstream (no purpose, basis, retention, owner), 6 damage photos (no retention), 7 staff rota and payroll (no retention).
4 Activity 9 (weather) is not personal data and does not belong in the record. Activity 7 includes sick days = health data, a special category (Art. 9) — needs an Art. 9(2) exception (employment law) and strict access. Activity 3: is the birth date needed for a web shop (minimisation)? Activity 8: camera on legitimate interests needs a documented balancing test and signs. Activity 4: the newsletter service may store data outside the EU — check (Art. 44–46). Activity 1: retention 8 years only for booking vouchers; accounting books 10 years (§ 147 AO).
5 WITH RECURSIVE over lake_lineage (session 18) → 16 weather_daily, 21 fact_sales, 23 dim_weather_day, 24 report_revenue_by_weather (24 also carries supplier terms via 22). 21 and 24 have no licence in the catalogue → add "CC BY 4.0 (DWD)" so the attribution reaches the report.
6 Good answers: purpose "measure which pages are used to improve the shop", legal basis consent via the cookie banner or legitimate interests with shortened IP addresses, deletion of raw files after e.g. 30 days, aggregates kept. Accept "delete it": no purpose, no owner.
:::

---

# Exercise: May We Use This Data? {.exercise}

One case per group: decide **yes, yes with conditions, or no** — with the law, the principle or the licence behind it.

::: cards
### A · Customer e-mails for a survey
Velo Neckar wants to e-mail all repair customers a satisfaction survey with a voucher for the next service.
### B · E-bike data
A customer's e-bike motor logs error codes and GPS tracks. The shop wants the error codes to offer a repair before a breakdown.
### C · Open data
A student team wants to use OpenStreetMap bike paths and DWD weather data in a commercial app.
### D · Training an AI
A rental start-up wants to train a model on photos of damaged bikes from the shop's lake, incl. IMG_0412.jpg.
### E · Selling insights
A data marketplace offers to buy "anonymised" web shop orders with postcode, birth date and items.
### F · Staff dashboard
The owner wants a dashboard of sales per salesperson and day, shown on the shop's screen.
:::

::: notes
About 20 min in groups of four + 8 min short presentations (one minute per group). All cases fictional; teaching material, not legal advice. Expected lines of argument (accept others with sound reasons):
A Yes with conditions: the survey with a voucher is likely advertising — consent or, in Germany, the existing-customer conditions of § 7(3) UWG; purpose limitation: phone numbers from repairs not for this; minimise (no birth date).
B Yes with conditions: Data Act — the user (customer) can ask the manufacturer to share the data with the shop (Art. 5), free for the user; GDPR — error codes linked to the owner are personal data; GPS tracks are not needed for the purpose (minimisation): ask only for error codes. The shop may not use the data to build a competing motor.
C Yes with conditions: DWD CC BY 4.0 (attribution, link, changes noted); OpenStreetMap ODbL (credit, and share-alike if the app distributes a derived database). Check the app's terms of use for map tiles separately.
D No as described: photos may show faces or licence plates (personal data, "unknown" in the catalogue); purpose limitation (photos were taken for repairs); IMG_0412 has no owner or description. With conditions: blur faces and plates, contract, clear purpose; damage detection is not a high-risk use under the AI Act, but data quality and representativeness matter anyway.
E No as described: postcode + birth date + items is very likely re-identifiable (Recital 26) — pseudonymised at best, not anonymous; selling needs a legal basis. Possible: aggregates (e.g. sales per product group and region). A marketplace itself would be a DGA data intermediation service.
F Yes with conditions: sales per salesperson are employee personal data; performance monitoring on a public screen is disproportionate — internal report for the owner only; Member States may set more specific rules for employee data (GDPR Art. 88). Debrief: in which cases did the licence decide, in which the GDPR, in which the Data Act?
:::

---

# Team Work: Your Project Data {.exercise}

1. List every table of your project that holds **personal data** — and which columns could be **removed** or **pseudonymised**
2. For one table: write a **record of processing** entry (purpose, legal basis, recipients, deletion period)
3. List every **external source** with its **licence** and the attribution line you will show
4. Name the **data owner** and the **data steward** of your case's main data
5. Add one slide "data protection and licences" to your final presentation

::: callout
**Final presentation (session 20):** design decisions, demo, lessons learned. One slide on data protection and licences shows that you thought about **access to data** — keep it short.
:::

::: notes
About 12 min. Walk around and ask: does your sample data contain real people? (If teams used real personal data from a company, they must replace it with fictional data before presenting.) Typical findings: birth dates and full addresses stored without need; a downloaded dataset without a licence note; nobody named as responsible. The presentation slide is optional but recommended; the exact requirements are in the project brief.
:::

---

# Key Takeaways

- **Personal data** is any data about an identifiable person; pseudonymised data still is, anonymous data is not
- The GDPR asks for a **legal basis**, follows **six principles** plus **accountability**, and gives people **rights**
- **Consent** must be freely given, specific, informed and unambiguous — and **provable**; a yes/no column is not proof
- **Data Act**: users get the data of their connected products; **DGA**: trusted data sharing; **AI Act**: data governance for high-risk AI
- **Open data** comes with a **licence** — attribution follows the lineage
- **Data governance** assigns decision rights: CDO, owner, steward, custodian; the strategy balances **defence and offence**
- Teaching material, not legal advice: in a real case, ask the **data protection officer**

::: source
Regulation (EU) 2016/679 (2016); Regulation (EU) 2023/2854 (2023); Regulation (EU) 2022/868 (2022); Regulation (EU) 2024/1689 (2024); Khatri and Brown (2010); DalleMule and Davenport (2017).
:::

---

# Next Session: Project Presentations and Exam Q&A

- **Team presentations** of the design projects
- Feedback round
- **Exam Q&A**: your questions on the whole course, question types and worked practice examples

::: callout
**Preparation:** finish the hands-on and worksheet 19. Finalise and rehearse your presentation (timing, demo, backup screenshots). Bring **your questions** for the Q&A — look through the key takeaways of all sessions.
:::

---

# References {.references}

- Abgabenordnung. (n.d.). *§ 147 Ordnungsvorschriften für die Aufbewahrung von Unterlagen*. Gesetze im Internet. Retrieved October 22, 2026, from https://www.gesetze-im-internet.de/ao_1977/__147.html
- Abraham, R., Schneider, J., & vom Brocke, J. (2019). Data governance: A conceptual framework, structured review, and research agenda. *International Journal of Information Management, 49*, 424–438. https://doi.org/10.1016/j.ijinfomgt.2019.07.008
- Bundesdatenschutzgesetz. (n.d.). *§ 38 Datenschutzbeauftragte nichtöffentlicher Stellen*. Gesetze im Internet. Retrieved October 22, 2026, from https://www.gesetze-im-internet.de/bdsg_2018/__38.html
- Commission Implementing Regulation (EU) 2023/138 of 21 December 2022 laying down a list of specific high-value datasets and the arrangements for their publication and re-use. (2023). *Official Journal of the European Union*, L 19, 43. http://data.europa.eu/eli/reg_impl/2023/138/oj
- Creative Commons. (n.d.). *Attribution 4.0 International (CC BY 4.0)*. Retrieved October 22, 2026, from https://creativecommons.org/licenses/by/4.0/
- DalleMule, L., & Davenport, T. H. (2017). What's your data strategy? *Harvard Business Review, 95*(3), 112–122.
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- de Maeyer, J. (n.d.). *Bright Sky: JSON API for DWD's open weather data* [API documentation]. Retrieved October 22, 2026, from https://brightsky.dev/docs/
- Deutscher Wetterdienst. (2024). *Terms of use for data on the CDC-OpenData area*. https://opendata.dwd.de/climate_environment/CDC/Terms_of_use.pdf

---

# References (continued) {.references}

- Directive 96/9/EC of the European Parliament and of the Council of 11 March 1996 on the legal protection of databases. (1996). *Official Journal of the European Communities*, L 77, 20. http://data.europa.eu/eli/dir/1996/9/oj
- Directive (EU) 2019/1024 of the European Parliament and of the Council of 20 June 2019 on open data and the re-use of public sector information (recast). (2019). *Official Journal of the European Union*, L 172, 56. http://data.europa.eu/eli/dir/2019/1024/oj
- European Commission. (n.d.-a). *Data Act explained*. Shaping Europe's digital future. Retrieved October 22, 2026, from https://digital-strategy.ec.europa.eu/en/factpages/data-act-explained
- European Commission. (n.d.-b). *Timeline for the implementation of the EU AI Act*. AI Act Service Desk. Retrieved October 22, 2026, from https://ai-act-service-desk.ec.europa.eu/en/ai-act/timeline/timeline-implementation-eu-ai-act
- European Commission. (n.d.-c). *What if my company/organisation fails to comply with the data protection rules?* Retrieved October 22, 2026, from https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/enforcement-and-sanctions/sanctions/what-if-my-companyorganisation-fails-comply-data-protection-rules_en
- European Commission. (2025). *Proposal for a regulation … as regards the simplification of the digital legislative framework … (Digital Omnibus)* (COM(2025) 837 final). https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52025PC0837
- Gesetz gegen den unlauteren Wettbewerb. (n.d.). *§ 7 Unzumutbare Belästigungen*. Gesetze im Internet. Retrieved October 22, 2026, from https://www.gesetze-im-internet.de/uwg_2004/__7.html
- GovData. (n.d.). *Datenlizenz Deutschland – Namensnennung – Version 2.0* [Data licence Germany – attribution – version 2.0]. https://www.govdata.de/dl-de/by-2-0
- Khatri, V., & Brown, C. V. (2010). Designing data governance. *Communications of the ACM, 53*(1), 148–152. https://doi.org/10.1145/1629175.1629210
- Lee, Y., Madnick, S., Wang, R., Wang, F., & Zhang, H. (2014). A cubic framework for the chief data officer: Succeeding in a world of big data. *MIS Quarterly Executive, 13*(1), 1–13.

---

# References (continued) {.references}

- OpenStreetMap Foundation. (n.d.). *Copyright and License*. Retrieved October 22, 2026, from https://www.openstreetmap.org/copyright
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1. http://data.europa.eu/eli/reg/2016/679/oj
- Regulation (EU) 2022/868 of the European Parliament and of the Council of 30 May 2022 on European data governance and amending Regulation (EU) 2018/1724 (Data Governance Act). (2022). *Official Journal of the European Union*, L 152, 1. http://data.europa.eu/eli/reg/2022/868/oj
- Regulation (EU) 2023/2854 of the European Parliament and of the Council of 13 December 2023 on harmonised rules on fair access to and use of data and amending Regulation (EU) 2017/2394 and Directive (EU) 2020/1828 (Data Act). (2023). *Official Journal of the European Union*, L, 2023/2854. http://data.europa.eu/eli/reg/2023/2854/oj
- Regulation (EU) 2024/1689 of the European Parliament and of the Council of 13 June 2024 laying down harmonised rules on artificial intelligence … (Artificial Intelligence Act). (2024). *Official Journal of the European Union*, L, 2024/1689. http://data.europa.eu/eli/reg/2024/1689/oj
- Regulation (EU) 2026/1744 of the European Parliament and of the Council of 8 July 2026 amending Regulations (EU) 2024/1689, (EU) 2018/1139 and (EU) 2023/1230 on simplifying the implementation of harmonised AI rules (Digital Omnibus on AI). (2026). *Official Journal of the European Union*, L, 2026/1744. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202601744
