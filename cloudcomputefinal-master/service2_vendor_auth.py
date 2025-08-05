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
class VendorRegisterModel(BaseModel):
    vendor_name: str
    email_address: str
    password: str
    phone: str
    address: str

class UserLogin(BaseModel):
    email_address: str
    password: str

# --- Routes ---
@app.put("/vendor/register")
async def register_vendor(vendor: VendorRegisterModel):
    mydb = connect_to_db()
    if not mydb:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor()
    try:
        cursor.execute("SELECT * FROM vendors WHERE email_address = %s", (vendor.email_address,))
        if cursor.fetchall():
            raise HTTPException(status_code=400, detail="Email already registered")
        cursor.execute("""
            INSERT INTO vendors (vendor_name, email_address, password, phone, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (vendor.vendor_name, vendor.email_address, vendor.password, vendor.phone, vendor.address))
        mydb.commit()
        return JSONResponse(content={"message": "Vendor registered successfully"})
    except mysql.connector.Error as err:
        print(f"Query error: {err}")
        raise HTTPException(status_code=500, detail="Database error")
    finally:
        cursor.close()
        mydb.close()

@app.put("/vendor/login")
async def vendor_login(user: UserLogin, response: Response):
    mydb = connect_to_db()
    if not mydb:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor = mydb.cursor()
    try:
        cursor.execute("""
            SELECT vendor_id, email_address FROM vendors
            WHERE email_address = %s AND password = %s
        """, (user.email_address, user.password))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        vendor_id, email = result
        token = str(uuid.uuid4())
        session[token] = {
            "vendor_id": vendor_id,
            "email_address": email,
            "user_type": "vendor",
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

