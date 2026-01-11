# Tasks: Phase II Full-Stack Todo App

**Feature**: Full-Stack Todo Web Application
**Date**: 2026-01-03
**Phase**: Implementation Tasks
**Status**: Ready for Implementation

## Overview

This document breaks down the Phase II plan into atomic, testable implementation tasks. Tasks are organized by phase and user story priority, following the dependency order defined in the specification and plan.

**Total Task Count**: 52 tasks
**Estimated Completion**: Sequential implementation by user story

---

## Task Organization

Tasks are grouped into the following phases:

1. **Phase 1: Project Setup** (T001-T004) - Initialize projects and dependencies
2. **Phase 2: Foundational Infrastructure** (T005-T011) - Database, auth infrastructure (blocks all user stories)
3. **Phase 3: User Story 1 - Authentication** (T012-T019) - Signup/Signin (P1)
4. **Phase 4: User Story 2 - View Todos** (T020-T023) - Read todos (P2)
5. **Phase 5: User Story 3 - Create Todo** (T024-T027) - Create todos (P3)
6. **Phase 6: User Story 4 - Edit Todo** (T028-T031) - Update todos (P4)
7. **Phase 7: User Story 5 - Delete Todo** (T032-T035) - Delete todos (P5)
8. **Phase 8: User Story 6 - Toggle Completion** (T036-T039) - Toggle status (P6)
9. **Phase 9: Polish & Cross-Cutting** (T040-T052) - Integration, error handling, responsive UI

Each user story phase is **independently testable** after completion.

---

## Phase 1: Project Setup

### Backend Setup

- [X] T001 [Setup] Initialize FastAPI backend project in backend/
  - **Preconditions**: Python 3.11+ installed
  - **Actions**:
    - Create `backend/` directory
    - Initialize Python virtual environment
    - Create `requirements.txt` with: fastapi, uvicorn, sqlmodel, pydantic, psycopg2-binary, alembic, python-dotenv, pytest
    - Create `backend/src/` directory structure
    - Create `backend/tests/` directory structure
  - **Artifacts**: `backend/requirements.txt`, `backend/src/`, `backend/tests/`
  - **Acceptance**: `pip install -r requirements.txt` succeeds, directories exist
  - **References**: plan.md sections "Project Structure", "Backend Architecture"

- [X] T002 [Setup] Create backend project structure and configuration in backend/
  - **Preconditions**: T001 completed
  - **Actions**:
    - Create `backend/src/main.py` (FastAPI app entry point)
    - Create `backend/src/config.py` (environment configuration)
    - Create `backend/src/database.py` (database connection setup)
    - Create `backend/.env.example` (template for environment variables)
    - Create `backend/alembic.ini` (Alembic configuration)
    - Create `backend/pytest.ini` (pytest configuration)
  - **Artifacts**: `backend/src/main.py`, `backend/src/config.py`, `backend/src/database.py`, `backend/.env.example`, `backend/alembic.ini`, `backend/pytest.ini`
  - **Acceptance**: `uvicorn src.main:app --reload` starts without errors
  - **References**: plan.md "Project Structure", quickstart.md "Backend Setup"

### Frontend Setup

- [X] T003 [Setup] Initialize Next.js frontend project in frontend/
  - **Preconditions**: Node.js 18+ installed
  - **Actions**:
    - Run `npx create-next-app@latest frontend` with TypeScript, App Router, Tailwind CSS
    - Install dependencies: `better-auth-client` (or equivalent auth SDK)
    - Create `frontend/src/app/` directory (App Router pages)
    - Create `frontend/src/components/` directory
    - Create `frontend/src/services/` directory (API communication)
    - Create `frontend/src/types/` directory (TypeScript types)
    - Create `frontend/src/hooks/` directory (custom React hooks)
  - **Artifacts**: `frontend/package.json`, `frontend/src/app/`, `frontend/src/components/`, `frontend/src/services/`, `frontend/src/types/`, `frontend/src/hooks/`
  - **Acceptance**: `npm run dev` starts Next.js server successfully
  - **References**: plan.md "Project Structure", "Frontend Architecture"

- [X] T004 [Setup] Configure frontend environment and API communication in frontend/
  - **Preconditions**: T003 completed
  - **Actions**:
    - Create `frontend/.env.local.example` (template for environment variables)
    - Create `frontend/src/services/api.ts` (Fetch API wrapper with base URL, credentials, error handling)
    - Configure Tailwind CSS with responsive breakpoints
    - Create `frontend/src/types/api.ts` (API request/response TypeScript types)
  - **Artifacts**: `frontend/.env.local.example`, `frontend/src/services/api.ts`, `frontend/tailwind.config.js`, `frontend/src/types/api.ts`
  - **Acceptance**: API service can make test fetch request to placeholder endpoint
  - **References**: plan.md "API Communication Layer", research.md "Decision 8"

---

## Phase 2: Foundational Infrastructure

### Database and Models

- [X] T005 [P1] [Foundational] Create User data model in backend/src/models/user.py
  - **Preconditions**: T002 completed, database.py configured
  - **Actions**:
    - Define `User` SQLModel with fields: id (UUID), email (unique, indexed), password_hash, created_at
    - Add email validation (format, max 255 chars)
    - Add relationship to Todo model (one-to-many)
    - Include Pydantic schema for API serialization
  - **Artifacts**: `backend/src/models/user.py`
  - **Acceptance**: Model imports without errors, includes all required fields and constraints
  - **References**: data-model.md "Entity: User", spec.md "Data Models"

