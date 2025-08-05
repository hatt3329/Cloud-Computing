from fastapi import FastAPI, HTTPException, Query
import mysql.connector

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

# --- Routes ---
@app.get("/products")
def get_all_products():
    mydb = connect_to_db()
    if not mydb:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()
    finally:
        cursor.close()
        mydb.close()

@app.get("/product/{product_id}")
def get_product_by_id(product_id: int):
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    finally:
        cursor.close()
        mydb.close()

@app.get("/products/filter")
def filter_products(category: str = Query(None), min_price: float = Query(None), max_price: float = Query(None)):
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if category:
            query += " AND category_id = (SELECT category_id FROM categories WHERE category_name = %s)"
            params.append(category)
        if min_price is not None:
            query += " AND unit_price >= %s"
            params.append(min_price)
        if max_price is not None:
            query += " AND unit_price <= %s"
            params.append(max_price)

        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        mydb.close()

