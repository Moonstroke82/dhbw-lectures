---
course: Data Management
session: 20
title: Project Presentations and Exam Q&A
subtitle: Team presentations of the design projects · peer feedback · the course in one map · practice question types and worked practice examples
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

# Project Presentations and Exam Q&A {.title}

::: notes
Last session, no new content. Time plan for today (3 h): welcome, running order and feedback sheet 10 min · team presentations with questions and peer feedback about 100 min, with a 10 min break after half of the teams · feedback round on the presentations 10 min · course synthesis 10 min · question types and how to approach them 8 min · worked practice examples 27 min · open questions 12 min · wrap-up 3 min.
Presentations block (2 h): plan the slot per team from the number of teams. With six teams, for example: 10 min presentation incl. demo + 4 min questions + 2 min to write the peer feedback = 16 min per team, 96 min in total. With more teams, shorten the presentation, not the questions. Keep time strictly and visibly for everyone (a timer on the lectern laptop, a one-minute sign) — fairness between teams matters more than any single talk. The exact presentation length, the grading criteria and the submission of the final documentation are in the project brief; check them before class and adjust the running order slide.
Exam Q&A (1 h): every example is a practice example written for this course, labelled "practice, not from an exam". Never say "this will come up" or "the exam will look like this". Exam format, duration and permitted aids: give only the official information from the examination office (the weighting between exam and project was still open in MODULE.md when this deck was written — update the notes once it is fixed).
How the results were produced: the SQL on the worked example slides was run with SQLite 3.45.1 on a fresh bikeshop.db built from bikeshop-schema.sql, bikeshop-data.sql and bikeshop-data-session09.sql; the data quality ratios were computed with pandas 3.0.6 on the six rows shown on the slide. All other examples are paper exercises.
:::

---

# Today's Agenda

1. Recap: what your presentation should show
2. Project presentations: running order and peer feedback
3. Feedback round
4. The course in one map
5. Exam Q&A: practice question types and how to approach them
6. Worked practice examples
7. Your questions

::: notes
Time and format guide (not shown to students):
0:00 Welcome, running order, feedback sheet (plenary) · 0:10 Presentations, first half (teams present, everyone else writes peer feedback) · ~0:58 Break · 1:08 Presentations, second half · 1:50 Feedback round (plenary) · 2:00 Course synthesis (input, questions to the room) · 2:10 Question types and approach (input) · 2:18 Worked practice examples (individual or pairs, then plenary) · 2:45 Open questions (plenary) · 2:57 Wrap-up.
If presentations overrun, shorten the worked examples (keep at least two), never the open questions: the students' own questions are the most useful part of the Q&A. The remaining worked examples are in worksheet 20 for self-study.
:::

---

# Recap: Where Session 19 Left Us

- The design project ran through the whole course: **ER model → schema → database and SQL → loading and quality → star schema**
- Session 19 added one more question: may we use this data — **personal data, legal basis, licences**?
- Your preparation: a rehearsed presentation with **design decisions, demo, lessons learned** — and **your questions** for the Q&A

::: callout
**Quick check:** which design decision of your team would you defend first if someone asked "why did you do it this way"?
:::

::: source
Sessions 4 and 19 of this course (milestones and final presentation).
:::

::: notes
Two or three teams answer the quick check in one sentence each. It warms up the room and reminds everyone that the presentation is about decisions and their reasons, not about showing every table. Check that every team has its demo ready (database file, notebook, backup screenshots) and that laptops connect to the projector before the first talk — test them during this recap if needed.
:::

---

# Project Presentations {.section}

Design decisions, demo, lessons learned

---

# Today's Running Order

| # | Team | Case | Peer feedback by |
|---|---|---|---|
| 1 | Team … | … | Team … |
| 2 | Team … | … | Team … |
| 3 | Team … | … | Team … |
| 4 | Team … | … | Team … |
| 5 | Team … | … | Team … |
| 6 | Team … | … | Team … |

- Each team gets the **same time**; questions from the audience follow every talk
- Every team writes **peer feedback** for one other team — everyone listens to all talks

::: notes
Fill in the table before class or draw the order at the start (cards in a hat; a team with a technical risk may go later). Pair the feedback teams so that no two teams give feedback to each other (team 1 → 2, 2 → 3, …, last → 1). The time per team goes into these notes only, never on the slide (see the time plan on the title slide). Announce it orally and keep the timer visible.
:::

