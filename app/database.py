from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from sqlalchemy.exc import SQLAlchemyError

# Baseクラスの定義
Base = declarative_base()

# エンジンの作成（エラーハンドリング追加）
try:
    engine = create_engine(
        os.getenv("DATABASE_URL", "mysql://user:sakepara2025@db:3306/pos_db"),
        pool_size=5,
        max_overflow=10
    )
except SQLAlchemyError as e:
    print(f"データベース接続エラー: {e}")
    raise

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        return db
    except:
        db.close() 