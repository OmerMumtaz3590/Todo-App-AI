# Evolution of Todo - Phase II: Full-Stack Web Application

A full-stack todo application built with FastAPI (Python) and Next.js (TypeScript), featuring user authentication and complete CRUD operations.

## 🎯 Features

### Authentication
- ✅ User registration with email/password
- ✅ Secure login with JWT tokens
- ✅ HTTP-only cookie sessions
- ✅ Password hashing with bcrypt

### Todo Management
- ✅ Create todos with title and description
- ✅ View all your todos
- ✅ Edit existing todos (inline editing)
- ✅ Delete todos (with confirmation)
- ✅ Toggle completion status
- ✅ User-specific data isolation

### UI/UX
- ✅ Responsive design (mobile-friendly)
- ✅ Real-time form validation
- ✅ Loading states and error handling
- ✅ Empty state messages
- ✅ Character counters

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - SQL databases with Python type hints
- **PostgreSQL** - Production database (via Neon)
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **PassLib** - Password hashing (bcrypt)
- **python-jose** - JWT token handling

### Frontend
- **Next.js 15** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling

### Database
- **Neon PostgreSQL** - Serverless PostgreSQL database

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Neon account (for PostgreSQL database)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd todo-app
```

### 2. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install
```

### 4. Configure Environment Variables

**Backend** (`backend/.env`):
```env
# Database
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Security
SECRET_KEY=your-secret-key-here-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# App
APP_NAME=Todo API
DEBUG=False

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Server
HOST=0.0.0.0
PORT=8000
```

**Frontend** (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Setup Database

**Create Neon Database:**
1. Go to https://console.neon.tech/
2. Create a new project
3. Copy the connection string
4. Update `DATABASE_URL` in `backend/.env`

**Run Migrations:**
```bash
cd backend
alembic upgrade head
```

### 6. Start Development Servers

**Backend** (Terminal 1):
```bash
cd backend
uvicorn src.main:app --reload
```
Backend will run on http://localhost:8000

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```
Frontend will run on http://localhost:3000

### 7. Access Application

Open http://localhost:3000 in your browser:
1. Click "Sign Up" to create an account
2. Sign in with your credentials
3. Start managing your todos!

## 📁 Project Structure

```
todo-app/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── todos.py         # Todo CRUD endpoints
│   │   │   └── middleware.py    # Auth middleware
│   │   ├── models/
│   │   │   ├── user.py          # User data model
│   │   │   └── todo.py          # Todo data model
│   │   ├── services/
│   │   │   ├── auth_service.py  # Auth business logic
│   │   │   └── todo_service.py  # Todo business logic
│   │   ├── schemas/
│   │   │   ├── auth_schemas.py  # Auth API schemas
│   │   │   └── todo_schemas.py  # Todo API schemas
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database connection
│   │   └── main.py              # FastAPI application
│   ├── alembic/                 # Database migrations
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
│
├── frontend/
│   ├── app/
│   │   ├── auth/
│   │   │   ├── signup/
│   │   │   │   └── page.tsx     # Signup page
│   │   │   └── signin/
│   │   │       └── page.tsx     # Signin page
│   │   ├── todos/
│   │   │   └── page.tsx         # Todo management page
│   │   ├── layout.tsx           # Root layout
│   │   └── page.tsx             # Home page
│   ├── services/
│   │   ├── authService.ts       # Auth API calls
│   │   └── todoService.ts       # Todo API calls
│   ├── types/
│   │   ├── auth.ts              # Auth type definitions
│   │   └── todo.ts              # Todo type definitions
│   ├── lib/
│   │   └── api.ts               # API utility wrapper
│   ├── package.json             # Node dependencies
│   └── .env.local               # Environment variables
│
├── specs/                       # Feature specifications
├── IMPLEMENTATION_STATUS.md     # Progress tracking
└── README.md                    # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Login and get session cookie
- `POST /auth/signout` - Logout and clear session

### Todos
- `GET /todos` - List all todos (requires auth)
- `POST /todos` - Create new todo (requires auth)
- `PUT /todos/{id}` - Update todo (requires auth)
- `PATCH /todos/{id}/toggle` - Toggle completion (requires auth)
- `DELETE /todos/{id}` - Delete todo (requires auth)

### Health Check
- `GET /` - API status
- `GET /health` - Health check

## 🧪 Testing

### Manual Testing Flow

1. **Signup Flow:**
   - Navigate to http://localhost:3000
   - Click "Sign Up"
   - Enter email and password (min 8 characters)
   - Verify redirect to signin page with success message

2. **Signin Flow:**
   - Enter credentials on signin page
   - Verify redirect to /todos page
   - Check that session persists on page reload

3. **Todo CRUD:**
   - **Create**: Click "Add Todo", fill form, submit
   - **View**: Verify todo appears in list
   - **Edit**: Click "Edit", modify fields, save
   - **Toggle**: Click checkbox to mark complete/incomplete
   - **Delete**: Click "Delete", confirm dialog

4. **Signout:**
   - Click "Sign Out" button
   - Verify redirect to signin page
   - Verify cannot access /todos without authentication

### Run Backend Tests (when implemented)

```bash
cd backend
pytest
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt rounds
- **JWT Tokens**: Secure session management
- **HTTP-Only Cookies**: XSS protection
- **CORS Configuration**: Restricted origins
- **Input Validation**: Server-side and client-side
- **User Isolation**: All queries filtered by user_id
- **SQL Injection Protection**: SQLModel ORM with parameterized queries

## 🐛 Troubleshooting

### Database Connection Issues

**Error**: `connection to server failed`
- Verify Neon database is running
- Check `DATABASE_URL` in `backend/.env`
- Ensure `?sslmode=require` is in connection string

### Migration Errors

**Error**: `Can't locate revision identified by 'xyz'`
```bash
cd backend
alembic stamp head
alembic upgrade head
```

### Frontend API Connection

**Error**: `Failed to fetch` or CORS errors
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `frontend/.env.local`
- Verify CORS_ORIGINS in `backend/.env` includes frontend URL

### Authentication Issues

**Error**: Session not persisting
- Check browser allows cookies from localhost
- Verify `access_token` cookie is set (DevTools → Application → Cookies)
- Ensure backend and frontend are on correct ports

## 📈 Performance Considerations

- Database connection pooling (pool_size=5, max_overflow=10)
- Indexed foreign keys for fast queries
- `updated_at` trigger for automatic timestamps
- React state management for optimistic UI updates

## 🚢 Deployment

### Backend (Railway/Render)

1. Connect repository to hosting platform
2. Set environment variables
3. Deploy with build command: `pip install -r requirements.txt`
4. Start command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`

### Frontend (Vercel)

1. Connect repository to Vercel
2. Set `NEXT_PUBLIC_API_URL` to production backend URL
3. Deploy with automatic build detection

### Database

- Already using Neon (serverless PostgreSQL)
- Update `DATABASE_URL` to production connection string
- Run migrations on production database

## 📝 License

This project is part of the "Evolution of Todo" learning series.

## 🤝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon Documentation](https://neon.tech/docs/introduction)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)

## ✨ Features Coming in Phase III

- AI-powered task suggestions
- Smart scheduling and reminders
- Analytics and insights
- Real-time collaboration
- Voice input

---

**Status**: ✅ Fully functional MVP with 75% task completion
**Last Updated**: 2026-01-03
