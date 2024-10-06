from pydantic import BaseModel
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(ItemCreate):
    id: int
    deleted: bool

    class ConfigDict:
        from_attributes = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

class ItemCartResponse(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

class ItemCreatedResponse(BaseModel):
    id: int

class CartResponse(ItemCreatedResponse):
    items: list[ItemCartResponse]
    price: float