- [X] T006 [P2] [Foundational] Create Todo data model in backend/src/models/todo.py
  - **Preconditions**: T005 completed
  - **Actions**:
    - Define `Todo` SQLModel with fields: id (UUID), user_id (FK to User), title (max 500), description (nullable), is_completed (default false), created_at, updated_at
    - Add foreign key constraint with ON DELETE CASCADE
    - Add validation for title (required, max 500 chars)
    - Add relationship to User model
    - Include Pydantic schema for API serialization
  - **Artifacts**: `backend/src/models/todo.py`
  - **Acceptance**: Model imports without errors, foreign key relationship established
  - **References**: data-model.md "Entity: Todo", spec.md "Data Models"

- [X] T007 [Foundational] Configure Neon PostgreSQL connection in backend/src/database.py
  - **Preconditions**: T002 completed, Neon account created
  - **Actions**:
    - Import SQLModel engine creation utilities
    - Read `DATABASE_URL` from environment variable
    - Create SQLAlchemy engine with connection pooling (pool_pre_ping=True)
    - Create session factory
    - Implement `get_session()` dependency for FastAPI
    - Add connection health check function
  - **Artifacts**: `backend/src/database.py` (updated)
  - **Acceptance**: Database connection succeeds with valid Neon connection string
  - **References**: research.md "Decision 4", quickstart.md "Database Setup"

- [X] T008 [Foundational] Initialize Alembic and create initial migration in backend/alembic/
  - **Preconditions**: T005, T006, T007 completed
  - **Actions**:
    - Run `alembic init alembic` to create migration structure
    - Update `alembic/env.py` to import SQLModel metadata
    - Generate initial migration: `alembic revision --autogenerate -m "create_users_and_todos_tables"`
    - Review migration file for User and Todo table creation
    - Add trigger for `updated_at` auto-update on Todo table
  - **Artifacts**: `backend/alembic/versions/001_create_users_and_todos_tables.py`
  - **Acceptance**: Migration file includes both tables with all constraints and indexes
  - **References**: data-model.md "Migration Strategy", quickstart.md "Initialize Database"

- [X] T009 [Foundational] Apply database migrations and verify schema in Neon (MANUAL: Requires Neon connection string - see SETUP_INSTRUCTIONS.md)
  - **Preconditions**: T008 completed, Neon connection configured
  - **Actions**:
    - Run `alembic upgrade head` to apply initial migration
    - Verify tables exist in Neon console: `users`, `todos`
    - Verify indexes exist: `users.email`, `todos.user_id`
    - Verify foreign key constraint: `todos.user_id` → `users.id` with CASCADE
    - Test connection with simple query
  - **Artifacts**: Database schema in Neon
  - **Acceptance**: Tables and indexes exist, foreign key constraint works
  - **References**: data-model.md "Database Schema", quickstart.md "Initialize Database"

### Authentication Infrastructure

- [X] T010 [P1] [Foundational] Integrate Better Auth SDK in backend/src/services/auth_service.py (Implemented JWT-based auth service)
  - **Preconditions**: T005 completed, Better Auth account created
  - **Actions**:
    - Install Better Auth Python SDK (or equivalent)
    - Create `AuthService` class
    - Implement `signup(email, password)` method (calls Better Auth API, creates User record)
    - Implement `signin(email, password)` method (validates credentials, returns session token)
    - Implement `verify_session(token)` method (validates session with Better Auth)
    - Add password hashing with bcrypt
    - Configure Better Auth API keys from environment
  - **Artifacts**: `backend/src/services/auth_service.py`
  - **Acceptance**: Service methods successfully call Better Auth API with test credentials
  - **References**: research.md "Decision 3", plan.md "Authentication Integration"

- [X] T011 [P1] [Foundational] Create authentication middleware in backend/src/api/middleware.py
  - **Preconditions**: T010 completed
  - **Actions**:
    - Create `require_auth` FastAPI dependency
    - Extract session token from HTTP-only cookie or Authorization header
    - Call `AuthService.verify_session()` to validate token
    - Return authenticated user object if valid
    - Raise 401 Unauthorized if session invalid or missing
    - Add CORS middleware configuration (allow frontend origin)
  - **Artifacts**: `backend/src/api/middleware.py`
  - **Acceptance**: Middleware correctly blocks unauthenticated requests, allows valid sessions
  - **References**: research.md "Decision 6", plan.md "Session Management"

---

## Phase 3: User Story 1 - Authentication (P1)

**User Story**: As a user, I want to sign up and sign in so that I can access my personal todo list.

### Backend Authentication Endpoints

- [X] T012 [P1] [US1] Create authentication API schemas in backend/src/schemas/auth_schemas.py
  - **Preconditions**: T005 completed
  - **Actions**:
    - Define `SignupRequest` Pydantic schema (email, password with validation)
    - Define `SignupResponse` Pydantic schema (message, user_id)
    - Define `SigninRequest` Pydantic schema (email, password)
    - Define `SigninResponse` Pydantic schema (message, user: {id, email})
    - Define `ErrorResponse` Pydantic schema (error message)
  - **Artifacts**: `backend/src/schemas/auth_schemas.py`
  - **Acceptance**: All schemas validate according to OpenAPI specification
  - **References**: contracts/openapi.yaml "Authentication Endpoints", spec.md "API Endpoints"

