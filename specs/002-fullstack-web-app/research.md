# Research & Technology Decisions: Phase II Full-Stack Todo App

**Feature**: Full-Stack Todo Web Application
**Date**: 2026-01-03
**Phase**: Phase 0 (Research)

## Overview

This document captures technology research and decision rationale for the Phase II full-stack implementation. All decisions comply with the Phase II constitution constraints and support the requirements defined in spec.md.

---

## Decision 1: Backend Web Framework

**Decision**: FastAPI

**Rationale**:
- **Automatic API Documentation**: FastAPI generates interactive OpenAPI/Swagger docs automatically, meeting the spec requirement for documented API endpoints
- **Type Safety**: Built-in Pydantic integration provides request/response validation with Python type hints (RULE QP-008 compliance)
- **Performance**: ASGI-based framework with async support (though not required for Phase II, provides future scalability)
- **Developer Experience**: Excellent IDE autocomplete and type checking due to type hints throughout
- **Modern Python**: Designed for Python 3.7+ with full type hint support
- **Ecosystem Integration**: Works seamlessly with SQLModel and Pydantic for end-to-end type safety

**Alternatives Considered**:
1. **Flask**:
   - Pros: Simpler, more established, larger ecosystem
   - Cons: No automatic API documentation, manual validation setup, less type-safe
   - Rejected: Requires more boilerplate for validation and documentation

2. **Django REST Framework**:
   - Pros: Comprehensive, batteries-included, admin interface
   - Cons: Heavy for a simple CRUD API, ORM tightly coupled to Django
   - Rejected: Overkill for Phase II requirements, slower development for simple APIs

**Implementation Impact**:
- Automatic OpenAPI spec generation reduces manual documentation effort
- Type hints enable better IDE support and catch errors at development time
- Pydantic schemas ensure request/response validation consistency

---

## Decision 2: ORM / Data Layer

**Decision**: SQLModel

**Rationale**:
- **Unified Models**: Single model definition for both database and API schemas reduces duplication
- **Type Safety**: Full type hint support integrates with FastAPI's Pydantic validation
- **SQLAlchemy Foundation**: Built on SQLAlchemy, providing battle-tested ORM functionality
- **Migration Support**: Compatible with Alembic for database migrations
- **Neon Compatibility**: Works seamlessly with PostgreSQL/Neon via standard connection string
- **Simplicity**: Less boilerplate than raw SQLAlchemy while maintaining power

**Alternatives Considered**:
1. **SQLAlchemy**:
   - Pros: Mature, feature-rich, widely used
   - Cons: More verbose, requires separate Pydantic models for API validation
   - Rejected: SQLModel provides SQLAlchemy power with less boilerplate

2. **Raw SQL with psycopg2**:
   - Pros: Maximum control, no ORM overhead
   - Cons: No automatic migrations, manual validation, SQL injection risk if not careful
   - Rejected: Too much manual work, doesn't meet type safety requirements (RULE QP-008)

3. **Tortoise ORM**:
   - Pros: Async-first, similar to Django ORM
   - Cons: Less mature, smaller ecosystem, async not required for Phase II
   - Rejected: SQLModel's FastAPI integration is superior for synchronous operations

**Implementation Impact**:
- User and Todo models defined once, used for database and API
- Automatic validation at database and API layers
- Type-safe queries reduce runtime errors

---

## Decision 3: Authentication Integration

**Decision**: Better Auth with custom FastAPI integration

**Rationale**:
- **Managed Service**: Better Auth handles password hashing, session management, security best practices
- **Phase II Requirement**: Specification explicitly requires Better Auth for signup/signin
- **Multi-Platform**: Provides both backend SDK and frontend client
- **Security**: Implements industry-standard security patterns (bcrypt hashing, secure sessions)
- **Session Management**: Handles token generation, validation, expiration automatically

**Integration Strategy**:
- **Backend**: Integrate Better Auth SDK with FastAPI middleware for authentication
- **Frontend**: Use Better Auth React SDK for client-side session management
- **Session Storage**: Better Auth manages sessions (likely database-backed or JWT-based)
- **API Protection**: FastAPI dependencies verify Better Auth sessions before allowing access to protected endpoints

**Alternatives Considered**:
1. **Custom Auth Implementation**:
   - Pros: Full control, no external dependency
   - Cons: Security-critical code, requires expertise, violates spec requirement
   - Rejected: Specification mandates Better Auth, custom implementation is risky

