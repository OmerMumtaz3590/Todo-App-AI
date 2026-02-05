#!/usr/bin/env pwsh

<#
.SYNOPSIS
    Deployment script for Todo Chatbot application to Kubernetes using Helm
.DESCRIPTION
    This script automates the deployment of the Todo Chatbot application to a local Minikube cluster.
    It includes all necessary steps from cluster setup to application verification.
.PARAMETER SkipMinikubeStart
    Skip starting Minikube if it's already running
.PARAMETER SkipDockerBuild
    Skip Docker image building if images are already built
.PARAMETER SkipHelmInstall
    Skip Helm installation if already deployed
.EXAMPLE
    ./deploy-k8s.ps1
    Deploy the application with all steps
.EXAMPLE
    ./deploy-k8s.ps1 -SkipMinikubeStart -SkipDockerBuild
    Deploy only the Helm release (skip cluster start and image build)
#>

param(
    [switch]$SkipMinikubeStart,
    [switch]$SkipDockerBuild,
    [switch]$SkipHelmInstall
)

# Function to write colored output
function Write-Status {
    param([string]$Message, [string]$Color = "White")
    Write-Host $Message -ForegroundColor $Color
}

function Write-Info {
    param([string]$Message)
    Write-Status "[INFO] $Message" "Green"
}

function Write-Warning {
    param([string]$Message)
    Write-Status "[WARNING] $Message" "Yellow"
}

function Write-Error {
    param([string]$Message)
    Write-Status "[ERROR] $Message" "Red"
}

function Write-Debug {
    param([string]$Message)
    Write-Status "[DEBUG] $Message" "Cyan"
}

