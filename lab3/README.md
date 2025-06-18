# Lab 3 - FastAPI Application

## Introduction
This lab demonstrates a FastAPI application with multiple routes and a Python driver script to interact with the API. I created a barebones to-do list where tasks can be created , updated, searched, marked complete/incomplete, counted, and deleted. 

## Description
The app includes simulates a task manager with features like the ability to mark tasks complete/incomplete, searching by title, adding tasks, task counting and filtering, and includes program interaction with Python driver script

## Design
- main.py: FastAPI server
- driver.py: Python client
- Routes use parameterized input styles and JSON responses

## Instructions
1. Run the server in terminal:
   uvicorn main:app --reload
2. Run driver in secondary bash:
   python driver.py
3. GUI will appear
