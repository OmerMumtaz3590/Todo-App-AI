# Quickstart Guide: Advanced Cloud Deployment with Event-Driven Architecture

**Feature**: Phase V - Advanced Cloud Deployment
**Created**: 2026-02-05

## Overview

This guide provides step-by-step instructions to get the event-driven todo application with Dapr and Kafka running locally using Minikube. The application features advanced task management capabilities including priorities, tags, search, recurring tasks, and reminders.

## Prerequisites

### System Requirements
- Docker Desktop (with Kubernetes enabled)
- Minikube (latest version)
- kubectl
- Helm 3.x
- Dapr CLI
- Node.js 18+ and npm
- Python 3.11+
- Java 11+ (for Kafka/Zookeeper)

### Installation Commands

**Windows (PowerShell as Administrator)**:
```powershell
# Install kubectl
choco install kubernetes-cli

# Install Helm
choco install kubernetes-helm

# Install Minikube
choco install minikube

# Install Dapr CLI
wget -q https://raw.githubusercontent.com/dapr/cli/master/install/install.ps1 -O install.ps1
.\install.ps1 -DownloadPath ./install

# Install Python
choco install python

# Install Node.js
choco install nodejs
```

**macOS (using Homebrew)**:
```bash
# Install kubectl
brew install kubectl

# Install Helm
brew install helm

# Install Minikube
brew install minikube

# Install Dapr CLI
brew install dapr/tap/dapr-cli

# Install Python and Node.js
brew install python@3.11 node
```

## Step 1: Start Minikube Cluster

```bash
# Start Minikube with sufficient resources for our services
minikube start \
  --memory=8192 \
  --cpus=4 \
  --disk-size=40g \
  --driver=docker \
  --kubernetes-version=stable

# Verify cluster is running
kubectl cluster-info
kubectl get nodes
```

## Step 2: Install Dapr

```bash
# Initialize Dapr on the cluster
dapr init -k

# Verify Dapr is running
kubectl get pods -n dapr-system

# Check Dapr CLI version matches runtime
dapr --version
```

## Step 3: Set Up Kafka for Event Streaming

### Option A: Self-hosted Kafka with Strimzi (Recommended for Development)

```bash
# Add Strimzi repository
helm repo add strimzi https://strimzi.io/charts/
helm repo update

# Install Strimzi operator
helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace

# Create Kafka cluster
kubectl apply -f - <<EOF
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
  namespace: kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 1
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 1
      transaction.state.log.replication.factor: 1
      transaction.state.log.min.isr: 1
      default.replication.factor: 1
      min.insync.replicas: 1
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 10Gi
        deleteClaim: false
  zookeeper:
    replicas: 1
    storage:
      type: persistent-claim
      size: 5Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
EOF

# Wait for Kafka to be ready
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka
```

### Option B: Redpanda Cloud (Requires Account)

```bash
# If using Redpanda Cloud, create a secret with your cluster details
kubectl create secret generic redpanda-cluster \
  --from-literal=addresses="your-redpanda-bootstrap-servers" \
  --from-literal=username="your-username" \
  --from-literal=password="your-password" \
  -n todo-app
```

## Step 4: Configure Dapr Components

Create the necessary Dapr components for pub/sub, state management, and secrets:

```bash
# Create Dapr component configurations
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "my-cluster-kafka-brokers.kafka.svc.cluster.local:9092"
  - name: authRequired
    value: "false"
  - name: consumerGroup
    value: "todo-app-group"
EOF

# Create state store component (using PostgreSQL through Dapr)
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-statestore
  namespace: todo-app
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: postgresql-secret
      key: connectionUrl
  - name: actorStateStore
    value: "true"
EOF

# Create secret store component
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: todo-secretstore
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
  metadata:
  - name: namespace
    value: "todo-app"
EOF

# Create binding for scheduled tasks (reminders)
kubectl apply -f - <<EOF
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-binding
  namespace: todo-app
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/30 * * * * *"  # Every 30 seconds for development
EOF
```

## Step 5: Create Application Namespace and Secrets

```bash
# Create namespace
kubectl create namespace todo-app

# Create PostgreSQL secret (update with your actual Neon connection string)
kubectl create secret generic postgresql-secret \
  --from-literal=connectionUrl="postgresql://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require" \
  -n todo-app

# Create other secrets
kubectl create secret generic todo-app-secrets \
  --from-literal=SECRET_KEY="your-32-characters-secret-key-here" \
  --from-literal=OPENAI_API_KEY="your-openai-api-key" \
  -n todo-app
```

## Step 6: Build and Push Container Images

```bash
# Configure Docker to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image with API URL
cd ../frontend
docker build --build-arg NEXT_PUBLIC_API_URL=http://todo-backend.todo-app.svc.cluster.local:8000 -t todo-frontend:latest .
```

## Step 7: Update and Deploy Helm Chart

Navigate to your Phase IV Helm chart and update it with Dapr annotations:

