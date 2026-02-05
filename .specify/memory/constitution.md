<!--
================================================================================
SYNC IMPACT REPORT
Version Change: 2.1.0 → 2.2.0 (MINOR - Phase V event-driven architecture rules added)

Added Sections:
- Section XI: Phase V Global Rules – Event-Driven Architecture Standards

Modified Principles:
- Section III: Phase V Constraints - Completely rewritten for event-driven architecture scope
- Section III: Phase Governance - Updated Phase V definition from "Production Cloud & Distributed Services" to "Event-Driven Distributed Services"
- Section IV: Technology Constraints - Updated Kafka and Dapr phase assignments from V to V+
- Appendix A: Phase Technology Matrix - Updated Kafka and Dapr phase requirements

Templates Updated:
- ✅ plan-template.md - No changes needed (Constitution Check references generic rules)
- ✅ spec-template.md - No changes needed (phase constraint references generic)
- ✅ tasks-template.md - No changes needed (task structure unchanged)

Deferred Items:
- N/A

Version Bump Rationale:
- MINOR bump: New section (Section XI) added, Phase V scope expanded
- New rules (EVS-*, DAP-*) are additive, not replacing existing rules
- Existing Phase I-IV governance is unchanged

================================================================================
-->

# Evolution of Todo — Global Constitution

> **Supreme Governing Document for All Agents and Development Activities**
>
> This constitution defines the immutable principles, constraints, and governance rules
> for the "Evolution of Todo" project across all phases (I through V). All agents,
> specifications, plans, tasks, and implementations MUST comply with this document.

---

## I. Spec-Driven Development (NON-NEGOTIABLE)

All development in this project follows a strict Spec-Driven Development (SDD) methodology.
No agent may write production code without prior approval through the defined workflow.

### The Mandatory Workflow

```
Constitution → Specification → Plan → Tasks → Implementation
```

1. **Constitution**: This document defines immutable project-wide rules
2. **Specification**: Defines WHAT must be built (features, requirements, acceptance criteria)
3. **Plan**: Defines HOW the specification will be implemented (architecture, structure)
4. **Tasks**: Breaks the plan into discrete, implementable units of work
5. **Implementation**: Code written strictly according to approved tasks

### Enforcement Rules

- **RULE SDD-001**: No agent may generate production code without an approved specification
- **RULE SDD-002**: No agent may generate code that implements features not in the specification
- **RULE SDD-003**: All code changes MUST trace back to a specific task in tasks.md
- **RULE SDD-004**: The specification MUST be approved before plan creation begins
- **RULE SDD-005**: The plan MUST be approved before task decomposition begins
- **RULE SDD-006**: Tasks MUST be approved before implementation begins

---

## II. Agent Behavior Rules (NON-NEGOTIABLE)

Agents operating within this project MUST adhere to strict behavioral constraints
to ensure consistency, traceability, and quality.

### Prohibited Actions

- **RULE ABR-001**: No manual coding by humans outside the agent workflow
- **RULE ABR-002**: No feature invention — agents MUST NOT create features not in specifications
- **RULE ABR-003**: No deviation from approved specifications
- **RULE ABR-004**: No code-level refinement — all refinements MUST occur at the specification level
- **RULE ABR-005**: No assumptions about requirements — ask for clarification when unclear
- **RULE ABR-006**: No future-phase features in current-phase implementation

### Required Actions

- **RULE ABR-007**: Agents MUST document all decisions in appropriate records (PHR, ADR)
- **RULE ABR-008**: Agents MUST validate work against acceptance criteria before completion
- **RULE ABR-009**: Agents MUST flag specification gaps rather than filling them with assumptions
- **RULE ABR-010**: Agents MUST maintain clear separation between phases

### Refinement Protocol

When changes are needed to delivered code:

1. Identify the specification gap or error
2. Update the specification document
3. Re-generate or update the plan if architectural changes are needed
4. Update tasks to reflect the specification change
5. Implement the change according to updated tasks

