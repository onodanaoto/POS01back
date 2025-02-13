from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
import os

app = FastAPI()

# 環境変数からCORS設定を取得
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "POS System API"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 商品検索エンドポイント
@app.get("/products/{code}")
async def get_product(code: str):
    try:
        db = SessionLocal()
        print(f"Database URL: {os.getenv('DATABASE_URL')}")  # デバッグ用
        # デバッグ用にクエリを出力
        print(f"Searching for product with code: {code}")
        
        # 商品マスタから商品を検索
        product = db.execute(
            "SELECT CODE, NAME, PRICE FROM 商品マスタ WHERE CODE = :code",
            {"code": code}
        ).fetchone()
        
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
            
        # デバッグ用に結果を出力
        print(f"Found product: {product}")
            
        return {
            "CODE": product.CODE,
            "NAME": product.NAME,
            "PRICE": product.PRICE
        }
    except Exception as e:
        print(f"Error details: {str(e)}")  # デバッグ用
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# 購入エンドポイント
@app.post("/purchase")
async def purchase(request: dict):
    # 購入処理の実装
    return {"status": "success"} 