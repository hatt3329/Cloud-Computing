from fastapi import FastAPI, Query, HTTPException, Request, Cookie, Header, Depends
from fastapi.responses import FileResponse, JSONResponse, Response
import os, json, mysql.connector, uuid, re
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
from datetime import datetime, timedelta

app = FastAPI()

# uvicorn main:app --reload

#Pydantic Models
#Users/Customers
class UserLogin(BaseModel):
    email_address: str
    password: str

class UserRegister(BaseModel):
    email_address: str
    password: str
    first_name: str
    last_name: str

class UserProfileUpdate(BaseModel):
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

#Vendor
class VendorRegisterModel(BaseModel):
    vendor_name: str
    email_address: str
    password: str
    phone: str
    address: str

class VendorProfileUpdate(BaseModel):
    vendor_name: Optional[str] = None
    email_address: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class VendorAddProduct(BaseModel):
    product_name: str | None = Field(None, max_length=225) 
    product_description: str | None = Field(None) 
    unit_price: Decimal
    stock_quantity: int
    category: str
    
class VendorUpdateProduct(BaseModel):
    product_name: str | None = Field(None, max_length=225) 
    product_description: str | None = Field(None) 
    unit_price: Decimal | None = None
    stock_quantity: int | None = None
    category: str | None = None

#Orders
class OrderCreate(BaseModel):
    shipping_cost: float
    total_amount: float
    delivery_date: str
    shipping_address_id: int
    billing_address_id: int
    payment: str


# --- Establish database connection ---
def connect_to_db():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="my_vegetable_shop"
        )
        print("Successfully connected to MySQL database")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    return mydb

session = {}


#verify helper 
def get_session_data(authorization: str = Header(default=None),session_id: str = Cookie(default=None)):
    print("Header:", authorization)
    print("Cookie:", session_id)

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
        raise HTTPException(status_code=403, detail="Expired session")

    return session_data

# START Customer Register and login 
@app.put("/register")
async def register(user: UserRegister):
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor()
    try:
        sql_query = "SELECT * FROM customers WHERE email_address = %s"
        params = (user.email_address,)
        mycursor.execute(sql_query, params)
        result = mycursor.fetchall()

        if result:  
            raise HTTPException(status_code=400, detail="Email already registered")

        sql_insert = "INSERT INTO customers (email_address, password, first_name, last_name) VALUES (%s, %s, %s, %s)"
        values = (user.email_address, user.password, user.first_name, user.last_name)
        mycursor.execute(sql_insert, values)
        mydb.commit()

        return JSONResponse(content={"message": "User registered successfully"})

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()

@app.put("/login")
async def login(user: UserLogin, response: Response):
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor()
    try:
        sql_query = "SELECT customer_id, email_address FROM customers WHERE email_address = %s AND password = %s"
        params = (user.email_address, user.password)
        mycursor.execute(sql_query, params)
        result = mycursor.fetchone() 

        if not result:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        customer_id, email_address = result

        session_id = str(uuid.uuid4())

        expiration_time = datetime.now() + timedelta(days=1) 
        session[session_id] = {
            "customer_id": customer_id,
            "email_address": email_address,
            "user_type": "customer",
            "expires": expiration_time
        }
        print(f"Session store after login: {session}")

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=60 * 60 * 24
        )
        return {"message": "Login successful",
                "token": session_id}

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()
# ------------------------ END OF USER REGISTER AND LOGIN -----------------------------

#------------------------ START Customer Manangement routes -------------------------

@app.get("/Logout")
async def Logout(request: Request, session_id: Optional[str] = Cookie(None)):
    if not session:
        raise HTTPException(status_code=403, detail="User not logged in")
    
    session_data = session.get(session_id)
    
    if not session_data or datetime.now() > session_data["expires"]:
        if session_data:
            del session[session_id]
        raise HTTPException(status_code=403, detail="expired session")
    

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        if session_id in session:
            del session[session_id]
        return {"message": "Logout successful"}

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()
    
