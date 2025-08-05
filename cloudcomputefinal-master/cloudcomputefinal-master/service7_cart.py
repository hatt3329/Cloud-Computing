from fastapi import FastAPI, HTTPException, Depends, Header, Cookie
from pydantic import BaseModel
from datetime import datetime, timedelta
from decimal import Decimal
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

# --- Models ---
class CartItem(BaseModel):
    product_id: int
    quantity: int

# --- Routes ---
@app.put("/cart")
def add_to_cart(item: CartItem, session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            INSERT INTO shopping_cart (customer_id, product_id, quantity)
            VALUES (%s, %s, %s)
        """, (customer_id, item.product_id, item.quantity))
        mydb.commit()
        return {"message": "Item added to cart"}
    finally:
        cursor.close()
        mydb.close()

@app.put("/checkout")
def checkout(session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT product_id, quantity FROM shopping_cart WHERE customer_id = %s", (customer_id,))
        cart_items = cursor.fetchall()
        if not cart_items:
            raise HTTPException(status_code=400, detail="Cart is empty")

        now = datetime.now()
        shipping_cost = Decimal("0.00")
        total_amount = Decimal("0.00")

        cursor.execute("""
            INSERT INTO orders (customer_id, order_date, shipping_cost, total_amount, delivery_date,
            shipping_address_id, billing_address_id, payment_method, order_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Processing')
        """, (customer_id, now, shipping_cost, total_amount, now + timedelta(days=5), 1, 1, 'Credit Card'))
        order_id = cursor.lastrowid

        for product_id, quantity in cart_items:
            cursor.execute("SELECT unit_price, stock_quantity FROM products WHERE product_id = %s", (product_id,))
            result = cursor.fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail=f"Product ID {product_id} not found")
            price, stock_quantity = result
            if quantity > stock_quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product ID {product_id}")

            new_stock_quantity = stock_quantity - quantity
            cursor.execute("UPDATE products SET stock_quantity = %s WHERE product_id = %s", (new_stock_quantity, product_id))
            total_amount += price * quantity
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, price))

        cursor.execute("UPDATE orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))
        cursor.execute("DELETE FROM shopping_cart WHERE customer_id = %s", (customer_id,))
        mydb.commit()

        return {"message": "Checkout complete", "order_id": order_id}
    except mysql.connector.Error as err:
        mydb.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        mydb.close()
