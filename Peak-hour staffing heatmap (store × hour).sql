SELECT
  store_id,
  order_hour,
  COUNT(DISTINCT transaction_id) AS txns,
  ROUND(SUM(line_net_sales),2) AS net_sales,
  ROUND(AVG(service_time_sec),1) AS avg_service_sec
FROM v_sales_line
WHERE is_refund = 0
GROUP BY store_id, order_hour
ORDER BY store_id, order_hour;