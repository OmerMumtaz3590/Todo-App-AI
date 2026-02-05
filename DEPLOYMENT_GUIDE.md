# Deployment Guide for Todo Application

## Overview

This guide provides step-by-step instructions for deploying the full-stack todo application to production using Vercel for the frontend and a cloud provider for the backend.

## Prerequisites

1. **Vercel Account**: For frontend deployment
2. **Neon PostgreSQL**: Database already configured
3. **Backend Hosting**: Options include:
   - Vercel Serverless Functions
   - Railway.app
   - Render.com
   - AWS/Azure/GCP

## Deployment Options

### Option 1: Full Vercel Deployment (Recommended)

Deploy both frontend and backend to Vercel using serverless functions.

#### Step 1: Configure Environment Variables

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=https://your-backend-url.vercel.app
```

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
SECRET_KEY=your-32-character-secret-key
DEBUG=False
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

#### Step 2: Update Vercel Configuration

Create `vercel.json` in the root directory:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/next"
    },
    {
      "src": "backend/src/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "backend/src/main.py"
    },
    {
      "src": "/(.*)",
      "dest": "frontend"
    }
  ]
}
```

#### Step 3: Install Vercel CLI and Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel
```

### Option 2: Separate Frontend/Backend Deployment

#### Frontend Deployment to Vercel

1. **Install dependencies**:
```bash
cd frontend
npm install
```

2. **Configure environment**:
```bash
# Create .env.local
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

3. **Deploy**:
```bash
vercel
```

#### Backend Deployment Options

**Option A: Railway.app**

1. Create new project on Railway.app
2. Connect GitHub repository
3. Set environment variables:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `SECRET_KEY`: 32+ character secret key
   - `DEBUG`: `False`
   - `CORS_ORIGINS`: `https://your-frontend-url.vercel.app`

**Option B: Render.com**

1. Create new Web Service
2. Connect repository
3. Set build command: `pip install -r requirements.txt && alembic upgrade head`
4. Set start command: `uvicorn src.main:app --host 0.0.0.0 --port 8000`
5. Add environment variables

## Production Configuration

### Backend Configuration Updates

Update `backend/src/config.py`:
```python
class Settings(BaseSettings):
    # Update CORS for production
    cors_origins: list[str] = ["https://your-frontend-url.vercel.app"]

    # Production settings
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
```

### Database Migration

Run migrations before deployment:
```bash
cd backend
alembic upgrade head
```

## Monitoring and Maintenance

### Health Checks

- Frontend: `https://your-frontend-url.vercel.app`
- Backend: `https://your-backend-url.com/health`
- API Docs: `https://your-backend-url.com/docs`

### Logging

Configure logging in `backend/src/main.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure `CORS_ORIGINS` includes your frontend URL
2. **Database Connection**: Verify Neon connection string format
3. **Environment Variables**: Check all required variables are set
4. **Migration Issues**: Run `alembic upgrade head` before deployment

### Debugging

Check logs on your hosting provider's dashboard or use:
```bash
# For local testing
uvicorn src.main:app --reload --log-level debug
```

## Rollback Procedure

1. Revert to previous Git commit
2. Redeploy using Vercel dashboard
3. Check database integrity
4. Monitor application logs

## Next Steps

1. ✅ Configure environment variables
2. ✅ Update deployment configuration
3. ⏳ Test deployment locally
4. ⏳ Deploy to production
5. ⏳ Verify all functionality

**Note**: The current project has basic Vercel configuration but needs backend deployment setup and production environment configuration.