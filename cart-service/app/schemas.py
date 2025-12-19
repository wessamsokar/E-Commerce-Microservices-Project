from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CartItemBase(BaseModel):
    product_id: str = Field(..., min_length=1, max_length=128)
    quantity: int = Field(1, ge=1)


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: int
    user_id: str

    model_config = ConfigDict(from_attributes=True)
