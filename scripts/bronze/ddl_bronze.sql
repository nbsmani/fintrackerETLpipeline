/*
    DDL Script for Bronze Layer Tables
    Database: commodity_db.

    Tables:
    1. bronze_symbols: Stores symbol information.
    2. bronze_prices: Stores price data with ingestion timestamps.
    The timezone is set to UTC for consistency.
*/


SET search_path TO bronze;

ALTER DATABASE commodity_db SET timezone TO 'UTC';

CREATE TABLE IF NOT EXISTS bronze_prices (
    price_id BIGSERIAL PRIMARY KEY,
    name TEXT,
    price TEXT,
    symbol TEXt,
    updatedAt TEXT ,
    updatedAtReadable TEXT,
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    uuid UUID);

CREATE TABLE IF NOT EXISTS bronze_symbols(
    symbol_id SERIAL PRIMARY KEY,
    name TEXT,
    symbol TEXT,
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP);



