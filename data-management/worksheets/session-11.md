---
course: Data Management
session: 11
title: NoSQL Databases
subtitle: Practice tasks on CAP and BASE, the four NoSQL families, document design and JSON documents in SQLite
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 11 on your own or with your project team. Tasks 1 to 3 and the exam-style task can be done on paper; for tasks 4, 5 and the optional challenge you need Jupyter with Python's built-in `json` and `sqlite3` modules (SQLite 3.38 or newer for the JSON operators; check with `sqlite3.sqlite_version`). The lab tasks use the food co-op's order documents in [foodcoop-orders-session11.json](data/foodcoop-orders-session11.json); all names in the data are fictional. The in-class hands-on on the bike shop needs the four scripts [bikeshop-schema.sql](data/bikeshop-schema.sql), [bikeshop-data.sql](data/bikeshop-data.sql), [bikeshop-data-session09.sql](data/bikeshop-data-session09.sql) and [bikeshop-documents-session11.sql](data/bikeshop-documents-session11.sql). The terms follow the session slides, which are based on Sadalage and Fowler (2013), Elmasri and Navathe (2016, Chapter 24), Gilbert and Lynch (2002), Brewer (2012), Pritchett (2008), Vogels (2009) and the SQLite documentation (SQLite, n.d.).

```python
import json
import sqlite3

with open("foodcoop-orders-session11.json", encoding="utf-8") as f:
    orders = json.load(f)              # a list of dicts, one per order

con = sqlite3.connect(":memory:")
con.execute("PRAGMA foreign_keys = ON")
con.execute("""CREATE TABLE order_doc (
                   order_no INTEGER PRIMARY KEY,
                   doc      TEXT NOT NULL CHECK (json_valid(doc)))""")
with con:
    for o in orders:
        con.execute("INSERT INTO order_doc VALUES (?, ?)",
                    (o["order_no"], json.dumps(o, ensure_ascii=False)))

def run(sql, con=con):
    """Run one statement; show the rows, the changed rows or the error."""
    try:
        cur = con.execute(sql)
        rows = cur.fetchall()
        print(rows if cur.description else f"{cur.rowcount} row(s) changed")
    except sqlite3.Error as e:
        print(type(e).__name__, "-", e)
```

## True or False?

Decide whether each statement is **true** or **false**. Correct every false statement in one sentence.

1. The C in CAP means the same as the C in ACID.
2. During a network partition, a distributed system has to give up either consistency or availability.
3. A system that chooses availability during a partition may answer with outdated data.
4. "Eventually consistent" means that the replicas never agree.
5. Sharding stores copies of the same data on several servers so that the system survives the failure of one server.
6. A key-value store can efficiently find all values that contain a given word.
7. In a "schemaless" document store, the application code must know which fields a document has.
8. BASE stands for "basically available, soft state, eventually consistent".

::: answer lines=10
:::

::: solution
1. **False.** CAP consistency means that all replicas return the latest write; ACID consistency means that a transaction takes the database from one valid state (constraints, business rules) to another.
2. **True** (Gilbert & Lynch, 2002). Without a partition, a system can be both consistent and available (Brewer, 2012).
3. **True.** That is the AP choice: every request gets a response, possibly from a replica that has not seen the latest write.
4. **False.** If no new updates are made, all replicas eventually return the last written value (Vogels, 2009); they may differ only for a while.
5. **False.** That is **replication**. Sharding distributes **different** data to different servers (e.g. customers A–K and L–Z).
6. **False.** The store does not look inside the value; it can only get, put and delete by key. A content query would read every value.
7. **True.** The structure moves from the database into the code that reads the data (implicit schema; Sadalage & Fowler, 2013, Chapter 3).
8. **True** (Pritchett, 2008).

Marking: one point per statement; for false statements, the point requires a correct correction.
:::

## Which Data Store?

For each use case, choose the most suitable family — **key-value**, **document**, **column-family**, **graph** or **relational** — and give **two reasons**. Then name one thing that would be **harder** with your choice.

