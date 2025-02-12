import os
import sqlalchemy
import urllib.parse
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# .env を明示的に指定して読み込む
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# 環境変数を取得
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "3306")  # デフォルトを 3306 に設定
DB_NAME = os.getenv("DB_NAME")
DB_SSL_CA = os.getenv("DB_SSL_CA")

# 必須環境変数のチェック（ない場合はエラーを出す）
required_vars = {"DB_USER", "DB_PASSWORD", "DB_HOST", "DB_NAME", "DB_SSL_CA"}
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    raise EnvironmentError(f"⚠ 環境変数が不足しています: {', '.join(missing_vars)}")

# DBモデルのベースクラス（`declarative_base()` の二重定義を削除）
Base = declarative_base()

# パスワードをURLエンコード
encoded_password = quote_plus(DB_PASSWORD)

# SQLAlchemy の接続URLを作成
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}?ssl_ca={DB_SSL_CA}"
)

# 証明書ファイルが存在するかチェック
if not os.path.exists(DB_SSL_CA):
    raise FileNotFoundError(f"⚠ SSL証明書が見つかりません: {DB_SSL_CA}")

# デバッグ出力（本番環境ではコメントアウト）
print("Connecting to database:", SQLALCHEMY_DATABASE_URL)

# SQLAlchemyの設定
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)  # `echo=True` で SQL をログ出力

# セッション作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import models

# FastAPIの依存関係として `get_db` を定義
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
