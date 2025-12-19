import random
from decimal import Decimal
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


class PayRequest(BaseModel):
	order_id: str = Field(..., min_length=1)
	amount: Decimal = Field(..., ge=0)


app = FastAPI(title="Payment Service", version="0.1.0")


@app.get("/health")
async def health():
	return {"status": "ok", "service": "payment-service"}


@app.post("/pay")
async def pay(req: PayRequest):
	result = random.choice(["success", "failed"])  # simulate gateway
	return {"status": result, "order_id": req.order_id, "amount": str(req.amount)}
