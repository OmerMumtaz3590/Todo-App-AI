"""Todo data model."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


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

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")


class TodoPublic(SQLModel):
    """Public todo schema for API responses."""

    id: UUID
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class TodoCreate(SQLModel):
    """Schema for todo creation."""

    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = None


class TodoUpdate(SQLModel):
    """Schema for todo updates."""

    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = None
