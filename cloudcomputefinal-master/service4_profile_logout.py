from fastapi import FastAPI, HTTPException, Request, Cookie, Header, Depends
import mysql.connector
from datetime import datetime

app = FastAPI()

# --- DB Connection ---
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="my_vegetable_shop"
        )
    except mysql.connector.Error as err:
        print("DB Error:", err)
        return None

# --- Session Store ---
session = {}

# --- Session Helper ---
def get_session_data(authorization: str = Header(default=None), session_id: str = Cookie(default=None)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.replace("Bearer ", "")
    elif session_id:
        token = session_id

    if not token or token not in session:
        raise HTTPException(status_code=403, detail="Authentication required")

    session_data = session[token]
    if datetime.now() > session_data["expires"]:
        del session[token]
        raise HTTPException(status_code=403, detail="Session expired")

    return session_data

# --- Routes ---
@app.get("/Logout")
async def logout(request: Request, session_id: str = Cookie(None)):
    if not session or session_id not in session:
        raise HTTPException(status_code=403, detail="Not logged in or session expired")
    del session[session_id]
    return {"message": "Logout successful"}

@app.get("/profile")
async def view_profile(request: Request, session_data: dict = Depends(get_session_data)):
    user_type = session_data["user_type"]
    user_id = session_data.get("customer_id") or session_data.get("vendor_id")
    
    def get_profile(table, id_col, id_val):
        mydb = connect_to_db()
        cursor = mydb.cursor()
        try:
            cursor.execute(f"SELECT * FROM {table} WHERE {id_col} = %s", (id_val,))
            return cursor.fetchone()
        finally:
            cursor.close()
            mydb.close()

    if user_type == "customer":
        result = get_profile("customers", "customer_id", user_id)
        return {"profile": {
            "customer_id": result[0],
            "email_address": result[1],
            "first_name": result[3],
            "last_name": result[4]
        }}
    elif user_type == "vendor":
        result = get_profile("vendors", "vendor_id", user_id)
        return {"profile": {
            "vendor_id": result[0],
            "vendor_name": result[1],
            "email_address": result[2],
            "phone": result[4],
            "address": result[5]
        }}
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")

