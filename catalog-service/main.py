from typing import List, Generator
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import SessionLocal, engine, Base
from app import models
from app.schemas import Product, ProductCreate

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Catalog Service", version="0.1.0")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "catalog-service"}


@app.get("/products", response_model=List[Product])
def list_products(db: Session = Depends(get_db)):
    items = db.query(models.Product).all()
    return items


@app.post("/products", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    # If client provides an explicit ID, attempt to use it
    product = models.Product(
        id=payload.id,
        name=payload.name,
        price=payload.price,
        description=payload.description,
    )
    try:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
