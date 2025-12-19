from sqlalchemy import Column, Integer, String, UniqueConstraint
from .db import Base


class CartItem(Base):
    __tablename__ = "cart_items"
    __table_args__ = (
        UniqueConstraint("user_id", "product_id", name="uq_user_product"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(128), index=True, nullable=False)
    product_id = Column(String(128), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
