"""Integration tests for Dapr component integration."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from dapr.clients import DaprClient
from src.dapr_integration.client import DaprService


class TestDaprIntegration:
    """Tests for Dapr service integration."""

    @pytest.fixture
    def dapr_service(self):
        """Create a DaprService instance for testing."""
        return DaprService()

    @pytest.fixture
    def mock_dapr_client(self):
        """Mock Dapr client for testing."""
        with patch('src.dapr_integration.client.DaprClient') as mock:
            yield mock

    def test_dapr_service_initialization(self):
        """Test DaprService can be initialized properly."""
        service = DaprService()
        assert service is not None
        assert service.client is None  # Client should be created on demand

    def test_get_dapr_client(self, mock_dapr_client):
        """Test retrieving Dapr client from DaprService."""
        service = DaprService()

        # Mock the client creation
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        client = service.get_client()

        assert client is not None
        assert service.client is mock_client  # Client should be cached

    def test_save_state_via_dapr(self, mock_dapr_client):
        """Test saving state using Dapr state management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client
        service.client = mock_client  # Inject mocked client

        store_name = "todo-statestore"
        key = "test-key"
        value = {"test": "data", "status": "success"}

        result = service.save_state(store_name, key, value)

        assert result is True  # Assuming successful mock
        mock_client.save_state.assert_called_once_with(
            store_name=store_name,
            key=key,
            value=json.dumps(value),
            etag=None,
            options=ANY  # Using ANY matcher for options parameter
        )

    def test_get_state_via_dapr(self, mock_dapr_client):
        """Test retrieving state using Dapr state management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        # Mock the response
        mock_response = Mock()
        mock_response.data = json.dumps({"retrieved": "data"}).encode('utf-8')
        mock_client.get_state.return_value = mock_response

        service.client = mock_client  # Inject mocked client

        store_name = "todo-statestore"
        key = "test-key"

        result = service.get_state(store_name, key)

        assert result == {"retrieved": "data"}
        mock_client.get_state.assert_called_once_with(store_name, key)

    def test_get_state_returns_none_if_no_data(self, mock_dapr_client):
        """Test that get_state returns None when no data is found."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        # Mock response with no data
        mock_response = Mock()
        mock_response.data = None
        mock_client.get_state.return_value = mock_response

        service.client = mock_client  # Inject mocked client

        result = service.get_state("todo-statestore", "nonexistent-key")
        assert result is None

    def test_delete_state_via_dapr(self, mock_dapr_client):
        """Test deleting state using Dapr state management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client
        service.client = mock_client  # Inject mocked client

        store_name = "todo-statestore"
        key = "test-key"

        result = service.delete_state(store_name, key)

        assert result is True  # Assuming successful mock
        mock_client.delete_state.assert_called_once_with(store_name, key, etag=None)

    def test_get_secret_via_dapr(self, mock_dapr_client):
        """Test retrieving secrets using Dapr secret management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        # Mock the response
        mock_response = Mock()
        mock_response.data = {"secret-key": "secret-value"}
        mock_client.get_secret.return_value = mock_response

        service.client = mock_client  # Inject mocked client

        store_name = "todo-secretstore"
        key = "secret-key"

        result = service.get_secret(store_name, key)

        assert result == "secret-value"
        mock_client.get_secret.assert_called_once_with(store_name, key, None)

    def test_get_nonexistent_secret_returns_none(self, mock_dapr_client):
        """Test that get_secret returns None when secret doesn't exist."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        # Mock response with empty data
        mock_response = Mock()
        mock_response.data = {}  # Empty dictionary when secret not found
        mock_client.get_secret.return_value = mock_response

        service.client = mock_client

        result = service.get_secret("todo-secretstore", "nonexistent-key")
        assert result is None

    def test_invoke_method_via_dapr(self, mock_dapr_client):
        """Test service invocation using Dapr service invocation."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        # Mock the response
        mock_response = Mock()
        mock_response.data = json.dumps({"result": "success"}).encode('utf-8')
        mock_client.invoke_method.return_value = mock_response

        service.client = mock_client  # Inject mocked client

        app_id = "test-app"
        method_name = "test-method"
        data = {"test": "data"}

        result = service.invoke_method(app_id, method_name, data)

        assert result == {"result": "success"}
        mock_client.invoke_method.assert_called_once()
        args, kwargs = mock_client.invoke_method.call_args
        assert kwargs['app_id'] == app_id
        assert kwargs['method_name'] == method_name
        assert kwargs['http_verb'] == "POST"

    def test_publish_event_via_dapr(self, mock_dapr_client):
        """Test publishing events using Dapr pub/sub."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client
        service.client = mock_client  # Inject mocked client

        pubsub_name = "todo-pubsub"
        topic_name = "task-events"
        data = {"event": "test-data", "type": "test-event"}

        result = service.publish_event(pubsub_name, topic_name, data)

        assert result is True  # Assuming successful mock
        mock_client.publish_event.assert_called_once_with(
            pubsub_name=pubsub_name,
            topic_name=topic_name,
            data=json.dumps(data),
            data_content_type='application/json'
        )

    def test_publish_event_with_string_data(self, mock_dapr_client):
        """Test publishing events with string data using Dapr pub/sub."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client
        service.client = mock_client

        pubsub_name = "todo-pubsub"
        topic_name = "reminder-events"
        data = '{"event_type": "reminder_triggered", "task_id": "test-123"}'

        result = service.publish_event(pubsub_name, topic_name, data)

        assert result is True  # Assuming successful mock
        mock_client.publish_event.assert_called_once_with(
            pubsub_name=pubsub_name,
            topic_name=topic_name,
            data=data,  # String data should be passed as-is
            data_content_type='application/json'
        )

    @pytest.mark.asyncio
    async def test_save_temp_processing_state(self, mock_dapr_client):
        """Test saving temporary processing state using Dapr state management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client
        service.client = mock_client

        key = "test-processing-key"
        processing_data = {"step": "validation", "status": "in-progress"}

        result = service.save_temp_processing_state(key, processing_data)

        assert result is True  # Assuming successful mock
        # Verify the call was made to save state with the correct key format
        mock_client.save_state.assert_called_once()
        args, kwargs = mock_client.save_state.call_args
        assert kwargs['key'] == f"processing:{key}"
        assert kwargs['store_name'] == "todo-statestore"

    @pytest.mark.asyncio
    async def test_get_temp_processing_state(self, mock_dapr_client):
        """Test retrieving temporary processing state using Dapr state management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client

        # Mock response
        mock_response = Mock()
        mock_response.data = json.dumps({"step": "validation", "status": "complete"}).encode('utf-8')
        mock_client.get_state.return_value = mock_response

        service.client = mock_client

        key = "test-processing-key"

        result = service.get_temp_processing_state(key)

        assert result == {"step": "validation", "status": "complete"}
        # Verify the call was made with the correct key format
        mock_client.get_state.assert_called_once_with("todo-statestore", f"processing:{key}")

    @pytest.mark.asyncio
    async def test_cleanup_processing_state(self, mock_dapr_client):
        """Test cleaning up temporary processing state using Dapr state management."""
        service = DaprService()
        mock_client = Mock()
        mock_dapr_client.return_value = mock_client
        service.client = mock_client

        key = "test-processing-key"

        result = service.cleanup_processing_state(key)

        assert result is True  # Assuming successful mock
        # Verify the call was made with the correct key format
        mock_client.delete_state.assert_called_once_with("todo-statestore", f"processing:{key}")


if __name__ == "__main__":
    pytest.main([__file__])