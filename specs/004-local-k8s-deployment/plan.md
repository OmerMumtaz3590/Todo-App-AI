# Implementation Plan: Local Kubernetes Deployment

**Branch**: `004-local-k8s-deployment` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-local-k8s-deployment/spec.md`

## Summary

Containerize the Todo Chatbot application (Next.js frontend + FastAPI backend) using Docker multi-stage builds, deploy to a local Minikube cluster via Helm charts, and establish AI-assisted operations patterns using kubectl-ai and kagent. This is a deployment-only phase with no application code changes.

## Technical Context

**Language/Version**: Python 3.11+ (backend), Node.js 18+ (frontend), YAML (Kubernetes manifests)
**Primary Dependencies**: Docker, Minikube, Helm 3.x, kubectl, kubectl-ai, kagent, Gordon (Docker AI Agent)
**Storage**: Neon PostgreSQL (external, connection string via K8s Secret)
**Testing**: Manual verification via `docker run`, `helm test`, `kubectl get pods`
**Target Platform**: Local Minikube cluster (single-node Kubernetes)
**Project Type**: Infrastructure/DevOps (no application code changes)
**Performance Goals**: Pod startup < 60s, rollback < 60s, image build < 5 minutes
**Constraints**: Single backend container, single frontend container (no microservices per DIS-002)
**Scale/Scope**: 1 replica each for local development, configurable via values.yaml

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Phase Compliance** (per Constitution Section III):
- [x] Current phase identified: Phase IV
- [x] No future-phase technologies used (RULE PG-002) — No Kafka, Dapr, service mesh
- [x] Architecture appropriate for current phase (RULE PG-003) — Minikube, not production cloud

**Spec-Driven Compliance** (per Constitution Section I):
- [x] Specification approved before this plan (RULE SDD-004) — spec.md complete
- [x] No features beyond specification scope (RULE SDD-002) — deployment only

**Technology Compliance** (per Constitution Section IV):
- [x] Only phase-appropriate technologies used (RULE TC-001) — Docker, K8s, Helm all Phase IV
- [x] Additional libraries justified (RULE TC-003) — Gordon, kubectl-ai, kagent per constitution

**Quality Compliance** (per Constitution Section V):
- [x] Clean architecture principles followed (RULE QP-001 to QP-004) — infrastructure separation
- [x] Type hints planned for all public functions (RULE QP-008) — N/A (no code changes)
- [x] Error handling strategy defined (RULE QP-009) — health probes, rollback

**Phase IV Infrastructure Compliance** (per Constitution Section X):
- [x] All services run in Kubernetes (DIS-001)
- [x] Separate Dockerfiles for frontend and backend (DIS-002)
- [x] Gordon preferred for Dockerfile creation (DIS-003)
- [x] Multi-stage builds required (DIS-004)
- [x] No embedded secrets in images (DIS-005)
- [x] Minikube target environment (DIS-010)
- [x] Helm Charts required (DIS-011)
- [x] AI-assisted tooling used (DIS-012)
- [x] Config stored under specs/infra/ (DIS-013)
- [x] Health probes required (DIS-014)
- [x] Secrets in K8s Secrets (DIS-020)
- [x] values.yaml for all params (DIS-021)
- [x] Non-root containers (DIS-023)

## Project Structure

### Documentation (this feature)

```text
specs/004-local-k8s-deployment/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Technology decisions
├── quickstart.md        # Phase 1: Deployment guide
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Infrastructure Configuration (specs/infra/)

```text
specs/infra/
├── docker/
│   ├── backend.Dockerfile       # FastAPI container
│   └── frontend.Dockerfile      # Next.js container
├── helm/
│   └── todo-chatbot/            # Helm chart
│       ├── Chart.yaml           # Chart metadata
│       ├── values.yaml          # Default values
│       └── templates/
│           ├── _helpers.tpl     # Template helpers
│           ├── backend-deployment.yaml
│           ├── backend-service.yaml
│           ├── frontend-deployment.yaml
│           ├── frontend-service.yaml
│           ├── secrets.yaml
│           ├── configmap.yaml
│           └── ingress.yaml     # Optional
├── minikube/
│   └── setup.md                 # Minikube configuration guide
└── aiops/
    └── patterns.md              # kubectl-ai & kagent usage patterns
```

