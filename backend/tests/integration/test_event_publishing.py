"""Integration tests for Dapr event publishing functionality."""
import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from uuid import uuid4
from fastapi.testclient import TestClient

from src.main import app
from src.events.publisher import EventPublisher
from src.models.todo import Todo, PriorityEnum


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def mock_dapr_client():
    """Mock Dapr client for testing event publishing."""
    with patch('dapr.clients.DaprClient') as mock:
        yield mock


class TestEventPublishingIntegration:
    """Integration tests for event publishing via Dapr."""

    async def test_event_publisher_initialization(self):
        """Test that EventPublisher can be initialized."""
        publisher = EventPublisher()
        assert publisher is not None

    async def test_publish_task_created_event(self, mock_dapr_client):
        """Test publishing of task created events via Dapr pub/sub."""
        # Mock the Dapr client and its methods
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample task data
        task_data = {
            "id": str(uuid4()),
            "user_id": str(uuid4()),
            "title": "Test Task",
            "description": "Test Description",
            "priority": "HIGH",
            "tags": ["test", "feature"],
            "due_date": datetime.now().isoformat(),
            "remind_at": datetime.now().isoformat(),
            "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1",
            "created_at": datetime.now().isoformat()
        }

        # Test the publish method
        result = await publisher.publish_task_created(task_data)

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'task-events'

    async def test_publish_task_updated_event(self, mock_dapr_client):
        """Test publishing of task updated events via Dapr pub/sub."""
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample task data
        task_data = {
            "id": str(uuid4()),
            "user_id": str(uuid4()),
            "title": "Updated Task",
            "description": "Updated Description",
            "priority": "MEDIUM",
            "tags": ["updated", "feature"],
            "due_date": datetime.now().isoformat(),
            "remind_at": datetime.now().isoformat(),
            "recurrence_rule": "RRULE:FREQ=WEEKLY;INTERVAL=1",
            "updated_at": datetime.now().isoformat()
        }
        changed_fields = ["title", "priority", "tags"]

        # Test the publish method
        result = await publisher.publish_task_updated(task_data, changed_fields)

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'task-events'

    async def test_publish_task_completed_event(self, mock_dapr_client):
        """Test publishing of task completed events via Dapr pub/sub."""
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample task data
        task_data = {
            "id": str(uuid4()),
            "user_id": str(uuid4()),
            "completed_at": datetime.now().isoformat()
        }

        # Test the publish method
        result = await publisher.publish_task_completed(task_data)

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'task-events'

    async def test_publish_recurring_task_created_event(self, mock_dapr_client):
        """Test publishing of recurring task created events via Dapr pub/sub."""
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample recurring task data
        task_data = {
            "id": str(uuid4()),
            "user_id": str(uuid4()),
            "title": "Daily Standup",
            "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1",
            "next_occurrence": datetime.now().isoformat(),
            "created_at": datetime.now().isoformat()
        }

        # Test the publish method
        result = await publisher.publish_recurring_task_created(task_data)

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'recurring-events'

    async def test_publish_recurring_task_instance_created_event(self, mock_dapr_client):
        """Test publishing of recurring task instance created events via Dapr pub/sub."""
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample data
        original_task_id = str(uuid4())
        new_instance_id = str(uuid4())
        user_id = str(uuid4())
        occurrence_date = datetime.now()

        # Test the publish method
        result = await publisher.publish_recurring_task_instance_created(
            original_task_id, new_instance_id, user_id, occurrence_date
        )

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'recurring-events'

    async def test_publish_reminder_scheduled_event(self, mock_dapr_client):
        """Test publishing of reminder scheduled events via Dapr pub/sub."""
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample data
        task_id = str(uuid4())
        user_id = str(uuid4())
        scheduled_time = datetime.now()

        # Test the publish method
        result = await publisher.publish_reminder_scheduled(
            task_id, user_id, scheduled_time
        )

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'reminder-events'

    async def test_publish_reminder_triggered_event(self, mock_dapr_client):
        """Test publishing of reminder triggered events via Dapr pub/sub."""
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        publisher = EventPublisher()
        publisher.dapr_client = mock_client_instance  # Inject mocked client

        # Create sample data
        task_id = str(uuid4())
        user_id = str(uuid4())

        # Test the publish method
        result = await publisher.publish_reminder_triggered(
            task_id, user_id
        )

        # Verify that the method called Dapr's publish_event
        assert result is True  # Assuming successful mock
        mock_client_instance.publish_event.assert_called_once()
        args, kwargs = mock_client_instance.publish_event.call_args
        assert kwargs['pubsub_name'] == 'todo-pubsub'
        assert kwargs['topic_name'] == 'reminder-events'

    @pytest.mark.integration
    async def test_full_event_flow_via_api(self, test_client, mock_dapr_client):
        """Integration test for full event flow through API endpoints."""
        # This would test the actual API endpoints that trigger event publishing
        # Mock the Dapr client to avoid needing an actual Dapr sidecar
        mock_client_instance = Mock()
        mock_dapr_client.return_value = mock_client_instance

        # Create a new todo through the API
        response = test_client.post("/todos/", json={
            "title": "Test Task with Event",
            "description": "Task for event testing",
            "priority": "HIGH",
            "tags": ["test", "event"],
            "due_date": "2024-12-31T23:59:59",
            "remind_at": "2024-12-30T09:00:00",
            "recurrence_rule": "RRULE:FREQ=DAILY;INTERVAL=1"
        })

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == "Test Task with Event"
        assert response_data["priority"] == "HIGH"

        # Verify that an event was published
        assert mock_client_instance.publish_event.called
        # Additional assertions would depend on exact implementation details


if __name__ == "__main__":
    pytest.main([__file__])