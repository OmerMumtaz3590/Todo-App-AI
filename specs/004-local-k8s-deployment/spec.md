# Feature Specification: Local Kubernetes Deployment

**Feature Branch**: `004-local-k8s-deployment`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Implement Phase IV: Local Kubernetes Deployment of Todo Chatbot"

## Constitution Compliance

**Target Phase**: Phase IV

**Pre-Specification Gate** (per Constitution Section VII):
- [x] Request aligns with current phase scope
- [x] No future-phase features requested
- [x] Requirements are clear and unambiguous

**Phase Constraints Verified** (per Constitution Section III):
- [x] Only phase-appropriate features specified
- [x] No references to future-phase technologies
- [x] Scope boundaries respected

**Phase IV Compliance Notes**:
- Docker containerization: Allowed (DIS-001, DIS-002)
- Kubernetes via Minikube: Allowed (DIS-010)
- Helm Charts: Allowed (DIS-011)
- AI-assisted tooling (Gordon, kubectl-ai, kagent): Allowed (DIS-003, DIS-012)
- No Kafka, Dapr, service mesh, or multi-cluster: Correctly excluded (Phase V)
- Single backend + single frontend containers: Compliant (no microservices)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Containerize Application Services (Priority: P1)

As a developer, I want to build container images for both the frontend and backend services so that the application can run consistently in any container-compatible environment.

The frontend (Next.js chat interface) and backend (FastAPI with OpenAI Agents SDK) each need their own container image. Images should be production-optimized with multi-stage builds that exclude development dependencies and source artifacts. The Docker AI Agent (Gordon) should be the preferred tool for generating and optimizing Dockerfiles.

**Why this priority**: Containerization is the foundation for all subsequent deployment work. Without container images, there is nothing to deploy to Kubernetes.

**Independent Test**: Build both images locally with `docker build`, then run each with `docker run` and verify the application is accessible. The frontend should serve pages and the backend should respond to health check requests.

**Acceptance Scenarios**:

1. **Given** the project source code, **When** a developer runs the Docker build command for the backend, **Then** a container image is produced that starts the FastAPI server and responds to requests on the configured port
2. **Given** the project source code, **When** a developer runs the Docker build command for the frontend, **Then** a container image is produced that serves the Next.js application and responds to requests on the configured port
3. **Given** a built backend image, **When** the container starts, **Then** it does NOT contain development dependencies, build tools, or source code beyond what is needed at runtime
4. **Given** a built frontend image, **When** the container starts, **Then** it does NOT contain `node_modules` devDependencies, `.next/cache`, or build-time-only files
5. **Given** either container image, **When** inspecting the running process, **Then** it runs as a non-root user
6. **Given** either container image, **When** inspecting environment variables, **Then** no secrets, API keys, or credentials are baked into the image

---

### User Story 2 - Deploy to Local Kubernetes via Helm (Priority: P2)

As a developer, I want to deploy the containerized application to a local Minikube cluster using Helm so that I can validate the full deployment pipeline locally before moving to production infrastructure.

This includes starting and configuring Minikube, creating Helm charts that define all Kubernetes resources (deployments, services, secrets, ingress), and running `helm install` to bring the application up. Sensitive configuration values (database URL, JWT secret, OpenAI API key) must be managed through Kubernetes Secrets, while non-sensitive parameters are exposed through Helm `values.yaml`.

**Why this priority**: Kubernetes deployment is the core deliverable of Phase IV. It validates that the containerized application works in an orchestrated environment with proper networking, secret management, and health monitoring.

**Independent Test**: Run `minikube start`, `helm install`, and verify both services are running. Access the application through the Minikube-exposed URL, sign in, and send a chat message to the AI assistant. Verify the response comes back successfully.

**Acceptance Scenarios**:

1. **Given** a fresh Minikube cluster, **When** a developer runs the Helm install command, **Then** both frontend and backend pods start and reach a "Ready" state
2. **Given** a running deployment, **When** a user accesses the application URL, **Then** the frontend loads and can communicate with the backend
3. **Given** Helm values with database URL, JWT secret, and OpenAI API key, **When** the deployment starts, **Then** these values are injected as Kubernetes Secrets and available to the backend container as environment variables
4. **Given** a running deployment, **When** the backend pod is killed, **Then** Kubernetes automatically restarts it and the application recovers without manual intervention
5. **Given** a running deployment, **When** a developer runs `helm upgrade` with updated values, **Then** the deployment rolls out changes without downtime
6. **Given** a running deployment, **When** a developer runs `helm rollback`, **Then** the previous version is restored successfully
7. **Given** a Helm chart, **When** inspecting `values.yaml`, **Then** all configurable parameters (replicas, image tags, resource limits, environment-specific settings) are exposed and documented
8. **Given** a running deployment, **When** Kubernetes checks pod health, **Then** both liveness and readiness probes pass for all pods

---

### User Story 3 - AI-Assisted Kubernetes Operations (Priority: P3)

As a developer, I want to use AI-powered tools (kubectl-ai and kagent) to generate Kubernetes manifests, debug deployment issues, and perform common cluster operations using natural language commands.

This includes documented patterns for using `kubectl-ai` to generate or modify manifests, run kubectl commands from natural language descriptions, and using `kagent` to analyze cluster state, diagnose problems, and suggest fixes. These patterns serve as a reference guide for ongoing operations.

**Why this priority**: AI-assisted tooling improves developer productivity but is not required for the core deployment to function. The application works without it; these tools make operations more efficient.

**Independent Test**: Use kubectl-ai to generate a valid Kubernetes manifest from a natural language description. Use kagent to analyze the running cluster and produce a health report. Both should produce actionable, correct output.