2. **Auth0 / OAuth Providers**:
   - Pros: Enterprise-grade, social login support
   - Cons: Out of Phase II scope (spec prohibits OAuth/SSO), adds complexity
   - Rejected: Phase II limited to email/password auth only

**Implementation Impact**:
- Better Auth SDK integrated into FastAPI app initialization
- Session verification as FastAPI dependency for protected routes
- Frontend SDK provides useAuth hook for authentication state

---

## Decision 4: Neon PostgreSQL Connection

**Decision**: Standard PostgreSQL connection via SQLModel/SQLAlchemy with Neon connection string

**Rationale**:
- **Standard Protocol**: Neon uses standard PostgreSQL wire protocol
- **No Special Client**: Standard PostgreSQL drivers work without modification
- **Connection Pooling**: SQLAlchemy provides connection pooling automatically
- **Environment Config**: Connection string stored in environment variable for security
- **Serverless Benefits**: Neon handles scaling, backups, high availability automatically

**Connection Strategy**:
```python
# Connection string format
DATABASE_URL = "postgresql://[user]:[password]@[neon-hostname]/[database]?sslmode=require"

# SQLModel engine creation with connection pooling
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
```

**Best Practices**:
- Use SSL/TLS connection (sslmode=require)
- Enable connection pool pre-ping to handle connection drops
- Set appropriate pool size for Phase II scale (default: 5-10 connections)
- Use environment variables for connection string (never commit credentials)

**Implementation Impact**:
- Standard PostgreSQL connection eliminates vendor lock-in
- Connection pooling handles concurrent requests efficiently
- Automatic reconnection on transient failures

---

## Decision 5: Next.js Routing Approach

**Decision**: Next.js 14+ App Router

**Rationale**:
- **Modern Standard**: App Router is the recommended approach for Next.js 14+
- **Server Components**: Better performance with server-side rendering by default
- **Layouts**: Shared layouts reduce code duplication
- **Loading States**: Built-in loading.tsx pattern for better UX
- **Error Handling**: Built-in error.tsx pattern for error boundaries
- **File-Based**: Intuitive file system routing matches URL structure

**Routing Structure**:
```
src/app/
├── layout.tsx           # Root layout with auth provider
├── page.tsx             # Home page (redirect to /todos or /auth/signin)
├── auth/
│   ├── signup/
│   │   └── page.tsx     # /auth/signup
│   └── signin/
│       └── page.tsx     # /auth/signin
└── todos/
    └── page.tsx         # /todos (protected route)
```

**Alternatives Considered**:
1. **Pages Router**:
   - Pros: More established, larger community knowledge base
   - Cons: Being phased out, less modern features, more client-side work
   - Rejected: App Router is the future, better for new projects

**Implementation Impact**:
- Server components reduce client-side JavaScript bundle size
- Built-in loading and error states improve UX
- Layout system eliminates navigation component duplication

---

## Decision 6: Session Management Strategy

**Decision**: HTTP-only cookies with Better Auth session tokens

**Rationale**:
- **Security**: HTTP-only cookies prevent XSS attacks (JavaScript cannot access)
- **Automatic Handling**: Browsers automatically include cookies in requests
- **CSRF Protection**: SameSite cookie attribute prevents CSRF attacks
- **Better Auth Standard**: Better Auth uses cookie-based sessions by default
- **Simplicity**: No manual token management in frontend code

**Session Flow**:
1. User signs in via POST /auth/signin
2. Backend verifies credentials with Better Auth
3. Better Auth creates session, returns session cookie (HTTP-only, Secure, SameSite)
4. Browser automatically includes cookie in subsequent requests
5. Backend verifies session cookie with Better Auth on each protected request

**Alternatives Considered**:
1. **JWT in localStorage**:
   - Pros: Stateless, works with mobile apps
   - Cons: Vulnerable to XSS, not HTTP-only, manual token management
   - Rejected: Less secure than HTTP-only cookies for web apps

2. **JWT in Authorization header**:
   - Pros: Stateless, explicit control
   - Cons: Requires manual token storage and refresh, vulnerable to XSS if stored in localStorage
   - Rejected: More complex with minimal benefit for Phase II