1. The coworking space records every opening of a door by its 2,000 badge readers, around the clock.
2. The sports club website keeps the login sessions of its members.
3. The food co-op publishes recipes: each has a title, a varying list of ingredients, optional photos, tags and comments.
4. The car-sharing company wants to detect fraud: customer accounts that share a payment card, a phone number or a device, possibly over several steps.
5. The coworking space writes monthly invoices and books the payments.
6. The sports club's league tables are calculated once a night and shown thousands of times a day.

::: hint
Ask for each case: how is the data read (by one key, as a whole object, as a time range, along relationships, with arbitrary questions)? And how bad is a wrong or missing answer?
:::

::: answer lines=14
:::

::: solution
Accept other choices with a sound argument; the reasons matter more than the label.

1. **Column-family** (or a time-series database): very high write volume, data naturally ordered by reader and time, sparse attributes per reader. Harder: ad-hoc questions across readers, joins with member data.
2. **Key-value**: access only by session ID, short-lived, simple and fast; easy to distribute. Harder: questions on the content ("all sessions of member M2").
3. **Document**: a recipe is one object read as a whole; fields vary from recipe to recipe; ingredients and comments are naturally nested. Harder: consistent ingredient names across recipes, queries such as "all recipes that use products of farm X" if farms are only copied in as text.
4. **Graph**: the question is a traversal over relationships of unknown depth (account – card – account – phone – account). Harder: bulk aggregation over all customers; in SQL each step would be one more self join.
5. **Relational**: money needs ACID transactions, integrity constraints and exact totals; the data volume is small. Harder: hardly anything relevant here.
6. **Key-value** (as a cache): key = league and season, value = the finished table; read-heavy, rebuilt nightly, a stale value for a few minutes is harmless. The source data (matches, results) stays relational. Harder: nothing beyond keeping the cache up to date.

Marking: one point per case for a suitable family with two reasons; the "harder" part is needed for the point in at least four of the six cases.
:::

## Embed or Reference: The Coworking Space

The coworking space from earlier worksheets wants a **member app**. Its main screen, "My bookings", shows the member's name and plan and the member's bookings with date, desk, room and hours. The relational data (extract):

::: columns
**member**

| member_no | name | plan_code |
|---|---|---|
| M1 | Jonas Weber | FLEX |
| M2 | Sara Öztürk | FIX |
| M3 | Tim Lang | NULL |

**desk**

| desk_no | room |
|---|---|
| D2 | Quiet room |
| D4 | Open space |
| D7 | Open space |
|||
**booking**

| booking_no | member_no | desk_no | booking_date | hours |
|---|---|---|---|---|
| 1 | M1 | D4 | 2027-05-03 | 8 |
| 2 | M2 | D7 | 2027-05-03 | 4 |
| 3 | M1 | D4 | 2027-05-04 | NULL |
| 4 | M3 | D2 | 2027-05-04 | 6 |
| 5 | M2 | D7 | 2027-05-05 | 4 |
| 6 | M1 | D2 | 2027-05-05 | NULL |
:::

1. Design a JSON document for the "My bookings" screen and write it out for member **M1**. Decide for each piece of data whether you **embed** or **reference** it, and justify one embed and one reference decision.
2. Desk D2 moves from the quiet room to the open space. How many of your documents change? How many rows change in the relational model?
3. The reception wants a second screen: "Who sits where **today**?" Is your document collection a good fit for this screen? What would you do instead?

::: hint
Embedding means: one read for the screen, but copies. Look at which data belongs to the member (and changes with the member) and which data is shared by many members.
:::

::: answer lines=16
:::

::: solution
1. One document per member, with the bookings embedded (they belong to the member and are read with them):

```json
{ "member_no": "M1", "name": "Jonas Weber", "plan": "FLEX",
  "bookings": [
    { "booking_no": 1, "date": "2027-05-03", "desk": "D4", "room": "Open space", "hours": 8 },
    { "booking_no": 3, "date": "2027-05-04", "desk": "D4", "room": "Open space", "hours": null },
    { "booking_no": 6, "date": "2027-05-05", "desk": "D2", "room": "Quiet room", "hours": null } ] }
```

