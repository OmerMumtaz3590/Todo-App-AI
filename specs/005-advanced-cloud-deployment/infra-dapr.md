# Dapr Infrastructure Specification: Task Management System

**Feature**: Advanced Cloud Deployment - Phase V
**Sub-feature**: Dapr integration and configuration
**Created**: 2026-02-05

## Overview

This document specifies the Dapr infrastructure configuration for the task management system, implementing service components for pub/sub, state management, secrets, service invocation, and job scheduling.

## Dapr Configuration Components

### Pub/Sub Component (Apache Kafka)

**Component Name**: `task-pubsub`
**Type**: `pubsub.kafka`
**Version**: `v1`

#### Configuration Details:
- **Brokers**: Kafka cluster endpoints (local: Minikube, cloud: Azure AKS/Redpanda)
- **Consumer Group**: Separate groups for different services (frontend, backend, reminder-service)
- **Auth**: SASL_SSL for secure communication
- **Partitions**: Configurable based on expected load
- **Replication Factor**: Minimum 2 for durability
- **Retention Policy**: 7 days for debugging, configurable

#### Topics Configuration:
- `task-events`: Task lifecycle events
- `reminder-events`: Scheduled reminder notifications
- `task-update-events`: Task property changes
- `recurring-events`: Recurring task generation
- `notification-events`: User notification events

### State Store Component (PostgreSQL)

**Component Name**: `task-statestore`
**Type**: `state.postgresql`
**Version**: `v1`

#### Configuration Details:
- **Connection String**: Reference to Neon database connection via secrets
- **Table Name**: `dapr_state` (default)
- **Schema**: `public` (default)
- **Actor State Store**: True for actor-based services
- **Concurrency**: FirstWrite (to handle concurrent updates)
- **Consistency**: Strong for critical operations

### Secret Store Component (Kubernetes)

**Component Name**: `task-secretstore`
**Type**: `secretstores.kubernetes`
**Version**: `v1`

#### Configuration Details:
- **Namespace**: Application namespace (`todo-app`)
- **Allow Reference**: Allow only specific secret references for security
- **Trust Domain**: Kubernetes cluster trust domain

### Service Invocation Component (mTLS)

**Component Name**: `task-serviceinvocation`
**Type**: Dapr's built-in service invocation
**Configuration**:
- **Authentication**: mTLS enabled
- **Protocol**: HTTP/2 for efficiency
- **Load Balancing**: Round-robin
- **Retry Policy**: Exponential backoff with max 5 retries

## Dapr Sidecar Configuration

### Sidecar Annotations for Kubernetes Deployments

#### Backend Service:
```yaml
dapr.io/enabled: "true"
dapr.io/app-id: "todo-backend"
dapr.io/app-port: "8000"
dapr.io/app-protocol: "http"
dapr.io/app-max-concurrency: "10"
dapr.io/config: "app-config"
dapr.io/log-level: "info"
dapr.io/sidecar-cpu-limit: "0.5"
dapr.io/sidecar-cpu-request: "0.1"
dapr.io/sidecar-memory-limit: "512Mi"
dapr.io/sidecar-memory-request: "128Mi"
```

#### Frontend Service:
```yaml
dapr.io/enabled: "true"
dapr.io/app-id: "todo-frontend"
dapr.io/app-port: "3000"
dapr.io/app-protocol: "http"
dapr.io/app-max-concurrency: "100"
dapr.io/config: "app-config"
dapr.io/log-level: "info"
```

## Dapr API Usage Patterns

### Pub/Sub Operations

#### Publishing Events:
```python
# Python example
dapr_client.publish_event(
    pubsub_name='task-pubsub',
    topic_name='task-events',
    data=json.dumps(event_data),
    metadata={
        'ttlInSeconds': '3600'
    }
)
```

#### Subscribing to Events:
```python
# Dapr subscription configuration (components/task-subscription.yaml)
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-processor-subscription
spec:
  topic: task-events
  route: /process-task
  pubsubname: task-pubsub
  scopes:
  - todo-backend
```

### State Operations

#### Saving State:
```python
# Save task state
dapr_client.save_state(
    store_name='task-statestore',
    key=f'user-{user_id}-task-{task_id}',
    value=task_data
)
```

#### Retrieving State:
```python
# Get task state
task_state = dapr_client.get_state(
    store_name='task-statestore',
    key=f'user-{user_id}-task-{task_id}'
).data
```

#### Deleting State:
```python
# Delete task state
dapr_client.delete_state(
    store_name='task-statestore',
    key=f'user-{user_id}-task-{task_id}'
)
```

