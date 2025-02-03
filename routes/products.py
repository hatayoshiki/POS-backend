from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Product

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-product/")
def get_product(jan_code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.jan_code == jan_code).first()
    if product:
        return {"jan_code": product.jan_code, "name": product.name, "price": product.price}
    return {"error": "商品がマスタ未登録です"}
