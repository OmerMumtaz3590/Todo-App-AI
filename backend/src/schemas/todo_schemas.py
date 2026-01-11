"""Todo API request and response schemas."""
from uuid import UUID
from datetime import datetime
from sqlmodel import SQLModel, Field


class TodoResponse(SQLModel):
    """Response schema for a single todo."""

    id: UUID
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class TodoListResponse(SQLModel):
    """Response schema for a list of todos."""

    todos: list[TodoResponse]


class CreateTodoRequest(SQLModel):
    """Request schema for creating a todo."""

    title: str = Field(min_length=1, max_length=500, description="Todo title")
    description: str | None = Field(default=None, description="Optional todo description")


class UpdateTodoRequest(SQLModel):
    """Request schema for updating a todo."""

    title: str = Field(min_length=1, max_length=500, description="Todo title")
    description: str | None = Field(default=None, description="Optional todo description")


class ToggleCompletionResponse(SQLModel):
    """Response schema for toggling todo completion."""

    message: str = Field(default="Todo completion status updated")
    todo: TodoResponse
