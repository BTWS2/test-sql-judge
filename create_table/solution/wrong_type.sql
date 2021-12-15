-- Start with empty database
CREATE TABLE PEOPLE
(
    NAME   CHAR(10),
    HIRED  BOOL,
    STORE  INTEGER,
    HOURLY BOOL DEFAULT 1
);