**Refinement MUST NOT occur directly at the code level.**

---

## III. Phase Governance

The "Evolution of Todo" project progresses through five distinct phases.
Each phase has strict scope boundaries that MUST NOT be violated.

### Phase Definitions

| Phase | Name | Scope Summary |
|-------|------|---------------|
| I | In-Memory Console | Python CLI, in-memory storage, single user, basic CRUD |
| II | Full-Stack Web | Python REST API, Neon PostgreSQL, Next.js frontend, authentication |
| III | MCP Agentic Chatbot | Natural-language task management via MCP tools, Claude/OpenAI agents, stateless API |
| IV | Cloud-Native Local Deployment | Docker containerization, Kubernetes (Minikube), Helm Charts, AI-assisted ops |
| V | Event-Driven Distributed Services | Kafka event streaming, Dapr sidecar, distributed architecture, cloud infrastructure |

### Phase Boundary Rules

- **RULE PG-001**: Each phase specification MUST NOT reference future phase features
- **RULE PG-002**: Implementation MUST NOT include code for features in later phases
- **RULE PG-003**: Architecture decisions MUST be appropriate for the current phase only
- **RULE PG-004**: Phase transitions require explicit specification updates
- **RULE PG-005**: Backward compatibility within a phase is mandatory; cross-phase is not guaranteed

### Phase I Constraints (In-Memory Console)

The following are **explicitly allowed** in Phase I:
- Python 3.11+ as primary language
- In-memory data structures (lists, dictionaries)
- Console-based CLI interface
- Single-user operation
- Basic CRUD operations

The following are **explicitly prohibited** in Phase I:
- Database connections or ORM usage
- File system persistence
- Network operations or HTTP
- Authentication or authorization
- Multi-user support
- Web frameworks
- External service integrations
- Async operations (unless for CLI responsiveness)

### Phase II Constraints (Full-Stack Web Application)

The following are **explicitly allowed** in Phase II:
- Python REST API using FastAPI or similar
- Neon Serverless PostgreSQL database
- SQLModel or equivalent ORM/data layer
- Next.js frontend (React, TypeScript)
- Better Auth for signup/signin
- Web-based user interface
- Authentication and authorization
- Multi-user support
- HTTP/HTTPS network operations
- RESTful API design
- Session management

The following are **explicitly prohibited** in Phase II:
- Container orchestration (Docker/Kubernetes)
- Message queues or event streaming
- AI or agent frameworks
- Microservices architecture
- Advanced cloud infrastructure

### Phase III Constraints (MCP Agentic Chatbot)

The following are **explicitly allowed** in Phase III (adds to Phase II):
- MCP (Model Context Protocol) server implementation
- Claude API / Anthropic SDK integration
- OpenAI Agents SDK integration
- Natural-language chatbot interface for task management
- Conversation and message persistence in database
- MCP tool definitions and registration
- Agent orchestration logic (single-agent or multi-agent)
- Streaming responses (SSE) from agent to frontend
- Markdown rendering in chat UI

The following are **explicitly prohibited** in Phase III:
- Server-side session objects, Redis, or in-memory caches for chat state
- Conversation state stored anywhere other than the database
- MCP tools that do NOT accept `user_id` as first parameter
- MCP tools that skip user authentication/authorization checks
- Container orchestration (Docker/Kubernetes)
- Message queues or event streaming (Kafka, RabbitMQ)
- Microservices architecture — single deployable backend required
- Bypassing the natural-language interface for primary task operations

### Phase IV Constraints (Cloud-Native Local Deployment)

The following are **explicitly allowed** in Phase IV (adds to Phase III):
- Docker containerization with separate Dockerfiles for frontend and backend
- Kubernetes orchestration via Minikube for local development
- Helm Charts for service packaging and deployment
- AI-assisted infrastructure tooling (Gordon, kubectl-ai, kagent)
- Kubernetes Secrets for sensitive configuration values
- Spec-driven infrastructure generation from `specs/infra/`
- Container image registries (local or remote)
- Kubernetes health checks, liveness/readiness probes
- Ingress controllers for local service routing