Embed the bookings: 1:N, owned by the member, always shown with the member, one read for the screen. The **room** is a copy of desk data: either embed it (the screen needs it, one read; accept the redundancy) or **reference** the desk by `desk_no` only and look the room up in a small desk collection (desks are shared by all members and change on their own). Both are correct with this reasoning. The plan code can be embedded as a value; the monthly fee belongs to the plan and should be referenced. Open bookings get `"hours": null` or no `hours` field at all — either is acceptable if stated.

2. If the room is embedded: every member document with a booking on D2 changes — M1 (booking 6) and M3 (booking 4), so **2 documents** (and the app must find them all). Relational: **1 row** in `desk`. If the room is referenced: 0 member documents, 1 desk document. Whether old bookings should keep "Quiet room" (where the member actually sat) is a business question — a snapshot can be correct.

3. No: the screen needs all bookings of **one date** across all members, so it would read every member document and filter the embedded arrays. Options: a second collection organised by date (one document per day with the bookings, i.e. a different aggregate for a different access pattern), an index on the embedded booking dates if the store supports it, or simply keep this in the relational database, where `WHERE booking_date = …` with an index answers it directly.

Marking: part 1 three points (correct document for M1 including the NULL hours, one justified embed, one justified reference), part 2 one point, part 3 one point.
:::

## Lab: The Food Co-op's Order Documents

Run the set-up cell from the introduction. The file contains the co-op's orders as JSON documents. Each order embeds the member and the ordered items with the price at the time of the order.

1. In **Python**, without SQL: compute the total of order 2 from the list `orders`. Then try the same for order 6. What happens, and why?
2. With SQL on `order_doc`: all orders picked up in **Ladenburg**, with order number, member name and date.
3. Revenue **per farm** (price × quantity of all items), highest first. Then find the item that is not counted correctly, explain why, and correct the query.
4. Which members ordered **goat cheese**? Which orders have **no items**, and which orders have a **note**?
5. List the dates and prices of all **potato** items. Should the old orders be updated when the co-op changes the price of potatoes? Why or why not?

::: hint
`json_each(o.doc, '$.items')` turns the items array into rows; `i.value ->> 'quantity'` takes a field out of each item. A missing field gives NULL — and NULL in a multiplication gives NULL, which `sum()` ignores.
:::

::: answer lines=16
:::

::: solution
All statements were run with Python 3.13 and SQLite 3.45.1 on exactly this file; results as observed.

1. `o2 = next(o for o in orders if o["order_no"] == 2)`, `sum(i["price"] * i["quantity"] for i in o2["items"])` → 3 × 2.40 + 7.50 + 2 × 1.30 = **17.3** (round to two decimals; floating point). Order 6 raises **KeyError: 'quantity'**: its honey item has the field `"qty"` instead of `"quantity"`. Nobody stopped this document from being stored — there is no schema to check it.
2. `SELECT order_no, doc ->> '$.member.name', doc ->> '$.date' FROM order_doc WHERE doc ->> '$.pickup' = 'Ladenburg' ORDER BY order_no;` → 5 rows: 1 Jana Roth 2027-05-04, 3 Ute Brenner 2027-05-05, 4 Jana Roth 2027-05-11, 7 Lotte Hahn 2027-05-12, 8 Ute Brenner 2027-05-18.
3. `SELECT i.value ->> 'farm' AS farm, round(sum((i.value ->> 'price') * (i.value ->> 'quantity')), 2) AS revenue FROM order_doc AS o, json_each(o.doc, '$.items') AS i GROUP BY farm ORDER BY revenue DESC;` → Ziegenhof Odenwald 27.7, Obsthof Bergstraße 24.8, Hofgut Neckarblick 17.2, Imkerei Kraichgau **7.5**, Gärtnerei Sonnenfeld 1.5. Finding it: `… WHERE i.value ->> 'quantity' IS NULL` → order 6, Honey, `"qty": 2`. The product price × NULL is NULL and `sum()` silently ignores it — no error, just a wrong figure. Fix: `coalesce(i.value ->> 'quantity', i.value ->> 'qty')` → Imkerei Kraichgau **22.5** (the other farms unchanged; total 93.7). Better long-term: correct the document and validate documents before they are stored.
4. Goat cheese: `SELECT DISTINCT o.doc ->> '$.member.name' FROM order_doc o, json_each(o.doc, '$.items') i WHERE i.value ->> 'product' = 'Goat cheese';` → Jana Roth, Lotte Hahn. No items: `WHERE json_array_length(doc, '$.items') = 0` → order 5. Note: `WHERE doc ->> '$.note' IS NOT NULL` → order 3 ("Please pack without plastic") and order 5 ("Cancelled by member"). Different documents have different fields — and order 7's member even has a phone number that no other order has.
5. `SELECT o.doc ->> '$.date', i.value ->> 'price' FROM order_doc o, json_each(o.doc, '$.items') i WHERE i.value ->> 'product' = 'Potatoes' ORDER BY 1;` → 2027-05-04 2.8, 2027-05-11 2.6, 2027-05-12 2.6. **No**: the price in an order is what the member was charged at the time (a snapshot, like `price_charged` in the bike shop). Here the copy is intended; updating it would falsify the history. The current list price belongs in a product record of its own.

