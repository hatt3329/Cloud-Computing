/********************************************************
* This script creates the database named my_vegetable_shop
*********************************************************/

-- Drop the database if it exists
DROP DATABASE IF EXISTS my_vegetable_shop;

-- Create the database
CREATE DATABASE my_vegetable_shop;

-- Use the newly created database
USE my_vegetable_shop;

-- Create categories table
CREATE TABLE categories (
  category_id   INT           PRIMARY KEY AUTO_INCREMENT,
  category_name VARCHAR(255)  NOT NULL UNIQUE
);

-- Create vendors table (for Vendor Management)
CREATE TABLE vendors (
  vendor_id     INT           PRIMARY KEY AUTO_INCREMENT,
  vendor_name   VARCHAR(255)  NOT NULL UNIQUE,
  email_address VARCHAR(255)  NOT NULL UNIQUE,
  password      VARCHAR(255)  NOT NULL,
  phone         VARCHAR(20),
  address       VARCHAR(255)
);

-- Create products table (for Product Management)
CREATE TABLE products (
  product_id    INT            PRIMARY KEY AUTO_INCREMENT,
  category_id   INT            NOT NULL,
  vendor_id     INT            NOT NULL,
  product_code  VARCHAR(50)    NOT NULL UNIQUE,
  product_name  VARCHAR(255)   NOT NULL,
  description   TEXT,
  unit_price    DECIMAL(10,2)  NOT NULL,
  stock_quantity INT           NOT NULL DEFAULT 0,
  date_added    DATETIME       DEFAULT NULL,
  CONSTRAINT products_fk_categories
    FOREIGN KEY (category_id)
    REFERENCES categories (category_id),
  CONSTRAINT products_fk_vendors
    FOREIGN KEY (vendor_id)
    REFERENCES vendors (vendor_id)
);

-- Create customers table (for Customer Management)
CREATE TABLE customers (
  customer_id   INT           PRIMARY KEY AUTO_INCREMENT,
  email_address VARCHAR(255)  NOT NULL UNIQUE,
  password      VARCHAR(255)  NOT NULL,
  first_name    VARCHAR(60)   NOT NULL,
  last_name     VARCHAR(60)   NOT NULL
);

-- Create addresses table (for Customer Shipping/Billing)
CREATE TABLE addresses (
  address_id    INT           PRIMARY KEY AUTO_INCREMENT,
  customer_id   INT           NOT NULL,
  line1         VARCHAR(60)   NOT NULL,
  line2         VARCHAR(60)   DEFAULT NULL,
  city          VARCHAR(40)   NOT NULL,
  state         VARCHAR(2)    NOT NULL,
  zip_code      VARCHAR(10)   NOT NULL,
  phone         VARCHAR(12)   NOT NULL,
  is_shipping   TINYINT    NOT NULL DEFAULT 0, -- 1 for shipping, 0 for billing
  CONSTRAINT addresses_fk_customers
    FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id)
);

-- Create orders table (for Orders Service)
CREATE TABLE orders (
  order_id        INT           PRIMARY KEY AUTO_INCREMENT,
  customer_id     INT           NOT NULL,
  order_date      DATETIME      NOT NULL,
  shipping_cost   DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  total_amount    DECIMAL(10,2) NOT NULL,
  delivery_date   DATETIME      DEFAULT NULL,
  shipping_address_id INT       NOT NULL,
  billing_address_id INT        NOT NULL,
  payment_method  VARCHAR(50)   NOT NULL,
  order_status    VARCHAR(50)   NOT NULL DEFAULT 'Pending',
  CONSTRAINT orders_fk_customers
    FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id),
  CONSTRAINT orders_fk_shipping_address
    FOREIGN KEY (shipping_address_id)
    REFERENCES addresses (address_id),
  CONSTRAINT orders_fk_billing_address
    FOREIGN KEY (billing_address_id)
    REFERENCES addresses (address_id)
);

-- Create order_items table (for tracking products in orders)
CREATE TABLE order_items (
  item_id         INT           PRIMARY KEY AUTO_INCREMENT,
  order_id        INT           NOT NULL,
  product_id      INT           NOT NULL,
  quantity        INT           NOT NULL,
  price_at_order  DECIMAL(10,2) NOT NULL,
  CONSTRAINT order_items_fk_orders
    FOREIGN KEY (order_id)
    REFERENCES orders (order_id),
  CONSTRAINT order_items_fk_products
    FOREIGN KEY (product_id)
    REFERENCES products (product_id)
);

-- Create shopping cart table (for Shopping Cart Service)
CREATE TABLE shopping_cart (
  cart_id        INT           PRIMARY KEY AUTO_INCREMENT,
  customer_id    INT           NOT NULL,
  product_id     INT           NOT NULL,
  quantity       INT           NOT NULL,
  CONSTRAINT shopping_cart_fk_customers
    FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id),
  CONSTRAINT shopping_cart_fk_products
    FOREIGN KEY (product_id)
    REFERENCES products (product_id)
);

-- Create reviews table (for Reviews Service)
CREATE TABLE reviews (
  review_id      INT           PRIMARY KEY AUTO_INCREMENT,
  product_id     INT           NOT NULL,
  customer_id    INT           NOT NULL,
  rating         INT           NOT NULL CHECK(rating >= 1 AND rating <= 5),
  review_text    TEXT,
  review_date    DATETIME      DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT reviews_fk_products
    FOREIGN KEY (product_id)
    REFERENCES products (product_id),
  CONSTRAINT reviews_fk_customers
    FOREIGN KEY (customer_id)
    REFERENCES customers (customer_id)
);

