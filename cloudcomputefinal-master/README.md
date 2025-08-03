# Online Vegetable Storefront

## Introduction

This is a web-based storefront API designed for an online vegetable vendor, enabling customers and vendors to interact through a fast and secure platform. Built with **FastAPI** and **MySQL**, it supports customer registration, product browsing, order management, vendor administration, and more. The system includes both a backend API (`main.py`) and a CLI-based client (`driver.py`) for interacting with the application.

---

## Project Description

This project acts full-featured e-commerce system tailored to a vegetable shop. It includes:

- **Customer features**: registration, login, profile management, product browsing, reviews, shopping cart, and checkout.
- **Vendor features**: product management, profile updates, and inventory control.
- **Admin features** (implicit via DB setup): database-backed session handling and return processing.

The backend exposes RESTful endpoints with FastAPI, while a MySQL database stores all persistent data. Interaction and testing can be done through the command-line `driver.py`.

---

## Project Design

### Components

- **Database Schema** (`Script.sql`)
  - Tables: `customers`, `vendors`, `products`, `orders`, `order_items`, `reviews`, `addresses`, `categories`, `shopping_cart`
  - Sample data is included for vendors, products, and customers

- **Backend API** (`main.py`)
  - Developed using **FastAPI**
  - Handles:
    - User/vendor login & registration
    - Profile management
    - Product search, filter, and management
    - Review operations
    - Cart and order processing
    - Order returns

- **Client CLI Interface** (`driver.py`)
  - Interactive menu for testing all endpoints
  - Handles sessions, login tokens, and routes

---

## How to Run

### Requirements

Make sure you have installed:

- Python 3.10+
- MySQL Server
- Python packages: (`pip install fastapi uvicorn requests mysql-connector-python`)

### How to run

- Set up the Database: (`mysql -u root -p < Script.sql`)
- Start Fast API Backend from Root: (`uvicorn main:app --reload`)
- Run the Client Interface: (`python driver.py`)

### Services

## User Registration & Login
- `PUT /register` – Register a new customer.
- `PUT /login` – Log in as a customer.

## Vendor Registration & Login
- `PUT /vendor/register` – Register a new vendor.
- `PUT /vendor/login` – Log in as a vendor.

## Profile Management
- `GET /profile` – View current profile (customer or vendor).
- `PUT /update_user_info/{customer_id}` – Update customer profile.
- `PUT /update_vendor_info/{vendor_id}` – Update vendor profile.

## Logout
- `GET /Logout` – End the current session and log out.

## Product Search
- `GET /products` – View all products.
- `GET /product/{product_id}` – View details for a specific product.
- `GET /products/filter` – Filter products by category or price.

## Product Management (Vendor Only)
- `PUT /addproduct` – Add a new product.
- `GET /myproducts` – View vendor’s products.
- `PUT /product/{product_id}` – Update an existing product.
- `DELETE /product/{product_id}` – Delete a product.

## Review Services (Customer Only)
- `PUT /review` – Create a product review.
- `PUT /review/{review_id}` – Edit a review.
- `DELETE /review/{review_id}` – Delete a review.

## Shopping Cart & Checkout
- `PUT /cart` – Add an item to the cart.
- `PUT /checkout` – Complete purchase and create order.

## Orders & Returns
- `GET /order` – View past customer orders.
- `PUT /return/{order_id}` – Return an order.



### Structure

- main.py         # FastAPI backend with all endpoints
- driver.py       # CLI test interface using requests
- Script.sql      # MySQL schema and seed data
- README.md       # Project documentation
