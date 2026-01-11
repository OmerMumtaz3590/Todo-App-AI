# Data Model: Phase II Full-Stack Todo App

**Feature**: Full-Stack Todo Web Application
**Date**: 2026-01-03
**Phase**: Phase 1 (Design)
**Database**: Neon PostgreSQL (Serverless PostgreSQL)

## Overview

This document defines the database schema for the Phase II full-stack todo application. The data model consists of two primary entities: User and Todo, with a one-to-many relationship. The schema is designed for SQLModel/SQLAlchemy implementation and follows PostgreSQL best practices.

---

## Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id (PK, UUID)       │
│ email (unique)      │
│ password_hash       │
│ created_at          │
└─────────────────────┘
          │
          │ 1
          │
          │ *
          ▼
┌─────────────────────┐
│       Todo          │
├─────────────────────┤
│ id (PK, UUID)       │
│ user_id (FK)        │
│ title               │
│ description         │
│ is_completed        │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

**Relationship**: One User has many Todos. One Todo belongs to one User.

---

## Entity: User

### Purpose
Represents an authenticated user account in the system. Users can sign up, sign in, and manage their own todos.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the user (auto-generated) |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User's email address for login |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password (managed by Better Auth) |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Account creation timestamp |

### Indexes

- **Primary Key Index**: `id` (automatic with PRIMARY KEY)
- **Unique Index**: `email` (automatic with UNIQUE constraint)
- **Additional Index**: `email` for fast lookup during authentication

### Constraints

- **Primary Key**: `id` must be unique and not null
- **Unique Constraint**: `email` must be unique across all users
- **Email Format**: Application layer validates email format before insert
- **Password**: Never store plain-text passwords (Better Auth handles hashing)

### SQLModel Definition (Pseudocode)

```python
from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (not a database column)
    todos: list["Todo"] = Relationship(back_populates="user")
```

### Validation Rules

- **Email**:
  - Must be valid email format (RFC 5322)
  - Must be unique
  - Case-insensitive comparison (normalize to lowercase before insert)
  - Maximum length: 255 characters

- **Password (pre-hash)**:
  - Minimum length: 8 characters
  - Must meet Better Auth security requirements
  - Hashed with bcrypt before storage

### Data Examples

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "password_hash": "$2b$12$KIXxLVq8YrJ7Hx4pQ8Z9OeN7XqJ8vQ7Zx9KpL8mN6Zy5X4wR3sT6u",
  "created_at": "2026-01-03T10:00:00Z"
}
```

---

## Entity: Todo

### Purpose
Represents a single todo/task item owned by a user. Users can create, read, update, delete, and toggle the completion status of their todos.

### Attributes

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the todo (auto-generated) |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEX | Owner of this todo |
| `title` | VARCHAR(500) | NOT NULL | Title/summary of the todo |
| `description` | TEXT | NULLABLE | Optional detailed description |
| `is_completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Completion status |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Todo creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | Last modification timestamp |

### Indexes

- **Primary Key Index**: `id` (automatic with PRIMARY KEY)
- **Foreign Key Index**: `user_id` (for efficient user todo lookups)
- **Composite Index**: `(user_id, created_at DESC)` for paginated queries (future optimization)

### Constraints

- **Primary Key**: `id` must be unique and not null
- **Foreign Key**: `user_id` references `users.id`
  - **ON DELETE CASCADE**: Deleting a user deletes all their todos
  - **ON UPDATE CASCADE**: Updating user.id updates all related todos (unlikely scenario)
- **NOT NULL**: `title`, `user_id`, `is_completed`, `created_at`, `updated_at` cannot be null
- **Title Length**: Maximum 500 characters (application validates before insert)

### SQLModel Definition (Pseudocode)

```python
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=500)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (not a database column)
    user: User = Relationship(back_populates="todos")
```

### Validation Rules

- **Title**:
  - Required (not null, not empty string)
  - Maximum length: 500 characters
  - Trimmed of leading/trailing whitespace before insert