### Application Code (no changes)

```text
backend/
├── src/
│   ├── main.py          # FastAPI app (port 8000, /health endpoint)
│   ├── config.py        # Environment variables
│   ├── models/          # SQLModel entities
│   ├── api/             # Route handlers
│   └── services/        # Business logic
├── requirements.txt     # Python dependencies
└── alembic/             # Database migrations

frontend/
├── app/                 # Next.js 15 App Router
├── components/          # React components
├── services/            # API client
├── package.json         # Node dependencies
└── next.config.js       # Build configuration
```

**Structure Decision**: Infrastructure-only changes. All new files go under `specs/infra/`. Application code remains unchanged. Dockerfiles placed adjacent to their respective service directories during implementation but defined in specs/infra/.

## Implementation Phases

### Phase 1: Containerization (US1)

| Step | Description | Tools/Commands | Dependencies |
|------|-------------|----------------|--------------|
| 1.1 | Create backend Dockerfile | Gordon → `backend/Dockerfile` | None |
| 1.2 | Create frontend Dockerfile | Gordon → `frontend/Dockerfile` | None |
| 1.3 | Build backend image | `docker build -t todo-backend:local ./backend` | 1.1 |
| 1.4 | Build frontend image | `docker build -t todo-frontend:local ./frontend` | 1.2 |
| 1.5 | Test backend container | `docker run -p 8000:8000 todo-backend:local` | 1.3 |
| 1.6 | Test frontend container | `docker run -p 3000:3000 todo-frontend:local` | 1.4 |
| 1.7 | Verify non-root user | `docker exec <id> whoami` | 1.5, 1.6 |
| 1.8 | Verify no embedded secrets | `docker history`, `docker inspect` | 1.5, 1.6 |

**Backend Dockerfile Requirements**:
- Base: `python:3.11-slim`
- Multi-stage: builder + runtime
- Non-root user: `appuser` (UID 1000)
- Workdir: `/app`
- Port: 8000
- Entrypoint: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
- No .env file copied (secrets via environment)

**Frontend Dockerfile Requirements**:
- Base: `node:18-alpine`
- Multi-stage: deps → builder → runner
- Non-root user: `nextjs` (UID 1001)
- Workdir: `/app`
- Port: 3000
- Entrypoint: `npm start` or `node server.js` (standalone)
- Build-time: `NEXT_PUBLIC_API_URL` as ARG

### Phase 2: Minikube Setup (US2 - Part 1)

| Step | Description | Tools/Commands | Dependencies |
|------|-------------|----------------|--------------|
| 2.1 | Start Minikube | `minikube start --memory=4096 --cpus=2` | None |
| 2.2 | Enable ingress addon | `minikube addons enable ingress` | 2.1 |
| 2.3 | Configure Docker env | `eval $(minikube docker-env)` | 2.1 |
| 2.4 | Build images in Minikube | `docker build` (inside Minikube Docker) | 2.3, Phase 1 |
| 2.5 | Verify images available | `minikube ssh -- docker images` | 2.4 |

**Minikube Configuration**:
- Driver: docker (Windows default)
- Memory: 4096 MB minimum
- CPUs: 2 minimum
- Kubernetes version: stable (v1.28+)
- Addons: ingress, dashboard (optional)

### Phase 3: Helm Chart Creation (US2 - Part 2)

| Step | Description | Tools/Commands | Dependencies |
|------|-------------|----------------|--------------|
| 3.1 | Create chart scaffold | `helm create todo-chatbot` | None |
| 3.2 | Define Chart.yaml | Chart name, version, appVersion | 3.1 |
| 3.3 | Define values.yaml | All configurable parameters | 3.1 |
| 3.4 | Create backend deployment | `templates/backend-deployment.yaml` | 3.3 |
| 3.5 | Create backend service | `templates/backend-service.yaml` | 3.4 |
| 3.6 | Create frontend deployment | `templates/frontend-deployment.yaml` | 3.3 |
| 3.7 | Create frontend service | `templates/frontend-service.yaml` | 3.6 |
| 3.8 | Create secrets template | `templates/secrets.yaml` | 3.3 |
| 3.9 | Create configmap template | `templates/configmap.yaml` | 3.3 |
| 3.10 | Create ingress template | `templates/ingress.yaml` (optional) | 3.5, 3.7 |
| 3.11 | Lint chart | `helm lint specs/infra/helm/todo-chatbot` | 3.4-3.10 |

