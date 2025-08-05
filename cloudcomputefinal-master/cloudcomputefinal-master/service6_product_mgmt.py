from fastapi import FastAPI, HTTPException, Depends, Header, Cookie
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
import mysql.connector, uuid, re

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
class VendorAddProduct(BaseModel):
    product_name: str | None = Field(None, max_length=225)
    product_description: str | None = None
    unit_price: Decimal
    stock_quantity: int
    category: str

class VendorUpdateProduct(BaseModel):
    product_name: str | None = Field(None, max_length=225)
    product_description: str | None = None
    unit_price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    category: Optional[str] = None

# --- Routes ---
@app.put("/addproduct")
async def add_product(product: VendorAddProduct, session_data: dict = Depends(get_session_data)):
    vendor_id = session_data.get("vendor_id")
    category_id = 1
    match product.category:
        case "Leafy Greens": category_id = 1
        case "Cruciferous": category_id = 2
        case "Root Vegetables": category_id = 3
        case "Fruit Vegetables": category_id = 4
        case "Bulbs & Alliums": category_id = 5
        case _: category_id = 1

    clean_name = re.sub(r'\s+', '-', product.product_name.strip().lower())
    product_code = f"{clean_name}-{str(uuid.uuid4())[:8]}"

    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            INSERT INTO products (category_id, vendor_id, product_code, product_name, description, unit_price, stock_quantity, date_added)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (category_id, vendor_id, product_code, product.product_name, product.product_description,
              product.unit_price, product.stock_quantity, datetime.now()))
        mydb.commit()
        return {"message": "Product added successfully"}
    finally:
        cursor.close()
        mydb.close()

@app.get("/myproducts")
async def my_products(session_data: dict = Depends(get_session_data)):
    vendor_id = session_data.get("vendor_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            SELECT product_id, product_name, description, unit_price, stock_quantity
            FROM products WHERE vendor_id = %s
        """, (vendor_id,))
        return cursor.fetchall()
    finally:
        cursor.close()
        mydb.close()

@app.put("/product/{product_id}")
def update_product(product_id: int, product: VendorUpdateProduct, session_data: dict = Depends(get_session_data)):
    vendor_id = session_data.get("vendor_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE product_id = %s AND vendor_id = %s", (product_id, vendor_id))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found or access denied")

        updates = []
        values = []
        for field, value in product.model_dump(exclude_unset=True).items():
            updates.append(f"{field} = %s")
            values.append(value)

        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")

        values.extend([product_id, vendor_id])
        cursor.execute(f"UPDATE products SET {', '.join(updates)} WHERE product_id = %s AND vendor_id = %s", tuple(values))
        mydb.commit()
        return {"message": "Product updated"}
    finally:
        cursor.close()
        mydb.close()

@app.delete("/product/{product_id}")
def delete_product(product_id: int, session_data: dict = Depends(get_session_data)):
    vendor_id = session_data.get("vendor_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s AND vendor_id = %s", (product_id, vendor_id))
        mydb.commit()
        if cursor.rowcount == 0:
            return {"message": "No permission to delete this product"}
        return {"message": "Product deleted"}
    finally:
        cursor.close()
        mydb.close()
