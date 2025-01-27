from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import or_, func
import logging

from ..database import get_db
from ..models.product import Product
from app.schemas.product import Product as ProductSchema

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()

@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@router.get("/search")
def search_product_by_code(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(
        Product.prd_id == code
    ).first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.prd_id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product 