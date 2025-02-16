from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import get_db
from models import Transaction, TransactionDetail
from pydantic import BaseModel
from typing import List
import logging

router = APIRouter()

# ✅ ロギング設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# リクエスト用モデル
class ProductDetail(BaseModel):
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int
    TAX_CD: str

class TransactionCreate(BaseModel):
    EMP_CD: str = "9999999999"
    POS_NO: str = "90"
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int
    TAX_CD: str

# ✅ 修正: `items` を削除し、単体データとして扱う
class TransactionCreate(BaseModel):
    EMP_CD: str = "9999999999"
    POS_NO: str = "90"
    PRD_ID: int
    PRD_CODE: str
    PRD_NAME: str
    PRD_PRICE: int
    TAX_CD: str

# ✅ 取引登録 API
@router.post("/transactions/")
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        # 1-1 取引テーブルへ登録
        new_transaction = Transaction(
            EMP_CD=transaction.EMP_CD,
            STORE_CD="30",  # 固定値
            POS_NO=transaction.POS_NO,
            TOTAL_AMT=0  # 初期値
        )
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)  # TRD_ID を取得
        
        print(f"✅ 取得した TRD_ID: {new_transaction.TRD_ID}")

        # ✅ 1-2 取引明細テーブルへ登録
        # 🔹 同じ TRD_ID の中で最大の DTL_ID を取得し、+1 する
        max_detail_id = db.query(func.coalesce(func.max(TransactionDetail.DTL_ID), 0)).filter(
            TransactionDetail.TRD_ID == new_transaction.TRD_ID
        ).scalar()
        new_detail_id = max_detail_id + 1

        new_detail = TransactionDetail(
            TRD_ID=new_transaction.TRD_ID,  # 取引キー
            DTL_ID=new_detail_id,  # 取引明細一意キー（手動で採番）
            PRD_ID=transaction.PRD_ID,
            PRD_CODE=transaction.PRD_CODE,
            PRD_NAME=transaction.PRD_NAME,
            PRD_PRICE=transaction.PRD_PRICE,
            TAX_CD=transaction.TAX_CD,
            CODE=transaction.PRD_CODE[:2] if transaction.PRD_CODE else "XX",  # ✅ 最初の2文字 or 'XX' をセット
            NAME=transaction.PRD_NAME[:2] if transaction.PRD_NAME else "NA"  # ✅ 商品名の先頭2文字
        )
        db.add(new_detail)
        total_amount = transaction.PRD_PRICE

        # ✅ 1-3 & 1-4 合計金額を計算・取引テーブルを更新
        new_transaction.TOTAL_AMT = total_amount
        db.commit()

        return {"success": True, "total_amount": total_amount}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"エラー: {str(e)}")
