---
course: Data Management
session: 3
title: Semantic Data Modelling I: The ER Model
subtitle: Practice tasks on entity types, attributes, keys, relationships, cardinalities and notations
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 3 on your own or in a study group. Use **Chen notation** unless a task says otherwise, and the **(min, max) notation** as defined in session 3: the pair is written next to the entity type it describes. Paper and pencil are enough; if you prefer a tool, draw.io (diagrams.net) has shapes for both notations. Task 6 is in the style of an exam question.

## Entity Types and Kinds of Attributes

A fitness studio wants to store data about its **members**. Classify each attribute as **key**, **simple**, **composite**, **multi-valued** or **derived** (more than one label can apply), and give a one-line reason.

1. membership_no
2. full name (first name and last name)
3. date of birth
4. age
5. address
6. phone numbers
7. booked training goals (e.g. "strength", "endurance")
8. number of visits this month

Then explain the difference between the **entity** "Anna Berger, membership 20431" and the **entity type** *Member*.

::: answer lines=10
:::

::: solution
1. **Key:** unique for each member, assigned by the studio, stable.
2. **Composite:** first name + last name.
3. **Simple:** one value, not split further.
4. **Derived:** calculated from date of birth; should not be stored.
5. **Composite:** street, postcode, city.
6. **Multi-valued:** a member can have several phone numbers.
7. **Multi-valued:** several goals per member. If goals have their own attributes (e.g. a trainer, a target date), they become an entity type (rule of thumb based on Staud, 2005).
8. **Derived:** counted from stored check-ins.

An **entity** is one distinguishable thing of the real world (this one member). The **entity type** is the set of all entities with the same properties, drawn as a rectangle (Chen, 1976; Elmasri & Navathe, 2016).
:::

## Good Key or Poor Key?

Judge each proposed key with the three criteria from session 3: **unique, stable, never empty**. If it is a poor key, suggest a better one.

1. E-mail address for *Employee*
2. Matriculation number for *Student*
3. Flight number (e.g. LH 400) for *Flight*
4. Product name for *Product*
5. Name + date of birth for *Hotel guest*
6. IMEI (device number) for *Company smartphone*

::: answer lines=9
:::

::: solution
1. **Poor:** e-mail addresses change (name change, new domain) and may be missing for employees without a computer workplace. Better: employee number.
2. **Good:** unique and stable for the whole study period, assigned when the student enrols.
3. **Poor on its own:** the same flight number is used every day. Better: flight number + date (a key made of several attributes).
4. **Poor:** names change (rebranding) and can repeat (same name in different sizes). Better: article number or EAN/GTIN.
5. **Poor:** two guests can share both values, and guests do not always give their date of birth (empty). Better: guest number.
6. **Good:** unique per device, never changes, always present. (If a device is replaced, it is a new entity anyway.)
:::

## Ask from Both Sides

For each pair, write the **two questions** you ask, the **cardinality** (1:1, 1:N or M:N) and the **(min, max)** pair on each side. State any business rule you assume.

1. Library member — **currently borrows** — book copy
2. Country — **has capital** — city
3. Doctor — **treats** — patient
4. Building — **contains** — flat
5. Author — **writes** — book

::: answer lines=12
:::

::: hint
Example for customer — places — order: "How many orders can one customer place?" (0 to N) and "By how many customers is one order placed?" (exactly 1). Result: 1:N, Customer (0, N), Order (1, 1).
:::

