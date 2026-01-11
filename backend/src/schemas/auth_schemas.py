"""Authentication API request and response schemas."""
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import SQLModel, Field


class SignupRequest(SQLModel):
    """Request schema for user signup."""

    email: EmailStr = Field(description="User email address")
    password: str = Field(min_length=8, max_length=255, description="User password (min 8 characters)")


class SignupResponse(SQLModel):
    """Response schema for successful signup."""

    message: str = Field(default="Account created successfully")
    user_id: UUID


class SigninRequest(SQLModel):
    """Request schema for user signin."""

    email: EmailStr = Field(description="User email address")
    password: str = Field(description="User password")


class SigninResponse(SQLModel):
    """Response schema for successful signin."""

    message: str = Field(default="Signed in successfully")
    user: dict  # {"id": UUID, "email": str}


class MessageResponse(SQLModel):
    """Generic message response schema."""

    message: str


class ErrorResponse(SQLModel):
    """Error response schema."""

    error: str
    detail: str | None = None