**values.yaml Structure**:
```yaml
# Image configuration
backend:
  image:
    repository: todo-backend
    tag: local
    pullPolicy: IfNotPresent
  replicas: 1
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  service:
    type: ClusterIP
    port: 8000

frontend:
  image:
    repository: todo-frontend
    tag: local
    pullPolicy: IfNotPresent
  replicas: 1
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  service:
    type: ClusterIP
    port: 3000

# Secrets (base64 encoded in secrets.yaml)
secrets:
  databaseUrl: ""      # Required: Neon PostgreSQL connection string
  secretKey: ""        # Required: JWT secret (min 32 chars)
  openaiApiKey: ""     # Required: OpenAI API key

# ConfigMap (non-sensitive)
config:
  appName: "Todo API"
  debug: "false"
  algorithm: "HS256"
  accessTokenExpireMinutes: "1440"
  corsOrigins: '["http://localhost:3000"]'

# Ingress (optional)
ingress:
  enabled: false
  className: nginx
  host: todo.local
```

### Phase 4: Deployment Workflow (US2 - Part 3)

| Step | Description | Tools/Commands | Dependencies |
|------|-------------|----------------|--------------|
| 4.1 | Create namespace | `kubectl create namespace todo-app` | Phase 2 |
| 4.2 | Create secrets file | `secrets.yaml` with base64 values | 4.1 |
| 4.3 | Install Helm release | `helm install todo specs/infra/helm/todo-chatbot -n todo-app -f secrets.yaml` | Phase 3, 4.2 |
| 4.4 | Verify pods running | `kubectl get pods -n todo-app` | 4.3 |
| 4.5 | Verify services | `kubectl get svc -n todo-app` | 4.3 |
| 4.6 | Port-forward backend | `kubectl port-forward svc/todo-backend 8000:8000 -n todo-app` | 4.4 |
| 4.7 | Port-forward frontend | `kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app` | 4.4 |
| 4.8 | Test application | Browser → `http://localhost:3000` | 4.6, 4.7 |
| 4.9 | Test upgrade | `helm upgrade todo specs/infra/helm/todo-chatbot -n todo-app` | 4.3 |
| 4.10 | Test rollback | `helm rollback todo -n todo-app` | 4.9 |

**Health Probes Configuration**:
```yaml
# Backend
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 5

# Frontend
livenessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 10
readinessProbe:
  httpGet:
    path: /
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 5
```

### Phase 5: AI-Assisted Operations (US3)

| Step | Description | Tools/Commands | Dependencies |
|------|-------------|----------------|--------------|
| 5.1 | Document kubectl-ai patterns | `specs/infra/aiops/patterns.md` | Phase 4 |
| 5.2 | Document kagent patterns | `specs/infra/aiops/patterns.md` | Phase 4 |
| 5.3 | Test kubectl-ai manifest generation | Natural language → YAML | 5.1 |
| 5.4 | Test kagent cluster analysis | Cluster state → Health report | 5.2 |

**kubectl-ai Patterns** (minimum 5):
1. Scale deployment: "Scale todo-backend to 3 replicas"
2. Get pod logs: "Show logs from the todo-backend pod"
3. Describe resource: "Describe the todo-frontend deployment"
4. Create HPA: "Create HorizontalPodAutoscaler for backend with min 1 max 5 at 70% CPU"
5. Debug pod: "Why is the todo-backend pod not ready?"

**kagent Patterns** (minimum 3):
1. Cluster health: "Analyze cluster health and report issues"
2. Resource usage: "Show resource utilization for todo-app namespace"
3. Troubleshoot: "Why are pods in CrashLoopBackOff?"

