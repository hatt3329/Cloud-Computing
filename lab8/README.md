# FastAPI Hello World with docker

## Intro

This FastAPI applicationreturns a "Hello, World!" message. It uses Docker containers, which make it easy to run and deploy.

---

## Description

The end goal of this project was to demonstrate how we can FastAPI to make a rest API. It includes:
- A single route that returns a JSON message.
- A working Docker container to encapsulate the API.
- Using docker commands for easy setup

---

## 🛠️ Design of the Project

- Framework: [FastAPI](https://fastapi.tiangolo.com/)
- Language: Python 3.11
- Containerization: Docker
- Dependencies: Installed from `requirements.txt`
- **Entry**: `hello.py`
- **Port**: 8000

---

## How to Run

- Install Docker
- Clone the repository
- Build the docker image:  `docker build -t fastapi-hello`
- Run docker: `docker run -d -p 8000:8000 fastapi-hello`
- Access API with local host: ` http://localhost:8000`


### Structure

- Dockerfile
- hello.py
- requirements.txt


