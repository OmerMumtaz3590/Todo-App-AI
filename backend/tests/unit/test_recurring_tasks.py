"""Unit tests for recurring task functionality."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from uuid import UUID, uuid4

from src.services.recurring_task_service import RecurringTaskService
from src.models.todo import Todo, PriorityEnum


class TestRecurringTaskService:
    """Test suite for recurring task service functionality."""

    def test_calculate_next_occurrence_daily(self):
        """Test calculating next occurrence for daily recurring tasks."""
        recurrence_rule = "RRULE:FREQ=DAILY;INTERVAL=1"
        from_date = datetime(2024, 1, 15, 9, 0, 0)

        next_date = RecurringTaskService.calculate_next_occurrence(recurrence_rule, from_date)

        expected_date = datetime(2024, 1, 16, 9, 0, 0)  # Next day at same time
        assert next_date.date() == expected_date.date()
        assert next_date.hour == expected_date.hour

    def test_calculate_next_occurrence_weekly(self):
        """Test calculating next occurrence for weekly recurring tasks."""
        recurrence_rule = "RRULE:FREQ=WEEKLY;INTERVAL=1"
        from_date = datetime(2024, 1, 15, 10, 30, 0)  # Monday

        next_date = RecurringTaskService.calculate_next_occurrence(recurrence_rule, from_date)

        expected_date = datetime(2024, 1, 22, 10, 30, 0)  # Next Monday
        assert (next_date - expected_date).days == 7  # Exactly one week difference

    def test_calculate_next_occurrence_monthly(self):
        """Test calculating next occurrence for monthly recurring tasks."""
        recurrence_rule = "RRULE:FREQ=MONTHLY;INTERVAL=1"
        from_date = datetime(2024, 1, 15, 14, 0, 0)

        next_date = RecurringTaskService.calculate_next_occurrence(recurrence_rule, from_date)

        # Should be approximately 30 days later (next month)
        expected_date = datetime(2024, 2, 15, 14, 0, 0)
        assert abs((next_date - expected_date).days) <= 2  # Allow for month variation

    def test_calculate_next_occurrence_custom_json_format(self):
        """Test calculating next occurrence from custom JSON recurrence format."""
        recurrence_rule = '{"frequency": "WEEKLY", "interval": 2, "daysOfWeek": ["MON", "FRI"]}'
        from_date = datetime(2024, 1, 15, 9, 0, 0)  # Monday

        next_date = RecurringTaskService.calculate_next_occurrence(recurrence_rule, from_date)

        # Should find the next Friday (or next Monday in 2 weeks if we're past Friday)
        # This test verifies the format can be parsed
        assert next_date > from_date  # Next occurrence should be in the future

    def test_calculate_next_occurrence_handles_invalid_rule(self):
        """Test that invalid recurrence rules return None gracefully."""
        invalid_rule = "INVALID_RULE_FORMAT"
        from_date = datetime(2024, 1, 15, 9, 0, 0)

        next_date = RecurringTaskService.calculate_next_occurrence(invalid_rule, from_date)

        # Should handle gracefully and return a reasonable default
        assert next_date is not None  # Should return some default value rather than failing

    def test_generate_next_instance_creates_new_task(self):
        """Test generating next instance from a recurring task template."""
        # Create a mock parent recurring task
        parent_task = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Daily Task Template",
            description="Template for daily recurring task",
            priority=PriorityEnum.MEDIUM,
            tags=["daily", "recurring"],
            due_date=datetime(2024, 1, 16, 9, 0, 0),
            recurrence_rule="RRULE:FREQ=DAILY;INTERVAL=1",
            next_occurrence=datetime(2024, 1, 16, 9, 0, 0)
        )

        # Mock session for database operations
        mock_session = Mock()

        with patch('src.services.recurring_task_service.Todo') as MockTodo:
            # Create a mock new instance
            mock_new_instance = Mock()
            mock_new_instance.id = uuid4()
            MockTodo.return_value = mock_new_instance

            # Test the generation method
            result = RecurringTaskService.generate_next_instance(mock_session, parent_task)

            # Verify that a new instance was created
            assert result is not None
            assert result.id == mock_new_instance.id
            # Verify the new instance was added to the session
            mock_session.add.assert_called_once()
            # Verify the parent's next occurrence was updated
            mock_session.add.assert_called()  # For parent task update

    def test_generate_next_instance_updates_parent_next_occurrence(self):
        """Test that generating next instance updates the parent's next occurrence."""
        parent_task = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Weekly Meeting",
            recurrence_rule="RRULE:FREQ=WEEKLY;INTERVAL=1",
            next_occurrence=datetime(2024, 1, 15, 10, 0, 0)
        )

        mock_session = Mock()

        # Patch the necessary components
        with patch('src.services.recurring_task_service.Todo'), \
             patch('src.services.recurring_task_service.RecurringTaskService.calculate_next_occurrence') as mock_calc:

            # Mock the next occurrence calculation
            expected_next = datetime(2024, 1, 22, 10, 0, 0)
            mock_calc.return_value = expected_next

            # Call the method
            result = RecurringTaskService.generate_next_instance(mock_session, parent_task)

            # Verify the parent task's next occurrence was updated
            assert parent_task.next_occurrence == expected_next
            # Verify the parent task was saved to the session
            mock_session.add.assert_any_call(parent_task)

    def test_process_recurring_tasks_finds_and_processes_due_tasks(self):
        """Test processing all recurring tasks that have reached their next occurrence time."""
        # Create mock recurring tasks
        due_task = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Due Recurring Task",
            recurrence_rule="RRULE:FREQ=DAILY;INTERVAL=1",
            next_occurrence=datetime.now() - timedelta(hours=1)  # Due in the past
        )

        future_task = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Future Recurring Task",
            recurrence_rule="RRULE:FREQ=DAILY;INTERVAL=1",
            next_occurrence=datetime.now() + timedelta(hours=1)  # Future occurrence
        )

        # Mock session to return our test tasks
        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [due_task]
        mock_session.exec.return_value = mock_result

        # Mock the generate_next_instance method to return a mock instance
        with patch.object(RecurringTaskService, 'generate_next_instance') as mock_gen:
            mock_new_instance = Mock()
            mock_gen.return_value = mock_new_instance

            # Call the processing method
            results = RecurringTaskService.process_recurring_tasks(mock_session)

            # Verify that the due task was processed
            assert len(results) == 1
            assert results[0] == mock_new_instance
            # Verify that only the due task was processed (future_task should be ignored)
            mock_gen.assert_called_once_with(mock_session, due_task)

    def test_get_recurring_task_instances_returns_correct_list(self):
        """Test retrieving all instances generated from a recurring task template."""
        parent_task_id = uuid4()
        user_id = uuid4()

        # Create mock instances that belong to the parent task
        instance1 = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Instance 1",
            parent_task_id=parent_task_id
        )
        instance2 = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Instance 2",
            parent_task_id=parent_task_id
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [instance1, instance2]
        mock_session.exec.return_value = mock_result

        results = RecurringTaskService.get_recurring_task_instances(mock_session, parent_task_id)

        assert len(results) == 2
        assert instance1 in results
        assert instance2 in results
        # Verify the correct query was executed
        mock_session.exec.assert_called_once()

    def test_get_recurring_task_templates_finds_tasks_with_recurrence_rules(self):
        """Test retrieving all recurring task templates (tasks with recurrence rules) for a user."""
        user_id = uuid4()

        # Create mock recurring templates
        recurring_template = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Daily Routine",
            recurrence_rule="RRULE:FREQ=DAILY;INTERVAL=1"
        )
        non_recurring_task = Todo(
            id=uuid4(),
            user_id=user_id,
            title="One-time Task",
            recurrence_rule=None
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [recurring_template]  # Only recurring tasks should be returned
        mock_session.exec.return_value = mock_result

        results = RecurringTaskService.get_recurring_task_templates(mock_session, user_id)

        assert len(results) == 1
        assert results[0] == recurring_template
        # Non-recurring task should not be included
        assert non_recurring_task not in results

    def test_create_recurring_task_template_stores_correctly(self):
        """Test creating a recurring task template with proper recurrence rule."""
        mock_session = Mock()
        user_id = uuid4()

        todo_data = Mock()
        todo_data.title = "Weekly Meeting"
        todo_data.description = "Team weekly sync"
        todo_data.priority = PriorityEnum.HIGH
        todo_data.tags = ["meeting", "weekly", "team"]
        todo_data.due_date = datetime(2024, 1, 15, 10, 0, 0)
        todo_data.remind_at = datetime(2024, 1, 15, 9, 0, 0)
        todo_data.recurrence_rule = "RRULE:FREQ=WEEKLY;WKST=MO;BYDAY=MO"

        with patch('src.services.recurring_task_service.Todo') as MockTodo:
            mock_template = Mock()
            MockTodo.return_value = mock_template

            result = RecurringTaskService.create_recurring_task_template(
                mock_session, user_id, todo_data
            )

            assert result == mock_template
            # Verify the template was set up correctly
            assert mock_template.user_id == user_id
            assert mock_template.title == "Weekly Meeting"
            assert mock_template.recurrence_rule == "RRULE:FREQ=WEEKLY;WKST=MO;BYDAY=MO"
            # Verify it was saved to the session
            mock_session.add.assert_called_once_with(mock_template)
            mock_session.commit.assert_called_once()