# Tasks: Phase III MCP Agentic Chatbot

**Input**: Design documents from `/specs/003-todo-ai-chatbot/`
**Prerequisites**: plan.md, research.md, data-model.md, constitution.md (Phase III rules)

**Tests**: Not explicitly requested in spec — test tasks omitted per template rules.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Constitution Compliance

**Pre-Task Gate** (per Constitution Section VII):
- [x] Plan is approved (RULE SDD-005)
- [x] Constitution Check in plan passes
- [x] Technical context is complete
- [x] Project structure is defined

**Agent Behavior Rules** (per Constitution Section II):
- [x] All tasks trace to specification requirements (RULE ABR-002)
- [x] No feature invention in task list (RULE ABR-002)
- [x] No future-phase work included (RULE ABR-006)
- [x] All tasks have clear, verifiable deliverables (RULE ABR-008)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/app/`, `frontend/services/`, `frontend/types/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install new dependencies and configure environment for Phase III agent capabilities

- [x] T001 Install `openai-agents` and `openai` packages in backend/requirements.txt
- [x] T002 Add `OPENAI_API_KEY` to backend/.env and backend/src/config.py Settings class
- [x] T003 [P] Create backend/src/models/conversation.py with Conversation SQLModel entity per data-model.md
- [x] T004 [P] Create backend/src/models/message.py with Message SQLModel entity per data-model.md
- [x] T005 Register Conversation and Message models in backend/src/models/__init__.py
- [x] T006 Create Alembic migration backend/alembic/versions/002_create_conversations_and_messages_tables.py for conversations and messages tables with foreign keys, indexes, and updated_at trigger

**Checkpoint**: New dependencies installed, environment configured, database schema extended with conversation/message tables

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core MCP tool functions and agent setup that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create backend/src/tools/__init__.py package directory
- [x] T008 Create backend/src/tools/todo_tools.py with @function_tool decorated functions: `todo_list(user_id)`, `todo_create(user_id, title, description)`, `todo_update(user_id, todo_id, title, description)`, `todo_delete(user_id, todo_id)`, `todo_toggle(user_id, todo_id)` — each accepting user_id as first param (MCP-020), returning dict (MCP-022), following naming convention (MCP-023)
- [x] T009 Create backend/src/tools/conversation_tools.py with @function_tool decorated functions: `conversation_list(user_id)`, `conversation_get(user_id, conversation_id)`, `conversation_delete(user_id, conversation_id)` — following same MCP rules
- [x] T010 Create backend/src/services/agent_service.py with: Agent definition using OpenAI Agents SDK (`Agent(name, instructions, tools)`), `run_agent(user_id, conversation_id, user_message)` method that loads history from DB, appends user message, calls `Runner.run()`, persists response, returns agent reply (per research.md pattern)
- [x] T011 Create backend/src/services/conversation_service.py with: `create_conversation(session, user_id, title)`, `get_conversations(session, user_id)`, `get_conversation(session, conversation_id, user_id)`, `delete_conversation(session, conversation_id, user_id)`, `get_messages(session, conversation_id)`, `add_message(session, conversation_id, role, content)` — all state in DB (MCP-010 through MCP-013)
- [x] T012 Create backend/src/schemas/chat_schemas.py with Pydantic models: `ChatRequest(message: str, conversation_id: Optional[str])`, `ChatResponse(response: str, conversation_id: str)`, `ConversationPublic(id, title, created_at, updated_at)`, `MessagePublic(id, role, content, created_at)`

**Checkpoint**: Foundation ready — MCP tools, agent service, conversation service, and schemas all defined. User story implementation can now begin.

---

## Phase 3: User Story 1 — Chat with AI to Manage Todos (Priority: P1) MVP

**Goal**: User can send a natural-language message and receive an AI response that manages their todos via MCP tools. This is the core chatbot interaction loop.

**Independent Test**: Send "Show me my todos" in chat and receive a formatted list from the agent. Send "Add a todo called Buy groceries" and verify it appears in the database.

### Implementation for User Story 1

- [x] T013 [US1] Create backend/src/api/chat.py with `POST /api/chat` endpoint: authenticate user via get_current_user dependency, accept ChatRequest body, call agent_service.run_agent(), return ChatResponse (MCP-050, MCP-052)
- [x] T014 [US1] Register chat router in backend/src/main.py alongside existing auth and todos routers
- [x] T015 [US1] Create frontend/types/chat.ts with TypeScript interfaces: `ChatMessage { id, role, content, created_at }`, `Conversation { id, title, created_at, updated_at }`, `ChatRequest { message, conversation_id? }`, `ChatResponse { response, conversation_id }`
- [x] T016 [US1] Create frontend/services/chatService.ts with: `sendMessage(message, conversationId?)`, `getConversations()`, `getConversation(conversationId)`, `deleteConversation(conversationId)` using existing api.ts wrapper
- [x] T017 [US1] Create frontend/app/chat/page.tsx as the primary chat interface: message input, message list, send button, loading/typing indicator (MCP-060, MCP-062), auto-scroll to bottom, sign-out button
- [x] T018 [US1] Add Markdown rendering support to chat messages in frontend/app/chat/page.tsx using dangerouslySetInnerHTML with a simple markdown-to-html conversion or install react-markdown (MCP-061)

**Checkpoint**: At this point, User Story 1 should be fully functional — user can chat with AI assistant to manage todos through natural language.

---

