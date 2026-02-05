"""Agent orchestration service using OpenAI Agents SDK (Phase III).

Implements the load-on-request pattern per MCP-010 through MCP-013:
1. Load conversation history from DB
2. Build message list
3. Run agent with tools
4. Persist response to DB
5. Return agent reply

The agent MUST NOT fabricate data (MCP-030) — all data access goes through tools.
"""
import os
from uuid import UUID

from agents import Agent, Runner, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from sqlmodel import Session

from ..config import settings
from ..database import engine
from ..models.conversation import Conversation
from ..models.message import Message
from ..services.conversation_service import ConversationService
from ..tools.todo_tools import todo_list, todo_create, todo_update, todo_delete, todo_toggle
from ..tools.conversation_tools import conversation_list, conversation_get, conversation_delete


# Set API key for OpenAI
os.environ["OPENAI_API_KEY"] = settings.openai_api_key

SYSTEM_INSTRUCTIONS = """You are a helpful AI todo assistant. You help users manage their tasks through natural language conversation.

You have access to the following tools for managing todos:
- todo_list: List all todos for the user
- todo_create: Create a new todo
- todo_update: Update a todo's title and description
- todo_delete: Delete a todo
- todo_toggle: Mark a todo as complete/incomplete

And for managing conversations:
- conversation_list: List past conversations
- conversation_get: Get a specific conversation
- conversation_delete: Delete a conversation

IMPORTANT RULES:
- Always use the provided user_id when calling tools. Never fabricate or guess data.
- When listing todos, format them clearly with completion status.
- When creating todos, confirm the creation to the user.
- Be concise but friendly in your responses.
- If a tool returns an error, explain it to the user in simple terms.
- Use markdown formatting for better readability (lists, bold, etc.).
"""

# Create the agent with all MCP tools
todo_agent = Agent(
    name="Todo Assistant",
    instructions=SYSTEM_INSTRUCTIONS,
    tools=[
        todo_list,
        todo_create,
        todo_update,
        todo_delete,
        todo_toggle,
        conversation_list,
        conversation_get,
        conversation_delete,
    ],
)


async def run_agent(
    user_id: str, conversation_id: str | None, user_message: str
) -> tuple[str, str]:
    """Run the agent with conversation history from DB.

    Args:
        user_id: The authenticated user's UUID string.
        conversation_id: Existing conversation UUID or None to start new.
        user_message: The user's natural language message.

    Returns:
        Tuple of (agent_response_text, conversation_id).
    """
    with Session(engine) as session:
        # Get or create conversation
        if conversation_id:
            conversation = ConversationService.get_conversation(
                session, UUID(conversation_id), UUID(user_id)
            )
            if not conversation:
                # Conversation not found — create a new one
                conversation = ConversationService.create_conversation(
                    session, UUID(user_id)
                )
        else:
            conversation = ConversationService.create_conversation(
                session, UUID(user_id)
            )

        conv_id = conversation.id

        # Load message history from DB (MCP-011, MCP-043)
        db_messages = ConversationService.get_messages(session, conv_id)

        # Build input list for the agent
        # Inject user_id into system instructions so tools can use it
        input_messages = []
        input_messages.append({
            "role": "user",
            "content": f"[SYSTEM CONTEXT] My user_id is: {user_id}. Use this user_id for all tool calls.",
        })
        input_messages.append({
            "role": "assistant",
            "content": "Understood. I will use your user_id for all tool operations.",
        })

        for msg in db_messages:
            input_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        # Append the new user message
        input_messages.append({"role": "user", "content": user_message})

        # Persist user message to DB
        ConversationService.add_message(session, conv_id, "user", user_message)

        # Auto-generate conversation title from first user message
        if not conversation.title:
            ConversationService.update_conversation_title(
                session, conv_id, user_message
            )

    # Run the agent (outside session context since tools open their own sessions)
    result = await Runner.run(todo_agent, input_messages)
    agent_response = result.final_output or "I'm sorry, I couldn't generate a response."

    # Persist assistant response to DB
    with Session(engine) as session:
        ConversationService.add_message(session, conv_id, "assistant", agent_response)
        ConversationService.touch_conversation(session, conv_id)

    return agent_response, str(conv_id)


async def run_agent_stream(
    user_id: str, conversation_id: str | None, user_message: str
):
    """Run the agent with streaming output.

    Args:
        user_id: The authenticated user's UUID string.
        conversation_id: Existing conversation UUID or None to start new.
        user_message: The user's natural language message.

    Yields:
        Tuples of (chunk_text, conversation_id). Final yield has chunk_text=None.
    """
    with Session(engine) as session:
        # Get or create conversation
        if conversation_id:
            conversation = ConversationService.get_conversation(
                session, UUID(conversation_id), UUID(user_id)
            )
            if not conversation:
                conversation = ConversationService.create_conversation(
                    session, UUID(user_id)
                )
        else:
            conversation = ConversationService.create_conversation(
                session, UUID(user_id)
            )

        conv_id = conversation.id

        # Load message history from DB
        db_messages = ConversationService.get_messages(session, conv_id)

        input_messages = []
        input_messages.append({
            "role": "user",
            "content": f"[SYSTEM CONTEXT] My user_id is: {user_id}. Use this user_id for all tool calls.",
        })
        input_messages.append({
            "role": "assistant",
            "content": "Understood. I will use your user_id for all tool operations.",
        })

        for msg in db_messages:
            input_messages.append({
                "role": msg.role,
                "content": msg.content,
            })

        input_messages.append({"role": "user", "content": user_message})

        # Persist user message
        ConversationService.add_message(session, conv_id, "user", user_message)

        # Auto-generate title
        if not conversation.title:
            ConversationService.update_conversation_title(
                session, conv_id, user_message
            )

    # Stream the agent response
    full_response = ""
    result = Runner.run_streamed(todo_agent, input_messages)

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            chunk = event.data.delta
            if chunk:
                full_response += chunk
                yield chunk, str(conv_id)

    # If no streaming happened, use final output
    if not full_response and result.final_output:
        full_response = result.final_output
        yield full_response, str(conv_id)

    # Persist complete assistant response
    if full_response:
        with Session(engine) as session:
            ConversationService.add_message(
                session, conv_id, "assistant", full_response
            )
            ConversationService.touch_conversation(session, conv_id)