@app.put("/update_user_info/{customer_id}")
def update_user_info(customer_id: str, update_user_info:  UserProfileUpdate): 
    """
    Updates user information from given customer_id
    """
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor(dictionary=True)

    try:
        mycursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        existing_address = mycursor.fetchone()

        if not existing_address:
            raise HTTPException(status_code=404, detail="Address not found")

        update_fields = []
        values = []

        for field, value in update_user_info.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(value)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        sql_query = f"UPDATE customers SET {', '.join(update_fields)} WHERE customer_id = %s"
        values.append(customer_id)

        mycursor.execute(sql_query, tuple(values))
        mydb.commit()

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()
# ---------------------------------   END OF USER MANAGEMENT     ------------------------------------------



# ------------------------------------START OF VENDOR REGISTER AND LOGIN --------------------------------
@app.put("/vendor/register")
async def VendorRegister(user: VendorRegisterModel):
    print(user.model_dump())
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor()
    try:
        sql_query = "SELECT * FROM vendors WHERE email_address = %s"
        params = (user.email_address,)
        mycursor.execute(sql_query, params)
        result = mycursor.fetchall()

        if result:  
            raise HTTPException(status_code=400, detail="Email already registered")

        sql_insert = "INSERT INTO vendors (vendor_name, email_address, password, phone, address) VALUES (%s, %s, %s, %s, %s)"
        values = (user.vendor_name, user.email_address, user.password, user.phone, user.address)
        mycursor.execute(sql_insert, values)
        mydb.commit()

        return JSONResponse(content={"message": "Vendor registered successfully"})

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()

@app.put("/vendor/login")
async def VendorLogin(user: UserLogin, response: Response):
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor()
    try:
        sql_query = "SELECT vendor_id, email_address FROM vendors WHERE email_address = %s AND password = %s"
        params = (user.email_address, user.password)
        mycursor.execute(sql_query, params)
        result = mycursor.fetchone() 

        if not result:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        vendor_id, email_address = result

        session_id = str(uuid.uuid4())

        expiration_time = datetime.now() + timedelta(days=1) 
        session[session_id] = {
            "vendor_id": vendor_id,
            "email_address": email_address,
            "user_type": "vendor",
            "expires": expiration_time
        }
        print(f"Session store after login: {session}")

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=60 * 60 * 24
        )
        return {"message": "Login successful",  
                "token": session_id}

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()

# --------------------- START VENDOR PROFILE UPDATE ------------------------------
@app.put("/update_vendor_info/{vendor_id}")
def update_vendor_info(vendor_id: str, update_user_info:  VendorProfileUpdate):
    """
    Updates user information from given vendor_id
    """
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor(dictionary=True)

    try:
        mycursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
        existing_address = mycursor.fetchone()

        if not existing_address:
            raise HTTPException(status_code=404, detail="Address not found")

        update_fields = []
        values = []

        for field, value in update_user_info.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(value)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        sql_query = f"UPDATE vendors SET {', '.join(update_fields)} WHERE vendor_id = %s"
        values.append(vendor_id)

        mycursor.execute(sql_query, tuple(values))
        mydb.commit()

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()
# ---------------------- END VENDOR PROFILE UPDATE ---------------------------

#VIEW CUSTOMER AND VENDOR PROFILE
@app.get("/profile")
async def view_profile(request: Request, session_data: dict = Depends(get_session_data)):
    user_type = session_data["user_type"]
    user_id = session_data.get("customer_id") or session_data.get("vendor_id")
    
    if user_type == "customer":
        result = get_profile_from_db("customers", "customer_id", session_data["customer_id"])
        return {"profile": {
            "customer_id": result[0],
            "email_address": result[1],
            "first_name": result[3],
            "last_name": result[4]
        }}

    elif user_type == "vendor":
        result = get_profile_from_db("vendors", "vendor_id", session_data["vendor_id"])
        return {"profile": {
            "vendor_id": result[0],
            "vendor_name": result[1],
            "email_address": result[2],
            "phone": result[4],
            "address": result[5]
        }}
    else:
        raise HTTPException(status_code=400, detail="Invalid user type")