- [X] T013 [P1] [US1] Implement POST /auth/signup endpoint in backend/src/api/auth.py
  - **Preconditions**: T010, T012 completed
  - **Actions**:
    - Create FastAPI router for authentication endpoints
    - Implement `POST /auth/signup` endpoint
    - Validate email format and password length (min 8 chars)
    - Check for existing user with same email (return 409 Conflict)
    - Call `AuthService.signup()` to create user
    - Return 201 Created with user_id
    - Handle errors (400 validation, 409 duplicate email, 500 server error)
  - **Artifacts**: `backend/src/api/auth.py` (POST /auth/signup)
  - **Acceptance**: Endpoint creates user in database, returns correct status codes and response format
  - **References**: contracts/openapi.yaml "POST /auth/signup", spec.md "FR-001"

- [X] T014 [P1] [US1] Implement POST /auth/signin endpoint in backend/src/api/auth.py
  - **Preconditions**: T010, T012, T013 completed
  - **Actions**:
    - Implement `POST /auth/signin` endpoint
    - Validate request body (email, password)
    - Call `AuthService.signin()` to verify credentials
    - Return session cookie (HTTP-only, Secure, SameSite=Lax) on success
    - Return 200 OK with user info (id, email) on success
    - Return 401 Unauthorized if credentials invalid
  - **Artifacts**: `backend/src/api/auth.py` (POST /auth/signin)
  - **Acceptance**: Endpoint validates credentials, sets session cookie, returns user info
  - **References**: contracts/openapi.yaml "POST /auth/signin", spec.md "FR-002"

- [X] T015 [P1] [US1] Implement POST /auth/signout endpoint in backend/src/api/auth.py
  - **Preconditions**: T011, T014 completed
  - **Actions**:
    - Implement `POST /auth/signout` endpoint (requires authentication)
    - Use `require_auth` middleware dependency
    - Clear session cookie (set Max-Age=0)
    - Invalidate session in Better Auth
    - Return 200 OK with success message
  - **Artifacts**: `backend/src/api/auth.py` (POST /auth/signout)
  - **Acceptance**: Endpoint clears session, subsequent requests with old session fail authentication
  - **References**: contracts/openapi.yaml "POST /auth/signout", spec.md "FR-003"

### Frontend Authentication Pages

- [X] T016 [P1] [US1] Create authentication TypeScript types in frontend/src/types/auth.ts
  - **Preconditions**: T004 completed
  - **Actions**:
    - Define `SignupRequest` interface
    - Define `SignupResponse` interface
    - Define `SigninRequest` interface
    - Define `SigninResponse` interface
    - Define `User` interface (id, email)
    - Define `AuthState` interface (user, loading, error)
  - **Artifacts**: `frontend/src/types/auth.ts`
  - **Acceptance**: Types match backend API contracts exactly
  - **References**: contracts/openapi.yaml schemas, spec.md "Frontend TypeScript Types"

- [X] T017 [P1] [US1] Create authentication service in frontend/src/services/authService.ts
  - **Preconditions**: T004, T016 completed
  - **Actions**:
    - Implement `signup(email, password): Promise<SignupResponse>` method
    - Implement `signin(email, password): Promise<SigninResponse>` method
    - Implement `signout(): Promise<void>` method
    - Use `api.ts` wrapper with credentials: 'include' for cookies
    - Handle API errors and map to user-friendly messages
  - **Artifacts**: `frontend/src/services/authService.ts`
  - **Acceptance**: All methods correctly call backend API endpoints and handle responses
  - **References**: spec.md "Frontend Interaction Flows - Authentication Flow"

- [X] T018 [P1] [US1] Create signup page at frontend/src/app/auth/signup/page.tsx
  - **Preconditions**: T017 completed
  - **Actions**:
    - Create signup page component with form (email, password fields)
    - Add client-side validation (email format, password min 8 chars)
    - Call `authService.signup()` on form submit
    - Display loading state during API call
    - On success: redirect to signin page with success message
    - On error: display validation errors inline below fields
    - Add link to signin page
    - Style with Tailwind CSS (responsive for mobile/desktop)
  - **Artifacts**: `frontend/src/app/auth/signup/page.tsx`
  - **Acceptance**: User can complete signup flow, see appropriate feedback messages
  - **References**: spec.md "AC-001-1", "AC-001-2", "Frontend Interaction Flows - Signup Flow"

- [X] T019 [P1] [US1] Create signin page at frontend/src/app/auth/signin/page.tsx
  - **Preconditions**: T017 completed
  - **Actions**:
    - Create signin page component with form (email, password fields)
    - Call `authService.signin()` on form submit
    - Display loading state during API call
    - On success: store session (handled by cookies), redirect to `/todos`
    - On error: display authentication error message
    - Add link to signup page
    - Style with Tailwind CSS (responsive)
  - **Artifacts**: `frontend/src/app/auth/signin/page.tsx`
  - **Acceptance**: User can sign in, session persists, redirects to todo list
  - **References**: spec.md "AC-002-1", "AC-002-2", "Frontend Interaction Flows - Signin Flow"

**US1 Acceptance Test**: After T019, user can signup, signin, and signout. Session persists across page reloads.

---

## Phase 4: User Story 2 - View Todos (P2)

**User Story**: As a signed-in user, I want to view all my todos so that I can see what I need to do.

### Backend View Todos Endpoint

