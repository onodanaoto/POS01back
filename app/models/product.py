from sqlalchemy import Column, Integer, String
from ..database import Base

class Product(Base):
    __tablename__ = "products"

    prd_id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(13), unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False) 