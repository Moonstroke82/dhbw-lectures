---
course: Data Management
session: 2
title: Data Types and Data Management Fundamentals
subtitle: Practice tasks on data, information and knowledge, types of data, metadata and the data lifecycle
program: DHBW · Digital Business Management (Business IT) · Semester 2
---

This worksheet lets you practise the concepts of session 2 on your own or in a study group. You need no software for the tasks; if you want to look at real files, open them in a text editor (not in Excel), so you can see their raw structure. Task 7 is in the style of an exam question.

## Data, Information, Knowledge, Wisdom

A warehouse manager collects the following statements. Assign each one to a level of the DIKW hierarchy (data, information, knowledge, wisdom; Ackoff, 1989; Rowley, 2007) and give a one-line reason.

1. "4,812"
2. "On 14 March, 4,812 parcels left warehouse North."
3. "If more than 4,500 parcels leave per day, the evening shift needs two extra packers; otherwise deliveries are late."
4. "We should hire seasonal packers from November, and train them in October, so that the Christmas peak does not damage our delivery promise."
5. "Parcels per day, warehouse North, March: 4,812; 4,390; 5,021; …"

::: answer lines=7
:::

::: solution
1. **Data:** a number without context; we do not know what it counts.
2. **Information:** the same number with meaning and context (what, where, when).
3. **Knowledge:** information combined with experience about cause and effect; it says *how* things work.
4. **Wisdom** (judgement): a decision about what to do and why, weighing goals and consequences.
5. **Information:** a series of values with context. Students who answer "data, because it is just a list of numbers" have missed that the label provides the context. Accept "data" only with the argument that it is raw input for further analysis.

Marking hint: the boundaries between the levels are fuzzy (Rowley, 2007). What matters is the argument with context, experience and judgement.
:::

## Classify the Datasets

For each dataset, decide whether it is **structured, semi-structured or unstructured**, justify briefly, and suggest where you would store it.

1. A GPX file (an XML format) with the route of a run recorded by a sports watch
2. Audio recordings of calls to a customer hotline
3. A budget plan in Excel with merged cells, colour coding and comments
4. Messages from temperature sensors in a cold-storage warehouse, sent as JSON
5. The product catalogue of an online shop in a relational database
6. Chat transcripts from customer support, with time stamp, agent ID and the text of each message
7. A Parquet file with all sales transactions of the last five years

::: answer lines=10
:::

::: hint
Ask: is there a schema? Is it defined **before** storing (structured), carried **in the data itself** (semi-structured), or missing (unstructured)? Many real datasets are mixed.
:::

::: solution
1. **Semi-structured:** XML tags describe the elements (track points with latitude, longitude, time); the number of points varies. Storage: file storage or data lake; the points can be loaded into a table for analysis.
2. **Unstructured:** audio has no data model a database can use directly; speech-to-text produces unstructured text. Metadata (date, duration, caller number) is structured. Storage: object storage or file system, metadata in a database.
3. **Structured in principle, but poorly structured:** cells form a grid, but merged cells, colours and comments carry meaning that no program can read reliably. A good answer notes that it has to be cleaned before it can be loaded into a database.
4. **Semi-structured:** self-describing keys, the structure can vary between sensor types. Storage: document database, time-series database or data lake; often flattened into a table.
5. **Structured:** fixed schema defined in advance. Storage: where it is, a relational database.
6. **Mixed:** time stamp and agent ID are structured, the message text is unstructured. Storage: a table with a text column, or a document database; text analysis needs NLP.
7. **Structured:** columnar format with a defined schema (McKinney, 2022). Storage: data lake or data warehouse.
:::

## Recognise the Format

Look at the four snippets. For each, name the **format**, the **type of data**, and the **number of records** it contains. Which snippets are **self-describing**, and why?

