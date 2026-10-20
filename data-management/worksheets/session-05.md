---
course: Data Management
session: 5
title: The Relational Model
subtitle: Practice tasks on relations, keys, integrity constraints and mapping ER models to relational schemas
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 5 on your own or with your project team. Use the notation from the slides: write relation names in capitals, the **primary key in bold** (on paper: underline it) and foreign keys in *italics* with an arrow to the referenced relation, e.g. BIKE(**frame_no**, brand, *customer_no* → CUSTOMER). Paper and pencil are enough. Tasks 5 and 6 continue the car-sharing and sports club cases from worksheet 4.

## Read a Relation

A training provider keeps its workshops in this table:

| workshop_no | title | trainer | workshop_date | fee |
|---|---|---|---|---|
| W-01 | Excel basics | Kaya | 2027-03-04 | 120 |
| W-02 | SQL for beginners | Novak | 2027-03-11 | 150 |
| W-03 | Data visualisation | Kaya, Brandt | 2027-03-18 | 180 |
| W-02 | SQL for beginners | Novak | 2027-03-11 | 150 |

1. What are the **degree** and the **cardinality** of the table as shown?
2. Suggest a sensible **domain** for *workshop_no*, *workshop_date* and *fee*.
3. The table breaks **two properties** of a relation. Name them, point to the affected rows or cells, and say how you would fix each problem.
4. A fellow student says: "The cardinality of WORKSHOP is 1:N." What is wrong with this sentence?

::: answer lines=10
:::

::: solution
1. Degree **5** (five attributes). Cardinality **4** rows as shown; as a correct relation (without the duplicate) it would be **3** tuples.
2. *workshop_no*: strings of the form "W-" followed by two digits. *workshop_date*: valid calendar dates (e.g. only dates in the training year). *fee*: non-negative amounts in euros with two decimals. Any precise, sensible definition gets full credit; "text" or "number" alone is too vague, because a domain also restricts the allowed values.
3. Two violations:
  - **No duplicate tuples:** row 4 repeats row 2. Fix: delete it and declare *workshop_no* as primary key so that the database rejects duplicates.
  - **Atomic values:** the trainer cell of W-03 holds two values ("Kaya, Brandt"). Fix: a separate relation WORKSHOP_TRAINER(**workshop_no, trainer**) with *workshop_no* → WORKSHOP; with a TRAINER relation, *trainer* becomes a foreign key as well (the M:N rule).
4. It confuses two meanings of "cardinality". The cardinality of a **relation** is its number of tuples (here 3 or 4). 1:N is the cardinality of a **relationship** in the ER model.
:::

## True or False: Keys

The relation CAR(licence_plate, vin, model, colour, owner_no) stores the cars of a fleet. Both the licence plate and the vehicle identification number (vin) are unique for every car. Decide whether each statement is **true or false** and give a one-line reason.

1. {licence_plate, colour} is a superkey.
2. {licence_plate, colour} is a candidate key.
3. CAR has two candidate keys.
4. In the current data, every model appears only once, so *model* is a candidate key.
5. *owner_no* is a foreign key, so its values must be unique in CAR.
6. Every relation has at least one superkey.
7. A primary key value may be NULL as long as it is not known yet.

Finally: which attribute would you choose as **primary key** of CAR, and why?

::: answer lines=10
:::

::: hint
A key is a rule about **all possible** states of the relation, not just about the rows that happen to be stored today.
:::

::: solution
1. **True:** it contains licence_plate, which alone is unique.
2. **False:** it is not minimal; colour can be removed without losing uniqueness.
3. **True:** {licence_plate} and {vin}.
4. **False:** sample data can disprove a key but never prove one. The business rule says that several cars can have the same model.
5. **False:** an owner can have several cars; a foreign key only has to match an existing primary key value (or be NULL).
6. **True:** the set of all attributes is always a superkey, because a relation has no duplicate tuples.
7. **False:** entity integrity forbids NULL in any part of the primary key.

