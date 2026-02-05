"""Todo API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from uuid import UUID
from typing import Optional, List
from datetime import datetime

from ..database import get_session
from ..schemas.todo_schemas import (
    TodoResponse,
    TodoListResponse,
    CreateTodoRequest,
    UpdateTodoRequest,
    ToggleCompletionResponse,
    PriorityEnum,
)
from ..schemas.auth_schemas import MessageResponse
from ..services.todo_service import TodoService
from .middleware import get_current_user
from ..models.user import User

router = APIRouter(prefix="/todos", tags=["Todos"])


def todo_to_response(todo) -> TodoResponse:
    """Convert a Todo model to TodoResponse with all Phase V fields."""
    return TodoResponse(
        id=todo.id,
        title=todo.title,
        description=todo.description,
        is_completed=todo.is_completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
        priority=todo.priority,
        tags=todo.tags if todo.tags else [],
        due_date=todo.due_date,
        remind_at=todo.remind_at,
        recurrence_rule=todo.recurrence_rule,
        next_occurrence=todo.next_occurrence,
        parent_task_id=todo.parent_task_id,
    )


@router.get("", response_model=TodoListResponse)
async def get_todos(
    priority: Optional[PriorityEnum] = Query(None, description="Filter by priority"),
    tags: Optional[List[str]] = Query(None, description="Filter by tags"),
    status: Optional[str] = Query(None, description="Filter by status: pending or completed"),
    due_date_from: Optional[datetime] = Query(None, description="Filter by due date from"),
    due_date_to: Optional[datetime] = Query(None, description="Filter by due date to"),
    sort_by: Optional[str] = Query(None, description="Sort by: due_date, priority, title, created_at"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Get all todos for the authenticated user with optional filtering and sorting.

    - **priority**: Filter by priority level (HIGH, MEDIUM, LOW)
    - **tags**: Filter by tags (can specify multiple)
    - **status**: Filter by completion status (pending, completed)
    - **due_date_from**: Filter todos with due date on or after this date
    - **due_date_to**: Filter todos with due date on or before this date
    - **sort_by**: Sort by field (due_date, priority, title, created_at)
    - **sort_order**: Sort order (asc, desc)

    Returns todos matching filters, empty array if no todos.
    """
    todos = TodoService.get_todos(
        session,
        current_user.id,
        priority=priority,
        tags=tags,
        status=status,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return TodoListResponse(
        todos=[todo_to_response(todo) for todo in todos],
        total=len(todos)
    )


@router.get("/search", response_model=TodoListResponse)
async def search_todos(
    q: str = Query(..., min_length=1, description="Search query"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """
    Search todos by keyword in title, description, and tags.

    - **q**: Search query string (required)

    Returns matching todos, empty array if no matches.
    """
    todos = TodoService.search_todos(session, current_user.id, q)
    return TodoListResponse(
        todos=[todo_to_response(todo) for todo in todos],
        total=len(todos)
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
