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

# ✅ ルーターの登録
router = APIRouter()
app.include_router(products.router)
app.include_router(transactions.router)


