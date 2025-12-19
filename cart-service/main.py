from typing import List, Generator
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine, Base
from app import models
from app.schemas import CartItem, CartItemCreate


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cart Service", version="0.1.0")


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.get("/health")
async def health():
	return {"status": "ok", "service": "cart-service"}


@app.get("/cart/{user_id}", response_model=List[CartItem])
def get_cart(user_id: str, db: Session = Depends(get_db)):
	items = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).all()
	return items


@app.post("/cart/{user_id}", response_model=CartItem, status_code=status.HTTP_201_CREATED)
def add_item(user_id: str, payload: CartItemCreate, db: Session = Depends(get_db)):
	# Upsert: if item exists, increment quantity
	item = (
		db.query(models.CartItem)
		.filter(
			models.CartItem.user_id == user_id,
			models.CartItem.product_id == payload.product_id,
		)
		.first()
	)
	if item:
		item.quantity += payload.quantity
	else:
		item = models.CartItem(
			user_id=user_id,
			product_id=payload.product_id,
			quantity=payload.quantity,
		)
		db.add(item)
	try:
		db.commit()
		db.refresh(item)
		return item
	except Exception as e:
		db.rollback()
		raise HTTPException(status_code=400, detail=str(e))


@app.delete("/cart/{user_id}")
def clear_cart(user_id: str, db: Session = Depends(get_db)):
	deleted = (
		db.query(models.CartItem)
		.filter(models.CartItem.user_id == user_id)
		.delete(synchronize_session=False)
	)
	db.commit()
	return {"deleted": deleted}