**Acceptance Scenarios**:

1. **Given** a natural language description of a desired Kubernetes resource, **When** a developer uses kubectl-ai, **Then** a valid manifest is generated that can be applied to the cluster
2. **Given** a running deployment with a known issue, **When** a developer uses kagent to analyze the cluster, **Then** the tool identifies the problem and suggests a remediation
3. **Given** the project repository, **When** a developer looks for AI-ops documentation, **Then** a reference guide exists with common kubectl-ai and kagent usage patterns for this project
4. **Given** a need to scale the deployment, **When** a developer describes the scaling intent in natural language to kubectl-ai, **Then** the correct `kubectl scale` or HPA manifest is generated

---

### Edge Cases

- What happens when Minikube runs out of allocated memory or CPU? The Helm chart should define resource requests and limits so pods fail predictably rather than causing node instability.
- What happens when the Neon database is unreachable from inside the cluster? The backend health check should report unhealthy, and the pod should be restarted by Kubernetes.
- What happens when a developer upgrades the Helm chart with invalid values? The `helm upgrade` command should fail with a clear validation error, and the running deployment should remain unaffected.
- What happens when Docker build fails due to missing dependencies? The Dockerfile should fail at the build stage with a clear error message indicating which dependency is missing.
- What happens when Minikube is not running and a developer tries to deploy? The Helm command should fail with a clear error indicating the cluster is unreachable.
- What happens when the frontend cannot reach the backend inside the cluster? The service discovery configuration should ensure the frontend uses the backend's Kubernetes Service DNS name, not a hardcoded IP.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a Dockerfile for the backend service that produces a production-ready container image
- **FR-002**: System MUST provide a Dockerfile for the frontend service that produces a production-ready container image
- **FR-003**: Both Dockerfiles MUST use multi-stage builds to exclude build tools and development dependencies from final images
- **FR-004**: Both container images MUST run processes as a non-root user
- **FR-005**: Container images MUST NOT embed any secrets, API keys, or credentials
- **FR-006**: System MUST provide Helm chart(s) that package all Kubernetes resources needed to deploy the full application
- **FR-007**: Helm charts MUST define Kubernetes Deployments with liveness and readiness probes for all services
- **FR-008**: Helm charts MUST manage sensitive values (database URL, JWT secret, OpenAI API key) through Kubernetes Secrets
- **FR-009**: Helm `values.yaml` MUST expose all configurable parameters including replica counts, image tags, resource limits, and environment-specific settings
- **FR-010**: System MUST provide commands or scripts to start and configure a Minikube cluster suitable for running the application
- **FR-011**: System MUST support `helm install`, `helm upgrade`, and `helm rollback` workflows
- **FR-012**: System MUST provide documentation of kubectl-ai and kagent usage patterns for common operations (manifest generation, debugging, scaling, health analysis)
- **FR-013**: Frontend containers MUST be configured to discover the backend via Kubernetes Service DNS names, not hardcoded addresses
- **FR-014**: All Kubernetes manifests and Helm charts MUST be stored under `specs/infra/` in the project repository
- **FR-015**: All infrastructure configuration MUST be version-controlled and follow the project's spec-driven development workflow

### Key Entities

- **Container Image**: A built Docker image for either the frontend or backend service. Identified by name and tag. Stored in a container registry (local Minikube registry or external).
- **Helm Chart**: A package of Kubernetes resource templates and default values. Identified by chart name and version. Contains deployments, services, secrets, and optional ingress definitions.
- **Kubernetes Secret**: A resource that stores sensitive configuration values (database credentials, API keys, JWT secrets). Referenced by pods at runtime, never baked into images.
- **Kubernetes Deployment**: A resource that manages pod replicas for a service. Includes health probes, resource limits, and environment variable injection from secrets and config maps.

## Assumptions

- Minikube is already installed on the developer's machine (installation is out of scope; configuration and startup are in scope)
- Docker Desktop or equivalent Docker daemon is available for building images
- The developer has an active Neon database with a valid connection string
- kubectl-ai and kagent CLI tools are installed or installable via standard package managers
- Gordon (Docker AI Agent) is available through Docker Desktop
- The existing Phase III application (frontend + backend) is functional and passes basic smoke tests before containerization begins

## Out of Scope

- Production cloud deployment (AWS EKS, GCP GKE, Azure AKS) — Phase V
- Kafka event streaming — Phase V
- Dapr sidecar integration — Phase V
- Microservices decomposition — Phase V
- Service mesh (Istio, Linkerd) — Phase V
- CI/CD pipeline automation — not specified in Phase IV
- Monitoring and observability stack (Prometheus, Grafana) — Phase V
- Database migration or schema changes — no new data model work
- Application feature changes — Phase IV is deployment-only

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can build both container images from source in a single sequence of commands and have them ready for deployment
- **SC-002**: A developer can go from a fresh Minikube cluster to a fully running application (both services healthy, accessible via browser) by executing the documented deployment commands
- **SC-003**: The deployed application maintains full functionality — users can sign in, chat with the AI assistant, manage todos, and view conversation history identically to the non-containerized version
- **SC-004**: A deployment rollback via `helm rollback` restores the previous working version within 60 seconds
- **SC-005**: When a pod crashes, Kubernetes restarts it and the service recovers automatically without developer intervention
- **SC-006**: All sensitive configuration values are stored in Kubernetes Secrets and never appear in plain text in version-controlled files, container images, or pod environment variable listings
- **SC-007**: The AI-ops reference guide includes at least 5 documented kubectl-ai patterns and 3 documented kagent patterns covering common operational scenarios
