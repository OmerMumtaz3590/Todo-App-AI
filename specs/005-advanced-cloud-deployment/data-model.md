# Data Model: Advanced Task Management Features

**Feature**: Phase V - Advanced Cloud Deployment
**Created**: 2026-02-05

## Overview

This document defines the data model updates for implementing advanced task management features including priorities, tags, due dates, recurring tasks, and reminders in the event-driven architecture.

## Updated Task Entity

### Fields

| Field Name | Type | Constraints | Description |
|------------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique identifier for the task |
| `user_id` | String | Foreign Key, Required | Owner of the task |
| `title` | String(255) | Required | Title of the task |
| `description` | Text | Optional | Detailed description of the task |
| `completed` | Boolean | Default: false | Completion status |
| `priority` | String(Enum) | Values: "HIGH", "MEDIUM", "LOW" | Priority level of the task |
| `tags` | JSON/Array | Max items: 10, Item length: 50 chars | Array of tag strings for categorization |
| `due_date` | DateTime | Optional | Date and time when the task is due |
| `remind_at` | DateTime | Optional | Date and time for sending reminder notification |
| `recurrence_rule` | JSON/String | Optional | Recurrence pattern in iCal format or custom JSON |
| `next_occurrence` | DateTime | Optional | Next occurrence date for recurring tasks |
| `parent_task_id` | Integer | Foreign Key, Optional | Reference to template for recurring tasks |
| `created_at` | DateTime | Auto-set | Timestamp when task was created |
| `updated_at` | DateTime | Auto-set, Updated | Timestamp when task was last updated |
| `completed_at` | DateTime | Optional | Timestamp when task was completed |

### Field Relationships

- `user_id` → `users.id` (Many-to-One)
- `parent_task_id` → `tasks.id` (Self-reference for recurring task templates)

### Validation Rules

- `priority` must be one of: "HIGH", "MEDIUM", "LOW"
- `due_date` must be in the future (not for recurring templates)
- `remind_at` must be before `due_date` (if both are set)
- `recurrence_rule` must follow valid recurrence pattern format
- `tags` array can contain maximum 10 items
- Each tag string must be 1-50 characters
- Each tag must match pattern: alphanumeric, hyphens, underscores only
- `remind_at` and `due_date` cannot be set for recurring task templates (parent tasks)

### Indexes

| Name | Fields | Purpose |
|------|--------|---------|
| `idx_user_priority_due_date` | user_id, priority, due_date | Optimize priority and due date filtering |
| `idx_user_tags` | user_id, tags | Optimize tag-based searches (GIN index for arrays) |
| `idx_remind_at` | remind_at | Optimize reminder scheduling queries |
| `idx_recurrence_rule` | parent_task_id, next_occurrence | Optimize recurring task processing |
| `idx_user_completed_updated` | user_id, completed, updated_at | Optimize user task list queries |

## Event Schema

### Task Event Types

#### 1. Task Created Event
```json
{
  "id": "unique-event-id",
  "type": "task.created",
  "source": "/api/tasks",
  "time": "2024-01-01T12:00:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid",
    "title": "Task title",
    "description": "Task description",
    "priority": "HIGH",
    "tags": ["work", "urgent"],
    "due_date": "2024-01-15T09:00:00Z",
    "remind_at": "2024-01-14T09:00:00Z",
    "recurrence_rule": null,
    "created_at": "2024-01-01T12:00:00Z"
  }
}
```

#### 2. Task Updated Event
```json
{
  "id": "unique-event-id",
  "type": "task.updated",
  "source": "/api/tasks/123",
  "time": "2024-01-02T10:00:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid",
    "title": "Updated task title",
    "priority": "MEDIUM",
    "tags": ["work", "urgent", "follow-up"],
    "due_date": "2024-01-20T09:00:00Z",
    "remind_at": "2024-01-19T09:00:00Z",
    "changed_fields": ["title", "priority", "due_date"]
  }
}
```

#### 3. Task Completed Event
```json
{
  "id": "unique-event-id",
  "type": "task.completed",
  "source": "/api/tasks/123/complete",
  "time": "2024-01-15T10:30:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid",
    "completed_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 4. Recurring Task Instance Created Event
```json
{
  "id": "unique-event-id",
  "type": "recurring.task.instance.created",
  "source": "/services/recurring-task-processor",
  "time": "2024-01-16T00:00:00Z",
  "data": {
    "original_task_id": 100,  // Parent template
    "new_instance_id": 200,   // New recurring instance
    "user_id": "user-uuid",
    "occurrence_date": "2024-01-23T00:00:00Z"
  }
}
```

#### 5. Reminder Scheduled Event
```json
{
  "id": "unique-event-id",
  "type": "reminder.scheduled",
  "source": "/services/reminder-service",
  "time": "2024-01-14T09:00:00Z",
  "data": {
    "task_id": 123,
    "user_id": "user-uuid",
    "scheduled_time": "2024-01-14T09:00:00Z",
    "reminder_type": "due_date_reminder"
  }
}
```

## Dapr State Store Structure

### Task State Management

Dapr state store will be used for:
1. Temporary processing state during event handling
2. Recurring task scheduler state
3. Reminder processing state

#### Sample State Keys
```
user-{user_id}-task-{task_id}-processing-lock
recurring-rule-{rule_id}-last-execution
reminder-job-{job_id}-state
```

### State Value Structure
```json
{
  "taskId": 123,
  "userId": "user-uuid",
  "status": "processing|completed|failed",
  "createdAt": "2024-01-01T12:00:00Z",
  "updatedAt": "2024-01-01T12:00:00Z",
  "metadata": {
    "attempts": 1,
    "lastError": null
  }
}
```

## Search and Filtering Schema

### Search Index
The following fields should be indexed for efficient searching:
- `title` (full-text search)
- `description` (full-text search)
- `tags` (array index)
- `priority` (value index)
- `due_date` (range index)

### Filtering Combinations
The system should support efficient filtering by:
- `user_id` + `priority` (common combination)
- `user_id` + `due_date` range
- `user_id` + `tags` (any of multiple tags)
- `user_id` + `completed` + `priority`
- `user_id` + `tags` + `due_date` range

## Event Sourcing Considerations

### Event Store Structure
Events related to tasks will be stored in the `task-events` Kafka topic and may be materialized to a separate event store for long-term retention and replay capabilities.

### State Reconstruction
Task state can be reconstructed by:
1. Reading the current state from the database
2. Applying all related events in chronological order
3. The resulting state represents the current task condition

### Snapshotting Strategy
- Take snapshots every N events for performance
- Store snapshots in the main database alongside current state
- Use snapshots as a starting point for replay operations