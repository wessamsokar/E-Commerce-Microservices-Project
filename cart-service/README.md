# cart-service (FastAPI)

FastAPI microservice for a Shopping Cart using SQLite + SQLAlchemy.

## Endpoints

- `GET /health` – service health check
- `GET /cart/{user_id}` – list all items in a user's cart
- `POST /cart/{user_id}` – add item to cart (upsert by product_id)
- `DELETE /cart/{user_id}` – clear user's cart

Request example (POST /cart/john):

```json
{ "product_id": "sku-123", "quantity": 2 }
```

## Local Run

```powershell
cd "c:\Users\Dell\OneDrive\Documents\Semester 5\Cloud Computing\Project\cart-service"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Docker

```powershell
docker build -t cart-service:dev .
docker run --rm -p 8000:8000 cart-service:dev
```

Open http://localhost:8000/health
