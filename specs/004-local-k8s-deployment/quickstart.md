# Quickstart: Local Kubernetes Deployment

**Feature**: 004-local-k8s-deployment
**Prerequisites**: Docker Desktop, Minikube, Helm 3.x, kubectl

## Prerequisites Check

```bash
# Verify Docker is running
docker --version
docker info

# Verify Minikube is installed
minikube version

# Verify Helm is installed
helm version

# Verify kubectl is installed
kubectl version --client
```

## Step 1: Start Minikube

```bash
# Start Minikube with recommended resources
minikube start --memory=4096 --cpus=2 --driver=docker

# Enable ingress addon (optional)
minikube addons enable ingress

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Step 2: Configure Docker to Use Minikube

```bash
# Point Docker CLI to Minikube's Docker daemon
# On Windows PowerShell:
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# On Windows CMD:
@FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env --shell cmd') DO @%i

# On Linux/macOS:
eval $(minikube docker-env)

# Verify (should show Minikube's Docker)
docker info | grep -i name
```

## Step 3: Build Container Images

```bash
# Build backend image
docker build -t todo-backend:local ./backend

# Build frontend image (with API URL for Kubernetes)
docker build \
  --build-arg NEXT_PUBLIC_API_URL=http://todo-backend:8000 \
  -t todo-frontend:local \
  ./frontend

# Verify images are available
docker images | grep todo
```

## Step 4: Create Kubernetes Namespace

```bash
# Create dedicated namespace
kubectl create namespace todo-app

# Set as default (optional)
kubectl config set-context --current --namespace=todo-app
```

## Step 5: Create Secrets File

Create a file named `secrets.yaml` (DO NOT COMMIT THIS FILE):

```yaml
# secrets.yaml - KEEP THIS FILE OUT OF VERSION CONTROL
secrets:
  databaseUrl: "postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require"
  secretKey: "your-jwt-secret-key-minimum-32-characters-long"
  openaiApiKey: "sk-your-openai-api-key"
```

## Step 6: Deploy with Helm

```bash
# Navigate to repository root
cd /path/to/todo-app

# Install the Helm release
helm install todo specs/infra/helm/todo-chatbot \
  --namespace todo-app \
  -f secrets.yaml

# Watch pods come up
kubectl get pods -n todo-app -w
```

## Step 7: Access the Application

```bash
# Option A: Port forwarding (recommended for local dev)
# Terminal 1 - Backend
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app

# Terminal 2 - Frontend
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app

# Open browser to http://localhost:3000

# Option B: Minikube service (alternative)
minikube service todo-frontend -n todo-app
```

## Step 8: Verify Deployment

```bash
# Check all resources
kubectl get all -n todo-app

# Check pod logs
kubectl logs -l app=todo-backend -n todo-app
kubectl logs -l app=todo-frontend -n todo-app

# Test backend health
curl http://localhost:8000/health
# Expected: {"status":"healthy"}

# Test frontend
curl http://localhost:3000
# Expected: HTML response
```

## Common Operations

### Upgrade Deployment

```bash
# After changing values or images
helm upgrade todo specs/infra/helm/todo-chatbot \
  --namespace todo-app \
  -f secrets.yaml
```

### Rollback Deployment

```bash
# List revisions
helm history todo -n todo-app

# Rollback to previous version
helm rollback todo -n todo-app

# Rollback to specific revision
helm rollback todo 1 -n todo-app
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/todo-backend -n todo-app

# Frontend logs
kubectl logs -f deployment/todo-frontend -n todo-app

# All pods in namespace
kubectl logs -l app.kubernetes.io/instance=todo -n todo-app
```

### Scale Deployment

```bash
# Scale backend to 3 replicas
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Or update values.yaml and upgrade
helm upgrade todo specs/infra/helm/todo-chatbot \
  --set backend.replicas=3 \
  -n todo-app
```

### Restart Pods

```bash
# Restart backend pods
kubectl rollout restart deployment/todo-backend -n todo-app

# Restart all deployments
kubectl rollout restart deployment -n todo-app
```

### Uninstall

```bash
# Remove Helm release
helm uninstall todo -n todo-app

# Delete namespace (removes everything)
kubectl delete namespace todo-app

# Stop Minikube
minikube stop
```

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n todo-app

# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'

# Check resource constraints
kubectl top pods -n todo-app
```

### Image Pull Errors

```bash
# Verify Docker context is Minikube
docker info | grep -i name

# Rebuild images (if context was wrong)
eval $(minikube docker-env)
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend

# Verify images exist
minikube ssh -- docker images | grep todo
```

### Database Connection Issues

```bash
# Check secret is mounted
kubectl exec -it deployment/todo-backend -n todo-app -- env | grep DATABASE

# Test connection from pod
kubectl exec -it deployment/todo-backend -n todo-app -- \
  python -c "from src.database import engine; print(engine.url)"
```

### CORS Errors

```bash
# Update CORS origins in values
helm upgrade todo specs/infra/helm/todo-chatbot \
  --set config.corsOrigins='["http://localhost:3000","http://todo-frontend:3000"]' \
  -n todo-app
```

## AI-Assisted Operations

### kubectl-ai Examples

```bash
# Generate a HPA manifest
kubectl-ai "Create a HorizontalPodAutoscaler for todo-backend with min 1, max 5 replicas at 70% CPU"

# Debug a failing pod
kubectl-ai "Why is the todo-backend pod not ready?"

# Get logs with filtering
kubectl-ai "Show error logs from todo-backend in the last hour"
```

### kagent Examples

```bash
# Cluster health analysis
kagent analyze --namespace todo-app

# Resource utilization report
kagent report resources --namespace todo-app

# Troubleshoot specific issue
kagent troubleshoot pod todo-backend-xxx -n todo-app
```

## Environment Configuration

### Development (Default)

```yaml
# values.yaml overrides
backend:
  replicas: 1
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
config:
  debug: "true"
```

### Production-like (Local Testing)

```yaml
# values-prod.yaml
backend:
  replicas: 2
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "1000m"
frontend:
  replicas: 2
config:
  debug: "false"
ingress:
  enabled: true
  host: todo.local
```

```bash
# Deploy with production values
helm upgrade todo specs/infra/helm/todo-chatbot \
  -n todo-app \
  -f secrets.yaml \
  -f values-prod.yaml
```