- [X] T020 [P2] [US2] Create todo service in backend/src/services/todo_service.py
  - **Preconditions**: T006 completed
  - **Actions**:
    - Create `TodoService` class
    - Implement `get_todos(user_id: UUID) -> list[Todo]` method
    - Query todos filtered by user_id, ordered by created_at DESC
    - Ensure user can only access their own todos
    - Return empty list if no todos
  - **Artifacts**: `backend/src/services/todo_service.py` (get_todos method)
  - **Acceptance**: Service correctly retrieves todos for specific user, enforces data isolation
  - **References**: spec.md "FR-007", data-model.md "Query Patterns"

- [X] T021 [P2] [US2] Create todo API schemas in backend/src/schemas/todo_schemas.py
  - **Preconditions**: T006 completed
  - **Actions**:
    - Define `TodoResponse` Pydantic schema (id, title, description, is_completed, created_at, updated_at)
    - Define `TodoListResponse` Pydantic schema (todos: list[TodoResponse])
    - Define `CreateTodoRequest` Pydantic schema (title, description optional)
    - Define `UpdateTodoRequest` Pydantic schema (title, description optional)
  - **Artifacts**: `backend/src/schemas/todo_schemas.py`
  - **Acceptance**: Schemas match OpenAPI specification exactly
  - **References**: contracts/openapi.yaml "Todo Schemas"

- [X] T022 [P2] [US2] Implement GET /todos endpoint in backend/src/api/todos.py
  - **Preconditions**: T011, T020, T021 completed
  - **Actions**:
    - Create FastAPI router for todo endpoints
    - Implement `GET /todos` endpoint (requires authentication)
    - Use `require_auth` middleware to get current user
    - Call `TodoService.get_todos(user.id)` to fetch todos
    - Return 200 OK with `TodoListResponse`
    - Return empty array if user has no todos
  - **Artifacts**: `backend/src/api/todos.py` (GET /todos)
  - **Acceptance**: Endpoint returns all todos for authenticated user, empty array for new user
  - **References**: contracts/openapi.yaml "GET /todos", spec.md "FR-007"

### Frontend View Todos Page

- [X] T023 [P2] [US2] Create todo list page at frontend/src/app/todos/page.tsx
  - **Preconditions**: T019, T022 completed
  - **Actions**:
    - Create protected todo list page (requires authentication)
    - Call `GET /todos` API on page load
    - Display loading state while fetching todos
    - Render list of todos with: title, description, completion status
    - Handle empty state with helpful message ("No todos yet. Create your first todo!")
    - Add signout button in header
    - Redirect to signin page if not authenticated
    - Style with Tailwind CSS (responsive list layout)
  - **Artifacts**: `frontend/src/app/todos/page.tsx`
  - **Acceptance**: User sees their todos, empty state if none exist, can signout
  - **References**: spec.md "AC-003-1", "AC-003-2", "Frontend Interaction Flows - View Todos Flow"

**US2 Acceptance Test**: After T023, signed-in user can view their todo list (empty or with todos from other stories).

---

## Phase 5: User Story 3 - Create Todo (P3)

**User Story**: As a signed-in user, I want to create a new todo so that I can track tasks I need to complete.

### Backend Create Todo Endpoint

- [X] T024 [P3] [US3] Implement create_todo method in backend/src/services/todo_service.py
  - **Preconditions**: T020 completed
  - **Actions**:
    - Add `create_todo(user_id: UUID, title: str, description: str | None) -> Todo` method
    - Validate title is not empty and max 500 chars
    - Create new Todo with user_id, title, description, is_completed=False
    - Save to database and return created todo
  - **Artifacts**: `backend/src/services/todo_service.py` (create_todo method)
  - **Acceptance**: Service creates todo with correct user association and default values
  - **References**: spec.md "FR-008", data-model.md "Create Todo"

- [X] T025 [P3] [US3] Implement POST /todos endpoint in backend/src/api/todos.py
  - **Preconditions**: T011, T021, T024 completed
  - **Actions**:
    - Implement `POST /todos` endpoint (requires authentication)
    - Use `require_auth` middleware to get current user
    - Validate request body with `CreateTodoRequest` schema
    - Call `TodoService.create_todo(user.id, title, description)`
    - Return 201 Created with `TodoResponse`
    - Return 400 Bad Request if validation fails (title empty, title too long)
  - **Artifacts**: `backend/src/api/todos.py` (POST /todos)
  - **Acceptance**: Endpoint creates todo, returns correct status codes, enforces user ownership
  - **References**: contracts/openapi.yaml "POST /todos", spec.md "FR-008"

### Frontend Create Todo UI

- [X] T026 [P3] [US3] Create todo service in frontend/src/services/todoService.ts
  - **Preconditions**: T004 completed
  - **Actions**:
    - Implement `getTodos(): Promise<TodoListResponse>` method
    - Implement `createTodo(title, description): Promise<TodoResponse>` method
    - Implement `updateTodo(id, title, description): Promise<TodoResponse>` method
    - Implement `deleteTodo(id): Promise<void>` method
    - Implement `toggleComplete(id): Promise<TodoResponse>` method
    - Use `api.ts` wrapper with credentials: 'include'
  - **Artifacts**: `frontend/src/services/todoService.ts`
  - **Acceptance**: All methods correctly call backend API endpoints
  - **References**: spec.md "Frontend Interaction Flows"

