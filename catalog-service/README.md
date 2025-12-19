# catalog-service (FastAPI)

FastAPI microservice for a Product Catalog using SQLite + SQLAlchemy.

## Endpoints

- `GET /health` – service health check
- `GET /products` – list all products
- `POST /products` – create a product (body: `{ id?, name, price, description? }`)

## Local Run

```bash
python -m venv .venv
.venv\Scripts\activate  # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

SQLite file: `catalog.db` in the service directory.

## Docker

```bash
docker build -t catalog-service:dev .
docker run --rm -p 8000:8000 catalog-service:dev
```

Open: http://localhost:8000/health