## Phase 4: User Story 2 — Conversation History and Management (Priority: P2)

**Goal**: User can view past conversations, switch between them, and continue previous conversations. Conversations persist across sessions (MCP-013).

**Independent Test**: Start a conversation, sign out, sign back in, and verify conversations are listed. Click a past conversation and verify message history loads. Delete a conversation and verify it's removed.

### Implementation for User Story 2

- [x] T019 [US2] Create backend/src/api/conversations.py with REST endpoints: `GET /api/conversations` (list user's conversations), `GET /api/conversations/{conversation_id}` (get conversation with messages), `DELETE /api/conversations/{conversation_id}` — all authenticated (MCP-053)
- [x] T020 [US2] Register conversations router in backend/src/main.py
- [x] T021 [US2] Add conversation sidebar to frontend/app/chat/page.tsx: list conversations on left panel, click to load conversation, active conversation highlight, new conversation button (MCP-063)
- [x] T022 [US2] Add conversation deletion UI in frontend/app/chat/page.tsx: delete button per conversation with confirmation, update sidebar after deletion
- [x] T023 [US2] Update frontend/services/chatService.ts to include `getConversationMessages(conversationId)` method for loading full message history when switching conversations

**Checkpoint**: User Stories 1 AND 2 should both work — user can chat, view history, switch conversations, and delete old ones.

---

## Phase 5: User Story 3 — Streaming Responses (Priority: P3)

**Goal**: Agent responses stream to the frontend in real-time via SSE, providing a responsive chat experience instead of waiting for the full response (MCP-051).

**Independent Test**: Send a message and verify the response appears token-by-token in the chat UI rather than all at once after a delay.

### Implementation for User Story 3

- [x] T024 [US3] Update backend/src/api/chat.py to add `POST /api/chat/stream` endpoint that returns `StreamingResponse` with `text/event-stream` media type, streaming agent output tokens as SSE events (MCP-051)
- [x] T025 [US3] Update backend/src/services/agent_service.py to add `run_agent_stream(user_id, conversation_id, user_message)` method using `Runner.run_streamed()` that yields response chunks
- [x] T026 [US3] Update frontend/services/chatService.ts to add `sendMessageStream(message, conversationId?, onChunk)` method that reads SSE stream using `ReadableStream` / `getReader()` and calls onChunk callback per token
- [x] T027 [US3] Update frontend/app/chat/page.tsx to use streaming send for messages: display tokens as they arrive, show typing indicator during stream, finalize message when stream completes

**Checkpoint**: All user stories functional — chat works, history persists, responses stream in real-time.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Navigation, UX improvements, and integration polish across all user stories

- [x] T028 [P] Update frontend/app/layout.tsx to add navigation bar with links: Home, Chat (primary), Todos (secondary per MCP-064)
- [x] T029 [P] Update frontend/app/page.tsx landing page to direct users to chat interface as primary action (MCP-003)
- [x] T030 Update frontend/app/chat/page.tsx with auto-generated conversation titles from first user message (per data-model.md: truncated to 100 chars)
- [x] T031 [P] Add proper error handling in chat UI: display agent errors as user-friendly messages (MCP-032), handle network failures gracefully, show retry option
- [x] T032 Verify all MCP tools enforce user_id authorization (MCP-021) — review todo_tools.py and conversation_tools.py for ownership checks
- [x] T033 Run Alembic migration and verify conversations/messages tables created correctly with all foreign keys and indexes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Phase 2 completion — core chat loop
- **User Story 2 (Phase 4)**: Depends on Phase 2 completion — can run after or parallel with US1
- **User Story 3 (Phase 5)**: Depends on Phase 3 completion (US1) — extends the chat endpoint with streaming
- **Polish (Phase 6)**: Depends on Phase 3 and Phase 4 completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — Independent of US1 for backend, but frontend shares chat/page.tsx with US1
- **User Story 3 (P3)**: Depends on US1 — extends the chat endpoint and frontend with streaming

### Within Each User Story

- Models before services
- Services before endpoints
- Backend before frontend
- Core implementation before integration

### Parallel Opportunities

- T003 and T004 can run in parallel (different model files)
- T008 and T009 can run in parallel (different tool files)
- T028 and T029 can run in parallel (different frontend files)
- T028 and T031 can run in parallel (different concerns)

---

## Parallel Example: Phase 2

```bash
# Launch model creation in parallel:
Task: T003 "Create Conversation model in backend/src/models/conversation.py"
Task: T004 "Create Message model in backend/src/models/message.py"

# Launch tool creation in parallel:
Task: T008 "Create todo_tools.py with @function_tool functions"
Task: T009 "Create conversation_tools.py with @function_tool functions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (dependencies, env, models, migration)
2. Complete Phase 2: Foundational (tools, agent, services, schemas)
3. Complete Phase 3: User Story 1 (chat endpoint, chat UI)
4. **STOP and VALIDATE**: Test chat with AI independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational -> Foundation ready
2. Add User Story 1 -> Test independently -> Deploy/Demo (MVP!)
3. Add User Story 2 -> Test independently -> Deploy/Demo (conversation history)
4. Add User Story 3 -> Test independently -> Deploy/Demo (streaming UX)
5. Each story adds value without breaking previous stories

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- All MCP tools must accept user_id as first param (MCP-020)
- All conversation state must be in database only (MCP-010)
- Agent must not fabricate data — always call tools (MCP-030)
