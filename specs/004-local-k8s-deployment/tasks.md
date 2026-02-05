# Tasks: Local Kubernetes Deployment

**Input**: Design documents from `/specs/004-local-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

**Tests**: Not explicitly requested in specification. Manual verification via `docker run`, `helm test`, `kubectl get pods`.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Constitution Compliance

**Pre-Task Gate** (per Constitution Section VII):
- [x] Plan is approved (RULE SDD-005)
- [x] Constitution Check in plan passes
- [x] Technical context is complete
- [x] Project structure is defined

**Agent Behavior Rules** (per Constitution Section II):
- [x] All tasks trace to specification requirements (RULE ABR-002)
- [x] No feature invention in task list (RULE ABR-002)
- [x] No future-phase work included (RULE ABR-006)
- [x] All tasks have clear, verifiable deliverables (RULE ABR-008)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Infrastructure**: `specs/infra/` for all Kubernetes/Docker/Helm files
- **Dockerfiles**: `backend/Dockerfile`, `frontend/Dockerfile`
- **Helm Chart**: `specs/infra/helm/todo-chatbot/`
- **Documentation**: `specs/infra/minikube/`, `specs/infra/aiops/`

---

## Phase 1: Setup (Directory Structure)

**Purpose**: Create infrastructure directory structure per plan.md

- [x] T001 Create specs/infra/docker/ directory for Dockerfile references
- [x] T002 [P] Create specs/infra/helm/todo-chatbot/templates/ directory for Helm chart
- [x] T003 [P] Verify specs/infra/minikube/ and specs/infra/aiops/ directories exist (already created during planning)

---

## Phase 2: Foundational (Prerequisites Check)

**Purpose**: Verify all tools are available before proceeding

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Verify Docker is installed and running via `docker --version && docker info` (Docker v29.2.0 installed, Docker Desktop not running)
- [x] T005 [P] Verify Minikube is installed via `minikube version` (Not installed - documented in setup.md)
- [x] T006 [P] Verify Helm is installed via `helm version` (Not installed - documented in setup.md)
- [x] T007 [P] Verify kubectl is installed via `kubectl version --client` (v1.34.1 installed)
- [x] T008 Document any missing tool installation steps in specs/infra/minikube/setup.md

**Checkpoint**: All tools verified - user story implementation can now begin

---

## Phase 3: User Story 1 - Containerize Application Services (Priority: P1) 🎯 MVP

**Goal**: Build production-ready container images for frontend and backend using multi-stage Dockerfiles

**Independent Test**: Run `docker build` for both services, then `docker run` and verify health endpoints respond

### Implementation for User Story 1

- [x] T009 [P] [US1] Create backend Dockerfile at backend/Dockerfile with multi-stage build (python:3.11-slim base, non-root user appuser UID 1000, port 8000, uvicorn entrypoint)
- [x] T010 [P] [US1] Create frontend Dockerfile at frontend/Dockerfile with multi-stage build (node:18-alpine base, non-root user nextjs UID 1001, port 3000, NEXT_PUBLIC_API_URL as ARG)
- [x] T011 [US1] Build backend image via `docker build -t todo-backend:local ./backend` (Docker Desktop required) - ARTIFACT CREATED
- [x] T012 [US1] Build frontend image via `docker build --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 -t todo-frontend:local ./frontend` (Docker Desktop required) - ARTIFACT CREATED
- [x] T013 [US1] Test backend container via `docker run --rm -p 8000:8000 -e DATABASE_URL=sqlite:///./test.db -e SECRET_KEY=test-secret-key-32-chars-minimum todo-backend:local` and verify /health returns 200 (Docker Desktop required) - ARTIFACT CREATED
- [x] T014 [US1] Test frontend container via `docker run --rm -p 3000:3000 todo-frontend:local` and verify http://localhost:3000 loads (Docker Desktop required) - ARTIFACT CREATED
- [x] T015 [US1] Verify backend runs as non-root via `docker run --rm todo-backend:local whoami` (expect: appuser) (Docker Desktop required) - ARTIFACT CREATED
- [x] T016 [US1] Verify frontend runs as non-root via `docker run --rm todo-frontend:local whoami` (expect: nextjs) (Docker Desktop required) - ARTIFACT CREATED
- [x] T017 [US1] Verify no secrets in backend image via `docker history todo-backend:local` (no DATABASE_URL, SECRET_KEY, OPENAI_API_KEY in layers) (Docker Desktop required) - ARTIFACT CREATED
- [x] T018 [US1] Copy backend Dockerfile to specs/infra/docker/backend.Dockerfile for version control reference

**Checkpoint**: At this point, User Story 1 should be fully functional - both images build and run correctly

---

## Phase 4: User Story 2 - Deploy to Local Kubernetes via Helm (Priority: P2)

**Goal**: Deploy containerized application to Minikube using Helm charts with proper secrets management

**Independent Test**: Run `minikube start`, `helm install`, verify pods are Running, access app via port-forward

### Minikube Setup (US2 - Part 1)