Marking: one point per question; for 3 the point requires the explanation of the NULL and a correct fix.
:::

## Back to Tables: Normalise the Order Documents

The co-op's treasurer wants proper reports and asks you to move the orders into a relational database.

1. Derive a relational schema in **3NF** from the documents (session 6): relations, primary keys and foreign keys. Where does the price go?
2. Create the tables in the same `:memory:` database and fill them from `order_doc` with `INSERT … SELECT` statements that use `->>` and `json_each`. What happens with the honey item of order 6, and what does this tell you about the two models?
3. Check the row counts and repeat the revenue per farm with a join. Then change Lotte Hahn's phone number in both models: how many rows, how many documents?

::: hint
`json_each` works in `INSERT … SELECT` as in a normal query. A member appears in several orders: `GROUP BY` or `DISTINCT` gives one row per member. Use `CHECK (quantity > 0)` and `NOT NULL` as in session 7.
:::

::: answer lines=16
:::

::: solution
All statements were run in SQLite 3.45.1 on the documents of the lab task; results as observed.

1. MEMBER(**member_no**, name, phone) · FARM(**name**) · PRODUCT(**name**, *farm* → FARM) · COOP_ORDER(**order_no**, order_date, *member_no* → MEMBER, pickup, paid, note) · ORDER_ITEM(***order_no*** → COOP_ORDER, ***product*** → PRODUCT, quantity, price_charged). The price **charged** depends on the order and the product, so it belongs in ORDER_ITEM (history); a current list price would be an attribute of PRODUCT, which the documents do not contain. Using surrogate keys (farm_id, product_no) as in worksheet 10 is also correct.
2. Example statements:
   - `INSERT INTO member (member_no, name, phone) SELECT doc ->> '$.member.member_no', doc ->> '$.member.name', max(doc ->> '$.member.phone') FROM order_doc GROUP BY doc ->> '$.member.member_no';` → 5 rows (max() picks the phone number where one exists)
   - `INSERT INTO farm (name) SELECT DISTINCT i.value ->> 'farm' FROM order_doc o, json_each(o.doc, '$.items') i;` → 5 rows; products in the same way → 10 rows
   - `INSERT INTO coop_order SELECT order_no, doc ->> '$.date', doc ->> '$.member.member_no', doc ->> '$.pickup', doc ->> '$.paid', doc ->> '$.note' FROM order_doc;` → 8 rows (JSON true/false arrive as 1/0)
   - `INSERT INTO order_item SELECT o.order_no, i.value ->> 'product', i.value ->> 'quantity', i.value ->> 'price' FROM order_doc o, json_each(o.doc, '$.items') i;` → **NOT NULL constraint failed: order_item.quantity**, and because the statement is atomic, no item is inserted at all.

   The relational schema **rejects** the faulty document that the document collection accepted. With `coalesce(i.value ->> 'quantity', i.value ->> 'qty')` → 15 rows. Data quality rules live in the schema here, in the application code in the document model.
