
-- Query 1: products listed by price
SELECT product_code, product_name, list_price, discount_percent
FROM products
ORDER BY list_price DESC;
