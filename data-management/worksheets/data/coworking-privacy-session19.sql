-- Coworking space: member data, consents and data subject requests
-- (Data Management, worksheet 19: access to data, legal and organisational aspects)
--
-- Three tables, independent of the other course databases:
--   cw_member        16 members with the data the booking app keeps about them
--   cw_consent       the log of consents for the newsletter and for photos of members
--                    on the website and on social media (given / withdrawn)
--   cw_request       requests of members who exercised their data protection rights
-- All names and events are fictional. Teaching material, not legal advice.
--
--   import sqlite3
--   con = sqlite3.connect("coworking-privacy.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   with open("coworking-privacy-session19.sql", encoding="utf-8") as f:
--       con.executescript(f.read())
--
-- Running this script again deletes and rebuilds the three tables.
-- Row counts afterwards: cw_member 16, cw_consent 18, cw_request 6.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS cw_request;
DROP TABLE IF EXISTS cw_consent;
DROP TABLE IF EXISTS cw_member;

CREATE TABLE cw_member (
    member_no   TEXT    PRIMARY KEY,
    name        TEXT    NOT NULL,
    e_mail      TEXT    NOT NULL UNIQUE,
    birth_year  INTEGER NOT NULL CHECK (birth_year BETWEEN 1930 AND 2010),
    postcode    TEXT    NOT NULL,
    profession  TEXT,
    plan        TEXT    NOT NULL CHECK (plan IN ('DAY', 'FLEX', 'FIX', 'TEAM')),
    start_date  TEXT    NOT NULL CHECK (start_date IS date(start_date)),
    end_date    TEXT             CHECK (end_date IS date(end_date))   -- NULL = still a member
);

INSERT INTO cw_member VALUES
('M01', 'Jonas Weber',     'jonas.weber@example.org',    1991, '68159', 'software developer', 'FLEX', '2026-01-15', NULL),
('M02', 'Sara Öztürk',     'sara.oeztuerk@example.com',  1988, '68161', 'translator',         'FIX',  '2026-03-01', NULL),
('M03', 'Tim Lang',        'tim.lang@example.net',       1995, '69117', 'student',            'DAY',  '2026-04-10', '2026-12-31'),
('M04', 'Nora Haas',       'nora.haas@example.org',      1984, '68165', 'architect',          'FLEX', '2026-05-02', NULL),
('M05', 'Felix Braun',     'felix.braun@example.com',    1991, '68159', 'software developer', 'FIX',  '2026-05-15', NULL),
('M06', 'Ali Kaya',        'ali.kaya@example.net',       1979, '67059', 'tax adviser',        'FIX',  '2026-07-01', NULL),
('M07', 'Julia Roth',      'julia.roth@example.org',     1993, '68165', 'designer',           'FIX',  '2027-01-13', NULL),
('M08', 'Ben Graf',        'ben.graf@example.com',       1991, '68159', 'software developer', 'DAY',  '2026-09-20', NULL),
('M09', 'Lina Brandt',     'lina.brandt@example.net',    1986, '01067', 'sales manager',      'TEAM', '2027-02-01', NULL),
('M10', 'Emre Yilmaz',     'emre.yilmaz@example.org',    1999, '68163', 'student',            'DAY',  '2026-10-05', NULL),
('M11', 'Hanna Vogt',      'hanna.vogt@example.com',     1972, '69120', 'psychotherapist',    'FIX',  '2026-02-01', NULL),
('M12', 'Paul Neumann',    'paul.neumann@example.net',   1988, '68161', 'journalist',         'FLEX', '2026-06-01', '2027-02-28'),
('M13', 'Mia Schröder',    'mia.schroeder@example.org',  1995, '69117', 'student',            'DAY',  '2026-11-11', NULL),
('M14', 'David Klein',     'david.klein@example.com',    1984, '68165', 'architect',          'TEAM', '2027-02-01', NULL),
('M15', 'Laura Fuchs',     'laura.fuchs@example.net',    1990, '68169', 'marketing manager',  'FLEX', '2026-08-15', NULL),
('M16', 'Can Arslan',      'can.arslan@example.org',     1999, '68163', 'student',            'DAY',  '2027-03-02', NULL);

-- One row per event. purpose: 'newsletter' or 'photos' (photos of the member on the
-- website and on social media). form: 'web-2026' = sign-up form with an unticked box;
-- 'welcome-pack' = paper form with all boxes ticked in advance (used until June 2026).
CREATE TABLE cw_consent (
    event_id    INTEGER PRIMARY KEY,
    member_no   TEXT    NOT NULL REFERENCES cw_member (member_no),
    purpose     TEXT    NOT NULL CHECK (purpose IN ('newsletter', 'photos')),
    action      TEXT    NOT NULL CHECK (action IN ('given', 'withdrawn')),
    event_on    TEXT    NOT NULL CHECK (event_on IS date(event_on)),
    form        TEXT             CHECK (form IN ('web-2026', 'welcome-pack')),
    CHECK ((action = 'given') = (form IS NOT NULL))
);

INSERT INTO cw_consent VALUES
( 1, 'M01', 'newsletter', 'given',     '2026-01-15', 'welcome-pack'),
( 2, 'M01', 'photos',     'given',     '2026-01-15', 'welcome-pack'),
( 3, 'M02', 'newsletter', 'given',     '2026-03-01', 'welcome-pack'),
( 4, 'M02', 'photos',     'given',     '2026-03-01', 'welcome-pack'),
( 5, 'M04', 'photos',     'given',     '2026-07-20', 'web-2026'),
( 6, 'M05', 'newsletter', 'given',     '2026-07-02', 'web-2026'),
( 7, 'M06', 'newsletter', 'given',     '2026-07-01', 'web-2026'),
( 8, 'M06', 'photos',     'given',     '2026-07-01', 'web-2026'),
( 9, 'M07', 'photos',     'given',     '2027-01-13', 'web-2026'),
(10, 'M07', 'newsletter', 'given',     '2027-01-13', 'web-2026'),
(11, 'M06', 'photos',     'withdrawn', '2026-12-03', NULL),
(12, 'M09', 'photos',     'given',     '2027-02-01', 'web-2026'),
(13, 'M11', 'photos',     'given',     '2026-02-01', 'welcome-pack'),
(14, 'M12', 'photos',     'given',     '2026-07-10', 'web-2026'),
(15, 'M14', 'photos',     'given',     '2027-02-01', 'web-2026'),
(16, 'M14', 'photos',     'withdrawn', '2027-03-20', NULL),
(17, 'M15', 'newsletter', 'given',     '2026-08-15', 'web-2026'),
(18, 'M15', 'photos',     'given',     '2026-08-15', 'web-2026');

-- Requests under the GDPR rights. answered_on NULL = still open.
CREATE TABLE cw_request (
    request_id   INTEGER PRIMARY KEY,
    member_no    TEXT    NOT NULL REFERENCES cw_member (member_no),
    kind         TEXT    NOT NULL CHECK (kind IN ('access', 'rectification', 'erasure', 'objection', 'portability')),
    received_on  TEXT    NOT NULL CHECK (received_on IS date(received_on)),
    answered_on  TEXT             CHECK (answered_on IS date(answered_on)),
    note         TEXT
);

INSERT INTO cw_request VALUES
(1, 'M03', 'erasure',       '2027-01-08', '2027-01-20', 'former member, asks to delete all data'),
(2, 'M11', 'access',        '2027-01-25', '2027-03-02', 'wants a copy of all data incl. badge scans'),
(3, 'M02', 'objection',     '2027-02-10', '2027-02-11', 'no more marketing e-mails'),
(4, 'M12', 'erasure',       '2027-03-01', NULL,         'former member since February'),
(5, 'M08', 'rectification', '2027-03-05', '2027-03-06', 'wrong postcode'),
(6, 'M01', 'portability',   '2027-03-10', NULL,         'booking history as CSV for a new provider');