The following are **explicitly prohibited** in Phase IV:
- Message queues or event streaming (Kafka, RabbitMQ)
- Microservices architecture — single backend, single frontend containers required
- Multi-cluster Kubernetes deployments
- Production cloud provider infrastructure (AWS EKS, GCP GKE, Azure AKS)
- Dapr sidecar integration
- Service mesh patterns (Istio, Linkerd)

### Phase V Constraints (Event-Driven Distributed Services)

The following are **explicitly allowed** in Phase V (adds to Phase IV):
- Kafka event streaming with Dapr abstraction layer
- Dapr sidecar integration for pub/sub, state management, secrets, service invocation
- Event-driven architecture with asynchronous processing
- Microservices decomposition with loose coupling
- Multi-cluster Kubernetes deployments (production cloud providers)
- Advanced cloud infrastructure (managed K8s, cloud-native services)
- Production observability stack (Prometheus, Grafana, Jaeger)
- Cron jobs and scheduled tasks via Dapr bindings
- Service mesh patterns for inter-service communication

The following are **explicitly prohibited** in Phase V:
- Direct Kafka client usage — always use Dapr Pub/Sub abstraction
- Synchronous processing for new event-based features
- Monolithic architecture for new functionality (must be microservices)

---

## IV. Technology Constraints

The following technology stack is mandated for this project.
Deviations require constitutional amendment.

### Backend Technologies

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| Python 3.11+ | I | Primary language |
| In-memory data structures | I | Phase I storage |
| FastAPI | II | Web framework for REST API |
| SQLModel | II | ORM and data modeling |
| Neon DB (PostgreSQL) | II | Cloud database |
| Pydantic | II | Data validation |

### Frontend Technologies

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| Next.js 14+ | II | React framework |
| TypeScript | II | Type-safe frontend |
| React | II | UI library |

### Authentication Technologies

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| Better Auth | II | Authentication service |

### Infrastructure Technologies

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| Docker | IV | Containerization |
| Kubernetes (Minikube) | IV | Local container orchestration |
| Helm | IV | Kubernetes package management |
| Kafka | V+ | Event streaming |
| Dapr | V+ | Distributed runtime |

### Infrastructure Tooling (AI-Assisted)

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| Gordon (Docker AI Agent) | IV | Dockerfile creation and optimization |
| kubectl-ai | IV | AI-assisted K8s manifest and command generation |
| kagent | IV | AI-assisted K8s analysis and troubleshooting |

### AI/Agent Technologies

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| MCP (Model Context Protocol) | III | Tool contract for agentic task management |
| Claude API / Anthropic SDK | III | LLM provider for chatbot agent |
| OpenAI Agents SDK | III | Agent orchestration framework |
| Dapr AI Agents | V+ | Distributed agent runtime |

### Technology Rules

- **RULE TC-001**: Only technologies listed for the current or earlier phases may be used
- **RULE TC-002**: Version constraints MUST be respected (minimum versions specified)
- **RULE TC-003**: Additional libraries MUST be justified and documented in the plan
- **RULE TC-004**: No proprietary or licensed tools without explicit approval

---

## V. Quality Principles

All code and architecture MUST adhere to these quality principles.

### Clean Architecture

- **RULE QP-001**: Clear separation of concerns between layers
- **RULE QP-002**: Dependencies flow inward (UI → Application → Domain → Infrastructure)
- **RULE QP-003**: Domain logic MUST NOT depend on infrastructure details
- **RULE QP-004**: Each module MUST have a single, well-defined responsibility

### Stateless Services

