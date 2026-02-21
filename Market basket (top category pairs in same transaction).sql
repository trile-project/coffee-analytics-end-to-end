WITH cats AS (
  SELECT transaction_id, category
  FROM v_sales_line
  WHERE is_refund = 0
  GROUP BY transaction_id, category
),
pairs AS (
  SELECT a.category AS cat_a, b.category AS cat_b, COUNT(*) AS txn_counta
  FROM cats a
  JOIN cats b
    ON a.transaction_id = b.transaction_id
   AND a.category < b.category
  GROUP BY a.category, b.category
)
SELECT * FROM pairs
ORDER BY txn_count DESC
LIMIT 25;