```bash
# Apply Dapr annotations and deploy using your existing Phase IV Helm chart
helm upgrade --install todo \
  ./specs/infra/helm/todo-chatbot \
  --namespace todo-app \
  --set backend.image.repository=todo-backend \
  --set backend.image.tag=latest \
  --set frontend.image.repository=todo-frontend \
  --set frontend.image.tag=latest \
  --set backend.dapr.enabled=true \
  --set backend.dapr.appId=todo-backend \
  --set frontend.dapr.enabled=true \
  --set frontend.dapr.appId=todo-frontend \
  --create-namespace
```

## Step 8: Verify the Deployment

```bash
# Check if all pods are running
kubectl get pods -n todo-app

# Check Dapr sidecars are injected
kubectl describe pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check if Kafka topics are created
kubectl exec -it -n kafka deployment/my-cluster-kafka -c kafka -- \
  bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## Step 9: Test the Application

### Access the Application

```bash
# Port forward to access the services
kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app &
kubectl port-forward svc/todo-backend 8000:8000 -n todo-app &
```

Now open your browser to `http://localhost:3000` to access the application.

### API Testing

Test the advanced features:

```bash
# 1. Create a task with priority and tags
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR-JWT-TOKEN" \
  -d '{
    "title": "High priority task",
    "description": "This is urgent!",
    "priority": "HIGH",
    "tags": ["urgent", "work"],
    "due_date": "2024-12-31T23:59:59Z",
    "remind_at": "2024-12-30T09:00:00Z"
  }'

# 2. Create a recurring task
curl -X POST http://localhost:8000/recurring-tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR-JWT-TOKEN" \
  -d '{
    "title": "Daily Standup",
    "description": "Daily team standup meeting",
    "priority": "MEDIUM",
    "tags": ["meeting", "routine"],
    "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1",
    "due_date": "2024-12-31T09:00:00Z"
  }'

# 3. Search tasks
curl "http://localhost:8000/tasks/search?q=urgent" \
  -H "Authorization: Bearer YOUR-JWT-TOKEN"

# 4. Filter tasks by priority
curl "http://localhost:8000/tasks?priority=HIGH" \
  -H "Authorization: Bearer YOUR-JWT-TOKEN"
```

## Step 10: Monitor Event Processing

Monitor the application logs to verify events are being processed:

```bash
# Monitor backend logs for event processing
kubectl logs -f deployment/todo-backend -n todo-app

# Monitor Dapr sidecar logs
kubectl logs -f deployment/todo-backend -c daprd -n todo-app

# Check Kafka topics for published events
kubectl exec -it -n kafka deployment/my-cluster-kafka -c kafka -- \
  bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic task-events --from-beginning
```

## Troubleshooting

### Common Issues and Solutions

**Issue**: Dapr sidecar not injected
- Solution: Verify Dapr is initialized and the correct annotations are in your deployments
```bash
kubectl get pods -n todo-app -o yaml | grep dapr
```

**Issue**: Kafka connection errors
- Solution: Verify Kafka cluster is running and the pubsub component configuration is correct
```bash
kubectl get pods -n kafka
kubectl describe component todo-pubsub -n todo-app
```

**Issue**: Database connection errors
- Solution: Check that PostgreSQL secret is correctly configured and accessible
```bash
kubectl describe secret postgresql-secret -n todo-app
kubectl logs -f deployment/todo-backend -n todo-app
```

**Issue**: Event publishing/consuming not working
- Solution: Verify Dapr pubsub component and Kafka cluster status
```bash
dapr status -k
kubectl get pods -n kafka
```

## Development Workflow

### Local Development with Dapr

For faster development cycles, you can run the services locally with Dapr sidecars:

```bash
# Run backend with Dapr
cd backend
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 uvicorn src.main:app --reload

# Run frontend with Dapr (in separate terminal)
cd frontend
dapr run --app-id todo-frontend --app-port 3000 --dapr-http-port 3501 npm run dev
```

### Hot Reload Configuration

With Dapr, you can maintain hot reload during development by running services locally with Dapr CLI as shown above.

## Scaling the Application

To scale the application based on load:

```bash
# Scale backend deployment
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Scale frontend deployment
kubectl scale deployment todo-frontend --replicas=3 -n todo-app
```

## Clean Up

To remove all resources:

```bash
# Uninstall Helm release
helm uninstall todo -n todo-app

# Remove Kafka cluster
kubectl delete -f https://strimzi.io/examples/latest/kafka/kafka-persistent-single.yaml -n kafka

# Remove Dapr
dapr uninstall -k

# Stop Minikube
minikube stop

# Optionally delete Minikube cluster completely
minikube delete
```

## Next Steps

1. **Production Deployment**: Follow the cloud deployment guide to deploy to Azure AKS
2. **Monitoring Setup**: Configure Prometheus and Grafana for monitoring
3. **Security Hardening**: Enable mTLS and configure proper authentication
4. **Performance Tuning**: Optimize Kafka and Dapr configurations for production
5. **CI/CD Pipeline**: Set up GitHub Actions for automated deployments

This quickstart guide provides a complete local development environment for the event-driven todo application. The architecture follows Phase V requirements with Dapr for service mesh capabilities and Kafka for event streaming.