from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    trd_id = Column(Integer, primary_key=True, autoincrement=True)
    datetime = Column(DateTime, nullable=False, default=func.now())
    emp_cd = Column(String(10), nullable=False)
    store_cd = Column(String(5), nullable=False)
    pos_no = Column(String(3), nullable=False)
    total_amt = Column(Integer, nullable=False, default=0)

    # リレーションシップ
    details = relationship("TransactionDetail", back_populates="transaction") 
