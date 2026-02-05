# Research: Local Kubernetes Deployment

**Feature**: 004-local-k8s-deployment
**Date**: 2026-02-04

## Technology Decisions

### 1. Docker Base Images

**Decision**: `python:3.11-slim` for backend, `node:18-alpine` for frontend

**Rationale**:
- `python:3.11-slim` (143MB) vs `python:3.11` (1GB) — significant size reduction
- Slim includes essential build tools for pip install, then removed in multi-stage
- `node:18-alpine` (48MB) — smallest Node.js image, sufficient for Next.js standalone
- Alpine uses musl libc which is fully compatible with Next.js

**Alternatives Considered**:
- `python:3.11-alpine`: Smaller but requires additional build tools for psycopg2
- `python:3.12`: Not all dependencies tested on 3.12 yet
- `node:20-alpine`: Next.js 15 officially supports Node 18+, 20 is optional

### 2. Kubernetes Environment

**Decision**: Minikube with Docker driver

**Rationale**:
- Minikube is the constitutionally mandated tool (DIS-010)
- Docker driver is default on Windows and works with Docker Desktop
- Single-node cluster is sufficient for local development
- Built-in addons (ingress, dashboard) simplify configuration

**Alternatives Considered**:
- Kind (Kubernetes in Docker): Faster startup but less feature-rich
- Docker Desktop Kubernetes: Simpler but less configurable
- k3d (k3s in Docker): Lightweight but less compatible with production K8s

### 3. Container Registry Strategy

**Decision**: Build images directly into Minikube's Docker daemon

**Rationale**:
- `eval $(minikube docker-env)` points Docker CLI to Minikube's daemon
- No external registry needed for local development
- Images immediately available to Kubernetes without push/pull
- Simpler workflow: build → deploy (no registry step)

**Alternatives Considered**:
- Docker Hub: Requires account, push/pull latency, not needed for local dev
- Minikube registry addon: Additional complexity, useful for CI/CD later
- Local registry container: Overkill for single-developer workflow

### 4. Helm Chart Structure

**Decision**: Single unified chart for the entire application

**Rationale**:
- Application is tightly coupled (frontend needs backend URL)
- Simpler deployment: one `helm install` command
- Shared secrets and configmaps
- Phase IV scope is local dev only — microservices separation is Phase V

**Alternatives Considered**:
- Separate charts per service: Better for microservices, overkill for Phase IV
- Umbrella chart with subcharts: Adds complexity without benefit here

### 5. Secrets Management

**Decision**: Kubernetes Secrets via Helm values with separate secrets.yaml file

**Rationale**:
- Constitution requires K8s Secrets (DIS-020)
- Helm `--set` or `-f secrets.yaml` injects values at deploy time
- `secrets.yaml` is gitignored — never committed
- Base64 encoding handled by Helm template

**Alternatives Considered**:
- Sealed Secrets: Enterprise-grade, overkill for local dev
- External Secrets Operator: Requires external secret store (Vault, AWS SM)
- HashiCorp Vault: Production-ready but complex setup
- SOPS: Good for GitOps, adds encryption key management

### 6. Frontend-Backend Communication

**Decision**: Kubernetes Service DNS with build-time API URL injection

**Rationale**:
- Next.js requires `NEXT_PUBLIC_API_URL` at build time for client-side code
- Inside cluster: `http://todo-backend.todo-app.svc.cluster.local:8000`
- ARG in Dockerfile allows different URLs per environment
- Service-to-service communication uses ClusterIP (internal only)

**Alternatives Considered**:
- Runtime environment variable: Not supported for NEXT_PUBLIC_* vars
- API proxy in Next.js: Works but adds latency
- Hardcoded URL: Not portable across environments

### 7. Health Check Strategy

**Decision**: HTTP GET probes on existing endpoints

**Rationale**:
- Backend already has `/health` endpoint (returns 200 OK)
- Frontend responds to `/` with 200 when healthy
- Kubernetes liveness probe: restart on failure
- Kubernetes readiness probe: remove from service on failure
- Different timing: backend faster startup, frontend needs longer

