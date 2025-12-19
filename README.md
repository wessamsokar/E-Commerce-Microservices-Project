# E-commerce Microservices Monorepo

This repository contains a minimal, runnable scaffold for an e-commerce system using microservices.

## Structure

- catalog-service: Product catalog API (FastAPI + SQLite)
- cart-service: Shopping cart API (Node.js/Express)
- order-service: Order management API (Node.js/Express)
- payment-service: Payment API (Node.js/Express)
- frontend: Static site served via Nginx
- k8s-manifests: Kubernetes Deployments/Services and namespace

## Quickstart (local)

Most services use Node.js/Express; `catalog-service` uses Python/FastAPI. Example run:

```bash
cd catalog-service
python -m venv .venv
.venv\Scripts\activate  # On Windows PowerShell
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Node-based services default to `PORT=3000`. FastAPI catalog runs on `8000`. Override example (Node):

```bash
PORT=4001 npm start
```

## Docker build

```bash
# Example for catalog-service
cd catalog-service
docker build -t catalog-service:dev .
docker run --rm -p 3000:3000 catalog-service:dev
```

## Kubernetes (templates)

Manifests use namespace `ecommerce`. Update image names before applying.

```bash
kubectl apply -f k8s-manifests/namespace.yaml
kubectl apply -f k8s-manifests/
```
