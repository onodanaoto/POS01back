from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Azure MySQL用の接続文字列（SSL設定を追加）
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://Tech0Gen8TA4:sakepara2025@tech0-gen-8-step4-db-4.mysql.database.azure.com:3306/pos_db?ssl=true"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ssl_ca": "/etc/ssl/certs/ca-certificates.crt"
        }
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 