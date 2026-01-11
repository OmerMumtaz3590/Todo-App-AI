"""Custom exceptions for the Todo application.

This module defines application-specific exceptions for error handling.

Spec Reference: FR-009 (validate input, display error messages)
Plan Reference: DD-003 (Error Handling Strategy)
"""


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID does not exist."""

    pass


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass
