from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class OrderItemCreate(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=128)
    quantity: int = Field(..., ge=1)
    unit_price: Decimal = Field(..., ge=0)


class OrderCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=128)
    items: List[OrderItemCreate]


class OrderItem(BaseModel):
    id: int
    product_id: str
    quantity: int
    unit_price: Decimal

    model_config = ConfigDict(from_attributes=True)


class Order(BaseModel):
    id: int
    user_id: str
    status: str
    total: Decimal
    items: List[OrderItem]

    model_config = ConfigDict(from_attributes=True)
