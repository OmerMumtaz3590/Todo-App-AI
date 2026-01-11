"""Todo API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID

from ..database import get_session
from ..schemas.todo_schemas import (
    TodoResponse,
    TodoListResponse,
    CreateTodoRequest,
    UpdateTodoRequest,
    ToggleCompletionResponse,
)
from ..schemas.auth_schemas import MessageResponse
from ..services.todo_service import TodoService
from .middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.get("", response_model=TodoListResponse)
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get all todos for the authenticated user.

    Returns todos ordered by created_at DESC, empty array if no todos.
    """
    todos = TodoService.get_todos(session, current_user.id)
    return TodoListResponse(
        todos=[
            TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                is_completed=todo.is_completed,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            )
            for todo in todos
        ]
    )


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_data: CreateTodoRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Create a new todo for the authenticated user.

    - **title**: Todo title (1-500 characters, required)
    - **description**: Optional todo description
    """
    todo = TodoService.create_todo(session, current_user.id, todo_data)
    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: UUID,
    todo_data: UpdateTodoRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Update an existing todo.

    - **title**: New todo title (1-500 characters)
    - **description**: New optional todo description

    Returns 404 if todo not found or doesn't belong to user.
    """
    todo = TodoService.update_todo(session, todo_id, current_user.id, todo_data)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )


@router.patch("/{todo_id}/toggle", response_model=ToggleCompletionResponse)
async def toggle_completion(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Toggle the completion status of a todo.

    Returns 404 if todo not found or doesn't belong to user.
    """
    todo = TodoService.toggle_completion(session, todo_id, current_user.id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return ToggleCompletionResponse(
        todo=TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            is_completed=todo.is_completed,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )
    )


@router.delete("/{todo_id}", response_model=MessageResponse)
async def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Delete a todo.

    Returns 404 if todo not found or doesn't belong to user.
    """
    success = TodoService.delete_todo(session, todo_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return MessageResponse(message="Todo deleted successfully")
