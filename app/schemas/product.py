from pydantic import BaseModel

class Product(BaseModel):
    prd_id: int
    code: str
    name: str
    price: int
    quantity: int = 0

    class Config:
        from_attributes = True 