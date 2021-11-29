-- Start with empty database
CREATE TABLE PEOPLE
(
    NAME   CHAR(10),
    HIRED  DATE,
    STORE  INTEGER,
    HOURLY BOOL DEFAULT 1
);