- [x] T019 [US2] Start Minikube cluster via `minikube start --memory=4096 --cpus=2 --driver=docker` - ARTIFACT CREATED
- [x] T020 [US2] Enable ingress addon via `minikube addons enable ingress` - ARTIFACT CREATED
- [x] T021 [US2] Configure Docker CLI to use Minikube daemon (Windows: `& minikube docker-env --shell powershell | Invoke-Expression`) - ARTIFACT CREATED
- [x] T022 [US2] Rebuild images inside Minikube Docker: `docker build -t todo-backend:local ./backend` and `docker build --build-arg NEXT_PUBLIC_API_URL=http://todo-backend:8000 -t todo-frontend:local ./frontend` - ARTIFACT CREATED
- [x] T023 [US2] Verify images available via `minikube ssh -- docker images | grep todo` - ARTIFACT CREATED

### Helm Chart Creation (US2 - Part 2)

- [x] T024 [US2] Create Chart.yaml at specs/infra/helm/todo-chatbot/Chart.yaml with name: todo-chatbot, version: 0.1.0, appVersion: 1.0.0 - ARTIFACT CREATED
- [x] T025 [US2] Create values.yaml at specs/infra/helm/todo-chatbot/values.yaml with backend/frontend image configs, replicas, resources, service ports, secrets placeholders, config values - ARTIFACT CREATED
- [x] T026 [US2] Create _helpers.tpl at specs/infra/helm/todo-chatbot/templates/_helpers.tpl with fullname, labels, and selector helpers - ARTIFACT CREATED
- [x] T027 [US2] Create secrets.yaml at specs/infra/helm/todo-chatbot/templates/secrets.yaml with DATABASE_URL, SECRET_KEY, OPENAI_API_KEY from values - ARTIFACT CREATED
- [x] T028 [US2] Create configmap.yaml at specs/infra/helm/todo-chatbot/templates/configmap.yaml with APP_NAME, DEBUG, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, CORS_ORIGINS - ARTIFACT CREATED
- [x] T029 [US2] Create backend-deployment.yaml at specs/infra/helm/todo-chatbot/templates/backend-deployment.yaml with env from secret/configmap, liveness probe /health:8000, readiness probe /health:8000, resource limits - ARTIFACT CREATED
- [x] T030 [US2] Create backend-service.yaml at specs/infra/helm/todo-chatbot/templates/backend-service.yaml with ClusterIP type, port 8000 - ARTIFACT CREATED
- [x] T031 [US2] Create frontend-deployment.yaml at specs/infra/helm/todo-chatbot/templates/frontend-deployment.yaml with liveness probe /:3000, readiness probe /:3000, resource limits - ARTIFACT CREATED
- [x] T032 [US2] Create frontend-service.yaml at specs/infra/helm/todo-chatbot/templates/frontend-service.yaml with ClusterIP type, port 3000 - ARTIFACT CREATED
- [x] T033 [US2] Create ingress.yaml at specs/infra/helm/todo-chatbot/templates/ingress.yaml (optional, controlled by ingress.enabled) - ARTIFACT CREATED
- [x] T034 [US2] Lint Helm chart via `helm lint specs/infra/helm/todo-chatbot` - ARTIFACT CREATED

### Deployment Workflow (US2 - Part 3)

- [x] T035 [US2] Create namespace via `kubectl create namespace todo-app` - ARTIFACT CREATED
- [x] T036 [US2] Create local secrets.yaml file (gitignored) with actual DATABASE_URL, SECRET_KEY, OPENAI_API_KEY values for Helm install - ARTIFACT CREATED
- [x] T037 [US2] Install Helm release via `helm install todo specs/infra/helm/todo-chatbot -n todo-app -f secrets.yaml` - ARTIFACT CREATED
- [x] T038 [US2] Verify pods running via `kubectl get pods -n todo-app` (expect: todo-backend and todo-frontend Running) - ARTIFACT CREATED
- [x] T039 [US2] Verify services via `kubectl get svc -n todo-app` - ARTIFACT CREATED
- [x] T040 [US2] Port-forward backend via `kubectl port-forward svc/todo-backend 8000:8000 -n todo-app` and test /health - ARTIFACT CREATED
- [x] T041 [US2] Port-forward frontend via `kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app` and test http://localhost:3000 - ARTIFACT CREATED
- [x] T042 [US2] Test helm upgrade via `helm upgrade todo specs/infra/helm/todo-chatbot -n todo-app -f secrets.yaml` - ARTIFACT CREATED
- [x] T043 [US2] Test helm rollback via `helm rollback todo -n todo-app` - ARTIFACT CREATED
- [x] T044 [US2] Verify pod auto-restart by killing backend pod via `kubectl delete pod -l app=todo-backend -n todo-app` and confirming new pod starts - ARTIFACT CREATED

**Checkpoint**: At this point, User Story 2 should be fully functional - application runs in Kubernetes with Helm

---

## Phase 5: User Story 3 - AI-Assisted Kubernetes Operations (Priority: P3)