3. Counts: member 5, farm 5, product 10, coop_order 8, order_item 15. `SELECT p.farm, round(sum(oi.quantity * oi.price_charged), 2) FROM order_item oi JOIN product p ON p.name = oi.product GROUP BY p.farm ORDER BY 2 DESC;` → the same figures as the corrected lab query (Ziegenhof Odenwald 27.7 … Gärtnerei Sonnenfeld 1.5). Phone number: `UPDATE member SET phone = … WHERE member_no = 'F05'` → **1 row**; in the documents, every order of Lotte Hahn would have to change (1 document here, but one per order as soon as she orders again) — and older orders without the phone number remain different.

Marking: part 1 two points (relations with keys, price in ORDER_ITEM), part 2 two points (working statements, explanation of the NOT NULL error), part 3 one point.
:::

## Exam-Style Task: Car-Sharing Goes Distributed

This task is in the style of an exam question. The car-sharing company from earlier worksheets (customers, vehicles, bookings) now runs its app on servers in **two data centres** that replicate their data. The relational data (extract):

::: columns
**customer**

| customer_no | name |
|---|---|
| 1 | Aylin Şahin |
| 2 | Moritz Lang |

**vehicle**

| licence_plate | model |
|---|---|
| MA-CS 101 | VW ID.3 |
| MA-CS 104 | Fiat 500e |
| MA-CS 107 | Renault Zoe |
|||
**booking**

| booking_no | customer_no | licence_plate | start_date | km |
|---|---|---|---|---|
| 2 | 1 | MA-CS 101 | 2027-02-03 | 12 |
| 3 | 2 | MA-CS 104 | 2027-02-10 | 48 |
| 4 | 1 | MA-CS 107 | 2027-02-14 | NULL |
| 6 | 1 | MA-CS 101 | 2027-03-02 | 23 |
:::

1. Explain the CAP theorem in your own words. Use a concrete situation in the car-sharing app in which the connection between the two data centres fails. (2 points)
2. For each operation, decide whether the company should prefer **consistency** or **availability** during a partition, and justify it with the business risk: (a) booking a car for a time slot, (b) the list "vehicles you recently looked at". (2 points)
3. The app's screen "My trips" shows a customer's trips with date, vehicle model and km. Design a **JSON document** for this screen and write it out for **Aylin Şahin**. (3 points)
4. The model name of MA-CS 101 was entered wrongly and must be corrected. Explain why this is more work with your documents than in the relational database. (1 point)
5. Choose a suitable NoSQL family for (a) the live GPS position of every car, sent every 5 seconds, and (b) the app's login sessions. Give one reason each. (2 points)

::: answer lines=24
:::

::: solution
The JSON document in part 3 was checked with Python's `json.loads`.

1. CAP: in a distributed system, a network **partition** (lost connection between servers) can always happen; while it lasts, the system can guarantee either **consistency** (every read sees the latest write, all replicas agree) or **availability** (every request to a working server gets an answer), not both (Gilbert & Lynch, 2002). Example: the link between the data centres fails; Aylin books MA-CS 101 for Saturday in data centre 1; Moritz asks data centre 2 for the same car and slot. Data centre 2 either refuses or delays the request (C) or answers from its own, outdated data and may accept a second booking (A).
2. (a) **Consistency**: a double booking means two customers at one car, an angry customer and possibly a taxi paid by the company; refusing a booking for a few minutes is the smaller damage. (b) **Availability**: an outdated or incomplete list is harmless; the app should never fail because of it.
3. One document per customer with the trips embedded:

```json
{ "customer_no": 1, "name": "Aylin Şahin",
  "trips": [
    { "booking_no": 2, "date": "2027-02-03", "licence_plate": "MA-CS 101", "model": "VW ID.3",     "km": 12 },
    { "booking_no": 4, "date": "2027-02-14", "licence_plate": "MA-CS 107", "model": "Renault Zoe", "km": null },
    { "booking_no": 6, "date": "2027-03-02", "licence_plate": "MA-CS 101", "model": "VW ID.3",     "km": 23 } ] }
```

4. The model name is **copied** into every trip with this vehicle, in every customer's document (here bookings 2 and 6 of Aylin, and any other customer who used MA-CS 101). The application must find and update all of them; forgetting one leaves contradictory data (update anomaly). In the relational model, it is one `UPDATE` of one row in `vehicle`.
5. (a) **Column-family** (or time-series) store: very high write volume, data ordered by car and time, read as time ranges. (b) **Key-value** store: access only by session key, short-lived, very fast reads and writes.

