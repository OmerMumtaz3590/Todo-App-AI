"""Todo business logic service."""
from datetime import datetime
from uuid import UUID
from sqlmodel import Session, select
from typing import List, Optional
from ..models.todo import Todo, TodoCreate, TodoUpdate, PriorityEnum


class TodoService:
    """Service for managing todo operations."""

    @staticmethod
    def get_todos(session: Session, user_id: UUID, priority: Optional[PriorityEnum] = None,
                  tags: Optional[List[str]] = None, status: Optional[str] = None,
                  due_date_from: Optional[datetime] = None, due_date_to: Optional[datetime] = None,
                  sort_by: Optional[str] = None, sort_order: Optional[str] = None) -> list[Todo]:
        """
        Retrieve all todos for a specific user with optional filtering and sorting.

        Args:
            session: Database session
            user_id: UUID of the user
            priority: Filter by priority level (HIGH, MEDIUM, LOW)
            tags: Filter by tags (array of tag strings)
            status: Filter by completion status (pending, completed)
            due_date_from: Filter by due date from
            due_date_to: Filter by due date to
            sort_by: Sort by field (due_date, priority, title, created_at)
            sort_order: Sort order (asc, desc)

        Returns:
            List of todos matching filters and sorted as requested, empty list if no todos
        """
        statement = select(Todo).where(Todo.user_id == user_id)

        # Apply filters
        if priority:
            statement = statement.where(Todo.priority == priority)

        if status:
            if status == "pending":
                statement = statement.where(Todo.is_completed == False)
            elif status == "completed":
                statement = statement.where(Todo.is_completed == True)

        if due_date_from:
            statement = statement.where(Todo.due_date >= due_date_from)

        if due_date_to:
            statement = statement.where(Todo.due_date <= due_date_to)

        # Apply tag filter - check if any of the provided tags are in the todo's tags
        if tags:
            for tag in tags:
                statement = statement.where(Todo.tags.contains([tag]))

        # Apply sorting
        if sort_by == "due_date":
            if sort_order == "desc":
                statement = statement.order_by(Todo.due_date.desc())
            else:
                statement = statement.order_by(Todo.due_date.asc())
        elif sort_by == "priority":
            if sort_order == "desc":
                statement = statement.order_by(Todo.priority.desc())
            else:
                statement = statement.order_by(Todo.priority.asc())
        elif sort_by == "title":
            if sort_order == "desc":
                statement = statement.order_by(Todo.title.desc())
            else:
                statement = statement.order_by(Todo.title.asc())
        else:  # Default sort by created_at
            if sort_order == "desc":
                statement = statement.order_by(Todo.created_at.desc())
            else:
                statement = statement.order_by(Todo.created_at.asc())

        todos = session.exec(statement).all()
        return list(todos)

    @staticmethod
    def search_todos(session: Session, user_id: UUID, query: str) -> list[Todo]:
        """
        Search todos by keyword in title, description, and tags.

        Args:
            session: Database session
            user_id: UUID of the user
            query: Search query string

        Returns:
            List of todos matching the search query, empty list if no matches
        """
        statement = select(Todo).where(
            Todo.user_id == user_id
        ).where(
            (Todo.title.ilike(f'%{query}%')) |
            (Todo.description.ilike(f'%{query}%'))
        )

        todos = session.exec(statement).all()

        # For tag searching, we'll need to handle this separately since arrays are involved
        # Additional search logic can be implemented based on specific requirements

        return list(todos)

    @staticmethod
    def get_todo_by_id(session: Session, todo_id: UUID, user_id: UUID) -> Todo | None:
        """
        Retrieve a specific todo by ID for a user.

        Args:
            session: Database session
            todo_id: UUID of the todo
            user_id: UUID of the user (for authorization)

        Returns:
            Todo if found and belongs to user, None otherwise
        """
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def create_todo(session: Session, user_id: UUID, todo_data: TodoCreate) -> Todo:
        """
        Create a new todo for a user.

        Args:
            session: Database session
            user_id: UUID of the user
            todo_data: Todo creation data

        Returns:
            Created Todo instance
        """
        todo = Todo(
            user_id=user_id,
            title=todo_data.title,
            description=todo_data.description,
            priority=todo_data.priority,
            tags=todo_data.tags if todo_data.tags else [],
            due_date=todo_data.due_date,
            remind_at=todo_data.remind_at,
            recurrence_rule=todo_data.recurrence_rule
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def update_todo(
        session: Session, todo_id: UUID, user_id: UUID, todo_data: TodoUpdate
    ) -> Todo | None:
        """
        Update an existing todo.

        Args:
            session: Database session
            todo_id: UUID of the todo to update
            user_id: UUID of the user (for authorization)
            todo_data: Todo update data

        Returns:
            Updated Todo if found and belongs to user, None otherwise
        """
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return None

        # Update fields
        if todo_data.title is not None:
            todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description
        if todo_data.priority is not None:
            todo.priority = todo_data.priority
        if todo_data.tags is not None:
            todo.tags = todo_data.tags
        if todo_data.due_date is not None:
            todo.due_date = todo_data.due_date
        if todo_data.remind_at is not None:
            todo.remind_at = todo_data.remind_at
        if todo_data.recurrence_rule is not None:
            todo.recurrence_rule = todo_data.recurrence_rule
        if todo_data.is_completed is not None:
            todo.is_completed = todo_data.is_completed

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def toggle_completion(
        session: Session, todo_id: UUID, user_id: UUID
    ) -> Todo | None:
        """
        Toggle the completion status of a todo.

        Args:
            session: Database session
            todo_id: UUID of the todo to toggle
            user_id: UUID of the user (for authorization)

        Returns:
            Updated Todo if found and belongs to user, None otherwise
        """
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return None

        todo.is_completed = not todo.is_completed
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def delete_todo(session: Session, todo_id: UUID, user_id: UUID) -> bool:
        """
        Delete a todo.

        Args:
            session: Database session
            todo_id: UUID of the todo to delete
            user_id: UUID of the user (for authorization)

        Returns:
            True if deleted, False if not found or unauthorized
        """
        todo = TodoService.get_todo_by_id(session, todo_id, user_id)
        if not todo:
            return False

        session.delete(todo)
        session.commit()
        return True
