-- Velo Neckar bike shop: repair jobs as JSON documents (Data Management, session 11)
--
-- Builds a "document collection" next to the relational tables: one JSON document
-- per repair job, with the bike, its owner, the repair lines and the mechanics
-- embedded. The documents are made with SQLite's built-in JSON functions
-- (json_object, json_group_array; SQLite 3.38 or newer, ORDER BY inside an
-- aggregate needs SQLite 3.44 or newer). All names are fictional.
-- Run the three scripts of session 9 first, then this one:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql",
--                  "bikeshop-documents-session11.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- or with the SQLite command-line tool, in the same order.
-- Running this script again rebuilds the documents from the current tables.
-- Afterwards: repair_job_doc has 12 rows (one document per repair job).

DROP TABLE IF EXISTS repair_job_doc;

-- One row per document: the key and the document itself (JSON stored as text)
CREATE TABLE repair_job_doc (
    job_no  INTEGER PRIMARY KEY,
    doc     TEXT    NOT NULL CHECK (json_valid(doc))
);

INSERT INTO repair_job_doc (job_no, doc)
SELECT j.job_no,
       json_object(
           'job_no',      j.job_no,
           'date',        j.job_date,
           'description', j.description,
           'bike',        json_object(
                              'frame_no', b.frame_no,
                              'brand',    b.brand,
                              'model',    b.model,
                              'owner',    CASE WHEN c.customer_no IS NULL THEN NULL
                                               ELSE json_object('customer_no', c.customer_no,
                                                                'name',        c.name,
                                                                'city',        c.city)
                                          END),
           'lines',       (SELECT json_group_array(
                                      json_object('part_no',  l.part_no,
                                                  'part',     p.name,
                                                  'quantity', l.quantity,
                                                  'price',    l.price_charged)
                                      ORDER BY l.part_no)
                           FROM   repair_line AS l
                           JOIN   spare_part  AS p ON p.part_no = l.part_no
                           WHERE  l.job_no = j.job_no),
           'mechanics',   (SELECT json_group_array(e.name ORDER BY e.employee_no)
                           FROM   job_mechanic AS jm
                           JOIN   employee     AS e ON e.employee_no = jm.employee_no
                           WHERE  jm.job_no = j.job_no)
       )
FROM      repair_job AS j
JOIN      bike       AS b ON b.frame_no = j.frame_no
LEFT JOIN customer   AS c ON c.customer_no = b.customer_no
ORDER BY  j.job_no;
