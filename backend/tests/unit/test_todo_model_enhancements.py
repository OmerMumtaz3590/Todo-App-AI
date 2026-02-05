"""Unit tests for enhanced Todo model with Phase V fields."""
import pytest
from datetime import datetime
from uuid import UUID
from src.models.todo import Todo, TodoCreate, TodoUpdate, PriorityEnum


class TestTodoModelEnhancements:
    """Test suite for Phase V Todo model enhancements."""

    def test_todo_model_has_priority_field(self):
        """Test that Todo model has priority field."""
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            priority=PriorityEnum.HIGH
        )
        assert todo.priority == PriorityEnum.HIGH
        assert todo.priority in [PriorityEnum.HIGH, PriorityEnum.MEDIUM, PriorityEnum.LOW]

    def test_todo_model_has_tags_field(self):
        """Test that Todo model has tags field."""
        tags = ["work", "urgent", "development"]
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            tags=tags
        )
        assert todo.tags == tags
        assert isinstance(todo.tags, list)

    def test_todo_model_has_due_date_field(self):
        """Test that Todo model has due_date field."""
        due_date = datetime(2024, 12, 31, 23, 59, 59)
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            due_date=due_date
        )
        assert todo.due_date == due_date

    def test_todo_model_has_remind_at_field(self):
        """Test that Todo model has remind_at field."""
        remind_at = datetime(2024, 12, 30, 9, 0, 0)
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            remind_at=remind_at
        )
        assert todo.remind_at == remind_at

    def test_todo_model_has_recurrence_rule_field(self):
        """Test that Todo model has recurrence_rule field."""
        recurrence_rule = "RRULE:FREQ=DAILY;INTERVAL=1"
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            recurrence_rule=recurrence_rule
        )
        assert todo.recurrence_rule == recurrence_rule

    def test_todo_model_has_next_occurrence_field(self):
        """Test that Todo model has next_occurrence field."""
        next_occurrence = datetime(2024, 12, 2, 9, 0, 0)
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            next_occurrence=next_occurrence
        )
        assert todo.next_occurrence == next_occurrence

    def test_todo_model_has_parent_task_id_field(self):
        """Test that Todo model has parent_task_id field."""
        parent_task_id = "some-parent-task-uuid"
        todo = Todo(
            user_id="test-user-id",
            title="Test Task",
            parent_task_id=parent_task_id
        )
        assert todo.parent_task_id == parent_task_id

    def test_todo_create_schema_has_new_fields(self):
        """Test that TodoCreate schema includes new Phase V fields."""
        todo_create = TodoCreate(
            title="Test Task",
            priority=PriorityEnum.MEDIUM,
            tags=["test", "feature"],
            due_date=datetime(2024, 12, 31),
            remind_at=datetime(2024, 12, 30, 9, 0, 0),
            recurrence_rule="RRULE:FREQ=WEEKLY;BYDAY=MO"
        )

        assert todo_create.priority == PriorityEnum.MEDIUM
        assert "test" in todo_create.tags
        assert todo_create.due_date.year == 2024
        assert todo_create.remind_at.hour == 9
        assert "FREQ=WEEKLY" in todo_create.recurrence_rule

    def test_todo_update_schema_has_new_fields(self):
        """Test that TodoUpdate schema includes new Phase V fields."""
        todo_update = TodoUpdate(
            priority=PriorityEnum.LOW,
            tags=["updated", "tag"],
            due_date=datetime(2025, 1, 15),
            remind_at=datetime(2025, 1, 14, 10, 0, 0),
            recurrence_rule="RRULE:FREQ=MONTHLY;INTERVAL=1",
            is_completed=True
        )

        assert todo_update.priority == PriorityEnum.LOW
        assert "updated" in todo_update.tags
        assert todo_update.due_date.month == 1
        assert todo_update.remind_at.hour == 10
        assert "FREQ=MONTHLY" in todo_update.recurrence_rule
        assert todo_update.is_completed is True

    def test_priority_enum_values(self):
        """Test that PriorityEnum has the correct values."""
        assert PriorityEnum.HIGH.value == "HIGH"
        assert PriorityEnum.MEDIUM.value == "MEDIUM"
        assert PriorityEnum.LOW.value == "LOW"

    def test_todo_defaults(self):
        """Test default values for new fields."""
        todo = Todo(
            user_id="test-user-id",
            title="Test Task"
        )

        # Default priority should be MEDIUM
        assert todo.priority == PriorityEnum.MEDIUM

        # Default tags should be empty list
        assert todo.tags == []

        # Optional fields should be None by default
        assert todo.due_date is None
        assert todo.remind_at is None
        assert todo.recurrence_rule is None
        assert todo.next_occurrence is None
        assert todo.parent_task_id is None


if __name__ == "__main__":
    pytest.main([__file__])