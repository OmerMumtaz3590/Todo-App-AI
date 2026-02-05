"""Todo data model."""
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel


class PriorityEnum(str, Enum):
    """Priority levels for tasks."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class Todo(SQLModel, table=True):
    """Todo model for task management."""

    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # New Phase V fields for intermediate features
    priority: Optional[PriorityEnum] = Field(default=PriorityEnum.MEDIUM)
    tags: Optional[List[str]] = Field(default=[], sa_column_kwargs={"server_default": "'[]'", "nullable": True})
    due_date: Optional[datetime] = Field(default=None)
    remind_at: Optional[datetime] = Field(default=None)

    # New Phase V fields for advanced features
    recurrence_rule: Optional[str] = Field(default=None, max_length=500)  # iCal format or custom JSON
    next_occurrence: Optional[datetime] = Field(default=None)
    parent_task_id: Optional[UUID] = Field(foreign_key="todos.id", nullable=True)  # For recurring task templates

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")

    # Relationship to parent task for recurring tasks
    parent_task: Optional["Todo"] = Relationship(back_populates="child_tasks", remote_side=[id])
    child_tasks: List["Todo"] = Relationship(back_populates="parent_task")


class TodoPublic(SQLModel):
    """Public todo schema for API responses."""

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    # New Phase V fields
    priority: Optional[PriorityEnum] = PriorityEnum.MEDIUM
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    next_occurrence: Optional[datetime] = None
    parent_task_id: Optional[UUID] = None


class TodoCreate(SQLModel):
    """Schema for todo creation."""

    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = None
    # New Phase V fields
    priority: Optional[PriorityEnum] = PriorityEnum.MEDIUM
    tags: Optional[List[str]] = []
    due_date: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None


class TodoUpdate(SQLModel):
    """Schema for todo updates."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    tags: Optional[List[str]] = None
    due_date: Optional[datetime] = None
    remind_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    is_completed: Optional[bool] = None
