# Kafka Infrastructure Specification: Task Management System

**Feature**: Advanced Cloud Deployment - Phase V
**Sub-feature**: Kafka integration and configuration
**Created**: 2026-02-05

## Overview

This document specifies the Apache Kafka infrastructure configuration for the task management system, implementing event-driven communication patterns through Dapr pub/sub abstraction.

## Kafka Cluster Configuration

### Cluster Architecture
- **Broker Count**: Minimum 3 for HA in production, 1 for local development
- **Partitions**: Configurable per topic based on throughput requirements
- **Replication Factor**: 3 for production, 1 for local development
- **Zookeeper**: Embedded (KRaft mode preferred) or separate ensemble

### Topic Specifications

#### 1. `task-events`
- **Partitions**: 6 (scaleable based on event volume)
- **Replication**: 3
- **Retention**: 7 days (for debugging and replay)
- **Cleanup Policy**: Compact (for task state updates)
- **Segment Bytes**: 100MB
- **Description**: All task lifecycle events (create, update, delete, complete)

#### 2. `reminder-events`
- **Partitions**: 3
- **Replication**: 3
- **Retention**: 3 days (time-sensitive notifications)
- **Cleanup Policy**: Delete (short-lived events)
- **Description**: Scheduled and triggered reminder notifications

#### 3. `task-update-events`
- **Partitions**: 4
- **Replication**: 3
- **Retention**: 7 days
- **Cleanup Policy**: Compact (for tracking changes)
- **Description**: Changes to task properties (priority, tags, due dates)

#### 4. `recurring-events`
- **Partitions**: 2
- **Replication**: 3
- **Retention**: 30 days (longer for recurring task history)
- **Cleanup Policy**: Delete
- **Description**: Recurring task generation and scheduling events

#### 5. `notification-events`
- **Partitions**: 4
- **Replication**: 3
- **Retention**: 1 day (transient notifications)
- **Cleanup Policy**: Delete
- **Description**: User notification dispatch events

## Kafka Configuration Parameters

### Server Properties
```properties
# Performance tuning
num.network.threads=8
num.io.threads=16
socket.send.buffer.bytes=102400
socket.receive.buffer.bytes=102400
socket.request.max.bytes=104857600

# Log management
log.retention.hours=168
log.segment.bytes=1073741824
log.retention.check.interval.ms=300000

# Replication
default.replication.factor=3
min.insync.replicas=2

# Performance optimization
replica.fetch.max.bytes=1048576
message.max.bytes=1000012
replica.fetch.response.max.bytes=1048576
```

### Client Configuration
- **Producer Acknowledgments**: `acks=all` for durability
- **Producer Retries**: `retries=2147483647` (effectively infinite)
- **Consumer Group Protocol**: `classic` or `consumer` (new protocol)
- **Serialization**: JSON for events (avro for production systems)

## Kafka Security Configuration

### Authentication
- **SASL/SSL**: Enabled for secure communication
- **Mechanism**: SCRAM-SHA-256 or OAUTHBEARER
- **Client Authentication**: Required for producers and consumers
- **Super User**: Dedicated admin account for monitoring

### Authorization
- **ACLs**: Fine-grained access control per topic
- **Principal Mapping**: Map to internal user roles
- **Resource Types**: Topics, Consumer Groups, Clusters

### Encryption
- **Inter-broker**: TLS 1.2+ for all internal communication
- **Client-broker**: TLS 1.2+ for all external communication
- **Data at Rest**: Encrypted volumes (if required)

## Kafka Connect Configuration

### Connectors Needed
1. **Monitor Connector**: Monitor system health and performance
2. **Archive Connector**: Archive old events to long-term storage
3. **Alert Connector**: Send alerts based on topic metrics

## Kafka Streams Processing

### Stream Processing Requirements
- **Repartitioning**: For load balancing across consumers
- **Windowing**: Time-based windows for event aggregation
- **Joins**: Join events from different topics when needed
- **Aggregations**: Aggregate events for reporting

## Dapr-Kafka Integration

### Dapr Component Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-broker-1:9092,kafka-broker-2:9092,kafka-broker-3:9092"
  - name: consumerGroup
    value: "dapr-consumer-group"
  - name: clientID
    value: "dapr-client"
  - name: authRequired
    value: "true"
  - name: saslUsername
    value: "dapr-user"
  - name: saslPassword
    value: "{{ .secrets.kafka.password }}"
  - name: maxMessageBytes
    value: "1048576"
  - name: consumeRetryInterval
    value: "200ms"
```

### Topic Declaration for Dapr
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-topic
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: topic
    value: "task-events"
  - name: partitionCount
    value: "6"
  - name: replicationFactor
    value: "3"
```

## Local Development Configuration (Minikube)

### Kafka Deployment
- **Image**: `bitnami/kafka:latest` or `strimzi/kafka:latest`
- **Storage**: Persistent volumes for log data
- **Resources**:
  - CPU: 0.5-1.0 cores
  - Memory: 1-2GB per broker
  - Storage: 10GB+ per broker

