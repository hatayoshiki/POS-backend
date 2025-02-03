import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env ファイルの読み込み
load_dotenv()

# MySQL の接続情報を環境変数から取得
DATABASE_URL = os.getenv("DATABASE_URL")

# MySQL の設定
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL が .env に設定されていません")

# SQLAlchemy のエンジンを作成
engine = create_engine(DATABASE_URL, echo=True)

# セッションを作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースモデル
Base = declarative_base()
