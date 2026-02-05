"""Recurring task business logic service."""
from datetime import datetime, timedelta
from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo, PriorityEnum
from .todo_service import TodoService
import json
from dateutil import rrule
from dateutil.parser import parse


class RecurringTaskService:
    """Service for managing recurring task operations."""

    @staticmethod
    def create_recurring_task_template(session: Session, user_id: UUID, todo_data) -> Todo:
        """
        Create a recurring task template (the pattern that will generate instances).

        Args:
            session: Database session
            user_id: UUID of the user
            todo_data: Todo creation data with recurrence rule

        Returns:
            Created recurring task template instance
        """
        # Create the recurring task template
        recurring_template = Todo(
            user_id=user_id,
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            tags=todo_data.tags if todo_data.tags else [],
            due_date=todo_data.due_date,
            remind_at=todo_data.remind_at,
            recurrence_rule=todo_data.recurrence_rule,
            next_occurrence=RecurringTaskService.calculate_next_occurrence(
                todo_data.recurrence_rule, datetime.now()
            ),
            parent_task_id=None  # This is the template itself, so no parent
        )
        session.add(recurring_template)
        session.commit()
        session.refresh(recurring_template)
        return recurring_template

    @staticmethod
    def calculate_next_occurrence(recurrence_rule: str, from_date: datetime = None) -> datetime:
        """
        Calculate the next occurrence based on the recurrence rule.

        Args:
            recurrence_rule: The recurrence rule in iCal format or custom JSON
            from_date: The date to calculate from (defaults to current time)

        Returns:
            Datetime of the next occurrence
        """
        if not from_date:
            from_date = datetime.now()

        # For simplicity, supporting basic recurrence patterns
        # In production, you'd want to use a more robust parser like rrule
        if not recurrence_rule:
            return None

        try:
            # If it's in iCal format (RFC 5545), parse it
            if recurrence_rule.startswith("RRULE:"):
                # Parse RRULE and get next occurrence
                # This is a simplified version - in practice you'd want more sophisticated parsing
                import re
                freq_match = re.search(r'FREQ=([^;]+)', recurrence_rule)
                if freq_match:
                    freq = freq_match.group(1)

                    # Map frequencies to timedelta increments
                    if freq == "DAILY":
                        return from_date + timedelta(days=1)
                    elif freq == "WEEKLY":
                        return from_date + timedelta(weeks=1)
                    elif freq == "MONTHLY":
                        # Simple approach - add approximately one month
                        return from_date + timedelta(days=30)
                    elif freq == "YEARLY":
                        return from_date + timedelta(days=365)

            # If it's a custom JSON format, parse it
            elif recurrence_rule.startswith('{'):
                rule_data = json.loads(recurrence_rule)
                # Process custom recurrence rule based on the format
                # This is a simplified approach
                frequency = rule_data.get('frequency', 'DAILY')
                interval = rule_data.get('interval', 1)

                if frequency == 'DAILY':
                    return from_date + timedelta(days=interval)
                elif frequency == 'WEEKLY':
                    return from_date + timedelta(weeks=interval)
                elif frequency == 'MONTHLY':
                    return from_date + timedelta(days=interval * 30)
                elif frequency == 'YEARLY':
                    return from_date + timedelta(days=interval * 365)

        except Exception:
            # If parsing fails, return None or default to daily
            pass

        # Default fallback - daily recurrence
        return from_date + timedelta(days=1)

    @staticmethod
    def generate_next_instance(session: Session, parent_task: Todo) -> Optional[Todo]:
        """
        Generate the next instance of a recurring task based on the template.

        Args:
            session: Database session
            parent_task: The recurring task template

        Returns:
            The newly created task instance, or None if generation failed
        """
        if not parent_task.recurrence_rule:
            return None

        # Calculate next occurrence date
        next_date = RecurringTaskService.calculate_next_occurrence(
            parent_task.recurrence_rule,
            parent_task.next_occurrence or datetime.now()
        )

        if not next_date:
            return None

        # Create a new instance based on the template
        new_instance = Todo(
            user_id=parent_task.user_id,
            title=parent_task.title,
            description=parent_task.description,
            priority=parent_task.priority,
            tags=parent_task.tags,
            due_date=next_date if parent_task.due_date else None,
            remind_at=next_date - timedelta(hours=1) if parent_task.remind_at else None,  # 1hr before due date if applicable
            recurrence_rule=None,  # Instance doesn't have recurrence rule
            parent_task_id=parent_task.id  # Reference back to the template
        )

        session.add(new_instance)
        session.commit()
        session.refresh(new_instance)

        # Update the parent's next occurrence
        parent_task.next_occurrence = RecurringTaskService.calculate_next_occurrence(
            parent_task.recurrence_rule, next_date
        )
        session.add(parent_task)
        session.commit()

        return new_instance

    @staticmethod
    def process_recurring_tasks(session: Session) -> List[Todo]:
        """
        Process all recurring tasks that are due to generate their next instance.

        Args:
            session: Database session

        Returns:
            List of newly created task instances
        """
        # Get all recurring tasks (templates with recurrence rules)
        statement = select(Todo).where(
            Todo.recurrence_rule.is_not(None),
            Todo.next_occurrence.is_not(None),
            Todo.next_occurrence <= datetime.now()
        )
        recurring_tasks = session.exec(statement).all()

        new_instances = []
        for task in recurring_tasks:
            # Generate next instance
            instance = RecurringTaskService.generate_next_instance(session, task)
            if instance:
                new_instances.append(instance)

        return new_instances

    @staticmethod
    def get_recurring_task_instances(session: Session, parent_task_id: UUID) -> List[Todo]:
        """
        Get all instances generated from a recurring task template.

        Args:
            session: Database session
            parent_task_id: ID of the parent recurring task template

        Returns:
            List of task instances generated from the template
        """
        statement = select(Todo).where(Todo.parent_task_id == parent_task_id)
        instances = session.exec(statement).all()
        return list(instances)

    @staticmethod
    def get_recurring_task_templates(session: Session, user_id: UUID) -> List[Todo]:
        """
        Get all recurring task templates for a user (tasks with recurrence rules).

        Args:
            session: Database session
            user_id: UUID of the user

        Returns:
            List of recurring task templates (tasks with recurrence rules)
        """
        statement = select(Todo).where(
            Todo.user_id == user_id,
            Todo.recurrence_rule.is_not(None)
        )
        templates = session.exec(statement).all()
        return list(templates)