### Phase 6: Verification & Documentation

| Step | Description | Tools/Commands | Dependencies |
|------|-------------|----------------|--------------|
| 6.1 | End-to-end test | Sign in → Chat → Manage todos | Phase 4 |
| 6.2 | Pod crash recovery test | `kubectl delete pod` → verify restart | Phase 4 |
| 6.3 | Write quickstart.md | Complete deployment guide | All phases |
| 6.4 | Copy Dockerfiles to specs/infra | Version control | Phase 1 |
| 6.5 | Commit all artifacts | Git commit | 6.4 |

## Environment Variables

### Backend Container

| Variable | Source | Required | Description |
|----------|--------|----------|-------------|
| DATABASE_URL | Secret | Yes | Neon PostgreSQL connection string |
| SECRET_KEY | Secret | Yes | JWT signing key (min 32 chars) |
| OPENAI_API_KEY | Secret | Yes | OpenAI API key for agents |
| ALGORITHM | ConfigMap | No | JWT algorithm (default: HS256) |
| ACCESS_TOKEN_EXPIRE_MINUTES | ConfigMap | No | Token expiry (default: 1440) |
| APP_NAME | ConfigMap | No | Application name |
| DEBUG | ConfigMap | No | Debug mode (default: false) |
| CORS_ORIGINS | ConfigMap | No | Allowed CORS origins (JSON array) |
| HOST | Hardcoded | No | 0.0.0.0 |
| PORT | Hardcoded | No | 8000 |

### Frontend Container

| Variable | Source | Required | Description |
|----------|--------|----------|-------------|
| NEXT_PUBLIC_API_URL | Build ARG / ConfigMap | Yes | Backend API URL (K8s service DNS) |
| NEXT_PUBLIC_APP_NAME | Build ARG | No | Application name |
| NODE_ENV | Hardcoded | No | production |
| PORT | Hardcoded | No | 3000 |

**Frontend-to-Backend Discovery**:
- Inside cluster: `http://todo-backend.todo-app.svc.cluster.local:8000`
- Via ingress: Configured in ingress rule
- Via port-forward: `http://localhost:8000`

## Complexity Tracking

> No Constitution Check violations. All Phase IV rules followed.

| Concern | Resolution |
|---------|------------|
| Frontend needs backend URL at build time | Use ARG for build-time injection, or runtime JS config |
| Secrets management | Helm values with --set or separate secrets.yaml file (gitignored) |
| Minikube Docker daemon | Use `eval $(minikube docker-env)` to build directly |
| Database migrations | Run manually or as init container (out of scope for Phase IV MVP) |

## Dependencies Summary

```
Phase 1 (Containerization)
├── 1.1 Backend Dockerfile → 1.3 Build → 1.5 Test
├── 1.2 Frontend Dockerfile → 1.4 Build → 1.6 Test
└── 1.5, 1.6 → 1.7, 1.8 (Verification)

Phase 2 (Minikube) ← Phase 1
└── 2.1 Start → 2.2 Ingress → 2.3 Docker env → 2.4 Build in cluster → 2.5 Verify

Phase 3 (Helm) [Parallel with Phase 2]
└── 3.1 Scaffold → 3.2-3.10 Templates → 3.11 Lint

Phase 4 (Deployment) ← Phase 2, Phase 3
└── 4.1 Namespace → 4.2 Secrets → 4.3 Install → 4.4-4.10 Verify/Test

Phase 5 (AI-Ops) ← Phase 4
└── 5.1-5.2 Document → 5.3-5.4 Test

Phase 6 (Verification) ← All
└── 6.1-6.5 Test, Document, Commit
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Minikube resource exhaustion | Set resource limits in values.yaml; document minimum requirements |
| Database unreachable | Health check fails → pod restart; document network requirements |
| Image build failures | Multi-stage isolation; clear error messages; Gordon assistance |
| CORS issues in cluster | Configure CORS_ORIGINS to include K8s service URLs |
| Secrets exposure | Never commit secrets.yaml; use Helm --set or sealed-secrets |
