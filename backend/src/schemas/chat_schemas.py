"""Chat request/response schemas for Phase III."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel


class ChatRequest(SQLModel):
    """Request body for the chat endpoint."""

    message: str
    conversation_id: Optional[str] = None


class ChatResponse(SQLModel):
    """Response body from the chat endpoint."""

    response: str
    conversation_id: str


class ConversationPublic(SQLModel):
    """Public conversation schema for API responses."""

    id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime


class MessagePublic(SQLModel):
    """Public message schema for API responses."""

    id: UUID
    role: str
    content: str
    created_at: datetime
