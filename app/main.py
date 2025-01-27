from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .routes import products
import logging
import sys

# ロギングの設定
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI()

# CORSの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ミドルウェアでリクエスト/レスポンスをログ
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger = logging.getLogger("api")
    logger.debug(f"Request path: {request.url.path}")
    logger.debug(f"Request query params: {request.query_params}")
    
    response = await call_next(request)
    
    logger.debug(f"Response status: {response.status_code}")
    return response

# ルーターの登録
app.include_router(products.router, prefix="/api/products", tags=["products"]) 