- [X] T027 [P3] [US3] Add create todo form to frontend/src/app/todos/page.tsx
  - **Preconditions**: T023, T025, T026 completed
  - **Actions**:
    - Add "Add Todo" button above todo list
    - Create inline form or modal with title and description fields
    - Add client-side validation (title required, max 500 chars)
    - Call `todoService.createTodo()` on submit
    - On success: add new todo to list, clear form
    - On error: display validation errors
    - Style with Tailwind CSS (responsive form)
  - **Artifacts**: `frontend/src/app/todos/page.tsx` (updated with create form)
  - **Acceptance**: User can create todo, see it immediately in list, form resets
  - **References**: spec.md "AC-004-1", "AC-004-2", "Frontend Interaction Flows - Create Todo Flow"

**US3 Acceptance Test**: After T027, user can create new todos with title and optional description.

---

## Phase 6: User Story 4 - Edit Todo (P4)

**User Story**: As a signed-in user, I want to edit an existing todo so that I can update its details.

### Backend Update Todo Endpoint

- [X] T028 [P4] [US4] Implement update_todo method in backend/src/services/todo_service.py
  - **Preconditions**: T024 completed
  - **Actions**:
    - Add `update_todo(user_id: UUID, todo_id: UUID, title: str, description: str | None) -> Todo` method
    - Validate title is not empty and max 500 chars
    - Find todo by id and user_id (enforce ownership)
    - Raise 404 Not Found if todo doesn't exist
    - Raise 403 Forbidden if todo belongs to different user
    - Update title and description, save to database
    - updated_at timestamp automatically updated by trigger
    - Return updated todo
  - **Artifacts**: `backend/src/services/todo_service.py` (update_todo method)
  - **Acceptance**: Service updates todo only if user owns it, rejects unauthorized updates
  - **References**: spec.md "FR-009", data-model.md "Update Todo"

- [X] T029 [P4] [US4] Implement PUT /todos/:id endpoint in backend/src/api/todos.py
  - **Preconditions**: T011, T021, T028 completed
  - **Actions**:
    - Implement `PUT /todos/{id}` endpoint (requires authentication)
    - Use `require_auth` middleware to get current user
    - Validate request body with `UpdateTodoRequest` schema
    - Call `TodoService.update_todo(user.id, id, title, description)`
    - Return 200 OK with `TodoResponse`
    - Return 400 Bad Request if validation fails
    - Return 403 Forbidden if user doesn't own todo
    - Return 404 Not Found if todo doesn't exist
  - **Artifacts**: `backend/src/api/todos.py` (PUT /todos/:id)
  - **Acceptance**: Endpoint updates todo, enforces ownership, returns correct status codes
  - **References**: contracts/openapi.yaml "PUT /todos/:id", spec.md "FR-009"

### Frontend Edit Todo UI

- [X] T030 [P4] [US4] Create TodoItem component in frontend/src/components/TodoItem.tsx
  - **Preconditions**: T023 completed
  - **Actions**:
    - Create reusable TodoItem component (display mode)
    - Props: todo object, onEdit, onDelete, onToggle callbacks
    - Display title, description, completion status
    - Add edit button, delete button, completion toggle checkbox
    - Style with Tailwind CSS (responsive card layout)
  - **Artifacts**: `frontend/src/components/TodoItem.tsx`
  - **Acceptance**: Component renders todo with action buttons
  - **References**: plan.md "Frontend Component Structure"

- [X] T031 [P4] [US4] Add edit functionality to todo list in frontend/src/app/todos/page.tsx
  - **Preconditions**: T027, T029, T030 completed
  - **Actions**:
    - Add edit mode state to TodoItem or inline edit form
    - On edit button click: show edit form with pre-filled values
    - Add cancel button to discard changes
    - Call `todoService.updateTodo(id, title, description)` on submit
    - On success: update todo in list view
    - On error: display validation errors
    - Use TodoItem component to render each todo
  - **Artifacts**: `frontend/src/app/todos/page.tsx` (updated with edit functionality)
  - **Acceptance**: User can edit todo, see changes immediately, cancel to discard
  - **References**: spec.md "AC-005-1", "AC-005-2", "Frontend Interaction Flows - Edit Todo Flow"

**US4 Acceptance Test**: After T031, user can edit existing todos and see updated values.

---

## Phase 7: User Story 5 - Delete Todo (P5)

**User Story**: As a signed-in user, I want to delete a todo so that I can remove completed or unwanted tasks.

### Backend Delete Todo Endpoint

- [X] T032 [P5] [US5] Implement delete_todo method in backend/src/services/todo_service.py
  - **Preconditions**: T028 completed
  - **Actions**:
    - Add `delete_todo(user_id: UUID, todo_id: UUID) -> None` method
    - Find todo by id and user_id (enforce ownership)
    - Raise 404 Not Found if todo doesn't exist
    - Raise 403 Forbidden if todo belongs to different user
    - Delete todo from database
  - **Artifacts**: `backend/src/services/todo_service.py` (delete_todo method)
  - **Acceptance**: Service deletes todo only if user owns it, rejects unauthorized deletes
  - **References**: spec.md "FR-010", data-model.md "Delete Todo"

- [X] T033 [P5] [US5] Implement DELETE /todos/:id endpoint in backend/src/api/todos.py
  - **Preconditions**: T011, T032 completed
  - **Actions**:
    - Implement `DELETE /todos/{id}` endpoint (requires authentication)
    - Use `require_auth` middleware to get current user
    - Call `TodoService.delete_todo(user.id, id)`
    - Return 200 OK with success message
    - Return 403 Forbidden if user doesn't own todo
    - Return 404 Not Found if todo doesn't exist
  - **Artifacts**: `backend/src/api/todos.py` (DELETE /todos/:id)
  - **Acceptance**: Endpoint deletes todo, enforces ownership, returns correct status codes
  - **References**: contracts/openapi.yaml "DELETE /todos/:id", spec.md "FR-010"