- **Description**:
  - Optional (can be null or empty)
  - No maximum length (TEXT field)
  - Trimmed of leading/trailing whitespace if provided

- **is_completed**:
  - Boolean value only (true/false)
  - Defaults to false on creation

- **Timestamps**:
  - `created_at`: Set once on creation, never updated
  - `updated_at`: Set on creation, updated on every modification

### Data Examples

```json
{
  "id": "660f9511-f3ac-52e5-b827-557766551111",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Complete Phase II implementation",
  "description": "Build full-stack todo app with FastAPI backend and Next.js frontend",
  "is_completed": false,
  "created_at": "2026-01-03T10:05:00Z",
  "updated_at": "2026-01-03T10:05:00Z"
}
```

---

## Relationships

### User → Todo (One-to-Many)

**Description**: One user can have many todos. Each todo belongs to exactly one user.

**Implementation**:
- Foreign key `todos.user_id` references `users.id`
- Cascade delete: When a user is deleted, all their todos are deleted
- Index on `user_id` for fast lookups

**Query Patterns**:
```sql
-- Get all todos for a specific user
SELECT * FROM todos WHERE user_id = '550e8400-e29b-41d4-a716-446655440000';

-- Get user with their todos (join)
SELECT u.*, t.*
FROM users u
LEFT JOIN todos t ON u.id = t.user_id
WHERE u.id = '550e8400-e29b-41d4-a716-446655440000';
```

---

## Database Schema (SQL DDL)

### Create Users Table

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for email lookups (authentication)
CREATE INDEX idx_users_email ON users(email);
```

### Create Todos Table

```sql
CREATE TABLE todos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Index for user todo lookups
CREATE INDEX idx_todos_user_id ON todos(user_id);

-- Composite index for paginated queries (future optimization)
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC);
```

### Update Trigger for updated_at

```sql
-- Function to automatically update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function before updates
CREATE TRIGGER update_todos_updated_at
    BEFORE UPDATE ON todos
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

---

## Migration Strategy

### Initial Migration (Create Tables)

**Migration Name**: `001_create_users_and_todos_tables`

**Up Migration**:
1. Create `users` table
2. Create index on `users.email`
3. Create `todos` table
4. Create index on `todos.user_id`
5. Create composite index on `todos(user_id, created_at DESC)`
6. Create `update_updated_at_column()` function
7. Create trigger `update_todos_updated_at`

**Down Migration**:
1. Drop trigger `update_todos_updated_at`
2. Drop function `update_updated_at_column()`
3. Drop table `todos` (CASCADE to drop indexes)
4. Drop table `users` (CASCADE to drop indexes)

### Migration Tool

Use Alembic with SQLModel for schema migrations:

