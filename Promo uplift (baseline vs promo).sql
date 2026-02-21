WITH daily AS (
  SELECT order_date, promo_type,
         SUM(line_net_sales) AS net_sales,
         COUNT(DISTINCT transaction_id) AS txns
  FROM v_sales_line
  WHERE is_refund = 0
  GROUP BY order_date, promo_type
),
baseline AS (
  SELECT order_date,
         SUM(net_sales)/NULLIF(SUM(txns),0) AS baseline_aov
  FROM daily
  WHERE promo_type = 'None'
  GROUP BY order_date
)
SELECT d.promo_type,
       ROUND(AVG(d.net_sales/d.txns),2) AS promo_aov,
       ROUND(AVG(b.baseline_aov),2)     AS baseline_aov,
       ROUND(AVG((d.net_sales/d.txns) - b.baseline_aov),2) AS uplift_aov
FROM daily d
JOIN baseline b ON d.order_date = b.order_date
WHERE d.promo_type <> 'None'
GROUP BY d.promo_type
ORDER BY uplift_aov DESC;