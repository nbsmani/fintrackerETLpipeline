/*

* This script defines a stored procedure to promote data from the bronze layer to the silver layer.
* It includes necessary transformations, filtering for data quality, and checks for duplicates based on batch_id. 
* The procedure is executed at the end of the script, and results are displayed for both layers.

*/

SET search_path TO silver;
ALTER DATABASE commodity_db SET timezone TO 'UTC';
    
CREATE OR REPLACE PROCEDURE silver.promote_bronze_to_silver()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Create a staged version of the bronze data with necessary transformations and filtering
    INSERT INTO silver_prices (
        commodity_name,
        price,
        symbol,
        api_updated_at,
        prc_updated_at_readable,
        ingested_at,
        batch_id
    ) WITH clean_staging AS (
        SELECT
            name AS commodity_name,
            price::DECIMAL(16, 4) AS price,
            UPPER(symbol) AS symbol,
            updatedAt::TIMESTAMPTZ AS api_updated_at,
            updatedAtReadable AS prc_updated_at_readable,
            ingested_at,
            uuid AS batch_id
        FROM bronze.bronze_prices
        WHERE price IS NOT NULL
            AND price > 0.0000
            AND symbol IS NOT NULL 
    )-- Move data from bronze to silver layer
    SELECT cs.* FROM clean_staging cs
        WHERE NOT EXISTS (
        SELECT 1
        FROM silver.silver_prices sp
        WHERE sp.batch_id = cs.batch_id
    );

    RAISE NOTICE 'Data promoted from bronze to silver layer successfully.';
    
    COMMENT ON PROCEDURE silver.promote_bronze_to_silver IS 'This procedure promotes data from the bronze layer to the silver layer, applying necessary transformations and ensuring data quality by filtering out invalid records. It also checks for duplicates based on batch_id to prevent reprocessing of the same data.';
    END;
    $$;
   
    
-- This executes the logic you just built
CALL silver.promote_bronze_to_silver();

-- Check the results
SELECT * FROM bronze.bronze_prices;
SELECT * FROM silver.silver_prices;