Marking guide (10 points):

- Part 1: 1 point for the three properties with the core statement (during a partition: C or A), 1 point for a fitting car-sharing example that shows both options.
- Part 2: 1 point each for a sensible choice with a business-risk justification. Choosing A for (a) is acceptable only with a convincing compensation process (e.g. "detect double bookings afterwards and offer a replacement car").
- Part 3: 1 point for a valid JSON structure (objects, array, quoted keys), 1 point for embedding the trips with the three bookings and the model names, 1 point for correct values including the missing km (`null` or field left out).
- Part 4: 1 point for "copies in many documents → all must be updated, risk of inconsistency" compared with one row.
- Part 5: 1 point each for family and reason.
- Common mistakes: confusing CAP consistency with ACID consistency; "a system must always give up one of the three"; trips stored as separate documents without the customer and without a reason; JSON with single quotes or a trailing comma.
:::

## Optional Challenge: From Tables to Documents {.optional}

Use the relational tables you filled in task 5. The co-op's member portal wants **one document per member** with the member number, the name and an array of their orders (order number, date and order total).

1. Write **one** `SELECT` that builds these documents with `json_object` and `json_group_array` (both are built into SQLite). Show the documents for members F02 and F04.
2. Member F04's only order is cancelled and has no items. What total does your query give, and is that what the portal should show?

::: hint
A correlated subquery in the select list can build the array of one member's orders; a second correlated subquery inside it computes each order's total. `total()` returns 0.0 instead of NULL for an order without items (session 10).
:::

::: answer lines=10
:::

::: solution
Run in SQLite 3.45.1 on the tables from task 5; output as observed.

1. 
```sql
SELECT json_object('member_no', m.member_no, 'name', m.name,
         'orders', (SELECT json_group_array(
                              json_object('order_no', o.order_no, 'date', o.order_date,
                                          'total', (SELECT round(total(quantity * price_charged), 2)
                                                    FROM order_item AS oi
                                                    WHERE oi.order_no = o.order_no))
                              ORDER BY o.order_no)
                     FROM coop_order AS o WHERE o.member_no = m.member_no))
FROM   member AS m
WHERE  m.member_no IN ('F02', 'F04')
ORDER  BY m.member_no;
```

→ `{"member_no":"F02","name":"Malik Osei","orders":[{"order_no":2,"date":"2027-05-04","total":17.3},{"order_no":6,"date":"2027-05-12","total":20.8}]}` and `{"member_no":"F04","name":"Kemal Aydın","orders":[{"order_no":5,"date":"2027-05-11","total":0.0}]}`. `ORDER BY` inside `json_group_array` needs SQLite 3.44 or newer; without it the order of the array is not guaranteed.

2. Total **0.0**. Technically correct (no items), but the portal should show the order as **cancelled** (from the note, or better from a status column such as `status = 'cancelled'` that the relational model should have instead of a free-text note). Leaving cancelled orders out of the array is also acceptable if stated.
:::

## References {.references}

- Brewer, E. (2012). CAP twelve years later: How the "rules" have changed. *Computer, 45*(2), 23–29. https://doi.org/10.1109/MC.2012.37
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Gilbert, S., & Lynch, N. (2002). Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services. *ACM SIGACT News, 33*(2), 51–59. https://doi.org/10.1145/564585.564601
- Pritchett, D. (2008). BASE: An ACID alternative. *ACM Queue, 6*(3), 48–55. https://doi.org/10.1145/1394127.1394128
- Sadalage, P. J., & Fowler, M. (2013). *NoSQL distilled: A brief guide to the emerging world of polyglot persistence*. Addison-Wesley.
- SQLite. (n.d.). *JSON functions and operators*. Retrieved October 21, 2026, from https://www.sqlite.org/json1.html
- Vogels, W. (2009). Eventually consistent. *Communications of the ACM, 52*(1), 40–44. https://doi.org/10.1145/1435417.1435432
