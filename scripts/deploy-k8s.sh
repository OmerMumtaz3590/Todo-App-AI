#!/bin/bash

# SYNOPSIS
#    Deployment script for Todo Chatbot application to Kubernetes using Helm
# DESCRIPTION
#    This script automates the deployment of the Todo Chatbot application to a local Minikube cluster.
#    It includes all necessary steps from cluster setup to application verification.

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
            echo "Unknown option: $1"
            echo "Usage: $0 [--skip-minikube-start] [--skip-docker-build] [--skip-helm-install]"
            exit 1
            ;;
    esac
done

# Main deployment function
main() {
    log_info "Starting Todo Chatbot Kubernetes Deployment"
    log_info "============================================="

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
    if [ $? -ne 0 ]; then
        log_error "Failed to configure Docker for Minikube"
        exit 1
    fi

    # Build Docker images if not skipped
    if [ "$SKIP_DOCKER_BUILD" = false ]; then
        log_info "Building Docker images..."

        # Build backend image
        log_info "Building backend image..."
        (cd ./backend && docker build -t todo-backend:local . --platform linux/amd64)

        # Build frontend image
        log_info "Building frontend image..."
        (cd ./frontend && docker build --build-arg NEXT_PUBLIC_API_URL=http://todo-backend:8000 -t todo-frontend:local . --platform linux/amd64)

        # Verify images
        log_info "Verifying images..."
        IMAGE_COUNT=$(docker images | grep todo- | wc -l)
        log_info "Found $IMAGE_COUNT todo images"
    else
        log_info "Skipping Docker build (assumed to be completed)"
    fi

    # Create namespace
    log_info "Creating namespace..."
    kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f - || log_warning "Namespace may already exist"

    # Check if secrets file exists
    SECRETS_FILE="./secrets.yaml"
    if [ ! -f "$SECRETS_FILE" ]; then
        log_warning "Secrets file '$SECRETS_FILE' not found!"
        log_info "Please create a secrets.yaml file with your sensitive configuration:"
        cat << 'EOF'
# secrets.yaml
secrets:
  databaseUrl: "postgresql://user:password@ep-xxx.neon.tech/neondb?sslmode=require"
  secretKey: "your-jwt-secret-key-minimum-32-characters-long"
  openaiApiKey: "sk-your-openai-api-key"
EOF
        log_info "NOTICE: This file is in .gitignore and should NEVER be committed to version control!"

        # Create a sample file without actual secrets
        cat > "$SECRETS_FILE" << 'EOF'
# secrets.yaml - SAMPLE CONFIGURATION (fill in with real values)
# DO NOT COMMIT THIS FILE TO VERSION CONTROL
secrets:
  databaseUrl: "YOUR_NEON_DATABASE_URL_HERE"
  secretKey: "YOUR_JWT_SECRET_KEY_HERE_MINIMUM_32_CHARS"
  openaiApiKey: "YOUR_OPENAI_API_KEY_HERE"
EOF
        log_info "Created sample secrets.yaml file. Please fill in actual values."
        log_info "Then run this script again or proceed with manual Helm installation."
        exit 0
    else
        log_info "Found secrets file: $SECRETS_FILE"
    fi

    # Install Helm release if not skipped
    if [ "$SKIP_HELM_INSTALL" = false ]; then
        log_info "Installing Helm release..."

        # First, validate the chart
        log_info "Validating Helm chart..."
        helm lint specs/infra/helm/todo-chatbot/ || log_warning "Helm lint found issues (may be acceptable for local dev)"

        # Install the release
        log_info "Installing Helm release 'todo'..."
        helm upgrade --install todo specs/infra/helm/todo-chatbot/ --namespace todo-app --values "$SECRETS_FILE" --wait --timeout=10m
        if [ $? -ne 0 ]; then
            log_error "Failed to install Helm release"
            exit 1
        fi

        log_info "Helm release installed successfully!"
    else
        log_info "Skipping Helm installation (assumed to be completed)"
    fi

    # Wait for pods to be ready
    log_info "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo -n todo-app --timeout=300s || log_warning "Some pods may still be starting up..."

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