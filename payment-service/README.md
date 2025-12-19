# payment-service (FastAPI)

FastAPI microservice that simulates payments.

## Endpoints

- `GET /health` – service health check
- `POST /pay` – simulate processing; randomly returns `{ "status": "success" }` or `{ "status": "failed" }`

Request example:

```json
{ "order_id": "123", "amount": 15.49 }
```

## Local Run

```powershell
cd "c:\Users\Dell\OneDrive\Documents\Semester 5\Cloud Computing\Project\payment-service"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Docker

```powershell
docker build -t payment-service:dev .
docker run --rm -p 8000:8000 payment-service:dev
```

Open http://localhost:8000/health
