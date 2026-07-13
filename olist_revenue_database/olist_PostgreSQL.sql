SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month,
       SUM(price) AS revenue
FROM orders
JOIN order_items ON orders.order_id = order_items.order_id
GROUP BY month
ORDER BY month;