---
course: Data Management
session: 4
title: Semantic Data Modelling II
subtitle: Practice tasks on weak entity types, M:N and recursive relationships, specialisation and modelling pitfalls
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 4 on your own or with your project team. Use Chen notation (Chen, 1976) unless a task says otherwise; the terms follow the session slides (based on Elmasri & Navathe, 2016; Staud, 2005). Paper and pencil are enough; if you prefer a tool, draw.io (diagrams.net) has shapes for both Chen and crow's-foot notation.

## Weak or Strong?

Decide for each entity type whether it should be modelled as **weak** or **strong**. For weak entity types, name the owner and the partial key.

| Entity type | Weak or strong? | Owner | Partial key |
|---|---|---|---|
| A room in a hotel | | | |
| A hotel guest | | | |
| A floor in a building | | | |
| A season of a TV series | | | |
| An episode of a TV series | | | |
| A bank account | | | |

::: hint
Ask two questions: does the thing make sense without its owner, and does the business give it a number of its own that is unique on its own?
:::

::: solution
- Room: **weak**, owner hotel, partial key room number (room 101 exists in many hotels).
- Guest: **strong**, guests have a customer or guest number.
- Floor: **weak**, owner building, partial key floor number.
- Season: **weak**, owner TV series, partial key season number.
- Episode: **weak**, owner season (and through it the series), partial key episode number. A chain of weak entity types is allowed.
- Bank account: **strong**, identified by the IBAN. In a model of one bank it could also be seen as weak with owner branch and partial key account number, which is how account numbers worked before the IBAN; accept that answer with this reasoning.
:::

## Where Does the Attribute Go?

A language school offers courses. Students enrol in courses; each course is taught by one teacher. For each attribute, say whether it belongs to *Student*, *Course*, *Teacher* or to the relationship **enrols in**, and give a one-line reason.

1. Date of birth
2. Course fee (list price)
3. Fee the student actually paid (after discounts)
4. Final grade
5. Maximum number of participants
6. Date of enrolment

::: answer lines=6
:::

::: solution
1. *Student*: a property of the person alone.
2. *Course*: the list price is the same for every participant.
3. **enrols in**: it depends on the pair (student, course); discounts differ per student. This is also pitfall 2 (missing history): the paid amount must not change when the list price changes.
4. **enrols in**: a grade is given to one student in one course.
5. *Course*: a property of the course offering.
6. **enrols in**: each enrolment has its own date.
:::

## Recursive Relationships

Model each situation as a recursive relationship in Chen notation. Give **role names** and **cardinalities**, and write one sentence that reads the relationship using the roles.

1. A course at the university may require other courses as prerequisites.
2. In a football league, teams play matches against each other.
3. A person can be married to at most one other person at a time.

::: answer lines=8
:::

::: solution
1. *Course* **requires** *Course*, M:N, roles *course* and *prerequisite*: "a course in the role *course* requires N courses in the role *prerequisite*, and a course can be a prerequisite for M courses."
2. *Team* **plays against** *Team* with roles *home team* and *away team*, M:N. Because a match has its own attributes (date, score) and the same two teams meet twice per season, a better model is an entity type *Match* with two 1:N relationships to *Team* (home and away). Students who notice this have understood pitfall 1 (attribute or entity).
3. *Person* **is married to** *Person*, 1:1, roles *spouse* and *spouse*, partial on both sides. If marriages over time should be stored (history), it becomes M:N with attributes *from* and *to*, or an entity type *Marriage*.
:::

## Specialisation in a Car-Sharing Business

A car-sharing company manages **vehicles**. All vehicles have a licence plate, a model, a location and a mileage. **Electric cars** additionally have a battery capacity and a charging plug type; **combustion cars** have a fuel type and a tank size. The company also offers **vans**, which can be electric or combustion and have a load volume.

1. Draw the specialisation hierarchy with the superclass and all subclasses and their own attributes.
2. Decide on the constraints (disjoint or overlapping, total or partial) for each specialisation and justify them.
3. Only electric cars are linked to **charging sessions** (start, end, kWh). Add this relationship. Why does it belong to the subclass and not to *Vehicle*?

::: hint
"Electric or combustion" and "van or not" are two different criteria. A superclass can have more than one specialisation.
:::

::: answer lines=10
:::

