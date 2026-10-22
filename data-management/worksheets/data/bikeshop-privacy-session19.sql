-- Velo Neckar bike shop: consent log and record of processing activities
-- (Data Management, session 19: access to data, legal and organisational aspects)
--
-- Adds three tables to the bike shop database:
--   consent_text         the versions of the newsletter sign-up text the shop has used
--                        (where it was shown, whether the box was pre-ticked, whether
--                        the sign-up had to be confirmed by e-mail = double opt-in)
--   consent_event        the log of newsletter consents: given, confirmed, withdrawn
--   processing_activity  the shop's draft record of processing activities: what personal
--                        data is processed for which purpose, on which legal basis,
--                        for how long and by whom (with gaps on purpose)
-- All names and events are fictional. The account ids are those of the web shop export
-- of session 13 (webshop_customer, bikeshop-dq-session13.sql); load that script first if
-- you want to compare the log with the export's newsletter column.
-- Teaching material, not legal advice: the legal bases in processing_activity are
-- examples for discussion, not a legal assessment of a real business.
--
--   import sqlite3
--   con = sqlite3.connect("bikeshop.db")
--   con.execute("PRAGMA foreign_keys = ON")
--   for script in ["bikeshop-schema.sql", "bikeshop-data.sql",
--                  "bikeshop-data-session09.sql", "bikeshop-dq-session13.sql",
--                  "bikeshop-privacy-session19.sql"]:
--       with open(script, encoding="utf-8") as f:
--           con.executescript(f.read())
--
-- Running this script again deletes and rebuilds the three tables.
-- Row counts afterwards: consent_text 3, consent_event 20, processing_activity 9.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS consent_event;
DROP TABLE IF EXISTS consent_text;
DROP TABLE IF EXISTS processing_activity;

CREATE TABLE consent_text (
    text_version   TEXT    PRIMARY KEY,
    channel        TEXT    NOT NULL,
    wording        TEXT    NOT NULL,                              -- what the person saw
    used_from      TEXT    NOT NULL CHECK (used_from IS date(used_from)),
    used_until     TEXT             CHECK (used_until IS date(used_until)),  -- NULL = still in use
    pre_ticked     INTEGER NOT NULL CHECK (pre_ticked IN (0, 1)),          -- 1 = box ticked by default
    double_opt_in  INTEGER NOT NULL CHECK (double_opt_in IN (0, 1))        -- 1 = e-mail confirmation required
);

INSERT INTO consent_text VALUES
('APP-1',  'web shop app 1.x (old)',
           'Yes, send me news and offers.',
           '2021-03-01', '2023-06-30', 1, 0),
('WEB-2',  'web shop 2.0 sign-up form',
           'I would like to receive the Velo Neckar newsletter (news, offers and events) by e-mail about once a month. I can unsubscribe at any time with the link in every newsletter.',
           '2023-07-01', NULL, 0, 1),
('SHOP-1', 'paper form at the till',
           'I would like to receive the Velo Neckar newsletter (news, offers and events) by e-mail about once a month. I can unsubscribe at any time with the link in every newsletter.',
           '2024-01-01', NULL, 0, 1);

-- One row per event. 'given' = the person ticked the box or signed the form;
-- 'confirmed' = the person clicked the link in the confirmation e-mail;
-- 'withdrawn' = the person unsubscribed.
CREATE TABLE consent_event (
    event_id      INTEGER PRIMARY KEY,
    account_id    TEXT    NOT NULL,                  -- web shop account (W01 ... W20)
    purpose       TEXT    NOT NULL CHECK (purpose IN ('newsletter')),
    action        TEXT    NOT NULL CHECK (action IN ('given', 'confirmed', 'withdrawn')),
    event_at      TEXT    NOT NULL CHECK (event_at IS datetime(event_at)),
    text_version  TEXT    REFERENCES consent_text (text_version),   -- for 'given' events
    CHECK ((action = 'given') = (text_version IS NOT NULL))
);

