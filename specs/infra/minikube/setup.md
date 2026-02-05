# Minikube Setup Guide

**Phase**: IV - Cloud-Native Local Deployment
**Purpose**: Configure local Kubernetes cluster for Todo Chatbot deployment

## Prerequisites

- Docker Desktop installed and running
- Minikube installed (`choco install minikube` or `brew install minikube`)
- kubectl installed (`choco install kubernetes-cli` or `brew install kubectl`)
- Helm 3.x installed (`choco install kubernetes-helm` or `brew install helm`)
- Minimum 8GB RAM (4GB allocated to Minikube)
- Minimum 20GB free disk space

## Minikube Configuration

### Recommended Settings

```bash
# Start with recommended resources
minikube start \
  --memory=4096 \
  --cpus=2 \
  --disk-size=20g \
  --driver=docker \
  --kubernetes-version=stable

# Verify cluster
minikube status
kubectl cluster-info
```

### Windows-Specific Setup

```powershell
# PowerShell - Start Minikube
minikube start --memory=4096 --cpus=2 --driver=docker

# Configure Docker CLI to use Minikube's Docker daemon
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Verify
docker info | Select-String "Name"
```

### Linux/macOS Setup

```bash
# Start Minikube
minikube start --memory=4096 --cpus=2 --driver=docker

# Configure Docker CLI
eval $(minikube docker-env)

# Verify
docker info | grep "Name:"
```

## Required Addons

```bash
# Enable ingress controller (optional but recommended)
minikube addons enable ingress

# Enable metrics server (for resource monitoring)
minikube addons enable metrics-server

# Enable dashboard (optional, for visual management)
minikube addons enable dashboard

# List enabled addons
minikube addons list | grep enabled
```

## Cluster Verification

```bash
# Check node status
kubectl get nodes -o wide

# Check system pods
kubectl get pods -n kube-system

# Check available resources
kubectl top nodes  # Requires metrics-server

# View cluster info
kubectl cluster-info
```

## Common Issues

### Docker Driver Issues (Windows)

**Problem**: Minikube fails to start with Docker driver

**Solution**:
```powershell
# Ensure Docker Desktop is running
# Ensure WSL2 is enabled (Settings → General → Use WSL2)

# Reset Minikube if corrupted
minikube delete
minikube start --driver=docker
```

### Insufficient Resources

**Problem**: Pods stuck in Pending state

**Solution**:
```bash
# Check resource usage
kubectl describe node minikube | grep -A 10 "Allocated resources"

# Increase Minikube resources
minikube stop
minikube config set memory 6144
minikube config set cpus 3
minikube start
```

### DNS Resolution Issues

**Problem**: Pods cannot resolve external hostnames

**Solution**:
```bash
# Check CoreDNS
kubectl get pods -n kube-system -l k8s-app=kube-dns

# Restart CoreDNS
kubectl rollout restart deployment/coredns -n kube-system
```

### Image Pull Failures

**Problem**: ImagePullBackOff errors

**Solution**:
```bash
# Ensure Docker context is Minikube
eval $(minikube docker-env)  # or PowerShell equivalent

# Verify images exist in Minikube's Docker
minikube ssh -- docker images | grep todo

# Rebuild if needed
docker build -t todo-backend:local ./backend
docker build -t todo-frontend:local ./frontend
```

## Lifecycle Commands

```bash
# Stop cluster (preserves state)
minikube stop

# Start stopped cluster
minikube start

# Pause cluster (frees CPU/memory)
minikube pause

# Unpause cluster
minikube unpause

# Delete cluster (destroys everything)
minikube delete

# Delete and recreate
minikube delete && minikube start --memory=4096 --cpus=2
```

## Accessing Services

### Port Forwarding (Recommended)

```bash
# Forward backend
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app &

# Forward frontend
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app &

# Access at http://localhost:3000
```

### Minikube Service Command

```bash
# Open service in browser
minikube service todo-frontend -n todo-app

# Get service URL
minikube service todo-frontend -n todo-app --url
```

### Ingress (if enabled)

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (or C:\Windows\System32\drivers\etc\hosts)
# <minikube-ip> todo.local

# Access at http://todo.local
```

## Monitoring

### Dashboard

```bash
# Open Kubernetes dashboard
minikube dashboard

# Get dashboard URL
minikube dashboard --url
```

### Resource Monitoring

```bash
# Node resources
kubectl top nodes

# Pod resources
kubectl top pods -n todo-app

# All namespaces
kubectl top pods -A
```

## Cleanup

```bash
# Remove application
helm uninstall todo -n todo-app
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Full cleanup
minikube delete --all --purge
```
