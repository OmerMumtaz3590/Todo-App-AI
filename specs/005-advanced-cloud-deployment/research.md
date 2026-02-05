# Research Findings: Advanced Cloud Deployment with Event-Driven Architecture

**Feature**: Phase V - Advanced Cloud Deployment
**Created**: 2026-02-05

## Research Summary

This document consolidates research findings for implementing the event-driven architecture with Dapr and Kafka for the todo application.

## Key Decisions

### 1. Cloud Platform Selection
- **Decision**: Azure AKS (Azure Kubernetes Service)
- **Rationale**: Selected based on documentation familiarity, enterprise features, and integration capabilities with other Azure services. AKS provides managed Kubernetes with reduced operational overhead.
- **Alternatives considered**:
  - Google GKE: Strong contender with Anthos integration
  - Oracle OKE: Cost-effective but less documentation support
  - AWS EKS: Alternative option with extensive services

### 2. Kafka Provider
- **Decision**: Redpanda Cloud (free tier)
- **Rationale**: Chosen based on the specific requirement in the feature description that states "Redpanda Cloud free tier preferred". Offers Kafka-compatible API with better performance characteristics.
- **Alternatives considered**:
  - Self-hosted Kafka on Kubernetes with Strimzi operator
  - Azure Event Hubs for Kafka
  - Confluent Cloud

### 3. Task Priority Enum Values
- **Decision**: Three-tier priority system (HIGH, MEDIUM, LOW)
- **Rationale**: Matches the specification requirement for "high/medium/low" priorities
- **Implementation**: Will use string enum in the Task model

### 4. Tagging System Implementation
- **Decision**: Array of strings for tags with flexible naming
- **Rationale**: Flexible approach that allows multiple tags per task while keeping implementation simple
- **Considerations**: Need to implement tag validation to prevent abuse

### 5. Recurring Task Rules Implementation
- **Decision**: JSON object storing recurrence pattern
- **Rationale**: Flexible approach that allows complex recurrence rules while keeping database schema simple
- **Format**: Will follow RFC 5545 (iCalendar) recurrence rule format or a simplified version

### 6. Reminder System Architecture
- **Decision**: Dapr Job API with cron bindings for scheduling
- **Rationale**: Aligns with Phase V requirement to use Dapr for scheduled tasks (RULE DAP-005)
- **Implementation**: Use Dapr's cron binding capability for time-based triggers

### 7. Search Implementation Strategy
- **Decision**: Application-level search with database LIKE queries initially, with consideration for full-text search later
- **Rationale**: Practical approach for MVP implementation without requiring additional services like Elasticsearch
- **Scalability**: Can be enhanced later with dedicated search services

### 8. Dapr Component Configuration
- **Decision**: Separate components for pubsub, state, secrets, and bindings
- **Rationale**: Modularity and following Dapr best practices
- **State Store**: PostgreSQL will be used via Dapr state component wrapper

## Technology Integrations Researched

### Dapr with FastAPI
- Dapr provides Python SDK for integration with FastAPI applications
- Sidecar pattern allows for service invocation, state management, and pub/sub without code changes
- Configuration via Kubernetes annotations

### Kafka Integration via Dapr
- Dapr pubsub component can abstract Kafka complexity
- Provides uniform API regardless of underlying pubsub implementation
- Supports both publishing and consuming with retry policies

### Helm Chart Enhancements
- Need to add Dapr annotations to existing Phase IV Helm charts
- Additional templates for Dapr components (pubsub, state store, etc.)
- Environment-specific values for different deployment targets

## Risks and Mitigations

### 1. Dapr Learning Curve
- **Risk**: Team unfamiliarity with Dapr patterns
- **Mitigation**: Leverage existing documentation and start with simple pub/sub patterns

### 2. Kafka Message Ordering
- **Risk**: Task events may be processed out of order
- **Mitigation**: Include sequence numbers in events and implement idempotent processing

### 3. Reminder Delivery Reliability
- **Risk**: Missed or duplicated reminders
- **Mitigation**: Implement idempotent reminder handling and persistent state tracking

### 4. Database Migration Complexity
- **Risk**: Adding new fields to existing Task table
- **Mitigation**: Use Alembic migrations with proper testing

## Architecture Patterns Researched

### Event-Driven Architecture Patterns
- Command Query Responsibility Segregation (CQRS) for separating read/write operations
- Event sourcing for maintaining task state through event replay
- Saga pattern for complex operations spanning multiple services

### Dapr Building Blocks Applied
- Service-to-service invocation using Dapr's service invocation API
- State management using Dapr's state store API with PostgreSQL
- Publish/subscribe using Dapr's pubsub API with Kafka
- Secret management using Dapr's secret store API
- Actor pattern for recurring task management (optional future enhancement)

## Performance Considerations

### Event Processing
- Need to consider throughput requirements (1000+ concurrent events per Phase V requirements)
- Implement batching where appropriate for efficiency
- Use Dapr's built-in retry and circuit breaker patterns

### Database Operations
- Balance between Dapr state management and direct database access
- Consider caching strategies for frequently accessed data
- Optimize queries involving new fields (priority, tags, due_date)

## Deployment Considerations

### Local Development (Minikube)
- Dapr requires initialization on the cluster
- Kafka can be deployed as a container for local development
- Resource constraints should be considered for local environment

### Cloud Deployment (AKS)
- Dapr extension for AKS simplifies installation
- Integration with Azure services (Key Vault, PostgreSQL)
- Monitoring and observability setup with Azure Monitor

## Next Steps

1. Update Task model with new fields (priority, tags, due_date, remind_at, recurrence_rule)
2. Implement Dapr integration in backend services
3. Create Kafka topics and Dapr pubsub configuration
4. Implement MCP tools for new features
5. Update Helm charts for Dapr sidecar injection
6. Set up CI/CD pipeline for event-driven architecture