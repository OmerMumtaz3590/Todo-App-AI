"""Unit tests for reminder service functionality."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from uuid import UUID, uuid4

from src.services.reminder_service import ReminderService
from src.models.todo import Todo, PriorityEnum


class TestReminderService:
    """Test suite for reminder service functionality."""

    def test_schedule_reminder_for_task_with_remind_at(self):
        """Test scheduling a reminder for a task with remind_at set."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Task",
            remind_at=datetime(2024, 1, 15, 9, 0, 0)
        )

        result = ReminderService.schedule_reminder(todo)

        # Should return the remind_at datetime
        assert result == todo.remind_at

    def test_schedule_reminder_returns_none_for_task_without_remind_at(self):
        """Test that scheduling reminder returns None if no remind_at is set."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Task"
            # No remind_at field
        )

        result = ReminderService.schedule_reminder(todo)

        # Should return None since no reminder time is set
        assert result is None

    def test_get_upcoming_reminders_within_timeframe(self):
        """Test getting upcoming reminders within a specified timeframe."""
        user_id = uuid4()

        # Create mock upcoming reminder
        upcoming_reminder = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Upcoming Task",
            remind_at=datetime.now() + timedelta(minutes=30),  # 30 minutes from now
            is_completed=False
        )

        # Create mock future reminder (outside 60-minute window)
        future_reminder = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Future Task",
            remind_at=datetime.now() + timedelta(hours=2),  # 2 hours from now
            is_completed=False
        )

        # Create mock past reminder (should be excluded)
        past_reminder = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Past Task",
            remind_at=datetime.now() - timedelta(minutes=10),  # 10 minutes ago
            is_completed=False
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [upcoming_reminder]
        mock_session.exec.return_value = mock_result

        results = ReminderService.get_upcoming_reminders(mock_session, user_id, within_minutes=60)

        # Should return only the upcoming reminder within the 60-minute window
        assert len(results) == 1
        assert results[0] == upcoming_reminder

    def test_get_upcoming_reminders_excludes_completed_tasks(self):
        """Test that get_upcoming_reminders excludes completed tasks."""
        user_id = uuid4()

        # Create upcoming reminder that's completed (should be excluded)
        completed_reminder = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Completed Task",
            remind_at=datetime.now() + timedelta(minutes=15),
            is_completed=True  # Task is completed
        )

        # Create upcoming reminder that's not completed (should be included)
        active_reminder = Todo(
            id=uuid4(),
            user_id=user_id,
            title="Active Task",
            remind_at=datetime.now() + timedelta(minutes=30),
            is_completed=False  # Task is not completed
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [active_reminder]
        mock_session.exec.return_value = mock_result

        results = ReminderService.get_upcoming_reminders(mock_session, user_id, within_minutes=60)

        # Should return only the active reminder
        assert len(results) == 1
        assert results[0] == active_reminder
        assert completed_reminder not in results

    def test_get_pending_reminders_finds_overdue_uncompleted_tasks(self):
        """Test getting pending reminders that are overdue and not completed."""
        # Create mock overdue reminder
        overdue_reminder = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Overdue Task",
            remind_at=datetime.now() - timedelta(minutes=30),  # 30 minutes ago
            is_completed=False  # Not completed
        )

        # Create mock overdue completed task (should be excluded)
        overdue_completed = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Overdue Completed Task",
            remind_at=datetime.now() - timedelta(minutes=30),  # 30 minutes ago
            is_completed=True  # Already completed
        )

        # Create mock future reminder (should be excluded)
        future_reminder = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Future Task",
            remind_at=datetime.now() + timedelta(minutes=30),  # 30 minutes in future
            is_completed=False
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [overdue_reminder]
        mock_session.exec.return_value = mock_result

        results = ReminderService.get_pending_reminders(mock_session)

        # Should return only the overdue uncompleted reminder
        assert len(results) == 1
        assert results[0] == overdue_reminder
        assert overdue_completed not in results
        assert future_reminder not in results

    def test_trigger_reminder_success(self):
        """Test successfully triggering a reminder for a task."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Test Task",
            remind_at=datetime.now(),
            is_completed=False
        )

        result = ReminderService.trigger_reminder(todo)

        # Should return True for successful trigger
        assert result is True

    def test_trigger_reminder_fails_for_completed_tasks(self):
        """Test that triggering reminder fails for completed tasks."""
        completed_todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Completed Task",
            remind_at=datetime.now(),
            is_completed=True  # Already completed
        )

        result = ReminderService.trigger_reminder(completed_todo)

        # Should return False since task is already completed
        assert result is False

    def test_trigger_reminder_fails_for_tasks_without_remind_at(self):
        """Test that triggering reminder fails for tasks without remind_at."""
        incomplete_todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Incomplete Task"
            # No remind_at field
        )

        result = ReminderService.trigger_reminder(incomplete_todo)

        # Should return False since no reminder is scheduled
        assert result is False

    @pytest.mark.asyncio
    async def test_process_reminders_async_finds_and_triggers_due_reminders(self):
        """Test processing all due reminders asynchronously."""
        # Create mock due reminder
        due_reminder = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Due Reminder",
            remind_at=datetime.now() - timedelta(seconds=1),  # Just due
            is_completed=False
        )

        # Create mock future reminder (should be excluded)
        future_reminder = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Future Reminder",
            remind_at=datetime.now() + timedelta(hours=1),
            is_completed=False
        )

        # Create mock completed reminder (should be excluded)
        completed_reminder = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Completed Reminder",
            remind_at=datetime.now() - timedelta(minutes=10),
            is_completed=True  # Already completed
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [due_reminder]
        mock_session.exec.return_value = mock_result

        # Mock the trigger_reminder method to return success
        with patch.object(ReminderService, 'trigger_reminder', return_value=True):
            results = await ReminderService.process_reminders_async(mock_session)

            # Should return only the due reminder that was triggered
            assert len(results) == 1
            assert results[0] == due_reminder

    @pytest.mark.asyncio
    async def test_process_reminders_async_only_triggers_successfully_handled_reminders(self):
        """Test that only successfully triggered reminders are returned."""
        # Create mock due reminder
        due_reminder = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Due Reminder",
            remind_at=datetime.now() - timedelta(seconds=1),
            is_completed=False
        )

        mock_session = Mock()
        mock_result = Mock()
        mock_result.all.return_value = [due_reminder]
        mock_session.exec.return_value = mock_result

        # Mock trigger_reminder to return False (failure)
        with patch.object(ReminderService, 'trigger_reminder', return_value=False):
            results = await ReminderService.process_reminders_async(mock_session)

            # Should return empty list since trigger failed
            assert len(results) == 0

    def test_cancel_reminder_clears_remind_at_field(self):
        """Test canceling a reminder clears the remind_at field."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Task with Reminder",
            remind_at=datetime.now()
        )

        original_remind_at = todo.remind_at
        assert original_remind_at is not None

        result = ReminderService.cancel_reminder(todo)

        # Should return True for successful cancellation
        assert result is True
        # Should clear the remind_at field
        assert todo.remind_at is None

    def test_cancel_reminder_fails_for_tasks_without_reminder(self):
        """Test that canceling reminder fails for tasks without a reminder."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Task without Reminder"
            # No remind_at field
        )

        result = ReminderService.cancel_reminder(todo)

        # Should return False since there was no reminder to cancel
        assert result is False

    def test_update_reminder_time_changes_remind_at_field(self):
        """Test updating reminder time changes the remind_at field."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Task with Reminder",
            remind_at=datetime.now() - timedelta(days=1)  # Past time
        )

        new_reminder_time = datetime.now() + timedelta(hours=2)  # 2 hours in future

        result = ReminderService.update_reminder_time(todo, new_reminder_time)

        # Should return True for successful update
        assert result is True
        # Should update the remind_at field
        assert todo.remind_at == new_reminder_time

    def test_update_reminder_time_fails_for_past_times(self):
        """Test that updating reminder time fails if new time is in the past."""
        todo = Todo(
            id=uuid4(),
            user_id=uuid4(),
            title="Task with Reminder",
            remind_at=datetime.now() + timedelta(hours=1)  # Future time
        )

        past_time = datetime.now() - timedelta(hours=1)  # 1 hour ago

        result = ReminderService.update_reminder_time(todo, past_time)

        # Should return False since new time is in the past
        assert result is False
        # Should not change the original remind_at time
        assert todo.remind_at > datetime.now()  # Still in future