**Alternatives Considered**:
- TCP socket probe: Less informative, just checks port open
- Exec probe: Adds complexity, no benefit for HTTP services
- gRPC probe: Not applicable (HTTP services)

### 8. Resource Limits

**Decision**: 256Mi-512Mi memory, 100m-500m CPU per container

**Rationale**:
- Backend (FastAPI): Light memory footprint, CPU for request handling
- Frontend (Next.js): Higher memory for SSR, moderate CPU
- Minikube default: 4GB RAM, 2 CPUs — allows headroom for system
- Limits prevent runaway processes from affecting other pods

**Alternatives Considered**:
- No limits: Risk of resource exhaustion on constrained Minikube
- Higher limits: Wastes resources on single-node cluster
- Lower limits: Risk of OOM kills during peak load

### 9. Ingress Controller

**Decision**: Optional NGINX Ingress (disabled by default)

**Rationale**:
- Port-forward is simpler for local development
- Ingress useful for testing production-like routing
- NGINX is Minikube's default ingress controller
- Can be enabled in values.yaml when needed

**Alternatives Considered**:
- Traefik: More features but more complex
- Contour: Envoy-based, enterprise-grade
- Ambassador: API Gateway focus, overkill here

### 10. AI-Assisted Tooling

**Decision**: kubectl-ai for manifest generation, kagent for troubleshooting

**Rationale**:
- Constitution requires AI-assisted tooling (DIS-012)
- kubectl-ai: Natural language → kubectl commands or YAML manifests
- kagent: Cluster analysis, problem diagnosis, remediation suggestions
- Both tools enhance developer productivity without being required for core functionality

**Alternatives Considered**:
- K9s: Great TUI but not AI-powered
- Lens: GUI-focused, not CLI-native
- k8sgpt: Alternative to kagent, similar functionality

## Codebase Analysis Summary

### Backend (FastAPI)

| Aspect | Finding |
|--------|---------|
| Entry point | `uvicorn src.main:app --host 0.0.0.0 --port 8000` |
| Health endpoint | `GET /health` returns `{"status": "healthy"}` |
| Dependencies | 22 packages in requirements.txt (incl. OpenAI, psycopg) |
| Secrets needed | DATABASE_URL, SECRET_KEY, OPENAI_API_KEY |
| Config pattern | Pydantic Settings with env file support |
| Build artifacts | `__pycache__/`, `.pytest_cache/`, `*.pyc` |

### Frontend (Next.js)

| Aspect | Finding |
|--------|---------|
| Entry point | `npm start` → Next.js production server |
| Health endpoint | `GET /` returns 200 |
| Dependencies | 10 packages (Next 15, React 19, Tailwind) |
| Build command | `npm run build` → `.next/` directory |
| Runtime vars | `NEXT_PUBLIC_API_URL` (build-time) |
| Build artifacts | `.next/`, `node_modules/` (8000+ files) |

### Docker Build Considerations

| Challenge | Solution |
|-----------|----------|
| Python wheel compilation | Multi-stage: compile in builder, copy wheels to runtime |
| Node modules size | Multi-stage: deps → build → standalone (prunes devDependencies) |
| Next.js standalone | Enable `output: 'standalone'` in next.config.js |
| Non-root execution | Create appuser/nextjs users with explicit UIDs |
| Secrets in layers | Never COPY .env files; use ENV only at runtime |

## Open Questions Resolved

| Question | Resolution |
|----------|------------|
| Where to store Dockerfiles? | `backend/Dockerfile`, `frontend/Dockerfile` (also copy to specs/infra/) |
| How to pass secrets? | Helm values → K8s Secrets → env vars |
| Database migrations? | Manual via `alembic upgrade head` (out of scope for Phase IV) |
| Frontend API URL? | Build-time ARG for NEXT_PUBLIC_*, runtime for SSR |
| Windows Minikube driver? | Docker driver (default, works with Docker Desktop) |
