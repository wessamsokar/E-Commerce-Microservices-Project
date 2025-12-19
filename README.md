# E-Commerce Microservices Platform

A complete microservices-based e-commerce system built with **FastAPI**, containerized with **Docker**, orchestrated with **Kubernetes (KinD)**, and managed using **ArgoCD GitOps**.

---

## 📋 Project Overview

This project implements a cloud-native e-commerce backend using microservices architecture with:
- ✅ **4 Independent Microservices** (Catalog, Cart, Order, Payment)
- ✅ **Containerization** with Docker
- ✅ **Local Kubernetes** cluster using KinD
- ✅ **GitOps Deployment** with ArgoCD
- ✅ **Order Tracking Dashboard** (HTML/JavaScript)
- ✅ **REST APIs** with FastAPI
- ✅ **SQLite Databases** for data persistence

---

## 🏗️ Architecture

### Microservices

| Service | Port | Technology | Database | Description |
|---------|------|------------|----------|-------------|
| **catalog-service** | 8000 | Python/FastAPI | SQLite | Product catalog CRUD operations |
| **cart-service** | 8001 | Python/FastAPI | SQLite | Shopping cart management |
| **order-service** | 8003 | Python/FastAPI | SQLite | Order creation & tracking |
| **payment-service** | 8002 | Python/FastAPI | Mock | Payment confirmation (simulated) |
| **frontend** | 8080 | HTML/JS | - | Order tracking dashboard |

### Technology Stack

