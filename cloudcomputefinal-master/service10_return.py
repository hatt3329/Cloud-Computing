from fastapi import FastAPI, HTTPException, Depends, Header, Cookie
from datetime import datetime
import mysql.connector

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

# --- Route ---
@app.put("/return/{order_id}")
def return_order(order_id: int, session_data: dict = Depends(get_session_data)):
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("UPDATE orders SET order_status = 'Returned' WHERE order_id = %s", (order_id,))
        mydb.commit()
        return {"message": f"Order {order_id} marked as returned"}
    finally:
        cursor.close()
        mydb.close()

