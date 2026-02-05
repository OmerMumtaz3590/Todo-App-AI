# Phase II Setup Instructions

## Prerequisites Completed
- ✅ Backend project initialized with Python virtual environment
- ✅ Frontend project initialized with Next.js and TypeScript
- ✅ Database models created (User, Todo)
- ✅ Alembic migrations configured
- ✅ Git for development (Windows users: install Git for Windows so bash is available, or set `CLAUDE_CODE_GIT_BASH_PATH` to the path of `bash.exe`)

> 💡 Tip: If `claude` or other tools that require bash are failing on Windows, install Git for Windows from https://git-scm.com/downloads and then either ensure `git`/`bash` are on your PATH or set `CLAUDE_CODE_GIT_BASH_PATH` to the installed `bash.exe` and restart VS Code.

## Manual Setup Required

### 1. Neon PostgreSQL Database

**Create Neon Database:**
1. Go to https://neon.tech and sign up/sign in
2. Create a new project (free tier is sufficient)
3. Copy the connection string (format: `postgresql://user:pass@host/db?sslmode=require`)

**Update Backend Configuration:**
```bash
cd backend
# Edit .env file
DATABASE_URL=<your-neon-connection-string>
SECRET_KEY=<generate-a-32-char-secret-key>
```

**Run Database Migrations:**
```bash
cd backend
./venv/Scripts/alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create users and todos tables
```

**Verify Tables Created:**
- Log in to Neon console
- Check that `users` and `todos` tables exist
- Verify indexes and foreign key constraints

### 2. Start Backend Server

```bash
cd backend
./venv/Scripts/uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend should be accessible at: http://localhost:8000
API docs at: http://localhost:8000/docs

### 3. Start Frontend Server

```bash
cd frontend
npm run dev
```

Frontend should be accessible at: http://localhost:3000

## Current Status

### ✅ Completed Tasks (11/52):
- **Phase 1 Complete**: Project setup (T001-T004)
- **Phase 2 Partial**: Models and migrations (T005-T008)

### 🔄 Needs Manual Completion:
- **T009**: Apply database migrations (requires Neon connection string)

### 📋 Remaining Tasks (41/52):
- **T010-T011**: Authentication infrastructure (Auth service, middleware)
- **Phase 3**: User Story 1 - Authentication (T012-T019)
- **Phase 4**: User Story 2 - View Todos (T020-T023)
- **Phase 5**: User Story 3 - Create Todo (T024-T027)
- **Phase 6**: User Story 4 - Edit Todo (T028-T031)
- **Phase 7**: User Story 5 - Delete Todo (T032-T035)
- **Phase 8**: User Story 6 - Toggle Completion (T036-T039)
- **Phase 9**: Polish & Cross-Cutting (T040-T052)

## Files Created

### Backend (18 files):
1. `requirements.txt` - Python dependencies
2. `src/config.py` - Configuration management
3. `src/database.py` - Database connection
4. `src/main.py` - FastAPI application
5. `src/models/user.py` - User model
6. `src/models/todo.py` - Todo model
7. `src/models/__init__.py` - Models package
8. `.env.example` - Environment template
9. `.env` - Development configuration
10. `alembic.ini` - Migration config
11. `alembic/env.py` - Alembic environment (updated)
12. `alembic/versions/001_create_users_and_todos_tables.py` - Initial migration
13. `pytest.ini` - Test configuration
14. `.gitignore` - Python ignore patterns

### Frontend (12 files):
1. `package.json` - Node dependencies
2. `tsconfig.json` - TypeScript configuration
3. `next.config.js` - Next.js configuration
4. `tailwind.config.ts` - Tailwind CSS config
5. `postcss.config.js` - PostCSS config
6. `app/layout.tsx` - Root layout
7. `app/globals.css` - Global styles
8. `app/page.tsx` - Home page
9. `lib/api.ts` - API communication utility
10. `types/api.ts` - API TypeScript types
11. `.env.local.example` - Environment template
12. `.env.local` - Development configuration
13. `.gitignore` - Node ignore patterns

### Root (1 file):
1. `.gitignore` - Project-wide ignore patterns

## Next Steps

After completing the manual setup above, continue implementation with:

1. **T010**: Integrate Better Auth SDK
2. **T011**: Create authentication middleware
3. **Phase 3**: Implement authentication endpoints and pages

All remaining tasks are documented in `specs/002-fullstack-web-app/tasks.md` with detailed acceptance criteria and references.

## Architecture Overview

**Backend Stack:**
- FastAPI (web framework)
- SQLModel (ORM)
- Neon PostgreSQL (database)
- Alembic (migrations)
- Pydantic (validation)
- PassLib + python-jose (authentication)

**Frontend Stack:**
- Next.js 15 (React framework)
- TypeScript (type safety)
- Tailwind CSS (styling)
- Fetch API (HTTP client)

**Authentication:**
- JWT tokens (via python-jose)
- Password hashing (bcrypt via passlib)
- HTTP-only cookies for session management

## Troubleshooting

### Git Bash or WSL Bash for Claude Code (Windows)
- If you use Claude Code on Windows and Git Bash isn't in PATH, set the environment variable `CLAUDE_CODE_GIT_BASH_PATH` to the full path of `bash.exe` (commonly `C:\Program Files\Git\bin\bash.exe`) so tools that require bash can find it.
- Installing Git for Windows requires administrator privileges; if you don't have admin rights, you can use WSL's bash (`C:\Windows\System32\bash.exe`) as an alternative in many cases.
- For a permanent user-level setting run in PowerShell (example using WSL bash):
```powershell
[Environment]::SetEnvironmentVariable('CLAUDE_CODE_GIT_BASH_PATH','C:\Windows\System32\bash.exe','User')
```
- To set it for VS Code workspace, add to `.vscode/settings.json`:
```json
{
  "terminal.integrated.env.windows": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Windows\\System32\\bash.exe"
  }
}
```
- Restart VS Code after making changes. If Claude still fails to start, install Git for Windows (requires admin) from https://git-scm.com/downloads and update `CLAUDE_CODE_GIT_BASH_PATH` accordingly.

### Backend won't start
- Check `DATABASE_URL` is set in `.env`
- Check `SECRET_KEY` is set (min 32 characters)
- Verify virtual environment is activated
- Check all dependencies installed: `pip list`

### Frontend won't start
- Check `node_modules` exists: `npm install`
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Check Node.js version: `node --version` (should be 18+)

### Database migration fails
- Verify Neon connection string format
- Check database exists in Neon console
- Ensure SSL mode is enabled: `?sslmode=require`
- Test connection: `./venv/Scripts/alembic current`

## Documentation References

- **Specification**: `specs/002-fullstack-web-app/spec.md`
- **Plan**: `specs/002-fullstack-web-app/plan.md`
- **Data Model**: `specs/002-fullstack-web-app/data-model.md`
- **API Contracts**: `specs/002-fullstack-web-app/contracts/openapi.yaml`
- **Tasks**: `specs/002-fullstack-web-app/tasks.md`
- **Quickstart**: `specs/002-fullstack-web-app/quickstart.md`