---

# What a Strong Presentation Shows

::: cards
### The case and its questions
What does the business do, and which **business questions** should the data answer?
### Design decisions
Two or three decisions with **reasons**: a weak entity type, an M:N table, a normal form, a constraint, the grain of the star.
### Demo
The database **answers** a question live: a query, a result, what one row means — backup screenshots ready.
### Data and quality
Where the data comes from, its **licence**, which defects you found and how you **measured** the improvement.
### Access to data
One slide: personal data, legal basis, licences and attribution — kept short.
### Lessons learned
What went wrong, what you would **do differently**, who did what in the team.
:::

::: source
Milestones from session 4; access to data from session 19.
:::

::: notes
These are the contents announced since session 4 ("design decisions, demo, lessons learned") plus the optional data protection slide of session 19. The grading criteria are in the project brief — if they differ, adjust this slide. A good demo is short: one business question, the query, the result, and one sentence on what one row means. Teams that tried something that failed (an API that changed, a pipeline that loaded duplicates) should say so: lessons learned are part of the content.
:::

---

# Peer Feedback Sheet {.exercise}

For the team you are assigned to: rate each criterion and note **one observation**.

| Criterion | What to look for | ++ | + | o | − |
|---|---|---|---|---|---|
| Case and questions | clear business case, concrete business questions | | | | |
| Data model and schema | decisions explained with reasons and course concepts | | | | |
| Database and SQL | constraints on, queries answer the questions, demo works | | | | |
| Data and quality | sources, licences, quality rules, before and after | | | | |
| Star schema | process, grain, facts, dimensions stated | | | | |
| Access to data | personal data, legal basis, attribution considered | | | | |
| Presentation | structure, clarity, answers to questions | | | | |

- Finish with **one strength**, **one question** and **one suggestion**

::: notes
Print one sheet per team in advance, or let teams copy the table into a shared document. The peer feedback is formative: it goes to the presenting team, not into the grade, unless the project brief says otherwise. Collect the sheets at the end and hand them to the teams (or the teams exchange them directly). If a criterion did not apply to a case, students tick nothing and write "not shown". The ratings are a conversation starter; the written observation is what helps the team.
:::

---

# Giving Useful Feedback

::: columns
**Three questions**

- **Where is the team going?** What did they want to show?
- **How did it go?** What worked, what did not — with an **observation**
- **Where next?** One concrete step to improve
|||
**Rules for today**

- Describe what you **saw or heard**, not the person
- Be **specific**: "the star has no grain statement" beats "the model is unclear"
- **Suggest**, do not rewrite: one change, with a reason
- Ask questions that help the team **think further**
:::

::: source
Hattie and Timperley (2007); own rules for this course.
:::

::: notes
Hattie and Timperley (2007) describe effective feedback as answering three questions — where am I going (feed up), how am I going (feed back), where to next (feed forward) — and show that feedback about the task and the process helps more than feedback about the person. The rules on the right are the same as in the peer review of session 12. During the feedback round after all talks, ask two or three teams to read out one strength and one suggestion they wrote; then add the lecturer's own general observations (patterns across teams, not grades).
:::

---

# Feedback Round {.exercise}

1. Each feedback team reads out **one strength** and **one suggestion** for its team
2. The presenting team may answer in **one sentence**
3. Together: which **design decision** did several teams struggle with? Which **lesson learned** came up most often?

::: notes
About 10 min after the last talk. Keep it short and positive; detailed feedback is on the sheets. Collect the patterns from question 3 on the whiteboard — they are also good material for the Q&A (often: grain of the star schema, NULL handling in outer joins, cleaning decisions that were really business decisions, missing licence notes). Record them in your own course notes for the next run of the course.
:::

---

# Course Synthesis {.section}

From a business case to data the organisation can use

---

# The Course in One Map