### Frontend Delete Todo UI

- [X] T034 [P5] [US5] Add confirmation dialog component in frontend/src/components/ConfirmDialog.tsx
  - **Preconditions**: T030 completed
  - **Actions**:
    - Create reusable ConfirmDialog component
    - Props: isOpen, title, message, onConfirm, onCancel
    - Show overlay with confirm/cancel buttons
    - Style with Tailwind CSS (responsive modal)
  - **Artifacts**: `frontend/src/components/ConfirmDialog.tsx`
  - **Acceptance**: Dialog component displays and handles user actions
  - **References**: plan.md "Frontend Component Structure"

- [X] T035 [P5] [US5] Add delete functionality to todo list in frontend/src/app/todos/page.tsx
  - **Preconditions**: T031, T033, T034 completed
  - **Actions**:
    - On delete button click: show ConfirmDialog
    - On confirm: call `todoService.deleteTodo(id)`
    - On success: remove todo from list view
    - On error: display error message, keep todo in list
    - On cancel: close dialog, no changes
  - **Artifacts**: `frontend/src/app/todos/page.tsx` (updated with delete functionality)
  - **Acceptance**: User can delete todo after confirmation, todo removed from UI
  - **References**: spec.md "AC-006-1", "AC-006-2", "Frontend Interaction Flows - Delete Todo Flow"

**US5 Acceptance Test**: After T035, user can delete todos with confirmation dialog.

---

## Phase 8: User Story 6 - Toggle Completion (P6)

**User Story**: As a signed-in user, I want to mark todos as complete or incomplete so that I can track my progress.

### Backend Toggle Completion Endpoint

- [X] T036 [P6] [US6] Implement toggle_complete method in backend/src/services/todo_service.py
  - **Preconditions**: T032 completed
  - **Actions**:
    - Add `toggle_complete(user_id: UUID, todo_id: UUID) -> Todo` method
    - Find todo by id and user_id (enforce ownership)
    - Raise 404 Not Found if todo doesn't exist
    - Raise 403 Forbidden if todo belongs to different user
    - Toggle is_completed boolean (true ↔ false)
    - Save to database (updated_at auto-updated)
    - Return updated todo
  - **Artifacts**: `backend/src/services/todo_service.py` (toggle_complete method)
  - **Acceptance**: Service toggles completion status, enforces ownership
  - **References**: spec.md "FR-011", data-model.md "Toggle Todo Completion"

- [X] T037 [P6] [US6] Implement PATCH /todos/:id/complete endpoint in backend/src/api/todos.py
  - **Preconditions**: T011, T036 completed
  - **Actions**:
    - Implement `PATCH /todos/{id}/complete` endpoint (requires authentication)
    - Use `require_auth` middleware to get current user
    - Call `TodoService.toggle_complete(user.id, id)`
    - Return 200 OK with `TodoResponse` (updated is_completed value)
    - Return 403 Forbidden if user doesn't own todo
    - Return 404 Not Found if todo doesn't exist
  - **Artifacts**: `backend/src/api/todos.py` (PATCH /todos/:id/complete)
  - **Acceptance**: Endpoint toggles completion, returns updated todo
  - **References**: contracts/openapi.yaml "PATCH /todos/:id/complete", spec.md "FR-011"

### Frontend Toggle Completion UI

- [X] T038 [P6] [US6] Update TodoItem component with completion toggle in frontend/src/components/TodoItem.tsx
  - **Preconditions**: T030 completed
  - **Actions**:
    - Add checkbox or toggle switch for completion status
    - Style completed todos differently (strikethrough text, muted color)
    - Pass onToggle callback from parent
    - Provide immediate visual feedback on click
  - **Artifacts**: `frontend/src/components/TodoItem.tsx` (updated with toggle)
  - **Acceptance**: Component shows completion status visually, handles toggle click
  - **References**: plan.md "Frontend Component Structure"

- [X] T039 [P6] [US6] Add toggle completion functionality to todo list in frontend/src/app/todos/page.tsx
  - **Preconditions**: T035, T037, T038 completed
  - **Actions**:
    - On toggle click: call `todoService.toggleComplete(id)` immediately
    - Optimistically update UI (show new status before API response)
    - On success: confirm UI state matches API response
    - On error: revert UI state, display error message
  - **Artifacts**: `frontend/src/app/todos/page.tsx` (updated with toggle functionality)
  - **Acceptance**: User can toggle completion, see immediate visual feedback
  - **References**: spec.md "AC-007-1", "AC-007-2", "Frontend Interaction Flows - Toggle Completion Flow"

**US6 Acceptance Test**: After T039, user can toggle todo completion status with immediate visual feedback.

---

## Phase 9: Polish & Cross-Cutting Concerns

### Integration and Configuration

- [ ] T040 [Integration] Connect frontend root layout to auth state in frontend/src/app/layout.tsx
  - **Preconditions**: T019 completed
  - **Actions**:
    - Create root layout component
    - Add Better Auth provider or custom AuthContext
    - Implement useAuth hook to access auth state globally
    - Handle session initialization on app load
    - Provide user info to all pages
  - **Artifacts**: `frontend/src/app/layout.tsx`, `frontend/src/hooks/useAuth.ts`
  - **Acceptance**: Auth state available throughout app, session persists across reloads
  - **References**: research.md "Decision 7", plan.md "Session Management"

