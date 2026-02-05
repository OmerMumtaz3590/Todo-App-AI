# AI-Assisted Kubernetes Operations

**Phase**: IV - Cloud-Native Local Deployment
**Purpose**: Document kubectl-ai and kagent usage patterns for Todo Chatbot

## Overview

AI-assisted tooling enhances Kubernetes operations by allowing natural language commands and intelligent cluster analysis. These tools are recommended per Constitution Section X (DIS-012).

## kubectl-ai Patterns

kubectl-ai translates natural language into kubectl commands or Kubernetes manifests.

### Pattern 1: Scale Deployment

**Use case**: Adjust replica count for a deployment

```bash
# Natural language
kubectl-ai "Scale todo-backend to 3 replicas in namespace todo-app"

# Generated command
kubectl scale deployment todo-backend --replicas=3 -n todo-app

# Alternative: Generate HPA manifest
kubectl-ai "Create HPA for todo-backend with min 1, max 5 at 70% CPU"
```

**Output example**:
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: todo-backend-hpa
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: todo-backend
  minReplicas: 1
  maxReplicas: 5
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### Pattern 2: View Pod Logs

**Use case**: Debug application issues by viewing logs

```bash
# Recent logs
kubectl-ai "Show logs from todo-backend pod in the last 10 minutes"

# Generated command
kubectl logs -l app=todo-backend -n todo-app --since=10m

# Error logs only
kubectl-ai "Show error logs from todo-frontend"

# Generated command
kubectl logs -l app=todo-frontend -n todo-app | grep -i error

# Follow logs in real-time
kubectl-ai "Stream live logs from todo-backend"

# Generated command
kubectl logs -f deployment/todo-backend -n todo-app
```

### Pattern 3: Describe Resources

**Use case**: Get detailed information about Kubernetes resources

```bash
# Describe deployment
kubectl-ai "Describe the todo-frontend deployment"

# Generated command
kubectl describe deployment todo-frontend -n todo-app

# Describe pod
kubectl-ai "Show details of the crashing todo-backend pod"

# Generated command
kubectl describe pod -l app=todo-backend -n todo-app

# Describe service
kubectl-ai "What endpoints does the todo-backend service have?"

# Generated command
kubectl describe svc todo-backend -n todo-app
```

### Pattern 4: Debug Pod Issues

**Use case**: Diagnose why a pod is not working

```bash
# Generic debug
kubectl-ai "Why is the todo-backend pod not ready?"

# Generated output
# 1. kubectl get pods -n todo-app -l app=todo-backend
# 2. kubectl describe pod <pod-name> -n todo-app
# 3. kubectl logs <pod-name> -n todo-app --previous (if restarting)
# Analysis: Pod is failing readiness probe, database connection refused

# Check events
kubectl-ai "Show recent events for todo-app namespace"

# Generated command
kubectl get events -n todo-app --sort-by='.lastTimestamp' --field-selector type!=Normal

# Check resource usage
kubectl-ai "Is todo-backend running out of memory?"

# Generated command
kubectl top pod -l app=todo-backend -n todo-app
```

### Pattern 5: Generate Manifests

**Use case**: Create Kubernetes resource definitions

```bash
# Create ConfigMap
kubectl-ai "Create a ConfigMap named app-config with key DEBUG=true"

# Generated manifest
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: todo-app
data:
  DEBUG: "true"

# Create Secret (careful with this!)
kubectl-ai "Create a secret for database credentials"

# Generated command (prompts for values)
kubectl create secret generic db-credentials \
  --from-literal=DATABASE_URL='...' \
  -n todo-app

# Create NetworkPolicy
kubectl-ai "Allow only frontend to access backend on port 8000"

# Generated manifest
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: backend-ingress
  namespace: todo-app
spec:
  podSelector:
    matchLabels:
      app: todo-backend
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: todo-frontend
    ports:
    - port: 8000
```

### Pattern 6: Rollout Management

