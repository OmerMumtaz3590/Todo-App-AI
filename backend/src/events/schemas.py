"""Event schemas for the event-driven architecture."""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from uuid import UUID


class BaseEvent(BaseModel):
    """Base event schema for all events."""
    id: str  # Unique identifier for the event
    type: str  # Type of the event (e.g., task.created, task.updated)
    source: str  # Source of the event (e.g., /api/tasks)
    time: datetime  # Timestamp of the event
    data: Dict[str, Any]  # Event-specific data payload
    correlation_id: Optional[str] = None  # ID to correlate related events
    causation_id: Optional[str] = None  # ID of the event that caused this event


class TaskCreatedEvent(BaseModel):
    """Schema for task created event."""
    id: str
    type: str = "task.created"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12345",
                "type": "task.created",
                "source": "/api/tasks",
                "time": "2024-01-01T10:00:00Z",
                "data": {
                    "task_id": "uuid-of-task",
                    "user_id": "uuid-of-user",
                    "title": "New task title",
                    "description": "Task description",
                    "priority": "MEDIUM",
                    "tags": ["work", "important"],
                    "due_date": "2024-01-15T09:00:00Z",
                    "remind_at": "2024-01-14T09:00:00Z",
                    "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1",
                    "created_at": "2024-01-01T10:00:00Z"
                }
            }
        }


class TaskUpdatedEvent(BaseModel):
    """Schema for task updated event."""
    id: str
    type: str = "task.updated"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12346",
                "type": "task.updated",
                "source": "/api/tasks/task-uuid",
                "time": "2024-01-01T11:00:00Z",
                "data": {
                    "task_id": "uuid-of-task",
                    "user_id": "uuid-of-user",
                    "title": "Updated task title",
                    "description": "Updated description",
                    "priority": "HIGH",
                    "tags": ["work", "important", "urgent"],
                    "due_date": "2024-01-20T09:00:00Z",
                    "remind_at": "2024-01-19T09:00:00Z",
                    "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1",
                    "changed_fields": ["title", "priority", "due_date"],
                    "updated_at": "2024-01-01T11:00:00Z"
                }
            }
        }


class TaskCompletedEvent(BaseModel):
    """Schema for task completed event."""
    id: str
    type: str = "task.completed"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12347",
                "type": "task.completed",
                "source": "/api/tasks/task-uuid/toggle",
                "time": "2024-01-01T12:00:00Z",
                "data": {
                    "task_id": "uuid-of-task",
                    "user_id": "uuid-of-user",
                    "completed_at": "2024-01-01T12:00:00Z"
                }
            }
        }


class RecurringTaskCreatedEvent(BaseModel):
    """Schema for recurring task created event."""
    id: str
    type: str = "recurring.task.created"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12348",
                "type": "recurring.task.created",
                "source": "/api/recurring-tasks",
                "time": "2024-01-01T09:00:00Z",
                "data": {
                    "task_id": "uuid-of-parent-task",
                    "user_id": "uuid-of-user",
                    "title": "Daily Standup",
                    "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1",
                    "next_occurrence": "2024-01-02T09:00:00Z",
                    "created_at": "2024-01-01T09:00:00Z"
                }
            }
        }


class RecurringTaskInstanceCreatedEvent(BaseModel):
    """Schema for recurring task instance created event."""
    id: str
    type: str = "recurring.task.instance.created"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12349",
                "type": "recurring.task.instance.created",
                "source": "/services/recurring-task-processor",
                "time": "2024-01-02T00:00:00Z",
                "data": {
                    "original_task_id": "uuid-of-parent-task",
                    "new_instance_id": "uuid-of-new-instance",
                    "user_id": "uuid-of-user",
                    "occurrence_date": "2024-01-02T09:00:00Z"
                }
            }
        }


class ReminderScheduledEvent(BaseModel):
    """Schema for reminder scheduled event."""
    id: str
    type: str = "reminder.scheduled"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12350",
                "type": "reminder.scheduled",
                "source": "/services/reminder-service",
                "time": "2024-01-01T09:00:00Z",
                "data": {
                    "task_id": "uuid-of-task",
                    "user_id": "uuid-of-user",
                    "scheduled_time": "2024-01-01T10:00:00Z",
                    "reminder_type": "due_date_reminder"
                }
            }
        }


class ReminderTriggeredEvent(BaseModel):
    """Schema for reminder triggered event."""
    id: str
    type: str = "reminder.triggered"
    source: str
    time: datetime
    data: Dict[str, Any]
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "evt-12351",
                "type": "reminder.triggered",
                "source": "/services/reminder-service",
                "time": "2024-01-01T10:00:00Z",
                "data": {
                    "task_id": "uuid-of-task",
                    "user_id": "uuid-of-user",
                    "triggered_time": "2024-01-01T10:00:00Z",
                    "reminder_type": "due_date_reminder"
                }
            }
        }


class EventPayload(BaseModel):
    """Generic event payload structure."""
    task_id: Optional[UUID] = None
    user_id: UUID
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    next_occurrence: Optional[datetime] = None
    parent_task_id: Optional[UUID] = None
    changed_fields: Optional[List[str]] = None