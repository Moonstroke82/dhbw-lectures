---
course: Data Management
session: 6
title: Efficient Database Design: Normalisation
subtitle: Practice tasks on anomalies, functional dependencies, normal forms and denormalisation
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 6 on your own or with your project team. Use the notation from the slides: functional dependencies as X → Y, relation names in capitals, the **primary key in bold** (on paper: underline it) and foreign keys in *italics* with an arrow to the referenced relation, e.g. BIKE(**frame_no**, model, *customer_no* → CUSTOMER). The definitions of the normal forms follow the slides, which are based on Codd (1972), Kent (1983) and Elmasri and Navathe (2016, Chapter 14). Paper and pencil are enough. The spreadsheet in task 4 is also available as a CSV file: [neckar-catering-orders.csv](data/neckar-catering-orders.csv). Task 7 continues the sports club case from worksheets 4 and 5.

## Spot the Anomalies

A music school keeps its lessons in one table. Each student learns each instrument with exactly one teacher; each teacher always teaches in the same room.

| student_no | student_name | instrument | teacher_no | teacher_name | teacher_phone | room |
|---|---|---|---|---|---|---|
| S-01 | Mia Lang | piano | T-2 | Jonas Ott | 0621 4401 | R1 |
| S-02 | Ben Kurz | guitar | T-5 | Vesna Ilić | 0621 4405 | R3 |
| S-03 | Lina Vogel | piano | T-2 | Jonas Ott | 0621 4401 | R1 |
| S-01 | Mia Lang | violin | T-7 | Clara Sommer | 0621 4407 | R2 |

1. Which facts are stored **more than once**? Name two.
2. Give one concrete example each of an **update**, an **insert** and a **delete anomaly** in this table.
3. Which "things" (entity types) are mixed in this one table?

::: answer lines=10
:::

::: solution
1. The name of student S-01 (twice) and everything about teacher T-2: name, phone and room appear in every lesson he gives. Any one of these is enough as an example.
2. Model answers (other concrete examples are fine if they name rows or values):
  - **Update:** Jonas Ott gets a new phone number. Both rows with T-2 must be changed; if only one is, the table contains two phone numbers for the same teacher.
  - **Insert:** a new teacher who has no students yet cannot be stored, because a row needs a student (student_no is part of the key and must not be NULL).
  - **Delete:** Ben Kurz stops learning the guitar. Deleting his row also deletes the only record of teacher Vesna Ilić, her phone number and her room.
3. *Student*, *Teacher* (with room) and the lesson relationship between them (who learns which instrument with whom). If rooms had more attributes, *Room* would be a fourth one.
:::

## Reading Functional Dependencies from Data

A parcel service stores deliveries in this table:

| parcel_no | sender_no | sender_name | dest_postcode | dest_city | driver_no | driver_name | depot |
|---|---|---|---|---|---|---|---|
| 7001 | S-1 | Kraus KG | 68159 | Mannheim | D-4 | Lena Roth | Mannheim-Nord |
| 7002 | S-2 | Bauer AG | 69117 | Heidelberg | D-7 | Paul Klein | Heidelberg |
| 7003 | S-1 | Kraus KG | 68161 | Mannheim | D-4 | Lena Roth | Mannheim-Nord |
| 7004 | S-3 | Kraus KG | 68159 | Mannheim | D-9 | Lena Roth | Mannheim-Süd |
| 7005 | S-2 | Bauer AG | 69117 | Heidelberg | D-7 | Paul Klein | Heidelberg |

**Part A.** For each functional dependency, decide whether the data **violates** it or whether it **may hold**. For violations, name the rows.

1. sender_no → sender_name
2. sender_name → sender_no
3. dest_postcode → dest_city
4. dest_city → dest_postcode
5. driver_name → depot
6. dest_postcode → driver_no
7. driver_no → depot

