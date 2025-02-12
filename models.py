from sqlalchemy import Column, Integer, String, CHAR ,ForeignKey, TIMESTAMP, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base

class ProductMaster(Base):
    __tablename__ = "m_product_yoshiki_products"

    PRD_ID = Column(Integer, primary_key=True, autoincrement=True)
    CODE = Column(String(13), unique=True, nullable=False) 
    NAME = Column(String(50), nullable=False)
    PRICE = Column(Integer, nullable=False)

# 取引テーブル（m_product_yoshiki_transactions）
class Transaction(Base):
    __tablename__ = "m_product_yoshiki_transactions"

    TRD_ID = Column(Integer, primary_key=True, autoincrement=True)  # 取引一意キー
    DATETIME = Column(TIMESTAMP, server_default=func.current_timestamp())  # 取引日時（現在日時）
    EMP_CD = Column(String(10), default="9999999999", nullable=False)  # レジ担当者コード
    STORE_CD = Column(String(5), default="30", nullable=False)  # 店舗コード（固定値 '30'）
    POS_NO = Column(String(3), default="90", nullable=False)  # POS機ID（固定値 '90'）
    TOTAL_AMT = Column(Integer, default=0, nullable=False)  # 合計金額

    details = relationship("TransactionDetail", back_populates="transaction", cascade="all, delete")

# 取引明細テーブル（m_product_yoshiki_transaction_details）
class TransactionDetail(Base):
    __tablename__ = "m_product_yoshiki_transaction_details"

    DTL_ID = Column(Integer, primary_key=True, autoincrement=True)  # ✅ 自動インクリメントを追加
    TRD_ID = Column(Integer, ForeignKey("m_product_yoshiki_transactions.TRD_ID"), nullable=False)
    PRD_ID = Column(Integer, nullable=False)
    PRD_CODE = Column(String(13), nullable=False)
    PRD_NAME = Column(String(50), nullable=False)
    PRD_PRICE = Column(Integer, nullable=False)
    TAX_CD = Column(String(2), nullable=False)
    CODE = Column(String(2), nullable=False, default="XX")  # ✅ CODE のデフォルト値
    NAME = Column(String(20), nullable=False, default="NA")  # ✅ NAME のデフォルト値 

    transaction = relationship("Transaction", back_populates="details")