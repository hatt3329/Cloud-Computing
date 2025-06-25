
-- Query 5: join categories and products together
SELECT c.category_name, p.product_name, p.list_price
FROM categories c
JOIN products p ON c.category_id = p.category_id
ORDER BY c.category_name ASC, p.product_name ASC;
