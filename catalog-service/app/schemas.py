from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=1024)


class ProductCreate(ProductBase):
    # Allow client to provide explicit id or let DB autogenerate
    id: Optional[int] = None


class Product(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
