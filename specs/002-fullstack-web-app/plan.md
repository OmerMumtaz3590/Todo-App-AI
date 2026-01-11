# Implementation Plan: Full-Stack Todo Web Application

**Branch**: `002-fullstack-web-app` | **Date**: 2026-01-03 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/002-fullstack-web-app/spec.md`

**Note**: This plan defines HOW the Phase II full-stack todo web application will be built, strictly derived from the specification and constitution.

## Summary

Build a full-stack web application that implements all 5 Basic Level Todo features (create, read, update, delete, toggle completion) with multi-user authentication. The backend provides a RESTful API using FastAPI with Neon PostgreSQL for persistence. The frontend is a responsive Next.js application with Better Auth integration for user signup/signin. The system ensures complete data isolation between users, with all todos associated with their owning user.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/JavaScript (frontend with Next.js 14+)
**Primary Dependencies**:
- Backend: FastAPI (web framework), SQLModel (ORM), Pydantic (validation), Better Auth SDK (authentication)
- Frontend: Next.js 14+, React, TypeScript, Better Auth Client
**Storage**: Neon Serverless PostgreSQL (cloud-hosted PostgreSQL database)
**Testing**: pytest (backend unit/integration tests), Jest/React Testing Library (frontend tests)
**Target Platform**: Web application (backend API server + frontend web server)
**Project Type**: Web application (separate backend and frontend codebases)
**Performance Goals**:
- API response time < 2 seconds for all operations
- Support 100+ concurrent authenticated users
- Page load time < 5 seconds for todo list view
**Constraints**:
- No Docker/Kubernetes (Phase II prohibition)
- No background jobs or async workers (Phase II prohibition)
- No real-time features/WebSockets (Phase II prohibition)
- No AI/agent frameworks (Phase II prohibition)
- Session-based authentication only (no OAuth/SSO in Phase II)
**Scale/Scope**:
- Target: 100+ concurrent users
- Up to 1000 todos per user without pagination
- Single backend API server and single frontend web server

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Phase Compliance** (per Constitution Section III):
- [x] Current phase identified: Phase II (Full-Stack Web)
- [x] No future-phase technologies used (RULE PG-002) - No Docker, Kubernetes, Kafka, AI agents
- [x] Architecture appropriate for current phase (RULE PG-003) - Web application with REST API, database, and frontend

**Spec-Driven Compliance** (per Constitution Section I):
- [x] Specification approved before this plan (RULE SDD-004) - spec.md exists and passed validation
- [x] No features beyond specification scope (RULE SDD-002) - All features derived from spec requirements

**Technology Compliance** (per Constitution Section IV):
- [x] Only phase-appropriate technologies used (RULE TC-001):
  - Python REST API ✓ (Phase II allowed)
  - Neon PostgreSQL ✓ (Phase II allowed)
  - Next.js ✓ (Phase II allowed)
  - Better Auth ✓ (Phase II allowed)
  - FastAPI ✓ (Phase II allowed)
  - SQLModel ✓ (Phase II allowed)
- [x] Additional libraries justified (RULE TC-003):
  - Pydantic: Required for FastAPI request/response validation
  - React Testing Library: Industry standard for frontend testing
  - JWT library: Required for Better Auth session management

**Quality Compliance** (per Constitution Section V):
- [x] Clean architecture principles followed (RULE QP-001 to QP-004):
  - Backend: Models → Services → API Controllers (layered architecture)
  - Frontend: Pages → Components → API Services (layered architecture)
  - Domain logic in services, not controllers or components
- [x] Type hints planned for all public functions (RULE QP-008):
  - Python backend uses type hints throughout
  - TypeScript frontend provides static typing
- [x] Error handling strategy defined (RULE QP-009):
  - Backend: HTTP status codes with JSON error responses
  - Frontend: User-friendly error messages with inline validation

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web-app/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (database schema)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   └── openapi.yaml     # OpenAPI 3.0 specification
├── checklists/          # Quality validation
│   └── requirements.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application structure (backend + frontend)

backend/
├── src/
│   ├── models/          # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py      # User model
│   │   └── todo.py      # Todo model
│   ├── services/        # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py      # Authentication logic
│   │   └── todo_service.py      # Todo CRUD logic
│   ├── api/             # FastAPI controllers/routes
│   │   ├── __init__.py
│   │   ├── auth.py      # Auth endpoints (/auth/*)
│   │   └── todos.py     # Todo endpoints (/todos/*)
│   ├── schemas/         # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── auth_schemas.py
│   │   └── todo_schemas.py
│   ├── config.py        # Configuration (env vars, database connection)
│   ├── database.py      # Database session management
│   └── main.py          # FastAPI app entry point
├── tests/
│   ├── unit/            # Unit tests (services, models)
│   ├── integration/     # Integration tests (API endpoints)
│   └── conftest.py      # Pytest fixtures
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── README.md            # Backend setup instructions

frontend/
├── src/
│   ├── app/             # Next.js App Router pages
│   │   ├── layout.tsx   # Root layout with auth provider
│   │   ├── page.tsx     # Home/redirect page
│   │   ├── auth/
│   │   │   ├── signup/
│   │   │   │   └── page.tsx    # Signup page
│   │   │   └── signin/
│   │   │       └── page.tsx    # Signin page
│   │   └── todos/
│   │       └── page.tsx         # Todo list page (protected)
│   ├── components/      # Reusable React components
│   │   ├── TodoList.tsx
│   │   ├── TodoItem.tsx
│   │   ├── TodoForm.tsx
│   │   ├── AuthForm.tsx
│   │   └── Layout.tsx
│   ├── services/        # API communication layer
│   │   ├── authService.ts       # Auth API calls
│   │   └── todoService.ts       # Todo API calls
│   ├── types/           # TypeScript type definitions
│   │   ├── auth.ts
│   │   └── todo.ts
│   ├── hooks/           # Custom React hooks
│   │   ├── useAuth.ts   # Authentication state hook
│   │   └── useTodos.ts  # Todo data management hook
│   └── lib/             # Utility functions
│       └── api.ts       # Axios/fetch configuration
├── public/              # Static assets
├── tests/               # Frontend tests
│   └── components/
├── package.json         # Node dependencies
├── tsconfig.json        # TypeScript configuration
├── next.config.js       # Next.js configuration
├── .env.local.example   # Environment variable template
└── README.md            # Frontend setup instructions

# Root level
.env                     # Environment variables (gitignored)
.gitignore
README.md                # Project overview and setup
```