INSERT INTO consent_event VALUES
( 1, 'W03', 'newsletter', 'given',     '2022-04-11 18:02:15', 'APP-1'),
( 2, 'W15', 'newsletter', 'given',     '2022-08-08 09:41:03', 'APP-1'),
( 3, 'W18', 'newsletter', 'given',     '2023-05-30 20:15:47', 'APP-1'),
( 4, 'W09', 'newsletter', 'given',     '2023-09-14 12:30:00', 'WEB-2'),
( 5, 'W09', 'newsletter', 'confirmed', '2023-09-14 12:33:21', NULL),
( 6, 'W02', 'newsletter', 'given',     '2024-02-01 07:55:10', 'WEB-2'),
( 7, 'W02', 'newsletter', 'confirmed', '2024-02-01 08:01:44', NULL),
( 8, 'W01', 'newsletter', 'given',     '2024-05-02 10:14:09', 'WEB-2'),
( 9, 'W01', 'newsletter', 'confirmed', '2024-05-02 10:20:31', NULL),
(10, 'W02', 'newsletter', 'withdrawn', '2025-01-10 19:03:12', NULL),
(11, 'W04', 'newsletter', 'given',     '2025-03-10 16:45:00', 'WEB-2'),
(12, 'W04', 'newsletter', 'confirmed', '2025-03-10 16:47:52', NULL),
(13, 'W14', 'newsletter', 'given',     '2026-03-03 11:20:18', 'WEB-2'),
(14, 'W14', 'newsletter', 'confirmed', '2026-03-03 11:24:40', NULL),
(15, 'W05', 'newsletter', 'given',     '2026-11-15 15:10:00', 'SHOP-1'),
(16, 'W05', 'newsletter', 'confirmed', '2026-11-16 08:12:05', NULL),
(17, 'W08', 'newsletter', 'given',     '2026-12-01 21:37:29', 'WEB-2'),
(18, 'W12', 'newsletter', 'given',     '2027-01-25 13:05:44', 'WEB-2'),
(19, 'W12', 'newsletter', 'confirmed', '2027-01-25 13:09:02', NULL),
(20, 'W09', 'newsletter', 'withdrawn', '2027-04-20 06:58:30', NULL);

-- Draft record of processing activities (GDPR Art. 30 lists what such a record contains).
-- NULL = not yet clarified. Legal bases are written as GDPR article references.
CREATE TABLE processing_activity (
    activity_id     INTEGER PRIMARY KEY,
    activity        TEXT    NOT NULL,
    purpose         TEXT,
    legal_basis     TEXT,
    data_subjects   TEXT    NOT NULL,
    data_categories TEXT    NOT NULL,
    recipients      TEXT,                     -- incl. processors (service providers)
    retention       TEXT,                     -- when the data is deleted
    owner           TEXT,                     -- who in the shop is responsible
    special_category INTEGER NOT NULL CHECK (special_category IN (0, 1)),  -- Art. 9 data involved
    personal_data   INTEGER NOT NULL CHECK (personal_data IN (0, 1))
);

INSERT INTO processing_activity VALUES
(1, 'till sales and invoices',
    'sell goods, issue invoices, keep accounting records',
    'Art. 6(1)(b); Art. 6(1)(c)',
    'customers', 'name, address, items bought, amount, payment method',
    'tax adviser', '8 years (booking vouchers, § 147 AO)', 'Laura Becker', 0, 1),
(2, 'repair jobs',
    'carry out repairs, call the customer when the bike is ready',
    'Art. 6(1)(b)',
    'customers', 'name, phone, bike, frame number, repair lines',
    NULL, NULL, 'Katrin Vogel', 0, 1),
(3, 'web shop accounts and orders',
    'run customer accounts, deliver orders',
    'Art. 6(1)(b)',
    'web shop customers', 'name, e-mail, postcode, city, birth date, orders',
    'web shop hosting (processor), payment provider, parcel service', '3 years after last order', 'Laura Becker', 0, 1),
(4, 'e-mail newsletter',
    'send news, offers and events by e-mail',
    'Art. 6(1)(a)',
    'subscribers', 'e-mail, name, consent log',
    'newsletter service (processor)', 'until consent is withdrawn', 'Laura Becker', 0, 1),
(5, 'web shop clickstream',
    NULL,
    NULL,
    'web shop visitors', 'IP address, pages viewed, time stamps, device',
    'web analytics tool', NULL, NULL, 0, 1),
(6, 'damage photos of bikes',
    'document damage before and after a repair',
    'Art. 6(1)(b)',
    'customers', 'photos of bikes (faces or licence plates possible)',
    NULL, NULL, 'Katrin Vogel', 0, 1),
(7, 'staff rota and payroll',
    'plan shifts, pay salaries',
    'Art. 6(1)(b); Art. 6(1)(c)',
    'employees', 'name, bank account, working hours, sick days',
    'payroll office (processor)', NULL, 'owner', 1, 1),
(8, 'video camera at the entrance',
    'prevent and investigate theft',
    'Art. 6(1)(f)',
    'customers, employees, passers-by', 'video images',
    NULL, '72 hours', 'owner', 0, 1),
(9, 'weather data for the revenue analysis',
    'compare revenue on good and bad bike days',
    NULL,
    'none', 'hourly weather per station',
    NULL, NULL, 'Laura Becker', 0, 0);