```text
A)  order_id;customer;amount
    4711;C-102;249.90
    4712;C-215;35.00

B)  {"order_id": 4713, "customer": "C-102",
     "items": [{"sku": "B-2", "qty": 1}, {"sku": "A-7", "qty": 3}]}

C)  <invoice number="R-2027-118">
      <buyer>C-215</buyer>
      <total currency="EUR">35.00</total>
    </invoice>

D)  192.0.2.17 - - [14/Mar/2027:10:02:31 +0100] "GET /cart HTTP/1.1" 200 5123
```

::: answer lines=8
:::

::: solution
- **A) CSV** (semicolon as separator), **structured**, 2 records (the first line is the header). Not self-describing in the strict sense: the header names the columns, but types and meaning are not part of the file.
- **B) JSON**, **semi-structured**, 1 record with a nested list of 2 items. **Self-describing:** every value carries its key.
- **C) XML**, **semi-structured**, 1 record (an invoice). **Self-describing:** tags and attributes name the elements (e.g. *currency*).
- **D) Web server log line**, **semi-structured**: a fixed pattern (IP address, time stamp, request, status code, size), but no names for the fields; 1 record. Not self-describing; you need to know the log format to read it.

Self-describing data (B, C) is typical of semi-structured data (Abiteboul, 1997): the structure travels with the data.
:::

## One Booking, Three Forms

A train booking arrives from a web API as JSON:

```json
{"booking_no": "BK-5521",
 "date": "2027-06-02",
 "route": {"from": "Mannheim Hbf", "to": "Berlin Hbf"},
 "passengers": [{"name": "Lena Vogt", "bahncard": 25},
                {"name": "Ole Vogt", "bahncard": null}]}
```

1. Why can this booking not be stored as **one row** of a single table with fixed columns?
2. Propose **two tables** (column names only) that hold the same information without losing anything.
3. Write the same booking as an **unstructured** e-mail (one or two sentences). What would a program have to do to get the passenger names out of the e-mail?

::: answer lines=10
:::

::: solution
1. The number of passengers varies (here 2, next time 1 or 5). A table with fixed columns would need columns like passenger_1, passenger_2 …, which wastes space or runs out. Also, *route* is nested and *bahncard* can be missing (null).
2. BOOKING(booking_no, booking_date, from_station, to_station) and PASSENGER(booking_no, passenger_name, bahncard). *booking_no* in PASSENGER links each passenger to the booking (the relational solution follows in sessions 3–5).
3. Example: "Hi, please book Mannheim to Berlin on 2 June for me (BahnCard 25) and my brother Ole, who has no BahnCard. Thanks, Lena Vogt". A program would need text analysis (NLP) to recognise names, stations, dates and BahnCard types, to resolve "me" and "my brother" (Ole **Vogt**?) and to deal with missing or ambiguous information. The structured information is still there, but implicit.
:::

## Metadata of an Open Dataset

A city publishes a dataset with hourly counts from its **bicycle counting stations**. Assign each metadata item to **business**, **technical** or **operational** metadata.

1. "count = number of bicycles passing in both directions within one hour"
2. Column *count* has the data type INTEGER
3. Last update: 2 April 2027, 03:00; 24 rows rejected because of sensor errors
4. Responsible: city traffic department
5. File format CSV, UTF-8, semicolon as separator
6. Licence: Data licence Germany – attribution – version 2.0
7. The data comes from induction loops, is aggregated per hour and then exported to the open data portal

You want to use the dataset to argue for a new cycle lane. Which **two** metadata items are most important before you trust the data, and why?

::: answer lines=10
:::

::: solution
1. **Business:** meaning and definition.
2. **Technical:** structure and data type.
3. **Operational:** processing information (load time, rejected rows).
4. **Business:** owner and responsibility.
5. **Technical:** format and encoding.
6. **Business** (rules of use). Some frameworks treat licences as governance metadata; accept with justification.
7. **Technical:** lineage (where the data comes from and how it is processed). Also accept "operational" if the student focuses on the processing steps.

Most important items (any two with a good reason): **1**, because "both directions" and "per hour" change how the numbers must be read; **3**, because rejected rows and gaps can distort totals; **7**, because induction loops may not detect all bikes (e.g. carbon frames), which is a limitation for the argument. **6** matters if the result is published.
:::

