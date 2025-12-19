# order-service (FastAPI)

FastAPI microservice for Orders using SQLite + SQLAlchemy. Creates an order, calculates total, saves with `PENDING`, mocks payment, and updates status to `CONFIRMED` or `FAILED`.

## Endpoint

- `POST /orders` – create an order

Request body:

```json
{
  "user_id": "john",
  "items": [
    { "product_id": "sku-1", "quantity": 2, "unit_price": 9.99 },
    { "product_id": "sku-2", "quantity": 1, "unit_price": 5.5 }
  ]
}
```

Response body includes `id`, `status`, `total`, and `items`.

Payment mock: if `PAYMENT_URL` env var is set, the service will `POST` `{ user_id, amount }` to it and treat HTTP 200 as success. Otherwise, payment is assumed to succeed.

## Local Run

```powershell
cd "c:\Users\Dell\OneDrive\Documents\Semester 5\Cloud Computing\Project\order-service"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Optionally set a payment URL:

```powershell
$env:PAYMENT_URL = "http://localhost:8081/pay"
```

## Docker

```powershell
docker build -t order-service:dev .
docker run --rm -p 8000:8000 order-service:dev
```

Open http://localhost:8000/health