- [ ] T041 [Integration] Implement protected route logic in frontend/src/app/todos/layout.tsx
  - **Preconditions**: T040 completed
  - **Actions**:
    - Create todos layout that checks authentication
    - Redirect to signin if not authenticated
    - Show loading state while checking session
    - Use useAuth hook to access current user
  - **Artifacts**: `frontend/src/app/todos/layout.tsx`
  - **Acceptance**: Unauthenticated users redirected to signin, authenticated users see todos
  - **References**: spec.md "Frontend Interaction Flows - Unauthorized Access"

- [ ] T042 [Integration] Configure CORS and session cookies in backend/src/main.py
  - **Preconditions**: T011 completed
  - **Actions**:
    - Add CORS middleware with allowed origins from environment
    - Configure session cookie settings (HTTP-only, Secure, SameSite=Lax, Max-Age)
    - Set CORS credentials to true
    - Register all API routers (auth, todos)
    - Add root health check endpoint (GET /)
  - **Artifacts**: `backend/src/main.py` (updated with CORS and routers)
  - **Acceptance**: Frontend can call backend API with credentials, session cookies work
  - **References**: research.md "Decision 6", quickstart.md "CORS Configuration"

### Error Handling

- [ ] T043 [Error Handling] Add global error handler in backend/src/main.py
  - **Preconditions**: T042 completed
  - **Actions**:
    - Add FastAPI exception handler for 400, 401, 403, 404, 500 errors
    - Return consistent `ErrorResponse` schema for all errors
    - Log errors with appropriate severity
    - Return user-friendly error messages (no stack traces in production)
  - **Artifacts**: `backend/src/main.py` (updated with exception handler)
  - **Acceptance**: All API errors return consistent format with appropriate status codes
  - **References**: spec.md "API Validation and Error Handling", contracts/openapi.yaml "ErrorResponse"

- [ ] T044 [Error Handling] Add API error handling in frontend/src/services/api.ts
  - **Preconditions**: T004 completed
  - **Actions**:
    - Parse API error responses and extract error message
    - Map HTTP status codes to user-friendly messages
    - Handle network errors (timeout, connection refused)
    - Handle 401 errors specifically (redirect to signin on session expiration)
    - Provide default error message for unexpected errors
  - **Artifacts**: `frontend/src/services/api.ts` (updated with error handling)
  - **Acceptance**: API errors display user-friendly messages, session expiration redirects to signin
  - **References**: spec.md "Frontend Interaction Flows - Error Handling Flows"

- [ ] T045 [Error Handling] Add error boundary component in frontend/src/components/ErrorBoundary.tsx
  - **Preconditions**: T040 completed
  - **Actions**:
    - Create React ErrorBoundary component
    - Catch rendering errors and display fallback UI
    - Log errors to console (or error tracking service if configured)
    - Provide "Try Again" button to reset error state
  - **Artifacts**: `frontend/src/components/ErrorBoundary.tsx`
  - **Acceptance**: App doesn't crash on component errors, shows fallback UI
  - **References**: plan.md "Frontend Component Structure"

### UI Polish and Responsiveness

- [ ] T046 [UI] Add responsive navigation in frontend/src/components/Navigation.tsx
  - **Preconditions**: T040 completed
  - **Actions**:
    - Create Navigation component with app title, signout button
    - Show user email in header when authenticated
    - Use Tailwind responsive breakpoints (mobile: hamburger menu, desktop: horizontal nav)
    - Style with consistent color scheme
  - **Artifacts**: `frontend/src/components/Navigation.tsx`
  - **Acceptance**: Navigation works on mobile and desktop, signout button accessible
  - **References**: research.md "Decision 9", spec.md "NFR-001"

- [ ] T047 [UI] Add loading states to all async operations in frontend/
  - **Preconditions**: T039 completed
  - **Actions**:
    - Add loading spinners to signup, signin, and signout buttons
    - Add loading skeleton to todo list while fetching
    - Add loading states to create, edit, delete, toggle operations
    - Disable submit buttons during async operations to prevent double-submission
  - **Artifacts**: Updated pages and components with loading states
  - **Acceptance**: All async operations show loading feedback, buttons disabled during operations
  - **References**: spec.md "SC-003"

- [ ] T048 [UI] Add empty state handling to todo list in frontend/src/app/todos/page.tsx
  - **Preconditions**: T023 completed
  - **Actions**:
    - Display empty state message when user has no todos
    - Add illustration or icon for empty state
    - Include call-to-action ("Create your first todo!")
    - Style with Tailwind CSS
  - **Artifacts**: `frontend/src/app/todos/page.tsx` (updated with empty state)
  - **Acceptance**: Empty state is helpful and encourages user to create first todo
  - **References**: spec.md "AC-003-2"

- [ ] T049 [UI] Implement responsive layout for mobile in frontend/
  - **Preconditions**: T046 completed
  - **Actions**:
    - Verify all pages work on mobile viewport (320px+)
    - Adjust form layouts for mobile (single column)
    - Ensure touch targets are at least 44x44px
    - Test on mobile breakpoint (Tailwind sm: 640px)
    - Adjust todo list layout for mobile (cards stack vertically)
  - **Artifacts**: Updated pages with responsive styles
  - **Acceptance**: App is fully functional on mobile and desktop
  - **References**: spec.md "NFR-001", research.md "Decision 9 - Responsive Strategy"

### Testing and Documentation

