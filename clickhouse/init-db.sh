#!/bin/bash
set -e

clickhouse-client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS jobsity_challenge;
    DROP TABLE IF EXISTS jobsity_challenge.trips;
    CREATE TABLE IF NOT EXISTS jobsity_challenge.trips
    (
        uuid UUID,
        hash_value String,
        region String,
        origin_latitude Float64,
        origin_longitude Float64,
        destination_latitude Float64,
        destination_longitude Float64,
        date_time Datetime,
        datasource String,
        year_week String
    )
    ENGINE = MergeTree()
    PRIMARY KEY uuid
    ORDER BY uuid;
EOSQL