Primary key: **vin**. It never changes during the life of the car, while a licence plate can change when the car is registered again (new owner, new district, personalised plate). *licence_plate* stays an alternate key with a uniqueness rule. Choosing licence_plate with a sound argument (shorter, used in every business process) earns partial credit only if the student mentions the stability problem.
:::

## Integrity Constraints in a Coworking Space

A coworking space uses three relations:

- PLAN(**plan_code**, monthly_fee)
- MEMBER(**member_no**, name, *plan_code* → PLAN) — *plan_code* may be NULL (members without a plan pay per day)
- BOOKING(**desk_no, booking_date**, *member_no* → MEMBER) — *member_no* is NOT NULL

Current data: PLAN contains (FLEX, 99) and (FIX, 249). MEMBER contains (M1, Jonas Weber, FLEX), (M2, Sara Öztürk, FIX) and (M3, Tim Lang, NULL). BOOKING contains (D4, 2027-05-03, M1) and (D7, 2027-05-03, M2).

For each operation, decide whether it is **accepted**. If not, name the **integrity constraint** it violates.

1. Insert member (M4, Eva Kim, PRO)
2. Insert booking (D4, 2027-05-03, M3)
3. Insert booking (NULL, 2027-05-04, M2)
4. Change the monthly fee of FLEX to "ninety-nine"
5. Insert member (M5, Ali Demir, NULL)
6. Delete member M1
7. Delete plan FLEX

For operations 6 and 7: which **referential action** (restrict, cascade, set NULL) would you define, and why?

::: answer lines=12
:::

::: solution
1. **Rejected:** referential integrity, plan PRO does not exist in PLAN.
2. **Rejected:** key constraint, desk D4 is already booked on 2027-05-03.
3. **Rejected:** entity integrity, *desk_no* is part of the primary key and must not be NULL.
4. **Rejected:** domain constraint, the fee must be a number.
5. **Accepted:** *plan_code* is allowed to be NULL.
6. Depends on the referential action, because booking (D4, 2027-05-03) refers to M1. Restrict: rejected. Cascade: the booking is deleted as well. Set NULL: not possible, because *member_no* in BOOKING is NOT NULL. Recommendation: **restrict**, because bookings are needed for invoicing; a leaving member is better marked as inactive than deleted. Cascade is acceptable if the student argues that only future bookings are stored.
7. M1 refers to FLEX. Recommendation: **restrict**, because the business must first move members to another plan. Set NULL is defensible (members become pay-per-day), but it silently changes their contract. **Cascade is wrong**: deleting a plan must never delete members.
:::

## Map the Basics: A Food Co-op

A food co-op has the following ER model. Map it to a relational schema. Mark all primary and foreign keys and say which foreign keys may be NULL.

- **Member** (member_no, name, address = street + postcode + city, several phone numbers, date of birth, age)
- **Farm** (farm_id, name, region)
- **Product** (product_no, name, unit). Each product comes from exactly one farm; a farm supplies one or more products (**supplies**, 1:N).
- Members **rate** products (M:N) with stars and a comment; each member rates a product at most once.
- A member can rent at most one **Locker** (locker_no, location); a locker is rented by at most one member; renting is optional on both sides (**rents**, 1:1).

::: answer lines=12
:::

::: hint
Check each attribute type from session 3: composite, multi-valued and derived attributes are mapped differently.
:::

::: solution
- MEMBER(**member_no**, name, street, postcode, city, date_of_birth). The composite address is split into its parts; *age* is **derived** and not stored.
- MEMBER_PHONE(**member_no, phone_no**), *member_no* → MEMBER. A multi-valued attribute becomes its own relation, and both attributes form the key.
- FARM(**farm_id**, name, region)
- PRODUCT(**product_no**, name, unit, *farm_id* → FARM). The foreign key goes on the N side and is **NOT NULL** (every product comes from exactly one farm).
- RATING(**member_no, product_no**, stars, comment), *member_no* → MEMBER, *product_no* → PRODUCT. The M:N relationship becomes its own relation; the composite key also enforces "at most one rating per member and product".
- LOCKER(**locker_no**, location, *member_no* → MEMBER), *member_no* **may be NULL** (free locker) and needs a **uniqueness rule** (one locker per member). Putting *locker_no* into MEMBER instead (nullable, unique) is equally correct, because participation is optional on both sides. Without the uniqueness rule the mapping only expresses 1:N, so the answer is incomplete.
:::