### Secret Operations

#### Retrieving Secrets:
```python
# Get database connection string
secret_response = dapr_client.get_secret(
    store_name='task-secretstore',
    key='database-url',
    metadata={'namespace': 'todo-app'}
)
database_url = secret_response.data['database-url']
```

### Service Invocation

#### Calling Another Service:
```python
# Call reminder service
response = dapr_client.invoke_method(
    app_id='reminder-service',
    method_name='schedule-reminder',
    data=json.dumps(reminder_request),
    http_verb='POST'
)
```

## Dapr Job Scheduling (Cron Bindings)

### Reminder Scheduler Binding:
```yaml
apiVersion: dapr.io/v2alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "*/5 * * * *"  # Check for reminders every 5 minutes
---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: reminder-scheduler-subscription
spec:
  topic: reminder-cron
  route: /check-and-send-reminders
  pubsubname: reminder-cron
  scopes:
  - reminder-service
```

### Recurring Task Generator:
```yaml
apiVersion: dapr.io/v2alpha1
kind: Component
metadata:
  name: recurring-task-cron
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "0 1 * * *"  # Check for recurring tasks daily at 1AM
---
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: recurring-task-subscription
spec:
  topic: recurring-task-cron
  route: /generate-recurring-tasks
  pubsubname: recurring-task-cron
  scopes:
  - task-service
```

## Dapr Configuration for Resilience

### Circuit Breaker Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: app-config
spec:
  spec:
    tracing:
      samplingRate: "1"
      zipkin:
        endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v2/spans"
  httpPipeline:
    handlers:
    - name: circuitBreaker
      type: middleware.http.circuitbreaker
      metadata:
      - name: maxRequests
        value: "1"
      - name: timeout
        value: "30s"
      - name: interval
        value: "1m"
```

### Retry and Timeout Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: service-calls-config
spec:
  serviceInvocation:
    retryPolicy:
      threshold: 3
      backoff:
        initialInterval: 200ms
        maxInterval: 15s
        multiplier: 2
    timeout: 30s
```

## Security Configuration

### Service-to-Service Authentication:
- mTLS enabled for all Dapr sidecar communications
- Service principal authentication for cloud deployments
- Certificate rotation policy (90-day renewal)
- Identity-based access control (Azure AD for AKS)

### Secret Management:
- Secrets stored in Kubernetes secrets for K8s deployments
- Automatic secret refresh intervals
- Encrypted secret transport
- RBAC for secret access

## Monitoring and Observability

### Dapr Telemetry Configuration:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: tracing-config
spec:
  tracing:
    samplingRate: "0.8"
    zipkin:
      endpointAddress: "http://jaeger-collector.default.svc.cluster.local:9411/api/v2/spans"
  metric:
    enabled: true
    rules:
    - name: dapr_requests_total
      description: "Total number of requests"
```

### Logging Configuration:
- Structured JSON logging
- Correlation IDs for distributed tracing
- Log levels configurable per environment
- Centralized log aggregation (Fluentd/Filebeat)

## Deployment Considerations

### Local Deployment (Minikube):
- Dapr installed with self-hosted Kafka/Redpanda
- Neon database connection
- In-memory state stores for development (configurable)
- Local certificate generation for mTLS

### Cloud Deployment (Azure AKS):
- Managed Dapr (if available) or self-managed
- Azure Managed Kafka (or Redpanda Cloud)
- Azure Key Vault for secret management
- Azure Monitor for telemetry
- Private endpoints for secure access

## Performance Requirements

### Dapr Sidecar Resources:
- CPU: Minimum 0.1 core, Limit 0.5 core
- Memory: Minimum 128MB, Limit 512MB
- Network: Efficient gRPC communication
- Storage: Minimal for sidecar operations

### Throughput Targets:
- Handle 1000+ events per second through pub/sub
- Sub-second response times for state operations
- < 50ms latency for service invocations
- Support 10,000+ concurrent Dapr sidecars

## Success Criteria

- Dapr sidecars successfully integrated with all services in local Minikube environment
- Event-driven communication operates reliably through Dapr pub/sub with Kafka
- State management uses Dapr state stores with Neon PostgreSQL backend
- Secrets are properly managed through Dapr secret stores
- Service invocation works correctly between services using Dapr
- Job scheduling operates properly using Dapr cron bindings for reminders
- Performance meets targets with <100ms latency for all Dapr operations
- System demonstrates resilience with automatic recovery from Dapr sidecar failures