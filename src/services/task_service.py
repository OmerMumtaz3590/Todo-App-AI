"""Task service for managing todo tasks in memory.

Spec Reference: FR-001 through FR-011
Plan Reference: services/task_service.py, DD-001, DD-002
"""

from ..exceptions import TaskNotFoundError, ValidationError
from ..models import Task


class TaskService:
    """Service for managing todo tasks in memory.

    This service provides CRUD operations for tasks stored in an in-memory
    dictionary. Task IDs are auto-generated and never reused.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self) -> None:
        """Initialize the task service with empty storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate a unique task ID (never reused).

        Returns:
            A unique integer ID for a new task
        """
        task_id = self._next_id
        self._next_id += 1
        return task_id

    def add_task(self, title: str) -> Task:
        """Add a new task with the given title.

        Args:
            title: The task description (must be non-empty)

        Returns:
            The newly created Task

        Raises:
            ValidationError: If title is empty or whitespace-only

        Spec Reference: FR-001 (add tasks), US1-AC2, US1-AC3
        """
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        task_id = self._generate_id()
        task = Task(id=task_id, title=title.strip())
        self._tasks[task_id] = task
        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks (may be empty)

        Spec Reference: FR-003 (view all tasks)
        """
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Task:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task with the given ID

        Raises:
            TaskNotFoundError: If no task with the given ID exists

        Spec Reference: US3-AC3, US4-AC2, US5-AC2
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return self._tasks[task_id]

    def update_task(self, task_id: int, title: str) -> Task:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update
            title: The new title (must be non-empty)

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If no task with the given ID exists
            ValidationError: If title is empty or whitespace-only

        Spec Reference: FR-004, US4-AC1, US4-AC2, US4-AC3
        """
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty")

        task = self.get_task(task_id)  # Raises TaskNotFoundError if not found
        task.title = title.strip()
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Raises:
            TaskNotFoundError: If no task with the given ID exists

        Spec Reference: FR-005, US5-AC1, US5-AC2, US5-AC3
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        del self._tasks[task_id]

    def mark_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If no task with the given ID exists

        Spec Reference: FR-006, US3-AC1
        """
        task = self.get_task(task_id)
        task.is_complete = True
        return task

    def mark_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If no task with the given ID exists

        Spec Reference: FR-007, US3-AC2
        """
        task = self.get_task(task_id)
        task.is_complete = False
        return task
