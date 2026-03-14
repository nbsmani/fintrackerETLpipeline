-- create gold schema
CREATE SCHEMA IF NOT EXISTS gold;

-- Dimension: symbols
CREATE TABLE IF NOT EXISTS gold.dim_symbol (
	symbol_id SERIAL PRIMARY KEY,
	symbol VARCHAR(10) UNIQUE NOT NULL,
	commodity_name VARCHAR (25) NOT NULL
);


-- Fact: prices (mirrors silver structure)
CREATE TABLE IF NOT EXISTS gold.fact_prices (
    fact_id BIGSERIAL PRIMARY KEY,
    symbol_id INTEGER NOT NULL REFERENCES gold.dim_symbol(symbol_id),
    commodity_name VARCHAR(25) NOT NULL,
    price DECIMAL(16, 4) NOT NULL,
    symbol VARCHAR(10) NOT NULL,
    api_updated_at TIMESTAMPTZ NOT NULL,
    prc_updated_at_readable VARCHAR(25),
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    batch_id UUID NOT NULL
);