CREATE TABLE IF NOT EXISTS users
(
    users_id    BIGINT PRIMARY KEY,
    name        VARCHAR(100),
    surname     VARCHAR(100),
    lang        VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS provider
(
    provider_id uuid PRIMARY KEY,
    name        VARCHAR(100),
    website     VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS wod
(
    wod_id      uuid PRIMARY KEY,
    wod_day     date,
    title       VARCHAR(150),
    content     TEXT,
    provider_id uuid UNIQUE
);
