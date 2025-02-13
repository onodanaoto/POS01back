from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List
import os

app = FastAPI()

# 環境変数からCORS設定を取得
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "https://tech0-gen8-step4-pos-app-78.azurewebsites.net").split(",")
if not any(CORS_ORIGINS):
    CORS_ORIGINS = ["http://localhost:3000"] if os.getenv("ENV") == "development" else ["https://tech0-gen8-step4-pos-app-78.azurewebsites.net"]

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
@app.get("/products/search")
async def get_product(code: str = Query(...)):
    try:
        db = SessionLocal()
        print(f"Database URL: {os.getenv('DATABASE_URL')}")
        print(f"Searching for product with code: {code}")
        
        product = db.execute(
            "SELECT CODE, NAME, PRICE FROM 商品マスタ WHERE CODE = :code",
            {"code": code}
        ).fetchone()
        
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
            
        print(f"Found product: {product}")
        return {
            "CODE": product.CODE,
            "NAME": product.NAME,
            "PRICE": product.PRICE
        }
    except Exception as e:
        print(f"Error details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# 購入エンドポイント
@app.post("/purchase")
async def purchase(request: dict):
    # 購入処理の実装
    return {"status": "success"} 