**Structure Decision**: Web application structure (Option 2) selected because the specification explicitly requires separate backend REST API and frontend web application. Backend provides API endpoints for authentication and todo management. Frontend consumes these APIs and handles user interface and interaction. This separation allows independent development, testing, and deployment of backend and frontend components while maintaining clear API contracts.

## Complexity Tracking

> **No violations** - all architecture decisions comply with Phase II constitution constraints.

---

## Phase 0: Research & Technology Decisions

### Research Questions

The following technology decisions need research and justification:

1. **FastAPI vs Flask vs Django REST Framework**: Which Python web framework best fits Phase II requirements?
2. **SQLModel vs SQLAlchemy vs Raw SQL**: Which data layer approach balances simplicity with type safety?
3. **Better Auth Integration**: How to integrate Better Auth with FastAPI backend and Next.js frontend?
4. **Neon PostgreSQL Connection**: Best practices for connecting to Neon Serverless PostgreSQL from FastAPI?
5. **Next.js App Router vs Pages Router**: Which routing approach for Next.js 14+?
6. **Session Management Strategy**: How to handle authentication sessions between frontend and backend?
7. **Frontend State Management**: Do we need Redux/Zustand or is React state sufficient?
8. **API Communication**: Fetch vs Axios vs custom abstraction?

### Research Findings

*(To be populated by research agents - see research.md)*

Key decisions to be documented:
- Web framework choice and rationale
- ORM/data layer choice and rationale
- Authentication integration pattern
- Session management approach (cookies, JWT, headers)
- Frontend state management strategy
- API communication approach

---

## Phase 1: Design Artifacts

### Data Model

*(To be generated in data-model.md)*

Expected entities:
1. **User**:
   - id (primary key, UUID)
   - email (unique, indexed)
   - password_hash (hashed with bcrypt)
   - created_at (timestamp)

2. **Todo**:
   - id (primary key, UUID)
   - user_id (foreign key to User, indexed)
   - title (string, required, max 500 chars)
   - description (text, optional)
   - is_completed (boolean, default false)
   - created_at (timestamp)
   - updated_at (timestamp)

Relationships:
- User has many Todos (one-to-many)
- Todo belongs to one User (foreign key constraint with ON DELETE CASCADE)

### API Contracts

*(To be generated in contracts/openapi.yaml)*

Expected endpoints (from spec.md):

**Authentication Endpoints:**
- POST /auth/signup - Create new user account
- POST /auth/signin - Authenticate user and establish session
- POST /auth/signout - End user session

