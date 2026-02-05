---
id: 003
title: Amend Phase IV Cloud-Native Deployment
stage: constitution
date: 2026-02-04
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 003-todo-ai-chatbot
user: architect
command: /sp.constitution
labels: ["constitution", "phase-iv", "kubernetes", "docker", "helm", "deployment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - null
---

## Prompt

Enhance constitution for Phase IV – Cloud-Native Local Deployment

Add/enhance these sections:

## Deployment & Infrastructure Standards (Phase IV+)
- All services MUST run in Kubernetes (Minikube for local)
- Containerization: separate Dockerfiles for frontend (Next.js/ChatKit) and backend (FastAPI)
- Prefer Docker AI Agent (Gordon) for Dockerfile creation & optimization
- Packaging: Helm Charts required (one chart or separate for frontend/backend)
- AI-assisted ops: kubectl-ai for manifests/commands, kagent for analysis & troubleshooting
- Spec-driven infra: all K8s/Helm config generated from specs/infra/

## Security & Configuration
- Sensitive values (DB URL, JWT secret, OpenAI keys) in Kubernetes Secrets
- Helm values.yaml for configurable parameters
- Enforce existing stateless + JWT rules in containerized environment

Update file, show added/changed parts, then commit.

## Response snapshot

Amended constitution from v2.0.0 to v2.1.0 (MINOR bump). Key changes:

- **Phase IV redefined**: "Distributed Services" → "Cloud-Native Local Deployment"
- **Phase V redefined**: "Cloud Native" → "Production Cloud & Distributed Services"
- **New Section X**: Phase IV Global Rules – Deployment & Infrastructure Standards (18 DIS-* rules)
  - DIS-001–005: Containerization (Minikube, separate Dockerfiles, Gordon, multi-stage, no embedded secrets)
  - DIS-010–014: Kubernetes & Orchestration (Helm required, kubectl-ai/kagent, specs/infra/, health checks)
  - DIS-020–024: Security & Configuration (K8s Secrets, values.yaml, non-root, NetworkPolicies)
  - DIS-030–032: Infrastructure as Code (version-controlled, SDD workflow, Helm versioning)
  - DIS-040–042: Deployment Workflow (build→push→helm, rollback, environment parity)
- **Technology tables updated**: Docker/K8s moved from Phase V→IV, new Infrastructure Tooling table (Gordon, kubectl-ai, kagent), Helm added
- **Quality Principles**: Cloud-Native Readiness changed from "(Phase V)" to "(Phase IV+)"
- **Phase Technology Matrix**: Updated with 6 new Phase IV entries

Templates verified — no changes needed (plan-template.md, spec-template.md, tasks-template.md all use generic rule references).

## Outcome

- Impact: Constitution v2.1.0 — Phase IV scope defined with 18 new deployment rules
- Tests: N/A (governance document)
- Files: 1 file modified (.specify/memory/constitution.md)
- Next prompts: /sp.specify for Phase IV feature, then /sp.plan, /sp.tasks, /sp.implement
- Reflection: MINOR bump appropriate since Phase IV was never implemented; no backward compatibility break for existing artifacts

## Evaluation notes (flywheel)

- Failure modes observed: None — clean amendment
- Graders run and results (PASS/FAIL): Manual review PASS — all placeholders filled, version line matches report, dates ISO format, rules declarative and testable
- Prompt variant (if applicable): standard /sp.constitution invocation with detailed user input
- Next experiment: Phase IV specification and planning using the new constitution rules
