# Research: Phase III MCP Agentic Chatbot (Backend)

**Date**: 2026-02-04
**Branch**: `003-todo-ai-chatbot`

## 1. MCP Server Implementation

**Decision**: Use `mcp.server.fastmcp.FastMCP` from the official MCP Python SDK (`mcp>=1.0`)

**Rationale**:
- Official SDK maintained by Anthropic with high-quality documentation
- `@mcp.tool()` decorator pattern is simple and mirrors existing FastAPI patterns
- Supports streamable-http transport natively
- Tools are defined as plain Python functions with type hints — the SDK auto-generates JSON schemas

**Alternatives Considered**:
- Custom tool registry: Rejected — reinvents the wheel, no interoperability
- LangChain tool wrappers: Rejected — adds heavyweight dependency not in constitution

**Key Pattern**:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Todo MCP Server")

@mcp.tool()
def todo_list(user_id: str) -> dict:
    """List all todos for a user."""
    ...
```

## 2. OpenAI Agents SDK Integration

**Decision**: Use `openai-agents` SDK with `Runner.run()` and manual conversation history via `to_input_list()`

**Rationale**:
- Constitution mandates OpenAI Agents SDK for agent orchestration (TC-001)
- `Runner.run()` with explicit input list gives full control over conversation state
- Avoids SQLiteSession (agent SDK's built-in) since constitution requires all state in PostgreSQL (MCP-011)
- `@function_tool` decorator registers Python functions as agent-callable tools

**Alternatives Considered**:
- `SQLiteSession` from agents SDK: Rejected — violates MCP-011 (all state in DB), adds second database
- LangChain agents: Rejected — not in constitution technology list
- Direct OpenAI API calls: Rejected — loses tool orchestration benefits

**Key Pattern**:
```python
from agents import Agent, Runner, function_tool

agent = Agent(
    name="Todo Assistant",
    instructions="...",
    tools=[todo_list, todo_create, ...],
)
# Load history from DB, append new message, run agent
messages = load_messages_from_db(conversation_id)
messages.append({"role": "user", "content": user_message})
result = await Runner.run(agent, messages)
```

## 3. Conversation Persistence Strategy

**Decision**: Store conversations and messages in PostgreSQL via SQLModel, load-on-request pattern

**Rationale**:
- Constitution rules MCP-010 through MCP-013 mandate stateless server with DB-only state
- Each request: load conversation history → build message list → run agent → save response
- No in-memory caches, no Redis, no session objects
- Messages ordered by `created_at` for deterministic reconstruction (MCP-043)

**Alternatives Considered**:
- Redis for conversation cache: Rejected — explicitly prohibited (MCP-010)
- Agent SDK's SQLiteSession: Rejected — violates single-DB requirement

## 4. MCP Tools as Function Tools (not MCP Server)

**Decision**: Define MCP tools as `@function_tool` decorated functions for the OpenAI Agent, NOT as a separate MCP server process

**Rationale**:
- The user's scope specifies a stateless `/api/{user_id}/chat` endpoint
- Running a separate MCP server process adds deployment complexity inappropriate for Phase III (single deployable backend — MCP rule)
- The OpenAI Agents SDK `@function_tool` pattern achieves the same goal: the agent calls typed Python functions to manage todos
- The tools follow MCP naming conventions (`todo_create`, `todo_list`, etc.) and accept `user_id` as first param per MCP-020
- If a full MCP server is needed later (Phase IV+), the tool functions can be trivially wrapped with `@mcp.tool()`

**Alternatives Considered**:
- Separate MCP server with stdio transport: Rejected — adds subprocess management, violates single-deployable rule
- MCP server on streamable-http co-hosted: Viable but unnecessary complexity for Phase III

## 5. Chat Endpoint Design

**Decision**: `POST /api/{user_id}/chat` with JSON body `{ "message": str, "conversation_id": str | null }`

**Rationale**:
- `user_id` in path matches existing `/todos` endpoint patterns
- `conversation_id` is optional — null starts a new conversation
- JWT verification via existing cookie-based auth middleware
- Returns `{ "response": str, "conversation_id": str }`

## 6. New Dependencies

| Package | Purpose | Justification (TC-003) |
|---------|---------|----------------------|
| `openai-agents` | Agent orchestration | Constitution mandates (Phase III) |
| `openai` | OpenAI API client (transitive) | Required by openai-agents |

Note: `mcp` SDK is NOT needed as a direct dependency since we use `@function_tool` pattern rather than a standalone MCP server.