**Todo CRUD Endpoints:**
- GET /todos - Retrieve all todos for authenticated user
- POST /todos - Create new todo
- GET /todos/:id - Retrieve specific todo
- PUT /todos/:id - Update existing todo
- DELETE /todos/:id - Remove todo
- PATCH /todos/:id/complete - Toggle completion status

Each endpoint will include:
- Request schema (parameters, body, headers)
- Response schema (success and error cases)
- Authentication requirements
- HTTP status codes
- Example requests/responses

### Quickstart Guide

*(To be generated in quickstart.md)*

Expected sections:
1. Prerequisites (Python 3.11+, Node.js 18+, Neon account)
2. Backend setup (install dependencies, configure .env, run migrations, start server)
3. Frontend setup (install dependencies, configure .env, start dev server)
4. Database setup (Neon connection string, schema initialization)
5. Better Auth configuration (API keys, frontend/backend integration)
6. Running tests
7. Common issues and troubleshooting

---

## Architecture Decisions

### Backend Architecture

**Framework: FastAPI**
- RESTful API framework for Python
- Automatic OpenAPI documentation generation
- Built-in request/response validation with Pydantic
- Async support (though not required for Phase II)
- Type hints throughout for better IDE support

**Data Layer: SQLModel**
- Type-safe ORM built on SQLAlchemy and Pydantic
- Single model definition for database and API schemas
- Excellent integration with FastAPI
- Automatic validation and serialization

**Database: Neon PostgreSQL**
- Serverless PostgreSQL (cloud-hosted, managed)
- No manual infrastructure management (complies with Phase II)
- Connection pooling handled by Neon
- Automatic backups and scaling

**Authentication: Better Auth**
- Managed authentication service
- Handles password hashing, session management
- Provides ready-made signup/signin endpoints
- Integrates with both backend and frontend

**Layered Architecture:**
1. **API Layer** (FastAPI controllers):
   - Handle HTTP requests/responses
   - Request validation
   - Authentication verification
   - Delegate to service layer

2. **Service Layer** (Business logic):
   - Todo CRUD operations
   - User authorization checks
   - Data validation beyond schema validation

3. **Model Layer** (SQLModel):
   - Database schema definitions
   - Relationships
   - Basic field validation

4. **Database Layer**:
   - Connection management
   - Session handling
   - Query execution

### Frontend Architecture

**Framework: Next.js 14+**
- React framework with App Router
- Server-side rendering (SSR) for better SEO and performance
- File-based routing
- Built-in TypeScript support

**Authentication: Better Auth Client**
- Frontend SDK for Better Auth
- Session state management
- Automatic token handling
- Protected route patterns

**Component Structure:**
1. **Pages** (App Router):
   - Route-level components
   - Data fetching coordination
   - Layout composition

2. **Components**:
   - Reusable UI elements
   - Presentational logic
   - Form handling

3. **Services**:
   - API communication
   - HTTP client configuration
   - Request/response transformation

4. **Hooks**:
   - Custom React hooks for auth state
   - Custom React hooks for todo data
   - Reusable stateful logic

**State Management:**
- React state and Context API (no Redux needed for Phase II)
- useAuth hook for authentication state
- useTodos hook for todo list state
- Local component state for forms and UI

**Responsive Design:**
- Mobile-first CSS approach
- Tailwind CSS for utility-first styling
- Responsive breakpoints for desktop/mobile
- Touch-friendly UI controls

### Integration Architecture

**Frontend ↔ Backend Flow:**
1. Frontend sends HTTP request to backend API
2. Backend validates authentication (session/token)
3. Backend processes request through service layer
4. Backend returns JSON response
5. Frontend updates UI based on response

**Authentication Flow:**
1. **Signup:**
   - Frontend: POST /auth/signup with email/password
   - Backend: Validate, hash password, create user
   - Backend: Return success
   - Frontend: Redirect to signin

2. **Signin:**
   - Frontend: POST /auth/signin with credentials
   - Backend: Verify credentials via Better Auth
   - Backend: Create session, return session token/cookie
   - Frontend: Store session, redirect to /todos

3. **Authenticated Requests:**
   - Frontend: Include session token in request headers/cookies
   - Backend: Verify token with Better Auth
   - Backend: Extract user ID from session
   - Backend: Process request with user context

**Error Handling Flow:**
1. Backend returns appropriate HTTP status code (400, 401, 403, 404, 500)
2. Backend includes error message in JSON response body
3. Frontend displays user-friendly error message
4. Frontend provides actionable recovery (retry, correct input, re-authenticate)

### Database Architecture

