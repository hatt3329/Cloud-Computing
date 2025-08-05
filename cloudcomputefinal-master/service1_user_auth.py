from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
import mysql.connector, uuid

app = FastAPI()

# --- Database connection ---
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="my_vegetable_shop"
        )
    except mysql.connector.Error as err:
        print(f"DB connection error: {err}")
        return None

# --- Session store ---
session = {}

# --- Pydantic Models ---
class UserLogin(BaseModel):
    email_address: str
    password: str

class UserRegister(BaseModel):
    email_address: str
    password: str
    first_name: str
    last_name: str

# --- Routes ---
@app.put("/register")
async def register(user: UserRegister):
    mydb = connect_to_db()
    if not mydb:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor()
    try:
        cursor.execute("SELECT * FROM customers WHERE email_address = %s", (user.email_address,))
        if cursor.fetchall():
            raise HTTPException(status_code=400, detail="Email already registered")
        cursor.execute("""
            INSERT INTO customers (email_address, password, first_name, last_name)
            VALUES (%s, %s, %s, %s)
        """, (user.email_address, user.password, user.first_name, user.last_name))
        mydb.commit()
        return JSONResponse(content={"message": "User registered successfully"})
    except mysql.connector.Error as err:
        print(f"Query error: {err}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        mydb.close()

@app.put("/login")
async def login(user: UserLogin, response: Response):
    mydb = connect_to_db()
    if not mydb:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor()
    try:
        cursor.execute("""
            SELECT customer_id, email_address FROM customers
            WHERE email_address = %s AND password = %s
        """, (user.email_address, user.password))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        customer_id, email = result
        token = str(uuid.uuid4())
        session[token] = {
            "customer_id": customer_id,
            "email_address": email,
            "user_type": "customer",
            "expires": datetime.now() + timedelta(days=1)
        }

        response.set_cookie(
            key="session_id",
            value=token,
            httponly=True,
            max_age=86400
        )
        return {"message": "Login successful", "token": token}
    except mysql.connector.Error as err:
        print(f"Login error: {err}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        mydb.close()