## Map Specialisation and Weak Entity Types: Car-Sharing

Take the car-sharing model from worksheet 4: superclass **Vehicle** (licence_plate, model, location, mileage); specialisation by drive type into **Electric vehicle** (battery_capacity, plug_type) and **Combustion vehicle** (fuel_type, tank_size), disjoint and total; a second, partial specialisation **Van** (load_volume); weak entity type **Charging session** (partial key start_time; end_time, kwh) owned by *Electric vehicle*.

1. Map the model with **option A** (superclass and subclasses).
2. Could you use **option B** (subclasses only) or **option C** (one relation) for the drive-type specialisation? And for *Van*? Explain.
3. What should happen to the charging sessions when an electric vehicle is deleted?
4. Is *licence_plate* a good primary key here? Use what you know about keys.

::: answer lines=14
:::

::: solution
1. Option A:
  - VEHICLE(**licence_plate**, model, location, mileage)
  - ELECTRIC_VEHICLE(**licence_plate**, battery_capacity, plug_type), *licence_plate* → VEHICLE
  - COMBUSTION_VEHICLE(**licence_plate**, fuel_type, tank_size), *licence_plate* → VEHICLE
  - VAN(**licence_plate**, load_volume), *licence_plate* → VEHICLE
  - CHARGING_SESSION(**licence_plate, start_time**, end_time, kwh), *licence_plate* → ELECTRIC_VEHICLE (not → VEHICLE: only electric vehicles can charge)
2. **Drive type:** option B would work for the drive type alone, because it is disjoint and total, but *Van* and every other relationship of *Vehicle* would then have to refer to two relations, so it is a poor choice. Option C works: VEHICLE gets *drive_type* and four nullable columns; that is acceptable with this few attributes, but the rule "only electric vehicles have a battery capacity" needs a CHECK constraint, and CHARGING_SESSION can no longer refer to electric vehicles only. **Van:** option B is impossible, because the specialisation is partial (vehicles that are not vans would be lost). Option C is the simplest solution: a nullable column *load_volume* in VEHICLE.
3. Charging sessions are a weak entity type and cannot exist without their owner, so **cascade** is the natural choice. A good answer adds that sessions are billing records; the business may need to keep them (then **restrict**, and mark vehicles as retired instead of deleting them).
4. Not ideal: licence plates can change (new registration), and the plate is part of the key of CHARGING_SESSION, so a change would have to be propagated. A stable natural key (vin) or a surrogate key (vehicle_id) is better; *licence_plate* stays as an alternate key with a uniqueness rule.
:::

## Exam-Style Task: Map the Sports Club

This task is in the style of an exam question. Map the following ER model (the solution of the exam-style task on worksheet 4) to a relational schema. Mark all primary and foreign keys and state which foreign keys may be NULL. Justify your choice for the specialisation in one sentence.

- **Member** (member_no, name, date_of_birth, joining_date); disjoint and total specialisation into **Adult member** (no own attributes) and **Youth member** (parent_phone)
- **Department** (name, monthly_fee); Member **is member of** Department, M:N, with attribute joined_on
- **Team**: weak entity type, owner *Department*, partial key team_no
- Member **coaches** Team, 1:N; every team has exactly one coach, a member coaches at most two teams
- Member **mentors** Member, recursive 1:N, roles *mentor* and *mentee*, optional on both sides

::: answer lines=14
:::

::: solution
Model answer:

