from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Purchase

router = APIRouter()

# DBセッションを取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/purchase/")
def create_purchase(product_id: int, quantity: int, db: Session = Depends(get_db)):
    new_purchase = Purchase(product_id=product_id, quantity=quantity)
    db.add(new_purchase)
    db.commit()
    return {"message": "購入が完了しました"}
