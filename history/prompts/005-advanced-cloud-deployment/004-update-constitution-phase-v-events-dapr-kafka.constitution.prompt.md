---
id: "004"
title: "Update constitution Phase V events dapr kafka"
stage: "constitution"
date_iso: "2026-02-05"
model: "claude-sonnet-4-5-20250929"
surface: "agent"
feature: "advanced-cloud-deployment"
branch: "005-advanced-cloud-deployment"
user: "Claude"
command: "/sp.constitution Update constitution for Phase V: Advanced Cloud Deployment with event-driven architecture"
labels: ["constitution", "phase-v", "event-driven", "dapr", "kafka", "cloud", "microservices"]
links:
  spec: "../specs/005-advanced-cloud-deployment/spec.md"
  plan: "../specs/005-advanced-cloud-deployment/plan.md"
  tasks: "../specs/005-advanced-cloud-deployment/tasks.md"
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - .specify/memory/constitution.md
tests_yaml: |
  - constitution validity check
  - rule consistency verification
  - phase constraint validation
outcome: "Successfully updated constitution with Phase V event-driven architecture rules and requirements"
evaluation: "Constitution now includes comprehensive rules for event-driven architecture, Dapr integration, Kafka streaming, and cloud deployment. All new requirements are properly integrated while preserving existing rules."
---

# Update constitution for Phase V: Advanced Cloud Deployment with event-driven architecture

## PROMPT_TEXT

Update constitution for Phase V: Advanced Cloud Deployment with event-driven architecture

Add these mandatory global rules (Phase V+):

1. From Phase V onward: application MUST be event-driven using Kafka (or compatible Pub/Sub) + Dapr for decoupling
2. All new features (recurring tasks, due dates/reminders, priorities, tags, search/filter/sort) MUST use events for async processing
3. Use Dapr sidecar for:
   - Pub/Sub (Kafka abstraction)
   - State management
   - Secrets
   - Service invocation
   - Jobs API or cron bindings for reminders
4. Deployments MUST support:
   - Local: Minikube with Dapr + self-hosted Kafka/Redpanda
   - Cloud: AKS / GKE / OKE with managed or self-hosted Kafka
5. Infrastructure remains fully spec-driven (specs/infra/dapr.md, specs/infra/kafka.md, specs/infra/cloud.md)
6. CI/CD via GitHub Actions required for build → push → deploy pipeline
7. Maintain stateless pods; Neon DB + Dapr state as single source of truth
8. No direct Kafka client code — always use Dapr Pub/Sub abstraction
9. All services MUST run with Dapr sidecar in production-grade K8s
10. Monitoring/logging basics MUST be documented

Preserve previous phase rules.
Commit with: "Update constitution: add Phase V event-driven, Dapr & cloud standards"

## RESPONSE_TEXT

Constitution has been successfully updated to include Phase V rules for event-driven architecture. Key additions include:

1. New Section XI: Phase V Global Rules – Event-Driven Architecture Standards (EVS-*, DAP-*)
2. Updated Phase V constraints to reflect event-driven architecture requirements
3. Modified technology matrix to move Kafka and Dapr from V+ to V (now required in Phase V)
4. Added detailed rules for Dapr integration (DAP-001 through DAP-005)
5. Added comprehensive event-driven architecture rules (EVS-001 through EVS-020)
6. Updated deployment requirements to include both local (Minikube) and cloud (AKS/GKE/OKE) targets
7. Enhanced infrastructure requirements with spec-driven approach for Dapr, Kafka, and cloud components
8. Added CI/CD requirements with GitHub Actions mandate
9. Strengthened security requirements with non-root containers and proper secret management
10. Preserved all existing Phase I-IV rules and constraints

The constitution now properly governs Phase V development with event-driven architecture patterns using Dapr and Kafka, while maintaining backward compatibility with existing phases.