**Part B.** The business confirms: parcel_no → sender_no, dest_postcode, driver_no · sender_no → sender_name · dest_postcode → dest_city · driver_no → driver_name, depot. What is the primary key? Is the table in 2NF? In 3NF? Decompose it into 3NF.

::: hint
Look for two rows with the **same** value on the left side. If their values on the right side differ, the dependency is violated. If you find no such pair, the data does not contradict it — but that is not a proof.
:::

::: answer lines=12
:::

::: solution
Part A:

1. **May hold:** S-1 always has Kraus KG, S-2 always Bauer AG.
2. **Violated:** rows 7001 and 7004 have the same sender name but S-1 and S-3 (two different companies called Kraus KG).
3. **May hold:** 68159 is always Mannheim, 69117 always Heidelberg.
4. **Violated:** Mannheim appears with 68159 and 68161 (rows 7001 and 7003).
5. **Violated:** Lena Roth appears with Mannheim-Nord and Mannheim-Süd (rows 7001 and 7004); there are two drivers with this name (D-4 and D-9).
6. **Violated:** 68159 appears with D-4 and D-9 (rows 7001 and 7004).
7. **May hold:** D-4 is always Mannheim-Nord, D-7 always Heidelberg.

Sample data can disprove a dependency but never prove it; "may hold" must be confirmed by the business, as in Part B.

Part B:

- Primary key: **parcel_no** (it determines all other attributes).
- **2NF: yes.** The key has only one attribute, so there can be no partial dependencies.
- **3NF: no.** Transitive dependencies: parcel_no → sender_no → sender_name; parcel_no → dest_postcode → dest_city; parcel_no → driver_no → driver_name, depot.
- Decomposition:
  - PARCEL(**parcel_no**, *sender_no* → SENDER, *dest_postcode* → POSTCODE, *driver_no* → DRIVER)
  - SENDER(**sender_no**, sender_name)
  - POSTCODE(**postcode**, city)
  - DRIVER(**driver_no**, driver_name, depot)

Good answers note that many real systems keep postcode and city together in the address on purpose: a postcode does not always identify exactly one town, and a postcode table must be maintained. Leaving city in PARCEL with this justification is acceptable if the student names it as a deliberate decision.
:::

## Key and Normal Form

For each relation, the business rules are given as functional dependencies. Name all **candidate keys**, the **highest normal form** (1NF, 2NF, 3NF or BCNF) the relation meets, and the dependency that prevents the next higher normal form. All relations are in 1NF.

1. EXAM_RESULT(student_no, course_no, grade, course_title) with {student_no, course_no} → grade and course_no → course_title
2. COURSE_OFFER(course_no, semester, lecturer_no, lecturer_name, room) with {course_no, semester} → lecturer_no, room and lecturer_no → lecturer_name
3. COUNTRY(iso_code, name, capital) with iso_code → name, capital and name → iso_code
4. PROJECT_WORK(employee_no, project_no, hours, manager_no, manager_name) with {employee_no, project_no} → hours, project_no → manager_no and manager_no → manager_name

::: answer lines=10
:::

::: hint
First find the key: which attributes appear on no right-hand side? They must be part of every key. Then check partial dependencies (2NF), then dependencies between non-key attributes (3NF), then whether every determinant is a superkey (BCNF).
:::

::: solution
1. Key {student_no, course_no}. **1NF only:** course_no → course_title is a partial dependency (course_title depends on part of the key). Fix: COURSE(**course_no**, course_title).
2. Key {course_no, semester}. **2NF:** no attribute depends on only course_no or only semester; but lecturer_no → lecturer_name is transitive, so not 3NF. Fix: LECTURER(**lecturer_no**, lecturer_name).
3. Candidate keys {iso_code} and {name}. **BCNF:** both determinants (iso_code and name) are candidate keys. name → capital is not a transitive dependency, because name is a key. A common mistake is to call this a 3NF violation.
4. Key {employee_no, project_no}. **1NF only:** project_no → manager_no is a partial dependency; in addition, manager_no → manager_name is transitive. Fix: PROJECT(**project_no**, *manager_no* → MANAGER), MANAGER(**manager_no**, manager_name), PROJECT_WORK(**employee_no, project_no**, hours). Full credit needs both problems to be named.
:::