- **Backend Framework**: FastAPI (Python 3.9+)
- **Containerization**: Docker
- **Orchestration**: Kubernetes (KinD)
- **GitOps**: ArgoCD
- **Database**: SQLite (embedded)
- **API Docs**: Swagger/OpenAPI (auto-generated)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop)
- **kubectl** - [Install Guide](https://kubernetes.io/docs/tasks/tools/)
- **KinD** - [Install Guide](https://kind.sigs.k8s.io/docs/user/quick-start/)

---

## 💻 Local Development

### 1. Run Services Locally

Each service can run independently for development:

#### Catalog Service (Port 8000)
```powershell
cd catalog-service
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Cart Service (Port 8001)
```powershell
cd cart-service
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

#### Order Service (Port 8003)
```powershell
cd order-service
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8003
```

#### Payment Service (Port 8002)
```powershell
cd payment-service
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

#### Frontend Dashboard (Port 8080)
```powershell
cd frontend/public
python -m http.server 8080
```

### 2. Access APIs

- **Catalog**: http://localhost:8000/docs
- **Cart**: http://localhost:8001/docs
- **Order**: http://localhost:8003/docs
- **Payment**: http://localhost:8002/docs
- **Dashboard**: http://localhost:8080

---

## 🐳 Docker Deployment

### Build Docker Images

```powershell
# Build all services
docker build -t catalog-service:v1 .\catalog-service
docker build -t cart-service:v1 .\cart-service
docker build -t order-service:v1 .\order-service
docker build -t payment-service:v1 .\payment-service
docker build -t frontend:v1 .\frontend
```

### Run Containers

```powershell
docker run -d --name catalog -p 8000:8000 catalog-service:v1
docker run -d --name cart -p 8001:8001 cart-service:v1
docker run -d --name order -p 8003:8003 order-service:v1
docker run -d --name payment -p 8002:8002 payment-service:v1
docker run -d --name frontend -p 8080:80 frontend:v1
```

---

## ☸️ Kubernetes Deployment

### 1. Create KinD Cluster

```powershell
kind create cluster --name ecommerce
```

### 2. Load Images to KinD

```powershell
C:\Users\Dell\kind.exe load docker-image catalog-service:v1 --name ecommerce
C:\Users\Dell\kind.exe load docker-image cart-service:v1 --name ecommerce
C:\Users\Dell\kind.exe load docker-image order-service:v1 --name ecommerce
C:\Users\Dell\kind.exe load docker-image payment-service:v1 --name ecommerce
C:\Users\Dell\kind.exe load docker-image frontend:v1 --name ecommerce
```

### 3. Deploy Services

```powershell
# Create namespace
kubectl apply -f k8s-manifests/namespace.yaml

# Deploy all services
kubectl apply -f k8s-manifests/
```

### 4. Verify Deployment

```powershell
kubectl get pods -n ecommerce
kubectl get services -n ecommerce
kubectl get deployments -n ecommerce
```

### 5. Access Services via Port Forward

```powershell
# Order Service for Dashboard
kubectl port-forward -n ecommerce svc/order-service 8003:80

# Frontend
kubectl port-forward -n ecommerce svc/frontend 8081:80
```

---

## 🔄 ArgoCD GitOps

### 1. Install ArgoCD

```powershell
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### 2. Access ArgoCD UI

```powershell
# Port forward
kubectl port-forward svc/argocd-server -n argocd 9090:443

# Get admin password
$password = kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}"
[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($password))
```

**ArgoCD Login:**
- URL: https://localhost:9090
- Username: `admin`
- Password: (from command above)

### 3. Deploy Application via ArgoCD

ArgoCD will automatically sync your Kubernetes manifests from Git repository.

---

## 📊 Order Tracking Dashboard

The frontend provides a real-time order tracking interface:

1. **Access**: http://localhost:8080
2. **Features**:
   - View all orders
   - Filter by status (PENDING, CONFIRMED, FAILED)
   - Real-time order updates
   - Order details with items

---

## 🧪 Testing the System

### 1. Add Products (Catalog Service)

Visit http://localhost:8000/docs and use the POST `/products` endpoint:

```json
{
  "id": 1,
  "name": "Laptop",
  "price": 1299.99,
  "description": "Gaming Laptop"
}
```

### 2. Create Order (Order Service)

Visit http://localhost:8003/docs and use POST `/orders`:

```json
{
  "user_id": "customer_001",
  "items": [
    {
      "product_id": "1",
      "quantity": 2,
      "unit_price": 1299.99
    }
  ]
}
```

### 3. View Orders

Open http://localhost:8080 to see all orders in the dashboard.

---

## 📁 Project Structure

```
.
├── catalog-service/         # Product catalog microservice
│   ├── app/                # FastAPI application
│   ├── Dockerfile          # Container image
│   └── requirements.txt    # Python dependencies
├── cart-service/           # Shopping cart microservice
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── order-service/          # Order management microservice
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
├── payment-service/        # Payment processing microservice
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Order tracking dashboard
│   ├── public/
│   │   └── index.html     # Dashboard UI
│   └── Dockerfile
├── k8s-manifests/          # Kubernetes manifests
│   ├── namespace.yaml     # ecommerce namespace
│   ├── catalog-service.yaml
│   ├── cart-service.yaml
│   ├── order-service.yaml
│   ├── payment-service.yaml
│   └── frontend.yaml
└── README.md              # This file
```

---

## 🔧 Troubleshooting

### Port Already in Use
```powershell
# Change port when running services
uvicorn main:app --reload --port 8010
```

### Docker Image Not Found in KinD
```powershell
# Verify image exists
docker images

# Reload image to KinD
kind load docker-image <service>:v1 --name ecommerce
```

### Pods Not Starting
```powershell
# Check pod logs
kubectl logs -n ecommerce <pod-name>

# Describe pod for events
kubectl describe pod -n ecommerce <pod-name>
```

---

## 📚 API Documentation

Each service provides auto-generated API documentation via Swagger UI:

- Catalog: http://localhost:8000/docs
- Cart: http://localhost:8001/docs
- Order: http://localhost:8003/docs
- Payment: http://localhost:8002/docs

---

## 🎯 Project Requirements Checklist

- [x] ✅ **4 Microservices** (Catalog, Cart, Order, Payment)
- [x] ✅ **REST APIs** with FastAPI
- [x] ✅ **Dockerfiles** for all services
- [x] ✅ **KinD** local Kubernetes cluster
- [x] ✅ **Kubernetes Manifests** (Deployments + Services)
- [x] ✅ **ArgoCD** GitOps setup
- [x] ✅ **Order Tracking Dashboard** (HTML/JS)
- [x] ✅ **SQLite Database** for data persistence

---

## 📝 License

This project is for educational purposes.

---

## 👥 Contributors

Cloud Computing - Semester 5 Project
