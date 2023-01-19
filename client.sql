CREATE TABLE client (
    username varchar(255) NOT NULL,
    code int NOT NULL,
    password varchar(255) NOT NULL,
    reports int NOT NULL DEFAULT(0),
    PRIMARY KEY (username)
);