**Use case**: Manage deployment updates

```bash
# Check rollout status
kubectl-ai "Is the todo-backend rollout complete?"

# Generated command
kubectl rollout status deployment/todo-backend -n todo-app

# Rollback
kubectl-ai "Rollback todo-frontend to the previous version"

# Generated command
kubectl rollout undo deployment/todo-frontend -n todo-app

# View rollout history
kubectl-ai "Show deployment history for todo-backend"

# Generated command
kubectl rollout history deployment/todo-backend -n todo-app
```

### Pattern 7: Execute Commands in Pods

**Use case**: Debug or inspect running containers

```bash
# Open shell
kubectl-ai "Open a shell in the todo-backend pod"

# Generated command
kubectl exec -it deployment/todo-backend -n todo-app -- /bin/sh

# Run specific command
kubectl-ai "Check environment variables in todo-backend"

# Generated command
kubectl exec deployment/todo-backend -n todo-app -- env | grep -E '(DATABASE|SECRET|OPENAI)'

# Test network connectivity
kubectl-ai "Can todo-frontend reach todo-backend on port 8000?"

# Generated command
kubectl exec deployment/todo-frontend -n todo-app -- \
  wget -q -O- http://todo-backend:8000/health
```

## kagent Patterns

kagent provides intelligent cluster analysis and troubleshooting.

### Pattern 1: Cluster Health Analysis

**Use case**: Overall cluster health check

```bash
# Full health report
kagent analyze --namespace todo-app

# Example output
┌──────────────────────────────────────────────────────────────┐
│ Cluster Health Report - todo-app namespace                    │
├──────────────────────────────────────────────────────────────┤
│ Status: ⚠️  Warning                                           │
│                                                               │
│ Pods: 2/2 Running                                             │
│ Services: 2/2 Available                                       │
│ Deployments: 2/2 Ready                                        │
│                                                               │
│ Issues Found:                                                 │
│ - todo-backend: High restart count (3 in last hour)          │
│ - todo-frontend: Resource limits not set                      │
│                                                               │
│ Recommendations:                                              │
│ 1. Check backend logs for crash reason                        │
│ 2. Add resource limits to frontend deployment                 │
└──────────────────────────────────────────────────────────────┘
```

### Pattern 2: Resource Utilization

**Use case**: Monitor resource usage and optimization

```bash
# Resource report
kagent report resources --namespace todo-app

# Example output
┌─────────────────────────────────────────────────────────────┐
│ Resource Utilization - todo-app                              │
├─────────────────────────────────────────────────────────────┤
│ Pod                   CPU (req/lim)    Memory (req/lim)      │
│ ─────────────────────────────────────────────────────────── │
│ todo-backend-abc123   45m/100m-500m    180Mi/256Mi-512Mi    │
│ todo-frontend-xyz789  30m/100m-500m    220Mi/256Mi-512Mi    │
├─────────────────────────────────────────────────────────────┤
│ Total Namespace       75m/200m-1000m   400Mi/512Mi-1024Mi   │
│ Node Capacity         2000m            4096Mi               │
│ Utilization           3.75%            9.8%                 │
├─────────────────────────────────────────────────────────────┤
│ Optimization Suggestions:                                    │
│ - Backend CPU request (100m) underutilized by 55%           │
│ - Consider reducing requests or adding HPA                   │
└─────────────────────────────────────────────────────────────┘
```

### Pattern 3: Troubleshooting

**Use case**: Diagnose specific problems

