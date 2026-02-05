"""Conversation management API endpoints for Phase III (MCP-053)."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..api.middleware import get_current_user
from ..database import get_session
from ..models.user import User
from ..schemas.chat_schemas import ConversationPublic, MessagePublic
from ..services.conversation_service import ConversationService

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("", response_model=dict)
async def list_conversations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """List all conversations for the authenticated user."""
    conversations = ConversationService.get_conversations(session, current_user.id)
    return {
        "conversations": [
            ConversationPublic(
                id=c.id,
                title=c.title,
                created_at=c.created_at,
                updated_at=c.updated_at,
            ).model_dump()
            for c in conversations
        ]
    }


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Get a specific conversation with all messages."""
    conversation = ConversationService.get_conversation(
        session, conversation_id, current_user.id
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    messages = ConversationService.get_messages(session, conversation_id)
    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "messages": [
            MessagePublic(
                id=m.id,
                role=m.role,
                content=m.content,
                created_at=m.created_at,
            ).model_dump()
            for m in messages
        ],
    }


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Delete a conversation and all its messages."""
    deleted = ConversationService.delete_conversation(
        session, conversation_id, current_user.id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return {"message": "Conversation deleted successfully"}