**Implementation Impact**:
- Frontend doesn't need to manually manage tokens
- Backend session verification is automatic with Better Auth middleware
- Secure by default with HTTP-only and Secure flags

---

## Decision 7: Frontend State Management

**Decision**: React Context API + Custom Hooks (no Redux/Zustand)

**Rationale**:
- **Simplicity**: Phase II requirements don't justify Redux complexity
- **Built-in**: Context API is part of React core, no external dependency
- **Sufficient Scope**: Authentication state and todo list state are simple enough for Context
- **Custom Hooks**: useAuth and useTodos provide clean API for components
- **Phase II Scale**: 100 concurrent users don't require advanced state optimization

**State Architecture**:
1. **Authentication State** (AuthContext + useAuth hook):
   - Current user
   - Session status (loading, authenticated, unauthenticated)
   - Sign in/out functions

2. **Todo State** (TodosContext + useTodos hook):
   - Todo list
   - Loading states
   - CRUD operations (create, update, delete, toggle)

3. **Local Component State**:
   - Form inputs
   - UI toggles
   - Temporary validation errors

**Alternatives Considered**:
1. **Redux Toolkit**:
   - Pros: Powerful, dev tools, time-travel debugging
   - Cons: Boilerplate overhead, learning curve, overkill for simple state
   - Rejected: Phase II state management is simple enough for Context API

2. **Zustand**:
   - Pros: Simple API, minimal boilerplate
   - Cons: External dependency, Context API sufficient for Phase II
   - Rejected: Context API meets requirements without adding dependencies

**Implementation Impact**:
- Less boilerplate than Redux
- No external state management library needed
- Easy to upgrade to Redux/Zustand in Phase III if needed

---

## Decision 8: API Communication Layer

**Decision**: Native Fetch API with custom wrapper utility

**Rationale**:
- **No External Dependency**: Fetch is built into modern browsers
- **Sufficient Features**: Fetch handles all Phase II requirements (GET, POST, PUT, DELETE, headers)
- **Custom Wrapper**: Thin wrapper adds error handling, authentication, base URL configuration
- **Type Safety**: TypeScript ensures request/response typing
- **Lightweight**: No additional bundle size from HTTP libraries

**API Utility Structure**:
```typescript
// lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export async function apiRequest<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    credentials: 'include', // Include cookies
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'API request failed');
  }

  return response.json();
}
```

**Alternatives Considered**:
1. **Axios**:
   - Pros: Feature-rich, interceptors, automatic JSON parsing
   - Cons: External dependency, larger bundle size, overkill for simple CRUD
   - Rejected: Fetch API sufficient for Phase II, no need for extra dependency

2. **React Query / SWR**:
   - Pros: Caching, automatic refetching, optimistic updates
   - Cons: External dependency, learning curve, Phase II doesn't require caching
   - Rejected: Phase II scope doesn't justify caching complexity

**Implementation Impact**:
- Zero external HTTP library dependencies
- Custom wrapper centralizes error handling and authentication
- Easy to add caching layer in Phase III if needed

---

## Decision 9: CSS/Styling Approach

**Decision**: Tailwind CSS for utility-first styling

**Rationale**:
- **Rapid Development**: Utility classes speed up UI development
- **Responsive Design**: Built-in responsive breakpoints for mobile/desktop
- **Consistent Design**: Design tokens ensure visual consistency
- **Small Bundle**: PurgeCSS removes unused styles in production
- **No CSS Files**: Styles colocated with components (no separate CSS files to manage)
- **Phase II Requirements**: Spec requires responsive UI for desktop + mobile

**Responsive Strategy**:
- Mobile-first approach (base styles for mobile, breakpoints for desktop)
- Tailwind breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Touch-friendly button sizes (minimum 44x44px tap targets)
- Readable font sizes on all devices

**Alternatives Considered**:
1. **CSS Modules**:
   - Pros: Traditional CSS, no learning curve
   - Cons: More verbose, separate files, manual responsive breakpoints
   - Rejected: Tailwind faster for rapid UI development

2. **Styled Components / Emotion**:
   - Pros: CSS-in-JS, dynamic styling
   - Cons: Runtime overhead, larger bundle, overkill for Phase II
   - Rejected: Tailwind sufficient, no need for dynamic styling

**Implementation Impact**:
- Rapid UI development with utility classes
- Automatic responsive design with Tailwind breakpoints
- Small production bundle with unused style purging

