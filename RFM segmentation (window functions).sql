WITH rfm AS (
  SELECT
    customer_id,
    DATEDIFF(CURRENT_DATE, MAX(order_date)) AS recency_days,
    COUNT(DISTINCT transaction_id) AS frequency,
    SUM(line_net_sales) AS monetary
  FROM v_sales_line
  WHERE is_refund = 0
  GROUP BY customer_id
),
scored AS (
  SELECT *,
    NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
    NTILE(5) OVER (ORDER BY frequency)        AS f_score,
    NTILE(5) OVER (ORDER BY monetary)         AS m_score
  FROM rfm
)
SELECT r_score,f_score,m_score,
       COUNT(*) AS customers,
       ROUND(AVG(monetary),2) AS avg_monetary
FROM scored
GROUP BY r_score,f_score,m_score
ORDER BY r_score DESC, f_score DESC, m_score DESC;