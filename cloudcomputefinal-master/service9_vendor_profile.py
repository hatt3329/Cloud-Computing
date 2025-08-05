from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
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

# --- Model ---
class VendorProfileUpdate(BaseModel):
    vendor_name: Optional[str] = None
    email_address: Optional[str] = None
    password: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# --- Route ---
@app.put("/update_vendor_info/{vendor_id}")
def update_vendor_info(vendor_id: str, update: VendorProfileUpdate):
    mydb = connect_to_db()
    if not mydb:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = mydb.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM vendors WHERE vendor_id = %s", (vendor_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Vendor not found")

        fields = []
        values = []
        for field, value in update.model_dump(exclude_unset=True).items():
            fields.append(f"{field} = %s")
            values.append(value)

        if not fields:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        values.append(vendor_id)
        query = f"UPDATE vendors SET {', '.join(fields)} WHERE vendor_id = %s"
        cursor.execute(query, tuple(values))
        mydb.commit()

        return {"message": "Vendor profile updated successfully"}
    finally:
        cursor.close()
        mydb.close()
