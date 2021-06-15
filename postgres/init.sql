-- Basic Postgres setup
-- CREATE USER docker;
-- ALTER USER docker WITH PASSWORD 'my_password123';
-- CREATE DATABASE docker;
GRANT ALL PRIVILEGES ON DATABASE docker TO docker;

-- Project setup
CREATE SCHEMA jobsity_challenge;
-- GRANT ALL ON jobsity_challenge.* TO docker WITH GRANT OPTION;

DROP TABLE IF EXISTS jobsity_challenge.trips;

CREATE TABLE IF NOT EXISTS jobsity_challenge.trips
(
    uuid UUID PRIMARY KEY,
    hash_value VARCHAR(32) NOT NULL,
    region VARCHAR(256) NOT NULL,
    origin_latitude NUMERIC(18, 15) NOT NULL,
    origin_longitude NUMERIC(18, 15) NOT NULL,
    destination_latitude NUMERIC(18, 15) NOT NULL,
    destination_longitude NUMERIC(18, 15) NOT NULL,
    date_time TIMESTAMP NOT NULL,
    datasource VARCHAR(256) NOT NULL
);

CREATE INDEX idx_trips_similar
ON jobsity_challenge.trips (region, date_time);
