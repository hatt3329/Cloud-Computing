
-- Query 6: john doe's address
SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
FROM customers c
JOIN addresses a ON c.customer_id = a.customer_id
WHERE c.email_address = 'john.doe@yahoo.com'
ORDER BY a.zip_code ASC;