::: solution
1. "How many copies can one member borrow at the moment?" 0 to N. "By how many members can one copy be borrowed at the moment?" 0 or 1. **1:N**, Member (0, N), Copy (0, 1). (If borrowing history is stored, it becomes M:N; this is why the relationship says *currently*.)
2. "How many capitals does a country have?" Usually exactly 1. "Of how many countries is a city the capital?" 0 or 1. **1:1**, Country (1, 1), City (0, 1). Business rule: countries with several capitals (e.g. South Africa) are ignored or would make it 1:N.
3. "How many patients does a doctor treat?" 0 to N. "By how many doctors is a patient treated?" 1 to N (in the practice's view a patient has at least one treating doctor). **M:N**, Doctor (0, N), Patient (1, N). Accept (0, N) for the patient with a reason.
4. "How many flats does a building contain?" 1 to N (0 if the database also stores office buildings). "In how many buildings is a flat?" exactly 1. **1:N**, Building (1, N), Flat (1, 1).
5. "How many books does an author write?" 1 to N (0 if authors are registered before their first book). "How many authors does a book have?" 1 to N. **M:N**, Author (1, N), Book (1, N).

Marking hint: both questions must be asked; reading the cardinality from one side only is the most frequent mistake. Other minimum values are correct if the stated business rule supports them.
:::

## Translate Between Notations

Each line gives a relationship in **(min, max) notation**. For each one, write (a) the Chen cardinality labels (1, N, M) and where they go, and (b) the crow's-foot symbol at **each end** of the line (exactly one, zero or one, one or many, zero or many).

1. Department (1, N) — **employs** — Employee (1, 1)
2. Person (0, 1) — **holds** — Passport (1, 1)
3. Student (0, N) — **attends** — Course (0, N)

::: answer lines=9
:::

::: hint
In crow's-foot notation, the symbol next to an entity type answers the question asked **from the other side**: "one customer places zero or many orders" is drawn at the *Order* end.
:::

::: solution
1. (a) **1** at the *Department* side, **N** at the *Employee* side (1:N). (b) At the *Employee* end: **one or many** (a department employs 1 to N employees). At the *Department* end: **exactly one** (an employee is employed by exactly one department).
2. (a) **1** at both sides (1:1). (b) At the *Passport* end: **zero or one** (a person holds 0 or 1 passport). At the *Person* end: **exactly one** (every passport belongs to exactly one person).
3. (a) **M** and **N** (M:N). (b) **Zero or many** at both ends (a student attends 0 to N courses; a course is attended by 0 to N students).

Marking hint: the typical error is swapping the ends, because (min, max) is written next to the entity type it describes, while the crow's-foot symbol sits next to the entity type that is counted.
:::

## Model a Veterinary Practice

Draw an ER model in **Chen notation** with attributes, keys, cardinalities and participation.

- **Owners** are registered with owner number, name, address and one or more phone numbers.
- Each **pet** has a microchip number, name, species and date of birth. Every pet belongs to exactly one owner; every registered owner has at least one pet.
- **Vets** have a staff number, name and specialisation.
- A **treatment** has a number, a date and a diagnosis. It concerns exactly one pet and is carried out by exactly one vet.
- In a treatment, **medications** (code, name, unit price) can be prescribed, each with a dosage and a quantity.

::: answer lines=14
:::

::: solution
- Entity types: *Owner* (**owner_no**, name, address as composite attribute, phone as multi-valued attribute), *Pet* (**chip_no**, name, species, date_of_birth), *Vet* (**staff_no**, name, specialisation), *Treatment* (**treatment_no**, treatment_date, diagnosis), *Medication* (**med_code**, name, unit_price).
- *Owner* **owns** *Pet*: **1:N**, Owner (1, N), Pet (1, 1).
- *Pet* **receives** *Treatment*: **1:N**, Pet (0, N), Treatment (1, 1).
- *Vet* **carries out** *Treatment*: **1:N**, Vet (0, N), Treatment (1, 1).
- *Treatment* **prescribes** *Medication*: **M:N** with relationship attributes **dosage** and **quantity**, Treatment (0, N), Medication (0, N).

Marking hints: dosage and quantity must be attributes of the relationship, not of *Medication* (they depend on the pair). Age of the pet must not be stored. Modelling *Treatment* as a relationship between *Pet* and *Vet* is a defensible variant only if the student notices that it then cannot be linked to medications in plain Chen notation; the entity type is the better solution.
:::

## Exam-Style Task: Conference Organiser

This task is in the style of an exam question. A company organises a one-day IT conference. Draw an ER model in **Chen notation** with keys, cardinalities and participation in (min, max) notation.

- **Participants** have a participant number, name, e-mail address and company.
- Each participant buys exactly one **ticket type** (code, name, price); a ticket type can be bought by many participants.
- **Talks** have a talk number, title and duration. Each talk is given by one or more participants as **speakers**; a participant can give several talks or none.
- Each talk takes place in exactly one **room** (room name, capacity) at a start time; a room hosts several talks during the day.
- Participants **register** for talks; for each registration the time of registration is stored.

::: answer lines=14
:::

::: solution
Model answer:

- Entity types: *Participant* (**participant_no**, name, e_mail, company), *TicketType* (**code**, name, price), *Talk* (**talk_no**, title, duration), *Room* (**room_name**, capacity).
- *Participant* **buys** *TicketType*: 1:N, Participant (1, 1), TicketType (0, N).
- *Participant* **gives** *Talk*: M:N, Participant (0, N), Talk (1, N).
- *Talk* **takes place in** *Room*: 1:N, Talk (1, 1), Room (0, N). The start time is an attribute of *Talk* (or of the relationship; both are correct for a 1:N relationship, because each talk takes place only once).
- *Participant* **registers for** *Talk*: M:N with attribute **registered_at**, Participant (0, N), Talk (0, N).

Marking guide (10 points):

- Four entity types with sensible key attributes: 2 points
- **buys** with correct cardinality and participation: 1 point
- **gives** as M:N, with total participation of *Talk*: 2 points
- **takes place in** with correct cardinality and a sensible place for the start time: 2 points
- **registers for** as M:N with relationship attribute *registered_at*: 2 points
- Correct Chen notation (rectangles, diamonds, ellipses, underlined keys): 1 point

Common mistakes: two relationships between *Participant* and *Talk* merged into one (giving and attending are different facts); *registered_at* placed in *Participant*; *Speaker* as an entity type without saying how it relates to *Participant* (accept a separate entity type only if the student explains that speakers are not registered as participants).
:::

## Redraw in Crow's-Foot Notation {.optional}

Redraw your model of the veterinary practice (task 5) in **crow's-foot notation**, with the attributes inside the boxes. What becomes harder to see, compared with Chen notation?

::: answer lines=8
:::

::: solution
- Boxes *Owner*, *Pet*, *Vet*, *Treatment*, *Medication* with their attributes listed inside; key attributes marked (e.g. PK).
- *Owner*–*Pet*: exactly one at the *Owner* end, one or many at the *Pet* end. *Pet*–*Treatment*: exactly one at the *Pet* end, zero or many at the *Treatment* end. *Vet*–*Treatment*: exactly one at the *Vet* end, zero or many at the *Treatment* end. *Treatment*–*Medication*: zero or many at both ends.
- Harder to see: the **attributes of the M:N relationship** (dosage, quantity) have no natural place, because crow's-foot lines carry only a name (Chen vs. crow's-foot comparison, session 3). Many tools solve this by drawing an extra box *Prescription* between the two; that is already a step towards tables (session 5). Multi-valued and composite attributes are also less visible in a flat attribute list.
:::

## References {.references}

- Chen, P. P.-S. (1976). The entity-relationship model—Toward a unified view of data. *ACM Transactions on Database Systems, 1*(1), 9–36. https://doi.org/10.1145/320434.320440
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Staud, J. L. (2005). *Datenmodellierung und Datenbankentwurf: Ein Vergleich aktueller Methoden*. Springer. https://doi.org/10.1007/b137949