### Topic Creation Script
```bash
# Create topics for local development
kafka-topics.sh --create --topic task-events --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
kafka-topics.sh --create --topic reminder-events --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
kafka-topics.sh --create --topic task-update-events --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
kafka-topics.sh --create --topic recurring-events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics.sh --create --topic notification-events --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1
```

## Cloud Deployment Configuration (Azure AKS)

### Managed Kafka Options
1. **Azure Event Hubs for Kafka**: Native Kafka API compatibility
2. **Confluent Cloud**: Fully managed Kafka service
3. **Self-hosted with Strimzi**: Operator-based Kafka on K8s
4. **Redpanda Cloud**: Modern Kafka-compatible platform (preferred per requirements)

### Redpanda Cloud Configuration
- **Tier**: Shared or Dedicated based on requirements
- **Regions**: Multi-region for HA
- **Throughput**: Configurable based on event volume
- **Storage**: SSD-based for performance
- **Management**: Web UI and CLI tools

### Self-Managed Kafka with Strimzi
```yaml
apiVersion: kafka.strimzi.io/v1beta2
kind: Kafka
metadata:
  name: todo-kafka
spec:
  kafka:
    version: 3.6.0
    replicas: 3
    listeners:
      - name: plain
        port: 9092
        type: internal
        tls: false
      - name: tls
        port: 9093
        type: internal
        tls: true
    config:
      offsets.topic.replication.factor: 3
      transaction.state.log.replication.factor: 3
      transaction.state.log.min.isr: 2
      default.replication.factor: 3
      min.insync.replicas: 2
      inter.broker.protocol.version: "3.6"
    storage:
      type: jbod
      volumes:
      - id: 0
        type: persistent-claim
        size: 100Gi
        deleteClaim: false
  zookeeper:
    replicas: 3
    storage:
      type: persistent-claim
      size: 10Gi
      deleteClaim: false
  entityOperator:
    topicOperator: {}
    userOperator: {}
```

## Monitoring and Observability

### Kafka Metrics
- **Throughput**: Messages per second (inbound and outbound)
- **Latency**: End-to-end message delivery time
- **Consumption Lag**: Consumer group lag behind producer
- **Partition Distribution**: Load balancing across partitions
- **Disk Usage**: Storage consumption and growth rate

### Key Metrics to Track
- `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec`
- `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec`
- `kafka.consumer:type=consumer-fetch-manager-metrics,client-id=*,topic=*`
- `kafka.server:type=ReplicaManager,name=UnderReplicatedPartitions`

### Monitoring Tools Integration
- **Prometheus**: Kafka Exporter for metrics collection
- **Grafana**: Dashboards for Kafka performance visualization
- **Jaeger**: Distributed tracing for message flows
- **ELK Stack**: Log aggregation and analysis

## Performance Tuning

### Partition Sizing Guidelines
- **Throughput-Based**: ~1MB/sec per partition for optimal performance
- **Consumer Parallelism**: Match partitions to consumer count
- **Cluster Resources**: Ensure adequate resources per partition
- **Balancing**: Distribute partitions evenly across brokers

### Producer Tuning
- `batch.size`: 16384 bytes (default)
- `linger.ms`: 5ms for batching optimization
- `compression.type`: snappy for balance of speed and compression
- `acks`: all for durability

### Consumer Tuning
- `fetch.min.bytes`: 1 byte (for real-time processing)
- `max.poll.records`: 500 (balance throughput and memory)
- `enable.auto.commit`: false (for precise control)
- `auto.offset.reset`: earliest (for replay capability)

## Backup and Disaster Recovery

### Backup Strategy
- **Topic Snapshots**: Periodic backup of critical topic data
- **Configuration Backup**: Export and version-control topic configurations
- **Offset Backup**: Preserve consumer positions for disaster recovery

### Recovery Procedures
- **Topic Restoration**: Recreate topics with identical configuration
- **Data Recovery**: Replay events from backup to current state
- **Offset Recovery**: Resume consumption from correct positions

## Event Schema Management

### Schema Registry
- **Avro**: Preferred for schema evolution
- **JSON Schema**: For simpler validation requirements
- **Compatibility Rules**: Backward/forward compatibility policies
- **Versioning**: Semantic versioning for schema evolution

### Schema Evolution
- **Backward Compatible**: New versions can read old messages
- **Forward Compatible**: Old versions can read new messages
- **Full Compatibility**: Bidirectional compatibility
- **Breaking Changes**: Coordinated deployment strategy

## Success Criteria

- Kafka cluster successfully deployed and operational in local Minikube environment with Dapr integration
- All required topics created with appropriate partitions and retention policies
- Dapr pub/sub successfully publishes and consumes events from Kafka topics
- Event throughput supports 1000+ events per second with <100ms latency
- System demonstrates resilience with automatic recovery from broker failures
- Kafka cluster properly secured with authentication and encryption
- Cloud deployment (Redpanda or AKS with Strimzi) supports the same functionality as local development environment