- **RULE QP-005**: FastAPI server MUST be completely stateless regarding conversations (Phase III+). No session objects, no Redis, no in-memory caches for chat state
- **RULE QP-006**: All conversation state MUST be persisted in database tables (`conversations`, `messages`). No other storage mechanism is permitted for chat state
- **RULE QP-007**: Session state MUST be managed through tokens, not server memory. Authentication state flows via Bearer tokens only

### Code Quality Standards

- **RULE QP-008**: All public functions MUST have type hints (Python) or type annotations (TypeScript)
- **RULE QP-009**: Error handling MUST be explicit — no silent failures
- **RULE QP-010**: Logging MUST be structured and include correlation IDs (Phase II+)
- **RULE QP-011**: Configuration MUST be externalized via environment variables

### Testing Requirements

- **RULE QP-012**: Unit tests are required for all business logic
- **RULE QP-013**: Integration tests are required for all external interfaces
- **RULE QP-014**: Contract tests are required for all API endpoints (Phase II+)
- **RULE QP-015**: Tests MUST be written before implementation (TDD) when specified

### Cloud-Native Readiness (Phase IV+)

- **RULE QP-016**: Services MUST be containerizable
- **RULE QP-017**: Services MUST support horizontal scaling
- **RULE QP-018**: Services MUST implement health checks
- **RULE QP-019**: Services MUST handle graceful shutdown
- **RULE QP-020**: Services MUST support configuration injection

---

## VI. Development Workflow

### Specification Workflow (`/sp.specify`)

1. Receive feature request or phase requirements
2. Validate request against constitution and phase constraints
3. Generate specification with:
   - User stories (prioritized)
   - Acceptance criteria (Given/When/Then)
   - Functional requirements
   - Edge cases
   - Key entities
4. Obtain approval before proceeding

### Planning Workflow (`/sp.plan`)

1. Load approved specification
2. Validate against constitution (Constitution Check)
3. Generate technical plan with:
   - Technical context
   - Project structure
   - Architecture decisions
   - Component relationships
4. Obtain approval before proceeding

### Task Generation Workflow (`/sp.tasks`)

1. Load approved plan and specification
2. Generate task list organized by:
   - Setup phase
   - Foundational phase
   - User story phases (per priority)
   - Polish phase
3. Include dependencies and parallel opportunities
4. Obtain approval before implementation

### Implementation Workflow (`/sp.implement`)

1. Load approved tasks
2. Execute tasks in dependency order
3. Validate each task against acceptance criteria
4. Create appropriate test coverage
5. Document completion in task list

---

## VII. Quality Gates

### Pre-Specification Gate

- [ ] Request aligns with current phase scope
- [ ] No future-phase features requested
- [ ] Requirements are clear and unambiguous

### Pre-Plan Gate

- [ ] Specification is approved
- [ ] All user stories have acceptance criteria
- [ ] Edge cases are documented
- [ ] Key entities are defined

### Pre-Task Gate

- [ ] Plan is approved
- [ ] Constitution Check passes
- [ ] Technical context is complete
- [ ] Project structure is defined

### Pre-Implementation Gate

- [ ] Tasks are approved
- [ ] Dependencies are clear
- [ ] Parallel opportunities identified
- [ ] Each task has clear deliverables

### Post-Implementation Gate

- [ ] All tasks completed
- [ ] All acceptance criteria pass
- [ ] Tests are passing
- [ ] Code review completed
- [ ] Documentation updated

---

## VIII. Governance

### Constitutional Supremacy

This constitution is the supreme governing document for the "Evolution of Todo" project.
In case of conflict between this constitution and any other document:

1. This constitution takes precedence
2. The conflicting document MUST be updated to comply
3. If the constitution is wrong, an amendment MUST be proposed

### Amendment Process

Constitutional amendments require:

1. **Proposal**: Written proposal with rationale
2. **Review**: Impact analysis on existing specifications and plans
3. **Approval**: Explicit approval from project authority
4. **Documentation**: Updated constitution with version increment
5. **Propagation**: All dependent documents updated for compliance

