from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class TransactionDetail(Base):
    __tablename__ = "transaction_details"

    trd_id = Column(Integer, ForeignKey("transactions.trd_id"), primary_key=True)
    dtl_id = Column(Integer, primary_key=True, autoincrement=True)
    prd_id = Column(Integer, ForeignKey("products.prd_id"), nullable=False)
    prd_code = Column(String(13), nullable=False)
    prd_name = Column(String(50), nullable=False)
    prd_price = Column(Integer, nullable=False)

    # リレーションシップ
    transaction = relationship("Transaction", back_populates="details")
    product = relationship("Product") 