## Normalise a Messy Spreadsheet: Neckar Catering

*Neckar Catering* delivers food to companies. The office keeps its orders in this spreadsheet (also as [CSV file](data/neckar-catering-orders.csv)):

| order_no | order_date | client | client_city | items | unit_prices | driver | van |
|---|---|---|---|---|---|---|---|
| O-1001 | 2027-06-01 | K-12 Rhein Software GmbH | Mannheim | D-03 Falafel wrap x40; D-11 Fruit salad x40 | 4.50; 3.20 | Sami Yilmaz | MA-NC 101 |
| O-1002 | 2027-06-01 | K-07 Kanzlei Vogt | Heidelberg | D-05 Spinach quiche x12 | 5.80 | Ella Fischer | MA-NC 102 |
| O-1003 | 2027-06-03 | K-12 Rhein Software GmbH | Mannheim | D-05 Spinach quiche x25; D-11 Fruit salad x25; D-20 Coffee pot x5 | 5.80; 3.20; 12.00 | Sami Yilmaz | MA-NC 101 |
| O-1004 | 2027-06-04 | K-19 Stadtbibliothek Mannheim | Mannheim | D-03 Falafel wrap x30 | 4.50 | Ella Fischer | MA-NC 102 |

Business rules: each order is for one client and is delivered by one driver. Each driver always uses the same van. The unit prices are taken from the menu, and the menu prices change every season.

1. Why is this spreadsheet not a relation in 1NF? Name every problem.
2. Bring it into **1NF**. Give the attribute list, the primary key and the number of rows.
3. Write down all **functional dependencies**.
4. Normalise to **2NF** and then to **3NF**. Write the final schema with primary and foreign keys.
5. Check your result: which anomaly from the original spreadsheet does your schema prevent? Give one example.

::: hint
Introduce keys where the spreadsheet only has names (a driver number). For the prices, ask: does the price depend on the dish alone, or on the dish **in this order**?
:::

::: answer lines=16
:::

::: solution
1. Not atomic: **items** holds a list of dishes with quantities (a repeating group), **unit_prices** holds a list that only fits the items by position, **client** combines client number and name in one cell. Drivers are identified only by name. Any three of these with a correct explanation earn full credit.
2. 1NF: ORDER_1NF(**order_no, dish_no**, order_date, client_no, client_name, client_city, dish_name, quantity, unit_price, driver_no, driver_name, van_plate); one row per order and dish, so **7 rows** (2 + 1 + 3 + 1).
3. Functional dependencies:
  - order_no → order_date, client_no, driver_no
  - client_no → client_name, client_city
  - dish_no → dish_name, list_price
  - {order_no, dish_no} → quantity, price_charged
  - driver_no → driver_name, van_plate
  - Prices: because menu prices change every season, the spreadsheet's unit price is split into two facts: the current **list_price** of the dish and the **price_charged** in this order (history, pitfall 2 from session 4). Students who keep only one price and argue that it is the price charged ({order_no, dish_no} → unit_price) are also correct; keeping only the dish price loses the history and earns partial credit.
4. Normalisation in two steps:
  - **2NF** (remove partial dependencies on the key {order_no, dish_no}): ORDER_LINE(**order_no, dish_no**, quantity, price_charged) · DISH(**dish_no**, dish_name, list_price) · ORDER_2NF(**order_no**, order_date, client_no, client_name, client_city, driver_no, driver_name, van_plate)
  - **3NF** (remove transitive dependencies from ORDER_2NF), final schema below
  - CATERING_ORDER(**order_no**, order_date, *client_no* → CLIENT, *driver_no* → DRIVER)
  - CLIENT(**client_no**, client_name, city)
  - DRIVER(**driver_no**, driver_name, van_plate)
  - ORDER_LINE(**order_no, dish_no**, quantity, price_charged), *order_no* → CATERING_ORDER, *dish_no* → DISH
  - DISH(**dish_no**, dish_name, list_price)
  - Naming: ORDER is a reserved word in SQL, so a different relation name (CATERING_ORDER) is sensible. A separate VAN(**van_plate**, …) relation is fine if vans get attributes of their own; if every van also has exactly one driver, van_plate is an alternate key of DRIVER.