```bash
# Troubleshoot pod
kagent troubleshoot pod todo-backend-abc123 -n todo-app

# Example output
┌─────────────────────────────────────────────────────────────┐
│ Troubleshooting: todo-backend-abc123                         │
├─────────────────────────────────────────────────────────────┤
│ Status: CrashLoopBackOff                                     │
│ Restarts: 5                                                  │
│ Last State: Terminated (Error, exit code 1)                  │
│                                                               │
│ Root Cause Analysis:                                          │
│ ✗ Container exited with error code 1                         │
│ ✗ Log analysis: "DATABASE_URL environment variable not set"  │
│                                                               │
│ Diagnosis:                                                    │
│ The application requires DATABASE_URL but the secret is      │
│ not properly mounted or the secret key is misspelled.        │
│                                                               │
│ Remediation Steps:                                            │
│ 1. Verify secret exists: kubectl get secret -n todo-app      │
│ 2. Check secret keys: kubectl describe secret todo-secrets   │
│ 3. Verify env mount in deployment spec                        │
│ 4. Restart deployment after fixing                            │
└─────────────────────────────────────────────────────────────┘

# Troubleshoot service
kagent troubleshoot service todo-backend -n todo-app

# Example output
┌─────────────────────────────────────────────────────────────┐
│ Service Troubleshooting: todo-backend                        │
├─────────────────────────────────────────────────────────────┤
│ Service Type: ClusterIP                                      │
│ Port: 8000                                                   │
│ Endpoints: 10.244.0.5:8000                                   │
│                                                               │
│ Connectivity Test:                                            │
│ ✓ DNS resolution: todo-backend.todo-app.svc.cluster.local   │
│ ✓ Endpoint reachable: HTTP 200 OK                            │
│ ✓ Health check passing: /health returns healthy              │
│                                                               │
│ Status: Service is healthy                                    │
└─────────────────────────────────────────────────────────────┘
```

### Pattern 4: Security Audit

**Use case**: Check for security issues

```bash
# Security scan
kagent audit security --namespace todo-app

# Example output
┌─────────────────────────────────────────────────────────────┐
│ Security Audit - todo-app                                    │
├─────────────────────────────────────────────────────────────┤
│ ⚠️  Warnings: 2                                               │
│ ✗  Violations: 0                                              │
│                                                               │
│ Warnings:                                                     │
│ 1. todo-backend: No NetworkPolicy defined                     │
│    → Pods can receive traffic from any source                 │
│    → Recommendation: Add NetworkPolicy to restrict ingress    │
│                                                               │
│ 2. todo-frontend: Container runs as root                      │
│    → Security best practice violation                         │
│    → Recommendation: Add securityContext with runAsNonRoot   │
│                                                               │
│ Passed Checks:                                                │
│ ✓ Secrets not exposed in environment                          │
│ ✓ No privileged containers                                    │
│ ✓ Resource limits defined                                     │
└─────────────────────────────────────────────────────────────┘
```

## Best Practices

### When to Use kubectl-ai

- Quick one-off commands you don't remember syntax for
- Generating manifest templates
- Debugging pod issues with natural language questions
- Learning kubectl by seeing generated commands

### When to Use kagent

- Comprehensive health checks before deployments
- Root cause analysis of complex issues
- Resource optimization recommendations
- Security audits

### Workflow Integration

```bash
# Pre-deployment check
kagent analyze --namespace todo-app

# Deploy
helm upgrade todo specs/infra/helm/todo-chatbot -n todo-app

# Post-deployment verification
kubectl-ai "Are all pods in todo-app namespace ready?"

# If issues arise
kagent troubleshoot deployment todo-backend -n todo-app

# Performance check
kagent report resources --namespace todo-app
```

## Installation

### kubectl-ai

```bash
# macOS/Linux
brew install kubectl-ai

# Windows
choco install kubectl-ai

# Verify
kubectl-ai --version
```

### kagent

```bash
# macOS/Linux
brew install kagent

# Windows
choco install kagent

# Verify
kagent --version
```

## Configuration

Both tools may require API keys for LLM functionality:

```bash
# Set OpenAI API key (if using OpenAI backend)
export OPENAI_API_KEY="sk-..."

# Or configure in tool-specific config
kubectl-ai config set api-key "sk-..."
kagent config set api-key "sk-..."
```
