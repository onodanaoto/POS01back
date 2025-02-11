from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List

app = FastAPI()

# CORSミドルウェアの設定を修正
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://tech0-gen8-step4-pos-app-77.azurewebsites.net"  # フロントエンドのURL
    ],
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
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
    db = SessionLocal()
    try:
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
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# 購入エンドポイント
@app.post("/purchase")
async def purchase(request: dict):
    # 購入処理の実装
    return {"status": "success"} 