-- Insert categories
INSERT INTO categories (category_name) VALUES
('Leafy Greens'),
('Root Vegetables'),
('Fruiting Vegetables'),
('Alliums'),
('Herbs');

-- Insert vendors
INSERT INTO vendors (vendor_name, email_address, password, phone, address) VALUES
('Green Harvest Farms', 'info@greenharvest.com', 'vendorpass1', '555-1001', '123 Farm Rd, Rural Town, CA 90210'),
('Organic Delights Co.', 'contact@organicdelights.com', 'vendorpass2', '555-1002', '456 Garden Ln, Green Acres, OR 97005'),
('Fresh Produce Collective', 'support@freshproduce.net', 'vendorpass3', '555-1003', '789 Market St, Cityville, NY 10001');

-- Insert products
INSERT INTO products (category_id, vendor_id, product_code, product_name, description, unit_price, stock_quantity, date_added) VALUES
(1, 1, 'SPINACH-GHF', 'Organic Spinach', 'Fresh, organic spinach from Green Harvest Farms. Great for salads or cooking.', '3.49', 150, '2024-06-15 10:00:00'),
(1, 2, 'KALE-ODC', 'Lacinato Kale', 'Nutrient-rich Lacinato kale from Organic Delights Co. Perfect for smoothies.', '2.99', 120, '2024-06-16 11:30:00'),
(2, 1, 'CARROTS-GHF', 'Sweet Carrots', 'Crunchy and sweet carrots, ideal for snacking or roasting.', '2.19', 200, '2024-06-15 10:15:00'),
(2, 3, 'POTATOES-FPC', 'Russet Potatoes (5lb)', 'Versatile russet potatoes, great for baking, mashing, or frying.', '4.99', 80, '2024-06-17 09:00:00'),
(3, 1, 'TOMATOES-GHF', 'Vine-Ripened Tomatoes', 'Juicy and flavorful vine-ripened tomatoes, perfect for salads and sauces.', '3.99', 100, '2024-06-18 14:00:00'),
(3, 2, 'CUCUMBER-ODC', 'English Cucumber', 'Long, seedless English cucumbers, refreshing and crisp.', '1.79', 90, '2024-06-18 14:30:00'),
(4, 3, 'GARLIC-FPC', 'Garlic Bulbs (Organic)', 'Pungent organic garlic, essential for many dishes.', '1.29', 300, '2024-06-17 09:15:00'),
(4, 1, 'ONIONS-GHF', 'Yellow Onions (3lb)', 'Common yellow onions, great for cooking bases.', '2.59', 180, '2024-06-15 10:30:00'),
(5, 2, 'BASIL-ODC', 'Fresh Basil Bunch', 'Aromatic fresh basil, perfect for Italian cuisine.', '2.29', 70, '2024-06-19 08:00:00'),
(5, 3, 'PARSLEY-FPC', 'Curly Parsley Bunch', 'Fresh curly parsley, great as a garnish or in cooking.', '1.89', 60, '2024-06-19 08:15:00');

-- Insert customers
INSERT INTO customers (email_address, password, first_name, last_name) VALUES
('alice.smith@example.com', 'password_hash_alice', 'Alice', 'Smith'),
('bob.johnson@example.com', 'password_hash_bob', 'Bob', 'Johnson'),
('carol.davis@example.com', 'password_hash_carol', 'Carol', 'Davis');

-- Insert customer addresses
INSERT INTO addresses (customer_id, line1, line2, city, state, zip_code, phone, is_shipping) VALUES
(1, '123 Main St', NULL, 'Anytown', 'CA', '90210', '555-1111', 1),  -- Alice's shipping
(1, '123 Main St', NULL, 'Anytown', 'CA', '90210', '555-1111', 0),  -- Alice's billing
(2, '456 Oak Ave', 'Apt 10B', 'Otherville', 'NY', '10001', '555-2222', 1),  -- Bob's shipping
(2, '789 Pine Ln', NULL, 'Otherville', 'NY', '10001', '555-2222', 0),  -- Bob's billing
(3, '101 Cedar Blvd', NULL, 'Veggieburg', 'TX', '75001', '555-3333', 1),  -- Carol's shipping
(3, '101 Cedar Blvd', NULL, 'Veggieburg', 'TX', '75001', '555-3333', 0);  -- Carol's billing

-- Insert orders
INSERT INTO orders (customer_id, order_date, shipping_cost, total_amount, delivery_date, shipping_address_id, billing_address_id, payment_method, order_status) VALUES
(1, '2024-07-10 10:00:00', '5.00', '11.48', '2024-07-12 14:30:00', 1, 2, 'Credit Card', 'Shipped'),
(2, '2024-07-11 11:15:00', '3.50', '20.78', '2024-07-13 16:00:00', 3, 4, 'PayPal', 'Processing'),
(3, '2024-07-12 09:30:00', '2.00', '8.57', '2024-07-14 12:00:00', 5, 6, 'Credit Card', 'Pending');

-- Insert order items
INSERT INTO order_items (order_id, product_id, quantity, price_at_order) VALUES
(1, 1, 2, 3.49),
(1, 4, 1, 2.19),
(2, 2, 3, 2.99),
(2, 5, 2, 3.99),
(3, 6, 5, 1.79);

