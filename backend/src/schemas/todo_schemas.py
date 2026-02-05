"""Todo API request and response schemas."""
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field
from enum import Enum


class PriorityEnum(str, Enum):
    """Priority levels for tasks."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class TodoResponse(SQLModel):
    """Response schema for a single todo."""

    id: UUID
    title: str
    description: str | None
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    # Phase V fields
    priority: Optional[PriorityEnum] = PriorityEnum.MEDIUM
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    next_occurrence: Optional[datetime] = None
    parent_task_id: Optional[UUID] = None


class TodoListResponse(SQLModel):
    """Response schema for a list of todos."""

    todos: list[TodoResponse]
    total: Optional[int] = None


class CreateTodoRequest(SQLModel):
    """Request schema for creating a todo."""

    title: str = Field(min_length=1, max_length=500, description="Todo title")
    description: str | None = Field(default=None, description="Optional todo description")
    # Phase V fields
    priority: Optional[PriorityEnum] = Field(default=PriorityEnum.MEDIUM, description="Task priority")
    tags: Optional[List[str]] = Field(default=[], description="List of tags")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    remind_at: Optional[datetime] = Field(default=None, description="Reminder time")
    recurrence_rule: Optional[str] = Field(default=None, max_length=500, description="iCal recurrence rule")


class UpdateTodoRequest(SQLModel):
    """Request schema for updating a todo."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=500, description="Todo title")
    description: Optional[str] = Field(default=None, description="Optional todo description")
    # Phase V fields
    priority: Optional[PriorityEnum] = Field(default=None, description="Task priority")
    tags: Optional[List[str]] = Field(default=None, description="List of tags")
    due_date: Optional[datetime] = Field(default=None, description="Due date for the task")
    remind_at: Optional[datetime] = Field(default=None, description="Reminder time")
    recurrence_rule: Optional[str] = Field(default=None, max_length=500, description="iCal recurrence rule")
    is_completed: Optional[bool] = Field(default=None, description="Completion status")


class ToggleCompletionResponse(SQLModel):
    """Response schema for toggling todo completion."""

    message: str = Field(default="Todo completion status updated")
    todo: TodoResponse
