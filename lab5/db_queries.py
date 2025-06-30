import mysql.connector
import unittest

# connection settings
DB_CONFIG = {
    'user': 'root',          
    'password': 'Ilovedad247$!',
    'host': 'localhost',
    'database': 'my_guitar_shop'
}
#call for the connection to database
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

#defining of queries

#ordered by price
def get_products_ordered_by_price():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT product_code, product_name, list_price, discount_percent
        FROM products
        ORDER BY list_price DESC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#customers m to z
def get_customers_m_to_z():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT first_name, last_name, CONCAT(last_name, ', ', first_name) AS full_name
        FROM customers
        WHERE last_name >= 'M'
        ORDER BY last_name ASC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#prices between 500 and 2000
def get_products_price_between_500_and_2000():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT product_name, list_price, date_added
        FROM products
        WHERE list_price > 500 AND list_price < 2000
        ORDER BY date_added DESC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#items greater than 500
def get_order_items_total_greater_than_500():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT item_id, item_price, discount_amount, quantity,
               item_price * quantity AS price_total,
               discount_amount * quantity AS discount_total,
               (item_price - discount_amount) * quantity AS item_total
        FROM order_items
        WHERE (item_price - discount_amount) * quantity > 500
        ORDER BY item_total DESC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#combining products
def get_categories_join_products():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.category_name, p.product_name, p.list_price
        FROM categories c
        JOIN products p ON c.category_id = p.category_id
        ORDER BY c.category_name ASC, p.product_name ASC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#grabbing customers address
def get_customer_john_doe_addresses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
        FROM customers c
        JOIN addresses a ON c.customer_id = a.customer_id
        WHERE c.email_address = 'john.doe@yahoo.com'
        ORDER BY a.zip_code ASC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#grabbing shipping address
def get_customers_with_shipping_addresses():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.first_name, c.last_name, a.line1, a.city, a.state, a.zip_code
        FROM customers c
        JOIN addresses a ON c.shipping_address_id = a.address_id
        ORDER BY a.zip_code ASC;
    ''')
    result = cursor.fetchall()
    conn.close()
    return result

#unit tests
class TestGuitarShopQueries(unittest.TestCase):
    def test_products_ordered_by_price(self):
        result = get_products_ordered_by_price()
        self.assertTrue(len(result) > 0)

    def test_customers_m_to_z(self):
        result = get_customers_m_to_z()
        self.assertTrue(len(result) > 0)

    def test_products_price_between(self):
        result = get_products_price_between_500_and_2000()
        self.assertTrue(len(result) > 0)

    def test_order_items_total_greater(self):
        result = get_order_items_total_greater_than_500()
        self.assertTrue(len(result) > 0)

    def test_categories_join_products(self):
        result = get_categories_join_products()
        self.assertTrue(len(result) > 0)

    def test_customer_john_doe_addresses(self):
        result = get_customer_john_doe_addresses()
        self.assertTrue(isinstance(result, list))

    def test_customers_with_shipping_addresses(self):
        result = get_customers_with_shipping_addresses()
        self.assertTrue(len(result) > 0)

if __name__ == '__main__':
    unittest.main()