- MEMBER(**member_no**, name, date_of_birth, joining_date, member_type, *mentor_no* → MEMBER), *mentor_no* may be NULL
- YOUTH_MEMBER(**member_no**, parent_phone), *member_no* → MEMBER
- DEPARTMENT(**dept_name**, monthly_fee)
- MEMBERSHIP(**member_no, dept_name**, joined_on), *member_no* → MEMBER, *dept_name* → DEPARTMENT
- TEAM(**dept_name, team_no**, *coach_no* → MEMBER), *dept_name* → DEPARTMENT, *coach_no* NOT NULL

Specialisation: *Adult member* has no own attributes, so a type column in MEMBER plus a relation for youth members (a mix of options A and C) is the leanest solution. Pure option C (*parent_phone* as a nullable column in MEMBER) or pure option A (ADULT_MEMBER and YOUTH_MEMBER relations) are also correct if justified.

Marking guide (10 points):

- MEMBER with primary key and all attributes: 1 point
- Recursive **mentors** as nullable foreign key *mentor_no* → MEMBER in MEMBER: 2 points (1 for the self-reference, 1 for nullable)
- Specialisation mapped consistently with a sensible justification: 2 points
- M:N **is member of** as own relation with composite primary key and *joined_on*: 2 points
- TEAM with composite primary key (*dept_name*, *team_no*) and *dept_name* as foreign key: 2 points
- **coaches** as *coach_no* in TEAM, NOT NULL; the limit "at most two teams" noted as a business rule that the schema cannot express (CHECK or application logic): 1 point

Common mistakes: foreign key for **coaches** put into MEMBER (that only allows one team per coach); TEAM with *team_no* alone as key (team 1 exists in every department); *joined_on* placed in MEMBER.
:::

## Reverse Mapping: A Dental Practice {.optional}

You find the following relational schema in a dental practice. Reconstruct the **ER model** (Chen notation): entity types, relationships with cardinalities and participation, and attributes. Which parts of the original ER model can you **not** reconstruct with certainty?

- INSURER(**insurer_id**, name)
- PATIENT(**patient_no**, name, date_of_birth, *insurer_id* → INSURER), *insurer_id* may be NULL
- PATIENT_ALLERGY(**patient_no, allergy**), *patient_no* → PATIENT
- DENTIST(**dentist_no**, name)
- APPOINTMENT(**appointment_no**, start_time, *patient_no* → PATIENT, *dentist_no* → DENTIST), both foreign keys NOT NULL
- TREATMENT(**code**, description, fee)
- PERFORMED(**appointment_no, code**, quantity), *appointment_no* → APPOINTMENT, *code* → TREATMENT

::: answer lines=10
:::

::: solution
- Entity types: *Insurer*, *Patient*, *Dentist*, *Appointment*, *Treatment*. *Appointment* is an entity type (not an M:N relationship between patient and dentist), because it has its own key.
- *Allergy* is a **multi-valued attribute** of *Patient* (PATIENT_ALLERGY has no attributes of its own).
- *Insurer* **insures** *Patient*: 1:N, optional for the patient (nullable foreign key); whether every insurer must have at least one patient cannot be seen.
- *Patient* **has** *Appointment*: 1:N, mandatory for the appointment. *Dentist* **treats in** *Appointment*: 1:N, mandatory for the appointment.
- *Appointment* **includes** *Treatment*: M:N with attribute *quantity*.
- Not reconstructable with certainty: the **minimum cardinalities on the 1 side** (must every patient have an appointment? must every treatment have been performed?), **relationship names**, and whether PERFORMED was an M:N relationship or a weak entity type in the original model. Derived attributes (e.g. age) that were not stored are lost as well.
:::

## References {.references}

- Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM, 13*(6), 377–387. https://doi.org/10.1145/362384.362685
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Gadatsch, A. (2019). *Datenmodellierung: Einführung in die Entity-Relationship-Modellierung und das Relationenmodell* (2nd ed.). Springer Vieweg. https://doi.org/10.1007/978-3-658-25730-9
