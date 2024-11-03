-- models/moving_average.sql
WITH base_data AS (
    SELECT
        close,
        ticker
    FROM public.raw_stock_data
),
moving_avg_data AS (
    SELECT
        ticker,
        close,
        AVG(close) OVER (PARTITION BY ticker ORDER BY ticker ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS moving_avg
    FROM base_data
)
SELECT * FROM moving_avg_data
