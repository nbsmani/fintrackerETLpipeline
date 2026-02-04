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
DROP TABLE IF EXISTS bronze_prices;
CREATE TABLE IF NOT EXISTS bronze_prices (
    price_id BIGSERIAL PRIMARY KEY,
    commodity_name VARCHAR(25),
    price DECIMAL(16, 4),
    symbol VARCHAR(10),
    api_updated_at TIMESTAMPTZ ,
    prc_updated_at_readable VARCHAR(25),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP);

COPY bronze.bronze_prices(commodity_name, price, symbol, api_updated_at, prc_updated_at_readable)
FROM '/commodity-tracker/data/landing_zone/price2026-02-01T22-10-10Z.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM bronze_prices LIMIT 5;