#viewprofile helper
def get_profile_from_db(table: str, id_column: str, user_id: str):
    mydb = connect_to_db()
    mycursor = mydb.cursor()
    try:
        sql = f"SELECT * FROM {table} WHERE {id_column} = %s"
        mycursor.execute(sql, (user_id,))
        result = mycursor.fetchone()

        if not result:
            raise HTTPException(status_code=404, detail="Profile not found")

        return result

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()

# -------------------- END VIEW PROFILE ------------------------------

# === SERVICE 3: Product Search (get_all_products, get_product_by_id, filter_products) here ===
from fastapi import Path

@app.get("/products")
def get_all_products():
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        return products
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
        if min_price:
            query += " AND unit_price >= %s"
            params.append(min_price)
        if max_price:
            query += " AND unit_price <= %s"
            params.append(max_price)
        cursor.execute(query, tuple(params))
        return cursor.fetchall()
    finally:
        cursor.close()
        mydb.close()

#-------------------START ADD PRODUCT FROM PROFILE ------------------
@app.put("/addproduct/")
async def addproduct(request: Request, vendor:  VendorAddProduct, session_data: dict = Depends(get_session_data)):
    user_type = session_data["user_type"]
    user_id = session_data.get("customer_id") or session_data.get("vendor_id")

    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor()

    try:
        category_id = 0
        match vendor.category:
            case "":
                category_id = 1
            case "Leafy Greens":
                category_id = 2
            case "Cruciferous":
                category_id = 3
            case "Root Vegetables":
                category_id = 4
            case "Fruit Vegetables":
                category_id = 5
            case "Bulbs & Alliums":
                category_id = 6
            case _:
                category_id = 1
            
        clean_name = re.sub(r'\s+', '-', vendor.product_name.strip().lower())
        unique_suffix = str(uuid.uuid4())[:8]
        product_code = f"{clean_name}-{unique_suffix}"

        CurrentTime = datetime.now()
        sql_insert = "INSERT INTO products (category_id,vendor_id, product_code, product_name, description, unit_price, stock_quantity, date_added) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (category_id, user_id, product_code, vendor.product_name, vendor.product_description, vendor.unit_price, vendor.stock_quantity, CurrentTime)
        mycursor.execute(sql_insert, values)
        mydb.commit()

        return JSONResponse(content={"message": "Product added successfully"})

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()

#-------------------END ADD PRODUCT FROM PROFILE-------------------------------


# ------------------- START VIEW PRODUCTS ASSOCIATED WITH PROFILE -------------------------------
@app.get("/myproducts/")
async def myproducts(request: Request, session_data: dict = Depends(get_session_data)):
    user_type = session_data["user_type"]
    user_id = session_data.get("customer_id") or session_data.get("vendor_id")

    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    mycursor = mydb.cursor()
    try:
        sql_query = "SELECT product_id, product_name, description, unit_price, stock_quantity FROM products WHERE vendor_id = %s"
        params = (user_id,)
        mycursor.execute(sql_query, params)
        result = mycursor.fetchall()
        return result

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        raise HTTPException(status_code=500, detail=f"Database query error: {err}")
    finally:
        mycursor.close()
        mydb.close()
#------------------------END VIEW PRODUCTS ASSOCIATED WITH PROFILE---------------------

# === INSERT SERVICE 5: Reviews (create, delete, edit) here ===
class Review(BaseModel):
    product_id: int
    rating: int
    review_text: Optional[str] = None

@app.put("/review")
def create_review(review: Review, session_data: dict = Depends(get_session_data)):
    customer_id = session_data["customer_id"]
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO reviews (product_id, customer_id, rating, review_text) VALUES (%s, %s, %s, %s)",
                       (review.product_id, customer_id, review.rating, review.review_text))
        mydb.commit()
        return {"message": "Review added"}
    finally:
        cursor.close()
        mydb.close()