### Version Numbering

Constitution versions follow semantic versioning:

- **MAJOR**: Backward-incompatible governance changes or principle removals
- **MINOR**: New principles or sections added
- **PATCH**: Clarifications, wording fixes, non-semantic refinements

### Compliance Verification

- All specifications MUST include a constitution compliance checklist
- All plans MUST include a Constitution Check section
- All implementations MUST trace to approved tasks
- All agents MUST validate their work against this constitution

### Enforcement

Violations of this constitution result in:

1. **Immediate halt** of the violating work
2. **Root cause analysis** of how the violation occurred
3. **Correction** through proper specification updates
4. **Prevention** through process improvement

---

## IX. Phase III Global Rules – MCP & Agentic Chatbot Architecture

These rules are **NON-NEGOTIABLE** for all Phase III work and supersede any conflicting
guidance in earlier sections when operating within Phase III scope.

### 1. Interface Philosophy

- **RULE MCP-001**: Natural language is the **ONLY** user interface for task management in Phase III. Users interact with a chatbot; the chatbot invokes MCP tools to perform CRUD and other operations.
- **RULE MCP-002**: The classic REST API remains available for possible future or programmatic use, but is **NOT** the primary interaction path. No new REST endpoints are required unless an MCP tool needs one internally.
- **RULE MCP-003**: The frontend MUST present a conversational chat interface as the primary view. Any traditional todo-list UI is secondary and optional.

### 2. Statelessness Requirement (strict)

- **RULE MCP-010**: The FastAPI server MUST be completely stateless regarding conversations. No session objects, no Redis, no in-memory caches for chat state.
- **RULE MCP-011**: All conversation state MUST live in the database in `conversations` and `messages` tables. A conversation is reconstructed from the database on every request.
- **RULE MCP-012**: Each API request MUST be self-contained: it carries a `conversation_id` (or starts a new one) and a user message. The server loads history from the database, calls the agent, persists the response, and returns it.
- **RULE MCP-013**: Server restart MUST NOT lose any conversation state. All state is in the database; restarts are invisible to users.

### 3. MCP Tools Contract (non-negotiable)

- **RULE MCP-020**: Every MCP tool MUST accept `user_id` as its first required parameter (type: `string`).
- **RULE MCP-021**: Every MCP tool MUST validate that the authenticated user matches the provided `user_id` before performing any operation. Mismatches MUST return an authorization error.
- **RULE MCP-022**: Every MCP tool MUST return a simple, structured response (dictionary/object). No raw strings, no HTML, no unstructured output.
- **RULE MCP-023**: MCP tool names MUST follow the pattern `<resource>_<action>` (e.g., `todo_create`, `todo_list`, `todo_update`, `todo_delete`, `conversation_list`).
- **RULE MCP-024**: MCP tool descriptions MUST be clear enough for the LLM agent to select the correct tool without ambiguity. Descriptions are part of the contract.
- **RULE MCP-025**: MCP tools MUST NOT hold or cache state between invocations. Each invocation is independent and hits the database directly.

### 4. Agent Behavior (Phase III specific)

- **RULE MCP-030**: The agent (Claude or OpenAI) is the intermediary between the user's natural language and the MCP tools. The agent MUST NOT fabricate data — it calls tools for all data access.
- **RULE MCP-031**: The agent MUST NOT bypass MCP tools to execute raw SQL or direct database calls. All data operations go through registered tools.
- **RULE MCP-032**: The agent MUST gracefully handle tool errors and report them to the user in natural language. No stack traces or raw error objects in user-facing responses.
- **RULE MCP-033**: The agent MUST maintain conversation context by loading prior messages from the database, not from any in-memory store.
- **RULE MCP-034**: The agent MUST respect user authorization boundaries — it can only access todos and conversations belonging to the authenticated user.

### 5. Database Schema Rules (Phase III additions)

