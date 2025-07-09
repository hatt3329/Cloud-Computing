from fastapi import FastAPI, HTTPException, Query, Path, Body
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Guitar Shop API")

# Linking with my database
DATABASE_URL = "mysql+mysqlconnector://root:Ilovedad247%24%21@localhost:3306/my_guitar_shop"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# establishing product model
class ProductDB(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255))
    product_code = Column(String(10))
    description = Column(Text)
    list_price = Column(Float)
    discount_percent = Column(Float)

# the routes

# ping
@app.get("/ping")
def ping():
    return {"message": "pong"}

# product list
@app.get("/products", response_model=List[dict])
def get_products():
    db = SessionLocal()
    products = db.query(ProductDB).all()
    result = [{"id": p.product_id, "name": p.product_name, "price": p.list_price} for p in products]
    db.close()
    return result

# product count
@app.get("/products/count")
def product_count():
    db = SessionLocal()
    count = db.query(ProductDB).count()
    db.close()
    return {"count": count}

#product price
@app.put("/products/{product_id}/price")
def update_price(product_id: int, price: float = Body(...)):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if product:
        product.list_price = price
        db.commit()
        db.refresh(product)
        db.close()
        return {"id": product.product_id, "new_price": product.list_price}
    db.close()
    raise HTTPException(status_code=404, detail="Product not found")
# product name
@app.put("/products/{product_id}/name")
def update_name(product_id: int, name: str = Body(...)):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if product:
        product.product_name = name
        db.commit()
        db.refresh(product)
        db.close()
        return {"id": product.product_id, "new_name": product.product_name}
    db.close()
    raise HTTPException(status_code=404, detail="Product not found")

# price filter for expensive items
@app.get("/products/expensive")
def expensive_products():
    db = SessionLocal()
    products = db.query(ProductDB).filter(ProductDB.list_price >= 1000).all()
    result = [{"id": p.product_id, "name": p.product_name, "price": p.list_price} for p in products]
    db.close()
    return result

# filter by affordability
@app.get("/products/affordable")
def affordable_products():
    db = SessionLocal()
    products = db.query(ProductDB).filter(ProductDB.list_price < 1000).all()
    result = [{"id": p.product_id, "name": p.product_name, "price": p.list_price} for p in products]
    db.close()
    return result

#discounted items
@app.get("/products/discounted")
def discounted_products():
    db = SessionLocal()
    products = db.query(ProductDB).filter(ProductDB.discount_percent > 0).all()
    result = [{"id": p.product_id, "name": p.product_name, "discount": p.discount_percent} for p in products]
    db.close()
    return result


@app.get("/products/{product_id}")
def get_product(product_id: int):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    db.close()
    if product:
        return {"id": product.product_id, "name": product.product_name, "price": product.list_price}
    raise HTTPException(status_code=404, detail="Product not found")

#Discount Update
@app.put("/products/{product_id}/discount")
def update_discount(product_id: int, discount_percent: float = Body(...)):
    db = SessionLocal()
    product = db.query(ProductDB).filter(ProductDB.product_id == product_id).first()
    if product:
        product.discount_percent = discount_percent
        db.commit()
        db.refresh(product)
        db.close()
        return {"id": product.product_id, "new_discount_percent": product.discount_percent}
    db.close()
    raise HTTPException(status_code=404, detail="Product not found")