from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 許可するフロントエンドの URL
origins = [
    "https://tech0-gen8-step4-pos-app-99.azurewebsites.net",  # フロントエンドのURL
    "http://localhost:3000"  # ローカル開発時（必要なら追加）
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジン
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可（GET, POST など）
    allow_headers=["*"],  # すべてのヘッダーを許可
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI"}
