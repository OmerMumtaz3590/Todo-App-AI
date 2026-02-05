#!/bin/bash

# SYNOPSIS
#    Deployment script for Todo Chatbot application to Kubernetes using Helm
# DESCRIPTION
#    This script automates the deployment of the Todo Chatbot application to a local Minikube cluster.
#    It includes all necessary steps from cluster setup to application verification.
# OPTIONS
#    --skip-minikube-start: Skip starting Minikube if it's already running
#    --skip-docker-build: Skip Docker image building if images are already built
#    --skip-helm-install: Skip Helm installation if already deployed
# EXAMPLES
#    ./deploy-k8s.sh
#    Deploy the application with all steps
#    ./deploy-k8s.sh --skip-minikube-start --skip-docker-build
#    Deploy only the Helm release (skip cluster start and image build)

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Functions for colored output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_debug() {
    echo -e "${CYAN}[DEBUG]${NC} $1"
}

# Parse command line arguments
SKIP_MINIKUBE_START=false
SKIP_DOCKER_BUILD=false
SKIP_HELM_INSTALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-minikube-start)
            SKIP_MINIKUBE_START=true
            shift
            ;;
        --skip-docker-build)
            SKIP_DOCKER_BUILD=true
            shift
            ;;
        --skip-helm-install)
            SKIP_HELM_INSTALL=true
            shift
            ;;
        *)
            log_error "Unknown option: $1"
            echo "Usage: $0 [--skip-minikube-start] [--skip-docker-build] [--skip-helm-install]"
            exit 1
            ;;
    esac
done

