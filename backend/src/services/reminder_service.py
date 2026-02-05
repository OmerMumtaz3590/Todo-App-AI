"""Reminder business logic service."""
from datetime import datetime, timedelta
from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo
import asyncio


class ReminderService:
    """Service for managing reminder operations."""

    @staticmethod
    def schedule_reminder(todo: Todo) -> Optional[datetime]:
        """
        Schedule a reminder based on the todo's remind_at field.

        Args:
            todo: The todo item with reminder information

        Returns:
            Scheduled reminder datetime, or None if no reminder scheduled
        """
        if not todo.remind_at:
            return None

        # The actual scheduling would be handled by Dapr Jobs API or cron bindings
        # This is a placeholder for the logic
        return todo.remind_at

    @staticmethod
    def get_upcoming_reminders(session: Session, user_id: UUID, within_minutes: int = 60) -> List[Todo]:
        """
        Get all upcoming reminders for a user within the specified timeframe.

        Args:
            session: Database session
            user_id: UUID of the user
            within_minutes: Look ahead timeframe in minutes (default 60 minutes)

        Returns:
            List of todos with reminders scheduled within the timeframe
        """
        look_ahead_time = datetime.now() + timedelta(minutes=within_minutes)

        statement = select(Todo).where(
            Todo.user_id == user_id,
            Todo.remind_at.is_not(None),
            Todo.remind_at <= look_ahead_time,
            Todo.remind_at >= datetime.now(),
            Todo.is_completed == False
        ).order_by(Todo.remind_at.asc())

        reminders = session.exec(statement).all()
        return list(reminders)

    @staticmethod
    def get_pending_reminders(session: Session) -> List[Todo]:
        """
        Get all pending reminders that should have been triggered but weren't.

        Args:
            session: Database session

        Returns:
            List of todos with overdue reminders that haven't been completed
        """
        statement = select(Todo).where(
            Todo.remind_at.is_not(None),
            Todo.remind_at < datetime.now(),
            Todo.is_completed == False
        ).order_by(Todo.remind_at.desc())

        reminders = session.exec(statement).all()
        return list(reminders)

    @staticmethod
    def trigger_reminder(todo: Todo) -> bool:
        """
        Trigger a reminder for a specific todo item.

        Args:
            todo: The todo item to trigger a reminder for

        Returns:
            True if reminder was successfully triggered, False otherwise
        """
        # In a real implementation, this would send the reminder to the user
        # via the appropriate channel (push notification, email, etc.)
        # Here we're just simulating the action

        if not todo.remind_at or todo.is_completed:
            return False

        # This would typically integrate with a notification service
        # For now, we just log that the reminder should be sent
        print(f"Triggering reminder for todo '{todo.title}' (ID: {todo.id}) at {datetime.now()}")

        # The actual reminder triggering would be done via Dapr bindings
        # This is where we'd publish the reminder event via Dapr
        return True

    @staticmethod
    async def process_reminders_async(session: Session) -> List[Todo]:
        """
        Asynchronously process all reminders that are due.

        Args:
            session: Database session

        Returns:
            List of todos for which reminders were triggered
        """
        # Get all todos with reminders that are due or overdue
        statement = select(Todo).where(
            Todo.remind_at.is_not(None),
            Todo.remind_at <= datetime.now(),
            Todo.is_completed == False
        )
        due_reminders = session.exec(statement).all()

        triggered_reminders = []
        for todo in due_reminders:
            # Trigger the reminder
            success = ReminderService.trigger_reminder(todo)
            if success:
                triggered_reminders.append(todo)

        return triggered_reminders

    @staticmethod
    def cancel_reminder(todo: Todo) -> bool:
        """
        Cancel a scheduled reminder for a todo item.

        Args:
            todo: The todo item to cancel the reminder for

        Returns:
            True if reminder was successfully canceled, False otherwise
        """
        # In a real implementation, this would cancel the scheduled reminder
        # in the Dapr Jobs API or other scheduling system
        if not todo.remind_at:
            return False

        # Update the todo to clear the reminder
        todo.remind_at = None
        return True

    @staticmethod
    def update_reminder_time(todo: Todo, new_reminder_time: datetime) -> bool:
        """
        Update the reminder time for a todo item.

        Args:
            todo: The todo item to update the reminder for
            new_reminder_time: The new reminder time

        Returns:
            True if reminder time was successfully updated, False otherwise
        """
        if new_reminder_time <= datetime.now():
            return False  # Cannot set reminder in the past

        # Update the reminder time
        todo.remind_at = new_reminder_time
        return True