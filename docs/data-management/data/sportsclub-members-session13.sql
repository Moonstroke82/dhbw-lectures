-- Sports club: merged member list for the data quality lab (Data Management, worksheet 13)
--
-- The football and the tennis department kept their own spreadsheets. A volunteer has
-- merged them into one list, loaded as it arrived: all columns TEXT, no constraints.
-- department is the club's reference list of departments.
-- All names, e-mail addresses and phone numbers are fictional.
--
--   import sqlite3
--   con = sqlite3.connect(":memory:")
--   with open("sportsclub-members-session13.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- Running the script again deletes and rebuilds both tables.
-- Row counts afterwards: member_list 16, department 2.

DROP TABLE IF EXISTS member_list;
DROP TABLE IF EXISTS department;

CREATE TABLE department (
    name          TEXT PRIMARY KEY,
    monthly_fee   NUMERIC NOT NULL
);

INSERT INTO department VALUES
    ('Football', 12.00),
    ('Tennis',   18.00);

-- member_type: 'adult' or 'youth' (under 18 on the reference date 2027-06-01).
-- Club rule: every youth member has a parent's phone number.
CREATE TABLE member_list (
    member_no     TEXT,
    name          TEXT,
    birth_date    TEXT,
    member_type   TEXT,
    department    TEXT,
    joined_on     TEXT,
    e_mail        TEXT,
    parent_phone  TEXT
);

INSERT INTO member_list VALUES
    ('M101', 'Tom Berger',     '1985-03-14', 'adult', 'Football', '2015-09-01', 'tom.berger@example.org',   NULL),
    ('M102', 'Mila Schneider', '2013-07-22', 'youth', 'Football', '2021-04-10', NULL,                       '0621 1234 102'),
    ('M103', 'Kerem Aydın',    '1992-11-02', 'adult', 'Tennis',   '2019-05-01', 'kerem.aydin@example.com',  NULL),
    ('M104', 'Lena Vogt',      '2011-01-30', 'youth', 'Tennis',   '2020-03-15', 'lena.vogt@example.net',    NULL),
    ('M105', 'Paul Hartmann',  '1978-06-05', 'adult', 'Footbal',  '2010-08-01', 'p.hartmann@example.org',   NULL),
    ('M106', 'Sara Ludwig',    '2014-09-09', 'Youth', 'Football', '2022-09-01', NULL,                       '0621 1234 106'),
    ('M107', 'Jonas Klein',    '2012-02-17', 'adult', 'Football', '2019-09-01', NULL,                       NULL),
    ('M108', 'Eva Brandt',     '1990-04-25', 'adult', 'Tennis',   '2018-04-01', 'eva.brandt@example.com',   NULL),
    ('M108', 'Nils Brandt',    '2010-12-12', 'youth', 'Tennis',   '2018-04-01', NULL,                       '0621 1234 108'),
    ('M109', 'Ida Krüger',     '1969-10-10', 'A',     'Tennis',   '01.05.2016', 'ida.krueger@example.org',  NULL),
    ('M110', 'Lukas Weiß',     '2009-08-03', 'youth', 'Football', '2016-09-01', 'lukas.weiss@example.net',  '0621 1234 110'),
    ('M111', 'Tim Sommer',     '1995-01-20', 'adult', 'Football', '1994-06-01', 'tim.sommer@example.com',   NULL),
    ('M112', 'Lena Vogt',      '2011-01-30', 'youth', 'Football', '2023-02-01', 'lena.vogt@example.net',    '0621 1234 112'),
    ('M113', 'Anton Fuchs',    '1958-12-01', 'adult', 'Tennis',   '1990-04-01', NULL,                       NULL),
    ('M114', 'Marie Lang',     '2016-05-05', 'youth', 'Football', '2026-09-01', NULL,                       '0621 1234 114'),
    ('M115', 'Yusuf Demir',    '2001-07-07', 'adult', 'Football', '2027-08-15', 'yusuf.demir@example.org',  NULL);
