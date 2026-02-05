---
id: 002
title: Amend Phase III MCP Agentic Architecture
stage: constitution
date: 2026-02-04
surface: agent
model: claude-opus-4-5
feature: none
branch: 002-fullstack-web-app
user: system
command: /sp.constitution
labels: ["constitution", "phase-iii", "mcp", "agentic-chatbot", "stateless", "amendment"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Update the project Constitution file to make it Phase III ready with strong emphasis on MCP architecture, stateless design and correct agent behavior.

Add these new or expanded rules:

## Phase III Global Rules – MCP & Agentic Chatbot Architecture

1. Interface Philosophy
   - Natural language is now the ONLY user interface for task management
   - Classic REST API remains for possible future use, but is NOT the primary interaction path

2. Statelessness Requirement (strict)
   - FastAPI server MUST be completely stateless regarding conversations
   - No session objects, no redis, no in-memory caches for chat state
   - All state lives in database: conversations + messages tables

3. MCP Tools Contract (non-negotiable)
   - Every tool MUST:
     - Accept user_id as first required parameter (string)
     - Validate that the authenticated user matches this user_id
     - Return simple structured response

## Response snapshot

Constitution successfully amended from version 1.1.0 to 2.0.0 (MAJOR).

Key changes:
1. Phase III redefined from generic "Enhanced Web" to "MCP Agentic Chatbot" — natural-language task management via MCP tools, Claude/OpenAI agents, stateless API
2. New Section IX added: "Phase III Global Rules – MCP & Agentic Chatbot Architecture" with 7 subsections and 34 new rules (MCP-001 through MCP-064)
3. Technology matrix updated: MCP SDK, Claude API, and OpenAI Agents SDK introduced at Phase III (previously Phase V)
4. Statelessness rules (QP-005 through QP-007) updated to enforce from Phase III onward
5. Phase III constraints explicitly prohibit session objects, Redis, in-memory caches, and MCP tools without user_id validation

New rule categories:
- Interface Philosophy (MCP-001 to MCP-003): NL-first interface mandate
- Statelessness Requirement (MCP-010 to MCP-013): Strict database-only conversation state
- MCP Tools Contract (MCP-020 to MCP-025): Tool signature and behavior requirements
- Agent Behavior (MCP-030 to MCP-034): Agent integrity and authorization rules
- Database Schema Rules (MCP-040 to MCP-044): conversations/messages table requirements
- API Endpoint Rules (MCP-050 to MCP-053): Chat endpoint and streaming requirements
- Frontend Rules (MCP-060 to MCP-064): Chat UI and Markdown rendering requirements

## Outcome

- ✅ Impact: MAJOR constitutional amendment redefines Phase III from generic "Enhanced Web" to MCP-driven agentic chatbot architecture with 34 new non-negotiable rules governing interface philosophy, statelessness, tool contracts, agent behavior, schema, API, and frontend
- 🧪 Tests: N/A (constitutional document)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Create Phase III specification following new constitutional rules; verify templates against new Phase III constraints
- 🧠 Reflection: MAJOR version bump justified — Phase III scope fundamentally changed from generic enhancement to a specific MCP architecture with strict statelessness and tool contract requirements. All future Phase III specs/plans must comply with the 34 new MCP-* rules.

## Evaluation notes (flywheel)

- Failure modes observed: None - amendment completed successfully with all 7 subsections and rule numbering consistent
- Graders run and results (PASS/FAIL): Manual verification PASS - all placeholders replaced, version incremented correctly, rule numbering sequential and gap-free within subsections
- Prompt variant (if applicable): N/A - direct amendment request
- Next experiment (smallest change to try): Verify plan-template.md, spec-template.md, and tasks-template.md against new Phase III rules; templates flagged with ⚠️ in sync impact report
