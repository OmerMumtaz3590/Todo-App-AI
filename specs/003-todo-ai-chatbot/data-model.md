# Data Model: Phase III MCP Agentic Chatbot

**Date**: 2026-02-04
**Branch**: `003-todo-ai-chatbot`

## Existing Entities (Phase II — NOT modified per MCP-044)

### User
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| email | VARCHAR(255) | UNIQUE, NOT NULL, indexed |
| password_hash | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMP | NOT NULL |

### Todo
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| user_id | UUID | FK → users.id, NOT NULL, indexed, CASCADE delete |
| title | VARCHAR(500) | NOT NULL |
| description | TEXT | nullable |
| is_completed | BOOLEAN | NOT NULL, default false |
| created_at | TIMESTAMP | NOT NULL |
| updated_at | TIMESTAMP | NOT NULL, trigger-updated |

## New Entities (Phase III)

### Conversation (MCP-040)
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| user_id | UUID | FK → users.id, NOT NULL, indexed, CASCADE delete |
| title | VARCHAR(255) | nullable, auto-generated from first message |
| created_at | TIMESTAMP | NOT NULL, default utcnow |
| updated_at | TIMESTAMP | NOT NULL, default utcnow, trigger-updated |

**Relationships**:
- `Conversation.user_id → User.id` (many-to-one)
- `Conversation → Messages` (one-to-many, cascade delete)

### Message (MCP-041)
| Field | Type | Constraints |
|-------|------|-------------|
| id | UUID | PK, default uuid4 |
| conversation_id | UUID | FK → conversations.id, NOT NULL, indexed, CASCADE delete |
| role | VARCHAR(20) | NOT NULL, enum: "user" / "assistant" |
| content | TEXT | NOT NULL |
| created_at | TIMESTAMP | NOT NULL, default utcnow |

**Relationships**:
- `Message.conversation_id → Conversation.id` (many-to-one)

**Ordering**: Messages MUST be ordered by `created_at ASC` within a conversation (MCP-043)

## Entity Relationship Diagram

```
┌──────────┐     1:N     ┌──────────────┐     1:N     ┌──────────┐
│   User   │────────────▶│ Conversation │────────────▶│ Message  │
│          │             │              │             │          │
│ id (PK)  │             │ id (PK)      │             │ id (PK)  │
│ email    │             │ user_id (FK) │             │ conv_id  │
│ pass_hash│             │ title        │             │ role     │
│ created  │             │ created_at   │             │ content  │
└──────────┘             │ updated_at   │             │ created  │
     │                   └──────────────┘             └──────────┘
     │ 1:N
     ▼
┌──────────┐
│   Todo   │
│          │
│ id (PK)  │
│ user_id  │
│ title    │
│ desc     │
│ complete │
│ created  │
│ updated  │
└──────────┘
```

## Validation Rules

- `Message.role` must be one of: `"user"`, `"assistant"`
- `Conversation.title` is nullable; auto-set from first user message (truncated to 100 chars)
- All UUIDs are v4
- Cascading deletes: deleting a User deletes their Conversations and Messages
- Cascading deletes: deleting a Conversation deletes its Messages
