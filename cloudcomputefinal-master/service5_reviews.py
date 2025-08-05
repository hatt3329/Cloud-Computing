from fastapi import FastAPI, HTTPException, Depends, Header, Cookie
from pydantic import BaseModel
from typing import Optional
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

# --- Models ---
class Review(BaseModel):
    product_id: int
    rating: int
    review_text: Optional[str] = None

# --- Routes ---
@app.put("/review")
def create_review(review: Review, session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            INSERT INTO reviews (product_id, customer_id, rating, review_text)
            VALUES (%s, %s, %s, %s)
        """, (review.product_id, customer_id, review.rating, review.review_text))
        mydb.commit()
        return {"message": "Review added"}
    finally:
        cursor.close()
        mydb.close()

@app.put("/review/{review_id}")
def edit_review(review_id: int, updated: Review, session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("""
            UPDATE reviews
            SET rating = %s, review_text = %s
            WHERE review_id = %s AND customer_id = %s
        """, (updated.rating, updated.review_text, review_id, customer_id))
        mydb.commit()
        return {"message": "Review updated"}
    finally:
        cursor.close()
        mydb.close()

@app.delete("/review/{review_id}")
def delete_review(review_id: int, session_data: dict = Depends(get_session_data)):
    customer_id = session_data.get("customer_id")
    mydb = connect_to_db()
    try:
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM reviews WHERE review_id = %s AND customer_id = %s", (review_id, customer_id))
        mydb.commit()
        return {"message": "Review deleted"}
    finally:
        cursor.close()
        mydb.close()