---

## Decision 10: Testing Frameworks

**Decision**:
- **Backend**: pytest for unit and integration tests
- **Frontend**: Jest + React Testing Library for component and integration tests

**Rationale - Backend (pytest)**:
- **Python Standard**: Most popular Python testing framework
- **Fixtures**: Powerful fixture system for test setup/teardown
- **FastAPI Integration**: FastAPI provides test client for integration tests
- **Phase II Requirements**: RULE QP-012 requires unit tests for business logic

**Rationale - Frontend (Jest + RTL)**:
- **React Standard**: Jest + React Testing Library is industry standard for React apps
- **User-Centric**: RTL focuses on testing component behavior from user perspective
- **Next.js Integration**: Next.js has built-in Jest configuration
- **Assertions**: Rich assertion library and mocking capabilities

**Testing Strategy**:
- **Backend Unit Tests**: Service layer logic (todo CRUD, authorization)
- **Backend Integration Tests**: API endpoints with test database
- **Frontend Component Tests**: Individual component rendering and interactions
- **Frontend Integration Tests**: Full authentication and todo management flows

**Alternatives Considered**:
1. **Backend - unittest**:
   - Pros: Built into Python standard library
   - Cons: More verbose, less feature-rich than pytest
   - Rejected: pytest is more powerful and easier to use

2. **Frontend - Cypress**:
   - Pros: End-to-end testing, real browser
   - Cons: Slower, more complex setup, overkill for Phase II
   - Rejected: Jest + RTL sufficient for Phase II component testing

**Implementation Impact**:
- pytest fixtures for test database setup/teardown
- FastAPI test client for integration testing API endpoints
- React Testing Library ensures accessibility-focused tests

---

## Summary of Key Technologies

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| Backend Framework | FastAPI | Latest | Auto documentation, type safety, modern Python |
| Backend ORM | SQLModel | Latest | Unified models, type safety, SQLAlchemy power |
| Backend Database | Neon PostgreSQL | Cloud | Serverless, managed, Phase II requirement |
| Backend Auth | Better Auth SDK | Latest | Managed auth, Phase II requirement |
| Backend Testing | pytest | Latest | Python standard, fixture system |
| Frontend Framework | Next.js | 14+ | App Router, SSR, TypeScript support |
| Frontend Language | TypeScript | Latest | Type safety, better IDE support |
| Frontend Auth | Better Auth Client | Latest | Session management, React SDK |
| Frontend Styling | Tailwind CSS | Latest | Utility-first, responsive, rapid development |
| Frontend State | React Context + Hooks | Built-in | Sufficient for Phase II, no external deps |
| Frontend HTTP | Fetch API | Built-in | No external dep, sufficient features |
| Frontend Testing | Jest + RTL | Latest | React standard, user-centric testing |

---

## Risk Assessment

### Low Risk Decisions
- FastAPI, Next.js, PostgreSQL: Well-established technologies with large communities
- SQLModel: Built on SQLAlchemy, maintains compatibility path
- Tailwind CSS: Popular, well-documented, easy to replace if needed

### Medium Risk Decisions
- Better Auth: Managed service dependency, potential vendor lock-in
  - Mitigation: Better Auth provides standard authentication patterns, relatively easy to replace
- App Router: Newer Next.js pattern, less community knowledge than Pages Router
  - Mitigation: Official Next.js recommendation, documentation is comprehensive

### High Risk Decisions
- None identified for Phase II scope

---

## Phase II Compliance Check

All technology decisions comply with Phase II constitutional constraints:

✓ No Docker/Kubernetes (using standard hosting platforms)
✓ No background jobs or async workers (synchronous request/response only)
✓ No real-time features (no WebSockets, no Socket.io)
✓ No message queues or event streaming (no Kafka, no RabbitMQ)
✓ No AI or agent frameworks (no OpenAI SDK, no LangChain)
✓ No microservices architecture (single backend API, single frontend app)
✓ Only Phase II approved technologies (FastAPI, Neon, Next.js, Better Auth)

---

## Next Steps

1. ✓ Research complete - all technology decisions documented and justified
2. Next: Generate data-model.md with detailed database schema
3. Next: Generate contracts/openapi.yaml with complete API specification
4. Next: Generate quickstart.md with development setup instructions