# Main deployment function
function Start-Deployment {
    Write-Info "Starting Todo Chatbot Kubernetes Deployment"
    Write-Info "=============================================="

    # Check prerequisites
    Write-Info "Checking prerequisites..."
    $prerequisites = @("docker", "minikube", "kubectl")
    if (-not $SkipHelmInstall) {
        $prerequisites += "helm"
    }

    foreach ($tool in $prerequisites) {
        try {
            $result = Invoke-Expression "$tool version 2>&1"
            if ($LASTEXITCODE -eq 0) {
                Write-Info "$tool is installed"
            } else {
                throw "$tool is not available"
            }
        } catch {
            Write-Error "$tool is not installed or not in PATH"
            Write-Error "Please install $tool before continuing"
            exit 1
        }
    }

    # Start Minikube if not skipped
    if (-not $SkipMinikubeStart) {
        Write-Info "Starting Minikube cluster..."
        try {
            $minikubeStatus = minikube status --format='{{.Host}}' 2>$null
            if ($minikubeStatus -ne "Running") {
                Write-Info "Starting Minikube with recommended settings..."
                minikube start --memory=4096 --cpus=2 --driver=docker --kubernetes-version=stable
                if ($LASTEXITCODE -eq 0) {
                    Write-Info "Minikube started successfully"
                } else {
                    throw "Failed to start Minikube"
                }
            } else {
                Write-Info "Minikube is already running"
            }

            # Enable required addons
            Write-Info "Enabling required addons..."
            minikube addons enable ingress
            minikube addons enable metrics-server
        } catch {
            Write-Error "Failed to start or configure Minikube: $($_.Exception.Message)"
            exit 1
        }
    } else {
        Write-Info "Skipping Minikube start (assumed to be running)"
    }

    # Configure Docker to use Minikube's Docker daemon
    Write-Info "Configuring Docker to use Minikube..."
    & minikube -p minikube docker-env --shell powershell | Invoke-Expression
    if ($LASTEXITCODE -eq 0) {
        Write-Info "Docker configured for Minikube"
    } else {
        Write-Error "Failed to configure Docker for Minikube"
        exit 1
    }

    # Install Dapr
    Write-Info "Installing Dapr on the cluster..."
    try {
        dapr init -k
        Write-Info "Dapr installed successfully"
    } catch {
        Write-Error "Failed to install Dapr: $($_.Exception.Message)"
        exit 1
    }

    # Wait for Dapr to be ready
    Write-Info "Waiting for Dapr to be ready..."
    kubectl wait --for=condition=ready pod -l app=dapr-placement-server -n dapr-system --timeout=300s
    kubectl wait --for=condition=ready pod -l app=dapr-sidecar-injector -n dapr-system --timeout=300s
    Write-Info "Dapr system is ready"

    # Install Strimzi Kafka operator if not using external Kafka
    Write-Info "Installing Strimzi Kafka operator..."
    try {
        # Add Strimzi Helm repo
        helm repo add strimzi https://strimzi.io/charts/
        helm repo update

        # Install Strimzi operator
        helm install strimzi strimzi/strimzi-kafka-operator --namespace kafka --create-namespace
        Write-Info "Strimzi Kafka operator installed"

        # Wait for operator to be ready
        kubectl wait --for=condition=ready pod -l name=strimzi-cluster-operator --namespace kafka --timeout=300s
        Write-Info "Strimzi operator is ready"
    } catch {
        Write-Error "Failed to install Strimzi: $($_.Exception.Message)"
        exit 1
    }

    # Create Kafka cluster
    Write-Info "Creating Kafka cluster..."
    $kafkaYaml = @"
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
"@

    try {
        $kafkaYaml | kubectl apply -f -
        Write-Info "Kafka cluster created, waiting for readiness..."

        # Wait for Kafka to be ready
        kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=600s -n kafka
        Write-Info "Kafka cluster is ready"
    } catch {
        Write-Error "Failed to create Kafka cluster: $($_.Exception.Message)"
        exit 1
    }

    # Build Docker images if not skipped
    if (-not $SkipDockerBuild) {
        Write-Info "Building Docker images..."

        # Build backend image
        Write-Info "Building backend image..."
        Push-Location ./backend
        try {
            docker build -t todo-backend:local . --platform linux/amd64
            if ($LASTEXITCODE -eq 0) {
                Write-Info "Backend image built successfully"
            } else {
                throw "Failed to build backend image"
            }
        } finally {
            Pop-Location
        }

        # Build frontend image
        Write-Info "Building frontend image..."
        Push-Location ./frontend
        try {
            docker build --build-arg NEXT_PUBLIC_API_URL=http://todo-backend:8000 -t todo-frontend:local . --platform linux/amd64
            if ($LASTEXITCODE -eq 0) {
                Write-Info "Frontend image built successfully"
            } else {
                throw "Failed to build frontend image"
            }
        } finally {
            Pop-Location
        }

        # Verify images
        Write-Info "Verifying images..."
        $images = docker images | Select-String "todo"
        if ($images.Count -ge 2) {
            Write-Info "Found required images"
        } else {
            Write-Warning "Expected 2 todo images, found less than 2"
        }
    } else {
        Write-Info "Skipping Docker build (assumed to be completed)"
    }

    # Create namespace
    Write-Info "Creating namespace..."
    kubectl create namespace todo-app --dry-run=client -o yaml | kubectl apply -f -
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Namespace may already exist"
    }

    # Check if secrets file exists
    $secretsFile = "./secrets.yaml"
    if (-not (Test-Path $secretsFile)) {
        Write-Warning "Secrets file '$secretsFile' not found!"
        Write-Info "Please create a secrets.yaml file with your sensitive configuration:"
        Write-Info @"
# secrets.yaml - SAMPLE CONFIGURATION (fill in with real values)
# DO NOT COMMIT THIS FILE TO VERSION CONTROL
secrets:
  databaseUrl: "YOUR_NEON_DATABASE_URL_HERE"
  secretKey: "YOUR_JWT_SECRET_KEY_HERE_MINIMUM_32_CHARS"
  openaiApiKey: "YOUR_OPENAI_API_KEY_HERE"
"@
        Write-Info "Then run this script again or proceed with manual Helm installation."
        exit 0
    } else {
        Write-Info "Found secrets file: $secretsFile"
    }

    # Install Helm release if not skipped
    if (-not $SkipHelmInstall) {
        Write-Info "Installing Helm release..."

        # First, validate the chart
        Write-Info "Validating Helm chart..."
        helm lint specs/infra/helm/todo-chatbot/
        if ($LASTEXITCODE -ne 0) {
            Write-Warning "Helm lint found issues (may be acceptable for local dev)"
        }

        # Install the release
        Write-Info "Installing Helm release 'todo'..."
        helm upgrade --install todo specs/infra/helm/todo-chatbot/ --namespace todo-app --values $secretsFile --wait --timeout=10m
        if ($LASTEXITCODE -eq 0) {
            Write-Info "Helm release installed successfully!"
        } else {
            Write-Error "Failed to install Helm release"
            exit 1
        }
    } else {
        Write-Info "Skipping Helm installation (assumed to be completed)"
    }

    # Wait for pods to be ready
    Write-Info "Waiting for pods to be ready..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo -n todo-app --timeout=300s
    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Some pods may still be starting up..."
    }

    # Show deployment status
    Write-Info "Deployment status:"
    kubectl get all -n todo-app

    # Show pod logs
    Write-Info "Backend pod logs:"
    kubectl logs -l app=todo-backend -n todo-app --tail=10

    Write-Info "Frontend pod logs:"
    kubectl logs -l app=todo-frontend -n todo-app --tail=10

    # Provide access instructions
    Write-Info "=============================================="
    Write-Info "DEPLOYMENT COMPLETED SUCCESSFULLY!"
    Write-Info "=============================================="
    Write-Info ""
    Write-Info "To access the application:"
    Write-Info "1. Port forward the services:"
    Write-Info "   Terminal 1: kubectl port-forward svc/todo-backend 8000:8000 -n todo-app"
    Write-Info "   Terminal 2: kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app"
    Write-Info "   Browser: http://localhost:3000"
    Write-Info ""
    Write-Info "Alternative access via Minikube:"
    Write-Info "   minikube service todo-frontend -n todo-app --url"
    Write-Info ""
    Write-Info "To verify health: curl http://localhost:8000/health (after port forward)"
    Write-Info ""
    Write-Info "To view all resources: kubectl get all -n todo-app"
    Write-Info "To view logs: kubectl logs -l app=todo-backend -n todo-app"
    Write-Info ""
    Write-Info "For cleanup: helm uninstall todo -n todo-app && kubectl delete namespace todo-app"
}

# Call the main function
Start-Deployment