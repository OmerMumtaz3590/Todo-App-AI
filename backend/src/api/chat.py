"""Chat API endpoint for Phase III agentic chatbot (MCP-050, MCP-052)."""
import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from ..api.middleware import get_current_user
from ..models.user import User
from ..schemas.chat_schemas import ChatRequest, ChatResponse
from ..services import agent_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    """Send a message to the AI assistant and get a response.

    Authenticates user via JWT cookie, runs the agent with conversation
    history loaded from DB, persists the response, and returns it.

    MCP-050: Single chat endpoint accepting user message and returning agent response.
    MCP-052: Authenticated via Bearer token (cookie-based JWT).
    """
    try:
        response_text, conversation_id = await agent_service.run_agent(
            user_id=str(current_user.id),
            conversation_id=request.conversation_id,
            user_message=request.message,
        )
        return ChatResponse(response=response_text, conversation_id=conversation_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent error: {str(e)}",
        )


@router.post("/chat/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    """Stream a response from the AI assistant via SSE (MCP-051).

    Returns a text/event-stream with chunks of the agent's response
    as they are generated.
    """
    async def event_generator():
        try:
            conversation_id = None
            async for chunk, conv_id in agent_service.run_agent_stream(
                user_id=str(current_user.id),
                conversation_id=request.conversation_id,
                user_message=request.message,
            ):
                conversation_id = conv_id
                data = json.dumps({"chunk": chunk, "conversation_id": conv_id})
                yield f"data: {data}\n\n"

            # Send done event
            yield f"data: {json.dumps({'done': True, 'conversation_id': conversation_id})}\n\n"
        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