5. Examples: if Rhein Software moves to Heidelberg, the city is changed once in CLIENT (update); a new dish can be added to DISH before anyone orders it (insert); deleting order O-1002 no longer deletes the only record of client Kanzlei Vogt (delete). One correct example is enough.
:::

## Boyce–Codd Normal Form: A Driving School

A driving school stores which instructor trains which student for which licence class:

TRAINING(student_no, licence_class, instructor_no)

Business rules: a student can train for several licence classes (e.g. B for cars, A for motorbikes). For each licence class, a student has exactly one instructor. Each instructor teaches **only one** licence class; a licence class is taught by several instructors.

1. Write down the functional dependencies.
2. Name all candidate keys.
3. Is TRAINING in 3NF? Is it in BCNF? Justify both answers.
4. Decompose TRAINING into BCNF relations.
5. Which business rule can no longer be checked within a single relation after your decomposition? Would you decompose anyway?

::: answer lines=12
:::

::: solution
1. {student_no, licence_class} → instructor_no · instructor_no → licence_class
2. {student_no, licence_class} and {student_no, instructor_no}. The second is a key because instructor_no determines licence_class, so {student_no, instructor_no} determines all attributes and is minimal.
3. **3NF: yes.** The only dependency whose determinant is not a superkey is instructor_no → licence_class, and licence_class is part of a candidate key (a prime attribute), which 3NF allows. All attributes are part of some key, so there are no non-key attributes at all. **BCNF: no**, because the determinant instructor_no is not a superkey.
4. INSTRUCTOR(**instructor_no**, licence_class) and TRAINING(**student_no, instructor_no**), *instructor_no* → INSTRUCTOR.
5. The rule "a student has only **one** instructor per licence class" ({student_no, licence_class} → instructor_no) is lost: the new TRAINING relation would accept two class-B instructors for the same student. Both answers are acceptable with a reason: decompose (redundancy of the instructor's class removed; the rule is checked by the application or a trigger) or stay in 3NF (the rule is more important than the small redundancy). Textbooks note that 3NF can always be reached without losing dependencies, BCNF not always.
:::

## Denormalise or Not?

An online bookshop has a normalised operational database. Its developers propose the following changes. For each one, decide: is it **denormalisation**? Would you **accept** it? Name the cost or risk and how consistency could be ensured.

1. Add a column *order_total* to ORDER, so the order overview page does not have to sum up the order lines.
2. Copy the customer's delivery address into ORDER at checkout.
3. Build a reporting table SALES_REPORT(order_date, book_title, category_name, customer_city, revenue), reloaded every night from the operational tables, for the analytics team.
4. Add *category_name* to BOOK next to *category_id*, so the book page needs no join.
5. Store the customer's *age* in CUSTOMER for marketing campaigns.

::: answer lines=12
:::

::: solution
1. **Denormalisation** (derived data). Acceptable only with a reason, e.g. the overview page is read very often. Cost: every change of an order line must update the total (in the same transaction or by a trigger), otherwise totals become wrong. Alternatives: compute on the fly or use a view. After invoicing, when lines no longer change, a stored total is a harmless snapshot.
2. **Not denormalisation:** the delivery address at the time of the order is a different fact from the customer's current address (history). Accept; it must **not** change when the customer moves.
3. **Denormalisation, deliberately**, for analytics. Accept: the table is only read, and the nightly reload (ETL) keeps it consistent. This is the idea behind star schemas in a data warehouse (session 17). Cost: the report is up to one day old.
4. **Denormalisation** that violates 3NF (category_id → category_name). Reject: the join is cheap, and renaming a category would create an update anomaly in every book row.
5. Not denormalisation in the strict sense, but **derived data** that goes out of date every day (pitfall 3 from session 4). Reject: store date_of_birth and compute the age when needed.

Marking: one point per item for a correct decision with a reason; the cost or consistency measure is needed for full credit on items 1, 3 and 4.
:::

## Exam-Style Task: The Sports Club's Membership List

This task is in the style of an exam question. The treasurer of the sports club from worksheets 4 and 5 keeps the following list:

| member_no | member_name | youth | parent_phone | dept_name | monthly_fee | joined_on | head_no | head_name |
|---|---|---|---|---|---|---|---|---|
| M-01 | Nina Hoff | no | – | Football | 25.00 | 2024-09-01 | M-08 | Karl Brenner |
| M-02 | Tim Akın | yes | 0176 22001 | Football | 25.00 | 2025-03-15 | M-08 | Karl Brenner |
| M-02 | Tim Akın | yes | 0176 22001 | Tennis | 40.00 | 2026-04-01 | M-11 | Eva Lorenz |
| M-08 | Karl Brenner | no | – | Football | 25.00 | 2019-01-10 | M-08 | Karl Brenner |

Business rules: a member can belong to several departments; joined_on is the date the member joined that department. Each department has one monthly fee and one head of department, who is a member of the club (head_no is a member number). A parent phone number is stored for youth members only.

1. Give one example each of an update, an insert and a delete anomaly in this list. (3 points)
2. Write down all functional dependencies and the primary key. (3 points)
3. What is the highest normal form of the list? Justify your answer. (1 point)
4. Decompose the list into 3NF. Mark primary and foreign keys. (3 points)

::: answer lines=16
:::

::: solution
1. Examples (1 point each, any correct concrete example):
  - **Update:** the football fee rises to 28.00; three rows must be changed. Or: Karl Brenner changes his name; it is stored as member_name and as head_name.
  - **Insert:** a new department (e.g. handball) with its fee and head cannot be stored before a member joins it.
  - **Delete:** if Tim Akın leaves tennis, the row with the only record of the tennis department, its fee and its head is deleted.
2. Primary key {member_no, dept_name} (1 point). Dependencies (2 points; 1 point if one group is missing):
  - member_no → member_name, youth, parent_phone
  - dept_name → monthly_fee, head_no
  - head_no → head_name
  - {member_no, dept_name} → joined_on
3. **1NF** (1 point): the values are atomic, but member_name and monthly_fee depend on only part of the key (partial dependencies), so 2NF is violated.
4. 3NF schema (3 points: 1 per relation with correct keys):
  - MEMBER(**member_no**, member_name, youth, parent_phone)
  - DEPARTMENT(**dept_name**, monthly_fee, *head_no* → MEMBER)
  - MEMBERSHIP(**member_no, dept_name**, joined_on), *member_no* → MEMBER, *dept_name* → DEPARTMENT
  - head_name is **not** stored again: the head is a member, so the name is found in MEMBER (head_no → head_name is the same fact as member_no → member_name). A separate HEAD relation with head_name earns 2 of 3 points. Splitting youth members into YOUTH_MEMBER(**member_no**, parent_phone) as on worksheet 5 is also correct.

Common mistakes: joined_on placed in MEMBER (it belongs to the pair member and department); dept_name as key of MEMBERSHIP alone; monthly_fee kept in MEMBERSHIP.
:::

## References {.references}

- Codd, E. F. (1972). Further normalization of the data base relational model. In R. Rustin (Ed.), *Data base systems* (pp. 33–64). Prentice-Hall.
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Kent, W. (1983). A simple guide to five normal forms in relational database theory. *Communications of the ACM, 26*(2), 120–125. https://doi.org/10.1145/358024.358054