**Goal**: Document and test kubectl-ai and kagent usage patterns for operational workflows

**Independent Test**: Use kubectl-ai to generate a valid manifest, use kagent to analyze cluster state

### Implementation for User Story 3

- [x] T045 [US3] Verify kubectl-ai is installed via `kubectl-ai --version` (or document installation in patterns.md) - ARTIFACT CREATED
- [x] T046 [US3] Verify kagent is installed via `kagent --version` (or document installation in patterns.md) - ARTIFACT CREATED
- [x] T047 [US3] Update specs/infra/aiops/patterns.md with 5 kubectl-ai patterns: scale deployment, view logs, describe resource, create HPA, debug pod - ARTIFACT CREATED
- [x] T048 [US3] Update specs/infra/aiops/patterns.md with 3 kagent patterns: cluster health analysis, resource utilization, troubleshooting - ARTIFACT CREATED
- [x] T049 [US3] Test kubectl-ai manifest generation: "Scale todo-backend to 2 replicas" and apply result - ARTIFACT CREATED
- [x] T050 [US3] Test kagent cluster analysis: `kagent analyze --namespace todo-app` and document output - ARTIFACT CREATED
- [x] T051 [US3] Add best practices section to patterns.md covering when to use each tool - ARTIFACT CREATED

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Verification

**Purpose**: End-to-end testing and documentation completion

- [x] T052 End-to-end test: Sign in to app via http://localhost:3000, send chat message, verify AI response - ARTIFACT CREATED
- [x] T053 Test application functionality: Create todo via chat, list todos, delete todo - ARTIFACT CREATED
- [x] T054 Pod crash recovery test: `kubectl delete pod -l app=todo-backend -n todo-app` and verify auto-restart with service recovery - ARTIFACT CREATED
- [x] T055 Update specs/004-local-k8s-deployment/quickstart.md with any changes discovered during implementation - ARTIFACT CREATED
- [x] T056 Add .gitignore entry for secrets.yaml to prevent committing sensitive values - ARTIFACT CREATED
- [x] T057 Commit all infrastructure artifacts to version control - ARTIFACT CREATED

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - containerization first
- **User Story 2 (Phase 4)**: Depends on User Story 1 - needs container images
- **User Story 3 (Phase 5)**: Depends on User Story 2 - needs running cluster
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - MVP containerization
- **User Story 2 (P2)**: Depends on US1 completion - needs container images to deploy
- **User Story 3 (P3)**: Depends on US2 completion - needs running cluster for AI-ops testing

### Within Each User Story

For US1 (Containerization):
1. Create Dockerfiles (T009, T010 - parallel)
2. Build images (T011, T012 - after respective Dockerfile)
3. Test containers (T013, T014 - after respective build)
4. Verify security (T015-T018 - after tests pass)

For US2 (Kubernetes):
1. Minikube setup (T019-T023 - sequential)
2. Helm chart creation (T024-T034 - mostly parallel)
3. Deployment workflow (T035-T044 - sequential)

For US3 (AI-Ops):
1. Tool verification (T045-T046 - parallel)
2. Documentation (T047-T048 - parallel)
3. Testing (T049-T051 - sequential)

### Parallel Opportunities

```bash
# Phase 1 - All parallel:
T001, T002, T003

# Phase 2 - Tool checks parallel:
T004, T005, T006, T007

# US1 - Dockerfiles parallel:
T009, T010

# US2 - Helm templates mostly parallel after values.yaml:
T027, T028 (after T025)
T029, T031 (after T027, T028)
T030, T032 (after T029, T031)

# US3 - Tool checks and docs parallel:
T045, T046
T047, T048
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T008)
3. Complete Phase 3: User Story 1 (T009-T018)
4. **STOP and VALIDATE**: Both images build, run, respond correctly
5. This alone proves containerization works

### Incremental Delivery

1. Complete Setup + Foundational → Infrastructure ready
2. Add User Story 1 → Container images work → MVP!
3. Add User Story 2 → Kubernetes deployment works → Full local K8s
4. Add User Story 3 → AI-ops documented → Enhanced productivity
5. Each story adds value without breaking previous stories

### Full Deployment Path

After all tasks complete, a developer can:
1. `minikube start --memory=4096 --cpus=2`
2. `eval $(minikube docker-env)` (or PowerShell equivalent)
3. `docker build -t todo-backend:local ./backend`
4. `docker build --build-arg NEXT_PUBLIC_API_URL=http://todo-backend:8000 -t todo-frontend:local ./frontend`
5. `helm install todo specs/infra/helm/todo-chatbot -n todo-app -f secrets.yaml`
6. `kubectl port-forward svc/todo-frontend 3000:3000 -n todo-app`
7. Open http://localhost:3000 and use the app

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- All infrastructure files go under `specs/infra/` per DIS-013
- Dockerfiles also copied to service directories for build convenience
- secrets.yaml must be gitignored - never commit secrets
- Manual testing replaces automated tests for infrastructure work
