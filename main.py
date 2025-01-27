from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth import router as auth_router
from app.routes import products

load_dotenv()

app = FastAPI()

# CORSの設定を強化
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # フロントエンドのURL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(products.router, prefix="/api/products", tags=["products"])

# データベース設定
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

try:
    engine = create_engine(database_url)
except SQLAlchemyError as e:
    print(f"データベース接続エラー: {e}")
    raise

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
        return {"status": "healthy", "database": "connected"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed"
        )

@app.get("/")
async def root():
    return {"message": "Hello World"}