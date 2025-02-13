from fastapi import APIRouter, HTTPException , Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import ProductMaster

router = APIRouter()
# ✅ ロガー設定（デバッグ用）
logger = logging.getLogger(__name__)

@router.get("/get-product/")
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
