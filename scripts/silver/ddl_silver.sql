/*
    DDL Script for silver Layer Tables
    Database: commodity_db.

    Tables:
    1. bronze_symbols: Stores symbol information.
    2. bronze_prices: Stores price data with ingestion timestamps.
    The timezone is set to UTC for consistency.
*/


SET search_path TO silver;

ALTER DATABASE commodity_db SET timezone TO 'UTC';
-- DROP TABLE IF EXISTS silver_prices;
CREATE TABLE IF NOT EXISTS silver_prices (
    price_id BIGSERIAL PRIMARY KEY,
    commodity_name VARCHAR(25),
    price DECIMAL(16, 4),
    symbol VARCHAR(10),
    api_updated_at TIMESTAMPTZ ,
    prc_updated_at_readable VARCHAR(25),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    batch_id UUID);
