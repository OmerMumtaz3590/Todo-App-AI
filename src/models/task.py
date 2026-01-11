"""Task data model.

Spec Reference: Key Entities -> Task (id: int, title: str, is_complete: bool)
Plan Reference: DD-004 (Task Model Implementation), models/task.py
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique identifier for the task (positive integer)
        title: Description of the task (non-empty string)
        is_complete: Whether the task is marked as done (default: False)
    """

    id: int
    title: str
    is_complete: bool = False
