"""Todo business logic service."""
from uuid import UUID
from sqlmodel import Session, select
from ..models.todo import Todo, TodoCreate, TodoUpdate


class TodoService:
    """Service for managing todo operations."""

    @staticmethod
    def get_todos(session: Session, user_id: UUID) -> list[Todo]:
        """
        Retrieve all todos for a specific user.

        Args:
            session: Database session
            user_id: UUID of the user

        Returns:
            List of todos ordered by created_at DESC, empty list if no todos
        """
        statement = (
            select(Todo)
            .where(Todo.user_id == user_id)
            .order_by(Todo.created_at.desc())
        )
        todos = session.exec(statement).all()
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
        todo.title = todo_data.title
        if todo_data.description is not None:
            todo.description = todo_data.description

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
