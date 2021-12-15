-- Start with empty database
CREATE TABLE PEOPLE
(
    NAME   CHAR(10),
    HIRED  DATE,
    STORE  INTEGER,
    HOURLY BOOL DEFAULT 1
);

INSERT INTO PEOPLE VALUES
    ('John', '2000-01-01', 1, 1),
    ('Mary', '2000-01-01', 1, 0),
    ('John', '2000-01-01', 2, 1),
    ('Mary', '2000-01-01', 2, 0);
