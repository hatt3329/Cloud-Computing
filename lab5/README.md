# Lab 5 - Python Database Queries

# Intro

This is my work for lab 5, where we are taking the SQL queries we made in lab 4 and converting them over to code python along with constructing unit tests for them.


# Description

Instead of making 7 separate files, I decied to combine all of them into one single python file with the following queries.
 - showing products by price
 - displaying customers with last names M through Z
 - displaying items with prices between 500 and 2000
 - displaying items greater than 500 dollars
 - the joining of products and categories
 - displaying customer email addresses
 - grabbing shipping address

# Design

- Database: `my_guitar_shop` (tables like `products`, `customers`, `orders`, etc.)
- Python file: I combined all the queries into 1 python file (`guitar_db_queries.py`) for easier testing and accessibility.
- DBeaver: Used to test and visualize queries before coding them.

# How to use

- Ensure the SQL python connector is installed ("pip install mysql-connector-python")
- ensure the connections settings under DB_CONFIG line up with your local version of the guitar database
- run the python file ("python db_queries.py")
- you should recieve a terminal response with time the test took along with with confirmation each test was successful
 
 