```bash
# Generate migration
alembic revision --autogenerate -m "create_users_and_todos_tables"

# Apply migration
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

---

## Data Access Patterns

### Common Queries

**1. Get User by Email (Authentication)**
```sql
SELECT id, email, password_hash, created_at
FROM users
WHERE email = $1;
```

**2. Get All Todos for User**
```sql
SELECT id, title, description, is_completed, created_at, updated_at
FROM todos
WHERE user_id = $1
ORDER BY created_at DESC;
```

**3. Get Single Todo (with ownership check)**
```sql
SELECT id, user_id, title, description, is_completed, created_at, updated_at
FROM todos
WHERE id = $1 AND user_id = $2;
```

**4. Create Todo**
```sql
INSERT INTO todos (id, user_id, title, description, is_completed, created_at, updated_at)
VALUES ($1, $2, $3, $4, $5, NOW(), NOW())
RETURNING *;
```

**5. Update Todo**
```sql
UPDATE todos
SET title = $1, description = $2, updated_at = NOW()
WHERE id = $3 AND user_id = $4
RETURNING *;
```

**6. Toggle Todo Completion**
```sql
UPDATE todos
SET is_completed = NOT is_completed, updated_at = NOW()
WHERE id = $1 AND user_id = $2
RETURNING *;
```

**7. Delete Todo**
```sql
DELETE FROM todos
WHERE id = $1 AND user_id = $2
RETURNING id;
```

---

## Performance Considerations

### Phase II Scale (100 concurrent users, up to 1000 todos per user)

**Estimated Database Size**:
- Users: 100 rows × ~300 bytes = ~30 KB
- Todos: 100,000 rows × ~600 bytes = ~60 MB
- Total: ~60 MB (well within Neon free tier)

**Index Strategy**:
- Primary key indexes: Automatic, O(log n) lookups
- `users.email` index: Fast authentication lookups
- `todos.user_id` index: Fast user todo list retrieval
- Composite index `(user_id, created_at)`: Optimized for pagination (future use)

**Query Performance**:
- User authentication: < 10ms (indexed email lookup)
- Get todos for user: < 50ms (indexed user_id lookup, up to 1000 rows)
- CRUD operations: < 20ms (primary key lookups)

**Connection Pooling**:
- SQLAlchemy default pool size: 5 connections
- Sufficient for Phase II scale (100 concurrent users with request/response pattern)
- No connection exhaustion expected

---

## Data Integrity

### Referential Integrity
- Foreign key constraint ensures every todo belongs to a valid user
- CASCADE delete ensures orphaned todos are cleaned up when user is deleted

### Data Consistency
- Timestamps default to server time (UTC) for consistency
- `updated_at` automatically updated via trigger
- Boolean defaults prevent null confusion

### Validation Layers
1. **Database Level**: NOT NULL, UNIQUE, FOREIGN KEY constraints
2. **ORM Level**: SQLModel field validation
3. **API Level**: Pydantic schema validation
4. **Application Level**: Business logic validation in services

---

## Security Considerations

### Password Security
- Passwords never stored in plain text
- Hashing handled by Better Auth (bcrypt with appropriate cost factor)
- Password hash field is VARCHAR(255) to accommodate hash format

### Data Isolation
- Every todo query includes `user_id` filter (via `WHERE user_id = $1`)
- Foreign key constraint prevents invalid user references
- No cross-user data access possible at database level

### SQL Injection Prevention
- All queries use parameterized statements (no string concatenation)
- SQLModel/SQLAlchemy handles parameterization automatically
- Input validation prevents malicious payloads

---

## Backup and Recovery

**Neon Managed Backups**:
- Automatic continuous backups
- Point-in-time recovery (PITR) available
- No manual backup configuration required for Phase II

**Data Export** (if needed):
```bash
# Export users table
pg_dump -h [neon-host] -U [user] -t users -d [database] > users_backup.sql

# Export todos table
pg_dump -h [neon-host] -U [user] -t todos -d [database] > todos_backup.sql
```

---

## Future Considerations (Out of Phase II Scope)

**Potential Phase III+ Enhancements**:
- Todo categories (new table `categories`, many-to-many relationship)
- Todo tags (new table `tags`, many-to-many relationship)
- Todo priorities (add `priority` column to todos)
- Todo due dates (add `due_date` column to todos)
- User profile data (extend `users` table with additional fields)
- Shared todos (new table `todo_shares`, many-to-many relationship)
- Soft delete (add `deleted_at` column, modify queries to filter deleted records)
- Audit trail (new table `audit_log` for change history)

---

## Phase II Compliance

✓ Two entities only (User, Todo)
✓ Simple one-to-many relationship
✓ No advanced features (categories, tags, sharing)
✓ No soft delete or audit trail
✓ Standard PostgreSQL types (no custom types)
✓ Indexes for performance without over-optimization
✓ Neon PostgreSQL (Phase II approved technology)

---

## Summary

The Phase II data model is intentionally simple and focused on core functionality:
- **2 entities** (User, Todo)
- **1 relationship** (User has many Todos)
- **7 fields per entity** (minimal but sufficient)
- **3 indexes** (primary keys + user_id + email)
- **Clean foreign key cascade** (user deletion cleans up todos)

This design supports all Phase II requirements while remaining easy to understand, test, and maintain.
