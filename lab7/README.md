FastAPI Headers and Cookies Lab

Introduction:
This project was made to show how you can work with headers and cookies in a FastAPI app. It’s a small lab project that focuses on sending and receiving these values through simple API routes.

## What This Project Does
This FastAPI service lets you test out how HTTP headers and cookies work. It includes five basic routes:
- One route checks if the server is running (`/ping`).
- Another one reads custom headers sent by the client.
- There’s a route to set cookies, and another to read them.
- The last route shows how you can use both headers and cookies in one request.

There’s also a Python script (`cookie_driver.py`) that acts as a test client. It sends requests to each of the routes so you can see the results in your terminal.

There are five routes total:
- `/ping`: Just makes sure the server is working.
- `/get-header`: Reads a header value you send in.
- `/set-cookie`: Sets a cookie in your browser or client.
- `/get-cookie`: Pulls the cookie back out and shows you what’s there.
- `/header-and-cookie`: Combines both headers and cookies in one route.

##How to Run Everything
- In one console, run the fastAPI app: `python -m uvicorn cookie:app --reload`
- You should see that the fastAPI server is now functioning
- Create a 2nd terminal and call the python driver: python cookie_driver.py
- This will the display the results of all 5 routes