**Schema Design:**
- Two tables: users and todos
- Foreign key relationship (todos.user_id → users.id)
- Indexes on: users.email, todos.user_id
- Timestamps for audit trail

**Migration Strategy:**
- SQLModel/Alembic for schema migrations
- Version-controlled migration scripts
- Forward-only migrations (no automatic rollback in Phase II)
- Manual verification before applying to production

**Connection Management:**
- Connection pooling via SQLModel/SQLAlchemy
- Environment variable for Neon connection string
- Automatic reconnection on connection loss
- Connection limits appropriate for Phase II scale

### Development Environment

**Backend Development:**
- Python virtual environment (venv)
- FastAPI development server with auto-reload
- Pytest for automated testing
- .env file for local configuration

**Frontend Development:**
- Node.js environment
- Next.js development server with hot reload
- Jest + React Testing Library for testing
- .env.local for local configuration

**Database Development:**
- Neon free tier or development tier
- Separate database for development vs production
- Sample data scripts for testing

**Local Integration:**
- Backend runs on localhost:8000
- Frontend runs on localhost:3000
- Frontend configured to proxy API requests to backend
- CORS configured on backend to allow frontend origin

---

## Non-Functional Requirements

### Performance
- API response time < 2 seconds per specification
- Frontend page load < 5 seconds per specification
- Database queries optimized with proper indexes
- No N+1 query problems

### Security
- Passwords hashed with bcrypt (via Better Auth)
- SQL injection prevention via parameterized queries (SQLModel)
- Authentication required for all todo endpoints
- User authorization checks (users can only access own todos)
- HTTPS in production (enforced by hosting)
- Environment variables for secrets

### Scalability
- Support 100+ concurrent users per specification
- Stateless API servers (session in database/Better Auth)
- Connection pooling for database
- Horizontal scaling ready (though not implemented in Phase II)

### Maintainability
- Type hints throughout backend code
- TypeScript throughout frontend code
- Clean architecture with clear layer boundaries
- Comprehensive tests (unit and integration)
- API documentation via OpenAPI/Swagger

### Reliability
- Error handling at all layers
- User-friendly error messages
- Graceful degradation on errors
- Database transactions for data integrity

---

## Testing Strategy

### Backend Testing
1. **Unit Tests** (services layer):
   - Todo service CRUD operations
   - Authorization logic
   - Input validation

2. **Integration Tests** (API layer):
   - API endpoint behavior
   - Authentication requirements
   - Error responses
   - Database interactions

3. **Test Database**:
   - Separate Neon database for tests
   - Reset between test runs
   - Sample data fixtures

### Frontend Testing
1. **Component Tests**:
   - TodoList rendering
   - TodoItem interactions
   - Form validation
   - Error displays

2. **Integration Tests**:
   - Authentication flows
   - Todo CRUD flows
   - API error handling

3. **Mock API**:
   - Mock API responses for tests
   - Test error scenarios
   - Test loading states

---

## Deployment Considerations (Phase II Scope)

**Note:** Phase II does not include Docker/Kubernetes or advanced deployment automation.

**Backend Deployment:**
- Deploy to platform supporting Python web apps (e.g., Railway, Render, Heroku)
- Environment variables configured in hosting platform
- Neon connection string in production environment
- HTTPS enforced

**Frontend Deployment:**
- Deploy to Next.js-compatible hosting (e.g., Vercel, Netlify)
- Environment variables configured in hosting platform
- Backend API URL configured for production
- Static assets served via CDN

**Database:**
- Neon production tier
- Automatic backups by Neon
- Connection string kept secure

---

## Constraints and Limitations

**Phase II Constraints (enforced by constitution):**
- No Docker/Kubernetes containerization
- No background jobs or async workers
- No real-time features (WebSockets)
- No message queues or event streaming
- No AI or agent frameworks
- No microservices architecture
- No advanced caching (Redis, etc.)

**Functional Limitations (per spec):**
- No password reset functionality
- No email verification
- No OAuth/social login
- No todo categories/tags/priorities
- No todo search or filtering
- No todo sharing or collaboration
- No pagination (up to 1000 todos per user)
- No audit trail or change history

---

## Next Steps

1. **Phase 0 Complete:** Generate research.md with technology decisions
2. **Phase 1 Complete:** Generate data-model.md, contracts/openapi.yaml, quickstart.md
3. **Update Agent Context:** Run update-agent-context script
4. **Phase 2:** Execute `/sp.tasks` to generate task breakdown from this plan
5. **Implementation:** Execute `/sp.implement` to build the application per tasks

---

**Constitution Compliance Final Check:** ✓ All requirements met, no violations
