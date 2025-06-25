
-- Query 7: customer only shipping addresses
SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
FROM customers c
JOIN addresses a ON c.shipping_address_id = a.address_id
ORDER BY a.zip_code ASC;
