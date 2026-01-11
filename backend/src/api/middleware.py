"""FastAPI middleware and dependencies for authentication."""
from typing import Optional

from fastapi import Cookie, Depends, HTTPException, status
from sqlmodel import Session

from ..database import get_session
from ..models.user import User
from ..services.auth_service import AuthService


async def get_current_user(
    session: Session = Depends(get_session),
    access_token: Optional[str] = Cookie(None, alias="access_token")
) -> User:
    """
    FastAPI dependency to get the current authenticated user.

    Extracts JWT token from HTTP-only cookie and validates it.

    Args:
        session: Database session (injected)
        access_token: JWT token from cookie (injected)

    Returns:
        Authenticated user

    Raises:
        HTTPException: 401 if not authenticated or invalid token
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = AuthService.get_current_user(session, access_token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    session: Session = Depends(get_session),
    access_token: Optional[str] = Cookie(None, alias="access_token")
) -> Optional[User]:
    """
    FastAPI dependency to get the current user (optional).

    Returns None if not authenticated, instead of raising an exception.

    Args:
        session: Database session (injected)
        access_token: JWT token from cookie (injected)

    Returns:
        Authenticated user or None
    """
    if not access_token:
        return None

    user = AuthService.get_current_user(session, access_token)

    return user
