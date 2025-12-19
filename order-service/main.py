import os
from decimal import Decimal
from typing import Generator, List

import httpx
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine, Base
from app import models
from app.schemas import OrderCreate, Order


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="0.1.0")

# Allow CORS for local frontend/testing; tighten in production
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


def get_db() -> Generator[Session, None, None]:
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


@app.get("/health")
async def health():
	return {"status": "ok", "service": "order-service"}


async def confirm_payment(total: Decimal, user_id: str) -> bool:
	"""Mock payment confirmation.

	If PAYMENT_URL env var is set, POST to it with { user_id, amount }.
	Otherwise, simulate success.
	"""
	payment_url = os.getenv("PAYMENT_URL")
	if not payment_url:
		return True  # mock success

	try:
		async with httpx.AsyncClient(timeout=5.0) as client:
			resp = await client.post(payment_url, json={"user_id": user_id, "amount": str(total)})
			return resp.status_code == 200
	except Exception:
		return False


@app.post("/orders", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
	if not payload.items:
		raise HTTPException(status_code=400, detail="Order must contain at least one item")

	# Calculate total
	total = Decimal("0")
	for it in payload.items:
		# Pydantic gave Decimal for unit_price; ensure non-negative
		if it.unit_price < 0:
			raise HTTPException(status_code=400, detail="unit_price must be >= 0")
		total += it.unit_price * it.quantity

	# Create order with PENDING status
	order = models.Order(user_id=payload.user_id, status="PENDING", total=total)
	for it in payload.items:
		order.items.append(
			models.OrderItem(
				product_id=it.product_id,
				quantity=it.quantity,
				unit_price=it.unit_price,
			)
		)

	try:
		db.add(order)
		db.commit()
		db.refresh(order)
	except Exception as e:
		db.rollback()
		raise HTTPException(status_code=400, detail=f"Failed to create order: {e}")

	# Confirm payment via mock/HTTP call
	ok = await confirm_payment(total=order.total, user_id=order.user_id)
	order.status = "CONFIRMED" if ok else "FAILED"
	db.add(order)
	db.commit()
	db.refresh(order)
	if not ok:
		# Surface that payment failed but return the created order state
		# Client can inspect status field
		pass

	return order


@app.get("/orders", response_model=List[Order])
async def list_orders(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
	q = db.query(models.Order).order_by(models.Order.id.desc()).offset(offset).limit(limit)
	orders = q.all()
	return orders