::: solution
1. Superclass *Vehicle* (licence_plate as key, model, location, mileage). Specialisation 1 by drive type: *Electric vehicle* (battery_capacity, plug_type) and *Combustion vehicle* (fuel_type, tank_size). Specialisation 2 by body type: *Van* (load_volume). A van is then an electric or a combustion vehicle **and** a van.
2. Drive type: **disjoint** and **total** (every vehicle has exactly one drive type; hybrids would make it overlapping, so a good answer asks the business). Van: a single subclass, **partial** (most vehicles are not vans). Modelling *Car* and *Van* as a disjoint, total body-type specialisation is also correct if *Car* gets own attributes.
3. *Electric vehicle* **has** *Charging session* (1:N); charging session can be a weak entity type with partial key start time. It belongs to the subclass because combustion cars never take part in it; attaching it to *Vehicle* would allow charging sessions for diesel cars and hide a business rule.
:::

## Find the Pitfalls

A student modelled an online bookshop as follows. Find **at least four** problems, name the pitfall, and propose a fix.

- Entity type *Customer* with attributes: customer_no, name, street, city, **age**, **number_of_orders**
- Entity type *Order* with attributes: order_no, date, **book_title**, **book_price**, quantity
- Entity type *Book* with attributes: ISBN, title, current_price, **publisher_name**, **publisher_address**
- Relationship *Customer* **has** *Order*
- Relationship *Customer* **visits** *Website*

::: answer lines=10
:::

::: solution
- *age* and *number_of_orders*: **derived data stored**. Store date_of_birth; count orders with a query.
- *book_title* and *book_price* in *Order*, and only one book per order: wrong structure. An order has several lines, so introduce a weak entity type *Order line* (owner *Order*, partial key line_no) with quantity and **price_paid** (history, pitfall 2), related to *Book*.
- *publisher_name* and *publisher_address*: **attribute or entity**. A publisher publishes many books and has its own attributes, so it becomes an entity type *Publisher* with a 1:N relationship to *Book*.
- **has**: **unclear meaning**. Better *places*, with cardinality 1:N.
- **visits** *Website*: **process, not data**. A website visit is an event; unless the shop wants to store visits (then: entity type *Session* or *Visit* with timestamps), drop it.
- Optional finding: address as a single entity type for customers with several delivery addresses.
:::

## Exam-Style Task: Sports Club {.optional}

A sports club wants a database. Model the following in Chen notation, including keys, cardinalities and participation. This task is in the style of an exam question.

- **Members** have a member number, name, date of birth and joining date. Members are either **adult** or **youth** members; for youth members, a parent's phone number is stored.
- The club has **departments** (football, tennis, …) with a name and a monthly fee. Members can join several departments; the date of joining a department is stored.
- Each department has **teams**, numbered within the department (e.g. football team 1, 2, 3).
- Each team has exactly one member as **coach**; a member can coach at most two teams.
- Some members act as **mentors** for new members.

::: answer lines=14
:::

::: solution
Marking guide (10 points):

- *Member* (member_no, name, date_of_birth, joining_date) as superclass; subclasses *Adult* and *Youth* (parent_phone), **disjoint and total**: 2 points
- *Department* (name as key, monthly_fee); M:N **is member of** with attribute *joined_on*: 2 points
- *Team* as **weak entity type**, owner *Department*, partial key team_no; identifying relationship 1:N with total participation of *Team*: 2 points
- **coaches** between *Member* and *Team*, 1:N (a member coaches 0 to 2 teams; each team has exactly 1 coach, total participation of *Team*). The upper limit of 2 cannot be expressed in plain Chen notation; note it as a business rule or use (min,max) notation (0,2) and (1,1): 2 points
- Recursive **mentors** on *Member*, 1:N with roles *mentor* and *mentee*, partial on both sides: 1 point
- Readable naming and correct notation overall: 1 point
:::

## References {.references}

- Chen, P. P.-S. (1976). The entity-relationship model—Toward a unified view of data. *ACM Transactions on Database Systems, 1*(1), 9–36. https://doi.org/10.1145/320434.320440
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Staud, J. L. (2005). *Datenmodellierung und Datenbankentwurf: Ein Vergleich aktueller Methoden*. Springer. https://doi.org/10.1007/b137949
