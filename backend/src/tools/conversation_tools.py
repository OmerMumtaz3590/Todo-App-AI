"""MCP conversation tool functions for agent orchestration (Phase III).

Each tool follows MCP contract rules:
- MCP-020: user_id as first required parameter
- MCP-022: Returns structured dict response
- MCP-023: Naming convention <resource>_<action>
- MCP-025: Stateless — hits database directly per invocation
"""
from uuid import UUID

from agents import function_tool
from sqlmodel import Session, select

from ..database import engine
from ..models.conversation import Conversation
from ..models.message import Message


@function_tool
def conversation_list(user_id: str) -> dict:
    """List all conversations for a user, ordered by most recent first.

    Args:
        user_id: The authenticated user's UUID.
    """
    with Session(engine) as session:
        statement = (
            select(Conversation)
            .where(Conversation.user_id == UUID(user_id))
            .order_by(Conversation.updated_at.desc())
        )
        conversations = session.exec(statement).all()
        return {
            "conversations": [
                {
                    "id": str(c.id),
                    "title": c.title,
                    "created_at": c.created_at.isoformat(),
                    "updated_at": c.updated_at.isoformat(),
                }
                for c in conversations
            ],
            "count": len(conversations),
        }


@function_tool
def conversation_get(user_id: str, conversation_id: str) -> dict:
    """Get a specific conversation with its messages.

    Args:
        user_id: The authenticated user's UUID.
        conversation_id: The UUID of the conversation to retrieve.
    """
    with Session(engine) as session:
        statement = select(Conversation).where(
            Conversation.id == UUID(conversation_id),
            Conversation.user_id == UUID(user_id),
        )
        conversation = session.exec(statement).first()
        if not conversation:
            return {"error": "Conversation not found or access denied."}

        msg_statement = (
            select(Message)
            .where(Message.conversation_id == UUID(conversation_id))
            .order_by(Message.created_at.asc())
        )
        messages = session.exec(msg_statement).all()

        return {
            "id": str(conversation.id),
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "messages": [
                {
                    "id": str(m.id),
                    "role": m.role,
                    "content": m.content,
                    "created_at": m.created_at.isoformat(),
                }
                for m in messages
            ],
        }


@function_tool
def conversation_delete(user_id: str, conversation_id: str) -> dict:
    """Delete a conversation and all its messages.

    Args:
        user_id: The authenticated user's UUID.
        conversation_id: The UUID of the conversation to delete.
    """
    with Session(engine) as session:
        statement = select(Conversation).where(
            Conversation.id == UUID(conversation_id),
            Conversation.user_id == UUID(user_id),
        )
        conversation = session.exec(statement).first()
        if not conversation:
            return {"error": "Conversation not found or access denied."}

        title = conversation.title or "Untitled"
        session.delete(conversation)
        session.commit()
        return {"message": f"Conversation '{title}' deleted successfully."}
