import traceback
import logging
from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from routes import products, transactions
from models import ProductMaster , Transaction , TransactionDetail 
from database import get_db, engine, Base, SessionLocal
from pydantic import BaseModel
from typing import List

# ✅ ロガー設定（print の代わりに使用）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS 設定
origins = [
    "https://tech0-gen8-step4-pos-app-99.azurewebsites.net",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ルーターの登録
router = APIRouter()
app.include_router(products.router)
app.include_router(transactions.router)

# 商品検索 API
@app.get("/get-product/")
def get_product(jan_code: str, db: Session = Depends(get_db)):
    try:
        logger.info(f"🔍 JANコード検索: {jan_code}")

        # 🔹 `strip()` で空白除去
        product = db.query(ProductMaster).filter(ProductMaster.CODE == jan_code.strip()).first()
        logger.info(f"📦 取得した商品: {product}")

        if product:
            response_data = {
                "name": product.NAME,
                "price": product.PRICE
            }
            logger.info(f"🚀 返すデータ: {response_data}")
            return response_data
        else:
            logger.warning("⚠️ 商品が見つかりません")
            return {"error": "商品が見つかりません"}

    except Exception as e:
        logger.error("❌ エラー発生", exc_info=True)
        return HTTPException(status_code=500, detail="エラーが発生しました")


