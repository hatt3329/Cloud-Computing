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
            password="Ilovedad247$!",
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
@app.get("/order")
async def get_customer_orders(session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    if not customer_id:
        raise HTTPException(status_code=403, detail="Only customers can view orders")

    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            SELECT 
                oi.order_id,
                p.product_name,
                oi.quantity,
                oi.price_at_order
            FROM 
                order_items oi
            JOIN 
                products p ON oi.product_id = p.product_id
            JOIN 
                orders o ON oi.order_id = o.order_id
            WHERE 
                o.customer_id = %s
        """, (customer_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        mydb.close()