- **RULE MCP-040**: A `conversations` table MUST exist with at minimum: `id`, `user_id`, `title`, `created_at`, `updated_at`.
- **RULE MCP-041**: A `messages` table MUST exist with at minimum: `id`, `conversation_id`, `role` (user/assistant/tool), `content`, `created_at`.
- **RULE MCP-042**: Foreign key constraints MUST enforce referential integrity: `messages.conversation_id → conversations.id`, `conversations.user_id → users.id`.
- **RULE MCP-043**: Messages MUST be ordered by `created_at` to reconstruct conversation history deterministically.
- **RULE MCP-044**: Existing `todos` table from Phase II MUST NOT be modified for MCP compatibility. MCP tools read/write todos through the existing data layer.

### 6. API Endpoint Rules (Phase III additions)

- **RULE MCP-050**: A single chat endpoint (e.g., `POST /api/chat`) MUST accept a user message and return the agent's response. This is the primary API for the frontend.
- **RULE MCP-051**: The chat endpoint MUST support streaming responses (SSE) to provide real-time agent output to the frontend.
- **RULE MCP-052**: The chat endpoint MUST authenticate the user via Bearer token (same auth system as Phase II).
- **RULE MCP-053**: Conversation management endpoints (list, get, delete) MAY be implemented as REST or as MCP tools invocable through the chat interface.

### 7. Frontend Rules (Phase III additions)

- **RULE MCP-060**: The Next.js frontend MUST implement a chat interface component as the primary interaction surface.
- **RULE MCP-061**: The chat UI MUST render Markdown in assistant responses (lists, bold, code blocks, etc.).
- **RULE MCP-062**: The chat UI MUST display a loading/typing indicator while waiting for agent responses.
- **RULE MCP-063**: The chat UI MUST support conversation history — users can switch between past conversations.
- **RULE MCP-064**: The existing Phase II todo UI components MAY be preserved but are NOT the primary interface.

---

## X. Phase IV Global Rules – Deployment & Infrastructure Standards

These rules are **NON-NEGOTIABLE** for all Phase IV work and supersede any conflicting
guidance in earlier sections when operating within Phase IV scope.

### 1. Containerization Requirements

- **RULE DIS-001**: All services MUST run in Kubernetes (Minikube for local development). No bare-metal or direct `docker run` deployments for production-like environments.
- **RULE DIS-002**: Separate Dockerfiles MUST exist for frontend (Next.js) and backend (FastAPI). A single monolithic container is prohibited.
- **RULE DIS-003**: Docker AI Agent (Gordon) SHOULD be the preferred tool for Dockerfile creation, optimization, and security hardening. Manual Dockerfile authoring is permitted but Gordon-first is the default.
- **RULE DIS-004**: Docker images MUST use multi-stage builds to minimize image size. Final images MUST NOT contain build tools, source code, or development dependencies.
- **RULE DIS-005**: Docker images MUST NOT embed secrets, API keys, or credentials. All sensitive values MUST be injected at runtime via Kubernetes Secrets.

### 2. Kubernetes & Orchestration

- **RULE DIS-010**: Minikube MUST be the target Kubernetes environment for local development and testing. All manifests MUST work on a single-node Minikube cluster.
- **RULE DIS-011**: Helm Charts are REQUIRED for packaging and deploying services. Raw `kubectl apply -f` of individual manifests is prohibited for production-like deployments. Helm charts MAY be structured as one unified chart or separate charts per service.
- **RULE DIS-012**: AI-assisted tooling MUST be used where applicable: `kubectl-ai` for manifest generation and kubectl commands, `kagent` for cluster analysis and troubleshooting. Manual manifest authoring is permitted as fallback.
- **RULE DIS-013**: All Kubernetes manifests, Helm charts, and infrastructure configuration MUST be generated from and stored under `specs/infra/`. Spec-driven infrastructure is mandatory.
- **RULE DIS-014**: Every Kubernetes Deployment MUST define liveness and readiness probes. Services without health checks MUST NOT be deployed.

