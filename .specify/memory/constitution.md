<!--
================================================================================
SYNC IMPACT REPORT
================================================================================
Version Change: 1.0.0 → 1.1.0 (MINOR - Phase II technology matrix updated with full-stack requirements)

Added Sections:
- N/A

Modified Principles:
- Section III: Phase Governance - Phase II definition expanded to full-stack web application
- Section IV: Technology Constraints - Phase II technologies updated to include REST API, Neon PostgreSQL, SQLModel, Next.js, Better Auth
- Appendix A: Phase Technology Matrix - Updated to reflect Phase II full-stack capabilities

Removed Sections:
- N/A

Templates Updated:
- ✅ plan-template.md - Constitution Check section aligned
- ✅ spec-template.md - Phase constraints section verified
- ✅ tasks-template.md - Agent behavior rules verified

Deferred Items:
- None

Version Bump Rationale:
- MINOR bump: New technologies added to Phase II without removing existing phase structure
- Phase isolation preserved: Phase I remains in-memory only, Phase III+ unchanged
- Backward compatible: Existing Phase I work unaffected
- Material expansion: Phase II scope significantly broadened from file persistence to full-stack web

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
| III | Enhanced Web | Advanced features, optimizations, improved UX |
| IV | Distributed Services | Microservices architecture, event-driven patterns |
| V | Cloud Native | Kubernetes, Kafka, Dapr, AI agents, orchestration |

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

### Phase III Constraints (Enhanced Web)

Adds to Phase II:
- Performance optimizations
- Advanced UI/UX features
- Caching strategies
- Background job processing
- Third-party integrations
- Still prohibited: Distributed systems, event streaming, AI agents

### Phase IV Constraints (Distributed Services)

Adds to Phase III:
- Microservices architecture
- Service mesh patterns
- Event-driven communication
- API gateway patterns
- Still prohibited: Container orchestration, AI agents, advanced cloud infrastructure

### Phase V Constraints (Cloud Native)

Adds to Phase IV:
- Docker containerization
- Kubernetes orchestration
- Kafka event streaming
- Dapr sidecar integration
- OpenAI Agents SDK
- MCP (Model Context Protocol)
- Advanced cloud infrastructure

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
| Docker | V | Containerization |
| Kubernetes | V | Orchestration |
| Kafka | V | Event streaming |
| Dapr | V | Distributed runtime |

### AI/Agent Technologies

| Technology | Phase Introduced | Purpose |
|------------|------------------|---------|
| OpenAI Agents SDK | V | Agent orchestration |
| MCP | V | Model context protocol |

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

- **RULE QP-005**: Services MUST be stateless where cloud-native deployment is targeted (Phase V)
- **RULE QP-006**: State MUST be externalized to databases, caches, or message queues
- **RULE QP-007**: Session state MUST be managed through tokens, not server memory

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

### Cloud-Native Readiness (Phase V)

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
|------------|---|----|----|----|----|
| Python | ✓ | ✓ | ✓ | ✓ | ✓ |
| In-memory | ✓ | | | | |
| FastAPI | | ✓ | ✓ | ✓ | ✓ |
| SQLModel | | ✓ | ✓ | ✓ | ✓ |
| Neon DB | | ✓ | ✓ | ✓ | ✓ |
| Next.js | | ✓ | ✓ | ✓ | ✓ |
| TypeScript | | ✓ | ✓ | ✓ | ✓ |
| Better Auth | | ✓ | ✓ | ✓ | ✓ |
| Docker | | | | | ✓ |
| Kubernetes | | | | | ✓ |
| Kafka | | | | | ✓ |
| Dapr | | | | | ✓ |
| AI/Agents | | | | | ✓ |

---

**Version**: 1.1.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2026-01-03
