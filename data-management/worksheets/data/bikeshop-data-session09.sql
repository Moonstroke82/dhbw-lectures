-- Velo Neckar bike shop: extra rows for session 9 (Data Management, joins)
--
-- Adds three rows to the sample data of session 8, so that the join examples
-- have a two-level supervisor hierarchy, a mechanic without repair jobs and
-- a spare part that has never been used. All names are fictional.
-- Run the three scripts in this order:
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- or with the SQLite command-line tool:
--   sqlite3 bikeshop.db < bikeshop-schema.sql
--   sqlite3 bikeshop.db < bikeshop-data.sql
--   sqlite3 bikeshop.db < bikeshop-data-session09.sql
--
-- Row counts afterwards: employee 8, mechanic 5, spare_part 12 (all other tables unchanged).

PRAGMA foreign_keys = ON;

-- A new apprentice, supervised by the journeyman Deniz Arslan (2), who is supervised by Katrin Vogel (1).
-- Tim has not been assigned to any repair job yet.
INSERT INTO employee (employee_no, name) VALUES
    (8, 'Tim Krause');

INSERT INTO mechanic (employee_no, qualification, supervisor_no) VALUES
    (8, 'apprentice', 2);

-- A spare part that is on the list but has not been used in any repair yet.
INSERT INTO spare_part (part_no, name, list_price) VALUES
    ('P-112', 'Mudguard set', 24.90);
