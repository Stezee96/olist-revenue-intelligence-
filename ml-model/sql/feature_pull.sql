WITH items AS (
  SELECT
    oi.order_id,
    SUM(oi.price)         AS price,
    SUM(oi.freight_value) AS freight_value,
    (ARRAY_AGG(p.product_category_name ORDER BY oi.price DESC))[1] AS product_category,
    (ARRAY_AGG(s.seller_state         ORDER BY oi.price DESC))[1] AS seller_state
  FROM order_items oi
  JOIN products p ON oi.product_id = p.product_id
  JOIN sellers  s ON oi.seller_id  = s.seller_id
  GROUP BY oi.order_id
)
SELECT
  o.order_id,
  c.customer_state,
  i.price,
  i.freight_value,
  i.product_category,
  i.seller_state,
  (o.order_delivered_customer_date::date - o.order_purchase_timestamp::date) AS delivery_days,
  (o.order_delivered_customer_date::date - o.order_estimated_delivery_date::date) AS lateness,
  CASE
    WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 1
    ELSE 0
  END AS is_late,
  CASE WHEN r.review_score IN (1,2) THEN 1 ELSE 0 END AS bad_review
FROM orders o
JOIN items i ON o.order_id = i.order_id
JOIN customers c ON o.customer_id = c.customer_id
JOIN reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND r.review_score <> 3
;