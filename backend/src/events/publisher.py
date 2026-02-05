"""Event publisher utilities for Dapr pub/sub integration."""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException
from dapr.clients import DaprClient
from .schemas import (
    TaskCreatedEvent, TaskUpdatedEvent, TaskCompletedEvent,
    RecurringTaskCreatedEvent, RecurringTaskInstanceCreatedEvent,
    ReminderScheduledEvent, ReminderTriggeredEvent
)


class EventPublisher:
    """Utility class for publishing events via Dapr pub/sub."""

    def __init__(self):
        """Initialize the event publisher."""
        self.dapr_client = None  # Will be initialized on demand to avoid connection issues

    def _get_dapr_client(self) -> DaprClient:
        """Get a Dapr client instance, creating one if needed."""
        if not self.dapr_client:
            self.dapr_client = DaprClient()
        return self.dapr_client

    async def publish_task_created(self, task_data: Dict[str, Any], source: str = "/api/tasks") -> bool:
        """
        Publish a task created event.

        Args:
            task_data: Dictionary containing task information
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "task_id": str(task_data.get("id")),
                "user_id": str(task_data.get("user_id")),
                "title": task_data.get("title"),
                "description": task_data.get("description"),
                "priority": task_data.get("priority"),
                "tags": task_data.get("tags", []),
                "due_date": task_data.get("due_date").isoformat() if task_data.get("due_date") else None,
                "remind_at": task_data.get("remind_at").isoformat() if task_data.get("remind_at") else None,
                "recurrence_rule": task_data.get("recurrence_rule"),
                "created_at": task_data.get("created_at").isoformat() if task_data.get("created_at") else None
            }

            event = TaskCreatedEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='task-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing task created event: {str(e)}")
            return False

    async def publish_task_updated(self, task_data: Dict[str, Any], changed_fields: list, source: str = "/api/tasks") -> bool:
        """
        Publish a task updated event.

        Args:
            task_data: Dictionary containing updated task information
            changed_fields: List of field names that were changed
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "task_id": str(task_data.get("id")),
                "user_id": str(task_data.get("user_id")),
                "title": task_data.get("title"),
                "description": task_data.get("description"),
                "priority": task_data.get("priority"),
                "tags": task_data.get("tags", []),
                "due_date": task_data.get("due_date").isoformat() if task_data.get("due_date") else None,
                "remind_at": task_data.get("remind_at").isoformat() if task_data.get("remind_at") else None,
                "recurrence_rule": task_data.get("recurrence_rule"),
                "changed_fields": changed_fields,
                "updated_at": task_data.get("updated_at").isoformat() if task_data.get("updated_at") else None
            }

            event = TaskUpdatedEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='task-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing task updated event: {str(e)}")
            return False

    async def publish_task_completed(self, task_data: Dict[str, Any], source: str = "/api/tasks") -> bool:
        """
        Publish a task completed event.

        Args:
            task_data: Dictionary containing task information
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "task_id": str(task_data.get("id")),
                "user_id": str(task_data.get("user_id")),
                "completed_at": datetime.now().isoformat()
            }

            event = TaskCompletedEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='task-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing task completed event: {str(e)}")
            return False

    async def publish_recurring_task_created(self, task_data: Dict[str, Any], source: str = "/api/recurring-tasks") -> bool:
        """
        Publish a recurring task created event.

        Args:
            task_data: Dictionary containing recurring task information
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "task_id": str(task_data.get("id")),
                "user_id": str(task_data.get("user_id")),
                "title": task_data.get("title"),
                "recurrence_rule": task_data.get("recurrence_rule"),
                "next_occurrence": task_data.get("next_occurrence").isoformat() if task_data.get("next_occurrence") else None,
                "created_at": task_data.get("created_at").isoformat() if task_data.get("created_at") else None
            }

            event = RecurringTaskCreatedEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='recurring-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing recurring task created event: {str(e)}")
            return False

    async def publish_recurring_task_instance_created(self, original_task_id: str, new_instance_id: str, user_id: str, occurrence_date: datetime, source: str = "/services/recurring-task-processor") -> bool:
        """
        Publish a recurring task instance created event.

        Args:
            original_task_id: ID of the original recurring task template
            new_instance_id: ID of the new recurring task instance
            user_id: User ID
            occurrence_date: Occurrence date
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "original_task_id": original_task_id,
                "new_instance_id": new_instance_id,
                "user_id": user_id,
                "occurrence_date": occurrence_date.isoformat()
            }

            event = RecurringTaskInstanceCreatedEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='recurring-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing recurring task instance created event: {str(e)}")
            return False

    async def publish_reminder_scheduled(self, task_id: str, user_id: str, scheduled_time: datetime, reminder_type: str = "due_date_reminder", source: str = "/services/reminder-service") -> bool:
        """
        Publish a reminder scheduled event.

        Args:
            task_id: Task ID
            user_id: User ID
            scheduled_time: When the reminder is scheduled for
            reminder_type: Type of reminder (default: due_date_reminder)
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "task_id": task_id,
                "user_id": user_id,
                "scheduled_time": scheduled_time.isoformat(),
                "reminder_type": reminder_type
            }

            event = ReminderScheduledEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='reminder-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing reminder scheduled event: {str(e)}")
            return False

    async def publish_reminder_triggered(self, task_id: str, user_id: str, reminder_type: str = "due_date_reminder", source: str = "/services/reminder-service") -> bool:
        """
        Publish a reminder triggered event.

        Args:
            task_id: Task ID
            user_id: User ID
            reminder_type: Type of reminder (default: due_date_reminder)
            source: Source of the event

        Returns:
            True if event was published successfully, False otherwise
        """
        try:
            event_data = {
                "task_id": task_id,
                "user_id": user_id,
                "triggered_time": datetime.now().isoformat(),
                "reminder_type": reminder_type
            }

            event = ReminderTriggeredEvent(
                id=str(uuid.uuid4()),
                source=source,
                time=datetime.now(),
                data=event_data
            )

            with self._get_dapr_client() as client:
                client.publish_event(
                    pubsub_name='todo-pubsub',
                    topic_name='reminder-events',
                    data=json.dumps(event.dict()),
                    data_content_type='application/json'
                )

            return True
        except Exception as e:
            print(f"Error publishing reminder triggered event: {str(e)}")
            return False

    def close(self):
        """Close the Dapr client connection."""
        if self.dapr_client:
            self.dapr_client.close()
            self.dapr_client = None