## Lifecycle of Loyalty Programme Data

A drugstore chain runs a loyalty app: customers collect points, and the chain uses the purchase data for personalised coupons. For each **stage of the data lifecycle** (plan · create or acquire · store and maintain · use and share · archive and delete), describe one **activity** and one **risk** in this case.

::: answer lines=12
:::

::: solution
Example answer (one activity and one risk per stage):

- **Plan:** define which data is needed for points and coupons, and for what purpose. Risk: collecting "everything, just in case" without a clear purpose (problem under the GDPR principle of purpose limitation, session 19).
- **Create or acquire:** registration in the app, purchases scanned at the till. Risk: typing errors in e-mail addresses, the same customer registered twice.
- **Store and maintain:** customer and purchase data in a database, backups, quality checks. Risk: data from the app and from the tills does not match (different customer numbers).
- **Use and share:** coupon selection, reports, sharing with a marketing agency. Risk: sharing without a legal basis, or coupons that reveal sensitive information (e.g. pregnancy-related products).
- **Archive and delete:** delete inactive accounts after a defined period, keep only what accounting law requires. Risk: data is never deleted because nobody is responsible.

Marking hint: the risks must fit the stage. Deletion is the stage most often forgotten (DAMA International, 2017).
:::

## Exam-Style Task: Types of Data

This task is in the style of an exam question.

1. Explain the difference between **structured** and **semi-structured** data. Give one business example for each.
2. A company records its online team meetings. For each meeting, the system stores the **video file**, an **automatic transcript** and a **record** with date, duration and participant list. Classify each of the three parts and explain why the meeting as a whole is a typical example of **mixed** data.

::: answer lines=14
:::

::: solution
Model answer:

1. **Structured data** follows a fixed schema that is defined before the data is stored: rows and columns with defined data types, e.g. the customer table in an ERP system. **Semi-structured data** is self-describing: tags or keys mark the elements, but the structure is flexible and can vary from record to record, e.g. JSON from a web API or an XML e-invoice (Abiteboul, 1997; Gandomi & Haider, 2015).
2. Video file: **unstructured** (no data model a database can use). Transcript: **unstructured** text (sentences have a structure, but there is no schema). Record with date, duration and participants: **structured**, or semi-structured if stored as JSON with a variable participant list. The meeting is "mixed" because one business object combines parts of different types: the structured metadata makes the unstructured parts findable and manageable, and each part needs different storage and analysis methods.

Marking guide (8 points):

- Definition of structured data (fixed schema, defined in advance): 1.5 points; example: 0.5 points
- Definition of semi-structured data (self-describing, flexible structure): 1.5 points; example: 0.5 points
- Correct classification of the three parts, 1 point each: 3 points
- Explanation of "mixed" with reference to metadata or different processing: 1 point
:::

## References {.references}

- Abiteboul, S. (1997). Querying semi-structured data. In F. Afrati & P. Kolaitis (Eds.), *Database Theory — ICDT '97* (Lecture Notes in Computer Science, Vol. 1186, pp. 1–18). Springer.
- Ackoff, R. L. (1989). From data to wisdom. *Journal of Applied Systems Analysis, 16*, 3–9.
- DAMA International. (2017). *DAMA-DMBOK: Data management body of knowledge* (2nd ed.). Technics Publications.
- Gandomi, A., & Haider, M. (2015). Beyond the hype: Big data concepts, methods, and analytics. *International Journal of Information Management, 35*(2), 137–144. https://doi.org/10.1016/j.ijinfomgt.2014.10.007
- McKinney, W. (2022). *Python for data analysis: Data wrangling with pandas, NumPy, and Jupyter* (3rd ed.). O'Reilly Media.
- Rowley, J. (2007). The wisdom hierarchy: Representations of the DIKW hierarchy. *Journal of Information Science, 33*(2), 163–180. https://doi.org/10.1177/0165551506070706
