"""User data model."""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr


class User(SQLModel, table=True):
    """User model for authentication and todo ownership."""

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: list["Todo"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class UserPublic(SQLModel):
    """Public user schema for API responses (excludes sensitive data)."""

    id: UUID
    email: EmailStr
    created_at: datetime


class UserCreate(SQLModel):
    """Schema for user creation."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=255)