![Map of the course in four columns. Part A, foundations: how do we describe the data? Sessions 1 to 6 with data types, ER model, relational model and normalisation, resulting in a normalised schema. Part B, SQL and databases: how do we store and query it? Sessions 7 to 11 with DDL and DML, joins, aggregation and transactions, and NoSQL, resulting in a database that answers questions. Part C, quality and access: how do we get good data in? Sessions 13 to 16 with quality dimensions and metrics, cleaning with pandas, files and APIs, and ETL, resulting in clean, integrated data. Part D, storage and rules: where does the data live and who may use it? Sessions 17 to 19 with data warehouse and star schema, lake, lakehouse, mesh and fabric, EU data law and governance, resulting in data the organisation can use. Below, the project milestones M1 to M5 and the presentation](img/synthesis-course-map.png){width=86%}

::: source
Own illustration based on sessions 1–19 of this course; milestones from session 4.
:::

::: notes
Walk through the map from left to right in about three minutes, one sentence per part. Each part answers one question, and the result of each part is the input of the next: a normalised schema becomes tables, tables are filled with cleaned and integrated data, and that data is stored for analysis under rules. Point at the bottom row: the design project followed the same path. Ask: in which column did your team spend the most time? (Usually C — loading and cleaning take longer than expected; that is a realistic lesson.)
:::

---

# Five Threads Through the Course

| Thread | Where it came up |
|---|---|
| **Business rules first** | cardinalities (3), functional dependencies (6), constraints (7), quality rules (13), access rules (19) |
| **What does one row mean?** | relations (5), joins and `GROUP BY` (9–10), cleaning duplicates (14), the grain of a star (17) |
| **Integrity is designed, not hoped for** | keys and foreign keys (5, 7), ACID (10), CAP and BASE (11), idempotent loads (16) |
| **Fix at the source** | normalisation against anomalies (6), quality causes (13), cleaning moves defects (14), lineage (18) |
| **Data has a context** | metadata (2), licences (15, 19), catalogues (18), purpose and legal basis (19) |

::: source
Own summary of sessions 1–19 of this course, based on Elmasri and Navathe (2016), Pipino et al. (2002), Kimball and Ross (2013) and DAMA International (2017).
:::

::: notes
These threads connect topics that students tend to learn as separate boxes. For revision, suggest the threads as a checklist: for any concept, ask which thread it belongs to. Example question to the room: "What does count(*) after a LEFT JOIN have in common with duplicate customer accounts?" — both are about what one row means. Keep this slide to about five minutes.
:::

---

# Exam Q&A {.section}

Practice question types, how to approach them, worked practice examples

---

# Practice Question Types

| Type | Typical operator | A good answer … |
|---|---|---|
| **Explain and distinguish** | define, explain, compare | names the **criterion** of the difference, with an example for each side |
| **Model a case** | draw, model, map | uses every fact of the case text; keys, cardinalities, participation |
| **Normalise** | determine, decompose | lists the **dependencies**, names the normal form **with the reason** |
| **Write and read SQL** | write, predict, find the error | states what **one row** means; predicts the result; names the cause |
| **Measure and treat** | calculate, assess | shows rule, numerator, denominator — then a **decision** with a reason |
| **Design and argue** | design, recommend, justify | grain, facts, dimensions — or law, principle, licence **applied to the case** |

::: callout
These are **practice** question types used in the worksheets of this course. They are not taken from any exam.
:::

::: notes
Exam format details (duration, permitted aids, number of tasks, weighting with the project) are announced by the lecturer and the examination office; give only official information here. Point out that every worksheet of the course has an exam-style practice task with a marking guide, and worksheet 20 is a mixed revision set across all parts. Do not make statements such as "this will be in the exam" or "this is likely to come up". Session 1 promised: core slides are exam-relevant, optional slides only if covered in class — repeat that rule.
:::

---

# How to Approach a Question

1. **Read the operator**: "name" asks for a list, "explain" for reasons, "assess" for a judgement
2. **Mark the business rules** in the case: "exactly one", "at most", "per day", "is stored"
3. **Predict before you write**: how many rows, which value, which normal form?
4. **Show your steps**: dependencies, join path, numerator and denominator — partial credit needs visible work
5. **State assumptions** where the case is open: "assumption: a member can book a room only once per day"
6. **Check the points**: roughly one argument or one element per point

::: callout
Common slips: cardinality read from one side only · `= NULL` · `count(*)` after an outer join · a ratio without its denominator · a law named but not applied to the case
:::

::: source
Own guidance based on the exercises and worksheets of this course.
:::

