"""Conversation and message persistence service (Phase III).

All conversation state lives in the database per MCP-010 through MCP-013.
No in-memory caches, no Redis, no session objects.
"""
from datetime import datetime
from uuid import UUID

from sqlmodel import Session, select

from ..models.conversation import Conversation
from ..models.message import Message


class ConversationService:
    """Service for managing conversations and messages."""

    @staticmethod
    def create_conversation(
        session: Session, user_id: UUID, title: str | None = None
    ) -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation(user_id=user_id, title=title)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversations(session: Session, user_id: UUID) -> list[Conversation]:
        """Get all conversations for a user, ordered by most recent."""
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        return list(session.exec(statement).all())

    @staticmethod
    def get_conversation(
        session: Session, conversation_id: UUID, user_id: UUID
    ) -> Conversation | None:
        """Get a specific conversation, verifying ownership."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id,
        )
        return session.exec(statement).first()

    @staticmethod
    def delete_conversation(
        session: Session, conversation_id: UUID, user_id: UUID
    ) -> bool:
        """Delete a conversation and its messages (cascade). Returns True if deleted."""
        conversation = ConversationService.get_conversation(
            session, conversation_id, user_id
        )
        if not conversation:
            return False
        session.delete(conversation)
        session.commit()
        return True

    @staticmethod
    def get_messages(session: Session, conversation_id: UUID) -> list[Message]:
        """Get all messages for a conversation, ordered by created_at ASC (MCP-043)."""
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return list(session.exec(statement).all())

    @staticmethod
    def add_message(
        session: Session, conversation_id: UUID, role: str, content: str
    ) -> Message:
        """Add a message to a conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def update_conversation_title(
        session: Session, conversation_id: UUID, title: str
    ) -> None:
        """Set conversation title (auto-generated from first message)."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(statement).first()
        if conversation and not conversation.title:
            conversation.title = title[:100]
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()

    @staticmethod
    def touch_conversation(session: Session, conversation_id: UUID) -> None:
        """Update the conversation's updated_at timestamp."""
        statement = select(Conversation).where(Conversation.id == conversation_id)
        conversation = session.exec(statement).first()
        if conversation:
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()
