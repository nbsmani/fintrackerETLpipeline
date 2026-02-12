SET search_path TO gold;

ALTER DATABASE commodity_db SET timezone TO 'UTC';

 CREATE TABLE IF NOT EXISTS gold.dim_symbol (price_id BIGSERIAL PRIMARY KEY,
             commodity_name VARCHAR(25), 
             symbol VARCHAR(10)
             );

CREATE TABLE IF NOT EXISTS gold.fact_price (
    price_id BIGSERIAL PRIMARY KEY,
    price DECIMAL(16, 4),
    api_updated_at TIMESTAMPTZ,
    prc_updated_at_readable VARCHAR(25), 
    ingested_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP, 
    batch_id UUID);