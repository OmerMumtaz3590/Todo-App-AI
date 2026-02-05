"""Dapr client utilities for the event-driven architecture."""
from typing import Dict, Any, Optional, List
import json
from datetime import datetime
from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateOptions
from dapr.ext.fastapi import DaprApp
from fastapi import FastAPI


class DaprService:
    """Utility class for interacting with Dapr building blocks."""

    def __init__(self, app: Optional[FastAPI] = None):
        """
        Initialize the Dapr service.

        Args:
            app: FastAPI app instance (optional, for Dapr ext)
        """
        self.client = None
        self.dapr_app = None

        if app:
            self.dapr_app = DaprApp(app)

    def get_client(self) -> DaprClient:
        """Get a Dapr client instance, creating one if needed."""
        if not self.client:
            self.client = DaprClient()
        return self.client

    # Dapr State Management Methods
    def save_state(self, store_name: str, key: str, value: Any, etag: Optional[str] = None) -> bool:
        """
        Save state using Dapr state management.

        Args:
            store_name: Name of the state store (e.g., 'todo-statestore')
            key: State key
            value: Value to store
            etag: Optional etag for concurrency control

        Returns:
            True if successful, False otherwise
        """
        try:
            client = self.get_client()

            # Convert value to JSON string for storage
            data = json.dumps(value) if not isinstance(value, str) else value

            # Create a state item with options
            options = StateOptions(concurrency='first-write')

            client.save_state(
                store_name=store_name,
                key=key,
                value=data,
                etag=etag,
                options=options.__dict__ if etag else None
            )
            return True
        except Exception as e:
            print(f"Error saving state: {str(e)}")
            return False

    def get_state(self, store_name: str, key: str) -> Optional[Any]:
        """
        Get state using Dapr state management.

        Args:
            store_name: Name of the state store
            key: State key

        Returns:
            Retrieved value or None if not found
        """
        try:
            client = self.get_client()
            response = client.get_state(store_name, key)

            if response.data:
                # Attempt to deserialize as JSON, fallback to string
                try:
                    return json.loads(response.data.decode('utf-8'))
                except json.JSONDecodeError:
                    return response.data.decode('utf-8')
            return None
        except Exception as e:
            print(f"Error getting state: {str(e)}")
            return None

    def delete_state(self, store_name: str, key: str, etag: Optional[str] = None) -> bool:
        """
        Delete state using Dapr state management.

        Args:
            store_name: Name of the state store
            key: State key
            etag: Optional etag for concurrency control

        Returns:
            True if successful, False otherwise
        """
        try:
            client = self.get_client()
            client.delete_state(store_name, key, etag=etag)
            return True
        except Exception as e:
            print(f"Error deleting state: {str(e)}")
            return False

    # Dapr Secret Management Methods
    def get_secret(self, store_name: str, key: str, metadata: Optional[Dict[str, str]] = None) -> Optional[str]:
        """
        Get secret using Dapr secret management.

        Args:
            store_name: Name of the secret store (e.g., 'todo-secretstore')
            key: Secret key
            metadata: Optional metadata for the secret request

        Returns:
            Secret value or None if not found
        """
        try:
            client = self.get_client()
            response = client.get_secret(store_name, key, metadata)
            return response.data.get(key) if response.data and key in response.data else None
        except Exception as e:
            print(f"Error getting secret: {str(e)}")
            return None

    def bulk_get_secret(self, store_name: str, metadata: Optional[Dict[str, str]] = None) -> Optional[Dict[str, str]]:
        """
        Get multiple secrets using Dapr secret management.

        Args:
            store_name: Name of the secret store
            metadata: Optional metadata for the secret request

        Returns:
            Dictionary of secret key-value pairs or None if error
        """
        try:
            client = self.get_client()
            response = client.get_bulk_secret(store_name, metadata)
            return dict(response.data) if response.data else {}
        except Exception as e:
            print(f"Error getting bulk secrets: {str(e)}")
            return None

    # Dapr Service Invocation Methods
    def invoke_method(self, app_id: str, method_name: str, data: Optional[Any] = None, http_verb: str = "POST",
                           http_querystring: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """
        Invoke method on another service using Dapr service invocation.

        Args:
            app_id: Target service ID
            method_name: Method name to invoke
            data: Optional data to send
            http_verb: HTTP verb (default: POST)
            http_querystring: Optional query parameters

        Returns:
            Response from the target service or None if error
        """
        try:
            client = self.get_client()

            # Convert data to JSON if needed
            if data is not None and not isinstance(data, bytes):
                data = json.dumps(data).encode('utf-8')

            response = client.invoke_method(
                app_id=app_id,
                method_name=method_name,
                data=data,
                http_verb=http_verb,
                http_querystring=http_querystring
            )

            # Attempt to decode and parse response as JSON
            if response.data:
                try:
                    return json.loads(response.data.decode('utf-8'))
                except json.JSONDecodeError:
                    return response.data.decode('utf-8')
            return None
        except Exception as e:
            print(f"Error invoking method: {str(e)}")
            return None

    # Dapr Pub/Sub Methods
    def publish_event(self, pubsub_name: str, topic_name: str, data: Any) -> bool:
        """
        Publish an event using Dapr pub/sub.

        Args:
            pubsub_name: Name of the pub/sub component
            topic_name: Topic name to publish to
            data: Event data to publish

        Returns:
            True if successful, False otherwise
        """
        try:
            client = self.get_client()

            # Convert data to JSON string if needed
            if not isinstance(data, str):
                data = json.dumps(data)

            client.publish_event(
                pubsub_name=pubsub_name,
                topic_name=topic_name,
                data=data,
                data_content_type='application/json'
            )
            return True
        except Exception as e:
            print(f"Error publishing event: {str(e)}")
            return False

    # Helper methods for common patterns
    def save_temp_processing_state(self, key: str, processing_data: Dict[str, Any]) -> bool:
        """
        Save temporary processing state for event handling.

        Args:
            key: Unique key for the processing state
            processing_data: Data about the current processing state

        Returns:
            True if saved successfully, False otherwise
        """
        processing_data["updated_at"] = datetime.now().isoformat()
        return self.save_state("todo-statestore", f"processing:{key}", processing_data)

    def get_temp_processing_state(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get temporary processing state for event handling.

        Args:
            key: Unique key for the processing state

        Returns:
            Processing state data or None if not found
        """
        return self.get_state("todo-statestore", f"processing:{key}")

    def cleanup_processing_state(self, key: str) -> bool:
        """
        Clean up temporary processing state after processing is complete.

        Args:
            key: Unique key for the processing state

        Returns:
            True if cleaned up successfully, False otherwise
        """
        return self.delete_state("todo-statestore", f"processing:{key}")

    def close(self):
        """Close the Dapr client connection."""
        if self.client:
            self.client.close()
            self.client = None