# Main deployment function
main() {
    log_info "Starting Todo Chatbot Kubernetes Deployment"
    log_info "=============================================="

    # Check prerequisites
    log_info "Checking prerequisites..."
    local prerequisites=("docker" "minikube" "kubectl")
    if [ "$SKIP_HELM_INSTALL" = false ]; then
        prerequisites+=("helm")
    fi

    for tool in "${prerequisites[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool is not installed or not in PATH"
            log_error "Please install $tool before continuing"
            exit 1
        else
            log_info "$tool is installed"
        fi
    done

    # Start Minikube if not skipped
    if [ "$SKIP_MINIKUBE_START" = false ]; then
        log_info "Starting Minikube cluster..."
        MINIKUBE_STATUS=$(minikube status --format='{{.Host}}' 2>/dev/null || echo "stopped")

        if [ "$MINIKUBE_STATUS" != "Running" ]; then
            log_info "Starting Minikube with recommended settings..."
            minikube start --memory=4096 --cpus=2 --driver=docker --kubernetes-version=stable
            if [ $? -eq 0 ]; then
                log_info "Minikube started successfully"
            else
                log_error "Failed to start Minikube"
                exit 1
            fi
        else
            log_info "Minikube is already running"
        fi

        # Enable required addons
        log_info "Enabling required addons..."
        minikube addons enable ingress
        minikube addons enable metrics-server
    else
        log_info "Skipping Minikube start (assumed to be running)"
    fi

    # Configure Docker to use Minikube's Docker daemon
    log_info "Configuring Docker to use Minikube..."
    eval $(minikube docker-env)
    if [ $? -eq 0 ]; then
        log_info "Docker configured for Minikube"
    else
        log_error "Failed to configure Docker for Minikube"
        exit 1
    fi

    # Install Dapr
    log_info "Installing Dapr on the cluster..."
    if dapr init -k; then
        log_info "Dapr installed successfully"
    else
        log_error "Failed to install Dapr"
        exit 1
    fi

    # Wait for Dapr to be ready
    log_info "Waiting for Dapr to be ready..."
    kubectl wait --for=condition=ready pod -l app=dapr-placement-server -n dapr-system --timeout=300s
    kubectl wait --for=condition=ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
    log_info "Dapr system is ready"

    # Install Strimzi Kafka operator if not using external Kafka
    log_info "Installing Strimzi Kafka operator..."

    # Add Strimzi Helm repo
    helm repo add strimzi https://strimzi.io/charts/
    helm repo update

    # Install Strimzi operator
    helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace --wait
    if [ $? -eq 0 ]; then
        log_info "Strimzi Kafka operator installed"
    else
        log_error "Failed to install Strimzi Kafka operator"
        exit 1
    fi

    # Wait for operator to be ready
    kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator --namespace kafka --timeout=300s
    log_info "Strimzi operator is ready"

    # Create Kafka cluster
    log_info "Creating Kafka cluster..."
    cat <<EOF | kubectl apply -f -
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

    if [ $? -eq 0 ]; then
        log_info "Kafka cluster created, waiting for readiness..."

        # Wait for Kafka to be ready
        kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=600s -n kafka
        if [ $? -eq 0 ]; then
            log_info "Kafka cluster is ready"
        else
            log_error "Kafka cluster failed to become ready"
            exit 1
        fi
    else
        log_error "Failed to create Kafka cluster"
        exit 1
    fi

    # Build Docker images if not skipped
    if [ "$SKIP_DOCKER_BUILD" = false ]; then
        log_info "Building Docker images..."

        # Build backend image
        log_info "Building backend image..."
        cd backend
        if docker build -t todo-backend:local . --platform linux/amd64; then
            log_info "Backend image built successfully"
        else
            log_error "Failed to build backend image"
            exit 1
        fi
        cd ..

        # Build frontend image
        log_info "Building frontend image..."
        cd frontend
        if docker build --build-arg NEXT_PUBLIC_API_URL=http://todo-backend:8000 -t todo-frontend:local . --platform linux/amd64; then
            log_info "Frontend image built successfully"
        else
            log_error "Failed to build frontend image"
            exit 1
        fi
        cd ..

        # Verify images
        log_info "Verifying images..."
        if docker images | grep -q "todo-"; then
            log_info "Found required images"
        else
            log_warning "Expected to find todo images, but none found"
        fi
    else
        log_info "Skipping Docker build (assumed to be completed)"
    fi

    # Create namespace
    log_info "Creating namespace..."
    kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
    if [ $? -ne 0 ]; then
        log_warning "Namespace may already exist"
    fi

    # Check if secrets file exists
    local secrets_file="./secrets.yaml"
    if [ ! -f "$secrets_file" ]; then
        log_warning "Secrets file '$secrets_file' not found!"
        log_info "Please create a secrets.yaml file with your sensitive configuration:"
        cat <<'EOF'
# secrets.yaml - SAMPLE CONFIGURATION (fill in with real values)
# DO NOT COMMIT THIS FILE TO VERSION CONTROL
secrets:
  databaseUrl: "YOUR_NEON_DATABASE_URL_HERE"
  secretKey: "YOUR_JWT_SECRET_KEY_HERE_MINIMUM_32_CHARS"
  openaiApiKey: "YOUR_OPENAI_API_KEY_HERE"
EOF
        log_info "Then run this script again or proceed with manual Helm installation."
        exit 0
    else
        log_info "Found secrets file: $secrets_file"
    fi

    # Install Helm release if not skipped
    if [ "$SKIP_HELM_INSTALL" = false ]; then
        log_info "Installing Helm release..."

        # First, validate the chart
        log_info "Validating Helm chart..."
        if helm lint specs/infra/helm/todo-chatbot/; then
            log_info "Helm lint passed"
        else
            log_warning "Helm lint found issues (may be acceptable for local dev)"
        fi

        # Install the release
        log_info "Installing Helm release 'todo'..."
        if helm upgrade --install todo specs/infra/helm/todo-chatbot/ --namespace todo-app --values "$secrets_file" --wait --timeout=10m; then
            log_info "Helm release installed successfully!"
        else
            log_error "Failed to install Helm release"
            exit 1
        fi
    else
        log_info "Skipping Helm installation (assumed to be completed)"
    fi

    # Wait for pods to be ready
    log_info "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo -n todo-app --timeout=300s
    if [ $? -ne 0 ]; then
        log_warning "Some pods may still be starting up..."
    fi

    # Show deployment status
    log_info "Deployment status:"
    kubectl get all -n todo-app

    # Show pod logs
    log_info "Backend pod logs:"
    kubectl logs -l app=todo-backend -n todo-app --tail=10

    log_info "Frontend pod logs:"
    kubectl logs -l app=todo-frontend -n todo-app --tail=10

    # Provide access instructions
    log_info "=============================================="
    log_info "DEPLOYMENT COMPLETED SUCCESSFULLY!"
    log_info "=============================================="
    echo
    log_info "To access the application:"
    log_info "1. Port forward the services:"
    log_info "   Terminal 1: kubectl port-forward svc/todo-backend 8000:8000 -n todo-app"
    log_info "   Terminal 2: kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app"
    log_info "   Browser: http://localhost:3000"
    echo
    log_info "Alternative access via Minikube:"
    log_info "   minikube service todo-frontend -n todo-app --url"
    echo
    log_info "To verify health: curl http://localhost:8000/health (after port forward)"
    echo
    log_info "To view all resources: kubectl get all -n todo-app"
    log_info "To view logs: kubectl logs -l app=todo-backend -n todo-app"
    echo
    log_info "For cleanup: helm uninstall todo -n todo-app && kubectl delete namespace todo-app"
}

# Call the main function
main "$@"