"""MCP todo tool functions for agent orchestration (Phase III).

Each tool follows MCP contract rules:
- MCP-020: user_id as first required parameter
- MCP-022: Returns structured dict response
- MCP-023: Naming convention <resource>_<action>
- MCP-025: Stateless — hits database directly per invocation
"""
from uuid import UUID

from agents import function_tool
from sqlmodel import Session, select

from ..database import engine
from ..models.todo import Todo


@function_tool
def todo_list(user_id: str) -> dict:
    """List all todos for a user. Returns a list of todos with their id, title, description, completion status, and timestamps.

    Args:
        user_id: The authenticated user's UUID.
    """
    with Session(engine) as session:
        statement = (
            select(Todo)
            .where(Todo.user_id == UUID(user_id))
            .order_by(Todo.created_at.desc())
        )
        todos = session.exec(statement).all()
        return {
            "todos": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "description": t.description,
                    "is_completed": t.is_completed,
                    "created_at": t.created_at.isoformat(),
                    "updated_at": t.updated_at.isoformat(),
                }
                for t in todos
            ],
            "count": len(todos),
        }


@function_tool
def todo_create(user_id: str, title: str, description: str = "") -> dict:
    """Create a new todo for a user.

    Args:
        user_id: The authenticated user's UUID.
        title: The title of the todo (required, max 500 chars).
        description: Optional description for the todo.
    """
    with Session(engine) as session:
        todo = Todo(
            user_id=UUID(user_id),
            title=title[:500],
            description=description if description else None,
        )
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return {
            "id": str(todo.id),
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed,
            "created_at": todo.created_at.isoformat(),
            "message": f"Todo '{todo.title}' created successfully.",
        }


@function_tool
def todo_update(user_id: str, todo_id: str, title: str, description: str = "") -> dict:
    """Update an existing todo's title and description.

    Args:
        user_id: The authenticated user's UUID.
        todo_id: The UUID of the todo to update.
        title: The new title for the todo.
        description: The new description for the todo.
    """
    with Session(engine) as session:
        statement = select(Todo).where(
            Todo.id == UUID(todo_id), Todo.user_id == UUID(user_id)
        )
        todo = session.exec(statement).first()
        if not todo:
            return {"error": "Todo not found or access denied."}

        todo.title = title[:500]
        todo.description = description if description else None
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return {
            "id": str(todo.id),
            "title": todo.title,
            "description": todo.description,
            "is_completed": todo.is_completed,
            "message": f"Todo '{todo.title}' updated successfully.",
        }


@function_tool
def todo_delete(user_id: str, todo_id: str) -> dict:
    """Delete a todo.

    Args:
        user_id: The authenticated user's UUID.
        todo_id: The UUID of the todo to delete.
    """
    with Session(engine) as session:
        statement = select(Todo).where(
            Todo.id == UUID(todo_id), Todo.user_id == UUID(user_id)
        )
        todo = session.exec(statement).first()
        if not todo:
            return {"error": "Todo not found or access denied."}

        title = todo.title
        session.delete(todo)
        session.commit()
        return {"message": f"Todo '{title}' deleted successfully."}


@function_tool
def todo_toggle(user_id: str, todo_id: str) -> dict:
    """Toggle the completion status of a todo.

    Args:
        user_id: The authenticated user's UUID.
        todo_id: The UUID of the todo to toggle.
    """
    with Session(engine) as session:
        statement = select(Todo).where(
            Todo.id == UUID(todo_id), Todo.user_id == UUID(user_id)
        )
        todo = session.exec(statement).first()
        if not todo:
            return {"error": "Todo not found or access denied."}

        todo.is_completed = not todo.is_completed
        session.add(todo)
        session.commit()
        session.refresh(todo)
        status = "completed" if todo.is_completed else "incomplete"
        return {
            "id": str(todo.id),
            "title": todo.title,
            "is_completed": todo.is_completed,
            "message": f"Todo '{todo.title}' marked as {status}.",
        }
