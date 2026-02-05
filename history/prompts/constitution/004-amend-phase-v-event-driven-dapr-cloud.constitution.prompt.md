---
id: "004"
title: "Update constitution Phase V event-driven Dapr cloud standards"
stage: "constitution"
date_iso: "2026-02-05"
model: "claude-sonnet-4-5-20250929"
surface: "agent"
feature: "none"
branch: "004-local-k8s-deployment"
user: "Claude"
command: "/sp.constitution Update constitution for Phase V: Advanced Cloud Deployment"
labels: ["constitution", "phase-v", "event-driven", "dapr", "kafka", "cloud"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - constitution validation
outcome: "Successfully updated constitution to add Phase V rules for event-driven architecture, Dapr integration, Kafka streaming, and cloud deployment standards"
evaluation: "The constitution was updated with 20 new mandatory rules for Phase V including event-driven architecture, Dapr sidecar integration, and cloud deployment standards. All previous phase rules were preserved and the document maintains consistency with existing governance structure."
---

# Update constitution: add Phase V event-driven, Dapr & cloud standards

## PROMPT_TEXT

Update constitution for Phase V: Advanced Cloud Deployment

Add these mandatory global rules (Phase V+):

1. From Phase V onward: application MUST be event-driven using Kafka (or compatible Pub/Sub) + Dapr for decoupling
2. All new features (recurring tasks, due dates/reminders, priorities, tags, search/filter/sort) MUST use events for async processing
3. Use Dapr sidecar for:
   - Pub/Sub (Kafka abstraction)
   - State management
   - Secrets
   - Service invocation
   - Jobs API or cron bindings for scheduled reminders
4. Deployments MUST support:
   - Local: Minikube with Dapr + self-hosted Kafka/Redpanda
   - Cloud: AKS / GKE / OKE with managed or self-hosted Kafka
5. Infrastructure remains fully spec-driven (specs/infra/dapr.md, specs/infra/kafka.md, specs/infra/cloud.md)
6. CI/CD via GitHub Actions required for build → push → deploy
7. Maintain stateless pods; Neon DB + Dapr state as single source of truth
8. No direct Kafka client code — always use Dapr Pub/Sub abstraction
9. All services MUST run with Dapr sidecar in production-grade K8s
10. Monitoring/logging basics MUST be documented

Preserve previous phase rules.
Commit with: "Update constitution: add Phase V event-driven, Dapr & cloud standards"

## RESPONSE_TEXT

I have successfully updated the constitution file with the new Phase V rules as requested. The key changes include:

### New Section Added: XI. Phase V Global Rules – Event-Driven Architecture Standards

This section includes 20 new mandatory rules organized into 5 categories:

1. **Event-Driven Architecture Requirements (EVS-001 to EVS-005)**:
   - Applications must be event-driven using Kafka + Dapr for decoupling
   - New features must use events for async processing
   - Events must be idempotent and support replay
   - Event schemas must be versioned and backward-compatible

2. **Dapr Sidecar Integration (DAP-001 to DAP-005)**:
   - Dapr sidecar must be used for all Pub/Sub, state management, secrets, service invocation
   - No direct Kafka client code - always use Dapr abstraction
   - Cron jobs must use Dapr bindings

3. **Deployment & Infrastructure Requirements (EVS-006 to EVS-010)**:
   - Support for local Minikube with Dapr + Kafka/Redpanda
   - Cloud support for AKS/GKE/OKE with managed/self-hosted Kafka
   - All services must run with Dapr sidecar in production
   - Infrastructure remains spec-driven under `specs/infra/`
   - CI/CD via GitHub Actions required

4. **Service Architecture (EVS-011 to EVS-015)**:
   - Maintain stateless pods with Neon DB + Dapr as source of truth
   - Microservices architecture required for new functionality
   - Services must have bounded contexts
   - Circuit breakers and saga patterns for resilience

5. **Observability & Monitoring (EVS-016 to EVS-020)**:
   - Distributed tracing via Dapr
   - Centralized logging with correlation IDs
   - Prometheus metrics
   - Event processing health checks
   - Production monitoring documentation

### Other Changes Made:
- Updated Phase V definition from "Production Cloud & Distributed Services" to "Event-Driven Distributed Services"
- Modified Phase V constraints section to reflect event-driven architecture requirements
- Updated technology matrix to show Kafka and Dapr availability in Phase V
- Updated version from 2.1.0 to 2.2.0 with minor version bump rationale
- Maintained all previous phase rules and governance structure

The constitution now comprehensively covers the event-driven architecture requirements for Phase V while preserving all existing governance for previous phases.