### 3. Security & Configuration

- **RULE DIS-020**: Sensitive values (database URLs, JWT secrets, OpenAI API keys) MUST be stored in Kubernetes Secrets. ConfigMaps are for non-sensitive configuration only.
- **RULE DIS-021**: Helm `values.yaml` MUST expose all configurable parameters (replicas, image tags, resource limits, environment-specific settings). Hardcoded values in templates are prohibited.
- **RULE DIS-022**: Existing statelessness rules (MCP-010 through MCP-013) and JWT authentication rules (QP-007) MUST be enforced identically in the containerized environment. Containerization does not relax any Phase III constraints.
- **RULE DIS-023**: Container images MUST run as non-root users. Privileged containers are prohibited.
- **RULE DIS-024**: Kubernetes NetworkPolicies SHOULD restrict inter-pod communication to only necessary paths (frontend → backend, backend → database).

### 4. Infrastructure as Code

- **RULE DIS-030**: All infrastructure configuration MUST be version-controlled under `specs/infra/` in the project repository. No manual cluster modifications outside of tracked configuration.
- **RULE DIS-031**: Infrastructure changes MUST follow the same SDD workflow as application code: Specification → Plan → Tasks → Implementation. Ad-hoc `kubectl` commands that modify cluster state are prohibited outside of debugging.
- **RULE DIS-032**: Helm chart versions MUST be incremented for every deployment-affecting change, following semantic versioning.

### 5. Deployment Workflow

- **RULE DIS-040**: The deployment pipeline MUST support: `docker build` → `docker push` (to local or remote registry) → `helm upgrade --install`. No manual container management.
- **RULE DIS-041**: Rollback MUST be possible via `helm rollback` at any time. Deployments that break rollback capability are prohibited.
- **RULE DIS-042**: Environment parity MUST be maintained: the same Docker images and Helm charts used in local Minikube MUST be deployable to production Kubernetes clusters (Phase V) with only `values.yaml` overrides.

---

## XI. Phase V Global Rules – Event-Driven Architecture Standards

These rules are **NON-NEGOTIABLE** for all Phase V work and supersede any conflicting
guidance in earlier sections when operating within Phase V scope.

### 1. Event-Driven Architecture Requirements

- **RULE EVS-001**: From Phase V onward: application MUST be event-driven using Kafka (or compatible Pub/Sub) + Dapr for decoupling. All new service-to-service communication must be asynchronous via events.
- **RULE EVS-002**: All new features (recurring tasks, due dates/reminders, priorities, tags, search/filter/sort) MUST use events for async processing. Synchronous API calls for new features are prohibited.
- **RULE EVS-003**: Events MUST be idempotent and support replay. Event handlers MUST be designed to handle duplicate events safely.
- **RULE EVS-004**: Event schemas MUST be versioned and backward-compatible. Breaking changes to event schemas require coordinated deployments.
- **RULE EVS-005**: Event sourcing pattern SHOULD be used where appropriate for maintaining system state from event streams.

### 2. Dapr Sidecar Integration

- **RULE DAP-001**: Dapr sidecar MUST be used for Pub/Sub abstraction. No direct Kafka client code — always use Dapr Pub/Sub APIs.
- **RULE DAP-002**: Dapr sidecar MUST be used for state management. All persistent state operations go through Dapr state store APIs.
- **RULE DAP-003**: Dapr sidecar MUST be used for secrets management. All secret access goes through Dapr secret store APIs.
- **RULE DAP-004**: Dapr sidecar MUST be used for service invocation. All service-to-service calls go through Dapr service invocation APIs.
- **RULE DAP-005**: Dapr sidecar MUST be used for cron jobs or scheduled tasks via Dapr bindings for reminders and other time-based triggers.

### 3. Deployment & Infrastructure Requirements