@app.delete("/review/{review_id}")
def delete_review(review_id: int, session_data: dict = Depends(get_session_data)):
    
    customer_id = session_data["customer_id"]
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM reviews WHERE review_id = %s AND customer_id = %s", (review_id, customer_id))
        mydb.commit()
        return {"message": "Review deleted"}
    finally:
        cursor.close()
        mydb.close()

@app.put("/review/{review_id}")
def edit_review(review_id: int, updated: Review, session_data: dict = Depends(get_session_data)):
    customer_id = session_data["customer_id"]
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("UPDATE reviews SET rating = %s, review_text = %s WHERE review_id = %s AND customer_id = %s",
                       (updated.rating, updated.review_text, review_id, customer_id))
        mydb.commit()
        return {"message": "Review updated"}
    finally:
        cursor.close()
        mydb.close()

# === INSERT SERVICE 6: Product Management (update/delete product) here ===
@app.put("/product/{product_id}")
def update_product(product_id: int, product: VendorUpdateProduct, session_data: dict = Depends(get_session_data)):
    vendor_id = session_data.get("vendor_id")
    mydb = connect_to_db()

    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = mydb.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM products WHERE product_id = %s AND vendor_id = %s", (product_id, vendor_id))
        existing_product = cursor.fetchone()

        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found or permission denied")

        update_fields = []
        values = []

        for field, value in product.model_dump(exclude_unset=True).items():
            update_fields.append(f"{field} = %s")
            values.append(value)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        sql_query = f"UPDATE products SET {', '.join(update_fields)} WHERE product_id = %s AND vendor_id = %s"
        values.extend([product_id, vendor_id])

        cursor.execute(sql_query, tuple(values))
        mydb.commit()

        return {"message": "Product Successfully updated"}
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
            return {"message": "Other vendors product you have no permission to delete"}
        else:
            return {"message": "Product Successfully deleted"}
    finally:
        cursor.close()
        mydb.close()

# === INSERT SERVICE 7: Shopping Cart (add_to_cart, checkout) here ===
class CartItem(BaseModel):
    product_id: int
    quantity: int

@app.get("/order")
async def get_customer_order(request: Request, session_data: dict = Depends(get_session_data)):
    user_type = session_data["user_type"]
    user_id = session_data.get("customer_id") or session_data.get("vendor_id")
    mydb = connect_to_db()
    if mydb is None:
        raise HTTPException(status_code=500, detail="Database connection failed")
    try:
        cursor = mydb.cursor()
        query = """
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
    o.customer_id = %s;
        """
        cursor.execute(query, (user_id,))
        order_items = cursor.fetchall()
        return order_items
    finally:
        cursor.close()
        mydb.close()

@app.put("/cart")
def add_to_cart(item: CartItem, session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("INSERT INTO shopping_cart (customer_id, product_id, quantity) VALUES (%s, %s, %s)",
                       (customer_id, item.product_id, item.quantity))

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

        shipping_cost = 0.0
        total_amount = 0.0

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
                raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found.")
            
            price, stock_quantity = result

            if quantity > stock_quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product ID {product_id}. Only {stock_quantity} items available.")


            new_stock_quantity = stock_quantity - quantity
            cursor.execute("""
                UPDATE products
                SET stock_quantity = %s
                WHERE product_id = %s
            """, (new_stock_quantity, product_id))

            total_amount = Decimal('0.00')
            total_amount += price * quantity
            # Insert the cart item into the 'order_items' table
            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price_at_order)
                VALUES (%s, %s, %s, %s)
            """, (order_id, product_id, quantity, price))

        cursor.execute("UPDATE orders SET total_amount = %s WHERE order_id = %s", (total_amount, order_id))

        cursor.execute("DELETE FROM shopping_cart WHERE customer_id = %s", (customer_id,))

        mydb.commit()

        return {"message": "Checkout complete", "order_id": order_id}

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback() 
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    finally:
        cursor.close()
        mydb.close()

# === INSERT SERVICE 10: Return Order here ===
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