::: notes
Show "claim – reason – case fact" on the board, e.g. "The booking is a weak entity type (claim), because it cannot be identified without its room (reason): rooms are numbered within a house (case fact)." For SQL on paper: write the query in clauses on separate lines, then check each SELECT column against the GROUP BY. For drawings: label every relationship and give the notation (Chen or crow's foot). Assumptions are fine when the case leaves a rule open — but not to change a rule that the case states.
:::

---

# Worked Practice Example 1: Explain and Distinguish {.exercise}

*Practice, not from an exam.* Distinguish a **data warehouse** from a **data lake**. Give one example for each from the bike shop.

::: columns
**Weak answer**

"A data warehouse is for structured data and a data lake is for big data. Both store data for analysis."
|||
**Stronger answer**

- **Criterion 1 — when the structure is applied**: the warehouse defines it **on write** (cleaned, integrated tables); the lake stores raw files and applies it **on read**
- **Criterion 2 — data and users**: warehouse — integrated, historical data for **BI** (fact_sales by day and weather); lake — any format, also unstructured, for exploration and ML (clickstream files, damage photos)
- **Risk**: a lake without a catalogue becomes a **swamp**
:::

::: source
Practice example based on Serra (2024) and Inmon (2005); bike shop examples from sessions 17–18.
:::

::: notes
About 4 min: students write their own two-sentence answer first, then compare with the two versions. Why the weak answer is weak: no criterion, "big data" is a property of data and not a storage concept (session 1), and no example. Marking idea for such a question (practice): one point per criterion with an example, one point for a correct consequence or risk. Alternative criteria that are also correct: subject-oriented and integrated (Inmon) vs. raw and multi-purpose; cost of change; typical users.
:::

---

# Worked Practice Example 2: Normalise a List {.exercise}

*Practice, not from an exam.* The sports club keeps its **course registrations** in one list. Key: (course_no, member_no).

| course_no | title | trainer_no | trainer_name | member_no | member_name | paid |
|---|---|---|---|---|---|---|
| K1 | Yoga | T1 | Ines Bauer | 1001 | Paul Meier | yes |
| K1 | Yoga | T1 | Ines Bauer | 1002 | Eva Lorenz | no |
| K2 | Pilates | T1 | Ines Bauer | 1001 | Paul Meier | yes |
| K3 | Spinning | T2 | Tom Sander | 1003 | Jan Wolf | yes |

1. List the functional dependencies
2. In which normal form is the list? Why?
3. Decompose it into 3NF

::: source
Practice example based on Elmasri and Navathe (2016, Chapter 14).
:::

::: notes
About 6 min individually, then the solution on the next slide. Business rules to state if students ask: each course has exactly one trainer; "paid" refers to the registration of one member for one course.
:::

---

# Worked Practice Example 2: Solution

1. **Dependencies**: course_no → title, trainer_no · trainer_no → trainer_name · member_no → member_name · (course_no, member_no) → paid
2. **1NF only**: values are atomic, but title and trainer_no depend on **part** of the key (course_no) and member_name on member_no — **partial** dependencies violate 2NF; trainer_name depends **transitively** via trainer_no
3. **3NF decomposition**:
   - COURSE(**course_no**, title, *trainer_no* → TRAINER)
   - TRAINER(**trainer_no**, trainer_name)
   - MEMBER(**member_no**, member_name)
   - REGISTRATION(**course_no** → COURSE, **member_no** → MEMBER, paid)

::: callout
Check: every fact is stored **once** — Ines Bauer's name now appears in one row, and a course without registrations can be stored.
:::

::: source
Practice example based on Elmasri and Navathe (2016, Chapter 14).
:::

::: notes
Typical slips: forgetting the composite determinant of "paid"; calling the list 2NF because "there are no repeating groups"; decomposing into COURSE(course_no, title, trainer_no, trainer_name), which is 2NF but not 3NF. Anomalies to name if asked: update (Ines Bauer changes her name in three rows), insertion (a new course without members), deletion (deleting Jan Wolf's registration loses trainer T2 and course K3).
:::

---

# Worked Practice Example 3: Find the Error {.exercise}

*Practice, not from an exam.* Bike shop: **every spare part** with the number of repair jobs **since 1 March 2027** in which it was used — parts without such jobs with 0.

```sql
SELECT p.part_no, p.name, count(*) AS jobs
FROM spare_part p
LEFT JOIN repair_line l ON l.part_no = p.part_no
LEFT JOIN repair_job  j ON j.job_no  = l.job_no
WHERE j.job_date >= '2027-03-01'
GROUP BY p.part_no, p.name;
```

1. The shop has 12 spare parts. How many rows does the query return — and why?
2. Correct the query. Which parts get 0?

::: source
Practice example on the bike shop data; based on Elmasri and Navathe (2016, Chapter 7) and session 9–10 of this course.
:::

::: notes
About 6 min in pairs. Let them predict before revealing the solution. The data is the fresh bike shop database (three scripts); students who have their notebook open may run it.
:::

---

# Worked Practice Example 3: Solution

- **9 rows** (observed): the `WHERE` condition on the optional table removes every row the outer join filled with NULL — the `LEFT JOIN` behaves like an inner join
- Second error: `count(*)` counts rows, also the NULL row of a part without jobs → count a column of the **optional** table

```sql
SELECT p.part_no, p.name, count(j.job_no) AS jobs
FROM spare_part p
LEFT JOIN repair_line l ON l.part_no = p.part_no
LEFT JOIN repair_job  j ON j.job_no  = l.job_no
                       AND j.job_date >= '2027-03-01'
GROUP BY p.part_no, p.name;
```

- **12 rows**; 0 jobs for **P-104** Chain 9-speed, **P-107** Gear cable, **P-112** Mudguard set

::: source
Own example on the bike shop data; results observed with SQLite 3.45.1.
:::

::: notes
All observed on the fresh database. Only moving the condition into ON but keeping count(*) gives 12 rows with wrong numbers: P-103 Brake pads 4 (it counts all four repair lines, also those before March), P-104, P-107 and P-112 each 1 (observed). Moving the condition and counting j.job_no gives the right answer: P-103 1 (job 508), and so on. Point out the two answer elements a marker would look for: the cause (WHERE removes NULL rows; count(*) counts the NULL row) and the fix with the expected result.
:::

---

# Worked Practice Example 4: Measure and Treat {.exercise}

*Practice, not from an exam.* The car-sharing company's vehicle list. Rules: mileage filled and ≥ 0 · last service an ISO date · one row per licence plate.

| plate | model | mileage_km | last_service |
|---|---|---|---|
| HD-CS 101 | ID.3 | 42310 | 2027-03-02 |
| HD-CS 102 | Zoe | | 2027-01-15 |
| HD-CS 103 | Corsa-e | −150 | 2026-11-30 |
| HD-CS 104 | ID.3 | 18900 | 15.02.2027 |
| HD-CS 101 | ID.3 | 42310 | 2027-03-02 |
| HD-CS 105 | 500e | 9870 | |

1. Calculate completeness and validity of the mileage, and the uniqueness of the plates
2. Decide a treatment for each defect

::: source
Practice example based on Pipino et al. (2002) and Government Data Quality Hub (2021).
:::

::: notes
About 6 min individually. Remind: validity is measured on the filled values, completeness on all rows (session 13) — otherwise a missing value counts twice. Solution follows in the notes of this slide to keep the deck short; show it on the board.
Solution (computed with pandas 3.0.6 on these six rows): completeness of mileage 1 − 1/6 = 83.3 %; validity of mileage on the five filled values 1 − 1/5 = 80 % (HD-CS 103 negative); uniqueness of plates 1 − 1/6 = 83.3 % (HD-CS 101 twice, identical rows). Last service: completeness 5/6, validity 4/5 (HD-CS 104 in German format). Treatments: duplicate 101 → drop the exact copy (identical in all columns); 102 missing mileage → ask the fleet team or read it from the telematics system, do not fill with a mean (it would look valid); 103 −150 → flag and ask, likely a typing error, never silently take the absolute value; 104 date → standardise to 2027-02-15 (a format defect, the value is recoverable); 105 missing service date → flag; a car without a known service date may be a safety question for the business. Point out: valid is not accurate — 42310 km is valid but only the odometer can confirm it. Fix at the source: a CHECK (mileage_km >= 0) and a date CHECK in the fleet database.
:::

---

# Worked Practice Example 5: Design and Argue {.exercise}

*Practice, not from an exam.* The sports club's tennis department rents out **courts by the hour**. It wants to analyse **bookings per court, weekday and member type**, and the treasurer wants to put the **booking list with names** on the public website.

1. Name the business process, the **grain**, two **dimensions** and two **facts**. Which fact is not additive?
2. May the club publish the booking list with names? Argue with **one principle** and **one legal basis**

::: source
Practice example based on Kimball and Ross (2013) and Regulation (EU) 2016/679 (2016, Art. 5 and 6); teaching material, not legal advice.
:::

::: notes
About 6 min in pairs, then collect answers. Model answer (practice): 1 Process: court booking. Grain: one booking of one court for one hour slot (or one booking). Dimensions: date (weekday, month), court (surface, indoor/outdoor), member (type: adult, youth, guest), time slot. Facts: hours booked, fee paid (additive); utilisation in % per court and day is non-additive (ratios are recomputed from hours, not summed). 2 Names of members are personal data. Publishing on a public website is not needed for the purpose "organise court use" (data minimisation, purpose limitation); the membership contract covers internal use, not public display. Options: show only "booked" without names, or a members-only area; publishing names would need consent. Good answers apply the principle to the case — just naming "GDPR" earns little.
:::

---

# Your Questions {.exercise}

::: cards
### Concepts
Which term or distinction is still unclear?
### SQL
Which query type do you want to see once more?
### Data and pipelines
Cleaning, APIs, ETL — what would you like to repeat?
### Architecture and rules
Warehouse, lake, GDPR, licences — what is open?
:::

- Write your question on a card — **anonymous** is fine; we answer the most frequent ones first

::: notes
About 12 min. Collect cards, cluster them quickly by the four boxes, answer the largest cluster first. Answer with course material (point to the session and slide) and a small example on the board; do not answer questions about the content of the exam beyond the official information. If a question needs more time than available, point to the matching worksheet task.
:::

---

# Key Takeaways

- The course follows one path: **describe → store and query → get good data in → store for analysis, under rules**
- The design project applied every part to **your own case** — design decisions need **reasons**
- Useful feedback names an **observation** and **one next step**
- Answer by the **operator**, use the **case facts**, **show your steps**, state **assumptions**
- Revise by **threads**: business rules, the meaning of one row, integrity, fix at the source, context

::: source
Own summary of sessions 1–20 of this course; Hattie and Timperley (2007).
:::

---

# After Today: Preparing for the Exam

- **Worksheet 20**: a mixed revision set across Parts A–D — **practice, not from an exam**
- The **exam-style practice task** of every worksheet, with its marking guide
- The **key takeaways** of all sessions; core slides are exam-relevant, optional slides only where covered in class
- Your team's **peer feedback** — and the final documentation as described in the **project brief**

::: callout
**Thank you** for twenty sessions of questions, discussions and databases. Exam format, date and permitted aids: as announced by the examination office.
:::

::: notes
Point to the course website for all decks and worksheets. Ask for the official course evaluation if the university runs one, and invite short written feedback on the course (what to keep, what to change) for the 2028 run — record it in your own course notes together with the timing feedback for the decks. Do not give additional hints about exam content.
:::

---

# References {.references}

- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Government Data Quality Hub. (2021, June 24). *Meet the data quality dimensions*. GOV.UK. https://www.gov.uk/government/news/meet-the-data-quality-dimensions
- Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81–112. https://doi.org/10.3102/003465430298487
- Inmon, W. H. (2005). *Building the data warehouse* (4th ed.). Wiley.
- Kimball, R., & Ross, M. (2013). *The data warehouse toolkit: The definitive guide to dimensional modeling* (3rd ed.). Wiley.
- Pipino, L. L., Lee, Y. W., & Wang, R. Y. (2002). Data quality assessment. *Communications of the ACM, 45*(4), 211–218. https://doi.org/10.1145/505248.506010
- Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data, and repealing Directive 95/46/EC (General Data Protection Regulation). (2016). *Official Journal of the European Union*, L 119, 1. http://data.europa.eu/eli/reg/2016/679/oj
- Serra, J. (2024). *Deciphering data architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh*. O'Reilly Media.