- **RULE EVS-006**: Deployments MUST support local Minikube with Dapr + self-hosted Kafka/Redpanda for development and testing.
- **RULE EVS-007**: Deployments MUST support cloud environments: AKS / GKE / OKE with managed or self-hosted Kafka for production.
- **RULE EVS-008**: All services MUST run with Dapr sidecar in production-grade K8s environments. Services without Dapr sidecars are prohibited in Phase V.
- **RULE EVS-009**: Infrastructure remains fully spec-driven with configurations under `specs/infra/dapr.md`, `specs/infra/kafka.md`, and `specs/infra/cloud.md`.
- **RULE EVS-010**: CI/CD via GitHub Actions is required for build → push → deploy pipelines.

### 4. Service Architecture

- **RULE EVS-011**: Maintain stateless pods; Neon DB + Dapr state store act as single source of truth for all application state.
- **RULE EVS-012**: Microservices architecture is required for new functionality. Services MUST be decomposed around business capabilities.
- **RULE EVS-013**: Services MUST have bounded contexts with clear ownership boundaries. Cross-service queries are discouraged in favor of eventual consistency via events.
- **RULE EVS-014**: Circuit breaker patterns MUST be implemented for resilience between services via Dapr's built-in circuit breaking.
- **RULE EVS-015**: Saga pattern SHOULD be implemented for distributed transactions across services.

### 5. Observability & Monitoring

- **RULE EVS-016**: Distributed tracing MUST be enabled across all services using Dapr's tracing capabilities.
- **RULE EVS-017**: Centralized logging MUST be implemented with structured logs containing correlation IDs for event traceability.
- **RULE EVS-018**: Metrics collection MUST be standardized using Prometheus format and exported via Dapr's metrics.
- **RULE EVS-019**: Health checks MUST include readiness for event processing and connection to message brokers.
- **RULE EVS-020**: Monitoring and alerting basics MUST be documented and implemented for production environments.

---

## Appendix A: Quick Reference

### The Workflow

```
Constitution → Specification → Plan → Tasks → Implementation
     ↑              ↓            ↓       ↓           ↓
     └──────────────────── Refinement Loop ─────────┘
```

### Key Commands

| Command | Purpose | Input | Output |
|---------|---------|-------|--------|
| `/sp.constitution` | View/amend constitution | Amendment request | Updated constitution |
| `/sp.specify` | Create specification | Feature request | spec.md |
| `/sp.plan` | Create technical plan | Approved spec | plan.md |
| `/sp.tasks` | Generate task list | Approved plan | tasks.md |
| `/sp.implement` | Execute tasks | Approved tasks | Code |

### Phase Technology Matrix

| Technology | I | II | III | IV | V |
|------------|---|----|----|----|---|
| Python | ✓ | ✓ | ✓ | ✓ | ✓ |
| In-memory | ✓ | | | | |
| FastAPI | | ✓ | ✓ | ✓ | ✓ |
| SQLModel | | ✓ | ✓ | ✓ | ✓ |
| Neon DB | | ✓ | ✓ | ✓ | ✓ |
| Next.js | | ✓ | ✓ | ✓ | ✓ |
| TypeScript | | ✓ | ✓ | ✓ | ✓ |
| Better Auth | | ✓ | ✓ | ✓ | ✓ |
| MCP SDK | | | ✓ | ✓ | ✓ |
| Claude API | | | ✓ | ✓ | ✓ |
| OpenAI Agents SDK | | | ✓ | ✓ | ✓ |
| Docker | | | | ✓ | ✓ |
| Kubernetes | | | | ✓ | ✓ |
| Helm | | | | ✓ | ✓ |
| Gordon | | | | ✓ | ✓ |
| kubectl-ai | | | | ✓ | ✓ |
| kagent | | | | ✓ | ✓ |
| Kafka | | | | | ✓ |
| Dapr | | | | | ✓ |

---

**Version**: 2.2.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-02-05