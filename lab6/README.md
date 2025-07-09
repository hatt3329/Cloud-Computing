Guitar Shop FastAPI Lab 6

Introduction

This project implements a FastAPI-based backend service for managing a Guitar Shop database using MySQL. It demonstrates the creation of a RESTful API capable of interacting with a relational database to retrieve and update product data efficiently.

Project Description:
The Guitar Shop API integrates with a live my_guitar_shop MySQL database using SQLAlchemy ORM. The application provides over 10 API endpoints using GET and PUT HTTP methods, allowing users to:

- Retrieve all product records

- Retrieve individual products by ID

- Retrieve the total count of products

- Filter products by price range and discount status

- Update product prices, names, and discount percentages

The project includes:

- guit_routes.py: The FastAPI application is configured to connect to the MySQL database.

- driver_guit.py: A Python driver script utilizing the requests library to test and validate API functionality.

Project Design

Framework: FastAPI (Python)

Database: MySQL (my_guitar_shop), interfaced via SQLAlchemy ORM

Testing: Python driver script using requests for endpoint testing

Endpoints: Over 10 RESTful API endpoints using GET and PUT methods, employing query strings, path parameters, and JSON payloads for data operations.

Interactive Documentation: Accessible via Swagger UI at http://127.0.0.1:8000/docs.

Detailed Instructions for Running the Project

1. Ensure that a MySQL server is running locally with the my_guitar_shop database and required tables populated.

2. Starting the FastAPI Server:

- Navigate to the directory containing guit_routes.py.

- Execute the following command to launch the FastAPI server: "python -m uvicorn guit_routes:app --reload"


3. Running the Python Driver for Testing

- Open a new terminal in the same directory.

- Execute the following command: "python driver_guit.py"

- The log will display the results of the program

- The terminal that is running the FastAPI server


