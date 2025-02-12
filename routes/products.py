from fastapi import APIRouter, HTTPException , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ProductMaster

router = APIRouter()

# DB セッションを取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 商品検索 API
@router.get("/get-product/")
def get_product(jan_code: str, db: Session = Depends(get_db)):
    product = db.query(ProductMaster).filter(ProductMaster.CODE == jan_code).first()

    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

    return {
        "PRD_ID": product.PRD_ID,
        "CODE": product.CODE,
        "NAME": product.NAME,
        "PRICE": product.PRICE
    }