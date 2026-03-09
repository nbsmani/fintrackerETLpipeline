-- 1. Populate symbol dimension
INSERT INTO gold.dim_symbol (symbol, commodity_name)
SELECT DISTINCT 
    UPPER(symbol) as symbol,
    INITCAP(commodity_name) as commodity_name
FROM silver.silver_prices s
WHERE NOT EXISTS (
    SELECT 1 FROM gold.dim_symbol d 
    WHERE d.symbol = UPPER(s.symbol)
);

-- 2. Populate fact table (exactly matching silver)
INSERT INTO gold.fact_prices (
    symbol_id,
    commodity_name,
    price,
    symbol,
    api_updated_at,
    prc_updated_at_readable,
    ingested_at,
    batch_id
)
SELECT 
    d.symbol_id,
    s.commodity_name,
    s.price,
    s.symbol,
    s.api_updated_at,
    s.prc_updated_at_readable,
    s.ingested_at,
    s.batch_id
FROM silver.silver_prices s
JOIN gold.dim_symbol d ON UPPER(s.symbol) = d.symbol
WHERE NOT EXISTS (
    SELECT 1 FROM gold.fact_prices f 
    WHERE f.batch_id = s.batch_id
    AND f.api_updated_at = s.api_updated_at
);