- [ ] T050 [Testing] Write backend unit tests in backend/tests/
  - **Preconditions**: All backend endpoints completed (T015, T022, T025, T029, T033, T037)
  - **Actions**:
    - Create `tests/unit/test_todo_service.py` (test TodoService methods)
    - Create `tests/unit/test_auth_service.py` (test AuthService methods)
    - Mock database interactions
    - Test validation logic, error cases, edge cases
    - Achieve >80% code coverage for services
  - **Artifacts**: `backend/tests/unit/test_todo_service.py`, `backend/tests/unit/test_auth_service.py`
  - **Acceptance**: `pytest` runs successfully, all unit tests pass
  - **References**: research.md "Decision 10", plan.md "Testing Strategy"

- [ ] T051 [Testing] Write backend integration tests in backend/tests/
  - **Preconditions**: T050 completed
  - **Actions**:
    - Create `tests/integration/test_auth_api.py` (test auth endpoints)
    - Create `tests/integration/test_todo_api.py` (test todo endpoints)
    - Use FastAPI TestClient with test database
    - Test full request/response cycles
    - Test authentication and authorization
    - Test error cases (401, 403, 404)
  - **Artifacts**: `backend/tests/integration/test_auth_api.py`, `backend/tests/integration/test_todo_api.py`
  - **Acceptance**: Integration tests pass, API contracts verified
  - **References**: research.md "Decision 10", plan.md "Testing Strategy"

- [X] T052 [Documentation] Create environment setup documentation in README.md
  - **Preconditions**: All setup tasks completed (T001-T004)
  - **Actions**:
    - Create root README.md with project overview
    - Document prerequisites (Python, Node.js, Neon, Better Auth accounts)
    - Link to quickstart.md for detailed setup
    - Document project structure
    - Document available scripts (backend: uvicorn, pytest; frontend: dev, build, test)
    - Include architecture diagram reference
  - **Artifacts**: `README.md`
  - **Acceptance**: README provides clear project overview and links to setup guide
  - **References**: quickstart.md, plan.md

---

## Dependency Graph

### Critical Path (Must Complete Sequentially)

```
Setup (T001-T004)
  ↓
Foundational (T005-T011) [BLOCKS ALL USER STORIES]
  ↓
US1: Authentication (T012-T019) [BLOCKS US2-US6]
  ↓
US2: View Todos (T020-T023) [BLOCKS US3-US6]
  ↓
US3: Create Todo (T024-T027) [BLOCKS US4-US6 testing]
  ↓
US4: Edit Todo (T028-T031)
  ↓
US5: Delete Todo (T032-T035)
  ↓
US6: Toggle Completion (T036-T039)
  ↓
Polish (T040-T052)
```

### Parallelizable Tasks (Can Execute Concurrently)

**Within Foundational Phase**:
- T005 (User model) + T006 (Todo model) can run in parallel after T002
- T010 (Auth service) can run in parallel with T005-T009 (database setup)

**Within US1 (Authentication)**:
- T012 (Backend schemas) + T016 (Frontend types) can run in parallel after T010
- T013, T014, T015 (Backend endpoints) can run sequentially, but T017 (Frontend service) can start after T016
- T018 (Signup page) + T019 (Signin page) can run in parallel after T017

**Within US2 (View Todos)**:
- T020 (Todo service) + T021 (Todo schemas) can run in parallel after T006
- T023 (Frontend page) can start immediately after T019 (doesn't need T022 completed for UI development)

**Within US3-US6**:
- Backend service method + Frontend service method can be developed in parallel
- Backend endpoint + Frontend component can be developed in parallel (with contract as source of truth)

**Within Polish Phase**:
- T043, T044, T045 (Error handling) can run in parallel after T042
- T046, T047, T048, T049 (UI polish) can run in parallel after T045
- T050, T051 (Testing) can run in parallel after all endpoints completed

---

## Phase II Compliance

All tasks strictly comply with Phase II constitutional constraints:

✓ **No Docker/Kubernetes**: Using standard hosting (Neon managed database, standard deployment)
✓ **No Background Jobs**: All operations synchronous request/response
✓ **No Real-time Features**: No WebSockets, no Socket.io
✓ **No Message Queues**: No Kafka, no RabbitMQ
✓ **No AI/Agents**: No OpenAI SDK, no LangChain
✓ **No Microservices**: Single backend API, single frontend app
✓ **Phase II Technologies Only**: FastAPI, SQLModel, Neon, Next.js, Better Auth

---

## Acceptance Criteria Summary

Each user story has testable acceptance criteria that MUST pass before proceeding to next phase:

- **US1 (Authentication)**: User can signup, signin, signout. Session persists across reloads.
- **US2 (View Todos)**: User can view their todo list. Empty state displays helpful message.
- **US3 (Create Todo)**: User can create new todo with title and optional description.
- **US4 (Edit Todo)**: User can edit existing todo. Changes reflect immediately.
- **US5 (Delete Todo)**: User can delete todo after confirmation.
- **US6 (Toggle Completion)**: User can mark todo complete/incomplete with visual feedback.

---

## References

- **Specification**: `specs/002-fullstack-web-app/spec.md`
- **Plan**: `specs/002-fullstack-web-app/plan.md`
- **Data Model**: `specs/002-fullstack-web-app/data-model.md`
- **API Contracts**: `specs/002-fullstack-web-app/contracts/openapi.yaml`
- **Research**: `specs/002-fullstack-web-app/research.md`
- **Quickstart**: `specs/002-fullstack-web-app/quickstart.md`
- **Constitution**: `.specify/memory/constitution.md`

---

**End of Tasks Document**
